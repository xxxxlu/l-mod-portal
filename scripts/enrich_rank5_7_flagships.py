#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/enrich_rank5_7_flagships.py
Console, command and curated-mod content for ranks 5-7
(Elden Ring, Skyrim Special Edition, Fallout 4).

Writes only the fields in OWNED_FIELDS of those three games, through gamedata_guard:
the master data must exist, radar and trainer fields are never written (trainer data
comes from fling_trainer_sync.py), and in public/data.js only the GAMES_DATA segment
changes (TRANSLATIONS_DATA is left alone).

Usage: python3 scripts/enrich_rank5_7_flagships.py [--dry-run]
"""

from gamedata_guard import write_owned_fields

# ==============================================================================
# RANK 5: 艾尔登法环 (Elden Ring)
# ==============================================================================
ELDEN_RING_DATA = {
    "hasConsole": False,
    "consoleShortcut": "无原生打字终端 (采用 ModEngine2 离线引导 + The Grand Archives CT 表 / FLiNG 修改器)",
    "consoleEnableGuide": {
        "zh-CN": "【离线启动指南（只在单机离线用）】\n1. 方案一 (ModEngine2 免修改文件)：解压 ModEngine2，将模组放入 /mod 目录，直接双击 launchmod_eldenring.bat 启动，这样启动不加载 EAC，只能离线玩；别带着改过的游戏或存档上线。\n2. 方案二 (替换引导)：进入游戏根目录 Game/，将原版 start_protected_game.exe 重命名为 .bak，将 eldenring.exe 复制一份并重命名为 start_protected_game.exe，新建文本文件 steam_appid.txt 写入 1245620，启动即可离线畅玩。\n3. 方案三 (无缝联机 Seamless Co-op)：该模组使用独立的 .co2 存档，走自己的联机方式、不连官方匹配服务器。它是第三方 Mod，会不会被封号没有人能担保。",
        "en": "EAC Offline Bypass & ModEngine2 Launch Guide: Launch via launchmod_eldenring.bat or rename start_protected_game.exe and place steam_appid.txt (1245620) to start without Easy Anti-Cheat (offline only). Never take a modded game or save online; nothing here can guarantee you won't be banned."
    },
    "popularCommands": [],
    "hasMods": True,
    "modInstallPath": "<SteamLibrary>/steamapps/common/ELDEN RING/Game/mod/",
    "curatedMods": [
        {
            "id": "mod_seamless_coop",
            "title": "Elden Ring Seamless Co-op",
            "author": "yuiamoroll",
            "category": "多人联机 (Multiplayer)",
            "desc": "联机模组，移除了击败 Boss 后被遣返回单人世界的限制，支持全图联机、死亡后围观队友复活、共乘灵马，使用独立的 .co2 存档，不连接官方匹配服务器（第三方 Mod，存在导致封号的风险）。",
            "dependencies": [
                "None (自带独立引导器)"
            ],
            "installPath": "<GameRoot>/Game/ersc/",
            "installSteps": [
                "解压 SeamlessCoop.zip 得到 ersc 文件夹与 launch_elden_ring_seamlesscoop.exe",
                "将上述文件复制进游戏目录 Game/ 下",
                "用记事本打开 Game/ersc/ersc_settings.ini，在 cooppassword = 后面输入你和队友约定的联机密码",
                "双击 launch_elden_ring_seamlesscoop.exe 启动游戏，进入游戏后使用道具栏中的【小人偶】进行联机"
            ],
            "isDirect": True,
            "nexusUrl": "https://github.com/yuiamoroll/EldenRingSeamlessCoopRelease",
            "version": "v2.0.3",
            "downloadUrl": "https://github.com/yuiamoroll/EldenRingSeamlessCoopRelease/releases/download/v2.0.3/_ersc_release_2_0_3.zip",
            "downloadFilename": "_ersc_release_2_0_3.zip"
        },
        {
            "id": "mod_modengine2",
            "title": "ModEngine2",
            "author": "soulsmods",
            "category": "框架 / 前置 (Core Framework)",
            "desc": "用于加载各类 Mod 资源（如 .dcx、.param、regulation.bin 等）而无需解包游戏文件，自带不加载 EAC 的离线启动方式，不修改游戏原始文件。",
            "dependencies": [
                "Microsoft Visual C++ 2015-2022 Redistributable"
            ],
            "installPath": "<GameRoot>/ModEngine2/",
            "installSteps": [
                "解压 ModEngine2 压缩包到任意纯英文路径 (推荐放到游戏根目录下)",
                "将下载的武器、服装或平衡性 Mod 解压后扔进 ModEngine2/mod/ 文件夹中",
                "双击运行 launchmod_eldenring.bat 启动游戏（不加载 EAC，只能离线玩）。"
            ],
            "isDirect": True,
            "nexusUrl": "https://github.com/soulsmods/ModEngine2",
            "version": "release-2.1.0",
            "downloadUrl": "https://github.com/soulsmods/ModEngine2/releases/download/release-2.1.0/ModEngine-2.1.0.0-win64.zip",
            "downloadFilename": "ModEngine-2.1.0.0-win64.zip"
        },
        {
            "id": "mod_grand_archives_ct",
            "title": "Elden Ring CT (The Grand Archives / TGA)",
            "author": "The Grand Archives",
            "category": "调试工具 (Debug / Cheat Tool)",
            "desc": "用于调试与资源查看的 Cheat Engine 表，可生成包含 DLC 在内的全部物品 (Item Gib)、点亮全部赐福传送点、开启自由视角飞行摄像机、复活 NPC，以及重置 Boss 挑战状态。",
            "dependencies": [
                "Cheat Engine 7.5+",
                "EAC Offline Bypass"
            ],
            "installPath": "自定义目录 (配合 Cheat Engine 使用)",
            "installSteps": [
                "下载并安装 Cheat Engine 7.5+",
                "先运行 launchmod_eldenring.bat 进入游戏并载入存档",
                "双击打开 EldenRing.CT 表，点击左上角电脑图标附着到 eldenring.exe 进程",
                "勾选 Open 表头，展开 Scripts -> Item Gib 即可按列表生成对应装备"
            ],
            "isDirect": False,
            "nexusUrl": "https://github.com/The-Grand-Archives/Elden-Ring-CT-TGA"
        },
        {
            "id": "mod_err_reforged",
            "title": "ERR - ELDEN RING Reforged",
            "author": "Kirnifr and the Reforged team",
            "category": "玩法机制调整 (Gameplay Overhaul)",
            "desc": "重新设计交界地的战斗机制：加入类似《只狼》的招架弹反系统、新的法术连段、复仇者难度模式，以及赐福点 Boss 连战挑战。",
            "dependencies": [
                "ModEngine2"
            ],
            "installPath": "<ModEngine2Root>/mod/",
            "installSteps": [
                "下载 ERR 安装包，将其解压覆盖至 ModEngine2/mod/ 目录下",
                "启动 launchmod_eldenring.bat 进入游戏"
            ],
            "isDirect": False,
            "nexusUrl": "https://www.nexusmods.com/eldenring/mods/541",
            "version": "2.3.9.1",
            "downloads": "1.3M",
            "endorsements": "16.7K",
            "checkedAt": "2026-11-20"
        }
    ],
    "consoleCategories": []
}

# ==============================================================================
# RANK 6: 上古卷轴5：天际重制版 (Skyrim Special Edition)
# ==============================================================================
SKYRIM_SE_DATA = {
    "hasConsole": True,
    "consoleShortcut": "~ (Tilde 键)",
    "consoleEnableGuide": {
        "zh-CN": "Bethesda Creation 引擎原生提供全功能控制台：\n1. 快捷键：游戏中随时按下键盘左上角【~】键 (波浪键 / ESC下方) 暂停并呼出全屏控制台；\n2. 输入法避坑：若无反应，请在 Windows 任务栏切换为'英语(美国)'美式键盘输入法，或在 Documents/My Games/Skyrim Special Edition/Skyrim.ini 的 [General] 下确认 bAllowConsole=1；\n3. 成就与防闪退：使用控制台或打 Mod 会打上脏标记锁定 Steam 成就，强烈建议安装 SSE Engine Fixes 恢复成就，它还修了一批引擎问题，但不能保证不闪退。\n4. 简写技巧：FormID 开头的多余 0 可省略，如 player.additem 0000000F 10000 可简写为 player.additem f 10000！",
        "en": "Bethesda Creation Engine Native Console: Press ~ (Tilde) key in-game to toggle. Supports Hex FormIDs, batch (.bat) scripts, quest stage jumping, and free camera."
    },
    "popularCommands": [
        "tgm",
        "player.additem 0000000F 100000",
        "player.setav carryweight 99999",
        "tcl",
        "tmm 1",
        "coc qasmoke",
        "unlock"
    ],
    "hasMods": True,
    "modInstallPath": "<SteamLibrary>/steamapps/common/Skyrim Special Edition/Data/",
    "curatedMods": [
        {
            "id": "mod_skse64",
            "title": "Skyrim Script Extender (SKSE64)",
            "author": "Ian Patterson and Stephen Abel (ianpatt, behippo)",
            "category": "框架 / 前置",
            "desc": "扩展 Papyrus 脚本引擎功能的工具，是许多高级 UI 与功能类 Mod 的前置。",
            "dependencies": [
                "None (独立启动器)"
            ],
            "installPath": "<GameRoot>/",
            "installSteps": [
                "下载与当前游戏版本匹配的 SKSE64 压缩包",
                "将压缩包内的 skse64_loader.exe 与 .dll 文件复制到游戏根目录（与 SkyrimSE.exe 同级）",
                "将 Data/ 文件夹合并进游戏的 Data/ 目录",
                "之后启动游戏请运行 skse64_loader.exe"
            ],
            "isDirect": True,
            "nexusUrl": "https://github.com/ianpatt/skse64",
            "version": "v2.2.6",
            "downloads": "14.8M",
            "endorsements": "128.5K",
            "checkedAt": "2026-11-20",
            "downloadUrl": "https://github.com/ianpatt/skse64/releases/download/v2.2.6/skse64_2_02_06.7z",
            "downloadFilename": "skse64_2_02_06.7z"
        },
        {
            "id": "mod_sse_engine_fixes",
            "title": "SSE Engine Fixes (skse64 plugin)",
            "author": "aers - Nukem - Ryan",
            "category": "引擎修复",
            "desc": "SKSE64 插件，用于修复引擎相关问题，包括高帧率下的物理异常、口型不同步、部分内存泄漏与崩溃问题；可选配置在使用 Mod 时仍启用 Steam 成就。",
            "dependencies": [
                "SKSE64",
                "Address Library for SKSE Plugins"
            ],
            "installPath": "<GameRoot>/Data/SKSE/Plugins/",
            "installSteps": [
                "安装 Part 1 到 MO2 或 Vortex 模组管理器中并启用",
                "将 Part 2 解压后的 d3dx9_42.dll 与 tbb.dll 手动放入游戏根目录 (与 SkyrimSE.exe 同级)",
                "配置 EngineFixes.toml 开启 EnableAchievementsWithMods = true"
            ],
            "isDirect": False,
            "nexusUrl": "https://www.nexusmods.com/skyrimspecialedition/mods/17230",
            "version": "7.0.20",
            "downloads": "30.4M",
            "endorsements": "189.4K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "mod_skyui",
            "title": "SkyUI",
            "author": "SkyUI Team",
            "category": "界面",
            "desc": "为 PC 玩家优化界面的 Mod，提供物品列表排序/搜索、分类收藏夹，以及 MCM（Mod 配置菜单）等功能。",
            "dependencies": [
                "SKSE64"
            ],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "需先安装 SKSE64",
                "通过 MO2 或 Vortex 安装 SkyUI 压缩包并启用",
                "用 skse64_loader.exe 启动游戏后，按 ESC 可看到 Mod Configuration 菜单"
            ],
            "isDirect": False,
            "nexusUrl": "https://www.nexusmods.com/skyrimspecialedition/mods/12604",
            "version": "6.9",
            "downloads": "26.6M",
            "endorsements": "509.2K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "mod_ussep",
            "title": "Unofficial Skyrim Special Edition Patch - USSEP",
            "author": "The Unofficial Patch Project Team",
            "category": "漏洞修复",
            "desc": "综合性的漏洞修复补丁，目标是修复官方未解决的大量任务、网格、材质与文本等问题。",
            "dependencies": [
                "Skyrim Special Edition 官方三大DLC"
            ],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "通过模组管理器安装 USSEP",
                "在插件加载顺序中将该补丁放在官方 DLC 之后、其余 Mod 之前"
            ],
            "isDirect": False,
            "nexusUrl": "https://www.nexusmods.com/skyrimspecialedition/mods/266",
            "version": "4.3.9c",
            "downloads": "28.6M",
            "endorsements": "482.1K",
            "checkedAt": "2026-11-20"
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 角色状态与上帝模式 (God Mode & Invulnerability)",
            "commands": [
                {
                    "id": "skyrim_tgm",
                    "name": {
                        "zh-CN": "开关上帝模式 (tgm)",
                        "en": "Toggle God Mode (tgm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "开启后角色免疫伤害，耐力与魔法不再消耗，负重不受限制；再次输入可关闭。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_tim",
                    "name": {
                        "zh-CN": "不死模式",
                        "en": "Immortal Mode (tim)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tim",
                    "desc": "生命值/魔法/耐力正常扣减；生命值可被降到0，但不会因此死亡，其他伤害判定照常",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_tcl",
                    "name": {
                        "zh-CN": "开关穿墙穿模模式 (Toggle Collision)",
                        "en": "Toggle Collision (tcl)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tcl",
                    "desc": "关闭物理碰撞检测，角色可以在空中自由移动并穿过墙体，可用于脱离被卡住的地形。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_carryweight",
                    "name": {
                        "zh-CN": "将背包负重上限设为 99,999",
                        "en": "Set Carry Weight Upper Limit"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 99999",
                    "desc": "将角色负重上限直接设置为 99,999 磅，基本不会再因超重而减速。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim_Mod:Actor_Value_Indices"
                },
                {
                    "id": "skyrim_speedmult",
                    "name": {
                        "zh-CN": "修改角色奔跑移速为 1.5 倍 (默认 100)",
                        "en": "Set Movement Speed Multiplier"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav speedmult 150",
                    "desc": "将移动速度基础值设为 150%（默认 100），收起或拔出武器一次后生效，可加快跑图速度。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim_Mod:Actor_Value_Indices"
                }
            ]
        },
        {
            "category": "💰 货币、开锁与技能熟练度提升 (Gold, Lockpicks & Skill Training)",
            "commands": [
                {
                    "id": "skyrim_add_gold_100k",
                    "name": {
                        "zh-CN": "增加 100,000 金币 (FormID: 0000000F / f)",
                        "en": "Add 100,000 Gold"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 100000",
                    "desc": "向背包增加 10 万金币。可简写为 player.additem f 100000。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Gold"
                },
                {
                    "id": "skyrim_add_lockpicks",
                    "name": {
                        "zh-CN": "增加 1,000 个开锁器 (FormID: 0000000A / a)",
                        "en": "Add 1,000 Lockpicks"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000A 1000",
                    "desc": "向背包增加 1,000 个开锁器。可简写为 player.additem a 1000。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Lockpick"
                },
                {
                    "id": "skyrim_add_dragon_souls",
                    "name": {
                        "zh-CN": "获取 100 个龙魂",
                        "en": "Add 100 Dragon Souls"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav dragonsouls 100",
                    "desc": "向角色增加 100 个龙魂，可用于解锁已习得词语的龙吼技能。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim_Mod:Actor_Value_Indices"
                },
                {
                    "id": "skyrim_advskill_smithing",
                    "name": {
                        "zh-CN": "锻造技能等级提升至 100",
                        "en": "Advance Smithing Skill to 100"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.advskill smithing 999999",
                    "desc": "为锻造技能注入大量经验，使其升至满级 100（对应 Perk 仍需自行点出）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_advskill_enchanting",
                    "name": {
                        "zh-CN": "附魔技能等级提升至 100",
                        "en": "Advance Enchanting Skill to 100"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.advskill enchanting 999999",
                    "desc": "为附魔技能注入大量经验，使其升至满级 100（对应 Perk 仍需自行点出）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_advskill_alchemy",
                    "name": {
                        "zh-CN": "炼金技能等级提升至 100",
                        "en": "Advance Alchemy Skill to 100"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.advskill alchemy 999999",
                    "desc": "为炼金技能注入大量经验，使其升至满级 100。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                }
            ]
        },
        {
            "category": "🐉 龙吼学习与冷却时间调整 (Dragon Shouts & Cooldown)",
            "commands": [
                {
                    "id": "skyrim_shout_unrelenting_force",
                    "name": {
                        "zh-CN": "习得不卸之力龙吼第一段 (Fus)",
                        "en": "Teach Unrelenting Force, word 1 (Fus)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.teachword 13e22",
                    "desc": "习得龙吼【不卸之力】第一段（Fus），可击退敌人；第二段词条ID为13e23，第三段为13e24。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Unrelenting_Force"
                },
                {
                    "id": "skyrim_shout_whirlwind_sprint",
                    "name": {
                        "zh-CN": "旋风冲刺（第一段）",
                        "en": "Whirlwind Sprint (word 1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.teachword 2f7bb",
                    "desc": "习得旋风冲刺龙吼第一段（Wuld）；第二段 Wuld Nah 的词条ID为 02f7bc，第三段 Wuld Nah Kest 为 02f7bd",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Whirlwind_Sprint"
                },
                {
                    "id": "skyrim_shout_dragonrend",
                    "name": {
                        "zh-CN": "降龙之吼（第一段）",
                        "en": "Dragonrend (word 1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.teachword 44251",
                    "desc": "习得降龙之吼第一段（Joor）",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Dragonrend"
                },
                {
                    "id": "skyrim_zero_shout_recovery",
                    "name": {
                        "zh-CN": "龙吼冷却时间归零 (可连续释放龙吼)",
                        "en": "Set Shout Recovery Cooldown to Zero"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav shoutrecoverymult 0",
                    "desc": "将龙吼冷却恢复倍率设为 0，使龙吼可以连续释放，无需等待冷却。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim_Mod:Actor_Value_Indices"
                }
            ]
        },
        {
            "category": "⚡ 魔神器与传奇武器 (Daedric Artifacts & Legendary Weapons)",
            "commands": [
                {
                    "id": "skyrim_spawn_dawnbreaker",
                    "name": {
                        "zh-CN": "派发魔神器：破晓者 (美瑞蒂亚单手剑/亡灵克星金光爆炸)",
                        "en": "Spawn Dawnbreaker (0002ac61)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0004e4ee 1",
                    "desc": "美瑞蒂亚的魔神器单手剑，攻击附加 10 点火焰伤害；击杀亡灵时有几率引发火焰爆炸，使周围亡灵着火并可能被烧毁。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Dawnbreaker"
                },
                {
                    "id": "skyrim_spawn_mace_of_molag_bal",
                    "name": {
                        "zh-CN": "派发魔神器：莫拉格·巴尔钉头锤 (灵魂陷阱与体力吸取)",
                        "en": "Spawn Mace of Molag Bal (000233e3)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000233e3 1",
                    "desc": "莫拉格·巴尔的魔神器钉头锤，每次命中造成 25 点耐力和 25 点魔法伤害，并施加 3 秒灵魂陷阱效果。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Mace_of_Molag_Bal"
                },
                {
                    "id": "skyrim_spawn_mehrunes_razor",
                    "name": {
                        "zh-CN": "派发魔神器：梅鲁涅斯的剃刀 (小概率直接击杀目标)",
                        "en": "Spawn Mehrunes' Razor (000240d2)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000240d2 1",
                    "desc": "破坏魔神的匕首，每次命中有 1.98% 的几率直接击杀目标。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Mehrunes_Razor"
                },
                {
                    "id": "skyrim_spawn_azuras_star",
                    "name": {
                        "zh-CN": "派发魔神器：阿祖拉之星 (可重复使用的灵魂石)",
                        "en": "Spawn Azura's Star (00063b27)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00063b27 1",
                    "desc": "可重复使用的大型灵魂石，为武器或装备充能时只消耗其中储存的灵魂，星体本身不会被消耗。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Azura%27s_Star"
                },
                {
                    "id": "skyrim_spawn_spellbreaker",
                    "name": {
                        "zh-CN": "派发魔神器：破法者 (举盾生成 50 点魔法结界)",
                        "en": "Spawn Spellbreaker (0004585a)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00045f96 1",
                    "desc": "瘟疫魔神的重盾，格挡时生成可抵御最多 50 点法术伤害的护盾。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Spellbreaker"
                },
                {
                    "id": "skyrim_spawn_wabbajack",
                    "name": {
                        "zh-CN": "派发魔神器：瓦巴杰克 (疯神法杖搞怪随机形变)",
                        "en": "Spawn Wabbajack (000139b9)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0002ac6f 1",
                    "desc": "谢尔格拉的魔神法杖，攻击会触发随机效果：可能造成元素伤害、治疗目标、使目标隐形，或把目标变成鸡、兔子、泥沼蟹等动物，偶尔会直接杀死目标。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Wabbajack"
                }
            ]
        },
        {
            "category": "🛠️ 锻造装备与材料 (Daedric/Dragon Armor & Materials)",
            "commands": [
                {
                    "id": "skyrim_spawn_daedric_sword",
                    "name": {
                        "zh-CN": "派发魔族巨剑 (Daedric Greatsword: 0001396b)",
                        "en": "Spawn Daedric Greatsword"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000139b9 1",
                    "desc": "派发魔族巨剑，基础伤害在天际双手武器中较高。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Daedric_Smithing"
                },
                {
                    "id": "skyrim_spawn_daedric_armor",
                    "name": {
                        "zh-CN": "派发魔族重甲胸甲 (Daedric Armor: 00013969)",
                        "en": "Spawn Daedric Armor Heavy"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0001396b 1",
                    "desc": "派发魔族重甲的胸甲部件，护甲值在天际重甲中处于较高水平。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Daedric_Smithing"
                },
                {
                    "id": "skyrim_spawn_daedric_hearts",
                    "name": {
                        "zh-CN": "派发 100 颗魔族之心 (稀缺锻造素材: 0003ad5b)",
                        "en": "Spawn 100 Daedric Hearts"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0003ad5b 100",
                    "desc": "一次性获得 100 颗魔族之心，是锻造魔族护甲与武器所需的材料。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Daedra_Heart"
                },
                {
                    "id": "skyrim_spawn_dragon_scales",
                    "name": {
                        "zh-CN": "派发 100 个龙鳞 (龙骨防具核心素材: 0003ad57)",
                        "en": "Spawn 100 Dragon Scales"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0003ada3 100",
                    "desc": "一次性获得 100 个龙鳞，是锻造龙鳞轻甲等龙骨装备所需的材料。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Dragon_Scales"
                },
                {
                    "id": "skyrim_spawn_ebony_ingots",
                    "name": {
                        "zh-CN": "派发 100 个乌木锭 (重装强化金属: 0003ad5e)",
                        "en": "Spawn 100 Ebony Ingots"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0005ad9d 100",
                    "desc": "一次性获得 100 个乌木锭，可用于在工作台强化装备（含强化至「传奇」等级）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Ebony_Ingot"
                }
            ]
        },
        {
            "category": "🚨 任务卡关修复与进度推进 (Quest Bug Fixes & SetStage)",
            "commands": [
                {
                    "id": "skyrim_fix_greybeards_mq105",
                    "name": {
                        "zh-CN": "修复高吼峰灰胡子召唤卡关 (setstage MQ105 10)",
                        "en": "Fix Greybeards Call Quest (MQ105)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage MQ105 10",
                    "desc": "若击败第一条飞龙后灰胡子的召唤吼声未能触发，可用此指令强制推进任务阶段。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:The_Way_of_the_Voice"
                },
                {
                    "id": "skyrim_fix_alduins_wall_mq203",
                    "name": {
                        "zh-CN": "修复【奥杜因之墙】NPC卡关 (setstage MQ203 280)",
                        "en": "Fix Alduin's Wall Quest Bug (MQ203)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage MQ203 280",
                    "desc": "若伊思本或戴尔芬卡在该步骤不触发后续对话，可用此指令强制将任务推进到下一阶段。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Alduin%27s_Wall"
                },
                {
                    "id": "skyrim_fix_vaermina_da16",
                    "name": {
                        "zh-CN": "修复【苏醒之梦】卡关 (setstage DA16 200)",
                        "en": "Fix Waking Nightmare Quest Bug (DA16)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage DA16 200",
                    "desc": "若喝下药水后无法进入梦境回忆而卡关，可用此指令将任务跳到净化完成阶段。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Waking_Nightmare"
                },
                {
                    "id": "skyrim_sqt_query",
                    "name": {
                        "zh-CN": "查询当前所有活动任务的目标代码 (Show Quest Targets)",
                        "en": "Show Active Quest Targets (sqt)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "sqt",
                    "desc": "在控制台输出当前激活任务的 Quest ID 与目标内部代号，用于排查任务卡关。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_companion_moveto",
                    "name": {
                        "zh-CN": "强制将卡在地形或失踪的随从传送至身旁",
                        "en": "Teleport Missing Follower to Player"
                    },
                    "syntax_type": "creation_hex",
                    "code": "prid 000a2c94\nmoveto player",
                    "desc": "可将卡在地形中或走丢的随从（例如莱迪亚 Lydia，ID 000A2C94）传送到玩家面前。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                }
            ]
        },
        {
            "category": "🏡 炉火 DLC 建材补给与清除悬赏 (Hearthfire & Crime Clearing)",
            "commands": [
                {
                    "id": "skyrim_hearthfire_quarried_stone",
                    "name": {
                        "zh-CN": "派发 500 个采掘石料 (炉火豪宅地基核心: 0300306c)",
                        "en": "Spawn 500 Quarried Stones"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0300306c 500",
                    "desc": "炉火 DLC 建造房屋所需的建材之一，省去在采石坑手动挖掘的步骤。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Quarried_Stone"
                },
                {
                    "id": "skyrim_hearthfire_clay",
                    "name": {
                        "zh-CN": "派发 500 块粘土 (墙壁与烤箱素材: 03003043)",
                        "en": "Spawn 500 Clays"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 03003043 500",
                    "desc": "一次性获得 500 块粘土，是建造炉火房屋部分房间所需的材料之一。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Clay"
                },
                {
                    "id": "skyrim_hearthfire_iron_ingots",
                    "name": {
                        "zh-CN": "派发 300 块铁锭 (用于打造成千枚铁钉与合页)",
                        "en": "Spawn 300 Iron Ingots for Nails"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0005ace4 300",
                    "desc": "一次性获得 300 块铁锭，可在铁砧上加工成铁钉等建材。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Iron_Ingot"
                },
                {
                    "id": "skyrim_clear_bounty",
                    "name": {
                        "zh-CN": "清空当前要塞所有通缉悬赏罪名",
                        "en": "Clear All Crime Bounty"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setcrimegold 0",
                    "desc": "将当前悬赏金清零，卫兵会停止敌对状态，无需入狱或缴纳罚款。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                }
            ]
        },
        {
            "category": "🌌 开发者房间、全地图标与全法术解锁 (Dev Room, Map & All Spells)",
            "commands": [
                {
                    "id": "skyrim_coc_qasmoke",
                    "name": {
                        "zh-CN": "传送至开发者测试房间烟雾房 (coc qasmoke: 包含全天际所有物品箱)",
                        "en": "Teleport to Dev Smoke Room (coc qasmoke)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "coc qasmoke",
                    "desc": "Bethesda 官方的测试房间，摆放着按分类整理的全部物品宝箱，可直接拿取。输入 coc riverwood 可传送回溪木镇。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_tmm_1",
                    "name": {
                        "zh-CN": "点亮大地图所有地标 (Toggle Map Markers: 包含未探明区域)",
                        "en": "Unlock All Map Markers (tmm 1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tmm 1",
                    "desc": "点亮地图上约 400 个地下城、山峰、营地与城市地标，并可直接快速旅行至这些地点。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_psb_all_spells",
                    "name": {
                        "zh-CN": "解锁全天际所有魔法与法术 (Player Spell Book)",
                        "en": "Unlock All Spells (psb)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "psb",
                    "desc": "将游戏中所有法术（包括未在游戏中实际使用的测试法术）加入角色的法术书。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_tfc_freecam",
                    "name": {
                        "zh-CN": "开启自由飞行摄影摄像机并暂停时间 (tfc 1)",
                        "en": "Toggle Free Camera (tfc 1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tfc 1",
                    "desc": "开启自由摄像机并暂停游戏画面，可脱离角色视角在场景中自由移动和缩放，便于截图。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_tm_hide_hud",
                    "name": {
                        "zh-CN": "隐藏/恢复全部界面 HUD 与准星 (无UI纯净截图)",
                        "en": "Toggle Menus / Hide HUD (tm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tm",
                    "desc": "隐藏或恢复血条、罗盘、准星等界面元素（隐藏后仍可打开控制台重新输入 tm 恢复）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                }
            ]
        }
    ]
}

# ==============================================================================
# RANK 7: 辐射4：次世代更新版 (Fallout 4 Next-Gen)
# ==============================================================================
FALLOUT_4_DATA = {
    "hasConsole": True,
    "consoleShortcut": "~ (Tilde 键)",
    "consoleEnableGuide": {
        "zh-CN": "【次世代大更新避坑与控制台开启】\n1. 控制台呼出：游戏中按下【~】(波浪键) 暂停并呼出控制台；\n2. 2024 次世代大更新 (v1.10.980/984) 避坑必看：\n   - 路径一 (次世代原生模式)：若玩次世代新版，必须安装对应次世代分支的 F4SE (v0.7.2+) 与 Address Library Next-Gen，并在 Steam 游戏属性中设置【仅在我启动该游戏时更新】减少后台自动更新（不能保证不被更新）；\n   - 路径二 (经典降级模式)：若想享受数万款旧 Mod，使用【Fallout 4 Downgrader】一键将主程序回退至 1.10.163 黄金稳定版；\n3. 极速批处理 (bat 命令)：在游戏根目录新建文本文件 (如 all_materials.txt)，游戏中只需在控制台输入 bat all_materials，瞬间一次性执行上百条指令！",
        "en": "Fallout 4 Creation Engine Console: Press ~ (Tilde) to toggle. Next-Gen Update (v1.10.980+) compatible with F4SE v0.7.2+ or use Downgrader to v1.10.163. Supports bat batch scripts and dynamic legendary attachmod enchantments."
    },
    "popularCommands": [
        "tgm",
        "player.additem 0000000F 100000",
        "player.setav carryweight 99999",
        "setav 349 9999999",
        "attachmod 001cc2ac",
        "attachmod 001e7c20",
        "tcl",
        "coc RedRocketExt"
    ],
    "hasMods": True,
    "modInstallPath": "<SteamLibrary>/steamapps/common/Fallout 4/Data/",
    "curatedMods": [
        {
            "id": "mod_f4se",
            "title": "Fallout 4 Script Extender (F4SE)",
            "author": "F4SE Team",
            "category": "框架 / 前置",
            "desc": "扩展 Fallout 4 脚本功能的工具，是 Place Everywhere、MCM 等许多 Mod 的前置；次世代更新后需要 0.7.2+ 版本的 loader。",
            "dependencies": [
                "None (独立启动器)"
            ],
            "installPath": "<GameRoot>/",
            "installSteps": [
                "下载与当前游戏版本对应的 F4SE 压缩包（次世代版 0.7.2+，旧版/降级版 0.6.23）",
                "将 f4se_loader.exe 与相关 .dll 复制到 Fallout 4 游戏根目录",
                "将 Data/ 文件夹合并进游戏 Data 目录",
                "之后启动游戏请运行 f4se_loader.exe"
            ],
            "isDirect": True,
            "nexusUrl": "https://www.nexusmods.com/fallout4/mods/42147",
            "version": "0.7.9",
            "downloads": "8.7M",
            "endorsements": "102.8K",
            "checkedAt": "2026-11-20",
            "downloadUrl": "https://github.com/ianpatt/f4se/releases/download/v0.6.23/f4se_0_06_23.7z",
            "downloadFilename": "f4se_0_06_23.7z"
        },
        {
            "id": "mod_buffout_4",
            "title": "Buffout 4",
            "author": "Ryan",
            "category": "引擎修复",
            "desc": "修复部分引擎 Bug，并在游戏崩溃时生成 Crash Log，辅助排查是哪个 Mod 或资源导致的问题（日志分析仍需人工判断，不保证完全准确）。",
            "dependencies": [
                "F4SE",
                "xSE Plugin Preloader",
                "Address Library for F4SE Plugins"
            ],
            "installPath": "<GameRoot>/Data/F4SE/Plugins/",
            "installSteps": [
                "使用 MO2 或 Vortex 安装 Buffout 4 及其前置 xSE Plugin Preloader",
                "若发生崩溃，可在 Documents/My Games/Fallout4/F4SE/ 查看 crash-*.log 排查原因"
            ],
            "isDirect": False,
            "nexusUrl": "https://www.nexusmods.com/fallout4/mods/47359",
            "version": "1.28.6",
            "downloads": "3.4M",
            "endorsements": "40.2K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "mod_place_everywhere",
            "title": "Place Everywhere",
            "author": "TheLich",
            "category": "玩法 / 建造",
            "desc": "工房建造 Mod，解除红圈禁止摆放的限制，支持物体穿插、三轴精确旋转（X/Y/Z）与缩放。",
            "dependencies": [
                "F4SE"
            ],
            "installPath": "<GameRoot>/Data/F4SE/Plugins/",
            "installSteps": [
                "确保已安装 F4SE",
                "通过模组管理器安装 Place Everywhere",
                "进入建造模式后，按 F1 切换碰撞检测，按 F2 切换贴合吸附"
            ],
            "isDirect": False,
            "nexusUrl": "https://www.nexusmods.com/fallout4/mods/9424",
            "version": "1.22.1.1240",
            "downloads": "7.2M",
            "endorsements": "120.4K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "mod_sim_settlements_2",
            "title": "Sim Settlements 2",
            "author": "Sim Settlements Team",
            "category": "玩法 / 聚落",
            "desc": "聚落建造系统重做的 Mod，为 Fallout 4 增加城市模拟玩法，包含主线剧情与多名有配音的 NPC。",
            "dependencies": [
                "Workshop Framework",
                "HUDFramework"
            ],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "安装前置 Workshop Framework",
                "安装 Sim Settlements 2 及其剧情扩展章节包",
                "在游戏内建造并拾取【ASAM 传感器】以开始第一块规划区"
            ],
            "isDirect": False,
            "nexusUrl": "https://www.nexusmods.com/fallout4/mods/47976",
            "version": "3.8.1a",
            "downloads": "4.4M",
            "endorsements": "37.4K",
            "checkedAt": "2026-11-20"
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 角色状态与废土生存 (God Mode & Wasteland Survival)",
            "commands": [
                {
                    "id": "fo4_tgm",
                    "name": {
                        "zh-CN": "开关上帝模式 (tgm)",
                        "en": "Toggle God Mode (tgm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "开启后角色免疫伤害、辐射伤害与水下缺氧伤害，弹药、负重与行动点不受限制，且无需换弹；再次输入关闭。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_tim",
                    "name": {
                        "zh-CN": "开关不死锁血模式 (tim)",
                        "en": "Toggle Immortal Mode (tim)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tim",
                    "desc": "角色仍会正常受到伤害显示效果，但生命值不会降到 0 而死亡；不会获得辐射免疫、无限行动点或弹药。注意：遇到处决类死亡动画时可能导致角色异常，请谨慎使用存档。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_tcl",
                    "name": {
                        "zh-CN": "开关穿墙飞行模式 (Toggle Collision: 悬浮飞行穿墙)",
                        "en": "Toggle Collision (tcl)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tcl",
                    "desc": "关闭物理碰撞，角色可以穿过地形与建筑自由移动，可用于脱离卡住的地形。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_rads_zero",
                    "name": {
                        "zh-CN": "角色辐射污染清零 (消除红色上限减血条)",
                        "en": "Clear Radiation Pollution"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav rads 0",
                    "desc": "将角色当前的辐射值清零，恢复因辐射占用而减少的生命上限。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_carryweight",
                    "name": {
                        "zh-CN": "永久扩增随身背包负重上限至 99,999 (捡垃圾核心)",
                        "en": "Set Carry Weight Limit"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 99999",
                    "desc": "将角色负重上限设置为 99,999，基本不会再因负重超限而减速。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                }
            ]
        },
        {
            "category": "💰 货币、发夹与聚变核心能源 (Caps, Bobby Pins & Fusion Cores)",
            "commands": [
                {
                    "id": "fo4_add_caps_100k",
                    "name": {
                        "zh-CN": "增加 100,000 瓶盖货币 (FormID: 0000000F / f)",
                        "en": "Add 100,000 Bottle Caps"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 100000",
                    "desc": "向背包增加 10 万瓶盖。可简写为 player.additem f 100000。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_add_bobby_pins",
                    "name": {
                        "zh-CN": "增加 1,000 根发夹开锁器 (FormID: 0000000A / a)",
                        "en": "Add 1,000 Bobby Pins"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000A 1000",
                    "desc": "向背包增加 1,000 根发夹，用于撬锁。可简写为 player.additem a 1000。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Bobby_pin_(Fallout_4)"
                },
                {
                    "id": "fo4_add_fusion_cores",
                    "name": {
                        "zh-CN": "派发 100 颗核聚变核心 (动力装甲电池: 00075fe4)",
                        "en": "Add 100 Fusion Cores"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00075fe4 100",
                    "desc": "向背包增加 100 颗满电的核聚变核心，用于给动力装甲供电。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_add_stimpaks",
                    "name": {
                        "zh-CN": "派发 200 支治疗针 (Stimpak: 00023736)",
                        "en": "Add 200 Stimpaks"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00023736 200",
                    "desc": "向背包增加 200 支治疗针。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Stimpak_(Fallout_4)"
                },
                {
                    "id": "fo4_add_radaway",
                    "name": {
                        "zh-CN": "派发 100 支消辐宁 (RadAway: 00023742)",
                        "en": "Add 100 RadAway"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00023742 100",
                    "desc": "派发 100 支消辐宁药剂，净化废土辐射带来的体内污染。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/RadAway_(Fallout_4)"
                }
            ]
        },
        {
            "category": "🏗️ 聚落建造空间与建材补给 (Settlement Building & Materials)",
            "commands": [
                {
                    "id": "fo4_settlement_size_bypass",
                    "name": {
                        "zh-CN": "解除聚落建造空间容量上限 (setav 349 9999999)",
                        "en": "Bypass Settlement Building Size Budget"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setav 349 9999999",
                    "desc": "在工房模式下对着工房控制台使用本指令，可将建造空间预算上限提高到极大值，使建造容量条基本不会用满。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_settlement_triangles_bypass",
                    "name": {
                        "zh-CN": "解除聚落绘制调用(Draw Call)预算上限",
                        "en": "Remove settlement draw-call budget cap"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setav 34B 9999999",
                    "desc": "AV 348 是聚落当前已使用的三角面计数，不是上限，设成极大值不会解除建造限制；三角面上限已由另一条命令(AV 349)覆盖，这里应改用 AV 34B 设置绘制调用预算上限，才能进一步解除建造数量限制",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_scrapall",
                    "name": {
                        "zh-CN": "拆解回收当前已加载区域的废墟",
                        "en": "Scrap eligible junk in the currently loaded area"
                    },
                    "syntax_type": "creation_hex",
                    "code": "scrapall",
                    "desc": "进出工房模式后输入，拆解回收当前已加载区域(非整个地图)内可拆解的废墟；官方Wiki提示该命令可能误删范围外物品，需谨慎使用",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_add_steel_1000",
                    "name": {
                        "zh-CN": "派发 1,000 块钢铁 (基础建材: 000731a4)",
                        "en": "Spawn 1,000 Steel"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000731a4 1000",
                    "desc": "向背包增加 1,000 块钢铁，是建造所需的基础材料之一。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_add_wood_1000",
                    "name": {
                        "zh-CN": "派发 1,000 捆木材 (木结构基础: 000731a3)",
                        "en": "Spawn 1,000 Wood"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000731a3 1000",
                    "desc": "向背包增加 1,000 捆木材，是建造所需的基础材料之一。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_add_copper_500",
                    "name": {
                        "zh-CN": "派发 500 块纯铜 (发电机与电网电缆: 0006907c)",
                        "en": "Spawn 500 Copper"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0006907c 500",
                    "desc": "向背包增加 500 块铜，铜是搭建发电机、电线塔等通电设施所需的材料。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                }
            ]
        },
        {
            "category": "🔫 传奇武器词条自定义附魔 (Legendary Weapon Modding & Attachmod)",
            "commands": [
                {
                    "id": "fo4_attachmod_two_shot",
                    "name": {
                        "zh-CN": "手持武器附魔【双弹】传奇词条 (多发射一发弹药)",
                        "en": "Attach Legendary Mod: Two Shot"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001cc2ad",
                    "desc": "为当前手持武器附加传奇词条【双弹】：每次射击额外多发射一发弹药，但后坐力增加 25%。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_explosive",
                    "name": {
                        "zh-CN": "手持武器附魔【爆破】传奇词条 (子弹命中后产生范围爆炸)",
                        "en": "Attach Legendary Mod: Explosive"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001e73bd",
                    "desc": "为武器附加传奇词条【爆破】：子弹命中后造成 15 点范围爆炸伤害。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_furious",
                    "name": {
                        "zh-CN": "手持武器附魔【狂怒】传奇词条 (近战连续命中递增伤害)",
                        "en": "Attach Legendary Mod: Furious"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001ef481",
                    "desc": "近战武器专属词条：连续命中同一目标时，每次伤害提高 15%。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_never_ending",
                    "name": {
                        "zh-CN": "手持武器附魔【无底洞】传奇词条 (弹匣容量等于携带弹药数)",
                        "en": "Attach Legendary Mod: Never Ending"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001cc2ac",
                    "desc": "将弹匣容量设置为与携带的备用弹药数量相同，可以减少换弹次数（镭射火枪、注射器枪、鱼叉枪与垃圾枪除外）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_kneecapper",
                    "name": {
                        "zh-CN": "手持武器附魔【膝盖收割者】传奇词条 (20%几率使双腿瘫痪)",
                        "en": "Attach Legendary Mod: Kneecapper"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001f1048",
                    "desc": "命中敌人有 20% 几率使其双腿瘫痪，大幅降低移动速度。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_instigating",
                    "name": {
                        "zh-CN": "手持武器附魔【煽动】传奇词条 (对满血目标造成双倍伤害: 001f31b9)",
                        "en": "Attach Legendary Mod: Instigating"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001f04b8",
                    "desc": "若目标生命值为满，本次攻击造成双倍伤害；适合用于遭遇战的第一击。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                }
            ]
        },
        {
            "category": "🤖 全套 X-01 动力装甲与毁灭军备 (X-01 Power Armor & Heavy Ordnance)",
            "commands": [
                {
                    "id": "fo4_spawn_x01_helm",
                    "name": {
                        "zh-CN": "派发 X-01 动力装甲头盔 (00154ac8)",
                        "en": "Spawn X-01 Power Armor Helmet"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac5 1",
                    "desc": "派发 X-01 动力装甲头盔，可在装甲工作台升级，加装红外线侦测等模组。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/X-01_power_armor_(Fallout_4)"
                },
                {
                    "id": "fo4_spawn_x01_torso",
                    "name": {
                        "zh-CN": "派发 X-01 动力装甲胸甲 (00154ac5)",
                        "en": "Spawn X-01 Power Armor Torso"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac8 1",
                    "desc": "派发 X-01 动力装甲躯干部件，可改装喷气背包（Jetpack）实现飞行。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/X-01_power_armor_(Fallout_4)"
                },
                {
                    "id": "fo4_spawn_x01_arms",
                    "name": {
                        "zh-CN": "派发 X-01 动力装甲左臂 (00154ac3) 与右臂 (00154ac4)",
                        "en": "Spawn X-01 Power Armor Arms"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac3 1",
                    "desc": "派发 X-01 左右臂部件，可改装特斯拉线圈等近战强化模组。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/X-01_power_armor_(Fallout_4)"
                },
                {
                    "id": "fo4_spawn_x01_legs",
                    "name": {
                        "zh-CN": "派发 X-01 动力装甲左腿 (00154ac6) 与右腿 (00154ac7)",
                        "en": "Spawn X-01 Power Armor Legs"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac6 1",
                    "desc": "派发 X-01 左右腿部装甲，改装校准减震器可额外增加 100 点负重上限。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/X-01_power_armor_(Fallout_4)"
                },
                {
                    "id": "fo4_spawn_fat_man",
                    "name": {
                        "zh-CN": "派发【胖子核弹发射器】(Fat Man: 001685c9) 与迷你核弹",
                        "en": "Spawn Fat Man Launcher & Mini Nuke"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000bd56f 1",
                    "desc": "派发胖子核弹发射器；可搭配 player.additem 000e6b2e 20 额外获得 20 枚迷你核弹。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fat_Man_(Fallout_4)"
                },
                {
                    "id": "fo4_spawn_gauss_rifle",
                    "name": {
                        "zh-CN": "派发高斯步枪 (Gauss Rifle: 00004240) 与 2mm 电磁弹",
                        "en": "Spawn Gauss Rifle & 2mm EC"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000d1eb0 1",
                    "desc": "派发高斯步枪，蓄力后可发射高伤害的穿透弹药。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Gauss_rifle_(Fallout_4)"
                }
            ]
        },
        {
            "category": "👥 伙伴好感度、恶性卡关与阵营进度抢救 (Affinity & Quest Repair)",
            "commands": [
                {
                    "id": "fo4_max_companion_affinity",
                    "name": {
                        "zh-CN": "伙伴好感度设为 1000",
                        "en": "Max Companion Affinity (setav CA_affinity 1000)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setav CA_affinity 1000",
                    "desc": "点击目标同伴后输入本指令，可将好感度设为 1000（好感事件在 250/500/750/1000 触发；若该同伴可恋爱，上限为 1100），并解锁对应的专属 Perk。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_fix_cambridge_danse",
                    "name": {
                        "zh-CN": "修复剑桥警察局丹斯战斗后不说话卡关 (setstage BoS100 40)",
                        "en": "Fix Cambridge Police Danse Dialog Bug"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage BoS100 40",
                    "desc": "若剑桥警察局战斗结束后丹斯未触发后续对话而卡住，可用此指令强制推进任务阶段。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fire_Support"
                },
                {
                    "id": "fo4_companion_moveto",
                    "name": {
                        "zh-CN": "失踪伙伴与狗肉传送回身旁 (player.moveto)",
                        "en": "Teleport Missing Companion (Dogmeat) to Player"
                    },
                    "syntax_type": "creation_hex",
                    "code": "0001d162.moveto player",
                    "desc": "可将狗肉（Dogmeat，ID 0001D162）或走散的同伴传送到玩家面前。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Dogmeat_(Fallout_4)"
                }
            ]
        },
        {
            "category": "⚡ 属性与等级调整 (SPECIAL & Leveling)",
            "commands": [
                {
                    "id": "fo4_max_all_special",
                    "name": {
                        "zh-CN": "力量(Strength)设为10",
                        "en": "Set Strength (SPECIAL) to 10"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav strength 10",
                    "desc": "该命令只把「力量(Strength)」一项设为10；若要把全部7项SPECIAL都设为10，需要对每一项属性分别执行 player.setav <属性名> 10",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_setlevel_50",
                    "name": {
                        "zh-CN": "角色等级直升 50 级 (解锁高阶军械与动力甲刷新)",
                        "en": "Set Player Level to 50"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setlevel 50",
                    "desc": "将角色等级设置为 50 级，使商店与战利品池中出现更高等级装备（包括 X-01 动力装甲）的概率提高。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_adv_skill_points",
                    "name": {
                        "zh-CN": "瞬间赋予 10 点额外特技加点点数 (Perk Points)",
                        "en": "Add 10 Perk Points"
                    },
                    "syntax_type": "creation_hex",
                    "code": "cgf \"Game.AddPerkPoints\" 10",
                    "desc": "为角色增加 10 点 Perk 点数，可用于点出更多技能。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                }
            ]
        },
        {
            "category": "🌌 场景探索、全图地标与自由运镜摄影 (Dev Room, Exploration & FreeCam)",
            "commands": [
                {
                    "id": "fo4_tmm_1",
                    "name": {
                        "zh-CN": "点亮波士顿联邦大地图所有地标 (tmm 1: 支持快速传送)",
                        "en": "Unlock All Map Markers (tmm 1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tmm 1",
                    "desc": "点亮地图上的全部地标，并解锁对应的快速旅行。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_coc_redrocket",
                    "name": {
                        "zh-CN": "传送至红火箭维修站基地 (coc RedRocketExt)",
                        "en": "Teleport to Red Rocket Truck Stop"
                    },
                    "syntax_type": "creation_hex",
                    "code": "coc RedRocketExt",
                    "desc": "将玩家传送到红火箭维修站（Red Rocket Truck Stop）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_tfc_freecam",
                    "name": {
                        "zh-CN": "开启自由飞行摄影相机并定格画面 (tfc 1)",
                        "en": "Toggle Free Camera (tfc 1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tfc 1",
                    "desc": "开启自由摄像机并暂停游戏画面，可脱离角色视角自由移动镜头，便于截图。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_tm_hide_hud",
                    "name": {
                        "zh-CN": "隐藏/恢复全部界面 HUD 界面 (无UI纯净截图)",
                        "en": "Toggle Menus / Hide HUD (tm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tm",
                    "desc": "隐藏全屏准星、血条、AP槽与罗盘。(隐藏后按 ~ 盲打 tm 回车即可重新呼出界面)。",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                }
            ]
        }
    ]
}

OWNED_FIELDS = (
    "hasConsole", "consoleShortcut", "consoleEnableGuide", "consoleCategories", "popularCommands",
    "hasMods", "modInstallPath", "curatedMods",
)

GAME_DATA = (
    (("elden-ring",), ELDEN_RING_DATA),
    (("the-elder-scrolls-v-skyrim-special-edition", "skyrim-se"), SKYRIM_SE_DATA),
    (("fallout-4",), FALLOUT_4_DATA),
)


def build_updates(games):
    ids = {g["id"] for g in games}
    updates = {}
    for aliases, data in GAME_DATA:
        for gid in aliases:
            if gid in ids:
                updates[gid] = dict(data)
    return updates


if __name__ == "__main__":
    write_owned_fields("enrich_rank5_7_flagships.py", OWNED_FIELDS, build_updates)
