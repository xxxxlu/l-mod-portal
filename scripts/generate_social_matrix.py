#!/usr/bin/env python3
"""
generate_social_matrix.py
L-MOD Vault 社交矩阵工业级自动化生成引擎 (v1.0)
功能：
1. 发布文案过一遍平台用词替换（只换说法，不许换出没做过的承诺）；
2. 从游戏数据抽取并组装「小红书 5 联图卡片数据」与「B站动态专栏文案」；
   数据优先读 src/data/games_top100.json（本地未入库），没有就只读 public/data.js 的 GAMES_DATA；
3. 输出 HTML 预览页面 (3:4 比例) 与剪贴板文案，只写 public/social_matrix/<id>_social_cards.html；
4. 口径与 scripts/render_cards_png.py 文件头一致：不写实测 / 已校验 / 零封号 / 秒推网盘 / 连夜更新。
"""

import json
import os
import sys
import argparse
from pathlib import Path

# 路径基准
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "src" / "data" / "games_top100.json"
DATA_JS_PATH = BASE_DIR / "public" / "data.js"
OUTPUT_DIR = BASE_DIR / "public" / "social_matrix"
FLAGSHIP_IDS = ["cyberpunk-2077", "black-myth-wukong", "witcher-3", "baldurs-gate-3",
                "elden-ring", "skyrim-se", "fallout-4"]
NOTE_BADGE = "老L整理 · 未逐条实测"

# ========================================================
# 1. 发布文案用词替换表：和 render_cards_png.py 同一张，在 private/social_ops/word_map.json（不进仓库）
# ========================================================
from social_word_map import load_word_map

DESENSITIZATION_MAP = load_word_map("regex")

# 爆款情绪与场景化包装模板 (针对游戏类型与痛点)
GAME_HOOK_PRESETS = {
    "cyberpunk-2077": {
        "title_hook": "2077 也能开控制台！开源 CET 框架极客自救指南",
        "pain_point": "还在去来路不明的网站下修改器？教你用开源 CET 框架打开控制台，只在单机用。",
        "bundle_tag": "⚡ 赛博救赎全神装套件"
    },
    "black-myth-wukong": {
        "title_hook": "黑神话手残被虎先锋劝退？用 UE4SS 打开引擎控制台教程",
        "pain_point": "卡关卡到摔手柄？教你用控制台慢动作和全图鉴指令，体验齐天大圣真神力！",
        "bundle_tag": "🐒 大圣觉醒全法术破荒包"
    },
    "witcher-3": {
        "title_hook": "巫师3次世代版隐藏彩蛋：改一行配置开启游戏自带控制台",
        "pain_point": "手滑选错后悔终生？用控制台指令弥补爱丽丝遗憾，全师匠神装一键毕业！",
        "bundle_tag": "🐺 猎魔人传奇救赎大礼包"
    },
    "baldurs-gate-3": {
        "title_hook": "博德之门3 控制台怎么开？Script Extender 控制台窗口指南",
        "pain_point": "装 Mod 后闪退？先看清版本和前置，再用开源 Script Extender 的控制台窗口。",
        "bundle_tag": "🎲 费伦大陆天神下凡组合包"
    },
    "elden-ring": {
        "title_hook": "法环黄金树幽影太折磨？离线轮椅方案：ModEngine2 + CT 表",
        "pain_point": "被狂龙和双月骑士虐哭？单机离线减负方案，别把改过的存档带进联机。",
        "bundle_tag": "💍 艾尔登之王全追忆轮椅包"
    },
    "skyrim-se": {
        "title_hook": "老滚5重制版恶性卡关/闪退怎么救？B社原生控制台避坑急救指南",
        "pain_point": "任务NPC不说话卡住？试试用 setstage 推进任务（先存档），全魔神器与龙吼指令一并整理。",
        "bundle_tag": "🐉 龙裔降临全魔神器破荒包"
    },
    "fallout-4": {
        "title_hook": "辐射4次世代大更新Mod全崩溃？游戏自带控制台与传奇武器附魔指南",
        "pain_point": "造房子空间被锁死？教你用原生指令无限扩建聚落，全传奇双弹爆破武器自定义附魔！",
        "bundle_tag": "⚡ 废土之王全传奇军备包"
    }
}


