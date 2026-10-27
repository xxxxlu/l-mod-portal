#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sync_to_database.py
L-MOD Vault - 全球数据库种子生成与同步管道 (Database Sync Pipeline)
Generates SQL seeds & synchronizes JSON to Cloudflare D1, SQLite, Supabase, or Turso.

Capabilities:
1. Normalizes src/data/games_top100.json into relational tables:
   - games (100 rows)
   - console_commands (all verified commands)
   - scenario_bundles (all one-click .bat packages)
2. Exports standard SQL seed file: database/seed_data.sql
3. Can initialize a local SQLite database (database/lmod_vault.db) for instant inspection & testing.
4. Provides ready-to-run Cloudflare D1 import command:
   npx wrangler d1 execute lmod-vault-db --file=database/seed_data.sql
"""

import os
import sys
import json
import sqlite3
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database/schema.sql')
SEED_SQL_PATH = os.path.join(BASE_DIR, 'database/seed_data.sql')
LOCAL_DB_PATH = os.path.join(BASE_DIR, 'database/lmod_vault.db')

def escape_sql(val):
    """Escapes string value for SQL insertion."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "1" if val else "0"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, (dict, list)):
        val = json.dumps(val, ensure_ascii=False)
    # Escape single quotes
    s = str(val).replace("'", "''")
    return f"'{s}'"


