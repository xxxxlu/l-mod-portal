/**
 * Cloudflare Pages Function: /api/v1/games/:id/bundles
 * Retrieve official scenario packages and one-click bat profiles
 */

export async function onRequestGet(context) {
  const { params, env } = context;
  const gameId = params.id;

  if (!gameId || !/^[a-z0-9-]+$/.test(gameId)) {
    return new Response(JSON.stringify({ code: 40000, message: 'Invalid game ID format' }), { status: 400 });
  }

  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const { results } = await db.prepare(
      `SELECT id, game_id, name, description, commands_json, created_at
       FROM scenario_bundles
       WHERE game_id = ?
       ORDER BY created_at ASC`
    ).bind(gameId).all();

    const bundles = (results || []).map(b => {
      let commands = [];
      try {
        commands = b.commands_json ? JSON.parse(b.commands_json) : [];
      } catch (e) {}
      return {
        id: b.id,
        game_id: b.game_id,
        name: b.name,
        description: b.description || '官方精选一键场景配置包',
        command_count: commands.length,
        download_url: `/api/v1/games/${b.game_id}/download?bundle_id=${b.id}`
      };
    });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        game_id: gameId,
        total: bundles.length,
        bundles
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
      message: 'Failed to retrieve scenario bundles',
      details: err.message
    }), { status: 500 });
  }
}
