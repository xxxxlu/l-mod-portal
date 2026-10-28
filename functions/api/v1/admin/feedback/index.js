/**
 * Cloudflare Pages Function: GET /api/v1/admin/feedback
 * Player Bug Reports & Feedback Audit Stream with Registered User Insights
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const url = new URL(request.url);
    const status = url.searchParams.get('status');
    const category = url.searchParams.get('category');
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10));
    const pageSize = Math.min(50, Math.max(5, parseInt(url.searchParams.get('page_size') || '20', 10)));
    const offset = (page - 1) * pageSize;

    const conditions = [];
    const params = [];

    if (status && status !== 'all') {
      conditions.push('cf.status = ?');
      params.push(status);
    }

    if (category && category !== 'all') {
      conditions.push('cf.category = ?');
      params.push(category);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const countRes = await db.prepare(
      `SELECT count(*) as total FROM community_feedback cf ${whereClause}`
    ).bind(...params).first();

    const total = countRes?.total || 0;

    const sql = `
      SELECT cf.id, cf.game_id, cf.category, cf.content, cf.player_nickname,
             cf.player_ip_country, cf.status, cf.created_at, cf.user_id, cf.player_email,
             g.title as game_title, g.title_zh as game_title_zh,
             u.email as verified_email, u.nickname as registered_nickname, u.avatar_url as registered_avatar
      FROM community_feedback cf
      LEFT JOIN games g ON cf.game_id = g.id
      LEFT JOIN users u ON cf.user_id = u.id
      ${whereClause}
      ORDER BY cf.id DESC
      LIMIT ? OFFSET ?
    `;

    const { results } = await db.prepare(sql).bind(...params, pageSize, offset).all();

    // Summary counters
    const statusCounts = await db.prepare(
      `SELECT status, count(*) as count FROM community_feedback GROUP BY status`
    ).all();
    const counts = { pending: 0, verified: 0, resolved: 0 };
    (statusCounts.results || []).forEach(r => { counts[r.status] = r.count; });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        page,
        page_size: pageSize,
        total,
        total_pages: Math.ceil(total / pageSize),
        status_counts: counts,
        items: (results || []).map(r => ({
          ...r,
          is_registered: Boolean(r.user_id || r.verified_email),
          display_email: r.verified_email || r.player_email || null
        }))
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
      message: 'Failed to fetch community feedback',
      details: err.message
    }), { status: 500 });
  }
}
