/**
 * Cloudflare Pages Function: POST /api/v1/admin/trainers/:id/withdraw
 * Take an active package down (or discard an unfinished upload): mark it withdrawn and delete its
 * KV chunks to free space. The D1 row stays as history; re-listing means uploading again.
 */

import { logAdminAction } from '../../_auth.js';
import { getDb, getKv, json, isPackageId, deleteChunks } from '../../../trainers/_store.js';

export async function onRequestPost(context) {
  const { request, env, params, data } = context;
  const db = getDb(env);
  const kv = getKv(env);
  const admin = data?.admin || { username: '老L·站长' };
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  const id = String(params.id || '');
  if (!isPackageId(id)) return json({ code: 40001, message: '包 ID 不合法' }, 400);

  try {
    const row = await db.prepare('SELECT * FROM trainer_packages WHERE id = ?').bind(id).first();
    if (!row) return json({ code: 40400, message: '没有这个包' }, 404);
    if (row.status === 'withdrawn') return json({ code: 40900, message: '这个包已经下架了' }, 409);

    await db.prepare("UPDATE trainer_packages SET status = 'withdrawn' WHERE id = ?").bind(id).run();

    let freedKeys = 0;
    let purgeError = null;
    if (kv) {
      try { freedKeys = await deleteChunks(kv, row); } catch (e) { purgeError = e.message; }
    }

    await logAdminAction(db, {
      action: row.status === 'uploading' ? 'trainer_upload_discard' : 'trainer_package_withdraw',
      entity: 'trainer_packages',
      entity_id: id,
      details: {
        game_id: row.game_id,
        file_name: row.file_name,
        sha256: row.sha256,
        previous_status: row.status,
        freed_keys: freedKeys,
        purge_error: purgeError
      },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return json({
      code: 0,
      message: row.status === 'uploading' ? '已丢弃这次上传' : '已下架，文件已从 KV 删除',
      data: { id, game_id: row.game_id, freed_keys: freedKeys, purge_error: purgeError }
    });
  } catch (err) {
    return json({ code: 50000, message: '下架失败', details: err.message }, 500);
  }
}
