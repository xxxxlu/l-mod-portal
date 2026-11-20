#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_to_database.py
Generates the SQL that loads the game data into Cloudflare D1 (database/seed_data.sql)
and checks it against a local SQLite copy (database/lmod_vault.db).

Source: src/data/games_top100.json when it exists, otherwise the GAMES_DATA block of
public/data.js (read only; this script never writes either file).

Why the SQL looks the way it does:
- user_favorites and user_radar_subscriptions reference games(id) with ON DELETE CASCADE.
  "INSERT OR REPLACE INTO games" deletes the old row before inserting, which silently
  deletes every user's favorites and subscriptions for that game. Game rows are therefore
  only upserted (INSERT ... ON CONFLICT(id) DO UPDATE) and never deleted or replaced.
  A game that is removed from the data stays in D1; remove it by hand after dealing with
  its favorites and subscriptions.
- console_commands and scenario_bundles are rebuilt per game from the data, so commands
  and bundles that were removed from the data also leave D1. Commands that were created
  or edited in the admin console (they have an admin_audit_logs row with
  entity = 'console_commands') are kept as they are.
- Edits made to game rows in the admin console are overwritten: public/data.js is the
  source of truth for game content.
"""

import argparse
import json
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
DATA_JS_PATH = os.path.join(BASE_DIR, 'public/data.js')
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
SEED_SQL_PATH = os.path.join(DATABASE_DIR, 'seed_data.sql')
LOCAL_DB_PATH = os.path.join(DATABASE_DIR, 'lmod_vault.db')
# Applied in this order to build the local copy, the same order D1 got them.
SCHEMA_FILES = ['schema.sql', 'migration_v2.sql', 'migration_v3_admin.sql', 'migration_v4_users.sql']

GAMES_DATA_HEAD = "window.GAMES_DATA = "
GAMES_DATA_TAIL = ";\n\nwindow.GAMES_DATABASE"

# Commands the admin console created or edited; reseeding leaves them alone.
ADMIN_TOUCHED_COMMANDS = (
    "SELECT entity_id FROM admin_audit_logs "
    "WHERE entity = 'console_commands' AND entity_id IS NOT NULL"
)

GAME_COLUMNS = [
    'rank', 'title', 'title_zh', 'titles_json', 'developer', 'release_year', 'genre',
    'steam_rating', 'steam_app_id', 'header_image', 'has_console', 'console_shortcut',
    'console_guide_zh', 'console_guide_en', 'has_mods', 'mod_install_path', 'has_trainer',
    'verified_patch', 'latest_steam_patch', 'compatibility_status', 'radar_risk_title',
    'radar_risk_desc', 'radar_summary', 'pitfall_note', 'raw_json',
]


def escape_sql(val):
    """Render a Python value as an SQL literal."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "1" if val else "0"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, (dict, list)):
        val = json.dumps(val, ensure_ascii=False)
    s = str(val).replace("'", "''")
    return f"'{s}'"


def text_of(val, lang='zh-CN'):
    """Pick one language from a {lang: text} dict; plain values pass through."""
    if isinstance(val, dict):
        return val.get(lang) or ''
    return '' if val is None else str(val)


def load_games():
    """Return (games, source_path) from the master JSON, or GAMES_DATA in public/data.js."""
    if os.path.exists(GAMES_JSON_PATH):
        with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f), GAMES_JSON_PATH
    with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    a = text.index(GAMES_DATA_HEAD) + len(GAMES_DATA_HEAD)
    b = text.index(GAMES_DATA_TAIL)
    return json.loads(text[a:b]), DATA_JS_PATH


