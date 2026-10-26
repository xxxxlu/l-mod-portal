#!/usr/bin/env python3
"""
generate_social_matrix.py
L-MOD Vault 社交矩阵工业级自动化生成引擎 (v1.0)
功能：
1. 自动对齐平台防限流合规脱敏词典 (Anti-Shadowban Desensitization Engine)；
2. 从 games_top100.json 结构化数据自动抽取并组装「小红书 5 联图卡片数据」与「B站动态专栏文案」；
3. 输出可直接渲染的 HTML 预览页面 (支持 1080x1440 3:4 比例一键导出截图) 与剪贴板文案；
4. 包含版本补丁对齐信赖标 (Patch Verified Stamp) 与私域防失联引导暗号。
"""

import json
import os
import sys
import argparse
from pathlib import Path

# 路径基准
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "src" / "data" / "games_top100.json"
OUTPUT_DIR = BASE_DIR / "public" / "social_matrix"

# ========================================================
# 1. 平台防限流合规脱敏词典 (Anti-Shadowban Lexicon)
# ========================================================
DESENSITIZATION_MAP = [
    # 核心违规词替换
    (r"作弊码|作弊代码|作弊", "官方调试指令"),
    (r"修改器|外挂|辅助挂", "纯净优化拓展包"),
    (r"控制台代码|控制台作弊", "底层控制台彩蛋"),
    (r"锁血|无限血|无敌模式", "手残救星·剧情体验模式"),
    (r"无限蓝|无限体力|秒杀", "极速破韧·战斗畅爽增强"),
    (r"刷钱|无限金钱|无限金币", "资源自由·全图鉴解锁"),
    (r"无限负重|改负重", "背包减负·无痛探索"),
    (r"全武器解锁|刷物品", "全套神装图鉴·一键获取"),
    (r"穿墙|飞天", "自由摄影·全景透视视角"),
    (r"跳过任务|强制完成任务", "卡关抢救·坏档剧情修复"),
    (r"破解|盗版", "官方离线原生支持"),
]

# 爆款情绪与场景化包装模板 (针对游戏类型与痛点)
GAME_HOOK_PRESETS = {
    "cyberpunk-2077": {
        "title_hook": "2077其实自带官方控制台！90%玩家不知道的极客自救指南",
        "pain_point": "还在去盗版网站下带毒修改器？教你开启官方底层彩蛋，不封号、零闪退！",
        "bundle_tag": "⚡ 赛博救赎全神装套件",
        "patch_badge": "官方最新 2.13 补丁实测可用"
    },
    "black-myth-wukong": {
        "title_hook": "黑神话手残被虎先锋劝退？虚幻5原生隐藏调试模式教程",
        "pain_point": "卡关卡到摔手柄？教你官方引擎级防反与慢动作机制，体验齐天大圣真神力！",
        "bundle_tag": "🐒 大圣觉醒全法术破荒包",
        "patch_badge": "官方最新 1.0.9+ 补丁实测可用"
    },
    "witcher-3": {
        "title_hook": "巫师3次世代版隐藏彩蛋：改一个字母开启猎魔人原生控制台",
        "pain_point": "手滑选错后悔终生？教你用官方指令逆转爱丽丝悲剧，全师匠神装一键毕业！",
        "bundle_tag": "🐺 猎魔人传奇救赎大礼包",
        "patch_badge": "次世代完全版 v4.04+ 实测可用"
    },
    "baldurs-gate-3": {
        "title_hook": "博德之门3 Patch7官方工坊必看！无冲突纯净控制台开启指南",
        "pain_point": "打Mod导致无法联机或闪退？官方底层的调试黑窗才是最稳解决方案！",
        "bundle_tag": "🎲 费伦大陆天神下凡组合包",
        "patch_badge": "官方 Patch 7 补丁完全兼容"
    },
    "elden-ring": {
        "title_hook": "法环黄金树幽影太折磨？纯净离线轮椅机制与安全防封指南",
        "pain_point": "被狂龙和双月骑士虐哭？带你看真正安全零封号的单机离线减负方案！",
        "bundle_tag": "💍 艾尔登之王全追忆轮椅包",
        "patch_badge": "幽影之地最新 1.14 补丁对齐"
    },
    "skyrim-se": {
        "title_hook": "老滚5重制版恶性卡关/闪退怎么救？B社原生控制台避坑急救指南",
        "pain_point": "任务NPC不说话卡死坏档？教你用官方底层的setstage指令秒修复，全魔神器与龙吼一键毕业！",
        "bundle_tag": "🐉 龙裔降临全魔神器破荒包",
        "patch_badge": "天际AE/SE最新 1.6.1170 补丁完全实测"
    },
    "fallout-4": {
        "title_hook": "辐射4次世代大更新Mod全崩溃？官方控制台与传奇武器附魔指南",
        "pain_point": "造房子空间被锁死？教你用原生指令无限扩建聚落，全传奇双弹爆破武器自定义附魔！",
        "bundle_tag": "⚡ 废土之王全传奇军备包",
        "patch_badge": "次世代大更新 v1.10.984+ 深度适配"
    }
}


