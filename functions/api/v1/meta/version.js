/**
 * Cloudflare Pages Function: /api/v1/meta/version
 * Cache eviction and database revision detection
 */

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  let totalGames = 100;
  let totalCommands = 1093;

  if (db) {
    try {
      const gRow = await db.prepare('SELECT count(*) as count FROM games').first();
      const cRow = await db.prepare('SELECT count(*) as count FROM console_commands').first();
      if (gRow) totalGames = gRow.count;
      if (cRow) totalCommands = cRow.count;
    } catch (e) {}
  }

  return new Response(JSON.stringify({
    code: 0,
    message: 'success',
    data: {
      api_version: 'v1',
      build_timestamp: 1729864800,
      revision: '2026.10.27',
      total_games: totalGames,
      total_commands: totalCommands
    }
  }), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=60, s-maxage=300'
    }
  });
}
