/**
 * A small stand-in for the Cloudflare D1 binding on top of node:sqlite (Node 22.13+),
 * for testing Pages Functions without wrangler.
 *
 * Same behaviour that matters here: foreign keys on, `undefined` bindings rejected,
 * db.batch() is one transaction that rolls back when any statement fails.
 */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { DatabaseSync } from 'node:sqlite';

export const REPO = path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../..');

function checkParams(params) {
  for (const p of params) {
    if (p === undefined) throw new Error('D1_TYPE_ERROR: Type \'undefined\' not supported for value');
    if (typeof p === 'boolean') throw new Error('D1_TYPE_ERROR: booleans must be bound as 0/1 in this shim');
  }
  return params;
}

class Statement {
  constructor(d1, sql, params = []) {
    this.d1 = d1;
    this.sql = sql;
    this.params = params;
  }

  bind(...params) {
    return new Statement(this.d1, this.sql, params);
  }

  _isReader() {
    return /^\s*(SELECT|WITH|PRAGMA)/i.test(this.sql) || /\bRETURNING\b/i.test(this.sql);
  }

  _exec() {
    this.d1.queries++;
    const st = this.d1.db.prepare(this.sql);
    const params = checkParams(this.params);
    if (this._isReader()) return { results: st.all(...params), success: true };
    const r = st.run(...params);
    return { results: [], success: true, meta: { changes: Number(r.changes) } };
  }

  async all() {
    return this._exec();
  }

  async first() {
    const { results } = this._exec();
    return results.length ? results[0] : null;
  }

  async run() {
    return this._exec();
  }
}

export class D1Shim {
  constructor(file) {
    // node:sqlite turns foreign keys on by default; off while the migrations load their demo rows
    this.db = new DatabaseSync(file, { enableForeignKeyConstraints: false });
    this.queries = 0;
    this.beforeBatch = null;
  }

  enableForeignKeys() {
    this.db.exec('PRAGMA foreign_keys = ON');
  }

  prepare(sql) {
    return new Statement(this, sql);
  }

  async batch(statements) {
    if (this.beforeBatch) this.beforeBatch();
    this.db.exec('BEGIN');
    try {
      const out = statements.map(s => s._exec());
      this.db.exec('COMMIT');
      return out;
    } catch (err) {
      this.db.exec('ROLLBACK');
      throw err;
    }
  }

  scalar(sql, ...params) {
    const row = this.db.prepare(sql).get(...params);
    return row ? Object.values(row)[0] : null;
  }
}

export function readGamesData() {
  const text = fs.readFileSync(path.join(REPO, 'public/data.js'), 'utf8');
  const head = 'window.GAMES_DATA = ';
  const a = text.indexOf(head) + head.length;
  const b = text.indexOf(';\n\nwindow.GAMES_DATABASE');
  return JSON.parse(text.slice(a, b));
}

/** Python-side output of scripts/sync_to_database.py for the same data (seed SQL or derived rows). */
export function python(code) {
  const res = spawnSync('python3', ['-c', code], {
    cwd: path.join(REPO, 'scripts'), encoding: 'utf8', maxBuffer: 64 * 1024 * 1024
  });
  if (res.status !== 0) throw new Error(`python failed: ${res.stderr}`);
  return res.stdout;
}

/**
 * Fresh database like production: schema + migrations v2–v5 (foreign keys off while loading,
 * the migrations ship demo rows), the games seeded by sync_to_database.py from public/data.js.
 */
export function makeDatabase(dir) {
  const d1 = new D1Shim(path.join(dir, 'test.sqlite'));
  for (const name of ['schema.sql', 'migration_v2.sql', 'migration_v3_admin.sql', 'migration_v4_users.sql',
    'migration_v5_game_docs.sql', 'migration_v6_telemetry.sql', 'migration_v7_trainer_packages.sql']) {
    d1.db.exec(fs.readFileSync(path.join(REPO, 'database', name), 'utf8'));
  }
  const seed = python(
    'import sync_to_database as s\n' +
    'games, _ = s.load_games()\n' +
    'sql, _, _ = s.generate_seed_sql(games)\n' +
    'print(sql)'
  );
  d1.db.exec(seed);
  d1.enableForeignKeys();
  return d1;
}

/** env.ASSETS that serves files from public/ (radar_status.json, trainers.json). */
export function assetsFromPublic(overrides = {}) {
  return {
    async fetch(request) {
      const p = new URL(request.url).pathname;
      if (Object.prototype.hasOwnProperty.call(overrides, p)) {
        const body = overrides[p];
        return body === null ? new Response('not found', { status: 404 }) : new Response(body);
      }
      const file = path.join(REPO, 'public', p);
      if (!fs.existsSync(file)) return new Response('<html>spa</html>', { status: 200 });
      return new Response(fs.readFileSync(file));
    }
  };
}
