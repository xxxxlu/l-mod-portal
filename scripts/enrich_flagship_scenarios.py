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
                "【CET热键防呆】：首次进入游戏按 ~ 键（或你自己绑定的键）没反应，可以先切换到英文输入法（Caps Lock 关闭）试试；CET 官方安装要求游戏开在无边框窗口模式下运行，独占全屏模式下可能呼不出来。"
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
                "【UE4SS 前置】：UE4SS 去它的 GitHub 发布页下载。本站的 .bat 会把 mods.txt 里的 ConsoleEnablerMod 从 0 改成 1（改之前会另存 mods.txt.bak）；如果 mods.txt 里没有这一行，要自己手动加一行。"
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
echo  [i] 进游戏按 F10 试试控制台。
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
                "【零注入原生开启】：次世代版 4.04 官方原生隐藏了调试控制台，只需改动 general.ini 添加 DBGConsoleOn=true 即可，不需要下载任何第三方 exe。",
                "【昆特牌速胜】：打牌输了想砸键盘？控制台输入 winGwint(true) 可以直接判定赢下当前这局牌（执行前先存档）。",
                "【把紫玫瑰要回来】：石之心 DLC 剧情里如果把紫色玫瑰（Violet rose）这个任务道具交出去了，可以用控制台补一支回背包：additem('Violet rose')（执行前先存档）。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "w3_starter_bundle",
                "type": "starter",
                "name": "新手入门指令包",
                "tag": "萌新入门",
                "badge": "入门套装",
                "desc": "开启上帝模式 + 提升攻击伤害 + 获得 100,000 克朗 + 解锁全部快速旅行路标 + 解除路标距离限制，用于快速搭建一个轻松的游戏环境。",
                "highlights": [
                    "god 开启上帝模式（杰洛特免疫伤害）",
                    "likeaboss 攻击伤害变为敌方最大生命值的 40%（不影响杰洛特受到的伤害）",
                    "addmoney(100000) 增加 100,000 克朗",
                    "ShowAllFT(1) 解锁全部快速旅行路标",
                    "AllowFT(1) 解除路标限制，可在地图任意已探索位置直接快速旅行",
                    "大红/大蓝/大绿突变诱发物各 10 个"
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
                "【Script Extender 控制台】：Patch 7 有了官方模组管理器，但控制台还是要靠 Norbyte 的 Script Extender。它默认开着 EnableAchievements，就是用来恢复装 Mod 后的成就的；用控制台具体会不会影响成就没有人核实过，执行前先存档。",
                "【长休不用囤太多补给】：长休 (Long Rest) 只要凑够 40 点营地补给 (Camp Supplies) 就会触发——一份 Supply Pack 本身就有 40 点；战术难度 (Tactician) 门槛是 80 点，自定义难度最高到 120 点。凑够门槛后全队就会回满生命值和法术位，补给囤得比门槛还多也不会有额外效果。",
                "【队友好感时机】：BG3 官方 Osiris 文档里没有 SetAttitude 这个改好感度的函数——Attitude 管的是 NPC 交易价格，队友好感用的是 ChangeApprovalRating。建议在第一章营地初次对话后再用它改好感，比较容易触发影心、阿斯代伦、盖尔等人的好感剧情，也能避开剧情好感上限卡住的情况。执行前先存档。"
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
echo      设置文件放在 bin 目录，依据是 Norbyte/bg3se 官方 README 的配置项说明表。
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
                "【EAC 与封号】：FromSoftware 的 Easy Anti-Cheat 检测到内存修改会对账号做处罚，具体处罚时长官方没有公开说明，网上流传的天数也无法确认。切勿在官方联机在线状态下注入，改游戏只在离线下进行（用 ModEngine2 或替换启动的方式不加载 EAC，只能离线玩）。",
                "【幽影树庇护机制】：幽影之地的难度主要看幽影树庇护（Scadutree Blessing），它和角色等级分开计算。在赐福点使用收集到的幽影树碎片可以提升庇护，提高造成的伤害、降低受到的伤害；它只在幽影之地生效。卡关时优先找碎片。",
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
                "【FormID省略前导零】：控制台输入代码时，前导的 0 可以全部省略。比如金币的 FormID 是 0000000F，直接输入 player.additem f 100000 也能生效。",
                "【别随手跑 caqs】：任务卡关不要图省事运行 caqs（强制推进全游戏的任务进度）——UESP 上写的是“不建议日常使用，可能导致游戏崩溃”，卡关应该用 setstage <QuestID> <Stage> 针对性处理具体那个任务。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "skyrim_starter_bundle",
                "type": "starter",
                "name": "抓根宝开荒起飞包",
                "tag": "👑 萌新首选 · 零门槛",
                "badge": "天际首富",
                "desc": "开启上帝模式 + 立即获得 10 万金币 + 负重上限提升至 50,000 + 可用于脱离卡住的地形，方便新手开局。",
                "highlights": [
                    "tgm 上帝模式（角色免疫伤害，耐力与魔法不消耗，负重不受限制）",
                    "player.additem f 100000（获得 10 万金币）",
                    "player.modav carryweight 50000（提升负重上限）",
                    "tcl 穿墙开关（可用于脱离卡住的地形）"
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
                "tag": "🛠️ 坏档急救",
                "badge": "急救工具",
                "desc": "用于解决任务 NPC 卡死不动、复活重要随从、快速进入官方测试房间等情况。",
                "highlights": [
                    "resurrect 1（点击NPC尸体使其复活并回满生命值）",
                    "coc qasmoke（传送到官方测试房间；输入 coc riverwood 返回溪木镇）",
                    "setstage 用于强制推进卡住的任务",
                    "tai / tcai 用于解除 NPC 的 AI 死锁状态"
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
                "【聚落建造空间不够用】：走到工坊按 ~ 选中工作台（会出现类似 000249dc 的编号）；349 是三角面数量的建造上限，调大它（比如 setav 349 9999999）能放宽建造上限；348 是当前已经用掉的量，想腾地方要把它调小（比如 setav 348 0），调大 348 只会让游戏以为你已经把预算用满，别调反了。"
            ]
        },
        "scenarioBundles": [
            {
                "id": "fo4_starter_bundle",
                "type": "starter",
                "name": "避难所新手起飞包",
                "tag": "👑 萌新首选 · 零门槛",
                "badge": "废土首富",
                "desc": "开启上帝模式 + 获得 10 万瓶盖 + 100 个核聚变核心 + 负重上限提升至 50,000，适合动力装甲长时间探索。",
                "highlights": [
                    "tgm 上帝模式（角色免疫伤害，行动点与弹药不受限制）",
                    "player.additem f 100000（获得 10 万瓶盖）",
                    "player.additem 75fe4 100（获得 100 个满电核聚变核心）",
                    "负重上限提升，方便携带动力装甲骨架与 X-01 装甲"
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
