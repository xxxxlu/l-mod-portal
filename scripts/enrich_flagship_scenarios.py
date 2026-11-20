#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scenario bundles, pitfall notes, batch helper scripts and patch tags for the
flagship games listed in FLAGSHIP_DATA.

Writes only those five fields of those games, through gamedata_guard: the master
data must exist, radar and trainer fields are never written, and in public/data.js
only the GAMES_DATA segment changes (TRANSLATIONS_DATA is left alone).
Other games are not touched (this script used to reset every other game's
verifiedPatch / radarSecretCode, overwriting the values other scripts set).

Usage: python3 scripts/enrich_flagship_scenarios.py [--dry-run]
"""

from gamedata_guard import write_owned_fields

OWNED_FIELDS = ("verifiedPatch", "radarSecretCode", "pitfallNote", "scenarioBundles", "batScript")

FLAGSHIP_DATA = {
    "cyberpunk-2077": {
        "verifiedPatch": "2.13（未实测）",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L避坑笔记 (赛博朋克2077 v2.13)",
            "tips": [
                "【版本语法避坑】：2.0+ 往日之影彻底重构了专精成长树，千万别运行网上旧版 1.63 的 SetLevel 代码，否则专精树直接永久卡死！本站套餐改用了 2.0 之后的 SetProficiencyLevel 写法（没有逐条实测）。",
                "【CET热键防呆】：首次进入游戏按 ~ 键若没反应，请先切换到英文输入法（Caps Lock关）。CET 控制台必须在全屏或无边框窗口模式下呼出。",
                "【剧情Fact生效机理】：救赎包里的 Fact 标志位修改后，建议立刻进行一次快速存档 (F5) 再读档 (F9)，即可瞬间刷新 NPC 状态机与夜之城任务树。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "cp_starter_bundle",
                "type": "starter",
                "name": "新手破荒起飞包",
                "tag": "👑 萌新首选 · 零门槛",
                "badge": "开荒神装",
                "desc": "一键激活完全无敌 + 无限耐力狂奔 + 200万启动资金 + 50本技能专精书 + 顶级材料满载，轻松踏平夜之城开局！",
                "highlights": [
                    "Game.GodMode(true) 完全无敌抗揍",
                    "Game.InfiniteStamina(true) 无限耐力不喘气",
                    "2,000,000 欧元启动现金买空武器店",
                    "50 本特权书 + 20 本属性技能书点满核心",
                    "金色 5 阶制造组件与军火弹药全满"
                ],
                "code": """-- [老L·极客场景套餐] 赛博朋克2077 新手破荒起飞包 (v2.13，未实测)
Game.GodMode(true)
Game.InfiniteStamina(true)
Game.AddToInventory("Items.money", 2000000)
Game.AddToInventory("Items.PerkPointSkillbook", 50)
Game.AddToInventory("Items.AttributePointSkillbook", 20)
Game.AddToInventory("Items.LegendaryMaterial1", 2000)
Game.AddToInventory("Items.QuickHackLegendaryMaterial1", 2000)
Game.AddToInventory("Items.CyberwareMaterial5", 1000)"""
            },
            {
                "id": "cp_salvation_bundle",
                "type": "salvation",
                "name": "隐藏结局救赎包",
                "tag": "💖 意难平救赎 · 剧情党狂喜",
                "badge": "完美剧情",
                "desc": "一键注入关键剧情 Fact 标志位！不用纠结油田对话直接解锁天台单挑荒坂塔隐藏死神结局，朱迪/帕南跨性别推倒，瞬开全城快速传送！",
                "highlights": [
                    "修复油田对话！天台静默4分钟触发「单挑荒坂塔隐藏死神结局」",
                    "解锁朱迪恋爱权限 (跨性别男女V皆可推倒潜水)",
                    "解锁帕南恋爱权限 (跨性别男女V皆可魔蜥浪漫)",
                    "夜之城全图 150+ 快速旅行数据终端瞬开",
                    "一键消散 NCPD 全城警星与暴恐机动队通缉"
                ],
                "code": """-- [老L·极客场景套餐] 赛博朋克2077 隐藏结局与意难平救赎包 (v2.13，未实测)
Game.GetQuestsSystem():SetFactStr("sq032_johnny_friend", 1)
Game.GetQuestsSystem():SetFactStr("fast_travel_all_unlocked", 1)
Game.GetQuestsSystem():SetFactStr("judy_romanceable", 1)
Game.GetQuestsSystem():SetFactStr("panam_romanceable", 1)
Game.GetQuestsSystem():SetFactStr("q115_done", 1)
Game.GetPreventionSpawnSystem():RequestDespawnPreventionAgents()"""
            },
            {
                "id": "cp_arsenal_bundle",
                "type": "arsenal",
                "name": "二周目全神装满配包",
                "tag": "⚔️ 战力天花板 · 毕业满配",
                "badge": "不朽神装",
                "desc": "五大技能树一键拉满60级！打包往日之影黑墙冲锋枪【厄瑞玻斯】+ 荒坂传家太刀【觉】+ 5++远地点时停义体 + 奇美拉核心插件 + 全豪车解锁！",
                "highlights": [
                    "猎头/黑客/忍者/破坏/工程五大技能直升 60 级满级",
                    "终极 5++ 义体：远地点时停 + 黑墙 Canto Mk.6 + 量子调谐器",
                    "绝版不朽：厄瑞玻斯黑墙枪 + 大力神 3AX + 觉 + 涅槃 + 白虎",
                    "奇美拉核心插件（爆裂穿透动能高爆 + 终极壁垒200%穿墙）",
                    "全夜之城所有载具与保时捷911超跑全买断"
                ],
                "code": """-- [老L·极客场景套餐] 赛博朋克2077 二周目全神装满配包 (v2.13，未实测)
