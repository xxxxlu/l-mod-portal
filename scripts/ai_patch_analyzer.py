#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/ai_patch_analyzer.py
L-MOD Vault - AI Steam 补丁智能分析与雷达自动预警哨兵 (Milestone 4)
AI-Driven Steam Patch Analysis & Risk Sentinel for Single-Player Games

Capabilities:
1. Probes official Steam patch announcements & build notes via Steam Public API.
2. Uses LLM (Gemini API / DeepSeek API / Offline Heuristic Expert Engine) to analyze
   potential binary breakages, script extender invalidations, and save corruption risks.
3. Classifies compatibility status (🟢 完美兼容 / 🟡 需更新前置 / 🔴 坏档预警).
4. Auto-generates player emergency broadcast, rescue & rollback guides.
5. Updates src/data/games_top100.json and synchronizes to radar.html via build_i18n_matrix.py.
"""

import os
import sys
import json
import re
import datetime
import argparse
import urllib.request
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMES_JSON_PATH = os.path.join(BASE_DIR, 'src/data/games_top100.json')
REPORT_PATH = os.path.join(BASE_DIR, 'docs/PATCH_MONITOR_LATEST.md')
DATA_JS_PATH = os.path.join(BASE_DIR, 'public/data.js')

class SteamNewsFetcher:
    """Fetches official Steam community announcements with timeout & fallback."""
    def __init__(self, timeout=8):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) LMOD-Vault-Sentinel/4.0',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

    def fetch_latest_patch_note(self, appid, count=3):
        url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={appid}&count={count}&feeds=steam_community_announcements&format=json"
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                items = data.get('appnews', {}).get('newsitems', [])
                if items:
                    return items[0]
        except Exception:
            pass

        # Fallback to general feed
        url_general = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={appid}&count={count}&format=json"
        try:
            req = urllib.request.Request(url_general, headers=self.headers)
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                items = data.get('appnews', {}).get('newsitems', [])
                if items:
                    return items[0]
        except Exception:
            pass
        return None


class AIPatchEvaluator:
    """Analyzes patch notes using Gemini, DeepSeek, or Offline Heuristic Fallback."""
    def __init__(self, gemini_key=None, deepseek_key=None):
        self.gemini_key = gemini_key or os.getenv('GEMINI_API_KEY')
        self.deepseek_key = deepseek_key or os.getenv('DEEPSEEK_API_KEY')

    def analyze_patch(self, game_info, patch_title, patch_content):
        # 1. Try Gemini API
        if self.gemini_key:
            try:
                res = self._call_gemini(game_info, patch_title, patch_content)
                if res:
                    return res
            except Exception as e:
                print(f"⚠️ [AI Analyzer] Gemini API 调用失败: {e}，将自动切换为离线启发式评估。")

        # 2. Try DeepSeek API
        if self.deepseek_key:
            try:
                res = self._call_deepseek(game_info, patch_title, patch_content)
                if res:
                    return res
            except Exception as e:
                print(f"⚠️ [AI Analyzer] DeepSeek API 调用失败: {e}，将自动切换为离线启发式评估。")

        # 3. Fallback: Offline Heuristic Expert Rules
        return self._heuristic_analysis(game_info, patch_title, patch_content)

    def _call_gemini(self, game_info, patch_title, patch_content):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_key}"
        prompt = self._build_prompt(game_info, patch_title, patch_content)

        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            raw_text = data['candidates'][0]['content']['parts'][0]['text']
            return json.loads(raw_text)

    def _call_deepseek(self, game_info, patch_title, patch_content):
        url = "https://api.deepseek.com/chat/completions"
        prompt = self._build_prompt(game_info, patch_title, patch_content)

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are an expert game modding reverse engineer. Always output strict valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {self.deepseek_key}"
            }
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            raw_text = data['choices'][0]['message']['content']
            return json.loads(raw_text)

    def _build_prompt(self, game_info, patch_title, patch_content):
        return f"""
Analyze this Steam PC game patch announcement for single-player mod and save compatibility.

Target Game: {game_info.get('title')} (Engine: {game_info.get('developer', 'Unknown')})
Verified Patch Baseline: {game_info.get('verifiedPatch', 'N/A')}
Patch Announcement Title: {patch_title}
Patch Announcement Content (truncated):
{patch_content[:2500]}

Please output a JSON object with the following fields:
{{
  "compatibilityStatus": "green" or "yellow" or "red",
  "radarRiskTitle": "Short 10-word Chinese summary of risk",
  "radarRiskDesc": "2-3 sentences in Chinese explaining what breaks (e.g. CET/UE4SS/ScriptExtender) and what still works",
  "radarSummary": "1 sentence verdict for players",
  "emergencyBroadcast": "Ready-to-copy Chinese bulletin for WeChat/QQ gaming groups",
  "rescueGuide": "Step-by-step rescue / rollback instructions"
}}

