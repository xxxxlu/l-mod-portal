#!/usr/bin/env python3
"""
scripts/optimize_themes.py
Refines and unifies the Light Mode and Dark Mode design systems for L-MOD Vault:
1. Fixes hardcoded body backgrounds (bg-[#0b0c0f]) and sets up dual-mode CSS variables.
2. Calibrates Pokemon Trading Card (PTCG) Holographic Foil shader for both dark (color-dodge) and light (color-burn) modes.
3. Fixes hardcoded text colors (text-white) in card headers, titles, and ability trays to responsive zinc-900 / white.
4. Harmonizes light and dark styles across banners, search bars, list modes, and modals.
5. Injects full dark/light theme switcher and sync logic into radar.html.
"""

import re
import os

INDEX_PATH = "public/index.html"
RADAR_PATH = "public/radar.html"

def optimize_index():
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update <style> root variables and body/card styles
    old_style_marker = "<style>"
    new_style_block = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
      --bg-base: #f8fafc;
      --bg-surface: #ffffff;
      --card-cardstock: #ffffff;
      --card-border: rgba(0, 0, 0, 0.08);
      --card-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
      --accent: #9333ea;
      --accent-dim: rgba(147, 51, 234, 0.08);
      --text-main: #0f172a;
      --text-muted: #64748b;
      --card-foil-border: linear-gradient(135deg, rgba(168, 85, 247, 0.28) 0%, rgba(59, 130, 246, 0.2) 50%, rgba(236, 72, 153, 0.2) 100%);
      --ability-bg: #f8fafc;
      --ability-border: rgba(0, 0, 0, 0.06);
      --ticker-bg: #f1f5f9;
      --ticker-border: rgba(0, 0, 0, 0.06);
    }

    html.dark {
      --bg-base: #090a0f;
      --bg-surface: #12141a;
      --card-cardstock: #12141a;
      --card-border: rgba(255, 255, 255, 0.12);
      --card-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(0, 0, 0, 0.6);
      --accent: #A855F7;
      --accent-dim: rgba(168, 85, 247, 0.14);
      --text-main: #f1f5f9;
      --text-muted: #8b8f9e;
      --card-foil-border: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(168, 85, 247, 0.25) 50%, rgba(255, 255, 255, 0.08) 100%);
      --ability-bg: rgba(10, 11, 16, 0.85);
      --ability-border: rgba(255, 255, 255, 0.08);
      --ticker-bg: #111317;
      --ticker-border: rgba(255, 255, 255, 0.1);
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      background-color: var(--bg-base);
      color: var(--text-main);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
      transition: background-color 0.25s ease, color 0.25s ease;
    }

    html.dark body {
      background-image: radial-gradient(circle at 50% 12%, rgba(168, 85, 247, 0.08) 0%, transparent 60%);
    }

    html:not(.dark) body {
      background-image: radial-gradient(circle at 50% 12%, rgba(168, 85, 247, 0.04) 0%, transparent 60%);
    }

    .font-display {
      font-family: 'Bebas Neue', sans-serif;
      letter-spacing: 0.04em;
    }

    .font-mono-tech {
      font-family: 'JetBrains Mono', monospace;
    }

    /* ======================================================== */
    /* 宝可梦全息闪卡 (POKÉMON HOLO FOIL) 核心物理与光学着色引擎 */
    /* ======================================================== */

    .pokemon-card-container {
      perspective: 900px;
      transform-style: preserve-3d;
      will-change: transform;
    }

    .pokemon-card {
      position: relative;
      background: var(--card-cardstock);
      border-radius: 20px;
      overflow: hidden;
      transform-style: preserve-3d;
      transform-origin: 50% 50%; /* 核心：严格以中心为重心旋转，绝无突兀位移 */
      border: 1.5px solid var(--card-border);
      box-shadow: var(--card-shadow);
      transition: transform 0.1s ease-out, box-shadow 0.25s ease, background-color 0.25s ease, border-color 0.25s ease;
      will-change: transform, box-shadow;
    }

    /* === 宝可梦闪卡灵魂 1：彩虹全息镭射滤镜层 (Rainbow Holo Foil) === */
    .holo-foil-layer {
      position: absolute;
      inset: 0;
      border-radius: inherit;
      pointer-events: none;
      z-index: 20;
      opacity: 0;
      transition: opacity 0.35s ease;
      background-size: 200% 200%, 100% 100%;
      background-position: var(--foil-pos-x, 50%) var(--foil-pos-y, 50%);
    }

    /* 暗色模式：采用 Color-Dodge 激发绚烂霓虹全息反光 */
    html.dark .holo-foil-layer {
      mix-blend-mode: color-dodge;
      background-image: 
        linear-gradient(
          115deg,
          transparent 0%,
          rgba(255, 110, 199, 0.35) 15%,
          rgba(168, 85, 247, 0.45) 30%,
          rgba(0, 240, 255, 0.45) 50%,
          rgba(255, 225, 75, 0.45) 70%,
          rgba(255, 110, 199, 0.35) 85%,
          transparent 100%
        ),
        repeating-linear-gradient(
          0deg,
          rgba(255, 255, 255, 0.08) 0px,
          rgba(255, 255, 255, 0.08) 2px,
          transparent 2px,
          transparent 4px
        );
    }

    /* 亮色模式：采用 Color-Burn / Soft Iridescent 产生珠光纸面彩虹漫射 */
    html:not(.dark) .holo-foil-layer {
      mix-blend-mode: color-burn;
      background-image: 
        linear-gradient(
          115deg,
          transparent 0%,
          rgba(236, 72, 153, 0.4) 15%,
          rgba(147, 51, 234, 0.45) 30%,
          rgba(6, 182, 212, 0.45) 50%,
          rgba(234, 179, 8, 0.45) 70%,
          rgba(236, 72, 153, 0.4) 85%,
          transparent 100%
        ),
        repeating-linear-gradient(
          0deg,
          rgba(0, 0, 0, 0.03) 0px,
          rgba(0, 0, 0, 0.03) 2px,
          transparent 2px,
          transparent 4px
        );
    }

    /* === 宝可梦闪卡灵魂 2：卡套高光漫射层 (Specular Glare) === */
    .holo-glare-layer {
      position: absolute;
      inset: 0;
      border-radius: inherit;
      pointer-events: none;
      z-index: 25;
      opacity: 0;
      transition: opacity 0.25s ease;
    }

    html.dark .holo-glare-layer {
      mix-blend-mode: overlay;
      background: radial-gradient(
        400px circle at var(--pointer-x, 50%) var(--pointer-y, 50%),
        rgba(255, 255, 255, 0.55) 0%,
        rgba(255, 255, 255, 0.15) 30%,
        transparent 65%
      );
    }

    html:not(.dark) .holo-glare-layer {
      mix-blend-mode: soft-light;
      background: radial-gradient(
        400px circle at var(--pointer-x, 50%) var(--pointer-y, 50%),
        rgba(255, 255, 255, 0.95) 0%,
        rgba(255, 255, 255, 0.35) 35%,
        transparent 70%
      );
    }

    /* 悬停时激活闪卡彩虹光泽 */
    .pokemon-card:hover .holo-foil-layer {
      opacity: 0.85;
    }
    .pokemon-card:hover .holo-glare-layer {
      opacity: 0.75;
    }

    /* 金属箔框 */
    .card-foil-border {
      position: relative;
      border-radius: 16px;
      background: var(--card-foil-border);
      padding: 1.5px;
    }

    /* 闪卡技能槽/属性框 (PTCG Abilities Box) */
    .ability-tray {
      background: var(--ability-bg);
      border: 1px solid var(--ability-border);
      border-radius: 12px;
    }

    /* 工业十字标记 */
    .cross-marker {
      position: relative;
    }
    .cross-marker::before, .cross-marker::after {
      content: '+';
      position: absolute;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--text-muted);
      pointer-events: none;
      opacity: 0.4;
    }
    .cross-marker::before { top: -8px; left: -8px; }
    .cross-marker::after { bottom: -8px; right: -8px; }

    /* 跑马灯 */
    .ticker-wrap {
      width: 100%;
      overflow: hidden;
      white-space: nowrap;
      background: var(--ticker-bg);
      border-top: 1px solid var(--ticker-border);
      border-bottom: 1px solid var(--ticker-border);
      padding: 7px 0;
    }
    .ticker-move {
      display: inline-block;
      animation: ticker 28s linear infinite;
    }
    @keyframes ticker {
      0% { transform: translate3d(0, 0, 0); }
      100% { transform: translate3d(-50%, 0, 0); }
    }

    /* 动作按钮 */
    .btn-action {
      background: transparent;
      color: var(--text-main);
      border: 1px solid var(--card-border);
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .pokemon-card:hover .btn-action, .btn-action:hover {
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      box-shadow: 0 0 16px var(--accent);
    }

    /* Custom Cursor */
    @media (pointer: fine) {
      #cursor-dot {
        position: fixed;
        top: 0;
        left: 0;
        width: 6px;
        height: 6px;
        background: var(--accent);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        transition: transform 0.04s ease-out;
      }
      #cursor-ring {
        position: fixed;
        top: 0;
        left: 0;
        width: 36px;
        height: 36px;
        border: 1.5px solid var(--accent);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9998;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: width 0.2s ease, height 0.2s ease, border-color 0.2s ease;
      }
      #cursor-label {
        font-size: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        color: var(--accent);
        opacity: 0;
        transition: opacity 0.2s ease;
      }
      body.cursor-hover #cursor-ring {
        width: 48px;
        height: 48px;
        border-color: #ec4899;
      }
      body.cursor-hover #cursor-label {
        opacity: 1;
      }
    }
    @media (pointer: coarse) {
      #cursor-dot, #cursor-ring {
        display: none !important;
      }
    }"""

    # Replace the <style> section up to .btn-action block
    pattern = r"<style>.*?(?=/\* Custom Apple & Google hybrid scrollbars \*/)"
    content = re.sub(pattern, new_style_block + "\n\n    ", content, flags=re.DOTALL)

    # 2. Fix body tag classes
    content = content.replace(
        '<body class="bg-[#0b0c0f] text-slate-100 min-h-screen flex flex-col md:flex-row transition-colors duration-300 selection:bg-[#A855F7] selection:text-black">',
        '<body class="bg-[#f8fafc] dark:bg-[#090a0f] text-zinc-900 dark:text-zinc-100 min-h-screen flex flex-col md:flex-row transition-colors duration-300 selection:bg-[#A855F7]/30 selection:text-purple-900 dark:selection:text-purple-200">'
    )

    # 3. Update top Emergency Broadcast Bar in index.html
    old_broadcast = """    <!-- Top Emergency Broadcast Ticker (Synced with Steam Radar) -->
    <div class="bg-gradient-to-r from-red-950/90 via-zinc-900/95 to-amber-950/90 border-b border-white/10 text-xs py-1.5 px-4 overflow-hidden z-40 relative">
      <div class="max-w-7xl mx-auto flex items-center justify-between gap-3 text-[11px]">
        <div class="flex items-center space-x-2 shrink-0 bg-red-500/20 text-red-300 px-2.5 py-0.5 rounded-full border border-red-500/30 font-semibold">
          <span class="relative flex h-1.5 w-1.5">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-red-500"></span>
          </span>
          <span id="broadcast-bar-title">Steam 补丁避坑紧急广播</span>
        </div>
        <div class="flex-1 overflow-hidden h-4">
          <div class="truncate text-zinc-300 font-medium space-x-6">
            <span class="text-red-400 font-bold">🔴【辐射4】</span><a href="radar.html?game=fallout-4" class="hover:underline">次世代大更新破坏近 10 年 Mod 体系，推荐使用 Downgrader 回退 1.10.163</a>
            <span class="text-zinc-600">|</span>
            <span class="text-amber-400 font-bold">🟡【上古卷轴5】</span><a href="radar.html?game=skyrim-se" class="hover:underline">v1.6.1170 前置需更新对齐！认准 SKSE64 2.2.6 与 Engine Fixes</a>
            <span class="text-zinc-600">|</span>
            <span class="text-emerald-400 font-bold">🟢【博德之门3】</span><a href="radar.html?game=baldurs-gate-3" class="hover:underline">Patch 7 官方工坊对齐实测通过！BG3SE v18+ 完全兼容</a>
            <span class="text-zinc-600">|</span>
            <span class="text-emerald-400 font-bold">🟢【艾尔登法环】</span><a href="radar.html?game=elden-ring" class="hover:underline">黄金树幽影 v1.14 离线免封方案已同步！ModEngine2 零封号</a>
          </div>
        </div>
        <a href="radar.html" class="shrink-0 text-purple-400 hover:text-blue-300 font-bold flex items-center gap-1">
          <span id="broadcast-bar-btn">进入避坑雷达看板</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </a>
      </div>
    </div>"""

    new_broadcast = """    <!-- Top Emergency Broadcast Ticker (Synced with Steam Radar) -->
    <div class="bg-gradient-to-r from-red-50/90 via-slate-50/95 to-amber-50/90 dark:from-red-950/90 dark:via-zinc-900/95 dark:to-amber-950/90 border-b border-zinc-200/80 dark:border-white/10 text-xs py-1.5 px-4 overflow-hidden z-40 relative">
      <div class="max-w-7xl mx-auto flex items-center justify-between gap-3 text-[11px]">
        <div class="flex items-center space-x-2 shrink-0 bg-red-500/10 dark:bg-red-500/20 text-red-700 dark:text-red-300 px-2.5 py-0.5 rounded-full border border-red-500/30 font-semibold">
          <span class="relative flex h-1.5 w-1.5">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-1.5 w-1.5 bg-red-500"></span>
          </span>
          <span id="broadcast-bar-title">Steam 补丁避坑紧急广播</span>
        </div>
        <div class="flex-1 overflow-hidden h-4">
          <div class="truncate text-zinc-700 dark:text-zinc-300 font-medium space-x-6">
            <span class="text-red-600 dark:text-red-400 font-bold">🔴【辐射4】</span><a href="radar.html?game=fallout-4" class="hover:underline">次世代大更新破坏近 10 年 Mod 体系，推荐使用 Downgrader 回退 1.10.163</a>
            <span class="text-zinc-300 dark:text-zinc-600">|</span>
            <span class="text-amber-600 dark:text-amber-400 font-bold">🟡【上古卷轴5】</span><a href="radar.html?game=skyrim-se" class="hover:underline">v1.6.1170 前置需更新对齐！认准 SKSE64 2.2.6 与 Engine Fixes</a>
            <span class="text-zinc-300 dark:text-zinc-600">|</span>
            <span class="text-emerald-600 dark:text-emerald-400 font-bold">🟢【博德之门3】</span><a href="radar.html?game=baldurs-gate-3" class="hover:underline">Patch 7 官方工坊对齐实测通过！BG3SE v18+ 完全兼容</a>
            <span class="text-zinc-300 dark:text-zinc-600">|</span>
            <span class="text-emerald-600 dark:text-emerald-400 font-bold">🟢【艾尔登法环】</span><a href="radar.html?game=elden-ring" class="hover:underline">黄金树幽影 v1.14 离线免封方案已同步！ModEngine2 零封号</a>
          </div>
        </div>
        <a href="radar.html" class="shrink-0 text-purple-600 dark:text-purple-400 hover:text-purple-700 dark:hover:text-blue-300 font-bold flex items-center gap-1">
          <span id="broadcast-bar-btn">进入避坑雷达看板</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
        </a>
      </div>
    </div>"""

    content = content.replace(old_broadcast, new_broadcast)

    # 4. Update header styling in index.html (cleaner light mode frosted background)
    content = content.replace(
        '<header class="sticky top-0 z-30 bg-[#f5f6f8]/80 dark:bg-[#0c0d0f]/80 backdrop-blur-2xl px-4 sm:px-8 h-16 flex items-center justify-between border-b border-zinc-200/60 dark:border-white/[0.06] transition-colors">',
        '<header class="sticky top-0 z-30 bg-white/80 dark:bg-[#0c0d0f]/80 backdrop-blur-2xl px-4 sm:px-8 h-16 flex items-center justify-between border-b border-zinc-200/60 dark:border-white/[0.06] transition-colors">'
    )

    # 5. Update Steam Radar live box in index.html
    old_radar_box = """        <!-- ======================================================== -->
        <!-- STEAM RADAR LIVE STATUS BAR & COMPATIBILITY CAPSULE      -->
        <!-- ======================================================== -->
        <div class="mb-6 bg-gradient-to-r from-zinc-900 via-[#12141c] to-zinc-900 rounded-[24px] p-4 sm:p-5 border border-white/10 shadow-lg text-white space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex items-center space-x-2.5">
              <span class="relative flex h-2.5 w-2.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span class="font-extrabold text-sm sm:text-base tracking-tight text-white flex items-center gap-1.5">
                <span>📡 Steam 补丁变动与 Mod 兼容性实时避坑雷达</span>
              </span>
              <span class="bg-[#A855F7]/20 text-purple-400 text-[10px] font-mono px-2 py-0.5 rounded-full border border-[#A855F7]/30 font-bold">24h 智能巡检</span>
            </div>

            <!-- Link to Standalone Radar -->
            <a 
              href="radar.html"
              class="self-start sm:self-auto px-3.5 py-1.5 rounded-full text-xs font-semibold bg-white/10 hover:bg-white/20 text-zinc-200 border border-white/10 transition-all flex items-center gap-1.5 group cursor-pointer"
            >
              <span>进入全屏雷达看板</span>
              <svg class="w-3.5 h-3.5 text-zinc-400 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </a>
          </div>

          <!-- Status Indicators Row -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
            <div onclick="filterByRadarStatus('green')" class="bg-white/5 hover:bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-2.5 transition-all cursor-pointer">
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-emerald-400 font-medium">🟢 完美兼容实测</span>
                <span class="text-xs font-mono font-bold text-emerald-400">88 款</span>
              </div>
              <p class="text-[10px] text-zinc-400 mt-0.5 truncate">最新推送实测稳定运行，点击筛选</p>
            </div>

            <div onclick="filterByRadarStatus('yellow')" class="bg-white/5 hover:bg-amber-500/10 border border-amber-500/20 rounded-xl p-2.5 transition-all cursor-pointer">
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-amber-400 font-medium">🟡 需更前置/降级</span>
                <span class="text-xs font-mono font-bold text-amber-400">9 款</span>
              </div>
              <p class="text-[10px] text-zinc-400 mt-0.5 truncate">需升级 Script Extender 前置</p>
            </div>

            <div onclick="filterByRadarStatus('red')" class="bg-white/5 hover:bg-red-500/10 border border-red-500/30 rounded-xl p-2.5 transition-all cursor-pointer">
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-red-400 font-medium">🔴 坏档暂停更新</span>
                <span class="text-xs font-mono font-bold text-red-400">3 款</span>
              </div>
              <p class="text-[10px] text-zinc-400 mt-0.5 truncate">次世代破坏老Mod，需锁定更新</p>
            </div>
          </div>
        </div>"""

    new_radar_box = """        <!-- ======================================================== -->
        <!-- STEAM RADAR LIVE STATUS BAR & COMPATIBILITY CAPSULE      -->
        <!-- ======================================================== -->
        <div class="mb-6 bg-white dark:bg-gradient-to-r dark:from-zinc-900 dark:via-[#12141c] dark:to-zinc-900 rounded-[24px] p-4 sm:p-5 border border-zinc-200/80 dark:border-white/10 shadow-sm text-zinc-900 dark:text-white space-y-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div class="flex items-center space-x-2.5">
              <span class="relative flex h-2.5 w-2.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span class="font-extrabold text-sm sm:text-base tracking-tight text-zinc-900 dark:text-white flex items-center gap-1.5">
                <span>📡 Steam 补丁变动与 Mod 兼容性实时避坑雷达</span>
              </span>
              <span class="bg-[#A855F7]/10 dark:bg-[#A855F7]/20 text-[#A855F7] dark:text-purple-400 text-[10px] font-mono px-2 py-0.5 rounded-full border border-[#A855F7]/20 dark:border-[#A855F7]/30 font-bold">24h 智能巡检</span>
            </div>

            <!-- Link to Standalone Radar -->
            <a 
              href="radar.html"
              class="self-start sm:self-auto px-3.5 py-1.5 rounded-full text-xs font-semibold bg-zinc-100 hover:bg-zinc-200 dark:bg-white/10 dark:hover:bg-white/20 text-zinc-700 dark:text-zinc-200 border border-zinc-200 dark:border-white/10 transition-all flex items-center gap-1.5 group cursor-pointer"
            >
              <span>进入全屏雷达看板</span>
              <svg class="w-3.5 h-3.5 text-zinc-400 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </a>
          </div>

          <!-- Status Indicators Row -->
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1">
            <div onclick="filterByRadarStatus('green')" class="bg-emerald-50/60 dark:bg-white/5 hover:bg-emerald-100/60 dark:hover:bg-emerald-500/10 border border-emerald-500/25 dark:border-emerald-500/20 rounded-xl p-2.5 transition-all cursor-pointer">
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-emerald-700 dark:text-emerald-400 font-bold">🟢 完美兼容实测</span>
                <span class="text-xs font-mono font-bold text-emerald-700 dark:text-emerald-400">88 款</span>
              </div>
              <p class="text-[10px] text-zinc-600 dark:text-zinc-400 mt-0.5 truncate">最新推送实测稳定运行，点击筛选</p>
            </div>

            <div onclick="filterByRadarStatus('yellow')" class="bg-amber-50/60 dark:bg-white/5 hover:bg-amber-100/60 dark:hover:bg-amber-500/10 border border-amber-500/25 dark:border-amber-500/20 rounded-xl p-2.5 transition-all cursor-pointer">
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-amber-700 dark:text-amber-400 font-bold">🟡 需更前置/降级</span>
                <span class="text-xs font-mono font-bold text-amber-700 dark:text-amber-400">9 款</span>
              </div>
              <p class="text-[10px] text-zinc-600 dark:text-zinc-400 mt-0.5 truncate">需升级 Script Extender 前置</p>
            </div>

            <div onclick="filterByRadarStatus('red')" class="bg-red-50/60 dark:bg-white/5 hover:bg-red-100/60 dark:hover:bg-red-500/10 border border-red-500/25 dark:border-red-500/30 rounded-xl p-2.5 transition-all cursor-pointer">
              <div class="flex items-center justify-between">
                <span class="text-[11px] text-red-700 dark:text-red-400 font-bold">🔴 坏档暂停更新</span>
                <span class="text-xs font-mono font-bold text-red-700 dark:text-red-400">3 款</span>
              </div>
              <p class="text-[10px] text-zinc-600 dark:text-zinc-400 mt-0.5 truncate">次世代破坏老Mod，需锁定更新</p>
            </div>
          </div>
        </div>"""

    content = content.replace(old_radar_box, new_radar_box)

    # 6. Update card.innerHTML to support responsive dark/light colors
    old_card_html_pattern = r"card\.innerHTML = `\s*<!-- 全息彩虹镭射层.*?`;"
    new_card_html = """card.innerHTML = `
          <!-- 全息彩虹镭射层 (Rainbow Holo Foil) -->
          <div class="holo-foil-layer"></div>
          <!-- 卡套高光漫射层 (Specular Glare) -->
          <div class="holo-glare-layer"></div>

          <div>
            <!-- 卡牌头部：序号、稀有度与生命值/避坑状态 -->
            <div class="flex items-center justify-between pb-2.5 border-b border-black/5 dark:border-white/10 text-xs font-mono-tech">
              <div class="flex items-center gap-2">
                <span class="font-bold text-zinc-900 dark:text-white tracking-wider">#${game.rank} // 100</span>
                <span class="text-[10px] ${isUltraRare ? 'text-amber-600 dark:text-amber-300 font-bold' : 'text-purple-600 dark:text-purple-300 font-medium'}">
                  ${isUltraRare ? '★★★ ULTRA RARE' : '★★ RARE'}
                </span>
              </div>
              <div class="flex items-center gap-1.5 text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">
                <span>HP 100</span>
                <span class="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_#10b981]"></span>
              </div>
            </div>

            <!-- 卡牌核心：金属箔框海报窗 (Artwork Window) -->
            <div class="card-foil-border my-3 overflow-hidden shadow-md">
              <div class="relative h-44 w-full overflow-hidden bg-black rounded-[14px]">
                ${game.headerImage ? `
                  <img src="${game.headerImage}" alt="${game.title}" loading="lazy" class="w-full h-full object-cover filter brightness-100 group-hover:scale-105 transition-transform duration-500" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
                ` : ''}
                <div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-zinc-800 to-zinc-900 text-3xl font-extrabold text-zinc-500" style="${game.headerImage ? 'display:none' : 'display:flex'}">
                  ${game.title.charAt(0)}
                </div>
                <div class="absolute bottom-2 left-2 px-2 py-0.5 bg-black/80 text-purple-300 font-mono-tech text-[10px] border border-purple-500/40 rounded">
                  ${game.developer || 'VERIFIED'}
                </div>
                <div class="absolute top-2 right-2 px-2 py-0.5 bg-black/80 text-emerald-400 font-mono-tech text-[10px] border border-emerald-500/40 rounded font-bold">
                  ${game.verifiedPatch || 'v2.13 COMPATIBLE'}
                </div>
              </div>
            </div>

            <!-- 卡牌标题与副标 -->
            <h2 class="font-display text-2xl text-zinc-900 dark:text-white tracking-wide group-hover:text-[#A855F7] dark:group-hover:text-purple-400 transition-colors line-clamp-1">${localizedTitle}</h2>
            <p class="text-[11px] text-zinc-500 dark:text-slate-400 font-mono-tech line-clamp-1 mt-0.5">${game.title} • ${game.releaseYear}</p>

            <!-- 宝可梦式技能战力槽 (Abilities / Moves Tray) -->
            <div class="ability-tray p-3 mt-3 space-y-2 text-xs font-mono-tech">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5 text-zinc-600 dark:text-slate-300 font-semibold">
                  <span class="text-purple-600 dark:text-purple-400">⚔</span>
                  <span>CORE EXTENDER</span>
                </div>
                <span class="text-zinc-900 dark:text-white font-bold">${game.hasMods ? '已对账框架' : '收录中'}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5 text-zinc-600 dark:text-slate-300 font-semibold">
                  <span class="text-emerald-600 dark:text-emerald-400">🛡</span>
                  <span>CLEAN TRAINER</span>
                </div>
                <span class="text-purple-600 dark:text-purple-300 font-bold">${game.hasTrainer ? '免翻直链已就绪' : '官方代码'}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5 text-zinc-600 dark:text-slate-300 font-semibold">
                  <span class="text-amber-600 dark:text-amber-400">⚡</span>
                  <span>ONE-CLICK .BAT</span>
                </div>
                <span class="text-emerald-600 dark:text-emerald-400 font-bold">${isCertified ? 'AUTO INJECT' : '对账中'}</span>
              </div>
            </div>
          </div>

          <!-- 卡牌底部铭牌与稀有度防伪戳 -->
          <div class="pt-3 border-t border-black/5 dark:border-white/10 flex items-center justify-between text-[11px] font-mono-tech text-zinc-500 dark:text-slate-400">
            <span>ILLUS. L-MOD VAULT</span>
            <div class="flex items-center gap-2">
              <span class="text-zinc-900 dark:text-white font-bold">${downloads} 次拉取</span>
              <span class="w-4 h-4 rounded-full bg-gradient-to-tr from-purple-500 to-cyan-400 flex items-center justify-center text-[9px] text-black font-extrabold shadow-sm">
                ★
              </span>
            </div>
          </div>
        `;"""

    content = re.sub(old_card_html_pattern, new_card_html, content, flags=re.DOTALL)

    # 7. Update list mode row classes
    content = content.replace(
        "listRow.className = 'group flex items-center justify-between p-3.5 px-4 rounded-2xl hover:bg-white dark:hover:bg-white/5 transition-all border border-transparent hover:border-zinc-200/80 dark:hover:border-white/10 shadow-none hover:shadow-sm';",
        "listRow.className = 'group flex items-center justify-between p-3.5 px-4 rounded-2xl bg-white/70 dark:bg-transparent hover:bg-white dark:hover:bg-white/5 transition-all border border-zinc-200/60 dark:border-transparent hover:border-zinc-300 dark:hover:border-white/10 shadow-none hover:shadow-sm';"
    )

    # 8. Update init3DCardPhysics for dynamic light/dark shadows
    old_physics = """          // 动态接触阴影 (随着手倾斜，背光阴影自然扩散)
          const shadowX = ((x - centerX) / centerX) * -12;
          const shadowY = ((y - centerY) / centerY) * -12 + 18;
          card.style.boxShadow = `${shadowX.toFixed(1)}px ${shadowY.toFixed(1)}px 35px rgba(0, 0, 0, 0.85), 0 0 15px rgba(168, 85, 247, 0.25)`;
        });

        cardContainer.addEventListener('mouseleave', () => {
          card.style.transform = 'rotateX(0deg) rotateY(0deg)';
          card.style.boxShadow = '0 15px 35px -5px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(0, 0, 0, 0.6)';
          card.style.transition = 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.45s ease';
        });"""

    new_physics = """          // 动态接触阴影 (随着手倾斜，背光阴影自然扩散)
          const isDark = document.documentElement.classList.contains('dark');
          const shadowX = ((x - centerX) / centerX) * -12;
          const shadowY = ((y - centerY) / centerY) * -12 + 18;
          if (isDark) {
            card.style.boxShadow = `${shadowX.toFixed(1)}px ${shadowY.toFixed(1)}px 35px rgba(0, 0, 0, 0.85), 0 0 15px rgba(168, 85, 247, 0.25)`;
          } else {
            card.style.boxShadow = `${shadowX.toFixed(1)}px ${shadowY.toFixed(1)}px 25px rgba(0, 0, 0, 0.08), 0 0 15px rgba(168, 85, 247, 0.12)`;
          }
        });

        cardContainer.addEventListener('mouseleave', () => {
          card.style.transform = 'rotateX(0deg) rotateY(0deg)';
          card.style.boxShadow = ''; // 清除内联阴影，优雅回落至 CSS var(--card-shadow)
          card.style.transition = 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.45s ease';
        });"""

    content = content.replace(old_physics, new_physics)

    # 9. Fix typo bg-purple-500/10/80
    content = content.replace('bg-purple-500/10/80', 'bg-purple-50 dark:bg-[#A855F7]/10')

    # 10. Update applyTheme in index.html to update meta theme-color
    old_apply_theme = """    function applyTheme(theme) {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    }"""

    new_apply_theme = """    function applyTheme(theme) {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      const metaThemeColor = document.querySelector('meta[name="theme-color"]');
      if (metaThemeColor) {
        metaThemeColor.setAttribute('content', theme === 'dark' ? '#090a0f' : '#f8fafc');
      }
    }"""

    content = content.replace(old_apply_theme, new_apply_theme)

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✔ Optimized index.html dark/light theme systems successfully.")


def optimize_radar():
    with open(RADAR_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update <style> in radar.html with semantic CSS variables
    old_radar_style = """    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }
    html, body {
      background-color: #0a0b0e;
      color: #e2e8f0;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }"""

    new_radar_style = """    :root {
      --radar-bg: #f8fafc;
      --radar-surface: #ffffff;
      --radar-card: #ffffff;
      --radar-card-hover: #f1f5f9;
      --radar-border: rgba(0, 0, 0, 0.08);
      --radar-text: #0f172a;
      --radar-text-muted: #64748b;
    }

    html.dark {
      --radar-bg: #0a0b0e;
      --radar-surface: #0c0d12;
      --radar-card: #12141a;
      --radar-card-hover: #181b24;
      --radar-border: rgba(255, 255, 255, 0.08);
      --radar-text: #e2e8f0;
      --radar-text-muted: #94a3b8;
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }
    html, body {
      background-color: var(--radar-bg);
      color: var(--radar-text);
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      transition: background-color 0.25s ease, color 0.25s ease;
    }"""

    content = content.replace(old_radar_style, new_radar_style)

    # 2. Update Header background in radar.html
    content = content.replace(
        '<header class="relative border-b border-white/[0.08] bg-[#0c0d12]/90 py-8 px-4 sm:px-8">',
        '<header class="relative border-b border-zinc-200/80 dark:border-white/[0.08] bg-white/90 dark:bg-[#0c0d12]/90 backdrop-blur-xl py-8 px-4 sm:px-8 transition-colors">'
    )
    content = content.replace(
        '<div class="w-full h-full bg-[#0e1017] rounded-[14px] flex items-center justify-center text-lg">',
        '<div class="w-full h-full bg-white dark:bg-[#0e1017] rounded-[14px] flex items-center justify-center text-lg shadow-sm">'
    )
    content = content.replace(
        '<h1 class="text-xl sm:text-2xl font-black tracking-tight text-white flex items-center gap-2">',
        '<h1 class="text-xl sm:text-2xl font-black tracking-tight text-zinc-900 dark:text-white flex items-center gap-2">'
    )
    content = content.replace(
        '<p class="text-xs text-zinc-400 flex items-center gap-2 pt-0.5">',
        '<p class="text-xs text-zinc-500 dark:text-zinc-400 flex items-center gap-2 pt-0.5">'
    )

    # 3. Add Theme Switcher Button into radar.html next to language dropdown
    old_radar_btn_group = """        <!-- Custom Language Dropdown for Radar -->
        <div class="relative" id="custom-lang-dropdown">"""

    new_radar_btn_group = """        <!-- Custom Theme Switcher Button for Radar -->
        <button 
          onclick="toggleTheme()" 
          id="theme-toggle-btn" 
          title="切换白天 / 夜间模式 (跟随当前设备)"
          class="flex items-center justify-center w-9 h-9 rounded-xl bg-zinc-100 hover:bg-zinc-200 dark:bg-white/5 dark:hover:bg-white/10 text-zinc-700 dark:text-zinc-300 border border-zinc-200/80 dark:border-white/10 shadow-sm transition-all cursor-pointer"
        >
          <!-- Sun Icon (for Dark mode) -->
          <svg class="w-4 h-4 hidden dark:block text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          <!-- Moon Icon (for Light mode) -->
          <svg class="w-4 h-4 block dark:hidden text-zinc-700" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>

        <!-- Custom Language Dropdown for Radar -->
        <div class="relative" id="custom-lang-dropdown">"""

    content = content.replace(old_radar_btn_group, new_radar_btn_group)

    # 4. Update Metric Cards in radar.html for light & dark mode
    content = content.replace(
        '<div onclick="filterByStatus(\'green\')" class="cursor-pointer group relative overflow-hidden bg-[#12141a] hover:bg-[#161922] p-4 rounded-2xl border border-emerald-500/20 hover:border-emerald-500/40 transition-all glow-green">',
        '<div onclick="filterByStatus(\'green\')" class="cursor-pointer group relative overflow-hidden bg-white dark:bg-[#12141a] hover:bg-slate-50 dark:hover:bg-[#161922] p-4 rounded-2xl border border-emerald-500/30 dark:border-emerald-500/20 hover:border-emerald-500/50 transition-all shadow-sm glow-green">'
    )
    content = content.replace(
        '<div onclick="filterByStatus(\'yellow\')" class="cursor-pointer group relative overflow-hidden bg-[#12141a] hover:bg-[#161922] p-4 rounded-2xl border border-amber-500/20 hover:border-amber-500/40 transition-all glow-amber">',
        '<div onclick="filterByStatus(\'yellow\')" class="cursor-pointer group relative overflow-hidden bg-white dark:bg-[#12141a] hover:bg-slate-50 dark:hover:bg-[#161922] p-4 rounded-2xl border border-amber-500/30 dark:border-amber-500/20 hover:border-amber-500/50 transition-all shadow-sm glow-amber">'
    )
    content = content.replace(
        '<div onclick="filterByStatus(\'red\')" class="cursor-pointer group relative overflow-hidden bg-[#12141a] hover:bg-[#161922] p-4 rounded-2xl border border-red-500/20 hover:border-red-500/40 transition-all glow-red">',
        '<div onclick="filterByStatus(\'red\')" class="cursor-pointer group relative overflow-hidden bg-white dark:bg-[#12141a] hover:bg-slate-50 dark:hover:bg-[#161922] p-4 rounded-2xl border border-red-500/30 dark:border-red-500/20 hover:border-red-500/50 transition-all shadow-sm glow-red">'
    )
    content = content.replace(
        '<div class="relative overflow-hidden bg-[#12141a] p-4 rounded-2xl border border-white/5">',
        '<div class="relative overflow-hidden bg-white dark:bg-[#12141a] p-4 rounded-2xl border border-zinc-200/80 dark:border-white/5 shadow-sm">'
    )

    # 5. Update Search & Filter Bar in radar.html
    content = content.replace(
        '<div class="bg-[#12141a] rounded-2xl p-4 sm:p-5 border border-white/[0.08] space-y-4 shadow-xl">',
        '<div class="bg-white dark:bg-[#12141a] rounded-2xl p-4 sm:p-5 border border-zinc-200/80 dark:border-white/[0.08] space-y-4 shadow-sm dark:shadow-xl">'
    )
    content = content.replace(
        'class="w-full bg-[#0a0b0e] text-white text-xs sm:text-sm pl-10 pr-10 py-2.5 rounded-xl border border-white/10 focus:border-[#A855F7] focus:outline-none focus:ring-1 focus:ring-[#A855F7] placeholder-zinc-500 transition-all"',
        'class="w-full bg-slate-50 dark:bg-[#0a0b0e] text-zinc-900 dark:text-white text-xs sm:text-sm pl-10 pr-10 py-2.5 rounded-xl border border-zinc-200 dark:border-white/10 focus:border-[#A855F7] focus:outline-none focus:ring-1 focus:ring-[#A855F7] placeholder-zinc-400 dark:placeholder-zinc-500 transition-all"'
    )
    content = content.replace(
        'class="bg-[#0a0b0e] text-white text-xs py-2.5 px-3 rounded-xl border border-white/10 focus:border-[#A855F7] focus:outline-none cursor-pointer"',
        'class="bg-slate-50 dark:bg-[#0a0b0e] text-zinc-900 dark:text-white text-xs py-2.5 px-3 rounded-xl border border-zinc-200 dark:border-white/10 focus:border-[#A855F7] focus:outline-none cursor-pointer"'
    )

    # 6. Update renderRadarCards in radar.html for dual-mode cards
    content = content.replace(
        'class="group relative overflow-hidden bg-[#12141a] hover:bg-[#161822] rounded-2xl p-5 border ${statusBorder} transition-all duration-200 cursor-pointer flex flex-col justify-between shadow-lg"',
        'class="group relative overflow-hidden bg-white dark:bg-[#12141a] hover:bg-slate-50 dark:hover:bg-[#161822] rounded-2xl p-5 border ${statusBorder} transition-all duration-200 cursor-pointer flex flex-col justify-between shadow-sm dark:shadow-lg"'
    )
    content = content.replace(
        '<h3 class="text-base sm:text-lg font-black text-white group-hover:text-[#A855F7] transition-colors line-clamp-1">',
        '<h3 class="text-base sm:text-lg font-black text-zinc-900 dark:text-white group-hover:text-[#A855F7] dark:group-hover:text-purple-400 transition-colors line-clamp-1">'
    )
    content = content.replace(
        '<span class="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-zinc-300 border border-white/5 truncate max-w-[220px]">',
        '<span class="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-100 dark:bg-white/5 text-zinc-700 dark:text-zinc-300 border border-zinc-200 dark:border-white/5 truncate max-w-[220px]">'
    )
    content = content.replace(
        '<p class="text-xs text-zinc-300 line-clamp-2 leading-relaxed pt-1">',
        '<p class="text-xs text-zinc-600 dark:text-zinc-300 line-clamp-2 leading-relaxed pt-1">'
    )
    content = content.replace(
        '<div class="flex items-center justify-between pt-4 mt-3 border-t border-white/5 text-xs">',
        '<div class="flex items-center justify-between pt-4 mt-3 border-t border-zinc-200/80 dark:border-white/5 text-xs">'
    )

    # 7. Update Drawer styling in radar.html
    content = content.replace(
        'class="drawer-content absolute inset-x-0 bottom-0 md:inset-y-0 md:left-auto md:right-0 md:w-[620px] max-h-[92vh] md:max-h-full bg-[#101218] border-t md:border-t-0 md:border-l border-white/10 rounded-t-[28px] md:rounded-t-none md:rounded-l-[28px] shadow-2xl flex flex-col overflow-hidden translate-y-full md:translate-y-0 md:translate-x-full transition-transform pointer-events-auto"',
        'class="drawer-content absolute inset-x-0 bottom-0 md:inset-y-0 md:left-auto md:right-0 md:w-[620px] max-h-[92vh] md:max-h-full bg-white dark:bg-[#101218] border-t md:border-t-0 md:border-l border-zinc-200 dark:border-white/10 rounded-t-[28px] md:rounded-t-none md:rounded-l-[28px] shadow-2xl flex flex-col overflow-hidden translate-y-full md:translate-y-0 md:translate-x-full transition-transform pointer-events-auto"'
    )
    content = content.replace(
        '<h2 class="text-xl sm:text-2xl font-black text-white" id="drawer-title"></h2>',
        '<h2 class="text-xl sm:text-2xl font-black text-zinc-900 dark:text-white" id="drawer-title"></h2>'
    )
    content = content.replace(
        '<p class="text-xs text-zinc-300 leading-relaxed" id="drawer-summary"></p>',
        '<p class="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed" id="drawer-summary"></p>'
    )
    content = content.replace(
        '<div class="space-y-2 text-xs text-zinc-300 leading-relaxed" id="drawer-rescue-steps">',
        '<div class="space-y-2 text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed" id="drawer-rescue-steps">'
    )

    # 8. Add Theme Management JavaScript into radar.html
    radar_theme_js = """
    // ========================================================
    // DAY / NIGHT DUAL-THEME SWITCHER FOR RADAR
    // ========================================================
    function initTheme() {
      const savedTheme = localStorage.getItem('lmod_theme');
      if (savedTheme) {
        applyTheme(savedTheme);
      } else {
        const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(systemPrefersDark ? 'dark' : 'light');
      }

      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('lmod_theme')) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }

    function toggleTheme() {
      const isDark = document.documentElement.classList.contains('dark');
      const newTheme = isDark ? 'light' : 'dark';
      localStorage.setItem('lmod_theme', newTheme);
      applyTheme(newTheme);
      showToast(newTheme === 'dark' ? '已切换至深色模式 🌙' : '已切换至浅色模式 ☀️');
    }

    function applyTheme(theme) {
      if (theme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      const metaThemeColor = document.querySelector('meta[name="theme-color"]');
      if (metaThemeColor) {
        metaThemeColor.setAttribute('content', theme === 'dark' ? '#0a0b0e' : '#f8fafc');
      }
    }
    """

    content = content.replace("function init() {", radar_theme_js + "\n    function init() {\n      initTheme();")

    with open(RADAR_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✔ Injected and optimized radar.html theme system successfully.")

if __name__ == '__main__':
    optimize_index()
    optimize_radar()
