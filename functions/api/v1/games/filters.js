/**
 * Cloudflare Pages Function: /api/v1/games/filters
 * Aggregated taxonomy metrics for UI filter tags and badges
 *
 * compat_status 计数来自 public/radar_status.json 的 v2 结果（见 ../../_radar_status.js），不再按 D1 旧雷达列分组；
 * 雷达数据读不到时 compat_status 为 null。
 */

import { loadRadarStatus, radarCounts } from '../../_radar_status.js';

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 503 });
  }

  try {
    // 1. Group by Genre
    const genreRows = await db.prepare(
      'SELECT genre, count(*) as count FROM games WHERE is_hidden = 0 GROUP BY genre ORDER BY count DESC'
    ).all();

    // 2. Radar status counts (v2, from radar_status.json)
    const radarStatus = await loadRadarStatus(context);

    // 3. Flags summary
    const flagRow = await db.prepare(
      'SELECT sum(has_console) as with_console, sum(has_mods) as with_mods, sum(has_trainer) as with_trainer, count(*) as total FROM games WHERE is_hidden = 0'
    ).first();

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        total_games: flagRow?.total || 100,
        flags: {
          with_console: flagRow?.with_console || 0,
          with_mods: flagRow?.with_mods || 0,
          with_trainer: flagRow?.with_trainer || 0
        },
        compat_status: radarStatus ? (() => {
          const c = radarCounts(radarStatus);
          return { green: c.green, yellow: c.yellow, red: c.red, unchecked: Math.max(0, (flagRow?.total || 0) - c.total) };
        })() : null,
        radar_updated_at: radarStatus ? radarStatus.updatedAt : null,
        genres: genreRows.results || []
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to aggregate filters',
      details: err.message
    }), { status: 500 });
  }
}
