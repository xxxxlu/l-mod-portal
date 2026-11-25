/**
 * Cloudflare Pages Function: GET /api/v1/catalog/:id
 * 一款游戏的整份数据（和 public/data.js GAMES_DATA 里的一项同形），真源是 D1 games.raw_json。
 *
 * 雷达字段叠加 public/radar_status.json，修改器字段叠加 public/trainers.json（见 ./_game_doc.js）；
 * 隐藏的游戏回 404。缓存和跨域同 /api/v1/catalog。
 */

import { loadRadarStatus } from '../../_radar_status.js';
import {
  GAME_ID_RE, PUBLIC_CORS_HEADERS, cachedBody, catalogEtag, etagMatches, jsonResponse,
  loadTrainers, overlayMachineFields, readCatalogVersion
} from './_game_doc.js';

export async function onRequestGet(context) {
  const { request, env, params } = context;
  const gameId = String(params.id || '');
  const errHeaders = { ...PUBLIC_CORS_HEADERS, 'Cache-Control': 'no-store' };

  if (!GAME_ID_RE.test(gameId) || gameId.length > 64) {
    return jsonResponse({ code: 40000, message: 'Invalid game ID format' }, 400, errHeaders);
  }
  const db = env.DB || env.lmod_vault_db;
  if (!db) return jsonResponse({ code: 50300, message: 'Database binding missing' }, 503, errHeaders);

  try {
    const [version, radarStatus, trainers] = await Promise.all([
      readCatalogVersion(db), loadRadarStatus(context), loadTrainers(context)
    ]);
    const etag = catalogEtag(version, radarStatus, trainers);
    const headers = {
      ...PUBLIC_CORS_HEADERS,
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=0, must-revalidate',
      'ETag': etag,
      'X-Catalog-Version': version
    };
    if (etagMatches(request, etag)) return new Response(null, { status: 304, headers });

    const body = await cachedBody(`game:${gameId}:${etag}`, async () => {
      const row = await db.prepare('SELECT raw_json FROM games WHERE id = ? AND is_hidden = 0').bind(gameId).first();
      if (!row || !row.raw_json) return null;
      const game = overlayMachineFields(JSON.parse(row.raw_json), radarStatus, trainers);
      return JSON.stringify({ code: 0, message: 'success', data: { version, game } });
    });
    if (body === null) {
      return jsonResponse({ code: 40401, message: `Game '${gameId}' not found` }, 404, errHeaders);
    }
    return new Response(body, { headers });
  } catch (err) {
    return jsonResponse({ code: 50000, message: 'Failed to load the game', details: err.message }, 500, errHeaders);
  }
}
