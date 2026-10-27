/**
 * Cloudflare Pages Function: POST /api/v1/admin/password
 * Allow Station Master to change password directly from admin console
 */

import { getAdminCredentials, logAdminAction } from './_auth.js';

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  const admin = data?.admin || { username: 'admin' };
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const { old_password, new_password } = await request.json();

    if (!old_password || !new_password) {
      return new Response(JSON.stringify({ code: 40000, message: '旧密码与新密码均不能为空' }), { status: 400 });
    }

    if (new_password.length < 6) {
      return new Response(JSON.stringify({ code: 40000, message: '新密码长度至少需要 6 个字符' }), { status: 400 });
    }

    const { username: currentUsername, password: currentPassword, legacyKey } = await getAdminCredentials(env, db);

    const isOldMatch = (old_password === currentPassword) || (old_password === legacyKey);
    if (!isOldMatch) {
      return new Response(JSON.stringify({ code: 40100, message: '原密码核验错误，无法更改密码' }), { status: 401 });
    }

    const newCreds = {
      username: currentUsername || 'admin',
      password: new_password,
      updated_at: new Date().toISOString()
    };

    await db.prepare(`
      INSERT INTO system_settings (key, value, description, updated_at)
      VALUES ('admin_credentials', ?, '站长后台登录账号与密码', CURRENT_TIMESTAMP)
      ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
    `).bind(JSON.stringify(newCreds)).run();

    await logAdminAction(db, {
      action: 'change_admin_password',
      entity: 'system_settings',
      entity_id: 'admin_credentials',
      details: { username: newCreds.username },
      admin_user: admin.username || 'admin',
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: '站长登录密码修改成功！新密码已即刻生效于 D1 数据库',
      data: { username: newCreds.username, updated_at: newCreds.updated_at }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: '密码修改失败',
      details: err.message
    }), { status: 500 });
  }
}
