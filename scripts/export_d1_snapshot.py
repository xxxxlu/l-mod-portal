#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/export_d1_snapshot.py —— 从 D1（只读）导出游戏数据，重新生成 public/data.js 的 GAMES_DATA 快照

D1 games.raw_json 是游戏数据的真源（后台直接改它）。public/data.js 里的 GAMES_DATA 只是快照，用在：
  - 网站先用它渲染、接口拿不到时兜底（GitHub Pages、断网、接口挂了）；
  - 每天的雷达 / 修改器定时任务读它、往里写机器字段；
  - scripts/build_game_aliases.py 生成 AI 助手的别名表。
所以发版前跑一次，把后台改的内容带进快照。

规则：
  - 只读 D1：只执行 SELECT。
  - 隐藏的游戏（games.is_hidden = 1）不进快照。
  - 机器字段（雷达 RADAR_FIELDS、修改器 TRAINER_FIELDS）以现在的 data.js 为准：它们由定时任务每天写进
    data.js，D1 里的是导入那天的旧值。快照里没有的新游戏：修改器字段按 public/trainers.json 算，
    雷达字段留空，等下一次雷达定时任务补上。
  - 只替换 data.js 里 `window.GAMES_DATA = …;` 一段，TRANSLATIONS_DATA 等不动；
    同时按新快照重写 public/radar_status.json（隐藏的游戏随之去掉）。
  - 不写 src/data/games_top100.json（本机主数据已退役）。

用法：
  python3 scripts/export_d1_snapshot.py --local --dry-run       # 本地 D1，只看会改什么
  python3 scripts/export_d1_snapshot.py --local                 # 本地 D1，写 public/data.js + radar_status.json
  python3 scripts/export_d1_snapshot.py --sqlite <file.sqlite>  # 从一个 SQLite 文件读（例如导入了备份的演练库）
  python3 scripts/export_d1_snapshot.py --remote --dry-run      # 线上 D1（只读 SELECT；照样先问 boss）
  加 --output <dir> 把 data.js / radar_status.json 写到别的目录（不动仓库里的文件）

写完之后：
  python3 scripts/build_game_aliases.py        # AI 助手的别名表跟着快照走
  python3 scripts/build_prod.py && python3 scripts/verify_deployment.py && python3 scripts/verify_i18n_dual_pages.py
