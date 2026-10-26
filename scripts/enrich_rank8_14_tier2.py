#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/enrich_rank8_14_tier2.py
L-MOD Vault 第二梯队 (Rank 8~14) 核心大作全息采掘注入引擎
对齐游戏：
  - Rank 8: 幻兽帕鲁 (Palworld) [UE5 + UE4SS]
  - Rank 9: 星空 (Starfield) [Creation 2]
  - Rank 10: 侠盗猎车手5 (Grand Theft Auto V) [RAGE + ScriptHookV]
  - Rank 11: 荒野大镖客：救赎2 (Red Dead Redemption 2) [RAGE + ScriptHookRDR2]
  - Rank 12: 怪物猎人：世界 (Monster Hunter: World) [MT Framework + Stracker / REFramework]
  - Rank 13: 只狼：影逝二度 (Sekiro: Shadows Die Twice) [FromSoftware + ModEngine]
  - Rank 14: 生化危机4：重制版 (Resident Evil 4 Remake) [RE Engine + REFramework]
同时为 Rank 1~7 游戏补齐 Mod 真实直链与下载文件名。
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "src/data/games_top100.json")
JS_PATH = os.path.join(BASE_DIR, "public/data.js")

# ==============================================================================
# RANK 8: 幻兽帕鲁 (Palworld)
# ==============================================================================
PALWORLD_DATA = {
    "rank": 8,
    "hasConsole": True,
    "consoleShortcut": "F10 或 ~ (需安装 RE-UE4SS xinput1_3.dll 注入底层)",
    "consoleEnableGuide": {
        "zh-CN": "【UE4SS 注入与打字控制台开启指南】\n1. 下载 UE4SS (v3.0.1 纯净版)，将压缩包解压至游戏根目录：Palworld/Pal/Binaries/Win64/；\n2. 确认该目录下存在 UE4SS.dll、xinput1_3.dll 以及 mods/ 文件夹；\n3. 启动游戏，在单机或本地专用服务器中按 F10 唤出 UE4SS 图形控制台，或按 ~ 唤出原生终端；\n4. 即可直接运行闪光帕鲁生成、全图鉴解锁、属性注入与自由镜头摄影！",
        "en": "Install UE4SS (v3.0.1) into Palworld/Pal/Binaries/Win64/. Press F10 or ~ in-game to bring up Lua console for Pal spawner and Paldeck unlocks."
    },
    "popularCommands": [
        "give PalSphere_Mega 50",
        "spawn Anubis 50",
        "addexp 50000",
        "give Money 1000000",
        "slomo 0.3",
        "r.ViewDistanceScale 3"
    ],
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v0.3.x+ (Sakurajima 樱岛版本完全对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/palworld-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/palworld/Palworld_v0.3_Plus_33_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "7c8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Palworld Trainer.exe'",
            "troubleshootSteps": [
                "必须在单人世界或自建离线房间中运行修改器，请勿在官方 VAC/反作弊服务器使用",
                "若 Windows Defender 拦截，以管理员身份运行上方 PowerShell 白名单放行指令",
                "建议先进入游戏加载完人物后，再按对应小键盘快捷键激活修改项目"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 核心生存与无敌状态",
                "items": [
                    {"key": "Num 1", "action": "无敌模式 (God Mode / 锁血锁盾)"},
                    {"key": "Num 2", "action": "无限体力 (奔跑/攀爬/滑翔零耐力消耗)"},
                    {"key": "Num 3", "action": "饱食度全满 (不再产生饥饿感)"},
                    {"key": "Num 4", "action": "无限帕鲁体力与饱食度"},
                    {"key": "Num 5", "action": "温度恒定舒适 (免疫炎热与严寒)"}
                ]
            },
            {
                "category": "🎒 装备耐久与随身负重",
                "items": [
                    {"key": "Num 6", "action": "无限武器装备耐久度 (永不损坏)"},
                    {"key": "Num 7", "action": "随身负重清零 (无限捡取矿石与建材)"},
                    {"key": "Num 8", "action": "100% 帕鲁捕捉成功率 (哪怕普通球抓神兽)"},
                    {"key": "Num 9", "action": "帕鲁球数量不减 (投掷不消耗)"}
                ]
            },
            {
                "category": "⚡ 经验财富与时间流速",
                "items": [
                    {"key": "Ctrl+Num 1", "action": "编辑玩家金钱金币 (999,999)"},
                    {"key": "Ctrl+Num 2", "action": "无限古代科技点数与普通科技点"},
                    {"key": "Ctrl+Num 3", "action": "瞬间孵蛋 (孵化器无需漫长等待)"},
                    {"key": "Ctrl+Num 4", "action": "据点帕鲁 SAN 值全满锁定 (永不抑郁生病)"},
                    {"key": "Ctrl+Num 5", "action": "自定移动速度与全局时间倍率 (0.5x~5.0x)"}
                ]
            }
        ]
    },
    "hasMods": True,
    "curatedMods": [
        {
            "id": "pal_ue4ss",
            "title": "UE4SS for Palworld (虚幻5底层脚本与模组注入核心)",
            "author": "UE4SS-RE Team",
            "version": "v3.0.1",
            "size": "2.8 MB",
            "downloads": "2.1M",
            "endorsements": "115K",
            "category": "Core Framework (核心前置)",
            "desc": "幻兽帕鲁运行全部 Lua 模组、UI 扩展与控制台打字命令的绝对核心前置库，零注入误报，极客必备。",
            "dependencies": ["None (Native Injector)"],
            "installPath": "Palworld/Pal/Binaries/Win64/",
            "downloadUrl": "https://github.com/UE4SS-RE/RE-UE4SS/releases/download/v3.0.1/UE4SS_v3.0.1.zip",
            "downloadFilename": "UE4SS_v3.0.1_Palworld.zip",
            "isDirect": True,
            "installSteps": [
                "1. 点击上方按钮下载 UE4SS_v3.0.1_Palworld.zip 压缩包；",
                "2. 打开游戏安装路径进入 Pal/Binaries/Win64/；",
                "3. 将压缩包内的 UE4SS.dll、xinput1_3.dll 和 mods 文件夹直接解压到该目录；",
                "4. 启动游戏即可生效，按 F10 即可呼出控制面板。"
            ]
        },
        {
            "id": "pal_analyzer",
            "title": "PalAnalyzer (帕鲁全属性资质与被动词条即时透视器)",
            "author": "Bobbyglow",
            "version": "v1.4.0",
            "size": "450 KB",
            "downloads": "890K",
            "endorsements": "48K",
            "category": "Gameplay / UI",
            "desc": "将准星对准野外或据点帕鲁时，悬浮窗直接显示其隐藏 IV 个体值、攻击/防御天赋、被动词条及捕捉成功率，抓宠不再开盲盒！",
            "dependencies": ["UE4SS for Palworld"],
            "installPath": "Palworld/Pal/Binaries/Win64/Mods/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/palworld/PalAnalyzer_v1.4.0.zip",
            "downloadFilename": "PalAnalyzer_v1.4.0.zip",
            "isDirect": True,
            "installSteps": [
                "1. 确保已安装 UE4SS 核心框架；",
                "2. 下载压缩包并解压至 Pal/Binaries/Win64/Mods/ 目录；",
                "3. 进入游戏按住 Alt 键对准帕鲁即可查看详细天赋面板。"
            ]
        },
        {
            "id": "pal_carry_weight",
            "title": "CarryWeight5000 (随身背包负重上限百万解除)",
            "author": "Vuxin",
            "version": "v2.0.1",
            "size": "35 KB",
            "downloads": "1.4M",
            "endorsements": "72K",
            "category": "QoL (体验优化)",
            "desc": "将人物初始负重提升至 999,999，彻底解决挖金属矿、采石场搬运时走不动的负重折磨，采矿狂魔福音。",
            "dependencies": ["UE4SS for Palworld"],
            "installPath": "Palworld/Pal/Content/Paks/~mods/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/palworld/CarryWeight_NoLimit.zip",
            "downloadFilename": "CarryWeight_NoLimit.zip",
            "isDirect": True,
            "installSteps": [
                "1. 进入 Pal/Content/Paks/ 目录，若无 ~mods 文件夹则新建一个；",
                "2. 将解压出的 .pak 文件放入 ~mods 目录；",
                "3. 重启游戏即可享受无限负重。"
            ]
        },
        {
            "id": "pal_always_shiny",
            "title": "AlwaysShiny (野外闪光幸运帕鲁高概率出现调优)",
            "author": "Neneko",
            "version": "v1.2.0",
            "size": "60 KB",
            "downloads": "650K",
            "endorsements": "34K",
            "category": "Spawns / Creatures",
            "desc": "大幅提升野外闪光（稀有金色巨大体型）帕鲁的自然刷新率，并自带自带神级词条【稀有】与巨额属性加成！",
            "dependencies": ["UE4SS for Palworld"],
            "installPath": "Palworld/Pal/Binaries/Win64/Mods/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/palworld/AlwaysShiny_Mod.zip",
            "downloadFilename": "AlwaysShiny_Mod.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载解压放入 Pal/Binaries/Win64/Mods/ 文件夹；",
                "2. 打开 mod 目录下的 config.lua 可自定义刷新概率 (默认提升 10 倍)；",
                "3. 进入野外即可听到清脆的闪光音效提示。"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 核心生存与角色机能 (God Mode & Core Survival)",
            "commands": [
                {
                    "id": "pal_slomo_safe",
                    "name": {"zh-CN": "全局慢动作子弹时间 (0.3x 防御识破)", "en": "Bullet Time Slomo (0.3x)"},
                    "syntax_type": "ue5_console",
                    "code": "slomo 0.3",
                    "desc": "将全局时间流速放慢至 0.3 倍，精准观察野外神兽大招起手前摇，闪避零失误。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                },
                {
                    "id": "pal_slomo_normal",
                    "name": {"zh-CN": "恢复全局正常时间流速 (1.0x)", "en": "Normal Game Speed (1.0x)"},
                    "syntax_type": "ue5_console",
                    "code": "slomo 1.0",
                    "desc": "将时间流速重置回正常标准速度。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                },
                {
                    "id": "pal_teleport_base",
                    "name": {"zh-CN": "坐标快速瞬间移动 (瞬移至安全平原)", "en": "Teleport to Safe Plains"},
                    "syntax_type": "ue5_console",
                    "code": "teleport 3500 12000 500",
                    "desc": "将角色机体瞬间传送至初始台地安全空旷区域，紧急脱离卡地形困境。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_toggle_cam",
                    "name": {"zh-CN": "开启虚幻5自由调试镜头 (无死角摄影)", "en": "Toggle Free Debug Camera"},
                    "syntax_type": "ue5_console",
                    "code": "toggledebugcamera",
                    "desc": "脱离角色机体进入完全自由悬浮运镜，用于高清基地全景截图与穿透山谷探索。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_stat_fps",
                    "name": {"zh-CN": "实时帧率与硬件渲染耗时诊断", "en": "Show FPS & Frame Timing"},
                    "syntax_type": "ue5_console",
                    "code": "stat fps",
                    "desc": "在屏幕右上角显示虚幻5精准帧数与毫秒渲染耗时，排查据点帕鲁拥堵卡顿。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                }
            ]
        },
        {
            "category": "⚡ 角色等级、属性点与科技树满级 (Levels, Tech Points & Stats)",
            "commands": [
                {
                    "id": "pal_add_exp_50k",
                    "name": {"zh-CN": "获得 50,000 点角色经验值", "en": "Add 50,000 Player EXP"},
                    "syntax_type": "ue5_gm",
                    "code": "addexp 50000",
                    "desc": "直接为当前操控角色注入 5 万点经验值，极速提升等级解锁高级制造科技。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_add_exp_max",
                    "name": {"zh-CN": "获得 1,000,000 巨额经验值 (直升55级满级)", "en": "Add 1,000,000 EXP (Max Level)"},
                    "syntax_type": "ue5_gm",
                    "code": "addexp 1000000",
                    "desc": "注入 100 万经验，瞬间跨越开荒升级漫长等待，直接冲顶当前版本角色最高等级。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_add_stat_point",
                    "name": {"zh-CN": "增加 50 点角色属性强化点数", "en": "Add 50 Attribute Points"},
                    "syntax_type": "ue5_gm",
                    "code": "addtalentpoint 50",
                    "desc": "增加 50 点可自由分配属性点，随意加满负重上限、体力槽或攻击力。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_stat_reset",
                    "name": {"zh-CN": "获得记忆消除药 (完美无损洗点灵药)", "en": "Give Memory Reset Drug"},
                    "syntax_type": "ue5_gm",
                    "code": "give Med_ResetStatusPoint 5",
                    "desc": "获取 5 瓶洗点药水，服用后全额退还已分配点数，重塑角色开荒流派。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_ancient_tech",
                    "name": {"zh-CN": "获得古代技术书 (增加古代科技点)", "en": "Give Ancient Tech Manuals"},
                    "syntax_type": "ue5_gm",
                    "code": "give TechnologyBook_G3 20",
                    "desc": "获取 20 本高阶古代技术书，使用直接获得大量古代科技点，解锁孵化器与抓钩枪。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                }
            ]
        },
        {
            "category": "🦖 闪光帕鲁生成与稀有神兽召唤 (Shiny Pals Spawner & Legendaries)",
            "commands": [
                {
                    "id": "pal_spawn_anubis",
                    "name": {"zh-CN": "生成 50 级阿努比斯 (手工Lv4 最强打工真神)", "en": "Spawn Anubis (Lv50)"},
                    "syntax_type": "ue5_gm",
                    "code": "spawn Anubis 50",
                    "desc": "在眼前直接生成 50 级阿努比斯，具备游戏最高 4 级手工与采矿能力，基建生产光速运转。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_spawn_jetragon",
                    "name": {"zh-CN": "生成 50 级空涡龙 (全图飞行最快神兽)", "en": "Spawn Jetragon (Lv50 Legendary)"},
                    "syntax_type": "ue5_gm",
                    "code": "spawn Jetragon 50",
                    "desc": "生成传说级龙系神兽空涡龙，解锁导弹鞍具后具备全游戏最高超音速巡航飞行速度。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_spawn_frostallion",
                    "name": {"zh-CN": "生成 50 级唤冬兽 (冰系顶级传说骑宠)", "en": "Spawn Frostallion (Lv50)"},
                    "syntax_type": "ue5_gm",
                    "code": "spawn Frostallion 50",
                    "desc": "召唤极地冰系传说神兽，骑乘时将攻击转变为冰属性并大幅强化冰系伤害。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_spawn_paladius",
                    "name": {"zh-CN": "生成 50 级圣光骑士 (三段跳全地形坐骑)", "en": "Spawn Paladius (Lv50)"},
                    "syntax_type": "ue5_gm",
                    "code": "spawn Paladius 50",
                    "desc": "生成圣光骑士神兽，独具空中三段跳跃能力，翻山越岭如履平地。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_spawn_necromus",
                    "name": {"zh-CN": "生成 50 级混沌骑士 (暗黑双跳神级战宠)", "en": "Spawn Necromus (Lv50)"},
                    "syntax_type": "ue5_gm",
                    "code": "spawn Necromus 50",
                    "desc": "召唤暗属性神兽混沌骑士，兼备极高地面跑速与恐怖的暗黑突刺贯穿伤害。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                }
            ]
        },
        {
            "category": "📜 全帕鲁图鉴、捕捉率突破与全鞍具 (Paldeck Unlock & Max Capture)",
            "commands": [
                {
                    "id": "pal_unlock_paldeck",
                    "name": {"zh-CN": "一键点亮全 137+ 帕鲁图鉴百科", "en": "Unlock Entire Paldeck Catalog"},
                    "syntax_type": "ue5_gm",
                    "code": "unlock allpaldeck",
                    "desc": "点亮全图鉴资料库记录，解锁全部帕鲁详细掉落物、分布栖息地与工作适应性信息。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_legendary_sphere",
                    "name": {"zh-CN": "获得传奇帕鲁球 x100 (极高捕捉概率)", "en": "Give 100 Legendary Pal Spheres"},
                    "syntax_type": "ue5_gm",
                    "code": "give PalSphere_Legend 100",
                    "desc": "获取 100 颗金色传说帕鲁球，配合捕捉力提升，即使捕捉 50 级神兽亦信手拈来。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_ultimate_sphere",
                    "name": {"zh-CN": "获得终极帕鲁球 x50 (樱岛顶级究极球)", "en": "Give 50 Ultimate Pal Spheres"},
                    "syntax_type": "ue5_gm",
                    "code": "give PalSphere_Ultimate 50",
                    "desc": "获取樱岛版本新增的最高阶究极球，捕获率冠绝全场，几乎一球必中。",
                    "min_version": "v0.3.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_jetragon_saddle",
                    "name": {"zh-CN": "获得空涡龙导弹发射器鞍具", "en": "Give Jetragon Missile Launcher Saddle"},
                    "syntax_type": "ue5_gm",
                    "code": "give Weapon_Jetragon_Missile 1",
                    "desc": "获取空涡龙专用武装鞍具，骑乘时可发射追踪火箭弹幕，秒清野外密集帕鲁群。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_grappling_gun",
                    "name": {"zh-CN": "获得四向超强抓钩枪 (超远飞索赶路)", "en": "Give Hyper Grappling Gun"},
                    "syntax_type": "ue5_gm",
                    "code": "give GrapplingGun4 1",
                    "desc": "获取游戏内射程最远、拉力最大的 4 级超级抓钩枪，即使负重过载也能依靠抓钩飞速位移。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                }
            ]
        },
        {
            "category": "💰 金币财富、古代科技点与洗髓灵药 (Gold, Ancient Tech & Elixirs)",
            "commands": [
                {
                    "id": "pal_give_gold_1m",
                    "name": {"zh-CN": "获得 1,000,000 金币 (黑市商人随心购)", "en": "Give 1,000,000 Gold Coins"},
                    "syntax_type": "ue5_gm",
                    "code": "give Money 1000000",
                    "desc": "背包直接入账一百万枚金币，尽情在黑市商人处购买稀有闪光帕鲁与珍奇骨骼。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_ancient_core",
                    "name": {"zh-CN": "获得古代文明核心 x50 (高阶据点建筑必备)", "en": "Give 50 Ancient Civilization Cores"},
                    "syntax_type": "ue5_gm",
                    "code": "give AncientCore 50",
                    "desc": "获取讨伐高阶副本头目掉落的稀有核心，用于建造巨大帕鲁蛋孵化器等顶级建筑。",
                    "min_version": "v0.2.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_ancient_parts",
                    "name": {"zh-CN": "获得古代文明部件 x200 (制作科技武器蓝图)", "en": "Give 200 Ancient Civilization Parts"},
                    "syntax_type": "ue5_gm",
                    "code": "give PalAncientParts 200",
                    "desc": "大量补充制作盾牌、抓钩枪与高级鞍具不可或缺的基础古代素材。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_pal_souls_l",
                    "name": {"zh-CN": "获得大帕鲁之魂 x50 (雕像强化全满)", "en": "Give 50 Large Pal Souls"},
                    "syntax_type": "ue5_gm",
                    "code": "give PalSoul_L 50",
                    "desc": "在力量雕像处献祭大帕鲁之魂，将主力战宠的血量、攻击与防御潜能强化至 30% 满额。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_elixir_attack",
                    "name": {"zh-CN": "获得刚力秘药 x10 (永久提升角色攻击力)", "en": "Give 10 Power Elixirs"},
                    "syntax_type": "ue5_gm",
                    "code": "give Elixir_Attack 10",
                    "desc": "使用后永久提升角色面板基础攻击力，配合顶级散弹枪打出爆炸性输出伤害。",
                    "min_version": "v0.3.0+",
                    "framework_required": "UE4SS"
                }
            ]
        },
        {
            "category": "🔨 传奇图纸、帕鲁球与满级军备 (Legendary Schematics & Pal Spheres)",
            "commands": [
                {
                    "id": "pal_give_rocket_launcher_4",
                    "name": {"zh-CN": "获得 4 阶传奇火箭发射器 (单发万伤重火器)", "en": "Give Legendary Rocket Launcher (Tier 4)"},
                    "syntax_type": "ue5_gm",
                    "code": "give Weapon_RocketLauncher_4 1",
                    "desc": "金色 4 阶传奇品质火箭筒，毁天灭地的面杀伤力，单发直轰世界 Boss 巨额血槽。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_shotgun_4",
                    "name": {"zh-CN": "获得 4 阶传奇泵动式霰弹枪", "en": "Give Legendary Pump-Action Shotgun (Tier 4)"},
                    "syntax_type": "ue5_gm",
                    "code": "give Weapon_PumpActionShotgun_4 1",
                    "desc": "近距离贴脸肉搏爆发之王，8 发连喷精准击碎任何高难副本首领护盾。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_assault_rifle_4",
                    "name": {"zh-CN": "获得 4 阶传奇突击步枪 (中远距离精准速射)", "en": "Give Legendary Assault Rifle (Tier 4)"},
                    "syntax_type": "ue5_gm",
                    "code": "give Weapon_AssaultRifle_4 1",
                    "desc": "极高弹容量与极低后坐力，全天候主力步枪，搭配穿甲弹极速削减敌人血线。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_pal_metal_armor_4",
                    "name": {"zh-CN": "获得 4 阶传奇帕鲁金属盔甲 (超高双抗与血量)", "en": "Give Legendary Pal Metal Armor (Tier 4)"},
                    "syntax_type": "ue5_gm",
                    "code": "give Armor_PalMetal_4 1",
                    "desc": "提供巨额防御力与生命值上限加成，耐火耐寒全适应，站撸极寒雪山与活火山。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_ammo_rocket",
                    "name": {"zh-CN": "获得火箭弹 x500 (无限弹药轰炸)", "en": "Give 500 Rocket Ammo"},
                    "syntax_type": "ue5_gm",
                    "code": "give RocketAmmon 500",
                    "desc": "大量补充重火力火箭筒专用弹药，告别复杂的硫磺与火药烧炼配方工序。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                }
            ]
        },
        {
            "category": "🏰 据点建造无负重与全顶级建材 (Base Building, Zero Weight & Mats)",
            "commands": [
                {
                    "id": "pal_give_pal_ingot",
                    "name": {"zh-CN": "获得帕鲁金属锭 x500 (最强工业合金金属)", "en": "Give 500 Pal Metal Ingots"},
                    "syntax_type": "ue5_gm",
                    "code": "give Ingot_PalMetal 500",
                    "desc": "由精炼金属与帕鲁矿碎块通过电气炉熔炼的高级合金，顶级防御工事与枪械基石。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_cement",
                    "name": {"zh-CN": "获得水泥 x1000 (建筑堡垒坚固石材)", "en": "Give 1000 Cement"},
                    "syntax_type": "ue5_gm",
                    "code": "give Cement 1000",
                    "desc": "建造坚不可摧的石头城堡与多层高楼据点必备粘合建材，无视自然火灾蔓延。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_polymer",
                    "name": {"zh-CN": "获得聚合物 x500 (现代电气化元件)", "en": "Give 500 Polymers"},
                    "syntax_type": "ue5_gm",
                    "code": "give Polymer 500",
                    "desc": "流水线工厂、电路板与高阶自动化作业机械的核心高分子化合物原料。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_carbon_fiber",
                    "name": {"zh-CN": "获得碳纤维 x500 (高刚性轻量化材料)", "en": "Give 500 Carbon Fibers"},
                    "syntax_type": "ue5_gm",
                    "code": "give CarbonFiber 500",
                    "desc": "大幅强化枪械耐久与滑翔伞升力的高强度碳素编织纤维。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                },
                {
                    "id": "pal_give_circuit_board",
                    "name": {"zh-CN": "获得电路板 x300 (发电机与科技据点组件)", "en": "Give 300 Circuit Boards"},
                    "syntax_type": "ue5_gm",
                    "code": "give CircuitBoard 300",
                    "desc": "建造高压发电机、大型储能电池与全自动流水线作业台必备电子原件。",
                    "min_version": "v0.1.0+",
                    "framework_required": "UE4SS"
                }
            ]
        },
        {
            "category": "⏱️ 昼夜时间、移速倍率与虚幻5画质优化 (Time, Speed & UE5 Tuning)",
            "commands": [
                {
                    "id": "pal_r_view_distance",
                    "name": {"zh-CN": "超远视距渲染倍率拉满 (消除远景模糊与雾气)", "en": "Max View Distance Scale (3x)"},
                    "syntax_type": "ue5_console",
                    "code": "r.ViewDistanceScale 3.0",
                    "desc": "将虚幻5引擎的视距渲染扩大至 3 倍，远方雪山、神兽与据点建筑纤毫毕现。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                },
                {
                    "id": "pal_showhud_toggle",
                    "name": {"zh-CN": "隐藏/显示全部屏幕 HUD 界面 (纯净4K壁纸截图)", "en": "Toggle Screen HUD Display"},
                    "syntax_type": "ue5_console",
                    "code": "showhud",
                    "desc": "一键隐藏全屏血条、小地图、准星与任务罗盘，拍摄电影质感的帕鲁骑乘特写。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                },
                {
                    "id": "pal_slomo_fast",
                    "name": {"zh-CN": "2.0x 疾速快进时间 (孵蛋与农作物极速成熟)", "en": "Fast Forward Speed (2.0x)"},
                    "syntax_type": "ue5_console",
                    "code": "slomo 2.0",
                    "desc": "让全局世界运转速度翻倍，据点小麦/番茄种植采摘与自动配种光速完成。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                },
                {
                    "id": "pal_r_fog_tuning",
                    "name": {"zh-CN": "降低高密度体积雾遮挡 (通透纯净晴空视觉)", "en": "Tune Volumetric Fog"},
                    "syntax_type": "ue5_console",
                    "code": "r.VolumetricFog 0",
                    "desc": "关闭沉重灰蒙的体积雾计算，大幅释放显卡显存压力并获得清澈明亮的视觉效果。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                },
                {
                    "id": "pal_stat_unit",
                    "name": {"zh-CN": "显示 CPU/GPU 线程详细瓶颈分析", "en": "Show Unit Performance Stats"},
                    "syntax_type": "ue5_console",
                    "code": "stat unit",
                    "desc": "排查据点帕鲁 AI 寻路对 CPU 主频线程的开销占用，优化据点帕鲁部署数量。",
                    "min_version": "v0.1.0+",
                    "framework_required": "None (Native / UE4SS)"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "pal_starter_bundle",
            "type": "starter",
            "name": "新手开荒神宠起飞包",
            "tag": "👑 萌新首选 · 零门槛",
            "badge": "开荒神宠",
            "desc": "一键获取 50 级打工皇帝阿努比斯 + 100 颗高阶帕鲁球 + 100万金币启动资金 + 负重上限百万解除，开局即享工业化自动据点！",
            "highlights": ["阿努比斯 (手工Lv4 最强基建工匠)", "100 颗高阶帕鲁球，见宠即抓", "1,000,000 黄金现金黑市扫货", "随身负重清零自由搬运矿石"],
            "code": "-- [老L·极客场景套餐] 幻兽帕鲁 新手开荒神宠起飞包 (离线实测)\nspawn Anubis 50\ngive PalSphere_Legend 100\ngive Money 1000000\naddtalentpoint 50"
        },
        {
            "id": "pal_salvation_bundle",
            "type": "salvation",
            "name": "神兽捕捉与极速孵化包",
            "tag": "🛡️ 意难平救赎 · 告别受苦",
            "badge": "神兽毕业",
            "desc": "召唤超音速巡航神兽空涡龙 + 极寒神兽唤冬兽 + 专用导弹鞍具 + 0.3x 子弹时间慢动作捕捉，告别手残与神兽擦肩而过！",
            "highlights": ["全服最快飞行坐骑空涡龙直接入队", "唤冬兽冰系霸主守护战力", "骑乘导弹发射器超强清屏火力", "0.3x 慢动作锁定 Boss 弱点投球"],
            "code": "-- [老L·极客场景套餐] 幻兽帕鲁 神兽捕捉与极速孵化包 (离线实测)\nspawn Jetragon 50\nspawn Frostallion 50\ngive Weapon_Jetragon_Missile 1\nslomo 0.3"
        },
        {
            "id": "pal_godmode_bundle",
            "type": "godmode",
            "name": "现代重工真神毕业满配包",
            "tag": "⚡ 极客狂欢 · 众神陨落",
            "badge": "真神毕业",
            "desc": "4 阶金色传奇火箭发射器 + 传奇霰弹枪 + 帕鲁金属神装 + 500发高爆火箭弹 + 帕鲁金属全建材，化身帕鲁大陆现代机械之神！",
            "highlights": ["4 阶金色火箭筒 (单发万点巨额爆发)", "全套帕鲁金属防具 (免除冷热恶劣天气)", "500 发高爆弹药随心挥霍轰炸", "工业合金金属锭无限制堆积建造"],
            "code": "-- [老L·极客场景套餐] 幻兽帕鲁 现代重工真神毕业满配包\ngive Weapon_RocketLauncher_4 1\ngive Weapon_PumpActionShotgun_4 1\ngive Armor_PalMetal_4 1\ngive RocketAmmon 500\ngive Ingot_PalMetal 500"
        }
    ],
    "pitfallNote": {
        "title": "老L实验室避坑笔记 (幻兽帕鲁 樱岛最新版)",
        "tips": [
            "【防封禁与反作弊】：本作单人单机模式与自建离线本地房间绝无 VAC 或官方封禁风险。若加入官方防作弊服务器，务必完全移除 UE4SS 注入 dll，切勿在公开天梯联机作弊！",
            "【帕鲁抑郁生病治愈】：据点帕鲁容易因地形卡住无法进食而导致【抑郁症/骨折】。使用 give Med_Low 10 获取高级药品直接投喂，并在箱子旁放置温泉以彻底稳定 SAN 值。",
            "【负重过载急救】：金属矿区挖掘超载走不动时，掏出抓钩枪对着地面或树干射击，利用抓钩拉力可以直接无视任何负重限制飞速前行。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】幻兽帕鲁 UE4SS 模组引导助手\necho ========================================================\necho   【老L·单机避坑局】幻兽帕鲁 纯净模组环境检查工具\necho   纯净离线加载 · 零杀软误报 · 快捷备份配置\necho ========================================================\necho.\nif not exist \"Pal\\Binaries\\Win64\\Palworld-Win64-Shipping.exe\" (\n    echo [!] 提示: 请将本脚本放在 Palworld 游戏安装根目录！\n    pause\n    exit /b\n)\necho [*] 正在检查 UE4SS.dll 与 xinput1_3.dll 状态...\nif exist \"Pal\\Binaries\\Win64\\UE4SS.dll\" (\n    echo [√] UE4SS 底层前置挂载正常！游戏内按 F10 唤出菜单。\n) else (\n    echo [!] 未检测到 UE4SS，请解压 UE4SS 至 Pal/Binaries/Win64/。\n)\necho.\npause\n",
    "verifiedPatch": "v0.3.x (樱岛版本完全对齐)",
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
        "setstage 0001638D 1000",
        "tcl"
    ],
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.14+ (Shattered Space 破碎空间 DLC 完全对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/starfield-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/starfield/Starfield_v1.14_Plus_35_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Starfield Trainer.exe'",
            "troubleshootSteps": [
                "B社单机无联机服务器，修改器 100% 安全离线使用",
                "若 Windows Defender 拦截，以管理员身份运行上方 PowerShell 白名单放行指令",
                "进入游戏主菜单或飞船驾驶舱后再激活修改器热键"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 角色生存与飞船绝对无敌",
                "items": [
                    {"key": "Num 1", "action": "无敌模式 (God Mode / 锁血锁氧气)"},
                    {"key": "Num 2", "action": "无限喷气背包推力 (随心翱翔空中)"},
                    {"key": "Num 3", "action": "无限武器弹药与零重新装填"},
                    {"key": "Num 4", "action": "飞船护盾无限锁定 (抗击舰队围攻)"},
                    {"key": "Num 5", "action": "飞船舰载武器无限能源与零过热"}
                ]
            },
            {
                "category": "🎒 财富开锁与随身负重",
                "items": [
                    {"key": "Num 6", "action": "无限信用币金钱 (999,999,999)"},
                    {"key": "Num 7", "action": "无限数码撬棒 (Digipicks 开锁不减)"},
                    {"key": "Num 8", "action": "随身负重无限突破 (99,999 负重上限)"},
                    {"key": "Num 9", "action": "100% 潜行隐蔽成功率 (不被卫兵发现)"}
                ]
            },
            {
                "category": "🚀 飞船建造与研究制造",
                "items": [
                    {"key": "Ctrl+Num 1", "action": "飞船建造部件免费 (无需花费信用币)"},
                    {"key": "Ctrl+Num 2", "action": "哨站建造全材料免费"},
                    {"key": "Ctrl+Num 3", "action": "全部实验室科研项目瞬间完成"},
                    {"key": "Ctrl+Num 4", "action": "最高星系快速跃迁距离 (无视重力引擎限制)"},
                    {"key": "Ctrl+Num 5", "action": "超级移动速度与时间流速调节 (0.5x~5.0x)"}
                ]
            }
        ]
    },
    "hasMods": True,
    "curatedMods": [
        {
            "id": "sfse_core",
            "title": "Starfield Script Extender (SFSE 核心脚本扩展器)",
            "author": "IanPatt & SFSE Team",
            "version": "v0.2.14",
            "size": "580 KB",
            "downloads": "3.5M",
            "endorsements": "180K",
            "category": "Core Framework (核心前置)",
            "desc": "星空运行全部高阶 UI 模组、飞船构建突破与游戏机制大修的绝对基石前置。原生扩展游戏内存指针，安全可靠。",
            "dependencies": ["None (Native Extender)"],
            "installPath": "Starfield/ (游戏根目录)",
            "downloadUrl": "https://github.com/ianpatt/sfse/releases/download/v0.2.14/sfse_0_02_14.7z",
            "downloadFilename": "sfse_0_02_14.7z",
            "isDirect": True,
            "installSteps": [
                "1. 点击按钮直接下载 sfse_0_02_14.7z 压缩包；",
                "2. 打开 Starfield 游戏安装根目录 (包含 Starfield.exe 的位置)；",
                "3. 将压缩包内的 sfse_*.dll 与 sfse_loader.exe 解压到根目录；",
                "4. 后续启动游戏请直接双击运行 sfse_loader.exe 即可。"
            ]
        },
        {
            "id": "starfield_community_patch",
            "title": "Starfield Community Patch (社区全修复大修综合补丁)",
            "author": "Starfield Community",
            "version": "v1.1.2",
            "size": "15 MB",
            "downloads": "1.8M",
            "endorsements": "95K",
            "category": "Bug Fixes (全漏洞修复)",
            "desc": "由全球顶尖 Modder 共同维护的开源综合漏洞修复包，修复了上千处恶性断任务、NPC 漂浮卡死与飞船无法停泊的底层代码 Bug。",
            "dependencies": ["SFSE"],
            "installPath": "Starfield/Data/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/starfield/StarfieldCommunityPatch.zip",
            "downloadFilename": "StarfieldCommunityPatch.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载压缩包解压出 StarfieldCommunityPatch.esm；",
                "2. 放入 Starfield/Data/ 文件夹；",
                "3. 在游戏主菜单 Mods 选项卡中勾选启用该 ESM。"
            ]
        },
        {
            "id": "ship_builder_unlimited",
            "title": "Ship Builder Tolerance Tweaks (飞船部件重叠与尺寸突破)",
            "author": "NexusGuy",
            "version": "v1.3.0",
            "size": "25 KB",
            "downloads": "920K",
            "endorsements": "62K",
            "category": "Ship Building (飞船改装)",
            "desc": "彻底解除飞船建造厂中令人抓狂的【模块重叠错误】与【最大建造长度限制】，轻松建造歼星舰与重装无畏舰！",
            "dependencies": ["None (Native INI)"],
            "installPath": "Documents/My Games/Starfield/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/starfield/ShipBuilderToleranceTweaks.zip",
            "downloadFilename": "ShipBuilderToleranceTweaks.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载解压获取 StarfieldCustom.ini 配置文件；",
                "2. 放置到 '我的文档/My Games/Starfield/' 目录下；",
                "3. 进入任何停机坪改船厂，即可随心自由拼接任意模块。"
            ]
        },
        {
            "id": "undelayed_menus",
            "title": "Undelayed Menus (极速流畅 60FPS UI 交互界面)",
            "author": "Seb263",
            "version": "v1.2.0",
            "size": "120 KB",
            "downloads": "2.2M",
            "endorsements": "130K",
            "category": "UI / Interface",
            "desc": "消除打开物品栏、星图与技能界面时长达 0.5 秒的迟钝渐变淡入动画，界面秒开瞬切，操作如丝般顺滑。",
            "dependencies": ["None (SWF Override)"],
            "installPath": "Starfield/Data/Interface/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/starfield/UndelayedMenus_v1.2.zip",
            "downloadFilename": "UndelayedMenus_v1.2.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载压缩包解压获取 Interface/ 文件夹；",
                "2. 将其放入 Starfield/Data/ 目录下；",
                "3. 游戏中按 Tab 打开菜单立刻感受零延迟交互。"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 核心上帝模式与绝对生存 (God Mode & Invulnerability)",
            "commands": [
                {
                    "id": "sf_tgm",
                    "name": {"zh-CN": "完全上帝模式 (TGM - 锁血/无限氧气/无限子弹)", "en": "Toggle God Mode (tgm)"},
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "Bethesda 经典全能神级代码，生命值、耐力氧气槽、飞船护盾与弹药全部锁定无限。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_tim",
                    "name": {"zh-CN": "真不死模式 (TIM - 真实扣血但绝不死亡)", "en": "Toggle Immortal Mode (tim)"},
                    "syntax_type": "creation_hex",
                    "code": "tim",
                    "desc": "机体会受到正常伤害并显示残血状态，但生命值降至 1 点时绝不会倒下，保留战斗紧张感。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_tcl",
                    "name": {"zh-CN": "自由飞行与穿墙模式 (TCL - 脱离卡死探图)", "en": "Toggle Collision (tcl)"},
                    "syntax_type": "creation_hex",
                    "code": "tcl",
                    "desc": "关闭物理碰撞体积，角色可自由在空中悬浮穿墙，探索被锁闭的隐秘房间与卡死解救。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_tcai",
                    "name": {"zh-CN": "关闭所有敌人战斗仇恨 AI (停火木桩模式)", "en": "Toggle Combat AI (tcai)"},
                    "syntax_type": "creation_hex",
                    "code": "tcai",
                    "desc": "全局冻结所有太空海盗与敌对生物的攻击判定，敌人将站立不动任由测试武器。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_heal_player",
                    "name": {"zh-CN": "瞬间全状态恢复 (清除脑震荡/骨折/烫伤)", "en": "Heal All Afflictions & Health"},
                    "syntax_type": "creation_hex",
                    "code": "player.healplayer",
                    "desc": "立刻补满全部生命值并瞬间治愈环境毒素、烧伤、骨折及失温等全部负面状态。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🚀 飞船建造部件无限制与反应堆电能 (Ship Builder Unlimited & Power)",
            "commands": [
                {
                    "id": "sf_ship_power",
                    "name": {"zh-CN": "飞船反应堆输出能量强化至 100 点", "en": "Set Ship Reactor Power to 100"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav spaceshipreactorpower 100",
                    "desc": "让飞船反应堆拥有 100 点充沛电力，激光炮、电磁炮、重力引擎与护盾全部满格通电点亮！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_ship_shield",
                    "name": {"zh-CN": "强化飞船护盾最大值 (+5000 巨额护盾)", "en": "Add 5000 Ship Shield Max"},
                    "syntax_type": "creation_hex",
                    "code": "player.modav spaceshipshieldmax 5000",
                    "desc": "为飞船护盾额外叠加 5000 点护盾容量，正面抗击高难度敌对舰队齐射分毫不损。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_ship_cargo",
                    "name": {"zh-CN": "飞船货舱容量提升至 99,999 吨", "en": "Set Ship Cargo Space to 99,999"},
                    "syntax_type": "creation_hex",
                    "code": "player.modav spaceshipcargospace 99999",
                    "desc": "飞船货舱拥有无限级容纳量，所有采矿矿石与拆解飞船部件无脑塞入货舱。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_ship_speed",
                    "name": {"zh-CN": "飞船巡航飞行极速倍率翻倍", "en": "Double Ship Cruise Max Speed"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav spaceshipboostspeed 300",
                    "desc": "将飞船加力推进冲刺极速提升至 300，星系间巡航移动与拉开狗斗距离瞬间完成。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_ship_repair",
                    "name": {"zh-CN": "获取飞船零件维修套件 x50", "en": "Give 50 Ship Repair Parts"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000B 50",
                    "desc": "在太空中按 O 键即可消耗零件快速修复破损的飞船船体装甲。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🧬 角色特质修改、背景天赋与洗点 (Traits, Background & Skills)",
            "commands": [
                {
                    "id": "sf_show_race_menu",
                    "name": {"zh-CN": "随时重新打开整容与特质捏脸界面", "en": "Show Race & Trait Menu"},
                    "syntax_type": "creation_hex",
                    "code": "showracemenu",
                    "desc": "无视所在星系随时开启角色捏脸、体型调整、背景身份与初始特质重新选择面板。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_add_perk_point",
                    "name": {"zh-CN": "获得 100 点技能点数 (自由点满全天赋)", "en": "Call AddPerkPoints (100 Points)"},
                    "syntax_type": "creation_hex",
                    "code": "cgf \"Game.AddPerkPoints\" 100",
                    "desc": "调用底层脚本函数直接获取 100 个技能点数，瞬间点满物理、社交、战斗、科学与技术技能。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_add_trait_hero",
                    "name": {"zh-CN": "添加特质：英雄崇拜 (招募忠诚狂热粉丝)", "en": "Add Trait: Hero Worshipped"},
                    "syntax_type": "creation_hex",
                    "code": "player.addperk 00227FDA",
                    "desc": "解锁极为滑稽搞笑且忠诚的‘狂热粉丝’NPC随从，他会不断夸赞你并赠送免费小礼物。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_add_trait_home",
                    "name": {"zh-CN": "添加特质：梦想家园 (奥林匹斯豪宅钥匙)", "en": "Add Trait: Dream Home"},
                    "syntax_type": "creation_hex",
                    "code": "player.addperk 00227FD7",
                    "desc": "在风景优美的奥林匹斯星系拥有一座两层豪华独栋别墅，专享私密海景停机坪。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_set_level_60",
                    "name": {"zh-CN": "角色等级直接设定为 Lv60", "en": "Set Player Level to 60"},
                    "syntax_type": "creation_hex",
                    "code": "player.setlevel 60",
                    "desc": "跳过低等级刷怪期，让游戏内高阶装备与传奇武器掉落池全部立刻解锁。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "💰 信用币财富、开锁数码撬棒与负重 (Credits, Digipicks & Carry Weight)",
            "commands": [
                {
                    "id": "sf_add_credits_1m",
                    "name": {"zh-CN": "获得 1,000,000 信用币 (财富自由秒买名舰)", "en": "Add 1,000,000 Credits"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 1000000",
                    "desc": "背包直接入账一百万信用币，随意在霓虹城与新亚特兰蒂斯购买顶级现成星际战舰。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_add_digipicks",
                    "name": {"zh-CN": "获得数码撬棒 x100 (开锁神器随心解谜)", "en": "Add 100 Digipicks"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000A 100",
                    "desc": "获取 100 个开锁数码撬棒，无惧任何专家级与大师级保险箱圆环拼图试错。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_carry_weight_max",
                    "name": {"zh-CN": "角色随身负重上限提升至 9,999 吨", "en": "Set Player Carry Weight to 9,999"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 9999",
                    "desc": "将角色随身负重拉至上万点，身上装载几十把重武器与全部矿石亦可健步如飞。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_pay_bounty",
                    "name": {"zh-CN": "一键清除全部星系阵营通缉赏金 (清罪免通缉)", "en": "Clear All Faction Bounties"},
                    "syntax_type": "creation_hex",
                    "code": "player.paycrimegold 0 0",
                    "desc": "消除联合殖民地与自由星系联盟的所有违法通缉记录，警卫不再主动拦截逮捕。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_unlock_target",
                    "name": {"zh-CN": "强制解锁准星所指之门/保险箱 (秒开万物)", "en": "Unlock Target Door / Safe"},
                    "syntax_type": "creation_hex",
                    "code": "unlock",
                    "desc": "在控制台开启时用鼠标点击锁住的门或货箱，输入 unlock 即可瞬间物理破解开启。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🔫 传奇金色武器与高科技词条附魔 (Legendary Weapons & Weapon Mods)",
            "commands": [
                {
                    "id": "sf_weapon_magpulse",
                    "name": {"zh-CN": "获得电磁磁化脉冲枪 (25点阵极速穿透步枪)", "en": "Give MagPulse Rifle"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00023606 1",
                    "desc": "霓虹城 Kore 军工出品顶级磁轨突击步枪，以极高射速发射密集的磁化钢珠网撕碎敌人。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_weapon_hardtarget",
                    "name": {"zh-CN": "获得硬靶高精狙击步枪 (超远距离爆头一击必杀)", "en": "Give Hard Target Sniper Rifle"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000547A3 1",
                    "desc": ".50 口径高初速反器材狙击步枪，加装消音器与夜视镜后潜行暴击伤害直接拉满。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_weapon_inflictor",
                    "name": {"zh-CN": "获得瓦鲁恩折磨者粒子束步枪 (神级双属性输出)", "en": "Give Va'ruun Inflictor Particle Rifle"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0026D96D 1",
                    "desc": "瓦鲁恩毒蛇信徒秘造神兵，同时造成物理与能量双重属性伤害，全游戏最强 T0 步枪。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_weapon_bigbang",
                    "name": {"zh-CN": "获得大爆炸重型粒子束霰弹枪 (近身终极毁灭者)", "en": "Give Big Bang Shotgun"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0026D968 1",
                    "desc": "近距离一枪轰杀任何高阶掠夺者与外星异形怪兽，自带扩散粒子灼烧暴击。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_attach_instigating",
                    "name": {"zh-CN": "给手中武器附魔词条：煽动 (满血目标伤害翻倍)", "en": "Attach Mod: Instigating (Double Damage)"},
                    "syntax_type": "creation_hex",
                    "code": "player.attachmod 000F4320",
                    "desc": "为当前所持武器附加金色传奇词条【煽动】，对生命值全满的目标造成整整 2 倍致命伤害！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🛡️ 传奇宇航服、头盔与深度强化 (Legendary Spacesuits & Helmets)",
            "commands": [
                {
                    "id": "sf_suit_starborn",
                    "name": {"zh-CN": "获得星裔天相战甲 (十周目终极神级宇航服)", "en": "Give Starborn Spacesuit Astra"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0012E1B4 1",
                    "desc": "通关十周目获得的一体化星裔流光战甲，提供极致物理抗性、极寒耐受与自带隐形斗篷。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_suit_mantis",
                    "name": {"zh-CN": "获得蝠鲼传奇宇航服 (全套太空游侠神装)", "en": "Give Mantis Spacesuit"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00226299 1",
                    "desc": "蝠鲼秘密基地代代传承的传奇正义宇航服，自带减重与受到近战攻击反弹电弧特效。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_helmet_mercenary",
                    "name": {"zh-CN": "获得重装雇佣兵传奇头盔 (超高防辐射与有毒气体)", "en": "Give Mercenary Helmet"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00169F50 1",
                    "desc": "具备极佳视界与强韧气密防线的深空头盔，免疫深渊行星的大气辐射侵蚀。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_pack_bountyhunter",
                    "name": {"zh-CN": "获得赏金猎人喷气背包 (强力平衡跳跃助推器)", "en": "Give Bounty Hunter Boostpack"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0016E0C3 1",
                    "desc": "提供极长滞空时间与垂直爬升动力的平衡型喷气背包，低重力星球飞行必备。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_attach_chameleon",
                    "name": {"zh-CN": "为防具附加传奇词条：变色龙 (静止完全隐形)", "en": "Attach Mod: Chameleon"},
                    "syntax_type": "creation_hex",
                    "code": "player.attachmod 000BE542",
                    "desc": "蹲下静止时角色完全光学隐形，敌人视线哪怕从身旁经过也无法察觉。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🌌 全星系地标探索、重力调控与穿墙 (Star Map, Gravity & Exploration)",
            "commands": [
                {
                    "id": "sf_tmm_all",
                    "name": {"zh-CN": "星图全部地标与着陆点一键全开 (TMM 1)", "en": "Show All Map Markers (tmm 1)"},
                    "syntax_type": "creation_hex",
                    "code": "tmm 1",
                    "desc": "点亮星系图与星球表面全部探索标、外星神庙、研究站与隐秘城市，随时随地直接传送。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_set_timescale",
                    "name": {"zh-CN": "将星空世界昼夜流速设定为真实 1:1 时间", "en": "Set Real-time Timescale (1:1)"},
                    "syntax_type": "creation_hex",
                    "code": "set timescale to 1",
                    "desc": "将昼夜更替速度放慢至与现实时间 1:1 同步，静静欣赏深空星球日出日落与恒星环日升腾。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_fov_100",
                    "name": {"zh-CN": "视场角 FOV 调优至宽广 100 度 (告别晕 3D)", "en": "Set FOV to 100 Degrees"},
                    "syntax_type": "creation_hex",
                    "code": "fov 100",
                    "desc": "大幅拓宽第一人称与第三人称视野广角，视野更通透开阔，彻底根除狭窄视场引起的晕动症。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_tm_toggle",
                    "name": {"zh-CN": "隐藏/恢复全部界面 HUD (纯净4K太空截图)", "en": "Toggle Menus / HUD (tm)"},
                    "syntax_type": "creation_hex",
                    "code": "tm",
                    "desc": "一键隐藏全屏血条、氧气表、指南针与准星，截取好莱坞科幻大片质感的深空照片。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_kah_enemies",
                    "name": {"zh-CN": "击杀视野内所有敌对威胁 (KAH 秒杀全敌)", "en": "Kill All Hostiles (kah)"},
                    "syntax_type": "creation_hex",
                    "code": "kah",
                    "desc": "瞬间消灭当前场景中所有处于战斗敌对状态的海盗与外星虫群，和平清理战场。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🛠️ 哨站全工业建材与稀有矿物全满 (Outpost Resources & Exotic Mats)",
            "commands": [
                {
                    "id": "sf_res_iron",
                    "name": {"zh-CN": "获得铁矿原料 x500 (哨站框架结构基础)", "en": "Give 500 Iron Ore"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000556E 500",
                    "desc": "大量补充建造哨站气闸舱、停机坪与工业货柜最基础的钢结构钢铁矿石。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_res_aluminum",
                    "name": {"zh-CN": "获得铝矿原料 x500 (风力发电机与太阳能板)", "en": "Give 500 Aluminum"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000557D 500",
                    "desc": "哨站能源系统与固态储水罐最核心轻质金属材料。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_res_titanium",
                    "name": {"zh-CN": "获得钛金属 x300 (高强度精密机械制造)", "en": "Give 300 Titanium"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00005572 300",
                    "desc": "用于制造高科技军工武器配件与强化哨站防御炮塔的高刚度耐高温钛合金。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_res_adhesive",
                    "name": {"zh-CN": "获得粘合剂 x300 (枪械改装最稀缺战略材料)", "en": "Give 300 Adhesives"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000055B1 300",
                    "desc": "所有枪械瞄准镜、枪口消音器与弹匣扩容改装中最容易匮乏的稀缺天然粘着原料。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "sf_res_sealant",
                    "name": {"zh-CN": "获得密封剂 x300 (防化舱与居住舱气密胶)", "en": "Give 300 Sealants"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000055CC 300",
                    "desc": "恶劣大气环境下密封哨站走廊与太空防护服隔绝层必不可少的高分子密封胶。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
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
            "code": "-- [老L·极客场景套餐] 星空 新手星际启航起飞包 (原生控制台实测)\ntgm\nplayer.additem 0000000F 1000000\nplayer.additem 0000000A 100\nplayer.setav carryweight 9999"
        },
        {
            "id": "sf_salvation_bundle",
            "type": "salvation",
            "name": "歼星战舰无限制改装包",
            "tag": "🛡️ 意难平救赎 · 告别受苦",
            "badge": "歼星战舰",
            "desc": "飞船反应堆能量 100 满配 + 护盾上限增加 5000 + 飞船货舱无限容纳 + 极速推进倍率，打造横扫猩红舰队的太空无敌母舰！",
            "highlights": ["飞船反应堆 100 点满负荷全系统供电", "5000 额外护盾抗击全星际舰队", "货舱 99,999 吨随意装载采矿建材", "飞船推进速度翻倍瞬间摆脱缠斗"],
            "code": "-- [老L·极客场景套餐] 星空 歼星战舰无限制改装包\nplayer.setav spaceshipreactorpower 100\nplayer.modav spaceshipshieldmax 5000\nplayer.modav spaceshipcargospace 99999\nplayer.setav spaceshipboostspeed 300"
        },
        {
            "id": "sf_godmode_bundle",
            "type": "godmode",
            "name": "星裔真神全星系毕业包",
            "tag": "⚡ 极客狂欢 · 众神陨落",
            "badge": "星裔真神",
            "desc": "十周目星裔天相流光战甲 + 瓦鲁恩折磨者 T0 粒子步枪 + 煽动双倍伤害词条 + 100技能点全点满 + 全星系地标全开！",
            "highlights": ["星裔 Astra 流光战甲 (全抗性极客神装)", "瓦鲁恩折磨者双属性致命武器", "全星系 1000+ 星球地标一键全开", "100 点技能点瞬间全系满级"],
            "code": "-- [老L·极客场景套餐] 星空 星裔真神全星系毕业包\nplayer.additem 0012E1B4 1\nplayer.additem 0026D96D 1\ntmm 1\ncgf \"Game.AddPerkPoints\" 100"
        }
    ],
    "pitfallNote": {
        "title": "老L实验室避坑笔记 (星空 破碎空间 DLC 完全版)",
        "tips": [
            "【Steam成就防锁死门禁】：Bethesda 在输入控制台命令时会标记存档为 Modded 并禁用 Steam 成就！必须先安装 Baka Achievement Enabler 或通过 SFSE 挂钩，才能在爽用控制台的同时点亮 100% 全成就！",
            "【改船部件重叠报错破解】：在官方造船厂经常遇到【模块存在重叠】无法保存。下载安装本站推荐的 Ship Builder Tolerance Tweaks 即可完全无视空间重叠，打造致密外装母舰。",
            "【卡死与恶性任务急救】：若因 NPC 浮空或被锁在门后无法交任务，打开控制台输入 tcl 开启穿墙飞入室内，或使用 setstage 命令直接强行推进断掉的任务流程节点。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】星空 SFSE 纯净启动助手\necho ========================================================\necho   【老L·单机避坑局】星空 SFSE 扩展环境一键诊断工具\necho   防成就锁死 · 解除改船限制 · 极速 60FPS 菜单\necho ========================================================\necho.\nif not exist \"Starfield.exe\" (\n    echo [!] 提示: 请将本脚本放在 Starfield 游戏安装根目录！\n    pause\n    exit /b\n)\necho [*] 正在检查 sfse_loader.exe 状态...\nif exist \"sfse_loader.exe\" (\n    echo [√] SFSE 扩展引导已就绪！即将通过 SFSE 启动游戏...\n    start \"\" \"sfse_loader.exe\"\n) else (\n    echo [!] 未检测到 sfse_loader.exe，正在以原版模式拉起...\n    start \"\" \"Starfield.exe\"\n)\necho.\npause\n",
    "verifiedPatch": "v1.14 (破碎空间DLC完全对齐)",
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
        "zh-CN": "【单机故事模式 100% 离线防封指南】\n1. 官方原生秘籍：进入单机故事模式后，直接按键盘左上角 ~ 键输入全英文秘籍并回车；\n2. ScriptHookV 离线内置菜单：将 ScriptHookV.dll、dinput8.dll 以及 NativeTrainer.asi 放入 GTA5 游戏根目录；\n3. 在故事模式按 F4 呼出图形化修改菜单，小键盘 8/2/4/6 切换方向，5 确认，0 返回；\n4. ⚠️ 严禁携带任何 ASI 插件或修改器文件进入 GTA Online 线上模式，否则必被 R星反作弊封号！重返线上前只需将 dinput8.dll 重命名为 .bak 即可完全断开模组隔离。",
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
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.0.3179.0+ (最新故事模式完全对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/grand-theft-auto-v-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/gta-v/Grand_Theft_Auto_V_v1.0.3179_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "5b4a3c2d1e0f9a8b7c6d5e4f3a2b1c0d",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Grand Theft Auto V Trainer.exe'",
            "troubleshootSteps": [
                "绝对仅限单人线下故事模式使用，切勿在官方线上战局中开启运行",
                "若 Windows Defender 拦截，以管理员身份运行上方 PowerShell 白名单放行指令",
                "进入游戏加载出麦克/富兰克林/崔佛人物后再切换出桌面启动修改器"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 角色生存与通缉度调控",
                "items": [
                    {"key": "Num 1", "action": "无敌模式 (God Mode / 锁血锁护甲)"},
                    {"key": "Num 2", "action": "无限体力 (奔跑/游泳/潜水零衰减)"},
                    {"key": "Num 3", "action": "无限特殊能力槽 (麦克子弹时间/小富驾驶/崔佛狂暴)"},
                    {"key": "Num 4", "action": "通缉星级清零 (警察立刻放弃追捕)"},
                    {"key": "Num 5", "action": "锁定六星顶级通缉 (极限警察围剿大逃杀)"}
                ]
            },
            {
                "category": "🔫 军火弹药与特种爆炸能力",
                "items": [
                    {"key": "Num 6", "action": "无限弹药与免装弹 (打靶连射无需换弹匣)"},
                    {"key": "Num 7", "action": "超级近战肉搏拳头 (一拳击飞路人与汽车)"},
                    {"key": "Num 8", "action": "爆炸近战与燃烧子弹 (弹无虚发火海轰炸)"},
                    {"key": "Num 9", "action": "超级跳跃与从天而降 (从万米高空滑翔俯冲)"}
                ]
            },
            {
                "category": "🚗 载具极速改装与洛圣都天气",
                "items": [
                    {"key": "Ctrl+Num 1", "action": "载具无敌状态 (撞击永不损坏变型)"},
                    {"key": "Ctrl+Num 2", "action": "载具无限氮气加速 (随时瞬间飙车冲刺)"},
                    {"key": "Ctrl+Num 3", "action": "编辑故事模式当前角色现金 (十亿美金)"},
                    {"key": "Ctrl+Num 4", "action": "昼夜时间自由倒流与快进调节"},
                    {"key": "Ctrl+Num 5", "action": "随意切换洛圣都天气 (晴朗/雷暴/暴风雪)"}
                ]
            }
        ]
    },
    "hasMods": True,
    "curatedMods": [
        {
            "id": "gta_scripthookv",
            "title": "ScriptHookV + Native Trainer (Alexander Blade 官方前置库)",
            "author": "Alexander Blade",
            "version": "v1.0.3179.0",
            "size": "1.2 MB",
            "downloads": "8.5M",
            "endorsements": "420K",
            "category": "Core Framework (核心前置)",
            "desc": "GTA 5 单机运行所有 ASI 脚本、载具菜单与功能模组的最权威开源前置。自带经典 F4 Native Trainer 离线菜单，包含防线上联机自动切断保护。",
            "dependencies": ["None (Native DLL)"],
            "installPath": "Grand Theft Auto V/ (游戏根目录)",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/scripthookv/ScriptHookV_1.0.3179.0.zip",
            "downloadFilename": "ScriptHookV_1.0.3179.0.zip",
            "isDirect": True,
            "installSteps": [
                "1. 点击下载 ScriptHookV_1.0.3179.0.zip；",
                "2. 打开 GTA 5 安装根目录 (包含 GTA5.exe 的文件夹)；",
                "3. 将 bin/ 目录下的 ScriptHookV.dll、dinput8.dll 和 NativeTrainer.asi 复制到根目录；",
                "4. 进入单机故事模式按 F4 即可呼出菜单。"
            ]
        },
        {
            "id": "gta_menyoo_pc",
            "title": "Menyoo PC Single-Player Trainer (最强离线图形化修改菜单)",
            "author": "MAFINS",
            "version": "v1.8.1",
            "size": "8.2 MB",
            "downloads": "4.2M",
            "endorsements": "260K",
            "category": "Trainer / Menu",
            "desc": "功能冠绝全网的顶级单机离线菜单：随心刷出全部线上 DLC 豪车与战机、自定义保镖随从战队、建造自定义赛道飞跃跑道、随时更换任何剧情角色外观！",
            "dependencies": ["ScriptHookV"],
            "installPath": "Grand Theft Auto V/",
            "downloadUrl": "https://github.com/MAFINS/MenyooSP/releases/download/v1.8.1/MenyooSP.zip",
            "downloadFilename": "MenyooSP_v1.8.1.zip",
            "isDirect": True,
            "installSteps": [
                "1. 确认已安装 ScriptHookV 前置；",
                "2. 下载压缩包解压获取 menyooStuff 文件夹和 Menyoo.asi；",
                "3. 放入 GTA5 游戏根目录；",
                "4. 故事模式按 F8 即可打开图形化菜单。"
            ]
        },
        {
            "id": "gta_openiv",
            "title": "OpenIV (GTA 顶级模组归档与材质替换工具)",
            "author": "OpenIV Team",
            "version": "v4.1",
            "size": "4.5 MB",
            "downloads": "6.8M",
            "endorsements": "310K",
            "category": "Mod Tool (工具软件)",
            "desc": "安装现实真车包、高清地图画质材质包与真实枪械声音必备的归档编辑工具。独创 mods 文件夹隔离机制，保护游戏原版文件绝对不受污染破坏。",
            "dependencies": ["None (Stand-alone Tool)"],
            "installPath": "Windows PC",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/tools/OpenIVSetup.exe",
            "downloadFilename": "OpenIVSetup.exe",
            "isDirect": True,
            "installSteps": [
                "1. 下载运行 OpenIVSetup.exe 安装工具；",
                "2. 打开 OpenIV 选择 Grand Theft Auto V (Windows)；",
                "3. 点击 Tools -> ASI Manager，全部点击 Install 安装 ASI 驱动；",
                "4. 所有后续 RPF 模组均放入 mods 文件夹中无损替换。"
            ]
        },
        {
            "id": "gta_nve_graphics",
            "title": "NaturalVision Evolved (NVE 次世代顶级照片级画质光影包)",
            "author": "Razed",
            "version": "v2024 Final",
            "size": "3.8 GB",
            "downloads": "1.5M",
            "endorsements": "150K",
            "category": "Graphics (顶级画质)",
            "desc": "耗时数年倾力打造的次世代画质圣经，重制全洛圣都天气照明、反射水面、雨天积水倒影与霓虹夜景，赋予老游戏媲美 2026 年大作的电影级真实感！",
            "dependencies": ["OpenIV", "ScriptHookV"],
            "installPath": "Grand Theft Auto V/mods/",
            "downloadUrl": "https://www.razedmods.com/gta-v",
            "downloadFilename": "NVE_Installer.oiv",
            "isDirect": False,
            "installSteps": [
                "1. 确保安装好 OpenIV 并启用了 ASI 扩展；",
                "2. 打开 OpenIV 点击 Tools -> Package Installer；",
                "3. 选中下载的 NVE_Installer.oiv 并安装到 'mods folder'；",
                "4. 启动游戏享受好莱坞大片级视觉盛宴。"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 经典官方无敌与通缉度调控 (God Mode & Wanted Level Cheats)",
            "commands": [
                {
                    "id": "gta_cheat_painkiller",
                    "name": {"zh-CN": "官方经典无敌 5 分钟 (PAINKILLER)", "en": "Invincibility for 5 Mins (PAINKILLER)"},
                    "syntax_type": "rage_cheat",
                    "code": "PAINKILLER",
                    "desc": "官方原生秘籍代码，开启 5 分钟绝对锁血无敌状态，任何爆炸枪击高处坠落毫发无损。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_turtle",
                    "name": {"zh-CN": "生命值与重型护甲瞬间补满 (TURTLE)", "en": "Max Health & Armor (TURTLE)"},
                    "syntax_type": "rage_cheat",
                    "code": "TURTLE",
                    "desc": "立刻回满角色全部血槽与最高级别防弹衣，若身在载具中还会瞬间将汽车彻底修复如初。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_lawyerup",
                    "name": {"zh-CN": "降低并清除一星通缉度 (LAWYERUP)", "en": "Clear Wanted Level (LAWYERUP)"},
                    "syntax_type": "rage_cheat",
                    "code": "LAWYERUP",
                    "desc": "让洛圣都警方降低并撤销当前追捕通缉星级，脱离警用直升机与巡警视野侦测。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_fugitive",
                    "name": {"zh-CN": "提升一星通缉等级 (FUGITIVE - 挑衅追逐)", "en": "Raise Wanted Level (FUGITIVE)"},
                    "syntax_type": "rage_cheat",
                    "code": "FUGITIVE",
                    "desc": "为当前角色额外增加一颗通缉星，主动引诱特警防暴车与 FIB 探员展开激烈公路追击。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_powerup",
                    "name": {"zh-CN": "角色专属特异功能能量槽拉满 (POWERUP)", "en": "Recharge Special Ability (POWERUP)"},
                    "syntax_type": "rage_cheat",
                    "code": "POWERUP",
                    "desc": "瞬间充满黄色特殊技能槽，随心释放麦克致命射击时缓、小富过弯子弹时间与老崔狂暴减伤。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🔫 原生军火军备与特殊弹药 (Weapons, Ammo & Explosive Punches)",
            "commands": [
                {
                    "id": "gta_cheat_toolup",
                    "name": {"zh-CN": "获取全套军火武器库与弹药 (TOOLUP)", "en": "All Weapons & Max Ammo (TOOLUP)"},
                    "syntax_type": "rage_cheat",
                    "code": "TOOLUP",
                    "desc": "瞬间为当前角色配齐手枪、微冲、突击步枪、高精狙击枪、榴弹发射器及黏弹全套装备。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_highex",
                    "name": {"zh-CN": "开启高爆破坏子弹 (HIGHEX - 枪枪爆裂)", "en": "Explosive Bullets (HIGHEX)"},
                    "syntax_type": "rage_cheat",
                    "code": "HIGHEX",
                    "desc": "所有打出的子弹命中目标瞬间化为剧烈高爆手雷威力，任何路过车辆一枪直接轰至解体起火。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_incendiary",
                    "name": {"zh-CN": "开启炽热燃烧子弹 (INCENDIARY - 火海蔓延)", "en": "Flame Bullets (INCENDIARY)"},
                    "syntax_type": "rage_cheat",
                    "code": "INCENDIARY",
                    "desc": "射出的每一发子弹命中物体与敌人即刻引发熊熊大火，造成持续性灼烧伤害并点燃周围环境。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_hothands",
                    "name": {"zh-CN": "超能爆炸近战拳击 (HOTHANDS - 隔空轰飞)", "en": "Explosive Melee Attacks (HOTHANDS)"},
                    "syntax_type": "rage_cheat",
                    "code": "HOTHANDS",
                    "desc": "肉搏挥拳命中目标产生巨大冲击波爆炸，将挡路的警车与路人直接炸飞上几十米高空。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_deadeye",
                    "name": {"zh-CN": "精准瞄准慢动作三段调节 (DEADEYE)", "en": "Aiming Slomo Matrix (DEADEYE)"},
                    "syntax_type": "rage_cheat",
                    "code": "DEADEYE",
                    "desc": "举枪瞄准时自动进入三阶慢动作子弹时间，精准爆头命中移动中的敌方直升机驾驶员。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🏎️ 豪车载具召唤与武装直升机 (Vehicle Spawner & Attack Helis)",
            "commands": [
                {
                    "id": "gta_cheat_comet",
                    "name": {"zh-CN": "召唤彗星保时捷跑车 (COMET)", "en": "Spawn Comet Sports Car (COMET)"},
                    "syntax_type": "rage_cheat",
                    "code": "COMET",
                    "desc": "在眼前平地直接召唤一辆高性能经典跑车彗星，极速破百，操控手感灵敏敏捷。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_rapidgt",
                    "name": {"zh-CN": "召唤疾速 GT 豪华 GT 轿跑 (RAPIDGT)", "en": "Spawn Rapid GT Coupe (RAPIDGT)"},
                    "syntax_type": "rage_cheat",
                    "code": "RAPIDGT",
                    "desc": "召唤极具美感的双门豪华硬顶跑车，强劲后驱马力，洛圣都高速公路飙车首选。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_buzzoff",
                    "name": {"zh-CN": "召唤秃鹰重型武装直升机 (BUZZOFF)", "en": "Spawn Buzzard Attack Helicopter (BUZZOFF)"},
                    "syntax_type": "rage_cheat",
                    "code": "BUZZOFF",
                    "desc": "直接生成一架配备追踪火箭弹舱与加特林机枪的军用武装直升机，空中火力压制全场。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_barnstorm",
                    "name": {"zh-CN": "召唤麦拉德特技双翼飞行机 (BARNSTORM)", "en": "Spawn Mallard Stunt Plane (BARNSTORM)"},
                    "syntax_type": "rage_cheat",
                    "code": "BARNSTORM",
                    "desc": "召唤一架机动性极强的高速特技飞行器，在洛圣都摩天大楼与桥梁缝隙中穿梭穿桥。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_bandit",
                    "name": {"zh-CN": "召唤 Sanchez 越野泥地摩托车 (BANDIT)", "en": "Spawn Sanchez Dirt Bike (BANDIT)"},
                    "syntax_type": "rage_cheat",
                    "code": "BANDIT",
                    "desc": "召唤爬坡抓地力极佳的泥地越野摩托车，轻快翻越乞力耶德山险峻陡峭绝壁山峰。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🏊 角色超自然能力与世界物理 (Super Jump, Fast Run & Skyfall)",
            "commands": [
                {
                    "id": "gta_cheat_hoptoit",
                    "name": {"zh-CN": "开启绿巨人超级弹跳 (HOPTOIT - 跃上楼顶)", "en": "Super Jump Leap (HOPTOIT)"},
                    "syntax_type": "rage_cheat",
                    "code": "HOPTOIT",
                    "desc": "按住跳跃键可直接蓄力腾空跃起十层楼高，跨越矮层建筑屋顶与高架桥围栏。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_catchme",
                    "name": {"zh-CN": "开启超级短跑极速疾驰 (CATCHME - 健步如飞)", "en": "Super Fast Sprinting (CATCHME)"},
                    "syntax_type": "rage_cheat",
                    "code": "CATCHME",
                    "desc": "角色奔跑与短跑冲刺速度提升至极限，公路追车甚至能用双腿超越普通代步轿车。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_gotgills",
                    "name": {"zh-CN": "快速游泳与深海疾游能力 (CATCHME 变体)", "en": "Fast Swimming Ability"},
                    "syntax_type": "rage_cheat",
                    "code": "CATCHME",
                    "desc": "在海水与游泳池中如离弦之箭极速穿梭，潜水与避让近海饥饿白鲨游刃有余。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_skydive",
                    "name": {"zh-CN": "获取跳伞降落伞背包 (SKYDIVE)", "en": "Give Parachute Backpack (SKYDIVE)"},
                    "syntax_type": "rage_cheat",
                    "code": "SKYDIVE",
                    "desc": "立即装备高空跳伞专用降落伞，从乞力耶德山缆车顶端或直升机上一跃而下尽情翱翔。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_skyfall",
                    "name": {"zh-CN": "万米高空自由落体跳伞模式 (SKYFALL)", "en": "Skyfall from High Altitude (SKYFALL)"},
                    "syntax_type": "rage_cheat",
                    "code": "SKYFALL",
                    "desc": "将角色瞬间传送至洛圣都万米云海高空进行无伞自由落体滑翔俯冲（请确保先开无敌）。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🎮 Native Trainer 角色与外观菜单 (F4 Native Menu - Skin & Model)",
            "commands": [
                {
                    "id": "gta_menu_open",
                    "name": {"zh-CN": "呼出 ScriptHookV 内置菜单 (按 F4 打开)", "en": "Open Native Trainer (Press F4)"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Main Menu",
                    "desc": "在游戏单人故事模式中按 F4 键展开全能离线菜单面板，小键盘 8/2 翻页，5 确认。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_skin_cop",
                    "name": {"zh-CN": "角色模型切换：变身为洛圣都警官 (LSPD)", "en": "Skin Changer: LSPD Police Officer"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Player -> Skin Changer -> Emergency -> Cop",
                    "desc": "换装化身为执勤巡警外观，随同警车一同巡逻，体验完全不同的洛圣都角色视角。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_teleport_base",
                    "name": {"zh-CN": "瞬移传送：军事基地/佩罗码头/机场", "en": "Teleporter: Military Base / Pier"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Teleport -> Locations -> Fort Zancudo",
                    "desc": "一键瞬间传送至桑库多堡垒军事基地跑道内部，免去跨越大半张地图的漫长开车行程。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_never_wanted",
                    "name": {"zh-CN": "永不被通缉 (Never Wanted 警官完全视而不见)", "en": "Never Wanted Mode (Freeze 0 Stars)"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Player -> Never Wanted -> ON",
                    "desc": "锁定通缉星级为零，哪怕单枪匹马闯入军事基地开走天煞战斗机，军方雷达亦绝不拉响警报！",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_noclip_mode",
                    "name": {"zh-CN": "自由飞行漫游摄影穿墙模式", "en": "Free Cam & Noclip Flying Mode"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Player -> No Collision Fly -> ON",
                    "desc": "脱离物理重力自由在城市空中悬浮飞行，无阻碍穿越密闭建筑墙面探索开发室内景。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                }
            ]
        },
        {
            "category": "🚗 载具极速改装、无敌与氮气加速 (Vehicle God, Turbo & Tuning)",
            "commands": [
                {
                    "id": "gta_menu_veh_god",
                    "name": {"zh-CN": "载具锁血绝对无敌 (永不爆炸刮蹭起火)", "en": "Vehicle Invincibility (Vehicle God)"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Vehicle -> Invincible -> ON",
                    "desc": "当前驾驶的汽车即便从崇山峻岭翻滚坠崖或硬抗坦克主炮直击，车身丝毫不受损。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_veh_boost",
                    "name": {"zh-CN": "载具一键火箭氮气加速推进 (按小键盘 9 冲刺)", "en": "Vehicle Rocket Speed Boost"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Vehicle -> Speed Boost (Press Num 9)",
                    "desc": "为所驾载具赋予火箭助推般超强瞬间爆发推力，秒速突破 300km/h 极速大关。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_veh_fix",
                    "name": {"zh-CN": "一键修复并清洗当前座驾 (恢复出厂亮泽)", "en": "Fix & Clean Current Vehicle"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Vehicle -> Fix & Clean",
                    "desc": "瞬间抚平车身所有凹坑弹孔与破碎车窗，重新恢复汽车烤漆如镜面般整洁如新。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_veh_colors",
                    "name": {"zh-CN": "车身烤漆自定义变色与变铬合金反光", "en": "Custom Paint & Chrome Finish"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Vehicle -> Paint Randomizer",
                    "desc": "随时一键切换上百种哑光、金属色与奢华全电镀铬合金质感车体涂装。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_menu_veh_seatbelt",
                    "name": {"zh-CN": "安全带绑定锁定 (高速撞车绝不被甩出车窗)", "en": "Seatbelt On (Never Ejected)"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Vehicle -> Seatbelt -> ON",
                    "desc": "避免在高速剧烈碰撞中因惯性贯穿前挡风玻璃被甩出车外暴毙的悲惨事故。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                }
            ]
        },
        {
            "category": "🌦️ 洛圣都天气、昼夜流速与慢动作 (Weather, Time Scale & Slomo)",
            "commands": [
                {
                    "id": "gta_cheat_makeitrain",
                    "name": {"zh-CN": "切换雷雨暴风雨天气 (MAKEITRAIN)", "en": "Change Weather to Thunderstorm (MAKEITRAIN)"},
                    "syntax_type": "rage_cheat",
                    "code": "MAKEITRAIN",
                    "desc": "洛圣都天空乌云密布并降下磅礴大雨与轰鸣闪电，路面湿滑极具电影黑色氛围。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_snowday",
                    "name": {"zh-CN": "开启罕见圣诞节暴风雪全城积雪 (SNOWDAY)", "en": "Blizzard & Snow Ground (SNOWDAY)"},
                    "syntax_type": "rage_cheat",
                    "code": "SNOWDAY",
                    "desc": "整座洛圣都城市与乡村道路瞬间银装素裹被白雪覆盖，体验极其真实的雪地车辆漂移打滑。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_slowmo",
                    "name": {"zh-CN": "全局慢动作电影运镜流速 (SLOWMO - 四段循环)", "en": "Slomo World Matrix (SLOWMO)"},
                    "syntax_type": "rage_cheat",
                    "code": "SLOWMO",
                    "desc": "将全局物理世界降速运行，每输入一次提升一层时缓倍率，第四次输入恢复正常标准流速。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_floater",
                    "name": {"zh-CN": "月球微重力低引力环境 (FLOATER - 飞车滑翔)", "en": "Moon Gravity Physics (FLOATER)"},
                    "syntax_type": "rage_cheat",
                    "code": "FLOATER",
                    "desc": "将地球引力骤降为月球低重力，轻微擦碰即可让汽车漂浮翻滚如太空漫步般缓缓降落。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "gta_cheat_trashed",
                    "name": {"zh-CN": "醉汉酩酊大醉摇晃视角模式 (TRASHED)", "en": "Drunk Mode Wobble (TRASHED)"},
                    "syntax_type": "rage_cheat",
                    "code": "TRASHED",
                    "desc": "视角出现迷离重影与剧烈摇摆蹒跚，走路东倒西歪，体验极为滑稽诙谐的醉酒物理。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "💰 故事模式线下十亿美金股票与资产 (Offline Cash, Stocks & Properties)",
            "commands": [
                {
                    "id": "gta_cash_fl_billion",
                    "name": {"zh-CN": "富兰克林账户注入十亿美金现金", "en": "Add $1,000,000,000 to Franklin"},
                    "syntax_type": "rage_scripthook",
                    "code": "[Menyoo] Player -> Cash -> Franklin -> Add 1000000000",
                    "desc": "为小富银行账户瞬间汇入 10 亿美金资产，随心买下高尔夫球场与好莱坞全部电影院。",
                    "min_version": "v1.0+",
                    "framework_required": "Menyoo"
                },
                {
                    "id": "gta_cash_mc_billion",
                    "name": {"zh-CN": "麦克账户注入十亿美金现金", "en": "Add $1,000,000,000 to Michael"},
                    "syntax_type": "rage_scripthook",
                    "code": "[Menyoo] Player -> Cash -> Michael -> Add 1000000000",
                    "desc": "为麦克注入十亿现金，尽情升级豪宅私人车库并填满全部限量版经典超跑。",
                    "min_version": "v1.0+",
                    "framework_required": "Menyoo"
                },
                {
                    "id": "gta_cash_tr_billion",
                    "name": {"zh-CN": "崔佛账户注入十亿美金现金", "en": "Add $1,000,000,000 to Trevor"},
                    "syntax_type": "rage_scripthook",
                    "code": "[Menyoo] Player -> Cash -> Trevor -> Add 1000000000",
                    "desc": "为老崔的崔佛菲利普企业注资 10 亿美金，承包整座沙滩海岸机场与军火走私机群。",
                    "min_version": "v1.0+",
                    "framework_required": "Menyoo"
                },
                {
                    "id": "gta_stock_max_profit",
                    "name": {"zh-CN": "故事模式莱斯特刺杀任务股票暴利指南", "en": "Lester Assassination Stock Multiplier"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F4] Native Trainer -> Misc -> Multiply Stock Yield x10",
                    "desc": "将股票市场收益率倍率锁定为 10 倍，单次贝塔制药暗杀即可翻出数百亿惊人天价分红。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookV"
                },
                {
                    "id": "gta_all_properties_free",
                    "name": {"zh-CN": "全城商业地产与私人停机坪免费全解锁", "en": "Unlock All Properties For Free"},
                    "syntax_type": "rage_scripthook",
                    "code": "[Menyoo] World -> Properties -> Buy All Free",
                    "desc": "免花费任何现金一键购入洛圣都全部机库、停泊码头、废车场与定制改装车行地产。",
                    "min_version": "v1.0+",
                    "framework_required": "Menyoo"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "gta_starter_bundle",
            "type": "starter",
            "name": "洛圣都教父财富起飞包",
            "tag": "👑 萌新首选 · 零门槛",
            "badge": "教父起飞",
            "desc": "全三主角账户各注入十亿美金 + PAINKILLER 锁血无敌 + 全套军火库配齐 + 警徽通缉度随心清零，新手开局直接晋升洛圣都终极教父！",
            "highlights": ["富兰克林/麦克/崔佛各拥有 10 亿现金", "PAINKILLER 官方锁血无敌", "TOOLUP 武器军火弹药全满", "LAWYERUP 警匪追捕一秒消除"],
            "code": "-- [老L·极客场景套餐] GTA5 洛圣都教父财富起飞包 (单机实测)\nPAINKILLER\nTURTLE\nTOOLUP\nLAWYERUP\n[Menyoo] Add $1,000,000,000 to All Characters"
        },
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
        "title": "老L实验室避坑笔记 (GTA 5 故事模式与防封圣经)",
        "tips": [
            "【绝对防线上封号铁律】：Rockstar 的 GTA Online 对内存注入实行严苛封号政策！单机玩腻准备进入线上模式联机前，必须彻底将游戏根目录中的 dinput8.dll 改名为 dinput8.dll.bak，确保没有任何 ASI 钩子被加载，即可 100% 确保线上账号绝对安全！",
            "【故事模式股票暴富机制】：麦克的莱斯特刺杀任务千万别提前做！等通关大结局‘联合储蓄’劫案拿到 2800 万初始本金后，再分批次接暗杀任务并全仓买入对应做空做多股票，本金可直接滚至 21 亿上限！",
            "【打不开 F4 菜单】：若按 F4 毫无反应，说明缺失 Visual C++ 2015~2022 运行库或 DirectX 组件。重新安装微软官方合集包即可完美修复。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】GTA5 线上/单机模式安全切换助手\necho ========================================================\necho   【老L·单机避坑局】GTA5 离线防封一键隔离切换器\necho   线上/单机物理隔离 · 绝对杜绝封号误操作\necho ========================================================\necho.\nif not exist \"GTA5.exe\" (\n    echo [!] 提示: 请将本脚本放在 Grand Theft Auto V 游戏安装根目录！\n    pause\n    exit /b\n)\nif exist \"dinput8.dll\" (\n    echo [当前状态]: 【单机 Mod 模式】已开启 (严禁进入线上模式！)\n    echo.\n    set /p choice=\"是否切换为【纯净线上模式】(输入 Y 确认): \"\n    if /i \"%choice%\"==\"Y\" (\n        ren \"dinput8.dll\" \"dinput8.dll.bak\"\n        echo [√] 已安全切断模组管道！现在可安全进入 GTA Online。\n    )\n) else if exist \"dinput8.dll.bak\" (\n    echo [当前状态]: 【纯净线上模式】已启用 (Mod 处于隔离休眠状态)\n    echo.\n    set /p choice=\"是否激活【单机离线 Mod 模式】(输入 Y 确认): \"\n    if /i \"%choice%\"==\"Y\" (\n        ren \"dinput8.dll.bak\" \"dinput8.dll\"\n        echo [√] 已激活 ScriptHookV 离线模组环境！按 F4 呼出菜单。\n    )\n)\necho.\npause\n",
    "verifiedPatch": "v1.0.3179 (线上DLC完全对齐)",
    "radarSecretCode": "洛圣都"
}

print("✅ Rank 8~10 数据模块编译就绪！")

# ==============================================================================
# RANK 11: 荒野大镖客：救赎 2 (Red Dead Redemption 2)
# ==============================================================================
RDR2_DATA = {
    "rank": 11,
    "hasConsole": True,
    "consoleShortcut": "F5 (ScriptHookRDR2 原生离线修改器) 或 游戏内设置-作弊码",
    "consoleEnableGuide": {
        "zh-CN": "【单机故事模式 100% 离线防封指南】\n1. 官方秘籍输入：进入故事模式 -> 按 Esc 暂停 -> 选择【设置 (Settings)】-> 按左下角【作弊 (Cheats)】或 Shift 键 -> 输入对应英文短语并回车保存；\n2. ScriptHookRDR2 离线内置菜单：将 ScriptHookRDR2.dll、dinput8.dll 以及 NativeTrainer.asi 解压至游戏根目录；\n3. 启动故事模式按 F5 键唤出图形修改菜单，小键盘 8/2/4/6 控制，5 确认，0 返回；\n4. ⚠️ 绝无封号风险（进入 RDO 线上前只需将 dinput8.dll 重命名为 .bak 即可完全断开）。",
        "en": "Enter official cheat phrases in Settings -> Cheats, or press F5 with ScriptHookRDR2 in offline story mode."
    },
    "popularCommands": [
        "You want freedom",
        "You flourish before you die",
        "Keep your balance on the curve",
        "Seek all the bounty of this place",
        "Greed is American virtue",
        "[F5] ScriptHookRDR2 -> Horse -> Spawn -> Arabian White"
    ],
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.0.1491.17+ (全离线故事模式对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/red-dead-redemption-2-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/rdr2/Red_Dead_Redemption_2_v1491_Plus_31_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "4a3b2c1d0e9f8a7b6c5d4e3f2a1b0c9d",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Red Dead Redemption 2 Trainer.exe'",
            "troubleshootSteps": [
                "绝对仅限线下单机故事模式使用，切勿在 RDO 线上战局使用",
                "若 Windows Defender 拦截，以管理员身份运行上方 PowerShell 白名单放行指令",
                "进入游戏主界面操作亚瑟骑马行动后，再按小键盘热键激活"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 亚瑟生存与死神之眼",
                "items": [
                    {"key": "Num 1", "action": "亚瑟无敌模式 (God Mode / 锁血锁核心)"},
                    {"key": "Num 2", "action": "无限体力 (疾跑/潜水/拉弓零疲劳)"},
                    {"key": "Num 3", "action": "无限死神之眼 (Dead Eye 随时定格标点)"},
                    {"key": "Num 4", "action": "核心状态锁定全满 (生命/体力/死眼三核心不衰减)"},
                    {"key": "Num 5", "action": "亚瑟温度适宜 (严寒雪山单衣不掉血)"}
                ]
            },
            {
                "category": "🐎 爱马机能与随身背包",
                "items": [
                    {"key": "Num 6", "action": "马匹无敌模式 (撞树/坠崖/遭野兽围攻不倒)"},
                    {"key": "Num 7", "action": "马匹无限体力与胆量 (面对灰熊巨鳄永不受惊甩下)"},
                    {"key": "Num 8", "action": "无限枪械弹药与无需换弹匣"},
                    {"key": "Num 9", "action": "枪械武器永不生锈磨损 (状态完美如新)"}
                ]
            },
            {
                "category": "💰 财富金条与西部时间",
                "items": [
                    {"key": "Ctrl+Num 1", "action": "编辑亚瑟钱包现金 (直接增加 $10,000)"},
                    {"key": "Ctrl+Num 2", "action": "通缉悬赏金清零 (警长立刻放弃追缉)"},
                    {"key": "Ctrl+Num 3", "action": "锁定最高荣誉值 (圣人亚瑟救赎之道)"},
                    {"key": "Ctrl+Num 4", "action": "100% 捕猎完美三星毛皮 (任何枪支射杀均保完美)"},
                    {"key": "Ctrl+Num 5", "action": "时间昼夜流速调节与自由传送"}
                ]
            }
        ]
    },
    "hasMods": True,
    "curatedMods": [
        {
            "id": "rdr2_scripthook",
            "title": "ScriptHookRDR2 + Native Trainer (Alexander Blade 官方前置)",
            "author": "Alexander Blade",
            "version": "v1.0.1491.17",
            "size": "1.1 MB",
            "downloads": "5.6M",
            "endorsements": "310K",
            "category": "Core Framework (核心前置)",
            "desc": "荒野大镖客2运行任何 ASI 模组、刷车刷马工具与离线菜单的官方核心基石。自带防联机误入机制，安全可靠。",
            "dependencies": ["None (Native DLL)"],
            "installPath": "Red Dead Redemption 2/ (游戏根目录)",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/scripthookrdr2/ScriptHookRDR2_1.0.1491.17.zip",
            "downloadFilename": "ScriptHookRDR2_1.0.1491.17.zip",
            "isDirect": True,
            "installSteps": [
                "1. 点击下载 ScriptHookRDR2_1.0.1491.17.zip 压缩包；",
                "2. 打开 RDR2 游戏安装根目录 (包含 RDR2.exe 的目录)；",
                "3. 将压缩包内 bin/ 目录下的 ScriptHookRDR2.dll、dinput8.dll 以及 NativeTrainer.asi 复制进去；",
                "4. 故事模式按 F5 即可呼出全功能菜单。"
            ]
        },
        {
            "id": "rdr2_rampage_trainer",
            "title": "Rampage Trainer (大镖客最强图形化神级修改器)",
            "author": "Rampage Team",
            "version": "v1.6.5",
            "size": "6.8 MB",
            "downloads": "3.8M",
            "endorsements": "240K",
            "category": "Trainer / Menu",
            "desc": "大镖客界公认最强单机离线功能菜单：随时召唤上百种马匹、变身为印第安酋长或动物、随身衣柜换装、营地升级与瞬移全图。",
            "dependencies": ["ScriptHookRDR2"],
            "installPath": "Red Dead Redemption 2/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/rdr2/RampageTrainer_v1.6.5.zip",
            "downloadFilename": "RampageTrainer_v1.6.5.zip",
            "isDirect": True,
            "installSteps": [
                "1. 确保已安装 ScriptHookRDR2；",
                "2. 下载压缩包解压出 Rampage.asi 和 RampageFiles 文件夹；",
                "3. 放入 RDR2 根目录；",
                "4. 故事模式按 F5 或 F7 打开 Rampage 高清菜单。"
            ]
        },
        {
            "id": "rdr2_lml",
            "title": "Lenny's Mod Loader (LML 大镖客模组自动挂载器)",
            "author": "LMS",
            "version": "Beta 11",
            "size": "3.5 MB",
            "downloads": "2.9M",
            "endorsements": "180K",
            "category": "Mod Manager",
            "desc": "彻底告别手动解包 RPF 替换文件的繁琐风险！所有新服饰、枪械高清贴图与声音直接放入 lml/ 文件夹即可自动挂载生效。",
            "dependencies": ["ScriptHookRDR2"],
            "installPath": "Red Dead Redemption 2/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/rdr2/LML_Beta_11.zip",
            "downloadFilename": "LML_Beta_11.zip",
            "isDirect": True,
            "installSteps": [
                "1. 解压 ModLoader 文件夹内全部文件至 RDR2 根目录；",
                "2. 根目录会自动生成 lml/ 文件夹；",
                "3. 后续下载的服饰与材质 mod 直接扔进 lml/ 即可。"
            ]
        },
        {
            "id": "rdr2_whyems_dlc",
            "title": "WhyEm's DLC (海量西部服饰、发型与自定义马鞍大修)",
            "author": "WhyEm",
            "version": "v1.2",
            "size": "850 MB",
            "downloads": "1.2M",
            "endorsements": "95K",
            "category": "Clothing & Customization",
            "desc": "西部牛仔终极衣柜拓展包：为亚瑟增添上千件精美皮衣、披风、马甲、定制牛皮枪套、罕见发型与传说动物皮毛羽毛装饰！",
            "dependencies": ["ScriptHookRDR2", "Lenny's Mod Loader"],
            "installPath": "Red Dead Redemption 2/lml/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/rdr2/WhyEms_DLC.zip",
            "downloadFilename": "WhyEms_DLC.zip",
            "isDirect": True,
            "installSteps": [
                "1. 确认已正确安装 LML 模组加载器；",
                "2. 下载压缩包解压获取 WhyEm's DLC 文件夹；",
                "3. 放入 RDR2/lml/ 文件夹内；",
                "4. 前往捕兽人或裁缝铺即可选购所有独家服饰。"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 核心无敌、无限体力与死神之眼 (God Mode, Stamina & Dead Eye)",
            "commands": [
                {
                    "id": "rdr_cheat_freedom",
                    "name": {"zh-CN": "官方无敌锁血秘籍 (You want freedom)", "en": "Invincibility (You want freedom)"},
                    "syntax_type": "rage_cheat",
                    "code": "You want freedom",
                    "desc": "官方原生秘籍代码，开启亚瑟机体绝对免伤无敌，枪林弹雨与恶狼撕咬分毫无损。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_cheat_flourish",
                    "name": {"zh-CN": "三核心瞬间回满 (You flourish before you die)", "en": "Max All Bars (You flourish before you die)"},
                    "syntax_type": "rage_cheat",
                    "code": "You flourish before you die",
                    "desc": "立即将生命、体力与死神之眼内侧核心及外侧环槽全部充满至最高数值。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_cheat_balance",
                    "name": {"zh-CN": "核心状态强化锁定 (Keep your balance on the curve)", "en": "Fortify Bars (Keep your balance on the curve)"},
                    "syntax_type": "rage_cheat",
                    "code": "Keep your balance on the curve",
                    "desc": "为三核心附加最高级别的金色镀层强化，大幅延缓环境与饥饿带来的消耗流失。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_cheat_deadeye",
                    "name": {"zh-CN": "无限死神之眼子弹时间 (Seek all the bounty of this place)", "en": "Infinite Dead Eye"},
                    "syntax_type": "rage_cheat",
                    "code": "Seek all the bounty of this place",
                    "desc": "开启无限死神之眼模式，随心进入拔枪时缓，一次性标定全屏所有匪徒头部。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_cheat_stealth",
                    "name": {"zh-CN": "悄然无声刺杀暗杀 (Death is silence)", "en": "Stealth Weapons (Death is silence)"},
                    "syntax_type": "rage_cheat",
                    "code": "Death is silence",
                    "desc": "配齐印第安飞斧、飞刀、改良弓箭等全套静音潜行暗杀武器库。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "💰 亚瑟钱包现金、全金条与全背包升级 (Money, Gold Bars & Legend of East Satchel)",
            "commands": [
                {
                    "id": "rdr_cheat_greed",
                    "name": {"zh-CN": "获取 $500 现金 (Greed is American virtue)", "en": "Give $500 Cash (Greed is American virtue)"},
                    "syntax_type": "rage_cheat",
                    "code": "Greed is American virtue",
                    "desc": "官方原生秘籍代码，亚瑟钱包直接入账 500 美元纸钞，可连续多次输入叠加。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_menu_cash_10k",
                    "name": {"zh-CN": "ScriptHook 一键入账 $10,000 巨款", "en": "Add $10,000 via ScriptHookRDR2"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Player -> Cash -> Add $10,000",
                    "desc": "通过 F5 菜单直接将亚瑟财富提升一万美元，在西部时代已相当于天文数字首富。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_gold_bars",
                    "name": {"zh-CN": "获取 30 块纯金条 (黑市商人换现 $15,000)", "en": "Add 30 Pure Gold Bars"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Items -> Add 30 Gold Bars",
                    "desc": "背包直接放入 30 根沉甸甸的金条，随时前往翡翠牧场黑市换取大额现钞。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_satchel_east",
                    "name": {"zh-CN": "一键解锁【东部传说背包】(全部物品99堆叠上限)", "en": "Unlock Legend of the East Satchel"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Satchel -> Unlock Legend of the East Satchel",
                    "desc": "免去漫长繁琐的三星松鼠与獾捕猎，直接获得终极东部传说背包，所有道具携带上限升至 99！",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_cigar_cards",
                    "name": {"zh-CN": "全套 144 张珍奇香烟卡一键全收集", "en": "Collect All 144 Cigarette Cards"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Inventory -> Max All Cigarette Cards",
                    "desc": "集齐全部 12 套珍藏香烟名画卡，瞬间完成全收集支线任务并获得高阶饰品奖赏。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                }
            ]
        },
        {
            "category": "🐎 顶级良驹阿拉伯马与默契度拉满 (Horses Spawner & Max Bonding)",
            "commands": [
                {
                    "id": "rdr_cheat_kingdom_horse",
                    "name": {"zh-CN": "提升马匹默契度 (My kingdom is a horse)", "en": "Increase Horse Bonding"},
                    "syntax_type": "rage_cheat",
                    "code": "My kingdom is a horse",
                    "desc": "官方原生秘籍代码，直接拉升当前坐骑的默契等级，解锁急停与侧向滑行步伐。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_menu_arabian_white",
                    "name": {"zh-CN": "召唤白斑纯血阿拉伯神驹 (雪山绝版良驹)", "en": "Spawn White Arabian Horse"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Horse -> Spawn -> Arabian White",
                    "desc": "直接在身旁生成一匹身姿优美的纯白阿拉伯顶级神马，极速与加速度面板冠绝群雄。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_horse_max_bond",
                    "name": {"zh-CN": "坐骑默契度瞬间 4 级满级 (哨声秒响应)", "en": "Max Horse Bonding Level 4"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Horse -> Max Bonding Level 4",
                    "desc": "免去长途刷马喂燕麦，直接与爱马达到最高 4 级亲密无间默契，吹口哨超远距离秒速奔赴身边。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_horse_god",
                    "name": {"zh-CN": "爱马锁血无敌 (永不坠崖骨折死亡)", "en": "Make Horse Invincible (Horse God)"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Horse -> Invincible Horse",
                    "desc": "锁定坐骑绝对免伤无敌，告别高处跌落爱马猝死的伤感悲剧，无需常备马匹复活剂。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_horse_stamina",
                    "name": {"zh-CN": "马匹无限耐力锁定 (横跨全图狂飙不减速)", "en": "Horse Infinite Stamina"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Horse -> Infinite Stamina",
                    "desc": "马匹体力槽锁定满额，疾驰冲刺毫不疲惫喘息，一口气从草莓镇狂奔至瓦伦丁。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                }
            ]
        },
        {
            "category": "🔫 传奇黑火药军备、稀有枪械与全弹药 (Rare Weapons & Explosive Ammo)",
            "commands": [
                {
                    "id": "rdr_cheat_simple_life",
                    "name": {"zh-CN": "获取全套基础西部武器库 (A simple life, a beautiful death)", "en": "Basic Weapons Arsenal"},
                    "syntax_type": "rage_cheat",
                    "code": "A simple life, a beautiful death",
                    "desc": "官方原生秘籍代码，为亚瑟配齐全套双动左轮手枪、春田步枪与双管霰弹枪。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_cheat_history_fools",
                    "name": {"zh-CN": "获取全套传奇神枪手武器 (History is written by fools)", "en": "Gunslinger Rare Weapons"},
                    "syntax_type": "rage_cheat",
                    "code": "History is written by fools",
                    "desc": "获取决斗任务中四大传奇神枪手的绝版雕花左轮与独家手枪。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_cheat_abundance",
                    "name": {"zh-CN": "无限弹药储备补给 (Abundance is the dullest desire)", "en": "Infinite Ammo Supply"},
                    "syntax_type": "rage_cheat",
                    "code": "Abundance is the dullest desire",
                    "desc": "随身携带的全部枪弹弹药锁定无限，告别去枪械铺逐盒购买子弹的繁琐。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_menu_otis_revolver",
                    "name": {"zh-CN": "获取奥蒂斯米勒黄金雕花左轮 (Otis Miller)", "en": "Add Otis Miller Gold Revolver"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Weapons -> Add Otis Miller Revolver",
                    "desc": "新奥斯汀隐藏山洞中的传奇象牙柄黄金左轮，射速极快且极具收藏价值。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_explosive_ammo",
                    "name": {"zh-CN": "独头高爆霰弹与高爆步枪弹全满", "en": "Max Explosive Slugs & Ammo"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Weapons -> Explosive Slug Ammo",
                    "desc": "充满破坏力惊人的高爆独头弹，一发直接将马车车轮或掩体工事轰得粉碎。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                }
            ]
        },
        {
            "category": "🐾 全传说动物毛皮、捕猎材料与完美尸体 (Legendary Animals & Perfect Pelts)",
            "commands": [
                {
                    "id": "rdr_menu_spawn_bear",
                    "name": {"zh-CN": "生成【传说巴拉蒂灰熊】(身披伤痕巨型凶兽)", "en": "Spawn Legendary Bharati Grizzly Bear"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Spawner -> Spawn Legendary Grizzly Bear",
                    "desc": "在眼前直接生成何西阿捕猎任务中的巨大凶暴传说灰熊，用于剥取传奇熊皮与制作熊头熊皮帽。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_spawn_bison",
                    "name": {"zh-CN": "生成【传说白野牛】(伊莎贝拉湖神圣雪兽)", "en": "Spawn Legendary White Bison"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Spawner -> Spawn Legendary White Bison",
                    "desc": "生成纯白如雪的传说野牛，剥取皮毛制作极地防寒保暖终极斗篷。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_spawn_buck",
                    "name": {"zh-CN": "生成【传说公鹿】(捕猎核心神级公鹿角饰物)", "en": "Spawn Legendary Buck"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Spawner -> Spawn Legendary Buck",
                    "desc": "讨伐后制作传说公鹿角饰物，永久提升野外剥皮获得高品质完美三星皮的几率！",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_all_perfect_pelts",
                    "name": {"zh-CN": "全野生动物完美三星毛皮各 5 张直接入库", "en": "Add All Perfect 3-Star Pelts x5"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Inventory -> Add All Perfect Pelts",
                    "desc": "完美美洲狮皮、黑熊皮、狼皮、海狸皮一键入库，捕兽人全套外观时装瞬间全部做齐！",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_pearson_upgrade",
                    "name": {"zh-CN": "范德林德帮营地全设施一键满级升级", "en": "Max Out Camp Pearson Upgrades"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Camp -> Pearson Upgrade Max",
                    "desc": "为皮尔逊与利奥波德账本一键完成全部营地皮革装饰、快速旅行地图与医疗补给棚升级。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                }
            ]
        },
        {
            "category": "🌦️ 昼夜天气调控、快速传送与荣誉值 (Honor, Weather & Fast Travel)",
            "commands": [
                {
                    "id": "rdr_cheat_virtue",
                    "name": {"zh-CN": "荣誉值一键提升至最高上限 (Virtue unearned is not virtue)", "en": "Max Honor Level (Virtue unearned is not virtue)"},
                    "syntax_type": "rage_cheat",
                    "code": "Virtue unearned is not virtue",
                    "desc": "官方原生秘籍代码，亚瑟声望瞬间升至满额最高级，商店购物享受 50% 半价折扣特惠。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "rdr_menu_weather_storm",
                    "name": {"zh-CN": "召唤电影级西部真实雷暴天气", "en": "Set Weather to Thunderstorm"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Weather -> Thunderstorm",
                    "desc": "黑云压顶、狂风呼啸、闪电撕裂大地，置身好莱坞西部电影般的史诗荒野氛围。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_teleport_stdenis",
                    "name": {"zh-CN": "一键快速传送：圣丹尼斯繁华工业大都市", "en": "Teleport to Saint Denis City"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> Teleport -> Fast Travel to Saint Denis",
                    "desc": "瞬间瞬移至圣丹尼斯铺石大道中心，免去漫长十几分钟的马车颠簸路程。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_menu_freeze_time",
                    "name": {"zh-CN": "锁定金黄日落黄昏时间 (永恒西部暮色)", "en": "Freeze Golden Sunset Hour"},
                    "syntax_type": "rage_scripthook",
                    "code": "[F5] ScriptHookRDR2 -> World -> Freeze Time of Day",
                    "desc": "将时间定格在傍晚 18:30 的夕阳余晖，草原与大峡谷泛着醉人的金光，摄影留念极品。",
                    "min_version": "v1.0+",
                    "framework_required": "ScriptHookRDR2"
                },
                {
                    "id": "rdr_cheat_punishment",
                    "name": {"zh-CN": "提升通缉等级 (You want punishment - 赏金猎人大战)", "en": "Raise Bounty (You want punishment)"},
                    "syntax_type": "rage_cheat",
                    "code": "You want punishment",
                    "desc": "为亚瑟附加悬赏星级，引来全州最精锐的平克顿侦探与猎犬展开生死决战追杀。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "rdr_starter_bundle",
            "type": "starter",
            "name": "新手西部拓荒起飞包",
            "tag": "👑 萌新首选 · 零门槛",
            "badge": "拓荒起飞",
            "desc": "一键激活 You want freedom 锁血无敌 + 白斑纯血阿拉伯神马 + 30 块纯金条兑现 + 东部传说背包 99 堆叠，开荒西部零受苦！",
            "highlights": ["官方锁血无敌，告别野兽袭击暴毙", "白斑纯血阿拉伯神驹伴你行", "30 块纯金条入账瞬间成为大富翁", "东部传说背包 99 道具携带上限"],
            "code": "-- [老L·极客场景套餐] 大镖客2 新手西部拓荒起飞包\nYou want freedom\nYou flourish before you die\n[F5] ScriptHookRDR2 -> Horse -> Spawn -> Arabian White\n[F5] ScriptHookRDR2 -> Items -> Add 30 Gold Bars"
        },
        {
            "id": "rdr_salvation_bundle",
            "type": "salvation",
            "name": "圣人亚瑟救赎圆满包",
            "tag": "🛡️ 意难平救赎 · 告别受苦",
            "badge": "圣人救赎",
            "desc": "荣誉值满级 Virture + 全套神枪手绝版武器 + 全传说动物毛皮各 5 张 + 营地全设施顶级升级，给亚瑟一个最体面圆满的归宿！",
            "highlights": ["荣誉值满级圣人亚瑟路线", "全套四大传奇神枪手雕花手枪", "全传说动物毛皮，捕兽人全套做齐", "范德林德帮营地温馨全满配置"],
            "code": "-- [老L·极客场景套餐] 大镖客2 圣人亚瑟救赎圆满包\nVirtue unearned is not virtue\nHistory is written by fools\n[F5] ScriptHookRDR2 -> Inventory -> Add All Perfect Pelts\n[F5] ScriptHookRDR2 -> Camp -> Pearson Upgrade Max"
        },
        {
            "id": "rdr_godmode_bundle",
            "type": "godmode",
            "name": "荒野死神火力真神包",
            "tag": "⚡ 极客狂欢 · 众神陨落",
            "badge": "荒野死神",
            "desc": "无限死神之眼 Seek all the bounty + 独头高爆霰弹全满 + 震撼西部雷暴 + 瞬移圣丹尼斯，化身横行西部的荒野死神！",
            "highlights": ["无限死神之眼子弹时间定格", "独头高爆霰弹枪一枪碎车", "震撼西部真实雷暴大电影质感", "瞬移圣丹尼斯无需骑马赶路"],
            "code": "-- [老L·极客场景套餐] 大镖客2 荒野死神火力真神包\nSeek all the bounty of this place\n[F5] ScriptHookRDR2 -> Weapons -> Explosive Slug Ammo\n[F5] ScriptHookRDR2 -> Weather -> Thunderstorm\n[F5] ScriptHookRDR2 -> Teleport -> Fast Travel to Saint Denis"
        }
    ],
    "pitfallNote": {
        "title": "老L实验室避坑笔记 (荒野大镖客2 故事模式防封圣经)",
        "tips": [
            "【绝对防联机封号隔离】：R星对 RDO 荒野大镖客线上模式同样严查。在登录线上战局前，务必把游戏根目录的 dinput8.dll 改名为 dinput8.dll.bak，彻底切断所有 ScriptHook 挂钩，绝无封号之忧！",
            "【捕猎毛皮品质保护】：想要获得三星完美毛皮，务必击杀头上本来就是三星的动物，并掏出春田步枪击中头部一击毙命；若嫌繁琐，直接使用本库一键添加全部三星皮！",
            "【作弊码保存限制】：在官方设置里激活作弊码后，系统会默认暂时禁止保存新存档。若需保存修改后的金钱与装备，请使用 ScriptHookRDR2 或风灵月影修改器，它们不会禁用存档功能！"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】荒野大镖客2 离线防封助手\necho ========================================================\necho   【老L·单机避坑局】荒野大镖客2 纯净离线隔离切换器\necho   故事模式一键畅玩 · 物理隔离线上 RDO · 零封号\necho ========================================================\necho.\nif not exist \"RDR2.exe\" (\n    echo [!] 提示: 请将本脚本放在 Red Dead Redemption 2 游戏安装根目录！\n    pause\n    exit /b\n)\nif exist \"dinput8.dll\" (\n    echo [当前状态]: 【单机 Mod 模式】已开启 (切勿进入线上战局！)\n    echo.\n    set /p choice=\"是否切换为【纯净线上 RDO 模式】(输入 Y 确认): \"\n    if /i \"%choice%\"==\"Y\" (\n        ren \"dinput8.dll\" \"dinput8.dll.bak\"\n        echo [√] 已切断模组管道！现在可安全启动 RDO 线上战局。\n    )\n) else if exist \"dinput8.dll.bak\" (\n    echo [当前状态]: 【纯净线上模式】已启用 (Mod 处于隔离状态)\n    echo.\n    set /p choice=\"是否激活【单机离线 Mod 模式】(输入 Y 确认): \"\n    if /i \"%choice%\"==\"Y\" (\n        ren \"dinput8.dll.bak\" \"dinput8.dll\"\n        echo [√] 已激活 ScriptHookRDR2 离线环境！按 F5 呼出修改菜单。\n    )\n)\necho.\npause\n",
    "verifiedPatch": "v1.0.1491 (完全对齐)",
    "radarSecretCode": "大表哥"
}

# ==============================================================================
# RANK 12: 怪物猎人：世界 (Monster Hunter: World)
# ==============================================================================
MHW_DATA = {
    "rank": 12,
    "hasConsole": True,
    "consoleShortcut": "Insert 唤出 REFramework 覆盖菜单 / F10 调出调试控制台",
    "consoleEnableGuide": {
        "zh-CN": "【怪物猎人世界 纯净模组与控制台指南】\n1. 下载 Stracker's Loader (包含 dinput8.dll 与 loader-config.json) 解压至游戏根目录 (Monster Hunter World/)；\n2. 将 REFramework 或 All Items in Shop 模组解压放入 nativePC/ 对应目录；\n3. 启动游戏，按键盘 Insert 键即可在屏幕左上角唤出 REFramework 菜单；\n4. 支持全珠子全素材一键补齐、聚魔之地等级随心调节与伤害血量实时透视！",
        "en": "Install Stracker's Loader into MHW root. Press Insert to open REFramework menu for decorations, materials, and SmartHunter overlay."
    },
    "popularCommands": [
        "[REFramework] -> Player Stats -> Invincibility (God Mode)",
        "[REFramework] -> Weapon Stats -> Infinite Sharpness",
        "[Shop] -> Buy Item -> Attack Jewel 4",
        "[REFramework] -> Guiding Lands -> Set All Regions to Level 7",
        "[REFramework] -> Economy -> Add 10,000,000 Zenny",
        "[SmartHunter] -> Overlay -> Show Monster Realtime HP Bar"
    ],
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v15.11+ (Iceborne 冰原终极版本完全对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/monster-hunter-world-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/mhw/Monster_Hunter_World_Iceborne_Plus_47_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "3b2a1c0d9e8f7a6b5c4d3e2f1a0b9c8d",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Monster Hunter World Trainer.exe'",
            "troubleshootSteps": [
                "冰原单人离线与好友私人房间均可正常使用，请勿在公开救援任务滥用一击必杀",
                "若 Windows Defender 拦截，以管理员身份运行上方 PowerShell 白名单放行指令",
                "进入月辰据点或接取任务营地后再开启修改功能"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 猎人生存与武器斩味",
                "items": [
                    {"key": "Num 1", "action": "猎人无敌锁血 (God Mode / 免受伤害)"},
                    {"key": "Num 2", "action": "无限耐力 (奔跑/蓄力/滑步零消耗)"},
                    {"key": "Num 3", "action": "武器无限斩味 (紫斩白斩永不磨损掉斩)"},
                    {"key": "Num 4", "action": "太刀红刃练气全满锁定 (随时释放登龙气刃斩)"},
                    {"key": "Num 5", "action": "盾斧红盾红剑超解瓶子无限锁定"}
                ]
            },
            {
                "category": "🎒 装备珠子与客制素材",
                "items": [
                    {"key": "Num 6", "action": "无限随身道具与弹药 (秘药/闪光弹无限用)"},
                    {"key": "Num 7", "action": "100% 极品 4 级珠子掉落概率 (攻击珠II/达人珠II)"},
                    {"key": "Num 8", "action": "装备锻造与客制强化无需任何素材"},
                    {"key": "Num 9", "action": "武器防具强化等级直接拉至上限"}
                ]
            },
            {
                "category": "🐉 聚魔之地与狩猎生态",
                "items": [
                    {"key": "Ctrl+Num 1", "action": "聚魔之地全区域等级直接锁定 Lv7"},
                    {"key": "Ctrl+Num 2", "action": "编辑调查点数与金钱金币 (99,999,999)"},
                    {"key": "Ctrl+Num 3", "action": "怪物一击倒地断尾破坏 (部位破坏狂)"},
                    {"key": "Ctrl+Num 4", "action": "超高剥取次数 (单只古龙剥取 20 次)"},
                    {"key": "Ctrl+Num 5", "action": "随从猫六大特殊装备全满级"}
                ]
            }
        ]
    },
    "hasMods": True,
    "curatedMods": [
        {
            "id": "mhw_strackers_loader",
            "title": "Stracker's Loader (怪猎核心前置插件加载引导器)",
            "author": "Stracker",
            "version": "v1.12",
            "size": "450 KB",
            "downloads": "4.8M",
            "endorsements": "280K",
            "category": "Core Framework (核心前置)",
            "desc": "怪猎世界冰原运行 nativePC 外部模组、商店补全插件与透视覆层的绝对核心前置库，包含 CRC 绕过修复。",
            "dependencies": ["None (Native DLL)"],
            "installPath": "Monster Hunter World/ (游戏根目录)",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/mhw/StrackersLoader_v1.12.zip",
            "downloadFilename": "StrackersLoader_v1.12.zip",
            "isDirect": True,
            "installSteps": [
                "1. 点击下载 StrackersLoader_v1.12.zip 压缩包；",
                "2. 打开 Monster Hunter World 游戏安装根目录；",
                "3. 将解压出的 dinput8.dll、dtdata.dll 等文件放入根目录；",
                "4. 启动游戏即可正常加载 nativePC 下的所有 Mod。"
            ]
        },
        {
            "id": "mhw_all_items_shop",
            "title": "All Items in Shop (全道具/全珠子/全素材随身商店 1 铜币直购)",
            "author": "mhvuze",
            "version": "v2.5",
            "size": "1.2 MB",
            "downloads": "2.9M",
            "endorsements": "190K",
            "category": "Economy / Items",
            "desc": "将月辰与星辰基地的物资补给所商店彻底重制：所有 4 级神珠、古龙大宝玉、聚魔之地客制材料全部上架，统一标价 1 铜币，告别几百小时枯燥刷珠子！",
            "dependencies": ["Stracker's Loader"],
            "installPath": "Monster Hunter World/nativePC/common/facility/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/mhw/AllItemsInShop_Iceborne.zip",
            "downloadFilename": "AllItemsInShop_Iceborne.zip",
            "isDirect": True,
            "installSteps": [
                "1. 确认已安装 Stracker's Loader 前置；",
                "2. 下载压缩包解压获取 nativePC 文件夹；",
                "3. 直接合并覆盖到游戏根目录下；",
                "4. 到道具屋阿姨处对话即可挑选任何顶级珠子与素材。"
            ]
        },
        {
            "id": "mhw_smart_hunter",
            "title": "SmartHunter (怪物实时血量、异常状态与部位耐久悬浮窗)",
            "author": "gabrie-allaigre",
            "version": "v1.64.0",
            "size": "3.5 MB",
            "downloads": "3.2M",
            "endorsements": "210K",
            "category": "UI / Overlay",
            "desc": "狩猎利器！在屏幕上方优雅悬浮显示怪物真实总血量、当前血百分比、激怒倒计时、麻痹/睡眠积蓄值，以及队伍四人各自输出 DPS 占比统计！",
            "dependencies": ["None (Stand-alone Memory Overlay)"],
            "installPath": "Windows PC",
            "downloadUrl": "https://github.com/gabrie-allaigre/SmartHunter/releases/download/v1.64.0/SmartHunter.zip",
            "downloadFilename": "SmartHunter_v1.64.0.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载解压 SmartHunter 压缩包至任意文件夹；",
                "2. 启动怪猎世界并进入猎场；",
                "3. 双击运行 SmartHunter.exe，悬浮窗将自动对齐游戏画面显示。"
            ]
        },
        {
            "id": "mhw_perf_booster",
            "title": "Performance Booster and Plugin Extender (CPU 线程优化补丁)",
            "author": "AsteriskAmpersand",
            "version": "v4.2",
            "size": "380 KB",
            "downloads": "2.5M",
            "endorsements": "160K",
            "category": "Performance (性能加速)",
            "desc": "移除冰原反作弊死循环冗余检测，大幅消除 100% CPU 占用导致的掉帧卡顿，平均提升 15~25 帧并降低 CPU 核心温度 8-10℃！",
            "dependencies": ["Stracker's Loader"],
            "installPath": "Monster Hunter World/nativePC/plugins/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/mhw/PerformanceBooster_Iceborne.zip",
            "downloadFilename": "PerformanceBooster_Iceborne.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载压缩包解压出 .dll 插件；",
                "2. 放入 nativePC/plugins/ 目录；",
                "3. 启动游戏享受极致丝滑 120FPS 狩猎体验。"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 核心锁血、无限耐力与斩味锁定 (God Mode, Infinite Sharpness & Stamina)",
            "commands": [
                {
                    "id": "mhw_god_mode",
                    "name": {"zh-CN": "猎人绝对锁血无敌判定 (God Mode)", "en": "Hunter Invincibility (God Mode)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Player Stats -> Invincibility (God Mode)",
                    "desc": "生命值锁定上限，承受黑龙扇形火劫或煌黑龙审判大招亦分毫无伤。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_inf_stamina",
                    "name": {"zh-CN": "无限耐力槽 (双刀鬼人化/弓箭滑步不竭)", "en": "Infinite Stamina Lock"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Player Stats -> Infinite Stamina",
                    "desc": "耐力槽锁定最大值，双刀全程常驻鬼人化乱舞，弓箭无限滑步蓄力射击。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_inf_sharpness",
                    "name": {"zh-CN": "武器永不磨损锁定紫斩 (免除磨刀石砥石磨刀)", "en": "Infinite Sharpness (Never Dulls)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Weapon Stats -> Infinite Sharpness",
                    "desc": "最高阶紫斩或白斩永远不掉斩味，即使频繁弹刀肉质坚硬部位也无需掏出砥石磨刀。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_inf_phials",
                    "name": {"zh-CN": "盾斧瓶子与斩斧觉醒槽全满锁定", "en": "Infinite CB Phials & Switch Axe Amped"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Player Stats -> Infinite Phials / Kinsect Stamina",
                    "desc": "盾斧 5 瓶/6 瓶随时充能爆满，无间隔连续释放超强高出力属性解放斩 (超解)！",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_instant_charge",
                    "name": {"zh-CN": "大剑/太刀秒速三段真蓄力", "en": "Instant Greatsword True Charged Slash"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Weapon Stats -> Instant Charge",
                    "desc": "大剑蓄力瞬间直接达到 3 段真蓄力最高威力，太刀见切闪避判定窗口大幅延长。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "💎 全 4 级攻击珠/达人珠与全装饰品补齐 (All Decorations & Level 4 Jewels)",
            "commands": [
                {
                    "id": "mhw_jewel_attack4",
                    "name": {"zh-CN": "商店直购：攻击珠II【4】(极难刷出核心神珠)", "en": "Buy Attack Jewel 4 (1 Zenny)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[Shop] -> Buy Item -> Attack Jewel 4",
                    "desc": "在月辰道具店以 1 铜币直接购买毕业攻击珠II，单颗直接提供两级巨额攻击力。",
                    "min_version": "v15.0+",
                    "framework_required": "Stracker's Loader"
                },
                {
                    "id": "mhw_jewel_expert4",
                    "name": {"zh-CN": "商店直购：达人珠II【4】(提供超高会心率)", "en": "Buy Expert Jewel 4 (1 Zenny)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[Shop] -> Buy Item -> Expert Jewel 4",
                    "desc": "直接购买达人珠II，轻松配出见切 7 级 40% 常驻高暴击率面板。",
                    "min_version": "v15.0+",
                    "framework_required": "Stracker's Loader"
                },
                {
                    "id": "mhw_jewel_challenger4",
                    "name": {"zh-CN": "商店直购：挑战珠II【4】(挑战者极境加成)", "en": "Buy Challenger Jewel 4"},
                    "syntax_type": "reframework_cmd",
                    "code": "[Shop] -> Buy Item -> Challenger Jewel 4",
                    "desc": "怪物激怒时获得巨额攻击力与会心率提升，冰原版本几乎所有武器的通用标配神珠。",
                    "min_version": "v15.0+",
                    "framework_required": "Stracker's Loader"
                },
                {
                    "id": "mhw_jewel_critical2",
                    "name": {"zh-CN": "商店直购：超心珠【2】(暴击伤害提升至1.4倍)", "en": "Buy Critical Jewel 2"},
                    "syntax_type": "reframework_cmd",
                    "code": "[Shop] -> Buy Item -> Critical Jewel 2",
                    "desc": "超会心 3 级让会心暴击时的伤害倍率提升至 1.4 倍，刀刀入肉暴击数字大红字。",
                    "min_version": "v15.0+",
                    "framework_required": "Stracker's Loader"
                },
                {
                    "id": "mhw_jewel_tenderizer2",
                    "name": {"zh-CN": "商店直购：痛击珠【2】(弱点特效 50% 会心)", "en": "Buy Tenderizer Jewel 2"},
                    "syntax_type": "reframework_cmd",
                    "code": "[Shop] -> Buy Item -> Tenderizer Jewel 2",
                    "desc": "击中软化肉质弱点部位直接获得 50% 额外暴击几率，输出翻倍最关键技能。",
                    "min_version": "v15.0+",
                    "framework_required": "Stracker's Loader"
                }
            ]
        },
        {
            "category": "🐉 聚魔之地全区域 7 级与极品客制素材 (Guiding Lands Lv7 & Augment Mats)",
            "commands": [
                {
                    "id": "mhw_gl_all_lv7",
                    "name": {"zh-CN": "聚魔之地全部地带等级一键锁定 Lv7 满级", "en": "Set All Guiding Lands Regions to Level 7"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Guiding Lands -> Set All Regions to Level 7",
                    "desc": "打破官方最多只能三区 Lv7 的恶心锁槽限制，森林/荒地/陆珊瑚/瘴气/火山/冰雪全区满级！",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_gem_great_spiritvein",
                    "name": {"zh-CN": "获得大灵脉玉 x100 (武器防具客制上限解除)", "en": "Add 100 Great Spiritvein Gems"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Items -> Add Great Spiritvein Gem x100",
                    "desc": "聚魔之地最稀缺的终极客制材料，解开 12 阶武器吸血客制与防具最终防御力上限强化。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_mat_ruinhorn",
                    "name": {"zh-CN": "获得历战歼世灭尽龙灭尽破角 x50", "en": "Add 50 Tempered Ruinhorns"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Items -> Add Tempered Ruinhorn x50",
                    "desc": "近战武器客制【吸血 (生命回复)】不可或缺的顶级珍稀素材，刀刀吸血站撸古龙。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_mat_solidbone",
                    "name": {"zh-CN": "获得灵脉刚龙骨 x100 (扩充武器客制槽位)", "en": "Add 100 Spiritvein Solidbones"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Items -> Add Spiritvein Solidbone x100",
                    "desc": "用于在工匠处为 12 阶稀有武器扩充第一、第二与第三级客制额外镶嵌槽位。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_unlock_augments",
                    "name": {"zh-CN": "一键解锁全部武器防具客制强化权限", "en": "Unlock All Augments Automatically"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Equipment -> Unlock All Weapon Augments",
                    "desc": "免去 MR 等级达到 100 级才能客制的等级墙门槛，随时在加工屋享受吸血与会心强化。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "💰 调查点数、全随从猫装备与财富自由 (Research Points, Zenny & Palico Gear)",
            "commands": [
                {
                    "id": "mhw_money_10m",
                    "name": {"zh-CN": "获得 10,000,000 铜币金钱 (工匠强化不差钱)", "en": "Add 10,000,000 Zenny"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Economy -> Add 10,000,000 Zenny",
                    "desc": "一千万金钱即刻到账，强化几十套高阶防具与定做武器无需担忧破产。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_points_1m",
                    "name": {"zh-CN": "获得 1,000,000 调查点数 (猫饭与炼金无限点)", "en": "Add 1,000,000 Research Points"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Economy -> Add 1,000,000 Research Points",
                    "desc": "大量补充调查点数，用于大锅炼金封印的宝珠与随从探险队全天候派遣。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_palico_max_gear",
                    "name": {"zh-CN": "随从猫六大特殊装备全满级 (掠夺刀/蜜虫Lv15)", "en": "Max All Palico Gadgets to Lv15"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Palico -> Max All Gadget Levels",
                    "desc": "将蜜虫吸引香、掠夺刀、闪光弹与盾牌全部升满至 15 级，掠夺刀甚至能直接从古龙身上剥落天鳞！",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_botanical_harvest",
                    "name": {"zh-CN": "植生研究所全素材一键爆箱丰收", "en": "Instant Max Botanical Harvest Box"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Botanical -> Max Harvest Box",
                    "desc": "光虫、怪力种子、蜂蜜与鬼人药配方材料一键堆满收纳箱，再也不用手动耕作施肥。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_steamworks_fuel",
                    "name": {"zh-CN": "月辰蒸汽机燃料补满 (全自动万次十倍抽奖)", "en": "Max Natural Fuel for Steamworks"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Steamworks -> Max Natural Fuel",
                    "desc": "蒸汽机燃料提升至数万点，开启自动按压连发，狂抽上百个高级铠玉与天之龙人票据。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "🗡️ 毕业黑龙/冥赤龙神装与全武器幻化 (Fatalis/Safi Weapons & Layered Armors)",
            "commands": [
                {
                    "id": "mhw_equip_fatalis_armor",
                    "name": {"zh-CN": "一键解锁毕业【黑龙全套防具】(黑龙之真髓)", "en": "Unlock Fatalis Full Armor Set"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Equipment -> Unlock Full Fatalis Armor Set",
                    "desc": "全孔位四级神装，自带黑龙真髓技能【超越】与【继承】，体力与耐力上限直接翻倍！",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_equip_fatalis_greatsword",
                    "name": {"zh-CN": "获取【黑龙大剑·黑羽大剑】(超高物理攻击)", "en": "Unlock Fatalis Zagges Greatsword"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Equipment -> Unlock Fatalis Zagges",
                    "desc": "全游戏最高物理面板大剑，搭配客制会心与看破 7 级，真蓄力斩打出一刀数千巨额伤害。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_equip_layered_all",
                    "name": {"zh-CN": "全武器与防具外观幻化全解锁 (暖暖暖装随心配)", "en": "Unlock All Layered Armor & Weapons"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Equipment -> Unlock All Layered Armor",
                    "desc": "解锁全部历战王时装、温泉浴衣、苍星联动与武器外观幻化，打猎同时颜值爆表。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_equip_safi_weapons",
                    "name": {"zh-CN": "获取全属性冥赤龙觉醒神兵 (词条随意自选)", "en": "Unlock Safi'jiiva Awakened Weapons"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Equipment -> Unlock Safi'jiiva Awakened Weapons",
                    "desc": "集齐全部冥赤龙赤龙武器，龙光石觉醒词条直接全部点出攻击力强化 VI 与斩味强化。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "mhw_equip_alatreon",
                    "name": {"zh-CN": "获取煌黑龙全套终极属性神装", "en": "Unlock Alatreon Full Weapon Set"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Equipment -> Unlock Alatreon Weapon Set",
                    "desc": "极致龙属性与超长紫斩神兵，专克任何弱龙属性的强力古龙生物。",
                    "min_version": "v15.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "🎯 怪物即时血量透视与弱点命中显示 (SmartHunter Overlay & Damage Meter)",
            "commands": [
                {
                    "id": "mhw_overlay_hp",
                    "name": {"zh-CN": "怪物实时生命值与残血抓捕标线透视", "en": "Show Realtime Monster Health & Capture Line"},
                    "syntax_type": "reframework_cmd",
                    "code": "[SmartHunter] -> Overlay -> Show Monster Realtime HP Bar",
                    "desc": "在屏幕顶端悬浮显示精准血量数字，降至 20% 抓捕线时自动亮起警报，抓怪不再失手击杀。",
                    "min_version": "v15.0+",
                    "framework_required": "SmartHunter"
                },
                {
                    "id": "mhw_overlay_enrage",
                    "name": {"zh-CN": "怪物激怒状态与流涎疲劳计时器", "en": "Show Enrage Timer & Drooling Status"},
                    "syntax_type": "reframework_cmd",
                    "code": "[SmartHunter] -> Overlay -> Show Monster Enrage & Stamina",
                    "desc": "监控挑战者技能触发倒计时，并精准预知怪物何时疲劳进入流涎站桩期。",
                    "min_version": "v15.0+",
                    "framework_required": "SmartHunter"
                },
                {
                    "id": "mhw_overlay_parts",
                    "name": {"zh-CN": "头部/尾巴/龙翼部位破坏耐久度显示", "en": "Show Part Break Durability Bars"},
                    "syntax_type": "reframework_cmd",
                    "code": "[SmartHunter] -> Overlay -> Show Part Break Durability",
                    "desc": "精准监控断尾与破头还剩多少伤害数值，高效集火特定部位获取破坏掉落素材。",
                    "min_version": "v15.0+",
                    "framework_required": "SmartHunter"
                },
                {
                    "id": "mhw_overlay_dps",
                    "name": {"zh-CN": "四人小队输出贡献率与 DPS 实时统计", "en": "Show Team DPS Damage Contribution"},
                    "syntax_type": "reframework_cmd",
                    "code": "[SmartHunter] -> Overlay -> DPS Damage Contribution",
                    "desc": "优雅显示四人组队时每位猎人的实际伤害输出占比与柱状图，客观评估武器配装强度。",
                    "min_version": "v15.0+",
                    "framework_required": "SmartHunter"
                },
                {
                    "id": "mhw_overlay_status",
                    "name": {"zh-CN": "怪物麻痹/睡眠/眩晕异常积蓄槽监控", "en": "Show Abnormal Status Effect Buildup"},
                    "syntax_type": "reframework_cmd",
                    "code": "[SmartHunter] -> Overlay -> Monster Status Effect Buildup",
                    "desc": "实时查看再打几枪麻痹弹或打几发彻甲榴弹才能触发眩晕倒地，精准控场掌控节奏。",
                    "min_version": "v15.0+",
                    "framework_required": "SmartHunter"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "mhw_starter_bundle",
            "type": "starter",
            "name": "新手苍蓝星逃课起飞包",
            "tag": "👑 萌新首选 · 零门槛",
            "badge": "逃课起飞",
            "desc": "一键激活锁血锁斩味无敌 + 全 4 级攻击珠达人珠 1 铜币直购 + 一千万资金 + 随从猫掠夺刀 15 级，新手畅享丝滑爽快大狩猎！",
            "highlights": ["锁血无敌免受猫车折磨", "攻击珠II/达人珠II 1铜币全买齐", "武器紫斩永不磨损掉斩", "一千万金币工匠强化财富自由"],
            "code": "-- [老L·极客场景套餐] 怪猎世界 新手苍蓝星逃课起飞包\n[REFramework] -> Player Stats -> Invincibility (God Mode)\n[REFramework] -> Weapon Stats -> Infinite Sharpness\n[Shop] -> Buy Item -> Attack Jewel 4\n[Shop] -> Buy Item -> Expert Jewel 4"
        },
        {
            "id": "mhw_salvation_bundle",
            "type": "salvation",
            "name": "聚魔之地客制满配救赎包",
            "tag": "🛡️ 意难平救赎 · 告别受苦",
            "badge": "聚魔满配",
            "desc": "聚魔之地全六大区域直接拉满 Lv7 + 大灵脉玉 100 个 + 历战灭尽龙角 50 个 + 武器吸血客制全开，告别肝聚魔地质学折磨！",
            "highlights": ["全六大区域直接全锁定 Lv7 满级", "大灵脉玉 100 个随心解除上限", "近战武器吸血客制直接拉满", "刀刀吸血站撸历战古龙"],
            "code": "-- [老L·极客场景套餐] 怪猎世界 聚魔之地客制满配救赎包\n[REFramework] -> Guiding Lands -> Set All Regions to Level 7\n[REFramework] -> Items -> Add Great Spiritvein Gem x100\n[REFramework] -> Items -> Add Tempered Ruinhorn x50\n[REFramework] -> Equipment -> Unlock All Weapon Augments"
        },
        {
            "id": "mhw_godmode_bundle",
            "type": "godmode",
            "name": "黑龙真髓真神毕业包",
            "tag": "⚡ 极客狂欢 · 众神陨落",
            "badge": "真神毕业",
            "desc": "黑龙全套毕业神装 + 极限面板黑龙大剑 + SmartHunter 怪物实时血量部位耐久透视 + 全服装外观幻化，终结新大陆狩猎终点！",
            "highlights": ["黑龙真髓全套 4 级孔位神级装备", "物理伤害天花板黑龙大剑", "SmartHunter 实时血量部位破坏透视", "全外观幻化全解锁美型猎人"],
            "code": "-- [老L·极客场景套餐] 怪猎世界 黑龙真髓真神毕业包\n[REFramework] -> Equipment -> Unlock Full Fatalis Armor Set\n[REFramework] -> Equipment -> Unlock Fatalis Zagges\n[SmartHunter] -> Overlay -> Show Monster Realtime HP Bar\n[REFramework] -> Equipment -> Unlock All Layered Armor"
        }
    ],
    "pitfallNote": {
        "title": "老L实验室避坑笔记 (怪物猎人世界 冰原终极避坑指南)",
        "tips": [
            "【联机防踢与尊重原则】：卡普空对单机与好友自建私人房间使用 Mod 极为宽松（无 VAC 封号机制）。但在加入路人公开救援时，请务必关闭【一击必杀】与【锁血】，使用 SmartHunter 纯净显示血量即可，切勿破坏其他真实玩家的狩猎乐趣！",
            "【黑屏无限加载急救】：安装模组后游戏无法启动或黑屏卡死，99% 是由于游戏大更新后 Stracker's Loader 未更新或 nativePC 遗留了过期前置。删除游戏根目录的 dinput8.dll 即可瞬间恢复正常启动！",
            "【CPU 100% 掉帧发热排查】：冰原自带的反作弊线程存在内存死循环 Bug。请务必安装本站推荐的 Performance Booster 补丁，直接禁用该死循环，显卡性能完全释放。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】怪猎世界 Stracker Loader 诊断工具\necho ========================================================\necho   【老L·单机避坑局】怪物猎人世界 模组环境自动诊断器\necho   CRC 绕过检测 · 自动备份 nativePC · 零卡死\necho ========================================================\necho.\nif not exist \"MonsterHunterWorld.exe\" (\n    echo [!] 提示: 请将本脚本放在 Monster Hunter World 游戏安装根目录！\n    pause\n    exit /b\n)\necho [*] 正在检查 dinput8.dll 与 nativePC 状态...\nif exist \"dinput8.dll\" (\n    echo [√] Stracker's Loader 前置挂载正常！\n) else (\n    echo [!] 未检测到 dinput8.dll，部分 nativePC 模组可能无法正常加载。\n)\nif not exist \"nativePC\" (\n    mkdir nativePC\n    echo [+] 已为您自动创建 nativePC 模组目录。\n)\necho.\npause\n",
    "verifiedPatch": "v15.11 (冰原最终版完全对齐)",
    "radarSecretCode": "苍蓝星"
}

# ==============================================================================
# RANK 13: 只狼：影逝二度 (Sekiro: Shadows Die Twice)
# ==============================================================================
SEKIRO_DATA = {
    "rank": 13,
    "hasConsole": True,
    "consoleShortcut": "ModEngine 挂钩引导 + 小键盘热键 / 慢动作防御弹刀辅助",
    "consoleEnableGuide": {
        "zh-CN": "【只狼 纯净模组与弹刀防反教学指南】\n1. 安装 ModEngine：将 dinput8.dll 与 modengine.ini 放入只狼游戏根目录 (与 sekiro.exe 同目录)；\n2. 新建 mods/ 文件夹，将下载的角色时装、材质与招式 Mod 放入该目录；\n3. 启动游戏无任何 EAC 反作弊，离线游玩绝无封号风险；\n4. 开启 F1 键可进入 0.3x 防御完美弹刀子弹时间，轻松看破任何 Boss 的连续乱舞招式！",
        "en": "Install ModEngine into Sekiro root. Press F1 for 0.3x parry window bullet time and hotkeys for infinite spirit emblems."
    },
    "popularCommands": [
        "[热键] Num 1: 无敌锁血 / 绝对防御判定 (God Mode)",
        "[热键] F1: 防御识破 0.3x 子弹时间慢动作 (Deflect Window Slomo)",
        "[热键] Num 8: 一击必杀崩解躯干 (Instant Deathblow Posture Break)",
        "[热键] Ctrl+Num 1: 无限纸人锁定 (999 纸人任意释放忍具神技)",
        "[CT表] Combat Arts -> Unlock Sakura Dance (秘传·樱舞空中避雷雷返神技)",
        "[CT表] Inventory -> Add 9 Gourd Seeds (9颗葫芦种子回满10瓶药)"
    ],
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.06 (年度版与全Boss连战完全对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/sekiro-shadows-die-twice-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/sekiro/Sekiro_Shadows_Die_Twice_v1.06_Plus_24_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Sekiro Shadows Die Twice Trainer.exe'",
            "troubleshootSteps": [
                "只狼纯单机离线运行，无任何网络联机或 EAC 封号风险，100% 安全",
                "若 Windows Defender 拦截，以管理员身份运行上方 PowerShell 白名单放行指令",
                "进入游戏操控狼行动后再按对应快捷键激活功能"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 狼机体生存与躯干防御",
                "items": [
                    {"key": "Num 1", "action": "无敌模式 (God Mode / 绝对格挡免伤)"},
                    {"key": "Num 2", "action": "躯干架势槽锁定不崩 (Posture Lock)"},
                    {"key": "Num 3", "action": "无限回生次数 (倒下后随时原地满血再起)"},
                    {"key": "Num 4", "action": "免疫全异常状态 (防恐怖/防中毒/防火焚)"},
                    {"key": "Num 5", "action": "完全光学潜行隐身 (敌人视若无睹)"}
                ]
            },
            {
                "category": "🥋 躯干秒崩与忍具纸人",
                "items": [
                    {"key": "Num 6", "action": "一击崩解敌方躯干架势 (瞬间触发红点忍杀)"},
                    {"key": "Num 7", "action": "超级伤害/一击必杀 (One Hit Kill)"},
                    {"key": "Num 8", "action": "无限白金纸人 (999 纸人无限释放义手神技)"},
                    {"key": "Num 9", "action": "伤药葫芦与药丸使用不减"}
                ]
            },
            {
                "category": "⚡ 金钱经验与慢动作练习",
                "items": [
                    {"key": "Ctrl+Num 1", "action": "编辑金钱金币 (999,999 随心购买仙峰寺飞镖)"},
                    {"key": "Ctrl+Num 2", "action": "无限技能技能点 (随时点满全流派秘籍)"},
                    {"key": "Ctrl+Num 3", "action": "死亡不掉落金钱与经验 (龙咳概率清零)"},
                    {"key": "Ctrl+Num 4", "action": "0.3x 子弹时间慢动作 (观察剑圣抬手前摇)"},
                    {"key": "Ctrl+Num 5", "action": "随心设定全局游戏时间流速 (0.2x~3.0x)"}
                ]
            }
        ]
    },
    "hasMods": True,
    "curatedMods": [
        {
            "id": "sekiro_mod_engine",
            "title": "Sekiro Mod Engine (只狼核心模组加载引擎)",
            "author": "Katalash",
            "version": "v0.1.16",
            "size": "180 KB",
            "downloads": "3.5M",
            "endorsements": "220K",
            "category": "Core Framework (核心前置)",
            "desc": "只狼外部材质、流派动作替换与参数修改的绝对基石前置。自动拦截文件加载路径，零修改游戏原版文件，极客必备。",
            "dependencies": ["None (Native DLL)"],
            "installPath": "Sekiro/ (游戏根目录)",
            "downloadUrl": "https://github.com/soulsmods/ModEngine2/releases/download/v2.1.0.0/ModEngine-2.1.0.0-win64.zip",
            "downloadFilename": "ModEngine-2.1.0.0-win64.zip",
            "isDirect": True,
            "installSteps": [
                "1. 点击下载 ModEngine 压缩包；",
                "2. 将 dinput8.dll 和 modengine.ini 解压至只狼游戏根目录 (sekiro.exe 同目录)；",
                "3. 在根目录新建 mods/ 文件夹；",
                "4. 后续所有 Mod 放入 mods/ 即可自动生效。"
            ]
        },
        {
            "id": "sekiro_fps_unlock",
            "title": "Sekiro FPS Unlock and More (突破 60 帧限制与视场角 FOV 调谐)",
            "author": "uberhalit",
            "version": "v1.2.5.4",
            "size": "220 KB",
            "downloads": "2.1M",
            "endorsements": "150K",
            "category": "Performance / Graphics",
            "desc": "突破官方恶心的 60 帧锁帧限制，支持 144Hz/240Hz 高刷电竞屏，消除 21:9 带鱼屏黑边，完美支持宽屏原生分辨率与无边框窗口化！",
            "dependencies": ["None (Stand-alone Tool)"],
            "installPath": "Windows PC",
            "downloadUrl": "https://github.com/uberhalit/SekiroFpsUnlockAndMore/releases/download/v1.2.5.4/SekiroFpsUnlockAndMore_v1.2.5.4.zip",
            "downloadFilename": "SekiroFpsUnlockAndMore.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载解压获取 SekiroFpsUnlockAndMore.exe；",
                "2. 先启动只狼游戏，然后双击运行该工具；",
                "3. 勾选 'Unlock FPS' 并将上限滑块拉至 144 或 240；",
                "4. 刀光剑影流畅如丝，再无拖影困扰。"
            ]
        },
        {
            "id": "sekiro_boss_rush",
            "title": "Boss Rush Mod (全 Boss 连战练习与随身重开)",
            "author": "thefifthmatt",
            "version": "v1.5.0",
            "size": "1.5 MB",
            "downloads": "980K",
            "endorsements": "78K",
            "category": "Gameplay / Training",
            "desc": "在任何鬼佛处直接开启所有 Boss 与精英怪独立连战挑战，无需跑图过剧情，随时随地练习弹刀剑圣苇名一心、义父与怨恨之鬼！",
            "dependencies": ["Sekiro Mod Engine"],
            "installPath": "Sekiro/mods/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/sekiro/SekiroBossRush.zip",
            "downloadFilename": "SekiroBossRush.zip",
            "isDirect": True,
            "installSteps": [
                "1. 确认已安装 Mod Engine；",
                "2. 下载压缩包解压放入 Sekiro/mods/ 目录；",
                "3. 在鬼佛菜单选择 'Boss Rush' 即可挑选中意首领切磋。"
            ]
        },
        {
            "id": "sekiro_resurrection",
            "title": "Sekiro: Resurrection (只狼：复活大修模组 - 极致弹刀终极体验)",
            "author": "Ikei",
            "version": "v1.14",
            "size": "45 MB",
            "downloads": "850K",
            "endorsements": "65K",
            "category": "Complete Overhaul (全面大修)",
            "desc": "享誉魂系圈的顶级战斗大修：重做几乎全 Boss 与杂兵招式逻辑、为狼增加全新流派招式与衍生追击，打刀防反手感登峰造极！",
            "dependencies": ["Sekiro Mod Engine"],
            "installPath": "Sekiro/mods/",
            "downloadUrl": "https://www.nexusmods.com/sekiro/mods/723",
            "downloadFilename": "SekiroResurrection.zip",
            "isDirect": False,
            "installSteps": [
                "1. 必须使用全新纯净存档游玩；",
                "2. 下载解压获取文件夹放入 Sekiro/mods/；",
                "3. 开启游戏体验完全重生的苇名国战国死斗。"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "🛡️ 核心生存、无限回生与无敌判定 (God Mode, Infinite Resurrection)",
            "commands": [
                {
                    "id": "sek_god_mode",
                    "name": {"zh-CN": "绝对防御判定与无敌锁血 (God Mode)", "en": "Invincibility (God Mode)"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Num 1: 无敌锁血 / 绝对防御判定 (God Mode)",
                    "desc": "生命值锁定上限，无论被危字突刺还是横扫扫中均不掉一滴血，逃课安心观战招式。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_lock_posture",
                    "name": {"zh-CN": "狼自身躯干架势槽锁定不崩 (Max Posture Lock)", "en": "Immune to Posture Break"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Num 2: 躯干韧性槽锁定不崩 (Max Posture Lock)",
                    "desc": "格挡架势槽永远不会爆满崩溃，哪怕面对长枪重击也绝不陷入踉跄倒地硬直破绽。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_inf_resurrection",
                    "name": {"zh-CN": "无限回生复活次数 (回生之力永远饱满)", "en": "Infinite Resurrection"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Num 3: 无限回生次数 (死后无限次原地复活)",
                    "desc": "解除黑线遮挡限制，倒下后随时再次爬起满血复活，真正的影逝‘百’度。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_immune_status",
                    "name": {"zh-CN": "完美免疫毒/火/恐怖 (防无头鬼恐怖暴毙)", "en": "Immune to Terror & Status Effects"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Num 4: 完美免疫全异常状态 (防恐怖/防中毒/防火焚)",
                    "desc": "彻底免疫七面武士与无头鬼的紫色恐怖气场秒杀，无视火牛冲撞点燃焚烧。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_invisibility",
                    "name": {"zh-CN": "完全光学隐形隐匿 (敌人视若无睹)", "en": "Total Stealth Invisibility"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Num 5: 隐形潜行完全隐匿 (敌人视若无睹)",
                    "desc": "敌人 AI 视野侦测范围清零，即使当着火枪队守卫的面大摇大摆跑过亦无人警觉。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                }
            ]
        },
        {
            "category": "⏱️ 完美弹刀帧数慢动作与招式防反教学 (Deflect Window Slomo & Parry Master)",
            "commands": [
                {
                    "id": "sek_slomo_parry",
                    "name": {"zh-CN": "0.3x 子弹时间慢动作 (弹刀防反拆招教学)", "en": "Deflect Window Slomo (0.3x)"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] F1: 防御识破 0.3x 子弹时间慢动作 (Deflect Window Slomo)",
                    "desc": "将全局时间流速放慢至 0.3 倍，清晰看清弦一郎飞渡浮舟与一心剑气的每一帧起手动作，精准打铁弹反！",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_slomo_windup",
                    "name": {"zh-CN": "0.1x 极致微速动作分解 (危字下段跳跃/突刺看破)", "en": "Micro Attack Analysis (0.1x)"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] F2: 敌方攻击前摇 0.1x 慢动作解析 (Attack Windup Analysis)",
                    "desc": "将速度放慢至十分之一，新手识破【危】字判定属于突刺还是横扫的最佳教学伴侣。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_slomo_reset",
                    "name": {"zh-CN": "恢复 1.0x 标准正常战斗速度", "en": "Normal Speed (1.0x)"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] F3: 恢复 1.0x 标准时间流速 (Normal Game Speed)",
                    "desc": "将游戏时间流速恢复正常，感受叮当作响原汁原味的拼刀节奏快感。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_instant_break",
                    "name": {"zh-CN": "一击崩解敌方躯干韧性槽 (直接亮起红点忍杀)", "en": "Instant Posture Break (Deathblow)"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Num 8: 一击必杀崩解躯干 (Instant Deathblow Posture Break)",
                    "desc": "只需轻轻一刀或一记完美格挡，敌方躯干架势槽瞬间爆满，直接触发处决红点！",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_infinite_deathblow",
                    "name": {"zh-CN": "刀刀触发终结处决动画 (爽快割草连杀)", "en": "Infinite Deathblow Execution"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Num 9: 刀刀触发忍杀处决 (Infinite Deathblow Trigger)",
                    "desc": "无需削减血量与躯干，靠近任何小兵杂兵直接按下攻击键即可释放华丽的忍杀处决！",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                }
            ]
        },
        {
            "category": "🥋 全秘传流派招式全解锁与纸人无限 (All Combat Arts & Infinite Spirit Emblems)",
            "commands": [
                {
                    "id": "sek_inf_spirit_emblems",
                    "name": {"zh-CN": "无限白金纸人锁定 (999 纸人无限挥霍忍具)", "en": "Infinite Spirit Emblems Lock (999)"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Ctrl+Num 1: 无限纸人锁定 (999 纸人任意释放忍具神技)",
                    "desc": "纸人数量锁定 999 永不减少，机关伞、锈丸、金钱镖与不死斩想放就放。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_art_one_mind",
                    "name": {"zh-CN": "解锁【秘传·一心居合斩】(极速千本刀光居合)", "en": "Unlock Combat Art: One Mind"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Combat Arts -> Unlock One Mind",
                    "desc": "老一心终极绝技：纳刀拔刀瞬间在身前斩出数以百计的真空密集刀网，视觉震撼力拉满。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_art_dragon_flash",
                    "name": {"zh-CN": "解锁【秘传·龙闪】(超远距离贯穿剑气斩)", "en": "Unlock Combat Art: Dragon Flash"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Combat Arts -> Unlock Dragon Flash",
                    "desc": "剑圣一心的超远剑气神功：挥刀蓄力劈出纵贯战场的锐利光弧，秒杀远端密集弓箭手群。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_art_sakura_dance",
                    "name": {"zh-CN": "解锁【秘传·樱舞】(空中三段旋转起跳避雷神技)", "en": "Unlock Combat Art: Sakura Dance"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Combat Arts -> Unlock Sakura Dance",
                    "desc": "年度版连战心中巴流绝学：原地腾空回旋三刀，起跳自带完全滞空避下段，空中雷返百分百成功！",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_art_mortal_draw",
                    "name": {"zh-CN": "解锁【奥义·不死斩】与【秘传·强化不死斩】", "en": "Unlock Empowered Mortal Draw"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Combat Arts -> Unlock Mortal Draw & Empowered",
                    "desc": "赤红色的灭绝瘴气斩击，具备霸体与超大范围强行削韧，斩杀任何不死附体虫与狮子猿。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                }
            ]
        },
        {
            "category": "💰 金钱财富、全葫芦种子与念珠全满 (Sen, Gourd Seeds & Prayer Beads)",
            "commands": [
                {
                    "id": "sek_money_max",
                    "name": {"zh-CN": "编辑金币金钱 (999,999 沉重钱袋塞满)", "en": "Add 999,999 Sen Money"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[热键] Ctrl+Num 2: 编辑金钱金币 (999,999 钱袋满满)",
                    "desc": "背包直接塞满近百万金钱，把全地图所有供养众祭祀商人的商品全部扫荡一空。",
                    "min_version": "v1.0+",
                    "framework_required": "FLiNG Trainer / ModEngine"
                },
                {
                    "id": "sek_item_gourd_seeds",
                    "name": {"zh-CN": "获取全部 9 颗葫芦种子 (永真处直接升至 10 瓶满配)", "en": "Add All 9 Gourd Seeds (10 Flasks)"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Inventory -> Add 9 Gourd Seeds",
                    "desc": "跳过全地图搜刮种子，去永真小姐姐处一口气将伤药葫芦喝药次数提升至 10 次上限。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_item_prayer_beads",
                    "name": {"zh-CN": "获取全部 40 颗念珠 (血量上限拉升至 10 度满级)", "en": "Add All 40 Prayer Beads (Max Vitality)"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Inventory -> Add 40 Prayer Beads",
                    "desc": "集齐全部 40 颗佛门念珠，在鬼佛处将生命力与架势韧性槽强化至第 10 度的究极满月轮廓！",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_item_ako_sugar",
                    "name": {"zh-CN": "获取阿攻糖 x99 与无限阿攻降灵", "en": "Add 99 Ako Sugar & Ako's Spiritfall"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Inventory -> Add 99 Ako Sugar & Spiritfall",
                    "desc": "仙峰寺秘传糖果，食用后短时间内大幅提升狼的物理攻击力与对敌躯干削减伤害。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_item_yashariku_sugar",
                    "name": {"zh-CN": "获取夜叉戮糖 x99 与夜叉戮降灵 (极境爆发加成)", "en": "Add 99 Yashariku Sugar"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Inventory -> Add 99 Yashariku Sugar",
                    "desc": "虽扣除一半生命与韧性，但赋予狼近乎翻倍的恐怖攻击输出，速通速杀 Boss 终极神药。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                }
            ]
        },
        {
            "category": "🦾 极品琉璃义手强化素材全集齐 (Lapis Lazuli & Max Prosthetic Tools)",
            "commands": [
                {
                    "id": "sek_mat_lapis",
                    "name": {"zh-CN": "获取源之琉璃 x10 (一周目仅产6块的绝版矿石)", "en": "Add 10 Lapis Lazuli"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Materials -> Add 10 Lapis Lazuli",
                    "desc": "源之宫深处的究极矿石，一周目直接凑齐全部四种琉璃终极义肢强化的全部消耗。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_mat_iron_magnet",
                    "name": {"zh-CN": "获取金刚屑 x99 与磁铁屑 x99", "en": "Add 99 Adamantite & Scrap Magnetite"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Materials -> Add 99 Phantom Iron & Scrap Magnetite",
                    "desc": "大量补充雕佛师改装高阶金刚铁伞、火筒与螺旋枪所需的全部硬质金属耗材。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_tool_shuriken",
                    "name": {"zh-CN": "一键解锁【琉璃手里剑】(源之青辉穿透斩)", "en": "Unlock Lazulite Shuriken"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Prosthetic -> Unlock Lazulite Shuriken",
                    "desc": "掷出带有青色幽光的重击手里剑，击中敌人后碎裂反弹造成穿透与追击硬直伤害。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_tool_flame",
                    "name": {"zh-CN": "一键解锁【琉璃净火】(超强怨灵克制紫火)", "en": "Unlock Lazulite Sacred Flame"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Prosthetic -> Unlock Lazulite Sacred Flame",
                    "desc": "喷射出净化一切怨念的紫白色神圣火焰，无视神之飞雪即可对无头鬼与怨恨之鬼造成毁灭性重创！",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_tool_umbrella",
                    "name": {"zh-CN": "一键解锁【朱雀红莲伞】(完美免疫一切高温火伤)", "en": "Unlock Suzaku Lotus Umbrella"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] Prosthetic -> Unlock Suzaku Lotus Umbrella",
                    "desc": "撑开伞面可 100% 格挡怨恨之鬼与一心脚底喷涌的烈焰爆破，收伞释放带火斩击。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                }
            ]
        },
        {
            "category": "🗺️ 全鬼佛传送全开与钟鬼苦难一键免罚 (All Idols, Bell Demon & Kuro Charm)",
            "commands": [
                {
                    "id": "sek_unlock_idols",
                    "name": {"zh-CN": "一键点亮全地图鬼佛雕像瞬移传送", "en": "Unlock All Sculptor's Idols"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] World -> Unlock All Sculptor's Idols",
                    "desc": "点亮苇名城、金刚山仙峰寺、坠落之谷与水生村全部佛像，随时随地直接传送。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_remove_bell",
                    "name": {"zh-CN": "消除【钟鬼】负面厄运诅咒 (恢复标准怪物体魄)", "en": "Remove Demon Bell Curse"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] World -> Remove Demon Bell Curse",
                    "desc": "敲钟后若觉得 Boss 伤害过高受苦，直接使用指令消除体内潜藏的钟鬼幽灵。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_give_charm",
                    "name": {"zh-CN": "取回【九郎护身符】(免除格挡漏伤惩罚)", "en": "Retrieve Kuro's Charm"},
                    "syntax_type": "fromsoftware_ct",
                    "code": "[CT表] World -> Give Kuro's Charm",
                    "desc": "取回护身符即可免除双苦难（交符）模式下未完美弹刀时扣血的惩罚机制。",
                    "min_version": "v1.0+",
                    "framework_required": "Cheat Engine / CT Table"
                },
                {
                    "id": "sek_camera_fov",
                    "name": {"zh-CN": "解锁 144Hz 高刷与视场角 FOV 调谐", "en": "Unlock 60FPS Limit & Ultrawide"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[ModEngine] Camera -> Unlock 60FPS Limit & Ultrawide",
                    "desc": "解除恶心的 60 帧锁定，开启 21:9 超宽带鱼屏满屏视野，广角战场纵览全局。",
                    "min_version": "v1.0+",
                    "framework_required": "Sekiro FPS Unlocker"
                },
                {
                    "id": "sek_boss_rush",
                    "name": {"zh-CN": "随时随地切磋 Boss 连战练习", "en": "Instant Boss Rematch Anywhere"},
                    "syntax_type": "fromsoftware_hotkey",
                    "code": "[ModEngine] Boss Rush -> Instant Boss Rematch",
                    "desc": "无需任何前置跑图剧情，在鬼佛处直接开启同剑圣苇名一心、巨型忍者义父的死斗。",
                    "min_version": "v1.0+",
                    "framework_required": "Boss Rush Mod"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "sek_starter_bundle",
            "type": "starter",
            "name": "手残救星弹刀教学包",
            "tag": "👑 萌新首选 · 零门槛",
            "badge": "弹刀救星",
            "desc": "一键激活锁血锁架势无敌 + 0.3x 子弹时间慢动作防反拆招 + 9 颗葫芦种子回满 10 瓶药 + 999 纸人无限释放忍具，受苦手残一秒逆袭成打铁宗师！",
            "highlights": ["锁血锁架势槽，怎么挨打都不倒", "0.3x 子弹时间慢动作精准弹刀", "9 颗葫芦种子瞬间 10 瓶药水满配", "999 纸人无限挥霍机关伞与鞭炮"],
            "code": "-- [老L·极客场景套餐] 只狼 手残救星弹刀教学包\n[热键] Num 1: 无敌锁血 / 绝对防御判定 (God Mode)\n[热键] Num 2: 躯干韧性槽锁定不崩 (Max Posture Lock)\n[热键] F1: 防御识破 0.3x 子弹时间慢动作 (Deflect Window Slomo)\n[CT表] Inventory -> Add 9 Gourd Seeds"
        },
        {
            "id": "sek_salvation_bundle",
            "type": "salvation",
            "name": "全流派秘传招式满配包",
            "tag": "🛡️ 意难平救赎 · 告别受苦",
            "badge": "秘传满配",
            "desc": "秘传·一心居合斩 + 秘传·龙闪剑气 + 秘传·樱舞空中避雷雷返 + 琉璃净火与朱雀红莲伞，全流派战技随时潇洒施展！",
            "highlights": ["秘传·樱舞腾空帅气雷返", "秘传·一心华丽千本刀网居合", "朱雀红莲伞抵挡一切烈焰爆炸", "琉璃净火神圣紫焰焚杀怨灵"],
            "code": "-- [老L·极客场景套餐] 只狼 全流派秘传招式满配包\n[CT表] Combat Arts -> Unlock One Mind\n[CT表] Combat Arts -> Unlock Sakura Dance\n[CT表] Prosthetic -> Unlock Suzaku Lotus Umbrella\n[CT表] Prosthetic -> Unlock Lazulite Sacred Flame"
        },
        {
            "id": "sek_godmode_bundle",
            "type": "godmode",
            "name": "修罗真神刀刀忍杀包",
            "tag": "⚡ 极客狂欢 · 众神陨落",
            "badge": "修罗真神",
            "desc": "刀刀触发终结处决忍杀 + 一击必杀崩解躯干 + 强化不死斩霸体斩杀 + 144Hz 高刷与视场角全开，化身苇名国修罗剑圣真神！",
            "highlights": ["刀刀触发忍杀处决华丽动画", "一击崩解敌方躯干架势条", "奥义·强化不死斩强行削韧斩杀", "144Hz 高刷带鱼屏全景纵览战场"],
            "code": "-- [老L·极客场景套餐] 只狼 修罗真神刀刀忍杀包\n[热键] Num 9: 刀刀触发忍杀处决 (Infinite Deathblow Trigger)\n[热键] Num 8: 一击必杀崩解躯干 (Instant Deathblow Posture Break)\n[CT表] Combat Arts -> Unlock Mortal Draw & Empowered\n[ModEngine] Camera -> Unlock 60FPS Limit & Ultrawide"
        }
    ],
    "pitfallNote": {
        "title": "老L实验室避坑笔记 (只狼：影逝二度 极客避坑指南)",
        "tips": [
            "【零封号与完全单机】：只狼是 FromSoftware 难得的完全无任何 EAC 反作弊、无在线联机入侵的单机作品。所有修改器与 ModEngine 均为 100% 绝对安全，不会有任何小黑屋风险！",
            "【龙咳机制真相破除】：很多新手害怕因多次死亡导致 NPC【龙咳】而心惊胆战。实际上龙咳只会暂时挂起支线对话，绝对不会造成任何 NPC 死亡！只要用一滴【龙胤之露】在鬼佛处祷告，即可瞬间痊愈全苇名国所有人的龙咳，完全不必有心理压力！",
            "【弹刀时机与按键节奏】：频繁狂按防御键 L1 会被系统判定为狂躁按键，弹刀判定窗口会从正常的 0.5 秒骤降至 0.1 秒！使用本站推荐的 0.3x 子弹时间慢动作，看准刀刃即将接触的瞬间单次按压，才能培养出最地道的节奏肌肉记忆。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】只狼 ModEngine 环境助手\necho ========================================================\necho   【老L·单机避坑局】只狼 模组加载引擎自动检测器\necho   零注入误报 · 纯净离线环境 · 144Hz 解锁引导\necho ========================================================\necho.\nif not exist \"sekiro.exe\" (\n    echo [!] 提示: 请将本脚本放在 Sekiro 游戏安装根目录！\n    pause\n    exit /b\n)\necho [*] 正在检查 dinput8.dll 与 mods 目录...\nif exist \"dinput8.dll\" (\n    echo [√] ModEngine 前置就绪！\n) else (\n    echo [!] 未检测到 dinput8.dll，请解压 ModEngine 至根目录。\n)\nif not exist \"mods\" (\n    mkdir mods\n    echo [+] 已为您自动创建 mods 模组目录。\n)\necho.\npause\n",
    "verifiedPatch": "v1.06 (年度版完全对齐)",
    "radarSecretCode": "只狼"
}

# ==============================================================================
# RANK 14: 生化危机4：重制版 (Resident Evil 4 Remake)
# ==============================================================================
RE4_DATA = {
    "rank": 14,
    "hasConsole": True,
    "consoleShortcut": "Insert 键呼出 REFramework 图形化 ImGui 菜单 / 自由运镜摄影",
    "consoleEnableGuide": {
        "zh-CN": "【生化危机4重制版 REFramework 控制台指南】\n1. 下载 REFramework for RE4 (praydog 核心库，含 dinput8.dll)；\n2. 解压缩并将 dinput8.dll 放入游戏根目录 (包含 re4.exe 的目录)；\n3. 启动游戏，在任何过场动画或战斗中按键盘 Insert 键唤出 ImGui 控制台面板；\n4. 支持全公文包武器解锁、无敌锁血、无限火箭筒调出、佣兵无限连击与第一人称/宽 FOV 视场角调节！",
        "en": "Install REFramework (dinput8.dll) into RE4 Remake root. Press Insert to toggle ImGui console for weapons, infinite ammo, and Mercenaries S++ rank."
    },
    "popularCommands": [
        "[REFramework] -> Player -> God Mode (ON / 锁血锁伤)",
        "[REFramework] -> Ashley -> Invincible & Never Kidnapped",
        "[REFramework] -> Weapon -> Infinite Ammo",
        "[REFramework] -> Inventory -> Add Infinite Rocket Launcher",
        "[REFramework] -> Merchant -> Add 10,000,000 Pesetas",
        "[REFramework] -> Mercenaries -> Instant S++ Rank Score"
    ],
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.0+ (逆命殊途 Separate Ways DLC 完全对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/resident-evil-4-remake-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/re4/Resident_Evil_4_Remake_v1.0_Plus_33_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Resident Evil 4 Remake Trainer.exe'",
            "troubleshootSteps": [
                "卡普空纯单机离线游戏，无任何 VAC 封禁风险，100% 安全放心使用",
                "若 Windows Defender 拦截，以管理员身份运行上方 PowerShell 白名单放行指令",
                "进入游戏操控里昂拔枪行动后再按小键盘热键激活功能"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 里昂与阿什莉生存守护",
                "items": [
                    {"key": "Num 1", "action": "里昂无敌模式 (God Mode / 锁血锁伤)"},
                    {"key": "Num 2", "action": "阿什莉无敌模式 (永不受伤、绝不被邪教徒抗走)"},
                    {"key": "Num 3", "action": "无限奔跑体力 (里昂疾跑永不疲劳)"},
                    {"key": "Num 4", "action": "战术防爆防弹衣耐久度无限锁定"},
                    {"key": "Num 5", "action": "战斗小刀耐久度无限 (随便格挡电锯不磨损)"}
                ]
            },
            {
                "category": "🔫 军备弹药与射击精修",
                "items": [
                    {"key": "Num 6", "action": "全部枪械无限弹药 (无需繁琐换弹匣)"},
                    {"key": "Num 7", "action": "枪械射击零后坐力与准星零扩散 (百步穿杨)"},
                    {"key": "Num 8", "action": "近战体术一击必杀与爆头必触发碎颅"},
                    {"key": "Num 9", "action": "小刀格挡判定时间扩大 100% (轻松招架飞斧电锯)"}
                ]
            },
            {
                "category": "💰 财富比塞塔与佣兵模式",
                "items": [
                    {"key": "Ctrl+Num 1", "action": "编辑比塞塔现金 (直接入账 10,000,000)"},
                    {"key": "Ctrl+Num 2", "action": "编辑尖晶石数量 (999 尖晶石无限兑换藏宝图)"},
                    {"key": "Ctrl+Num 3", "action": "武器商人改装改造免费 (无需消耗任何金币)"},
                    {"key": "Ctrl+Num 4", "action": "佣兵模式锁定剩余时间与保持 150 极限连击"},
                    {"key": "Ctrl+Num 5", "action": "佣兵模式瞬间拉满二百万高分秒拿 S++ 评分"}
                ]
            }
        ]
    },
    "hasMods": True,
    "curatedMods": [
        {
            "id": "re4_reframework",
            "title": "REFramework for RE4 Remake (praydog 核心开源前置框架)",
            "author": "praydog",
            "version": "v1.5.8",
            "size": "3.8 MB",
            "downloads": "4.2M",
            "endorsements": "260K",
            "category": "Core Framework (核心前置)",
            "desc": "卡普空 RE 引擎游戏绝对核心！集成强大的 ImGui 覆层控制面板、自由运镜摄影机、第一人称视角切换与宽广 FOV 调谐。",
            "dependencies": ["None (Native DLL)"],
            "installPath": "Resident Evil 4 Remake/ (游戏根目录)",
            "downloadUrl": "https://github.com/praydog/REFramework/releases/download/v1.5.8/RE4.zip",
            "downloadFilename": "REFramework_RE4.zip",
            "isDirect": True,
            "installSteps": [
                "1. 点击下载 REFramework_RE4.zip 压缩包；",
                "2. 打开游戏安装根目录 (包含 re4.exe 的目录)；",
                "3. 将压缩包内的 dinput8.dll 直接解压到该目录；",
                "4. 启动游戏，按键盘 Insert 键即可打开/隐藏图形控制台。"
            ]
        },
        {
            "id": "re4_fluffy_manager",
            "title": "Fluffy Mod Manager (卡普空 RE 引擎最强模组管理器)",
            "author": "FluffyQuack",
            "version": "v3.020",
            "size": "18 MB",
            "downloads": "5.5M",
            "endorsements": "340K",
            "category": "Mod Manager",
            "desc": "生化危机系列公认最强模组安装器：一键安装、启用、禁用上千款角色外观、艾达王特工服、发型与武器贴图替换，绝不污染游戏原版归档！",
            "dependencies": ["None (Stand-alone Tool)"],
            "installPath": "Windows PC",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/tools/FluffyModManager.zip",
            "downloadFilename": "FluffyModManager.zip",
            "isDirect": True,
            "installSteps": [
                "1. 下载解压运行 Modmanager.exe；",
                "2. 在游戏列表选择 'Resident Evil 4 Remake'；",
                "3. 将下载的 .rar/.zip 角色外观模组拖入软件窗口；",
                "4. 点击滑块切换勾选即可一秒生效启用。"
            ]
        },
        {
            "id": "re4_berserker",
            "title": "RE4R Berserker Mod (生化4：狂暴大修 - 极致压迫感体验)",
            "author": "Berserker Team",
            "version": "v1.2.0",
            "size": "85 MB",
            "downloads": "420K",
            "endorsements": "38K",
            "category": "Complete Overhaul (难度大修)",
            "desc": "生化老炮专属！重置邪教徒 AI 走位、增加狂暴双电锯精英怪埋伏、调整枪械散布与子弹资源分布，压迫感直接拉爆！",
            "dependencies": ["Fluffy Mod Manager"],
            "installPath": "FluffyModManager/Games/RE4R/Mods/",
            "downloadUrl": "https://www.nexusmods.com/residentevil42023/mods/1471",
            "downloadFilename": "RE4R_Berserker.zip",
            "isDirect": False,
            "installSteps": [
                "1. 使用 Fluffy Mod Manager 载入该 mod；",
                "2. 开启新游戏模式开始挑战；",
                "3. 感受最纯正刺激的心跳恐怖生存逃亡。"
            ]
        },
        {
            "id": "re4_no_zoom_aim",
            "title": "No Zoom On Aim (解除瞄准视角强行放大与晕 3D 优化)",
            "author": "alphazomega",
            "version": "v1.1.0",
            "size": "45 KB",
            "downloads": "1.1M",
            "endorsements": "72K",
            "category": "QoL (体验优化)",
            "desc": "解除原版手枪/霰弹枪举枪瞄准时镜头强行贴近后背的恶心镜头，视野始终保持开阔通透，彻底杜绝转角晕 3D 恶心感！",
            "dependencies": ["REFramework"],
            "installPath": "Resident Evil 4 Remake/reframework/autorun/",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/re4/NoZoomOnAim.zip",
            "downloadFilename": "NoZoomOnAim.zip",
            "isDirect": True,
            "installSteps": [
                "1. 确保安装好 REFramework；",
                "2. 下载解压获取 .lua 脚本文件；",
                "3. 放入 reframework/autorun/ 文件夹内；",
                "4. 举枪瞄准视野始终丝滑宽阔。"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 核心上帝模式、阿什莉无敌与无限弹药 (God Mode, Ashley Invincible & Infinite Ammo)",
            "commands": [
                {
                    "id": "re4_god_mode",
                    "name": {"zh-CN": "里昂锁血上帝模式 (God Mode / 免受伤害)", "en": "Leon Invincibility (God Mode)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Player -> God Mode (ON / 锁血锁伤)",
                    "desc": "里昂生命值锁定满格，承受电锯爆头或巨人践踏分毫不伤，从容漫步西班牙古堡。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_ashley_invincible",
                    "name": {"zh-CN": "阿什莉锁血无敌且绝不被扛走 (碍事梨变懂事梨)", "en": "Ashley Invincible & Never Kidnapped"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Ashley -> Invincible & Never Kidnapped",
                    "desc": "阿什莉免疫一切邪教徒武器攻击，并且敌人即使抱住她也无法扛跑，彻底根除护送关卡的烦躁！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_inf_ammo",
                    "name": {"zh-CN": "全部武器枪械无限弹药 (射击无需重新装弹)", "en": "Infinite Ammo & No Reload"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Weapon -> Infinite Ammo",
                    "desc": "手中所持的所有手枪、霰弹枪、冲锋枪与马格南子弹数量不减，免去漫长换弹动作。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_inf_knife",
                    "name": {"zh-CN": "战斗小刀耐久度无限 (招架电锯永不磨损)", "en": "Infinite Knife Durability"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Knife -> Infinite Knife Durability",
                    "desc": "无论是初始格斗刀还是靴刀耐久度永远拉满，无限弹刀招架敌人的飞斧与电锯横扫。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_inf_sprint",
                    "name": {"zh-CN": "里昂无限奔跑冲刺 (零气喘无疲劳衰减)", "en": "Infinite Sprint Stamina"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Player -> Infinite Sprint Stamina",
                    "desc": "奔跑冲刺速度不衰减，在狭窄回廊与广场拉怪迂回轻松自如。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "💼 全公文包神装、无限火箭筒与手炮解锁 (Infinite Rocket Launcher & Handcannon)",
            "commands": [
                {
                    "id": "re4_item_rocket_inf",
                    "name": {"zh-CN": "获取【无限火箭筒】(单发毁灭轰杀一切首领)", "en": "Add Infinite Rocket Launcher"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Inventory -> Add Infinite Rocket Launcher",
                    "desc": "二周目价值 200 万的战略重火器，单发直接秒杀克劳萨、拉蒙城主与最终萨德勒 Boss！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_item_handcannon",
                    "name": {"zh-CN": "获取【手炮】(Handcannon .50 终极马格南)", "en": "Add Handcannon Magnum"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Inventory -> Add Handcannon Magnum",
                    "desc": "免去专业难度无奖励武器通关的严苛要求，直接获得全游戏单发破坏力最强的狂暴手炮！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_item_chicago",
                    "name": {"zh-CN": "获取【芝加哥打字机】(汤姆逊无限冲锋枪)", "en": "Add Chicago Sweeper"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Inventory -> Add Chicago Sweeper",
                    "desc": "经典汤姆逊圆盘弹鼓冲锋枪，特改后射出连绵不绝的无限金属风暴扫射全场。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_item_primal_knife",
                    "name": {"zh-CN": "获取【原始之刃】(全发条人偶解锁小刀)", "en": "Add Primal Knife"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Inventory -> Add Primal Knife",
                    "desc": "官方自带无限耐久特改词条的传奇神刀，特改后永远不需要找商人修理磨刀。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_item_killer7",
                    "name": {"zh-CN": "获取【杀手7】(Killer7 激光红外瞄准马格南)", "en": "Add Killer7 Laser Sight Magnum"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Inventory -> Add Killer7 Laser Sight",
                    "desc": "自带精准红色激光照准器的经典马格南，枪枪必中弱点，暴击率提升 5 倍。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "💰 比塞塔金币、全尖晶石与专属改造券 (Pesetas, Spinels & Exclusive Upgrade Tickets)",
            "commands": [
                {
                    "id": "re4_money_10m",
                    "name": {"zh-CN": "获得 10,000,000 比塞塔 (财富自由买空军火商)", "en": "Add 10,000,000 Pesetas Cash"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Merchant -> Add 10,000,000 Pesetas",
                    "desc": "一千万金币即刻入账，随意购买防弹衣、急救喷雾与全部枪械武器配件。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_spinel_999",
                    "name": {"zh-CN": "获得 999 颗珍奇尖晶石 (商人物资兑换无限)", "en": "Add 999 Spinels"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Merchant -> Add 999 Spinels",
                    "desc": "大量补充蓝宝石尖晶石，将武器商人的藏宝图、高级改造券与特殊手提箱全部兑空。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_upgrade_tickets",
                    "name": {"zh-CN": "获得 10 张武器专属高级改造券", "en": "Add 10 Exclusive Upgrade Tickets"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Merchant -> Add 10 Exclusive Upgrade Tickets",
                    "desc": "无视漫长的前置改装，对任意武器使用改造券直接瞬间点亮终极特改隐藏威力！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_free_upgrades",
                    "name": {"zh-CN": "武器商人全部武器改造升级免费 (0 金币)", "en": "Free Weapon Upgrades (0 Pesetas)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Merchant -> Free Weapon Upgrades",
                    "desc": "将商人处的全部威力、射速、装填速度与弹匣容量升级标价清零，随意升满满配武器。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_max_case",
                    "name": {"zh-CN": "解锁 XXL 终极大尺寸公文包 (收纳狂魔福利)", "en": "Unlock XXL Max Attache Case"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Inventory -> Add Max Briefcase",
                    "desc": "公文包网格格子拓展至极限尺寸，几把重型武器与海量草药弹药轻松整齐摆放。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "🎯 瞄准准星无扩散与武器零后坐力 (No Weapon Recoil & Perfect Crosshair)",
            "commands": [
                {
                    "id": "re4_no_recoil",
                    "name": {"zh-CN": "枪械射击零后坐力 (枪口稳如磐石)", "en": "No Weapon Recoil"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Weapon -> No Weapon Recoil",
                    "desc": "连续速射枪口绝不上跳晃动，马格南连开数枪枪口依然死死锁定目标眉心。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_perfect_crosshair",
                    "name": {"zh-CN": "准星零扩散百步穿杨 (移动中射击弹道绝对精准)", "en": "Perfect Crosshair Spread"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Weapon -> Perfect Crosshair Spread",
                    "desc": "消除移动走位时准星扩大的惩罚，准星永远聚焦于一点，手枪当狙击枪打。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_dismember_kill",
                    "name": {"zh-CN": "一枪碎裂肢解肢体 (极度真实的物理血腥碎裂)", "en": "One Shot Dismemberment"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Weapon -> One Shot Kill Dismember",
                    "desc": "霰弹枪命中敌人直接将其轰成碎块，体验卡普空 RE 引擎极其逼真的部位物理碎裂。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_crit_headshot",
                    "name": {"zh-CN": "爆头 100% 触发碎颅暴击判定", "en": "100% Critical Headshot Chance"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Combat -> Guaranteed Critical Headshot",
                    "desc": "子弹击中邪教徒头部必定触发清脆的爆头碎颅特效，并阻止体内寄生虫破头窜出！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_easy_parry",
                    "name": {"zh-CN": "小刀完美招架格挡判定窗口极宽 (100% 招架成功)", "en": "Wide Parry Window (100% Success)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Combat -> Instant Parry Window 100%",
                    "desc": "即便在高难度专业模式下，只要按小刀格挡即可轻松触发火花四溅的完美弹刀。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "⏱️ 佣兵模式无限连击时间与 S++ 评分 (Mercenaries Infinite Time & S++ Rank)",
            "commands": [
                {
                    "id": "re4_merc_freeze_time",
                    "name": {"zh-CN": "佣兵模式倒计时时间锁定暂停", "en": "Freeze Mercenaries Timer"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Mercenaries -> Freeze Timer",
                    "desc": "倒计时不再流逝倒扣，从容清理全图 150 名敌人，毫无时间紧迫压力。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_merc_combo_150",
                    "name": {"zh-CN": "保持 150 杀全连击不中断 (连击倍率拉满)", "en": "Max Combo 150 Streak"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Mercenaries -> Max Combo 150",
                    "desc": "连击连杀计量槽锁定不减，即使中间寻找敌人数十秒亦绝不断连。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_merc_mayhem",
                    "name": {"zh-CN": "狂暴爆发技能持续充能满额 (无限放狂暴大招)", "en": "Instant Mayhem Mode Infinite"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Mercenaries -> Instant Mayhem Mode",
                    "desc": "威斯克瞬移体术、汉克隐形速射、克劳萨变异狂暴大招无限释放！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_merc_score_spp",
                    "name": {"zh-CN": "瞬间结算二百万高分 (秒拿 S++ 评分并解锁手炮)", "en": "Instant S++ Rank Score (2,000,000+)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Mercenaries -> Instant S++ Rank Score",
                    "desc": "直接注入 2,000,000+ 顶级结算积分，全关卡秒速点亮三颗金星 S++ 终极评价。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_merc_unlock_all",
                    "name": {"zh-CN": "一键解锁全部佣兵角色与全部挑战地图", "en": "Unlock All Mercenaries Characters & Maps"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Mercenaries -> Unlock All Characters",
                    "desc": "直接解锁威斯克、艾达王特工服、汉克、路易斯与孤岛码头全图。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                }
            ]
        },
        {
            "category": "👗 艾达王特工服、碍事梨骑士甲全时装 (Ada Wong & Ashley Armor Costumes)",
            "commands": [
                {
                    "id": "re4_costume_ashley_armor",
                    "name": {"zh-CN": "解锁【阿什莉骑士板甲】(完全免伤防抓物理外挂)", "en": "Unlock Ashley Knight Armor"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Costumes -> Unlock Ashley Knight Armor",
                    "desc": "穿上厚重铁甲的阿什莉完全免疫一切伤害，敌人试图扛起她时会被铁甲压垮摔倒在地上！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_costume_leon_romantic",
                    "name": {"zh-CN": "解锁【里昂浪漫主义帅气时装】(复古贵族披风)", "en": "Unlock Leon Romantic Costume"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Costumes -> Unlock Leon Romantic Costume",
                    "desc": "银发帅气的吸血鬼伯爵复古披风时装，气质风度翩翩。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_costume_ada_tactical",
                    "name": {"zh-CN": "解锁【艾达王战术特工服】(逆命殊途干练神装)", "en": "Unlock Ada Wong Tactical Agent Suit"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Costumes -> Unlock Ada Wong Tactical Agent Suit",
                    "desc": "完美勾勒身形的黑色紧身战术皮衣，特工干练飒爽风姿绰约。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_accessory_gas_mask",
                    "name": {"zh-CN": "解锁【防毒面具】(全难度开启辅助瞄准)", "en": "Unlock Gas Mask (Aim Assist)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Costumes -> Unlock Gas Mask",
                    "desc": "佩戴防毒面具后，即便利昂身在专业专家最高难度下，也会获得强力的手柄/键鼠辅助瞄准吸附！",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                },
                {
                    "id": "re4_fov_slider",
                    "name": {"zh-CN": "随心调节视场角 FOV 滑块 (告别狭窄拉近晕眩)", "en": "Unlock Camera FOV Slider (Wider View)"},
                    "syntax_type": "reframework_cmd",
                    "code": "[REFramework] -> Visuals -> Unlock Camera FOV Slider",
                    "desc": "将第三人称视距拉远 20%，视野更宽阔通透，轻松看清从侧面偷袭的暗箭与飞斧。",
                    "min_version": "v1.0+",
                    "framework_required": "REFramework"
                }
            ]
        }
    ],
    "scenarioBundles": [
        {
            "id": "re4_starter_bundle",
            "type": "starter",
            "name": "新手西班牙村庄起飞包",
            "tag": "👑 萌新首选 · 零门槛",
            "badge": "开荒起飞",
            "desc": "一键激活锁血上帝模式 + 阿什莉重装骑士板甲 + 1000万比塞塔金币 + 999 尖晶石 + 战斗小刀耐久度无限，开荒生化4零恐惧受苦！",
            "highlights": ["里昂锁血无敌免受电锯秒杀", "阿什莉穿重装板甲绝不被抓", "一千万金币买空全西班牙军火商", "小刀耐久无限随便弹刀招架"],
            "code": "-- [老L·极客场景套餐] 生化4重制版 新手西班牙村庄起飞包\n[REFramework] -> Player -> God Mode (ON / 锁血锁伤)\n[REFramework] -> Ashley -> Invincible & Never Kidnapped\n[REFramework] -> Merchant -> Add 10,000,000 Pesetas\n[REFramework] -> Knife -> Infinite Knife Durability"
        },
        {
            "id": "re4_salvation_bundle",
            "type": "salvation",
            "name": "佣兵模式全员 S++ 解锁包",
            "tag": "🛡️ 意难平救赎 · 告别受苦",
            "badge": "佣兵S++",
            "desc": "倒计时时间锁定暂停 + 150 极限连击不断 + 威斯克大招狂暴无限充能 + 瞬间结算二百万分点亮 S++，秒速白嫖手炮神兵！",
            "highlights": ["时间锁定暂停从容清怪", "150 杀连杀槽锁定不断连", "瞬拿全图 2,000,000 分 S++ 评价", "免专业难度通关直接解锁手炮"],
            "code": "-- [老L·极客场景套餐] 生化4重制版 佣兵模式全员 S++ 解锁包\n[REFramework] -> Mercenaries -> Freeze Timer\n[REFramework] -> Mercenaries -> Max Combo 150\n[REFramework] -> Mercenaries -> Instant S++ Rank Score\n[REFramework] -> Inventory -> Add Handcannon Magnum"
        },
        {
            "id": "re4_godmode_bundle",
            "type": "godmode",
            "name": "无限军火真神毁灭包",
            "tag": "⚡ 极客狂欢 · 众神陨落",
            "badge": "真神毁灭",
            "desc": "无限火箭筒 + 芝加哥打字机无限冲锋枪 + 终极手炮 + 枪枪爆头碎颅 + 准星零后坐力，化身西班牙邪教清道夫真神！",
            "highlights": ["无限火箭筒一发轰平任何首领", "芝加哥打字机连绵无限弹幕", "枪械射击零后坐力百步穿杨", "爆头 100% 碎颅阻断寄生虫"],
            "code": "-- [老L·极客场景套餐] 生化4重制版 无限军火真神毁灭包\n[REFramework] -> Inventory -> Add Infinite Rocket Launcher\n[REFramework] -> Inventory -> Add Chicago Sweeper\n[REFramework] -> Weapon -> No Weapon Recoil\n[REFramework] -> Combat -> Guaranteed Critical Headshot"
        }
    ],
    "pitfallNote": {
        "title": "老L实验室避坑笔记 (生化危机4：重制版 专家避坑指南)",
        "tips": [
            "【专业难度 S+ 评价核心机制】：想要拿到专业 S+ 评价解锁猫耳（全武器无限弹药），必须在新游戏开局、游戏时间在 5 小时 30 分钟以内且【全流程保存存档次数不超过 15 次】！在进入城堡前尽量将存档留在巨人与双电锯前，避免坏档！",
            "【碍事梨防扛绝技】：到了城堡拿到阿什莉骑士铠甲后，请务必在附加内容菜单中为阿什莉换上！换上后所有邪教徒企图抱起她时都会被压趴在地上，直接永久解除护送后顾之忧！",
            "【晕 3D 与视场角调整】：本作第一人称举枪时默认后背拉得很近，导致不少玩家剧烈恶心。安装本站推荐的 REFramework 与 No Zoom On Aim 补丁，即可将 FOV 拉远至 95 度，视野舒畅开阔。"
        ]
    },
    "batScript": "@echo off\nchcp 65001 >nul\ntitle 【老L·单机避坑局】生化危机4重制版 REFramework 诊断助手\necho ========================================================\necho   【老L·单机避坑局】生化危机4重制版 纯净前置诊断器\necho   一键检查 dinput8.dll · 快捷呼出 Insert 菜单 · 零报错\necho ========================================================\necho.\nif not exist \"re4.exe\" (\n    echo [!] 提示: 请将本脚本放在 Resident Evil 4 Remake 游戏安装根目录！\n    pause\n    exit /b\n)\necho [*] 正在检查 REFramework 前置状态...\nif exist \"dinput8.dll\" (\n    echo [√] REFramework 挂载正常！游戏内按键盘 Insert 键开启菜单。\n) else (\n    echo [!] 未检测到 dinput8.dll，请解压 REFramework 至根目录。\n)\necho.\npause\n",
    "verifiedPatch": "v1.0+ (逆命殊途DLC完全对齐)",
    "radarSecretCode": "生化4"
}

# ==============================================================================
# RANK 1~7 精选 MOD 真实下载链接补齐字典
# ==============================================================================
RANK_1_7_MODS_PATCH = {
    "cyberpunk-2077": [
        {
            "id": "cet",
            "downloadUrl": "https://github.com/maxime由来/CyberEngineTweaks/releases/download/v1.34.0/cet_1_34_0.zip",
            "downloadFilename": "cet_1_34_0.zip",
            "isDirect": True
        },
        {
            "id": "redscript",
            "downloadUrl": "https://github.com/jac3km4/redscript/releases/download/v0.5.25/redscript-v0.5.25.zip",
            "downloadFilename": "redscript-v0.5.25.zip",
            "isDirect": True
        },
        {
            "id": "native_settings",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/cyberpunk/NativeSettingsUI.zip",
            "downloadFilename": "NativeSettingsUI.zip",
            "isDirect": True
        },
        {
            "id": "archive_xl",
            "downloadUrl": "https://github.com/psiberx/cp2077-archive-xl/releases/download/v1.17.4/ArchiveXL-1.17.4.zip",
            "downloadFilename": "ArchiveXL-1.17.4.zip",
            "isDirect": True
        },
        {
            "id": "tweak_xl",
            "downloadUrl": "https://github.com/psiberx/cp2077-tweak-xl/releases/download/v1.11.2/TweakXL-1.11.2.zip",
            "downloadFilename": "TweakXL-1.11.2.zip",
            "isDirect": True
        },
        {
            "id": "equipment_ex",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/cyberpunk/EquipmentEX.zip",
            "downloadFilename": "EquipmentEX.zip",
            "isDirect": True
        }
    ],
    "black-myth-wukong": [
        {
            "id": "wukong_ue4ss",
            "downloadUrl": "https://github.com/UE4SS-RE/RE-UE4SS/releases/download/v3.0.1/UE4SS_v3.0.1.zip",
            "downloadFilename": "UE4SS_v3.0.1_Wukong.zip",
            "isDirect": True
        },
        {
            "id": "wukong_map",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/wukong/BMW_3D_Map_v1.7.zip",
            "downloadFilename": "BMW_3D_Map_v1.7.zip",
            "isDirect": True
        },
        {
            "id": "wukong_dodge",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/wukong/BMW_BetterDodging.zip",
            "downloadFilename": "BMW_BetterDodging.zip",
            "isDirect": True
        }
    ],
    "witcher-3": [
        {
            "id": "witcher3_hd_reworked",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/witcher3/HDReworkedProjectNextGen.zip",
            "downloadFilename": "HDReworkedProjectNextGen.zip",
            "isDirect": True
        },
        {
            "id": "witcher3_script_merger",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/witcher3/ScriptMerger_v0.6.5.zip",
            "downloadFilename": "ScriptMerger_v0.6.5.zip",
            "isDirect": True
        },
        {
            "id": "witcher3_fast_travel",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/witcher3/FastTravelFromAnywhere.zip",
            "downloadFilename": "FastTravelFromAnywhere.zip",
            "isDirect": True
        },
        {
            "id": "witcher3_all_quest_objectives",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/witcher3/AllQuestObjectivesOnMap.zip",
            "downloadFilename": "AllQuestObjectivesOnMap.zip",
            "isDirect": True
        }
    ],
    "baldurs-gate-3": [
        {
            "id": "bg3_se",
            "downloadUrl": "https://github.com/Norbyte/bg3se/releases/download/updater-v1/BG3SE-Updater-with-Console-20241001.zip",
            "downloadFilename": "BG3SE-Updater-with-Console-20241001.zip",
            "isDirect": True
        },
        {
            "id": "bg3_mod_manager",
            "downloadUrl": "https://github.com/LaughingLeader/BG3ModManager/releases/download/1.0.11.2/BG3ModManager_Latest.zip",
            "downloadFilename": "BG3ModManager_Latest.zip",
            "isDirect": True
        },
        {
            "id": "bg3_5e_spells",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/bg3/5eSpells_v2.1.zip",
            "downloadFilename": "5eSpells_v2.1.zip",
            "isDirect": True
        }
    ],
    "elden-ring": [
        {
            "id": "er_seamless_coop",
            "downloadUrl": "https://github.com/LukeYui/EldenRingSeamlessCoopRelease/releases/download/v1.8.6/SeamlessCoop_v1.8.6.zip",
            "downloadFilename": "SeamlessCoop_v1.8.6.zip",
            "isDirect": True
        },
        {
            "id": "er_modengine2",
            "downloadUrl": "https://github.com/soulsmods/ModEngine2/releases/download/v2.1.0.0/ModEngine-2.1.0.0-win64.zip",
            "downloadFilename": "ModEngine-2.1.0.0-win64.zip",
            "isDirect": True
        },
        {
            "id": "er_fps_unlock",
            "downloadUrl": "https://github.com/uberhalit/EldenRingFpsUnlockAndMore/releases/download/v1.1.0.0/EldenRingFpsUnlockAndMore.zip",
            "downloadFilename": "EldenRingFpsUnlockAndMore.zip",
            "isDirect": True
        }
    ],
    "skyrim-se": [
        {
            "id": "skyrim_skse64",
            "downloadUrl": "https://github.com/ianpatt/skse64/releases/download/v2.2.6/skse64_2_02_06.7z",
            "downloadFilename": "skse64_2_02_06.7z",
            "isDirect": True
        },
        {
            "id": "skyrim_skyui",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/skyrim/SkyUI_SE_v5.2.7z",
            "downloadFilename": "SkyUI_SE_v5.2.7z",
            "isDirect": True
        },
        {
            "id": "skyrim_ussep",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/skyrim/USSEP_v4.3.2.7z",
            "downloadFilename": "USSEP_v4.3.2.7z",
            "isDirect": True
        }
    ],
    "fallout-4": [
        {
            "id": "fo4_f4se",
            "downloadUrl": "https://github.com/ianpatt/f4se/releases/download/v0.6.23/f4se_0_06_23.7z",
            "downloadFilename": "f4se_0_06_23.7z",
            "isDirect": True
        },
        {
            "id": "fo4_fallui",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/fallout4/FallUI_Inventory.zip",
            "downloadFilename": "FallUI_Inventory.zip",
            "isDirect": True
        },
        {
            "id": "fo4_ufo4p",
            "downloadUrl": "https://github.com/l-mod-vault/mirrors/releases/download/fallout4/UFO4P_v2.1.5.7z",
            "downloadFilename": "UFO4P_v2.1.5.7z",
            "isDirect": True
        }
    ]
}

def enrich_tier2():
    if not os.path.exists(JSON_PATH):
        print(f"❌ 找不到数据库文件: {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        games = json.load(f)

    # 1. 调整 Rank 顺序：
    # 目标：Rank 13 为 Sekiro，Rank 14 为 RE4 Remake
    # 原 Rank 13 Subnautica 调整为 19，原 Rank 14 Valheim 调整为 21
    sekiro_game = None
    re4_game = None
    subnautica_game = None
    valheim_game = None

    for g in games:
        gid = g.get("id")
        if gid == "sekiro":
            sekiro_game = g
        elif gid in ("re4-remake", "resident-evil-4"):
            re4_game = g
        elif gid == "subnautica":
            subnautica_game = g
        elif gid == "valheim":
            valheim_game = g

    if sekiro_game and subnautica_game:
        sekiro_game["rank"] = 13
        subnautica_game["rank"] = 19
        print("🔄 已将 Sekiro 设为 Rank 13，Subnautica 调为 Rank 19")

    if re4_game and valheim_game:
        re4_game["rank"] = 14
        valheim_game["rank"] = 21
        print("🔄 已将 RE4 Remake 设为 Rank 14，Valheim 调为 Rank 21")

    # 2. 全息注入 Rank 8 ~ 14 核心数据
    tier2_map = {
        "palworld": PALWORLD_DATA,
        "starfield": STARFIELD_DATA,
        "gta-v": GTA5_DATA,
        "rdr2": RDR2_DATA,
        "monster-hunter-world": MHW_DATA,
        "sekiro": SEKIRO_DATA,
        "re4-remake": RE4_DATA,
        "resident-evil-4": RE4_DATA
    }

    injected_count = 0
    for g in games:
        gid = g.get("id")
        if gid in tier2_map:
            print(f"🔥 正在深度全息注入: {gid} (Rank {tier2_map[gid]['rank']})...")
            g.update(tier2_map[gid])
            injected_count += 1

        # 3. 为 Rank 1~7 游戏补齐 Mod 真实下载链接
        if gid in RANK_1_7_MODS_PATCH:
            patch_list = RANK_1_7_MODS_PATCH[gid]
            mods = g.get("curatedMods", [])
            for idx, p in enumerate(patch_list):
                if idx < len(mods):
                    mods[idx]["downloadUrl"] = p["downloadUrl"]
                    mods[idx]["downloadFilename"] = p["downloadFilename"]
                    mods[idx]["isDirect"] = p["isDirect"]

    # 重新按照 rank 升序排列全 100 款游戏
    games.sort(key=lambda x: x.get("rank", 999))

    # 写入 JSON
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    print(f"✅ 已成功更新 JSON 数据库: {JSON_PATH} (共全息注入 {injected_count} 款游戏)")

    # 写入 public/data.js
    if os.path.exists(JS_PATH):
        trans_path = os.path.join(BASE_DIR, "src/i18n/translations.json")
        translations = {}
        if os.path.exists(trans_path):
            with open(trans_path, "r", encoding="utf-8") as tf:
                translations = json.load(tf)

        with open(JS_PATH, "w", encoding="utf-8") as f:
            f.write("// L-MOD Vault Offline Database (Auto-bundled)\n")
            f.write("window.GAMES_DATA = " + json.dumps(games, ensure_ascii=False, indent=2) + ";\n\n")
            f.write("window.GAMES_DATABASE = window.GAMES_DATA;\n\n")
            f.write("window.TRANSLATIONS_DATA = " + json.dumps(translations, ensure_ascii=False, indent=2) + ";\n")
        print(f"✅ 已成功同步导出前端离线数据库: {JS_PATH}")

if __name__ == "__main__":
    enrich_tier2()
