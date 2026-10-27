/**
 * Cloudflare Pages Function: POST /api/v1/admin/login
 * Station Master Zero Trust Authentication (Username & Password / Passkey)
 */

import { getAdminCredentials, getJwtSecret, signAdminJwt, logAdminAction } from './_auth.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  try {
    const body = await request.json();
    const providedUser = (body.username || body.account || '').trim();
    const providedPass = (body.password || body.secret_key || '').trim();

    if (!providedPass) {
      return new Response(JSON.stringify({
        code: 40001,
        message: '请输入站长登录密码 (Password required)'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json; charset=utf-8' }
      });
    }

    const { username: validUser, password: validPassword, legacyKey } = await getAdminCredentials(env, db);

    // Accept both:
    // 1) Username + Password check (if username is supplied)
    // 2) Password-only / Secret-key-only check (for legacy or direct passkey)
    let isUserMatch = true;
    if (providedUser) {
      const allowedUsers = [validUser.toLowerCase(), 'admin', 'laol', 'station_master'];
      isUserMatch = allowedUsers.includes(providedUser.toLowerCase());
    }

    const isPassMatch = (providedPass === validPassword) || (providedPass === legacyKey);

    if (!isUserMatch || !isPassMatch) {
      if (db) {
        await logAdminAction(db, {
          action: 'admin_login_failed',
          entity: 'auth',
          entity_id: providedUser || 'bad_credentials',
          details: `Failed credentials attempt (User: ${providedUser || 'none'}) from IP: ${clientIP}`,
          client_ip: clientIP
        });
      }

      return new Response(JSON.stringify({
        code: 40102,
        message: '账号或密码错误：站长特权通道鉴权失败 (Invalid Username or Password)'
      }), {
        status: 401,
        headers: { 'Content-Type': 'application/json; charset=utf-8' }
      });
    }

    // Credentials verified! Issue 7-day stateless JWT token
    const jwtSecret = getJwtSecret(env);
    const effectiveUsername = providedUser || validUser || 'admin';
    const token = await signAdminJwt({
      username: effectiveUsername,
      display_name: '老L·站长',
      client_ip: clientIP
    }, jwtSecret);

    if (db) {
      await logAdminAction(db, {
        action: 'admin_login_success',
        entity: 'auth',
        entity_id: effectiveUsername,
        details: `Station Master '${effectiveUsername}' logged in successfully via Web Crypto JWT`,
        client_ip: clientIP
      });
    }

    return new Response(JSON.stringify({
      code: 0,
      message: '站长特权认证通过，欢迎回到 L-MOD 控制平面',
      data: {
        token,
        token_type: 'Bearer',
        expires_in: 7 * 24 * 3600,
        admin_profile: {
          username: effectiveUsername,
          displayName: '老L·站长',
          role: 'super_admin',
          permissions: ['telemetry:read', 'vault:cms', 'ai:tune', 'radar:control'],
          node_region: request.headers.get('cf-ipcountry') || 'APAC-EDGE'
        }
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
      message: '登录鉴权服务异常',
      details: err.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }
}
