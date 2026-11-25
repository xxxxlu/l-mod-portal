#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/ai_social_publisher.py
L-MOD Vault - AI 社交矩阵文案与合规出图自动化生成引擎 (Milestone 4)
Automated Multi-Platform Social Copy Publisher

Capabilities:
1. Generates ready-to-publish social copy for Xiaohongshu (小红书), Bilibili, and Zhihu.
2. Optional word replacement from private/social_ops/word_map.json (not in the repo).
3. Generates high-CTR headlines, scenario bullet points, and trending topic tags.
4. Previews generated copy or saves it to private/social_ops/ (gitignored, never published).

口径与 scripts/render_cards_png.py 文件头一致（2026-11-19）：不写「实测 / 实机校验 / 认证补丁 /
零封号 / 实时雷达 / 100 款合集」；雷达状态按 v2 规则读 radarReason（见 docs/RADAR_V2_CONTRACT.md），
不再读 verifiedPatch 和旧的三色文案。只写 private/social_ops/<id>_social_copy.txt（加 --save 时；private/ 不进仓库）。
"""

import os
import sys
import json
import argparse
import datetime
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
DATA_JS_PATH = os.path.join(BASE_DIR, 'public/data.js')
OUTPUT_DIR = os.path.join(BASE_DIR, 'private', 'social_ops')

# 发布文案用词替换表：在 private/social_ops/word_map.json（不进仓库），没有就原样输出
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from social_word_map import load_word_map  # noqa: E402

ANTI_BAN_DICT = dict(load_word_map("plain"))

# 与网站雷达页同一套状态文案（v2 规则）
RADAR_REASON_TEXT = {
    "recent-update-hooks": "🔴 先别更新：刚更新，常用 Mod 框架可能要等适配",
    "recent-update": "🟡 留意更新：14 天内刚更新",
    "trainer-behind": "🟡 留意更新：近 90 天内有更新，修改器还没跟上",
    "quiet": "🟢 近期平稳：近 14 天没有新版本",
}


def radar_status_text(game):
    if (game.get('steamAppId') or 0) <= 0:
        return "⚪ 不在 Steam 上，不巡检"
    reason = game.get('radarReason')
    if reason in RADAR_REASON_TEXT:
        return RADAR_REASON_TEXT[reason]
    if game.get('compatibilityStatus'):
        return "旧版巡检结果，可能误报，以避坑雷达页面为准"
    return "⚪ 还没有巡检记录"


def load_games():
    """只读：优先 src/data/games_top100.json（本地未入库），没有就解析 public/data.js 的 GAMES_DATA。"""
    if os.path.exists(GAMES_JSON_PATH):
        with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    start = text.index('[', text.index('window.GAMES_DATA ='))
    games, _ = json.JSONDecoder().raw_decode(text, start)
    return games


def desensitize(text):
    """Applies the private word table if present; otherwise returns the text unchanged."""
    result = text
    for bad, good in ANTI_BAN_DICT.items():
        result = result.replace(bad, good)
    return result


def generate_copy_for_game(game, platform="all"):
    title = (game.get('titles') and game.get('titles', {}).get('zh-CN')) or game.get('title')
    rank = game.get('rank', 99)
    shortcut = game.get('consoleShortcut', '~ 键呼出')
    status_text = radar_status_text(game)

    # Helper to extract name and code safely
    def format_cmd(c):
        if isinstance(c, str):  # 有的游戏 popularCommands 是纯字符串（如艾尔登法环）
            return f"▫️ {c}"
        raw_name = c.get('name')
        if isinstance(raw_name, dict):
            name = raw_name.get('zh-CN') or raw_name.get('en') or list(raw_name.values())[0]
        else:
            name = str(raw_name or '常用指令')
        code = c.get('code') or c.get('command') or ''
        return f"▫️ {name}: `{code}`"

    # Popular commands preview
    cmd_snippets = []
    if game.get('popularCommands'):
        for c in game['popularCommands'][:4]:
            cmd_snippets.append(format_cmd(c))
    elif game.get('consoleCategories'):
        for cat in game['consoleCategories'][:2]:
            for c in cat.get('commands', [])[:2]:
                cmd_snippets.append(format_cmd(c))

    cmds_formatted = "\n".join(cmd_snippets) if cmd_snippets else "▫️ 一键开启无敌与全资源探索"

    # 1. Xiaohongshu (小红书) Format
    redbook = f"""📕 【小红书爆款文案 · Rank #{rank}《{title}》】
