#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/render_cards_png.py
L-MOD Vault 社交矩阵工业级高清出图与首发分发物料总装引擎 (Milestone 2)

功能职责：
1. 批量渲染 7 款旗舰游戏的 5 联图（1080x1440，3:4 竖图，小红书 / B 站规格）；
2. 输出分发物料包，包含小红书文案、B站动态/专栏；
3. 输出运营手册 (OPERATION_PLAYBOOK.md)；
4. 发布文案过一遍平台用词替换（只换说法，不许换出没做过的承诺）。

口径（2026-11-19 起，与网站 / README / 雷达页一致，只写做到的事）：
- 没有人逐条在游戏里试过这些指令和 Mod，不写「实测 / 亲测 / 已校验 / 认证 / 对齐最新补丁」；
- 7 款里只有 2077 / 黑神话 / 巫师3 / 博德3 的 .bat 会改配置文件，改之前另存 .bak；
  法环 / 老滚5 / 辐射4 的 .bat 只检查目录、打印提示；所有脚本都不备份存档；
- 没有网盘包、没有「一键还原 / 一键卸载」脚本、没有测试机，不写「秒推 / 秒领 / 连夜更新」；
- 避坑雷达每天比对一次 Steam 更新时间，不做实机测试，只说「可能」；
- 不写「零封号 / 零闪退 / 零报毒 / 100%」。

只写社媒产物，不读不写 data.js：
- PNG 卡片写 social_distribution/ 和 public/social_distribution/ 两处（站点页面要引用）；
- 两份发布文案和 OPERATION_PLAYBOOK.md 是运营资料，只写 private/social_ops/
  （.gitignore 已排除，不进公开仓库，也不随站点发布）。
