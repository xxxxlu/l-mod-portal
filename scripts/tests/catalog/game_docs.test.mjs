/**
 * Tests for the D1-as-source game data: public catalog endpoints, admin editor endpoints,
 * validation and the derived tables.
 *
 * Run: node --test scripts/tests/catalog/
 * (Node 22.13+ for node:sqlite; python3 for the seed, same as scripts/tests/db.)
 */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { after, before, describe, test } from 'node:test';

import { REPO, assetsFromPublic, makeDatabase, python, readGamesData } from './d1_shim.mjs';

const lib = await import(path.join(REPO, 'functions/api/v1/catalog/_game_doc.js'));
const catalogList = await import(path.join(REPO, 'functions/api/v1/catalog/index.js'));
const catalogGame = await import(path.join(REPO, 'functions/api/v1/catalog/[id].js'));
const adminGame = await import(path.join(REPO, 'functions/api/v1/admin/games/[id]/index.js'));
const adminList = await import(path.join(REPO, 'functions/api/v1/admin/games/index.js'));
const adminSave = await import(path.join(REPO, 'functions/api/v1/admin/games/save.js'));
const adminVisibility = await import(path.join(REPO, 'functions/api/v1/admin/games/visibility.js'));
const adminRevisions = await import(path.join(REPO, 'functions/api/v1/admin/games/[id]/revisions.js'));
const oldGamesList = await import(path.join(REPO, 'functions/api/v1/games/index.js'));

const GAMES = readGamesData();
const BY_ID = Object.fromEntries(GAMES.map(g => [g.id, g]));
// Old radar keys the API never returns (see functions/api/_radar_status.js)
const STRIPPED = ['verifiedPatch', 'radarRiskTitle', 'radarRiskDesc', 'emergencyAlert'];

let tmp;
let db;
let env;

function ctx(url, { method = 'GET', body, headers = {}, params = {} } = {}) {
  const init = { method, headers: { 'Content-Type': 'application/json', ...headers } };
  if (body !== undefined) init.body = JSON.stringify(body);
  return { request: new Request(`http://127.0.0.1:8788${url}`, init), env, params, data: { admin: { username: 'tester' } } };
}

async function json(res) {
  return { status: res.status, body: res.status === 304 ? null : await res.json(), headers: res.headers };
}

const getCatalog = (headers) => catalogList.onRequestGet(ctx('/api/v1/catalog', { headers })).then(json);
const getGame = (id, headers) => catalogGame.onRequestGet(ctx(`/api/v1/catalog/${id}`, { headers, params: { id } })).then(json);
const getAdminGame = id => adminGame.onRequestGet(ctx(`/api/v1/admin/games/${id}`, { params: { id } })).then(json);
const save = body => adminSave.onRequestPost(ctx('/api/v1/admin/games/save', { method: 'POST', body })).then(json);
const setHidden = (id, hidden) =>
  adminVisibility.onRequestPost(ctx('/api/v1/admin/games/visibility', { method: 'POST', body: { id, hidden } })).then(json);
const clone = v => JSON.parse(JSON.stringify(v));

before(() => {
  tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'lmod-catalog-'));
  db = makeDatabase(tmp);
  env = { DB: db, ASSETS: assetsFromPublic() };
});

after(() => {
  fs.rmSync(tmp, { recursive: true, force: true });
});

