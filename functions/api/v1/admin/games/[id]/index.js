/**
 * Cloudflare Pages Function: GET /api/v1/admin/games/:id
 * 后台游戏编辑器：读一款游戏的整份数据（D1 games.raw_json，原样，不叠加）。
 *
 * 返回：
 *   doc      库里的整份文档（编辑器在它上面改，保存时整份交回 POST /api/v1/admin/games/save）
 *   rev      games.content_rev（保存时作为 base_rev 交回，防止两个窗口互相覆盖）
 *   machine  机器维护字段的「对外实际值」：雷达看 public/radar_status.json，修改器看 public/trainers.json。
 *            这些字段后台改不了（保存时一律保留库里原值），这里只给编辑器显示。
 */

import { loadRadarStatus, radarApiObject, radarEntry } from '../../../../_radar_status.js';
import { MACHINE_FIELDS, jsonResponse, loadTrainers, trainerFieldsFor } from '../../../catalog/_game_doc.js';

export async function onRequestGet(context) {
  const { params, env } = context;
  const gameId = String(params.id || '');
  const db = env.DB || env.lmod_vault_db;
  const noStore = { 'Cache-Control': 'no-store' };

  if (!db) return jsonResponse({ code: 50000, message: 'Database binding missing' }, 500, noStore);
  if (!gameId) return jsonResponse({ code: 40000, message: 'Missing game ID parameter' }, 400, noStore);

  try {
    const row = await db.prepare(
      `SELECT id, raw_json, is_hidden, content_rev, updated_at,
              (SELECT count(*) FROM console_commands WHERE game_id = games.id) AS command_rows,
              (SELECT count(*) FROM scenario_bundles WHERE game_id = games.id) AS bundle_rows
         FROM games WHERE id = ?`
    ).bind(gameId).first();
    if (!row) return jsonResponse({ code: 40400, message: `Game '${gameId}' not found` }, 404, noStore);

    let doc = null;
    try {
      doc = JSON.parse(row.raw_json || 'null');
    } catch (e) {
      doc = null;
    }

    const [radarStatus, trainers] = await Promise.all([loadRadarStatus(context), loadTrainers(context)]);
    const entry = radarEntry(radarStatus, gameId);

    return jsonResponse({
      code: 0,
      message: 'success',
      data: {
        id: row.id,
        rev: row.content_rev,
        is_hidden: Boolean(row.is_hidden),
        updated_at: row.updated_at,
        doc,
        derived: { command_rows: row.command_rows, bundle_rows: row.bundle_rows },
        machine: {
          fields: MACHINE_FIELDS,
          radar: radarApiObject(entry, radarStatus),
          radar_source: radarStatus ? 'radar_status.json' : null,
          radar_updated_at: radarStatus ? radarStatus.updatedAt : null,
          trainer: trainers ? trainerFieldsFor(gameId, trainers) : null,
          trainers_generated_at: trainers ? trainers.generatedAt : null
        }
      }
    }, 200, noStore);
  } catch (err) {
    return jsonResponse({ code: 50000, message: 'Failed to fetch game details', details: err.message }, 500, noStore);
  }
}
