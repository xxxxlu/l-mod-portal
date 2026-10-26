#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/sanitize_database_bulk.py
L-MOD Vault Rank 15~100 批量自动化清洗与无害化去毒引擎 (Milestone 2 Final)

核心业务逻辑与防护机制：
1. 核心大作绝对保护：Rank 1~14 核心大作数据 100% 保持原样，绝不覆盖或降级已有 725 条指令与全息架构；
2. 批量无害化清洗与结构归一化 (Rank 15 ~ Rank 100，共 86 款游戏)：
   - 全面剔除虚假占位符：彻底清除在非原生控制台单机中遗留的通用假指令 (如 god, noclip, addmoney, killall, fly 等)；
   - 依据引擎特征精准分流与真实性重定向：
     * 原生控制台单机 (如 P社三部曲、FNV、骑砍2、星露谷、深海迷航、幻兽帕鲁/ARK、Valheim 等 21 款)：
       保留真实引擎指令，补全 Schema 强类型字段 (id, syntax_type, min_version, framework_required)，
       校准 popularCommands 为真实指令，杜绝任何占位字符；
     * 无原生打字控制台单机 (如动作 RPG、魂系、日系主机移植等 65 款)：
       hasConsole 真实校准为 False，清空虚假指令分类 (consoleCategories=[])，popularCommands 置空，
       重定向至 FLiNG 纯净修改器、开源前置运行库及安全离线免封指引；
3. 数据完整性兜底：
   - 校验 8 语言 titles 完整性；
   - 确保 trainerInfo 与 curatedMods 规范完整；
4. 原子双库同步持久化：
   - 更新 src/data/games_top100.json；
   - 同步写回 public/data.js (导出 window.GAMES_DATA, window.GAMES_DATABASE, window.TRANSLATIONS_DATA)。
