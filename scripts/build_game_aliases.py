#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_game_aliases.py
游戏别名（老头环 / 大表哥2 / bg3 …）的唯一来源是游戏数据里每款游戏的 `aliases` 字段。
网站搜索、前端 AI 助手直接读 window.GAMES_DATA；服务端 AI（Cloudflare Functions 读不到 data.js）
用本脚本生成的 functions/api/v1/ai/_game_aliases.js。

改别名：改 src/data/games_top100.json（或 public/data.js）里的 aliases → 运行本脚本。

用法：
  python3 scripts/build_game_aliases.py           # 生成服务端别名模块
  python3 scripts/build_game_aliases.py --check   # 只校验：别名冲突 / 模块是否过期（CI 用，过期则退出码 1）
"""

import argparse
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, "src/data/games_top100.json")
DATA_JS_PATH = os.path.join(BASE_DIR, "public/data.js")
OUT_PATH = os.path.join(BASE_DIR, "functions/api/v1/ai/_game_aliases.js")


def load_games():
    if os.path.exists(GAMES_JSON_PATH):
        with open(GAMES_JSON_PATH, encoding="utf-8") as f:
            return json.load(f)
    with open(DATA_JS_PATH, encoding="utf-8") as f:
        s = f.read()
    head = "window.GAMES_DATA = "
    a = s.index(head) + len(head)
    b = s.index(";\n\nwindow.GAMES_DATABASE", a)
    return json.loads(s[a:b])


def build_map(games):
    alias_map, conflicts = {}, []
    for g in games:
        for alias in g.get("aliases") or []:
            key = alias.strip().lower().replace(" ", "")
            if not key:
                continue
            if key in alias_map and alias_map[key] != g["id"]:
                conflicts.append(f"{alias}: {alias_map[key]} / {g['id']}")
            alias_map[key] = g["id"]
    # 长的在前：「辐射新维加斯」要先于「辐射」命中
    ordered = dict(sorted(alias_map.items(), key=lambda kv: (-len(kv[0]), kv[0])))
    return ordered, conflicts


def render(alias_map):
    body = json.dumps(alias_map, ensure_ascii=False, indent=2)
    return (
        "// ⚠️ 自动生成，勿手改。来源：游戏数据的 aliases 字段；生成：python3 scripts/build_game_aliases.py\n"
        "// 键已转小写、去空格，并按长度从长到短排好（遍历时先命中更具体的别名）。\n"
        f"export const GAME_ALIASES = {body};\n"
    )


def main():
    ap = argparse.ArgumentParser(description="生成服务端游戏别名模块")
    ap.add_argument("--check", action="store_true", help="只校验，不写文件")
    args = ap.parse_args()

    alias_map, conflicts = build_map(load_games())
    if conflicts:
        print("❌ 别名冲突（同一个别名指向多款游戏）：")
        for c in conflicts:
            print("   " + c)
        return 1
    text = render(alias_map)
    if args.check:
        current = open(OUT_PATH, encoding="utf-8").read() if os.path.exists(OUT_PATH) else ""
        if current != text:
            print(f"❌ {os.path.relpath(OUT_PATH, BASE_DIR)} 已过期，请运行 python3 scripts/build_game_aliases.py")
            return 1
        print(f"✅ 别名 {len(alias_map)} 条，无冲突，服务端模块是最新的")
        return 0
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ 已生成 {os.path.relpath(OUT_PATH, BASE_DIR)}：{len(alias_map)} 条别名")
    return 0


if __name__ == "__main__":
    sys.exit(main())
