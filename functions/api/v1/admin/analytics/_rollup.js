/**
 * Visitor analytics: daily roll-up, lazy maintenance and range aggregation (shared by admin/analytics/*).
 *
 * Why lazy: Pages Functions have no cron, so the roll-up runs when the admin opens the dashboard.
 *
 * Maintenance (runMaintenance), every dashboard load:
 *   1. Roll up every *completed* day (UTC+8) that has no row in telemetry_rollup_days yet.
 *      One D1 batch (= one transaction): delete that window's telemetry_daily rows, insert the aggregates,
 *      write one telemetry_rollup_days row per day. A day that is already marked is never recomputed, so
 *      re-running, or two admins loading at once, gives the same rows (idempotent).
 *   2. Purge raw events older than retention_days (default 90), but only days that are already rolled up,
 *      at most PURGE_BATCH rows per load. Once raw rows are gone their day is never rolled again.
 *   Nothing is written when there is nothing to roll or purge (the usual case after the first load of a day).
 *
 * Today is never written to telemetry_daily; it is aggregated live from raw rows (read-only) on each load.
 *
 * telemetry_daily metrics (value is weighted by 1/sample_rate, so sampled data reads as an estimate):
 *   events  ''                       all tracked events
 *   pv      ''                       page_view events
 *   uv      ''                       distinct visitors (session ids) that day
 *   event   <event_type>             events per type
 *   country <cf-ipcountry>           visitors   ┐ "visitors" = distinct sessions per day; summing days
 *   device  mobile|tablet|desktop|'' visitors   │ counts a returning visitor once per day (visitor-days).
 *   lang    zh-CN|en|…|''            visitors   │ '' = not recorded (rows from before migration v6)
 *   site    <host>|''                visitors   │
 *   referrer <host>|(direct)         visitors on page_view, top 50 per day
 *   game    <game_id>                visitors who opened the game page (page_view / legacy view_game), top 100
 *   page    <path, game pages as /#/game/*>   page_view count, top 50
 *   search  <query, lowercased>      count, top 50
 *   act:<event_type> <game_id>|''    per-game counts for trainer/mod/copy/.bat/AI actions
 *   fallback_reason <reason>         trainer_fallback count by reason, top 20
 *   mod_kind direct|page|nexus_page  mod_download_click by kind
 *   copy    <command text>           copy_code count, top 30
 *
 * Seed rows: migration_v3 inserted 36 fake events (session ids 'sess_*', dated 2026-10-27). They are
 * excluded from every aggregate here (SEED_FILTER) and reported separately so the dashboard can say so.
 */

export const TZ_OFFSET_HOURS = 8;              // days are cut at Beijing midnight
export const DEFAULT_RETENTION_DAYS = 90;
const PURGE_BATCH = 5000;
const MAX_EXACT_UV_EVENTS = 500000;            // above this, range UV falls back to summed daily UV

export const TRACKED_EVENTS = [
  'page_view', 'search_query', 'view_game', 'copy_code', 'download_bat',
  'trainer_official_click', 'trainer_download', 'trainer_fallback', 'mod_download_click', 'ai_ask'
];
const ACTION_EVENTS = ['trainer_official_click', 'trainer_download', 'trainer_fallback', 'mod_download_click', 'copy_code', 'download_bat', 'ai_ask'];

const SEED_FILTER = "NOT (substr(session_id, 1, 5) = 'sess_' AND created_at < '2026-10-28')";
const DAY = `date(created_at, '+${TZ_OFFSET_HOURS} hours')`;
const W = '(1.0 / COALESCE(sample_rate, 1))';
const WSUM = `CAST(ROUND(SUM(${W})) AS INTEGER)`;
const IN_LIST = (arr) => arr.map(t => `'${t}'`).join(', ');
const BASE = `created_at >= ?1 AND created_at < ?2 AND event_type IN (${IN_LIST(TRACKED_EVENTS)}) AND ${SEED_FILTER}`;

function topN(metric, dimExpr, valueExpr, where, n) {
  return `SELECT day, '${metric}' AS metric, dim, value FROM (
      SELECT day, dim, value, ROW_NUMBER() OVER (PARTITION BY day ORDER BY value DESC, dim) AS rn FROM (
        SELECT ${DAY} AS day, ${dimExpr} AS dim, ${valueExpr} AS value
        FROM telemetry_events WHERE ${BASE}${where ? ' AND ' + where : ''} GROUP BY 1, 2))
    WHERE rn <= ${n}`;
}

