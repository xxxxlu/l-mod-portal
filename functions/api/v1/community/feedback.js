/**
 * Cloudflare Pages Function: /api/v1/community/feedback
 * Player bug reports & mod feedback endpoint with authenticated user association
 */

import { extractUserToken, verifyUserJwt, getPlayerJwtSecret } from '../auth/_crypto.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  try {
    const body = await request.json().catch(() => ({}));
    const { game_id, category, content } = body;

    if (!content || typeof content !== 'string' || content.trim().length === 0) {
      return new Response(JSON.stringify({
        code: 40000,
        message: '反馈内容不能为空'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    const country = request.headers.get('cf-ipcountry') || 'Unknown';
    const sanitizedGameId = game_id ? String(game_id).slice(0, 64) : null;
    const sanitizedCategory = ['bug_report', 'mod_request', 'comment'].includes(category) ? category : 'bug_report';
    const sanitizedContent = content.trim().slice(0, 1000);
    
    let userId = body.user_id ? String(body.user_id).slice(0, 64) : null;
    let playerEmail = body.player_email ? String(body.player_email).slice(0, 128) : null;
    let nickname = (body.player_nickname || '').trim().slice(0, 50);

    // If request contains player JWT token, automatically bind verified user profile
    const token = extractUserToken(request);
    if (token) {
      const secret = getPlayerJwtSecret(env);
      const auth = await verifyUserJwt(token, secret);
      if (auth.valid && auth.payload) {
        userId = auth.payload.id || auth.payload.sub || userId;
        playerEmail = auth.payload.email || playerEmail;
        if (!nickname) nickname = auth.payload.nickname || '认证玩家';
      }
    }

    if (!nickname) nickname = '单机玩家';

    if (db) {
      await db.prepare(
        `INSERT INTO community_feedback 
         (game_id, category, content, player_nickname, player_ip_country, user_id, player_email, created_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)`
      ).bind(
        sanitizedGameId,
        sanitizedCategory,
        sanitizedContent,
        nickname,
        country,
        userId,
        playerEmail
      ).run();

      return new Response(JSON.stringify({
        code: 0,
        message: 'success',
        data: {
          submitted: true,
          user_id: userId,
          notice: '感谢反馈！老L智库运维中台已实时收录排查。'
        }
      }), {
        headers: { 'Content-Type': 'application/json; charset=utf-8' }
      });
    }

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: { submitted: true, notice: 'Feedback received (staging mode)' }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to process feedback',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
