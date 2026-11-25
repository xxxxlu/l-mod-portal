/**
 * Cloudflare Pages Function: GET /api/v1/admin/games/:id/revisions
 * 后台游戏编辑器的历史版本（每次保存前的整份 raw_json 存在 game_doc_revisions）。
 *
 *   GET …/revisions               最近 50 个版本的列表（不带正文）
 *   GET …/revisions?revision_id=N 取一个版本的整份文档；编辑器载入后要再点保存才会生效
 */

import { jsonResponse } from '../../../catalog/_game_doc.js';

export async function onRequestGet(context) {
  const { params, env, request } = context;
  const gameId = String(params.id || '');
  const db = env.DB || env.lmod_vault_db;
  const noStore = { 'Cache-Control': 'no-store' };
  if (!db) return jsonResponse({ code: 50000, message: 'Database binding missing' }, 500, noStore);

  try {
    const revisionId = new URL(request.url).searchParams.get('revision_id');
    if (revisionId) {
      const row = await db.prepare(
        'SELECT id, game_id, rev, raw_json, admin_user, created_at FROM game_doc_revisions WHERE id = ? AND game_id = ?'
      ).bind(Number(revisionId), gameId).first();
      if (!row) return jsonResponse({ code: 40400, message: 'Revision not found' }, 404, noStore);
      const { raw_json, ...meta } = row;
      return jsonResponse({ code: 0, message: 'success', data: { ...meta, doc: JSON.parse(raw_json) } }, 200, noStore);
    }

    const { results } = await db.prepare(
      `SELECT id, rev, admin_user, created_at, length(raw_json) AS bytes
         FROM game_doc_revisions WHERE game_id = ? ORDER BY id DESC LIMIT 50`
    ).bind(gameId).all();
    return jsonResponse({ code: 0, message: 'success', data: { game_id: gameId, revisions: results || [] } }, 200, noStore);
  } catch (err) {
    return jsonResponse({ code: 50000, message: 'Failed to read revisions', details: err.message }, 500, noStore);
  }
}
