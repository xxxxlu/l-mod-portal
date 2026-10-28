/**
 * Cloudflare Pages Function: POST /api/v1/auth/change-email
 * Securely Update Player Bound Email with New-Email OTP Verification
 */

import {
  getDatabase,
  getPlayerJwtSecret,
  extractUserToken,
  verifyUserJwt,
  signUserJwt
} from './_crypto.js';

const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

export async function onRequestPost(context) {
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
      message: '请先登录后再进行邮箱换绑操作',
      error: authResult.error
    }), { status: 401, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }

  const userId = authResult.payload.id || authResult.payload.sub;

  try {
    const body = await request.json().catch(() => ({}));
    const newEmail = (body.new_email || '').trim().toLowerCase();
    const code = (body.code || '').trim();

    // 2. Validate Inputs
    if (!newEmail || !EMAIL_REGEX.test(newEmail)) {
      return new Response(JSON.stringify({
        code: 40050,
        message: '请输入格式正确的新电子邮箱地址'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    if (!code || code.length !== 6) {
      return new Response(JSON.stringify({
        code: 40051,
        message: '请输入发送至新邮箱的 6 位数字验证码'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 3. Fetch Current User
    const user = await db.prepare(
      'SELECT id, email, nickname, avatar_url FROM users WHERE id = ? LIMIT 1'
    ).bind(userId).first();

    if (!user) {
      return new Response(JSON.stringify({
        code: 40400,
        message: '用户账号不存在'
      }), { status: 404, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    if (user.email === newEmail) {
      return new Response(JSON.stringify({
        code: 40052,
        message: '新邮箱不能与当前绑定邮箱相同'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 4. Verify New Email is not taken by another user
    const conflictUser = await db.prepare(
      'SELECT id FROM users WHERE email = ? AND id != ? LIMIT 1'
    ).bind(newEmail, userId).first();

    if (conflictUser) {
      return new Response(JSON.stringify({
        code: 40053,
        message: '该新邮箱已被其他玩家绑定，请更换其他邮箱'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 5. Verify OTP Code for new_email with purpose = 'change_email'
    const record = await db.prepare(
      `SELECT id, code, attempts,
              (strftime('%s', 'now') - strftime('%s', expires_at)) as expired_diff
       FROM email_verification_codes
       WHERE email = ? AND purpose = 'change_email' AND is_used = 0
       ORDER BY id DESC LIMIT 1`
    ).bind(newEmail).first();

    if (!record) {
      return new Response(JSON.stringify({
        code: 40054,
        message: '新邮箱验证码不存在或已使用，请重新获取'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    if (record.expired_diff !== null && record.expired_diff > 0) {
      return new Response(JSON.stringify({
        code: 40055,
        message: '新邮箱验证码已过期，请重新获取'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    if (record.attempts >= 5) {
      return new Response(JSON.stringify({
        code: 40056,
        message: '该验证码已连续输错 5 次失效，请重新获取'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    if (record.code !== code) {
      const newAttempts = record.attempts + 1;
      await db.prepare('UPDATE email_verification_codes SET attempts = ? WHERE id = ?').bind(newAttempts, record.id).run();
      const remaining = Math.max(0, 5 - newAttempts);
      return new Response(JSON.stringify({
        code: 40057,
        message: `验证码错误，还剩 ${remaining} 次机会`,
        data: { remaining_attempts: remaining }
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 6. Matched! Consume code & update user email
    await db.prepare('UPDATE email_verification_codes SET is_used = 1 WHERE id = ?').bind(record.id).run();
    await db.prepare('UPDATE users SET email = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').bind(newEmail, userId).run();

    // 7. Issue refreshed JWT token with updated email
    const newToken = await signUserJwt({
      id: user.id,
      email: newEmail,
      nickname: user.nickname,
      avatar_url: user.avatar_url
    }, secret);

    return new Response(JSON.stringify({
      code: 0,
      message: '安全绑定邮箱更换成功！',
      data: {
        token: newToken,
        email: newEmail
      }
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Set-Cookie': `lmod_player_token=${newToken}; Path=/; Max-Age=2592000; SameSite=Lax`
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '换绑邮箱处理失败，请稍后重试',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