"""

import io
import os
import sys
import json
import re
import math
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# 基础目录定位
BASE_DIR = Path(__file__).resolve().parent.parent
DISTRIBUTION_DIR = BASE_DIR / "social_distribution"
# 站点从 public/ 发布，首页和雷达页直接引用 public/social_distribution/ 下的 PNG，
# 两份必须一致，所以出图时同时写镜像（以前靠手工拷贝，容易一份新一份旧）。
PUBLIC_MIRROR_DIR = BASE_DIR / "public" / "social_distribution"
OUTPUT_DIRS = [DISTRIBUTION_DIR, PUBLIC_MIRROR_DIR]
# 发布文案和运营手册是运营资料，不进公开仓库（private/ 在 .gitignore 里）
PRIVATE_OPS_DIR = BASE_DIR / "private" / "social_ops"

# ==============================================================================
# 1. 字体配置 (精准匹配 macOS 系统内置高品质中英文字体)
# ==============================================================================
FONT_PATHS = {
    "chinese_bold": "/System/Library/Fonts/STHeiti Medium.ttc",
    "chinese_regular": "/System/Library/Fonts/STHeiti Light.ttc",
    "chinese_alt": "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "mono": "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
}

def load_fonts():
    """按层级初始化高精度排版字体字典"""
    fonts = {}
    c_bold = FONT_PATHS["chinese_bold"]
    c_reg = FONT_PATHS["chinese_regular"]
    mono_p = FONT_PATHS["mono"]

    fonts["h1"] = ImageFont.truetype(c_bold, 52)
    fonts["h2"] = ImageFont.truetype(c_bold, 40)
    fonts["h3"] = ImageFont.truetype(c_bold, 30)
    fonts["body_bold"] = ImageFont.truetype(c_bold, 24)
    fonts["body"] = ImageFont.truetype(c_reg, 24)
    fonts["body_sm"] = ImageFont.truetype(c_reg, 20)
    fonts["tag"] = ImageFont.truetype(c_bold, 20)
    fonts["tag_sm"] = ImageFont.truetype(c_bold, 16)
    fonts["code"] = ImageFont.truetype(mono_p, 23)
    fonts["code_sm"] = ImageFont.truetype(mono_p, 19)
    fonts["keycap"] = ImageFont.truetype(c_bold, 30)
    fonts["seal_title"] = ImageFont.truetype(c_bold, 18)
    fonts["seal_sub"] = ImageFont.truetype(mono_p, 16)
    return fonts

FONTS = load_fonts()

# ------------------------------------------------------------------------------
# 字形过滤：系统黑体没有 emoji 和 ✗ ➔ 等符号，直接画会变成方块（旧卡片上的 □ 就是这么来的）。
# 画字前按字体的 cmap 去掉画不出来的字符，能换的换成近似字符。
# ------------------------------------------------------------------------------
GLYPH_FALLBACKS = {"➔": "→", "✗": "×", "✔": "√", "✓": "√"}
_CMAP_CACHE = {}

def _font_cmap(font):
    path = getattr(font, "path", None)
    if not path:
        return None
    if path not in _CMAP_CACHE:
        try:
            from fontTools.ttLib import TTCollection, TTFont
            if str(path).lower().endswith(".ttc"):
                _CMAP_CACHE[path] = set(TTCollection(path).fonts[0].getBestCmap())
            else:
                _CMAP_CACHE[path] = set(TTFont(path).getBestCmap())
        except Exception:
            _CMAP_CACHE[path] = None  # 没有 fontTools 就不过滤
    return _CMAP_CACHE[path]

def renderable(text, font):
    cmap = _font_cmap(font) if font is not None else None
    if cmap is None or not text:
        return text
    out = []
    for ch in str(text):
        ch = GLYPH_FALLBACKS.get(ch, ch)
        if ch in "\n\t" or ord(ch) in cmap:
            out.append(ch)
    return "".join(out).strip()

# 画布内可写区域（外框 20~1060，内容区 60~1020）；超出的文字记下来，出图结束时报出来
CONTENT_LEFT, CONTENT_RIGHT = 56, 1024
OVERFLOW_LOG = []

class SafeDraw(ImageDraw.ImageDraw):
    """画字前过滤画不出的字符，并检查有没有写出内容区。"""
    current_card = ""

    def textbbox(self, xy, text, *args, **kwargs):
        return super().textbbox(xy, renderable(text, kwargs.get("font")), *args, **kwargs)

    def text(self, xy, text, *args, **kwargs):
        font = kwargs.get("font")
        clean = renderable(text, font)
        super().text(xy, clean, *args, **kwargs)
        if clean:
            box = super().textbbox(xy, clean, font=font, anchor=kwargs.get("anchor"))
            if box[0] < CONTENT_LEFT or box[2] > CONTENT_RIGHT:
                OVERFLOW_LOG.append(f"{self.current_card}: x={box[0]}~{box[2]} 「{clean}」")

# ==============================================================================
# 2. 发布文案用词替换表：在 private/social_ops/word_map.json（不进仓库），没有就原样输出
# ==============================================================================
from social_word_map import load_word_map

DESENSITIZATION_MAP = load_word_map("regex")

def sanitize_text(text: str) -> str:
    """按用词替换表替换（表不在仓库里，没有就原样返回）"""
    if not text:
        return ""
    result = str(text)
    for pattern, repl in DESENSITIZATION_MAP:
        result = re.sub(pattern, repl, result, flags=re.IGNORECASE)
    return result

# ==============================================================================
# 3. 旗舰游戏极客视觉与物料总装数据字典
# ==============================================================================
FLAGSHIP_GAMES = {
    "cyberpunk-2077": {
        "dir_name": "01_cyberpunk-2077",
        "title": "赛博朋克 2077 (Cyberpunk 2077)",
        "short_title": "赛博朋克2077",
        "game_folder": "Cyberpunk 2077",
        "secret_code": "2077",
        "radar_code": "老L单机888",
        "colors": {
            "primary": (252, 238, 10),      # Cyberpunk Yellow
            "secondary": (0, 240, 255),     # Neon Cyan
            "accent": (255, 0, 85),         # Neon Magenta / Crimson
            "bg_top": (10, 11, 17),
            "bg_bottom": (16, 18, 28),
            "card_bg": (19, 23, 34),
            "card_border": (38, 48, 68),
            "code_bg": (8, 10, 15),
            "text_white": (245, 247, 250),
            "text_muted": (148, 163, 184),
            "text_dim": (100, 116, 139),
        },
        "hook_card": {
            "eyebrow": "【开源 CET 框架 · 深度解密】",
            "title_line1": "2077 也能开控制台！",
            "title_line2": "不用来路不明的修改器",
            "pain_points": [
                "来路不明的修改器可能捆绑弹窗或后门，杀毒软件经常报毒",
                "游戏一更新，按内存地址改数据的工具常常失效甚至闪退",
                "乱改内存可能把存档弄坏，出了问题很难查是哪一步"
            ],
            "solution": "开源 CET 框架 · 源码公开 · 不用来路不明的 exe",
            "features": [
                ("⚡ 打开控制台", "无需安装独立 exe，解压开源的 CET 框架即可唤醒控制台"),
                ("🎮 场景化逃课套餐", "手残救星模式、全图鉴解锁、隐藏死神结局救赎"),
                ("🛡️ 游戏更新以后", "CET 跟着游戏版本适配，大更新后可能要等作者发新版")
            ]
        },
        "setup_card": {
            "title": "小白 3 步开启 CET 控制台",
            "subtitle": "无需编程基础 · 开源框架 · 源码公开",
            "steps": [
                {
                    "step": "STEP 01",
                    "title": "定位游戏安装根目录",
                    "detail": "Steam 客户端 ➔ 库中右键游戏 ➔ 【管理】 ➔ 【浏览本地文件】",
                    "path_box": "SteamLibrary/steamapps/common/Cyberpunk 2077/"
                },
                {
                    "step": "STEP 02",
                    "title": "解压放入 CET 开源底层框架",
                    "detail": "将纯净开源的 Cyber Engine Tweaks 解压直接放入游戏根目录：",
                    "path_box": "bin/x64/plugins/cyber_engine_tweaks/"
                },
                {
                    "step": "STEP 03",
                    "title": "启动游戏按下快捷键唤醒",
                    "detail": "进入游戏画面后按下快捷键，屏幕上方呼出半透明控制台光标！",
                    "key_text": "~ 键 (波浪键)",
                    "key_sub": "全屏/无边框模式下呼出"
                }
            ],
            "bat_note": {
                "title": "💡 附：老L的 .bat 脚本（纯文本）",
                "bullets": [
                    "放到游戏根目录运行，先检查 bin/x64/Cyberpunk2077.exe 在不在",
                    "把 CET 呼出键设成 ~ 键；原 bindings.json 先另存为 .bak",
                    "不下载、不安装 CET 本体，CET 要自己先放好；也不备份存档"
                ],
                "footer": "👉 脚本在 L-MOD Vault 网站本游戏页，纯文本，可用记事本查看"
            }
        },
        "commands_card": {
            "title": "常用高频逃课与救赎指令清单",
            "subtitle": "呼出 CET 控制台复制粘贴回车 · 执行前先存档",
            "commands": [
                {
                    "name": "手残救星 · 剧情体验模式",
                    "code": "Game.GodMode(true)",
                    "note": "完全免疫伤害与硬直，专心沉浸夜之城主线与支线剧情体验"
                },
                {
                    "name": "资源自由 · 全图鉴解锁",
                    "code": 'Game.AddToInventory("Items.money", 2000000)',
                    "note": "200万欧元瞬时到账，买空夜之城全城义体医生与黑客终端"
                },
                {
                    "name": "背包减负 · 无痛探索",
                    "code": "Game.InfiniteStamina(true)",
                    "note": "无限耐力狂奔不喘气，飞檐走壁探索夜之城高低地形"
                },
                {
                    "name": "隐藏结局 · 意难平救赎",
                    "code": 'Game.GetQuestsSystem():SetFactStr("sq032_johnny_friend", 1)',
                    "note": "修复油田对话遗憾！天台静默4分钟即可触发单挑荒坂塔死神结局"
                }
            ]
        },
        "mods_card": {
            "title": "解决痛点 · 精选 Mod",
            "subtitle": "只挑解决痛点的几款 · 装之前看清版本和前置要求",
            "mods": [
                {
                    "title": "Cyber Engine Tweaks (CET)",
                    "author": "yamashi",
                    "tag": "核心底座",
                    "desc": "社区开源的脚本与控制台框架（非官方），源码公开在 GitHub"
                },
                {
                    "title": "Native Settings UI",
                    "author": "jackhumbert",
                    "tag": "设置菜单",
                    "desc": "将所有模组配置直接集成进游戏原生主菜单，无需切桌面随时调节"
                },
                {
                    "title": "Equipment-EX (衣柜外观扩展)",
                    "author": "psiberx",
                    "tag": "赛博暖暖",
                    "desc": "突破原版装备栏限制，支持30+部位自由穿搭且不影响护甲战斗属性"
                }
            ]
        },
        "cta_card": {
            "code_main": "【老L单机888】 或 【2077】"
        }
    },

    "black-myth-wukong": {
        "dir_name": "02_black-myth-wukong",
        "title": "黑神话：悟空 (Black Myth: Wukong)",
        "short_title": "黑神话悟空",
        "game_folder": "BlackMythWukong",
        "secret_code": "黑神话",
        "radar_code": "老L单机888",
        "colors": {
            "primary": (255, 183, 3),       # Mythic Gold
            "secondary": (45, 212, 191),    # Jade Teal
            "accent": (239, 68, 68),        # Vermillion Red
            "bg_top": (12, 12, 15),
            "bg_bottom": (18, 18, 24),
            "card_bg": (22, 22, 28),
            "card_border": (50, 45, 35),
            "code_bg": (9, 9, 12),
            "text_white": (245, 247, 250),
            "text_muted": (156, 163, 175),
            "text_dim": (107, 114, 128),
        },
        "hook_card": {
            "eyebrow": "【虚幻5原生机制 · 深度解密】",
            "title_line1": "黑神话手残被虎先锋劝退？",
            "title_line2": "教你开启虚幻5原生调试模式",
            "pain_points": [
                "幽魂、白衣秀士、虎先锋卡关卡到摔手柄，挫败感极强甚至退款",
                "来路不明的修改器可能报毒，游戏一更新就失效或闪退",
                "想要体验齐天大圣全法术真神力，却受限于冗长痛苦的开荒刷怪"
            ],
            "solution": "开源 UE4SS 打开引擎自带控制台 · 源码公开",
            "features": [
                ("⚡ 打开控制台", "装好开源的 UE4SS 框架，改一行配置即可唤出控制台"),
                ("🎮 场景化逃课套餐", "0.4x 子弹时间、大圣六根遗物全集齐、影神图全图鉴解锁"),
                ("🛡️ 游戏更新以后", "UE4SS 可能要等作者适配新版本；先存档，更新情况看避坑雷达")
            ]
        },
        "setup_card": {
            "title": "小白 3 步唤醒引擎控制台",
            "subtitle": "无需编程基础 · 开源框架 · 改一行配置",
            "steps": [
                {
                    "step": "STEP 01",
                    "title": "定位游戏安装根目录",
                    "detail": "Steam 客户端 ➔ 库中右键游戏 ➔ 【管理】 ➔ 【浏览本地文件】",
                    "path_box": "SteamLibrary/steamapps/common/BlackMythWukong/"
                },
                {
                    "step": "STEP 02",
                    "title": "激活 UE4SS 控制台模块",
                    "detail": "将 UE4SS 框架放置在 Win64 下，修改 mods.txt 中控制台开关：",
                    "path_box": "b1/Binaries/Win64/ue4ss/mods.txt ➔ ConsoleEnablerMod : 1"
                },
                {
                    "step": "STEP 03",
                    "title": "启动游戏按下快捷键唤醒",
                    "detail": "进入游戏画面后按下快捷键，屏幕上方呼出虚幻5原生控制台命令行！",
                "key_text": "F10 键 或 ~ 键",
                    "key_sub": "按不出来就换另一个键试试"
                }
            ],
            "bat_note": {
                "title": "💡 附：老L的 .bat 脚本（纯文本）",
                "bullets": [
                    "放到游戏根目录运行，先检查 b1/Binaries/Win64 在不在",
                    "mods.txt 先另存为 mods.txt.bak，再把 ConsoleEnablerMod 改成 1",
                    "不安装 UE4SS 本体，没装只会提示；也不备份存档"
                ],
                "footer": "👉 脚本在 L-MOD Vault 网站本游戏页，纯文本，可用记事本查看"
            }
        },
        "commands_card": {
            "title": "常用高频逃课与救赎指令清单",
            "subtitle": "呼出控制台复制粘贴回车 · 建议土地庙存盘后再执行",
            "commands": [
                {
                    "name": "手残救星 · 0.4x 子弹时间",
                    "code": "slomo 0.4",
                    "note": "从容看清 Boss 抬手前摇，识破与看破判定窗口翻倍，动作丝滑"
                },
                {
                    "name": "资源自由 · 灵蕴全图鉴解锁",
                    "code": "additem 1002 500000",
                    "note": "直接获得 50 万灵蕴财富，随心铸造装备与点化披挂药材"
                },
                {
                    "name": "天赋自由 · 99点灵光满载",
                    "code": "addtalentpoint 99",
                    "note": "棍法、奇术、身法、毫毛天赋树全部随心点满，百变神格"
                },
                {
                    "name": "隐藏结局 · 六根大圣遗物集齐",
                    "code": "alllegacy",
                    "note": "一键集齐眼看喜、耳听怒等六根遗物，直通宿命轮回真结局"
                }
            ]
        },
        "mods_card": {
            "title": "解决痛点 · 精选 Mod",
            "subtitle": "只挑解决痛点的几款 · 装之前看清版本和前置要求",
            "mods": [
                {
                    "title": "UE4SS Framework",
                    "author": "UE4SS Team",
                    "tag": "引擎底座",
                    "desc": "社区开源的虚幻引擎脚本与调试框架（非官方），控制台要靠它"
                },
                {
                    "title": "Enhanced Wukong Map (全收集地图雷达)",
                    "author": "WukongModder",
                    "tag": "地图标记",
                    "desc": "补上原版没有的地图，显示土地庙、打坐蒲团与宝箱位置"
                },
                {
                    "title": "Ultra Ultrawide (带鱼屏黑边消除)",
                    "author": "Rose",
                    "tag": "视觉增强",
                    "desc": "消除 21:9 与 32:9 带鱼屏过场动画两侧黑边，画质沉浸感翻倍"
                }
            ]
        },
        "cta_card": {
            "code_main": "【老L单机888】 或 【黑神话】"
        }
    },

    "witcher-3": {
        "dir_name": "03_witcher-3",
        "title": "巫师3：狂猎 次世代完全版 (The Witcher 3)",
        "short_title": "巫师3次世代",
        "game_folder": "The Witcher 3",
        "secret_code": "巫师3",
        "radar_code": "老L单机888",
        "colors": {
            "primary": (245, 158, 11),      # Nilfgaardian Gold
            "secondary": (56, 189, 248),    # Wolf Silver Ice
            "accent": (220, 38, 38),        # Crimson Wolf Red
            "bg_top": (11, 14, 18),
            "bg_bottom": (18, 23, 30),
            "card_bg": (20, 25, 33),
            "card_border": (45, 55, 70),
            "code_bg": (8, 11, 15),
            "text_white": (245, 247, 250),
            "text_muted": (148, 163, 184),
            "text_dim": (100, 116, 139),
        },
        "hook_card": {
            "eyebrow": "【REDengine 原生机制 · 深度解密】",
            "title_line1": "巫师3次世代隐藏官方控制台",
            "title_line2": "改一个字母逆转爱丽丝悲剧",
            "pain_points": [
                "石之心通关后交出爱丽丝玫瑰懊悔终生，支线选错导致无法挽回的悲剧",
                "到处找第三方修改器，却遇到报毒、弹窗，次世代版更新后还闪退",
                "开荒捡垃圾负重爆仓、昆特牌连输砸键盘、跑图跑断腿令人烦躁"
            ],
            "solution": "游戏自带 ini 开关 · 不装第三方程序 · 只改一个配置文件",
            "features": [
                ("⚡ 打开控制台", "无需下载任何第三方 exe，仅需在 general.ini 加一行代码"),
                ("🎮 场景化逃课套餐", "杰洛特无双模式、全大陆路标全开、爱丽丝永存信物获取"),
                ("🛡️ 游戏更新以后", "控制台开关是游戏自带的；装的 Mod 更新后可能要等作者适配")
            ]
        },
        "setup_card": {
            "title": "小白 3 步唤醒官方隐藏控制台",
            "subtitle": "无需编程基础 · 不装第三方程序 · 游戏自带开关",
            "steps": [
                {
                    "step": "STEP 01",
                    "title": "定位游戏安装根目录",
                    "detail": "Steam 客户端 ➔ 库中右键游戏 ➔ 【管理】 ➔ 【浏览本地文件】",
                    "path_box": "SteamLibrary/steamapps/common/The Witcher 3/"
                },
                {
                    "step": "STEP 02",
                    "title": "修改原生 general.ini 配置文件",
                    "detail": "记事本打开 bin/config/base/general.ini，在 [General] 下加一行：",
                    "path_box": "bin/config/base/general.ini ➔ DBGConsoleOn=true"
                },
                {
                    "step": "STEP 03",
                    "title": "启动游戏按下快捷键唤醒",
                    "detail": "进入游戏后按下快捷键，屏幕上方即刻出现官方原生调试控制台！",
                    "key_text": "~ 键 (波浪键) 或 @ 键",
                    "key_sub": "次世代完全版原生支持"
                }
            ],
            "bat_note": {
                "title": "💡 附：老L的 .bat 脚本（纯文本）",
                "bullets": [
                    "放到游戏根目录运行，先检查 bin/config/base/general.ini 在不在",
                    "general.ini 先另存为 general.ini.bak，再写入 DBGConsoleOn=true",
                    "想还原就把 .bak 改回原名；不碰别的文件，也不备份存档"
                ],
                "footer": "👉 脚本在 L-MOD Vault 网站本游戏页，纯文本，可用记事本查看"
            }
        },
        "commands_card": {
            "title": "常用高频逃课与救赎指令清单",
            "subtitle": "呼出控制台复制粘贴回车 · 执行前先存档",
            "commands": [
                {
                    "name": "手残救星 · 猎魔人无双体验",
                    "code": "god",
                    "note": "杰洛特完全无敌状态，从容欣赏次世代光追与跌宕起伏的魔幻叙事"
                },
                {
                    "name": "资源自由 · 10万克朗到账",
                    "code": "addmoney(100000)",
                    "note": "直接获得 10 万克朗，轻松打造宗师级学派套装与白鸦葡萄园翻新"
                },
                {
                    "name": "背包减负 · 随时随地自由传送",
                    "code": "ShowAllFT(1) & AllowFT(1)",
                    "note": "全大陆快速旅行路标全开，解除野外路标限制，随时随地一键传送"
                },
                {
                    "name": "隐藏结局 · 拯救爱丽丝信物",
                    "code": "additem('Iris Rose') & additem('Aerondight EP2')",
                    "note": "让爱丽丝的紫色玫瑰与成长神剑湖女之剑永存杰洛特背包与葡萄园"
                }
            ]
        },
        "mods_card": {
            "title": "解决痛点 · 精选 Mod",
            "subtitle": "只挑解决痛点的几款 · 装之前看清版本和前置要求",
            "mods": [
                {
                    "title": "Community Patch Base",
                    "author": "W3 Community",
                    "tag": "社区前置",
                    "desc": "社区做的脚本合并与冲突修复前置，减少脚本红字报错"
                },
                {
                    "title": "Fast Travel from Anywhere",
                    "author": "JupiterTheGroove",
                    "tag": "快速传送",
                    "desc": "告别跑路到路标的繁琐操作，在大地图上点击任何已知路标即刻传送"
                },
                {
                    "title": "All Quest Objectives on Map",
                    "author": "Wolfmark",
                    "tag": "地图增强",
                    "desc": "在世界大地图上同时标出全部已接任务目标与商人位置，极其便利"
                }
            ]
        },
        "cta_card": {
            "code_main": "【老L单机888】 或 【巫师3】"
        }
    },

    "baldurs-gate-3": {
        "dir_name": "04_baldurs-gate-3",
        "title": "博德之门 3 (Baldur's Gate 3)",
        "short_title": "博德之门3",
        "game_folder": "Baldurs Gate 3",
        "secret_code": "博德3",
        "radar_code": "老L单机888",
        "colors": {
            "primary": (168, 85, 247),      # Astral Arcane Purple
            "secondary": (251, 191, 36),    # Baldur's Gold
            "accent": (244, 63, 94),        # Mindflayer Rose Red
            "bg_top": (12, 10, 20),
            "bg_bottom": (20, 16, 35),
            "card_bg": (22, 18, 38),
            "card_border": (58, 45, 90),
            "code_bg": (9, 7, 16),
            "text_white": (245, 247, 250),
            "text_muted": (167, 139, 250),
            "text_dim": (120, 105, 170),
        },
        "hook_card": {
            "eyebrow": "【Script Extender 框架 · 深度解密】",
            "title_line1": "博德之门3 控制台怎么开？",
            "title_line2": "Script Extender 控制台指南",
            "pain_points": [
                "官方模组管理器上线后，不少旧版修改器与 Mod 闪退、读不了档",
                "荣誉模式被秒灭队心态爆炸，长休营地补给天天翻垃圾桶令人头秃",
                "队友意难平剧情分支选错，好感度不足导致恋爱支线永久锁死"
            ],
            "solution": "Norbyte 开源 Script Extender · 控制台窗口 · 源码公开",
            "features": [
                ("⚡ 打开控制台", "社区开源的 Script Extender 带控制台窗口，回车即执行"),
                ("🎮 场景化逃课套餐", "全员常驻急速飞行、10万黄金、起源队友全满好感救赎"),
                ("🛡️ 游戏更新以后", "Script Extender 要跟着游戏版本更新，大补丁后可能要等作者")
            ]
        },
        "setup_card": {
            "title": "小白 3 步打开 SE 控制台",
            "subtitle": "无需编程基础 · 开源框架 · 源码公开",
            "steps": [
                {
                    "step": "STEP 01",
                    "title": "定位游戏安装根目录",
                    "detail": "Steam 客户端 ➔ 库中右键游戏 ➔ 【管理】 ➔ 【浏览本地文件】",
                    "path_box": "SteamLibrary/steamapps/common/Baldurs Gate 3/"
                },
                {
                    "step": "STEP 02",
                    "title": "配置 Script Extender 控制台开关",
                    "detail": "将 DWrite.dll 放入 bin 目录，并在配置文件中设置开启控制台：",
                    "path_box": "bin/ScriptExtenderSettings.json ➔ CreateConsole: true"
                },
                {
                    "step": "STEP 03",
                    "title": "启动游戏即现独立调试黑窗",
                    "detail": "启动游戏时后台自动弹出一个清爽控制台黑窗，直接回车执行 Osi 指令！",
                    "key_text": "Script Extender 黑窗",
                    "key_sub": "在这个窗口里输入回车",
                    "key_hint": "启动游戏时会多出一个控制台窗口"
                }
            ],
            "bat_note": {
                "title": "💡 附：老L的 .bat 脚本（纯文本）",
                "bullets": [
                    "生成 ScriptExtenderSettings.json，打开 SE 的控制台窗口",
                    "写在 %LocalAppData% 的 Larian 目录下；原文件先另存为 .bak",
                    "不放 DWrite.dll，Script Extender 本体要自己装；也不备份存档"
                ],
                "footer": "👉 脚本在 L-MOD Vault 网站本游戏页，纯文本，可用记事本查看"
            }
        },
        "commands_card": {
            "title": "常用高频逃课与救赎指令清单",
            "subtitle": "在 Script Extender 控制台窗口输入回车 · 执行前先存档",
            "commands": [
                {
                    "name": "手残救星 · 全员常驻急速术",
                    "code": 'Osi.ApplyStatus(GetHostCharacter(), "HASTE", -1)',
                    "note": "每回合动作翻倍且无疲劳惩罚，高难度战斗化身战神，轻松破关"
                },
                {
                    "name": "资源自由 · 费伦大陆首富",
                    "code": "Osi.AddGold(GetHostCharacter(), 100000)",
                    "note": "10 万黄金到手，买空翠绿隘口与下城区全城商人稀有法术与防具"
                },
                {
                    "name": "背包减负 · 自由飞行探索",
                    "code": 'Osi.ApplyStatus(GetHostCharacter(), "FLY", -1)',
                    "note": "赋予常驻自由飞行能力，跨越断崖天堑陷阱，跑图探索极致爽快"
                },
                {
                    "name": "意难平救赎 · 影心满好感",
                    "code": 'Osi.SetAttitude(GetHostCharacter(), "S_Player_Shadowheart...", 100)',
                    "note": "影心好感度直接拉满 100 点；剧情能不能触发还要看进度"
                }
            ]
        },
        "mods_card": {
            "title": "解决痛点 · 精选 Mod",
            "subtitle": "只挑解决痛点的几款 · 装之前看清版本和前置要求",
            "mods": [
                {
                    "title": "Norbyte Script Extender",
                    "author": "Norbyte",
                    "tag": "核心前置",
                    "desc": "社区开源的脚本扩展框架（非官方），能开控制台窗口"
                },
                {
                    "title": "Better Inventory UI",
                    "author": "Caskas",
                    "tag": "背包整理",
                    "desc": "智能分类卷轴、药水与钥匙背包，彻底告别四人小队翻背包找道具噩梦"
                },
                {
                    "title": "Party Limit Begone (解除小队上限)",
                    "author": "Scribe",
                    "tag": "全员集结",
                    "desc": "突破4人队伍限制，带上全部起源伙伴一同旅行冒险，触发全部大合唱对话"
                }
            ]
        },
        "cta_card": {
            "code_main": "【老L单机888】 或 【博德3】"
        }
    },
    "elden-ring": {
        "dir_name": "05_elden-ring",
        "title": "艾尔登法环 (Elden Ring)",
        "short_title": "艾尔登法环",
        "game_folder": "ELDEN RING",
        "secret_code": "法环",
        "radar_code": "老L单机888",
        "colors": {
            "primary": (234, 179, 8),       # Erdtree Gold
            "secondary": (56, 189, 248),    # Spirit Ash Blue
            "accent": (244, 63, 94),        # Destined Death Crimson
            "bg_top": (15, 12, 10),
            "bg_bottom": (24, 20, 16),
            "card_bg": (30, 26, 22),
            "card_border": (64, 54, 42),
            "code_bg": (12, 10, 8),
            "text_white": (248, 250, 252),
            "text_muted": (168, 162, 158),
            "text_dim": (120, 113, 108),
        },
        "hook_card": {
            "eyebrow": "【黄金树幽影 · 纯净轮椅方案】",
            "title_line1": "法环幽影之地太折磨？",
            "title_line2": "离线轮椅指南：只在单机用",
            "pain_points": [
                "幽影树碎片全图盲目搜寻翻罐子，立体地图跑图卡关折磨数小时",
                "被狂龙贝勒与双月骑士数值怪反复虐哭，招架失败挫败感拉满",
                "来路不明的工具可能带后门；带着改过的存档联机还有封号风险"
            ],
            "solution": "ModEngine2 离线启动 · 不加载 EAC · 别带进联机",
            "features": [
                ("⚡ 离线启动", "ModEngine2 启动时不加载 EAC，只能离线玩；联机请从 Steam 正常启动"),
                ("🎮 幽影树轮椅神技套餐", "幽影树庇护一键拉满、全追忆神装、仿身泪滴带头大哥无痛获取"),
                ("🛡️ 游戏更新以后", "ModEngine2 和 CT 表可能要等作者适配新版本；更新情况看避坑雷达")
            ]
        },
        "setup_card": {
            "title": "小白 3 步进入离线 Mod 环境",
            "subtitle": "ModEngine2 启动时不加载 EAC · 只能离线玩",
            "steps": [
                {
                    "step": "STEP 01",
                    "title": "定位游戏安装根目录",
                    "detail": "Steam 客户端 ➔ 库中右键游戏 ➔ 【管理】 ➔ 【浏览本地文件】",
                    "path_box": "SteamLibrary/steamapps/common/ELDEN RING/Game/"
                },
                {
                    "step": "STEP 02",
                    "title": "放入 ModEngine2 离线框架",
                    "detail": "解压 ModEngine2 放入纯英文目录，并将模组放入 /mod 文件夹：",
                    "path_box": "Game/ModEngine2/launchmod_eldenring.bat"
                },
                {
                    "step": "STEP 03",
                    "title": "用 ModEngine2 的脚本启动",
                    "detail": "双击 launchmod_eldenring.bat 启动，主菜单右下角提示已离线即可！",
                    "key_text": "launchmod.bat",
                    "key_sub": "从这里启动不加载 EAC",
                    "key_hint": "主菜单右下角提示离线就对了"
                }
            ],
            "bat_note": {
                "title": "💡 离线玩之前先看这三条",
                "bullets": [
                    "launchmod_eldenring.bat 是 ModEngine2 自带的，从它启动不加载 EAC",
                    "Seamless Co-op 用独立的 .co2 存档，不连官方匹配",
                    "想回官方联机就从 Steam 正常启动；别把改过的存档带上线"
                ],
                "footer": "👉 完整步骤和指令在 L-MOD Vault 网站本游戏页"
            }
        },
        "commands_card": {
            "title": "常用高频逃课与轮椅神技清单",
            "subtitle": "CT 表要配合 Cheat Engine 用 · 只在离线时用，先存档",
            "commands": [
                {
                    "name": "幽影树庇护拉满 · Lv20满级",
                    "code": "[CT表] Set Scadutree Blessing to 20",
                    "note": "幽影之地核心数值瞬间拉满，攻防减伤直接翻倍，拒绝幽影受苦"
                },
                {
                    "name": "手残救星 · 绝对免伤无敌",
                    "code": "Num 1 (God Mode)",
                    "note": "完全免疫伤害与异常状态，生命条锁定最大值，专心探索交界地"
                },
                {
                    "name": "子弹时间 · 0.3x 慢动作识破",
                    "code": "Ctrl+Num 3 (Slomo 0.3x)",
                    "note": "将全局流速降至 0.3 倍，Boss 出招前摇清晰可见，轻松掌握弹反"
                },
                {
                    "name": "资源自由 · 100万卢恩秒到账",
                    "code": "Ctrl+Num 1 (Add 1,000,000 Runes)",
                    "note": "随时自由升级洗点，并在圆桌厅堂扫荡全部锻造石与消耗品"
                }
            ]
        },
        "mods_card": {
            "title": "解决痛点 · 精选 Mod",
            "subtitle": "只挑解决痛点的几款 · 装之前看清版本和前置要求",
            "mods": [
                {
                    "title": "Seamless Co-op (无缝联机)",
                    "author": "LukeYui",
                    "tag": "联机 Mod",
                    "desc": "打完 Boss 不再被遣返，全图无缝跑图；用独立 .co2 存档，不连官方匹配"
                },
                {
                    "title": "ModEngine2 模组加载框架",
                    "author": "SoulsMods",
                    "tag": "加载框架",
                    "desc": "免解包挂载模组，启动时不加载 EAC（只能离线），不改原版文件"
                },
                {
                    "title": "The Grand Archives CT 调试表",
                    "author": "TGA Team",
                    "tag": "CT 调试表",
                    "desc": "全DLC装备道具一键派发、全图赐福点秒亮、360°自由运镜摄影"
                }
            ]
        },
        "cta_card": {
            "code_main": "【老L单机888】 或 【法环】"
        }
    },
    "skyrim-se": {
        "dir_name": "06_skyrim-se",
        "title": "上古卷轴5：天际重制版 (The Elder Scrolls V: Skyrim SE)",
        "short_title": "天际重制版",
        "game_folder": "Skyrim Special Edition",
        "secret_code": "老滚5",
        "radar_code": "老L单机888",
        "colors": {
            "primary": (56, 189, 248),       # Skyrim Frost Ice Blue
            "secondary": (234, 179, 8),      # Septim Nordic Gold
            "accent": (147, 197, 253),       # Ethereal Blue
            "bg_top": (10, 16, 24),
            "bg_bottom": (16, 24, 38),
            "card_bg": (22, 32, 48),
            "card_border": (45, 65, 95),
            "code_bg": (8, 12, 18),
            "text_white": (248, 250, 252),
            "text_muted": (148, 163, 184),
            "text_dim": (100, 116, 139),
        },
        "hook_card": {
            "eyebrow": "【天际13年 · 官方底层避坑救赎】",
            "title_line1": "老滚5任务卡死坏档闪退？",
            "title_line2": "B社原生控制台急救指南",
            "pain_points": [
                "任务NPC发呆不说话剧情死锁，数十小时心血存档直接报废",
                "地牢石头缝隙卡死动弹不得，或者高刷显示器推车鬼畜飞天",
                "满世界搜来路不明的修改器，可能被捆绑木马，一更新就CTD闪退"
            ],
            "solution": "游戏自带控制台 · 按 ~ 就能用 · 不用装任何东西",
            "features": [
                ("⚡ 1秒波浪键直达", "美式键盘 ~ 键一键呼出，原生代码无需任何第三方注入"),
                ("🛠️ 任务卡死试试 setstage", "按任务 ID 推进到指定阶段；先存档，阶段填错可能把任务弄乱"),
                ("🏰 16魔神器全集自由", "官方开发者烟雾房 coc qasmoke 直达，全法术全龙吼随心体验")
            ]
        },
        "setup_card": {
            "title": "小白 3 步唤醒 B社原生控制台",
            "subtitle": "游戏自带控制台 · 不用装第三方程序",
            "steps": [
                {
                    "step": "STEP 01",
                    "title": "定位游戏安装根目录",
                    "detail": "Steam 客户端 ➔ 库中右键老滚5 ➔ 【管理】 ➔ 【浏览本地文件】",
                    "path_box": "SteamLibrary/steamapps/common/Skyrim Special Edition/"
                },
                {
                    "step": "STEP 02",
                    "title": "确认 Skyrim.ini 配置",
                    "detail": "进入 Documents/My Games/Skyrim Special Edition/ 确认：",
                    "path_box": "[General] -> bAllowConsole=1 (默认已启用)"
                },
                {
                    "step": "STEP 03",
                    "title": "按 ~ 键呼出控制台终端",
                    "detail": "进入游戏，在主界面或探索时按下键盘左上角波浪键即可输入指令！",
                    "key_text": "~ / ` 键",
                    "key_sub": "美式键盘 ESC 下方波浪键"
                }
            ],
            "bat_note": {
                "title": "💡 极客避坑：老滚5 FormID 省略前导零秘籍",
                "bullets": [
                    "FormID 前面的 000 全部可省略！比如金币 0000000F，直接输 player.additem f 100000",
                    "严禁盲目运行 caqs (完成全任务)，这会破坏全图 NPC 状态机造成终极坏档",
                    "高刷新率显示器请配合 SSE Engine Fixes 锁定物理帧率，防止马车飞天"
                ],
                "footer": "👉 完整步骤和指令在 L-MOD Vault 网站本游戏页"
            }
        },
        "commands_card": {
            "title": "天际极客常用高频急救与神装清单",
            "subtitle": "游戏自带控制台指令 · 执行前先存档",
            "commands": [
                {
                    "name": "穿墙脱困 · 解除卡石缝绝境",
                    "code": "tcl",
                    "note": "开关全局物理碰撞，瞬间脱离地形卡死与地牢模型穿模"
                },
                {
                    "name": "开发者烟雾房 · 全道具宝箱",
                    "code": "coc qasmoke",
                    "note": "传送至官方全物品测试房，全神装/魔神器宝箱任取；输 coc riverwood 返回"
                },
                {
                    "name": "救活卡死NPC · 满血原地复活",
                    "code": "resurrect 1",
                    "note": "按 ~ 点击关键NPC尸体再输入，让 NPC 复活；任务能否继续还要看进度"
                },
                {
                    "name": "万能启动金币 · 10万塞普汀到账",
                    "code": "player.additem f 100000",
                    "note": "前导零已极客精简，买房买领地随从雇佣财富自由"
                }
            ]
        },
        "mods_card": {
            "title": "天际重制版三大常用前置",
            "subtitle": "B社 Mod 生态常用前置 · 减少 CTD 闪退、方便排错",
            "mods": [
                {
                    "title": "SKSE64 (脚本扩展器)",
                    "author": "Silverlock Team",
                    "tag": "Mod基石",
                    "desc": "全面拓宽天际 Papyrus 脚本引擎执行上限，现代高级模组必备核心"
                },
                {
                    "title": "SSE Engine Fixes (引擎修复)",
                    "author": "aers / Ryan",
                    "tag": "引擎修复",
                    "desc": "修复高帧率推车飞天、LipSync 嘴唇不同步，突破模组句柄限制"
                },
                {
                    "title": "Crash Logger SSE (崩溃日志)",
                    "author": "alandtse",
                    "tag": "排错雷达",
                    "desc": "闪退时输出日志，帮你找出可能出问题的插件"
                }
            ]
        },
        "cta_card": {
            "code_main": "【老L单机888】 或 【老滚5】"
        }
    },
    "fallout-4": {
        "dir_name": "07_fallout-4",
        "title": "辐射4：次世代更新版 (Fallout 4 Next-Gen)",
        "short_title": "辐射4",
        "game_folder": "Fallout 4",
        "secret_code": "辐射4",
        "radar_code": "老L单机888",
        "colors": {
            "primary": (34, 197, 94),        # Pip-Boy Phosphor Green
            "secondary": (250, 204, 21),     # Vault-Tec Yellow
            "accent": (56, 189, 248),        # Vault Suit Blue
            "bg_top": (10, 20, 15),
            "bg_bottom": (15, 28, 20),
            "card_bg": (20, 36, 26),
            "card_border": (40, 75, 52),
            "code_bg": (8, 16, 12),
            "text_white": (248, 250, 252),
            "text_muted": (167, 243, 208),
            "text_dim": (110, 160, 135),
        },
        "hook_card": {
            "eyebrow": "【次世代避坑 · 废土极客救赎】",
            "title_line1": "辐射4次世代更新Mod全崩？",
            "title_line2": "原生控制台与聚落无限扩建指南",
            "pain_points": [
                "2024 次世代大更新破坏 9 年 Mod 体系，F4SE 崩溃红字频发",
                "庇护山丘聚落建造容量被强制锁死变黄，想盖摩天大楼被卡脖子",
                "网上来路不明的修改器可能带病毒，游戏一更新就失效甚至坏档"
            ],
            "solution": "次世代 / 降级两条路写清楚 · 游戏自带控制台",
            "features": [
                ("⚡ 1秒开启原生控制台", "游戏自带控制台，按 ~ 键呼出，不用装任何东西"),
                ("🏗️ 聚落无限建造指令", "setav 349/348 重置建造容量，打造万物赛博主城"),
                ("🛡️ 次世代避坑双轨指南", "写清 1.10.984 次世代版与 1.10.163 降级两条路线")
            ]
        },
        "setup_card": {
            "title": "小白 3 步唤醒废土原生控制台",
            "subtitle": "无需复杂工具 · 少让 Steam 自动更新 · 游戏自带控制台",
            "steps": [
                {
                    "step": "STEP 01",
                    "title": "定位辐射4游戏安装根目录",
                    "detail": "Steam 库中右键 Fallout 4 ➔ 【管理】 ➔ 【浏览本地文件】",
                    "path_box": "SteamLibrary/steamapps/common/Fallout 4/"
                },
                {
                    "step": "STEP 02",
                    "title": "Steam 改成仅启动时更新",
                    "detail": "右键属性 ➔ 更新 ➔ 设置为【仅在我启动该游戏时更新】，减少后台更新：",
                    "path_box": "装了 F4SE 的话，用 f4se_loader.exe 启动游戏"
                },
                {
                    "step": "STEP 03",
                    "title": "按 ~ 键呼出控制台终端",
                    "detail": "游戏中随时按下波浪键 ~，屏幕底部出现光标即可输入官方原生指令！",
                    "key_text": "~ / ` 键",
                    "key_sub": "美式键盘 ESC 下方波浪键"
                }
            ],
            "bat_note": {
                "title": "💡 极客避坑：辐射4次世代更新与避坑要点",
                "bullets": [
                    "次世代更新重写了内存偏移，老版 F4SE 插件必须升级为 NG 版或回退 1.10.163",
                    "死亡三角区 (庇护山丘+红火箭+阿伯纳西) 避免同时高密建造，防止内存溢出",
                    "使用 scrapall 指令前务必先存盘，避免将重要动力装甲骨架误拆"
                ],
                "footer": "👉 完整步骤和指令在 L-MOD Vault 网站本游戏页"
            }
        },
        "commands_card": {
            "title": "辐射4常用高频聚落与传奇神装清单",
            "subtitle": "游戏自带控制台指令 · 执行前先存档",
            "commands": [
                {
                    "name": "聚落建造空间无限解除",
                    "code": "setav 349 9999999",
                    "note": "~ 点中工坊工作台输入 349与348，三角形面数重置为0，实现无限建造"
                },
                {
                    "name": "全聚落极速清理大平地",
                    "code": "scrapall",
                    "note": "领地内一键拆解所有杂木废墟杂草，自动转为木材钢铁存入工坊"
                },
                {
                    "name": "手残党真神 · 绝对无敌不死",
                    "code": "tgm",
                    "note": "切换上帝模式，无限生命/AP/弹药/负重，畅游辐射废土"
                },
                {
                    "name": "万能瓶盖财富自由",
                    "code": "player.additem f 100000",
                    "note": "瞬间到账 100,000 瓶盖，各大钻石城与芳邻镇商人扫荡自由"
                }
            ]
        },
        "mods_card": {
            "title": "辐射4次世代常用三大前置",
            "subtitle": "次世代版 Mod 常用前置 · 装之前看清版本要求",
            "mods": [
                {
                    "title": "F4SE (辐射4脚本扩展器)",
                    "author": "Ian Patterson",
                    "tag": "Mod引擎",
                    "desc": "拓宽原生脚本能力，支持高级UI与复杂功能Mod，次世代认准v0.7.2+"
                },
                {
                    "title": "Buffout 4 NG (崩溃修复)",
                    "author": "Ryan / Fudgy",
                    "tag": "崩溃修复",
                    "desc": "修复一部分引擎层面的崩溃问题，闪退时输出错误日志方便排错"
                },
                {
                    "title": "Fallout 4 Downgrader",
                    "author": "Zerratar",
                    "tag": "版本降级",
                    "desc": "把次世代版降级回 1.10.163（次世代更新之前的版本），老 Mod 能接着用"
                }
            ]
        },
        "cta_card": {
            "code_main": "【老L单机888】 或 【辐射4】"
        }
    }
}

# ==============================================================================
# 3b. 全部卡片通用的固定文案（只写做到的事；改之前对照文件头的口径）
# ==============================================================================
HEADER_BADGES = {
    "hook": "老L整理 · 未逐条实测",
    "setup": "源码公开 · 先备份存档",
    "commands": "未逐条实测 · 先存档",
    "mods": "装前先看版本要求",
    "cta": "每天比对 Steam 更新",
}

COMMANDS_FOOTER = [
    "※ 这些指令没有逐条在游戏里实测，版本不同可能失效；执行前先手动存档",
    "更多指令见 L-MOD Vault 网站本游戏页",
]

MOD_RULES_TITLE = "装 Mod 前的三件事："
MOD_RULES = [
    "1. 先手动备份存档：老L的脚本都不备份存档；",
    "2. 看清 Mod 页写的游戏版本和前置，游戏更新后可能要等作者适配；",
    "3. 一次只加一两个，出问题先删掉最近加的再试。",
]

CTA_TITLE = "更新提醒与资料入口"
CTA_SUBTITLE = "避坑雷达每天比对一次 Steam 更新时间 · 刚更新会标黄或标红"
CTA_VIP_TITLE = "L-MOD Vault 网站本游戏页（免费）"
CTA_VIP_BULLETS = [
    "老L写的 .bat 脚本：纯文本，可用记事本查看全部内容",
    "控制台指令清单与场景套餐，带中文说明",
    "精选 Mod 与前置框架的介绍",
    "本游戏的 Steam 更新提醒（避坑雷达）",
]
CTA_CODE_TITLE = "公众号后台或私信发送暗号，进玩家互助群："
CTA_CODE_HINT = "（交流 Mod 更新进度与坏档处理经验）"
CTA_NOTES = [
    ("更新提醒", "避坑雷达每天比对一次 Steam 更新时间；不做实机测试，所以只说「可能」"),
    ("存档自己备份", "老L的脚本都不备份存档；改配置、装 Mod 之前先手动复制存档文件夹"),
    ("玩家互助群", "不接广告，群文件不放 exe；交流 Mod 更新进度与坏档处理经验"),
]

# ==============================================================================
# 4. 高精度图形绘制工具库 (Pillow 几何美学引擎)
# ==============================================================================
class DrawingEngine:
    @staticmethod
    def create_gradient_canvas(width: int, height: int, c_top: tuple, c_bottom: tuple) -> Image.Image:
        """生成具有细腻高斯氛围的高级暗色渐变画布"""
        base = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(base)
        for y in range(height):
            ratio = y / float(height)
            r = int(c_top[0] * (1 - ratio) + c_bottom[0] * ratio)
            g = int(c_top[1] * (1 - ratio) + c_bottom[1] * ratio)
            b = int(c_top[2] * (1 - ratio) + c_bottom[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        return base

    @staticmethod
    def draw_badge(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, font: ImageFont.FreeTypeFont,
                   bg_color: tuple, text_color: tuple, border_color: tuple = None, pad_x: int = 14, pad_y: int = 6, radius: int = 8):
        """绘制高对比度状态药丸/徽章"""
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        box = [x, y, x + w + pad_x * 2, y + h + pad_y * 2]
        draw.rounded_rectangle(box, radius=radius, fill=bg_color, outline=border_color, width=1 if border_color else 0)
        draw.text((x + pad_x, y + pad_y - 1), text, font=font, fill=text_color)
        return box[2], box[3]

    @staticmethod
    def draw_code_box(draw: ImageDraw.ImageDraw, bbox: list, code_text: str, lang: str,
                      bg_color: tuple, border_color: tuple, accent_color: tuple, fonts: dict):
        """绘制带 macOS 极客风格三色圆点的 IDE 高亮代码块"""
        x1, y1, x2, y2 = bbox
        draw.rounded_rectangle(bbox, radius=12, fill=bg_color, outline=border_color, width=1)
        # 窗口红黄绿圆点
        draw.ellipse([x1 + 16, y1 + 14, x1 + 26, y1 + 24], fill=(255, 95, 87))
        draw.ellipse([x1 + 34, y1 + 14, x1 + 44, y1 + 24], fill=(254, 188, 46))
        draw.ellipse([x1 + 52, y1 + 14, x1 + 62, y1 + 24], fill=(40, 201, 64))
        # 语言指示器
        if lang:
            draw.text((x2 - 18, y1 + 18), lang, font=fonts["tag_sm"], fill=(120, 135, 155), anchor="rm")
        # 代码正文 (带控制台 > 提示符)
        draw.text((x1 + 20, y1 + 45), "> " + code_text, font=fonts["code"], fill=accent_color)

    @staticmethod
    def draw_keycap(draw: ImageDraw.ImageDraw, bbox: list, key_text: str, sub_text: str,
                    key_color: tuple, fonts: dict):
        """绘制拟物化极客按键效果"""
        x1, y1, x2, y2 = bbox
        # 键帽底座阴影
        draw.rounded_rectangle([x1, y1 + 4, x2, y2 + 4], radius=10, fill=(12, 15, 22))
        # 键帽正面
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(30, 36, 50), outline=(65, 80, 105), width=2)
        # 顶面高光细线
        draw.line([(x1 + 10, y1 + 3), (x2 - 10, y1 + 3)], fill=(95, 115, 145), width=1)
        # 按键字符
        draw.text(((x1 + x2) // 2, (y1 + y2) // 2 - 10), key_text, font=fonts["keycap"], fill=key_color, anchor="mm")
        if sub_text:
            draw.text(((x1 + x2) // 2, (y1 + y2) // 2 + 18), sub_text, font=fonts["body_sm"], fill=(180, 195, 215), anchor="mm")

    @staticmethod
    def draw_geek_seal(draw: ImageDraw.ImageDraw, cx: int, cy: int, radius: int,
                       primary_color: tuple, secondary_color: tuple, fonts: dict):
        """绘制老L品牌圆印（只是品牌标识，不代表任何认证）"""
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], outline=primary_color, width=3)
        r2 = radius - 8
        draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=secondary_color, width=1)
        r3 = radius - 15
        draw.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], outline=primary_color, width=2)
        draw.text((cx, cy - 28), "L-MOD", font=fonts["seal_title"], fill=primary_color, anchor="mm")
        draw.text((cx, cy + 1), "老L整理", font=fonts["body_bold"], fill=(255, 255, 255), anchor="mm")
        draw.text((cx, cy + 29), "仅限单机", font=fonts["seal_sub"], fill=secondary_color, anchor="mm")

    @staticmethod
    def draw_top_header(draw: ImageDraw.ImageDraw, tag_text: str, brand_text: str, patch_text: str,
                        tag_bg: tuple, tag_color: tuple, patch_color: tuple, colors: dict, fonts: dict):
        """绘制全卡系统通用顶部信息栏"""
        # 顶栏左侧药丸
        DrawingEngine.draw_badge(draw, 60, 60, tag_text, fonts["tag"], tag_bg, tag_color, radius=8)
        # 顶栏中间品牌标题
        draw.text((540, 78), brand_text, font=fonts["tag"], fill=colors["text_muted"], anchor="mm")
        # 顶栏右侧说明标（右对齐到 1020，以前固定从 x=800 起画，长一点就出框）
        pad_x = 14
        bbox = draw.textbbox((0, 0), patch_text, font=fonts["tag"])
        badge_x = 1020 - (bbox[2] - bbox[0]) - pad_x * 2
        DrawingEngine.draw_badge(draw, badge_x, 60, patch_text, fonts["tag"], (20, 35, 30), patch_color, border_color=(40, 80, 60), pad_x=pad_x, radius=8)
        # 顶部分隔细线
        draw.line([(60, 125), (1020, 125)], fill=(35, 45, 65), width=1)

    @staticmethod
    def draw_bottom_footer(draw: ImageDraw.ImageDraw, current_slide: int, total_slides: int,
                           hint_text: str, primary_color: tuple, colors: dict, fonts: dict):
        """绘制全卡系统通用底部导航与轮播点"""
        draw.line([(60, 1335), (1020, 1335)], fill=(35, 45, 65), width=1)
        draw.text((60, 1362), f"SLIDE {current_slide}/{total_slides}  {hint_text}", font=fonts["tag"], fill=colors["text_dim"])
        cx, cy = 970, 1370
        spacing = 24
        start_x = cx - ((total_slides - 1) * spacing)
        for i in range(1, total_slides + 1):
            dot_x = start_x + (i - 1) * spacing
            if i == current_slide:
                draw.ellipse([dot_x - 7, cy - 7, dot_x + 7, cy + 7], fill=primary_color)
            else:
                draw.ellipse([dot_x - 5, cy - 5, dot_x + 5, cy + 5], outline=(70, 85, 110), fill=(22, 26, 36), width=1)


# ==============================================================================
# 5. 卡片单张核心渲染引擎 (Card 1 ~ Card 5)
# ==============================================================================
class CardRenderer:
    def __init__(self, game_key: str):
        self.game_key = game_key
        self.data = FLAGSHIP_GAMES[game_key]
        self.c = self.data["colors"]
        self.w, self.h = 1080, 1440

    def _create_base(self, card_name: str = "") -> (Image.Image, ImageDraw.ImageDraw):
        img = DrawingEngine.create_gradient_canvas(self.w, self.h, self.c["bg_top"], self.c["bg_bottom"])
        draw = SafeDraw(img)
        draw.current_card = f"{self.data['dir_name']}/{card_name}"
        # 优雅的外层细框
        draw.rounded_rectangle([20, 20, 1060, 1420], radius=20, outline=(40, 50, 70), width=1)
        return img, draw

    def render_card_1_hook(self) -> Image.Image:
        """Card 1: 爆款痛点封面 (大字+痛点对比+老L品牌印章)"""
        img, draw = self._create_base("card_1_hook")
        h_data = self.data["hook_card"]

        # 1. 顶部 Header
        DrawingEngine.draw_top_header(
            draw, "🔥 避坑排雷", "L-MOD VAULT · 极客避坑智库",
            HEADER_BADGES["hook"],
            (50, 20, 25), (255, 90, 95), (45, 212, 191), self.c, FONTS
        )

        # 2. 醒目 Eyebrow 标
        DrawingEngine.draw_badge(draw, 60, 155, h_data["eyebrow"], FONTS["tag"], (40, 35, 15), self.c["primary"], radius=6)

        # 3. 爆款超大主标题 (两行，字号 52，分色)
        draw.text((60, 225), h_data["title_line1"], font=FONTS["h1"], fill=self.c["text_white"])
        draw.text((60, 295), h_data["title_line2"], font=FONTS["h1"], fill=self.c["primary"])

        # 4. 传统修改器三大致命痛点容器 (带红灰暗层与警告红标)
        box_y1, box_y2 = 385, 715
        draw.rounded_rectangle([60, box_y1, 1020, box_y2], radius=16, fill=self.c["card_bg"], outline=(100, 40, 45), width=2)
        # 警告标题
        draw.text((90, box_y1 + 25), "⚠️ 来路不明的修改器，常见三个坑：", font=FONTS["h3"], fill=(255, 90, 95))
        # 痛点列表
        for idx, pt in enumerate(h_data["pain_points"]):
            py = box_y1 + 75 + idx * 45
            draw.text((90, py), "✗", font=FONTS["body_bold"], fill=(239, 68, 68))
            draw.text((120, py), pt, font=FONTS["body"], fill=(200, 210, 225))
        # 容器内部分割线
        draw.line([(90, box_y1 + 225), (990, box_y1 + 225)], fill=(55, 65, 85), width=1)
        # 底部老L的做法（标签多宽，正文就从哪接着写）
        label = "✨ 老L的做法："
        draw.text((90, box_y1 + 245), label, font=FONTS["body_bold"], fill=self.c["secondary"])
        label_box = draw.textbbox((90, box_y1 + 245), label, font=FONTS["body_bold"])
        draw.text((label_box[2] + 8, box_y1 + 245), h_data["solution"], font=FONTS["body_bold"], fill=self.c["text_white"])

        # 5. 三大极客核心优势行
        for idx, (title, desc) in enumerate(h_data["features"]):
            fy = 745 + idx * 105
            draw.rounded_rectangle([60, fy, 1020, fy + 90], radius=12, fill=self.c["card_bg"], outline=self.c["card_border"], width=1)
            draw.text((90, fy + 18), title, font=FONTS["body_bold"], fill=self.c["primary"])
            draw.text((90, fy + 52), desc, font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 6. 老L品牌印章与说明
        seal_cx, seal_cy = 175, 1205
        DrawingEngine.draw_geek_seal(draw, seal_cx, seal_cy, 75, self.c["primary"], self.c["secondary"], FONTS)
        draw.rounded_rectangle([280, 1115, 1020, 1295], radius=14, fill=self.c["card_bg"], outline=self.c["card_border"], width=1)
        draw.text((310, 1135), "老L整理 · 免费分享", font=FONTS["body_bold"], fill=self.c["primary"])
        draw.text((310, 1175), "• 单机老玩家整理的避坑资料和指令，不收费", font=FONTS["body_sm"], fill=self.c["text_white"])
        draw.text((310, 1210), "• 想还原：删掉放进去的文件，再在 Steam 里验证游戏文件完整性", font=FONTS["body_sm"], fill=self.c["text_muted"])
        draw.text((310, 1250), "“认准老L避坑实验室 · 每一个单机好游戏都不留遗憾”", font=FONTS["body_sm"], fill=self.c["secondary"])

        # 7. 底部导航
        DrawingEngine.draw_bottom_footer(draw, 1, 5, "往右滑解锁 10 秒开启教程 ➔", self.c["primary"], self.c, FONTS)
        return img

    def render_card_2_setup(self) -> Image.Image:
        """Card 2: 打开控制台的 3 步 (3步可视化指引+路径高亮+.bat 脚本说明)"""
        img, draw = self._create_base("card_2_setup")
        s_data = self.data["setup_card"]

        # 1. 顶部 Header
        DrawingEngine.draw_top_header(
            draw, "⚡ 打开控制台", "L-MOD VAULT · 手把手配置",
            HEADER_BADGES["setup"],
            (20, 40, 50), (45, 212, 191), (45, 212, 191), self.c, FONTS
        )

        # 2. 醒目 Eyebrow & 主标题
        DrawingEngine.draw_badge(draw, 60, 155, "【打开控制台 · 3 步】", FONTS["tag"], (20, 35, 45), self.c["secondary"], radius=6)
        draw.text((60, 215), s_data["title"], font=FONTS["h1"], fill=self.c["text_white"])
        draw.text((60, 275), s_data["subtitle"], font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 3. 三大步骤大卡片 (每张高度 ~215px)
        step_y = [320, 555, 790]
        for idx, step in enumerate(s_data["steps"]):
            sy = step_y[idx]
            sh = 215
            draw.rounded_rectangle([60, sy, 1020, sy + sh], radius=16, fill=self.c["card_bg"], outline=self.c["card_border"], width=1)
            # 步骤序号标
            DrawingEngine.draw_badge(draw, 85, sy + 20, step["step"], FONTS["tag"], (35, 45, 65), self.c["primary"], radius=6)
            # 步骤名称
            draw.text((195, sy + 22), step["title"], font=FONTS["h3"], fill=self.c["text_white"])
            # 步骤操作说明
            draw.text((85, sy + 65), step["detail"], font=FONTS["body_sm"], fill=self.c["text_muted"])

            # 步骤内部视觉展示
            if "path_box" in step:
                draw.rounded_rectangle([85, sy + 110, 995, sy + 175], radius=10, fill=self.c["code_bg"], outline=(40, 50, 70), width=1)
                draw.text((110, sy + 130), "📁 " + step["path_box"], font=FONTS["code_sm"], fill=self.c["secondary"])
            elif "key_text" in step:
                DrawingEngine.draw_keycap(
                    draw, [85, sy + 105, 450, sy + 185],
                    step["key_text"], step.get("key_sub", ""),
                    self.c["primary"], FONTS
                )
                hint = step.get("key_hint", "按下快捷键，出现输入框就成功了")
                draw.text((480, sy + 130), hint, font=FONTS["body_bold"], fill=(50, 215, 150))

        # 4. 老L批处理 / 避坑说明 Box（只写脚本真正做的事）
        bat_y = 1035
        bat = s_data["bat_note"]
        draw.rounded_rectangle([60, bat_y, 1020, bat_y + 265], radius=16, fill=self.c["card_bg"], outline=self.c["primary"], width=2)
        draw.text((90, bat_y + 25), bat["title"], font=FONTS["h3"], fill=self.c["primary"])
        for b_idx, bullet in enumerate(bat["bullets"]):
            by = bat_y + 75 + b_idx * 40
            draw.text((90, by), bullet, font=FONTS["body_sm"], fill=self.c["text_white"])
        # 去哪看
        draw.text((90, bat_y + 210), bat["footer"], font=FONTS["body_bold"], fill=self.c["secondary"])

        # 5. 底部导航
        DrawingEngine.draw_bottom_footer(draw, 2, 5, "往右滑查看场景核心指令清单 ➔", self.c["primary"], self.c, FONTS)
        return img

    def render_card_3_commands(self) -> Image.Image:
        """Card 3: 场景化核心指令套餐清单 (场景套包+高亮代码块+功能解读)"""
        img, draw = self._create_base("card_3_commands")
        c_data = self.data["commands_card"]

        # 1. 顶部 Header
        DrawingEngine.draw_top_header(
            draw, "⚔️ 核心指令", "L-MOD VAULT · 逃课与救赎套餐",
            HEADER_BADGES["commands"],
            (40, 25, 45), (192, 132, 252), (50, 215, 150), self.c, FONTS
        )

        # 2. 醒目 Eyebrow & 主标题
        DrawingEngine.draw_badge(draw, 60, 155, "【核心指令 · 场景化套餐清单】", FONTS["tag"], (35, 20, 45), (216, 180, 254), radius=6)
        draw.text((60, 215), c_data["title"], font=FONTS["h1"], fill=self.c["text_white"])
        draw.text((60, 275), c_data["subtitle"], font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 3. 4 条高频实战指令卡片 (每张高度 ~215px)
        cmd_y = [320, 555, 790, 1025]
        for idx, cmd in enumerate(c_data["commands"]):
            cy = cmd_y[idx]
            ch = 215
            draw.rounded_rectangle([60, cy, 1020, cy + ch], radius=16, fill=self.c["card_bg"], outline=self.c["card_border"], width=1)
            # 功能名称
            draw.text((85, cy + 20), cmd["name"], font=FONTS["h3"], fill=self.c["primary"])
            # （以前这里有「官方已校验」标，没有人校验过，删掉）
            # IDE 终端风格代码块
            DrawingEngine.draw_code_box(
                draw, [85, cy + 65, 995, cy + 145],
                cmd["code"], "CONSOLE",
                self.c["code_bg"], (40, 50, 70), (50, 215, 150), FONTS
            )
            # 效果解读
            draw.text((85, cy + 165), "💡 " + cmd["note"], font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 4. 底部补充说明
        draw.text((540, 1266), COMMANDS_FOOTER[0], font=FONTS["body_sm"], fill=self.c["text_muted"], anchor="mm")
        draw.text((540, 1302), COMMANDS_FOOTER[1], font=FONTS["body_sm"], fill=self.c["text_dim"], anchor="mm")

        # 5. 底部导航
        DrawingEngine.draw_bottom_footer(draw, 3, 5, "往右滑查看精选 Mod ➔", self.c["primary"], self.c, FONTS)
        return img

    def render_card_4_mods(self) -> Image.Image:
        """Card 4: 精选 Mod (3 款解决痛点的 Mod + 下载量 + 装前须知)"""
        img, draw = self._create_base("card_4_mods")
        m_data = self.data["mods_card"]

        # 1. 顶部 Header
        DrawingEngine.draw_top_header(
            draw, "🛠️ 精选模组", "L-MOD VAULT · 精选 Mod",
            HEADER_BADGES["mods"],
            (25, 45, 35), (50, 215, 150), (50, 215, 150), self.c, FONTS
        )

        # 2. 醒目 Eyebrow & 主标题
        DrawingEngine.draw_badge(draw, 60, 155, "【解决痛点 · 精选 Mod】", FONTS["tag"], (20, 40, 30), (50, 215, 150), radius=6)
        draw.text((60, 215), m_data["title"], font=FONTS["h1"], fill=self.c["text_white"])
        draw.text((60, 275), m_data["subtitle"], font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 3. 3 款精选模组卡片 (每张高度 ~230px)
        mod_y = [320, 570, 820]
        for idx, mod in enumerate(m_data["mods"]):
            my = mod_y[idx]
            mh = 230
            draw.rounded_rectangle([60, my, 1020, my + mh], radius=16, fill=self.c["card_bg"], outline=self.c["card_border"], width=1)
            # 模组分类标
            DrawingEngine.draw_badge(draw, 85, my + 22, mod["tag"], FONTS["tag_sm"], (35, 45, 65), self.c["secondary"], radius=6)
            # 模组标题
            draw.text((200, my + 24), mod["title"], font=FONTS["h3"], fill=self.c["text_white"])
            # 作者（下载量不再上图：数字来源查不到，和网站数据也对不上）
            meta_text = f"作者: {mod['author']}"
            draw.text((85, my + 75), meta_text, font=FONTS["body_sm"], fill=self.c["text_dim"])
            # 痛点解决描述容器
            draw.rounded_rectangle([85, my + 115, 995, my + 200], radius=10, fill=self.c["code_bg"], outline=(35, 45, 65), width=1)
            draw.text((105, my + 135), "⚡ 解决痛点：" + mod["desc"], font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 4. 装 Mod 前的注意事项 Box（以前这里写「坏档隔离沙盒 / 大版本对齐检验 / 实机压力测试 30+ 小时」，都没做过）
        rule_y = 1080
        draw.rounded_rectangle([60, rule_y, 1020, rule_y + 215], radius=16, fill=self.c["card_bg"], outline=(50, 215, 150), width=2)
        draw.text((90, rule_y + 25), MOD_RULES_TITLE, font=FONTS["h3"], fill=(50, 215, 150))
        for r_idx, r_text in enumerate(MOD_RULES):
            draw.text((90, rule_y + 75 + r_idx * 40), r_text, font=FONTS["body_sm"], fill=self.c["text_white"])

        # 5. 底部导航
        DrawingEngine.draw_bottom_footer(draw, 4, 5, "往右滑查看资料入口与互助群 ➔", self.c["primary"], self.c, FONTS)
        return img

    def render_card_5_cta(self) -> Image.Image:
        """Card 5: 资料入口与互助群暗号 (网站本游戏页有什么 + 暗号框 + 3 条说明 + 老L品牌声明)

        以前这张写的是「一键懒人免配包 / 纯净前置离线包 / 100+ 条速查手册 / 后台秒推高速网盘 /
        补丁连夜追更、第一时间测试」——网盘包、测试机、追更都不存在，改成网站上真有的东西。
        """
        img, draw = self._create_base("card_5_cta")
        cta = self.data["cta_card"]

        # 1. 顶部 Header
        DrawingEngine.draw_top_header(
            draw, "🚀 极客福利", "L-MOD VAULT · 玩家社群",
            HEADER_BADGES["cta"],
            (40, 20, 50), (236, 72, 153), (50, 215, 150), self.c, FONTS
        )

        # 2. 醒目 Eyebrow & 主标题
        DrawingEngine.draw_badge(draw, 60, 155, "【极客福利 · 更新提醒】", FONTS["tag"], (35, 15, 40), (244, 114, 182), radius=6)
        draw.text((60, 215), CTA_TITLE, font=FONTS["h1"], fill=self.c["text_white"])
        draw.text((60, 275), CTA_SUBTITLE, font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 3. 网站本游戏页有什么
        vip_y = 320
        draw.rounded_rectangle([60, vip_y, 1020, vip_y + 515], radius=20, fill=self.c["card_bg"], outline=self.c["primary"], width=2)
        # 头部礼品标
        draw.text((90, vip_y + 25), "🎁 " + CTA_VIP_TITLE, font=FONTS["h2"], fill=self.c["primary"])
        # 物料清单列表
        for b_idx, bullet in enumerate(CTA_VIP_BULLETS):
            by = vip_y + 85 + b_idx * 38
            draw.text((90, by), "✔ " + bullet, font=FONTS["body_sm"], fill=self.c["text_white"])

        # 发光暗号核心区域
        code_box_y = vip_y + 255
        draw.rounded_rectangle([90, code_box_y, 990, code_box_y + 225], radius=16, fill=self.c["code_bg"], outline=self.c["secondary"], width=2)
        draw.text((540, code_box_y + 35), CTA_CODE_TITLE, font=FONTS["body_bold"], fill=self.c["text_muted"], anchor="mm")
        # 巨型暗号字符
        draw.text((540, code_box_y + 105), cta["code_main"], font=FONTS["h1"], fill=self.c["primary"], anchor="mm")
        draw.text((540, code_box_y + 175), CTA_CODE_HINT, font=FONTS["body_sm"], fill=self.c["secondary"], anchor="mm")

        # 4. 三条说明
        for g_idx, (g_title, g_desc) in enumerate(CTA_NOTES):
            gy = 860 + g_idx * 105
            draw.rounded_rectangle([60, gy, 1020, gy + 90], radius=12, fill=self.c["card_bg"], outline=self.c["card_border"], width=1)
            draw.text((90, gy + 18), g_title, font=FONTS["body_bold"], fill=self.c["secondary"])
            draw.text((90, gy + 52), g_desc, font=FONTS["body_sm"], fill=self.c["text_muted"])

        # 5. 老L品牌寄语
        draw.rounded_rectangle([60, 1195, 1020, 1295], radius=14, fill=self.c["code_bg"], outline=(40, 50, 70), width=1)
        draw.text((540, 1228), "“认准老L避坑实验室 · 每一个单机好游戏都不留遗憾”", font=FONTS["body_bold"], fill=self.c["primary"], anchor="mm")
        draw.text((540, 1265), "—— 老L (L-MOD Vault 首席极客玩家)", font=FONTS["body_sm"], fill=self.c["text_dim"], anchor="mm")

        # 6. 底部导航
        DrawingEngine.draw_bottom_footer(draw, 5, 5, "觉得有用请点赞 + 收藏 + 关注！ ➔", self.c["primary"], self.c, FONTS)
        return img


# ==============================================================================
# 6. 平台文案与分发物料生成器 (小红书 + B站动态/专栏)
# ==============================================================================
# 7 款里会改文件的 .bat（改之前另存 .bak）；其余 3 款的 .bat 只检查目录、打印提示。
# 事实来源：public/data.js 里各游戏的 batScript。脚本改了这里要跟着改。
BAT_SUMMARY = {
    "cyberpunk-2077": "把 CET 呼出键设成 ~ 键，原 bindings.json 先另存为 .bak",
    "black-myth-wukong": "把 UE4SS 的 ConsoleEnablerMod 改成 1，原 mods.txt 先另存为 .bak",
    "witcher-3": "在 general.ini 里写入 DBGConsoleOn=true，原文件先另存为 .bak",
    "baldurs-gate-3": "生成打开控制台窗口的 ScriptExtenderSettings.json，原文件先另存为 .bak",
    "elden-ring": None,
    "skyrim-se": None,
    "fallout-4": None,
}
BAT_NO_EDIT = "老L的 .bat 只检查游戏目录、打印提示，不改任何文件"

ENABLE_SUMMARY = {
    "cyberpunk-2077": "用开源的 CET 框架打开控制台",
    "black-myth-wukong": "用开源的 UE4SS 框架打开虚幻引擎自带的控制台",
    "witcher-3": "在 general.ini 里加一行，打开游戏自带的控制台",
    "baldurs-gate-3": "用开源的 Script Extender 打开控制台窗口",
    "elden-ring": "用 ModEngine2 离线加载 Mod，再配合 CT 表",
    "skyrim-se": "直接按 ~ 打开游戏自带的控制台",
    "fallout-4": "直接按 ~ 打开游戏自带的控制台",
}

# 3 套不同切入点的标题。注意：发布文案会过一遍用词替换（「修改器 / 外挂」→「第三方工具」），
# 所以别写「第三方修改器」，否则会变成「第三方第三方工具」。
TITLE_HOOKS = {
    "cyberpunk-2077": [
        "别再去下来路不明的修改器了！2077 用开源 CET 开控制台，手把手教你",
        "2077 极客自救指南：CET 控制台与救赎指令清单",
        "赛博朋克2077 开控制台保姆级教程：3 步搞定，附纯文本 .bat"
    ],
    "black-myth-wukong": [
        "黑神话手残被虎先锋劝退？教你用 UE4SS 打开引擎控制台",
        "卡关卡到摔手柄？黑神话悟空慢动作与全图鉴指令整理",
        "拒绝来路不明的外挂！黑神话悟空控制台保姆级教程"
    ],
    "witcher-3": [
        "改一行配置开启游戏自带控制台！巫师3次世代版指令与神装指南",
        "手滑选错后悔终生？用巫师3控制台指令弥补爱丽丝遗憾",
        "别再去下来路不明的修改器了！巫师3自带控制台，改一行配置就能开"
    ],
    "baldurs-gate-3": [
        "博德之门3 控制台怎么开？Script Extender 控制台窗口指南",
        "还在到处找修改器？博德之门3 用 Script Extender 开控制台",
        "告别长休食物焦虑！博德之门3调试指令与传奇神兵开荒指南"
    ],
    "elden-ring": [
        "法环黄金树幽影太折磨？离线轮椅方案：ModEngine2 + CT 表",
        "被狂龙和双月骑士虐哭？单机离线减负方案，别带进联机",
        "艾尔登法环幽影之地离线 Mod 环境保姆级教程"
    ],
    "skyrim-se": [
        "老滚5重制版任务卡关怎么救？游戏自带控制台急救指南",
        "任务NPC发呆不说话？试试用 setstage 推进任务（先存档）",
        "天际重制版控制台与16魔神器指令整理"
    ],
    "fallout-4": [
        "辐射4次世代更新后Mod全崩？控制台与降级路线指南",
        "造房子空间被锁死？用控制台指令扩建聚落，附传奇武器指令",
        "辐射4次世代版控制台保姆级教程"
    ],
}

HONEST_NOTES = [
    "这些指令和 Mod 没有逐条在游戏里实测过，版本不同可能失效；",
    "只在单机 / 离线模式下用，别带进联机；",
    "操作前先手动备份存档，老L的脚本都不备份存档。",
]


def _steps_md(game_key: str) -> str:
    lines = []
    for idx, step in enumerate(FLAGSHIP_GAMES[game_key]["setup_card"]["steps"], start=1):
        extra = step.get("path_box") or step.get("key_text") or ""
        extra = f"（`{extra}`）" if extra else ""
        lines.append(f"{idx}. **{step['title']}**：{step['detail']}{extra}")
    return "\n".join(lines)


def _bat_line(game_key: str) -> str:
    summary = BAT_SUMMARY.get(game_key)
    if summary:
        return f"老L写了一个纯文本 .bat：{summary}；可用记事本查看全部内容，不备份存档"
    return f"{BAT_NO_EDIT}；不备份存档"


class ContentGenerator:
    @staticmethod
    def generate_xiaohongshu_post(game_key: str) -> str:
        """生成小红书图文文案（只写做到的事）"""
        data = FLAGSHIP_GAMES[game_key]
        title = data["title"]
        short_title = data["short_title"]
        secret = data["secret_code"]
        radar = data["radar_code"]
        hooks = TITLE_HOOKS[game_key]
        notes = "\n".join(f"- {n}" for n in HONEST_NOTES)
        bat = data["setup_card"]["bat_note"]
        if BAT_SUMMARY.get(game_key):
            bat_block = f"*（嫌手动改麻烦的话：{_bat_line(game_key)}。脚本放在 L-MOD Vault 网站本游戏页。）*"
        else:
            bat_block = f"**{bat['title'].replace('💡 ', '')}**：\n" + "\n".join(f"- {b}" for b in bat["bullets"])

        md_content = f"""# 《{title}》小红书图文发布物料

