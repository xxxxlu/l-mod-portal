/**
 * Cloudflare Pages Function: POST /api/v1/admin/games/save
 * 后台游戏编辑器：整份保存一款游戏（或新建一款）。保存后网站下一次加载就能看到。
 *
 * 请求体：
 *   { "doc": { …整份游戏数据… }, "base_rev": 3 }     改已有的游戏（base_rev = 打开编辑器时拿到的 rev）
 *   { "doc": { … }, "create": true }                  新建（id 已存在——包括被隐藏的——会被拒绝）
 *   加 "dry_run": true 只校验、不写库
 *
 * 规则：
 *   - raw_json 是唯一真源。games 表其它列、console_commands、scenario_bundles 从它重新生成，
 *     和 raw_json 写在同一个 D1 batch（事务）里，要么全成要么全不成。
 *   - 雷达 / 修改器字段归每天的定时任务，交上来的值一律忽略，保留库里原值。
 *   - 校验见 ../../catalog/_game_doc.js validateGameDoc：结构错、新写进去的「实测 / 100% 安全」类说法 → 422。
 *   - 保存前的版本存进 game_doc_revisions；写 admin_audit_logs；system_settings.catalog_version +1（公开接口的缓存随之失效）。
 *   - 绝不 DELETE / REPLACE games 的行：user_favorites / user_radar_subscriptions 对它 ON DELETE CASCADE。
 */

import { logAdminAction } from '../_auth.js';
import {
  bumpCatalogVersionStmt, bundleRows, changedFields, commandRows, gameColumns, jsonResponse,
  mergeMachineFields, validateGameDoc
} from '../../catalog/_game_doc.js';

const COMMAND_COLS = ['id', 'game_id', 'category_id', 'category_name_zh', 'category_name_en', 'name_zh', 'name_en',
  'code', 'description', 'syntax_type', 'is_popular'];
const BUNDLE_COLS = ['id', 'game_id', 'name', 'description', 'commands_json', 'bat_script'];

// 一整组行作为一个 JSON 参数交给 SQLite 展开：免费版每次调用最多 50 条查询、每条最多 100 个绑定参数
function insertFromJson(db, table, cols, rows) {
  const select = cols.map(c => `json_extract(value, '$.${c}')`).join(', ');
  return db.prepare(`INSERT INTO ${table} (${cols.join(', ')}) SELECT ${select} FROM json_each(?)`)
    .bind(JSON.stringify(rows));
}

async function idCollisions(db, table, gameId, ids) {
  if (!ids.length) return [];
  const { results } = await db.prepare(
    `SELECT id, game_id FROM ${table} WHERE game_id != ? AND id IN (SELECT value FROM json_each(?))`
  ).bind(gameId, JSON.stringify(ids)).all();
  return results || [];
}