// Distinct visitors, each weighted by 1 / the sample rate it was recorded at (exact count when rate = 1)
function visitors(metric, dimExpr, where, n) {
  const perSession = `SELECT ${DAY} AS day, ${dimExpr} AS dim, session_id, MIN(COALESCE(sample_rate, 1)) AS r
      FROM telemetry_events WHERE ${BASE}${where ? ' AND ' + where : ''} GROUP BY 1, 2, 3`;
  const grouped = `SELECT day, dim, CAST(ROUND(SUM(1.0 / r)) AS INTEGER) AS value FROM (${perSession}) GROUP BY day, dim`;
  if (!n) return `SELECT day, '${metric}' AS metric, dim, value FROM (${grouped})`;
  return `SELECT day, '${metric}' AS metric, dim, value FROM (
      SELECT day, dim, value, ROW_NUMBER() OVER (PARTITION BY day ORDER BY value DESC, dim) AS rn FROM (${grouped}))
    WHERE rn <= ${n}`;
}

function plain(metric, dimExpr, valueExpr, where) {
  return `SELECT ${DAY} AS day, ${metric} AS metric, ${dimExpr} AS dim, ${valueExpr} AS value
    FROM telemetry_events WHERE ${BASE}${where ? ' AND ' + where : ''} GROUP BY 1, 2, 3`;
}

// Statements producing (day, metric, dim, value) for every metric over [?1, ?2).
// D1 allows at most 5 terms in one compound SELECT, so the parts are grouped 4 per statement.
const AGGREGATE_PARTS = [
  plain("'events'", "''", WSUM),
  plain("'pv'", "''", WSUM, "event_type = 'page_view'"),
  visitors('uv', "''"),
  plain("'event'", 'event_type', WSUM),
  visitors('country', "COALESCE(NULLIF(client_country, ''), 'Unknown')"),
  visitors('device', "COALESCE(device_type, '')"),
  visitors('lang', "COALESCE(ui_lang, '')"),
  visitors('site', "COALESCE(site_host, '')"),
  plain("'mod_kind'", "CASE WHEN target_payload = 'nexus_page' THEN 'nexus_page' WHEN target_payload LIKE '%:direct' THEN 'direct' ELSE 'page' END", WSUM, "event_type = 'mod_download_click'"),
  plain("'act:' || event_type", "COALESCE(game_id, '')", WSUM, `event_type IN (${IN_LIST(ACTION_EVENTS)})`),
  visitors('referrer', "COALESCE(referrer_host, '(direct)')", "event_type = 'page_view'", 50),
  visitors('game', 'game_id', "game_id IS NOT NULL AND event_type IN ('page_view', 'view_game')", 100),
  topN('page', "CASE WHEN instr(page_path, '#/game/') > 0 THEN substr(page_path, 1, instr(page_path, '#/game/') - 1) || '#/game/*' ELSE page_path END", WSUM, "event_type = 'page_view' AND page_path IS NOT NULL", 50),
  topN('search', 'lower(target_payload)', WSUM, "event_type = 'search_query' AND target_payload IS NOT NULL", 50),
  topN('fallback_reason', "COALESCE(target_payload, '')", WSUM, "event_type = 'trainer_fallback'", 20),
  topN('copy', 'target_payload', WSUM, "event_type = 'copy_code' AND target_payload IS NOT NULL", 30)
];
export const AGGREGATE_SQLS = [];
for (let i = 0; i < AGGREGATE_PARTS.length; i += 4) {
  AGGREGATE_SQLS.push(AGGREGATE_PARTS.slice(i, i + 4).join('\nUNION ALL\n'));
}

// ---------------------------------------------------------------------------------------------
// Time helpers. D1's CURRENT_TIMESTAMP is UTC text 'YYYY-MM-DD HH:MM:SS'; days are UTC+8.
// ---------------------------------------------------------------------------------------------
const DAY_MS = 86400000;
export function localDay(ms) { return new Date(ms + TZ_OFFSET_HOURS * 3600000).toISOString().slice(0, 10); }
export function dayStartMs(day) { return Date.parse(`${day}T00:00:00Z`) - TZ_OFFSET_HOURS * 3600000; }
export function addDays(day, n) { return new Date(Date.parse(`${day}T00:00:00Z`) + n * DAY_MS).toISOString().slice(0, 10); }
export function sqlTs(ms) { return new Date(ms).toISOString().replace('T', ' ').slice(0, 19); }

