/**
 * Cloudflare Pages Function: GET /api/v1/admin/games
 * Game CMS: List 100 Games with Status, Patches, Command Counts & Filters
 *
 * 雷达状态（compatibility_status / latest_steam_patch / radar）和 status 过滤、统计都用 public/radar_status.json
 * 的 v2 结果（见 ../../../_radar_status.js），不再用 D1 的旧雷达列。verified_patch 仍是后台自己的 D1 字段，只在后台显示。
 */

import { loadRadarStatus, radarCounts, radarEntry, radarIdsWithStatus, radarApiObject, RADAR_STATUSES } from '../../../_radar_status.js';

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const url = new URL(request.url);
    const q = url.searchParams.get('q');
    const status = url.searchParams.get('status');

    const conditions = [];
    const params = [];
    const radarStatus = await loadRadarStatus(context);

    if (status && status !== 'all') {
      if (!RADAR_STATUSES.includes(status) && status !== 'unchecked') {
        return new Response(JSON.stringify({ code: 40000, message: 'status must be one of: all, red, yellow, green, unchecked' }), { status: 400 });
      }
      // 雷达状态不在 D1 里：符合条件的 id 以一个 JSON 数组参数传入
      if (status === 'unchecked') {
        conditions.push('g.id NOT IN (SELECT value FROM json_each(?))');
        params.push(JSON.stringify(radarStatus ? Object.keys(radarStatus.games) : []));
      } else {
        conditions.push('g.id IN (SELECT value FROM json_each(?))');
        params.push(JSON.stringify(radarIdsWithStatus(radarStatus, status)));
      }
    }

    if (q && q.trim()) {
      conditions.push('(g.id LIKE ? OR g.title LIKE ? OR g.title_zh LIKE ?)');
      const pattern = `%${q.trim()}%`;
      params.push(pattern, pattern, pattern);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const sql = `
      SELECT g.id, g.rank, g.title, g.title_zh, g.developer, g.release_year,
             g.steam_app_id, g.header_image, g.verified_patch, g.pitfall_note, g.console_shortcut,
             g.updated_at,
             (SELECT count(*) FROM console_commands cc WHERE cc.game_id = g.id) as command_count,
             (SELECT count(*) FROM scenario_bundles sb WHERE sb.game_id = g.id) as bundle_count
      FROM games g
      ${whereClause}
      ORDER BY g.rank ASC
    `;

    const { results } = await db.prepare(sql).bind(...params).all();

    // Radar breakdown (v2)
    const counts = radarCounts(radarStatus);
    const totalRow = await db.prepare('SELECT count(*) AS total FROM games').first();
    const stats = {
      green: counts.green, yellow: counts.yellow, red: counts.red,
      unchecked: Math.max(0, (totalRow?.total || 0) - counts.total),
      total: totalRow?.total || 0
    };

    const games = (results || []).map(g => {
      const entry = radarEntry(radarStatus, g.id);
      return {
        ...g,
        compatibility_status: entry ? entry.compatibilityStatus : null,
        latest_steam_patch: entry ? (entry.latestSteamPatch || null) : null,
        radar: radarApiObject(entry, radarStatus)
      };
    });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        total: games.length,
        status_stats: stats,
        radar_source: radarStatus ? 'radar_status.json' : null,
        radar_updated_at: radarStatus ? radarStatus.updatedAt : null,
        games
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to fetch games CMS list',
      details: err.message
    }), { status: 500 });
  }
}
