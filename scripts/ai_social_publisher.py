#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/ai_social_publisher.py
L-MOD Vault - AI 社交矩阵文案与合规出图自动化生成引擎 (Milestone 4)
Automated Multi-Platform Copywriting & Anti-Censorship Desensitization Publisher

Capabilities:
1. Generates ready-to-publish social copy for Xiaohongshu (小红书), Bilibili, and Zhihu.
2. Built-in industrial-grade anti-censorship desensitization dictionary (避开作弊/修改器/外挂等限流词).
3. Generates high-CTR headlines, scenario bullet points, and trending topic tags.
4. Previews generated copy or saves directly to social_distribution/ ready for release.
"""

import os
import sys
import json
import argparse
import datetime
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
OUTPUT_DIR = os.path.join(BASE_DIR, 'social_distribution')

# Anti-Censorship Word Replacement Map
ANTI_BAN_DICT = {
    "作弊": "官方指令",
    "作弊码": "控制台代码",
    "修改器": "单机性能优化辅助",
    "外挂": "前置增强插件",
    "破解": "免翻纯净版",
    "锁血": "状态保护",
    "无限金币": "资产极速调校",
    "秒杀": "高能一击参数"
}

def desensitize(text):
    """Replaces sensitive words with compliant gaming terms."""
    result = text
    for bad, good in ANTI_BAN_DICT.items():
        result = result.replace(bad, good)
    return result


def generate_copy_for_game(game, platform="all"):
    title = (game.get('titles') and game.get('titles', {}).get('zh-CN')) or game.get('title')
    rank = game.get('rank', 99)
    shortcut = game.get('consoleShortcut', '~ 键呼出')
    status = game.get('compatibilityStatus', 'green')
    status_text = "🟢 补丁完美兼容" if status == 'green' else ("🟡 需更新前置" if status == 'yellow' else "🔴 坏档预警")
    verified = game.get('verifiedPatch', '最新官方版本')

    # Helper to extract name and code safely
    def format_cmd(c):
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
🔥 标题：终于找到了！《{title}》官方开发者指令与避坑全指南（建议收藏）

👋 宝子们！单机打到中后期卡关或者想爽玩二周目？
老L整理了《{title}》目前最全的【官方原生指令】与【避坑指南】！
绝无任何流氓假代码，对齐最新官方补丁（{verified}）实测可用！

✨ 【必用场景化指令】
{cmds_formatted}

🎮 【怎么在游戏里开启？】
进入游戏后，按下【{shortcut}】呼出输入框，直接粘贴回车即可生效！

🛡️ 【Steam 避坑雷达状态】
当前状态：{status_text}
单机玩家放心食用，零封号风险！进游戏前进群或主站可拿完整全套 100 款神作合集！

🏷️ 标签：
#{title} #{title}攻略 #Steam单机游戏 #单机游戏推荐 #单机游戏避坑 #Steam好游戏 #游戏日常
"""

    # 2. Bilibili (B站动态) Format
    bilibili = f"""📺 【B站专栏与动态文案 · 《{title}》】
━━━━━━━━━━━━━━━━━━━━━━━━
【老L单机智库】全球 100 款单机神作 · 第 {rank} 期：《{title}》

很多老哥私信问更新后旧 Mod 崩溃、控制台代码打不开的问题，今天把实机校验后的纯净代码与避坑指南整理出来了：

📌 当前 Steam 对账状态：{status_text} (认证补丁: {verified})
📌 控制台唤出方式：{shortcut}
📌 核心代码预览：
{cmds_formatted}

纯净无广，无需翻墙，拒绝流氓捆绑下载器。
完整 100 款单机大作数据库与 Steam 补丁实时避坑雷达请直接戳独立站查阅！
"""

    # Apply desensitization filter
    clean_redbook = desensitize(redbook)
    clean_bilibili = desensitize(bilibili)

    return {
        "redbook": clean_redbook,
        "bilibili": clean_bilibili
    }


def main():
    parser = argparse.ArgumentParser(description="L-MOD AI Social Copy Publisher")
    parser.add_argument('--game', type=str, default="cyberpunk-2077", help="游戏 ID (默认 cyberpunk-2077)")
    parser.add_argument('--save', action='store_true', help="将文案保存到 social_distribution/")
    args = parser.parse_args()

    with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)

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
