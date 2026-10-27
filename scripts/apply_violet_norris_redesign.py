#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_violet_norris_redesign.py
Applies the finalized #A855F7 Neon Violet + Lando Norris Kinetic 3D Tilt styling to public/index.html
"""

import os
import re

INDEX_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Head styles (Add fonts, variables, 3D tilt, and custom cursor)
old_style_marker = "<style>"
new_css = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
      --bg-base: #0b0c0f;
      --card-bg: #13151b;
      --card-border: #21242d;
      --accent: #A855F7; /* Neon Violet Final Selection */
      --accent-dim: rgba(168, 85, 247, 0.14);
      --card-border-hover: #A855F7;
      --text-muted: #8b8f9e;
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      background-color: var(--bg-base);
      color: #f3f4f6;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
    }

    .font-display {
      font-family: 'Bebas Neue', sans-serif;
      letter-spacing: 0.04em;
    }

    .font-mono-tech {
      font-family: 'JetBrains Mono', monospace;
    }

    /* === 诺里斯定制物理光标 === */
    #cursor-dot {
      position: fixed;
      top: 0;
      left: 0;
      width: 6px;
      height: 6px;
      background-color: var(--accent);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9999;
      transform: translate(-50%, -50%);
      box-shadow: 0 0 10px var(--accent);
      transition: opacity 0.2s ease;
    }

    #cursor-ring {
      position: fixed;
      top: 0;
      left: 0;
      width: 40px;
      height: 40px;
      border: 1.5px solid var(--accent);
      border-radius: 50%;
      pointer-events: none;
      z-index: 9998;
      transform: translate(-50%, -50%);
      transition: width 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                  height 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                  border-radius 0.28s ease,
                  background-color 0.2s ease;
      mix-blend-mode: difference;
    }

    body.cursor-hover #cursor-ring {
      width: 105px;
      height: 34px;
      border-radius: 999px;
      background-color: var(--accent);
      border-color: transparent;
      mix-blend-mode: normal;
    }
    body.cursor-hover #cursor-dot {
      opacity: 0;
    }

    #cursor-label {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 800;
      color: #000000;
      letter-spacing: 0.08em;
      opacity: 0;
      white-space: nowrap;
      pointer-events: none;
      transition: opacity 0.2s ease;
    }
    body.cursor-hover #cursor-label {
      opacity: 1;
    }

    /* === 3D 跟随鼠标微抬升 (紧致 4px 抬起 · 严格 1:1 无缩放) === */
    .card-3d-viewport {
      perspective: 750px;
      transform-style: preserve-3d;
    }

    .card-3d-body {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      position: relative;
      transform-style: preserve-3d;
      transform: translateZ(0);
      transition: transform 0.08s ease-out, 
                  border-color 0.25s ease, 
                  box-shadow 0.25s ease;
      will-change: transform, box-shadow;
    }

    .layer-z-header {
      transform: translateZ(8px);
      transform-style: preserve-3d;
    }
    .layer-z-media {
      transform: translateZ(14px);
      transform-style: preserve-3d;
    }
    .layer-z-text {
      transform: translateZ(22px);
      transform-style: preserve-3d;
    }
    .layer-z-btn {
      transform: translateZ(28px);
      transform-style: preserve-3d;
    }

    /* 动态表面反光层 */
    .glare-overlay {
      position: absolute;
      inset: 0;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.25s ease;
      background: linear-gradient(
        var(--glare-angle, 135deg),
        rgba(255, 255, 255, 0.08) 0%,
        var(--accent-dim) 40%,
        transparent 70%
      );
      z-index: 10;
    }
    .card-3d-body:hover .glare-overlay {
      opacity: 1;
    }

    /* 工业十字准星标记 */
    .cross-marker {
      position: relative;
    }
    .cross-marker::before, .cross-marker::after {
      content: '+';
      position: absolute;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #3b3f4d;
      pointer-events: none;
    }
    .cross-marker::before { top: -8px; left: -8px; }
    .cross-marker::after { bottom: -8px; right: -8px; }

    /* 跑马灯 */
    .ticker-wrap {
      width: 100%;
      overflow: hidden;
      white-space: nowrap;
      background: #111317;
      border-top: 1px solid var(--card-border);
      border-bottom: 1px solid var(--card-border);
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

    /* 诺里斯经典动作按钮 */
    .btn-action {
      background: transparent;
      color: #f3f4f6;
      border: 1px solid var(--card-border);
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .card-3d-body:hover .btn-action, .btn-action:hover {
      background: var(--accent);
      color: #000000;
      border-color: var(--accent);
      box-shadow: 0 0 16px var(--accent);
    }
"""

content = content.replace(old_style_marker, new_css, 1)

# 2. Add cursor elements inside <body>
if 'id="cursor-dot"' not in content:
    content = content.replace(
        '<body class="',
        '<!-- Custom Fluid Cursor -->\n  <div id="cursor-dot"></div>\n  <div id="cursor-ring"><span id="cursor-label">3D // 01</span></div>\n\n  <body class="',
        1
    )

# 3. Update body background styling
content = re.sub(
    r'<body class="[^"]*"',
    '<body class="bg-[#0b0c0f] text-slate-100 min-h-screen flex flex-col md:flex-row transition-colors duration-300 selection:bg-[#A855F7] selection:text-black"',
    content,
    count=1
)

# 4. Save updated file
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Injected head CSS and cursor DOM into public/index.html")