export async function readTelemetryConfig(db) {
  const cfg = { sample_rate: 1, retention_days: DEFAULT_RETENTION_DAYS };
  try {
    const row = await db.prepare("SELECT value FROM system_settings WHERE key = 'telemetry_config'").first();
    if (row && row.value) {
      const v = JSON.parse(row.value);
      const r = Number(v.sample_rate);
      if (Number.isFinite(r) && r > 0 && r <= 1) cfg.sample_rate = Math.max(0.01, r);
      const d = parseInt(v.retention_days, 10);
      if (d >= 30 && d <= 400) cfg.retention_days = d;
    }
  } catch (e) {}
  return cfg;
}

/**
 * Roll up completed days and purge expired raw rows. Safe to call on every load.
 * Returns what it did, for the dashboard footer.
 */
export async function runMaintenance(db, nowMs = Date.now()) {
  const cfg = await readTelemetryConfig(db);
  const today = localDay(nowMs);
  const result = { today, rolled_days: [], purged_rows: 0, retention_days: cfg.retention_days, rolled_through: null };

  const state = await db.prepare(
    `SELECT (SELECT MIN(created_at) FROM telemetry_events) AS min_ts,
            (SELECT MAX(day) FROM telemetry_rollup_days) AS last_day`
  ).first();

  // 1. Roll up [first un-rolled day, today)
  let startDay = null;
  if (state && state.last_day) startDay = addDays(state.last_day, 1);
  else if (state && state.min_ts) startDay = localDay(Date.parse(state.min_ts.replace(' ', 'T') + 'Z'));
  if (startDay && startDay < today) {
    const from = sqlTs(dayStartMs(startDay));
    const to = sqlTs(dayStartMs(today));
    const batch = await db.batch([
      db.prepare('DELETE FROM telemetry_daily WHERE day >= ?1 AND day < ?2').bind(startDay, today),
      ...AGGREGATE_SQLS.map(sql => db.prepare(`INSERT INTO telemetry_daily (day, metric, dim, value) ${sql}`).bind(from, to)),
      db.prepare(
        `INSERT OR REPLACE INTO telemetry_rollup_days (day, raw_events)
         SELECT ${DAY} AS day, COUNT(*) FROM telemetry_events
         WHERE created_at >= ?1 AND created_at < ?2 GROUP BY 1`
      ).bind(from, to),
      db.prepare(`SELECT day FROM telemetry_rollup_days WHERE day >= ?1 AND day < ?2 ORDER BY day`).bind(startDay, today)
    ]);
    result.rolled_days = (batch[batch.length - 1].results || []).map(r => r.day);
  }

  // 2. Purge raw rows past retention, only for days already rolled up
  const rolled = await db.prepare('SELECT MAX(day) AS last_day FROM telemetry_rollup_days').first();
  result.rolled_through = rolled ? rolled.last_day : null;
  if (rolled && rolled.last_day && state && state.min_ts) {
    const cutoffDay = addDays(today, -cfg.retention_days);
    const limitDay = cutoffDay <= rolled.last_day ? cutoffDay : addDays(rolled.last_day, 1);
    const cutoffTs = sqlTs(dayStartMs(limitDay));
    if (state.min_ts < cutoffTs) {
      const del = await db.prepare(
        `DELETE FROM telemetry_events WHERE id IN (
           SELECT id FROM telemetry_events WHERE created_at < ?1 ORDER BY created_at LIMIT ${PURGE_BATCH})`
      ).bind(cutoffTs).run();
      result.purged_rows = (del.meta && del.meta.changes) || 0;
    }
  }
  return result;
}

/** Live aggregates for [fromMs, toMs) straight from raw rows (read-only). */
export async function aggregateLive(db, fromMs, toMs) {
  const from = sqlTs(fromMs);
  const to = sqlTs(toMs);
  const out = await db.batch(AGGREGATE_SQLS.map(sql => db.prepare(sql).bind(from, to)));
  return out.flatMap(r => r.results || []);
}

