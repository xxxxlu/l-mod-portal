/**
 * Cloudflare Pages Function: GET /api/v1/trainers/manifest
 * Active site-hosted FLiNG trainer packages, for the website (both GitHub Pages and CF Pages) and the
 * desktop client. `mirror` matches the client's reserved `trainer.mirror` contract
 * (desktop/contract/types.ts → TrainerMirror: url / fileName / size / sha256; https only).
 *
 * {
 *   "schema": 1,
 *   "generatedAt": "...",
 *   "storage": "kv" | "unavailable",
 *   "games": {
 *     "<gameId>": {
 *       "mirror": { "url": "https://lmod-vault.pages.dev/dl/<gameId>/<file>", "fileName": "...", "size": 123, "sha256": "<64 hex>" },
 *       "version": "...", "gameVersion": "...", "fileName": "...", "uploadedAt": "...Z", "pageUrl": "https://flingtrainer.com/..."
 *     }
 *   }
 * }
 */

import { getDb, getKv, json, corsHeaders, isMissingTable, toIso, downloadPath } from './_store.js';

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = getDb(env);
  const kv = getKv(env);
  const origin = new URL(request.url).origin;

  const body = {
    schema: 1,
    generatedAt: new Date().toISOString(),
    storage: kv ? 'kv' : 'unavailable',
    games: {}
  };
  const okHeaders = corsHeaders(request, { 'Cache-Control': 'public, max-age=60', 'X-Content-Type-Options': 'nosniff' });

  if (!kv || !db) return json(body, 200, okHeaders);

  try {
    const { results } = await db.prepare(
      `SELECT game_id, fling_page_url, trainer_version, game_version, file_name, size, sha256, uploaded_at
         FROM trainer_packages
        WHERE status = 'active'
        ORDER BY game_id`
    ).all();

    for (const r of results || []) {
      body.games[r.game_id] = {
        mirror: {
          url: origin + downloadPath(r.game_id, r.file_name),
          fileName: r.file_name,
          size: Number(r.size),
          sha256: r.sha256
        },
        version: r.trainer_version || null,
        gameVersion: r.game_version || null,
        fileName: r.file_name,
        uploadedAt: toIso(r.uploaded_at),
        pageUrl: r.fling_page_url || null
      };
    }
    return json(body, 200, okHeaders);
  } catch (err) {
    if (isMissingTable(err)) return json(body, 200, okHeaders);
    return json({ ...body, error: 'manifest_unavailable' }, 503, corsHeaders(request, { 'Cache-Control': 'no-store' }));
  }
}
