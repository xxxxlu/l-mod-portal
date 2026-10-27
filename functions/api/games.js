/**
 * Cloudflare Pages Function: /api/games
 * Global Edge API endpoint for L-MOD Vault Game Database.
 * Runs on Cloudflare's 300+ Edge Data Centers with Anycast routing.
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const gameId = url.searchParams.get('id');
  const query = url.searchParams.get('q');
  const rank = url.searchParams.get('rank');

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'public, max-age=60, s-maxage=3600, stale-while-revalidate=86400'
  };

  try {
    // 1. If Cloudflare D1 Database binding 'DB' is available
    if (env.DB) {
      if (gameId) {
        const { results } = await env.DB.prepare(
          'SELECT * FROM games WHERE id = ?'
        ).bind(gameId).all();

        if (!results || results.length === 0) {
          return new Response(JSON.stringify({ error: 'Game not found', id: gameId }), {
            status: 404,
            headers: corsHeaders
          });
        }

        const game = results[0];
        // Parse JSON fields
        if (game.raw_json) {
          return new Response(game.raw_json, { headers: corsHeaders });
        }
        return new Response(JSON.stringify(game), { headers: corsHeaders });
      }

      // Query list of all games (lightweight projection)
      let sql = 'SELECT id, rank, title, title_zh, developer, release_year, genre, steam_rating, compatibility_status, verified_patch, latest_steam_patch, radar_risk_title FROM games';
      const params = [];

      if (query) {
        sql += ' WHERE title LIKE ? OR title_zh LIKE ? OR developer LIKE ?';
        const qPattern = `%${query}%`;
        params.push(qPattern, qPattern, qPattern);
      }

      sql += ' ORDER BY rank ASC';
      const stmt = env.DB.prepare(sql);
      const { results } = params.length > 0 ? await stmt.bind(...params).all() : await stmt.all();

      return new Response(JSON.stringify({
        source: 'cloudflare_d1_edge',
        total: results.length,
        games: results
      }), { headers: corsHeaders });
    }

    // 2. Fallback Response if DB binding is not yet bound
    return new Response(JSON.stringify({
      status: 'online',
      message: 'Cloudflare Edge API is active. Connect D1 binding "DB" in Cloudflare Pages dashboard to enable live SQL queries.',
      endpoints: ['/api/games', '/api/radar', '/api/feedback']
    }), { headers: corsHeaders });

  } catch (err) {
    return new Response(JSON.stringify({
      error: 'Database Query Failed',
      message: err.message
    }), {
      status: 500,
      headers: corsHeaders
    });
  }
}
