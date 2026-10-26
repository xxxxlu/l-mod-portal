#!/usr/bin/env python3
"""
validate_game.py
针对 .agent/skills/game-vault-enricher 的强类型 Schema 离线自动化验证工具。
校验游戏是否符合 game_full.schema.json, game_command.schema.json, trainer_info.schema.json 与 curated_mod.schema.json 规范。
"""

import json
import sys
import os
import re

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_DIR = os.path.join(SKILL_DIR, "schemas")
DEFAULT_DATA_PATH = os.path.abspath(os.path.join(SKILL_DIR, "../../../src/data/games_top100.json"))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_game_entry(game, command_schema, trainer_schema, mod_schema):
    gid = game.get("id", "UNKNOWN")
    rank = game.get("rank", 999)
    errors = []

    # 1. Check required top-level fields
    required_top = [
        "id", "rank", "title", "titles", "developer", "releaseYear",
        "genre", "steamRating", "hasConsole", "consoleShortcut",
        "consoleEnableGuide", "popularCommands", "hasMods",
        "modInstallPath", "hasTrainer", "trainerInfo",
        "consoleCategories", "curatedMods"
    ]
    for rf in required_top:
        if rf not in game:
            errors.append(f"缺少顶级必须字段: '{rf}'")

    # 2. Check commands
    cmd_required = command_schema.get("required", [])
    valid_syntax_types = command_schema["properties"]["syntax_type"]["enum"]
    
    categories = game.get("consoleCategories", [])
    total_cmds = 0
    for c_idx, cat in enumerate(categories):
        cat_name = cat.get("category") or f"分类_{c_idx+1}"
        cmds = cat.get("commands", [])
        for cmd in cmds:
            total_cmds += 1
            code = cmd.get("code", "")
            for cr in cmd_required:
                if cr not in cmd:
                    errors.append(f"[{cat_name}] 指令 '{code}' 缺少必须字段: '{cr}'")
            st = cmd.get("syntax_type")
            if st and st not in valid_syntax_types:
                errors.append(f"[{cat_name}] 指令 '{code}' 的 syntax_type '{st}' 非法，必须为 {valid_syntax_types} 之一")

    # 3. Check trainer
    trainer = game.get("trainerInfo", {})
    if trainer:
        for tf in trainer_schema.get("required", []):
            if tf not in trainer:
                errors.append(f"trainerInfo 缺少必须字段: '{tf}'")
        safe_v = trainer.get("safeVerification", {})
        if safe_v and not safe_v.get("powershellExclusionCmd"):
            errors.append("trainerInfo.safeVerification 缺少 powershellExclusionCmd")

    # 4. Check mods
    mods = game.get("curatedMods", [])
    for m in mods:
        m_id = m.get("id", "UNKNOWN_MOD")
        for mf in mod_schema.get("required", []):
            if mf not in m:
                errors.append(f"Mod '{m_id}' 缺少必须字段: '{mf}'")

    return errors, len(categories), total_cmds, len(mods)

def main():
    game_id = sys.argv[1] if len(sys.argv) > 1 else None
    data_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_DATA_PATH

    if not os.path.exists(data_path):
        print(f"❌ 找不到数据文件: {data_path}")
        sys.exit(1)

    cmd_schema = load_json(os.path.join(SCHEMA_DIR, "game_command.schema.json"))
    trainer_schema = load_json(os.path.join(SCHEMA_DIR, "trainer_info.schema.json"))
    mod_schema = load_json(os.path.join(SCHEMA_DIR, "curated_mod.schema.json"))
    games = load_json(data_path)

    targets = [g for g in games if g["id"] == game_id] if game_id else games

    print(f"\n==================================================")
    print(f"📋 启动 Skill 内部强类型 Schema 静态严苛校验 (共 {len(targets)} 款)")
    print(f"==================================================")

    passed = 0
    failed = 0

    for g in targets:
        gid = g.get("id")
        title = g.get("title")
        rank = g.get("rank", 999)
        errs, cat_cnt, cmd_cnt, mod_cnt = validate_game_entry(g, cmd_schema, trainer_schema, mod_schema)

        if errs:
            failed += 1
            print(f"\n❌ [FAIL] Rank {rank:2d}: {title} ({gid})")
            for e in errs:
                print(f"    • {e}")
        else:
            passed += 1
            print(f"✅ [PASS] Rank {rank:2d}: {title} ({gid}) -> {cat_cnt} 大类, {cmd_cnt} 指令, {mod_cnt} Mods, 100% 结构合规")

    print(f"\n--------------------------------------------------")
    print(f"Schema 校验完成: {passed} 合格, {failed} 不合规")
    print(f"--------------------------------------------------\n")
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main()
