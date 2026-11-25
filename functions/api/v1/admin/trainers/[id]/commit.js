/**
 * Cloudflare Pages Function: POST /api/v1/admin/trainers/:id/commit
 * Step 3 of an upload: check every chunk landed in KV with the expected length, then make this
 * package the game's active one. A previously active package is withdrawn and its chunks deleted.
 */

import { logAdminAction } from '../../_auth.js';
import {
  getDb, getKv, json, isPackageId, chunkKey, chunkLength, deleteChunks, downloadPath
} from '../../../trainers/_store.js';

export async function onRequestPost(context) {
  const { request, env, params, data } = context;
  const db = getDb(env);
  const kv = getKv(env);
  const admin = data?.admin || { username: '老L·站长' };
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);
  if (!kv) return json({ code: 50301, message: '存储未开通：TRAINER_FILES 这个 KV 绑定还没建' }, 503);

  const id = String(params.id || '');
  if (!isPackageId(id)) return json({ code: 40001, message: '包 ID 不合法' }, 400);

  try {
    const row = await db.prepare('SELECT * FROM trainer_packages WHERE id = ?').bind(id).first();
    if (!row) return json({ code: 40400, message: '没有这个上传' }, 404);
    if (row.status !== 'uploading') {
      return json({ code: 40900, message: `这个包已经是 ${row.status}` }, 409);
    }

    // Verify each chunk via its KV metadata. The value stream is cancelled unread.
    const size = Number(row.size);
    const missing = [];
    const wrongSize = [];
    for (let n = 0; n < Number(row.chunks); n++) {
      const res = await kv.getWithMetadata(chunkKey(row.kv_prefix, n), { type: 'stream' });
      if (!res || res.value === null) {
        missing.push(n);
        continue;
      }
      try { await res.value.cancel(); } catch (e) { /* already closed */ }
      if (!res.metadata || Number(res.metadata.len) !== chunkLength(size, n)) wrongSize.push(n);
    }
    if (missing.length || wrongSize.length) {
      return json({
        code: 40902,
        message: missing.length
          ? `分片 ${missing.join(', ')} 还没写进 KV，稍后重试提交或重新上传`
          : `分片 ${wrongSize.join(', ')} 大小不对，请重新上传`,
        data: { missing, wrongSize }
      }, 409);
    }

    const previous = await db.prepare(
      "SELECT * FROM trainer_packages WHERE game_id = ? AND status = 'active'"
    ).bind(row.game_id).first();

    // One transaction: retire the old active row first so the partial unique index never sees two.
    await db.batch([
      db.prepare("UPDATE trainer_packages SET status = 'withdrawn' WHERE game_id = ? AND status = 'active'")
        .bind(row.game_id),
      db.prepare("UPDATE trainer_packages SET status = 'active', uploaded_at = datetime('now') WHERE id = ? AND status = 'uploading'")
        .bind(id)
    ]);

    let freedKeys = 0;
    if (previous) {
      try { freedKeys = await deleteChunks(kv, previous); } catch (e) { /* left for a manual purge */ }
    }

    await logAdminAction(db, {
      action: previous ? 'trainer_package_replace' : 'trainer_package_publish',
      entity: 'trainer_packages',
      entity_id: id,
      details: {
        game_id: row.game_id,
        file_name: row.file_name,
        trainer_version: row.trainer_version,
        size,
        sha256: row.sha256,
        replaced: previous ? { id: previous.id, file_name: previous.file_name, sha256: previous.sha256, freed_keys: freedKeys } : null
      },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return json({
      code: 0,
      message: previous ? '已替换上架，旧包已下架并删除文件' : '已上架',
      data: { id, game_id: row.game_id, download_path: downloadPath(row.game_id, row.file_name), replaced: previous ? previous.id : null }
    });
  } catch (err) {
    return json({ code: 50000, message: '提交上架失败', details: err.message }, 500);
  }
}
