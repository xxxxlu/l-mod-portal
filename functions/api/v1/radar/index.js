/**
 * Cloudflare Pages Function: /api/v1/radar
 * Steam Patch Radar games compatibility matrix
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const statusFilter = url.searchParams.get('status');

  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    let sql = `
      SELECT id, rank, title, title_zh, steam_app_id, verified_patch, latest_steam_patch,
             compatibility_status, radar_risk_title, radar_risk_desc, radar_summary, pitfall_note
      FROM games
      WHERE steam_app_id IS NOT NULL
    `;
    const params = [];

    if (statusFilter && ['green', 'yellow', 'red'].includes(statusFilter)) {
      sql += ' AND compatibility_status = ?';
      params.push(statusFilter);
    }

    sql += ' ORDER BY rank ASC';

    const { results } = params.length > 0 ? await db.prepare(sql).bind(...params).all() : await db.prepare(sql).all();

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        filter: statusFilter || 'all',
        total: (results || []).length,
        items: results || []
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=60, s-maxage=300'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to retrieve radar games',
      details: err.message
    }), { status: 500 });
  }
}
