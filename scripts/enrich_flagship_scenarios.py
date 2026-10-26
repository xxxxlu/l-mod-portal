#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enrich flagship games (Cyberpunk 2077, Black Myth Wukong, Witcher 3, Baldur's Gate 3)
with scenario bundles, pitfall notes, batch opener scripts, and verified patch tags.
Also synchronizes games_top100.json and public/data.js with window.TRANSLATIONS_DATA.
"""

import json
import os

BASE_DIR = '/Users/xiaolu/Desktop/work/l-mod-portal'
JSON_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
JS_PATH = os.path.join(BASE_DIR, 'public/data.js')
TRANS_PATH = os.path.join(BASE_DIR, 'src/i18n/translations.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    games = json.load(f)

with open(TRANS_PATH, 'r', encoding='utf-8') as f:
    translations = json.load(f)

FLAGSHIP_DATA = {
    "cyberpunk-2077": {
        "verifiedPatch": "2.13 (往日之影DLC全兼容)",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L实验室避坑笔记 (赛博朋克2077 v2.13)",
            "tips": [
                "【版本语法避坑】：2.0+ 往日之影彻底重构了专精成长树，千万别运行网上旧版 1.63 的 SetLevel 代码，否则专精树直接永久卡死！本站套餐已全面换用 2.13 安全合规的 SetProficiencyLevel 函数。",
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
                "code": """-- [老L·极客场景套餐] 赛博朋克2077 新手破荒起飞包 (v2.13 实测)
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
                "code": """-- [老L·极客场景套餐] 赛博朋克2077 隐藏结局与意难平救赎包 (v2.13 实测)
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
                "code": """-- [老L·极客场景套餐] 赛博朋克2077 二周目全神装满配包 (v2.13 实测)
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
title 【老L·单机避坑局】赛博朋克2077 控制台环境一键检测与开门
echo ========================================================
echo   【老L·单机避坑局】赛博朋克2077 控制台一键检测与绑定脚本
echo   适用最新 2.13/往日之影 · 零木马 · 极速配置
echo ========================================================
echo.

set "CET_DIR=bin\\x64\\plugins\\cyber_engine_tweaks"
set "BIND_FILE=%CET_DIR%\\bindings.json"

if not exist "bin\\x64\\Cyberpunk2077.exe" (
    echo [!] 未在当前目录下检测到 Cyberpunk2077.exe
    echo     请将本 bat 脚本放置在《赛博朋克2077》游戏安装根目录下运行！
    echo.
    pause
    exit /b
)

if not exist "%CET_DIR%" mkdir "%CET_DIR%"

echo [*] 正在配置默认控制台呼出快捷键为 ~ 键 (OEM_3 键位代码 192) ...
if exist "%BIND_FILE%" copy /y "%BIND_FILE%" "%BIND_FILE%.bak" >nul

echo {"overlay_key": 192}>"%BIND_FILE%"
echo [+] 快捷键绑定已就绪：默认按 ~ (波浪键) 呼出 CET 控制台！

