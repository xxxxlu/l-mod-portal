/**
 * Cloudflare Pages Function: GET /api/v1/catalog
 * 游戏目录（列表视图用的轻字段），数据真源是 D1 games.raw_json。
 *
 * - 每款 = 整份游戏数据去掉 LIST_OMITTED_FIELDS（指令分类、Mod、修改器详情、说明、.bat …），
 *   字段名和 public/data.js 的 GAMES_DATA 一样；另加 commandCount / modCount 两个统计。
 * - 雷达字段叠加 public/radar_status.json，hasTrainer 叠加 public/trainers.json（见 ./_game_doc.js）。
 * - 隐藏的游戏（games.is_hidden = 1）不出现。
 * - 缓存：ETag = 目录版本号（后台每次保存 +1）+ 两份机器数据的时间；浏览器每次带 If-None-Match 来问，
 *   没变就回 304；变了重算，结果在边缘按 ETag 缓存约 60 秒。
 * - 跨域：公开 GET，Access-Control-Allow-Origin: *（GitHub Pages 站点从 https://xxxxlu.github.io 来读）。
 */

import { loadRadarStatus } from '../../_radar_status.js';
import {
  LIST_OMITTED_FIELDS, PUBLIC_CORS_HEADERS, cachedBody, catalogEtag, etagMatches, jsonResponse,
  loadTrainers, overlayMachineFields, readCatalogVersion
} from './_game_doc.js';

const REMOVE_PATHS = LIST_OMITTED_FIELDS.map(f => `'$.${f}'`).join(', ');

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return jsonResponse({ code: 50300, message: 'Database binding missing' }, 503,
      { ...PUBLIC_CORS_HEADERS, 'Cache-Control': 'no-store' });
  }

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

    const body = await cachedBody(`list:${etag}`, async () => {
      // json_remove 在 D1 里做，Function 只解析剩下的轻字段（免费版每次请求 CPU 只有 10ms）
      const { results } = await db.prepare(
        `SELECT json_remove(raw_json, ${REMOVE_PATHS}) AS doc,
                json_array_length(raw_json, '$.curatedMods') AS mod_count,
                (SELECT COALESCE(SUM(json_array_length(c.value, '$.commands')), 0)
                   FROM json_each(raw_json, '$.consoleCategories') AS c) AS command_count
           FROM games
          WHERE is_hidden = 0 AND raw_json IS NOT NULL
          ORDER BY rank ASC, id ASC`
      ).all();
      const games = (results || []).map(row => {
        const game = overlayMachineFields(JSON.parse(row.doc), radarStatus, trainers, { light: true });
        game.commandCount = row.command_count || 0;
        game.modCount = row.mod_count || 0;
        return game;
      });
      return JSON.stringify({
        code: 0,
        message: 'success',
        data: {
          version,
          radar_updated_at: radarStatus ? radarStatus.updatedAt : null,
          trainers_generated_at: trainers ? trainers.generatedAt : null,
          omitted_fields: LIST_OMITTED_FIELDS,
          total: games.length,
          games
        }
      });
    });

    return new Response(body, { headers });
  } catch (err) {
    return jsonResponse({ code: 50000, message: 'Failed to load the game catalog', details: err.message }, 500,
      { ...PUBLIC_CORS_HEADERS, 'Cache-Control': 'no-store' });
  }
}