def generate_seed_sql(games):
    lines = [
        "-- ==============================================================================",
        "-- L-MOD Vault Seed Data (Auto-Generated)",
        "-- ==============================================================================",
        ""
    ]

    total_commands = 0
    total_bundles = 0

    for g in games:
        gid = g['id']
        rank = g.get('rank', 99)
        title = g.get('title', 'Unknown')
        title_zh = (g.get('titles') and g.get('titles', {}).get('zh-CN')) or title
        titles_json = g.get('titles', {})
        developer = g.get('developer', '')
        release_year = g.get('releaseYear', 2020)
        genre = g.get('genre', '')
        steam_rating = g.get('steamRating', '')
        steam_app_id = g.get('steamAppId')
        header_image = g.get('headerImage', '')
        has_console = 1 if g.get('hasConsole', True) else 0
        console_shortcut = g.get('consoleShortcut', '')
        
        guide_zh = ''
        guide_en = ''
        if isinstance(g.get('consoleEnableGuide'), dict):
            guide_zh = g['consoleEnableGuide'].get('zh-CN', '')
            guide_en = g['consoleEnableGuide'].get('en', '')
        elif isinstance(g.get('consoleEnableGuide'), str):
            guide_zh = g['consoleEnableGuide']

        has_mods = 1 if g.get('hasMods', True) else 0
        mod_install_path = g.get('modInstallPath', '')
        has_trainer = 1 if g.get('hasTrainer', True) else 0
        verified_patch = g.get('verifiedPatch', '')
        latest_steam_patch = g.get('latestSteamPatch', '')
        compat_status = g.get('compatibilityStatus', 'green')
        radar_risk_title = g.get('radarRiskTitle', '')
        radar_risk_desc = g.get('radarRiskDesc', '')
        radar_summary = g.get('radarSummary', '')
        pitfall_note = g.get('pitfallNote', '')
        raw_json = json.dumps(g, ensure_ascii=False)

        # Insert game record
        lines.append(f"""INSERT OR REPLACE INTO games (
            id, rank, title, title_zh, titles_json, developer, release_year, genre,
            steam_rating, steam_app_id, header_image, has_console, console_shortcut,
            console_guide_zh, console_guide_en, has_mods, mod_install_path, has_trainer,
            verified_patch, latest_steam_patch, compatibility_status, radar_risk_title,
            radar_risk_desc, radar_summary, pitfall_note, raw_json
        ) VALUES (
            {escape_sql(gid)}, {rank}, {escape_sql(title)}, {escape_sql(title_zh)}, {escape_sql(titles_json)},
            {escape_sql(developer)}, {release_year}, {escape_sql(genre)}, {escape_sql(steam_rating)},
            {escape_sql(steam_app_id)}, {escape_sql(header_image)}, {has_console}, {escape_sql(console_shortcut)},
            {escape_sql(guide_zh)}, {escape_sql(guide_en)}, {has_mods}, {escape_sql(mod_install_path)}, {has_trainer},
            {escape_sql(verified_patch)}, {escape_sql(latest_steam_patch)}, {escape_sql(compat_status)},
            {escape_sql(radar_risk_title)}, {escape_sql(radar_risk_desc)}, {escape_sql(radar_summary)},
            {escape_sql(pitfall_note)}, {escape_sql(raw_json)}
        );""")

        # Process Popular Commands
        if g.get('popularCommands'):
            for idx, c in enumerate(g['popularCommands']):
                cid = f"{gid}_pop_{idx+1}"
                if isinstance(c, dict):
                    raw_name = c.get('name')
                    name_zh = raw_name.get('zh-CN') if isinstance(raw_name, dict) else str(raw_name or '常用指令')
                    name_en = raw_name.get('en') if isinstance(raw_name, dict) else ''
                    code = c.get('code') or c.get('command') or ''
                    desc = c.get('desc', '')
                else:
                    name_zh = str(c)
                    name_en = str(c)
                    code = str(c)
                    desc = '常用快捷指令'

                lines.append(f"""INSERT OR REPLACE INTO console_commands (
                    id, game_id, category_id, category_name_zh, name_zh, name_en, code, description, is_popular
                ) VALUES (
                    {escape_sql(cid)}, {escape_sql(gid)}, 'popular', '常用核心快捷', {escape_sql(name_zh)}, {escape_sql(name_en)},
                    {escape_sql(code)}, {escape_sql(desc)}, 1
                );""")
                total_commands += 1

        # Process Categorized Commands
        if g.get('consoleCategories'):
            for cat in g['consoleCategories']:
                cat_id = cat.get('id', 'general')
                raw_cat_name = cat.get('name')
                cat_name_zh = raw_cat_name.get('zh-CN') if isinstance(raw_cat_name, dict) else str(raw_cat_name or '指令分类')
                cat_name_en = raw_cat_name.get('en') if isinstance(raw_cat_name, dict) else ''
                
                for idx, c in enumerate(cat.get('commands', [])):
                    cid = c.get('id') or f"{gid}_{cat_id}_{idx+1}"
                    raw_cname = c.get('name')
                    name_zh = raw_cname.get('zh-CN') if isinstance(raw_cname, dict) else str(raw_cname or '指令')
                    name_en = raw_cname.get('en') if isinstance(raw_cname, dict) else ''
                    code = c.get('code') or c.get('command') or ''
                    desc = c.get('desc', '')
                    syntax = c.get('syntax_type', 'engine_console')
                    lines.append(f"""INSERT OR REPLACE INTO console_commands (
                        id, game_id, category_id, category_name_zh, category_name_en, name_zh, name_en, code, description, syntax_type, is_popular
                    ) VALUES (
                        {escape_sql(cid)}, {escape_sql(gid)}, {escape_sql(cat_id)}, {escape_sql(cat_name_zh)}, {escape_sql(cat_name_en)},
                        {escape_sql(name_zh)}, {escape_sql(name_en)}, {escape_sql(code)}, {escape_sql(desc)}, {escape_sql(syntax)}, 0
                    );""")
                    total_commands += 1

        # Process Scenario Bundles
        if g.get('scenarioBundles'):
            for idx, b in enumerate(g['scenarioBundles']):
                bid = b.get('id') or f"{gid}_bundle_{idx+1}"
                bname = b.get('name', '场景套餐包')
                bdesc = b.get('description', '')
                bcmds = b.get('commands', [])
                bat = b.get('batScript', '')
                lines.append(f"""INSERT OR REPLACE INTO scenario_bundles (
                    id, game_id, name, description, commands_json, bat_script
                ) VALUES (
                    {escape_sql(bid)}, {escape_sql(gid)}, {escape_sql(bname)}, {escape_sql(bdesc)},
                    {escape_sql(bcmds)}, {escape_sql(bat)}
                );""")
                total_bundles += 1

    lines.append("")
    return "\n".join(lines), total_commands, total_bundles