# 游戏数据（GAMES_DATA）里的自由文本有些自带承诺，比如「所有代码均针对 2.0/2.13 版本进行了真实校验」
# 「100%安全离线防封指南」「100% 零封号」。数据本身不归社媒脚本改，但不能原样搬上社媒卡片：
# 按分句（。！？；，换行）过滤，带这些说法的分句整句去掉，并打印出来方便核对。
import re as _re
# 「绝对前置」「100% 快速旅行路标」这类只是形容词，不算承诺，所以只匹配带承诺的组合
CLAIM_RE = _re.compile(r"实测|实机|真实校验|已校验|认证|绝无|绝对安全|绝对不连|100%\s*(?:安全|零|兼容|纯净|无|通过|对齐)"
                       r"|零封|无封禁|封号风险|防封|免封|零闪退|零报毒|零木马|完全隔离|物理隔离")
_CLAUSE_RE = _re.compile(r"[^。！？!?；;，,\n]*[。！？!?；;，,\n]?")
DROPPED_CLAUSES = []


def strip_claims(text, where=""):
    if isinstance(text, dict):
        text = text.get("zh-CN") or text.get("en") or ""
    if not text:
        return text
    kept = []
    for clause in _CLAUSE_RE.findall(str(text)):
        if not clause:
            continue
        if CLAIM_RE.search(clause):
            DROPPED_CLAUSES.append(f"{where}: {clause.strip()}")
            # 去掉的分句如果带换行，保留换行，免得把两条步骤粘在一起
            if clause.endswith("\n"):
                kept.append("\n")
            continue
        kept.append(clause)
    out = "".join(kept).strip()
    # 句尾残留的逗号 / 顿号换成句号
    out = _re.sub(r"[，,、]\s*(\n|$)", r"。\1", out)
    return out


def sanitize_text(text) -> str:
    """按用词替换表替换（表不在仓库里，没有就原样返回），支持字符串、多语言字典或 None"""
    import re
    if text is None:
        return ""
    if isinstance(text, dict):
        text = text.get("zh-CN") or text.get("en") or str(text)
    if not isinstance(text, str):
        text = str(text)

    result = text
    for pattern, replacement in DESENSITIZATION_MAP:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


_GAMES_CACHE = None

def load_games():
    """读游戏数据（只读）：优先 src/data/games_top100.json，没有就解析 public/data.js 的 GAMES_DATA。"""
    global _GAMES_CACHE
    if _GAMES_CACHE is not None:
        return _GAMES_CACHE
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            _GAMES_CACHE = json.load(f)
        print(f"📚 数据来源: {DATA_PATH.relative_to(BASE_DIR)}")
    elif DATA_JS_PATH.exists():
        text = DATA_JS_PATH.read_text(encoding="utf-8")
        marker = "window.GAMES_DATA ="
        start = text.index(marker) + len(marker)
        start = text.index("[", start)
        _GAMES_CACHE, _ = json.JSONDecoder().raw_decode(text, start)
        print(f"📚 数据来源: {DATA_JS_PATH.relative_to(BASE_DIR)} (GAMES_DATA，只读)")
    else:
        raise FileNotFoundError(f"Database not found: {DATA_PATH} / {DATA_JS_PATH}")
    return _GAMES_CACHE


