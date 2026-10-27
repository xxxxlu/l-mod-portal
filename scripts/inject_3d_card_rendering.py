#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/inject_3d_card_rendering.py
Injects the 3D Tilt Viewport and #A855F7 card template into public/index.html
"""

import os
import re

INDEX_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Define the old card creation block in renderGames
old_gallery_card_pattern = r"// 1\. GALLERY CARD \(Apple clean card with subtle shadow & hover lift\).*?galleryCon\.appendChild\(card\);"

new_gallery_card_code = """// 1. KINETIC 3D TILT GALLERY CARD (Strict 1:1 Scale · 4px Grounded Elevation · Multi-layer Parallax)
        const cardWrap = document.createElement('div');
        cardWrap.className = 'card-3d-viewport';
        cardWrap.setAttribute('data-3d-card', '');
        cardWrap.setAttribute('data-cursor', `3D // #${game.rank}`);

        const card = document.createElement('a');
        card.id = `game-card-${game.id}`;
        card.href = `#/game/${game.id}`;
        card.onclick = () => saveCatalogScroll(game.id);
        card.className = 'card-3d-body cross-marker group relative p-5 rounded-2xl flex flex-col justify-between h-[495px] transition-colors';

        card.innerHTML = `
          <div class="glare-overlay"></div>

          <!-- Top Meta Bar (Layer Z-8) -->
          <div class="layer-z-header flex items-center justify-between pb-3 border-b border-[#21242d] text-xs font-mono-tech">
            <span class="font-bold text-white">#${game.rank} // REPO</span>
            <span class="px-2 py-0.5 bg-[#A855F7]/15 text-[#A855F7] border border-[#A855F7]/40 font-bold text-[10px] rounded">
              [ ${game.verifiedPatch || 'v2.13 COMPATIBLE'} ]
            </span>
          </div>

          <!-- Game Media Poster (Layer Z-14) -->
          <div class="layer-z-media relative h-44 overflow-hidden my-3 bg-black border border-[#21242d] rounded-xl">
            ${game.headerImage ? `
              <img src="${game.headerImage}" alt="${game.title}" loading="lazy" class="w-full h-full object-cover filter brightness-100 group-hover:scale-105 transition-transform duration-500" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">
            ` : ''}
            <div class="w-full h-full flex items-center justify-center bg-gradient-to-br from-zinc-800 to-zinc-900 text-3xl font-extrabold text-zinc-500" style="${game.headerImage ? 'display:none' : 'display:flex'}">
              ${game.title.charAt(0)}
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-[#13151b] via-transparent to-black/30"></div>
            
            <div class="absolute bottom-2 left-2 px-2 py-0.5 bg-black/80 font-mono-tech text-[10px] text-[#A855F7] border border-[#A855F7]/40 rounded">
              ${game.developer || 'VERIFIED'}
            </div>
            <div class="absolute top-2 right-2">
              <span class="px-2 py-0.5 rounded text-[10px] font-mono-tech font-bold bg-black/70 text-emerald-400 border border-emerald-500/30 backdrop-blur-md">
                ${rating} 好评
              </span>
            </div>
          </div>

          <!-- Title and Info (Layer Z-22) -->
          <div class="layer-z-text">
            <h3 class="font-display text-2xl text-white tracking-wide group-hover:text-[#A855F7] transition-colors line-clamp-1">${localizedTitle}</h3>
            <p class="text-xs text-[#8b8f9e] font-mono-tech line-clamp-1 mt-0.5">${game.title} • ${game.releaseYear}</p>
            
            <div class="mt-3 space-y-1.5 text-xs font-mono-tech">
              <div class="flex items-center justify-between text-[#8b8f9e]">
                <span>MOD 生态:</span>
                <span class="text-white font-semibold">${game.hasMods ? '已对账框架' : '收录中'}</span>
              </div>
              <div class="flex items-center justify-between text-[#8b8f9e]">
                <span>纯净修改器:</span>
                <span class="text-[#A855F7] font-semibold">${game.hasTrainer ? '免翻直链已就绪' : '官方代码'}</span>
              </div>
              <div class="flex items-center justify-between text-[#8b8f9e]">
                <span>雷达避坑:</span>
                <span class="text-emerald-400 font-semibold">${isCertified ? '🟢 官方认证无损' : '🟡 持续对账中'}</span>
              </div>
            </div>
          </div>

          <!-- Bottom Action (Layer Z-28) -->
          <div class="layer-z-btn pt-3 border-t border-[#21242d] flex items-center justify-between text-xs font-mono-tech">
            <span class="text-[11px] text-[#8b8f9e]">${downloads} 次拉取</span>
            <span class="btn-action px-3 py-1 text-xs rounded transition-all">
              展开档案 ➔
            </span>
          </div>
        `;
        cardWrap.appendChild(card);
        galleryCon.appendChild(cardWrap);"""

# Replace the gallery card creation logic
content, count = re.subn(old_gallery_card_pattern, new_gallery_card_code, content, count=1, flags=re.DOTALL)
assert count == 1, "Failed to match old_gallery_card_pattern in renderGames"

# 2. Add init3DCardTilt() and initCustomCursor() functions right after renderGames()
physics_logic = """
    // === 诺里斯定制光标与 3D 物理倾角引擎 ===
    function init3DCardPhysics() {
      const cards = document.querySelectorAll('[data-3d-card]');
      cards.forEach(card => {
        const body = card.querySelector('.card-3d-body');
        if (!body || body.__has3dListener) return;
        body.__has3dListener = true;

        card.addEventListener('mousemove', (e) => {
          const rect = card.getBoundingClientRect();
          const x = e.clientX - rect.left;
          const y = e.clientY - rect.top;

          const centerX = rect.width / 2;
          const centerY = rect.height / 2;

          const rotateX = ((y - centerY) / centerY) * -11;
          const rotateY = ((x - centerX) / centerX) * 11;

          const shadowX = ((x - centerX) / centerX) * -10;
          const shadowY = ((y - centerY) / centerY) * -10 + 14;

          // 核心：严格 1:1 无缩放，紧致 4px 微抬，真实 Z 轴视差
          body.style.transform = `perspective(750px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(10px) translateY(-4px)`;
          body.style.borderColor = '#A855F7';
          body.style.boxShadow = `${shadowX.toFixed(1)}px ${shadowY.toFixed(1)}px 24px rgba(0, 0, 0, 0.75), 0 0 15px rgba(168, 85, 247, 0.2)`;

          const angle = Math.atan2(y - centerY, x - centerX) * (180 / Math.PI) + 90;
          body.style.setProperty('--glare-angle', `${angle.toFixed(1)}deg`);
        });

        card.addEventListener('mouseleave', () => {
          body.style.transform = 'perspective(750px) rotateX(0deg) rotateY(0deg) translateZ(0) translateY(0)';
          body.style.borderColor = 'var(--card-border)';
          body.style.boxShadow = 'none';
          body.style.transition = 'transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease, border-color 0.25s ease';
        });

        card.addEventListener('mouseenter', () => {
          body.style.transition = 'none';
        });
      });
    }

    let cursorInitialized = false;
    function initCustomCursor() {
      if (cursorInitialized) return;
      cursorInitialized = true;

      const dot = document.getElementById('cursor-dot');
      const ring = document.getElementById('cursor-ring');
      const label = document.getElementById('cursor-label');
      if (!dot || !ring) return;

      let mouseX = window.innerWidth / 2;
      let mouseY = window.innerHeight / 2;
      let ringX = mouseX;
      let ringY = mouseY;

      window.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
      });

      function animateCursor() {
        ringX += (mouseX - ringX) * 0.22;
        ringY += (mouseY - ringY) * 0.22;
        ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;
        requestAnimationFrame(animateCursor);
      }
      animateCursor();

      document.body.addEventListener('mouseover', (e) => {
        const targetCard = e.target.closest('[data-cursor]');
        if (targetCard) {
          document.body.classList.add('cursor-hover');
          if (label) label.innerText = targetCard.getAttribute('data-cursor') || '3D';
        } else if (e.target.closest('button, a')) {
          ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%) scale(1.35)`;
        } else {
          document.body.classList.remove('cursor-hover');
          ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%) scale(1)`;
        }
      });
    }
"""

# Append call inside renderGames()
render_games_end = "listCon.appendChild(listRow);\n      });"
replacement_render_games_end = """listCon.appendChild(listRow);\n      });\n      init3DCardPhysics();\n      initCustomCursor();"""

content = content.replace(render_games_end, replacement_render_games_end, 1)

# Also append the physics functions
content = content.replace("function renderGameDetailView(game) {", physics_logic + "\n    function renderGameDetailView(game) {", 1)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Injected 3D card physics & custom cursor into renderGames() in public/index.html")