const isPlainObject = v => Boolean(v) && typeof v === 'object' && !Array.isArray(v);

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  const adminUser = (data && data.admin && data.admin.username) || 'admin';
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';
  if (!db) return jsonResponse({ code: 50000, message: 'Database binding missing' }, 500);

  let body;
  try {
    body = await request.json();
  } catch (e) {
    return jsonResponse({ code: 40000, message: '请求体不是 JSON' }, 400);
  }
  const { doc: incoming, base_rev: baseRev, create = false, dry_run: dryRun = false } = body || {};
  if (!isPlainObject(incoming) || typeof incoming.id !== 'string' || !incoming.id) {
    return jsonResponse({ code: 40000, message: 'doc 必须是带 id 的整份游戏数据' }, 400);
  }
  const gameId = incoming.id;

  try {
    const row = await db.prepare('SELECT raw_json, content_rev, is_hidden FROM games WHERE id = ?').bind(gameId).first();
    if (create && row) {
      return jsonResponse({
        code: 40900,
        message: `id「${gameId}」已经存在${row.is_hidden ? '（是一款被隐藏的游戏，去列表里取消隐藏即可）' : ''}，换一个 id`
      }, 409);
    }
    if (!create && !row) return jsonResponse({ code: 40400, message: `游戏「${gameId}」不存在` }, 404);
    if (!create && Number(baseRev) !== row.content_rev) {
      return jsonResponse({
        code: 40901,
        message: `这款游戏在你打开编辑器之后被保存过（你的版本 ${baseRev}，库里 ${row.content_rev}），重新打开再改，免得覆盖别人的修改`,
        data: { current_rev: row.content_rev }
      }, 409);
    }

    let stored = null;
    if (row) {
      try {
        stored = JSON.parse(row.raw_json || 'null');
      } catch (e) {
        stored = null;
      }
    }
    const doc = mergeMachineFields(incoming, stored);
    const { errors, warnings } = validateGameDoc(doc, stored);

    const commands = commandRows(doc);
    const bundles = bundleRows(doc);
    const dupCmd = commands.map(c => c.id).filter((id, i, a) => a.indexOf(id) !== i);
    if (dupCmd.length) errors.push(`指令 id 重复（含自动生成的常用指令 id）：${[...new Set(dupCmd)].join(', ')}`);
    for (const c of await idCollisions(db, 'console_commands', gameId, commands.map(c => c.id))) {
      errors.push(`指令 id「${c.id}」已经被游戏「${c.game_id}」用了（指令 id 全站唯一），换一个`);
    }
    for (const b of await idCollisions(db, 'scenario_bundles', gameId, bundles.map(b => b.id))) {
      errors.push(`套餐 id「${b.id}」已经被游戏「${b.game_id}」用了（套餐 id 全站唯一），换一个`);
    }

    const changed = changedFields(stored, doc);
    if (errors.length) {
      return jsonResponse({ code: 42200, message: `有 ${errors.length} 处问题，没有保存`, data: { errors, warnings } }, 422);
    }
    if (dryRun) {
      return jsonResponse({ code: 0, message: '检查通过（没有保存）', data: { dry_run: true, warnings, changed_fields: changed } });
    }
    if (!create && !changed.length) {
      return jsonResponse({ code: 0, message: '没有改动，不用保存', data: { id: gameId, rev: row.content_rev, warnings, changed_fields: [] } });
    }

    const cols = gameColumns(doc);
    const colNames = Object.keys(cols);
    const rawJson = JSON.stringify(doc);
    const stmts = [];
    if (create) {
      stmts.push(db.prepare(
        `INSERT INTO games (id, ${colNames.join(', ')}, raw_json, is_hidden, content_rev, created_at, updated_at)
         VALUES (?, ${colNames.map(() => '?').join(', ')}, ?, 0, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)`
      ).bind(gameId, ...colNames.map(c => cols[c]), rawJson));
    } else {
      // 事务里再确认一次版本：不对就让 json() 报错，整个 batch 回滚（D1 的 batch 是一个事务）
      stmts.push(db.prepare(
        `SELECT json(CASE WHEN (SELECT content_rev FROM games WHERE id = ?) = ? THEN '1' ELSE 'rev-conflict' END)`
      ).bind(gameId, row.content_rev));
      stmts.push(db.prepare(
        `INSERT INTO game_doc_revisions (game_id, rev, raw_json, admin_user)
         SELECT id, content_rev, raw_json, ? FROM games WHERE id = ?`
      ).bind(adminUser, gameId));
      stmts.push(db.prepare(
        `UPDATE games SET ${colNames.map(c => `${c} = ?`).join(', ')}, raw_json = ?,
                content_rev = content_rev + 1, updated_at = CURRENT_TIMESTAMP
          WHERE id = ?`
      ).bind(...colNames.map(c => cols[c]), rawJson, gameId));
    }
    stmts.push(db.prepare('DELETE FROM console_commands WHERE game_id = ?').bind(gameId));
    stmts.push(db.prepare('DELETE FROM scenario_bundles WHERE game_id = ?').bind(gameId));
    if (commands.length) stmts.push(insertFromJson(db, 'console_commands', COMMAND_COLS, commands));
    if (bundles.length) stmts.push(insertFromJson(db, 'scenario_bundles', BUNDLE_COLS, bundles));
    stmts.push(db.prepare(
      `INSERT INTO admin_audit_logs (action, entity, entity_id, details, admin_user, client_ip) VALUES (?, 'games', ?, ?, ?, ?)`
    ).bind(
      create ? 'create_game_doc' : 'update_game_doc',
      gameId,
      JSON.stringify({
        title_zh: (doc.titles && doc.titles['zh-CN']) || doc.title,
        rev_from: create ? null : row.content_rev,
        rev_to: create ? 1 : row.content_rev + 1,
        changed_fields: changed,
        commands: commands.length,
        bundles: bundles.length,
        warnings: warnings.length
      }),
      adminUser,
      clientIP
    ));
    stmts.push(bumpCatalogVersionStmt(db));

    try {
      await db.batch(stmts);
    } catch (err) {
      const msg = String(err && err.message || err);
      if (/malformed JSON/i.test(msg)) {
        return jsonResponse({ code: 40901, message: '保存时这款游戏刚被别处改过，没有保存；重新打开再改' }, 409);
      }
      if (/UNIQUE constraint failed: games\.id/i.test(msg)) {
        return jsonResponse({ code: 40900, message: `id「${gameId}」已经存在，换一个 id` }, 409);
      }
      throw err;
    }

    return jsonResponse({
      code: 0,
      message: create ? `已新建「${(doc.titles && doc.titles['zh-CN']) || doc.title}」，刷新网站即可看到`
        : `已保存「${(doc.titles && doc.titles['zh-CN']) || doc.title}」，刷新网站即可看到`,
      data: {
        id: gameId,
        rev: create ? 1 : row.content_rev + 1,
        warnings,
        changed_fields: changed,
        commands: commands.length,
        bundles: bundles.length
      }
    });
  } catch (err) {
    return jsonResponse({ code: 50000, message: '保存失败', details: err.message }, 500);
  }
}
