/**
 * Cloudflare Pages Function: GET /api/v1/admin/analytics/events
 * Holographic Real-time Telemetry Event Stream with Pagination & Filtering
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const url = new URL(request.url);
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10));
    const pageSize = Math.min(100, Math.max(10, parseInt(url.searchParams.get('page_size') || '30', 10)));
    const eventType = url.searchParams.get('event_type');
    const gameId = url.searchParams.get('game_id');
    const country = url.searchParams.get('country');
    const search = url.searchParams.get('search');

    const offset = (page - 1) * pageSize;
    const conditions = [];
    const params = [];

    if (eventType && eventType !== 'all') {
      conditions.push('event_type = ?');
      params.push(eventType);
    }

    if (gameId && gameId !== 'all') {
      conditions.push('game_id = ?');
      params.push(gameId);
    }

    if (country && country !== 'all') {
      conditions.push('client_country = ?');
      params.push(country);
    }

    if (search && search.trim()) {
      conditions.push('(target_payload LIKE ? OR session_id LIKE ?)');
      const pattern = `%${search.trim()}%`;
      params.push(pattern, pattern);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    // Total count for pagination
    const countSql = `SELECT count(*) as total FROM telemetry_events ${whereClause}`;
    const countRes = await db.prepare(countSql).bind(...params).first();
    const total = countRes?.total || 0;

    // Fetch paginated events
    const querySql = `
      SELECT id, event_type, game_id, target_payload, session_id, user_id, client_country, created_at
      FROM telemetry_events
      ${whereClause}
      ORDER BY id DESC
      LIMIT ? OFFSET ?
    `;
    const { results } = await db.prepare(querySql).bind(...params, pageSize, offset).all();

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        page,
        page_size: pageSize,
        total,
        total_pages: Math.ceil(total / pageSize),
        events: results || []
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
      message: 'Failed to retrieve telemetry events',
      details: err.message
    }), { status: 500 });
  }
}
