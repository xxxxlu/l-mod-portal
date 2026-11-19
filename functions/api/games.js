/**
 * Cloudflare Pages Function: /api/games
 * Global Edge API endpoint for L-MOD Vault Game Database.
 * Runs on Cloudflare's 300+ Edge Data Centers with Anycast routing.
 *
 * 雷达字段：不输出 D1 里的旧雷达列 / raw_json 里的旧雷达字段，改用 public/radar_status.json 的 v2 结果
 * （见 ./_radar_status.js）。
 */

import { loadRadarStatus, withRadar, withRadarRawGame } from './_radar_status.js';

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
    const db = env.DB || env.lmod_vault_db;
    // 1. If Cloudflare D1 Database binding is available
    if (db) {
      const radarStatus = await loadRadarStatus(context);
      if (gameId) {
        const { results } = await db.prepare(
          'SELECT * FROM games WHERE id = ?'
        ).bind(gameId).all();

        if (!results || results.length === 0) {
          return new Response(JSON.stringify({ error: 'Game not found', id: gameId }), {
            status: 404,
            headers: corsHeaders
          });
        }

        const game = results[0];
        // raw_json 是早期灌库时的整份游戏数据（data.js 形状）：去掉里面的旧雷达字段，换成 v2 结果
        if (game.raw_json) {
          try {
            const raw = JSON.parse(game.raw_json);
            return new Response(JSON.stringify(withRadarRawGame(raw, radarStatus)), { headers: corsHeaders });
          } catch (e) {}
        }
        const { raw_json, ...row } = game;
        return new Response(JSON.stringify(withRadar(row, radarStatus)), { headers: corsHeaders });
      }

      // Query list of all games (lightweight projection)
      let sql = 'SELECT id, rank, title, title_zh, developer, release_year, genre, steam_rating FROM games';
      const params = [];

      if (query) {
        sql += ' WHERE title LIKE ? OR title_zh LIKE ? OR developer LIKE ?';
        const qPattern = `%${query}%`;
        params.push(qPattern, qPattern, qPattern);
      }

      sql += ' ORDER BY rank ASC';
      const stmt = db.prepare(sql);
      const { results } = params.length > 0 ? await stmt.bind(...params).all() : await stmt.all();

      return new Response(JSON.stringify({
        source: 'cloudflare_d1_edge',
        radar_source: radarStatus ? 'radar_status.json' : null,
        radar_updated_at: radarStatus ? radarStatus.updatedAt : null,
        total: results.length,
        games: results.map(row => withRadar(row, radarStatus))
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