## 📌 标题备选 (3选1)
- **【痛点避坑型】**：{hooks[0]}
- **【好奇干货型】**：{hooks[1]}
- **【教程型】**：{hooks[2]}

---

## 📝 正文（配 5 张卡片发布）

兄弟们，别再去来路不明的网站下载那些捆绑全家桶弹窗的“免费修改器”了！

很多玩家在玩【{short_title}】时，遇到 Boss 卡关或者手滑选错剧情，第一反应就是去网上搜修改器，结果要么被杀毒软件报毒，要么游戏一更新就失效、闪退……

其实这款游戏可以{ENABLE_SUMMARY[game_key]}，不用来路不明的 exe。
老L把开启步骤和常用指令整理了一份，先说清楚三件事：
{notes}

---

### ⚡ 小白 3 步：
{_steps_md(game_key)}

{bat_block}

---

### 🎮 老L场景套餐精选：
- **【手残救星·剧情体验模式】**：减少暴毙与受击硬直，手残党也能专心看主线剧情；
- **【资源自由·全图鉴解锁】**：开局财富与材料补给满载，少一点枯燥的捡垃圾；
- **【背包减负·无痛探索】**：无限耐力 / 快速旅行路标全开，少跑冤枉路；
- **【意难平救赎】**：用指令补上错过的剧情物品或好感度（能不能触发还看进度）。

