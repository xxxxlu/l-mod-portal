/**
 * Cloudflare Pages Function: POST /api/v1/admin/feedback/note
 * Body: { id, note, status? }  — saves the admin's handling note (<= 1000 chars) and, optionally, a new status.
 * handled_at is set to now. Requires migration v6 (community_feedback.admin_note / handled_at).
 */

import { logAdminAction } from '../_auth.js';

const STATUSES = ['pending', 'verified', 'resolved'];

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  let body;
  try { body = await request.json(); } catch (e) { return json({ code: 40000, message: 'Invalid JSON' }, 400); }
  const id = parseInt(body && body.id, 10);
  const note = typeof body.note === 'string' ? body.note.trim().slice(0, 1000) : '';
  const status = body.status === undefined || body.status === null || body.status === '' ? null : body.status;
  if (!id) return json({ code: 40000, message: '缺少反馈 ID' }, 400);
  if (status !== null && !STATUSES.includes(status)) return json({ code: 40000, message: '状态只能是 pending / verified / resolved' }, 400);

  try {
    const current = await db.prepare('SELECT id, status, game_id, admin_note FROM community_feedback WHERE id = ?1').bind(id).first();
    if (!current) return json({ code: 40400, message: '反馈不存在' }, 404);

    const nextStatus = status || current.status;
    await db.prepare(
      'UPDATE community_feedback SET admin_note = ?1, status = ?2, handled_at = CURRENT_TIMESTAMP WHERE id = ?3'
    ).bind(note || null, nextStatus, id).run();

    await logAdminAction(db, {
      action: 'update_feedback_note',
      entity: 'community_feedback',
      entity_id: String(id),
      details: {
        game_id: current.game_id,
        status: current.status === nextStatus ? nextStatus : { previous: current.status, updated: nextStatus },
        note_changed: (current.admin_note || '') !== note
      },
      admin_user: (data && data.admin && data.admin.username) || 'admin',
      client_ip: request.headers.get('cf-connecting-ip') || '127.0.0.1'
    });

    return json({ code: 0, message: `反馈 #${id} 已保存`, data: { id, status: nextStatus, admin_note: note || null } });
  } catch (err) {
    if (/no such column/i.test(err.message || '')) {
      return json({ code: 50000, message: '数据库还没执行 migration v6，暂时不能写处理备注' }, 500);
    }
    return json({ code: 50000, message: 'Failed to save feedback note', details: err.message }, 500);
  }
}
