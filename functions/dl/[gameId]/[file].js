/**
 * Cloudflare Pages Function: GET | HEAD /dl/:gameId/:fileName
 * Serves the game's active FLiNG trainer package from Workers KV.
 *
 * - The file is stored as KV chunks `<kv_prefix>/<n>`; GET pipes them in order into a FixedLengthStream,
 *   so the response carries an exact Content-Length and no bytes pass through JS (10 ms CPU budget).
 * - HEAD answers from D1 only; the website uses it as an 8-second preflight before starting a download
 *   and falls back to the FLiNG page when it fails.
 * - 404 when the game has no active package or the file name is not the active one (withdrawn/replaced).
 * - No Range support (Accept-Ranges: none): resuming across chunks would need byte skipping in JS.
 */

import { getDb, getKv, corsHeaders, chunkKey, isGameId } from '../../api/v1/trainers/_store.js';

const EXPOSE = 'Content-Length, Content-Disposition, ETag, X-Content-SHA256';

function safeDecode(v) {
  try { return decodeURIComponent(v); } catch (e) { return v; }
}

function contentDisposition(fileName) {
  const ascii = fileName.replace(/[^\x20-\x7e]/g, '_').replace(/["\\]/g, '_');
  return `attachment; filename="${ascii}"; filename*=UTF-8''${encodeURIComponent(fileName)}`;
}

function plain(request, status, message) {
  return new Response(message + '\n', {
    status,
    headers: corsHeaders(request, {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff',
      'Access-Control-Expose-Headers': EXPOSE
    })
  });
}

async function serve(context, headOnly) {
  const { request, env, params } = context;
  const db = getDb(env);
  const kv = getKv(env);
  const gameId = String(params.gameId || '');
  const rawName = String(params.file || '');

  if (!isGameId(gameId) || !rawName) return plain(request, 404, 'Not found');
  if (!db || !kv) return plain(request, 503, 'Trainer storage is not enabled');

  let row;
  try {
    row = await db.prepare(
      `SELECT id, file_name, size, sha256, chunks, kv_prefix
         FROM trainer_packages WHERE game_id = ? AND status = 'active'`
    ).bind(gameId).first();
  } catch (err) {
    return plain(request, /no such table/i.test(err.message) ? 404 : 503, 'Not found');
  }
  if (!row || (rawName !== row.file_name && safeDecode(rawName) !== row.file_name)) {
    return plain(request, 404, 'Not found');
  }

  const size = Number(row.size);
  const headers = corsHeaders(request, {
    'Content-Type': 'application/octet-stream',
    'Content-Length': String(size),
    'Content-Disposition': contentDisposition(row.file_name),
    'X-Content-Type-Options': 'nosniff',
    'Content-Security-Policy': "default-src 'none'; sandbox",
    'Cache-Control': 'no-cache',
    'ETag': `"${row.sha256}"`,
    'X-Content-SHA256': row.sha256,
    'Accept-Ranges': 'none',
    'Access-Control-Expose-Headers': EXPOSE
  });

  if (headOnly) return new Response(null, { status: 200, headers });

  // Open the first chunk before committing to a 200, so a purged/missing file still gets a clean 404.
  const first = await kv.get(chunkKey(row.kv_prefix, 0), { type: 'stream' });
  if (!first) return plain(request, 404, 'Not found');

  const { readable, writable } = new FixedLengthStream(size);
  const chunks = Number(row.chunks) || 1;
  const pump = (async () => {
    try {
      await first.pipeTo(writable, { preventClose: true });
      for (let n = 1; n < chunks; n++) {
        const part = await kv.get(chunkKey(row.kv_prefix, n), { type: 'stream' });
        if (!part) throw new Error(`chunk ${n} missing`);
        await part.pipeTo(writable, { preventClose: true });
      }
      await writable.close();
    } catch (err) {
      try { await writable.abort(err); } catch (e) { /* already errored */ }
    }
  })();
  if (typeof context.waitUntil === 'function') context.waitUntil(pump);

  return new Response(readable, { status: 200, headers });
}

export function onRequestGet(context) {
  return serve(context, false);
}

export function onRequestHead(context) {
  return serve(context, true);
}

export function onRequestOptions(context) {
  return new Response(null, {
    status: 204,
    headers: corsHeaders(context.request, {
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Access-Control-Max-Age': '86400'
    })
  });
}
