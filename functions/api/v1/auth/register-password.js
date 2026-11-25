/**
 * Cloudflare Pages Function: POST /api/v1/auth/register-password
 * Password-Based Player Registration with Strict Email Regex & Web Crypto PBKDF2
 */

import {
  getDatabase,
  getPlayerJwtSecret,
  isValidEmail,
  hashPassword,
  signUserJwt
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

  try {
    const body = await request.json().catch(() => ({}));
    const email = (body.email || '').trim().toLowerCase();
    const password = (body.password || '').trim();
    const confirmPassword = (body.confirm_password || '').trim();

    // 1. Strict Email Format Validation
    if (!isValidEmail(email)) {
      return new Response(JSON.stringify({
        code: 40001,
        message: '请输入有效合规的正规电子邮箱（例如 yourname@qq.com、gamer@163.com、xxx@gmail.com）'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 2. Password Strength Check
    if (!password || password.length < 6) {
      return new Response(JSON.stringify({
        code: 40002,
        message: '注册密码长度至少需要 6 位字符'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    if (password.length > 64) {
      return new Response(JSON.stringify({
        code: 40003,
        message: '密码长度不可超过 64 位字符'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 3. Confirm Password Match
    if (confirmPassword && password !== confirmPassword) {
      return new Response(JSON.stringify({
        code: 40004,
        message: '两次输入的密码不一致，请仔细核对'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 4. Check if Email Already Registered
    const existing = await db.prepare(
      'SELECT id FROM users WHERE email = ? LIMIT 1'
    ).bind(email).first();

    if (existing) {
      return new Response(JSON.stringify({
        code: 40005,
        message: '该邮箱已经注册，请直接切换至【登录】选项卡输入密码'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 5. PBKDF2 Password Hashing (100k iterations, random salt)
    const { hashHex, saltHex } = await hashPassword(password);

    // 6. Generate Unique Player Identity
    const newUserId = 'usr_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8);
    const randomNum = Math.floor(1000 + Math.random() * 9000);
    const defaultNickname = `单机玩家#${randomNum}`;
    const defaultAvatar = 'avatar.jpg';

    // 7. Insert New User into D1 Database
    await db.prepare(
      `INSERT INTO users (id, provider, email, nickname, avatar_url, password_hash, password_salt, status, created_at, last_login_at, updated_at)
       VALUES (?, 'password', ?, ?, ?, ?, ?, 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)`
    ).bind(newUserId, email, defaultNickname, defaultAvatar, hashHex, saltHex).run();

    // 8. Generate 30-Day Stateless JWT
    const secret = getPlayerJwtSecret(env);
    const token = await signUserJwt({
      id: newUserId,
      email,
      nickname: defaultNickname,
      avatar_url: defaultAvatar
    }, secret);

    const newUser = {
      id: newUserId,
      email,
      nickname: defaultNickname,
      avatar_url: defaultAvatar,
      has_password: true,
      created_at: new Date().toISOString(),
      last_login_at: new Date().toISOString()
    };

    return new Response(JSON.stringify({
      code: 0,
      message: '🎉 恭喜！账号注册成功，已自动登录进入 L-MOD Vault',
      data: {
        token,
        is_first_login: true,
        has_password: true,
        user: newUser
      }
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Set-Cookie': `lmod_player_token=${token}; Path=/; Max-Age=2592000; SameSite=Lax`
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '注册处理异常，请稍后重试',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