local ds = PlayerDevelopmentSystem.GetInstance(Game.GetPlayer()):GetDevelopmentData(Game.GetPlayer()) for _, p in ipairs({"Headhunter", "Netrunner", "Shinobi", "Solo", "Engineer"}) do ds:SetProficiencyLevel(gamedataProficiencyType[p], 60, telemetryLevelGainReason.Gameplay) end
Game.AddToInventory("Items.AdvancedSandevistanApogeePlusPlus", 1)
Game.AddToInventory("Items.HauntedCyberdeck_LegendaryPlusPlus", 1)
Game.AddToInventory("Items.AdvancedTimeBankLegendaryPlusPlus", 1)
Game.AddToInventory("Items.Preset_Borg4a_HauntedGun", 1)
Game.AddToInventory("Items.Preset_Hercules_Prototype", 1)
Game.AddToInventory("Items.Preset_Katana_Saburo", 1)
Game.AddToInventory("Items.Preset_Knife_Saburo", 1)
Game.AddToInventory("Items.Preset_Katana_Wakako", 1)
Game.AddToInventory("Items.ChimeraPowerMod", 1)
Game.AddToInventory("Items.ChimeraTechMod", 1)
Game.GetVehicleSystem():EnableAllPlayerVehicles()"""
            }
        ],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】赛博朋克2077 CET 呼出键设置
echo ========================================================
echo   【老L·单机避坑局】赛博朋克2077 CET 呼出键设置脚本
echo   把 CET 的呼出键写成 ~ 键；改之前把原 bindings.json 另存为 .bak
echo ========================================================
echo.

set "CET_DIR=bin\\x64\\plugins\\cyber_engine_tweaks"
set "BIND_FILE=%CET_DIR%\\bindings.json"

if not exist "bin\\x64\\Cyberpunk2077.exe" (
    echo [!] 当前目录下没有 bin\\x64\\Cyberpunk2077.exe，脚本什么都没改。
    echo     请把本脚本放到《赛博朋克2077》游戏安装根目录再运行。
    echo.
    pause
    exit /b
)

if not exist "%CET_DIR%" (
    echo [i] 没找到 %CET_DIR%，CET 可能还没装；先把这个目录建好。
    mkdir "%CET_DIR%"
)

if exist "%BIND_FILE%" (
    copy /y "%BIND_FILE%" "%BIND_FILE%.bak" >nul
    echo [+] 原来的 bindings.json 已另存为 bindings.json.bak
)

echo {"cet": {"overlay_key": 54043195528445952}}>"%BIND_FILE%"
echo [+] 已写入 %BIND_FILE%：CET 呼出键 = ~ 键
echo     按 CET 源码里的格式写的，没在游戏里试过；原文件里其它 Mod 的按键会被清掉，要用就从 .bak 拷回来。
echo.
echo ========================================================
echo  [i] 还要你自己确认：bin\\x64 下已经放好 CET 的文件。
echo      进游戏按 ~ 没反应：删掉 bindings.json 再启动，CET 会弹窗让你重新绑键。
echo      脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。
echo ========================================================
echo.
pause
"""
    },

    "black-myth-wukong": {
        "verifiedPatch": "v1.0.10.15610（未实测）",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L避坑笔记 (黑神话：悟空)",
            "tips": [
                "【打坐存盘后执行】：招式变身与道具全收集指令建议在土地庙打坐存盘后输入，避免由于过场动画强制卸载模型导致镜头卡顿。",
                "【0.4x 子弹时间妙用】：对于手残党，开启 slomo 0.4 子弹时间不仅能轻松看清 Boss 抬手，还能大幅延长看破识破判定帧，极其优雅地通关！",
                "【UE4SS 前置】：UE4SS 到它的 GitHub 发布页下载。本站的 .bat 会把 mods.txt 里的 ConsoleEnablerMod 从 0 改成 1（改之前另存 mods.txt.bak）；mods.txt 里没有这一行的话要自己加。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "bmw_starter_bundle",
                "type": "starter",
                "name": "新手破荒起飞包",
                "tag": "👑 萌新首选 · 识破无敌",
                "badge": "轻松通关",
                "desc": "一键激活 0.4x 子弹时间（识破看破窗口翻倍）+ 20万经验直升 + 99点灵光天赋 + 50万灵蕴财富 + 基础草药矿石满载！",
                "highlights": [
                    "slomo 0.4 开启从容子弹时间，手残党秒变动作大师",
                    "addexp 200000 注入海量经验直升等级",
                    "addtalentpoint 99 天赋灵光点数拉满，技能树自由点",
                    "additem 1002 500000 灵蕴财富直接自由",
                    "allitem 解锁全部初级药材与装备铸造矿石"
                ],
                "code": """# [老L·极客场景套餐] 黑神话悟空 新手破荒起飞包
slomo 0.4
addexp 200000
addtalentpoint 99
additem 1002 500000
allitem"""
            },
            {
                "id": "bmw_salvation_bundle",
                "type": "salvation",
                "name": "隐藏结局救赎包",
                "tag": "💖 意难平救赎 · 六根圆满",
                "badge": "真结局必吃",
                "desc": "一键集齐六根大圣遗物！影神图全妖魔神仙传记全图鉴解锁，全图打坐点与全部章回缩地土地庙瞬开，不漏任何意难平隐藏支线！",
                "highlights": [
                    "alllegacy 一键集齐大圣六根遗物，解锁真实圆满轮回真结局",
                    "allcard 影神图图鉴全开，全妖魔神仙生平图文全览",
                    "allmedition 1 全图全部章节土地庙打坐蒲团全点亮",
                    "allmap 解锁全部章回传送与土地庙缩地节点"
                ],
                "code": """# [老L·极客场景套餐] 黑神话悟空 隐藏结局救赎与全图鉴包
alllegacy
allcard
allmedition 1
allmap"""
            },
            {
                "id": "bmw_arsenal_bundle",
                "type": "arsenal",
                "name": "二周目全神装满配包",
                "tag": "⚔️ 战力天花板 · 毕业满配",
                "badge": "大圣真身",
                "desc": "全传奇神兵一键拥有（如意金箍棒、三尖两刃枪等）+ 锁子黄金甲大圣神装全套 + 54大妖王精魄化身全解锁 + 上清宝葫芦与极品酒食！",
                "highlights": [
                    "allweapon 如意金箍棒、三尖两刃枪、昆棍通天神兵齐聚",
                    "allequip 凤翅紫金冠、锁子黄金甲、藕丝步云履大圣套装",
                    "allsoulskill 54大妖王精魄化身与变身神通全解锁",
                    "allhulu 上清宝葫芦、彩玉葫芦等全品阶神级葫芦",
                    "allwine 全极品酒食与泡酒物收集齐备"
                ],
                "code": """# [老L·极客场景套餐] 黑神话悟空 二周目全神装满配包
allweapon
allequip
allsoulskill
allhulu
allwine"""
            }
        ],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】黑神话悟空 UE4SS 控制台开关