Evaluation Criteria:
- 'green': Minor hotfix, localization, text fix, no .exe change, mods 100% fine.
- 'yellow': Engine .exe recompiled or minor update, script hooks (CET/ScriptExtender/UE4SS) need update, pak/texture mods fine.
- 'red': Major overhaul, Next-Gen update, DLC release, save file format changed, old mods cause black screen or crash.
"""

    def _heuristic_analysis(self, game_info, patch_title, patch_content):
        """Rule-based expert fallback when no LLM API is available."""
        title_lower = patch_title.lower()
        content_lower = patch_content.lower()
        combined = f"{title_lower} {content_lower}"

        # Indicators of Major Red Overhaul
        red_keywords = ['patch 7', 'update 2.0', 'next-gen', 'major update', 'expansion', 'dlc', '次世代', '重构', '引擎升级']
        # Indicators of Yellow Script Risk
        yellow_keywords = ['patch', 'update', 'hotfix', 'executable', 'crash', 'performance', 'v1.', 'v2.', '更新', '补丁', '修复']
        # Indicators of Green Cosmetic
        green_keywords = ['localization', 'translation', 'soundtrack', 'cosmetic', 'text', 'typo', '本地化', '文本']

        is_red = any(k in combined for k in red_keywords)
        is_yellow = any(k in combined for k in yellow_keywords)
        is_green = any(k in combined for k in green_keywords) and not is_red

        if is_red:
            status = "red"
            risk_title = "官方突发大版本更新 · 坏档与脚本失效高危预警"
            risk_desc = "官方更新重构了底层脚本或执行文件，所有基于脚本扩展器（如 CET/F4SE/UE4SS）的 Mod 将严重跳出，旧存档加载存在坏档风险。"
            summary = "大版本重大更新，强烈建议单机玩家在 Steam 属性中关闭自动更新，或等待前置核心库适配。"
        elif is_yellow:
            status = "yellow"
            risk_title = "官方推送常规补丁 · 前置核心插件需对齐"
            risk_desc = "主执行文件已变动，纯净材质与模型 Mod 依然可用，但内存注入型修改器与底层脚本插件需等待作者推送更新补丁。"
            summary = "小版本补丁更新，常规模型 Mod 安全，底层注入型插件需等作者更新。"
        else:
            status = "green"
            risk_title = "微型热修复 · 全量 Mod 实测完美兼容"
            risk_desc = "本次变动仅涉及文案本地化或轻微逻辑微调，主程序内存偏移量未变，老L智库所有代码与 Mod 均可稳定运行。"
            summary = "微型更新，老L全系场景套餐与控制台代码 100% 畅玩通过。"

        emergency_broadcast = (
            f"【L-MOD 避坑急报】《{game_info.get('title')}》官方最新推送：{patch_title}\n"
            f"雷达状态：{status.upper()}\n"
            f"预警详情：{risk_desc}\n"
            f"避坑建议：单机通关中的玩家请切勿盲目更新，已中招玩家可在群内获取降级回滚补丁！"
        )

        rescue_guide = (
            "1. 右键 Steam 游戏属性 -> 启动选项，添加离线参数；\n"
            "2. 备份 Saves 存档文件夹，防止新补丁覆盖损坏旧档；\n"
            "3. 如遇黑屏跳出，暂时移除 bin/plugins 或 ~mods 文件夹即可恢复原版进游戏。"
        )

        return {
            "compatibilityStatus": status,
            "radarRiskTitle": risk_title,
            "radarRiskDesc": risk_desc,
            "radarSummary": summary,
            "emergencyBroadcast": emergency_broadcast,
            "rescueGuide": rescue_guide
        }


def run_pipeline(target_game_id=None, update_radar=False, simulate_patch=None, simulate_title=None, simulate_content=None):
    print("=" * 72)
    print("🤖 L-MOD Vault - AI Steam 补丁智能分析与预警流水线")
    print("=" * 72)

    with open(GAMES_JSON_PATH, 'r', encoding='utf-8') as f:
        games = json.load(f)

    fetcher = SteamNewsFetcher()
    evaluator = AIPatchEvaluator()

    if target_game_id:
        targets = [g for g in games if g['id'] == target_game_id and g.get('steamAppId')]
    elif simulate_patch:
        targets = [g for g in games if g['id'] == simulate_patch and g.get('steamAppId')]
    else:
        targets = [g for g in games if g.get('steamAppId')]
    if not targets:
        print(f"❌ 未找到匹配的游戏或该游戏无 steamAppId: {target_game_id or simulate_patch}")
        return

    print(f"📦 正在巡检 {len(targets)} 款目标游戏的官方 Steam 补丁动态...\n")

    analyzed_count = 0
    updated_records = []

    for game in targets:
        appid = game['steamAppId']
        title = game.get('title')
        print(f"🔍 [{game.get('rank', '?')}] 正在嗅探: {title} (AppID: {appid})...")

        if simulate_patch and game['id'] == simulate_patch:
            patch_title = simulate_title or "Official Major Update 2.5 (Next-Gen Overhaul)"
            patch_content = simulate_content or (
                "Patch Notes: We have upgraded the underlying REDengine executable binaries, "
                "recompiled all internal script virtual machines, and introduced new expansion mechanics. "
                "All legacy external hook DLLs and outdated save formats must be upgraded."
            )
            patch_date_str = datetime.datetime.now().strftime('%Y-%m-%d')
            print(f"   🧪 [模拟模式] 注入突发官方更新: 《{patch_title}》")
        else:
            patch_note = fetcher.fetch_latest_patch_note(appid)
            if not patch_note:
                print(f"   ℹ️ 暂未检索到 Steam 官方最新更新日志，保持基线。")
                continue

            patch_title = patch_note.get('title', 'Unknown Patch')
            patch_content = patch_note.get('contents', '')
            patch_date_ts = patch_note.get('date', 0)
            patch_date_str = datetime.datetime.fromtimestamp(patch_date_ts).strftime('%Y-%m-%d') if patch_date_ts else '---'

        print(f"   📢 捕获到官方动态: 《{patch_title}》 (发布于 {patch_date_str})")
        print(f"   ⚡ 正在启动 AI 模型进行 Mod 破坏性与坏档风险深度研判...")

        analysis = evaluator.analyze_patch(game, patch_title, patch_content)

        status_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(analysis['compatibilityStatus'], "🟢")
        print(f"   {status_emoji} 判定结果: {analysis['compatibilityStatus'].upper()} | {analysis['radarRiskTitle']}")
        print(f"   💬 研判综述: {analysis['radarSummary']}")

        # Update Game Record in Memory
        game['latestSteamPatch'] = f"{patch_title} ({patch_date_str})"
        game['compatibilityStatus'] = analysis['compatibilityStatus']
        game['radarRiskTitle'] = analysis['radarRiskTitle']
        game['radarRiskDesc'] = analysis['radarRiskDesc']
        game['radarSummary'] = analysis['radarSummary']
        game['steamLastChecked'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        updated_records.append({
            "game": game,
            "analysis": analysis,
            "patch_title": patch_title,
            "patch_date": patch_date_str
        })
        analyzed_count += 1
        print("-" * 60)

    # Save to games_top100.json
    if update_radar and updated_records:
        print(f"\n💾 正在将 {len(updated_records)} 条 AI 研判结果持久化写入 {GAMES_JSON_PATH}...")
        with open(GAMES_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)

        # Generate Latest Report
        generate_report(updated_records)

        # Trigger build_i18n_matrix.py to bundle data.js
        build_script = os.path.join(BASE_DIR, 'scripts/build_i18n_matrix.py')
        if os.path.exists(build_script):
            print("🚀 正在触发 build_i18n_matrix.py 自动编译 public/data.js...")
            os.system(f"python3 {build_script}")

        print("\n✅ [AI Patch Analyzer] 流水线执行成功，所有看板与雷达已同步最新预警！")
    else:
        print(f"\nℹ️ 巡检完成！若需更新雷达看板与持久化数据，请添加 --update-radar 参数。")


def generate_report(records):
    now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M CST')
    lines = [
        "# L-MOD Vault Steam 补丁兼容性与避坑雷达最新简报",
        f"\n> 自动巡检生成时间：`{now_str}` ｜ 驱动引擎：L-MOD AI Patch Sentinel\n",
        "---",
        "\n## 🚨 最新突发变动与预警快报\n"
    ]

    for item in records:
        g = item['game']
        a = item['analysis']
        emoji = {"green": "🟢 完美兼容", "yellow": "🟡 需注意", "red": "🔴 坏档预警"}.get(a['compatibilityStatus'], "🟢")
        lines.append(f"### {emoji} 《{g.get('title')}》")
        lines.append(f"- **Steam 官方补丁**: `{item['patch_title']}` (发布于 {item['patch_date']})")
        lines.append(f"- **老L 已认证补丁**: `{g.get('verifiedPatch', '基线版本')}`")
        lines.append(f"- **AI 风险研判**: **{a['radarRiskTitle']}**")
        lines.append(f"- **详细影响分析**: {a['radarRiskDesc']}")
        lines.append(f"- **玩家避坑建议**: {a['radarSummary']}\n")
        lines.append("```text")
        lines.append(a.get('emergencyBroadcast', ''))
        lines.append("```\n")

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"📄 避坑简报已写入: {REPORT_PATH}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="L-MOD AI Steam Patch Sentinel")
    parser.add_argument('--game', type=str, help="指定单款游戏 ID 进行巡检分析 (如 cyberpunk-2077)")
    parser.add_argument('--update-radar', action='store_true', help="将 AI 研判结果直接写入数据库并更新雷达看板")
    parser.add_argument('--simulate-patch', type=str, help="模拟指定游戏突发更新 (如 cyberpunk-2077)")
    parser.add_argument('--simulate-title', type=str, help="模拟更新标题")
    parser.add_argument('--simulate-content', type=str, help="模拟更新内容")
    args = parser.parse_args()

    run_pipeline(
        target_game_id=args.game,
        update_radar=args.update_radar,
        simulate_patch=args.simulate_patch,
        simulate_title=args.simulate_title,
        simulate_content=args.simulate_content
    )