完整指令清单在 L-MOD Vault 网站本游戏页，带中文说明，可以直接复制。

---

### 🎁 去哪看 / 怎么进群：
- .bat 脚本、指令清单、精选 Mod 都在 **L-MOD Vault 网站本游戏页**（链接见主页），免费看；
- 想交流 Mod 更新进度和坏档处理经验：在后台或私信发送暗号 **【{secret}】或【{radar}】**，进玩家互助群。

游戏更新以后，指令和 Mod 可能要等作者适配。更新情况看 L-MOD Vault 避坑雷达（每天比对一次 Steam 更新时间，不做实机测试）。觉得有用先**点赞 + 收藏**！

---

## 🏷️ 标签 (复制到小红书发布框)
#{short_title} #单机游戏 #Steam游戏 #单机游戏攻略 #游戏避坑指南 #游戏推荐 #老玩家自救 #Steam打折
"""
        return sanitize_text(md_content)

    @staticmethod
    def generate_bilibili_dynamic(game_key: str) -> str:
        """生成 B站动态短文 + 专栏图文 + 互动投票（只写做到的事）"""
        data = FLAGSHIP_GAMES[game_key]
        title = data["title"]
        short_title = data["short_title"]
        secret = data["secret_code"]
        radar = data["radar_code"]

        md_content = f"""# 《{title}》B站动态 / 专栏物料

