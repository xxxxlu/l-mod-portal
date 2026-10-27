/**
 * Cloudflare Pages Function: POST /api/v1/admin/feedback/status
 * Moderate Feedback Item Status (pending | verified | resolved)
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
    const { id, status } = await request.json();

    if (!id || !['pending', 'verified', 'resolved'].includes(status)) {
      return new Response(JSON.stringify({
        code: 40000,
        message: 'Invalid feedback ID or status (must be pending, verified, or resolved)'
      }), { status: 400 });
    }

    const currentItem = await db.prepare(
      'SELECT id, game_id, category, content, status FROM community_feedback WHERE id = ?'
    ).bind(id).first();

    if (!currentItem) {
      return new Response(JSON.stringify({ code: 40400, message: 'Feedback record not found' }), { status: 404 });
    }

    await db.prepare(
      'UPDATE community_feedback SET status = ? WHERE id = ?'
    ).bind(status, id).run();

    await logAdminAction(db, {
      action: 'update_feedback_status',
      entity: 'community_feedback',
      entity_id: String(id),
      details: { previous: currentItem.status, updated: status, game_id: currentItem.game_id },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: `反馈 #${id} 状态已更新为: ${status}`,
      data: { id, status }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to update feedback status',
      details: err.message
    }), { status: 500 });
  }
}
