#!/usr/bin/env python3
"""
audit_game_data.py (v2.0)
针对 l-mod-portal 游戏数据库的数据完整性、引擎语法合法性与真实性工业级自动化门禁脚本。

核心校验规则：
1. 真实性排查 (Anti-Fake Linter)：拦截在无原生打字控制台的游戏中出现通用假代码 (如 god, addmoney, noclip)；
2. 语法 Linter (Engine Syntax Linter)：
   - CET 驱动游戏 (如 赛博朋克 2077): 指令必须为合法 Lua/CET 语句 (以 Game. / local / vs = 开头)；
   - 虚幻引擎驱动游戏 (如 黑神话:悟空): 指令必须为合法 UE 控制台命令、原生 GM 命令或 UE4SS 脚本；
   - Bethesda Creation 引擎 (如 老滚5/辐射4): 物品指令必须为合法 Hex ID 及标准控制台格式；
3. 规模门禁指标：
   - Top 10 核心大作: 分类数 >= 8，指令总数 >= 40 条；
   - Top 30 热门单机: 分类数 >= 4，指令总数 >= 15 条；
4. 数据结构完整性：每条指令必须包含双语名称 (zh-CN, en)、可执行代码 code 及详细中文 desc；
5. FLiNG 修改器与 N网 Mod 真实性校验与安装指引完整性；
6. 结构化 Diff 报告：通过时输出详细分类结构与指令计数矩阵。
"""

import json
import sys
import os
import re

DATA_PATH = os.path.join(os.path.dirname(__file__), '../src/data/games_top100.json')

# 引擎已知关键词与特征映射
ENGINE_PROFILES = {
    "cyberpunk-2077": "cet",
    "black-myth-wukong": "ue5",
    "palworld": "ue5",
    "hogwarts-legacy": "ue4",
    "the-elder-scrolls-v-skyrim-special-edition": "creation",
    "skyrim-se": "creation",
    "fallout-4": "creation",
    "starfield": "creation",
    "baldurs-gate-3": "larian",
    "witcher-3": "witcher",
    "the-witcher-3-wild-hunt": "witcher",
    "elden-ring": "fromsoftware",
    "sekiro": "fromsoftware",
    "resident-evil-4": "reframework",
    "re4-remake": "reframework",
    "monster-hunter-world": "reframework",
    "gta-v": "rockstar_rage",
    "rdr2": "rockstar_rage",
    "hearts-of-iron-iv": "clausewitz",
    "stellaris": "clausewitz",
    "rimworld": "unity_dev",
    "factorio": "lua_factorio",
    "euro-truck-simulator-2": "prism3d",
    "slay-the-spire": "mod_the_spire",
}

# 通用占位符假代码黑名单（无该游戏原生引擎打字支持时绝对拦截）
GENERIC_FAKE_CODES = {
    "god", "godmode", "god mode",
    "addmoney", "add money", "addgold", "add cash",
    "noclip", "no clip", "fly",
    "giveall", "give all", "allweapons",
    "cheats 1", "sv_cheats 1", "debug 1"
}

# 虚幻引擎原生/调试命令前缀与常见 GM 命令
UE_VALID_COMMAND_PREFIXES = (
    "slomo ", "teleport", "toggledebugcamera", "showhud", "showhud ",
    "r.", "stat ", "viewmode ", "foliage.", "t.", "sg.", "tmm ",
    "allweapon", "allequip", "allhulu", "allitem", "allattritem",
    "allwine", "allseeds", "allrecipe", "alltaskitem", "allsoulskill",
    "alltalent", "allspell", "allmedition", "allmedition ", "allmap",
    "allcard", "alllegacy", "allachievements", "allmuseum", "allsurprise",
    "allarmortotop", "refreshallshop", "addexp ", "addtalentpoint ",
    "additem ", "soulskill ", "setspell ", "setsoulskill ", "setchapter ",
    "armortotop ", "costitem ", "card ", "mv ", "refreshshop ",
    "local ", "lib:", "StaticFindObject", "give ", "giveitem ", "spawn ", "addpal ",
    "unlock ", "setlevel ", "settime ", "fly", "ghost", "walk", "pal."
)

