/**
 * Cloudflare Pages Function: /api/v1/games/filters
 * Aggregated taxonomy metrics for UI filter tags and badges
 */

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    // 1. Group by Genre
    const genreRows = await db.prepare(
      'SELECT genre, count(*) as count FROM games GROUP BY genre ORDER BY count DESC'
    ).all();

    // 2. Group by Compatibility Status
    const compatRows = await db.prepare(
      'SELECT compatibility_status, count(*) as count FROM games GROUP BY compatibility_status'
    ).all();

    // 3. Flags summary
    const flagRow = await db.prepare(
      'SELECT sum(has_console) as with_console, sum(has_mods) as with_mods, sum(has_trainer) as with_trainer, count(*) as total FROM games'
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
        compat_status: (compatRows.results || []).reduce((acc, cur) => {
          acc[cur.compatibility_status] = cur.count;
          return acc;
        }, { green: 0, yellow: 0, red: 0 }),
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
