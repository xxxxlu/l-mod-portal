/**
 * Cloudflare Pages Function: POST /api/v1/admin/games/update
 * Game CMS Update: Baseline Patch, Compatibility Tri-color, Radar Notes & Pitfalls
 */

import { logAdminAction } from '../_auth.js';

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  const admin = data?.admin || { username: '老L·站长' };
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const payload = await request.json();
    const {
      id,
      verified_patch,
      latest_steam_patch,
      compatibility_status,
      radar_risk_title,
      radar_risk_desc,
      radar_summary,
      pitfall_note,
      console_shortcut
    } = payload;

    if (!id || typeof id !== 'string') {
      return new Response(JSON.stringify({ code: 40000, message: 'Game ID is required' }), { status: 400 });
    }

    if (compatibility_status && !['green', 'yellow', 'red'].includes(compatibility_status)) {
      return new Response(JSON.stringify({
        code: 40000,
        message: 'Invalid compatibility status. Must be "green", "yellow", or "red"'
      }), { status: 400 });
    }

    // Verify game exists
    const existing = await db.prepare('SELECT id, title_zh, compatibility_status FROM games WHERE id = ?').bind(id).first();
    if (!existing) {
      return new Response(JSON.stringify({ code: 40400, message: `Game '${id}' does not exist` }), { status: 404 });
    }

    const updateSql = `
      UPDATE games
      SET verified_patch = COALESCE(?, verified_patch),
          latest_steam_patch = COALESCE(?, latest_steam_patch),
          compatibility_status = COALESCE(?, compatibility_status),
          radar_risk_title = COALESCE(?, radar_risk_title),
          radar_risk_desc = COALESCE(?, radar_risk_desc),
          radar_summary = COALESCE(?, radar_summary),
          pitfall_note = COALESCE(?, pitfall_note),
          console_shortcut = COALESCE(?, console_shortcut),
          updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `;

    await db.prepare(updateSql).bind(
      verified_patch !== undefined ? verified_patch : null,
      latest_steam_patch !== undefined ? latest_steam_patch : null,
      compatibility_status !== undefined ? compatibility_status : null,
      radar_risk_title !== undefined ? radar_risk_title : null,
      radar_risk_desc !== undefined ? radar_risk_desc : null,
      radar_summary !== undefined ? radar_summary : null,
      pitfall_note !== undefined ? pitfall_note : null,
      console_shortcut !== undefined ? console_shortcut : null,
      id
    ).run();

    await logAdminAction(db, {
      action: 'update_game_cms',
      entity: 'games',
      entity_id: id,
      details: {
        title_zh: existing.title_zh,
        status_prev: existing.compatibility_status,
        status_now: compatibility_status || existing.compatibility_status,
        verified_patch,
        latest_steam_patch
      },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: `游戏【${existing.title_zh || id}】配置更新成功！已即时同步 D1 数据库`,
      data: { id, compatibility_status, verified_patch, latest_steam_patch, updated_at: new Date().toISOString() }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to update game data',
      details: err.message
    }), { status: 500 });
  }
}