"""

import argparse
import copy
import json
import os
import shutil
import sqlite3
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))

from fling_trainer_sync import apply_to_game  # noqa: E402
from gamedata_guard import GAMES_MARKER, TRAINER_FIELDS  # noqa: E402
from steam_patch_monitor import RADAR_FIELDS, write_radar_status  # noqa: E402

DATA_JS_PATH = os.path.join(BASE_DIR, 'public/data.js')
TRAINERS_PATH = os.path.join(BASE_DIR, 'public/trainers.json')
MASTER_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
DATABASE = 'lmod-vault-db'
WRANGLER = ['npx', '--yes', 'wrangler@4.154.0']
MACHINE_FIELDS = list(RADAR_FIELDS) + list(TRAINER_FIELDS)

QUERY = 'SELECT id, rank, raw_json, is_hidden FROM games ORDER BY rank ASC, id ASC'
QUERY_PRE_V5 = 'SELECT id, rank, raw_json, 0 AS is_hidden FROM games ORDER BY rank ASC, id ASC'


def fail(msg):
    raise SystemExit(f"❌ export_d1_snapshot: {msg}; nothing written.")


# ---------------------------------------------------------------------------
# 读 D1（只读）
# ---------------------------------------------------------------------------

def rows_from_wrangler(remote):
    def run(sql):
        cmd = WRANGLER + ['d1', 'execute', DATABASE, '--remote' if remote else '--local', '--json', '--command', sql]
        res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
        if res.returncode != 0:
            return None, (res.stderr or res.stdout)[-800:]
        try:
            out = json.loads(res.stdout)
        except json.JSONDecodeError:
            return None, f"wrangler printed something that is not JSON: {res.stdout[:300]!r}"
        return out[0]['results'], None

    rows, err = run(QUERY)
    if rows is None and 'is_hidden' in (err or ''):
        print("ℹ️ games.is_hidden 不存在（还没跑 migration_v5），当作全部公开")
        rows, err = run(QUERY_PRE_V5)
    if rows is None:
        fail(f"wrangler d1 execute failed:\n{err}")
    return rows


def rows_from_sqlite(path):
    if not os.path.exists(path):
        fail(f"{path} not found")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        try:
            rows = conn.execute(QUERY).fetchall()
        except sqlite3.OperationalError as exc:
            if 'is_hidden' not in str(exc):
                raise
            print("ℹ️ games.is_hidden 不存在（还没跑 migration_v5），当作全部公开")
            rows = conn.execute(QUERY_PRE_V5).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# 组快照
# ---------------------------------------------------------------------------

def split_games(text):
    """(start, end, games) of the GAMES_DATA array inside data.js."""
    idx = text.find(GAMES_MARKER)
    if idx == -1 or text.find(GAMES_MARKER, idx + 1) != -1:
        fail(f"expected exactly one {GAMES_MARKER!r} in data.js")
    start = idx + len(GAMES_MARKER)
    games, length = json.JSONDecoder().raw_decode(text[start:])
    end = start + length
    if not text.startswith(';', end) or not isinstance(games, list):
        fail("GAMES_DATA in data.js is not a `[...];` array")
    return start, end, games


def build_snapshot(rows, current_games, trainers):
    """D1 rows + current data.js → (games, report)."""
    current = {g['id']: g for g in current_games}
    trainer_entries = (trainers or {}).get('games') or {}
    games, hidden, new_ids = [], [], []
    seen = set()
    for row in rows:
        gid = row['id']
        if row.get('is_hidden'):
            hidden.append(gid)
            continue
        try:
            doc = json.loads(row['raw_json'] or 'null')
        except json.JSONDecodeError as exc:
            fail(f"games.raw_json of {gid!r} is not valid JSON ({exc})")
        if not isinstance(doc, dict) or doc.get('id') != gid:
            fail(f"games.raw_json of {gid!r} is not a game object with the same id")
        if gid in seen:
            fail(f"duplicate game id {gid!r}")
        seen.add(gid)

        old = current.get(gid)
        if old is not None:
            for key in MACHINE_FIELDS:
                if key in old:
                    doc[key] = copy.deepcopy(old[key])
                else:
                    doc.pop(key, None)
        else:
            new_ids.append(gid)
            apply_to_game(doc, trainer_entries.get(gid))
        games.append(doc)

    removed = [gid for gid in current if gid not in seen]
    changed = {}
    for g in games:
        old = current.get(g['id'])
        if old is None:
            continue
        keys = sorted(k for k in set(g) | set(old)
                      if k not in MACHINE_FIELDS and (g.get(k) != old.get(k) or (k in g) != (k in old)))
        if keys:
            changed[g['id']] = keys
    order_changed = [g['id'] for g in games if g['id'] in current] != [gid for gid in current if gid in seen]
    return games, {'hidden': hidden, 'new': new_ids, 'removed': removed, 'changed': changed,
                   'order_changed': order_changed}


def print_report(report, games):
    print(f"📦 快照：{len(games)} 款（D1 里隐藏 {len(report['hidden'])} 款，不进快照）")
    if report['new']:
        print(f"  ＋ 新游戏 {len(report['new'])}：{', '.join(report['new'])}（雷达字段等下一次定时任务补）")
    if report['removed']:
        print(f"  － 快照里去掉 {len(report['removed'])}：{', '.join(report['removed'])}")
    if report['changed']:
        print(f"  ✎ 内容有变化 {len(report['changed'])} 款：")
        for gid, keys in list(report['changed'].items())[:30]:
            print(f"     {gid}: {', '.join(keys)}")
        if len(report['changed']) > 30:
            print(f"     …（另有 {len(report['changed']) - 30} 款）")
    if report['order_changed']:
        print("  ↕ 顺序有变化（按 rank 重新排）")
    if not (report['new'] or report['removed'] or report['changed'] or report['order_changed']):
        print("  ✅ 和现在的 data.js 一样，没有要改的")


def main():
    parser = argparse.ArgumentParser(description="Export the game data from D1 (read-only) into public/data.js")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument('--local', action='store_true', help="本地开发用的 D1（wrangler --local）")
    src.add_argument('--remote', action='store_true', help="线上 D1（只执行 SELECT）")
    src.add_argument('--sqlite', metavar='FILE', help="从一个 SQLite 文件读")
    parser.add_argument('--data-js', default=DATA_JS_PATH, help="当前的 data.js（机器字段从这里取），默认 public/data.js")
    parser.add_argument('--output', metavar='DIR', help="写到这个目录（data.js + radar_status.json），默认就地改 public/")
    parser.add_argument('--dry-run', action='store_true', help="只报告会改什么，不写文件")
    args = parser.parse_args()

    with open(args.data_js, encoding='utf-8') as f:
        js_text = f.read()
    start, end, current_games = split_games(js_text)
    trainers = None
    if os.path.exists(TRAINERS_PATH):
        with open(TRAINERS_PATH, encoding='utf-8') as f:
            trainers = json.load(f)

    if args.sqlite:
        rows = rows_from_sqlite(args.sqlite)
    else:
        rows = rows_from_wrangler(remote=args.remote)
    if not rows:
        fail("D1 returned no games")

    games, report = build_snapshot(rows, current_games, trainers)
    print_report(report, games)
    if os.path.exists(MASTER_PATH):
        print(f"⚠️ 本机还有 {os.path.relpath(MASTER_PATH, BASE_DIR)}：主数据已退役（D1 是真源），这个文件不会再更新；"
              "建议改名备份，免得老脚本拿它覆盖 data.js。")
    if args.dry_run:
        print("ℹ️ --dry-run：没有写文件")
        return 0

    new_js = js_text[:start] + json.dumps(games, ensure_ascii=False, indent=2) + js_text[end:]
    if split_games(new_js)[2] != games:
        fail("output did not read back the same")
    out_dir = args.output or os.path.dirname(os.path.abspath(args.data_js))
    os.makedirs(out_dir, exist_ok=True)
    js_out = os.path.join(out_dir, 'data.js')
    tmp = js_out + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(new_js)
    os.replace(tmp, js_out)
    count, size = write_radar_status(games, os.path.join(out_dir, 'radar_status.json'))
    if args.output and os.path.exists(TRAINERS_PATH) and os.path.abspath(out_dir) != os.path.dirname(TRAINERS_PATH):
        shutil.copy2(TRAINERS_PATH, os.path.join(out_dir, 'trainers.json'))
    print(f"✅ 写好 {os.path.relpath(js_out, BASE_DIR)}（只换了 GAMES_DATA 一段）和 radar_status.json（{count} 款，{size} 字节）")
    print("下一步：python3 scripts/build_game_aliases.py，然后跑 build_prod / verify_deployment / verify_i18n_dual_pages 三道门禁")
    return 0


if __name__ == '__main__':
    sys.exit(main())
