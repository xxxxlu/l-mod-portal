/**
 * Cloudflare Pages Function: GET /api/v1/admin/games/[id]
 * Game CMS Detail: Complete Game Record + Commands + Scenario Bundles
 */

export async function onRequestGet(context) {
  const { params, env } = context;
  const gameId = params.id;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  if (!gameId) {
    return new Response(JSON.stringify({ code: 40000, message: 'Missing game ID parameter' }), { status: 400 });
  }

  try {
    const game = await db.prepare(
      `SELECT * FROM games WHERE id = ?`
    ).bind(gameId).first();

    if (!game) {
      return new Response(JSON.stringify({ code: 40400, message: `Game '${gameId}' not found in Vault` }), { status: 404 });
    }

    const [commandsRes, bundlesRes, logsRes] = await Promise.all([
      db.prepare(
        `SELECT * FROM console_commands WHERE game_id = ? ORDER BY category_id, is_popular DESC, name_zh ASC`
      ).bind(gameId).all(),
      db.prepare(
        `SELECT * FROM scenario_bundles WHERE game_id = ? ORDER BY id ASC`
      ).bind(gameId).all(),
      db.prepare(
        `SELECT * FROM patch_radar_logs WHERE game_id = ? ORDER BY checked_at DESC LIMIT 5`
      ).bind(gameId).all()
    ]);

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        game,
        commands: commandsRes.results || [],
        bundles: bundlesRes.results || [],
        radar_logs: logsRes.results || []
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
      message: 'Failed to fetch game details',
      details: err.message
    }), { status: 500 });
  }
}