━━━━━━━━━━━━━━━━━━━━━━━━
🔥 标题：终于找到了！《{title}》控制台指令与避坑指南（建议收藏）

👋 宝子们！单机打到中后期卡关或者想爽玩二周目？
老L整理了《{title}》常用的【控制台指令】与【避坑指南】！
先说清楚：指令没有逐条在游戏里实测，版本不同可能失效，用之前先手动备份存档。

✨ 【必用场景化指令】
{cmds_formatted}

🎮 【怎么在游戏里开启？】
进入游戏后，按下【{shortcut}】呼出输入框，粘贴后回车！

🛡️ 【Steam 避坑雷达状态】
当前状态：{status_text}
（雷达每天比对一次 Steam 更新时间，不做实机测试，所以只说「可能」）
只在单机 / 离线下用，别带进联机。完整指令清单在 L-MOD Vault 网站本游戏页（链接见主页）。

🏷️ 标签：
#{title} #{title}攻略 #Steam单机游戏 #单机游戏推荐 #单机游戏避坑 #Steam好游戏 #游戏日常
"""

    # 2. Bilibili (B站动态) Format
    bilibili = f"""📺 【B站专栏与动态文案 · 《{title}》】
━━━━━━━━━━━━━━━━━━━━━━━━
【老L单机智库】全球 100 款单机神作 · 第 {rank} 期：《{title}》

很多老哥私信问更新后旧 Mod 崩溃、控制台代码打不开的问题，今天把整理好的指令与避坑指南放出来：

📌 Steam 避坑雷达状态：{status_text}
📌 控制台唤出方式：{shortcut}
📌 核心代码预览（没有逐条实测，执行前先存档）：
{cmds_formatted}

不接广告，无需翻墙，不用来路不明的下载器。
单机游戏资料库与 Steam 避坑雷达（每天比对一次 Steam 更新时间）请到 L-MOD Vault 网站查阅！
"""

    # Optional word table (private, not in the repo)
    clean_redbook = desensitize(redbook)
    clean_bilibili = desensitize(bilibili)

    return {
        "redbook": clean_redbook,
        "bilibili": clean_bilibili
    }


def main():
    parser = argparse.ArgumentParser(description="L-MOD AI Social Copy Publisher")
    parser.add_argument('--game', type=str, default="cyberpunk-2077", help="游戏 ID (默认 cyberpunk-2077)")
    parser.add_argument('--save', action='store_true', help="将文案保存到 private/social_ops/（不进仓库）")
    args = parser.parse_args()

    games = load_games()

    target = next((g for g in games if g['id'] == args.game), None)
    if not target:
        print(f"❌ 未找到游戏 ID: {args.game}")
        return

    copies = generate_copy_for_game(target)

    print("=" * 72)
    print("📢 L-MOD Vault - AI 社交合规宣发文案生成引擎")
    print("=" * 72)
    print(copies['redbook'])
    print("-" * 72)
    print(copies['bilibili'])
    print("=" * 72)

    if args.save:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_file = os.path.join(OUTPUT_DIR, f"{args.game}_social_copy.txt")
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(copies['redbook'] + "\n\n" + "=" * 60 + "\n\n" + copies['bilibili'])
        print(f"💾 文案已保存至: {out_file}")


if __name__ == '__main__':
    main()
