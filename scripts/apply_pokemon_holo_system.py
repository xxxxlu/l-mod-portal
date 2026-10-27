#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/apply_pokemon_holo_system.py
Transforms public/index.html into the finalized Concept 9: Pokémon Holographic Foil Trading Card (PTCG) design system.
"""

import os
import re

INDEX_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update CSS in <head> for Pokémon Holo Foil Shader
old_css_start = "<style>"
old_css_end = "/* Custom Apple & Google hybrid scrollbars */"

new_holo_css = """<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
      --bg-base: #07080a;
      --card-cardstock: #111319;
      --card-border: rgba(255, 255, 255, 0.12);
      --accent: #A855F7; /* Neon Violet Accent */
      --accent-dim: rgba(168, 85, 247, 0.14);
      --text-muted: #8b8f9e;
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      background-color: var(--bg-base);
      color: #f1f5f9;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
      background-image: radial-gradient(circle at 50% 15%, rgba(168, 85, 247, 0.08) 0%, transparent 60%);
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
      
      /* 物理实体卡边缘：金属反光边框 + 扎实的真实接触阴影 */
      border: 1.5px solid rgba(255, 255, 255, 0.14);
      box-shadow: 
        0 15px 35px -5px rgba(0, 0, 0, 0.8),
        0 0 0 1px rgba(0, 0, 0, 0.6);
      
      transition: transform 0.1s ease-out, box-shadow 0.25s ease;
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
      mix-blend-mode: color-dodge; /* 产生闪卡独特的彩虹反光 */
      
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
      
      background-size: 200% 200%, 100% 100%;
      background-position: var(--foil-pos-x, 50%) var(--foil-pos-y, 50%);
      transition: opacity 0.35s ease;
    }

    /* === 宝可梦闪卡灵魂 2：卡套高光漫射层 (Specular Glare) === */
    .holo-glare-layer {
      position: absolute;
      inset: 0;
      border-radius: inherit;
      pointer-events: none;
      z-index: 25;
      opacity: 0;
      mix-blend-mode: overlay;
      
      background: radial-gradient(
        400px circle at var(--pointer-x, 50%) var(--pointer-y, 50%),
        rgba(255, 255, 255, 0.55) 0%,
        rgba(255, 255, 255, 0.15) 30%,
        transparent 65%
      );
      transition: opacity 0.25s ease;
    }

    /* 悬停时激活闪卡彩虹光泽 */
    .pokemon-card:hover .holo-foil-layer,
    .pokemon-card:hover .holo-glare-layer {
      opacity: 0.85;
    }

    /* 金属箔框 */
    .card-foil-border {
      position: relative;
      border-radius: 16px;
      background: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(168, 85, 247, 0.25) 50%, rgba(255, 255, 255, 0.08) 100%);
      padding: 1.5px;
    }

    /* 闪卡技能槽/属性框 (PTCG Abilities Box) */
    .ability-tray {
      background: rgba(10, 11, 15, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.1);
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

    /* 动作按钮 */
    .btn-action {
      background: transparent;
      color: #f3f4f6;
      border: 1px solid rgba(255, 255, 255, 0.14);
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .pokemon-card:hover .btn-action, .btn-action:hover {
      background: var(--accent);
      color: #000000;
      border-color: var(--accent);
      box-shadow: 0 0 16px var(--accent);
    }

    """

# Replace the style header
idx_start = content.find("<style>")
idx_end = content.find("/* Custom Apple & Google hybrid scrollbars */")
if idx_start != -1 and idx_end != -1:
    content = content[:idx_start] + new_holo_css + content[idx_end:]

# 2. Update renderGames() card template to render true Pokémon Holo Trading Cards
old_card_gen = r"// 1\. KINETIC 3D TILT GALLERY CARD.*?galleryCon\.appendChild\(cardWrap\);"

new_card_gen = """// 1. POKÉMON HOLOGRAPHIC FOIL TRADING CARD (PTCG Secret Rare Spec)
        const isUltraRare = game.rank <= 14;
        const cardWrap = document.createElement('div');
        cardWrap.className = 'pokemon-card-container';
        cardWrap.setAttribute('data-holo-card', '');

        const card = document.createElement('a');
        card.id = `game-card-${game.id}`;
        card.href = `#/game/${game.id}`;
        card.onclick = () => saveCatalogScroll(game.id);
        card.className = 'pokemon-card group relative p-4 flex flex-col justify-between h-[510px] cursor-pointer';

        card.innerHTML = `
          <!-- 全息彩虹镭射层 (Rainbow Holo Foil) -->
          <div class="holo-foil-layer"></div>
          <!-- 卡套高光漫射层 (Specular Glare) -->
          <div class="holo-glare-layer"></div>

          <div>
            <!-- 卡牌头部：序号、稀有度与生命值/避坑状态 -->
            <div class="flex items-center justify-between pb-2.5 border-b border-white/10 text-xs font-mono-tech">
              <div class="flex items-center gap-2">
                <span class="font-bold text-white tracking-wider">#${game.rank} // 100</span>
                <span class="text-[10px] ${isUltraRare ? 'text-amber-300 font-bold' : 'text-purple-300'}">
                  ${isUltraRare ? '★★★ ULTRA RARE' : '★★ RARE'}
                </span>
              </div>
              <div class="flex items-center gap-1.5 text-[10px] text-emerald-400 font-bold">
                <span>HP 100</span>
                <span class="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#10b981]"></span>
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
            <h2 class="font-display text-2xl text-white tracking-wide group-hover:text-[#A855F7] transition-colors line-clamp-1">${localizedTitle}</h2>
            <p class="text-[11px] text-slate-400 font-mono-tech line-clamp-1 mt-0.5">${game.title} • ${game.releaseYear}</p>

            <!-- 宝可梦式技能战力槽 (Abilities / Moves Tray) -->
            <div class="ability-tray p-3 mt-3 space-y-2 text-xs font-mono-tech">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5 text-slate-300 font-semibold">
                  <span class="text-purple-400">⚔</span>
                  <span>CORE EXTENDER</span>
                </div>
                <span class="text-white font-bold">${game.hasMods ? '已对账框架' : '收录中'}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5 text-slate-300 font-semibold">
                  <span class="text-emerald-400">🛡</span>
                  <span>CLEAN TRAINER</span>
                </div>
                <span class="text-purple-300 font-bold">${game.hasTrainer ? '免翻直链已就绪' : '官方代码'}</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-1.5 text-slate-300 font-semibold">
                  <span class="text-amber-400">⚡</span>
                  <span>ONE-CLICK .BAT</span>
                </div>
                <span class="text-emerald-400 font-bold">${isCertified ? 'AUTO INJECT' : '对账中'}</span>
              </div>
            </div>
          </div>

          <!-- 卡牌底部铭牌与稀有度防伪戳 -->
          <div class="pt-3 border-t border-white/10 flex items-center justify-between text-[11px] font-mono-tech text-slate-400">
            <span>ILLUS. L-MOD VAULT</span>
            <div class="flex items-center gap-2">
              <span class="text-white font-bold">${downloads} 次拉取</span>
              <span class="w-4 h-4 rounded-full bg-gradient-to-tr from-purple-500 to-cyan-400 flex items-center justify-center text-[9px] text-black font-extrabold shadow-sm">
                ★
              </span>
            </div>
          </div>
        `;
        cardWrap.appendChild(card);
        galleryCon.appendChild(cardWrap);"""

content, count = re.subn(old_card_gen, new_card_gen, content, count=1, flags=re.DOTALL)
assert count == 1, "Failed to replace gallery card generation"

# 3. Update physics function to center-anchored Pokémon Holo physics
old_physics_pattern = r"// === 诺里斯定制光标与 3D 物理倾角引擎 ===.*?function initCustomCursor\(\) \{"

new_holo_physics = """// === 宝可梦全息闪卡 (PTCG Holo Foil) 物理与着色引擎 ===
    function init3DCardPhysics() {
      const cards = document.querySelectorAll('[data-holo-card]');
      cards.forEach(cardContainer => {
        const card = cardContainer.querySelector('.pokemon-card');
        if (!card || card.__hasHoloListener) return;
        card.__hasHoloListener = true;

        cardContainer.addEventListener('mousemove', (e) => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;

          const centerX = rect.width / 2;
          const centerY = rect.height / 2;

          // 真实重心旋转角度 (rotateX, rotateY)，绝不带 translateY 或 translateZ 突兀位移！
          const rotateX = ((y - centerY) / centerY) * -13;
          const rotateY = ((x - centerX) / centerX) * 13;

          // 核心：严格围绕中心 50% 50% 旋转，不产生位移！
          card.style.transform = `rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg)`;

          // 彩虹镭射反光位置计算 (随着角度偏转，彩虹光斑滑过卡牌)
          const foilPosX = 50 + ((x - centerX) / centerX) * 50;
          const foilPosY = 50 + ((y - centerY) / centerY) * 50;
          card.style.setProperty('--foil-pos-x', `${foilPosX.toFixed(1)}%`);
          card.style.setProperty('--foil-pos-y', `${foilPosY.toFixed(1)}%`);

          // 高光反射点
          card.style.setProperty('--pointer-x', `${x.toFixed(1)}px`);
          card.style.setProperty('--pointer-y', `${y.toFixed(1)}px`);

          // 动态接触阴影 (随着手倾斜，背光阴影自然扩散)
          const shadowX = ((x - centerX) / centerX) * -12;
          const shadowY = ((y - centerY) / centerY) * -12 + 18;
          card.style.boxShadow = `${shadowX.toFixed(1)}px ${shadowY.toFixed(1)}px 35px rgba(0, 0, 0, 0.85), 0 0 15px rgba(168, 85, 247, 0.25)`;
        });

        cardContainer.addEventListener('mouseleave', () => {
          card.style.transform = 'rotateX(0deg) rotateY(0deg)';
          card.style.boxShadow = '0 15px 35px -5px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(0, 0, 0, 0.6)';
          card.style.transition = 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.45s ease';
        });

        cardContainer.addEventListener('mouseenter', () => {
          card.style.transition = 'none';
        });
      });
    }

    function initCustomCursor() {"""

content, count = re.subn(old_physics_pattern, new_holo_physics, content, count=1, flags=re.DOTALL)
assert count == 1, "Failed to replace physics functions"

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Successfully applied Pokémon Holo Foil system to public/index.html!")
