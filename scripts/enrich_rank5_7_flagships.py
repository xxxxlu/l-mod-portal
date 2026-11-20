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
            "category": "多人联机与系统大修",
            "desc": "魂系联机体验天花板！彻底移除打完Boss被强行遣返的联机限制，全图无空气墙无缝跑图、死亡围观复活、共乘托雷特灵马、用独立的 .co2 存档、不连官方匹配服务器（第三方 Mod，会不会被封号没有人能担保）。",
            "dependencies": [
                "None (自带独立引导器)"
            ],
            "installPath": "<GameRoot>/Game/ersc/",
            "installSteps": [
                "解压 SeamlessCoop.zip 得到 ersc 文件夹与 launch_elden_ring_seamlesscoop.exe",
                "将上述文件直接复制进游戏目录 Game/ 下",
                "用记事本打开 Game/ersc/ersc_settings.ini，在 cooppassword = 后面输入你和小伙伴约定的联机密码",
                "双击 launch_elden_ring_seamlesscoop.exe 启动，进入游戏后使用道具包里的【小人偶】即可无缝联机！"
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
            "category": "底层框架与核心前置",
            "desc": "法环挂载全类型 Mod 的核心基石！免解包直接挂载 .dcx, .param, regulation.bin 等资源，自带不加载 EAC 的启动方式（只能离线玩），不改游戏原版文件。",
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
            "category": "极客调试与数据检索",
            "desc": "法环极客神器！包含全DLC 物品一键生成 (Item Gib)、全赐福传送点秒亮、360° 自由飞行摄影相机、NPC 赎罪与死人复生、BOSS 随时重置挑战。",
            "dependencies": [
                "Cheat Engine 7.5+",
                "EAC Offline Bypass"
            ],
            "installPath": "自定义目录 (配合 Cheat Engine 使用)",
            "installSteps": [
                "下载并安装 Cheat Engine 7.5+",
                "先运行 launchmod_eldenring.bat 进入游戏并载入存档",
                "双击打开 EldenRing.CT 表，点击左上角电脑图标附着到 eldenring.exe 进程",
                "勾选 Open 表头，展开 Scripts -> Item Gib 即可按图鉴无痛派发全套装备！"
            ],
            "isDirect": False,
            "nexusUrl": "https://github.com/The-Grand-Archives/Elden-Ring-CT-TGA"
        },
        {
            "id": "mod_err_reforged",
            "title": "ERR - ELDEN RING Reforged",
            "author": "Kirnifr and the Reforged team",
            "category": "玩法机制全面重构",
            "desc": "重构交界地战斗机制：新增《只狼》完美招架弹反、全新法术连招、复仇者难度模式、赐福点 Boss 连战挑战！",
            "dependencies": [
                "ModEngine2"
            ],
            "installPath": "<ModEngine2Root>/mod/",
            "installSteps": [
                "下载 ERR 安装包，将其解压覆盖至 ModEngine2/mod/ 目录下",
                "启动 launchmod_eldenring.bat 开始全新的交界地冒险！"
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
            "category": "底层框架与核心前置",
            "desc": "天际Mod生态绝对的基石！大幅拓展 Papyrus 脚本引擎 API，现代 95% 以上的高级 UI、动作与功能 Mod 的强制前置依赖。",
            "dependencies": [
                "None (独立启动器)"
            ],
            "installPath": "<GameRoot>/",
            "installSteps": [
                "根据游戏版本下载对应的 SKSE64 压缩包 (当前最新版解压 skse64_2_02_06.7z)",
                "将压缩包内的 skse64_loader.exe 与两个 .dll 文件直接复制到游戏根目录 (与 SkyrimSE.exe 同级)",
                "将 Data/ 文件夹拖拽合并进游戏的 Data/ 目录",
                "以后每次启动游戏一律双击 skse64_loader.exe 启动！"
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
            "category": "引擎优化与Bug修复",
            "desc": "必装神级插件！彻底修复高帧率物理抽搐、Lip Sync 嘴唇不同步、内存泄漏与各种原因导致的 CTD 崩溃，并自动解锁控制台与 Mod 状态下的 Steam 官方成就！",
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
            "category": "界面增强与UI大修",
            "desc": "彻底颠覆原版主机风格的列表背包！提供强大的分类过滤、关键词搜索、装备属性多栏对照以及核心的 MCM (Mod 配置菜单)！",
            "dependencies": [
                "SKSE64"
            ],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "必须确保已先行安装 SKSE64",
                "通过 MO2 或 Vortex 直接导入 SkyUI_5.2SE.7z 压缩包并激活",
                "启动 skse64_loader.exe 进入游戏，按 ESC 即可看到新增的 Mod Configuration 菜单！"
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
            "category": "综合Bug全修与稳定增强",
            "desc": "耗时十余年修复了天际原版多达数万处恶性任务卡关、网格丢失、材质破损、NPC浮空与文字逻辑错误的总集补丁！",
            "dependencies": [
                "Skyrim Special Edition 官方三大DLC"
            ],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "通过模组管理器安装 USSEP 压缩包",
                "在插件加载顺序 (Load Order) 中将 Unofficial Skyrim Special Edition Patch.esp 置于官方 DLC 之后的最靠前位置！"
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
            "category": "👑 角色状态与神级上帝模式 (God Mode & Invulnerability)",
            "commands": [
                {
                    "id": "skyrim_tgm",
                    "name": {
                        "zh-CN": "开关全能上帝模式 (Toggle God Mode: 无敌/无限魔/无限耐/无限负重)",
                        "en": "Toggle God Mode (tgm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "开启后主角免疫任何物理与魔法伤害、受击不掉血、奔跑施法不消耗耐力与魔法、背包负重锁定无惩罚，爽快畅游天际！",
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
                        "zh-CN": "开关穿墙穿模模式 (Toggle Collision: 悬浮飞行自由穿墙)",
                        "en": "Toggle Collision (tcl)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tcl",
                    "desc": "关闭物理碰撞检测，角色可以在空中任意方向自由漫步飞行、穿透地下墓穴石壁或被卡在山谷缝隙时一秒脱困！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_carryweight",
                    "name": {
                        "zh-CN": "永久扩增随身背包负重上限至 99,999 (垃圾佬必备)",
                        "en": "Set Carry Weight Upper Limit"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 99999",
                    "desc": "将角色背包基础最大负重上限直接修改为 99,999 磅，下地城扫荡几百把重甲龙骨武器依然健步如飞！",
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
                    "desc": "将基础移动速度调为 150% (修改后收刀或拔刀一次即可激活生效)，大幅加快天际原野跑图赶路节奏！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim_Mod:Actor_Value_Indices"
                }
            ]
        },
        {
            "category": "💰 货币、开锁与全技能熟练度满级 (Gold, Lockpicks & Master Skills)",
            "commands": [
                {
                    "id": "skyrim_add_gold_100k",
                    "name": {
                        "zh-CN": "增加 100,000 金币 (FormID: 0000000F / f)",
                        "en": "Add 100,000 Gold"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 100000",
                    "desc": "瞬间向背囊注入 10 万金币，直接买下独孤城傲慢尖塔与各大要塞豪华房产！可简写为 player.additem f 100000。",
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
                    "desc": "派发 1,000 个天际开锁器，地牢宝箱随便撬开不再担心耗尽！可简写为 player.additem a 1000。",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Lockpick"
                },
                {
                    "id": "skyrim_add_dragon_souls",
                    "name": {
                        "zh-CN": "直接获取 100 个龙魂 (用于解锁全套龙吼铭文)",
                        "en": "Add 100 Dragon Souls"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav dragonsouls 100",
                    "desc": "直接向角色赋予 100 个龙魂，省去满世界追逐随机巨龙吸取龙魂的繁琐流程，随时解锁任意龙吼！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim_Mod:Actor_Value_Indices"
                },
                {
                    "id": "skyrim_advskill_smithing",
                    "name": {
                        "zh-CN": "锻造技能熟练度秒升 100 满级",
                        "en": "Advance Smithing Skill to 100"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.advskill smithing 999999",
                    "desc": "向锻造专业技能注入海量经验，无需重复打铁几千把铁匕首，直接点满魔族与龙骨锻造 Perk！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_advskill_enchanting",
                    "name": {
                        "zh-CN": "附魔技能熟练度秒升 100 满级",
                        "en": "Advance Enchanting Skill to 100"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.advskill enchanting 999999",
                    "desc": "附魔专业一秒满级，点出终极双重附魔 Perk，为一件装备同时铭刻两大强力神性词条！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                },
                {
                    "id": "skyrim_advskill_alchemy",
                    "name": {
                        "zh-CN": "炼金术熟练度秒升 100 满级",
                        "en": "Advance Alchemy Skill to 100"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.advskill alchemy 999999",
                    "desc": "炼金专业秒满级，随时调制出增幅数倍伤害与恢复效能的超强药剂！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                }
            ]
        },
        {
            "category": "🐉 全龙吼解锁与零冷却释放 (Dragon Shouts Mastery & Zero Cooldown)",
            "commands": [
                {
                    "id": "skyrim_shout_unrelenting_force",
                    "name": {
                        "zh-CN": "习得并解锁全三段【不卸之力】龙吼 (Fus Ro Dah)",
                        "en": "Teach Unrelenting Force (Fus Ro Dah)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.teachword 13e22",
                    "desc": "直接习得天际最著名的标志性龙吼【伏斯·洛·达】(不卸之力) 第一段铭文 (二段 13e23, 三段 13e24)，将敌人直接吼飞悬崖！",
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
                        "zh-CN": "龙吼冷却时间清零 (无限连续释放龙吼大招)",
                        "en": "Set Shout Recovery Cooldown to Zero"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav shoutrecoverymult 0",
                    "desc": "将龙吼冷却恢复乘数设置为 0，完全消除吼声施放后的漫长倒计时，化身真正的天际龙吼发射加农炮！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim_Mod:Actor_Value_Indices"
                }
            ]
        },
        {
            "category": "⚡ 全 16 件魔神器与远古神装 (Daedric Artifacts & Legendary Weapons)",
            "commands": [
                {
                    "id": "skyrim_spawn_dawnbreaker",
                    "name": {
                        "zh-CN": "派发魔神器：破晓者 (美瑞蒂亚单手剑/亡灵克星金光爆炸)",
                        "en": "Spawn Dawnbreaker (0002ac61)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0004e4ee 1",
                    "desc": "派发美瑞蒂亚光明神剑破晓者，攻击亡灵或尸鬼有极大几率引发大范围神圣爆炸消灭全场尸群！",
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
                    "desc": "残虐魔神钉头锤，击中敌人造成巨量耐力与魔法伤害，并施加 3 秒灵魂陷阱自动灌满黑色灵魂石！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Mace_of_Molag_Bal"
                },
                {
                    "id": "skyrim_spawn_mehrunes_razor",
                    "name": {
                        "zh-CN": "派发魔神器：梅鲁涅斯的剃刀 (近战微小几率一击秒杀一切)",
                        "en": "Spawn Mehrunes' Razor (000240d2)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000240d2 1",
                    "desc": "破坏魔神匕首，攻速极快且每次攻击均有 1.98% 几率直接斩杀无视目标生命值判定（对上古巨龙同样生效）！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Mehrunes_Razor"
                },
                {
                    "id": "skyrim_spawn_azuras_star",
                    "name": {
                        "zh-CN": "派发魔神器：阿祖拉之星 (永不破碎的无限灵魂石)",
                        "en": "Spawn Azura's Star (00063b27)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00063b27 1",
                    "desc": "附魔极客终极神器！捕获灵魂为装备充能后星体永远不会消耗碎裂，可永久反复循环使用！",
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
                    "desc": "瘟疫魔神重盾，格挡举盾时自动在面前张开一层抵御 50 点法术伤害的神圣护盾，完克法师与巨龙吐息！",
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
                    "desc": "谢尔格拉疯神法杖，释放随机不可预测的荒诞魔法：将敌人变成甜甜圈、甜甜圈或者泥沼蟹！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Wabbajack"
                }
            ]
        },
        {
            "category": "🛠️ 锻造神装、龙骨魔族与满级素材 (Daedric/Dragon Armor & Materials)",
            "commands": [
                {
                    "id": "skyrim_spawn_daedric_sword",
                    "name": {
                        "zh-CN": "派发魔族巨剑 (Daedric Greatsword: 0001396b)",
                        "en": "Spawn Daedric Greatsword"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000139b9 1",
                    "desc": "派发天际最高面板基础双手武器之一魔族巨剑，锋利无比造型狰狞霸气！",
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
                    "desc": "派发魔族全套重铠的核心胸甲部分，天际顶级护甲值物理免伤担当！",
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
                    "desc": "批量派发天际极度珍贵的魔族之心，用于在铁匠铺锻造全套魔族护甲与武器！",
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
                    "desc": "批量派发龙鳞，配合龙骨锻造轻甲防御之王【龙鳞轻甲】全套！",
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
                    "desc": "批量派发乌木锭，用于在砂轮和工作台将魔族装备强化至【传奇】(Legendary) 级！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Ebony_Ingot"
                }
            ]
        },
        {
            "category": "🚨 恶性死循环任务急救与强行推进 (Quest Bug Fixes & SetStage)",
            "commands": [
                {
                    "id": "skyrim_fix_greybeards_mq105",
                    "name": {
                        "zh-CN": "强行修复高吼峰灰胡子吼声任务卡关 (setstage MQ105 10)",
                        "en": "Fix Greybeards Call Quest (MQ105)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage MQ105 10",
                    "desc": "击败第一条飞龙后，若灰胡子召唤吼声迟迟不触发无法前往高吼峰，输入此指令强制推进任务阶段开启觐见！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:The_Way_of_the_Voice"
                },
                {
                    "id": "skyrim_fix_alduins_wall_mq203",
                    "name": {
                        "zh-CN": "强行修复【奥杜因之墙】戴尔芬与伊思本站桩不动卡关",
                        "en": "Fix Alduin's Wall Quest Bug (MQ203)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage MQ203 280",
                    "desc": "天空庇护之庙中伊思本不肯点火把或不讲解石壁壁画的祖传恶性 Bug，执行此行直接标记该步完成推进至下一幕！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Alduin%27s_Wall"
                },
                {
                    "id": "skyrim_fix_vaermina_da16",
                    "name": {
                        "zh-CN": "强行修复晨星城噩梦瓦尔米娜苏醒之梦喝药不进回忆",
                        "en": "Fix Waking Nightmare Quest Bug (DA16)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage DA16 200",
                    "desc": "晨星城祭司喝下折磨药水后卡死无法进入梦境回忆的恶性问题，直接跳至净化完成阶段！",
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
                    "desc": "在控制台输出当前激活任务的真实 Quest ID 与目标内部代号，排查卡关必备诊断指令！",
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
                    "desc": "例如将失踪的莱妹莱迪亚 (Lydia 000A2C94) 瞬移回自己面前，再也不用担心伙伴掉队失踪丢失全身家当！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Console"
                }
            ]
        },
        {
            "category": "🏡 炉火 DLC 观湖庄园全建材直装与领地免罪 (Hearthfire & Crime Clearing)",
            "commands": [
                {
                    "id": "skyrim_hearthfire_quarried_stone",
                    "name": {
                        "zh-CN": "派发 500 个采掘石料 (炉火豪宅地基核心: 0300306c)",
                        "en": "Spawn 500 Quarried Stones"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0300306c 500",
                    "desc": "炉火 DLC 自建豪宅（观湖庄园/风亭庄园）必备建材，无需在采石坑按E手动镐击挖掘半小时！",
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
                    "desc": "派发全套自建房所需粘土，用于快速搭建门厅、主厅、炼金塔与陈列室！",
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
                    "desc": "建造庄园需要成百上千根铁钉、门铰链与铁配件，派发铁锭在铁砧上一键敲打成型！",
                    "framework_required": "None (Native Console)",
                    "source": "https://en.uesp.net/wiki/Skyrim:Iron_Ingot"
                },
                {
                    "id": "skyrim_clear_bounty",
                    "name": {
                        "zh-CN": "清空当前要塞所有通缉悬赏罪名 (秒免罪无需坐牢)",
                        "en": "Clear All Crime Bounty"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setcrimegold 0",
                    "desc": "不小心打翻鸡或者误砍卫兵被全城通缉？输入本指令瞬间将悬赏清零，卫兵立即收刀停止敌对！",
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
                    "desc": "Bethesda 官方全物品展示房间！整齐摆放着全天际所有武器、防具、附魔装备、药水、原料的分类宝箱，随意拿取！输入 coc riverwood 即可传回溪木镇！",
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
                    "desc": "一键点亮天际省全部 400 余个地下城、山峰、营地与城市地标，且全部支持直接大地图快速传送！",
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
                    "desc": "将毁灭系、恢复系、变化系、幻术系与召唤系以及所有未实装的隐藏测试法术全部写入法术书！",
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
                    "desc": "脱离角色躯体，摄像机在空中 360 度任意穿行缩放，游戏画面定格暂停，拍摄天际极光与壮丽战斗大片的必备利器！",
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
                    "desc": "隐藏全屏血条、罗盘、准星与菜单界面 (注意隐藏后按 ~ 依然能输入，再次盲打 tm 回车即可恢复菜单)！",
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
            "category": "底层框架与核心前置",
            "desc": "辐射4模组底层扩展核心！释放 Papyrus 脚本潜力，Place Everywhere、MCM 等神级模组的绝对前置，次世代版已更新 v0.7.2+ 专用 loader。",
            "dependencies": [
                "None (独立启动器)"
            ],
            "installPath": "<GameRoot>/",
            "installSteps": [
                "下载与当前游戏版本完全对应的 F4SE 压缩包 (次世代版下 0.7.2+，降级版下 0.6.23)",
                "将 f4se_loader.exe 与相关 .dll 复制到 Fallout 4 游戏根目录",
                "将 Data/ 文件夹拖拽合并进游戏 Data 目录",
                "以后每次启动游戏直接双击 f4se_loader.exe！"
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
            "category": "引擎优化与闪退排错",
            "desc": "辐射4排错天花板神作！彻底修复武器碎片反弹崩溃、内存溢出闪退，并在崩溃瞬间生成高精度的 Crash Log 文本，明确指出是哪件装备或贴图导致报错！",
            "dependencies": [
                "F4SE",
                "xSE Plugin Preloader",
                "Address Library for F4SE Plugins"
            ],
            "installPath": "<GameRoot>/Data/F4SE/Plugins/",
            "installSteps": [
                "使用 MO2 或 Vortex 安装 Buffout 4 及其前置 xSE Plugin Preloader",
                "若发生闪退，前往 Documents/My Games/Fallout4/F4SE/ 查看 crash-*.log 即可精准破案！"
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
            "category": "工坊建造与功能增强",
            "desc": "垃圾佬造城必备神技！彻底解除工房红圈禁止摆放限制，支持穿插穿模、精准三轴旋转 (按 X/Y/Z)、缩放大小，把庇护山丘打造成赛博堡垒！",
            "dependencies": [
                "F4SE"
            ],
            "installPath": "<GameRoot>/Data/F4SE/Plugins/",
            "installSteps": [
                "确保已安装 F4SE",
                "通过模组管理器安装 Place Everywhere",
                "进入建造模式，按 F1 开关碰撞检测，按 F2 开关贴合吸附！"
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
            "category": "玩法机制全面重构",
            "desc": "将辐射4变成真正的模拟城市！刁民居民会自动划定商业区、住宅区、工业区自行建房交税，附带数十小时的全新全配音支线主线剧情！",
            "dependencies": [
                "Workshop Framework",
                "HUDFramework"
            ],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "安装前置 Workshop Framework",
                "安装 Sim Settlements 2 及其剧情扩展章节包",
                "在游戏内建造并拾取【ASAM 传感器】，启动第一块住宅规划区！"
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
                        "zh-CN": "开关全能上帝模式 (Toggle God Mode: 无敌/弹药无限/负重无限)",
                        "en": "Toggle God Mode (tgm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "开启后主角免疫一切枪弹物理打击与高空坠落、无限 AP 行动点、弹药无限且无需重新换弹、背包负重解除惩罚！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_tim",
                    "name": {
                        "zh-CN": "开关不死锁血模式 (Toggle Immortal Mode: 挨打掉血但绝对不死)",
                        "en": "Toggle Immortal Mode (tim)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tim",
                    "desc": "沉浸式战斗首选！角色受到攻击会正常流血受创与显示残废动画，但生命值降至最低点时锁死为 1，绝不会死亡坏档！",
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
                    "desc": "关闭物理体积碰撞，主角可在废土废墟大楼和废土深坑之间自由穿墙穿模飞行，卡进地形时秒脱困！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_rads_zero",
                    "name": {
                        "zh-CN": "角色辐射污染彻底清零 (消除红色上限减血条)",
                        "en": "Clear Radiation Pollution"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav rads 0",
                    "desc": "跳进发光海被重度辐射污染？输入本指令瞬间将体内的辐射累积清零，完整释放被红条侵占的生命上限！",
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
                    "desc": "将基础负重提升至 10 万磅，废土上的破轮胎、风扇、显微镜、核子可乐瓶通通搬走不再超重减速！",
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
                    "desc": "向背囊注入 10 万瓶盖，秒变废土顶级资本巨鳄，钻石城全部商铺随便扫荡！可简写为 player.additem f 100000。",
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
                    "desc": "生成 1,000 根发夹，撬开全联邦所有主保险箱与锁闭铁门！可简写为 player.additem a 1000。",
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
                    "desc": "派发 100 颗满电量核聚变核心，动力装甲喷气背包随便飞，彻底告别电量焦虑！",
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
                    "desc": "随身携带 200 支军规治疗针，快捷栏绑定随时续命！",
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
            "category": "🏗️ 聚落建造空间无限解除与全建材 (Infinite Settlement & Building Mats)",
            "commands": [
                {
                    "id": "fo4_settlement_size_bypass",
                    "name": {
                        "zh-CN": "彻底解除聚落建造空间容量上限 (setav 349 9999999)",
                        "en": "Bypass Settlement Building Size Budget"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setav 349 9999999",
                    "desc": "走到工房控制台前按下 ~ 鼠标点击工房，输入此代码将空间预算最大值提升至千万级，右上角建造容量条直接清空，随心所欲盖摩天大楼！",
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
                    "desc": "派发 1,000 块钢铁，用于搭建混凝土墙、金属工字钢架构与避难所大门！",
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
                    "desc": "派发 1,000 捆木料，快速建造谷仓、木屋、地板与哨塔防御设施！",
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
                    "desc": "聚落通电最紧缺的金属铜，批量派发，随意搭建核能发电机、电线塔与防御重型激光炮塔！",
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
                        "zh-CN": "手持武器附魔【双弹】传奇词条 (伤害直接翻倍: 001cc2ac)",
                        "en": "Attach Legendary Mod: Two Shot"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001cc2ad",
                    "desc": "把武器扔在地上，按 ~ 呼出控制台鼠标点击武器，输入此代码即可瞬间赋予【双弹】前缀，每次扣扳机射出双倍弹头，伤害翻倍！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_explosive",
                    "name": {
                        "zh-CN": "手持武器附魔【爆破】传奇词条 (每发附带范围爆炸: 001e7c20)",
                        "en": "Attach Legendary Mod: Explosive"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001e73bd",
                    "desc": "给冲锋枪、加特林或霰弹枪附魔爆破词条，子弹命中引发连锁范围剧烈爆炸，扫荡泥沼蟹与掠夺者如割草！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_furious",
                    "name": {
                        "zh-CN": "手持武器附魔【狂怒】传奇词条 (连续命中伤害无限叠加: 001f6ad4)",
                        "en": "Attach Legendary Mod: Furious"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001ef481",
                    "desc": "近战刀剑或高射速武器神器，每次命中同一目标伤害逐级倍增，单挑狂暴传奇死爪只需数秒！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_never_ending",
                    "name": {
                        "zh-CN": "手持武器附魔【无底洞】传奇词条 (无限弹匣免换弹: 001ed37e)",
                        "en": "Attach Legendary Mod: Never Ending"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001cc2ac",
                    "desc": "消除武器换弹动作，弹匣容量直接与背包总弹药打通，扣住扳机无限持续狂风骤雨般倾泻火力！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_legendary_weapon_effects"
                },
                {
                    "id": "fo4_attachmod_kneecapper",
                    "name": {
                        "zh-CN": "手持武器附魔【膝盖收割者】传奇词条 (20%几率打断腿瘫痪: 001f1048)",
                        "en": "Attach Legendary Mod: Kneecapper"
                    },
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001f1048",
                    "desc": "废土安全感神器，攻击命中敌人有 20% 几率强制打断其双腿，让凶残的狂暴死爪与突袭者当场倒地爬行！",
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
                    "desc": "潜行狙击流终极核心，开幕潜行爆头搭配消音武器打出高达数千点的极限毁灭数字！",
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
                    "desc": "派发辐射4最高等级动力装甲 X-01 头盔，装甲工作台上可升级高亮侦测红外 HUD！",
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
                    "desc": "派发 X-01 动力装甲躯干核心，可改装装备喷气飞行背包 (Jetpack) 实现翱翔飞行！",
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
                    "desc": "派发 X-01 左右双臂组件，可加装特斯拉线圈提高近战格斗与电击反伤威力！",
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
                    "desc": "派发 X-01 左右腿部装甲，改装校准减震器提供额外 100 磅巨额随身负重加成！",
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
                    "desc": "派发废土单兵战略核武器胖子发射器！搭配 player.additem 000e6b2e 20 获得 20 枚迷你核弹，弹指间强虏灰飞烟灭！",
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
                    "desc": "废土单发伤害之王高斯步枪，蓄力电磁加速射击造成毁灭性穿透伤害！",
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
                        "zh-CN": "伙伴好感度瞬间拉满 1000 (秒触发专属任务与终极Perk)",
                        "en": "Max Companion Affinity (setav CA_affinity 1000)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setav CA_affinity 1000",
                    "desc": "按 ~ 打开控制台鼠标点击同伴 (如派普、居里、凯特、丹斯)，输入此代码瞬间将好感度升至 1000 崇拜满级，立即触发告白对话并解锁强力专属永久被动 Perk！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_fix_cambridge_danse",
                    "name": {
                        "zh-CN": "强行修复剑桥警察局丹斯战斗后不说话卡关 (setstage BoS100 40)",
                        "en": "Fix Cambridge Police Danse Dialog Bug"
                    },
                    "syntax_type": "creation_hex",
                    "code": "setstage BoS100 40",
                    "desc": "剑桥警察局消灭狂暴尸鬼后，丹斯一直警戒重复'检查四周'不触发对话的经典祖传恶性 Bug，执行此行直接推进任务解冻对话！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fire_Support"
                },
                {
                    "id": "fo4_companion_moveto",
                    "name": {
                        "zh-CN": "失踪伙伴与狗肉瞬移召回身旁 (player.moveto)",
                        "en": "Teleport Missing Companion (Dogmeat) to Player"
                    },
                    "syntax_type": "creation_hex",
                    "code": "0001d162.moveto player",
                    "desc": "寻找走丢的心爱狗肉 (Dogmeat 0001D162) 或把走散的同伴秒传到主角跟前，再也不怕在废土走失！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Dogmeat_(Fallout_4)"
                }
            ]
        },
        {
            "category": "⚡ SPECIAL 属性拉满与批处理极速调优 (SPECIAL & Bat Scripts)",
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
                    "desc": "将角色等级瞬间提升至 50 级，废土所有军火商与野外动力装甲骨架将直接刷出顶级 X-01 装备！",
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
                    "desc": "向角色点数池注入 10 点专属 Perk 点，随心所欲点满枪侠、突击手与神秘客技能！",
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
                    "desc": "一键激活大地图所有庇护山丘、钻石城、发光海与钢铁兄弟会飞艇全部数百个地标，省去漫长探路！",
                    "framework_required": "None (Native Console)",
                    "source": "https://fallout.fandom.com/wiki/Fallout_4_console_commands"
                },
                {
                    "id": "fo4_coc_redrocket",
                    "name": {
                        "zh-CN": "瞬间传送至红火箭维修站基地 (coc RedRocketExt)",
                        "en": "Teleport to Red Rocket Truck Stop"
                    },
                    "syntax_type": "creation_hex",
                    "code": "coc RedRocketExt",
                    "desc": "不管身在何方遇到险境，输入本指令瞬间脱出并传送回红火箭维修站工房大本营！",
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
                    "desc": "暂停废土一切动作，相机脱离主角躯体自由升空俯瞰波士顿废墟壮观全景，拍摄工业级壁纸大片！",
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
