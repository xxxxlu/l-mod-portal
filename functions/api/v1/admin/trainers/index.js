/**
 * Cloudflare Pages Function: GET /api/v1/admin/trainers
 * Trainer package list + KV storage usage for the admin「修改器包」tab.
 */

import {
  getDb, getKv, json, isMissingTable, toIso, downloadPath,
  KV_QUOTA_BYTES, MAX_FILE_SIZE, CHUNK_SIZE, ALLOWED_EXTENSIONS
} from '../../trainers/_store.js';

export async function onRequestGet(context) {
  const { env } = context;
  const db = getDb(env);
  const kv = getKv(env);

  const storage = {
    enabled: Boolean(kv),
    tableReady: true,
    usedBytes: 0,
    quotaBytes: KV_QUOTA_BYTES,
    maxFileBytes: MAX_FILE_SIZE,
    chunkBytes: CHUNK_SIZE,
    allowedExtensions: ALLOWED_EXTENSIONS
  };

  if (!db) {
    return json({ code: 50000, message: 'Database binding missing' }, 500);
  }

  try {
    const { results } = await db.prepare(
      `SELECT id, game_id, fling_page_url, trainer_version, game_version, file_name, content_type,
              size, sha256, chunks, kv_prefix, status, uploaded_at, note
         FROM trainer_packages
        ORDER BY CASE status WHEN 'active' THEN 0 WHEN 'uploading' THEN 1 ELSE 2 END, uploaded_at DESC
        LIMIT 300`
    ).all();

    const packages = (results || []).map(r => ({
      ...r,
      uploaded_at: toIso(r.uploaded_at),
      download_path: r.status === 'active' ? downloadPath(r.game_id, r.file_name) : null
    }));

    // Withdrawn packages have their chunks deleted, so only active + unfinished uploads occupy KV.
    storage.usedBytes = packages
      .filter(p => p.status === 'active' || p.status === 'uploading')
      .reduce((sum, p) => sum + (Number(p.size) || 0), 0);
    storage.activeCount = packages.filter(p => p.status === 'active').length;

    return json({ code: 0, data: { storage, packages } });
  } catch (err) {
    if (isMissingTable(err)) {
      storage.tableReady = false;
      return json({
        code: 0,
        message: 'trainer_packages 表还没建（migration_v7 未执行）',
        data: { storage, packages: [] }
      });
    }
    return json({ code: 50000, message: '读取修改器包列表失败', details: err.message }, 500);
  }
}