"""

import os
import sys
import json
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, "src", "data", "games_top100.json")
DATA_JS_PATH = os.path.join(BASE_DIR, "public", "data.js")

# 21 款拥有官方原生打字控制台 / 开发者模式 / 官方调试工具链的游戏 ID 白名单
NATIVE_CONSOLE_GAMES = {
    "mount-and-blade-2",       # Rank 15: TaleWorlds 原生 Alt+~ 终端
    "stardew-valley",          # Rank 16: SMAPI 命令行终端 / 动物命名代码
    "subnautica",              # Rank 19: Unity 原生 ~ / Shift+Enter 终端
    "valheim",                 # Rank 21: Unity 原生 -console + F5 devcommands
    "fallout-new-vegas",       # Rank 25: Bethesda Creation/Gamebryo 原生 ~ 控制台
    "rimworld",                # Rank 26: Unity 原生开发者模式 (Development Mode)
    "sons-of-the-forest",      # Rank 29: 原生 cheatstick 盲打后 F1 控制台
    "satisfactory",            # Rank 30: 原生高级游戏设置 (AGS) + Ctrl+Shift+L 终端
    "factorio",                # Rank 31: 原生 Lua ~ / / 控制台
    "crusader-kings-3",        # Rank 34: P社 Clausewitz 原生 -debug_mode 终端
    "hearts-of-iron-4",        # Rank 35: P社 Clausewitz 原生 ~ 终端
    "stellaris",               # Rank 36: P社 Clausewitz 原生 ~ 终端
    "kingdom-come-deliverance",# Rank 48: CryEngine 原生 -devmode 终端
    "7-days-to-die",           # Rank 72: Unity 原生 F1 dm / cm 终端
    "ark-survival-evolved",    # Rank 73: UE4 原生 Tab admincheat 终端
    "the-sims-4",              # Rank 78: 原生 Ctrl+Shift+C testingcheats 终端
    "euro-truck-simulator-2",  # Rank 81: Prism3D 原生 ~ 开发者终端
    "beamng-drive",            # Rank 85: 原生 ~ Lua 终端 + F11 世界编辑器
    "hades",                   # Rank 98: Supergiant 原生神魔模式 / 调试配置
    "hollow-knight",           # Rank 99: Unity Scarab + DebugMod F1 菜单
    "slay-the-spire"           # Rank 100: Unity ModTheSpire + BaseMod ~ 终端
}

VALID_SYNTAX_TYPES = [
    'ue_console', 'gm_command', 'lua_function', 'creation_hex',
    'redengine_cmd', 'unity_dev', 'reframework_action', 'trainer_hotkey'
]

def normalize_command_metadata(gid, cmd_dict, cmd_idx):
    """
    规范化单条控制台指令的强类型元数据，确保满足 Schema 要求。
    """
    # 1. 确保唯一 ID
    if not cmd_dict.get("id"):
        cmd_dict["id"] = f"{gid}_cmd_{cmd_idx + 1}"

    # 2. 匹配并矫正合法语法类型 syntax_type
    current_st = cmd_dict.get("syntax_type")
    if current_st not in VALID_SYNTAX_TYPES:
        if gid in ["fallout-new-vegas", "skyrim-se", "fallout-4", "starfield"]:
            cmd_dict["syntax_type"] = "creation_hex"
        elif gid in ["factorio", "beamng-drive"]:
            cmd_dict["syntax_type"] = "lua_function"
        elif gid in ["ark-survival-evolved"]:
            cmd_dict["syntax_type"] = "ue_console"
        elif gid in ["rimworld", "valheim", "subnautica", "7-days-to-die", "stardew-valley", "hollow-knight", "slay-the-spire"]:
            cmd_dict["syntax_type"] = "unity_dev"
        else:
            cmd_dict["syntax_type"] = "gm_command"

    # 3. 补齐最低版本限制 min_version
    if not cmd_dict.get("min_version"):
        cmd_dict["min_version"] = "v1.0+ (Latest Official Patch)"

    # 4. 补齐依赖框架 framework_required
    if not cmd_dict.get("framework_required"):
        if gid == "hollow-knight":
            cmd_dict["framework_required"] = "Scarab / DebugMod"
        elif gid == "slay-the-spire":
            cmd_dict["framework_required"] = "ModTheSpire + BaseMod"
        elif gid == "stardew-valley":
            cmd_dict["framework_required"] = "SMAPI"
        elif gid == "kingdom-come-deliverance":
            cmd_dict["framework_required"] = "Cheat Mod (-devmode)"
        elif gid in ["hearts-of-iron-4", "crusader-kings-3", "stellaris"]:
            cmd_dict["framework_required"] = "Clausewitz Engine (-debug_mode)"
        else:
            cmd_dict["framework_required"] = "Native Engine Console"


def sanitize_database():
    print("=" * 70)
    print("🚀 启动 L-MOD Vault 数据库 Rank 15~100 批量无害化清洗与真实性校准")
    print("=" * 70)

    if not os.path.exists(GAMES_JSON_PATH):
        print(f"❌ 错误: 数据文件未找到 {GAMES_JSON_PATH}")
        sys.exit(1)

    # 备份原始数据库防灾
    backup_path = GAMES_JSON_PATH + ".bak"
    shutil.copyfile(GAMES_JSON_PATH, backup_path)
    print(f"📦 已建立原子备份: {backup_path}")

    with open(GAMES_JSON_PATH, "r", encoding="utf-8") as f:
        games = json.load(f)

    print(f"📊 载入游戏总数: {len(games)} 款")

    tier1_preserved = 0
    native_enriched = 0
    non_console_sanitized = 0

    for game in games:
        rank = game.get("rank", 999)
        gid = game.get("id", "")
        title = game.get("title", "")

        # -------------------------------------------------------------
        # 1. 核心防护：Rank 1~14 绝不篡改降级
        # -------------------------------------------------------------
        if rank <= 14:
            tier1_preserved += 1
            continue

        # -------------------------------------------------------------
        # 2. 原生控制台单机 (21 款)：保留并校准真实指令
        # -------------------------------------------------------------
        if gid in NATIVE_CONSOLE_GAMES:
            game["hasConsole"] = True

            # 结构化遍历与元数据规范
            cmd_counter = 0
            for cat in game.get("consoleCategories", []):
                for cmd in cat.get("commands", []):
                    normalize_command_metadata(gid, cmd, cmd_counter)
                    cmd_counter += 1

            # 真实性校准 popularCommands：取各分类前列真实指令，杜绝占位符与通用裸词
            pop_cmds = []
            generic_blacklist = {"god", "godmode", "god mode", "noclip", "fly", "kill", "addmoney", "giveall"}
            for cat in game.get("consoleCategories", []):
                for cmd in cat.get("commands", []):
                    code = cmd.get("code", "").strip()
                    if code.lower() in generic_blacklist:
                        continue
                    pop_cmds.append({
                        "name": cmd.get("name"),
                        "command": code,
                        "desc": cmd.get("desc")
                    })
                    if len(pop_cmds) >= 4:
                        break
                if len(pop_cmds) >= 4:
                    break
            game["popularCommands"] = pop_cmds
            native_enriched += 1

        # -------------------------------------------------------------
        # 3. 无原生控制台单机 (65 款)：真实置为 False，清空假指令，重定向修改器
        # -------------------------------------------------------------
        else:
            game["hasConsole"] = False
            game["consoleCategories"] = []
            game["popularCommands"] = []
            game["consoleShortcut"] = "无原生打字控制台 (请使用纯净修改器或离线前置)"
            game["consoleEnableGuide"] = {
                "zh-CN": f"《{title}》无官方原生打字控制台命令行。为保证游戏单机体验与存档安全，已为您校准并直连官方经认证的 FLiNG 纯净修改器（支持按键自由映射与多倍经验/不减物资）及开源前置环境，请前往【修改器】或【精选 MOD】专区直接获取。",
                "en": f"{title} does not feature a native in-game typing console. For safe single-player offline exploration, please refer to the verified FLiNG Trainer (clean hotkey toggles) or open-source community frameworks in the Trainer and Mods tabs below."
            }
            non_console_sanitized += 1

        # -------------------------------------------------------------
        # 4. 数据完整性兜底 (8 语言 titles 与放行说明保障)
        # -------------------------------------------------------------
        titles = game.get("titles", {})
        required_langs = ["zh-CN", "en", "zh-TW", "ja", "ko", "ru", "de", "es"]
        for lang in required_langs:
            if lang not in titles or not titles[lang]:
                titles[lang] = titles.get("en") or title

        trainer = game.setdefault("trainerInfo", {})
        if not trainer.get("officialUrl"):
            trainer["officialUrl"] = f"https://flingtrainer.com/trainer/{gid}-trainer/"
        
        sv = trainer.setdefault("safeVerification", {})
        if not sv.get("powershellExclusionCmd"):
            sv["powershellExclusionCmd"] = 'Add-MpPreference -ExclusionPath "D:\\Games\\Trainers"'
        if not sv.get("troubleshootSteps"):
            sv["troubleshootSteps"] = [
                "1. 【坚决抵制流氓捆绑】请务必通过上方官方绿色按钮前往 FLiNG 官方网站下载 Standalone 独立版；",
                "2. 【Windows Defender 报毒排错】内存修改器调用底层系统 API 易被误报为 HackTool，原版绝不含木马；",
                "3. 【10秒一键白名单】建立专用文件夹并运行上方 PowerShell 指令排除误杀；",
                "4. 【运行顺序】建议先启动游戏进入战役，再以管理员身份运行修改器激活。"
            ]

    # -----------------------------------------------------------------
    # 5. 写入主数据库 src/data/games_top100.json
    # -----------------------------------------------------------------
    with open(GAMES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    print(f"💾 主数据库保存完成: {GAMES_JSON_PATH}")

    # -----------------------------------------------------------------
    # 6. 读取已有翻译字典并同步写回 public/data.js
    # -----------------------------------------------------------------
    translations_data = {}
    if os.path.exists(DATA_JS_PATH):
        with open(DATA_JS_PATH, "r", encoding="utf-8") as f:
            js_raw = f.read()
            marker = "window.TRANSLATIONS_DATA = "
            idx = js_raw.find(marker)
            if idx != -1:
                t_json_str = js_raw[idx + len(marker):].strip()
                if t_json_str.endswith(";"):
                    t_json_str = t_json_str[:-1]
                try:
                    translations_data = json.loads(t_json_str)
                except Exception as e:
                    print(f"⚠️ 解析 TRANSLATIONS_DATA 出错: {e}")

    # 若未成功提取，从 build_i18n_matrix 模块导入兜底
    if not translations_data:
        try:
            sys.path.append(os.path.join(BASE_DIR, "scripts"))
            from build_i18n_matrix import TRANSLATIONS
            translations_data = TRANSLATIONS
        except Exception as e:
            print(f"⚠️ 导入 build_i18n_matrix 出错: {e}")

    with open(DATA_JS_PATH, "w", encoding="utf-8") as f:
        f.write("// L-MOD Vault Offline Database (Auto-bundled & Sanitized)\n")
        f.write("window.GAMES_DATA = " + json.dumps(games, ensure_ascii=False, indent=2) + ";\n\n")
        f.write("window.GAMES_DATABASE = window.GAMES_DATA;\n\n")
        f.write("window.TRANSLATIONS_DATA = " + json.dumps(translations_data, ensure_ascii=False, indent=2) + ";\n")
    print(f"💾 前端离线数据库双库同步完成: {DATA_JS_PATH}")

    print("\n" + "=" * 70)
    print("🎉 清洗汇总统计:")
    print(f"  • Rank 1~14 核心大作绝对保护: {tier1_preserved} 款 (零改动)")
    print(f"  • Rank 15~100 原生控制台真实校准: {native_enriched} 款 (保留并规范真实指令)")
    print(f"  • Rank 15~100 无原生控制台无害化去毒: {non_console_sanitized} 款 (清空虚假指令分类)")
    print(f"  • 全库总计: {len(games)} 款游戏")
    print("=" * 70)

if __name__ == "__main__":
    sanitize_database()
