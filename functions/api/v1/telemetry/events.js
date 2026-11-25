/**
 * Cloudflare Pages Function: POST /api/v1/telemetry/events
 * Anonymous visitor telemetry ingestion.
 *
 * Privacy: no IP is stored (the country comes from cf-ipcountry). A visitor is a random per-browser
 * session id. The referrer is stored as a host only, the device as mobile / tablet / desktop.
 * `ai_ask` never stores the question, whatever the client sends.
 *
 * Body: one event object or an array of up to 50, as JSON (Content-Type may be text/plain, which is
 * what navigator.sendBeacon and the client's simple-request fetch send).
 * Unknown event types and events without a valid session id are dropped, not stored as 'unknown'.
 *
 * Sampling: system_settings.telemetry_config.sample_rate (0.01–1, default 1 = everything). The decision
 * is per visitor (FNV-1a of the session id, same function as the client), and each stored row keeps the
 * rate it was sampled at so the dashboard can weight counts back up by 1/sample_rate.
 */

const EVENT_TYPES = new Set([
  'page_view',               // catalog / game detail / radar page
  'search_query',            // final query only, <= 100 chars
  'view_game',               // legacy (before v6): game detail opened
  'copy_code',
  'download_bat',
  'trainer_official_click',  // "go to the FLiNG site" link
  'trainer_download',        // installer-package session: download from this site (payload = version)
  'trainer_fallback',        // installer-package session: fell back to the official site (payload = reason)
  'mod_download_click',
  'ai_ask'                   // game id only
]);

const CORS_ORIGINS = [
  'https://xxxxlu.github.io',
  'https://lmod-vault.pages.dev',
  'http://localhost:8788',
  'http://127.0.0.1:8788'
];

const DEVICE_TYPES = new Set(['mobile', 'tablet', 'desktop']);
const UI_LANGS = new Set(['zh-CN', 'zh-TW', 'en', 'ja', 'ko', 'ru', 'de', 'es']);
const BOT_UA = /bot[\/\s;)]|bot$|spider|crawl|headless|lighthouse|slurp|facebookexternalhit/i;
const HOST_RE = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)*$/;
const GAME_ID_RE = /^[A-Za-z0-9][A-Za-z0-9-]{0,63}$/;
const SESSION_RE = /^[A-Za-z0-9_-]{6,64}$/;
const MAX_BODY_BYTES = 32 * 1024;

let configCache = { at: 0, rate: 1 };

export function fnv1a(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
}

async function getSampleRate(db) {
  if (Date.now() - configCache.at < 60 * 1000) return configCache.rate;
  let rate = 1;
  try {
    const row = await db.prepare("SELECT value FROM system_settings WHERE key = 'telemetry_config'").first();
    if (row && row.value) {
      const r = Number(JSON.parse(row.value).sample_rate);
      if (Number.isFinite(r) && r > 0 && r <= 1) rate = Math.max(0.01, r);
    }
  } catch (e) {}
  configCache = { at: Date.now(), rate };
  return rate;
}

function corsHeaders(request) {
  const origin = request.headers.get('Origin');
  const headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'Vary': 'Origin'
  };
  if (origin && (CORS_ORIGINS.includes(origin) || /^https:\/\/[a-z0-9-]+\.lmod-vault\.pages\.dev$/.test(origin))) {
    headers['Access-Control-Allow-Origin'] = origin;
    headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS';
    headers['Access-Control-Allow-Headers'] = 'Content-Type';
  }
  return headers;
}

function reply(request, status, body) {
  return new Response(JSON.stringify(body), { status, headers: corsHeaders(request) });
}

function deviceFromUA(ua) {
  ua = ua || '';
  if (/iPad|Tablet|PlayBook|Silk|Kindle/i.test(ua) || (/Android/i.test(ua) && !/Mobile/i.test(ua))) return 'tablet';
  if (/Mobi|iPhone|iPod|Android|Windows Phone|HarmonyOS/i.test(ua)) return 'mobile';
  return 'desktop';
}

function cleanHost(value) {
  if (!value || typeof value !== 'string') return null;
  const host = value.trim().toLowerCase().slice(0, 100);
  return HOST_RE.test(host) ? host : null;
}

function cleanPath(value) {
  if (!value || typeof value !== 'string') return null;
  let path = value.split('?')[0].trim();          // never keep a query string
  if (!path.startsWith('/')) return null;
  path = path.replace(/[\u0000-\u001f\u007f]/g, '').slice(0, 160);
  return path || null;
}

