/**
 * Cloudflare Pages Function: POST /api/v1/auth/verify-code
 * Player OTP Verification, Auto-Registration & Stateless JWT Token Generation
 */

import { getDatabase, getPlayerJwtSecret, signUserJwt, ensureAuthSchema } from './_crypto.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = getDatabase(env);

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }

  try {
    const body = await request.json().catch(() => ({}));
    const email = (body.email || '').trim().toLowerCase();
    const code = (body.code || '').trim();
    const purpose = (body.purpose || 'login').trim().toLowerCase();

    if (!email || !code || code.length !== 6) {
      return new Response(JSON.stringify({
        code: 40011,
        message: '请提供有效的邮箱与 6 位数字验证码'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 1. Query Latest Unused OTP Record for this email and purpose
    const record = await db.prepare(
      `SELECT id, email, code, purpose, expires_at, attempts, is_used,
              (strftime('%s', 'now') - strftime('%s', expires_at)) as expired_diff
       FROM email_verification_codes
       WHERE email = ? AND purpose = ? AND is_used = 0
       ORDER BY id DESC LIMIT 1`
    ).bind(email, purpose).first();

    if (!record) {
      return new Response(JSON.stringify({
        code: 40012,
        message: '验证码不存在或已使用，请重新获取'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 2. Check Expiration
    if (record.expired_diff !== null && record.expired_diff > 0) {
      return new Response(JSON.stringify({
        code: 40013,
        message: '验证码已过期（超过10分钟），请重新获取'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 3. Check Attempt Exhaustion (5 times limit)
    if (record.attempts >= 5) {
      return new Response(JSON.stringify({
        code: 40014,
        message: '该验证码已连续输错 5 次并已自动作废，请重新获取验证码'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 4. Validate Code Matching
    if (record.code !== code) {
      const newAttempts = record.attempts + 1;
      await db.prepare(
        'UPDATE email_verification_codes SET attempts = ? WHERE id = ?'
      ).bind(newAttempts, record.id).run();

      const remaining = Math.max(0, 5 - newAttempts);
      if (remaining === 0) {
        return new Response(JSON.stringify({
          code: 40014,
          message: '验证码错误！已达到 5 次上限，该验证码已作废，请重新获取。'
        }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }

      return new Response(JSON.stringify({
        code: 40015,
        message: `验证码错误，还剩 ${remaining} 次尝试机会`,
        data: { remaining_attempts: remaining }
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 5. Code Matched! Mark code as used
    await db.prepare(
      'UPDATE email_verification_codes SET is_used = 1 WHERE id = ?'
    ).bind(record.id).run();

    // 6. Handle Login & Auto-Registration Lifecycle
    if (purpose === 'login') {
      let user = await db.prepare(
        'SELECT id, provider, email, nickname, avatar_url, password_hash, created_at, last_login_at FROM users WHERE email = ? LIMIT 1'
      ).bind(email).first();

      let isFirstLogin = false;

      if (!user) {
        // Auto-register new player
        isFirstLogin = true;
        const newUserId = 'usr_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8);
        const randomNum = Math.floor(1000 + Math.random() * 9000);
        const defaultNickname = `单机玩家#${randomNum}`;
        const defaultAvatar = 'avatar.jpg';

        await db.prepare(
          `INSERT INTO users (id, provider, email, nickname, avatar_url, status, created_at, last_login_at, updated_at)
           VALUES (?, 'email', ?, ?, ?, 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)`
        ).bind(newUserId, email, defaultNickname, defaultAvatar).run();

        user = {
          id: newUserId,
          provider: 'email',
          email: email,
          nickname: defaultNickname,
          avatar_url: defaultAvatar,
          password_hash: null,
          created_at: new Date().toISOString(),
          last_login_at: new Date().toISOString()
        };
      } else {
        // Update last login timestamp
        await db.prepare(
          'UPDATE users SET last_login_at = CURRENT_TIMESTAMP WHERE id = ?'
        ).bind(user.id).run();
      }

      const hasPassword = Boolean(user.password_hash);
      const secret = getPlayerJwtSecret(env);
      const token = await signUserJwt({
        id: user.id,
        email: user.email,
        nickname: user.nickname,
        avatar_url: user.avatar_url
      }, secret);

      return new Response(JSON.stringify({
        code: 0,
        message: isFirstLogin ? '欢迎加入 L-MOD Vault！账号已自动创建' : '登录成功',
        data: {
          token,
          is_first_login: isFirstLogin,
          has_password: hasPassword,
          user: {
            id: user.id,
            email: user.email,
            nickname: user.nickname,
            avatar_url: user.avatar_url,
            has_password: hasPassword,
            created_at: user.created_at,
            last_login_at: user.last_login_at
          }
        }
      }), {
        status: 200,
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
          'Set-Cookie': `lmod_player_token=${token}; Path=/; Max-Age=2592000; SameSite=Lax`
        }
      });
    }

    // For non-login purposes (e.g. standalone verification step)
    return new Response(JSON.stringify({
      code: 0,
      message: '验证码核验通过',
      data: { verified: true, email: email, purpose: purpose }
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '验证码核验异常，请稍后重试',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
