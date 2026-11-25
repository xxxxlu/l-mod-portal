/**
 * Cloudflare Pages Function: PUT /api/v1/admin/trainers/:id/chunk/:n
 * Step 2 of an upload: the raw bytes of chunk n (0-based). The request body is handed to KV as a
 * stream — no JS copy, no hashing — so this stays inside the free plan's 10 ms CPU budget.
 */

import {
  getDb, getKv, json, isPackageId, chunkKey, chunkLength
} from '../../../../trainers/_store.js';

export async function onRequestPut(context) {
  const { request, env, params } = context;
  const db = getDb(env);
  const kv = getKv(env);

  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);
  if (!kv) return json({ code: 50301, message: '存储未开通：TRAINER_FILES 这个 KV 绑定还没建' }, 503);

  const id = String(params.id || '');
  const n = /^\d{1,3}$/.test(String(params.n)) ? Number(params.n) : -1;
  if (!isPackageId(id)) return json({ code: 40001, message: '包 ID 不合法' }, 400);

  try {
    const row = await db.prepare(
      'SELECT id, size, chunks, kv_prefix, status FROM trainer_packages WHERE id = ?'
    ).bind(id).first();
    if (!row) return json({ code: 40400, message: '没有这个上传' }, 404);
    if (row.status !== 'uploading') {
      return json({ code: 40900, message: `这个包已经是 ${row.status}，不能再写分片` }, 409);
    }

    const expected = chunkLength(Number(row.size), n);
    if (expected < 0 || n >= Number(row.chunks)) {
      return json({ code: 40002, message: `分片序号越界（共 ${row.chunks} 片）` }, 400);
    }

    const lenHeader = request.headers.get('Content-Length');
    if (lenHeader === null) return json({ code: 41100, message: '缺少 Content-Length' }, 411);
    const len = Number(lenHeader);
    if (len !== expected) {
      return json({ code: 40003, message: `分片 ${n} 应为 ${expected} 字节，收到 ${len}` }, 400);
    }

    await kv.put(chunkKey(row.kv_prefix, n), request.body, { metadata: { len } });
    return json({ code: 0, data: { id, n, len } });
  } catch (err) {
    return json({ code: 50000, message: `分片 ${n} 写入失败`, details: err.message }, 500);
  }
}