def extract_game_matrix_data(game_id: str):
    """从数据库抽取指定游戏的矩阵素材数据"""
    games = load_games()

    target_game = None
    for g in games:
        if g.get("id") == game_id:
            target_game = g
            break

    if not target_game:
        raise ValueError(f"Game with id '{game_id}' not found in database.")

    preset = GAME_HOOK_PRESETS.get(game_id, {
        "title_hook": f"{target_game.get('title')} 控制台与探索指南",
        "pain_point": "教你开启游戏的控制台功能；只在单机用，操作前先存档。",
        "bundle_tag": "🎮 核心探索增益包"
    })

    # 提取精选指令（优先从 popularCommands 与 核心分类抽取）
    commands_showcase = []
    for p in target_game.get("popularCommands", [])[:5]:
        if isinstance(p, dict):
            zh_name = p.get("zh-CN") or p.get("name", "")
            code_str = p.get("code", "")
        else:
            zh_name = str(p)
            code_str = str(p)
        commands_showcase.append({
            "name": sanitize_text(strip_claims(zh_name, f"{game_id} 指令名")),
            "code": code_str
        })

    # 若 popularCommands 不足，从 consoleCategories 补充
    if len(commands_showcase) < 4:
        for cat in target_game.get("consoleCategories", []):
            for cmd in cat.get("commands", [])[:2]:
                if len(commands_showcase) >= 6:
                    break
                cmd_name = cmd.get("name", "")
                if isinstance(cmd_name, dict):
                    zh_name = cmd_name.get("zh-CN", cmd_name.get("en", ""))
                else:
                    zh_name = str(cmd_name)
                commands_showcase.append({
                    "name": sanitize_text(strip_claims(zh_name, f"{game_id} 指令名")),
                    "code": cmd.get("code", "")
                })

    # 提取精选 Mod (Top 3)
    mods_showcase = []
    for mod in target_game.get("curatedMods", [])[:3]:
        mod_name = mod.get("title") or mod.get("name", "精选模组")
        mods_showcase.append({
            "name": sanitize_text(strip_claims(mod_name, f"{game_id} Mod 名")),
            "author": mod.get("author", "Community"),
            "downloads": mod.get("downloads", "100K+"),
            "desc": sanitize_text(strip_claims(sanitize_text(mod.get("desc", "")), f"{game_id} Mod 介绍"))
        })

    # 组合交付数据结构
    card_data = {
        "game_id": game_id,
        "title": target_game.get("title"),
        "genre": target_game.get("genre"),
        "developer": target_game.get("developer"),
        "releaseYear": target_game.get("releaseYear"),
        "steamRating": target_game.get("steamRating"),
        "patchBadge": NOTE_BADGE,
        "titleHook": preset["title_hook"],
        "painPoint": preset["pain_point"],
        "bundleTag": preset["bundle_tag"],
        "consoleShortcut": target_game.get("consoleShortcut", "`~` 键"),
        "enableGuide": strip_claims(sanitize_text(target_game.get("consoleEnableGuide", {}).get("zh-CN", "")), f"{game_id} 开启步骤"),
        "commands": commands_showcase,
        "mods": mods_showcase,
        # 以前是「输入暗号【Cybe】获取纯净一键包」：取英文标题前 4 个字母当暗号，而且没有一键包
        "trafficSecretKey": f"后台或私信发送暗号【{target_game.get('radarSecretCode') or '老L单机888'}】进玩家互助群"
    }

    return card_data


