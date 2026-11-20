#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/enrich_rank8_14_tier2.py
Content for ranks 8-14:
  - Rank 8: 幻兽帕鲁 (Palworld) [UE5 + UE4SS]
  - Rank 9: 星空 (Starfield) [Creation 2]
  - Rank 10: 侠盗猎车手5 (Grand Theft Auto V) [RAGE + ScriptHookV]
  - Rank 11: 荒野大镖客：救赎2 (Red Dead Redemption 2) [RAGE + ScriptHookRDR2]
  - Rank 12: 怪物猎人：世界 (Monster Hunter: World) [MT Framework + Stracker / REFramework]
  - Rank 13: 只狼：影逝二度 (Sekiro: Shadows Die Twice) [FromSoftware + ModEngine]
  - Rank 14: 生化危机4：重制版 (Resident Evil 4 Remake) [RE Engine + REFramework]

Writes only the fields in OWNED_FIELDS, through gamedata_guard: the master data must
exist, radar and trainer fields are never written (trainer data comes from
fling_trainer_sync.py), the order of the games is kept, and in public/data.js only
the GAMES_DATA segment changes (TRANSLATIONS_DATA is left alone).

Usage: python3 scripts/enrich_rank8_14_tier2.py [--dry-run]
"""

from gamedata_guard import write_owned_fields

# ==============================================================================
# RANK 8: 幻兽帕鲁 (Palworld)
# ==============================================================================
PALWORLD_DATA = {
    "rank": 8,
    "hasConsole": False,
    "consoleShortcut": "F10 或 ~ (需安装 RE-UE4SS xinput1_3.dll 注入底层)",
    "consoleEnableGuide": {
        "zh-CN": "【UE4SS 注入与打字控制台开启指南】\n1. 下载 UE4SS (v3.0.1 纯净版)，将压缩包解压至游戏根目录：Palworld/Pal/Binaries/Win64/；\n2. 确认该目录下存在 UE4SS.dll、xinput1_3.dll 以及 mods/ 文件夹；\n3. 启动游戏，在单机或本地专用服务器中按 F10 唤出 UE4SS 图形控制台，或按 ~ 唤出原生终端；\n4. 即可直接运行闪光帕鲁生成、全图鉴解锁、属性注入与自由镜头摄影！",
        "en": "Install UE4SS (v3.0.1) into Palworld/Pal/Binaries/Win64/. Press F10 or ~ in-game to bring up Lua console for Pal spawner and Paldeck unlocks."
    },
    "popularCommands": [],
    "hasMods": True,
    "curatedMods": [
        {
            "id": "pal_ue4ss",
            "title": "RE-UE4SS - Mod Loader - Debug Tool - Pak Mod Enabler",
            "author": "UE4SS-RE",
            "category": "Core Framework (核心前置)",
            "desc": "幻兽帕鲁运行 Lua 模组、UI 扩展与控制台命令类 Mod 所需的前置库。",
            "dependencies": [
                "None (Native Injector)"
            ],
            "installPath": "Palworld/Pal/Binaries/Win64/",
            "isDirect": True,
            "installSteps": [
                "1. 点击上方按钮下载 UE4SS_v3.0.1_Palworld.zip 压缩包；",
                "2. 打开游戏安装路径进入 Pal/Binaries/Win64/；",
                "3. 将压缩包内的 UE4SS.dll、xinput1_3.dll 和 mods 文件夹直接解压到该目录；",
                "4. 启动游戏即可生效，按 F10 即可呼出控制面板。"
            ],
            "nexusUrl": "https://github.com/UE4SS-RE/RE-UE4SS",
            "version": "3.0.1",
            "downloadUrl": "https://github.com/UE4SS-RE/RE-UE4SS/releases/download/v3.0.1/UE4SS_v3.0.1.zip",
            "downloadFilename": "UE4SS_v3.0.1.zip"
        },

    ],
    "consoleCategories": [],
    "scenarioBundles": [],
    "pitfallNote": {
        "title": "老L避坑笔记 (幻兽帕鲁 樱岛最新版)",
        "tips": [
            "【联机前先移除】：UE4SS 只在单人模式或自己开的本地房间里用，会不会被封没有人能担保。进官方或别人的服务器前，先把 UE4SS 的 dll 移走，别在公开服务器作弊。",
            "【帕鲁抑郁生病治愈】：据点帕鲁容易因地形卡住无法进食而导致【抑郁症/骨折】。使用 give Med_Low 10 获取高级药品直接投喂，并在箱子旁放置温泉以彻底稳定 SAN 值。",
            "【负重过载急救】：金属矿区挖掘超载走不动时，掏出抓钩枪对着地面或树干射击，利用抓钩拉力可以直接无视任何负重限制飞速前行。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】幻兽帕鲁 UE4SS 检查\necho ========================================================\necho   【老L·单机避坑局】幻兽帕鲁 UE4SS 检查脚本\necho   只检查 UE4SS.dll 在不在，不改任何文件\necho ========================================================\necho.\n\nset \"WIN64=Pal\\Binaries\\Win64\"\nif not exist \"Pal\\Binaries\\Win64\\Palworld-Win64-Shipping.exe\" (\n    echo [!] 当前目录下没有 Pal\\Binaries\\Win64\\Palworld-Win64-Shipping.exe，脚本什么都没改。\n    echo     请把本脚本放到 Palworld 游戏安装根目录再运行。\n    echo.\n    pause\n    exit /b\n)\nset \"UE4SS_DLL=\"\nif exist \"%WIN64%\\ue4ss\\UE4SS.dll\" set \"UE4SS_DLL=%WIN64%\\ue4ss\\UE4SS.dll\"\nif not defined UE4SS_DLL if exist \"%WIN64%\\UE4SS.dll\" set \"UE4SS_DLL=%WIN64%\\UE4SS.dll\"\nif defined UE4SS_DLL (\n    echo [+] 找到 %UE4SS_DLL%。只检查了文件在不在，没检查版本，也没检查能不能加载。\n    echo [i] 游戏内按 F10 试试 UE4SS 菜单。\n) else (\n    echo [!] 没找到 UE4SS.dll：请把 UE4SS 解压到 %WIN64%\\ 。\n)\necho [i] 只在单人模式或自己开的房间里用；进别人的服务器前先把 UE4SS 移走。\necho [i] 脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。\necho.\npause\n",
    "verifiedPatch": "v0.3.x（未实测）",
    "radarSecretCode": "帕鲁"
}

# ==============================================================================
# RANK 9: 星空 (Starfield)
# ==============================================================================
STARFIELD_DATA = {
    "rank": 9,
    "hasConsole": True,
    "consoleShortcut": "~ (波浪键直接唤出 Bethesda Creation 2 原生终端)",
    "consoleEnableGuide": {
        "zh-CN": "【Creation 2 原生控制台与防成就锁死指南】\n1. 键盘直接按 ~ 键呼出原生控制台；\n2. 首次输入指令前，建议安装 Baka Achievement Enabler 模组，防止开启控制台后 Steam 成就失效；\n3. 控制台支持全部物品 Hex 编号注入、飞船建造部件尺寸突破、特质修改与场景漫游！",
        "en": "Press ~ to open Creation 2 console. Install SFSE and Baka Achievement Enabler to prevent achievements from being disabled."
    },
    "popularCommands": [
        "player.additem 0000000F 1000000",
        "player.additem 0000000A 100",
        "tgm",
        "player.setav carryweight 9999",
        "tcl"
    ],
    "hasMods": True,
    "curatedMods": [
        {
            "id": "sfse_core",
            "title": "Starfield Script Extender (SFSE)",
            "author": "SFSE Team",
            "category": "框架 / 前置",
            "desc": "扩展 Starfield 脚本能力的工具，是许多 UI 与玩法类 Mod 的前置；游戏更新后需要等待作者更新对应版本。",
            "dependencies": [
                "None (Native Extender)"
            ],
            "installPath": "Starfield/ (游戏根目录)",
            "isDirect": False,
            "installSteps": [
                "1. 点击按钮直接下载 sfse_0_02_14.7z 压缩包；",
                "2. 打开 Starfield 游戏安装根目录 (包含 Starfield.exe 的位置)；",
                "3. 将压缩包内的 sfse_*.dll 与 sfse_loader.exe 解压到根目录；",
                "4. 后续启动游戏请直接双击运行 sfse_loader.exe 即可。"
            ],
            "nexusUrl": "https://www.nexusmods.com/starfield/mods/106",
            "version": "0.2.21",
            "downloads": "3.2M",
            "endorsements": "40.2K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "starfield_community_patch",
            "title": "Starfield Community Patch (SFCP)",
            "author": "Starfield Modding Community",
            "category": "漏洞修复",
            "desc": "由社区开发者维护的综合性漏洞修复 Mod，用于修复游戏中的任务、NPC 与其他已知问题。",
            "dependencies": [
                "SFSE"
            ],
            "installPath": "Starfield/Data/",
            "isDirect": False,
            "installSteps": [
                "1. 下载压缩包解压出 StarfieldCommunityPatch.esm；",
                "2. 放入 Starfield/Data/ 文件夹；",
                "3. 在游戏主菜单 Mods 选项卡中勾选启用该 ESM。"
            ],
            "nexusUrl": "https://www.nexusmods.com/starfield/mods/1",
            "version": "1.0.0",
            "downloads": "445.1K",
            "endorsements": "8.8K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "undelayed_menus",
            "title": "Undelayed Menus",
            "author": "Seb263",
            "category": "界面",
            "desc": "移除打开物品栏、星图与技能界面时约 0.5 秒的淡入动画，使菜单响应更快。",
            "dependencies": [
                "None (SWF Override)"
            ],
            "installPath": "Starfield/Data/Interface/",
            "isDirect": False,
            "installSteps": [
                "1. 下载压缩包解压获取 Interface/ 文件夹；",
                "2. 将其放入 Starfield/Data/ 目录下；",
                "3. 游戏中按 Tab 打开菜单即可感受更快的响应速度。"
            ],
            "nexusUrl": "https://www.nexusmods.com/starfield/mods/404",
            "version": "1.0.6",
            "downloads": "792.5K",
            "endorsements": "14.8K",
            "checkedAt": "2026-11-20"
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 核心上帝模式 (God Mode & Invulnerability)",
            "commands": [
                {
                    "id": "sf_tgm",
                    "name": {
                        "zh-CN": "开关上帝模式 (tgm)",
                        "en": "Toggle God Mode (tgm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "开启后角色生命值、氧气与弹药不受限制，飞船护盾也保持满值；再次输入关闭。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_tim",
                    "name": {
                        "zh-CN": "真不死模式 (TIM - 真实扣血但绝不死亡)",
                        "en": "Toggle Immortal Mode (tim)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tim",
                    "desc": "角色仍会正常受到伤害，但生命值不会降到 0 以下而倒下，保留战斗的紧张感。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_tcl",
                    "name": {
                        "zh-CN": "自由飞行与穿墙模式 (TCL - 脱离卡死探图)",
                        "en": "Toggle Collision (tcl)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tcl",
                    "desc": "关闭物理碰撞体积，角色可自由在空中悬浮穿墙，探索被锁闭的隐秘房间与卡死解救。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_tcai",
                    "name": {
                        "zh-CN": "关闭所有敌人战斗仇恨 AI (停火木桩模式)",
                        "en": "Toggle Combat AI (tcai)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tcai",
                    "desc": "全局冻结所有太空海盗与敌对生物的攻击判定，敌人将站立不动任由测试武器。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },

            ]
        },
        {
            "category": "🚀 飞船维修与部件补给 (Ship Repair & Parts)",
            "commands": [
                {
                    "id": "sf_ship_repair",
                    "name": {
                        "zh-CN": "获取飞船零件维修套件 x50",
                        "en": "Give 50 Ship Repair Parts"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0003FB19 50",
                    "desc": "在太空中按 O 键即可消耗零件快速修复破损的飞船船体装甲。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Ship_Parts"
                }
            ]
        },
        {
            "category": "🧬 角色外观、特质与等级调整 (Traits, Background & Leveling)",
            "commands": [
                {
                    "id": "sf_show_race_menu",
                    "name": {
                        "zh-CN": "随时重新打开整容与特质捏脸界面",
                        "en": "Show Race & Trait Menu"
                    },
                    "syntax_type": "creation_hex",
                    "code": "showracemenu",
                    "desc": "无视所在星系随时开启角色捏脸、体型调整、背景身份与初始特质重新选择面板。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_add_trait_hero",
                    "name": {
                        "zh-CN": "添加特质：英雄崇拜 (获得狂热粉丝NPC)",
                        "en": "Add Trait: Hero Worshipped"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.addperk 00227FD9",
                    "desc": "添加该特质后会获得一位会不定期出现并送礼物的「狂热粉丝」NPC，但他也会频繁打扰你。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Hero_Worshipped"
                },
                {
                    "id": "sf_add_trait_home",
                    "name": {
                        "zh-CN": "添加特质：梦想家园 (获得Nesoi住宅)",
                        "en": "Add Trait: Dream Home"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.addperk 00227FDF",
                    "desc": "添加该特质后，可在奥林匹斯星系的 Nesoi 获得一套自有住宅；需以每周 500 信用点的方式偿还共 12.5 万信用点的贷款。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Dream_Home_(Trait)"
                },
                {
                    "id": "sf_set_level_60",
                    "name": {
                        "zh-CN": "角色等级直接设定为 Lv60",
                        "en": "Set Player Level to 60"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setlevel 60",
                    "desc": "将角色等级设置为 60 级，使更高阶的装备与传奇武器在战利品与商店中出现的概率提高。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                }
            ]
        },
        {
            "category": "💰 信用币财富、开锁数码撬棒与负重 (Credits, Digipicks & Carry Weight)",
            "commands": [
                {
                    "id": "sf_add_credits_1m",
                    "name": {
                        "zh-CN": "获得 1,000,000 信用币",
                        "en": "Add 1,000,000 Credits"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 1000000",
                    "desc": "向背包增加 1,000,000 信用币。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_add_digipicks",
                    "name": {
                        "zh-CN": "获得数码撬棒 x100 (开锁小游戏备用)",
                        "en": "Add 100 Digipicks"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000A 100",
                    "desc": "向背包增加 100 个数码撬棒，用于开锁小游戏中的试错消耗。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_carry_weight_max",
                    "name": {
                        "zh-CN": "角色随身负重上限提升至 9,999",
                        "en": "Set Player Carry Weight to 9,999"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 9999",
                    "desc": "将角色负重上限设置为 9,999，基本不会再因超重而减速。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_pay_bounty",
                    "name": {
                        "zh-CN": "清除当前目标所属阵营的通缉赏金 (player.paycrimegold)",
                        "en": "Clear Faction Bounty"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.paycrimegold 0 0",
                    "desc": "支付当前目标所属阵营的通缉赏金（信用点从库存中扣除）；0 0 表示不进监狱也不没收赃物。每次只结清目标所属的那一个阵营，不会清除其他阵营的通缉。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_unlock_target",
                    "name": {
                        "zh-CN": "强制解锁准星所指之门/保险箱",
                        "en": "Unlock Target Door / Safe"
                    },
                    "syntax_type": "creation_hex",
                    "code": "unlock",
                    "desc": "控制台开启时用鼠标点击锁住的门或容器，输入 unlock 即可直接解锁。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                }
            ]
        },
        {
            "category": "🔫 传奇金色武器与高科技词条附魔 (Legendary Weapons & Weapon Mods)",
            "commands": [
                {
                    "id": "sf_weapon_hardtarget",
                    "name": {
                        "zh-CN": "获得硬靶高精狙击步枪 (Hard Target)",
                        "en": "Give Hard Target Sniper Rifle"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000546CC 1",
                    "desc": "Combatech 制造的 .50 口径弹药步枪，基础伤害较高。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Hard_Target"
                },
                {
                    "id": "sf_weapon_inflictor",
                    "name": {
                        "zh-CN": "获得瓦鲁恩折磨者粒子束步枪",
                        "en": "Give Va'ruun Inflictor Particle Rifle"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0026D8A0 1",
                    "desc": "瓦鲁恩教派制造的粒子束步枪，兼具物理与能量伤害。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Va%27ruun_Inflictor"
                },
                {
                    "id": "sf_weapon_bigbang",
                    "name": {
                        "zh-CN": "获得大爆炸粒子束霰弹枪 (Big Bang)",
                        "en": "Give Big Bang Shotgun"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0026D963 1",
                    "desc": "Combatech 制造的粒子束霰弹枪，近距离伤害较高。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Big_Bang"
                },
                {
                    "id": "sf_attach_instigating",
                    "name": {
                        "zh-CN": "给手中武器附魔词条：煽动 (满血目标伤害翻倍)",
                        "en": "Attach Mod: Instigating (Double Damage)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.attachmod 000F2012",
                    "desc": "为当前武器附加传奇词条【煽动】：若目标生命值为满，造成 2 倍伤害。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Effects"
                }
            ]
        },
        {
            "category": "🛡️ 传奇宇航服、头盔与深度强化 (Legendary Spacesuits & Helmets)",
            "commands": [
                {
                    "id": "sf_suit_starborn",
                    "name": {
                        "zh-CN": "获得星裔天相战甲 (NG+1 周目开始获得)",
                        "en": "Give Starborn Spacesuit Astra"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0012E187 1",
                    "desc": "进入新游戏+（NG+1）周目开始时获得的一体式宇航服，各项防护数值均衡且较高。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Starborn_Spacesuit_Astra"
                },
                {
                    "id": "sf_suit_mantis",
                    "name": {
                        "zh-CN": "获得蝠鲼传奇宇航服 (完成蝠鲼基地据点后获得)",
                        "en": "Give Mantis Spacesuit"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00226299 1",
                    "desc": "完成「蝠鲼的巢穴」任务后，在蝠鲼秘密基地获得的全套宇航服之一。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Mantis_Spacesuit"
                },
                {
                    "id": "sf_helmet_mercenary",
                    "name": {
                        "zh-CN": "佣兵太空头盔",
                        "en": "Mercenary Space Helmet"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0016E0B5 1",
                    "desc": "获得佣兵太空头盔（Mercenary Space Helmet）",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Mercenary_Space_Helmet"
                },
                {
                    "id": "sf_attach_chameleon",
                    "name": {
                        "zh-CN": "伪装",
                        "en": "Camouflaged"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.attachmod 0019AFF2",
                    "desc": "为防具附加「伪装」效果：潜行且静止不动时近乎隐形",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Effects"
                }
            ]
        },
        {
            "category": "🌌 星图探索与镜头/时间控制 (Star Map, Camera & Time)",
            "commands": [
                {
                    "id": "sf_tmm_all",
                    "name": {
                        "zh-CN": "点亮星图全部地标与着陆点 (TMM 1)",
                        "en": "Show All Map Markers (tmm 1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tmm 1",
                    "desc": "点亮星系图与星球表面全部探索标、外星神庙、研究站与隐秘城市，随时随地直接传送。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_set_timescale",
                    "name": {
                        "zh-CN": "将星空世界昼夜流速设定为真实 1:1 时间",
                        "en": "Set Real-time Timescale (1:1)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "set timescale to 1",
                    "desc": "将昼夜更替速度放慢至与现实时间 1:1 同步，静静欣赏深空星球日出日落与恒星环日升腾。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_tm_toggle",
                    "name": {
                        "zh-CN": "隐藏/恢复全部界面 HUD (纯净4K太空截图)",
                        "en": "Toggle Menus / HUD (tm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tm",
                    "desc": "隐藏或恢复血条、氧气表、指南针与准星等界面元素，便于截图。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_kah_enemies",
                    "name": {
                        "zh-CN": "击杀视野内所有敌对目标 (kah)",
                        "en": "Kill All Hostiles (kah)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "kah",
                    "desc": "立即杀死当前场景中处于战斗状态的所有敌对目标。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfield.fandom.com/wiki/Help_command"
                }
            ]
        },
        {
            "category": "🛠️ 哨站建材与稀有矿物补给 (Outpost Resources & Exotic Mats)",
            "commands": [
                {
                    "id": "sf_res_iron",
                    "name": {
                        "zh-CN": "获得铁矿原料 x500 (哨站框架结构基础)",
                        "en": "Give 500 Iron Ore"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000556E 500",
                    "desc": "大量补充建造哨站气闸舱、停机坪与工业货柜最基础的钢结构钢铁矿石。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_res_aluminum",
                    "name": {
                        "zh-CN": "获得铝矿原料 x500 (风力发电机与太阳能板)",
                        "en": "Give 500 Aluminum"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000557D 500",
                    "desc": "哨站能源系统与固态储水罐最核心轻质金属材料。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_res_titanium",
                    "name": {
                        "zh-CN": "获得钛金属 x300 (高强度精密机械制造)",
                        "en": "Give 300 Titanium"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000556D 300",
                    "desc": "用于制造高科技军工武器配件与强化哨站防御炮塔的高刚度耐高温钛合金。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_res_adhesive",
                    "name": {
                        "zh-CN": "获得粘合剂 x300 (枪械改装最稀缺战略材料)",
                        "en": "Give 300 Adhesives"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000055B1 300",
                    "desc": "所有枪械瞄准镜、枪口消音器与弹匣扩容改装中最容易匮乏的稀缺天然粘着原料。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_res_sealant",
                    "name": {
                        "zh-CN": "获得密封剂 x300 (防化舱与居住舱气密胶)",
                        "en": "Give 300 Sealants"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000055CC 300",
                    "desc": "用于密封哨站走廊与太空服隔绝层的高分子密封材料。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "sf_starter_bundle",
            "type": "starter",
            "name": "新手星际启航起飞包",
            "tag": "👑 萌新首选 · 零门槛",
            "badge": "星际起航",
            "desc": "开启上帝模式 + 获得 100 万信用币 + 100 个数码撬棒 + 负重上限提升至 9,999，方便新手开局。",
            "highlights": ["上帝模式，角色免疫伤害", "1,000,000 信用币，可用于购买飞船", "100 个数码撬棒，方便开锁", "负重上限 9,999，大幅减少负重限制"],
            "code": "-- [老L·极客场景套餐] 星空 新手星际启航起飞包 (原生控制台，未实测)\ntgm\nplayer.additem 0000000F 1000000\nplayer.additem 0000000A 100\nplayer.setav carryweight 9999"
        },

    ],
    "pitfallNote": {
        "title": "老L避坑笔记 (星空 破碎空间 DLC 完全版)",
        "tips": [
            "【Steam成就防锁死门禁】：Bethesda 在输入控制台命令时会标记存档为 Modded 并禁用 Steam 成就！可以装 Baka Achievement Enabler（需要 SFSE），让开过控制台的存档继续拿成就；游戏更新后它可能要等作者适配。",
            "【改船部件重叠报错破解】：在官方造船厂经常遇到【模块存在重叠】无法保存。下载安装本站推荐的 Ship Builder Tolerance Tweaks 即可完全无视空间重叠，打造致密外装母舰。",
            "【卡死与恶性任务急救】：若因 NPC 浮空或被锁在门后无法交任务，打开控制台输入 tcl 开启穿墙飞入室内，或使用 setstage 命令直接强行推进断掉的任务流程节点。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】星空 SFSE 启动助手\necho ========================================================\necho   【老L·单机避坑局】星空 SFSE 启动脚本\necho   找到 sfse_loader.exe 就用它启动，找不到就用原版启动\necho ========================================================\necho.\nif not exist \"Starfield.exe\" (\n    echo [!] 当前目录下没有 Starfield.exe，脚本什么都没改。\n    echo     请把本脚本放到 Starfield 游戏安装根目录再运行。\n    echo.\n    pause\n    exit /b\n)\nif exist \"sfse_loader.exe\" (\n    echo [+] 找到 sfse_loader.exe，用它启动游戏 ...\n    start \"\" \"sfse_loader.exe\"\n) else (\n    echo [i] 没找到 sfse_loader.exe，用 Starfield.exe 原版启动 ...\n    start \"\" \"Starfield.exe\"\n)\necho [i] 脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。\necho.\npause\n",
    "verifiedPatch": "v1.14（未实测）",
    "radarSecretCode": "星空"
}

# ==============================================================================
# RANK 10: 侠盗猎车手 5 (Grand Theft Auto V)
# ==============================================================================
GTA5_DATA = {
    "rank": 10,
    "hasConsole": True,
    "consoleShortcut": "~ (故事模式原生官方秘籍终端) 或 F4 (ScriptHookV 内置纯净修改菜单)",
    "consoleEnableGuide": {
        "zh-CN": "【单机故事模式指南】\n1. 官方原生秘籍：进入单机故事模式后，直接按键盘左上角 ~ 键输入全英文秘籍并回车；\n2. ScriptHookV 离线内置菜单：将 ScriptHookV.dll、dinput8.dll 以及 NativeTrainer.asi 放入 GTA5 游戏根目录；\n3. 在故事模式按 F4 呼出图形化修改菜单，小键盘 8/2/4/6 切换方向，5 确认，0 返回；\n4. ⚠️ 别带着 ASI 插件或修改器文件进 GTA Online 线上模式，有封号风险。把 dinput8.dll 改名为 .bak 只是停掉 ASI 加载器；mods 文件夹、改过的 rpf 等其它改动要自己移走。",
        "en": "Press ~ to input native cheats or press F4 with ScriptHookV for offline Native Trainer. NEVER go online with mods."
    },
    "popularCommands": [
        "PAINKILLER",
        "TURTLE",
        "TOOLUP",
        "COMET",
        "BUZZOFF",
        "LAWYERUP"
    ],
    "hasMods": True,
    "curatedMods": [
        {
            "id": "gta_scripthookv",
            "title": "Script Hook V",
            "author": "Alexander Blade",
            "category": "Core Framework (核心前置)",
            "desc": "GTA V 的脚本插件加载库，是运行 ASI 脚本和大多数离线单机 Mod 菜单的前置库。自带 Native Trainer 离线菜单；进入 GTA Online 多人模式时会自动关闭游戏，不能在线上使用。",
            "dependencies": [
                "None (Native DLL)"
            ],
            "installPath": "Grand Theft Auto V/ (游戏根目录)",
            "isDirect": False,
            "installSteps": [
                "1. 点击下载 ScriptHookV_1.0.3179.0.zip；",
                "2. 打开 GTA 5 安装根目录 (包含 GTA5.exe 的文件夹)；",
                "3. 将 bin/ 目录下的 ScriptHookV.dll、dinput8.dll 和 NativeTrainer.asi 复制到根目录；",
                "4. 进入单机故事模式按 F4 呼出菜单。"
            ],
            "nexusUrl": "https://www.dev-c.com/gtav/scripthookv/",
            "version": "supports build 1.0.3889.0 / 1.0.1158.13 (current)"
        },
        {
            "id": "gta_menyoo_pc",
            "title": "Menyoo PC [SP]",
            "author": "MAFINS",
            "category": "Trainer / Menu",
            "desc": "单机离线功能菜单，可以刷出载具（含线上 DLC 载具）、自定义随从、搭建赛道障碍物，并更换剧情角色外观。",
            "dependencies": [
                "ScriptHookV"
            ],
            "installPath": "Grand Theft Auto V/",
            "isDirect": True,
            "installSteps": [
                "1. 确认已安装 ScriptHookV 前置；",
                "2. 下载压缩包解压获取 menyooStuff 文件夹和 Menyoo.asi；",
                "3. 放入 GTA5 游戏根目录；",
                "4. 故事模式下按 F8 打开图形化菜单。"
            ],
            "nexusUrl": "https://github.com/MAFINS/MenyooSP",
            "version": "v1.8.1",
            "downloadUrl": "https://github.com/MAFINS/MenyooSP/releases/download/v1.8.1/MenyooSP.zip",
            "downloadFilename": "MenyooSP.zip"
        },
        {
            "id": "gta_openiv",
            "title": "OpenIV",
            "author": "OpenIV Team",
            "category": "Mod Tool (工具软件)",
            "desc": "RPF 归档编辑工具，用于安装车辆、材质与音效类 Mod。提供 mods 文件夹机制，替换文件时不会修改游戏原始文件。",
            "dependencies": [
                "None (Stand-alone Tool)"
            ],
            "installPath": "Windows PC",
            "isDirect": False,
            "installSteps": [
                "1. 下载运行 OpenIVSetup.exe 安装工具；",
                "2. 打开 OpenIV 选择 Grand Theft Auto V (Windows)；",
                "3. 点击 Tools -> ASI Manager，全部点击 Install 安装 ASI 驱动；",
                "4. 后续模组放入 mods 文件夹生效，不会修改原始游戏文件。"
            ],
            "nexusUrl": "https://openiv.com",
            "version": "4.1"
        },
        {
            "id": "gta_nve_graphics",
            "title": "NaturalVision Evolved",
            "author": "Razed",
            "category": "Graphics (画面)",
            "desc": "画面重制类 Mod，调整洛圣都的天气、光照、水面反射与夜景效果。",
            "dependencies": [
                "OpenIV",
                "ScriptHookV"
            ],
            "installPath": "Grand Theft Auto V/mods/",
            "isDirect": False,
            "installSteps": [
                "1. 确保安装好 OpenIV 并启用了 ASI 扩展；",
                "2. 打开 OpenIV 点击 Tools -> Package Installer；",
                "3. 选中下载的 NVE_Installer.oiv 并安装到 'mods folder'；",
                "4. 启动游戏查看效果。"
            ],
            "nexusUrl": "https://www.razedmods.com/gta-v"
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 官方秘籍：无敌与通缉等级 (Invincibility & Wanted Level Cheats)",
            "commands": [
                {
                    "id": "gta_cheat_painkiller",
                    "name": {
                        "zh-CN": "无敌状态 5 分钟 (PAINKILLER)",
                        "en": "Invincibility for 5 Mins (PAINKILLER)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "PAINKILLER",
                    "desc": "官方秘籍代码，开启 5 分钟无敌状态，免疫爆炸、枪击和坠落造成的伤害。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_turtle",
                    "name": {
                        "zh-CN": "生命值与重型护甲瞬间补满 (TURTLE)",
                        "en": "Max Health & Armor (TURTLE)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "TURTLE",
                    "desc": "瞬间回满角色生命值与护甲至最高等级；如果人在载具中，车辆也会被修复。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gta.fandom.com/wiki/Cheats_in_GTA_V"
                },
                {
                    "id": "gta_cheat_lawyerup",
                    "name": {
                        "zh-CN": "降低并清除一星通缉度 (LAWYERUP)",
                        "en": "Lower Wanted Level (LAWYERUP)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "LAWYERUP",
                    "desc": "官方秘籍代码，每次输入可降低一颗通缉星级，连续输入可逐步清空通缉度。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_fugitive",
                    "name": {
                        "zh-CN": "提升一星通缉等级 (FUGITIVE)",
                        "en": "Raise Wanted Level (FUGITIVE)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "FUGITIVE",
                    "desc": "官方秘籍代码，每次输入为角色增加一颗通缉星，引来警方追捕。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_powerup",
                    "name": {
                        "zh-CN": "角色专属特异功能能量槽拉满 (POWERUP)",
                        "en": "Recharge Special Ability (POWERUP)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "POWERUP",
                    "desc": "瞬间充满黄色特殊技能槽，随心释放麦克致命射击时缓、小富过弯子弹时间与老崔狂暴减伤。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                }
            ]
        },
        {
            "category": "🔫 原生军火军备与特殊弹药 (Weapons, Ammo & Explosive Punches)",
            "commands": [
                {
                    "id": "gta_cheat_toolup",
                    "name": {
                        "zh-CN": "获取全部武器与弹药 (TOOLUP)",
                        "en": "All Weapons & Max Ammo (TOOLUP)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "TOOLUP",
                    "desc": "官方秘籍代码，给予游戏中全部武器及对应弹药。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_highex",
                    "name": {
                        "zh-CN": "开启爆炸子弹 (HIGHEX)",
                        "en": "Explosive Bullets (HIGHEX)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "HIGHEX",
                    "desc": "官方秘籍代码，子弹命中目标会产生爆炸，伤害范围更大。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_incendiary",
                    "name": {
                        "zh-CN": "开启燃烧子弹 (INCENDIARY)",
                        "en": "Flame Bullets (INCENDIARY)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "INCENDIARY",
                    "desc": "官方秘籍代码，子弹命中目标会引燃并造成持续燃烧伤害。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_hothands",
                    "name": {
                        "zh-CN": "近战攻击附带爆炸 (HOTHANDS)",
                        "en": "Explosive Melee Attacks (HOTHANDS)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "HOTHANDS",
                    "desc": "官方秘籍代码，近战攻击命中目标会产生爆炸效果。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_deadeye",
                    "name": {
                        "zh-CN": "瞄准慢动作四段调节 (DEADEYE)",
                        "en": "Aiming Slow Motion (DEADEYE)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "DEADEYE",
                    "desc": "官方秘籍代码，举枪瞄准时进入慢动作，最多可连续输入四次加深效果，第四次输入恢复正常速度。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                }
            ]
        },
        {
            "category": "🏎️ 豪车载具召唤与武装直升机 (Vehicle Spawner & Attack Helis)",
            "commands": [
                {
                    "id": "gta_cheat_comet",
                    "name": {
                        "zh-CN": "召唤彗星保时捷跑车 (COMET)",
                        "en": "Spawn Comet Sports Car (COMET)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "COMET",
                    "desc": "官方秘籍代码，在角色面前召唤一辆 Comet 跑车。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_rapidgt",
                    "name": {
                        "zh-CN": "召唤 Rapid GT 跑车 (RAPIDGT)",
                        "en": "Spawn Rapid GT Coupe (RAPIDGT)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "RAPIDGT",
                    "desc": "官方秘籍代码，在角色面前召唤一辆 Rapid GT 跑车。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_buzzoff",
                    "name": {
                        "zh-CN": "召唤秃鹰武装直升机 (BUZZOFF)",
                        "en": "Spawn Buzzard Attack Helicopter (BUZZOFF)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "BUZZOFF",
                    "desc": "官方秘籍代码，召唤一架秃鹰武装直升机（配备机枪与导弹）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_barnstorm",
                    "name": {
                        "zh-CN": "召唤麦拉德特技飞机 (BARNSTORM)",
                        "en": "Spawn Mallard Stunt Plane (BARNSTORM)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "BARNSTORM",
                    "desc": "官方秘籍代码，在角色面前召唤一架 Mallard 特技飞机。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.pcgamer.com/uk/gta-5-cheats/"
                },
                {
                    "id": "gta_cheat_bandit",
                    "name": {
                        "zh-CN": "召唤 BMX 自行车 (BANDIT)",
                        "en": "Spawn BMX Bicycle (BANDIT)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "BANDIT",
                    "desc": "官方秘籍代码，召唤一辆 BMX 自行车；并非越野泥地摩托车（Sanchez，对应代码是 OFFROAD）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                }
            ]
        },
        {
            "category": "🏃 角色移动能力与世界物理 (Jump, Speed & Physics)",
            "commands": [
                {
                    "id": "gta_cheat_hoptoit",
                    "name": {
                        "zh-CN": "开启超级跳跃 (HOPTOIT)",
                        "en": "Super Jump (HOPTOIT)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "HOPTOIT",
                    "desc": "官方秘籍代码，大幅提升角色跳跃高度。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_catchme",
                    "name": {
                        "zh-CN": "开启快速奔跑 (CATCHME)",
                        "en": "Fast Running (CATCHME)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "CATCHME",
                    "desc": "官方秘籍代码，大幅提升角色奔跑速度。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gta.fandom.com/wiki/Cheats_in_GTA_V"
                },
                {
                    "id": "gta_cheat_gotgills",
                    "name": {
                        "zh-CN": "开启快速游泳能力 (GOTGILLS)",
                        "en": "Fast Swimming Ability (GOTGILLS)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "GOTGILLS",
                    "desc": "官方秘籍代码，大幅提升角色游泳速度。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gta.fandom.com/wiki/Cheats_in_GTA_V"
                },
                {
                    "id": "gta_cheat_skydive",
                    "name": {
                        "zh-CN": "获取跳伞降落伞背包 (SKYDIVE)",
                        "en": "Give Parachute Backpack (SKYDIVE)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "SKYDIVE",
                    "desc": "官方秘籍代码，为角色装备一个降落伞。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gta.fandom.com/wiki/Cheats_in_GTA_V"
                },
                {
                    "id": "gta_cheat_skyfall",
                    "name": {
                        "zh-CN": "高空自由落体 (SKYFALL)",
                        "en": "Skyfall from High Altitude (SKYFALL)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "SKYFALL",
                    "desc": "官方秘籍代码，将角色传送到高空后进行无伞自由落体，建议配合无敌状态一起使用。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                }
            ]
        },
        {
            "category": "🌦️ 洛圣都天气、昼夜流速与慢动作 (Weather, Time Scale & Slomo)",
            "commands": [
                {
                    "id": "gta_cheat_makeitrain",
                    "name": {
                        "zh-CN": "切换天气 (MAKEITRAIN)",
                        "en": "Change Weather (MAKEITRAIN)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "MAKEITRAIN",
                    "desc": "官方秘籍代码，随机切换洛圣都当前的天气状况。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_snowday",
                    "name": {
                        "zh-CN": "开启罕见圣诞节暴风雪全城积雪 (SNOWDAY)",
                        "en": "Blizzard & Snow Ground (SNOWDAY)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "SNOWDAY",
                    "desc": "使地面变得湿滑，车辆失控打滑漂移；并不会改变天气或让地图真的下雪、被积雪覆盖。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gta.fandom.com/wiki/Cheats_in_GTA_V"
                },
                {
                    "id": "gta_cheat_slowmo",
                    "name": {
                        "zh-CN": "全局慢动作 (SLOWMO)",
                        "en": "Slow Motion World (SLOWMO)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "SLOWMO",
                    "desc": "将全局物理世界降速运行，每输入一次提升一层时缓倍率，第四次输入恢复正常标准流速。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_floater",
                    "name": {
                        "zh-CN": "月球微重力低引力环境 (FLOATER - 飞车滑翔)",
                        "en": "Moon Gravity Physics (FLOATER)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "FLOATER",
                    "desc": "将地球引力骤降为月球低重力，轻微擦碰即可让汽车漂浮翻滚如太空漫步般缓缓降落。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_trashed",
                    "name": {
                        "zh-CN": "召唤垃圾车 (TRASHED)",
                        "en": "Spawn Trashmaster Garbage Truck (TRASHED)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "TRASHED",
                    "desc": "官方秘籍代码，召唤一辆 Trashmaster 垃圾车；并非醉酒摇晃视角模式（真正的醉酒秘籍代码是 LIQUOR）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "gta_salvation_bundle",
            "type": "salvation",
            "name": "武装直升机追逐套装",
            "tag": "⚔️ 战斗与追逐向组合",
            "badge": "武装对抗",
            "desc": "召唤秃鹰武装直升机，开启高爆子弹 (HIGHEX) 和爆炸近战 (HOTHANDS)，并用两次 FUGITIVE 将通缉等级提高 2 星。",
            "highlights": ["召唤秃鹰武装直升机", "HIGHEX：子弹命中后产生爆炸", "HOTHANDS：近战攻击附带爆炸", "两次 FUGITIVE 提升 2 星通缉等级"],
            "code": "-- [老L·极客场景套餐] GTA5 六星狂暴大逃杀激战包\nBUZZOFF\nHIGHEX\nHOTHANDS\nFUGITIVE\nFUGITIVE"
        },
        {
            "id": "gta_godmode_bundle",
            "type": "godmode",
            "name": "高空跳跃漫游套装",
            "tag": "⚡ 探索向组合",
            "badge": "自由漫游",
            "desc": "传送到高空自由落体 (SKYFALL)，配合超级跳跃 (HOPTOIT)、月球重力 (FLOATER)、路面打滑 (SNOWDAY) 与 5 分钟无敌 (PAINKILLER) 一起使用，方便在洛圣都到处探索。",
            "highlights": [
                "SKYFALL：传送至高空后自由落体",
                "HOPTOIT：大幅提升跳跃高度",
                "FLOATER：切换为月球低重力",
                "SNOWDAY：路面变得湿滑打滑",
                "PAINKILLER：5 分钟无敌状态"
            ],
            "code": "-- [老L·极客场景套餐] GTA5 超自然空中飞仙终极漫游包\nSKYFALL\nHOPTOIT\nFLOATER\nSNOWDAY\nPAINKILLER"
        }
    ],
    "pitfallNote": {
        "title": "老L避坑笔记 (GTA 5 故事模式)",
        "tips": [
            "【进线上前】：Rockstar 的 GTA Online 对内存注入查得很严。进线上模式前，把游戏根目录的 dinput8.dll 改名为 dinput8.dll.bak（停掉 ASI 加载器），mods 文件夹、改过的 rpf 等其它改动也要移走；没有办法保证不被封号。",
            "【故事模式股票暴富机制】：麦克的莱斯特刺杀任务千万别提前做！等通关大结局‘联合储蓄’劫案拿到 2800 万初始本金后，再分批次接暗杀任务并全仓买入对应做空做多股票，本金可直接滚至 21 亿上限！",
            "【打不开 F4 菜单】：若按 F4 毫无反应，说明缺失 Visual C++ 2015~2022 运行库或 DirectX 组件。去微软官网重新安装 Visual C++ 运行库和 DirectX 后再试。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】GTA5 ASI 加载器开关\necho ========================================================\necho   【老L·单机避坑局】GTA5 ASI 加载器开关脚本\necho   把 dinput8.dll 改名为 dinput8.dll.bak 来停用，或改回来启用\necho ========================================================\necho.\nif not exist \"GTA5.exe\" (\n    echo [!] 当前目录下没有 GTA5.exe，脚本什么都没改。\n    echo     请把本脚本放到 Grand Theft Auto V 游戏安装根目录再运行。\n    echo.\n    pause\n    exit /b\n)\n\nset \"MODE=\"\nif exist \"dinput8.dll\" set \"MODE=on\"\nif not defined MODE if exist \"dinput8.dll.bak\" set \"MODE=off\"\nif not defined MODE (\n    echo [i] 没有 dinput8.dll，也没有 dinput8.dll.bak：没装 ASI 加载器，脚本什么都没改。\n    echo.\n    pause\n    exit /b\n)\n\nset \"choice=\"\nif \"%MODE%\"==\"on\" echo [当前状态] 有 dinput8.dll：ASI 加载器会加载 ScriptHookV 等插件，只能玩故事模式。\nif \"%MODE%\"==\"on\" set /p \"choice=把 dinput8.dll 改名为 dinput8.dll.bak、停用 ASI 加载器？输入 Y 确认: \"\nif \"%MODE%\"==\"off\" echo [当前状态] 只有 dinput8.dll.bak：ASI 加载器已停用。\nif \"%MODE%\"==\"off\" set /p \"choice=把 dinput8.dll.bak 改回 dinput8.dll、重新启用 ASI 加载器？输入 Y 确认: \"\n\nif /i not \"%choice%\"==\"Y\" (\n    echo [i] 没有输入 Y，脚本什么都没改。\n    echo.\n    pause\n    exit /b\n)\n\nif \"%MODE%\"==\"on\" ren \"dinput8.dll\" \"dinput8.dll.bak\"\nif \"%MODE%\"==\"off\" ren \"dinput8.dll.bak\" \"dinput8.dll\"\n\nif exist \"dinput8.dll\" (\n    echo [结果] 现在有 dinput8.dll：ASI 加载器会被加载，故事模式按 F4 试试菜单。\n) else (\n    echo [结果] 现在没有 dinput8.dll：ASI 加载器不会被加载。\n)\necho.\necho ========================================================\necho  [i] 这个脚本只改 dinput8.dll 这一个文件的名字。\necho      其它改过的文件（mods 文件夹、改过的 rpf 等）它不管；进 GTA Online 前要自己全部移走，有封号风险。\necho      脚本不备份存档，改之前先手动备份。\necho ========================================================\necho.\npause\n",
    "verifiedPatch": "v1.0.3179（未实测）",
    "radarSecretCode": "洛圣都"
}

print("✅ Rank 8~10 数据模块编译就绪！")

# ==============================================================================
# RANK 11: 荒野大镖客：救赎 2 (Red Dead Redemption 2)
# ==============================================================================
RDR2_DATA = {
    "rank": 11,
    "hasConsole": False,
    "consoleShortcut": "F5 (ScriptHookRDR2 原生离线修改器) 或 游戏内设置-作弊码",
    "consoleEnableGuide": {
        "zh-CN": "【单机故事模式指南】\n1. 官方秘籍输入：进入故事模式 -> 按 Esc 暂停 -> 选择【设置 (Settings)】-> 按左下角【作弊 (Cheats)】或 Shift 键 -> 输入对应英文短语并回车保存；\n2. ScriptHookRDR2 离线内置菜单：将 ScriptHookRDR2.dll、dinput8.dll 以及 NativeTrainer.asi 解压至游戏根目录；\n3. 启动故事模式按 F5 键唤出图形修改菜单，小键盘 8/2/4/6 控制，5 确认，0 返回；\n4. ⚠️ 别带着 Mod 进 RDO 线上模式，有封号风险。把 dinput8.dll 改名为 .bak 只是停掉 ASI 加载器，其它改过的文件要自己移走。",
        "en": "Enter official cheat phrases in Settings -> Cheats, or press F5 with ScriptHookRDR2 in offline story mode."
    },
    "popularCommands": [
        "You want freedom",
        "You flourish before you die",
        "Seek all the bounty of this place",
        "Greed is American virtue",

    ],
    "hasMods": True,
    "curatedMods": [
        {
            "id": "rdr2_scripthook",
            "title": "Script Hook RDR2",
            "author": "Alexander Blade",
            "category": "Core Framework (核心前置)",
            "desc": "荒野大镖客2运行任何 ASI 模组、刷车刷马工具与离线菜单的核心前置（第三方工具，不是官方的）。只在故事模式用，进线上前把它移走。",
            "dependencies": [
                "None (Native DLL)"
            ],
            "installPath": "Red Dead Redemption 2/ (游戏根目录)",
            "isDirect": False,
            "installSteps": [
                "1. 点击下载 ScriptHookRDR2_1.0.1491.17.zip 压缩包；",
                "2. 打开 RDR2 游戏安装根目录 (包含 RDR2.exe 的目录)；",
                "3. 将压缩包内 bin/ 目录下的 ScriptHookRDR2.dll、dinput8.dll 以及 NativeTrainer.asi 复制进去；",
                "4. 故事模式按 F5 即可呼出全功能菜单。"
            ],
            "nexusUrl": "https://www.dev-c.com/rdr2/scripthookrdr2/",
            "version": "1.0.1491.17"
        },
        {
            "id": "rdr2_rampage_trainer",
            "title": "Rampage Trainer",
            "author": "RampageDev",
            "category": "Trainer / Menu",
            "desc": "单机离线功能菜单，提供召唤马匹、变身、更换装扮、营地管理与传送地图等功能。",
            "dependencies": [
                "ScriptHookRDR2"
            ],
            "installPath": "Red Dead Redemption 2/",
            "isDirect": False,
            "installSteps": [
                "1. 确保已安装 ScriptHookRDR2；",
                "2. 下载压缩包解压出 Rampage.asi 和 RampageFiles 文件夹；",
                "3. 放入 RDR2 根目录；",
                "4. 在故事模式下按 F5 打开菜单。"
            ],
            "nexusUrl": "https://www.nexusmods.com/reddeadredemption2/mods/233",
            "version": "1.6.9",
            "downloads": "3.8M",
            "endorsements": "62.7K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "rdr2_lml",
            "title": "Lenny's Mod Loader RDR",
            "author": "LMS",
            "category": "Mod Manager",
            "desc": "RPF 模组加载工具，新增的服饰、贴图与音效类模组放入 lml/ 文件夹就能生效，不需要手动解包替换游戏原始文件。",
            "dependencies": [
                "ScriptHookRDR2"
            ],
            "installPath": "Red Dead Redemption 2/",
            "isDirect": False,
            "installSteps": [
                "1. 解压 ModLoader 文件夹内全部文件至 RDR2 根目录；",
                "2. 根目录会自动生成 lml/ 文件夹；",
                "3. 后续下载的服饰与材质 mod 放入 lml/ 文件夹。"
            ],
            "nexusUrl": "https://www.rdr2mods.com/downloads/rdr2/tools/76-lennys-mod-loader-rdr/",
            "version": "0.6.8470.31280"
        },
        {
            "id": "rdr2_whyems_dlc",
            "title": "WhyEm's  DLC",
            "author": "WhyEm",
            "category": "Clothing & Customization",
            "desc": "服饰拓展包，新增 2500 多件服装与配饰，包括皮衣、外套与腰带等。",
            "dependencies": [
                "ScriptHookRDR2",
                "Lenny's Mod Loader"
            ],
            "installPath": "Red Dead Redemption 2/lml/",
            "isDirect": False,
            "installSteps": [
                "1. 确认已正确安装 LML 模组加载器；",
                "2. 下载压缩包解压获取 WhyEm's DLC 文件夹；",
                "3. 放入 RDR2/lml/ 文件夹内；",
                "4. 前往捕兽人或裁缝铺购买新增的服饰。"
            ],
            "nexusUrl": "https://www.nexusmods.com/reddeadredemption2/mods/671",
            "version": "Final",
            "downloads": "1.7M",
            "endorsements": "29.4K",
            "checkedAt": "2026-11-20"
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 核心秘籍合集 (Core Cheats)",
            "commands": [
                {
                    "id": "rdr_cheat_freedom",
                    "name": {
                        "zh-CN": "降低通缉等级 (You want freedom)",
                        "en": "Lower Wanted Level (You want freedom)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "You want freedom",
                    "desc": "官方秘籍短语，降低亚瑟当前的通缉星级。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.shacknews.com/article/108219/full-cheat-codes-list-in-red-dead-redemption-2"
                },
                {
                    "id": "rdr_cheat_flourish",
                    "name": {
                        "zh-CN": "三核心瞬间回满 (You flourish before you die)",
                        "en": "Refill All Bars (You flourish before you die)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "You flourish before you die",
                    "desc": "官方秘籍短语，立即回满生命、体力与死神之眼三项状态槽。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.shacknews.com/article/108219/full-cheat-codes-list-in-red-dead-redemption-2"
                },
                {
                    "id": "rdr_cheat_deadeye",
                    "name": {
                        "zh-CN": "无限死神之眼 (Be greedy only for foresight)",
                        "en": "Infinite Dead Eye"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Be greedy only for foresight",
                    "desc": "官方秘籍短语，死神之眼子弹时间效果不再消耗，可持续使用。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.powerpyx.com/red-dead-redemption-2-cheats/"
                },
                {
                    "id": "rdr_cheat_stealth",
                    "name": {
                        "zh-CN": "解锁潜行武器 (Death is silence)",
                        "en": "Stealth Weapons (Death is silence)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Death is silence",
                    "desc": "官方秘籍短语，解锁一套潜行武器：弓、火瓶、飞斧、飞刀与砍刀。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.powerpyx.com/red-dead-redemption-2-cheats/"
                }
            ]
        },
        {
            "category": "💰 现金 (Money)",
            "commands": [
                {
                    "id": "rdr_cheat_greed",
                    "name": {
                        "zh-CN": "获取 $500 现金 (Greed is now a virtue)",
                        "en": "Give $500 Cash (Greed is now a virtue)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Greed is now a virtue",
                    "desc": "官方原生秘籍代码，亚瑟钱包直接入账 500 美元纸钞，可连续多次输入叠加。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.powerpyx.com/red-dead-redemption-2-cheats/"
                }
            ]
        },
        {
            "category": "🐎 马匹默契度 (Horse Bonding)",
            "commands": [
                {
                    "id": "rdr_cheat_kingdom_horse",
                    "name": {
                        "zh-CN": "提升马匹默契度 (My kingdom is a horse)",
                        "en": "Increase Horse Bonding"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "My kingdom is a horse",
                    "desc": "官方原生秘籍代码，立即提升所有坐骑的默契等级，默契等级越高可解锁更多骑术动作。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.pcgamesn.com/red-dead-redemption-2/rdr2-cheats-pc"
                }
            ]
        },
        {
            "category": "🔫 武器套装与弹药 (Weapon Sets & Ammo)",
            "commands": [
                {
                    "id": "rdr_cheat_simple_life",
                    "name": {
                        "zh-CN": "获取全套基础西部武器库 (A simple life, a beautiful death)",
                        "en": "Basic Weapons Arsenal"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "A simple life, a beautiful death",
                    "desc": "官方秘籍短语，获得基础武器：卡特曼左轮手枪、兰开斯特连发枪与春田步枪（并非双管霰弹枪）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.pcgamesn.com/red-dead-redemption-2/rdr2-cheats-pc"
                },
                {
                    "id": "rdr_cheat_history_fools",
                    "name": {
                        "zh-CN": "解锁神枪手武器 (History is written by fools)",
                        "en": "Gunslinger Weapons (History is written by fools)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "History is written by fools",
                    "desc": "官方秘籍短语，解锁 Schofield 左轮手枪、双动左轮手枪与双管霰弹枪。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.pcgamesn.com/red-dead-redemption-2/rdr2-cheats-pc"
                },
                {
                    "id": "rdr_cheat_abundance",
                    "name": {
                        "zh-CN": "无限弹药储备补给 (Abundance is the dullest desire)",
                        "en": "Infinite Ammo Supply"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Abundance is the dullest desire",
                    "desc": "官方秘籍短语，子弹数量变为无限，不会再减少。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.shacknews.com/article/108219/full-cheat-codes-list-in-red-dead-redemption-2"
                }
            ]
        },
        {
            "category": "⭐ 荣誉值与通缉等级 (Honor & Wanted Level)",
            "commands": [
                {
                    "id": "rdr_cheat_virtue",
                    "name": {
                        "zh-CN": "提升荣誉值至最高 (Virtue unearned is not virtue)",
                        "en": "Max Honor Level (Virtue unearned is not virtue)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Virtue unearned is not virtue",
                    "desc": "官方原生秘籍代码，立即将荣誉值提升至最高等级。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.powerpyx.com/red-dead-redemption-2-cheats/"
                },
                {
                    "id": "rdr_cheat_punishment",
                    "name": {
                        "zh-CN": "提升通缉等级 (You want punishment)",
                        "en": "Increase Wanted Level (You want punishment)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "You want punishment",
                    "desc": "官方秘籍短语，立即提升当前通缉等级。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.shacknews.com/article/108219/full-cheat-codes-list-in-red-dead-redemption-2"
                }
            ]
        }
    ],
    "scenarioBundles": [],
    "pitfallNote": {
        "title": "老L避坑笔记 (荒野大镖客2 故事模式)",
        "tips": [
            "【进线上前】：R星对 RDO 线上模式同样严查。进线上战局前，把游戏根目录的 dinput8.dll 改名为 dinput8.dll.bak（停掉 ASI 加载器），其它改过的文件也要移走；没有办法保证不被封号。",
            "【捕猎毛皮品质保护】：想要获得三星完美毛皮，务必击杀头上本来就是三星的动物，并掏出春田步枪击中头部一击毙命；若嫌繁琐，直接使用本库一键添加全部三星皮！",
            "【作弊码保存限制】：在官方设置里激活作弊码后，系统会默认暂时禁止保存新存档。若需保存修改后的金钱与装备，请使用 ScriptHookRDR2 或风灵月影修改器，它们不会禁用存档功能！"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】荒野大镖客2 ASI 加载器开关\necho ========================================================\necho   【老L·单机避坑局】荒野大镖客2 ASI 加载器开关脚本\necho   把 dinput8.dll 改名为 dinput8.dll.bak 来停用，或改回来启用\necho ========================================================\necho.\nif not exist \"RDR2.exe\" (\n    echo [!] 当前目录下没有 RDR2.exe，脚本什么都没改。\n    echo     请把本脚本放到 Red Dead Redemption 2 游戏安装根目录再运行。\n    echo.\n    pause\n    exit /b\n)\n\nset \"MODE=\"\nif exist \"dinput8.dll\" set \"MODE=on\"\nif not defined MODE if exist \"dinput8.dll.bak\" set \"MODE=off\"\nif not defined MODE (\n    echo [i] 没有 dinput8.dll，也没有 dinput8.dll.bak：没装 ASI 加载器，脚本什么都没改。\n    echo.\n    pause\n    exit /b\n)\n\nset \"choice=\"\nif \"%MODE%\"==\"on\" echo [当前状态] 有 dinput8.dll：ASI 加载器会加载 ScriptHookRDR2 等插件，只能玩故事模式。\nif \"%MODE%\"==\"on\" set /p \"choice=把 dinput8.dll 改名为 dinput8.dll.bak、停用 ASI 加载器？输入 Y 确认: \"\nif \"%MODE%\"==\"off\" echo [当前状态] 只有 dinput8.dll.bak：ASI 加载器已停用。\nif \"%MODE%\"==\"off\" set /p \"choice=把 dinput8.dll.bak 改回 dinput8.dll、重新启用 ASI 加载器？输入 Y 确认: \"\n\nif /i not \"%choice%\"==\"Y\" (\n    echo [i] 没有输入 Y，脚本什么都没改。\n    echo.\n    pause\n    exit /b\n)\n\nif \"%MODE%\"==\"on\" ren \"dinput8.dll\" \"dinput8.dll.bak\"\nif \"%MODE%\"==\"off\" ren \"dinput8.dll.bak\" \"dinput8.dll\"\n\nif exist \"dinput8.dll\" (\n    echo [结果] 现在有 dinput8.dll：ASI 加载器会被加载，故事模式按 F5 试试菜单。\n) else (\n    echo [结果] 现在没有 dinput8.dll：ASI 加载器不会被加载。\n)\necho.\necho ========================================================\necho  [i] 这个脚本只改 dinput8.dll 这一个文件的名字。\necho      其它改过的文件它不管；进 RDO 线上模式前要自己全部移走，有封号风险。\necho      脚本不备份存档，改之前先手动备份。\necho ========================================================\necho.\npause\n",
    "verifiedPatch": "v1.0.1491（未实测）",
    "radarSecretCode": "大表哥"
}

# ==============================================================================
# RANK 12: 怪物猎人：世界 (Monster Hunter: World)
# ==============================================================================
MHW_DATA = {
    "rank": 12,
    "hasConsole": False,
    "consoleShortcut": "Insert 唤出 REFramework 覆盖菜单 / F10 调出调试控制台",
    "consoleEnableGuide": {
        "zh-CN": "【怪物猎人世界 纯净模组与控制台指南】\n1. 下载 Stracker's Loader (包含 dinput8.dll 与 loader-config.json) 解压至游戏根目录 (Monster Hunter World/)；\n2. 将 REFramework 或 All Items in Shop 模组解压放入 nativePC/ 对应目录；\n3. 启动游戏，按键盘 Insert 键即可在屏幕左上角唤出 REFramework 菜单；\n4. 支持全珠子全素材一键补齐、聚魔之地等级随心调节与伤害血量实时透视！",
        "en": "Install Stracker's Loader into MHW root. Press Insert to open REFramework menu for decorations, materials, and SmartHunter overlay."
    },
    "popularCommands": [],
    "hasMods": True,
    "curatedMods": [
        {
            "id": "mhw_strackers_loader",
            "title": "Stracker's Loader",
            "author": "Stracker",
            "category": "Core Framework (核心前置)",
            "desc": "怪物猎人世界：冰原运行 nativePC 外部模组、商店补全插件与透视覆层类 Mod 所需的前置加载库，包含 CRC 校验绕过修复。",
            "dependencies": [
                "None (Native DLL)"
            ],
            "installPath": "Monster Hunter World/ (游戏根目录)",
            "isDirect": False,
            "installSteps": [
                "1. 点击下载 StrackersLoader_v1.12.zip 压缩包；",
                "2. 打开 Monster Hunter World 游戏安装根目录；",
                "3. 将解压出的 dinput8.dll、dtdata.dll 等文件放入根目录；",
                "4. 启动游戏即可正常加载 nativePC 下的所有 Mod。"
            ],
            "nexusUrl": "https://www.nexusmods.com/monsterhunterworld/mods/1982",
            "version": "3.0.1",
            "downloads": "6.2M",
            "endorsements": "114.0K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "mhw_all_items_shop",
            "title": "Large Shop Assortment for Consumables and Combo Mats (Iceborne)",
            "author": "MHVuze",
            "category": "Economy / Items",
            "desc": "将月辰与星辰基地的道具商店物资替换：所有 4 级装饰品（珠子）、古龙大宝玉、聚魔之地专属材料全部上架，统一标价 1 铜币。",
            "dependencies": [
                "Stracker's Loader"
            ],
            "installPath": "Monster Hunter World/nativePC/common/facility/",
            "isDirect": False,
            "installSteps": [
                "1. 确认已安装 Stracker's Loader 前置；",
                "2. 下载压缩包解压获取 nativePC 文件夹；",
                "3. 直接合并覆盖到游戏根目录下；",
                "4. 到道具屋阿姨处对话即可购买珠子与素材。"
            ],
            "nexusUrl": "https://www.nexusmods.com/monsterhunterworld/mods/1959",
            "version": "1.02",
            "downloads": "36.1K",
            "endorsements": "1.8K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "mhw_smart_hunter",
            "title": "SmartHunter",
            "author": "r00telement",
            "category": "UI / Overlay",
            "desc": "在屏幕上方悬浮显示怪物总血量、当前血量百分比、激怒倒计时、麻痹/睡眠积蓄值，以及队伍四人的输出 DPS 占比统计。",
            "dependencies": [
                "None (Stand-alone Memory Overlay)"
            ],
            "installPath": "Windows PC",
            "isDirect": False,
            "installSteps": [
                "1. 下载解压 SmartHunter 压缩包至任意文件夹；",
                "2. 启动怪猎世界并进入猎场；",
                "3. 双击运行 SmartHunter.exe，悬浮窗将自动对齐游戏画面显示。"
            ],
            "nexusUrl": "https://github.com/r00telement/SmartHunter"
        },
        {
            "id": "mhw_perf_booster",
            "title": "Performance Booster and Plugin Extender",
            "author": "AsteriskAmpersand and Moonbunnie",
            "category": "Performance (性能加速)",
            "desc": "移除游戏里大量未优化、与游戏功能无关的代码来提升性能，CPU 受限的电脑上效果更明显；也让一些更复杂的插件能正常运行。效果因电脑而异，本站没有测过具体帧数。",
            "dependencies": [
                "Stracker's Loader"
            ],
            "installPath": "Monster Hunter World/nativePC/plugins/",
            "isDirect": False,
            "installSteps": [
                "1. 下载压缩包解压出 .dll 插件；",
                "2. 放入 nativePC/plugins/ 目录；",
                "3. 启动游戏查看帧率变化（效果因电脑而异）。"
            ],
            "nexusUrl": "https://www.nexusmods.com/monsterhunterworld/mods/3473",
            "version": "1.3",
            "downloads": "3.2M",
            "endorsements": "78.7K",
            "checkedAt": "2026-11-20"
        }
    ],
    "consoleCategories": [],
    "scenarioBundles": [],
    "pitfallNote": {
        "title": "老L避坑笔记 (怪物猎人世界 冰原终极避坑指南)",
        "tips": [
            "【联机防踢与尊重原则】：卡普空对单机与好友自建私人房间使用 Mod 比较宽松，但没有人能担保不封号。但在加入路人公开救援时，请务必关闭【一击必杀】与【锁血】，使用 SmartHunter 纯净显示血量即可，切勿破坏其他真实玩家的狩猎乐趣！",
            "【黑屏无限加载急救】：安装模组后游戏无法启动或黑屏卡死，99% 是由于游戏大更新后 Stracker's Loader 未更新或 nativePC 遗留了过期前置。删除游戏根目录的 dinput8.dll 即可瞬间恢复正常启动！",
            "【CPU 100% 掉帧发热排查】：冰原自带的反作弊线程存在内存死循环 Bug。请务必安装本站推荐的 Performance Booster 补丁，直接禁用该死循环，显卡性能完全释放。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】怪猎世界 Mod 目录检查\necho ========================================================\necho   【老L·单机避坑局】怪物猎人世界 Mod 目录检查脚本\necho   检查 dinput8.dll 在不在；没有 nativePC 目录就新建一个\necho ========================================================\necho.\nif not exist \"MonsterHunterWorld.exe\" (\n    echo [!] 当前目录下没有 MonsterHunterWorld.exe，脚本什么都没改。\n    echo     请把本脚本放到 Monster Hunter World 游戏安装根目录再运行。\n    echo.\n    pause\n    exit /b\n)\nif exist \"dinput8.dll\" (\n    echo [+] 找到 dinput8.dll：Stracker's Loader 用的就是这个文件名。只检查了文件在不在。\n) else (\n    echo [!] 没找到 dinput8.dll，依赖 Stracker's Loader 的 Mod 可能加载不了。\n)\nif not exist \"nativePC\" (\n    mkdir nativePC\n    echo [+] 已新建 nativePC 目录。\n) else (\n    echo [i] nativePC 目录已经有了，没有改动。\n)\necho [i] 脚本不备份存档，装 Mod 前先手动备份。\necho.\npause\n",
    "verifiedPatch": "v15.11（未实测）",
    "radarSecretCode": "苍蓝星"
}

# ==============================================================================
# RANK 13: 只狼：影逝二度 (Sekiro: Shadows Die Twice)
# ==============================================================================
SEKIRO_DATA = {
    "rank": 13,
    "hasConsole": False,
    "consoleShortcut": "ModEngine 挂钩引导 + 小键盘热键 / 慢动作防御弹刀辅助",
    "consoleEnableGuide": {
        "zh-CN": "【只狼 纯净模组与弹刀防反教学指南】\n1. 安装 ModEngine：将 dinput8.dll 与 modengine.ini 放入只狼游戏根目录 (与 sekiro.exe 同目录)；\n2. 新建 mods/ 文件夹，将下载的角色时装、材质与招式 Mod 放入该目录；\n3. 只狼没有 EAC 反作弊，也没有联机模式；\n4. 开启 F1 键可进入 0.3x 防御完美弹刀子弹时间，轻松看破任何 Boss 的连续乱舞招式！",
        "en": "Install ModEngine into Sekiro root. Press F1 for 0.3x parry window bullet time and hotkeys for infinite spirit emblems."
    },
    "popularCommands": [],
    "hasMods": True,
    "curatedMods": [
        {
            "id": "sekiro_mod_engine",
            "title": "ModEngine",
            "author": "Katalash",
            "category": "Core Framework (核心前置)",
            "desc": "用于加载外部材质、动作替换与参数修改类 Mod 的前置框架，通过拦截文件加载路径实现，不修改游戏原始文件。",
            "dependencies": [
                "None (Native DLL)"
            ],
            "installPath": "Sekiro/ (游戏根目录)",
            "isDirect": False,
            "installSteps": [
                "1. 点击下载 ModEngine 压缩包；",
                "2. 将 dinput8.dll 和 modengine.ini 解压至只狼游戏根目录 (sekiro.exe 同目录)；",
                "3. 在根目录新建 mods/ 文件夹；",
                "4. 后续所有 Mod 放入 mods/ 即可自动生效。"
            ],
            "nexusUrl": "https://github.com/katalash/ModEngine"
        },
        {
            "id": "sekiro_fps_unlock",
            "title": "Sekiro FPS Unlock and More",
            "author": "uberhalit",
            "category": "Performance / Graphics",
            "desc": "解除官方 60 帧的帧率限制，支持 144Hz/240Hz 高刷新率显示器，并支持 21:9 带鱼屏分辨率与无边框窗口模式。",
            "dependencies": [
                "None (Stand-alone Tool)"
            ],
            "installPath": "Windows PC",
            "isDirect": True,
            "installSteps": [
                "1. 下载解压获取 SekiroFpsUnlockAndMore.exe；",
                "2. 先启动只狼游戏，然后运行该工具；",
                "3. 勾选 'Unlock FPS' 并将上限滑块调整为 144 或 240。"
            ],
            "nexusUrl": "https://github.com/uberhalit/SekiroFpsUnlockAndMore",
            "version": "1.2.5.2",
            "downloadUrl": "https://github.com/uberhalit/SekiroFpsUnlockAndMore/releases/download/1.2.5.2/SekiroFpsUnlockAndMore_v1.2.5.2.exe",
            "downloadFilename": "SekiroFpsUnlockAndMore_v1.2.5.2.exe"
        },
        {
            "id": "sekiro_boss_rush",
            "title": "Boss Rush",
            "author": "thefifthmatt",
            "category": "Gameplay / Training",
            "desc": "在鬼佛处开启 Boss 与精英怪的独立连战挑战，无需重新跑图或触发剧情，可直接挑战剑圣苇名一心、义父与怨恨之鬼等首领。",
            "dependencies": [
                "Sekiro Mod Engine"
            ],
            "installPath": "Sekiro/mods/",
            "isDirect": False,
            "installSteps": [
                "1. 确认已安装 Mod Engine；",
                "2. 下载压缩包解压放入 Sekiro/mods/ 目录；",
                "3. 在鬼佛菜单选择 'Boss Rush' 即可挑选中意首领切磋。"
            ],
            "nexusUrl": "https://www.nexusmods.com/sekiro/mods/429",
            "version": "v0.2",
            "downloads": "97.1K",
            "endorsements": "3.4K",
            "checkedAt": "2026-11-20"
        },
        {
            "id": "sekiro_resurrection",
            "title": "Sekiro Resurrection",
            "author": "Ionian",
            "category": "Complete Overhaul (全面大修)",
            "desc": "战斗系统大修 Mod，重做了大部分 Boss 与杂兵的招式逻辑，为狼新增了新的招式与追击派生，并调整了打刀防反的手感。",
            "dependencies": [
                "Sekiro Mod Engine"
            ],
            "installPath": "Sekiro/mods/",
            "isDirect": False,
            "installSteps": [
                "1. 必须使用全新纯净存档游玩；",
                "2. 下载解压获取文件夹放入 Sekiro/mods/；",
                "3. 开启游戏体验完全重生的苇名国战国死斗。"
            ],
            "nexusUrl": "https://www.nexusmods.com/sekiro/mods/723",
            "version": "1.16.1",
            "downloads": "343.1K",
            "endorsements": "7.8K",
            "checkedAt": "2026-11-20"
        }
    ],
    "consoleCategories": [],
    "scenarioBundles": [],
    "pitfallNote": {
        "title": "老L避坑笔记 (只狼：影逝二度 极客避坑指南)",
        "tips": [
            "【完全单机】：只狼没有 EAC 反作弊，也没有联机和入侵，不存在联机封号的问题。修改器和 ModEngine 是第三方工具，用之前先备份存档。",
            "【龙咳机制真相破除】：很多新手害怕因多次死亡导致 NPC【龙咳】而心惊胆战。实际上龙咳只会暂时挂起支线对话，绝对不会造成任何 NPC 死亡！只要用一滴【龙胤之露】在鬼佛处祷告，即可瞬间痊愈全苇名国所有人的龙咳，完全不必有心理压力！",
            "【弹刀时机与按键节奏】：频繁狂按防御键 L1 会被系统判定为狂躁按键，弹刀判定窗口会从正常的 0.5 秒骤降至 0.1 秒！使用本站推荐的 0.3x 子弹时间慢动作，看准刀刃即将接触的瞬间单次按压，才能培养出最地道的节奏肌肉记忆。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】只狼 ModEngine 目录检查\necho ========================================================\necho   【老L·单机避坑局】只狼 ModEngine 目录检查脚本\necho   检查 dinput8.dll 在不在；没有 mods 目录就新建一个\necho ========================================================\necho.\nif not exist \"sekiro.exe\" (\n    echo [!] 当前目录下没有 sekiro.exe，脚本什么都没改。\n    echo     请把本脚本放到 Sekiro 游戏安装根目录再运行。\n    echo.\n    pause\n    exit /b\n)\nif exist \"dinput8.dll\" (\n    echo [+] 找到 dinput8.dll：ModEngine 用的就是这个文件名。只检查了文件在不在。\n) else (\n    echo [!] 没找到 dinput8.dll，请把 ModEngine 解压到游戏根目录。\n)\nif not exist \"mods\" (\n    mkdir mods\n    echo [+] 已新建 mods 目录。\n) else (\n    echo [i] mods 目录已经有了，没有改动。\n)\necho [i] 脚本不备份存档，装 Mod 前先手动备份。\necho.\npause\n",
    "verifiedPatch": "v1.06（未实测）",
    "radarSecretCode": "只狼"
}

# ==============================================================================
# RANK 14: 生化危机4：重制版 (Resident Evil 4 Remake)
# ==============================================================================
RE4_DATA = {
    "rank": 14,
    "hasConsole": False,
    "consoleShortcut": "Insert 键呼出 REFramework 图形化 ImGui 菜单 / 自由运镜摄影",
    "consoleEnableGuide": {
        "zh-CN": "【生化危机4重制版 REFramework 控制台指南】\n1. 下载 REFramework for RE4 (praydog 核心库，含 dinput8.dll)；\n2. 解压缩并将 dinput8.dll 放入游戏根目录 (包含 re4.exe 的目录)；\n3. 启动游戏，在任何过场动画或战斗中按键盘 Insert 键唤出 ImGui 控制台面板；\n4. 支持全公文包武器解锁、无敌锁血、无限火箭筒调出、佣兵无限连击与第一人称/宽 FOV 视场角调节！",
        "en": "Install REFramework (dinput8.dll) into RE4 Remake root. Press Insert to toggle ImGui console for weapons, infinite ammo, and Mercenaries S++ rank."
    },
    "popularCommands": [],
    "hasMods": True,
    "curatedMods": [
        {
            "id": "re4_reframework",
            "title": "REFramework",
            "author": "praydog",
            "category": "Core Framework (核心前置)",
            "desc": "卡普空 RE 引擎游戏的通用 Mod 框架，提供 ImGui 覆层控制面板、自由视角摄像机、第一人称视角切换与 FOV 调整功能。",
            "dependencies": [
                "None (Native DLL)"
            ],
            "installPath": "Resident Evil 4 Remake/ (游戏根目录)",
            "isDirect": True,
            "installSteps": [
                "1. 点击下载 REFramework_RE4.zip 压缩包；",
                "2. 打开游戏安装根目录 (包含 re4.exe 的目录)；",
                "3. 将压缩包内的 dinput8.dll 直接解压到该目录；",
                "4. 启动游戏，按键盘 Insert 键即可打开/隐藏图形控制台。"
            ],
            "nexusUrl": "https://github.com/praydog/REFramework",
            "version": "v1.5.8",
            "downloadUrl": "https://github.com/praydog/REFramework/releases/download/v1.5.8/RE4.zip",
            "downloadFilename": "RE4.zip"
        },
        {
            "id": "re4_fluffy_manager",
            "title": "Fluffy Manager 5000 (Fluffy Mod Manager)",
            "author": "FluffyQuack",
            "category": "Mod Manager",
            "desc": "生化危机系列的模组管理工具，用于安装、启用或禁用角色外观、艾达王特工服、发型与武器贴图替换类 Mod。",
            "dependencies": [
                "None (Stand-alone Tool)"
            ],
            "installPath": "Windows PC",
            "isDirect": False,
            "installSteps": [
                "1. 下载解压运行 Modmanager.exe；",
                "2. 在游戏列表选择 'Resident Evil 4 Remake'；",
                "3. 将下载的 .rar/.zip 角色外观模组拖入软件窗口；",
                "4. 点击滑块勾选即可启用对应 Mod。"
            ],
            "nexusUrl": "https://www.fluffyquack.com"
        },

    ],
    "consoleCategories": [],
    "scenarioBundles": [],
    "pitfallNote": {
        "title": "老L避坑笔记 (生化危机4：重制版 专家避坑指南)",
        "tips": [
            "【专业难度 S+ 评价核心机制】：想要拿到专业 S+ 评价解锁猫耳（全武器无限弹药），必须在新游戏开局、游戏时间在 5 小时 30 分钟以内且【全流程保存存档次数不超过 15 次】！在进入城堡前尽量将存档留在巨人与双电锯前，避免坏档！",
            "【碍事梨防扛绝技】：到了城堡拿到阿什莉骑士铠甲后，请务必在附加内容菜单中为阿什莉换上！换上后所有邪教徒企图抱起她时都会被压趴在地上，直接永久解除护送后顾之忧！",
            "【晕 3D 与视场角调整】：本作第一人称举枪时默认后背拉得很近，导致不少玩家剧烈恶心。安装本站推荐的 REFramework 与 No Zoom On Aim 补丁，即可将 FOV 拉远至 95 度，视野舒畅开阔。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】生化危机4重制版 REFramework 检查\necho ========================================================\necho   【老L·单机避坑局】生化危机4重制版 REFramework 检查脚本\necho   只检查 dinput8.dll 在不在，不改任何文件\necho ========================================================\necho.\nif not exist \"re4.exe\" (\n    echo [!] 当前目录下没有 re4.exe，脚本什么都没改。\n    echo     请把本脚本放到 Resident Evil 4 Remake 游戏安装根目录再运行。\n    echo.\n    pause\n    exit /b\n)\nif exist \"dinput8.dll\" (\n    echo [+] 找到 dinput8.dll：REFramework 用的就是这个文件名。只检查了文件在不在。\n    echo [i] 游戏内按 Insert 键试试 REFramework 菜单。\n) else (\n    echo [!] 没找到 dinput8.dll，请把 REFramework 解压到游戏根目录。\n)\necho [i] 脚本不备份存档，装 Mod 前先手动备份。\necho.\npause\n",
    "verifiedPatch": "v1.0+（未实测）",
    "radarSecretCode": "生化4"
}


OWNED_FIELDS = (
    "rank", "verifiedPatch", "radarSecretCode", "hasConsole", "consoleShortcut", "consoleEnableGuide",
    "consoleCategories", "popularCommands", "hasMods", "curatedMods", "pitfallNote", "scenarioBundles", "batScript",
)

TIER2_MAP = {
    "palworld": PALWORLD_DATA,
    "starfield": STARFIELD_DATA,
    "gta-v": GTA5_DATA,
    "rdr2": RDR2_DATA,
    "monster-hunter-world": MHW_DATA,
    "sekiro": SEKIRO_DATA,
    "re4-remake": RE4_DATA,
    "resident-evil-4": RE4_DATA,
}

# Sekiro / RE4 Remake take ranks 13 / 14; Subnautica / Valheim move to 19 / 21.
RANK_MOVES = (("sekiro", "subnautica", 13, 19), (("re4-remake", "resident-evil-4"), "valheim", 14, 21))


def build_updates(games):
    by_id = {g["id"]: g for g in games}
    updates = {}

    for first, second, first_rank, second_rank in RANK_MOVES:
        first_ids = first if isinstance(first, tuple) else (first,)
        first_id = next((gid for gid in first_ids if gid in by_id), None)
        if first_id and second in by_id:
            updates.setdefault(first_id, {})["rank"] = first_rank
            updates.setdefault(second, {})["rank"] = second_rank

    for gid, data in TIER2_MAP.items():
        if gid in by_id:
            updates.setdefault(gid, {}).update(data)

    return updates


if __name__ == "__main__":
    write_owned_fields("enrich_rank8_14_tier2.py", OWNED_FIELDS, build_updates)
