#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/schedule_tracker.py
L-MOD Vault 内容生产排期与进度追踪管理工具 (Schedule Tracker)
支持：
- list: 展示 Rank 5 ~ Rank 10 游戏的周排期看板与阶段矩阵；
- status <game_id>: 查询单款游戏的深度采掘与物料进度；
- advance <game_id> <stage> <status>: 推进指定游戏在流水线中的作业状态；
- report: 输出 Milestone 3 生产健康报告。
"""

import os
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEDULE_FILE = BASE_DIR / "src" / "data" / "production_schedule.json"
DATA_PATH = BASE_DIR / "src" / "data" / "games_top100.json"

STAGE_MAP = {
    "T-4": "T_minus_4_mining",
    "T-3": "T_minus_3_qa_gate",
    "T-2": "T_minus_2_visuals",
    "T-1": "T_minus_1_publishing",
    "T+0": "T_plus_0_community"
}

STATUS_ICONS = {
    "COMPLETED": "🟢 完成",
    "PASSED": "🟢 通过",
    "IN_PROGRESS": "🟡 进行中",
    "READY_FOR_RENDER": "🔵 待出图",
    "SCHEDULED": "⏳ 排期中",
    "PLANNED": "⚪ 规划中",
    "QUEUED": "⏳ 队列中",
    "PENDING": "⚪ 等待中",
    "FAILED": "🔴 未通过"
}

def load_schedule():
    if not SCHEDULE_FILE.exists():
        print(f"❌ 找不到排期数据文件: {SCHEDULE_FILE}")
        sys.exit(1)
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_schedule(data):
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def print_board():
    data = load_schedule()
    print("\n" + "=" * 115)
    print("📋 L-MOD Vault 旗舰游戏内容生产与自媒体排期总看板 (Milestone 3 / Rank 5 ~ Rank 10)")
    print("=" * 115)
    print(f"{'Rank':<5} | {'游戏名称':<22} | {'周期':<8} | {'T-4采掘':<8} | {'T-3门禁':<8} | {'T-2物料':<8} | {'T-1发布':<8} | {'发布日期':<10} | {'当前状态'}")
    print("-" * 115)

    for g in data.get("games", []):
        rank = f"Rank {g['rank']}"
        title = g["title"][:20]
        cycle = g["weekCycle"].split()[0]
        st = g.get("status", {})
        t4 = STATUS_ICONS.get(st.get("T_minus_4_mining", ""), st.get("T_minus_4_mining", ""))
        t3 = STATUS_ICONS.get(st.get("T_minus_3_qa_gate", ""), st.get("T_minus_3_qa_gate", ""))
        t2 = STATUS_ICONS.get(st.get("T_minus_2_visuals", ""), st.get("T_minus_2_visuals", ""))
        t1 = STATUS_ICONS.get(st.get("T_minus_1_publishing", ""), st.get("T_minus_1_publishing", ""))
        pub = g.get("targetPublishDate", "待定")
        stats = g.get("stats", {})
        stat_summary = f"{stats.get('categories', 0)}类/{stats.get('commands', 0)}条指令/{stats.get('mods', 0)}Mods"
        print(f"{rank:<5} | {title:<22} | {cycle:<8} | {t4:<8} | {t3:<8} | {t2:<8} | {t1:<8} | {pub:<10} | {stat_summary}")

    print("=" * 115)
    print("💡 每日生产节奏: 周一(T-4逆向拆包) ➔ 周二(T-3双重门禁) ➔ 周三(T-2出图总装) ➔ 周四/五(T-1矩阵发布) ➔ 周末(T+0社群雷达)")
    print("=" * 115 + "\n")

def print_game_status(game_id: str):
    data = load_schedule()
    g = next((x for x in data.get("games", []) if x["id"] == game_id), None)
    if not g:
        print(f"❌ 未在排期表中找到游戏 ID: '{game_id}'")
        return

    print(f"\n========================================================")
    print(f"🎮 游戏生产档案: Rank {g['rank']} - {g['title']}")
    print(f"========================================================")
    print(f"• 底层引擎架构: {g['engine']}")
    print(f"• 核心调试框架: {g['framework']}")
    print(f"• 排期归属周次: {g['weekCycle']} (目标发布日: {g['targetPublishDate']})")
    print(f"• 责任团队节点: {g['owner']}")
    print(f"• 核心攻坚亮点: {g['keyFocus']}")
    print(f"\n📊 工业资产对账:")
    st = g.get("stats", {})
    print(f"  - 八大分类大类: {st.get('categories', 0)}/8")
    print(f"  - 真实执行指令: {st.get('commands', 0)}/40")
    print(f"  - 精选 N网 Mod: {st.get('mods', 0)}/4")
    print(f"  - FLiNG修改器: {'✅ 已配置' if st.get('trainerReady') else '❌ 未配置'}")

    print(f"\n🚦 五步流水线推进状态:")
    flow = g.get("status", {})
    for stage_code, field in STAGE_MAP.items():
        val = flow.get(field, "PENDING")
        icon = STATUS_ICONS.get(val, val)
        desc = data["weeklyCadence"]["timelinePhases"].get(next(k for k in data["weeklyCadence"]["timelinePhases"] if stage_code in k), "")
        print(f"  [{stage_code}] {icon:<10} -> {desc}")
    print("========================================================\n")

def advance_stage(game_id: str, stage_arg: str, new_status: str = "COMPLETED"):
    data = load_schedule()
    g = next((x for x in data.get("games", []) if x["id"] == game_id), None)
    if not g:
        print(f"❌ 未在排期表中找到游戏 ID: '{game_id}'")
        return

    field = STAGE_MAP.get(stage_arg.upper())
    if not field:
        # 尝试匹配字段本身
        if stage_arg in g.get("status", {}):
            field = stage_arg
        else:
            print(f"❌ 非法阶段标识 '{stage_arg}'，请使用 T-4, T-3, T-2, T-1, T+0 之一")
            return

    old_status = g["status"].get(field, "UNKNOWN")
    g["status"][field] = new_status
    save_schedule(data)
    print(f"✅ 已成功更新 [{g['title']}] 的阶段 [{stage_arg}]：{old_status} ➔ {new_status}")

def generate_report():
    data = load_schedule()
    games = data.get("games", [])
    total = len(games)
    mining_done = sum(1 for g in games if g["status"].get("T_minus_4_mining") in ("COMPLETED", "PASSED"))
    qa_passed = sum(1 for g in games if g["status"].get("T_minus_3_qa_gate") == "PASSED")
    visual_ready = sum(1 for g in games if g["status"].get("T_minus_2_visuals") in ("COMPLETED", "READY_FOR_RENDER"))

    print("\n========================================================")
    print("📈 L-MOD Vault Milestone 3 生产进度与健康度综合报告")
    print("========================================================")
    print(f"• 覆盖大作矩阵: Rank 5 ~ Rank 10 (共计 {total} 款旗舰大作)")
    print(f"• 技术采掘达标: {mining_done}/{total} 款 (已完成深度全息数据挖掘)")
    print(f"• 门禁双严核验: {qa_passed}/{total} 款 (已达成 Schema/Linter 双 [PASS])")
    print(f"• 视觉出图就绪: {visual_ready}/{total} 款 (已准备好出图物料规范)")
    print(f"\n🏆 当前已全线攻克的旗舰级大作 (100% 具备工业级出厂标准):")
    for g in games:
        if g["status"].get("T_minus_3_qa_gate") == "PASSED":
            print(f"   ★ Rank {g['rank']:2d}: {g['title']:<25} ({g['engine']})")
    print("========================================================\n")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "list"
    if action == "list":
        print_board()
    elif action == "status":
        gid = sys.argv[2] if len(sys.argv) > 2 else "elden-ring"
        print_game_status(gid)
    elif action == "advance":
        if len(sys.argv) < 4:
            print("用法: python3 scripts/schedule_tracker.py advance <game_id> <stage> [new_status]")
        else:
            gid = sys.argv[2]
            stg = sys.argv[3]
            nst = sys.argv[4] if len(sys.argv) > 4 else "COMPLETED"
            advance_stage(gid, stg, nst)
    elif action == "report":
        generate_report()
    else:
        print_board()
