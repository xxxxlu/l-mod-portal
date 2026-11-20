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
        "scenarioBundles": [],
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
        "scenarioBundles": [],
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
        "scenarioBundles": [],
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
