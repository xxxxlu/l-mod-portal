/**
 * Cloudflare Pages Function: /api/v1/games
 * Lightweight Catalog Pagination with Edge Projection
 *
 * 雷达字段（compatibility_status / radar）来自 public/radar_status.json 的 v2 结果（见 ../../_radar_status.js），
 * 不再输出 D1 的旧雷达列（verified_patch / latest_steam_patch / radar_risk_title 等）。
 * compat_status 过滤：red | yellow | green | unchecked（没有巡检记录的游戏）。
 */

import { loadRadarStatus, radarIdsWithStatus, radarUnavailableResponse, withRadar, RADAR_STATUSES } from '../../_radar_status.js';

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // Pagination parameters validation
  const page = Math.max(parseInt(url.searchParams.get('page') || '1', 10), 1);
  const pageSize = Math.min(Math.max(parseInt(url.searchParams.get('page_size') || '24', 10), 1), 50);
  const offset = (page - 1) * pageSize;

  const genre = url.searchParams.get('genre');
  const compatStatus = url.searchParams.get('compat_status');
  const hasConsole = url.searchParams.get('has_console');
  const hasMods = url.searchParams.get('has_mods');
  const sortBy = url.searchParams.get('sort_by') || 'rank';

  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Database binding missing. Ensure D1 is bound in Pages settings.'
    }), { status: 503 });
  }

  try {
    const radarStatus = await loadRadarStatus(context);

    // Dynamic Parameterized SQL Query（隐藏的游戏不出现，见 database/migration_v5_game_docs.sql）
    const conditions = ['is_hidden = 0'];
    const params = [];

    if (genre && genre !== 'all') {
      conditions.push('genre = ?');
      params.push(genre);
    }
    if (compatStatus && compatStatus !== 'all') {
      if (!RADAR_STATUSES.includes(compatStatus) && compatStatus !== 'unchecked') {
        return new Response(JSON.stringify({
          code: 40000,
          message: 'compat_status must be one of: all, red, yellow, green, unchecked'
        }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }
      if (!radarStatus) return radarUnavailableResponse();
      // 雷达状态不在 D1 里：把符合条件的 id 作为一个 JSON 数组参数传进去（D1 单条语句最多 100 个绑定参数）
      if (compatStatus === 'unchecked') {
        conditions.push('id NOT IN (SELECT value FROM json_each(?))');
        params.push(JSON.stringify(Object.keys(radarStatus.games)));
      } else {
        conditions.push('id IN (SELECT value FROM json_each(?))');
        params.push(JSON.stringify(radarIdsWithStatus(radarStatus, compatStatus)));
      }
    }
    if (hasConsole !== null && hasConsole !== undefined) {
      conditions.push('has_console = ?');
      params.push(hasConsole === 'true' || hasConsole === '1' ? 1 : 0);
    }
    if (hasMods !== null && hasMods !== undefined) {
      conditions.push('has_mods = ?');
      params.push(hasMods === 'true' || hasMods === '1' ? 1 : 0);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    // 1. Get count for pagination
    const countSql = `SELECT COUNT(*) AS total FROM games ${whereClause}`;
    const totalRow = await db.prepare(countSql).bind(...params).first();
    const total = totalRow ? totalRow.total : 0;

    // 2. Projected lightweight fields query
    let orderClause = 'ORDER BY rank ASC';
    if (sortBy === 'release_year') orderClause = 'ORDER BY release_year DESC, rank ASC';
    if (sortBy === 'title') orderClause = 'ORDER BY title ASC';

    const querySql = `
      SELECT id, rank, title, title_zh, titles_json, developer, release_year, 
             genre, steam_rating, steam_app_id, header_image,
             has_console, console_shortcut, has_mods, has_trainer
      FROM games
      ${whereClause}
      ${orderClause}
      LIMIT ? OFFSET ?
    `;

    const queryParams = [...params, pageSize, offset];
    const { results } = await db.prepare(querySql).bind(...queryParams).all();

    // Map titles_json to clean object
    const sanitizedResults = (results || []).map(row => {
      let titles = {};
      try {
        titles = row.titles_json ? JSON.parse(row.titles_json) : {};
      } catch (e) {}
      const { titles_json, ...rest } = row;
      return {
        ...withRadar(rest, radarStatus),
        titles
      };
    });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        items: sanitizedResults
      },
      meta: {
        page,
        page_size: pageSize,
        total,
        has_more: offset + sanitizedResults.length < total,
        radar_source: radarStatus ? 'radar_status.json' : null,
        radar_updated_at: radarStatus ? radarStatus.updatedAt : null
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=60, s-maxage=3600, stale-while-revalidate=86400'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to query games catalog',
      details: err.message
    }), { status: 500 });
  }
}