def game_values(g):
    guide = g.get('consoleEnableGuide')
    titles = g.get('titles') or {}
    return {
        'rank': g.get('rank', 99),
        'title': g.get('title', 'Unknown'),
        'title_zh': titles.get('zh-CN') or g.get('title', 'Unknown'),
        'titles_json': titles,
        'developer': g.get('developer', ''),
        'release_year': g.get('releaseYear'),
        'genre': g.get('genre', ''),
        'steam_rating': g.get('steamRating', ''),
        'steam_app_id': g.get('steamAppId'),
        'header_image': g.get('headerImage', ''),
        'has_console': bool(g.get('hasConsole', False)),
        'console_shortcut': g.get('consoleShortcut', ''),
        'console_guide_zh': text_of(guide, 'zh-CN'),
        'console_guide_en': text_of(guide, 'en') if isinstance(guide, dict) else '',
        'has_mods': bool(g.get('hasMods', False)),
        'mod_install_path': g.get('modInstallPath', ''),
        'has_trainer': bool(g.get('hasTrainer', False)),
        'verified_patch': g.get('verifiedPatch', ''),
        'latest_steam_patch': g.get('latestSteamPatch', ''),
        'compatibility_status': g.get('compatibilityStatus'),
        'radar_risk_title': g.get('radarRiskTitle', ''),
        'radar_risk_desc': g.get('radarRiskDesc', ''),
        'radar_summary': g.get('radarSummary', ''),
        'pitfall_note': g.get('pitfallNote', ''),
        'raw_json': g,
    }


def command_rows(g):
    """Yield console_commands rows (dicts) for one game."""
    gid = g['id']
    for idx, c in enumerate(g.get('popularCommands') or []):
        if isinstance(c, dict):
            name = c.get('name')
            yield {
                'id': f"{gid}_pop_{idx + 1}", 'game_id': gid, 'category_id': 'popular',
                'category_name_zh': '常用指令', 'category_name_en': 'Popular',
                'name_zh': text_of(name, 'zh-CN') or '常用指令',
                'name_en': text_of(name, 'en') if isinstance(name, dict) else '',
                'code': c.get('code') or c.get('command') or '',
                'description': text_of(c.get('desc'), 'zh-CN'),
                'syntax_type': c.get('syntax_type', 'engine_console'), 'is_popular': 1,
            }
        else:
            yield {
                'id': f"{gid}_pop_{idx + 1}", 'game_id': gid, 'category_id': 'popular',
                'category_name_zh': '常用指令', 'category_name_en': 'Popular',
                'name_zh': str(c), 'name_en': str(c), 'code': str(c), 'description': '',
                'syntax_type': 'engine_console', 'is_popular': 1,
            }
    for cat in g.get('consoleCategories') or []:
        cat_id = cat.get('id', 'general')
        cat_name = cat.get('name')
        for idx, c in enumerate(cat.get('commands') or []):
            name = c.get('name')
            yield {
                'id': c.get('id') or f"{gid}_{cat_id}_{idx + 1}", 'game_id': gid,
                'category_id': cat_id,
                'category_name_zh': text_of(cat_name, 'zh-CN') or '指令分类',
                'category_name_en': text_of(cat_name, 'en') if isinstance(cat_name, dict) else '',
                'name_zh': text_of(name, 'zh-CN') or '指令',
                'name_en': text_of(name, 'en') if isinstance(name, dict) else '',
                'code': c.get('code') or c.get('command') or '',
                'description': text_of(c.get('desc'), 'zh-CN'),
                'syntax_type': c.get('syntax_type', 'engine_console'), 'is_popular': 0,
            }


def bundle_rows(g):
    """Yield scenario_bundles rows (dicts) for one game."""
    gid = g['id']
    for idx, b in enumerate(g.get('scenarioBundles') or []):
        commands = b.get('commands')
        if not commands and b.get('code'):
            commands = [line for line in str(b['code']).splitlines() if line.strip()]
        yield {
            'id': b.get('id') or f"{gid}_bundle_{idx + 1}", 'game_id': gid,
            'name': text_of(b.get('name'), 'zh-CN') or '指令套餐',
            'description': text_of(b.get('desc') or b.get('description'), 'zh-CN'),
            'commands_json': commands or [],
            'bat_script': b.get('batScript', ''),
        }


def insert_sql(table, row, conflict):
    cols = ', '.join(row)
    vals = ', '.join(escape_sql(v) for v in row.values())
    return f"INSERT INTO {table} ({cols}) VALUES ({vals}) {conflict};"