describe('public catalog', () => {
  test('list = data.js without the heavy fields, radar/trainer overlaid, with counts', async () => {
    const { status, body, headers } = await getCatalog();
    assert.equal(status, 200);
    assert.equal(headers.get('Access-Control-Allow-Origin'), '*');
    assert.match(headers.get('Cache-Control'), /max-age=0/);
    const games = body.data.games;
    assert.equal(games.length, GAMES.length);
    for (const item of games) {
      const g = BY_ID[item.id];
      for (const [k, v] of Object.entries(item)) {
        if (k === 'commandCount' || k === 'modCount') continue;
        assert.deepEqual(v, g[k], `${item.id}.${k}`);
      }
      for (const k of lib.LIST_OMITTED_FIELDS) {
        if (['compatibilityStatus', 'radarReason', 'radarStatusText', 'latestSteamPatch', 'latestSteamPatchUrl',
          'steamBuildId', 'steamBuildUpdatedAt', 'steamLastChecked', 'radarFramework', 'radarAdvice', 'radarSummary'].includes(k)) continue;
        assert.ok(!(k in item), `${item.id} should not carry ${k}`);
      }
      const cmds = (g.consoleCategories || []).reduce((n, c) => n + c.commands.length, 0);
      assert.equal(item.commandCount, cmds, `${item.id} commandCount`);
      assert.equal(item.modCount, (g.curatedMods || []).length, `${item.id} modCount`);
    }
  });

  test('ETag answers 304 and is weak-tolerant', async () => {
    const first = await getCatalog();
    const etag = first.headers.get('ETag');
    assert.ok(etag);
    assert.equal((await getCatalog({ 'If-None-Match': etag })).status, 304);
    assert.equal((await getCatalog({ 'If-None-Match': `W/${etag}` })).status, 304);
    assert.equal((await getCatalog({ 'If-None-Match': '"other"' })).status, 200);
  });

  test('one game = the data.js entry (old radar keys stripped)', async () => {
    for (const id of ['cyberpunk-2077', 'witcher-3', 'elden-ring', GAMES[GAMES.length - 1].id]) {
      const { status, body } = await getGame(id);
      assert.equal(status, 200);
      const expected = Object.fromEntries(Object.entries(BY_ID[id]).filter(([k]) => !STRIPPED.includes(k)));
      assert.deepEqual(body.data.game, expected, id);
    }
    assert.equal((await getGame('no-such-game')).status, 404);
    assert.equal((await getGame('Bad_ID')).status, 400);
  });

  test('without radar_status.json / trainers.json the stored values are served', async () => {
    const saved = env.ASSETS;
    env.ASSETS = assetsFromPublic({ '/radar_status.json': null, '/trainers.json': null });
    try {
      const { body } = await getGame('witcher-3');
      assert.equal(body.data.game.hasTrainer, BY_ID['witcher-3'].hasTrainer);
      assert.deepEqual(body.data.game.trainerInfo, BY_ID['witcher-3'].trainerInfo);
    } finally {
      env.ASSETS = saved;
    }
  });
});

describe('derived rows match scripts/sync_to_database.py', () => {
  test('games columns, console_commands and scenario_bundles', () => {
    const py = JSON.parse(python(
      'import json, sync_to_database as s\n' +
      'games, _ = s.load_games()\n' +
      'out = {}\n' +
      'for g in games:\n' +
      '    v = s.game_values(g)\n' +
      '    v.pop("raw_json")\n' +
      '    for k in ("verified_patch","latest_steam_patch","compatibility_status","radar_risk_title","radar_risk_desc","radar_summary"): v.pop(k)\n' +
      '    out[g["id"]] = {"cols": v, "cmds": list(s.command_rows(g)), "bundles": list(s.bundle_rows(g))}\n' +
      'print(json.dumps(out, ensure_ascii=False))'
    ));
    for (const g of GAMES) {
      const cols = lib.gameColumns(g);
      const p = py[g.id];
      for (const [k, v] of Object.entries(p.cols)) {
        const mine = k === 'titles_json' ? JSON.parse(cols[k]) : cols[k];
        const theirs = typeof v === 'boolean' ? (v ? 1 : 0) : v;
        assert.deepEqual(mine, theirs, `${g.id} games.${k}`);
      }
      assert.deepEqual(lib.commandRows(g), p.cmds.map(c => ({ ...c })), `${g.id} console_commands`);
      assert.deepEqual(lib.bundleRows(g).map(b => ({ ...b, commands_json: JSON.parse(b.commands_json) })),
        p.bundles, `${g.id} scenario_bundles`);
    }
  });
});

