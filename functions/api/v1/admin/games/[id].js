/**
 * Cloudflare Pages Function: GET /api/v1/admin/games/[id]
 * Game CMS Detail: Complete Game Record + Commands + Scenario Bundles
 *
 * 雷达字段换成 public/radar_status.json 的 v2 结果（见 ../../../_radar_status.js）；D1 的旧雷达列
 * （除后台自己的 verified_patch）和 patch_radar_logs（早期灌库和旧「手动巡检」生成的模拟记录）不再返回。
 */

import { loadRadarStatus, radarEntry, radarApiObject } from '../../../_radar_status.js';

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

    const [commandsRes, bundlesRes] = await Promise.all([
      db.prepare(
        `SELECT * FROM console_commands WHERE game_id = ? ORDER BY category_id, is_popular DESC, name_zh ASC`
      ).bind(gameId).all(),
      db.prepare(
        `SELECT * FROM scenario_bundles WHERE game_id = ? ORDER BY id ASC`
      ).bind(gameId).all()
    ]);

    const radarStatus = await loadRadarStatus(context);
    const entry = radarEntry(radarStatus, gameId);
    const { raw_json, latest_steam_patch, compatibility_status, radar_risk_title, radar_risk_desc, radar_summary, ...rest } = game;
    const gameOut = {
      ...rest,
      compatibility_status: entry ? entry.compatibilityStatus : null,
      latest_steam_patch: entry ? (entry.latestSteamPatch || null) : null,
      radar_risk_title: entry ? (entry.radarStatusText || null) : null,
      radar: radarApiObject(entry, radarStatus)
    };

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        game: gameOut,
        commands: commandsRes.results || [],
        bundles: bundlesRes.results || [],
        radar_logs: []
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
