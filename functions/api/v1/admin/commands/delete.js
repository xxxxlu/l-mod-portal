/**
 * Cloudflare Pages Function: POST /api/v1/admin/commands/delete
 * Console Commands CMS: Delete Command Record with Safeguard
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
    const { id } = await request.json();

    if (!id) {
      return new Response(JSON.stringify({ code: 40000, message: 'Command ID is required' }), { status: 400 });
    }

    const command = await db.prepare('SELECT id, game_id, name_zh, code FROM console_commands WHERE id = ?').bind(id).first();
    if (!command) {
      return new Response(JSON.stringify({ code: 40400, message: 'Command not found' }), { status: 404 });
    }

    await db.prepare('DELETE FROM console_commands WHERE id = ?').bind(id).run();

    await logAdminAction(db, {
      action: 'delete_command',
      entity: 'console_commands',
      entity_id: id,
      details: { game_id: command.game_id, name_zh: command.name_zh, code: command.code },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: `控制台指令【${command.name_zh}】已从 D1 库彻底删除`,
      data: { id, game_id: command.game_id }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to delete console command',
      details: err.message
    }), { status: 500 });
  }
}