describe('validation', () => {
  test('every game in data.js passes unchanged; brand-new copies only fail on real claims', () => {
    for (const g of GAMES) {
      assert.deepEqual(lib.validateGameDoc(g, g).errors, [], g.id);
    }
  });

  test('claims are blocked, negated wording is allowed', () => {
    const claims = s => lib.findClaims(s).map(h => h.phrase);
    assert.deepEqual(claims('指令没有逐条在游戏里实测，执行前先存档'), []);
    assert.deepEqual(claims('v1.14（未实测）'), []);
    assert.deepEqual(claims('它是第三方 Mod，会不会被封号没有人能担保'), []);
    assert.deepEqual(claims('没有人能担保不会被封号'), []);
    assert.deepEqual(claims('渲染分辨率 100%'), []);
    assert.ok(claims('所有指令均已实测').includes('实测'));
    assert.ok(claims('100% 安全防封').length > 0);
    assert.ok(claims('零风险，绝无封号').length >= 2);
    assert.ok(claims('完美兼容 Patch 7').length > 0);
    assert.ok(claims('Fully tested and guaranteed').length > 0);
    assert.deepEqual(claims('nothing here can guarantee you won\'t be banned'), []);
  });

  test('structure problems', () => {
    const g = clone(BY_ID['witcher-3']);
    g.consoleCategories[0].commands[0].source = 'http://not-https.example.org/x';
    g.curatedMods.push({ id: 'x', title: 'X' });
    g.titles['zh-CN'] = '';
    g.heatTier = 'gold';
    const { errors } = lib.validateGameDoc(g, BY_ID['witcher-3']);
    assert.ok(errors.some(e => e.includes('不是 https')), errors.join('\n'));
    assert.ok(errors.some(e => e.includes('缺 id / title / author')));
    assert.ok(errors.some(e => e.includes('titles.zh-CN')));
    assert.ok(errors.some(e => e.includes('heatTier')));
  });
});

