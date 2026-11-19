/**
 * Cloudflare Pages Function: POST /api/v1/admin/games/update
 * Game CMS Update: Baseline Patch, Console Shortcut & Pitfalls
 *
 * 雷达字段（compatibility_status / latest_steam_patch / radar_risk_title / radar_risk_desc / radar_summary）
 * 由每天的巡检脚本写进 public/data.js 和 public/radar_status.json，网站和接口都只读那里；
 * 后台再往 D1 写这几列不会生效，所以收到也忽略，并在返回里列出 ignored_fields。
 */

const RADAR_V2_OWNED_FIELDS = ['latest_steam_patch', 'compatibility_status', 'radar_risk_title', 'radar_risk_desc', 'radar_summary'];

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
      pitfall_note,
      console_shortcut
    } = payload;
    const ignoredFields = RADAR_V2_OWNED_FIELDS.filter(f => payload[f] !== undefined);

    if (!id || typeof id !== 'string') {
      return new Response(JSON.stringify({ code: 40000, message: 'Game ID is required' }), { status: 400 });
    }

    // Verify game exists
    const existing = await db.prepare('SELECT id, title_zh FROM games WHERE id = ?').bind(id).first();
    if (!existing) {
      return new Response(JSON.stringify({ code: 40400, message: `Game '${id}' does not exist` }), { status: 404 });
    }

    const updateSql = `
      UPDATE games
      SET verified_patch = COALESCE(?, verified_patch),
          pitfall_note = COALESCE(?, pitfall_note),
          console_shortcut = COALESCE(?, console_shortcut),
          updated_at = CURRENT_TIMESTAMP
      WHERE id = ?
    `;

    await db.prepare(updateSql).bind(
      verified_patch !== undefined ? verified_patch : null,
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
        verified_patch,
        ignored_fields: ignoredFields
      },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: `游戏【${existing.title_zh || id}】配置更新成功！已即时同步 D1 数据库` +
        (ignoredFields.length ? `（雷达字段由每日巡检维护，后台修改不生效，已忽略：${ignoredFields.join(', ')}）` : ''),
      data: { id, verified_patch, ignored_fields: ignoredFields, updated_at: new Date().toISOString() }
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
