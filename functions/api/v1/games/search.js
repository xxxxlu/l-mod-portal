/**
 * Cloudflare Pages Function: /api/v1/games/search
 * Fast Edge Typeahead & Debounced Search
 */

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
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const qPattern = `%${sanitizedQuery}%`;
    const sql = `
      SELECT id, rank, title, title_zh, developer, genre, compatibility_status, has_console
      FROM games
      WHERE title LIKE ? OR title_zh LIKE ? OR developer LIKE ? OR id LIKE ?
      ORDER BY rank ASC
      LIMIT 8
    `;

    const { results } = await db.prepare(sql).bind(qPattern, qPattern, qPattern, qPattern).all();

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        query: sanitizedQuery,
        total: (results || []).length,
        items: results || []
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