def generate_seed_sql(games):
    """Return (sql, command_count, bundle_count). See the module docstring for the rules."""
    lines = [
        "-- L-MOD Vault seed data, generated by scripts/sync_to_database.py",
        "-- Game rows are upserted, never deleted or replaced (favorites and subscriptions",
        "-- cascade from games). Commands and bundles are rebuilt per game; commands the",
        "-- admin console created or edited are kept.",
        "",
    ]
    total_commands = 0
    total_bundles = 0
    for g in games:
        gid = g['id']
        values = game_values(g)
        row = {'id': gid, **values}
        updates = ', '.join(f"{c} = excluded.{c}" for c in GAME_COLUMNS)
        lines.append(insert_sql(
            'games', row, f"ON CONFLICT(id) DO UPDATE SET {updates}, updated_at = CURRENT_TIMESTAMP"))

        lines.append(
            f"DELETE FROM console_commands WHERE game_id = {escape_sql(gid)} "
            f"AND id NOT IN ({ADMIN_TOUCHED_COMMANDS});")
        lines.append(f"DELETE FROM scenario_bundles WHERE game_id = {escape_sql(gid)};")
        for c in command_rows(g):
            lines.append(insert_sql('console_commands', c, "ON CONFLICT(id) DO NOTHING"))
            total_commands += 1
        for b in bundle_rows(g):
            lines.append(insert_sql('scenario_bundles', b, "ON CONFLICT(id) DO NOTHING"))
            total_bundles += 1
    lines.append("")
    return "\n".join(lines), total_commands, total_bundles


def apply_schema(conn, database_dir=DATABASE_DIR):
    for name in SCHEMA_FILES:
        with open(os.path.join(database_dir, name), 'r', encoding='utf-8') as f:
            conn.executescript(f.read())


def build_local_sqlite(seed_sql, db_path=LOCAL_DB_PATH, database_dir=DATABASE_DIR):
    """Build a fresh local SQLite copy (schema + migrations + seed) and return row counts."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    try:
        apply_schema(conn, database_dir)
        conn.execute('PRAGMA foreign_keys = ON')
        conn.executescript(seed_sql)
        conn.commit()
        counts = tuple(conn.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
                       for t in ('games', 'console_commands', 'scenario_bundles'))
        problems = conn.execute('PRAGMA foreign_key_check').fetchall()
    finally:
        conn.close()
    if problems:
        raise RuntimeError(f"foreign key check failed: {problems[:5]}")
    return counts


def main():
    parser = argparse.ArgumentParser(description="Generate the D1 seed SQL from the game data")
    parser.add_argument('--skip-local', action='store_true',
                        help="only write database/seed_data.sql, do not build the local SQLite copy")
    args = parser.parse_args()

    games, source = load_games()
    print(f"Source: {os.path.relpath(source, BASE_DIR)} ({len(games)} games)")
    seed_sql, total_cmds, total_bundles = generate_seed_sql(games)
    os.makedirs(DATABASE_DIR, exist_ok=True)
    with open(SEED_SQL_PATH, 'w', encoding='utf-8') as f:
        f.write(seed_sql)
    size_kb = os.path.getsize(SEED_SQL_PATH) / 1024
    print(f"Wrote {os.path.relpath(SEED_SQL_PATH, BASE_DIR)} ({size_kb:.1f} KB): "
          f"{len(games)} games, {total_cmds} commands, {total_bundles} bundles")

    if not args.skip_local:
        g_cnt, c_cnt, b_cnt = build_local_sqlite(seed_sql)
        print(f"Local SQLite copy {os.path.relpath(LOCAL_DB_PATH, BASE_DIR)}: "
              f"{g_cnt} games, {c_cnt} commands, {b_cnt} bundles, foreign keys OK")

    print("""
Loading into the production D1 (writes the live database; get the owner's go-ahead first):
  1. Back up first, to a folder outside the repo (the export contains the users table):
     npx wrangler d1 export lmod-vault-db --remote --output <backup-dir>/lmod-vault-db-<date>.sql
  2. Rehearse: load that backup into a local SQLite file, run database/seed_data.sql on it
     with PRAGMA foreign_keys = ON, and check that users, favorites and subscriptions are unchanged.
  3. Apply:
     npx wrangler d1 execute lmod-vault-db --remote --file=database/seed_data.sql
Without --remote, wrangler only touches the local development database.""")


if __name__ == '__main__':
    sys.exit(main())
