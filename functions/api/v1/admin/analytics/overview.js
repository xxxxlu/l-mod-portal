/**
 * Cloudflare Pages Function: GET /api/v1/admin/analytics/overview?range=today|7d|30d
 * Visitor dashboard. Runs the lazy daily roll-up / 90-day purge first (see _rollup.js), then answers
 * from telemetry_daily (completed days) + live raw rows (today). Empty data stays empty: no fallbacks.
 */

import { runMaintenance, buildRange, countSeedRows, readTelemetryConfig } from './_rollup.js';

const RANGES = { today: 1, '7d': 7, '30d': 30 };

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}

function topList(map, limit, keyName = 'key') {
  return Object.entries(map || {})
    .filter(([, v]) => v > 0)
    .sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])))
    .slice(0, limit)
    .map(([k, v]) => ({ [keyName]: k, count: v }));
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  const url = new URL(request.url);
  const rangeKey = RANGES[url.searchParams.get('range')] ? url.searchParams.get('range') : '7d';
  const days = RANGES[rangeKey];

  try {
    let maintenance;
    try {
      maintenance = await runMaintenance(db);
    } catch (err) {
      // The dashboard still answers from raw rows; the footer shows why the roll-up did not run
      maintenance = { error: err.message };
    }

    const [range, seedRows, cfg, usersRow] = await Promise.all([
      buildRange(db, days),
      countSeedRows(db),
      readTelemetryConfig(db),
      db.prepare(
        `SELECT
           (SELECT count(*) FROM users WHERE email IS NOT NULL) AS total_registered,
           (SELECT count(*) FROM users WHERE email IS NOT NULL AND created_at >= ?1) AS today_registered,
           (SELECT count(*) FROM users WHERE email IS NOT NULL AND last_login_at >= ?1) AS today_active,
           (SELECT count(*) FROM users WHERE password_hash IS NOT NULL AND password_hash != '') AS password_set_count,
           (SELECT count(*) FROM email_verification_codes WHERE created_at >= ?1) AS otp_sent_today`
      ).bind(new Date(Date.now() + 8 * 3600000).toISOString().slice(0, 10) + ' 00:00:00')
        .first().catch(() => null)
    ]);

    const t = range.totals;
    const ev = t.event || {};
    const sumMap = (m) => Object.values(m || {}).reduce((a, b) => a + b, 0);

    // Per-game action table (trainer / mod / AI / copy / .bat), with titles from D1 games
    const actionKeys = {
      trainer_official: 'act:trainer_official_click',
      trainer_download: 'act:trainer_download',
      trainer_fallback: 'act:trainer_fallback',
      mod_click: 'act:mod_download_click',
      ai_ask: 'act:ai_ask',
      copy_code: 'act:copy_code',
      download_bat: 'act:download_bat'
    };
    const perGame = {};
    Object.entries(actionKeys).forEach(([field, metric]) => {
      Object.entries(t[metric] || {}).forEach(([gid, v]) => {
        if (!gid) return;
        perGame[gid] = perGame[gid] || { game_id: gid };
        perGame[gid][field] = (perGame[gid][field] || 0) + v;
      });
    });
    Object.entries(t.game || {}).forEach(([gid, v]) => {
      perGame[gid] = perGame[gid] || { game_id: gid };
      perGame[gid].visitors = v;
    });
    const gameRows = Object.values(perGame)
      .map(g => ({ ...g, _score: (g.visitors || 0) * 1000 + Object.keys(actionKeys).reduce((a, k) => a + (g[k] || 0), 0) }))
      .sort((a, b) => b._score - a._score)
      .slice(0, 20);

    const ids = gameRows.map(g => g.game_id);
    const titles = {};
    if (ids.length) {
      const { results } = await db.prepare(
        'SELECT id, title, title_zh FROM games WHERE id IN (SELECT value FROM json_each(?1))'
      ).bind(JSON.stringify(ids)).all().catch(() => ({ results: [] }));
      (results || []).forEach(r => { titles[r.id] = r.title_zh || r.title; });
    }
    gameRows.forEach(g => { delete g._score; g.title = titles[g.game_id] || null; });

    return json({
      code: 0,
      message: 'success',
      data: {
        range: rangeKey,
        days,
        today: range.today,
        start_day: range.start_day,
        timezone: 'UTC+8',
        summary: {
          pv: (t.pv && t.pv['']) || 0,
          uv: range.range_uv,
          uv_exact: range.range_uv_exact,
          visitor_days: (t.uv && t.uv['']) || 0,
          events: (t.events && t.events['']) || 0,
          searches: ev.search_query || 0,
          trainer_official: ev.trainer_official_click || 0,
          trainer_download: ev.trainer_download || 0,
          trainer_fallback: ev.trainer_fallback || 0,
          mod_clicks: ev.mod_download_click || 0,
          ai_ask: ev.ai_ask || 0,
          copy_code: ev.copy_code || 0,
          download_bat: ev.download_bat || 0,
          legacy_view_game: ev.view_game || 0
        },
        event_breakdown: ev,
        trend: range.trend,
        top: {
          referrers: topList(t.referrer, 15, 'host'),
          pages: topList(t.page, 15, 'path'),
          searches: topList(t.search, 20, 'query'),
          countries: topList(t.country, 15, 'country'),
          devices: topList(t.device, 5, 'device'),
          langs: topList(t.lang, 10, 'lang'),
          sites: topList(t.site, 5, 'site'),
          copies: topList(t.copy, 10, 'code'),
          fallback_reasons: topList(t.fallback_reason, 10, 'reason'),
          mod_kinds: topList(t.mod_kind, 5, 'kind')
        },
        games: gameRows,
        dims_total: {
          country: sumMap(t.country), device: sumMap(t.device), lang: sumMap(t.lang), site: sumMap(t.site)
        },
        users_summary: usersRow || null,
        seed_rows_excluded: seedRows,
        sample_rate: cfg.sample_rate,
        retention_days: cfg.retention_days,
        maintenance,
        generated_at: new Date().toISOString()
      }
    });
  } catch (err) {
    return json({ code: 50000, message: 'Failed to aggregate telemetry metrics', details: err.message }, 500);
  }
}
