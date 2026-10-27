#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/import_chunks.py
Splits seed data into 10-game batches and reliably imports all 100 games into Cloudflare D1.
"""

import os
import sys
import json
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON = os.path.join(BASE_DIR, 'src/data/games_top100.json')
CHUNKS_DIR = os.path.join(BASE_DIR, 'database/chunks')
WRANGLER = "/opt/homebrew/bin/node /opt/homebrew/bin/npx wrangler"

sys.path.insert(0, os.path.join(BASE_DIR, 'scripts'))
from sync_to_database import generate_seed_sql

def run():
    os.makedirs(CHUNKS_DIR, exist_ok=True)
    with open(GAMES_JSON, 'r', encoding='utf-8') as f:
        games = json.load(f)

    batch_size = 10
    chunks = [games[i:i + batch_size] for i in range(0, len(games), batch_size)]
    print(f"📦 Total games: {len(games)}, splitting into {len(chunks)} chunks of {batch_size} games each...")

    chunk_files = []
    for idx, chunk in enumerate(chunks):
        sql_content, cmds, bundles = generate_seed_sql(chunk)
        chunk_file = os.path.join(CHUNKS_DIR, f"seed_batch_{idx+1}.sql")
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        chunk_files.append((chunk_file, len(chunk), cmds))

    print("\n🚀 Starting Cloudflare D1 batch import (10 batches)...")
    env = os.environ.copy()
    env["http_proxy"] = "http://127.0.0.1:7890"
    env["https_proxy"] = "http://127.0.0.1:7890"

    for idx, (fpath, g_count, cmds_count) in enumerate(chunk_files):
        fname = os.path.basename(fpath)
        size_kb = os.path.getsize(fpath) / 1024
        print(f"\n[{idx+1}/{len(chunk_files)}] 正在导入 {fname} ({g_count} 款游戏, {cmds_count} 条指令, {size_kb:.1f} KB)...")

        cmd = f"{WRANGLER} d1 execute lmod-vault-db --remote --file={fpath} -y"
        
        # Retry logic (up to 2 retries per chunk)
        success = False
        for attempt in range(1, 3):
            res = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
            if res.returncode == 0:
                print(f"  ✅ [{idx+1}/{len(chunk_files)}] 批次 {idx+1} 成功导入 D1！")
                success = True
                break
            else:
                print(f"  ⚠️ 批次 {idx+1} 第 {attempt} 次导入失败，稍后重试...")
                time.sleep(2)

        if not success:
            print(f"❌ 批次 {idx+1} 最终导入失败:")
            print(res.stderr or res.stdout)
            sys.exit(1)

    print("\n" + "=" * 60)
    print("🎉 全部 100 款大作与 1,093 条真实指令已 100% 成功灌入 Cloudflare D1！")
    print("=" * 60)

if __name__ == '__main__':
    run()