# 巫师 3 REDengine 3 原生控制台命令/函数白名单
WITCHER_VALID_PREFIXES = (
    "god", "likeaboss", "healme", "killall", "ciri", "geralt", "staminaboy",
    "secretgwint", "addgwintcards", "makeitrain", "stoprain", "witchcraft",
    "addmoney(", "removemoney(", "setlevel(", "levelup", "addskillpoints(",
    "addexp(", "cleardevelop", "additem(", "removeitem(", "showallft(", "showpins(",
    "allowft(", "showknownpins(", "settimer(", "settime(", "changeweather(",
    "gotonovigrad", "gotoskellige", "gotokaermorhen", "gotoprolog", "gotowyzima",
    "gototoussaint", "xy(", "spawn(", "learnskill(", "buffme(", "cat(", "drunk(",
    "appearance(", "wingwint(", "fadeout(", "fadein(", "setbeard(", "setcustomhead(",
    "shave", "dismember", "fov(", "resurrect"
)

def lint_command_syntax(gid, code):
    """
    针对各引擎语法进行严格 Linter 校验。
    返回 (is_valid, error_msg)
    """
    code_clean = code.strip()
    code_lower = code_clean.lower()
    engine_type = ENGINE_PROFILES.get(gid)

    # 1. 真实性检查：拦截通用裸词占位符
    # 针对巫师 3，god 为官方 REDengine 原生支持的指令；针对其他引擎拦截
    if engine_type == "witcher":
        is_witcher_valid = any(code_lower.startswith(prefix) for prefix in WITCHER_VALID_PREFIXES)
        if not is_witcher_valid:
            if code_lower in GENERIC_FAKE_CODES:
                return False, f"检测到通用虚假占位符代码 '{code_clean}'，未对接巫师3真实控制台指令"
            return False, f"巫师3控制台语法不合规: '{code_clean}' 不是有效的 WitcherScript 指令或函数"
        return True, ""

    if code_lower in GENERIC_FAKE_CODES:
        # 例外：Bethesda 引擎原生支持 tgm, 但 god 仍属于通用假占位符
        return False, f"检测到通用虚假占位符代码 '{code_clean}'，未对接该游戏真实引擎指令"

    # 2. 针对特定引擎的语法 Linter
    if engine_type == "cet":
        # CET 指令必须为合法 Lua / CET API
        if not (code_clean.startswith("Game.") or 
                code_clean.startswith("local ") or 
                code_clean.startswith("vs =") or 
                code_clean.startswith("for ") or 
                "Game.Get" in code_clean or 
                "Game.AddToInventory" in code_clean):
            return False, f"CET Lua 语法错误: '{code_clean}' 必须以 'Game.' 或合法 Lua 表达式开头"

    elif engine_type in ("ue4", "ue5"):
        # 虚幻引擎控制台指令或 GM 指令
        is_ue_valid = any(code_lower.startswith(prefix) for prefix in UE_VALID_COMMAND_PREFIXES)
        if not is_ue_valid:
            return False, f"虚幻引擎指令语法不合规: '{code_clean}' 不是合法的 UE 控制台参数或 GM 函数调用"

    elif engine_type == "creation":
        # Bethesda Creation 引擎 (Skyrim / Fallout 4 / Starfield)
        creation_prefixes = (
            "player.", "tgm", "tim", "tcl", "tmm ", "setstage ", "sqt", "help ",
            "moveto ", "coc ", "bat ", "tai", "tcai", "kill", "resurrect", "unlock",
            "showracemenu", "healplayer", "setav ", "modav ", "forceav ",
            "set timescale to ", "tfc", "sucsm ", "tm", "completequest ", "resetquest ",
            "getstage ", "psb", "fov ", "attachmod ", "removemod ", "inv", "csb",
            "fw ", "saq", "caqs", "scrapall", "equipitem ", "kah", "cgf "
        )
        is_creation_valid = any(code_lower.startswith(p) for p in creation_prefixes)
        if not is_creation_valid:
            return False, f"Creation 引擎指令不合规: '{code_clean}' 不是有效的 Bethesda 控制台指令"

    elif engine_type == "fromsoftware":
        # FromSoftware 专有引擎 (Elden Ring / Sekiro / DS3)
        # 魂系无原生打字命令行，使用规范化的热键/CT表动作/离线批处理脚本/参数注入
        fs_prefixes = (
            "[热键]", "[ct表]", "[tga]", "[item gib]", "[离线启动]", "[批处理]",
            "[modengine]", "[modengine2]", "[mod]",
            "num ", "ctrl+", "alt+", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
            "launchmod_eldenring", "start_protected_game", "modengine", "modengine2", "itemgib.", "param."
        )
        is_fs_valid = any(code_lower.startswith(p) for p in fs_prefixes) or "cheat table" in code_lower or "hotkey" in code_lower
        if not is_fs_valid:
            return False, f"FromSoftware 引擎指令不合规: '{code_clean}' 必须为标准热键、CT表注入或离线启动规范"

    elif engine_type == "reframework":
        # 卡普空 RE 引擎 / MT Framework (RE4 Remake / MHW / RE8)
        # 支持 REFramework ImGui 覆层、Stracker Loader 挂钩、原生小键盘热键
        rf_prefixes = (
            "[reframework]", "[imgui]", "[stracker]", "[overlay]", "[smarthunter]",
            "[shop]", "[fluffy]", "[热键]", "[insert]", "[f10]", "[ct表]", "[dinput8]",
            "num ", "ctrl+", "alt+", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10",
            "insert", "local "
        )
        is_rf_valid = any(code_lower.startswith(p) for p in rf_prefixes) or "reframework" in code_lower or "hotkey" in code_lower
        if not is_rf_valid:
            return False, f"REFramework / 卡普空引擎指令不合规: '{code_clean}' 必须为标准 REFramework 菜单路径、热键或脚本"

    elif engine_type == "rockstar_rage":
        # Rockstar RAGE 引擎 (GTA 5 / RDR 2)
        # 支持单机原生官方秘籍代码、ScriptHook 离线内置修改器路径与热键
        rage_prefixes = (
            "[f4] native trainer", "[f5] scripthookrdr2", "[scripthookv]", "[scripthookrdr2]",
            "[scripthook]", "[menyoo]", "[rampage]", "[热键]", "[trainer]", "[离线菜单]", "[lml]",
            "num ", "f4", "f5", "f7", "f8", "f3", "ctrl+", "alt+"
        )
        # 官方单机作弊码/短语白名单 (全小写匹配)
        rage_official_cheats = {
            "painkiller", "turtle", "catchme", "fugitive", "hoptoit", "skydive", "skyfall", "lawyerup",
            "deadeye", "comet", "rapidgt", "buzzoff", "barnstorm", "bandit", "trashed",
            "vinewood", "rocket", "liquor", "slowmo", "makeitrain", "snowday", "floater",
            "jhollywood", "powerup", "highex", "incendiary", "toolup", "hothands",
            "you want freedom", "you flourish before you die", "keep your balance on the curve",
            "seek all the bounty of this place", "you want more than you have", "you want punishment",
            "better than dog", "a simple life, a beautiful death", "death is silence",
            "history is written by fools", "abundance is the dullest desire", "greed is american virtue",
            "the lucky be strong evermore", "you long for sight and see nothing", "eat of knowledge",
            "share", "virtue unearned is not virtue", "my kingdom is a horse", "a fool on command",
            "guide me better", "make me better", "run! run! run!"
        }
        is_rage_valid = any(code_lower.startswith(p) for p in rage_prefixes) or code_lower in rage_official_cheats
        if not is_rage_valid:
            return False, f"Rockstar RAGE 引擎指令不合规: '{code_clean}' 必须为官方单机秘籍短语或 ScriptHook 菜单指令"

    elif engine_type == "larian":
        # 拉瑞安 Divinity 4.0 / Osiris / BG3 Script Extender
        is_larian_valid = (
            code_clean.startswith("Osi.") or 
            code_clean.startswith("_D(") or 
            code_clean.startswith("Ext.") or 
            code_clean.startswith("GetHostCharacter()") or 
            code_clean.startswith("TemplateAddTo") or 
            code_clean.startswith("local ") or 
            code_clean.startswith("for ") or 
            "Osi." in code_clean
        )
        if not is_larian_valid:
            return False, f"拉瑞安 Osiris / Script Extender 语法不合规: '{code_clean}' 必须以 'Osi.' 或合法 Lua/Osiris 表达式开头"

    return True, ""


