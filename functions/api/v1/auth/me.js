/**
 * Cloudflare Pages Function: GET /api/v1/auth/me
 * Comprehensive Player Profile, Synced Favorites, Radar Alerts & Feedback History
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
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }

  // 1. Authenticate Player Session
  const token = extractUserToken(request);
  const secret = getPlayerJwtSecret(env);
  const authResult = await verifyUserJwt(token, secret);

  if (!authResult.valid) {
    return new Response(JSON.stringify({
      code: 40100,
      message: '玩家未登录或会话已过期',
      error: authResult.error
    }), {
      status: 401,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });
  }

  const userId = authResult.payload.id || authResult.payload.sub;

  try {
    // 2. Fetch User Profile
    const user = await db.prepare(
      `SELECT id, provider, email, nickname, avatar_url,
              (password_hash IS NOT NULL AND password_hash != '') as has_password,
              status, created_at, last_login_at
       FROM users WHERE id = ? LIMIT 1`
    ).bind(userId).first();

    if (!user) {
      return new Response(JSON.stringify({
        code: 40400,
        message: '用户资料不存在'
      }), { status: 404, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 3. Fetch User Favorites (JOIN games)
    const favRes = await db.prepare(
      `SELECT uf.game_id, uf.created_at, g.rank, g.title, g.title_zh, g.header_image,
              g.genre, g.compatibility_status, g.verified_patch
       FROM user_favorites uf
       LEFT JOIN games g ON uf.game_id = g.id
       WHERE uf.user_id = ?
       ORDER BY uf.created_at DESC`
    ).bind(userId).all();

    // 4. Fetch Radar Subscriptions
    const subRes = await db.prepare(
      `SELECT urs.id, urs.game_id, urs.notify_channel, urs.notify_target, urs.created_at,
              g.title, g.title_zh, g.compatibility_status
       FROM user_radar_subscriptions urs
       LEFT JOIN games g ON urs.game_id = g.id
       WHERE urs.user_id = ?
       ORDER BY urs.created_at DESC`
    ).bind(userId).all();

    // 5. Fetch Community Feedback History
    const feedbackRes = await db.prepare(
      `SELECT cf.id, cf.game_id, cf.category, cf.content, cf.status, cf.created_at,
              g.title as game_title, g.title_zh as game_title_zh
       FROM community_feedback cf
       LEFT JOIN games g ON cf.game_id = g.id
       WHERE cf.user_id = ? OR (cf.player_email = ? AND cf.player_email IS NOT NULL)
       ORDER BY cf.id DESC
       LIMIT 20`
    ).bind(userId, user.email || '').all();

    const favorites = favRes.results || [];
    const radarSubs = subRes.results || [];
    const feedbacks = feedbackRes.results || [];

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        user: {
          id: user.id,
          provider: user.provider,
          email: user.email,
          nickname: user.nickname,
          avatar_url: user.avatar_url,
          has_password: Boolean(user.has_password),
          status: user.status,
          created_at: user.created_at,
          last_login_at: user.last_login_at
        },
        favorites: favorites,
        favorites_count: favorites.length,
        radar_subscriptions: radarSubs,
        radar_count: radarSubs.length,
        feedback_history: feedbacks,
        feedback_count: feedbacks.length
      }
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '读取用户档案失败',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