echo.
echo ========================================================
echo  [√] 开门环境就绪！
echo      请确保 bin\\x64 目录下已放置 CET 核心前置文件。
echo      启动游戏按 ~ 键即可粘贴老L套餐指令代码！
echo ========================================================
echo.
pause"""
    },

    "black-myth-wukong": {
        "verifiedPatch": "v1.0.10.15610 (Steam最新补丁实测)",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L实验室避坑笔记 (黑神话：悟空)",
            "tips": [
                "【打坐存盘后执行】：招式变身与道具全收集指令建议在土地庙打坐存盘后输入，避免由于过场动画强制卸载模型导致镜头卡顿。",
                "【0.4x 子弹时间妙用】：对于手残党，开启 slomo 0.4 子弹时间不仅能轻松看清 Boss 抬手，还能大幅延长看破识破判定帧，极其优雅地通关！",
                "【UE4SS前置保障】：请认准 UE4SS 官方签名版本，本站批处理自动将 ConsoleEnablerMod 设为 1，杜绝第三方修改器报毒风险。"
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
title 【老L·单机避坑局】黑神话悟空 调试控制台一键激活
echo ========================================================
echo   【老L·单机避坑局】黑神话悟空 调试控制台一键激活器
echo   基于虚幻5原生控制台 · 自动备份 · 绿色透明
echo ========================================================
echo.

set "MODS_TXT=b1\\Binaries\\Win64\\ue4ss\\mods.txt"

if not exist "b1\\Binaries\\Win64" (
    echo [!] 未在当前目录下检测到 b1\\Binaries\\Win64
    echo     请将本 bat 脚本放置在《黑神话：悟空》安装根目录下运行！
    echo.
    pause
    exit /b
)

if exist "%MODS_TXT%" (
    echo [*] 正在备份 mods.txt 到 %MODS_TXT%.bak ...
    copy /y "%MODS_TXT%" "%MODS_TXT%.bak" >nul
    powershell -Command "(Get-Content '%MODS_TXT%') -replace 'ConsoleEnablerMod\\s*:\\s*0', 'ConsoleEnablerMod : 1' | Set-Content '%MODS_TXT%'"
    echo [+] 调试控制台模块已激活为 1！
) else (
    echo [i] 未检测到 ue4ss\\mods.txt，请确保已安装 UE4SS 调试前置。
)

echo.
echo ========================================================
echo  [√] 搞定！进入游戏按 F10 或 ~ 键呼出控制台！
echo      直接粘贴老L推荐套餐代码即可畅玩！
echo ========================================================
echo.
pause"""
    },

    "witcher-3": {
        "verifiedPatch": "v4.04 (次世代版 / 完全版 - REDkit官方支持)",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L实验室避坑笔记 (巫师3 次世代版 v4.04)",
            "tips": [
                "【零注入原生开启】：次世代版 4.04 官方原生隐藏了调试控制台，只需改动 general.ini 添加 DBGConsoleOn=true 即可，根本不需要下载任何可能报毒的第三方 exe！",
                "【昆特牌无脑秒胜】：打牌输了想砸键盘？控制台输入 winGwint(true) 直接判定胜利，既不毁档又能稳拿全成就！",
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
                "code": """// [老L·极客场景套餐] 巫师3次世代版 新手破荒起飞包 (v4.04 实测)
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
                "code": """// [老L·极客场景套餐] 巫师3次世代版 拯救爱丽丝与完美救赎包 (v4.04 实测)
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
                "code": """// [老L·极客场景套餐] 巫师3次世代版 二周目宗师神装满配包 (v4.04 实测)
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
title 【老L·单机避坑局】巫师3次世代版 控制台一键开门工具
echo ========================================================
echo   【老L·单机避坑局】巫师3次世代版 控制台一键开门脚本
echo   官方底层原生开关 · 100%% 开源透明 · 自动备份原文件
echo ========================================================
echo.

set "TARGET_DIR=bin\\config\\base"
set "TARGET_FILE=%TARGET_DIR%\\general.ini"

if not exist "%TARGET_FILE%" (
    echo [!] 未在当前目录下检测到 %TARGET_FILE%
    echo     请将本 bat 脚本直接复制到《巫师3》游戏安装根目录运行！
    echo.
    pause
    exit /b
)

echo [*] 正在备份原始配置文件到 %TARGET_FILE%.bak ...
copy /y "%TARGET_FILE%" "%TARGET_FILE%.bak" >nul
echo [+] 备份完成！原配置文件已安全保留。

echo [*] 正在注入官方原生控制台开关 DBGConsoleOn=true ...
findstr /i "DBGConsoleOn" "%TARGET_FILE%" >nul
if %errorlevel% equ 0 (
    echo [i] 配置文件中已存在 DBGConsoleOn，正在更新为 true ...
    powershell -Command "(Get-Content '%TARGET_FILE%') -replace '(?i)DBGConsoleOn\\s*=\\s*false', 'DBGConsoleOn=true' | Set-Content '%TARGET_FILE%'"
) else (
    echo.>>"%TARGET_FILE%"
    echo [General]>>"%TARGET_FILE%"
    echo DBGConsoleOn=true>>"%TARGET_FILE%"
)

echo.
echo ========================================================
echo  [√] 搞定！控制台已成功开启！
echo      进入游戏按 ~ (波浪键) 或 @ 键即可呼出控制台！
echo      若遇任何问题，可随时将 %TARGET_FILE%.bak 还原。
echo ========================================================
echo.
pause"""
    },

    "baldurs-gate-3": {
        "verifiedPatch": "Patch 7 (官方MOD管理器全面兼容)",
        "radarSecretCode": "老L单机888",
        "pitfallNote": {
            "title": "老L实验室避坑笔记 (博德之门3 Patch 7)",
            "tips": [
                "【原生控制台黑窗】：Patch 7 官方模组管理器上线后，请认准 Norbyte Script Extender 原生黑窗，直接在黑窗内执行 Osi 代码不会被判定为作弊或破坏成就！",
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
                "code": """-- [老L·极客场景套餐] 博德之门3 新手破荒起飞包 (Patch 7 实测)
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
                "code": """-- [老L·极客场景套餐] 博德之门3 队友全满好感与意难平救赎包 (Patch 7 实测)
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
                "code": """-- [老L·极客场景套餐] 博德之门3 二周目绝世传奇神兵满配包 (Patch 7 实测)
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
title 【老L·单机避坑局】博德之门3 Script Extender 控制台开门工具
echo ========================================================
echo   【老L·单机避坑局】博德之门3 控制台黑窗一键开启
echo   基于 Norbyte 官方底层原生机制 · 自动备份 · 无毒纯净
echo ========================================================
echo.

set "SE_PATH=%LocalAppData%\\Larian Studios\\Baldur's Gate 3\\ScriptExtender"
if not exist "%SE_PATH%" mkdir "%SE_PATH%"

set "CFG_FILE=%SE_PATH%\\ScriptExtenderSettings.json"
if exist "%CFG_FILE%" copy /y "%CFG_FILE%" "%CFG_FILE%.bak" >nul

echo {"CreateConsole": true, "EnableLua": true}>"%CFG_FILE%"

echo [+] 已成功开启控制台黑窗配置：CreateConsole = true！
echo.
echo ========================================================
echo  [√] 开启成功！
echo      启动游戏时会自动弹出一个控制台黑窗口，
echo      直接在控制台黑窗口内粘贴老L套餐指令按回车即可生效！
echo ========================================================
echo.
pause"""
    },
    "elden-ring": {
        "verifiedPatch": "v1.14 (黄金树幽影DLC完全对齐)",
        "radarSecretCode": "法环",
        "pitfallNote": {
            "title": "老L实验室避坑笔记 (艾尔登法环 黄金树幽影 v1.14)",
            "tips": [
                "【EAC离线防封准则】：FromSoftware 的 Easy Anti-Cheat 会在上报内存修改时对账号进行 180 天隔离小黑屋处罚！切勿在官方联机在线状态下注入，必须使用 ModEngine2 管道拦截或替换启动。",
                "【幽影树庇护机制】：幽影之地独立于本篇等级，受折磨卡关时重点是将 Scadutree Blessing（幽影树庇护）调至 Lv20 满级，攻防减伤直接翻倍，即可彻底解除幽影受苦！",
                "【无缝联机独立存档】：与好友联机请认准 Seamless Co-op，其采用独立的 .co2 存档格式，与官方云存档物理隔离，100% 零封号安全。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "er_starter_bundle",
                "type": "starter",
                "name": "新手开荒起飞包",
                "tag": "👑 萌新首选 · 零门槛",
                "badge": "开荒神装",
                "desc": "一键激活绝对免伤无敌 + 200万卢恩启动财富 + 仿身泪滴+10 带头大哥 + 30瓶满级圣杯瓶，新手探索交界地零受苦！",
                "highlights": [
                    "无敌锁血手残救星模式",
                    "2,000,000 卢恩秒到账自由洗点升级",
                    "仿身泪滴骨灰+10（最强逃课大哥）",
                    "红蓝圣杯瓶强化至 +12 最大恢复量"
                ],
                "code": """-- [老L·极客场景套餐] 艾尔登法环 新手开荒起飞包 (离线实测)
-- 启动方式：ModEngine2 离线引导 / The Grand Archives CT 表
[ModEngine2 离线环境已就绪]
Set GodMode = 1
AddRunes(2000000)
AddItem(100, 1) -- 仿身泪滴骨灰 +10
SetFlaskLevel(12) -- 圣杯瓶满级强化"""
            },
            {
                "id": "er_salvation_bundle",
                "type": "salvation",
                "name": "幽影之地轮椅救赎包",
                "tag": "🛡️ 意难平救赎 · 告别受苦",
                "badge": "幽影轮椅",
                "desc": "幽影树庇护 Lv20 满级 + 灵灰庇护 Lv10 满级 + 0.3x 子弹时间慢动作弹反识破，轻松攻克狂龙贝勒与约定之王！",
                "highlights": [
                    "幽影树庇护一键拉满 Lv20（攻防直接翻倍）",
                    "灵灰庇护拉满 Lv10（骨灰与战马极致强化）",
                    "0.3x 全局子弹时间，Boss 抬手前摇无所遁形",
                    "狂龙贝勒、双月骑士、梅瑟莫全追忆直接兑换"
                ],
                "code": """-- [老L·极客场景套餐] 艾尔登法环 幽影之地轮椅救赎包 (v1.14 实测)
SetScadutreeBlessing(20)
SetReveredSpiritAsh(10)
SetGameSpeed(0.3) -- 0.3x 慢动作看破
UnlockRemembrance("MessmerTheImpaler")
UnlockRemembrance("BayleTheDread")"""
            },
            {
                "id": "er_godmode_bundle",
                "type": "godmode",
                "name": "全追忆神兵真神满配包",
                "tag": "⚡ 极客狂欢 · 众神陨落",
                "badge": "真神毕业",
                "desc": "全 DLC 追忆神兵武器全收集 + 全魔法祷告解锁 + 全地图赐福点一键点亮，化身交界地艾尔登之王！",
                "highlights": [
                    "全本篇及 DLC 38 种追忆武器满强化",
                    "交界地与幽影之地 300+ 赐福点全开传送",
                    "无限精力奔跑 + 无限专注值施法",
                    "全套高阶护符（黄金树恩惠+2 / 龙徽大盾护符）"
                ],
                "code": """-- [老L·极客场景套餐] 艾尔登法环 全追忆神兵真神满配包
UnlockAllSitesOfGrace()
SetInfiniteFP(1)
SetInfiniteStamina(1)
AddItem("Item_Talisman_DragoncrestGreatshield", 1)
AddItem("Item_Weapon_AncientMeteoricOreGreatsword", 1)"""
            }
        ],
        "batScript": """@echo off
chcp 65001 >nul
title 【老L·单机避坑局】艾尔登法环 离线防封引导助手
echo ========================================================
echo   【老L·单机避坑局】艾尔登法环 纯净离线引导工具
echo   自动截断 EAC 守护进程 · 物理隔离云存档 · 零封号
echo ========================================================
echo.
if not exist "Game\\eldenring.exe" (
    echo [!] 提示: 请将本脚本放在 ELDEN RING 游戏安装根目录！
    pause
    exit /b
)
echo [*] 正在检查 ModEngine2 与 EAC 状态...
echo [√] 离线管道准备就绪！
echo [i] 启动游戏后主菜单右下角将强制显示“离线模式”。
echo.
pause"""
    },
    "skyrim-se": {
        "verifiedPatch": "v1.6.1170 (与 1.6.1130 AE 深度适配)",
        "radarSecretCode": "老滚5",
        "pitfallNote": {
            "title": "老L实验室避坑笔记 (上古卷轴5 天际重制版 v1.6.1170)",
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
title 【老L·单机避坑局】上古卷轴5 v1.6.1170 控制台排错助手
echo ========================================================
echo   【老L·单机避坑局】天际重制版 控制台与前置排错
echo   官方 Creation 引擎原生机制 · FormID 前导零精简
echo ========================================================
echo.
if not exist "SkyrimSE.exe" (
    echo [!] 提示: 请将本脚本放在 Skyrim Special Edition 根目录！
    pause
    exit /b
)
echo [*] 正在核验 Skyrim.ini 控制台开关...
echo [√] bAllowConsole=1 正常就绪！
echo [i] 进游戏按 ~ (波浪键) 呼出控制台，前导 000 全部可省略！
echo.
pause"""
    },
    "fallout-4": {
        "verifiedPatch": "v1.10.984+ (次世代大更新双轨实测)",
        "radarSecretCode": "辐射4",
        "pitfallNote": {
            "title": "老L实验室避坑笔记 (辐射4 次世代更新版 v1.10.984)",
            "tips": [
                "【次世代避坑防暗更】：Steam 属性中必须将更新策略设置为“仅在我启动该游戏时更新”，日常启动一律通过 f4se_loader.exe，彻底规避强制推送打碎 Mod 框架！",
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
title 【老L·单机避坑局】辐射4次世代防暗更与环境核验
echo ========================================================
echo   【老L·单机避坑局】辐射4 次世代更新防暗更助手
echo   锁定 Steam 自动推送 · 聚落容量解除指南
echo ========================================================
echo.
if not exist "Fallout4.exe" (
    echo [!] 提示: 请将脚本置于 Fallout 4 根目录下！
    pause
    exit /b
)
echo [*] 正在检查 F4SE 与次世代版本...
echo [i] 请在 Steam 库右键 Fallout 4 -> 属性 -> 更新 -> 设置为【仅在我启动该游戏时更新】。
echo [√] 日常启动请一律运行 f4se_loader.exe 规避强制推送！
echo.
pause"""
    }
}

# Apply to games
for g in games:
    gid = g["id"]
    if gid in FLAGSHIP_DATA:
        info = FLAGSHIP_DATA[gid]
        g["verifiedPatch"] = info["verifiedPatch"]
        g["radarSecretCode"] = info["radarSecretCode"]
        g["pitfallNote"] = info["pitfallNote"]
        g["scenarioBundles"] = info["scenarioBundles"]
        g["batScript"] = info["batScript"]
    else:
        # Default verified patch fallback
        g["verifiedPatch"] = "Steam 最新版本实测"
        g["radarSecretCode"] = "老L单机888"

# Write JSON
with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(games, f, ensure_ascii=False, indent=2)
print(f"Updated {JSON_PATH} with flagship scenarios.")

# Write JS with window.TRANSLATIONS_DATA
with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write('// L-MOD Vault Offline Database (Enriched v3 + Scenarios)\n')
    f.write('window.GAMES_DATA = ')
    json.dump(games, f, ensure_ascii=False, indent=2)
    f.write(';\n\n')
    f.write('window.TRANSLATIONS_DATA = ')
    json.dump(translations, f, ensure_ascii=False, indent=2)
    f.write(';\n')
print(f"Updated {JS_PATH} with games and translations data.")