function cleanText(value, max) {
  if (value === undefined || value === null) return null;
  const text = String(value).replace(/[\u0000-\u001f\u007f]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, max);
  return text || null;
}

export function normalizeEvent(evt, ctx) {
  if (!evt || typeof evt !== 'object') return null;
  const type = typeof evt.event_type === 'string' ? evt.event_type.trim() : '';
  if (!EVENT_TYPES.has(type)) return null;
  const session = typeof evt.session_id === 'string' ? evt.session_id.trim() : '';
  if (!SESSION_RE.test(session)) return null;

  const gameId = typeof evt.game_id === 'string' && GAME_ID_RE.test(evt.game_id.trim()) ? evt.game_id.trim() : null;
  let payload = null;
  if (type === 'search_query') payload = cleanText(evt.target_payload, 100);
  else if (type !== 'ai_ask' && type !== 'page_view') payload = cleanText(evt.target_payload, 255);
  if (type === 'search_query' && !payload) return null;

  let referrer = cleanHost(evt.referrer_host);
  const siteHost = ctx.originHost || cleanHost(evt.site_host) || ctx.requestHost;
  if (referrer && (referrer === siteHost || referrer === ctx.requestHost)) referrer = null;

  return {
    event_type: type,
    game_id: gameId,
    target_payload: payload,
    session_id: session,
    user_id: typeof evt.user_id === 'string' && evt.user_id ? evt.user_id.slice(0, 64) : null,
    page_path: cleanPath(evt.page_path),
    referrer_host: referrer,
    device_type: DEVICE_TYPES.has(evt.device_type) ? evt.device_type : ctx.uaDevice,
    ui_lang: UI_LANGS.has(evt.ui_lang) ? evt.ui_lang : null,
    site_host: siteHost
  };
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  const declared = Number(request.headers.get('content-length') || 0);
  if (declared > MAX_BODY_BYTES) return reply(request, 413, { code: 41300, message: 'Payload too large' });

  let events;
  try {
    const raw = await request.text();
    if (raw.length > MAX_BODY_BYTES) return reply(request, 413, { code: 41300, message: 'Payload too large' });
    const parsed = JSON.parse(raw);
    events = Array.isArray(parsed) ? parsed : [parsed];
  } catch (err) {
    return reply(request, 400, { code: 40000, message: 'Invalid JSON payload' });
  }
  if (events.length === 0 || events.length > 50) {
    return reply(request, 400, { code: 40000, message: 'Batch size must be between 1 and 50' });
  }

  const ua = request.headers.get('user-agent') || '';
  if (BOT_UA.test(ua)) return reply(request, 202, { code: 0, message: 'ignored', accepted: 0, sample_rate: 1 });

  let originHost = null;
  try { originHost = cleanHost(new URL(request.headers.get('Origin') || '').hostname); } catch (e) {}
  const ctx = {
    originHost,
    requestHost: new URL(request.url).hostname,
    uaDevice: deviceFromUA(ua)
  };
  const rows = events.map(e => normalizeEvent(e, ctx)).filter(Boolean);

  const rate = db ? await getSampleRate(db) : 1;
  const kept = rate >= 1 ? rows : rows.filter(r => fnv1a(r.session_id) / 4294967296 < rate);
  const country = request.headers.get('cf-ipcountry') || 'Unknown';

  if (db && kept.length) {
    const statements = kept.map(r => db.prepare(
      `INSERT INTO telemetry_events
         (event_type, game_id, target_payload, session_id, user_id, client_country,
          page_path, referrer_host, device_type, ui_lang, site_host, sample_rate)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    ).bind(
      r.event_type, r.game_id, r.target_payload, r.session_id, r.user_id, country,
      r.page_path, r.referrer_host, r.device_type, r.ui_lang, r.site_host, rate
    ));
    // Before migration v6 the new columns do not exist: fall back to the original columns
    const legacy = () => db.batch(kept.map(r => db.prepare(
      `INSERT INTO telemetry_events (event_type, game_id, target_payload, session_id, user_id, client_country)
       VALUES (?, ?, ?, ?, ?, ?)`
    ).bind(r.event_type, r.game_id, r.target_payload, r.session_id, r.user_id, country)));
    // Write after responding; a failed write only loses analytics
    context.waitUntil(
      db.batch(statements)
        .catch(err => (/no such column/i.test((err && err.message) || '') ? legacy() : null))
        .catch(() => {})
    );
  }

  return reply(request, 202, {
    code: 0,
    message: 'accepted',
    accepted: kept.length,
    dropped: events.length - rows.length,
    sample_rate: rate
  });
}