def audit_game(game_id=None, verbose=True):
    if not os.path.exists(DATA_PATH):
        print(f"❌ 错误: 找不到数据库文件 {DATA_PATH}")
        return False

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)

    if game_id:
        target_games = [g for g in games if g["id"] == game_id]
        if not target_games:
            print(f"❌ 错误: 未在数据库中找到游戏 ID 为 '{game_id}' 的数据")
            return False
    else:
        target_games = games

    print(f"\n==================================================")
    print(f"🔍 启动 L-MOD Vault 游戏数据工业级自动化质检 (共检验 {len(target_games)} 款游戏)")
    print(f"==================================================")

    total_passed = 0
    total_failed = 0

    for g in target_games:
        gid = g["id"]
        title = g["title"]
        rank = g.get("rank", 999)
        issues = []
        diff_stats = []

        # 1. 检查控制台与指令大类
        categories = g.get("consoleCategories", [])
        total_cmds = sum(len(c.get("commands", [])) for c in categories)

        if rank <= 10:
            if len(categories) < 8:
                issues.append(f"Top 10 核心大作分类过少 (当前 {len(categories)} 类，硬性门槛需 ≥ 8 类)")
            if total_cmds < 40:
                issues.append(f"Top 10 核心大作指令严重不足 (当前 {total_cmds} 条，硬性门槛需 ≥ 40 条)")
        elif rank <= 30:
            if len(categories) < 4:
                issues.append(f"Top 30 热门单机分类过少 (当前 {len(categories)} 类，硬性门槛需 ≥ 4 类)")
            if total_cmds < 15:
                issues.append(f"Top 30 热门单机指令过少 (当前 {total_cmds} 条，硬性门槛需 ≥ 15 条)")

        # 检查分类与指令质量
        for idx, c in enumerate(categories):
            cat_name = c.get("category") or c.get("name") or f"分类_{idx+1}"
            cmds = c.get("commands", [])
            diff_stats.append((cat_name, len(cmds)))

            for cmd in cmds:
                code = cmd.get("code", "").strip()
                if not code:
                    issues.append("存在空代码指令")
                    continue

                # 检查双语名称
                name = cmd.get("name", {})
                if isinstance(name, dict):
                    if not name.get("zh-CN"):
                        issues.append(f"指令 '{code}' 缺少中文名称 (zh-CN)")
                    if not name.get("en"):
                        issues.append(f"指令 '{code}' 缺少英文名称 (en)")
                elif isinstance(name, str):
                    if not name:
                        issues.append(f"指令 '{code}' 名称为空")
                else:
                    issues.append(f"指令 '{code}' 名称格式不合规")

                # 检查中文说明
                desc = cmd.get("desc", "").strip()
                if not desc:
                    issues.append(f"指令 '{code}' 缺少中文说明")
                elif len(desc) < 5:
                    issues.append(f"指令 '{code}' 说明过短 ('{desc}')")

                # 运行引擎语法 Linter
                is_valid, linter_err = lint_command_syntax(gid, code)
                if not is_valid:
                    issues.append(f"语法 Linter 拦截: {linter_err}")

        # 2. 检查修改器
        trainer = g.get("trainerInfo", {})
        if not trainer.get("officialUrl") or "flingtrainer.com" not in trainer.get("officialUrl", ""):
            issues.append("缺少有效的 FLiNG 官方直连 URL")
        
        safe_ver = trainer.get("safeVerification", {})
        if not safe_ver.get("powershellExclusionCmd"):
            issues.append("缺少一键白名单 PowerShell 排除命令")

        hotkeys = trainer.get("hotkeysCategorized", [])
        if not hotkeys:
            issues.append("缺少分类热键矩阵")

        # 3. 检查精选 Mod
        mods = g.get("curatedMods", [])
        if not mods:
            issues.append("缺少 N网精选 Mod 推荐")
        for m in mods:
            if not m.get("installSteps") or len(m["installSteps"]) == 0:
                issues.append(f"Mod '{m.get('title')}' 缺少分步安装步骤")

        # 输出结果与 Diff 矩阵
        if issues:
            total_failed += 1
            print(f"\n⚠️ [FAIL] Rank {rank:2d}: {title} ({gid})")
            for iss in issues:
                print(f"    ❌ {iss}")
        else:
            total_passed += 1
            print(f"\n✅ [PASS] Rank {rank:2d}: {title} ({gid}) 检验合格！")
            print(f"    📊 分类统计 ({len(categories)} 大类, 共 {total_cmds} 条指令, {len(mods)} 个精选 Mods):")
            for cname, count in diff_stats:
                print(f"       • {cname}: {count} 条指令")

    print(f"\n--------------------------------------------------")
    print(f"质检汇总: {total_passed} 款游戏合格, {total_failed} 款待修正或扩充")
    print(f"--------------------------------------------------\n")
    return total_failed == 0

if __name__ == '__main__':
    gid = sys.argv[1] if len(sys.argv) > 1 else None
    success = audit_game(gid)
    sys.exit(0 if success else 1)
