/**
 * Cloudflare Pages Function: POST /api/v1/admin/games/visibility
 * 隐藏 / 取消隐藏一款游戏：{ "id": "elden-ring", "hidden": true }
 *
 * 只改 games.is_hidden，绝不删行：user_favorites / user_radar_subscriptions 对 games 是 ON DELETE CASCADE，
 * 删一行就连带删掉玩家的收藏和订阅。隐藏后公开目录、旧 /api/v1/games* 接口和 data.js 快照里都不再出现。
 */

import { bumpCatalogVersionStmt, jsonResponse } from '../../catalog/_game_doc.js';

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  const adminUser = (data && data.admin && data.admin.username) || 'admin';
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';
  if (!db) return jsonResponse({ code: 50000, message: 'Database binding missing' }, 500);

  try {
    const { id, hidden } = await request.json();
    if (typeof id !== 'string' || !id || typeof hidden !== 'boolean') {
      return jsonResponse({ code: 40000, message: '需要 { id, hidden: true|false }' }, 400);
    }
    const row = await db.prepare('SELECT id, title_zh, is_hidden FROM games WHERE id = ?').bind(id).first();
    if (!row) return jsonResponse({ code: 40400, message: `游戏「${id}」不存在` }, 404);
    if (Boolean(row.is_hidden) === hidden) {
      return jsonResponse({ code: 0, message: hidden ? '本来就是隐藏的' : '本来就是公开的', data: { id, hidden } });
    }

    await db.batch([
      db.prepare('UPDATE games SET is_hidden = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').bind(hidden ? 1 : 0, id),
      db.prepare(
        `INSERT INTO admin_audit_logs (action, entity, entity_id, details, admin_user, client_ip) VALUES (?, 'games', ?, ?, ?, ?)`
      ).bind(hidden ? 'hide_game' : 'unhide_game', id, JSON.stringify({ title_zh: row.title_zh }), adminUser, clientIP),
      bumpCatalogVersionStmt(db)
    ]);

    return jsonResponse({
      code: 0,
      message: hidden ? `已隐藏「${row.title_zh || id}」（玩家的收藏和订阅都还在）` : `已恢复显示「${row.title_zh || id}」`,
      data: { id, hidden }
    });
  } catch (err) {
    return jsonResponse({ code: 50000, message: '操作失败', details: err.message }, 500);
  }
}
