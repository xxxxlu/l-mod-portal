/**
 * Cloudflare Pages Function: /api/v1/auth/favorites
 * Millisecond Real-time Player Game Favorites Engine with Instant D1 Persistence
 */

import {
  getDatabase,
  getPlayerJwtSecret,
  extractUserToken,
  verifyUserJwt
} from './_crypto.js';

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = getDatabase(env);

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  const token = extractUserToken(request);
  const secret = getPlayerJwtSecret(env);
  const authResult = await verifyUserJwt(token, secret);

  if (!authResult.valid) {
    return new Response(JSON.stringify({ code: 40100, message: '未登录' }), { status: 401 });
  }

  const userId = authResult.payload.id || authResult.payload.sub;

  const { results } = await db.prepare(
    'SELECT game_id, created_at FROM user_favorites WHERE user_id = ? ORDER BY created_at DESC'
  ).bind(userId).all();

  return new Response(JSON.stringify({
    code: 0,
    message: 'success',
    data: {
      game_ids: (results || []).map(r => r.game_id),
      items: results || []
    }
  }), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = getDatabase(env);

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  const token = extractUserToken(request);
  const secret = getPlayerJwtSecret(env);
  const authResult = await verifyUserJwt(token, secret);

  if (!authResult.valid) {
    return new Response(JSON.stringify({
      code: 40100,
      message: '请先登录后再收藏游戏'
    }), { status: 401, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }

  const userId = authResult.payload.id || authResult.payload.sub;

  try {
    const body = await request.json().catch(() => ({}));
    const gameId = (body.game_id || '').trim();
    const action = (body.action || 'toggle').trim().toLowerCase();

    if (!gameId) {
      return new Response(JSON.stringify({ code: 40000, message: 'Game ID required' }), { status: 400 });
    }

    // Check if game exists
    const gameExists = await db.prepare('SELECT id FROM games WHERE id = ? LIMIT 1').bind(gameId).first();
    if (!gameExists) {
      return new Response(JSON.stringify({ code: 40400, message: '游戏不存在' }), { status: 404 });
    }

    // Check current favorite state
    const existing = await db.prepare(
      'SELECT game_id FROM user_favorites WHERE user_id = ? AND game_id = ?'
    ).bind(userId, gameId).first();

    let isFavorited = false;

    if (action === 'remove' || (action === 'toggle' && existing)) {
      // Remove
      await db.prepare('DELETE FROM user_favorites WHERE user_id = ? AND game_id = ?').bind(userId, gameId).run();
      isFavorited = false;
    } else {
      // Add
      await db.prepare('INSERT OR IGNORE INTO user_favorites (user_id, game_id, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)').bind(userId, gameId).run();
      isFavorited = true;
    }

    // Asynchronously record favorite telemetry event
    const country = request.headers.get('cf-ipcountry') || 'Unknown';
    context.waitUntil(
      db.prepare(
        `INSERT INTO telemetry_events (event_type, game_id, target_payload, session_id, user_id, client_country)
         VALUES (?, ?, ?, ?, ?, ?)`
      ).bind(
        isFavorited ? 'favorite_add' : 'favorite_remove',
        gameId,
        isFavorited ? 'Player favorited game' : 'Player unfavorited game',
        'auth_sync',
        userId,
        country
      ).run().catch(() => {})
    );

    // Get updated total favorites count for user
    const totalFavRes = await db.prepare('SELECT count(*) as count FROM user_favorites WHERE user_id = ?').bind(userId).first();

    return new Response(JSON.stringify({
      code: 0,
      message: isFavorited ? '已添加到我的单机收藏' : '已取消收藏',
      data: {
        game_id: gameId,
        is_favorited: isFavorited,
        total_favorites: totalFavRes?.count || 0
      }
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '收藏操作失败',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
