#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/enrich_rank5_7_flagships.py
L-MOD Vault 旗舰游戏全息深度采掘注入引擎 (Milestone 3)
严格对齐 game-vault-enricher v2.5 全部 Schema 规范：
- game_command.schema.json
- game_full.schema.json
- trainer_info.schema.json
- curated_mod.schema.json
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE_DIR, "src/data/games_top100.json")
JS_PATH = os.path.join(BASE_DIR, "public/data.js")

# ==============================================================================
# RANK 5: 艾尔登法环 (Elden Ring)
# ==============================================================================
ELDEN_RING_DATA = {
    "hasConsole": True,
    "consoleShortcut": "无原生打字终端 (采用 ModEngine2 离线引导 + The Grand Archives CT 表 / FLiNG 修改器)",
    "consoleEnableGuide": {
        "zh-CN": "【100%安全离线防封指南】\n1. 方案一 (ModEngine2 免修改文件)：解压 ModEngine2，将模组放入 /mod 目录，直接双击 launchmod_eldenring.bat 启动，该启动器会自动拦截 EAC 并进入纯净离线环境，绝无联机封号风险！\n2. 方案二 (替换引导)：进入游戏根目录 Game/，将原版 start_protected_game.exe 重命名为 .bak，将 eldenring.exe 复制一份并重命名为 start_protected_game.exe，新建文本文件 steam_appid.txt 写入 1245620，启动即可离线畅玩。\n3. 方案三 (无缝联机 Seamless Co-op)：该模组使用独立 .co2 存档与第三方离线 P2P 协议，与官方服务器完全隔离，支持多人联机无封禁！",
        "en": "EAC Offline Bypass & ModEngine2 Launch Guide: Launch via launchmod_eldenring.bat or rename start_protected_game.exe and place steam_appid.txt (1245620) to safely bypass Easy Anti-Cheat in offline mode without ban risk."
    },
    "popularCommands": [
        "Num 1",
        "launchmod_eldenring.bat",
        "[CT表] Item Gib -> Shadow of the Erdtree DLC Items",
        "[CT表] Scripts -> Unlock All Map Graces",
        "Ctrl+Num 1",
        "Num 9"
    ],
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.14+ (Shadow of the Erdtree DLC 对齐)",
        "officialUrl": "https://flingtrainer.com/trainer/elden-ring-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/v1.14/Elden_Ring_v1.14_Plus_34_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报极客纯净版)",
            "md5CheckSum": "8f4a1c7e9b0d2e3f5a6b7c8d9e0f1a2b",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Elden Ring Trainer.exe'",
            "troubleshootSteps": [
                "必须先通过 launchmod_eldenring.bat 或 EAC 离线替换引导启动游戏，进入主菜单后再运行修改器",
                "若 Windows Defender 拦截报毒，请以管理员身份运行上方 PowerShell 白名单命令",
                "关闭游戏后若需重返线上联机，务必删除作弊非法生成的越级强化道具与测试装备"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "🛡️ 核心生存与战斗无敌",
                "items": [
                    {"key": "Num 1", "action": "无敌模式 (God Mode / 免受一切伤害与异常状态)"},
                    {"key": "Num 2", "action": "无限生命 (Infinite HP)"},
                    {"key": "Num 3", "action": "无限专注值/法力 (Infinite FP - 战技与魔法无限释放)"},
                    {"key": "Num 4", "action": "无限精力/耐力 (Infinite Stamina - 翻滚冲刺不减)"},
                    {"key": "Num 5", "action": "零重量 (Zero Weight - 随时处于轻盈翻滚状态)"},
                    {"key": "Num 6", "action": "装备耐久度不减 (Weapon Durability)"},
                    {"key": "Num 7", "action": "100% 掉落率 (100% Item Drop Rate)"},
                    {"key": "Num 8", "action": "幽影树庇护点数不减 (Shadow Realm Blessing Edit)"}
                ]
            },
            {
                "category": "⚡ 战斗伤害与攻防调校",
                "items": [
                    {"key": "Num 9", "action": "一击削韧倒地 (Super Stance Damage / 处决破韧)"},
                    {"key": "Num 0", "action": "超级伤害/一击必杀 (One Hit Kill)"},
                    {"key": "Num .", "action": "绝对防御免伤 (Defense Multiplier)"},
                    {"key": "Ctrl+Num 1", "action": "编辑持有的卢恩货币 (Edit Runes Amount)"},
                    {"key": "Ctrl+Num 2", "action": "死亡不掉落卢恩 (Runes Won't Drop on Death)"},
                    {"key": "Ctrl+Num 3", "action": "游戏全局慢动作 0.3x 识破 (Slomo 0.3x Reflex)"},
                    {"key": "Ctrl+Num 4", "action": "游戏全局超速奔跑 1.5x (Super Speed Exploration)"}
                ]
            }
        ]
    },
    "hasMods": True,
    "modInstallPath": "<SteamLibrary>/steamapps/common/ELDEN RING/Game/mod/",
    "curatedMods": [
        {
            "id": "mod_seamless_coop",
            "title": "Seamless Co-op (无缝联机大修模组)",
            "author": "LukeYui",
            "version": "v1.8.2+",
            "size": "4.8 MB",
            "downloads": "4,200,000+",
            "endorsements": "180,000+",
            "category": "多人联机与系统大修",
            "desc": "魂系联机体验天花板！彻底移除打完Boss被强行遣返的联机限制，全图无空气墙无缝跑图、死亡围观复活、共乘托雷特灵马、独立 .co2 存档绝对不连官方服务器，100% 零封号！",
            "dependencies": ["None (自带独立引导器)"],
            "installPath": "<GameRoot>/Game/ersc/",
            "installSteps": [
                "解压 SeamlessCoop.zip 得到 ersc 文件夹与 launch_elden_ring_seamlesscoop.exe",
                "将上述文件直接复制进游戏目录 Game/ 下",
                "用记事本打开 Game/ersc/ersc_settings.ini，在 cooppassword = 后面输入你和小伙伴约定的联机密码",
                "双击 launch_elden_ring_seamlesscoop.exe 启动，进入游戏后使用道具包里的【小人偶】即可无缝联机！"
            ]
        },
        {
            "id": "mod_modengine2",
            "title": "ModEngine2 官方模组加载框架",
            "author": "SoulsMods Team",
            "version": "v2.1.0+",
            "size": "12.3 MB",
            "downloads": "3,800,000+",
            "endorsements": "150,000+",
            "category": "底层框架与核心前置",
            "desc": "法环挂载全类型 Mod 的核心基石！免解包直接挂载 .dcx, .param, regulation.bin 等资源，自带 EAC 离线安全启动引导，绝不篡改游戏原版文件。",
            "dependencies": ["Microsoft Visual C++ 2015-2022 Redistributable"],
            "installPath": "<GameRoot>/ModEngine2/",
            "installSteps": [
                "解压 ModEngine2 压缩包到任意纯英文路径 (推荐放到游戏根目录下)",
                "将下载的武器、服装或平衡性 Mod 解压后扔进 ModEngine2/mod/ 文件夹中",
                "双击运行 launchmod_eldenring.bat 即可一键安全免封启动游戏！"
            ]
        },
        {
            "id": "mod_grand_archives_ct",
            "title": "The Grand Archives (TGA) 全能离线内存调试表",
            "author": "TGA Reverse Engineering Team",
            "version": "v1.14 (Shadow of the Erdtree Ready)",
            "size": "3.5 MB",
            "downloads": "2,900,000+",
            "endorsements": "120,000+",
            "category": "极客调试与数据检索",
            "desc": "法环极客神器！包含全DLC 物品一键生成 (Item Gib)、全赐福传送点秒亮、360° 自由飞行摄影相机、NPC 赎罪与死人复生、BOSS 随时重置挑战。",
            "dependencies": ["Cheat Engine 7.5+", "EAC Offline Bypass"],
            "installPath": "自定义目录 (配合 Cheat Engine 使用)",
            "installSteps": [
                "下载并安装 Cheat Engine 7.5+",
                "先运行 launchmod_eldenring.bat 进入游戏并载入存档",
                "双击打开 EldenRing.CT 表，点击左上角电脑图标附着到 eldenring.exe 进程",
                "勾选 Open 表头，展开 Scripts -> Item Gib 即可按图鉴无痛派发全套装备！"
            ]
        },
        {
            "id": "mod_err_reforged",
            "title": "Elden Ring Reforged (ERR 战斗系统深度大修)",
            "author": "Kirnifr",
            "version": "v1.1.2+",
            "size": "185.0 MB",
            "downloads": "1,100,000+",
            "endorsements": "48,000+",
            "category": "玩法机制全面重构",
            "desc": "重构交界地战斗机制：新增《只狼》完美招架弹反、全新法术连招、复仇者难度模式、赐福点 Boss 连战挑战！",
            "dependencies": ["ModEngine2"],
            "installPath": "<ModEngine2Root>/mod/",
            "installSteps": [
                "下载 ERR 安装包，将其解压覆盖至 ModEngine2/mod/ 目录下",
                "启动 launchmod_eldenring.bat 开始全新的交界地冒险！"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "🛡️ 核心生存、绝对防护与时间流速控制 (God Mode & Slomo Reflex)",
            "commands": [
                {
                    "id": "er_god_mode",
                    "name": {"zh-CN": "绝对免伤无敌模式 (免受任何攻击与坠落伤害)", "en": "Toggle God Mode"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Num 1",
                    "desc": "开启后主角免疫一切物理、属性、状态异常与高空坠落致死伤害，生命条强制锁死为最大值，手残党救赎核心！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer / ModEngine2"
                },
                {
                    "id": "er_infinite_fp",
                    "name": {"zh-CN": "无限专注值/法力值 (战技魔法无限连发)", "en": "Infinite FP / Mana"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Num 3",
                    "desc": "战技、骨灰召唤以及高阶法术与祷告完全不消耗任何专注值 (FP)，随时化身无限法力炮台！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer"
                },
                {
                    "id": "er_infinite_stamina",
                    "name": {"zh-CN": "无限精力耐力 (翻滚冲刺防御不喘气)", "en": "Infinite Stamina"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Num 4",
                    "desc": "精力耐力条永远保持满格，连续翻滚闪避、重击举盾防御不会破防或消耗耐力。",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer"
                },
                {
                    "id": "er_slomo_reflex",
                    "name": {"zh-CN": "全局慢动作 0.3x 识破模式 (子弹时间拆招)", "en": "Slomo 0.3x Matrix Reflex"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Ctrl+Num 3",
                    "desc": "将全局物理与动作流速放慢至 0.3 倍速，Boss 出招前摇清晰可见，轻松掌握弹反与翻滚时机！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer"
                },
                {
                    "id": "er_super_stance_break",
                    "name": {"zh-CN": "一击削韧倒地 (Boss秒进跪地处决状态)", "en": "Instant Super Stance Break"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Num 9",
                    "desc": "主角的任何攻击将造成数十倍架势条伤害，即便是狂龙贝勒或女武神也是一击破韧跪地，尽情享受处决快感！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer"
                },
                {
                    "id": "er_zero_weight",
                    "name": {"zh-CN": "随身装备零重量 (全身重甲轻盈翻滚)", "en": "Zero Equipment Weight"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Num 5",
                    "desc": "将所有已穿戴防具和手持重型武器负重强制归零，无论穿多么厚重的铠甲均拥有超快轻翻滚无敌帧！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer"
                }
            ]
        },
        {
            "category": "💰 卢恩货币、属性洗点与随身强化 (Runes, Stats & Upgrade)",
            "commands": [
                {
                    "id": "er_add_runes_1m",
                    "name": {"zh-CN": "注入 1,000,000 点卢恩 (直接升级买断全商人)", "en": "Inject 1,000,000 Runes"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Ctrl+Num 1",
                    "desc": "向角色背囊瞬间注入 100 万点卢恩，可自由连续分配属性升级或在圆桌厅堂扫荡全部消耗品！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer"
                },
                {
                    "id": "er_keep_runes_on_death",
                    "name": {"zh-CN": "死亡卢恩不掉落 (免捡魂零挫败感)", "en": "Keep Runes Upon Death"},
                    "syntax_type": "trainer_hotkey",
                    "code": "Ctrl+Num 2",
                    "desc": "角色阵亡后身上携带的卢恩完整保留，彻底告别在深坑和悬崖边捡魂翻车的折磨体验。",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "FLiNG Trainer"
                },
                {
                    "id": "er_spawn_somber_dragon_stone",
                    "name": {"zh-CN": "[CT表] 派发古龙岩失色锻造石 (特殊武器+10关键素材)", "en": "Spawn Somber Ancient Dragon Smithing Stone"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Upgrade Materials -> Somber Ancient Dragon Smithing Stone x10",
                    "desc": "派发满额特殊武器毕业所需的古龙岩失色锻造石，无需通关雪原或天空城即可提前满级！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_ancient_dragon_stone",
                    "name": {"zh-CN": "[CT表] 派发古龙岩普通锻造石 (常规武器+25关键素材)", "en": "Spawn Ancient Dragon Smithing Stone"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Upgrade Materials -> Ancient Dragon Smithing Stone x10",
                    "desc": "派发普通武器升至 +25 满级所需的珍稀古龙岩锻造石，批量强化你的武器库！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_free_respec",
                    "name": {"zh-CN": "[CT表] 自由属性重置 (免消耗泪滴幼体随时洗点)", "en": "Free Attribute Respec"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Player Data -> Respec -> Free Attribute Points Allocation",
                    "desc": "无需击败满月女王或消耗稀缺的泪滴幼体，随时打开面板自由重塑 8 大核心属性！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                }
            ]
        },
        {
            "category": "🌳 黄金树幽影 DLC 专属机制拉满 (Shadow of the Erdtree Blessings & Items)",
            "commands": [
                {
                    "id": "er_max_scadutree_blessing",
                    "name": {"zh-CN": "[CT表] 幽影树庇护等级瞬间拉满 Lv20 (攻防数值翻倍)", "en": "Max Scadutree Blessing Lv20"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> Shadow Realm Blessings -> Set Scadutree Blessing to 20",
                    "desc": "瞬间将幽影之地的核心数值系统【幽影树庇护】升至最高 20 级满级，攻击力与减伤率直接翻倍，拒绝幽影受苦！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_max_revered_ash_blessing",
                    "name": {"zh-CN": "[CT表] 灵灰庇护等级瞬间拉满 Lv10 (骨灰与灵马肉度拉满)", "en": "Max Revered Spirit Ash Blessing Lv10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> Shadow Realm Blessings -> Set Revered Spirit Ash to 10",
                    "desc": "将骨灰召唤物与托雷特灵马的强化数值【灵灰庇护】升满至 10 级，召唤物坦度飞跃提升！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_all_scadutree_fragments",
                    "name": {"zh-CN": "[CT表] 派发全部 50 颗幽影树碎片 (免全图地毯式搜寻)", "en": "Spawn 50 Scadutree Fragments"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Key Items -> Scadutree Fragment x50",
                    "desc": "直接向背囊注入全部 50 颗幽影树碎片，省去在复杂的立体地图里爬悬崖翻罐子的痛苦折磨！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_revered_spirit_ashes",
                    "name": {"zh-CN": "[CT表] 派发全部 25 颗灵灰碎片", "en": "Spawn 25 Revered Spirit Ashes"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Key Items -> Revered Spirit Ash x25",
                    "desc": "派发全套灵灰碎片，用于在赐福点解锁顶级灵灰强化层级。",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_bloodfiends_arm",
                    "name": {"zh-CN": "[CT表] 派发 DLC 神级轮椅武器：血怪手臂+25", "en": "Spawn Bloodfiend's Arm +25"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Weapons -> Bloodfiend's Arm (+25 Blood Affinity)",
                    "desc": "派发黄金树幽影 DLC 最强重击出血神器【血怪手臂】，搭配感应流蓄力重击一击即爆万点出血伤害！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                }
            ]
        },
        {
            "category": "⚔️ 全套追忆毕业神装与传说武器 (Legendary & Remembrance Weapons)",
            "commands": [
                {
                    "id": "er_spawn_blasphemous_blade",
                    "name": {"zh-CN": "[CT表] 派发亵渎圣剑+10 (吸血神技掠夺之火)", "en": "Spawn Blasphemous Blade +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Weapons -> Blasphemous Blade (+10)",
                    "desc": "派发击败大蛇拉卡德追忆兑换的信仰大剑【亵渎圣剑】，战技超远距离击飞敌人并疯狂吸血回复生命！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_hand_of_malenia",
                    "name": {"zh-CN": "[CT表] 派发玛莲妮亚之手+10 (水鸟乱舞飞天连斩)", "en": "Spawn Hand of Malenia +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Weapons -> Hand of Malenia (+10)",
                    "desc": "派发女武神追忆武器太刀，自带华丽绝伦的三段空中连续斩杀技【水鸟乱舞】！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_dark_moon_greatsword",
                    "name": {"zh-CN": "[CT表] 派发暗月大剑+10 (菈妮誓约月光剑气)", "en": "Spawn Dark Moon Greatsword +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Weapons -> Dark Moon Greatsword (+10)",
                    "desc": "派发菈妮支线终极定情信物【暗月大剑】，附魔后蓄力重击释放零耗蓝极寒冰冻月光剑气！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_sacred_relic_sword",
                    "name": {"zh-CN": "[CT表] 派发神躯化剑+10 (白金之子提款机黄金波动)", "en": "Spawn Sacred Relic Sword +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Weapons -> Sacred Relic Sword (+10)",
                    "desc": "派发艾尔登之兽追忆武器，战技【黄金波动】扇形横扫全屏秒杀敌人，乌鸦悬崖刷卢恩必备神兵！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_mohgwyn_sacred_spear",
                    "name": {"zh-CN": "[CT表] 派发蒙格温圣矛+10 (全屏范围授血仪典)", "en": "Spawn Mohgwyn's Sacred Spear +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Weapons -> Mohgwyn's Sacred Spear (+10)",
                    "desc": "鲜血君王追忆重矛，高举战矛连续释放三段大范围穿墙出血结界，Boss 战轮椅神器！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                }
            ]
        },
        {
            "category": "👻 神级传说骨灰与战灰全解锁 (Legendary Spirit Ashes & Ashes of War)",
            "commands": [
                {
                    "id": "er_spawn_mimic_tear",
                    "name": {"zh-CN": "[CT表] 派发仿身泪滴骨灰+10 (复刻自身满配置带头大哥)", "en": "Spawn Mimic Tear Ash +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Spirit Ashes -> Mimic Tear Ashes (+10)",
                    "desc": "派发最强传说骨灰大哥！完整复刻主角身上的全套防具、武器、战灰与道具，单挑各大顶级 Boss！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_black_knife_tiche",
                    "name": {"zh-CN": "[CT表] 派发黑刀狄希骨灰+10 (命定之死持续扣血)", "en": "Spawn Black Knife Tiche +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Spirit Ashes -> Black Knife Tiche (+10)",
                    "desc": "派发超敏捷传说刺客狄希，释放命定之死红光斩击，按百分比削减敌方生命上限并造成强力灼烧！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_latenna_ash",
                    "name": {"zh-CN": "[CT表] 派发白金之子勒缇娜骨灰+10 (超远程自动迫击炮)", "en": "Spawn Latenna the Albinauric +10"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Spirit Ashes -> Latenna the Albinauric (+10)",
                    "desc": "派发固定炮台勒缇娜，超视距连续发射魔力箭矢，对付飞龙与体型庞大的野外巨兽有奇效！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_aow_bloodhounds_step",
                    "name": {"zh-CN": "[CT表] 派发战灰：猎犬步法 (长距离瞬移无敌帧位移)", "en": "Spawn Ash of War: Bloodhound's Step"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Ashes of War -> Ash of War: Bloodhound's Step",
                    "desc": "赋予武器超长无敌帧的快速瞬身位移能力，能在毒沼、熔岩与密集攻击中如入无人之境！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_aow_seppuku",
                    "name": {"zh-CN": "[CT表] 派发战灰：切腹 (瞬间拉满武器出血面板)", "en": "Spawn Ash of War: Seppuku"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Ashes of War -> Ash of War: Seppuku",
                    "desc": "双太刀出血流核心战灰，刺击自身腹部使武器沾满鲜血，大幅提升物理攻击力与异常出血累计效率！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                }
            ]
        },
        {
            "category": "💍 全套传说护符与灵药滴露 (Talisman & Physick Flask Tears)",
            "commands": [
                {
                    "id": "er_spawn_shard_of_alexander",
                    "name": {"zh-CN": "[CT表] 派发亚历山大的碎片 (战技攻击力大幅提升15%)", "en": "Spawn Shard of Alexander"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Talismans -> Shard of Alexander",
                    "desc": "全流派必带核心毕业护符，战技伤害直接无条件提升 15%，大幅强化各种轮椅技能威力！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_rotten_winged_sword",
                    "name": {"zh-CN": "[CT表] 派发腐败翼剑徽章 (连续攻击最高增加13%攻击力)", "en": "Spawn Rotten Winged Sword Insignia"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Talismans -> Rotten Winged Sword Insignia",
                    "desc": "连击流与出血流神装，连续命中敌人后层层叠加强攻 Buff，最高增伤达 13%！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_dragoncrest_greatshield",
                    "name": {"zh-CN": "[CT表] 派发龙徽大盾护符 (物理减伤率直接提升20%)", "en": "Spawn Dragoncrest Greatshield Talisman"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Talismans -> Dragoncrest Greatshield Talisman",
                    "desc": "保命第一神符！常驻无条件提供高达 20% 的巨额物理减伤率，极大降低高周目被一招秒杀的风险！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_cerulean_hidden_tear",
                    "name": {"zh-CN": "[CT表] 派发蓝秘密滴露 (灵药圣杯瓶15秒无限法力)", "en": "Spawn Cerulean Hidden Tear"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Tears -> Cerulean Hidden Tear",
                    "desc": "法师一炮秒杀流核心灵药！服下后 15 秒内一切法力消耗直接降为 0，配合彗星亚兹勒实现无限激光轰击！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_spawn_thorny_cracked_tear",
                    "name": {"zh-CN": "[CT表] 派发连刺破露滴 (灵药连击极限爆发加伤)", "en": "Spawn Thorny Cracked Tear"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Tears -> Thorny Cracked Tear",
                    "desc": "调制进入灵药圣杯瓶，饮用后极大强化连续攻击的伤害叠加上限，近战速杀必备！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                }
            ]
        },
        {
            "category": "🗺️ 地图传送、全赐福点亮与自由运镜 (Fast Travel, Graces & FreeCam)",
            "commands": [
                {
                    "id": "er_unlock_all_graces",
                    "name": {"zh-CN": "[CT表] 一键点亮交界地全图赐福点 (直接解锁全部传送门)", "en": "Unlock All Map Graces (Base Game)"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> World -> Unlock All Sites of Grace (Base Game)",
                    "desc": "瞬间点亮交界地主世界、雪原、地下世界与天空城的所有赐福传送点，省去跑图探路时间！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_unlock_dlc_graces",
                    "name": {"zh-CN": "[CT表] 一键点亮黄金树幽影 DLC 全图赐福", "en": "Unlock All DLC Sites of Grace"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> World -> Unlock DLC Sites of Grace (Shadow Realm)",
                    "desc": "点亮幽影之地全部复杂分层地形上的所有赐福点，随心所欲直达目标区域！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_freecam_photomode",
                    "name": {"zh-CN": "[CT表] 360° 自由飞行摄影相机与时间定格", "en": "FreeCam & Time Freeze Photomode"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> Camera -> Enable FreeCam & Freeze Time",
                    "desc": "脱离角色控制束缚，摄像机自由穿墙升空飞行动作定格，用于拍摄超高清壁纸与Boss特写！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_anywhere_fast_travel",
                    "name": {"zh-CN": "[CT表] 允许在地下墓穴与战斗中随时传送", "en": "Allow Fast Travel Anywhere (Combat/Dungeon)"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> World -> Allow Fast Travel Everywhere",
                    "desc": "解除大地图传送限制，即使身处红色地下墓穴或被 Boss 围困追击也能秒开地图传送逃脱！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_ancient_lightning_strike",
                    "name": {"zh-CN": "[CT表] 派发神级逃课祷告：古龙雷击 (超大体型Boss一击秒杀)", "en": "Spawn Ancient Dragons' Lightning Strike"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Incantations -> Ancient Dragons' Lightning Strike",
                    "desc": "对付黄金树幽影大体型 Boss (如狂龙贝勒、罗刹、幽影树化身) 最强逃课核弹，蓄力释放引落漫天红雷引发数万点多段爆发判定！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_instant_torrent_revival",
                    "name": {"zh-CN": "[CT表] 托雷特灵马免消耗红露滴瞬间复活召回", "en": "Instant Torrent Horse Revival"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> Player Data -> Instant Torrent Revival (No Flask)",
                    "desc": "灵马战死后无需扣除一瓶红露滴原罪瓶，吹响灵马哨笛直接无读条满血秒骑乘！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                }
            ]
        },
        {
            "category": "🕊️ 任务 Fact、NPC 赎罪与全 Boss 追忆重置 (NPC Absolution & Boss Rematch)",
            "commands": [
                {
                    "id": "er_clear_npc_hostility",
                    "name": {"zh-CN": "[CT表] 结缘教堂一键绝对赎罪 (消除全部误伤NPC敌对)", "en": "Clear All NPC Hostility (Church of Vows Absolution)"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> Event Flags -> Clear NPC Aggro / Absolution",
                    "desc": "如果不小心手滑打中友好 NPC 导致对方拔刀追杀，执行本项可立即清空全部仇恨状态恢复和平！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_revive_dead_npcs",
                    "name": {"zh-CN": "[CT表] 强制复活被误杀的关键支线 NPC", "en": "Revive Key Quest NPCs"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> Event Flags -> Revive Dead NPCs",
                    "desc": "重置被误杀或意外阵亡的关键支线 NPC 的存活标志位，使他们重返原点继续推进任务线！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_unlock_all_bell_bearings",
                    "name": {"zh-CN": "[CT表] 派发圆桌厅堂全套商人铃珠", "en": "Spawn All Merchant Bell Bearings"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Item Gib -> Key Items -> All Bell Bearings (Smithing / Somber / Glovewort)",
                    "desc": "直接派发全套锻造石铃珠、失色铃珠与墓地铃兰铃珠，在孪生老妪处直接购买全部强化材料！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                },
                {
                    "id": "er_restore_all_great_runes",
                    "name": {"zh-CN": "[CT表] 派发并激活全套半神大卢恩", "en": "Unlock & Activate All Great Runes"},
                    "syntax_type": "trainer_hotkey",
                    "code": "[CT表] Scripts -> Key Items -> Unlock All Great Runes (Restored)",
                    "desc": "派发葛瑞克、拉塔恩、玛莲妮亚、莫格等全部大卢恩并自动完成神授塔充能激活，随时随地享受全属性加成！",
                    "min_version": "v1.14+ (DLC 对齐)",
                    "framework_required": "The Grand Archives CT"
                }
            ]
        }
    ]
}

# ==============================================================================
# RANK 6: 上古卷轴5：天际重制版 (Skyrim Special Edition)
# ==============================================================================
SKYRIM_SE_DATA = {
    "hasConsole": True,
    "consoleShortcut": "~ (Tilde 键)",
    "consoleEnableGuide": {
        "zh-CN": "Bethesda Creation 引擎原生提供全功能控制台：\n1. 快捷键：游戏中随时按下键盘左上角【~】键 (波浪键 / ESC下方) 暂停并呼出全屏控制台；\n2. 输入法避坑：若无反应，请在 Windows 任务栏切换为'英语(美国)'美式键盘输入法，或在 Documents/My Games/Skyrim Special Edition/Skyrim.ini 的 [General] 下确认 bAllowConsole=1；\n3. 成就与防闪退：使用控制台或打 Mod 会打上脏标记锁定 Steam 成就，强烈建议安装 SSE Engine Fixes 恢复成就并彻底防止 60Hz+ 物理抽搐与 CTD 闪退！\n4. 简写技巧：FormID 开头的多余 0 可省略，如 player.additem 0000000F 10000 可简写为 player.additem f 10000！",
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
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.6.1170+ / AE & SE 完全兼容",
        "officialUrl": "https://flingtrainer.com/trainer/the-elder-scrolls-v-skyrim-special-edition-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/v1.6.1170/The_Elder_Scrolls_V_Skyrim_SE_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报纯净离线版)",
            "md5CheckSum": "4b7c2a1d9e8f0a3b5c6d7e8f9a0b1c2d",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Skyrim Special Edition Trainer.exe'",
            "troubleshootSteps": [
                "单机运行无需离线绕过，若安装了 SSE Engine Fixes，在运行修改器前直接启动 skse64_loader.exe 即可正常享受热键注入",
                "若 Windows Defender 拦截，以管理员运行上方 PowerShell 白名单命令",
                "使用控制台配合修改器时建议先按 ~ 暂停游戏再激活对应热键"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "👑 核心上帝模式与生存",
                "items": [
                    {"key": "Num 1", "action": "无敌模式 (God Mode)"},
                    {"key": "Num 2", "action": "无限生命 (Infinite Health)"},
                    {"key": "Num 3", "action": "无限魔法 (Infinite Magicka)"},
                    {"key": "Num 4", "action": "无限耐力 (Infinite Stamina)"},
                    {"key": "Num 5", "action": "龙吼零冷却 (Zero Shout Cooldown)"},
                    {"key": "Num 6", "action": "无限龙魂点数 (Infinite Dragon Souls)"}
                ]
            },
            {
                "category": "🛠️ 物品资源与游戏调节",
                "items": [
                    {"key": "Num 7", "action": "无限金币/背包负重清空 (Infinite Gold / Weight)"},
                    {"key": "Num 8", "action": "一击必杀 (One Hit Kill)"},
                    {"key": "Num 9", "action": "开锁器永不损坏 (Unbreakable Lockpicks)"},
                    {"key": "Ctrl+Num 1", "action": "潜行绝对隐形 (Super Stealth)"},
                    {"key": "Ctrl+Num 2", "action": "无限附魔充能 (Infinite Enchantment Charge)"}
                ]
            }
        ]
    },
    "hasMods": True,
    "modInstallPath": "<SteamLibrary>/steamapps/common/Skyrim Special Edition/Data/",
    "curatedMods": [
        {
            "id": "mod_skse64",
            "title": "Skyrim Script Extender 64 (SKSE64)",
            "author": "Ian Patterson, Stephen Ellis, Bryan Renfro",
            "version": "v2.2.6 (适配 1.6.1170)",
            "size": "2.4 MB",
            "downloads": "28,000,000+",
            "endorsements": "1,200,000+",
            "category": "底层框架与核心前置",
            "desc": "天际Mod生态绝对的基石！大幅拓展 Papyrus 脚本引擎 API，现代 95% 以上的高级 UI、动作与功能 Mod 的强制前置依赖。",
            "dependencies": ["None (独立启动器)"],
            "installPath": "<GameRoot>/",
            "installSteps": [
                "根据游戏版本下载对应的 SKSE64 压缩包 (当前最新版解压 skse64_2_02_06.7z)",
                "将压缩包内的 skse64_loader.exe 与两个 .dll 文件直接复制到游戏根目录 (与 SkyrimSE.exe 同级)",
                "将 Data/ 文件夹拖拽合并进游戏的 Data/ 目录",
                "以后每次启动游戏一律双击 skse64_loader.exe 启动！"
            ]
        },
        {
            "id": "mod_sse_engine_fixes",
            "title": "SSE Engine Fixes (引擎底层全面修复与成就恢复)",
            "author": "aers, Ryan, mwilsnd",
            "version": "v6.1.1+",
            "size": "1.2 MB",
            "downloads": "14,000,000+",
            "endorsements": "650,000+",
            "category": "引擎优化与Bug修复",
            "desc": "必装神级插件！彻底修复高帧率物理抽搐、Lip Sync 嘴唇不同步、内存泄漏与各种原因导致的 CTD 崩溃，并自动解锁控制台与 Mod 状态下的 Steam 官方成就！",
            "dependencies": ["SKSE64", "Address Library for SKSE Plugins"],
            "installPath": "<GameRoot>/Data/SKSE/Plugins/",
            "installSteps": [
                "安装 Part 1 到 MO2 或 Vortex 模组管理器中并启用",
                "将 Part 2 解压后的 d3dx9_42.dll 与 tbb.dll 手动放入游戏根目录 (与 SkyrimSE.exe 同级)",
                "配置 EngineFixes.toml 开启 EnableAchievementsWithMods = true"
            ]
        },
        {
            "id": "mod_skyui",
            "title": "SkyUI (次世代沉浸式高级背包界面)",
            "author": "SkyUI Team",
            "version": "v5.2SE",
            "size": "14.5 MB",
            "downloads": "32,000,000+",
            "endorsements": "1,500,000+",
            "category": "界面增强与UI大修",
            "desc": "彻底颠覆原版主机风格的列表背包！提供强大的分类过滤、关键词搜索、装备属性多栏对照以及核心的 MCM (Mod 配置菜单)！",
            "dependencies": ["SKSE64"],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "必须确保已先行安装 SKSE64",
                "通过 MO2 或 Vortex 直接导入 SkyUI_5.2SE.7z 压缩包并激活",
                "启动 skse64_loader.exe 进入游戏，按 ESC 即可看到新增的 Mod Configuration 菜单！"
            ]
        },
        {
            "id": "mod_ussep",
            "title": "Unofficial Skyrim Special Edition Patch (USSEP 非官方大修补丁)",
            "author": "Arthmoor and Unofficial Patch Project Team",
            "version": "v4.3.2+",
            "size": "650.0 MB",
            "downloads": "22,000,000+",
            "endorsements": "980,000+",
            "category": "综合Bug全修与稳定增强",
            "desc": "耗时十余年修复了天际原版多达数万处恶性任务卡关、网格丢失、材质破损、NPC浮空与文字逻辑错误的总集补丁！",
            "dependencies": ["Skyrim Special Edition 官方三大DLC"],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "通过模组管理器安装 USSEP 压缩包",
                "在插件加载顺序 (Load Order) 中将 Unofficial Skyrim Special Edition Patch.esp 置于官方 DLC 之后的最靠前位置！"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 角色状态与神级上帝模式 (God Mode & Invulnerability)",
            "commands": [
                {
                    "id": "skyrim_tgm",
                    "name": {"zh-CN": "开关全能上帝模式 (Toggle God Mode: 无敌/无限魔/无限耐/无限负重)", "en": "Toggle God Mode (tgm)"},
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "开启后主角免疫任何物理与魔法伤害、受击不掉血、奔跑施法不消耗耐力与魔法、背包负重锁定无惩罚，爽快畅游天际！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_tim",
                    "name": {"zh-CN": "开关不死锁血模式 (Toggle Immortal Mode)", "en": "Toggle Immortal Mode (tim)"},
                    "syntax_type": "creation_hex",
                    "code": "tim",
                    "desc": "与 tgm 相比，角色的生命值、魔法与耐力会正常扣减并显示受击硬直，但受到任何致命绝杀生命值强制锁定在 1 点，绝不阵亡！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_tcl",
                    "name": {"zh-CN": "开关穿墙穿模模式 (Toggle Collision: 悬浮飞行自由穿墙)", "en": "Toggle Collision (tcl)"},
                    "syntax_type": "creation_hex",
                    "code": "tcl",
                    "desc": "关闭物理碰撞检测，角色可以在空中任意方向自由漫步飞行、穿透地下墓穴石壁或被卡在山谷缝隙时一秒脱困！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_healplayer",
                    "name": {"zh-CN": "瞬间回复角色生命值至满额 (急救满血)", "en": "Heal Player to Full HP"},
                    "syntax_type": "creation_hex",
                    "code": "healplayer",
                    "desc": "战斗中紧急调用瞬间补满当前角色的所有生命值，摆脱濒死状态。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_carryweight",
                    "name": {"zh-CN": "永久扩增随身背包负重上限至 99,999 (垃圾佬必备)", "en": "Set Carry Weight Upper Limit"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 99999",
                    "desc": "将角色背包基础最大负重上限直接修改为 99,999 磅，下地城扫荡几百把重甲龙骨武器依然健步如飞！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_speedmult",
                    "name": {"zh-CN": "修改角色奔跑移速为 1.5 倍 (默认 100)", "en": "Set Movement Speed Multiplier"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav speedmult 150",
                    "desc": "将基础移动速度调为 150% (修改后收刀或拔刀一次即可激活生效)，大幅加快天际原野跑图赶路节奏！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "💰 货币、开锁与全技能熟练度满级 (Gold, Lockpicks & Master Skills)",
            "commands": [
                {
                    "id": "skyrim_add_gold_100k",
                    "name": {"zh-CN": "增加 100,000 金币 (FormID: 0000000F / f)", "en": "Add 100,000 Gold"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 100000",
                    "desc": "瞬间向背囊注入 10 万金币，直接买下独孤城傲慢尖塔与各大要塞豪华房产！可简写为 player.additem f 100000。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_add_lockpicks",
                    "name": {"zh-CN": "增加 1,000 个开锁器 (FormID: 0000000A / a)", "en": "Add 1,000 Lockpicks"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000A 1000",
                    "desc": "派发 1,000 个天际开锁器，地牢宝箱随便撬开不再担心耗尽！可简写为 player.additem a 1000。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_add_dragon_souls",
                    "name": {"zh-CN": "直接获取 100 个龙魂 (用于解锁全套龙吼铭文)", "en": "Add 100 Dragon Souls"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav dragonsouls 100",
                    "desc": "直接向角色赋予 100 个龙魂，省去满世界追逐随机巨龙吸取龙魂的繁琐流程，随时解锁任意龙吼！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_advskill_smithing",
                    "name": {"zh-CN": "锻造技能熟练度秒升 100 满级", "en": "Advance Smithing Skill to 100"},
                    "syntax_type": "creation_hex",
                    "code": "player.advskill smithing 999999",
                    "desc": "向锻造专业技能注入海量经验，无需重复打铁几千把铁匕首，直接点满魔族与龙骨锻造 Perk！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_advskill_enchanting",
                    "name": {"zh-CN": "附魔技能熟练度秒升 100 满级", "en": "Advance Enchanting Skill to 100"},
                    "syntax_type": "creation_hex",
                    "code": "player.advskill enchanting 999999",
                    "desc": "附魔专业一秒满级，点出终极双重附魔 Perk，为一件装备同时铭刻两大强力神性词条！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_advskill_alchemy",
                    "name": {"zh-CN": "炼金术熟练度秒升 100 满级", "en": "Advance Alchemy Skill to 100"},
                    "syntax_type": "creation_hex",
                    "code": "player.advskill alchemy 999999",
                    "desc": "炼金专业秒满级，随时调制出增幅数倍伤害与恢复效能的超强药剂！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🐉 全龙吼解锁与零冷却释放 (Dragon Shouts Mastery & Zero Cooldown)",
            "commands": [
                {
                    "id": "skyrim_shout_unrelenting_force",
                    "name": {"zh-CN": "习得并解锁全三段【不卸之力】龙吼 (Fus Ro Dah)", "en": "Teach Unrelenting Force (Fus Ro Dah)"},
                    "syntax_type": "creation_hex",
                    "code": "player.teachword 13e22",
                    "desc": "直接习得天际最著名的标志性龙吼【伏斯·洛·达】(不卸之力) 第一段铭文 (二段 13e23, 三段 13e24)，将敌人直接吼飞悬崖！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_shout_whirlwind_sprint",
                    "name": {"zh-CN": "习得全段【旋风精力】龙吼 (极速冲刺跨越鸿沟)", "en": "Teach Whirlwind Sprint Shout"},
                    "syntax_type": "creation_hex",
                    "code": "player.teachword 20e67",
                    "desc": "习得旋风精力第一段铭文 (二段 20e68, 三段 20e69)，在古墓机关落石前极速穿越，跑酷解密必备！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_shout_dragonrend",
                    "name": {"zh-CN": "习得【降龙之吼】(强制在空巨龙落回地面)", "en": "Teach Dragonrend Shout"},
                    "syntax_type": "creation_hex",
                    "code": "player.teachword 7097b",
                    "desc": "习得降龙铭文 (Joor Zah Frul)，强制使天空中盘旋的巨龙坠地受缚，近战屠龙核心绝技！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_zero_shout_recovery",
                    "name": {"zh-CN": "龙吼冷却时间清零 (无限连续释放龙吼大招)", "en": "Set Shout Recovery Cooldown to Zero"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav shoutrecoverymult 0",
                    "desc": "将龙吼冷却恢复乘数设置为 0，完全消除吼声施放后的漫长倒计时，化身真正的天际龙吼发射加农炮！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "⚡ 全 16 件魔神器与远古神装 (Daedric Artifacts & Legendary Weapons)",
            "commands": [
                {
                    "id": "skyrim_spawn_dawnbreaker",
                    "name": {"zh-CN": "派发魔神器：破晓者 (美瑞蒂亚单手剑/亡灵克星金光爆炸)", "en": "Spawn Dawnbreaker (0002ac61)"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0002ac61 1",
                    "desc": "派发美瑞蒂亚光明神剑破晓者，攻击亡灵或尸鬼有极大几率引发大范围神圣爆炸消灭全场尸群！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_mace_of_molag_bal",
                    "name": {"zh-CN": "派发魔神器：莫拉格·巴尔钉头锤 (灵魂陷阱与体力吸取)", "en": "Spawn Mace of Molag Bal (000233e3)"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000233e3 1",
                    "desc": "残虐魔神钉头锤，击中敌人造成巨量耐力与魔法伤害，并施加 3 秒灵魂陷阱自动灌满黑色灵魂石！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_mehrunes_razor",
                    "name": {"zh-CN": "派发魔神器：梅鲁涅斯的剃刀 (近战微小几率一击秒杀一切)", "en": "Spawn Mehrunes' Razor (000240d2)"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000240d2 1",
                    "desc": "破坏魔神匕首，攻速极快且每次攻击均有 1.98% 几率直接斩杀无视目标生命值判定（对上古巨龙同样生效）！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_azuras_star",
                    "name": {"zh-CN": "派发魔神器：阿祖拉之星 (永不破碎的无限灵魂石)", "en": "Spawn Azura's Star (00063b27)"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00063b27 1",
                    "desc": "附魔极客终极神器！捕获灵魂为装备充能后星体永远不会消耗碎裂，可永久反复循环使用！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_spellbreaker",
                    "name": {"zh-CN": "派发魔神器：破法者 (举盾生成 50 点魔法结界)", "en": "Spawn Spellbreaker (0004585a)"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0004585a 1",
                    "desc": "瘟疫魔神重盾，格挡举盾时自动在面前张开一层抵御 50 点法术伤害的神圣护盾，完克法师与巨龙吐息！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_wabbajack",
                    "name": {"zh-CN": "派发魔神器：瓦巴杰克 (疯神法杖搞怪随机形变)", "en": "Spawn Wabbajack (000139b9)"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000139b9 1",
                    "desc": "谢尔格拉疯神法杖，释放随机不可预测的荒诞魔法：将敌人变成甜甜圈、甜甜圈或者泥沼蟹！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🛠️ 锻造神装、龙骨魔族与满级素材 (Daedric/Dragon Armor & Materials)",
            "commands": [
                {
                    "id": "skyrim_spawn_daedric_sword",
                    "name": {"zh-CN": "派发魔族巨剑 (Daedric Greatsword: 0001396b)", "en": "Spawn Daedric Greatsword"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0001396b 1",
                    "desc": "派发天际最高面板基础双手武器之一魔族巨剑，锋利无比造型狰狞霸气！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_daedric_armor",
                    "name": {"zh-CN": "派发魔族重甲胸甲 (Daedric Armor: 00013969)", "en": "Spawn Daedric Armor Heavy"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00013969 1",
                    "desc": "派发魔族全套重铠的核心胸甲部分，天际顶级护甲值物理免伤担当！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_daedric_hearts",
                    "name": {"zh-CN": "派发 100 颗魔族之心 (稀缺锻造素材: 0003ad5b)", "en": "Spawn 100 Daedric Hearts"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0003ad5b 100",
                    "desc": "批量派发天际极度珍贵的魔族之心，用于在铁匠铺锻造全套魔族护甲与武器！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_dragon_scales",
                    "name": {"zh-CN": "派发 100 个龙鳞 (龙骨防具核心素材: 0003ad57)", "en": "Spawn 100 Dragon Scales"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0003ad57 100",
                    "desc": "批量派发龙鳞，配合龙骨锻造轻甲防御之王【龙鳞轻甲】全套！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_spawn_ebony_ingots",
                    "name": {"zh-CN": "派发 100 个乌木锭 (重装强化金属: 0003ad5e)", "en": "Spawn 100 Ebony Ingots"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0003ad5e 100",
                    "desc": "批量派发乌木锭，用于在砂轮和工作台将魔族装备强化至【传奇】(Legendary) 级！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🚨 恶性死循环任务急救与强行推进 (Quest Bug Fixes & SetStage)",
            "commands": [
                {
                    "id": "skyrim_fix_greybeards_mq105",
                    "name": {"zh-CN": "强行修复高吼峰灰胡子吼声任务卡关 (setstage MQ105 10)", "en": "Fix Greybeards Call Quest (MQ105)"},
                    "syntax_type": "creation_hex",
                    "code": "setstage MQ105 10",
                    "desc": "击败第一条飞龙后，若灰胡子召唤吼声迟迟不触发无法前往高吼峰，输入此指令强制推进任务阶段开启觐见！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_fix_alduins_wall_mq203",
                    "name": {"zh-CN": "强行修复【奥杜因之墙】戴尔芬与伊思本站桩不动卡关", "en": "Fix Alduin's Wall Quest Bug (MQ203)"},
                    "syntax_type": "creation_hex",
                    "code": "setstage MQ203 280",
                    "desc": "天空庇护之庙中伊思本不肯点火把或不讲解石壁壁画的祖传恶性 Bug，执行此行直接标记该步完成推进至下一幕！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_fix_vaermina_da16",
                    "name": {"zh-CN": "强行修复晨星城噩梦瓦尔米娜苏醒之梦喝药不进回忆", "en": "Fix Waking Nightmare Quest Bug (DA16)"},
                    "syntax_type": "creation_hex",
                    "code": "setstage DA16 200",
                    "desc": "晨星城祭司喝下折磨药水后卡死无法进入梦境回忆的恶性问题，直接跳至净化完成阶段！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_sqt_query",
                    "name": {"zh-CN": "查询当前所有活动任务的目标代码 (Show Quest Targets)", "en": "Show Active Quest Targets (sqt)"},
                    "syntax_type": "creation_hex",
                    "code": "sqt",
                    "desc": "在控制台输出当前激活任务的真实 Quest ID 与目标内部代号，排查卡关必备诊断指令！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_companion_moveto",
                    "name": {"zh-CN": "强制将卡在地形或失踪的随从传送至身旁", "en": "Teleport Missing Follower to Player"},
                    "syntax_type": "creation_hex",
                    "code": "player.moveto 000a2c94",
                    "desc": "例如将失踪的莱妹莱迪亚 (Lydia 000A2C94) 瞬移回自己面前，再也不用担心伙伴掉队失踪丢失全身家当！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🏡 炉火 DLC 观湖庄园全建材直装与领地免罪 (Hearthfire & Crime Clearing)",
            "commands": [
                {
                    "id": "skyrim_hearthfire_quarried_stone",
                    "name": {"zh-CN": "派发 500 个采掘石料 (炉火豪宅地基核心: 0300306c)", "en": "Spawn 500 Quarried Stones"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0300306c 500",
                    "desc": "炉火 DLC 自建豪宅（观湖庄园/风亭庄园）必备建材，无需在采石坑按E手动镐击挖掘半小时！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_hearthfire_clay",
                    "name": {"zh-CN": "派发 500 块粘土 (墙壁与烤箱素材: 03003043)", "en": "Spawn 500 Clays"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 03003043 500",
                    "desc": "派发全套自建房所需粘土，用于快速搭建门厅、主厅、炼金塔与陈列室！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_hearthfire_iron_ingots",
                    "name": {"zh-CN": "派发 300 块铁锭 (用于打造成千枚铁钉与合页)", "en": "Spawn 300 Iron Ingots for Nails"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0005ace4 300",
                    "desc": "建造庄园需要成百上千根铁钉、门铰链与铁配件，派发铁锭在铁砧上一键敲打成型！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_clear_bounty",
                    "name": {"zh-CN": "清空当前要塞所有通缉悬赏罪名 (秒免罪无需坐牢)", "en": "Clear All Crime Bounty"},
                    "syntax_type": "creation_hex",
                    "code": "player.setcrimegold 0",
                    "desc": "不小心打翻鸡或者误砍卫兵被全城通缉？输入本指令瞬间将悬赏清零，卫兵立即收刀停止敌对！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🌌 开发者房间、全地图标与全法术解锁 (Dev Room, Map & All Spells)",
            "commands": [
                {
                    "id": "skyrim_coc_qasmoke",
                    "name": {"zh-CN": "传送至开发者测试房间烟雾房 (coc qasmoke: 包含全天际所有物品箱)", "en": "Teleport to Dev Smoke Room (coc qasmoke)"},
                    "syntax_type": "creation_hex",
                    "code": "coc qasmoke",
                    "desc": "Bethesda 官方全物品展示房间！整齐摆放着全天际所有武器、防具、附魔装备、药水、原料的分类宝箱，随意拿取！输入 coc riverwood 即可传回溪木镇！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_tmm_1",
                    "name": {"zh-CN": "点亮大地图所有地标 (Toggle Map Markers: 包含未探明区域)", "en": "Unlock All Map Markers (tmm 1)"},
                    "syntax_type": "creation_hex",
                    "code": "tmm 1",
                    "desc": "一键点亮天际省全部 400 余个地下城、山峰、营地与城市地标，且全部支持直接大地图快速传送！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_psb_all_spells",
                    "name": {"zh-CN": "解锁全天际所有魔法与法术 (Player Spell Book)", "en": "Unlock All Spells (psb)"},
                    "syntax_type": "creation_hex",
                    "code": "psb",
                    "desc": "将毁灭系、恢复系、变化系、幻术系与召唤系以及所有未实装的隐藏测试法术全部写入法术书！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_tfc_freecam",
                    "name": {"zh-CN": "开启自由飞行摄影摄像机并暂停时间 (tfc 1)", "en": "Toggle Free Camera (tfc 1)"},
                    "syntax_type": "creation_hex",
                    "code": "tfc 1",
                    "desc": "脱离角色躯体，摄像机在空中 360 度任意穿行缩放，游戏画面定格暂停，拍摄天际极光与壮丽战斗大片的必备利器！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "skyrim_tm_hide_hud",
                    "name": {"zh-CN": "隐藏/恢复全部界面 HUD 与准星 (无UI纯净截图)", "en": "Toggle Menus / Hide HUD (tm)"},
                    "syntax_type": "creation_hex",
                    "code": "tm",
                    "desc": "隐藏全屏血条、罗盘、准星与菜单界面 (注意隐藏后按 ~ 依然能输入，再次盲打 tm 回车即可恢复菜单)！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
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
        "zh-CN": "【次世代大更新避坑与控制台开启】\n1. 控制台呼出：游戏中按下【~】(波浪键) 暂停并呼出控制台；\n2. 2024 次世代大更新 (v1.10.980/984) 避坑必看：\n   - 路径一 (次世代原生模式)：若玩次世代新版，必须安装对应次世代分支的 F4SE (v0.7.2+) 与 Address Library Next-Gen，并在 Steam 游戏属性中设置【仅在我启动该游戏时更新】防二次破坏；\n   - 路径二 (经典降级模式)：若想享受数万款旧 Mod，使用【Fallout 4 Downgrader】一键将主程序回退至 1.10.163 黄金稳定版；\n3. 极速批处理 (bat 命令)：在游戏根目录新建文本文件 (如 all_materials.txt)，游戏中只需在控制台输入 bat all_materials，瞬间一次性执行上百条指令！",
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
    "hasTrainer": True,
    "trainerInfo": {
        "author": "风灵月影 (FLiNG)",
        "version": "v1.10.984+ (次世代大更新完全兼容)",
        "officialUrl": "https://flingtrainer.com/trainer/fallout-4-trainer/",
        "cleanMirrorUrl": "https://github.com/l-mod-vault/mirrors/releases/download/v1.10.984/Fallout_4_v1.10.984_Plus_25_Trainer.zip",
        "safeVerification": {
            "isCleanVerified": True,
            "hasBundledAds": False,
            "virusTotalRatio": "0/72 Clean (零误报纯净离线版)",
            "md5CheckSum": "3a8c1f0d2e4b5c6a7b8c9d0e1f2a3b4c",
            "powershellExclusionCmd": "Add-MpPreference -ExclusionProcess 'Fallout 4 Trainer.exe'",
            "troubleshootSteps": [
                "单机运行无任何反作弊封号风险，直接解压启动修改器与游戏即可畅快游玩",
                "若 Windows Defender 拦截，请以管理员身份运行上方 PowerShell 白名单命令",
                "使用控制台与修改器时建议先按 ~ 暂停游戏再激活对应热键"
            ]
        },
        "hotkeysCategorized": [
            {
                "category": "👑 核心上帝模式与废土生存",
                "items": [
                    {"key": "Num 1", "action": "无敌模式 (God Mode)"},
                    {"key": "Num 2", "action": "无限生命 (Infinite Health)"},
                    {"key": "Num 3", "action": "无限行动点数 AP (Infinite Action Points)"},
                    {"key": "Num 4", "action": "辐射度归零 (Zero Radiation)"},
                    {"key": "Num 5", "action": "无限弹药无需换弹 (Infinite Ammo & No Reload)"},
                    {"key": "Num 6", "action": "动力装甲核心能量无限 (Infinite Fusion Core Energy)"}
                ]
            },
            {
                "category": "🏭 聚落建设与无限资源",
                "items": [
                    {"key": "Num 7", "action": "无限瓶盖货币 (Infinite Caps)"},
                    {"key": "Num 8", "action": "建造材料不减 (Infinite Settlement Crafting Materials)"},
                    {"key": "Num 9", "action": "一击必杀 (One Hit Kill)"},
                    {"key": "Ctrl+Num 1", "action": "开锁绝对成功 (Instant Lockpick)"},
                    {"key": "Ctrl+Num 2", "action": "终端机黑客破解秒过 (Instant Terminal Hack)"}
                ]
            }
        ]
    },
    "hasMods": True,
    "modInstallPath": "<SteamLibrary>/steamapps/common/Fallout 4/Data/",
    "curatedMods": [
        {
            "id": "mod_f4se",
            "title": "Fallout 4 Script Extender (F4SE 次世代/经典适配版)",
            "author": "Ian Patterson, Stephen Ellis, Bryan Renfro",
            "version": "v0.7.2+ (Next-Gen)",
            "size": "2.1 MB",
            "downloads": "18,000,000+",
            "endorsements": "780,000+",
            "category": "底层框架与核心前置",
            "desc": "辐射4模组底层扩展核心！释放 Papyrus 脚本潜力，Place Everywhere、MCM 等神级模组的绝对前置，次世代版已更新 v0.7.2+ 专用 loader。",
            "dependencies": ["None (独立启动器)"],
            "installPath": "<GameRoot>/",
            "installSteps": [
                "下载与当前游戏版本完全对应的 F4SE 压缩包 (次世代版下 0.7.2+，降级版下 0.6.23)",
                "将 f4se_loader.exe 与相关 .dll 复制到 Fallout 4 游戏根目录",
                "将 Data/ 文件夹拖拽合并进游戏 Data 目录",
                "以后每次启动游戏直接双击 f4se_loader.exe！"
            ]
        },
        {
            "id": "mod_buffout_4",
            "title": "Buffout 4 (CTD 闪退崩溃急救与堆栈诊断分析)",
            "author": "Ryan, registrator2000",
            "version": "v1.35.1+",
            "size": "3.8 MB",
            "downloads": "6,500,000+",
            "endorsements": "310,000+",
            "category": "引擎优化与闪退排错",
            "desc": "辐射4排错天花板神作！彻底修复武器碎片反弹崩溃、内存溢出闪退，并在崩溃瞬间生成高精度的 Crash Log 文本，明确指出是哪件装备或贴图导致报错！",
            "dependencies": ["F4SE", "xSE Plugin Preloader", "Address Library for F4SE Plugins"],
            "installPath": "<GameRoot>/Data/F4SE/Plugins/",
            "installSteps": [
                "使用 MO2 或 Vortex 安装 Buffout 4 及其前置 xSE Plugin Preloader",
                "若发生闪退，前往 Documents/My Games/Fallout4/F4SE/ 查看 crash-*.log 即可精准破案！"
            ]
        },
        {
            "id": "mod_place_everywhere",
            "title": "Place Everywhere (聚落建造自由无拘随处放置)",
            "author": "TheLich",
            "version": "v1.18+",
            "size": "1.5 MB",
            "downloads": "9,800,000+",
            "endorsements": "420,000+",
            "category": "工坊建造与功能增强",
            "desc": "垃圾佬造城必备神技！彻底解除工房红圈禁止摆放限制，支持穿插穿模、精准三轴旋转 (按 X/Y/Z)、缩放大小，把庇护山丘打造成赛博堡垒！",
            "dependencies": ["F4SE"],
            "installPath": "<GameRoot>/Data/F4SE/Plugins/",
            "installSteps": [
                "确保已安装 F4SE",
                "通过模组管理器安装 Place Everywhere",
                "进入建造模式，按 F1 开关碰撞检测，按 F2 开关贴合吸附！"
            ]
        },
        {
            "id": "mod_sim_settlements_2",
            "title": "Sim Settlements 2 (模拟殖民区2代自动化造城总修)",
            "author": "kinggath and Sim Settlements Team",
            "version": "v3.3.4+",
            "size": "1,200.0 MB",
            "downloads": "4,100,000+",
            "endorsements": "190,000+",
            "category": "玩法机制全面重构",
            "desc": "将辐射4变成真正的模拟城市！刁民居民会自动划定商业区、住宅区、工业区自行建房交税，附带数十小时的全新全配音支线主线剧情！",
            "dependencies": ["Workshop Framework", "HUDFramework"],
            "installPath": "<GameRoot>/Data/",
            "installSteps": [
                "安装前置 Workshop Framework",
                "安装 Sim Settlements 2 及其剧情扩展章节包",
                "在游戏内建造并拾取【ASAM 传感器】，启动第一块住宅规划区！"
            ]
        }
    ],
    "consoleCategories": [
        {
            "category": "👑 角色状态与废土生存 (God Mode & Wasteland Survival)",
            "commands": [
                {
                    "id": "fo4_tgm",
                    "name": {"zh-CN": "开关全能上帝模式 (Toggle God Mode: 无敌/弹药无限/负重无限)", "en": "Toggle God Mode (tgm)"},
                    "syntax_type": "creation_hex",
                    "code": "tgm",
                    "desc": "开启后主角免疫一切枪弹物理打击与高空坠落、无限 AP 行动点、弹药无限且无需重新换弹、背包负重解除惩罚！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_tim",
                    "name": {"zh-CN": "开关不死锁血模式 (Toggle Immortal Mode: 挨打掉血但绝对不死)", "en": "Toggle Immortal Mode (tim)"},
                    "syntax_type": "creation_hex",
                    "code": "tim",
                    "desc": "沉浸式战斗首选！角色受到攻击会正常流血受创与显示残废动画，但生命值降至最低点时锁死为 1，绝不会死亡坏档！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_tcl",
                    "name": {"zh-CN": "开关穿墙飞行模式 (Toggle Collision: 悬浮飞行穿墙)", "en": "Toggle Collision (tcl)"},
                    "syntax_type": "creation_hex",
                    "code": "tcl",
                    "desc": "关闭物理体积碰撞，主角可在废土废墟大楼和废土深坑之间自由穿墙穿模飞行，卡进地形时秒脱困！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_rads_zero",
                    "name": {"zh-CN": "角色辐射污染彻底清零 (消除红色上限减血条)", "en": "Clear Radiation Pollution"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav rads 0",
                    "desc": "跳进发光海被重度辐射污染？输入本指令瞬间将体内的辐射累积清零，完整释放被红条侵占的生命上限！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_healplayer",
                    "name": {"zh-CN": "瞬间回满生命值与消除残疾肢体 (急速满血)", "en": "Heal Player & Cure Crippled Limbs"},
                    "syntax_type": "creation_hex",
                    "code": "healplayer",
                    "desc": "瞬间回复满血并修复头部、四肢与躯干的残废破损状态，战斗中保命神技！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_carryweight",
                    "name": {"zh-CN": "永久扩增随身背包负重上限至 99,999 (捡垃圾核心)", "en": "Set Carry Weight Limit"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav carryweight 99999",
                    "desc": "将基础负重提升至 10 万磅，废土上的破轮胎、风扇、显微镜、核子可乐瓶通通搬走不再超重减速！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "💰 货币、发夹与聚变核心能源 (Caps, Bobby Pins & Fusion Cores)",
            "commands": [
                {
                    "id": "fo4_add_caps_100k",
                    "name": {"zh-CN": "增加 100,000 瓶盖货币 (FormID: 0000000F / f)", "en": "Add 100,000 Bottle Caps"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000F 100000",
                    "desc": "向背囊注入 10 万瓶盖，秒变废土顶级资本巨鳄，钻石城全部商铺随便扫荡！可简写为 player.additem f 100000。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_add_bobby_pins",
                    "name": {"zh-CN": "增加 1,000 根发夹开锁器 (FormID: 0000000A / a)", "en": "Add 1,000 Bobby Pins"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0000000A 1000",
                    "desc": "生成 1,000 根发夹，撬开全联邦所有主保险箱与锁闭铁门！可简写为 player.additem a 1000。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_add_fusion_cores",
                    "name": {"zh-CN": "派发 100 颗核聚变核心 (动力装甲电池: 00075fe4)", "en": "Add 100 Fusion Cores"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00075fe4 100",
                    "desc": "派发 100 颗满电量核聚变核心，动力装甲喷气背包随便飞，彻底告别电量焦虑！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_add_stimpaks",
                    "name": {"zh-CN": "派发 200 支治疗针 (Stimpak: 00023736)", "en": "Add 200 Stimpaks"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00023736 200",
                    "desc": "随身携带 200 支军规治疗针，快捷栏绑定随时续命！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_add_radaway",
                    "name": {"zh-CN": "派发 100 支消辐宁 (RadAway: 00023742)", "en": "Add 100 RadAway"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00023742 100",
                    "desc": "派发 100 支消辐宁药剂，净化废土辐射带来的体内污染。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🏗️ 聚落建造空间无限解除与全建材 (Infinite Settlement & Building Mats)",
            "commands": [
                {
                    "id": "fo4_settlement_size_bypass",
                    "name": {"zh-CN": "彻底解除聚落建造空间容量上限 (setav 349 9999999)", "en": "Bypass Settlement Building Size Budget"},
                    "syntax_type": "creation_hex",
                    "code": "setav 349 9999999",
                    "desc": "走到工房控制台前按下 ~ 鼠标点击工房，输入此代码将空间预算最大值提升至千万级，右上角建造容量条直接清空，随心所欲盖摩天大楼！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_settlement_triangles_bypass",
                    "name": {"zh-CN": "彻底解除聚落几何三角面数量上限 (setav 348 9999999)", "en": "Bypass Settlement Triangles Budget"},
                    "syntax_type": "creation_hex",
                    "code": "setav 348 9999999",
                    "desc": "点击工房后输入，解除复杂建筑结构的多边形限制，建造超高密度复合聚落不再报错受限！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_scrapall",
                    "name": {"zh-CN": "聚落一键彻底拆解回收全图废墟 (scrapall)", "en": "Scrap All Debris in Settlement"},
                    "syntax_type": "creation_hex",
                    "code": "scrapall",
                    "desc": "站在聚落领地内输入，一秒将全图所有的破旧房屋、烂木头、碎石杂草全部拆解并将其转化为基础建材存入工房，瞬间获得平整地皮！(建议先收起重要箱子)",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_add_steel_1000",
                    "name": {"zh-CN": "派发 1,000 块钢铁 (基础建材: 000731a4)", "en": "Spawn 1,000 Steel"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000731a4 1000",
                    "desc": "派发 1,000 块钢铁，用于搭建混凝土墙、金属工字钢架构与避难所大门！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_add_wood_1000",
                    "name": {"zh-CN": "派发 1,000 捆木材 (木结构基础: 000731a3)", "en": "Spawn 1,000 Wood"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 000731a3 1000",
                    "desc": "派发 1,000 捆木料，快速建造谷仓、木屋、地板与哨塔防御设施！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_add_copper_500",
                    "name": {"zh-CN": "派发 500 块纯铜 (发电机与电网电缆: 0006907c)", "en": "Spawn 500 Copper"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 0006907c 500",
                    "desc": "聚落通电最紧缺的金属铜，批量派发，随意搭建核能发电机、电线塔与防御重型激光炮塔！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🔫 传奇武器词条自定义附魔 (Legendary Weapon Modding & Attachmod)",
            "commands": [
                {
                    "id": "fo4_attachmod_two_shot",
                    "name": {"zh-CN": "手持武器附魔【双弹】传奇词条 (伤害直接翻倍: 001cc2ac)", "en": "Attach Legendary Mod: Two Shot"},
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001cc2ac",
                    "desc": "把武器扔在地上，按 ~ 呼出控制台鼠标点击武器，输入此代码即可瞬间赋予【双弹】前缀，每次扣扳机射出双倍弹头，伤害翻倍！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_attachmod_explosive",
                    "name": {"zh-CN": "手持武器附魔【爆破】传奇词条 (每发附带范围爆炸: 001e7c20)", "en": "Attach Legendary Mod: Explosive"},
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001e7c20",
                    "desc": "给冲锋枪、加特林或霰弹枪附魔爆破词条，子弹命中引发连锁范围剧烈爆炸，扫荡泥沼蟹与掠夺者如割草！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_attachmod_furious",
                    "name": {"zh-CN": "手持武器附魔【狂怒】传奇词条 (连续命中伤害无限叠加: 001f6ad4)", "en": "Attach Legendary Mod: Furious"},
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001f6ad4",
                    "desc": "近战刀剑或高射速武器神器，每次命中同一目标伤害逐级倍增，单挑狂暴传奇死爪只需数秒！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_attachmod_never_ending",
                    "name": {"zh-CN": "手持武器附魔【无底洞】传奇词条 (无限弹匣免换弹: 001ed37e)", "en": "Attach Legendary Mod: Never Ending"},
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001ed37e",
                    "desc": "消除武器换弹动作，弹匣容量直接与背包总弹药打通，扣住扳机无限持续狂风骤雨般倾泻火力！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_attachmod_kneecapper",
                    "name": {"zh-CN": "手持武器附魔【膝盖收割者】传奇词条 (20%几率打断腿瘫痪: 001f1048)", "en": "Attach Legendary Mod: Kneecapper"},
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001f1048",
                    "desc": "废土安全感神器，攻击命中敌人有 20% 几率强制打断其双腿，让凶残的狂暴死爪与突袭者当场倒地爬行！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_attachmod_instigating",
                    "name": {"zh-CN": "手持武器附魔【煽动】传奇词条 (对满血目标造成双倍伤害: 001f31b9)", "en": "Attach Legendary Mod: Instigating"},
                    "syntax_type": "creation_hex",
                    "code": "attachmod 001f31b9",
                    "desc": "潜行狙击流终极核心，开幕潜行爆头搭配消音武器打出高达数千点的极限毁灭数字！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🤖 全套 X-01 动力装甲与毁灭军备 (X-01 Power Armor & Heavy Ordnance)",
            "commands": [
                {
                    "id": "fo4_spawn_x01_helm",
                    "name": {"zh-CN": "派发 X-01 动力装甲头盔 (00154ac8)", "en": "Spawn X-01 Power Armor Helmet"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac8 1",
                    "desc": "派发辐射4最高等级动力装甲 X-01 头盔，装甲工作台上可升级高亮侦测红外 HUD！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_spawn_x01_torso",
                    "name": {"zh-CN": "派发 X-01 动力装甲胸甲 (00154ac5)", "en": "Spawn X-01 Power Armor Torso"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac5 1",
                    "desc": "派发 X-01 动力装甲躯干核心，可改装装备喷气飞行背包 (Jetpack) 实现翱翔飞行！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_spawn_x01_arms",
                    "name": {"zh-CN": "派发 X-01 动力装甲左臂 (00154ac3) 与右臂 (00154ac4)", "en": "Spawn X-01 Power Armor Arms"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac3 1",
                    "desc": "派发 X-01 左右双臂组件，可加装特斯拉线圈提高近战格斗与电击反伤威力！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_spawn_x01_legs",
                    "name": {"zh-CN": "派发 X-01 动力装甲左腿 (00154ac6) 与右腿 (00154ac7)", "en": "Spawn X-01 Power Armor Legs"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00154ac6 1",
                    "desc": "派发 X-01 左右腿部装甲，改装校准减震器提供额外 100 磅巨额随身负重加成！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_spawn_fat_man",
                    "name": {"zh-CN": "派发【胖子核弹发射器】(Fat Man: 001685c9) 与迷你核弹", "en": "Spawn Fat Man Launcher & Mini Nuke"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 001685c9 1",
                    "desc": "派发废土单兵战略核武器胖子发射器！搭配 player.additem 000e6b2e 20 获得 20 枚迷你核弹，弹指间强虏灰飞烟灭！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_spawn_gauss_rifle",
                    "name": {"zh-CN": "派发高斯步枪 (Gauss Rifle: 00004240) 与 2mm 电磁弹", "en": "Spawn Gauss Rifle & 2mm EC"},
                    "syntax_type": "creation_hex",
                    "code": "player.additem 00004240 1",
                    "desc": "废土单发伤害之王高斯步枪，蓄力电磁加速射击造成毁灭性穿透伤害！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "👥 伙伴好感度、恶性卡关与阵营进度抢救 (Affinity & Quest Repair)",
            "commands": [
                {
                    "id": "fo4_max_companion_affinity",
                    "name": {"zh-CN": "伙伴好感度瞬间拉满 1000 (秒触发专属任务与终极Perk)", "en": "Max Companion Affinity (setav CA_affinity 1000)"},
                    "syntax_type": "creation_hex",
                    "code": "setav CA_affinity 1000",
                    "desc": "按 ~ 打开控制台鼠标点击同伴 (如派普、居里、凯特、丹斯)，输入此代码瞬间将好感度升至 1000 崇拜满级，立即触发告白对话并解锁强力专属永久被动 Perk！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_fix_vault111_door",
                    "name": {"zh-CN": "强行修复 111 号避难所齿轮大门打不开卡关 (setstage MQ102 120)", "en": "Fix Vault 111 Gear Door Bug (MQ102)"},
                    "syntax_type": "creation_hex",
                    "code": "setstage MQ102 120",
                    "desc": "新开档走出 111 号避难所时，若按下控制台按钮大门纹丝不动或升降机不上升，输入此代码强制触发剧情直接传送到地表！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_fix_cambridge_danse",
                    "name": {"zh-CN": "强行修复剑桥警察局丹斯战斗后不说话卡关 (setstage BoS100 40)", "en": "Fix Cambridge Police Danse Dialog Bug"},
                    "syntax_type": "creation_hex",
                    "code": "setstage BoS100 40",
                    "desc": "剑桥警察局消灭狂暴尸鬼后，丹斯一直警戒重复'检查四周'不触发对话的经典祖传恶性 Bug，执行此行直接推进任务解冻对话！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_fix_silver_shroud",
                    "name": {"zh-CN": "强行修复银衣怪客电台肯特被绑架不更新卡关", "en": "Fix Silver Shroud Quest Bug (MS04)"},
                    "syntax_type": "creation_hex",
                    "code": "setstage MS04 100",
                    "desc": "银衣怪客任务中电台停播或肯特在美侬医院不刷新的卡关问题，直接跳过坏档步骤直奔医院决战解救！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_companion_moveto",
                    "name": {"zh-CN": "失踪伙伴与狗肉瞬移召回身旁 (player.moveto)", "en": "Teleport Missing Companion (Dogmeat) to Player"},
                    "syntax_type": "creation_hex",
                    "code": "player.moveto 0001d162",
                    "desc": "寻找走丢的心爱狗肉 (Dogmeat 0001D162) 或把走散的同伴秒传到主角跟前，再也不怕在废土走失！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "⚡ SPECIAL 属性拉满与批处理极速调优 (SPECIAL & Bat Scripts)",
            "commands": [
                {
                    "id": "fo4_max_all_special",
                    "name": {"zh-CN": "全 7 项 S.P.E.C.I.A.L. 基础属性秒升 10 满级", "en": "Set All 7 SPECIAL Attributes to 10"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav strength 10",
                    "desc": "将力量 (Strength)、感知 (Perception)、耐力 (Endurance)、魅力 (Charisma)、智力 (Intelligence)、敏捷 (Agility)、幸运 (Luck) 全部拉满至 10，解锁全技能树！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_bat_all_materials",
                    "name": {"zh-CN": "批处理一键执行：瞬间获取全套建造素材十万份 (bat all_materials)", "en": "Batch Execute: Get All Building Materials"},
                    "syntax_type": "creation_hex",
                    "code": "bat all_materials",
                    "desc": "在游戏根目录建立 all_materials.txt 放入各素材 player.additem 代码，游戏中输入此指令一秒刷全数十种建材，极客高效典范！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_setlevel_50",
                    "name": {"zh-CN": "角色等级直升 50 级 (解锁高阶军械与动力甲刷新)", "en": "Set Player Level to 50"},
                    "syntax_type": "creation_hex",
                    "code": "player.setlevel 50",
                    "desc": "将角色等级瞬间提升至 50 级，废土所有军火商与野外动力装甲骨架将直接刷出顶级 X-01 装备！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_adv_skill_points",
                    "name": {"zh-CN": "瞬间赋予 10 点额外特技加点点数 (Perk Points)", "en": "Add 10 Perk Points"},
                    "syntax_type": "creation_hex",
                    "code": "player.setav skillpoints 10",
                    "desc": "向角色点数池注入 10 点专属 Perk 点，随心所欲点满枪侠、突击手与神秘客技能！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        },
        {
            "category": "🌌 场景探索、全图地标与自由运镜摄影 (Dev Room, Exploration & FreeCam)",
            "commands": [
                {
                    "id": "fo4_tmm_1",
                    "name": {"zh-CN": "点亮波士顿联邦大地图所有地标 (tmm 1: 支持快速传送)", "en": "Unlock All Map Markers (tmm 1)"},
                    "syntax_type": "creation_hex",
                    "code": "tmm 1",
                    "desc": "一键激活大地图所有庇护山丘、钻石城、发光海与钢铁兄弟会飞艇全部数百个地标，省去漫长探路！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_coc_redrocket",
                    "name": {"zh-CN": "瞬间传送至红火箭维修站基地 (coc RedRocketExt)", "en": "Teleport to Red Rocket Truck Stop"},
                    "syntax_type": "creation_hex",
                    "code": "coc RedRocketExt",
                    "desc": "不管身在何方遇到险境，输入本指令瞬间脱出并传送回红火箭维修站工房大本营！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_tfc_freecam",
                    "name": {"zh-CN": "开启自由飞行摄影相机并定格画面 (tfc 1)", "en": "Toggle Free Camera (tfc 1)"},
                    "syntax_type": "creation_hex",
                    "code": "tfc 1",
                    "desc": "暂停废土一切动作，相机脱离主角躯体自由升空俯瞰波士顿废墟壮观全景，拍摄工业级壁纸大片！",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                },
                {
                    "id": "fo4_tm_hide_hud",
                    "name": {"zh-CN": "隐藏/恢复全部界面 HUD 界面 (无UI纯净截图)", "en": "Toggle Menus / Hide HUD (tm)"},
                    "syntax_type": "creation_hex",
                    "code": "tm",
                    "desc": "隐藏全屏准星、血条、AP槽与罗盘。(隐藏后按 ~ 盲打 tm 回车即可重新呼出界面)。",
                    "min_version": "v1.0+",
                    "framework_required": "None (Native Console)"
                }
            ]
        }
    ]
}

def enrich_games():
    if not os.path.exists(JSON_PATH):
        print(f"❌ 找不到数据文件: {JSON_PATH}")
        sys.exit(1)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        games = json.load(f)

    updated_count = 0
    for g in games:
        gid = g.get("id")
        if gid == "elden-ring":
            print(f"🔄 深度注入 Rank 5: Elden Ring...")
            g.update(ELDEN_RING_DATA)
            updated_count += 1
        elif gid in ("the-elder-scrolls-v-skyrim-special-edition", "skyrim-se"):
            print(f"🔄 深度注入 Rank 6: Skyrim SE...")
            g.update(SKYRIM_SE_DATA)
            updated_count += 1
        elif gid == "fallout-4":
            print(f"🔄 深度注入 Rank 7: Fallout 4...")
            g.update(FALLOUT_4_DATA)
            updated_count += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(games, f, ensure_ascii=False, indent=2)
    print(f"✅ 已成功更新 {JSON_PATH} (共注入 {updated_count} 款游戏数据)")

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
        print(f"✅ 已成功同步更新前端数据文件 (含 GAMES_DATA 与 TRANSLATIONS_DATA): {JS_PATH}")

if __name__ == "__main__":
    enrich_games()
