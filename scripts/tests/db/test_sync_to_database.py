"""Tests for scripts/sync_to_database.py.

Run: python3 -m unittest discover -s scripts/tests/db -v
"""
import copy
import json
import os
import sqlite3
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, 'scripts'))

import sync_to_database as sdb  # noqa: E402

GAMES = [
    {
        'id': 'game-a', 'rank': 1, 'title': 'Game A', 'titles': {'zh-CN': '游戏甲', 'en': 'Game A'},
        'steamAppId': 100, 'hasConsole': True, 'hasTrainer': True,
        'consoleEnableGuide': {'zh-CN': '按 ~ 打开', 'en': 'Press ~'},
        'popularCommands': [{'name': {'zh-CN': '加钱', 'en': 'Money'}, 'command': 'money 100', 'desc': '加 100'}],
        'consoleCategories': [{
            'id': 'cat', 'name': {'zh-CN': '分类', 'en': 'Category'},
            'commands': [
                {'id': 'a_keep', 'name': {'zh-CN': '保留', 'en': 'Keep'}, 'code': 'keep'},
                {'id': 'a_drop', 'name': {'zh-CN': '会删', 'en': 'Drop'}, 'code': 'drop'},
                {'id': 'a_edited', 'name': {'zh-CN': '原名', 'en': 'Original'}, 'code': 'edit'},
            ],
        }],
        'scenarioBundles': [{'id': 'a_bundle', 'name': '套餐', 'desc': '说明', 'code': 'money 100\nkeep'}],
    },
    {
        'id': 'game-b', 'rank': 2, 'title': 'Game B', 'titles': {'zh-CN': '游戏乙'},
        'steamAppId': 200, 'hasConsole': False,
        'scenarioBundles': [{'id': 'b_bundle', 'name': 'B 套餐', 'desc': '会删'}],
    },
]


def make_db(path):
    conn = sqlite3.connect(path)
    sdb.apply_schema(conn)
    # The migrations ship demo rows that point at real game ids; start from empty tables.
    for table in ('user_favorites', 'user_radar_subscriptions', 'patch_radar_logs',
                  'community_feedback', 'telemetry_events', 'admin_audit_logs'):
        conn.execute(f'DELETE FROM {table}')
    conn.commit()
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


class SeedSqlTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = make_db(os.path.join(self.tmp.name, 'test.db'))
        sql, _, _ = sdb.generate_seed_sql(GAMES)
        self.conn.executescript(sql)
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.conn.execute("INSERT INTO users (id, provider, nickname) VALUES ('u1', 'email', 'tester')")
        self.conn.execute("INSERT INTO user_favorites (user_id, game_id) VALUES ('u1', 'game-a')")
        self.conn.execute(
            "INSERT INTO user_radar_subscriptions (user_id, game_id, notify_channel, notify_target) "
            "VALUES ('u1', 'game-b', 'email', 'tester@example.invalid')")
        # A command created in the admin console, and a seeded command edited there.
        self.conn.execute(
            "INSERT INTO console_commands (id, game_id, name_zh, code) VALUES ('game-a_cmd_admin1', 'game-a', '后台加的', 'admin')")
        self.conn.execute("UPDATE console_commands SET name_zh = '后台改过' WHERE id = 'a_edited'")
        for cid in ('game-a_cmd_admin1', 'a_edited'):
            self.conn.execute(
                "INSERT INTO admin_audit_logs (action, entity, entity_id, details, admin_user) "
                "VALUES ('create_command', 'console_commands', ?, '{}', 'admin')", (cid,))
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def reseed(self, games):
        sql, cmds, bundles = sdb.generate_seed_sql(games)
        self.conn.executescript(sql)
        self.conn.execute('PRAGMA foreign_keys = ON')
        return sql

    def ids(self, table):
        return {r[0] for r in self.conn.execute(f'SELECT id FROM {table}')}

    def test_sql_never_replaces_or_deletes_games(self):
        sql, _, _ = sdb.generate_seed_sql(GAMES)
        self.assertNotIn('INSERT OR REPLACE INTO games', sql)
        self.assertNotIn('DELETE FROM games', sql)
        self.assertNotIn('REPLACE INTO games', sql.replace('INSERT INTO games', ''))

    def test_reseed_keeps_user_data_and_applies_changes(self):
        games = copy.deepcopy(GAMES)
        games[0]['title'] = 'Game A (renamed)'
        games[0]['consoleCategories'][0]['commands'] = [
            c for c in games[0]['consoleCategories'][0]['commands'] if c['id'] != 'a_drop']
        games[1]['scenarioBundles'] = []
        self.reseed(games)

        self.assertEqual(self.conn.execute('SELECT count(*) FROM user_favorites').fetchone()[0], 1)
        self.assertEqual(self.conn.execute('SELECT count(*) FROM user_radar_subscriptions').fetchone()[0], 1)
        self.assertEqual(self.conn.execute("SELECT title FROM games WHERE id = 'game-a'").fetchone()[0],
                         'Game A (renamed)')
        cmds = self.ids('console_commands')
        self.assertNotIn('a_drop', cmds)
        self.assertIn('a_keep', cmds)
        self.assertIn('game-a_cmd_admin1', cmds)
        self.assertEqual(self.conn.execute("SELECT name_zh FROM console_commands WHERE id = 'a_edited'").fetchone()[0],
                         '后台改过')
        self.assertEqual(self.ids('scenario_bundles'), {'a_bundle'})
        self.assertEqual(self.conn.execute('PRAGMA foreign_key_check').fetchall(), [])

    def test_reseed_is_repeatable(self):
        self.reseed(GAMES)
        before = {t: self.ids(t) for t in ('games', 'console_commands', 'scenario_bundles')}
        self.reseed(GAMES)
        after = {t: self.ids(t) for t in ('games', 'console_commands', 'scenario_bundles')}
        self.assertEqual(before, after)
        self.assertEqual(self.conn.execute('SELECT count(*) FROM user_favorites').fetchone()[0], 1)

    def test_bundle_fields_come_from_current_data_shape(self):
        row = self.conn.execute(
            "SELECT description, commands_json FROM scenario_bundles WHERE id = 'a_bundle'").fetchone()
        self.assertEqual(row[0], '说明')
        self.assertEqual(json.loads(row[1]), ['money 100', 'keep'])

    def test_game_flags_default_to_false(self):
        row = self.conn.execute(
            "SELECT has_console, has_mods, has_trainer, release_year FROM games WHERE id = 'game-b'").fetchone()
        self.assertEqual(tuple(row), (0, 0, 0, None))


class LoadGamesTest(unittest.TestCase):
    def test_falls_back_to_data_js_without_master(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_js = os.path.join(tmp, 'data.js')
            with open(data_js, 'w', encoding='utf-8') as f:
                f.write("// header\nwindow.GAMES_DATA = " + json.dumps(GAMES) +
                        ";\n\nwindow.GAMES_DATABASE = window.GAMES_DATA;\n")
            saved = (sdb.GAMES_JSON_PATH, sdb.DATA_JS_PATH)
            sdb.GAMES_JSON_PATH = os.path.join(tmp, 'missing.json')
            sdb.DATA_JS_PATH = data_js
            try:
                games, source = sdb.load_games()
            finally:
                sdb.GAMES_JSON_PATH, sdb.DATA_JS_PATH = saved
            self.assertEqual(source, data_js)
            self.assertEqual([g['id'] for g in games], ['game-a', 'game-b'])


class RepoDataTest(unittest.TestCase):
    def test_current_repo_data_builds_a_clean_local_copy(self):
        games, _ = sdb.load_games()
        sql, cmds, bundles = sdb.generate_seed_sql(games)
        with tempfile.TemporaryDirectory() as tmp:
            counts = sdb.build_local_sqlite(sql, db_path=os.path.join(tmp, 'repo.db'))
        self.assertEqual(counts, (len(games), cmds, bundles))


if __name__ == '__main__':
    unittest.main()