## 📱 1. B站动态短文 (配 5 张卡片发布)

大家好，我是老L！

很多兄弟私信问：玩《{short_title}》卡关或者遇到意难平剧情，怎么自救？网上下的修改器经常报毒弹窗，游戏一更新还失效。

今天整理了《{short_title}》的控制台开启指南：
- 🎮 开启方式：{ENABLE_SUMMARY[game_key]}；
- 🎮 附带新手开荒、意难平救赎、二周目神装三套场景指令；
- 🛠️ {_bat_line(game_key)}；
- ⚠️ 指令没有逐条实测，只在单机 / 离线下用，操作前先备份存档。

5 联图教程见配图，长按即可保存！.bat、指令清单和 Mod 介绍在 L-MOD Vault 网站本游戏页；想进玩家互助群交流，在后台或私信发送暗号【{secret}】或【{radar}】。

---

## 📰 2. B站专栏排版 (图文专栏)

### 引言：为什么不推荐来路不明的修改器？
有些修改器会捆绑弹窗或后门，而且按内存地址改数据，游戏一更新就容易失效甚至闪退。很多大作可以用游戏自带的控制台，或者开源、源码公开的框架（如 CET、UE4SS、Script Extender）做同样的事，来路更清楚。

### 一、先说清楚
- **游戏本体**：{title}
- **资料来源**：老L整理的开启步骤与常用指令，**没有逐条在游戏里实测**；
- **游戏更新以后**：框架和指令可能要等作者适配，更新情况看 L-MOD Vault 避坑雷达（每天比对一次 Steam 更新时间，不做实机测试，所以只说「可能」）；
- **存档**：老L的脚本都不备份存档，操作前请自己复制存档文件夹。