echo ========================================================
echo   【老L·单机避坑局】黑神话悟空 UE4SS 控制台开关脚本
echo   把 mods.txt 里的 ConsoleEnablerMod 改成 1；改之前另存 mods.txt.bak
echo ========================================================
echo.

set "WIN64=b1\\Binaries\\Win64"

if not exist "b1\\Binaries\\Win64" (
    echo [!] 当前目录下没有 b1\\Binaries\\Win64，脚本什么都没改。
    echo     请把本脚本放到《黑神话：悟空》游戏安装根目录再运行。
    echo.
    pause
    exit /b
)

set "MODS_TXT="
if exist "%WIN64%\\ue4ss\\Mods\\mods.txt" set "MODS_TXT=%WIN64%\\ue4ss\\Mods\\mods.txt"
if not defined MODS_TXT if exist "%WIN64%\\Mods\\mods.txt" set "MODS_TXT=%WIN64%\\Mods\\mods.txt"

if not defined MODS_TXT (
    echo [!] %WIN64%\\ue4ss\\Mods\\ 和 %WIN64%\\Mods\\ 下都没有 mods.txt，脚本什么都没改。
    echo     请先把 UE4SS 解压到 %WIN64%\\ 再运行本脚本。
    echo.
    pause
    exit /b
)

copy /y "%MODS_TXT%" "%MODS_TXT%.bak" >nul
echo [+] 已另存 %MODS_TXT%.bak
powershell -NoProfile -Command "(Get-Content '%MODS_TXT%') -replace 'ConsoleEnablerMod\\s*:\\s*0', 'ConsoleEnablerMod : 1' | Set-Content '%MODS_TXT%'"

findstr /r /i /c:"ConsoleEnablerMod *: *1" "%MODS_TXT%" >nul
if errorlevel 1 (
    echo [!] %MODS_TXT% 里没有 ConsoleEnablerMod 这一行。
    echo     请用记事本打开它，自己加一行：ConsoleEnablerMod : 1
) else (
    echo [+] %MODS_TXT% 里 ConsoleEnablerMod 现在是 1。
)

echo.
echo ========================================================
echo  [i] 进游戏按 F10 或 ~ 键试试控制台。
echo      脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。
echo ========================================================
echo.
pause
"""
    },

    "witcher-3": {
        "verifiedPatch": "v4.04（未实测）",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L避坑笔记 (巫师3 次世代版 v4.04)",
            "tips": [
                "【零注入原生开启】：次世代版 4.04 官方原生隐藏了调试控制台，只需改动 general.ini 添加 DBGConsoleOn=true 即可，根本不需要下载任何可能报毒的第三方 exe！",
                "【昆特牌无脑秒胜】：打牌输了想砸键盘？控制台输入 winGwint(true) 直接判定胜利（执行前先存档）。",
                "【爱丽丝玫瑰与湖女剑】：石之心通关后遗憾把玫瑰交出去了？输入 additem('Iris\\'s Rose') 即可让紫色玫瑰永远留在杰洛特背包与白鸦葡萄园！"
            ]
        },
        "scenarioBundles": [
            {
                "id": "w3_starter_bundle",
                "type": "starter",
                "name": "新手破荒起飞包",
                "tag": "👑 萌新首选 · 猎魔无双",
                "badge": "白狼无双",
                "desc": "一键激活绝对无敌 + 一击必杀秒杀一切狂猎孽鬼 + 10万克朗财富自由 + 全大陆路标瞬移全开 + 随时随地自由传送！",
                "highlights": [
                    "god 开启杰洛特完全无敌模式",
                    "likeaboss 一击必杀，秒杀任何高难度狂猎与野怪",
                    "addmoney(100000) 注入 100,000 克朗自由消费",
                    "ShowAllFT(1) 全大陆所有快速旅行路标瞬移全开",
                    "AllowFT(1) 解除路标限制，野外随时随地自由传送",
                    "红绿蓝极品大突变诱发物各 10 个"
                ],
                "code": """// [老L·极客场景套餐] 巫师3次世代版 新手破荒起飞包 (v4.04，未实测)
