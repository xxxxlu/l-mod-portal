/**
 * Cloudflare Pages Function: POST /api/v1/auth/set-password
 * Set / Update Player Independent Password with Web Crypto PBKDF2 (100k Iterations)
 */

import {
  getDatabase,
  getPlayerJwtSecret,
  extractUserToken,
  verifyUserJwt,
  hashPassword,
  verifyPassword
} from './_crypto.js';

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
      message: '请先登录后再进行密码设置',
      error: authResult.error
    }), { status: 401, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }

  const userId = authResult.payload.id || authResult.payload.sub;

  try {
    const body = await request.json().catch(() => ({}));
    const newPassword = (body.password || '').trim();
    const oldPassword = (body.old_password || '').trim();

    // 2. Password Strength & Length Check
    if (!newPassword || newPassword.length < 6 || newPassword.length > 64) {
      return new Response(JSON.stringify({
        code: 40030,
        message: '新密码长度必须在 6 至 64 个字符之间'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 3. Fetch User Record
    const user = await db.prepare(
      'SELECT id, password_hash, password_salt FROM users WHERE id = ? LIMIT 1'
    ).bind(userId).first();

    if (!user) {
      return new Response(JSON.stringify({
        code: 40400,
        message: '用户账号不存在'
      }), { status: 404, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 4. If password already exists, require and verify old_password
    if (user.password_hash) {
      if (!oldPassword) {
        return new Response(JSON.stringify({
          code: 40031,
          message: '该账号已设置独立密码，修改密码请输入原密码'
        }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }

      const isOldValid = await verifyPassword(oldPassword, user.password_salt, user.password_hash);
      if (!isOldValid) {
        return new Response(JSON.stringify({
          code: 40032,
          message: '原密码核验不正确，请重新输入'
        }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }
    }

    // 5. Generate Salt & PBKDF2 Hash
    const { hashHex, saltHex } = await hashPassword(newPassword);

    // 6. Update User Record
    await db.prepare(
      'UPDATE users SET password_hash = ?, password_salt = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
    ).bind(hashHex, saltHex, userId).run();

    return new Response(JSON.stringify({
      code: 0,
      message: '独立登录密码设置成功！您后续可使用【邮箱 + 密码】直接登录',
      data: {
        success: true,
        has_password: true
      }
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '设置密码失败，请稍后重试',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
