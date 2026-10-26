#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/pipeline_gate.py
L-MOD Vault 工业级五步作业流水线全流程自动化质检调度器 (Pipeline Gate)
功能：
1. 运行 validate_game.py 执行强类型 Schema 静态严苛校验；
2. 运行 audit_game_data.py 执行引擎语法与数据规模 Linter；
3. 检查社交矩阵素材与出图准备度 (Hook Preset / 5联图导出状态)；
4. 输出五步流水线 (T-4 ~ T+0) 综合诊断仪表盘与门禁状态。
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
DATA_PATH = BASE_DIR / "src" / "data" / "games_top100.json"
DIST_DIR = BASE_DIR / "social_distribution"

def run_command(cmd_args):
    result = subprocess.run(cmd_args, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def check_pipeline(game_id: str):
    print(f"\n========================================================")
    print(f"🚀 L-MOD Vault 五步工业级流水线门禁自检调度器: [{game_id}]")
    print(f"========================================================")

    if not DATA_PATH.exists():
        print(f"❌ 找不到主数据库文件: {DATA_PATH}")
        sys.exit(1)

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        games = json.load(f)

    target = next((g for g in games if g.get("id") == game_id), None)
    if not target:
        print(f"❌ 未在数据库中找到游戏 ID: '{game_id}'")
        sys.exit(1)

    title = target.get("title", game_id)
    rank = target.get("rank", 999)
    categories = target.get("consoleCategories", [])
    cmd_count = sum(len(c.get("commands", [])) for c in categories)
    mod_count = len(target.get("curatedMods", []))
    has_trainer = target.get("hasTrainer", False)

    print(f"🎮 目标游戏: Rank {rank} - {title}")
    print(f"📊 当前全息数据资产: {len(categories)} 大分类 | {cmd_count} 条指令 | {mod_count} 个精选 Mod | 修改器配置: {has_trainer}\n")

    # Step 1: T-4 技术采掘与数据完整性诊断
    t4_pass = len(categories) >= (8 if rank <= 10 else 4) and cmd_count >= (40 if rank <= 10 else 15) and mod_count >= 3
    t4_icon = "🟢 [PASS]" if t4_pass else "🔴 [FAIL]"
    print(f"1️⃣  【T-4 技术采掘对账】 {t4_icon}")
    print(f"    • 八大系统维度: {len(categories)}/8 {'达标' if len(categories)>=8 else '不足'}")
    print(f"    • 零假代码指令池: {cmd_count}/40 {'达标' if cmd_count>=40 else '不足'}")
    print(f"    • 精选Mod生态链: {mod_count}/3 {'达标' if mod_count>=3 else '不足'}")

    # Step 2: T-3 自动化门禁双重校验
    val_script = SCRIPTS_DIR / "validate_game.py"
    audit_script = SCRIPTS_DIR / "audit_game_data.py"

    val_ok, val_out, _ = run_command([sys.executable, str(val_script), game_id])
    audit_ok, audit_out, _ = run_command([sys.executable, str(audit_script), game_id])

    t3_pass = val_ok and audit_ok
    t3_icon = "🟢 [PASS]" if t3_pass else "🔴 [FAIL]"
    print(f"\n2️⃣  【T-3 本地门禁质检】 {t3_icon}")
    print(f"    • 强类型 Schema 静态校验: {'✅ 通过' if val_ok else '❌ 未通过'}")
    print(f"    • 引擎语法 Linter 与规模门禁: {'✅ 通过' if audit_ok else '❌ 未通过'}")
    if not t3_pass:
        if not val_ok:
            print("    [Schema 报错详情]:")
            for line in val_out.splitlines()[-6:]:
                print(f"       {line}")
        if not audit_ok:
            print("    [Linter 报错详情]:")
            for line in audit_out.splitlines()[-6:]:
                print(f"       {line}")

    # Step 3: T-2 视觉出图与物料就绪度
    # 检查是否已生成物料包目录
    target_dist = None
    for folder in DIST_DIR.glob(f"*_{game_id}"):
        if folder.is_dir():
            target_dist = folder
            break

    card_count = len(list((target_dist / "images").glob("*.png"))) if target_dist and (target_dist / "images").exists() else 0
    has_xhs = (target_dist / "xiaohongshu_post.md").exists() if target_dist else False
    has_bili = (target_dist / "bilibili_dynamic.md").exists() if target_dist else False

    t2_pass = card_count >= 5 and has_xhs and has_bili
    t2_icon = "🟢 [READY]" if t2_pass else "🟡 [PENDING]"
    print(f"\n3️⃣  【T-2 视觉出图物料】 {t2_icon}")
    print(f"    • 1080x1440 5联图卡片: {card_count}/5 张导出")
    print(f"    • 小红书脱敏文案: {'✅ 已就绪' if has_xhs else '⏳ 待生成'}")
    print(f"    • B站动态/专栏文案: {'✅ 已就绪' if has_bili else '⏳ 待生成'}")

    # Step 4 & 5: 发布与沉淀状态指示
    print(f"\n4️⃣  【T-1 矩阵发布规划】 ⏳ 待发布 (排期规划中)")
    print(f"5️⃣  【T+0 社群沉淀监控】 ⏳ 首评话术与雷达待接入")

    print(f"\n--------------------------------------------------------")
    if t3_pass:
        print(f"🎉 恭喜！[{game_id}] 核心数据采掘与 Schema/Linter 门禁已 100% 通过！")
        print(f"👉 下一步动作：执行 `python3 scripts/generate_social_matrix.py {game_id}` 生成社交物料！")
    else:
        print(f"⚠️  警告：[{game_id}] 尚未完全通过技术门禁，请根据上方报错修正后再推下一步！")
    print(f"--------------------------------------------------------\n")
    return t3_pass

if __name__ == "__main__":
    gid = sys.argv[1] if len(sys.argv) > 1 else "elden-ring"
    check_pipeline(gid)