god
likeaboss
addmoney(100000)
ShowAllFT(1)
AllowFT(1)
additem('Greater mutagen red', 10)
additem('Greater mutagen blue', 10)
additem('Greater mutagen green', 10)"""
            },
            {
                "id": "w3_salvation_bundle",
                "type": "salvation",
                "name": "隐藏结局救赎包",
                "tag": "💖 意难平救赎 · 拯救爱丽丝",
                "badge": "真爱救赎",
                "desc": "一键获取石之心意难平信物【爱丽丝之刀】与【爱丽丝的紫色玫瑰】+ 骑士美德终极神剑【湖女之剑】+ 昆特牌五大势力英雄牌库秒胜！",
                "highlights": [
                    "additem('Aerondight EP2') 获得随杀敌永久成长神剑「湖女之剑」",
                    "additem('Olgierd Sabre') 欧吉尔德爱刀「爱丽丝」充能重击",
                    "additem('Iris\\'s Rose') 爱丽丝的紫色玫瑰，世间永存信物",
                    "secretgwint 五大阵营顶级英雄昆特牌全收集",
                    "winGwint(true) 昆特牌局无脑秒胜，救赎打牌遗憾"
                ],
                "code": """// [老L·极客场景套餐] 巫师3次世代版 拯救爱丽丝与完美救赎包 (v4.04，未实测)
