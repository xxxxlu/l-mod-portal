"""Tests for scripts/export_d1_snapshot.py.

Run: python3 -m unittest discover -s scripts/tests/db -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO, 'scripts'))

import export_d1_snapshot as exp  # noqa: E402
import sync_to_database as sdb  # noqa: E402


def current_games():
    with open(exp.DATA_JS_PATH, encoding='utf-8') as f:
        return exp.split_games(f.read())[2]


class ExportSnapshotTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, 'd1.sqlite')
        games, _ = sdb.load_games()
        sql, _, _ = sdb.generate_seed_sql(games)
        sdb.build_local_sqlite(sql, db_path=self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, *args):
        return subprocess.run([sys.executable, os.path.join(REPO, 'scripts/export_d1_snapshot.py'), *args],
                              capture_output=True, text=True)

    def test_unchanged_database_reproduces_data_js_byte_for_byte(self):
        out = os.path.join(self.tmp.name, 'out')
        res = self.run_script('--sqlite', self.db, '--output', out)
        self.assertEqual(res.returncode, 0, res.stderr)
        for name in ('data.js', 'radar_status.json'):
            with open(os.path.join(out, name), 'rb') as a, open(os.path.join(REPO, 'public', name), 'rb') as b:
                self.assertEqual(a.read(), b.read(), name)

    def test_hidden_new_and_edited_games(self):
        import sqlite3
        conn = sqlite3.connect(self.db)
        conn.execute("UPDATE games SET is_hidden = 1 WHERE id = 'gta-v'")
        doc = json.loads(conn.execute("SELECT raw_json FROM games WHERE id = 'hades'").fetchone()[0])
        doc['titles']['zh-CN'] = '黑帝斯（改）'
        doc['compatibilityStatus'] = 'red'  # stale machine value in D1: the snapshot keeps data.js's
        conn.execute("UPDATE games SET raw_json = ? WHERE id = 'hades'", (json.dumps(doc, ensure_ascii=False),))
        new = {'id': 'brand-new', 'rank': 101, 'title': 'Brand New', 'titles': {'zh-CN': '新', 'en': 'Brand New'}}
        conn.execute("INSERT INTO games (id, rank, title, raw_json) VALUES ('brand-new', 101, 'Brand New', ?)",
                     (json.dumps(new),))
        conn.commit()
        conn.close()

        rows = exp.rows_from_sqlite(self.db)
        cur = current_games()
        games, report = exp.build_snapshot(rows, cur, None)
        by_id = {g['id']: g for g in games}
        self.assertNotIn('gta-v', by_id)
        self.assertEqual(report['removed'], ['gta-v'])
        self.assertEqual(report['new'], ['brand-new'])
        self.assertEqual(report['changed'], {'hades': ['titles']})
        self.assertEqual(by_id['hades']['titles']['zh-CN'], '黑帝斯（改）')
        old_hades = next(g for g in cur if g['id'] == 'hades')
        self.assertEqual(by_id['hades']['compatibilityStatus'], old_hades['compatibilityStatus'])
        # a new game gets the trainer fields of fling_trainer_sync (none here) and no radar fields
        self.assertEqual(by_id['brand-new']['hasTrainer'], False)
        self.assertNotIn('compatibilityStatus', by_id['brand-new'])
        self.assertEqual(games[-1]['id'], 'brand-new')

    def test_reads_only(self):
        before = os.path.getmtime(self.db)
        res = self.run_script('--sqlite', self.db, '--dry-run')
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn('没有写文件', res.stdout)
        self.assertEqual(os.path.getmtime(self.db), before)


if __name__ == '__main__':
    unittest.main()
