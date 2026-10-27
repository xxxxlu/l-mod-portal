/**
 * Cloudflare Pages Function: POST /api/v1/admin/commands/save
 * Console Commands CMS: Upsert (Create or Update) Command Record
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
    const body = await request.json();
    const {
      id,
      game_id,
      category_id,
      category_name_zh,
      category_name_en,
      name_zh,
      name_en,
      code,
      description,
      syntax_type,
      is_popular
    } = body;

    if (!game_id || !name_zh || !code) {
      return new Response(JSON.stringify({
        code: 40000,
        message: 'Missing mandatory fields: game_id, name_zh, and code are required'
      }), { status: 400 });
    }

    // Verify game exists
    const game = await db.prepare('SELECT id, title_zh FROM games WHERE id = ?').bind(game_id).first();
    if (!game) {
      return new Response(JSON.stringify({ code: 40400, message: `Target game '${game_id}' not found` }), { status: 404 });
    }

    // Generate command ID if creating new
    const commandId = id && id.trim() ? id.trim() : `${game_id}_cmd_${Date.now().toString(36)}`;

    // Check if command exists
    const existing = await db.prepare('SELECT id, name_zh FROM console_commands WHERE id = ?').bind(commandId).first();

    const isUpdate = Boolean(existing);

    if (isUpdate) {
      await db.prepare(`
        UPDATE console_commands
        SET game_id = ?, category_id = ?, category_name_zh = ?, category_name_en = ?,
            name_zh = ?, name_en = ?, code = ?, description = ?,
            syntax_type = ?, is_popular = ?
        WHERE id = ?
      `).bind(
        game_id,
        category_id || 'general',
        category_name_zh || '常用代码',
        category_name_en || 'General',
        name_zh,
        name_en || null,
        code,
        description || null,
        syntax_type || 'engine_console',
        is_popular ? 1 : 0,
        commandId
      ).run();
    } else {
      await db.prepare(`
        INSERT INTO console_commands
        (id, game_id, category_id, category_name_zh, category_name_en, name_zh, name_en, code, description, syntax_type, is_popular)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        commandId,
        game_id,
        category_id || 'general',
        category_name_zh || '常用代码',
        category_name_en || 'General',
        name_zh,
        name_en || null,
        code,
        description || null,
        syntax_type || 'engine_console',
        is_popular ? 1 : 0
      ).run();
    }

    await logAdminAction(db, {
      action: isUpdate ? 'update_command' : 'create_command',
      entity: 'console_commands',
      entity_id: commandId,
      details: { game_id, name_zh, code_snippet: code.slice(0, 50), syntax_type },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: `控制台指令【${name_zh}】${isUpdate ? '更新' : '创建'}成功！即刻生效于 D1`,
      data: {
        id: commandId,
        game_id,
        name_zh,
        code,
        is_update: isUpdate
      }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to save console command',
      details: err.message
    }), { status: 500 });
  }
}
