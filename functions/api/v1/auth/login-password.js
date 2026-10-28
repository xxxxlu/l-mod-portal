/**
 * Cloudflare Pages Function: POST /api/v1/auth/login-password
 * Direct Player Authentication via Email + PBKDF2 Password with Strict Email Regex Validation
 */

import {
  getDatabase,
  getPlayerJwtSecret,
  isValidEmail,
  hashPassword,
  verifyPassword,
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
    const autoRegister = Boolean(body.auto_register || body.action === 'register');

    // 1. Strict Email Format Regex Validation
    if (!isValidEmail(email)) {
      return new Response(JSON.stringify({
        code: 40040,
        message: '请输入有效合规的正规电子邮箱（例如 yourname@qq.com、gamer@163.com、xxx@gmail.com）'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 2. Password Check
    if (!password || password.length < 6) {
      return new Response(JSON.stringify({
        code: 40041,
        message: '密码长度至少需要 6 位字符'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 3. Fetch User Record by Email
    let user = await db.prepare(
      `SELECT id, provider, email, nickname, avatar_url, password_hash, password_salt, status, created_at, last_login_at 
       FROM users WHERE email = ? LIMIT 1`
    ).bind(email).first();

    // 4. If User does not exist: Smart Auto-Register or Prompt Register
    if (!user) {
      if (autoRegister) {
        // Auto-create new user
        const { hashHex, saltHex } = await hashPassword(password);
        const newUserId = 'usr_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 8);
        const randomNum = Math.floor(1000 + Math.random() * 9000);
        const defaultNickname = `单机玩家#${randomNum}`;
        const defaultAvatar = 'avatar.jpg';

        await db.prepare(
          `INSERT INTO users (id, provider, email, nickname, avatar_url, password_hash, password_salt, status, created_at, last_login_at, updated_at)
           VALUES (?, 'password', ?, ?, ?, ?, ?, 'active', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)`
        ).bind(newUserId, email, defaultNickname, defaultAvatar, hashHex, saltHex).run();

        const secret = getPlayerJwtSecret(env);
        const token = await signUserJwt({
          id: newUserId,
          email,
          nickname: defaultNickname,
          avatar_url: defaultAvatar
        }, secret);

        return new Response(JSON.stringify({
          code: 0,
          message: '🎉 欢迎新玩家！账号已自动建立并登录成功',
          data: {
            token,
            is_first_login: true,
            has_password: true,
            user: {
              id: newUserId,
              email,
              nickname: defaultNickname,
              avatar_url: defaultAvatar,
              has_password: true,
              created_at: new Date().toISOString(),
              last_login_at: new Date().toISOString()
            }
          }
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json; charset=utf-8',
            'Set-Cookie': `lmod_player_token=${token}; Path=/; Max-Age=2592000; SameSite=Lax`
          }
        });
      } else {
        return new Response(JSON.stringify({
          code: 40042,
          message: '该邮箱尚未注册，请切换至【注册新账号】或开启自动注册'
        }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }
    }

    // 5. If User exists but doesn't have password (e.g. initial OTP without password set)
    if (!user.password_hash || !user.password_salt) {
      // Establish password on this login
      const { hashHex, saltHex } = await hashPassword(password);
      await db.prepare(
        'UPDATE users SET password_hash = ?, password_salt = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
      ).bind(hashHex, saltHex, user.id).run();
      user.password_hash = hashHex;
      user.password_salt = saltHex;
    }

    // 6. Verify PBKDF2 Password
    const isValid = await verifyPassword(password, user.password_salt, user.password_hash);
    if (!isValid) {
      return new Response(JSON.stringify({
        code: 40043,
        message: '邮箱或密码不正确，请重新核对输入'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }

    // 7. Update last_login_at
    await db.prepare(
      'UPDATE users SET last_login_at = CURRENT_TIMESTAMP WHERE id = ?'
    ).bind(user.id).run();

    // 8. Generate 30-Day Stateless JWT Token
    const secret = getPlayerJwtSecret(env);
    const token = await signUserJwt({
      id: user.id,
      email: user.email,
      nickname: user.nickname,
      avatar_url: user.avatar_url
    }, secret);

    return new Response(JSON.stringify({
      code: 0,
      message: '登录成功，欢迎回到 L-MOD Vault！',
      data: {
        token,
        is_first_login: false,
        has_password: true,
        user: {
          id: user.id,
          email: user.email,
          nickname: user.nickname,
          avatar_url: user.avatar_url,
          has_password: true,
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

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '登录处理异常，请稍后重试',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
