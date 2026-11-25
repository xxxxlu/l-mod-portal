/**
 * Cloudflare Pages Function: /api/v1/games/search
 * Fast Edge Typeahead & Debounced Search
 *
 * compatibility_status / radar 来自 public/radar_status.json 的 v2 结果（见 ../../_radar_status.js），不读 D1 旧雷达列。
 */

import { loadRadarStatus, radarEntry } from '../../_radar_status.js';

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const q = (url.searchParams.get('q') || '').trim();

  if (!q) {
    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: { items: [] }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }

  // Max query length check
  const sanitizedQuery = q.slice(0, 50);
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 503 });
  }

  try {
    const qPattern = `%${sanitizedQuery}%`;
    const sql = `
      SELECT id, rank, title, title_zh, developer, genre, has_console
      FROM games
      WHERE is_hidden = 0 AND (title LIKE ? OR title_zh LIKE ? OR developer LIKE ? OR id LIKE ?)
      ORDER BY rank ASC
      LIMIT 8
    `;

    const { results } = await db.prepare(sql).bind(qPattern, qPattern, qPattern, qPattern).all();
    const radarStatus = await loadRadarStatus(context);
    // 联想搜索只带轻量的雷达状态；完整雷达信息看 /api/v1/games/:id
    const items = (results || []).map(row => {
      const entry = radarEntry(radarStatus, row.id);
      return {
        ...row,
        compatibility_status: entry ? entry.compatibilityStatus : null,
        radar_status_text: entry ? entry.radarStatusText || null : null
      };
    });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        query: sanitizedQuery,
        total: items.length,
        items
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=30, s-maxage=600'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Search query failed',
      details: err.message
    }), { status: 500 });
  }
}
