#!/usr/bin/env python3
"""
generate_games_data.py
Bootstrap for the master data (src/data/games_top100.json): the 100 games with
titles in 8 languages (EN, ZH-CN, ZH-TW, JA, KO, RU, DE, ES) and base metadata.

Only for starting from nothing: if the master data already exists, it stops
without writing (writing it would replace every game, including the radar fields
from steam_patch_monitor.py and the trainer fields from fling_trainer_sync.py).
It does not write public/data.js.

Ranks 11-100 get no placeholder content: no made-up mods, commands or trainer
hotkeys (trainer data comes from fling_trainer_sync.py).
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "src/data")
TARGET_PATH = os.path.join(OUTPUT_DIR, "games_top100.json")

if os.path.exists(TARGET_PATH):
    sys.exit(f"❌ {TARGET_PATH} already exists; this bootstrap would replace every game "
             f"(radar and trainer fields included). Nothing written.")

# Definition of the Top 100 Games with deep metadata
TOP_100_GAMES = [
    {
        "id": "cyberpunk-2077",
        "rank": 1,
        "title": "Cyberpunk 2077",
        "titles": {
            "en": "Cyberpunk 2077", "zh-CN": "赛博朋克 2077", "zh-TW": "電馭叛客 2077",
            "ja": "サイバーパンク2077", "ko": "사이버펑크 2077", "ru": "Cyberpunk 2077",
            "de": "Cyberpunk 2077", "es": "Cyberpunk 2077"
        },
        "developer": "CD PROJEKT RED",
        "releaseYear": 2020,
        "genre": "Open World Action RPG",
        "steamRating": "92% Very Positive",
        "hasConsole": True,
        "consoleShortcut": "~ (CET Overlay / Tilde)",
        "consoleEnableGuide": {
            "zh-CN": "安装 Cyber Engine Tweaks (CET) 核心插件，放入 bin\\x64\\plugins 文件夹。启动游戏按 ~ 键即可唤出控制台。",
            "en": "Install Cyber Engine Tweaks (CET) into bin\\x64\\plugins. Press ~ (Tilde) in-game to open the console.",
            "zh-TW": "安裝 Cyber Engine Tweaks (CET) 插件，放入 bin\\x64\\plugins 目錄。遊戲中按 ~ 鍵喚出主控台。",
            "ja": "Cyber Engine Tweaks (CET) を bin\\x64\\plugins に配置。ゲーム内で ~ キーを押してコンソールを起動。",
            "ko": "Cyber Engine Tweaks (CET) 플러그인을 bin\\x64\\plugins 폴더에 설치 후 게임 내 ~ 키로 콘솔 활성화.",
            "ru": "Установите мод Cyber Engine Tweaks (CET) в папку bin\\x64\\plugins. В игре нажмите ~ для открытия консоли.",
            "de": "Cyber Engine Tweaks (CET) in bin\\x64\\plugins kopieren. Im Spiel Taste ~ drücken.",
            "es": "Instala Cyber Engine Tweaks (CET) en bin\\x64\\plugins. Presiona ~ en el juego para abrir la consola."
        },
        "popularCommands": [
            {"name": {"zh-CN": "增加金钱 (100万)", "en": "Add Money (1,000,000)"}, "command": "Game.AddToInventory(\"Items.money\", 1000000)", "desc": "直接增加 1,000,000 欧元现金",
            "source": "https://wiki.redmodding.org/cyber-engine-tweaks/console/console/how-do-i"},
            {"name": {"zh-CN": "提升等级至满级 (60级)", "en": "Set Max Level (60)"}, "command": "Game.SetLevel(\"Level\", 60)", "desc": "将角色人物等级直接拉满",
            "source": "https://wiki.redmodding.org/cyber-engine-tweaks/console/console/how-do-i"},
            {"name": {"zh-CN": "声望直接拉满 (50级)", "en": "Max Street Cred (50)"}, "command": "Game.SetLevel(\"StreetCred\", 50)", "desc": "解锁夜之城对应等级的中间人委托与义体医生商品购买权限",
            "source": "https://wiki.redmodding.org/cyber-engine-tweaks/console/console/how-do-i"},
            {"name": {"zh-CN": "增加 50 点专精点数", "en": "Add Perk Points"}, "command": "PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()):AddDevelopmentPoints(50, gamedataDevelopmentPointType.Primary)", "desc": "增加 50 点可用于解锁天赋树技能的专精点数（Perk Points）",
            "source": "https://wiki.redmodding.org/cyber-engine-tweaks/console/console/how-do-i"},
            {"name": {"zh-CN": "添加太刀【觉】", "en": "Add Satori Katana"}, "command": "Game.AddToInventory(\"Items.Preset_Katana_Saburo\", 1)", "desc": "荒坂三郎的佩剑，可向远处敌人跃进攻击并发动居合斩造成流血效果",
            "source": "https://wiki.redmodding.org/cyberpunk-2077-modding/for-mod-creators/references-lists-and-overviews/cheat-sheet-tweak-ids/weapons/iconic-effects-by-weapon"},
            {"name": {"zh-CN": "添加强尼·银手同款手枪【马洛里安3516】", "en": "Add Malorian Arms 3516"}, "command": "Game.AddToInventory(\"Items.Preset_Silverhand_3516\", 1)", "desc": "强尼·银手专属手枪，快速近战攻击可点燃敌人，但会消耗枪内剩余全部子弹",
            "source": "https://cyberpunk.fandom.com/wiki/Malorian_Arms_3516_(2077)"}
        ],
        "hasMods": True,
        "modInstallPath": "Cyberpunk 2077\\archive\\pc\\mod",
        "mustHaveMods": [
            {
                "name": "Cyber Engine Tweaks",
                "category": "Core Framework",
                "desc": "提供 Mod 运行环境与游戏内控制台",
                "url": "https://www.nexusmods.com/cyberpunk2077/mods/107"
            },
            {
                "name": "redscript",
                "category": "Core Framework",
                "desc": "脚本扩展运行环境",
                "url": "https://www.nexusmods.com/cyberpunk2077/mods/1511"
            },
            {
                "name": "Native Settings UI",
                "category": "QoL",
                "desc": "在游戏设置菜单里直接调节MOD参数",
                "url": "https://www.nexusmods.com/cyberpunk2077/mods/3518"
            },
            {
                "name": "Let There Be Flight",
                "category": "Gameplay",
                "desc": "载具飞行MOD，在夜之城空中驾驶跑车",
                "url": "https://www.nexusmods.com/cyberpunk2077/mods/5208"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health (无限生命)"},
            {"key": "Num 2", "action": "Infinite Stamina (无限耐力)"},
            {"key": "Num 3", "action": "Infinite Ammo (无限子弹)"},
            {"key": "Num 0", "action": "One Hit Kill (一击必杀)"}
        ]
    },
    {
        "id": "black-myth-wukong",
        "rank": 2,
        "title": "Black Myth: Wukong",
        "titles": {
            "en": "Black Myth: Wukong", "zh-CN": "黑神话：悟空", "zh-TW": "黑神話：悟空",
            "ja": "黒神話：悟空", "ko": "검은 신화: 오공", "ru": "Black Myth: Wukong",
            "de": "Black Myth: Wukong", "es": "Black Myth: Wukong"
        },
        "developer": "Game Science (游戏科学)",
        "releaseYear": 2024,
        "genre": "Action RPG / Soulslike",
        "steamRating": "96% Overwhelmingly Positive",
        "hasConsole": False,
        "consoleShortcut": "无官方控制台 (需使用 UE4SS 框架)",
        "consoleEnableGuide": {
            "zh-CN": "游戏原生未开启输入控制台，可通过安装 UE4SS 虚幻引擎扩展工具按 F10 开启虚幻开发者控制台，或直接搭配修改器使用。",
            "en": "Native console is disabled by default. Install UE4SS into b1\\Binaries\\Win64 and press F10 for Unreal Dev Console.",
            "zh-TW": "原生未開啟控制台，安裝 UE4SS 插件後按 F10 開啟虛幻開發者調試視窗。",
            "ja": "ネイティブコンソールは無効。UE4SSを導入してF10キーでUnreal開発コンソールを起動可能。",
            "ko": "기본 콘솔 비활성화 상태. UE4SS 플러그인 설치 후 F10 키로 언리얼 콘솔 구동 가능.",
            "ru": "Консоль отключена разработчиками. Установите UE4SS для вызова консоли Unreal по F10.",
            "de": "Native Konsole deaktiviert. UE4SS installieren und F10 drücken für Entwickler-Konsole.",
            "es": "Consola nativa desactivada. Instala UE4SS en b1\\Binaries\\Win64 y presiona F10."
        },
        "popularCommands": [],
        "hasMods": True,
        "modInstallPath": "b1\\Content\\Paks\\~mods",
        "mustHaveMods": [],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health (无限生命)"},
            {"key": "Num 2", "action": "Infinite Mana (无限法力/法宝)"},
            {"key": "Num 3", "action": "Infinite Stamina (无限气力)"},
            {"key": "Num 4", "action": "Max Stick Gauge (无限棍势满豆)"},
            {"key": "Num 7", "action": "Infinite Will / Spark (无限灵蕴/灵光点)"}
        ]
    },
    {
        "id": "witcher-3",
        "rank": 3,
        "title": "The Witcher 3: Wild Hunt",
        "titles": {
            "en": "The Witcher 3: Wild Hunt", "zh-CN": "巫师 3：狂猎", "zh-TW": "巫師 3：狂獵",
            "ja": "ウィッチャー3 ワイルドハント", "ko": "더 위쳐 3: 와일드 헌트", "ru": "Ведьмак 3: Дикая Охота",
            "de": "The Witcher 3: Wild Hunt", "es": "The Witcher 3: Wild Hunt"
        },
        "developer": "CD PROJEKT RED",
        "releaseYear": 2015,
        "genre": "Open World RPG",
        "steamRating": "97% Overwhelmingly Positive",
        "hasConsole": True,
        "consoleShortcut": "~ 或 F2 键",
        "consoleEnableGuide": {
            "zh-CN": "找到游戏安装目录 The Witcher 3\\bin\\config\\base\\general.ini，在末尾新增一行 DBGConsoleOn=true，进游戏按 ~ 即可呼出。",
            "en": "Edit bin\\config\\base\\general.ini in Witcher 3 folder, add DBGConsoleOn=true at the bottom. Press ~ in-game.",
            "zh-TW": "打開 bin\\config\\base\\general.ini，新增一行 DBGConsoleOn=true，存檔後按 ~ 鍵即可開關。",
            "ja": "general.ini の末尾に DBGConsoleOn=true を追加保存し、ゲーム内で ~ を押す。",
            "ko": "general.ini 파일 하단에 DBGConsoleOn=true 추가 후 ~ 키로 활성화.",
            "ru": "В файле bin\\config\\base\\general.ini добавьте DBGConsoleOn=true. Нажмите ~ в игре.",
            "de": "In general.ini die Zeile DBGConsoleOn=true anhängen. Im Spiel ~ drücken.",
            "es": "Añade DBGConsoleOn=true al final de general.ini. Presiona ~ en el juego."
        },
        "popularCommands": [
            {
                "name": {
                    "zh-CN": "上帝模式 (God Mode)",
                    "en": "God Mode"
                },
                "command": "god",
                "desc": "开启后杰洛特免疫伤害，生命值与昆恩法印锁定，不会受到物理与法术伤害。",
                "source": "https://commands.gg/witcher3/god"
            },
            {
                "name": {
                    "zh-CN": "增加金币 (100,000 克朗)",
                    "en": "Add 100,000 Crowns"
                },
                "command": "addmoney(100000)",
                "desc": "增加 100,000 克朗，可用于购买宗师级装备材料或陶森特庄园升级等花费较高的内容。",
                "source": "https://commands.gg/witcher3/addmoney"
            },
            {
                "name": {
                    "zh-CN": "开始一局昆特牌对局",
                    "en": "Add All Gwent Cards"
                },
                "command": "secretgwint",
                "desc": "立即开始一局与 AI 对战的昆特牌比赛；不会直接把全部卡牌加入牌库。",
                "source": "https://commands.gg/witcher3/secretgwint"
            },
            {
                "name": {
                    "zh-CN": "直接获得湖中之剑 (血与酒成长型银剑)",
                    "en": "Add Aerondight Sword"
                },
                "command": "additem('Aerondight EP2')",
                "desc": "获得会随战斗表现持续强化基础伤害的银剑（Aerondight）。",
                "source": "https://witcher.fandom.com/wiki/Aerondight"
            },
            {
                "name": {
                    "zh-CN": "大地图点亮全部快速旅行路标",
                    "en": "Show All Fast Travel"
                },
                "command": "ShowAllFT(1)",
                "desc": "瞬间解锁白果园、威伦、诺维格瑞、群岛与陶森特的全部快速旅行路标。",
                "source": "https://commands.gg/witcher3/showallft"
            },
            {
                "name": {
                    "zh-CN": "获取大超同款宗师级遗忘狼防具 (次世代版 / 完全版特供)",
                    "en": "Add Netflix Wolven Armor"
                },
                "command": "additem('Netflix Armor 2')",
                "desc": "直接注入亨利·卡维尔网飞剧版同款纯黑宗师级遗弃狼战甲。",
                "source": "https://witcher.fandom.com/wiki/Grandmaster_forgotten_Wolven_armor"
            }
        ],
        "hasMods": True,
        "modInstallPath": "The Witcher 3\\Mods",
        "mustHaveMods": [
            {
                "name": "The Witcher 3 HD Reworked Project NextGen Edition",
                "category": "Graphics",
                "desc": "4K 材质画质增强重制包。",
                "url": "https://www.nexusmods.com/witcher3/mods/9963"
            },
            {
                "name": "Fast Travel From Anywhere",
                "category": "QoL",
                "desc": "无需跑回路标，随时随地开启世界地图传送",
                "url": "https://www.nexusmods.com/witcher3/mods/7157"
            },
            {
                "name": "No Fall Damage (CLASSIC)",
                "category": "QoL",
                "desc": "移除杰洛特哪怕跳一小格也摔死的设定",
                "url": "https://www.nexusmods.com/witcher3/mods/352"
            },
            {
                "name": "Over 9000 - Weight limit mod",
                "category": "QoL",
                "desc": "背包负重上限提升至 9000，狂捡垃圾不超重",
                "url": "https://www.nexusmods.com/witcher3/mods/3"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite Stamina"},
            {"key": "Num 3", "action": "Infinite Adrenaline"},
            {"key": "Num 5", "action": "Zero Toxicity (无毒性)"}
        ]
    },
    {
        "id": "baldurs-gate-3",
        "rank": 4,
        "title": "Baldur's Gate 3",
        "titles": {
            "en": "Baldur's Gate 3", "zh-CN": "博德之门 3", "zh-TW": "柏德之門 3",
            "ja": "バルダーズ・ゲート3", "ko": "발더스 게이트 3", "ru": "Baldur's Gate 3",
            "de": "Baldur's Gate 3", "es": "Baldur's Gate 3"
        },
        "developer": "Larian Studios",
        "releaseYear": 2023,
        "genre": "CRPG / Turn-Based Strategy",
        "steamRating": "96% Overwhelmingly Positive",
        "hasConsole": True,
        "consoleShortcut": "通过 BG3 Script Extender 控制台",
        "consoleEnableGuide": {
            "zh-CN": "下载 BG3 Script Extender 放入 bin 目录，在 ScriptExtenderSettings.json 开启 CreateConsole: true 即可呼出全功能命令行。",
            "en": "Download BG3 Script Extender into bin folder, set CreateConsole: true in config.",
            "zh-TW": "安裝 BG3 Script Extender 後在設定檔開啟 CreateConsole。",
            "ja": "BG3 Script Extender を bin フォルダに配置し、CreateConsole を有効化。",
            "ko": "BG3 Script Extender 설치 후 콘솔 모드 활성화.",
            "ru": "Установите BG3 Script Extender в папку bin и включите CreateConsole.",
            "de": "BG3 Script Extender in den bin-Ordner einfügen und CreateConsole aktivieren.",
            "es": "Instala BG3 Script Extender en bin y activa CreateConsole: true."
        },
        "popularCommands": [
            {
                "name": {
                    "zh-CN": "增加金币 (100,000 金币)",
                    "en": "Add 100,000 Gold"
                },
                "command": "Osi.AddGold(GetHostCharacter(), 100000)",
                "desc": "向背包增加 10 万金币，可用于购买装备和物资。",
                "source": "https://docs.baldursgate3.game/index.php?title=AddGold"
            },
            {
                "name": {
                    "zh-CN": "获得夺心魔寄生虫标本 x30",
                    "en": "Add 30 Illithid Parasites"
                },
                "command": "Osi.TemplateAddTo(\"1ec327be-3b7f-4502-9586-860e057e09ae\", GetHostCharacter(), 30)",
                "desc": "一次性获得 30 个夺心魔寄生虫标本，可用于解锁主角与队友的灵能异能。",
                "source": "https://bg3.wiki/wiki/Mind_Flayer_Parasite_Specimen"
            },
            {
                "name": {
                    "zh-CN": "获得博德安的巨人杀手巨剑 (传奇双手巨剑)",
                    "en": "Add Balduran's Giantslayer"
                },
                "command": "Osi.TemplateAddTo(\"7219fca3-5f41-43a0-8253-f4c09d8b6308\", GetHostCharacter(), 1)",
                "desc": "获得攻击伤害额外附加两倍力量调整值、并带有「巨人体型」技能的双手巨剑。",
                "source": "https://bg3.wiki/wiki/Balduran%27s_Giantslayer"
            },
            {
                "name": {
                    "zh-CN": "获得地狱火全套胸甲 (21AC全职业免熟练)",
                    "en": "Add Helldusk Armour"
                },
                "command": "Osi.TemplateAddTo(\"7ae705fd-1cfd-4482-a584-d2e68f9c1262\", GetHostCharacter(), 1)",
                "desc": "获得拉斐尔掉落的重甲，AC 21，任何职业穿戴都视为熟练，并对火焰伤害有抗性。",
                "source": "https://bg3.wiki/wiki/Helldusk_Armour"
            },
            {
                "name": {
                    "zh-CN": "赋予常驻急速术 (HASTE)",
                    "en": "Permanent Haste Buff"
                },
                "command": "Osi.ApplyStatus(GetHostCharacter(), \"HASTE\", -1)",
                "desc": "持续施加急速状态：每回合多一次动作、移动速度提升，且因手动施加不会到期陷入疲乏状态。",
                "source": "https://docs.baldursgate3.game/index.php?title=ApplyStatus"
            }
        ],
        "hasMods": True,
        "modInstallPath": "%LOCALAPPDATA%\\Larian Studios\\Baldur's Gate 3\\Mods",
        "mustHaveMods": [
            {
                "name": "Party Limit Begone",
                "category": "Gameplay",
                "desc": "将队伍人数上限提升至 16，可同时带上所有可招募的同伴",
                "url": "https://www.nexusmods.com/baldursgate3/mods/327"
            },
            {
                "name": "5e Spells",
                "category": "Content",
                "desc": "补充游戏未收录的官方桌面跑团法术",
                "url": "https://www.nexusmods.com/baldursgate3/mods/125"
            },
            {
                "name": "Bags Bags Bags",
                "category": "QoL",
                "desc": "药剂、卷轴、箭矢等物品自动归类整理背包",
                "url": "https://www.nexusmods.com/baldursgate3/mods/880"
            },
            {
                "name": "Native Camera Tweaks",
                "category": "Camera",
                "desc": "支持将镜头拉至平视的越肩第三人称视角",
                "url": "https://www.nexusmods.com/baldursgate3/mods/945"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite Spell Slots"},
            {"key": "Num 3", "action": "Infinite Action Points"}
        ]
    },
    {
        "id": "elden-ring",
        "rank": 5,
        "title": "Elden Ring",
        "titles": {
            "en": "Elden Ring", "zh-CN": "艾尔登法环", "zh-TW": "艾爾登法環",
            "ja": "エルデンリング", "ko": "엘든 링", "ru": "Elden Ring",
            "de": "Elden Ring", "es": "Elden Ring"
        },
        "developer": "FromSoftware",
        "releaseYear": 2022,
        "genre": "Action RPG / Open World Soulslike",
        "steamRating": "93% Very Positive",
        "hasConsole": False,
        "consoleShortcut": "无官方控制台 (支持无缝联机MOD & 修改器)",
        "consoleEnableGuide": {
            "zh-CN": "宫崎英高魂系游戏无官方控制台。单人探索推荐使用 Seamless Co-op（无缝联机模组）或离线模式修改器。",
            "en": "No native developer console. Seamless Co-op or offline trainers recommended.",
            "zh-TW": "魂系作品無官方指令視窗，單機推薦搭配 Seamless Co-op 模組。",
            "ja": "公式コンソールなし。Seamless Co-op や Mod Engine 2 を推奨。",
            "ko": "공식 콘솔 미지원. Seamless Co-op 및 오프라인 모드 추천.",
            "ru": "Официальной консоли нет. Рекомендуется Seamless Co-op и Mod Engine 2.",
            "de": "Keine offizielle Konsole. Seamless Co-op und Offline-Trainer empfohlen.",
            "es": "No hay consola oficial. Se recomienda Seamless Co-op o entrenadores offline."
        },
        "popularCommands": [],
        "hasMods": True,
        "modInstallPath": "ELDEN RING\\Game\\mods (使用 Mod Engine 2)",
        "mustHaveMods": [
            {
                "name": "Elden Ring Seamless Co-op",
                "category": "Multiplayer",
                "desc": "与好友联机推进全程剧情、骑乘灵马，且不会因死亡被遣返回单人世界",
                "url": "https://github.com/yuiamoroll/EldenRingSeamlessCoopRelease"
            },
            {
                "name": "Elden Ring Ultrawide Fix (TechieW) + Elden Ring Automatic FPS Unlocker (Apollo_2040)",
                "category": "Performance",
                "desc": "突破 60 帧锁定，支持 21:9 带鱼屏原生渲染",
                "url": "https://www.nexusmods.com/eldenring/mods/7870"
            },
            {
                "name": "Pause the game",
                "category": "QoL",
                "desc": "按 P 键暂停游戏，适合中途离开时使用",
                "url": "https://www.nexusmods.com/eldenring/mods/43"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite FP"},
            {"key": "Num 3", "action": "Infinite Stamina"},
            {"key": "Num 4", "action": "100% Drop Rate (百分百掉宝)"},
            {"key": "Num 0", "action": "Infinite Runes (无限卢恩)"}
        ]
    },
    {
        "id": "skyrim-se",
        "rank": 6,
        "title": "The Elder Scrolls V: Skyrim Special Edition",
        "titles": {
            "en": "The Elder Scrolls V: Skyrim SE", "zh-CN": "上古卷轴 5：天际重制版", "zh-TW": "上古卷軸 5：無界天際 特別版",
            "ja": "The Elder Scrolls V: Skyrim SE", "ko": "엘더스크롤 5: 스카이림 SE", "ru": "The Elder Scrolls V: Skyrim SE",
            "de": "The Elder Scrolls V: Skyrim SE", "es": "The Elder Scrolls V: Skyrim SE"
        },
        "developer": "Bethesda Game Studios",
        "releaseYear": 2016,
        "genre": "Open World RPG",
        "steamRating": "94% Very Positive",
        "hasConsole": True,
        "consoleShortcut": "~ (Tilde)",
        "consoleEnableGuide": {
            "zh-CN": "游戏原生支持！在游戏任意界面按键盘左上角 ~ 键即可打开控制台输入指令。",
            "en": "Native console enabled by default! Just press ~ (Tilde) anytime in-game.",
            "zh-TW": "原生支援，鍵盤按 ~ 即可呼出。",
            "ja": "キーボードの ~ (チルダ) キーを押すだけで即座に開きます。",
            "ko": "게임 중 언제든 ~ 키를 누르면 콘솔창이 활성화됩니다.",
            "ru": "Нажмите клавишу ~ (тильда) в игре.",
            "de": "Einfach die Taste ~ im Spiel drücken.",
            "es": "Presiona ~ (o la tecla bajo ESC) durante el juego."
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
        "modInstallPath": "Skyrim Special Edition\\Data",
        "mustHaveMods": [
            {
                "name": "Skyrim Script Extender (SKSE64)",
                "category": "Core Framework",
                "desc": "绝大部分现代脚本MOD前置",
                "url": "https://www.nexusmods.com/skyrimspecialedition/mods/30379"
            },
            {
                "name": "SkyUI",
                "category": "UI Overhaul",
                "desc": "优化原版界面，改善 PC 端的鼠标键盘操作体验。",
                "url": "https://www.nexusmods.com/skyrimspecialedition/mods/12604"
            },
            {
                "name": "Unofficial Skyrim Special Edition Patch - USSEP",
                "category": "Bug Fixes",
                "desc": "非官方的综合性原版 BUG 修复补丁。",
                "url": "https://www.nexusmods.com/skyrimspecialedition/mods/266"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite Magicka"},
            {"key": "Num 3", "action": "Infinite Carry Weight"}
        ]
    },
    {
        "id": "fallout-4",
        "rank": 7,
        "title": "Fallout 4",
        "titles": {
            "en": "Fallout 4", "zh-CN": "辐射 4", "zh-TW": "異塵餘生 4",
            "ja": "フォールアウト4", "ko": "폴아웃 4", "ru": "Fallout 4",
            "de": "Fallout 4", "es": "Fallout 4"
        },
        "developer": "Bethesda Game Studios",
        "releaseYear": 2015,
        "genre": "Post-Apocalyptic Open World RPG",
        "steamRating": "83% Very Positive",
        "hasConsole": True,
        "consoleShortcut": "~ (Tilde)",
        "consoleEnableGuide": {
            "zh-CN": "游戏原生支持！在游戏任意界面按键盘左上角 ~ 键即可打开控制台。",
            "en": "Native console enabled by default! Just press ~ (Tilde) anytime in-game.",
            "zh-TW": "原生支援，鍵盤按 ~ 即可呼出。",
            "ja": "ゲーム中に ~ キーを押すだけでコンソールが起動。",
            "ko": "게임 내에서 ~ 키를 눌러 콘솔 창을 활성화합니다.",
            "ru": "Нажмите ~ в игре.",
            "de": "Im Spiel Taste ~ drücken.",
            "es": "Presiona ~ en el juego."
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
        "modInstallPath": "Fallout 4\\Data",
        "mustHaveMods": [
            {
                "name": "Fallout 4 Script Extender (F4SE)",
                "category": "Core Framework",
                "desc": "辐射4模组核心引擎扩展",
                "url": "https://www.nexusmods.com/fallout4/mods/42147"
            },
            {
                "name": "Unofficial Fallout 4 Patch - UFO4P",
                "category": "Bug Fixes",
                "desc": "非官方的综合性 BUG 修复补丁，修复大量官方未解决的问题。",
                "url": "https://www.nexusmods.com/fallout4/mods/4598"
            },
            {
                "name": "Place Everywhere",
                "category": "Settlement Building",
                "desc": "聚落建房随处摆放，解除红字碰撞限制",
                "url": "https://www.nexusmods.com/fallout4/mods/9424"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite Action Points (AP)"},
            {"key": "Num 3", "action": "No Reload (免换弹)"}
        ]
    },
    {
        "id": "palworld",
        "rank": 8,
        "title": "Palworld",
        "titles": {
            "en": "Palworld", "zh-CN": "幻兽帕鲁", "zh-TW": "幻獸帕魯",
            "ja": "パルワールド", "ko": "팰월드", "ru": "Palworld",
            "de": "Palworld", "es": "Palworld"
        },
        "developer": "Pocketpair",
        "releaseYear": 2024,
        "genre": "Open World Survival Crafting",
        "steamRating": "93% Very Positive",
        "hasConsole": True,
        "consoleShortcut": "Enter 键 (聊天框输入管理员指令)",
        "consoleEnableGuide": {
            "zh-CN": "单人或联机服房主输入 /adminpassword 密码 获取管理员权限后，即可在聊天框直接输入 /teleport 等指令。",
            "en": "Enter /adminpassword <password> in chat window to gain admin rights, then use slash commands.",
            "zh-TW": "在聊天框輸入 /adminpassword 密碼 取得管理員權限。",
            "ja": "チャット欄で /adminpassword を入力して管理者コマンドを使用。",
            "ko": "채팅창에서 /adminpassword 로 관리자 권한 획득 후 명령어 사용.",
            "ru": "Введите /adminpassword <пароль> в чате.",
            "de": "Im Chat /adminpassword eingeben für Admin-Befehle.",
            "es": "Introduce /adminpassword en el chat para habilitar comandos de administrador."
        },
        "popularCommands": [],
        "hasMods": True,
        "modInstallPath": "Palworld\\Pal\\Binaries\\Win64\\Mods (基于 UE4SS)",
        "mustHaveMods": [
            {
                "name": "Carry Weight Increase",
                "category": "QoL",
                "desc": "提高帕鲁的负重上限，减少因超重导致的多次往返运输",
                "url": "https://www.nexusmods.com/palworld/mods/11"
            },
            {
                "name": "Pal IVs",
                "category": "QoL",
                "desc": "查看帕鲁的个体值、被动词条与隐藏属性"
            },
            {
                "name": "Map Unlocker",
                "category": "Exploration",
                "desc": "解锁全地图的战争迷雾，无需实地探索即可查看地图",
                "url": "https://www.nexusmods.com/palworld/mods/16"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite Stamina"},
            {"key": "Num 3", "action": "100% Catch Rate (百分百捕捉率)"},
            {"key": "Num 4", "action": "Fast Egg Hatching (光速孵蛋)"}
        ]
    },
    {
        "id": "starfield",
        "rank": 9,
        "title": "Starfield",
        "titles": {
            "en": "Starfield", "zh-CN": "星空", "zh-TW": "星空",
            "ja": "スターフィールド", "ko": "스타필드", "ru": "Starfield",
            "de": "Starfield", "es": "Starfield"
        },
        "developer": "Bethesda Game Studios",
        "releaseYear": 2023,
        "genre": "Space Action RPG",
        "steamRating": "61% Mixed",
        "hasConsole": True,
        "consoleShortcut": "~ (Tilde)",
        "consoleEnableGuide": {
            "zh-CN": "游戏原生支持！在游戏任意界面按键盘左上角 ~ 键即可开启控制台（注意：使用控制台会锁成就，建议装成就不锁MOD）。",
            "en": "Press ~ in-game. Console disables achievements; install Baka Achievement Enabler mod to re-enable them.",
            "zh-TW": "按 ~ 開啟控制台。建議安裝成就解鎖模組避免停用成就。",
            "ja": "~ キーで起動。実績が無効になるため実績有効化MOD推奨。",
            "ko": "~ 키로 콘솔 활성화. 도전과제 활성화 모드 사용 권장.",
            "ru": "Нажмите ~ в игре.",
            "de": "Taste ~ im Spiel drücken.",
            "es": "Presiona ~ en el juego."
        },
        "popularCommands": [
            "player.additem 0000000F 1000000",
            "player.additem 0000000A 100",
            "tgm",
            "player.setav carryweight 9999",
            "tcl"
        ],
        "hasMods": True,
        "modInstallPath": "Starfield\\Data",
        "mustHaveMods": [
            {
                "name": "Starfield Script Extender (SFSE)",
                "category": "Core Framework",
                "desc": "星空核心脚本前置",
                "url": "https://www.nexusmods.com/starfield/mods/106"
            },
            {
                "name": "StarUI Inventory",
                "category": "UI Overhaul",
                "desc": "优化物品栏界面显示，更清晰地展示物品的 DPS、价值等信息。",
                "url": "https://www.nexusmods.com/starfield/mods/773"
            },
            {
                "name": "Baka Achievement Enabler (SFSE)",
                "category": "Fix",
                "desc": "使用控制台命令或安装 Mod 后，仍可正常获得 Steam 成就。",
                "url": "https://www.nexusmods.com/starfield/mods/658"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite Oxygen"},
            {"key": "Num 3", "action": "Infinite Spaceship Hull/Shield"}
        ]
    },
    {
        "id": "gta-v",
        "rank": 10,
        "title": "Grand Theft Auto V",
        "titles": {
            "en": "Grand Theft Auto V", "zh-CN": "侠盗猎车手 5", "zh-TW": "俠盜獵車手 5",
            "ja": "グランド・セフト・オートV", "ko": "그랜드 테프트 오토 V", "ru": "Grand Theft Auto V",
            "de": "Grand Theft Auto V", "es": "Grand Theft Auto V"
        },
        "developer": "Rockstar Games",
        "releaseYear": 2013,
        "genre": "Open World Action-Adventure",
        "steamRating": "91% Very Positive",
        "hasConsole": True,
        "consoleShortcut": "~ (或直接按手机拨号代码)",
        "consoleEnableGuide": {
            "zh-CN": "单人故事模式下按键盘 ~ 键，或掏出主角手机拨打作弊号码即可生效！",
            "en": "Press ~ in single player story mode, or dial cheat numbers on your in-game cell phone.",
            "zh-TW": "單人戰役按 ~ 或撥打手機作弊號碼。",
            "ja": "ストーリーモードで ~ キーを押すか、携帯電話でチート番号をダイヤル。",
            "ko": "스토리 모드에서 ~ 키 또는 휴대폰 치트 번호 입력.",
            "ru": "Нажмите ~ в одиночном режиме или наберите номер в телефоне.",
            "de": "Im Story-Modus ~ drücken oder Cheat-Nummer im Handy wählen.",
            "es": "Presiona ~ en el modo historia o marca el número en el teléfono."
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
        "modInstallPath": "Grand Theft Auto V (使用 OpenIV & ScriptHookV)",
        "mustHaveMods": [
            {
                "name": "Script Hook V",
                "category": "Core Framework",
                "desc": "附带 Native Trainer 离线菜单，可用于刷出载具等基础功能。",
                "url": "https://www.dev-c.com/gtav/scripthookv/"
            },
            {
                "name": "NaturalVision Evolved",
                "category": "Graphics",
                "desc": "调整天气、光照与夜景等画面效果。",
                "url": "https://www.razedmods.com/gta-v"
            }
        ],
        "hasTrainer": True,
        "trainerHotkeys": [
            {"key": "F4", "action": "Open Native Trainer in-game"},
            {"key": "Num 1", "action": "Infinite Health"},
            {"key": "Num 2", "action": "Infinite Ammo"}
        ]
    }
]

# Generate remaining 90 games programmatically with rich template data to reach exactly 100 top games
REMAINING_GAMES_METADATA = [
    # 11 - 20
    ("rdr2", "Red Dead Redemption 2", "荒野大镖客：救赎 2", "Rockstar Games", 2018, "Open World Western RPG", "92% Very Positive", True, "游戏内设置->作弊菜单输入代码 (如 YOU FLOURISH BEFORE YOU DIE)", True, True),
    ("monster-hunter-world", "Monster Hunter: World", "怪物猎人：世界", "Capcom", 2018, "Action RPG", "88% Very Positive", False, "无官方控制台，使用 Stracker's Loader 装 MOD 或修改器", True, True),
    ("subnautica", "Subnautica", "深海迷航", "Unknown Worlds", 2018, "Underwater Survival", "96% Overwhelmingly Positive", True, "按 F3 取消勾选 Disable Console，再按 Enter 或 ~ 输入 item / oxygen", True, True),
    ("valheim", "Valheim", "英灵神殿", "Iron Gate", 2021, "Nordic Survival Crafting", "95% Overwhelmingly Positive", True, "Steam 启动项加 -console，进游戏按 F5 输入 devcommands", True, True),
    ("mount-and-blade-2", "Mount & Blade II: Bannerlord", "骑马与砍杀 2：霸主", "TaleWorlds", 2020, "Medieval Strategy Action RPG", "88% Very Positive", True, "按 Alt + ~ 呼出控制台输入 config.cheat_mode 1", True, True),
    ("stardew-valley", "Stardew Valley", "星露谷物语", "ConcernedApe", 2016, "Farming Sim RPG", "98% Overwhelmingly Positive", True, "使用 SMAPI 启动按控制台输入 player_additem [ID]", True, True),
    ("terraria", "Terraria", "泰拉瑞亚", "Re-Logic", 2011, "2D Sandbox Survival", "97% Overwhelmingly Positive", True, "单人使用 TShock 或 tModLoader 直接刷物品", True, True),
    ("hogwarts-legacy", "Hogwarts Legacy", "霍格沃茨之遗", "Avalanche Software", 2023, "Open World Wizard RPG", "91% Very Positive", False, "使用 UE4SS 开启控制台或搭配风灵月影修改器", True, True),
    ("sekiro", "Sekiro: Shadows Die Twice", "只狼：影逝二度", "FromSoftware", 2019, "Soulslike Action", "95% Overwhelmingly Positive", False, "无控制台，推荐使用 Sekiro Mod Engine 或修改器", True, True),
    ("dark-souls-3", "Dark Souls III", "黑暗之魂 3", "FromSoftware", 2016, "Action RPG Soulslike", "94% Very Positive", False, "搭配 Mod Engine 或 Cheat Engine CT 表刷取武器", True, True),
    
    # 21 - 30
    ("re4-remake", "Resident Evil 4 Remake", "生化危机 4 重制版", "Capcom", 2023, "Survival Horror", "97% Overwhelmingly Positive", False, "使用 REFramework (按 Insert 键呼出内置菜单修改器)", True, True),
    ("re-village", "Resident Evil Village", "生化危机 8：村庄", "Capcom", 2021, "Survival Horror", "95% Overwhelmingly Positive", False, "使用 REFramework 开启自由视角与无限子弹", True, True),
    ("dying-light", "Dying Light", "消逝的光芒", "Techland", 2015, "Zombie Action Parkour", "95% Overwhelmingly Positive", False, "解压 Data0.pak 修改属性或使用单文件修改器", True, True),
    ("dying-light-2", "Dying Light 2 Stay Human", "消逝的光芒 2", "Techland", 2022, "Action RPG Parkour", "79% Mostly Positive", True, "安装内置开发者菜单 (Developer Menu Mod) 按 ESC 打开", True, True),
    ("fallout-new-vegas", "Fallout: New Vegas", "辐射：新维加斯", "Obsidian Entertainment", 2010, "Post-Apocalyptic RPG", "96% Overwhelmingly Positive", True, "按 ~ 键输入 tgm / player.additem 0000000F 10000", True, True),
    ("rimworld", "RimWorld", "边缘世界", "Ludeon Studios", 2018, "Colony Sim Strategy", "98% Overwhelmingly Positive", True, "设置开启【开发者模式 (Development Mode)】，顶部直接刷小人与物资", True, True),
    ("project-zomboid", "Project Zomboid", "僵尸毁灭工程", "The Indie Stone", 2013, "Isometric Survival Horror", "94% Very Positive", True, "启动项加 -debug，进入游戏左侧多出一排官方内置上帝作弊图标", True, True),
    ("the-forest", "The Forest", "森林", "Endnight Games", 2018, "Survival Horror", "95% Overwhelmingly Positive", True, "主菜单直接盲打 developermodeon，按 F1 打开控制台输入 godmode on", True, True),
    ("sons-of-the-forest", "Sons of the Forest", "森林之子", "Endnight Games", 2024, "Survival Horror", "86% Very Positive", True, "主菜单盲打 cheatstick，进游戏按 F1 输入 godmode on / addallitems", True, True),
    ("satisfactory", "Satisfactory", "幸福工厂", "Coffee Stain Studios", 2024, "Automation Factory Building", "97% Overwhelmingly Positive", True, "按 Ctrl+Shift+L 激活，再按 ~ 打开控制台", True, True),
    
    # 31 - 40
    ("factorio", "Factorio", "异星工厂", "Wube Software", 2020, "Factory Simulation Strategy", "97% Overwhelmingly Positive", True, "按 ~ 键输入 /c game.player.cheat_mode=true 开启制造无消耗", True, True),
    ("cities-skylines", "Cities: Skylines", "城市：天际线", "Colossal Order", 2015, "City Builder Simulation", "93% Very Positive", True, "游戏内置自带官方无限金币、全里程碑解锁 MOD 开关", True, True),
    ("civ-6", "Sid Meier's Civilization VI", "文明 6", "Firaxis Games", 2016, "Turn-Based 4X Strategy", "86% Very Positive", True, "修改 AppOptions.txt 开启 EnableDebugMenu 1，按 ~ 打开调试台", True, True),
    ("crusader-kings-3", "Crusader Kings III", "十字军之王 3", "Paradox Development Studio", 2020, "Historical Grand Strategy", "92% Very Positive", True, "启动项加 -debug_mode，按 ~ 打开，一键添加金币、威望与特质", True, True),
    ("hearts-of-iron-4", "Hearts of Iron IV", "钢铁雄心 4", "Paradox Development Studio", 2016, "Grand Strategy Wargame", "92% Very Positive", True, "非铁人模式按 ~ 输入 research all / manpower 1000000", True, True),
    ("stellaris", "Stellaris", "群星", "Paradox Development Studio", 2016, "Sci-Fi 4X Strategy", "88% Very Positive", True, "非铁人按 ~ 输入 minerals 100000 / energy 100000 / alloys 100000", True, True),
    ("total-war-warhammer-3", "Total War: WARHAMMER III", "全面战争：战锤 3", "Creative Assembly", 2022, "Grand Strategy / RTS", "80% Very Positive", False, "通过创意工坊一键订阅 Mod Configuration Tool 与修改脚本", True, True),
    ("total-war-three-kingdoms", "Total War: Three Kingdoms", "全面战争：三国", "Creative Assembly", 2019, "Historical Strategy", "83% Very Positive", False, "创意工坊全量武将收集 MOD 与无限国库修改器", True, True),
    ("dragons-dogma-2", "Dragon's Dogma 2", "龙之信条 2", "Capcom", 2024, "Action RPG", "61% Mixed", False, "使用 REFramework 模组开启传送石无限购买与负重大修", True, True),
    ("armored-core-6", "Armored Core VI: Fires of Rubicon", "装甲核心 6：境界天火", "FromSoftware", 2023, "Mecha Action", "90% Very Positive", False, "Mod Engine 2 零件部件解锁与修改器", True, True),

    # 41 - 50
    ("ghost-of-tsushima", "Ghost of Tsushima DIRECTOR'S CUT", "对马岛之魂：导演剪辑版", "Sucker Punch / Nixxes", 2024, "Open World Samurai Action", "93% Very Positive", False, "支持画质去暗角 MOD 与单文件纯净修改器", True, True),
    ("god-of-war", "God of War", "战神 4", "Santa Monica Studio", 2022, "Action-Adventure", "96% Overwhelmingly Positive", False, "纯净修改器一键全技能解锁、无限斯巴达狂怒", True, True),
    ("spiderman-remastered", "Marvel's Spider-Man Remastered", "漫威蜘蛛侠：重制版", "Insomniac Games", 2022, "Superhero Open World", "96% Overwhelmingly Positive", False, "使用 SMPC Mod Tool 导入好莱坞蜘蛛侠制服模型", True, True),
    ("horizon-zero-dawn", "Horizon Zero Dawn", "地平线：零之曙光", "Guerrilla Games", 2020, "Post-Apocalyptic Action RPG", "87% Very Positive", False, "全技能点与无限资源修改器", True, True),
    ("days-gone", "Days Gone", "往日不再", "Bend Studio", 2021, "Zombie Open World", "92% Very Positive", False, "无限摩托车燃油、超大弹夹与暴走潮难度调节 MOD", True, True),
    ("death-stranding", "Death Stranding Director's Cut", "死亡搁浅：导演剪辑版", "Kojima Productions", 2022, "Open World Sci-Fi", "93% Very Positive", False, "修改器无限负重、外骨骼无限电量、无限开罗尔晶体", True, True),
    ("detroit-become-human", "Detroit: Become Human", "底特律：化身为人", "Quantic Dream", 2020, "Interactive Story", "95% Overwhelmingly Positive", False, "全分支流程图解锁与不限时选项辅助工具", False, True),
    ("kingdom-come-deliverance", "Kingdom Come: Deliverance", "天国：拯救", "Warhorse Studios", 2018, "Realistic Medieval RPG", "83% Very Positive", True, "Steam 启动项加 -devmode，按 ~ 打开，支持随时存档 MOD", True, True),
    ("mount-and-blade-warband", "Mount & Blade: Warband", "骑马与砍杀：战团", "TaleWorlds", 2010, "Action RPG Strategy", "97% Overwhelmingly Positive", True, "启动器勾选【打开作弊模式 (Enable Cheats)】，按 Ctrl+X 刷钱", True, True),
    ("stalker-shadow-of-chernobyl", "S.T.A.L.K.E.R.: Shadow of Chernobyl", "潜行者：切尔诺贝利的阴影", "GSC Game World", 2007, "Post-Apocalyptic FPS RPG", "95% Overwhelmingly Positive", True, "按 ~ 打开控制台，安装 Autumn Aurora 2 或 GAMMA 顶级模组", True, True),

    # 51 - 60
    ("metro-exodus", "Metro Exodus", "地铁：离去", "4A Games", 2019, "Atmospheric Story FPS", "89% Very Positive", False, "修改器防毒面具无限滤毒罐、武器不卡壳", True, True),
    ("control", "Control Ultimate Edition", "控制：终极版", "Remedy Entertainment", 2020, "Supernatural Action-Adventure", "90% Very Positive", True, "游戏菜单内置官方【辅助模式 (Assist Mode)】自带无敌与一击必杀", True, True),
    ("alan-wake-2", "Alan Wake 2", "心灵杀手 2", "Remedy Entertainment", 2023, "Survival Horror", "89% Metacritic", False, "无官方控制台，支持修改器无限手电筒电池与弹药", True, True),
    ("doom-eternal", "DOOM Eternal", "毁灭战士：永恒", "id Software", 2020, "Fast-Paced FPS", "91% Very Positive", True, "通关后关卡选择自带官方作弊秘籍（无限弹药、全晶石）", True, True),
    ("borderlands-3", "Borderlands 3", "无主之地 3", "Gearbox Software", 2019, "Looter Shooter", "85% Very Positive", False, "使用 Save Editor (存档修改器) 任意定制顶级词条传奇神枪", True, True),
    ("borderlands-2", "Borderlands 2", "无主之地 2", "Gearbox Software", 2012, "Looter Shooter", "95% Overwhelmingly Positive", True, "修改 WillowEngine.ini 启用控制台或使用 Gibbed 存档修改器", True, True),
    ("bioshock-infinite", "BioShock Infinite", "生化奇兵：无限", "Irrational Games", 2013, "Story FPS", "95% Overwhelmingly Positive", False, "修改 XEngine.ini 调整持枪视角与无限银鹰币修改器", False, True),
    ("dishonored-2", "Dishonored 2", "羞辱 2", "Arkane Studios", 2016, "Immersive Sim Stealth Action", "89% Very Positive", False, "内置新游戏+模式继承所有符文，搭配修改器无限魔法", True, True),
    ("prey", "Prey", "掠食", "Arkane Studios", 2017, "Sci-Fi Immersive Sim", "90% Very Positive", False, "修改器无限神经调整望远镜、无限材料制造机", True, True),
    ("hitman-3", "HITMAN World of Assassination", "杀手：暗杀世界", "IO Interactive", 2021, "Stealth Action", "90% Very Positive", False, "单机离线模式一键隐形、不被监控探头拍到修改器", True, True),

    # 61 - 70
    ("ac-odyssey", "Assassin's Creed Odyssey", "刺客信条：奥德赛", "Ubisoft", 2018, "Open World RPG", "89% Very Positive", False, "使用 AC Odyssey Inventory Editor (CE表) 刷全商城课金套装", True, True),
    ("ac-valhalla", "Assassin's Creed Valhalla", "刺客信条：英灵殿", "Ubisoft", 2020, "Viking Open World RPG", "83% Very Positive", False, "Cheat Engine 免费解锁全商城传奇武器与坐骑", True, True),
    ("ac-origins", "Assassin's Creed Origins", "刺客信条：起源", "Ubisoft", 2017, "Ancient Egypt Action RPG", "86% Very Positive", True, "内置官方【阿尼姆斯控制面板 (Animus Control Panel)】随意改参数", False, True),
    ("far-cry-5", "Far Cry 5", "孤岛惊魂 5", "Ubisoft", 2018, "Open World FPS", "80% Very Positive", False, "Resistance Mod 开启全自由武器解锁与移除绑架剧情", True, True),
    ("far-cry-6", "Far Cry 6", "孤岛惊魂 6", "Ubisoft", 2021, "Open World FPS", "74% Mostly Positive", False, "使用修改器免换弹、无限铀资源", True, True),
    ("watch-dogs-2", "Watch Dogs 2", "看门狗 2", "Ubisoft", 2016, "Hacker Open World", "83% Very Positive", False, "跳过 EAC 防作弊直接进入离线单机自由漫游修改", True, True),
    ("no-mans-sky", "No Man's Sky", "无人深空", "Hello Games", 2016, "Space Exploration Survival", "82% Very Positive", True, "游戏设置自带官方【自定义难度】随意开启免费制造与无敌", True, True),
    ("astroneer", "Astroneer", "异星探险家", "System Era Softworks", 2016, "Space Crafting Adventure", "92% Very Positive", True, "开启创造模式拥有无限泥土与全科技解锁", False, True),
    ("raft", "Raft", "木筏求生", "Redbeet Interactive", 2018, "Ocean Survival Crafting", "93% Very Positive", True, "安装 Raft Mod Loader 享受一键扩建大船与无限钩子", True, True),
    ("grounded", "Grounded", "禁闭求生", "Obsidian Entertainment", 2022, "Backyard Survival", "90% Very Positive", True, "游戏内置自带官方自定义游戏规则，关闭蜘蛛恐惧症与饥饿度", True, True),

    # 71 - 80
    ("green-hell", "Green Hell", "丛林地狱", "Creepy Jar", 2019, "Amazon Survival Sim", "87% Very Positive", True, "开启 Debug Mode 按 F1-F12 直接呼出刷物品菜单", True, True),
    ("7-days-to-die", "7 Days to Die", "七日杀", "The Fun Pimps", 2024, "Voxel Zombie Survival", "88% Very Positive", True, "按 F1 键输入 dm 开启上帝模式，再按 Q 即可自由飞天穿墙", True, True),
    ("ark-survival-evolved", "ARK: Survival Evolved", "方舟：生存进化", "Studio Wildcard", 2015, "Dinosaur Survival MMO/Single", "83% Very Positive", True, "按 Tab 键输入 enablecheats [密码] 后输入 admincheat god 随意刷龙", True, True),
    ("rust-single", "Rust", "腐蚀 (本地自建服)", "Facepunch Studios", 2018, "Survival Shooter", "87% Very Positive", True, "按 F1 键打开控制台，房主输入 inventory.give 直接刷任意枪械", True, True),
    ("conan-exiles", "Conan Exiles", "流放者柯南", "Funcom", 2018, "Survival Action RPG", "78% Mostly Positive", True, "设置界面直接【成为管理员】，按 Shift+End 呼出全能内置作弊盘", True, True),
    ("medieval-dynasty", "Medieval Dynasty", "中世纪王朝", "Render Cube", 2021, "Medieval Life Sim", "90% Very Positive", True, "游戏设置自带官方作弊滑块（无限负重、无限生命、快速建造）", False, True),
    ("kenshi", "Kenshi", "剑士", "Lo-Fi Games", 2018, "Sandbox Post-Apocalyptic RPG", "95% Overwhelmingly Positive", True, "自带官方 Forgotten Construction Set (FCS) 深度编辑器随心改数值", True, True),
    ("the-sims-4", "The Sims 4", "模拟人生 4", "Maxis / EA", 2014, "Life Simulation", "87% Very Positive", True, "按 Ctrl+Shift+C 输入 testingcheats true 再输入 motherlode 直接加 50000 块", True, True),
    ("planet-zoo", "Planet Zoo", "动物园之星", "Frontier Developments", 2019, "Zoo Management Sim", "90% Very Positive", True, "沙盒模式无限制金钱与保育点数自由打造超大野生动物园", True, True),
    ("jurassic-world-evolution-2", "Jurassic World Evolution 2", "侏罗纪世界：进化 2", "Frontier Developments", 2021, "Dinosaur Theme Park Sim", "87% Very Positive", True, "沙盒模式关闭恐龙发飙暴走与无限资金", True, True),

    # 81 - 90
    ("euro-truck-simulator-2", "Euro Truck Simulator 2", "欧洲卡车模拟 2", "SCS Software", 2012, "Truck Driving Sim", "97% Overwhelmingly Positive", True, "修改 config.cfg 开启 developer 1，按 ~ 开启控制台与自由飞天镜头", True, True),
    ("snowrunner", "SnowRunner", "雪地奔驰", "Saber Interactive", 2021, "Off-Road Physics Sim", "89% Very Positive", True, "官方集成 Mod.io 一键订阅改装神车与无限金钱修改", True, True),
    ("forza-horizon-5", "Forza Horizon 5", "极限竞速：地平线 5", "Playground Games", 2021, "Open World Racing", "88% Very Positive", False, "单人离线修改抽奖与游戏币（注意防封）", False, True),
    ("assetto-corsa", "Assetto Corsa", "神力科莎", "Kunos Simulazioni", 2014, "Racing Simulation", "92% Very Positive", True, "安装 Content Manager (CM) 模组管理神器，体验成千上万玩家自制赛道跑车", True, False),
    ("beamng-drive", "BeamNG.drive", "BeamNG.drive", "BeamNG", 2015, "Soft-body Physics Vehicle Sim", "97% Overwhelmingly Positive", True, "自带极其强大的官方 World Editor (按 F11 键进入上帝造物模式)", True, True),
    ("persona-5-royal", "Persona 5 Royal", "女神异闻录 5 皇家版", "ATLUS", 2022, "JRPG", "97% Overwhelmingly Positive", False, "使用 P5R Mod Manager 搭配修改器解锁全五维与全人格面具", True, True),
    ("persona-3-reload", "Persona 3 Reload", "女神异闻录 3 重制版", "ATLUS", 2024, "JRPG", "95% Overwhelmingly Positive", False, "Reloaded-II 模组加载器与全属性修改器", True, True),
    ("ff7-remake", "Final Fantasy VII Remake Intergrade", "最终幻想 7 重制版", "Square Enix", 2022, "Action RPG", "90% Very Positive", False, "海量蒂法、爱丽丝服装发型 MOD 与无伤修改器", True, True),
    ("ff16", "Final Fantasy XVI", "最终幻想 16", "Square Enix", 2024, "Action RPG", "80% Very Positive", False, "突破 60 帧过场动画锁定 MOD 与无限魔力修改器", True, True),
    ("nier-automata", "NieR:Automata", "尼尔：机械纪元", "Square Enix / PlatinumGames", 2017, "Action RPG", "87% Very Positive", True, "安装 FAR (Special K) 修复分辨率，通关后解锁官方内置作弊商店", True, True),

    # 91 - 100
    ("tales-of-arise", "Tales of Arise", "破晓传说", "Bandai Namco", 2021, "JRPG Action", "89% Very Positive", False, "移除战斗画质噪点 MOD 与无限文物点数修改器", True, True),
    ("like-a-dragon-infinite-wealth", "Like a Dragon: Infinite Wealth", "人中之龙 8", "Ryu Ga Gotoku Studio", 2024, "Turn-Based RPG", "90% Very Positive", False, "春日一番全职业经验值暴涨与无限美元修改器", True, True),
    ("yakuza-like-a-dragon", "Yakuza: Like a Dragon", "人中之龙 7", "Ryu Ga Gotoku Studio", 2020, "Turn-Based RPG", "95% Overwhelmingly Positive", False, "经营公司一秒百亿日元资金修改器", True, True),
    ("star-wars-jedi-survivor", "Star Wars Jedi: Survivor", "星球大战绝地：幸存者", "Respawn Entertainment", 2023, "Action Adventure", "67% Mixed", False, "纯净修改器一键原力无限、光剑一击必杀", True, True),
    ("star-wars-jedi-fallen-order", "Star Wars Jedi: Fallen Order", "星球大战绝地：陨落的武士团", "Respawn Entertainment", 2019, "Action Adventure", "89% Very Positive", False, "全光剑颜色水晶解锁与全技能树点亮修改器", True, True),
    ("dead-space-remake", "Dead Space Remake", "死亡空间：重制版", "Motive / EA", 2023, "Sci-Fi Survival Horror", "91% Very Positive", False, "修改器无限等离子切断枪弹药、无限静滞能量", True, True),
    ("dead-cells", "Dead Cells", "死亡细胞", "Motion Twin", 2018, "Roguelite Metroidvania", "97% Overwhelmingly Positive", True, "游戏菜单内置官方【辅助模式】支持无限复活与难度自由下调", True, True),
    ("hades", "Hades", "黑帝斯", "Supergiant Games", 2020, "Roguelike Action", "98% Overwhelmingly Positive", True, "游戏设置内置官方【神力模式 (God Mode)】每次死亡减伤增益 2%", True, True),
    ("hollow-knight", "Hollow Knight", "空洞骑士", "Team Cherry", 2017, "Metroidvania Action", "97% Overwhelmingly Positive", True, "安装 Scarab 模组管理器，支持 Debug Mod 按 F1 开启作弊菜单", True, True),
    ("slay-the-spire", "Slay the Spire", "杀戮尖塔", "MegaCrit", 2019, "Roguelike Deckbuilder", "97% Overwhelmingly Positive", True, "支持 Steam 创意工坊模组，内置自定义模式自由选牌与无敌开局", True, True)
]

# Assemble the 100 Games list
all_games = []
# First 10
all_games.extend(TOP_100_GAMES)

# Add remaining 90 games
for rank_offset, item in enumerate(REMAINING_GAMES_METADATA, start=11):
    gid, en_title, zh_title, dev, yr, genre, rating, has_console, console_guide, has_mods, has_trainer = item
    
    # Generic multilingual titles
    titles = {
        "en": en_title,
        "zh-CN": zh_title,
        "zh-TW": zh_title,
        "ja": en_title,
        "ko": en_title,
        "ru": en_title,
        "de": en_title,
        "es": en_title
    }
    
    game_obj = {
        "id": gid,
        "rank": rank_offset,
        "title": en_title,
        "titles": titles,
        "developer": dev,
        "releaseYear": yr,
        "genre": genre,
        "steamRating": rating,
        "hasConsole": has_console,
        "consoleShortcut": "~ / F1 / Settings" if has_console else "无官方控制台",
        "consoleEnableGuide": {
            "zh-CN": console_guide,
            "en": f"Official Console / Developer Guide for {en_title}: {console_guide}",
            "zh-TW": console_guide,
            "ja": f"{en_title} 公式コンソール / MOD ガイド: {console_guide}",
            "ko": f"{en_title} 공식 콘솔 및 모드 가이드: {console_guide}",
            "ru": f"Руководство по консоли и модам для {en_title}: {console_guide}",
            "de": f"Offizielle Konsole & Mod-Anleitung für {en_title}: {console_guide}",
            "es": f"Guía oficial de consola y mods para {en_title}: {console_guide}"
        },
        "popularCommands": [],
        "hasMods": has_mods,
        "modInstallPath": f"{en_title}\\Mods" if has_mods else "N/A",
        "mustHaveMods": [],
        "hasTrainer": has_trainer,
        "trainerHotkeys": []
    }
    all_games.append(game_obj)

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(TARGET_PATH, "w", encoding="utf-8") as f:
    json.dump(all_games, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(all_games)} games in {TARGET_PATH}")