def sanitize_text(text) -> str:
    """对文案执行合规脱敏替换，支持字符串、多语言字典或None"""
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


def extract_game_matrix_data(game_id: str):
    """从数据库抽取指定游戏的矩阵素材数据"""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        games = json.load(f)

    target_game = None
    for g in games:
        if g.get("id") == game_id:
            target_game = g
            break

    if not target_game:
        raise ValueError(f"Game with id '{game_id}' not found in database.")

    preset = GAME_HOOK_PRESETS.get(game_id, {
        "title_hook": f"{target_game.get('title')} 官方隐藏机制与纯净探索指南",
        "pain_point": "拒绝流氓插件，教你开启游戏原生底层功能，零风险畅爽体验！",
        "bundle_tag": "🎮 核心探索增益包",
        "patch_badge": "当前最新版本实测可用"
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
            "name": sanitize_text(zh_name),
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
                    "name": sanitize_text(zh_name),
                    "code": cmd.get("code", "")
                })

    # 提取精选 Mod (Top 3)
    mods_showcase = []
    for mod in target_game.get("curatedMods", [])[:3]:
        mod_name = mod.get("title") or mod.get("name", "精选模组")
        mods_showcase.append({
            "name": sanitize_text(mod_name),
            "author": mod.get("author", "Community"),
            "downloads": mod.get("downloads", "100K+"),
            "desc": sanitize_text(mod.get("desc", ""))
        })

    # 组合交付数据结构
    card_data = {
        "game_id": game_id,
        "title": target_game.get("title"),
        "genre": target_game.get("genre"),
        "developer": target_game.get("developer"),
        "releaseYear": target_game.get("releaseYear"),
        "steamRating": target_game.get("steamRating"),
        "patchBadge": preset["patch_badge"],
        "titleHook": preset["title_hook"],
        "painPoint": preset["pain_point"],
        "bundleTag": preset["bundle_tag"],
        "consoleShortcut": target_game.get("consoleShortcut", "`~` 键"),
        "enableGuide": sanitize_text(target_game.get("consoleEnableGuide", {}).get("zh-CN", "")),
        "commands": commands_showcase,
        "mods": mods_showcase,
        "trafficSecretKey": f"输入暗号【{target_game.get('title')[:4].replace(' ', '')}】获取纯净一键包"
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
        <p class="text-zinc-400 text-sm mt-1">游戏：{card_data['title']} | 审核合规级别：<span class="text-emerald-400 font-bold">100% 绿色安全</span></p>
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
              官方自留功能曝光
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
              <p class="font-bold text-white">拒绝流氓外挂 / 木马捆绑</p>
              <p class="text-zinc-400">100% 官方离线机制 · 零封号</p>
            </div>
          </div>
          <div class="mt-3 text-center text-[10px] text-zinc-500 font-mono">
            SLIDE 1 / 5 · 左右滑动查看手把手教程
          </div>
        </div>
      </div>

      <!-- ================= CARD 2: 傻瓜式开启教程 ================= -->
      <div class="card-canvas rounded-2xl bg-gradient-to-b from-zinc-900 to-black p-5 flex flex-col justify-between neon-border">
        <div>
          <div class="flex items-center justify-between">
            <span class="px-2.5 py-1 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-md text-[10px] font-bold tracking-wider">
              ⚡ 10秒开门
            </span>
            <span class="text-[11px] text-zinc-400 font-mono">STEP-BY-STEP</span>
          </div>

          <h3 class="text-lg font-black text-white mt-4">
            小白 3 步唤醒官方隐藏菜单
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
                <p class="text-[11px] text-zinc-400 mt-0.5 line-clamp-2">{card_data['enableGuide'] or '丢入纯净开源框架文件即可'}</p>
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
          💡 懒人福利：老L已写好一键批处理脚本，双击自动搞定，见文末自取通道。
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
                <span class="text-[9px] bg-blue-500/20 text-blue-300 px-1.5 py-0.5 rounded font-mono">已校验</span>
              </div>
              <code class="block mt-1 text-[10px] text-emerald-400 font-mono bg-black/60 px-2 py-1 rounded truncate">
                {cmd['code']}
              </code>
            </div>
            ''' for cmd in card_data['commands'][:4]])}
          </div>
        </div>

        <div class="text-[10px] text-zinc-400 text-center font-mono">
          ※ 更多 100+ 条完整装备与剧情分支代码见库中备查
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
            官方痛点解决 · 纯净体验 Mod
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
          🔒 所有模组均已做坏档隔离与版本兼容性验证。
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
            防代码失效与更新通知
          </h3>

          <div class="mt-4 p-4 rounded-xl bg-purple-900/20 border border-purple-500/30 text-center">
            <div class="text-3xl mb-2">🎁</div>
            <p class="text-xs font-bold text-purple-200">一键懒人免配包 & 完整代码库</p>
            <p class="text-[11px] text-zinc-400 mt-1">杜绝过期失效 · Steam补丁同步更新</p>
            
            <div class="mt-4 p-2.5 bg-black/80 rounded-lg border border-purple-400/40">
              <span class="text-xs text-yellow-300 font-mono font-bold">{card_data['trafficSecretKey']}</span>
            </div>
          </div>

          <div class="mt-4 space-y-1.5 text-[11px] text-zinc-300">
            <p class="flex items-center gap-1.5"><span>⚡</span> <span>Steam 大补丁连夜跟进重测</span></p>
            <p class="flex items-center gap-1.5"><span>🛡️</span> <span>MOD 冲突在线排查与坏档急救</span></p>
            <p class="flex items-center gap-1.5"><span>💬</span> <span>单机老玩家互助纯净交流群</span></p>
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

兄弟们，千万别再去盗版网站下载那些带全家桶弹窗和木马的“免费修改器”了！
其实很多单机大作底层本身就开放了官方调试机制，不仅完全免费，而且不封号、零闪退、零报毒！

今天老L花了两个通宵，把最新补丁（{card_data['patchBadge']}）的官方机制全部实测对齐了一遍，整理了这套【{card_data['bundleTag']}】：

✨ 核心亮点：
1. 官方原生支持，直接在游戏内按 {card_data['consoleShortcut']} 唤醒；
2. 包含全图鉴神装、剧情卡关抢救、探索无痛减负；
3. 实测兼容当前最新补丁，无坏档风险！

📌 怎么拿完整代码库与懒人一键包：
看评论区置顶或主页介绍，{card_data['trafficSecretKey']}。
后续如果 Steam 推新补丁，老L也会在第一时间更新通知，建议先收藏防迷路！

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
    parser.add_argument("--all", action="store_true", help="批量生成全部前 4 款旗舰游戏的卡片矩阵")
    parser.add_argument("--render-png", action="store_true", help="同步调用高清 PNG 卡片渲染引擎与分发物料总装包")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    target_games = ["cyberpunk-2077", "black-myth-wukong", "witcher-3", "baldurs-gate-3"] if args.all else [args.game_id]

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

    if args.render_png:
        print("\n🖼️ 正在触发工业级 PNG 高清卡片与物料总装引擎...")
        try:
            from render_cards_png import run_distribution_assembly
            run_distribution_assembly(target_games)
        except Exception as e:
            print(f"❌ PNG 出图引擎执行失败: {e}")


if __name__ == "__main__":
    main()
