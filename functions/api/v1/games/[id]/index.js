/**
 * Cloudflare Pages Function: /api/v1/games/:id
 * Single Game Full Metadata (excludes heavy command list for lean transfer)
 *
 * 雷达字段（compatibility_status / radar）来自 public/radar_status.json 的 v2 结果（见 ../../../_radar_status.js），
 * 不再输出 D1 的旧雷达列。
 */

import { loadRadarStatus, withRadar } from '../../../_radar_status.js';

export async function onRequestGet(context) {
  const { params, env } = context;
  const gameId = params.id;

  // Strict regex check to prevent directory traversal / injection
  if (!gameId || !/^[a-z0-9-]+$/.test(gameId)) {
    return new Response(JSON.stringify({
      code: 40000,
      message: 'Invalid game ID format'
    }), { status: 400 });
  }

  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 503 });
  }

  try {
    const game = await db.prepare(
      `SELECT id, rank, title, title_zh, titles_json, developer, release_year, 
              genre, steam_rating, steam_app_id, header_image,
              has_console, console_shortcut, console_guide_zh, console_guide_en,
              has_mods, mod_install_path, has_trainer, pitfall_note,
              created_at, updated_at
       FROM games
       WHERE id = ? AND is_hidden = 0`
    ).bind(gameId).first();

    if (!game) {
      return new Response(JSON.stringify({
        code: 40401,
        message: `Game '${gameId}' not found in L-MOD Vault`
      }), { status: 404 });
    }

    // Get command count and categories count for this game
    const stats = await db.prepare(
      `SELECT count(*) as total_commands, count(DISTINCT category_id) as total_categories
       FROM console_commands
       WHERE game_id = ?`
    ).bind(gameId).first();

    let titles = {};
    try {
      titles = game.titles_json ? JSON.parse(game.titles_json) : {};
    } catch (e) {}

    const { titles_json, ...rest } = game;
    const radarStatus = await loadRadarStatus(context);

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        ...withRadar(rest, radarStatus),
        titles,
        stats: {
          total_commands: stats?.total_commands || 0,
          total_categories: stats?.total_categories || 0
        }
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
      message: 'Failed to retrieve game details',
      details: err.message
    }), { status: 500 });
  }
}
