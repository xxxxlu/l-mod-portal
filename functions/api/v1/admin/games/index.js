/**
 * Cloudflare Pages Function: GET /api/v1/admin/games
 * Game CMS: List 100 Games with Status, Patches, Command Counts & Filters
 */

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

    if (status && status !== 'all') {
      conditions.push('g.compatibility_status = ?');
      params.push(status);
    }

    if (q && q.trim()) {
      conditions.push('(g.id LIKE ? OR g.title LIKE ? OR g.title_zh LIKE ?)');
      const pattern = `%${q.trim()}%`;
      params.push(pattern, pattern, pattern);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const sql = `
      SELECT g.id, g.rank, g.title, g.title_zh, g.developer, g.release_year,
             g.steam_app_id, g.header_image, g.verified_patch, g.latest_steam_patch,
             g.compatibility_status, g.radar_risk_title, g.pitfall_note, g.console_shortcut,
             g.updated_at,
             (SELECT count(*) FROM console_commands cc WHERE cc.game_id = g.id) as command_count,
             (SELECT count(*) FROM scenario_bundles sb WHERE sb.game_id = g.id) as bundle_count
      FROM games g
      ${whereClause}
      ORDER BY g.rank ASC
    `;

    const { results } = await db.prepare(sql).bind(...params).all();

    // Compatibility breakdown
    const statusSummary = await db.prepare(
      'SELECT compatibility_status, count(*) as count FROM games GROUP BY compatibility_status'
    ).all();
    const stats = { green: 0, yellow: 0, red: 0, total: 100 };
    (statusSummary.results || []).forEach(r => {
      if (r.compatibility_status in stats) stats[r.compatibility_status] = r.count;
    });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        total: results ? results.length : 0,
        status_stats: stats,
        games: results || []
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
