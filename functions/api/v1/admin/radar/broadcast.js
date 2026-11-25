/**
 * Cloudflare Pages Function: /api/v1/admin/radar/broadcast
 * Emergency Circuit-Breaker Broadcast Control (紧急熔断全局跑马灯广播)
 */

import { logAdminAction } from '../_auth.js';

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const row = await db.prepare('SELECT value, updated_at FROM system_settings WHERE key = "emergency_broadcast"').first();
    let broadcast = {
      enabled: false,
      level: 'yellow',
      title: 'Steam 补丁兼容性预警',
      message: '近期 Steam 推出部分游戏热更新，请注意查看指令与前置框架适配指示灯。',
      target_game_id: null,
      updated_at: new Date().toISOString()
    };

    if (row?.value) {
      try { broadcast = JSON.parse(row.value); } catch (e) {}
    }

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: broadcast
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to fetch emergency broadcast state',
      details: err.message
    }), { status: 500 });
  }
}

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  const admin = data?.admin || { username: '老L·站长' };
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const body = await request.json();
    const { enabled, level, title, message, target_game_id } = body;

    const validatedLevel = ['yellow', 'red', 'info'].includes(level) ? level : 'yellow';
    const nowIso = new Date().toISOString();

    const broadcastPayload = {
      enabled: Boolean(enabled),
      level: validatedLevel,
      title: (title || '全站紧急兼容性熔断广播').trim().slice(0, 100),
      message: (message || '').trim().slice(0, 500),
      target_game_id: target_game_id && target_game_id !== 'all' ? target_game_id.trim() : null,
      updated_at: nowIso
    };

    const broadcastJson = JSON.stringify(broadcastPayload);

    await db.prepare(`
      INSERT INTO system_settings (key, value, description, updated_at)
      VALUES ('emergency_broadcast', ?, '全站紧急熔断与补丁警示跑马灯广播配置', CURRENT_TIMESTAMP)
      ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
    `).bind(broadcastJson).run();

    await logAdminAction(db, {
      action: broadcastPayload.enabled ? 'activate_emergency_broadcast' : 'deactivate_emergency_broadcast',
      entity: 'system_settings',
      entity_id: 'emergency_broadcast',
      details: broadcastPayload,
      admin_user: admin.username,
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: broadcastPayload.enabled
        ? `🚨 全站【${validatedLevel.toUpperCase()}】紧急熔断广播已全网激活！`
        : '✅ 全站紧急广播已关闭并归档',
      data: broadcastPayload
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to update emergency broadcast',
      details: err.message
    }), { status: 500 });
  }
}
