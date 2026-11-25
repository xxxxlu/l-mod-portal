/**
 * Cloudflare Pages Function: POST /api/v1/admin/trainers/init
 * Step 1 of an upload: validate the metadata (SHA-256 already computed in the browser) and
 * create an `uploading` row. The browser then PUTs each chunk and calls /commit.
 *
 * Body: { game_id, file_name, size, sha256, trainer_version?, game_version?, fling_page_url?, note? }
 */

import { logAdminAction } from '../_auth.js';
import {
  getDb, getKv, json, isMissingTable, isGameId, isSha256, newPackageId, chunkCount,
  cleanFileName, fileExtension, ALLOWED_EXTENSIONS, MAX_FILE_SIZE, KV_QUOTA_BYTES, CHUNK_SIZE
} from '../../trainers/_store.js';

const CONTENT_TYPES = {
  '.zip': 'application/zip',
  '.exe': 'application/vnd.microsoft.portable-executable',
  '.rar': 'application/vnd.rar',
  '.7z': 'application/x-7z-compressed'
};

function text(v, max) {
  return typeof v === 'string' ? v.trim().slice(0, max) : '';
}

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = getDb(env);
  const kv = getKv(env);
  const admin = data?.admin || { username: '老L·站长' };
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);
  if (!kv) return json({ code: 50301, message: '存储未开通：TRAINER_FILES 这个 KV 绑定还没建' }, 503);

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ code: 40000, message: '请求体不是合法 JSON' }, 400);
  }

  const gameId = text(body.game_id, 80);
  const fileName = cleanFileName(body.file_name);
  const ext = fileExtension(fileName);
  const size = Number(body.size);
  const sha256 = text(body.sha256, 64).toLowerCase();
  const pageUrl = text(body.fling_page_url, 500);

  if (!isGameId(gameId)) return json({ code: 40001, message: '游戏 ID 不合法' }, 400);
  if (!fileName || !ALLOWED_EXTENSIONS.includes(ext)) {
    return json({ code: 40002, message: `只接受 ${ALLOWED_EXTENSIONS.join(' / ')} 文件` }, 400);
  }
  if (!Number.isInteger(size) || size <= 0) return json({ code: 40003, message: '文件大小不合法' }, 400);
  if (size > MAX_FILE_SIZE) {
    return json({ code: 41300, message: `文件超过 ${Math.round(MAX_FILE_SIZE / 1048576)} MB 上限` }, 413);
  }
  if (!isSha256(sha256)) return json({ code: 40004, message: 'SHA-256 必须是 64 位小写十六进制' }, 400);
  if (pageUrl && !/^https:\/\/(www\.)?flingtrainer\.com\//.test(pageUrl)) {
    return json({ code: 40005, message: '官网页面必须是 https://flingtrainer.com/ 下的地址' }, 400);
  }

  try {
    // The game must exist (the games table is the catalogue of record).
    const game = await db.prepare('SELECT id FROM games WHERE id = ?').bind(gameId).first();
    if (!game) return json({ code: 40006, message: `游戏 ${gameId} 不在 games 表里` }, 400);

    const active = await db.prepare(
      "SELECT id, sha256 FROM trainer_packages WHERE game_id = ? AND status = 'active'"
    ).bind(gameId).first();
    if (active && active.sha256 === sha256) {
      return json({ code: 40901, message: '和当前上架的文件完全一样（SHA-256 相同），不用重复上传' }, 409);
    }

    const used = await db.prepare(
      "SELECT COALESCE(SUM(size), 0) AS used FROM trainer_packages WHERE status IN ('active', 'uploading')"
    ).first();
    // A replaced package frees its space only after the new one is committed, so count both.
    if ((Number(used && used.used) || 0) + size > KV_QUOTA_BYTES) {
      return json({ code: 41301, message: 'KV 空间不够（免费额度 1 GB），先下架不用的包' }, 413);
    }

    const id = newPackageId();
    const chunks = chunkCount(size);
    const kvPrefix = `pkg/${id}`;

    await db.prepare(
      `INSERT INTO trainer_packages
         (id, game_id, fling_page_url, trainer_version, game_version, file_name, content_type,
          size, sha256, chunks, kv_prefix, status, note)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'uploading', ?)`
    ).bind(
      id, gameId, pageUrl || null, text(body.trainer_version, 120) || null, text(body.game_version, 120) || null,
      fileName, CONTENT_TYPES[ext] || 'application/octet-stream', size, sha256, chunks, kvPrefix,
      text(body.note, 500) || null
    ).run();

    await logAdminAction(db, {
      action: 'trainer_upload_start',
      entity: 'trainer_packages',
      entity_id: id,
      details: { game_id: gameId, file_name: fileName, size, sha256, chunks },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return json({ code: 0, message: '已登记，开始上传分片', data: { id, chunks, chunkSize: CHUNK_SIZE, fileName } });
  } catch (err) {
    if (isMissingTable(err)) {
      return json({ code: 50302, message: 'trainer_packages 表还没建（migration_v7 未执行）' }, 503);
    }
    return json({ code: 50000, message: '登记上传失败', details: err.message }, 500);
  }
}