additem('Aerondight EP2')
additem('Olgierd Sabre')
additem('Iris\\'s Rose')
secretgwint
winGwint(true)"""
            },
            {
                "id": "w3_arsenal_bundle",
                "type": "arsenal",
                "name": "二周目全神装满配包",
                "tag": "⚔️ 战力天花板 · 毕业满配",
                "badge": "宗师学派",
                "desc": "杰洛特等级瞬间拉满 100 级！次世代完全版专属【九尾白虎铠甲】+ 宗师级狼/熊/猫/飞狮极品双剑套装 + 湖女之剑顶级毕业！",
                "highlights": [
                    "setlevel(100) 杰洛特等级直升 100 级",
                    "次世代完全版专属联动：九尾白虎铠甲全套",
                    "宗师级狼学派极品双剑（狼学派信仰）",
                    "宗师级熊学派极品双剑（拜年重击流核心）",
                    "宗师级猫学派极品银剑（剑舞回旋流）",
                    "师匠级飞狮怪银剑（暴击瘾头流）"
                ],
                "code": """// [老L·极客场景套餐] 巫师3次世代版 二周目宗师神装满配包 (v4.04，未实测)
setlevel(100)
additem('White Tiger Armor')
additem('White Tiger Boots')
additem('Wolf School Silver Sword 4')
additem('Wolf School Steel Sword 4')
additem('Bear School silver sword 4')
additem('Bear School steel sword 4')
additem('Lynx School silver sword 4')
additem('Red Wolf Silver Sword 1')
additem('Aerondight EP2')
additem('Olgierd Sabre')"""
            }
        ],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】巫师3次世代版 控制台开关
echo ========================================================
echo   【老L·单机避坑局】巫师3次世代版 控制台开关脚本
echo   在 general.ini 里打开 DBGConsoleOn；改之前另存 general.ini.bak
echo ========================================================
echo.

set "TARGET_DIR=bin\\config\\base"
set "TARGET_FILE=%TARGET_DIR%\\general.ini"

if not exist "bin\\config\\base\\general.ini" (
    echo [!] 当前目录下没有 bin\\config\\base\\general.ini，脚本什么都没改。
    echo     请把本脚本放到《巫师3》游戏安装根目录再运行。
    echo.
    pause
    exit /b
)

copy /y "%TARGET_FILE%" "%TARGET_FILE%.bak" >nul
echo [+] 已另存 %TARGET_FILE%.bak

findstr /i "DBGConsoleOn" "%TARGET_FILE%" >nul
if %errorlevel% equ 0 (
    echo [i] general.ini 里已有 DBGConsoleOn，把 false 改成 true ...
    powershell -NoProfile -Command "(Get-Content '%TARGET_FILE%') -replace '(?i)DBGConsoleOn\\s*=\\s*false', 'DBGConsoleOn=true' | Set-Content '%TARGET_FILE%'"
) else (
    echo.>>"%TARGET_FILE%"
    echo [General]>>"%TARGET_FILE%"
    echo DBGConsoleOn=true>>"%TARGET_FILE%"
    echo [+] 已在 general.ini 末尾加上 [General] 和 DBGConsoleOn=true
)

findstr /r /i /c:"DBGConsoleOn *= *true" "%TARGET_FILE%" >nul
if errorlevel 1 (
    echo [!] general.ini 里没找到 DBGConsoleOn=true，请用记事本打开 %TARGET_FILE% 自己检查。
) else (
    echo [+] general.ini 里现在有 DBGConsoleOn=true。
)

echo.
echo ========================================================
echo  [i] 进游戏按 ~ (波浪键) 或 @ 键试试控制台。
echo      想还原：把 %TARGET_FILE%.bak 改回 general.ini。
echo      脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。
echo ========================================================
echo.
pause
"""
    },

    "baldurs-gate-3": {
        "verifiedPatch": "Patch 7（未实测）",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L避坑笔记 (博德之门3 Patch 7)",
            "tips": [
                "【Script Extender 控制台】：Patch 7 有了官方模组管理器，但控制台还是要靠 Norbyte 的 Script Extender。用控制台会不会影响成就没有人核实过（Script Extender 默认开着 EnableAchievements，用来恢复装 Mod 后的成就），执行前先存档。",
                "【长休补给一劳永逸】：博德之门3经常为搜刮营地苹果烤肠烦恼？直接注入 50 个营地补给包即可永久实现全员满血法术位拉满。",
                "【队友满好感时机】：好感度指令 SetAttitude 建议在第一章营地初次对话后使用，不仅能稳稳触发影心、阿斯代伦、盖尔的恋爱事件，还能避开剧情好感锁死。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "bg3_starter_bundle",
                "type": "starter",
                "name": "新手破荒起飞包",
                "tag": "👑 萌新首选 · 费伦首富",
                "badge": "博德首富",
                "desc": "一键注入 100,000 金币买空全城商人 + 50 个营地补给包告别长休食物烦恼 + 常驻绝对急速术（每回合动作翻倍）+ 自由飞行能力 + 30只寄生虫！",
                "highlights": [
                    "Osi.AddGold(100000) 10万黄金直接变身费伦大陆首富",
                    "50个营地补给包，长休法术位随时充满",
                    "常驻绝对急速术 (HASTE)，每回合动作翻倍且不疲劳",
                    "赋予常驻自由飞行 (FLY)，轻松跨越断崖天堑",
                    "30只夺心魔寄生虫标本，点满全脑池至尊灵能"
                ],
                "code": """-- [老L·极客场景套餐] 博德之门3 新手破荒起飞包 (Patch 7，未实测)
Osi.AddGold(GetHostCharacter(), 100000)
Osi.TemplateAddTo("1a95e0c5-59b4-4b5b-98cf-19da6d393796", GetHostCharacter(), 50)
Osi.ApplyStatus(GetHostCharacter(), "HASTE", -1)
Osi.ApplyStatus(GetHostCharacter(), "FLY", -1)
Osi.TemplateAddTo("5d94726a-939b-449e-b9b3-57c2df47b855", GetHostCharacter(), 30)"""
            },
            {
                "id": "bg3_salvation_bundle",
                "type": "salvation",
                "name": "隐藏结局救赎包",
                "tag": "💖 意难平救赎 · 队友全恋爱",
                "badge": "救赎起源",
                "desc": "影心、阿斯代伦、盖尔好感度瞬间拉满 100 点！救赎起源角色意难平，赠送星界灌注蝌蚪解锁半夺心魔灵能 + 10张绝对无敌护罩卷轴！",
                "highlights": [
                    "影心 (Shadowheart) 好感度拉满 100 点 (极度崇拜，直通白发救赎)",
                    "阿斯代伦 (Astarion) 好感度拉满 100 点 (解脱吸血鬼衍体束缚)",
                    "盖尔 (Gale) 好感度拉满 100 点 (解除神之自爆执念)",
                    "星界灌注蝌蚪解锁半夺心魔至尊灵能与自由飞行",
                    "无敌护罩卷轴 x10 (范围内全员绝对无敌，死保关键剧情NPC)"
                ],
                "code": """-- [老L·极客场景套餐] 博德之门3 队友全满好感与意难平救赎包 (Patch 7，未实测)
Osi.SetAttitude(GetHostCharacter(), "S_Player_Shadowheart_c7c13742-c166-4fec-bb4b-dc254dc2e080", 100)
Osi.SetAttitude(GetHostCharacter(), "S_Player_Astarion_c7c13742-c166-4fec-bb4b-dc254dc2e080", 100)
Osi.SetAttitude(GetHostCharacter(), "S_Player_Gale_ad9af97d-75da-406a-ae13-7071c563f604", 100)
Osi.TemplateAddTo("02359419-74d7-4632-af82-c5180f1350a4", GetHostCharacter(), 1)
Osi.TemplateAddTo("7f9b846e-1d5d-4f11-b0db-6e9faea18501", GetHostCharacter(), 10)"""
            },
            {
                "id": "bg3_arsenal_bundle",
                "type": "arsenal",
                "name": "二周目全神装满配包",
                "tag": "⚔️ 战力天花板 · 毕业满配",
                "badge": "金色传奇",
                "desc": "博德安巨人杀手巨剑 + 投掷神兵尼鲁纳三叉戟 + 全法系毕业神杖玛科赫什基 + 泰坦重弩 + 21AC免熟练地狱火重装 + 锁死23点属性首饰！",
                "highlights": [
                    "博德安的巨人杀手巨剑（传奇双手剑，力量加倍）",
                    "尼鲁纳三叉戟（投掷流至尊神器，雷鸣自返）",
                    "玛科赫什基传奇法杖（全法系毕业神杖，免消耗施法）",
                    "冈特·耶尔传奇重弩（泰坦重弩，恒定加速）",
                    "全套地狱火传奇重装（21AC 免熟练穿戴与绝对免火伤）",
                    "体质锁23「高等健康护符」+ 力量锁23「山丘巨人手套」"
                ],
                "code": """-- [老L·极客场景套餐] 博德之门3 二周目绝世传奇神兵满配包 (Patch 7，未实测)
Osi.TemplateAddTo("3b6b2512-cf49-411a-8260-cb56220b0805", GetHostCharacter(), 1)
Osi.TemplateAddTo("222e43bc-42f0-4667-8495-2be26ec490a4", GetHostCharacter(), 1)
Osi.TemplateAddTo("a8ff2900-349c-4f76-8d54-159e1ab5a7fa", GetHostCharacter(), 1)
Osi.TemplateAddTo("0c6aaec8-cbe9-450f-9f79-6a56ec94bb0a", GetHostCharacter(), 1)
Osi.TemplateAddTo("026fe827-ce47-49f3-855c-e587e91eb3c8", GetHostCharacter(), 1)
Osi.TemplateAddTo("33734689-d4bc-4676-9d3d-c12e52bca7e0", GetHostCharacter(), 1)
Osi.TemplateAddTo("fbb8968f-f179-4672-91d1-6677f523c9e6", GetHostCharacter(), 1)
Osi.TemplateAddTo("b272f04e-eb5d-4a15-b73f-d309074815a5", GetHostCharacter(), 1)
Osi.TemplateAddTo("9c9b7405-b778-4f05-8946-b333421295db", GetHostCharacter(), 1)
Osi.TemplateAddTo("d41dfa98-8ec1-4e4b-97e3-0d340b6e9a66", GetHostCharacter(), 20)"""
            }
        ],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】博德之门3 Script Extender 控制台开关