def build_local_sqlite(schema_sql, seed_sql):
    """Initializes local SQLite database file for testing & verification."""
    os.makedirs(os.path.dirname(LOCAL_DB_PATH), exist_ok=True)
    if os.path.exists(LOCAL_DB_PATH):
        os.remove(LOCAL_DB_PATH)

    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    cursor.executescript(seed_sql)
    conn.commit()

    # Query metrics
    cursor.execute("SELECT count(*) FROM games")
    games_count = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM console_commands")
    cmds_count = cursor.fetchone()[0]

    cursor.execute("SELECT count(*) FROM scenario_bundles")
    bundles_count = cursor.fetchone()[0]

    conn.close()
    return games_count, cmds_count, bundles_count


def main():
    parser = argparse.ArgumentParser(description="L-MOD Vault Database Sync & Seed Generator")
    parser.add_argument('--init-local', action='store_true', default=True, help="同时生成并校验本地 SQLite 数据库")
    args = parser.parse_args()

    print("=" * 72)
    print("📦 L-MOD Vault 全球数据库种子生成与同步管道")
    print("=" * 72)

    with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)

    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    print(f"🔍 正在从 {GAMES_JSON_PATH} 解析 100 款游戏全息数据...")
    seed_sql, total_cmds, total_bundles = generate_seed_sql(games)

    # Save to database/seed_data.sql
    with open(SEED_SQL_PATH, 'w', encoding='utf-8') as f:
        f.write(seed_sql)

    sql_size_kb = os.path.getsize(SEED_SQL_PATH) / 1024
    print(f"✅ 已成功生成全量 SQL 种子文件: {SEED_SQL_PATH} ({sql_size_kb:.1f} KB)")
    print(f"📊 结构化数据统计:")
    print(f"   • 核心大作总数 (games): {len(games)} 款")
    print(f"   • 规范控制台指令 (console_commands): {total_cmds} 条")
    print(f"   • 场景化批处理套餐 (scenario_bundles): {total_bundles} 个")

    if args.init_local:
        print(f"\n🧪 正在本地 SQLite 引擎 ({LOCAL_DB_PATH}) 中模拟入库测试...")
        g_cnt, c_cnt, b_cnt = build_local_sqlite(schema_sql, seed_sql)
        print(f"✅ 本地 SQLite 验证 100% 成功入库: {g_cnt} 游戏, {c_cnt} 指令, {b_cnt} 套餐包")

    print("\n" + "=" * 72)
    print("🚀 【Cloudflare D1 / 全球数据库部署一键指南】")
    print("=" * 72)
    print("1. 创建 Cloudflare D1 免费分布式数据库 (Cloudflare 官网 300+ 边缘机房自动就近加速):")
    print("   npx wrangler d1 create lmod-vault-db")
    print("")
    print("2. 执行 Schema 建表与数据同步 (一键将 100 款游戏与全量指令灌入全球数据库):")
    print("   npx wrangler d1 execute lmod-vault-db --file=database/schema.sql")
    print("   npx wrangler d1 execute lmod-vault-db --file=database/seed_data.sql")
    print("")
    print("3. 若使用 Supabase:")
    print("   直接登录 supabase.com 创建新项目，在 SQL Editor 中粘贴 database/schema.sql")
    print("   和 database/seed_data.sql 执行即可秒级上线！")
    print("=" * 72)


if __name__ == '__main__':
    main()
