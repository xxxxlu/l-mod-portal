/**
 * Cloudflare Pages Function: GET /api/v1/admin/commands
 * Console Commands CMS: Filter commands by game_id or search query
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const url = new URL(request.url);
    const gameId = url.searchParams.get('game_id');
    const search = url.searchParams.get('q');
    const category = url.searchParams.get('category');
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10));
    const pageSize = Math.min(100, Math.max(10, parseInt(url.searchParams.get('page_size') || '50', 10)));
    const offset = (page - 1) * pageSize;

    const conditions = [];
    const params = [];

    if (gameId && gameId !== 'all') {
      conditions.push('cc.game_id = ?');
      params.push(gameId);
    }

    if (category && category !== 'all') {
      conditions.push('cc.category_id = ?');
      params.push(category);
    }

    if (search && search.trim()) {
      conditions.push('(cc.name_zh LIKE ? OR cc.name_en LIKE ? OR cc.code LIKE ? OR cc.description LIKE ?)');
      const pattern = `%${search.trim()}%`;
      params.push(pattern, pattern, pattern, pattern);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const countRes = await db.prepare(
      `SELECT count(*) as total FROM console_commands cc ${whereClause}`
    ).bind(...params).first();
    const total = countRes?.total || 0;

    const sql = `
      SELECT cc.id, cc.game_id, cc.category_id, cc.category_name_zh, cc.category_name_en,
             cc.name_zh, cc.name_en, cc.code, cc.description, cc.syntax_type, cc.is_popular,
             cc.created_at, g.title_zh as game_title_zh, g.title as game_title
      FROM console_commands cc
      LEFT JOIN games g ON cc.game_id = g.id
      ${whereClause}
      ORDER BY cc.game_id ASC, cc.is_popular DESC, cc.name_zh ASC
      LIMIT ? OFFSET ?
    `;

    const { results } = await db.prepare(sql).bind(...params, pageSize, offset).all();

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        page,
        page_size: pageSize,
        total,
        total_pages: Math.ceil(total / pageSize),
        commands: results || []
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
      message: 'Failed to retrieve console commands',
      details: err.message
    }), { status: 500 });
  }
}