/**
 * Everything the dashboard needs for the last `days` days including today.
 * Completed days come from telemetry_daily, today from raw rows.
 */
export async function buildRange(db, days, nowMs = Date.now()) {
  const today = localDay(nowMs);
  const startDay = addDays(today, -(days - 1));
  const trendStart = addDays(today, -29);

  const [rangeRows, trendRows, live, firstDayRow] = await Promise.all([
    days > 1
      ? db.prepare('SELECT metric, dim, SUM(value) AS value FROM telemetry_daily WHERE day >= ?1 AND day < ?2 GROUP BY metric, dim')
          .bind(startDay, today).all().then(r => r.results || [])
      : Promise.resolve([]),
    db.prepare("SELECT day, metric, value FROM telemetry_daily WHERE metric IN ('pv', 'uv', 'events') AND dim = '' AND day >= ?1 AND day < ?2")
      .bind(trendStart, today).all().then(r => r.results || []),
    aggregateLive(db, dayStartMs(today), nowMs + 1000),
    db.prepare(`SELECT MIN(day) AS first_day FROM telemetry_rollup_days`).first()
  ]);

  // Merge completed days + today into metric -> dim -> value
  const totals = {};
  const add = (metric, dim, value) => {
    totals[metric] = totals[metric] || {};
    totals[metric][dim] = (totals[metric][dim] || 0) + (Number(value) || 0);
  };
  rangeRows.forEach(r => add(r.metric, r.dim, r.value));
  live.forEach(r => add(r.metric, r.dim, r.value));

  // Exact distinct visitors over the range (raw rows cover the last retention_days)
  const eventsInRange = (totals.events && totals.events['']) || 0;
  let rangeUv = null;
  let rangeUvExact = false;
  if (days === 1) {
    rangeUv = (totals.uv && totals.uv['']) || 0;
    rangeUvExact = true;
  } else if (eventsInRange <= MAX_EXACT_UV_EVENTS) {
    const row = await db.prepare(
      `SELECT CAST(ROUND(SUM(1.0 / r)) AS INTEGER) AS uv FROM (
         SELECT session_id, MIN(COALESCE(sample_rate, 1)) AS r FROM telemetry_events WHERE ${BASE} GROUP BY session_id)`
    ).bind(sqlTs(dayStartMs(startDay)), sqlTs(nowMs + 1000)).first();
    rangeUv = (row && row.uv) || 0;
    rangeUvExact = true;
  } else {
    rangeUv = (totals.uv && totals.uv['']) || 0; // visitor-days, an upper bound
  }

  // 30-day trend: only from the first day that has any data, so days before tracking are not shown as zero
  const liveTotals = {};
  live.forEach(r => { if (r.dim === '' && ['pv', 'uv', 'events'].includes(r.metric)) liveTotals[r.metric] = r.value; });
  const byDay = {};
  trendRows.forEach(r => { byDay[r.day] = byDay[r.day] || {}; byDay[r.day][r.metric] = r.value; });
  if (Object.keys(liveTotals).length) byDay[today] = liveTotals;
  const firstDay = [firstDayRow && firstDayRow.first_day, ...Object.keys(byDay)].filter(Boolean).sort()[0] || null;
  const trend = [];
  if (firstDay) {
    for (let d = firstDay < trendStart ? trendStart : firstDay; d <= today; d = addDays(d, 1)) {
      const v = byDay[d] || {};
      trend.push({ day: d, pv: v.pv || 0, uv: v.uv || 0, events: v.events || 0 });
    }
  }

  return { today, start_day: startDay, totals, range_uv: rangeUv, range_uv_exact: rangeUvExact, trend };
}

/** Count of migration_v3 seed rows still in raw storage (excluded from all numbers above). */
export async function countSeedRows(db) {
  try {
    const row = await db.prepare(
      `SELECT COUNT(*) AS n FROM telemetry_events WHERE created_at < '2026-10-28'
         AND (substr(session_id, 1, 5) = 'sess_' OR event_type NOT IN (${IN_LIST(TRACKED_EVENTS)}))`
    ).first();
    return (row && row.n) || 0;
  } catch (e) {
    return 0;
  }
}
