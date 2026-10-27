/**
 * Cloudflare Pages Function: /api/v1/games/:id/commands
 * Asynchronous on-demand console commands loader with categorization
 */

export async function onRequestGet(context) {
  const { params, request, env } = context;
  const gameId = params.id;
  const url = new URL(request.url);

  if (!gameId || !/^[a-z0-9-]+$/.test(gameId)) {
    return new Response(JSON.stringify({ code: 40000, message: 'Invalid game ID format' }), { status: 400 });
  }

  const categoryId = url.searchParams.get('category_id');
  const query = url.searchParams.get('q');
  const popularOnly = url.searchParams.get('popular_only') === 'true';

  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    // 1. Get all available categories for this game (for tab rendering)
    const catSql = `
      SELECT DISTINCT category_id, category_name_zh, category_name_en, count(*) as count
      FROM console_commands
      WHERE game_id = ?
      GROUP BY category_id
      ORDER BY count DESC
    `;
    const catResults = await db.prepare(catSql).bind(gameId).all();

    // 2. Build filtered commands query
    let conditions = ['game_id = ?'];
    let sqlParams = [gameId];

    if (categoryId && categoryId !== 'all') {
      conditions.push('category_id = ?');
      sqlParams.push(categoryId);
    }
    if (popularOnly) {
      conditions.push('is_popular = 1');
    }
    if (query) {
      conditions.push('(name_zh LIKE ? OR name_en LIKE ? OR code LIKE ? OR description LIKE ?)');
      const qPattern = `%${query.trim().slice(0, 50)}%`;
      sqlParams.push(qPattern, qPattern, qPattern, qPattern);
    }

    const cmdSql = `
      SELECT id, category_id, category_name_zh, category_name_en,
             name_zh, name_en, code, description, syntax_type, is_popular
      FROM console_commands
      WHERE ${conditions.join(' AND ')}
      ORDER BY is_popular DESC, id ASC
    `;

    const { results } = await db.prepare(cmdSql).bind(...sqlParams).all();

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        game_id: gameId,
        categories: catResults.results || [],
        total: (results || []).length,
        commands: results || []
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=300, s-maxage=86400, stale-while-revalidate=604800'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to fetch console commands',
      details: err.message
    }), { status: 500 });
  }
}