### 二、开启步骤
{_steps_md(game_key)}

### 三、场景化指令套餐精要
（详细代码见动态配图 Slide 3，或 L-MOD Vault 网站本游戏页）
- 手残救星模式：减少受击硬直，适合专心看剧情；
- 资源图鉴自由：开局财富补给，神装自由打造；
- 意难平救赎：补上错过的剧情物品或好感度（能不能触发还看进度）。

### 四、游戏更新以后
Steam 推送更新后，先看 L-MOD Vault 避坑雷达：刚更新的游戏会标黄或标红。按 exe 版本挂钩的框架可能要等作者发新版，着急的话先别更新。

---

## 🗳️ 3. 互动投票引导

**投票主题**：你在玩《{short_title}》时，最让你抓狂或意难平的是哪一点？
- 选项 A：高难度 Boss 疯狂卡关，手残被虐到怀疑人生
- 选项 B：开荒期金币物资极度匮乏，天天翻垃圾桶
- 选项 C：不小心选错对话分支，错过了隐藏真结局/心仪队友恋爱
- 选项 D：跑图全靠两条腿，经常在迷宫天堑里迷路转圈
- 选项 E：纯粹路过点赞投币！
"""
        return sanitize_text(md_content)


# ==============================================================================
# 7. 运营手册生成器 (OPERATION_PLAYBOOK.md)
# 手册不过用词替换：替换表那一节要写原词，过了替换就成了「调试指令 → 调试指令」。
# ==============================================================================
class PlaybookGenerator:
    """运营手册是运营资料（首评话术、用词替换、社群规则），模板在 private/social_ops/playbook_template.md，不进仓库。"""
    TEMPLATE_PATH = PRIVATE_OPS_DIR / "playbook_template.md"

    @staticmethod
    def generate_playbook():
        """有模板就原样返回；没有模板返回 None，跳过运营手册。"""
        try:
            return PlaybookGenerator.TEMPLATE_PATH.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None


# ==============================================================================
# 8. 主流程执行总装与批量出图
# ==============================================================================
def _write_everywhere(rel_path: str, data: bytes) -> list:
    """同一份产物写进 social_distribution/ 和 public/social_distribution/ 两处。"""
    written = []
    for base in OUTPUT_DIRS:
        target = base / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        written.append(target)
    return written


def _write_private(rel_path: str, data: bytes) -> list:
    """运营资料只写 private/social_ops/，不写进公开仓库和站点。"""
    target = PRIVATE_OPS_DIR / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return [target]


def run_distribution_assembly(target_games=None) -> int:
    print("=" * 70)
    print("🚀 L-MOD Vault 社交卡片出图与分发物料生成")
    print("=" * 70)

    start_time = time.time()
    OVERFLOW_LOG.clear()

    games_to_process = target_games or list(FLAGSHIP_GAMES.keys())
    generated_images = []
    generated_docs = []

    for gid in games_to_process:
        if gid not in FLAGSHIP_GAMES:
            print(f"⚠️ 跳过未知游戏 ID: {gid}")
            continue

        gdata = FLAGSHIP_GAMES[gid]
        dir_name = gdata["dir_name"]
        print(f"\n🎮 正在生成：[{gdata['title']}] ...")

        # 1. 渲染 5 张卡片
        renderer = CardRenderer(gid)
        cards = [
            ("card_1_hook.png", renderer.render_card_1_hook),
            ("card_2_setup.png", renderer.render_card_2_setup),
            ("card_3_commands.png", renderer.render_card_3_commands),
            ("card_4_mods.png", renderer.render_card_4_mods),
            ("card_5_cta.png", renderer.render_card_5_cta),
        ]

        for filename, render_fn in cards:
            img = render_fn()
            buf = io.BytesIO()
            img.save(buf, "PNG", optimize=True)
            written = _write_everywhere(f"{dir_name}/images/{filename}", buf.getvalue())
            size_kb = len(buf.getvalue()) / 1024.0
            generated_images.extend((str(t), img.size, size_kb) for t in written)
            print(f"  🖼️  {filename} ({img.size[0]}x{img.size[1]}, {size_kb:.1f} KB) ×{len(written)}")

        # 2. 小红书文案
        written = _write_private(f"{dir_name}/xiaohongshu_post.md",
                                 ContentGenerator.generate_xiaohongshu_post(gid).encode("utf-8"))
        generated_docs.extend(str(t) for t in written)
        print("  📝 xiaohongshu_post.md")

        # 3. B站动态/专栏
        written = _write_private(f"{dir_name}/bilibili_dynamic.md",
                                 ContentGenerator.generate_bilibili_dynamic(gid).encode("utf-8"))
        generated_docs.extend(str(t) for t in written)
        print("  📺 bilibili_dynamic.md")

    # 4. 运营手册（模板在 private/social_ops/，没有就跳过）
    playbook = PlaybookGenerator.generate_playbook()
    if playbook is None:
        print("\n📘 OPERATION_PLAYBOOK.md：没有 private/social_ops/playbook_template.md，跳过")
    else:
        written = _write_private("OPERATION_PLAYBOOK.md", playbook.encode("utf-8"))
        generated_docs.extend(str(t) for t in written)
        print("\n📘 OPERATION_PLAYBOOK.md")

    elapsed = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"⏱️  总耗时: {elapsed:.2f} 秒")
    print(f"📦 游戏: {len(games_to_process)} 款 · PNG 输出: " + ", ".join(os.path.relpath(d, BASE_DIR) for d in OUTPUT_DIRS)
          + f" · 文案与手册: {os.path.relpath(PRIVATE_OPS_DIR, BASE_DIR)}（不进仓库）")
    print(f"🖼️  PNG: {len(generated_images)} 个文件 · 📄 文案与手册: {len(generated_docs)} 个文件")
    if OVERFLOW_LOG:
        print("\n❌ 有文字超出卡片内容区（改短文案再出图）：")
        for line in OVERFLOW_LOG:
            print("  • " + line)
        return 1
    print("✅ 所有文字都在卡片内容区内")
    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="L-MOD Vault 社交卡片出图与分发物料生成")
    parser.add_argument("--game", type=str, help="只生成单款游戏 (如 cyberpunk-2077)；默认 7 款全部")
    args = parser.parse_args()

    targets = [args.game] if args.game else None
    sys.exit(run_distribution_assembly(targets))