def generate_html_card_preview(card_data: dict) -> str:
    """生成小红书/B站图文卡片 5 联图标准 HTML 预览组件"""
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{card_data['title']} - 社交矩阵图文卡片套件</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900&display=swap');
    body {{
      font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #090a0f;
    }}
    .card-canvas {{
      width: 400px;
      height: 533px; /* 3:4 比例 (相当于小红书 1080x1440) */
      box-shadow: 0 20px 40px rgba(0,0,0,0.6);
      position: relative;
      overflow: hidden;
    }}
    .neon-border {{
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}
  </style>
</head>
<body class="p-8 text-white min-h-screen">
  <div class="max-w-7xl mx-auto">
    <div class="mb-8 flex items-center justify-between border-b border-zinc-800 pb-4">
      <div>
        <h1 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400">
          L-MOD 实验室 · 社交平台标准化 5 联图套件
        </h1>
        <p class="text-zinc-400 text-sm mt-1">游戏：{card_data['title']} | 说明：<span class="text-emerald-400 font-bold">资料整理，指令没有逐条实测</span></p>
      </div>
      <div class="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5">
        <span>🛡️</span> {card_data['patchBadge']}
      </div>
    </div>

    <!-- 5 联图水平展示架 -->
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">

      <!-- ================= CARD 1: 爆款封面 ================= -->
      <div class="card-canvas rounded-2xl bg-gradient-to-b from-zinc-900 via-zinc-950 to-black p-5 flex flex-col justify-between neon-border">
        <div>
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 bg-red-500/20 text-red-400 border border-red-500/30 rounded-md text-[10px] font-bold tracking-wider uppercase">
              🔥 避坑排雷
            </span>
            <span class="text-[11px] text-zinc-400 font-mono">L-MOD VAULT</span>
          </div>

          <div class="mt-6">
            <span class="inline-block px-2 py-0.5 bg-yellow-400 text-black text-xs font-black rounded mb-2">
              隐藏功能曝光
            </span>
            <h2 class="text-xl font-black leading-tight tracking-tight text-white">
              {card_data['titleHook']}
            </h2>
          </div>

          <div class="mt-4 p-3 bg-zinc-900/80 rounded-xl border border-zinc-800">
            <p class="text-zinc-300 text-xs leading-relaxed">
              {card_data['painPoint']}
            </p>
          </div>
        </div>

        <div>
          <div class="bg-gradient-to-r from-blue-600/30 to-purple-600/30 border border-blue-500/30 rounded-xl p-3 flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center shrink-0 font-bold text-sm">
              ✓
            </div>
            <div class="text-[11px] text-zinc-200">
              <p class="font-bold text-white">不用来路不明的 exe</p>
              <p class="text-zinc-400">开源框架或游戏自带控制台 · 只在单机用</p>
            </div>
          </div>
          <div class="mt-3 text-center text-[10px] text-zinc-500 font-mono">
            SLIDE 1 / 5 · 左右滑动查看手把手教程
          </div>
        </div>
      </div>

      <!-- ================= CARD 2: 打开控制台 ================= -->
      <div class="card-canvas rounded-2xl bg-gradient-to-b from-zinc-900 to-black p-5 flex flex-col justify-between neon-border">
        <div>
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-md text-[10px] font-bold tracking-wider">
              ⚡ 打开控制台
            </span>
            <span class="text-[11px] text-zinc-400 font-mono">STEP-BY-STEP</span>
          </div>

          <h3 class="text-lg font-black text-white mt-4">
            小白 3 步唤醒控制台
          </h3>

          <div class="mt-4 space-y-2.5">
            <div class="p-2.5 rounded-xl bg-zinc-900/90 border border-zinc-800 flex gap-2.5 items-start">
              <span class="w-5 h-5 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold shrink-0">1</span>
              <div>
                <p class="text-xs font-bold text-zinc-100">定位游戏根目录</p>
                <p class="text-[11px] text-zinc-400 mt-0.5">Steam 库右键游戏 ➔ 管理 ➔ 浏览本地文件</p>
              </div>
            </div>

            <div class="p-2.5 rounded-xl bg-zinc-900/90 border border-zinc-800 flex gap-2.5 items-start">
              <span class="w-5 h-5 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold shrink-0">2</span>
              <div>
                <p class="text-xs font-bold text-zinc-100">配置底层开关或插件</p>
                <p class="text-[11px] text-zinc-400 mt-0.5 line-clamp-2">{card_data['enableGuide'] or '按网站本游戏页的步骤操作'}</p>
              </div>
            </div>

            <div class="p-2.5 rounded-xl bg-zinc-900/90 border border-zinc-800 flex gap-2.5 items-start">
              <span class="w-5 h-5 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold shrink-0">3</span>
              <div>
                <p class="text-xs font-bold text-zinc-100">进游戏按下快捷键</p>
                <p class="text-[11px] text-emerald-400 font-bold mt-0.5">控制台唤醒快捷键：{card_data['consoleShortcut']}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="p-2.5 bg-yellow-500/10 border border-yellow-500/20 rounded-xl text-[10px] text-yellow-300">
          💡 老L写的 .bat 在 L-MOD Vault 网站本游戏页，纯文本，可用记事本查看；脚本不备份存档。
        </div>
      </div>

      <!-- ================= CARD 3: 核心功能指令清单 ================= -->
      <div class="card-canvas rounded-2xl bg-gradient-to-b from-zinc-900 to-black p-5 flex flex-col justify-between neon-border">
        <div>
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 bg-purple-500/20 text-purple-400 border border-purple-500/30 rounded-md text-[10px] font-bold tracking-wider">
              {card_data['bundleTag']}
            </span>
            <span class="text-[11px] text-zinc-400 font-mono">COMMANDS</span>
          </div>

          <h3 class="text-lg font-black text-white mt-4">
            常用高频逃课调试指令
          </h3>

          <div class="mt-3 space-y-2">
            {''.join([f'''
            <div class="p-2 rounded-lg bg-zinc-900/90 border border-zinc-800">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-zinc-200">{cmd['name']}</span>
              </div>
              <code class="block mt-1 text-[10px] text-emerald-400 font-mono bg-black/60 px-2 py-1 rounded truncate">
                {cmd['code']}
              </code>
            </div>
            ''' for cmd in card_data['commands'][:4]])}
          </div>
        </div>

        <div class="text-[10px] text-zinc-400 text-center font-mono">
          ※ 指令没有逐条实测，执行前先存档；更多指令见网站本游戏页
        </div>
      </div>

      <!-- ================= CARD 4: 必备纯净模组 ================= -->
      <div class="card-canvas rounded-2xl bg-gradient-to-b from-zinc-900 to-black p-5 flex flex-col justify-between neon-border">
        <div>
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-md text-[10px] font-bold tracking-wider">
              🛠️ 必备优化
            </span>
            <span class="text-[11px] text-zinc-400 font-mono">CURATED MODS</span>
          </div>

          <h3 class="text-lg font-black text-white mt-4">
            解决痛点 · 精选 Mod
          </h3>

          <div class="mt-3 space-y-2.5">
            {''.join([f'''
            <div class="p-2.5 rounded-xl bg-zinc-900/90 border border-zinc-800">
              <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-white truncate max-w-[180px]">{mod['name']}</span>
                <span class="text-[10px] text-zinc-400">{mod['downloads']} 下</span>
              </div>
              <p class="text-[10px] text-zinc-400 mt-1 line-clamp-2 leading-relaxed">
                {mod['desc']}
              </p>
            </div>
            ''' for mod in card_data['mods']])}
          </div>
        </div>

        <div class="p-2.5 bg-zinc-800/60 rounded-xl text-[10px] text-zinc-400">
          🔒 装之前看清 Mod 页写的游戏版本和前置；先备份存档。
        </div>
      </div>

      <!-- ================= CARD 5: 转化与防失联 ================= -->
      <div class="card-canvas rounded-2xl bg-gradient-to-b from-zinc-900 via-purple-950/40 to-black p-5 flex flex-col justify-between border border-purple-500/40">
        <div>
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 bg-pink-500/20 text-pink-400 border border-pink-500/30 rounded-md text-[10px] font-bold tracking-wider">
              🚀 粉丝专属
            </span>
            <span class="text-[11px] text-zinc-400 font-mono">VIP ACCESS</span>
          </div>

          <h3 class="text-lg font-black text-white mt-4">
            更新提醒与资料入口
          </h3>

          <div class="mt-4 p-4 rounded-xl bg-purple-900/20 border border-purple-500/30 text-center">
            <div class="text-3xl mb-2">🎁</div>
            <p class="text-xs font-bold text-purple-200">L-MOD Vault 网站本游戏页（免费）</p>
            <p class="text-[11px] text-zinc-400 mt-1">.bat 脚本 · 指令清单 · 精选 Mod · 更新提醒</p>
            
            <div class="mt-4 p-2.5 bg-black/80 rounded-lg border border-purple-400/40">
              <span class="text-xs text-yellow-300 font-mono font-bold">{card_data['trafficSecretKey']}</span>
            </div>
          </div>

          <div class="mt-4 space-y-1.5 text-[11px] text-zinc-300">
            <p class="flex items-center gap-1.5"><span>📡</span> <span>避坑雷达每天比对一次 Steam 更新时间（不做实机测试）</span></p>
            <p class="flex items-center gap-1.5"><span>💾</span> <span>存档自己备份：老L的脚本都不备份存档</span></p>
            <p class="flex items-center gap-1.5"><span>💬</span> <span>玩家互助群：不接广告，群文件不放 exe</span></p>
          </div>
        </div>

        <div class="text-center text-[10px] text-zinc-400">
          关注老L · 每一个单机好游戏都不留遗憾
        </div>
      </div>

    </div>

    <!-- 剪贴板文案输出区 -->
    <div class="mt-10 bg-zinc-900 p-6 rounded-2xl border border-zinc-800">
      <h3 class="text-lg font-bold text-white mb-2 flex items-center gap-2">
        <span>📋</span> 平台合规发布文案草稿 (小红书/B站动态直接复制)
      </h3>
      <textarea class="w-full h-40 bg-black/60 border border-zinc-700 rounded-xl p-4 text-xs font-mono text-zinc-200 focus:outline-none focus:border-blue-500" readonly>
标题：{card_data['titleHook']}

兄弟们，别再去来路不明的网站下载那些带全家桶弹窗的“免费修改器”了！
很多单机大作可以用游戏自带的控制台，或者开源、源码公开的框架做到同样的事。

老L整理了这套【{card_data['bundleTag']}】：

✨ 核心亮点：
1. 控制台呼出方式：{card_data['consoleShortcut']}；
2. 包含全图鉴神装、剧情卡关抢救、探索无痛减负；
3. 先说清楚：指令没有逐条实测，只在单机 / 离线下用，操作前先备份存档（老L的脚本不备份存档）。

📌 去哪看：
.bat 脚本、指令清单和精选 Mod 在 L-MOD Vault 网站本游戏页（链接见主页）；{card_data['trafficSecretKey']}。
游戏更新以后指令和 Mod 可能要等作者适配，更新情况看避坑雷达，建议先收藏！

#单机游戏 #{card_data['title']} #游戏攻略 #Steam游戏 #单机游戏推荐 #游戏避坑指南
      </textarea>
    </div>
  </div>
</body>
</html>
"""
    return html_content


def main():
    parser = argparse.ArgumentParser(description="L-MOD Vault 社交矩阵工业级自动化生成引擎")
    parser.add_argument("game_id", nargs="?", default="cyberpunk-2077", help="目标游戏ID (如 cyberpunk-2077, black-myth-wukong)")
    parser.add_argument("--all", action="store_true", help="批量生成全部 7 款旗舰游戏的卡片矩阵")
    parser.add_argument("--render-png", action="store_true", help="同步调用高清 PNG 卡片渲染引擎与分发物料总装包")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    target_games = FLAGSHIP_IDS if args.all else [args.game_id]

    failed = False
    for gid in target_games:
        try:
            print(f"🚀 正在为游戏 [{gid}] 自动化生成社交矩阵素材与合规卡片...")
            card_data = extract_game_matrix_data(gid)
            html = generate_html_card_preview(card_data)
            out_file = OUTPUT_DIR / f"{gid}_social_cards.html"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"✅ 生成成功！预览文件已写入: {out_file}")
        except Exception as e:
            print(f"❌ 失败 [{gid}]: {e}")
            failed = True

    if DROPPED_CLAUSES:
        print("\n✂️  游戏数据里带承诺的分句，没有搬上社媒卡片（数据本身未改）：")
        for line in DROPPED_CLAUSES:
            print("  • " + line)

    if args.render_png:
        print("\n🖼️ 正在触发工业级 PNG 高清卡片与物料总装引擎...")
        try:
            from render_cards_png import run_distribution_assembly
            if run_distribution_assembly(target_games):
                failed = True
        except Exception as e:
            print(f"❌ PNG 出图引擎执行失败: {e}")
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
