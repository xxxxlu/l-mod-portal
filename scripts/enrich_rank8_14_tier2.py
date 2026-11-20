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
            "desc": "幻兽帕鲁运行全部 Lua 模组、UI 扩展与控制台打字命令的绝对核心前置库，极客必备。",
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
            "category": "Core Framework (核心前置)",
            "desc": "星空运行全部高阶 UI 模组、飞船构建突破与游戏机制大修的绝对基石前置。原生扩展游戏内存指针；游戏更新后要等作者发新版。",
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
            "category": "Bug Fixes (全漏洞修复)",
            "desc": "由全球顶尖 Modder 共同维护的开源综合漏洞修复包，修复了上千处恶性断任务、NPC 漂浮卡死与飞船无法停泊的底层代码 Bug。",
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
            "category": "UI / Interface",
            "desc": "消除打开物品栏、星图与技能界面时长达 0.5 秒的迟钝渐变淡入动画，界面秒开瞬切，操作如丝般顺滑。",
            "dependencies": [
                "None (SWF Override)"
            ],
            "installPath": "Starfield/Data/Interface/",
            "isDirect": False,
            "installSteps": [
                "1. 下载压缩包解压获取 Interface/ 文件夹；",
                "2. 将其放入 Starfield/Data/ 目录下；",
                "3. 游戏中按 Tab 打开菜单立刻感受零延迟交互。"
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
            "category": "👑 核心上帝模式与绝对生存 (God Mode & Invulnerability)",
            "commands": [
                {
                    "id": "sf_tgm",
                    "name": {
                        "zh-CN": "完全上帝模式 (TGM - 锁血/无限氧气/无限子弹)",
                        "en": "Toggle God Mode (tgm)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "Bethesda 经典全能神级代码，生命值、耐力氧气槽、飞船护盾与弹药全部锁定无限。",
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
                    "desc": "机体会受到正常伤害并显示残血状态，但生命值降至 1 点时绝不会倒下，保留战斗紧张感。",
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
            "category": "🚀 飞船建造部件无限制与反应堆电能 (Ship Builder Unlimited & Power)",
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
            "category": "🧬 角色特质修改、背景天赋与洗点 (Traits, Background & Skills)",
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
                        "zh-CN": "添加特质：英雄崇拜 (招募忠诚狂热粉丝)",
                        "en": "Add Trait: Hero Worshipped"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.addperk 00227FD9",
                    "desc": "解锁极为滑稽搞笑且忠诚的‘狂热粉丝’NPC随从，他会不断夸赞你并赠送免费小礼物。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Hero_Worshipped"
                },
                {
                    "id": "sf_add_trait_home",
                    "name": {
                        "zh-CN": "添加特质：梦想家园 (奥林匹斯豪宅钥匙)",
                        "en": "Add Trait: Dream Home"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.addperk 00227FDF",
                    "desc": "在风景优美的奥林匹斯星系拥有一座两层豪华独栋别墅，专享私密海景停机坪。",
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
                    "desc": "跳过低等级刷怪期，让游戏内高阶装备与传奇武器掉落池全部立刻解锁。",
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
                        "zh-CN": "获得 1,000,000 信用币 (财富自由秒买名舰)",
                        "en": "Add 1,000,000 Credits"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 1000000",
                    "desc": "背包直接入账一百万信用币，随意在霓虹城与新亚特兰蒂斯购买顶级现成星际战舰。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_add_digipicks",
                    "name": {
                        "zh-CN": "获得数码撬棒 x100 (开锁神器随心解谜)",
                        "en": "Add 100 Digipicks"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000A 100",
                    "desc": "获取 100 个开锁数码撬棒，无惧任何专家级与大师级保险箱圆环拼图试错。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Miscellaneous_Items"
                },
                {
                    "id": "sf_carry_weight_max",
                    "name": {
                        "zh-CN": "角色随身负重上限提升至 9,999 吨",
                        "en": "Set Player Carry Weight to 9,999"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 9999",
                    "desc": "将角色随身负重拉至上万点，身上装载几十把重武器与全部矿石亦可健步如飞。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_pay_bounty",
                    "name": {
                        "zh-CN": "一键清除全部星系阵营通缉赏金 (清罪免通缉)",
                        "en": "Clear All Faction Bounties"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.paycrimegold 0 0",
                    "desc": "支付你当前被通缉的、与所瞄准NPC同阵营的赏金（信用币从库存扣除），0 0表示不送监狱且不没收赃物；该命令每次只结清目标所属的一个阵营，并非一键清除全部阵营通缉赏金",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_unlock_target",
                    "name": {
                        "zh-CN": "强制解锁准星所指之门/保险箱 (秒开万物)",
                        "en": "Unlock Target Door / Safe"
                    },
                    "syntax_type": "creation_hex",
                    "code": "unlock",
                    "desc": "在控制台开启时用鼠标点击锁住的门或货箱，输入 unlock 即可瞬间物理破解开启。",
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
                        "zh-CN": "获得硬靶高精狙击步枪 (超远距离爆头一击必杀)",
                        "en": "Give Hard Target Sniper Rifle"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000546CC 1",
                    "desc": ".50 口径高初速反器材狙击步枪，加装消音器与夜视镜后潜行暴击伤害直接拉满。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Hard_Target"
                },
                {
                    "id": "sf_weapon_inflictor",
                    "name": {
                        "zh-CN": "获得瓦鲁恩折磨者粒子束步枪 (神级双属性输出)",
                        "en": "Give Va'ruun Inflictor Particle Rifle"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0026D8A0 1",
                    "desc": "瓦鲁恩毒蛇信徒秘造神兵，同时造成物理与能量双重属性伤害，全游戏最强 T0 步枪。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Va%27ruun_Inflictor"
                },
                {
                    "id": "sf_weapon_bigbang",
                    "name": {
                        "zh-CN": "获得大爆炸重型粒子束霰弹枪 (近身终极毁灭者)",
                        "en": "Give Big Bang Shotgun"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0026D963 1",
                    "desc": "近距离一枪轰杀任何高阶掠夺者与外星异形怪兽，自带扩散粒子灼烧暴击。",
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
                    "desc": "为当前所持武器附加金色传奇词条【煽动】，对生命值全满的目标造成整整 2 倍致命伤害！",
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
                        "zh-CN": "获得星裔天相战甲 (十周目终极神级宇航服)",
                        "en": "Give Starborn Spacesuit Astra"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0012E187 1",
                    "desc": "通关十周目获得的一体化星裔流光战甲，提供极致物理抗性、极寒耐受与自带隐形斗篷。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Starborn_Spacesuit_Astra"
                },
                {
                    "id": "sf_suit_mantis",
                    "name": {
                        "zh-CN": "获得蝠鲼传奇宇航服 (全套太空游侠神装)",
                        "en": "Give Mantis Spacesuit"
                    },
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00226299 1",
                    "desc": "蝠鲼秘密基地代代传承的传奇正义宇航服，自带减重与受到近战攻击反弹电弧特效。",
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
            "category": "🌌 全星系地标探索、重力调控与穿墙 (Star Map, Gravity & Exploration)",
            "commands": [
                {
                    "id": "sf_tmm_all",
                    "name": {
                        "zh-CN": "星图全部地标与着陆点一键全开 (TMM 1)",
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
                    "desc": "一键隐藏全屏血条、氧气表、指南针与准星，截取好莱坞科幻大片质感的深空照片。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfieldwiki.net/wiki/Starfield:Console"
                },
                {
                    "id": "sf_kah_enemies",
                    "name": {
                        "zh-CN": "击杀视野内所有敌对威胁 (KAH 秒杀全敌)",
                        "en": "Kill All Hostiles (kah)"
                    },
                    "syntax_type": "creation_hex",
                    "code": "kah",
                    "desc": "瞬间消灭当前场景中所有处于战斗敌对状态的海盗与外星虫群，和平清理战场。",
                    "framework_required": "None (Native Console)",
                    "source": "https://starfield.fandom.com/wiki/Help_command"
                }
            ]
        },
        {
            "category": "🛠️ 哨站全工业建材与稀有矿物全满 (Outpost Resources & Exotic Mats)",
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
                    "desc": "恶劣大气环境下密封哨站走廊与太空防护服隔绝层必不可少的高分子密封胶。",
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
            "desc": "一键激活 TGM 完全无敌 + 100万信用币启动资金 + 100把数码撬棒 + 随身负重万吨上限，萌新开局直接买下顶级战舰开荒！",
            "highlights": ["完全上帝模式，免受恶劣星球伤害", "1,000,000 信用币随心买船", "100 把数码撬棒，见箱就开", "负重上限 9,999 吨，垃圾随便捡"],
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
            "desc": "GTA 5 单机运行所有 ASI 脚本、载具菜单与功能模组的最权威开源前置。自带经典 F4 Native Trainer 离线菜单，包含防线上联机自动切断保护。",
            "dependencies": [
                "None (Native DLL)"
            ],
            "installPath": "Grand Theft Auto V/ (游戏根目录)",
            "isDirect": False,
            "installSteps": [
                "1. 点击下载 ScriptHookV_1.0.3179.0.zip；",
                "2. 打开 GTA 5 安装根目录 (包含 GTA5.exe 的文件夹)；",
                "3. 将 bin/ 目录下的 ScriptHookV.dll、dinput8.dll 和 NativeTrainer.asi 复制到根目录；",
                "4. 进入单机故事模式按 F4 即可呼出菜单。"
            ],
            "nexusUrl": "https://www.dev-c.com/gtav/scripthookv/",
            "version": "supports build 1.0.3889.0 / 1.0.1158.13 (current)"
        },
        {
            "id": "gta_menyoo_pc",
            "title": "Menyoo PC [SP]",
            "author": "MAFINS",
            "category": "Trainer / Menu",
            "desc": "功能冠绝全网的顶级单机离线菜单：随心刷出全部线上 DLC 豪车与战机、自定义保镖随从战队、建造自定义赛道飞跃跑道、随时更换任何剧情角色外观！",
            "dependencies": [
                "ScriptHookV"
            ],
            "installPath": "Grand Theft Auto V/",
            "isDirect": True,
            "installSteps": [
                "1. 确认已安装 ScriptHookV 前置；",
                "2. 下载压缩包解压获取 menyooStuff 文件夹和 Menyoo.asi；",
                "3. 放入 GTA5 游戏根目录；",
                "4. 故事模式按 F8 即可打开图形化菜单。"
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
            "desc": "安装现实真车包、高清地图画质材质包与真实枪械声音必备的归档编辑工具。独创 mods 文件夹隔离机制，保护游戏原版文件绝对不受污染破坏。",
            "dependencies": [
                "None (Stand-alone Tool)"
            ],
            "installPath": "Windows PC",
            "isDirect": False,
            "installSteps": [
                "1. 下载运行 OpenIVSetup.exe 安装工具；",
                "2. 打开 OpenIV 选择 Grand Theft Auto V (Windows)；",
                "3. 点击 Tools -> ASI Manager，全部点击 Install 安装 ASI 驱动；",
                "4. 所有后续 RPF 模组均放入 mods 文件夹中无损替换。"
            ],
            "nexusUrl": "https://openiv.com",
            "version": "4.1"
        },
        {
            "id": "gta_nve_graphics",
            "title": "NaturalVision Evolved",
            "author": "Razed",
            "category": "Graphics (顶级画质)",
            "desc": "耗时数年倾力打造的次世代画质圣经，重制全洛圣都天气照明、反射水面、雨天积水倒影与霓虹夜景，赋予老游戏媲美 2026 年大作的电影级真实感！",
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
                "4. 启动游戏享受好莱坞大片级视觉盛宴。"
            ],
            "nexusUrl": "https://www.razedmods.com/gta-v"
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 经典官方无敌与通缉度调控 (God Mode & Wanted Level Cheats)",
            "commands": [
                {
                    "id": "gta_cheat_painkiller",
                    "name": {
                        "zh-CN": "官方经典无敌 5 分钟 (PAINKILLER)",
                        "en": "Invincibility for 5 Mins (PAINKILLER)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "PAINKILLER",
                    "desc": "官方原生秘籍代码，开启 5 分钟绝对锁血无敌状态，任何爆炸枪击高处坠落毫发无损。",
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
                    "desc": "立刻回满角色全部血槽与最高级别防弹衣，若身在载具中还会瞬间将汽车彻底修复如初。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gta.fandom.com/wiki/Cheats_in_GTA_V"
                },
                {
                    "id": "gta_cheat_lawyerup",
                    "name": {
                        "zh-CN": "降低并清除一星通缉度 (LAWYERUP)",
                        "en": "Clear Wanted Level (LAWYERUP)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "LAWYERUP",
                    "desc": "让洛圣都警方降低并撤销当前追捕通缉星级，脱离警用直升机与巡警视野侦测。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_fugitive",
                    "name": {
                        "zh-CN": "提升一星通缉等级 (FUGITIVE - 挑衅追逐)",
                        "en": "Raise Wanted Level (FUGITIVE)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "FUGITIVE",
                    "desc": "为当前角色额外增加一颗通缉星，主动引诱特警防暴车与 FIB 探员展开激烈公路追击。",
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
                        "zh-CN": "获取全套军火武器库与弹药 (TOOLUP)",
                        "en": "All Weapons & Max Ammo (TOOLUP)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "TOOLUP",
                    "desc": "瞬间为当前角色配齐手枪、微冲、突击步枪、高精狙击枪、榴弹发射器及黏弹全套装备。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_highex",
                    "name": {
                        "zh-CN": "开启高爆破坏子弹 (HIGHEX - 枪枪爆裂)",
                        "en": "Explosive Bullets (HIGHEX)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "HIGHEX",
                    "desc": "所有打出的子弹命中目标瞬间化为剧烈高爆手雷威力，任何路过车辆一枪直接轰至解体起火。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_incendiary",
                    "name": {
                        "zh-CN": "开启炽热燃烧子弹 (INCENDIARY - 火海蔓延)",
                        "en": "Flame Bullets (INCENDIARY)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "INCENDIARY",
                    "desc": "射出的每一发子弹命中物体与敌人即刻引发熊熊大火，造成持续性灼烧伤害并点燃周围环境。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_hothands",
                    "name": {
                        "zh-CN": "超能爆炸近战拳击 (HOTHANDS - 隔空轰飞)",
                        "en": "Explosive Melee Attacks (HOTHANDS)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "HOTHANDS",
                    "desc": "肉搏挥拳命中目标产生巨大冲击波爆炸，将挡路的警车与路人直接炸飞上几十米高空。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_deadeye",
                    "name": {
                        "zh-CN": "精准瞄准慢动作三段调节 (DEADEYE)",
                        "en": "Aiming Slomo Matrix (DEADEYE)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "DEADEYE",
                    "desc": "举枪瞄准时自动进入三阶慢动作子弹时间，精准爆头命中移动中的敌方直升机驾驶员。",
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
                    "desc": "在眼前平地直接召唤一辆高性能经典跑车彗星，极速破百，操控手感灵敏敏捷。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_rapidgt",
                    "name": {
                        "zh-CN": "召唤疾速 GT 豪华 GT 轿跑 (RAPIDGT)",
                        "en": "Spawn Rapid GT Coupe (RAPIDGT)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "RAPIDGT",
                    "desc": "召唤极具美感的双门豪华硬顶跑车，强劲后驱马力，洛圣都高速公路飙车首选。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_buzzoff",
                    "name": {
                        "zh-CN": "召唤秃鹰重型武装直升机 (BUZZOFF)",
                        "en": "Spawn Buzzard Attack Helicopter (BUZZOFF)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "BUZZOFF",
                    "desc": "直接生成一架配备追踪火箭弹舱与加特林机枪的军用武装直升机，空中火力压制全场。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gtabase.com/grand-theft-auto-v/gta-5-cheats-pc-full-list-of-cheat-codes"
                },
                {
                    "id": "gta_cheat_barnstorm",
                    "name": {
                        "zh-CN": "召唤麦拉德特技双翼飞行机 (BARNSTORM)",
                        "en": "Spawn Mallard Stunt Plane (BARNSTORM)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "BARNSTORM",
                    "desc": "召唤一架机动性极强的高速特技飞行器，在洛圣都摩天大楼与桥梁缝隙中穿梭穿桥。",
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
            "category": "🏊 角色超自然能力与世界物理 (Super Jump, Fast Run & Skyfall)",
            "commands": [
                {
                    "id": "gta_cheat_hoptoit",
                    "name": {
                        "zh-CN": "开启绿巨人超级弹跳 (HOPTOIT - 跃上楼顶)",
                        "en": "Super Jump Leap (HOPTOIT)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "HOPTOIT",
                    "desc": "按住跳跃键可直接蓄力腾空跃起十层楼高，跨越矮层建筑屋顶与高架桥围栏。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.gtaboom.com/GTA_5_Cheats_PC"
                },
                {
                    "id": "gta_cheat_catchme",
                    "name": {
                        "zh-CN": "开启超级短跑极速疾驰 (CATCHME - 健步如飞)",
                        "en": "Super Fast Sprinting (CATCHME)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "CATCHME",
                    "desc": "角色奔跑与短跑冲刺速度提升至极限，公路追车甚至能用双腿超越普通代步轿车。",
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
                    "desc": "在海水与游泳池中如离弦之箭极速穿梭，潜水与避让近海饥饿白鲨游刃有余。",
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
                    "desc": "立即装备高空跳伞专用降落伞，从乞力耶德山缆车顶端或直升机上一跃而下尽情翱翔。",
                    "framework_required": "None (Native Console)",
                    "source": "https://gta.fandom.com/wiki/Cheats_in_GTA_V"
                },
                {
                    "id": "gta_cheat_skyfall",
                    "name": {
                        "zh-CN": "万米高空自由落体跳伞模式 (SKYFALL)",
                        "en": "Skyfall from High Altitude (SKYFALL)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "SKYFALL",
                    "desc": "将角色瞬间传送至洛圣都万米云海高空进行无伞自由落体滑翔俯冲（请确保先开无敌）。",
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
                        "zh-CN": "切换雷雨暴风雨天气 (MAKEITRAIN)",
                        "en": "Change Weather to Thunderstorm (MAKEITRAIN)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "MAKEITRAIN",
                    "desc": "洛圣都天空乌云密布并降下磅礴大雨与轰鸣闪电，路面湿滑极具电影黑色氛围。",
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
                        "zh-CN": "全局慢动作电影运镜流速 (SLOWMO - 四段循环)",
                        "en": "Slomo World Matrix (SLOWMO)"
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
            "name": "六星狂暴大逃杀激战包",
            "tag": "🛡️ 意难平救赎 · 告别受苦",
            "badge": "六星激战",
            "desc": "呼叫秃鹰重型武装直升机 + 开启 HIGHEX 高爆穿甲子弹 + 超能肉搏冲击波 + 锁定六星极限通缉，单挑整座洛圣都军警装甲力量！",
            "highlights": ["召唤秃鹰武装直升机空中轰炸", "HIGHEX 爆裂子弹枪枪起爆", "超能肉搏拳击隔空轰碎载具", "六星特警坦克封路大围捕"],
            "code": "-- [老L·极客场景套餐] GTA5 六星狂暴大逃杀激战包\nBUZZOFF\nHIGHEX\nHOTHANDS\nFUGITIVE\nFUGITIVE"
        },
        {
            "id": "gta_godmode_bundle",
            "type": "godmode",
            "name": "超自然空中飞仙终极漫游包",
            "tag": "⚡ 极客狂欢 · 众神陨落",
            "badge": "真神漫游",
            "desc": "万米高空云端自由落体 SKYFALL + 绿巨人十层楼超级跳跃 + 月球低重力微浮力 + 全城圣诞暴风雪，体验前所未见的荒诞洛圣都奇观！",
            "highlights": ["万米高空自由落体无伞俯冲", "超级跳跃跃过摩天大楼", "月球低重力飞车漫步", "罕见全城圣诞暴风雪漫延"],
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
            "desc": "大镖客界公认最强单机离线功能菜单：随时召唤上百种马匹、变身为印第安酋长或动物、随身衣柜换装、营地升级与瞬移全图。",
            "dependencies": [
                "ScriptHookRDR2"
            ],
            "installPath": "Red Dead Redemption 2/",
            "isDirect": False,
            "installSteps": [
                "1. 确保已安装 ScriptHookRDR2；",
                "2. 下载压缩包解压出 Rampage.asi 和 RampageFiles 文件夹；",
                "3. 放入 RDR2 根目录；",
                "4. 故事模式按 F5 或 F7 打开 Rampage 高清菜单。"
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
            "desc": "彻底告别手动解包 RPF 替换文件的繁琐风险！所有新服饰、枪械高清贴图与声音直接放入 lml/ 文件夹即可自动挂载生效。",
            "dependencies": [
                "ScriptHookRDR2"
            ],
            "installPath": "Red Dead Redemption 2/",
            "isDirect": False,
            "installSteps": [
                "1. 解压 ModLoader 文件夹内全部文件至 RDR2 根目录；",
                "2. 根目录会自动生成 lml/ 文件夹；",
                "3. 后续下载的服饰与材质 mod 直接扔进 lml/ 即可。"
            ],
            "nexusUrl": "https://www.rdr2mods.com/downloads/rdr2/tools/76-lennys-mod-loader-rdr/",
            "version": "0.6.8470.31280"
        },
        {
            "id": "rdr2_whyems_dlc",
            "title": "WhyEm's  DLC",
            "author": "WhyEm",
            "category": "Clothing & Customization",
            "desc": "西部牛仔终极衣柜拓展包：为亚瑟增添上千件精美皮衣、披风、马甲、定制牛皮枪套、罕见发型与传说动物皮毛羽毛装饰！",
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
                "4. 前往捕兽人或裁缝铺即可选购所有独家服饰。"
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
            "category": "👑 核心无敌、无限体力与死神之眼 (God Mode, Stamina & Dead Eye)",
            "commands": [
                {
                    "id": "rdr_cheat_freedom",
                    "name": {
                        "zh-CN": "降低通缉等级 (You want freedom)",
                        "en": "Lower Wanted Level (You want freedom)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "You want freedom",
                    "desc": "官方秘籍短语，降低亚瑟当前的通缉星级。RDR2 游戏内没有真正的『无敌』秘籍（多个权威来源一致确认）。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.shacknews.com/article/108219/full-cheat-codes-list-in-red-dead-redemption-2"
                },
                {
                    "id": "rdr_cheat_flourish",
                    "name": {
                        "zh-CN": "三核心瞬间回满 (You flourish before you die)",
                        "en": "Max All Bars (You flourish before you die)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "You flourish before you die",
                    "desc": "立即将生命、体力与死神之眼内侧核心及外侧环槽全部充满至最高数值。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.shacknews.com/article/108219/full-cheat-codes-list-in-red-dead-redemption-2"
                },
                {
                    "id": "rdr_cheat_deadeye",
                    "name": {
                        "zh-CN": "无限死神之眼子弹时间 (Seek all the bounty of this place)",
                        "en": "Infinite Dead Eye"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Be greedy only for foresight",
                    "desc": "开启无限死神之眼模式，随心进入拔枪时缓，一次性标定全屏所有匪徒头部。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.powerpyx.com/red-dead-redemption-2-cheats/"
                },
                {
                    "id": "rdr_cheat_stealth",
                    "name": {
                        "zh-CN": "悄然无声刺杀暗杀 (Death is silence)",
                        "en": "Stealth Weapons (Death is silence)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Death is silence",
                    "desc": "配齐印第安飞斧、飞刀、改良弓箭等全套静音潜行暗杀武器库。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.powerpyx.com/red-dead-redemption-2-cheats/"
                }
            ]
        },
        {
            "category": "💰 亚瑟钱包现金、全金条与全背包升级 (Money, Gold Bars & Legend of East Satchel)",
            "commands": [
                {
                    "id": "rdr_cheat_greed",
                    "name": {
                        "zh-CN": "获取 $500 现金 (Greed is American virtue)",
                        "en": "Give $500 Cash (Greed is American virtue)"
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
            "category": "🐎 顶级良驹阿拉伯马与默契度拉满 (Horses Spawner & Max Bonding)",
            "commands": [
                {
                    "id": "rdr_cheat_kingdom_horse",
                    "name": {
                        "zh-CN": "提升马匹默契度 (My kingdom is a horse)",
                        "en": "Increase Horse Bonding"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "My kingdom is a horse",
                    "desc": "官方原生秘籍代码，直接拉升当前坐骑的默契等级，解锁急停与侧向滑行步伐。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.pcgamesn.com/red-dead-redemption-2/rdr2-cheats-pc"
                }
            ]
        },
        {
            "category": "🔫 传奇黑火药军备、稀有枪械与全弹药 (Rare Weapons & Explosive Ammo)",
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
                        "zh-CN": "获取全套传奇神枪手武器 (History is written by fools)",
                        "en": "Gunslinger Rare Weapons"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "History is written by fools",
                    "desc": "官方秘籍短语，获得神枪手武器套装（含双动左轮手枪、双管霰弹枪等决斗相关武器）。",
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
                    "desc": "随身携带的全部枪弹弹药锁定无限，告别去枪械铺逐盒购买子弹的繁琐。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.shacknews.com/article/108219/full-cheat-codes-list-in-red-dead-redemption-2"
                }
            ]
        },
        {
            "category": "🌦️ 昼夜天气调控、快速传送与荣誉值 (Honor, Weather & Fast Travel)",
            "commands": [
                {
                    "id": "rdr_cheat_virtue",
                    "name": {
                        "zh-CN": "荣誉值一键提升至最高上限 (Virtue unearned is not virtue)",
                        "en": "Max Honor Level (Virtue unearned is not virtue)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "Virtue unearned is not virtue",
                    "desc": "官方原生秘籍代码，亚瑟声望瞬间升至满额最高级，商店购物享受 50% 半价折扣特惠。",
                    "framework_required": "None (Native Console)",
                    "source": "https://www.powerpyx.com/red-dead-redemption-2-cheats/"
                },
                {
                    "id": "rdr_cheat_punishment",
                    "name": {
                        "zh-CN": "提升通缉等级 (You want punishment - 赏金猎人大战)",
                        "en": "Raise Bounty (You want punishment)"
                    },
                    "syntax_type": "rage_cheat",
                    "code": "You want punishment",
                    "desc": "为亚瑟附加悬赏星级，引来全州最精锐的平克顿侦探与猎犬展开生死决战追杀。",
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
            "desc": "怪猎世界冰原运行 nativePC 外部模组、商店补全插件与透视覆层的绝对核心前置库，包含 CRC 绕过修复。",
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
            "desc": "将月辰与星辰基地的物资补给所商店彻底重制：所有 4 级神珠、古龙大宝玉、聚魔之地客制材料全部上架，统一标价 1 铜币，告别几百小时枯燥刷珠子！",
            "dependencies": [
                "Stracker's Loader"
            ],
            "installPath": "Monster Hunter World/nativePC/common/facility/",
            "isDirect": False,
            "installSteps": [
                "1. 确认已安装 Stracker's Loader 前置；",
                "2. 下载压缩包解压获取 nativePC 文件夹；",
                "3. 直接合并覆盖到游戏根目录下；",
                "4. 到道具屋阿姨处对话即可挑选任何顶级珠子与素材。"
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
            "desc": "狩猎利器！在屏幕上方优雅悬浮显示怪物真实总血量、当前血百分比、激怒倒计时、麻痹/睡眠积蓄值，以及队伍四人各自输出 DPS 占比统计！",
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
            "desc": "移除冰原反作弊死循环冗余检测，大幅消除 100% CPU 占用导致的掉帧卡顿。效果因电脑而异，本站没有测过具体帧数。",
            "dependencies": [
                "Stracker's Loader"
            ],
            "installPath": "Monster Hunter World/nativePC/plugins/",
            "isDirect": False,
            "installSteps": [
                "1. 下载压缩包解压出 .dll 插件；",
                "2. 放入 nativePC/plugins/ 目录；",
                "3. 启动游戏享受极致丝滑 120FPS 狩猎体验。"
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
            "desc": "只狼外部材质、流派动作替换与参数修改的绝对基石前置。自动拦截文件加载路径，零修改游戏原版文件，极客必备。",
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
            "desc": "突破官方恶心的 60 帧锁帧限制，支持 144Hz/240Hz 高刷电竞屏，消除 21:9 带鱼屏黑边，完美支持宽屏原生分辨率与无边框窗口化！",
            "dependencies": [
                "None (Stand-alone Tool)"
            ],
            "installPath": "Windows PC",
            "isDirect": True,
            "installSteps": [
                "1. 下载解压获取 SekiroFpsUnlockAndMore.exe；",
                "2. 先启动只狼游戏，然后双击运行该工具；",
                "3. 勾选 'Unlock FPS' 并将上限滑块拉至 144 或 240；",
                "4. 刀光剑影流畅如丝，再无拖影困扰。"
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
            "desc": "在任何鬼佛处直接开启所有 Boss 与精英怪独立连战挑战，无需跑图过剧情，随时随地练习弹刀剑圣苇名一心、义父与怨恨之鬼！",
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
            "desc": "享誉魂系圈的顶级战斗大修：重做几乎全 Boss 与杂兵招式逻辑、为狼增加全新流派招式与衍生追击，打刀防反手感登峰造极！",
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
            "desc": "卡普空 RE 引擎游戏绝对核心！集成强大的 ImGui 覆层控制面板、自由运镜摄影机、第一人称视角切换与宽广 FOV 调谐。",
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
            "desc": "生化危机系列公认最强模组安装器：一键安装、启用、禁用上千款角色外观、艾达王特工服、发型与武器贴图替换。",
            "dependencies": [
                "None (Stand-alone Tool)"
            ],
            "installPath": "Windows PC",
            "isDirect": False,
            "installSteps": [
                "1. 下载解压运行 Modmanager.exe；",
                "2. 在游戏列表选择 'Resident Evil 4 Remake'；",
                "3. 将下载的 .rar/.zip 角色外观模组拖入软件窗口；",
                "4. 点击滑块切换勾选即可一秒生效启用。"
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