echo ========================================================
echo   【老L·单机避坑局】博德之门3 Script Extender 控制台开关脚本
echo   在 bin\\ScriptExtenderSettings.json 里打开 CreateConsole；改之前另存 .bak
echo ========================================================
echo.

set "BIN_DIR="
if exist "bin\\bg3.exe" set "BIN_DIR=bin"
if not defined BIN_DIR if exist "bg3.exe" set "BIN_DIR=."

if not defined BIN_DIR (
    echo [!] 当前目录下没有 bin\\bg3.exe，脚本什么都没改。
    echo     请把本脚本放到《博德之门3》游戏安装根目录再运行。
    echo.
    pause
    exit /b
)

if not exist "%BIN_DIR%\\DWrite.dll" (
    echo [!] %BIN_DIR% 下没有 DWrite.dll：Script Extender 可能还没装，装好以后这个设置才起作用。
)

set "CFG_FILE=%BIN_DIR%\\ScriptExtenderSettings.json"
if exist "%CFG_FILE%" (
    copy /y "%CFG_FILE%" "%CFG_FILE%.bak" >nul
    echo [+] 原来的 ScriptExtenderSettings.json 已另存为 ScriptExtenderSettings.json.bak
)

echo {"CreateConsole": true}>"%CFG_FILE%"
echo [+] 已写入 %CFG_FILE%：CreateConsole = true
echo     原文件里的其它设置会被清掉，要用就从 .bak 拷回来。
echo.
echo ========================================================
echo  [i] 启动游戏时会多出一个 Script Extender 控制台窗口。
echo      在窗口里先按回车进入输入模式，再粘贴指令、回车执行。
echo      设置文件放在 bin 目录，依据是 Norbyte/bg3se 官方文档 Docs/Debugger.md。
echo      脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。
echo ========================================================
echo.
pause
"""
    },
    "elden-ring": {
        "verifiedPatch": "v1.14（未实测）",
        "radarSecretCode": "法环",
        "pitfallNote": {
            "title": "老L避坑笔记 (艾尔登法环 黄金树幽影 v1.14)",
            "tips": [
                "【EAC 与封号】：FromSoftware 的 Easy Anti-Cheat 会在上报内存修改时对账号进行 180 天隔离小黑屋处罚！切勿在官方联机在线状态下注入，改游戏只在离线下进行（用 ModEngine2 或替换启动的方式不加载 EAC，只能离线玩）。",
                "【幽影树庇护机制】：幽影之地独立于本篇等级，受折磨卡关时重点是将 Scadutree Blessing（幽影树庇护）调至 Lv20 满级，攻防减伤直接翻倍，即可彻底解除幽影受苦！",
                "【无缝联机独立存档】：Seamless Co-op 用独立的 .co2 存档，不连官方匹配服务器。它是第三方 Mod，会不会被封号没有人能担保；别把 .co2 存档改回原版存档带上线。"
            ]
        },
        "scenarioBundles": [],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】艾尔登法环 离线启动说明
echo ========================================================
echo   【老L·单机避坑局】艾尔登法环 离线启动说明
echo   本脚本只检查游戏主程序在不在，不改任何文件
echo ========================================================
echo.
if not exist "Game\\eldenring.exe" (
    echo [!] 当前目录下没有 Game\\eldenring.exe，脚本什么都没改。
    echo     请把本脚本放到 ELDEN RING 游戏安装根目录再运行。
    echo.
    pause
    exit /b
)
echo [+] 找到 Game\\eldenring.exe
echo [i] 用 Mod：解压 ModEngine2，Mod 放进它的 mod 目录，双击它自带的 launchmod_eldenring.bat 启动。
echo     这样启动不加载 EAC，只能离线玩；别带着改过的游戏或存档上线，有封号风险。
echo [i] 本脚本没有检查 ModEngine2 和 EAC，也不会替你启动游戏。
echo [i] 脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。
echo.
pause
"""
    },
    "skyrim-se": {
        "verifiedPatch": "v1.6.1170（未实测）",
        "radarSecretCode": "老滚5",
        "pitfallNote": {
            "title": "老L避坑笔记 (上古卷轴5 天际重制版 v1.6.1170)",
            "tips": [
                "【FormID省略前导零】：控制台输入代码时，前导 000 全部可以省略！比如金币 0000000F，直接输入 player.additem f 100000 即可生效。",
                "【严禁盲目运行 caqs】：任务卡关千万不要运行 caqs（强制完成全游戏所有任务），这会导致全图 NPC 状态机彻底崩溃毁坏全档！必须定向使用 setstage <QuestID> <Stage>。",
                "【高刷推车飞天修复】：高刷新率显示器（60Hz+）必须配合 SSE Engine Fixes 锁定物理引擎帧率，防止开局马车翻滚抽搐飞天。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "skyrim_starter_bundle",
                "type": "starter",
                "name": "抓根宝开荒起飞包",
                "tag": "👑 萌新首选 · 零门槛",
                "badge": "天际首富",
                "desc": "一键激活上帝模式 + 10万金币启动资金 + 负重上限扩充至 50,000 + 解除卡石缝绝境，舒适开局！",
                "highlights": [
                    "tgm 上帝模式（无限生命/魔力/耐力/弹药）",
                    "player.additem f 100000（瞬间到账 10 万塞普汀）",
                    "player.modav carryweight 50000（背包永远装不满）",
                    "tcl 穿墙脱困开关（一秒脱离地形卡死）"
                ],
                "code": """; [老L·极客场景套餐] 上古卷轴5 抓根宝开荒起飞包
tgm
player.additem f 100000
player.modav carryweight 50000
player.setav speedmult 130"""
            },
            {
                "id": "skyrim_salvation_bundle",
                "type": "salvation",
                "name": "恶性卡关与NPC复活救赎包",
                "tag": "🛡️ 坏档急救 · 逆天改命",
                "badge": "救砖神技",
                "desc": "定向解决任务 NPC 发呆死锁 + 死去关键随从原地满血复活 + 官方开发者全宝箱烟雾房直达，心血存档救星！",
                "highlights": [
                    "resurrect 1（点击NPC尸体瞬间满血原地复活）",
                    "coc qasmoke（瞬间传送官方全物品开发者房；输入 coc riverwood 返回溪木镇）",
                    "setstage 定向推进死循环任务，绝不破坏全图进度",
                    "tai / tcai 解除发呆木桩状态机死锁"
                ],
                "code": """; [老L·极客场景套餐] 上古卷轴5 恶性卡关与NPC复活救赎包
; 救活NPC：按 ~ 鼠标左键点击尸体后输入 resurrect 1
; 进入开发者烟雾房：
coc qasmoke
; 修复卡关任务（以唤醒巨龙为例，定向推进到击杀米尔墨尼尔）：
setstage MQ104 90"""
            },
            {
                "id": "skyrim_godmode_bundle",
                "type": "godmode",
                "name": "16大魔神器与全龙吼满配包",
                "tag": "⚡ 极客狂欢 · 天际真神",
                "badge": "抓根宝毕业",
                "desc": "16 件魔神神器直接入库 + 抓根宝全龙吼解锁并免 CD 施放 + 炉火豪宅全材料到账，化身塔洛斯真神！",
                "highlights": [
                    "瓦巴杰克、破晓者、莫拉格巴尔之槌全齐",
                    "全龙吼代码瞬间习得，龙魂拉满",
                    "炉火三领地豪宅建筑材料（萨维石/粘土/铁矿）全满",
                    "全魔法派系技能等级提升至 100 级"
                ],
                "code": """; [老L·极客场景套餐] 上古卷轴5 16大魔神器与全龙吼满配包
player.additem 2ac61 1 ; 莫拉格·巴尔之槌
player.additem 240d2 1 ; 破晓者
player.additem 2ac6f 1 ; 瓦巴杰克
player.additem 63b8b 1 ; 黑暗魔经
player.additem 300300f 200 ; 萨维石
player.modav shoutrecoverymult 0 ; 龙吼零CD"""
            }
        ],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】上古卷轴5 天际重制版 控制台说明
echo ========================================================
echo   【老L·单机避坑局】天际重制版 控制台说明
echo   本脚本只检查游戏主程序在不在，不改任何文件
echo ========================================================
echo.
if not exist "SkyrimSE.exe" (
    echo [!] 当前目录下没有 SkyrimSE.exe，脚本什么都没改。
    echo     请把本脚本放到 Skyrim Special Edition 游戏安装根目录再运行。
    echo.
    pause
    exit /b
)
echo [+] 找到 SkyrimSE.exe
echo [i] 进游戏按 ~ (波浪键) 呼出控制台；没反应就先切到英文输入法。
echo [i] FormID 开头的 0 可以省略，比如 player.additem 0000000F 100 可以写成 player.additem f 100。
echo [i] 脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。
echo.
pause
"""
    },
    "fallout-4": {
        "verifiedPatch": "v1.10.984+（未实测）",
        "radarSecretCode": "辐射4",
        "pitfallNote": {
            "title": "老L避坑笔记 (辐射4 次世代更新版 v1.10.984)",
            "tips": [
                "【减少自动更新】：Steam 属性里把更新设成“仅在我启动该游戏时更新”，装了 F4SE 的话日常用 f4se_loader.exe 启动。这只能减少后台更新，不能保证游戏不被更新；更新后 F4SE 和依赖它的 Mod 可能要等作者发新版。",
                "【聚落空间无限解除】：走到工坊工作台按 ~ 选中工作台（出现 000249dc），输入 setav 349 9999999 与 setav 348 9999999，容量条瞬间清零，实现真正的无限建造！",
                "【死亡三角区闪退预防】：联邦西北角庇护山丘、红火箭与阿伯纳西农场相隔极近，切勿在三地同时高密建造几万件建筑物体，防止内存溢出导致 CTD 闪退。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "fo4_starter_bundle",
                "type": "starter",
                "name": "避难所新手起飞包",
                "tag": "👑 萌新首选 · 零门槛",
                "badge": "废土首富",
                "desc": "一键上帝模式 + 10万瓶盖启动资金 + 100个核融合核心 + 负重上限扩充至 50,000，动力装甲跑图无限续航！",
                "highlights": [
                    "tgm 上帝模式（无限生命/AP/弹药/负重）",
                    "player.additem f 100000（10 万瓶盖财务自由）",
                    "player.additem 75fe4 100（100 个满电核融合核心）",
                    "全动力装甲骨架与 X-01 顶级装甲直接体验"
                ],
                "code": """; [老L·极客场景套餐] 辐射4 避难所新手起飞包
tgm
player.additem f 100000
player.additem 75fe4 100
player.modav carryweight 50000"""
            },
            {
                "id": "fo4_salvation_bundle",
                "type": "salvation",
                "name": "聚落无限建造与大平地极速清理包",
                "tag": "🏗️ 废土基建 · 赛博主城",
                "badge": "无限基建",
                "desc": "瞬间解除右上角聚落容量预算上限 + 一键拆解全图废墟杂草转化为木材钢铁存入工坊，打造赛博主城！",
                "highlights": [
                    "setav 349 9999999 / 348 9999999 建造容量条瞬间清零",
                    "scrapall 领地极速清理大平地（自动回收千吨建材）",
                    "各聚落千万钢铁/混凝土/木材一秒到账",
                    "聚落招募天花板解除"
                ],
                "code": """; [老L·极客场景套餐] 辐射4 聚落无限建造指令
; 走到工坊工作台正前方，按 ~ 点击工作台，输入：
setav 349 9999999
setav 348 9999999
; 极速清理当前领地杂草废墟（使用前请先存档）：
scrapall"""
            },
            {
                "id": "fo4_godmode_bundle",
                "type": "godmode",
                "name": "全传奇双弹附魔与核融合满配包",
                "tag": "⚡ 极客狂欢 · 废土霸主",
                "badge": "联邦霸主",
                "desc": "手持武器直接附魔【双弹 / 爆裂 / 煽动 / 无尽】传奇前缀 + 胖子核弹与高斯步枪满配，横扫废土发光海！",
                "highlights": [
                    "attachmod 1cc2a6（直接为当前武器附魔【双弹】词条）",
                    "attachmod 1e7173（附魔【爆裂】每发额外 15 点面伤爆炸）",
                    "attachmod 1f04b8（附魔【煽动】对满血目标双倍伤害）",
                    "迷你核弹与千发 2mm 电磁弹药即刻到账"
                ],
                "code": """; [老L·极客场景套餐] 辐射4 传奇武器词条自定义附魔
; 按 ~ 鼠标左键点击自己扔在地上的武器，输入：
attachmod 1cc2a6 ; 附魔【双弹 (Two Shot)】
; 补给 100 发胖子核弹与高斯步枪弹药：
player.additem e6b2e 100
player.additem 18abdf 500"""
            }
        ],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】辐射4 F4SE 启动说明
echo ========================================================
echo   【老L·单机避坑局】辐射4 F4SE 启动说明
echo   本脚本只检查有没有 f4se_loader.exe，不改任何文件
echo ========================================================
echo.
if not exist "Fallout4.exe" (
    echo [!] 当前目录下没有 Fallout4.exe，脚本什么都没改。
    echo     请把本脚本放到 Fallout 4 游戏安装根目录再运行。
    echo.
    pause
    exit /b
)
if exist "f4se_loader.exe" (
    echo [+] 找到 f4se_loader.exe：装了 F4SE 的话，日常用它启动游戏。
) else (
    echo [i] 没找到 f4se_loader.exe：还没装 F4SE，或者没放在游戏根目录。
)
echo [i] 想减少自动更新：Steam 库里右键 Fallout 4 → 属性 → 更新，设为【仅在我启动该游戏时更新】。
echo     这只能减少后台更新，不能保证游戏不被更新；更新后 F4SE 和依赖它的 Mod 可能要等作者发新版。
echo [i] 脚本不备份存档；指令没有逐条在游戏里实测，执行前先手动存档。
echo.
pause
"""
    }
}


def main():
    updates = {gid: {field: info[field] for field in OWNED_FIELDS} for gid, info in FLAGSHIP_DATA.items()}
    write_owned_fields("enrich_flagship_scenarios.py", OWNED_FIELDS, updates)


if __name__ == "__main__":
    main()