describe('admin editor', () => {
  test('save: whole doc, machine fields kept, derived tables rebuilt, version bumped, history kept', async () => {
    const id = 'witcher-3';
    const before = await getAdminGame(id);
    assert.equal(before.status, 200);
    const { rev, doc } = before.body.data;
    const etagBefore = (await getCatalog()).headers.get('ETag');
    const versionBefore = db.scalar("SELECT json_extract(value, '$.version') FROM system_settings WHERE key = 'catalog_version'");

    const edited = clone(doc);
    edited.pitfallNote = { title: '避坑笔记（测试）', tips: ['先备份存档。'] };
    edited.consoleCategories[0].commands[0].desc = '测试改过的说明';
    edited.hasTrainer = false;                 // machine field: ignored
    edited.compatibilityStatus = 'red';        // machine field: ignored
    const res = await save({ doc: edited, base_rev: rev });
    assert.equal(res.status, 200, JSON.stringify(res.body));
    assert.equal(res.body.data.rev, rev + 1);
    assert.deepEqual(res.body.data.changed_fields, ['consoleCategories', 'pitfallNote']);

    const stored = JSON.parse(db.scalar('SELECT raw_json FROM games WHERE id = ?', id));
    assert.equal(stored.hasTrainer, doc.hasTrainer);
    assert.equal(stored.compatibilityStatus, doc.compatibilityStatus);
    assert.deepEqual(Object.keys(stored), Object.keys(doc), 'field order kept');
    assert.equal(db.scalar('SELECT pitfall_note FROM games WHERE id = ?', id), '避坑笔记（测试）\n先备份存档。');
    const cmdId = doc.consoleCategories[0].commands[0].id;
    assert.equal(db.scalar('SELECT description FROM console_commands WHERE id = ?', cmdId), '测试改过的说明');
    assert.equal(db.scalar('SELECT count(*) FROM console_commands WHERE game_id = ?', id), lib.commandRows(stored).length);
    assert.equal(db.scalar('SELECT count(*) FROM game_doc_revisions WHERE game_id = ? AND rev = ?', id, rev), 1);
    assert.equal(db.scalar("SELECT count(*) FROM admin_audit_logs WHERE action = 'update_game_doc' AND entity_id = ?", id), 1);
    assert.equal(db.scalar("SELECT json_extract(value, '$.version') FROM system_settings WHERE key = 'catalog_version'"), versionBefore + 1);

    const after = await getCatalog();
    assert.notEqual(after.headers.get('ETag'), etagBefore);
    const pub = await getGame(id);
    assert.deepEqual(pub.body.data.game.pitfallNote, edited.pitfallNote);

    // history: the stored revision is the old doc
    const list = await adminRevisions.onRequestGet(ctx(`/api/v1/admin/games/${id}/revisions`, { params: { id } })).then(json);
    const revId = list.body.data.revisions[0].id;
    const one = await adminRevisions.onRequestGet(ctx(`/api/v1/admin/games/${id}/revisions?revision_id=${revId}`, { params: { id } })).then(json);
    assert.deepEqual(one.body.data.doc, doc);

    // restore it through a normal save
    const restore = await save({ doc: one.body.data.doc, base_rev: rev + 1 });
    assert.equal(restore.status, 200);
    assert.deepEqual(JSON.parse(db.scalar('SELECT raw_json FROM games WHERE id = ?', id)), doc);
  });

  test('stale base_rev is rejected before anything is written', async () => {
    const { rev, doc } = (await getAdminGame('elden-ring')).body.data;
    const res = await save({ doc, base_rev: rev - 1 });
    assert.equal(res.status, 409);
  });

  test('a save that loses a race inside the transaction rolls back completely', async () => {
    const id = 'skyrim-se';
    const { rev, doc } = (await getAdminGame(id)).body.data;
    const rawBefore = db.scalar('SELECT raw_json FROM games WHERE id = ?', id);
    const cmdsBefore = db.scalar('SELECT count(*) FROM console_commands WHERE game_id = ?', id);
    const edited = clone(doc);
    edited.consoleCategories = edited.consoleCategories.slice(0, 1);
    db.beforeBatch = () => db.db.exec(`UPDATE games SET content_rev = content_rev + 1 WHERE id = '${id}'`);
    try {
      const res = await save({ doc: edited, base_rev: rev });
      assert.equal(res.status, 409, JSON.stringify(res.body));
    } finally {
      db.beforeBatch = null;
    }
    assert.equal(db.scalar('SELECT raw_json FROM games WHERE id = ?', id), rawBefore);
    assert.equal(db.scalar('SELECT count(*) FROM console_commands WHERE game_id = ?', id), cmdsBefore);
    db.db.exec(`UPDATE games SET content_rev = ${rev} WHERE id = '${id}'`);
  });

  test('new claims are rejected; claims already in the old data only warn', async () => {
    const { rev, doc } = (await getAdminGame('cyberpunk-2077')).body.data;
    const bad = clone(doc);
    bad.consoleEnableGuide['zh-CN'] += '\n所有指令 100% 安全，已实测。';
    const res = await save({ doc: bad, base_rev: rev });
    assert.equal(res.status, 422);
    assert.ok(res.body.data.errors.some(e => e.includes('100% 安全')));
    assert.ok(res.body.data.errors.some(e => e.includes('实测')));

    const ok = clone(doc);
    ok.aliases = [...ok.aliases, '2077测试'];
    const res2 = await save({ doc: ok, base_rev: rev, dry_run: true });
    assert.equal(res2.status, 200);
    assert.ok(res2.body.data.warnings.some(w => w.includes('全版本兼容')), 'old latestPatch wording is a warning');
    assert.equal(db.scalar('SELECT content_rev FROM games WHERE id = ?', 'cyberpunk-2077'), rev, 'dry run writes nothing');
  });

  test('command ids are unique across games', async () => {
    const { rev, doc } = (await getAdminGame('witcher-3')).body.data;
    const other = BY_ID['cyberpunk-2077'].consoleCategories[0].commands[0].id;
    const bad = clone(doc);
    bad.consoleCategories[0].commands[0].id = other;
    const res = await save({ doc: bad, base_rev: rev });
    assert.equal(res.status, 422);
    assert.ok(res.body.data.errors.some(e => e.includes(other)));
  });

  test('create a game, then hide it: never deletes rows, favorites survive', async () => {
    const newDoc = {
      id: 'test-new-game', rank: 101, title: 'Test New Game',
      titles: { 'zh-CN': '测试新游戏', en: 'Test New Game' },
      aliases: ['测试'], developer: 'Test Studio', releaseYear: 2026, genre: 'Action', steamRating: '',
      hasConsole: false, consoleShortcut: '', consoleEnableGuide: { 'zh-CN': '', en: '' }, popularCommands: [],
      hasMods: false, modInstallPath: '', mustHaveMods: [], consoleCategories: [], curatedMods: [],
      communityReviews: [], steamAppId: 0, headerImage: '', radarSecretCode: '', lastUpdated: '2026-11-23',
      heatTier: 'emerald', scenarioBundles: [], pitfallNote: null,
      hasTrainer: true // machine field: forced to false on create
    };
    const created = await save({ doc: newDoc, create: true });
    assert.equal(created.status, 200, JSON.stringify(created.body));
    assert.equal((await save({ doc: newDoc, create: true })).status, 409);
    const stored = JSON.parse(db.scalar('SELECT raw_json FROM games WHERE id = ?', 'test-new-game'));
    assert.equal(stored.hasTrainer, false);
    assert.ok((await getCatalog()).body.data.games.some(g => g.id === 'test-new-game'));
    assert.equal((await getGame('test-new-game')).status, 200);

    // hide a game players have favorited / subscribed to
    db.db.exec("INSERT OR IGNORE INTO users (id, provider, nickname) VALUES ('u-test', 'email', 't')");
    db.db.exec("INSERT OR IGNORE INTO user_favorites (user_id, game_id) VALUES ('u-test', 'elden-ring')");
    db.db.exec("INSERT INTO user_radar_subscriptions (user_id, game_id, notify_target) VALUES ('u-test', 'elden-ring', 'x')");
    const counts = () => [
      db.scalar('SELECT count(*) FROM games'),
      db.scalar('SELECT count(*) FROM user_favorites'),
      db.scalar('SELECT count(*) FROM user_radar_subscriptions')
    ];
    const before = counts();
    assert.equal((await setHidden('elden-ring', true)).status, 200);
    assert.deepEqual(counts(), before);
    assert.ok(!(await getCatalog()).body.data.games.some(g => g.id === 'elden-ring'));
    assert.equal((await getGame('elden-ring')).status, 404);
    const old = await oldGamesList.onRequestGet(ctx('/api/v1/games?page_size=50&page=1')).then(json);
    assert.equal(old.body.meta.total, GAMES.length); // 100 + test-new-game - elden-ring
    const adminRows = await adminList.onRequestGet(ctx('/api/v1/admin/games?visibility=hidden')).then(json);
    assert.deepEqual(adminRows.body.data.games.map(g => g.id), ['elden-ring']);
    assert.equal((await setHidden('elden-ring', false)).status, 200);
    assert.equal((await getGame('elden-ring')).status, 200);
    assert.deepEqual(counts(), before);
  });

  test('no Function ever deletes or replaces a games row', () => {
    const files = [];
    const walk = dir => fs.readdirSync(dir, { withFileTypes: true }).forEach(e => {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) walk(p); else if (p.endsWith('.js')) files.push(p);
    });
    walk(path.join(REPO, 'functions'));
    for (const f of files) {
      const s = fs.readFileSync(f, 'utf8');
      assert.ok(!/DELETE\s+FROM\s+games\b/i.test(s), `${f} deletes games rows`);
      assert.ok(!/(?:INSERT\s+OR\s+REPLACE|REPLACE)\s+INTO\s+games\b/i.test(s), `${f} replaces games rows`);
    }
  });

  test('a save stays within the free-plan limits (≤ 50 queries, ≤ 100 bindings each)', async () => {
    const { rev, doc } = (await getAdminGame('cyberpunk-2077')).body.data;
    const edited = clone(doc);
    edited.lastUpdated = '2026-11-24';
    const q0 = db.queries;
    const res = await save({ doc: edited, base_rev: rev });
    assert.equal(res.status, 200);
    assert.ok(db.queries - q0 <= 50, `${db.queries - q0} queries`);
  });
});
