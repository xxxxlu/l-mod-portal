# -*- coding: utf-8 -*-
"""
scripts/fix_radar_anchors.py
Comprehensive anchor fixing for public/radar.html
"""

RADAR_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/radar.html'

with open(RADAR_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix HTML anchors in Card 2
old_card2 = """      <!-- Card 2: Amber Need Update -->
      <div onclick="filterByStatus('yellow')" class="cursor-pointer group relative overflow-hidden bg-[#12141a] hover:bg-[#161922] p-4 rounded-2xl border border-amber-500/20 hover:border-amber-500/40 transition-all glow-amber">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-medium text-amber-400 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
            <span>需更新前置 / 补丁对齐</span>
          </span>
          <span class="text-[10px] bg-amber-500/10 text-amber-300 px-2 py-0.5 rounded font-mono">注意前置</span>
        </div>
        <div class="flex items-baseline space-x-2">
          <span class="text-2xl sm:text-3xl font-black font-mono text-amber-400" id="stat-yellow">9</span>
          <span class="text-xs text-zinc-400">款需适配</span>
        </div>
        <p class="text-[11px] text-zinc-400 mt-1 line-clamp-1">老版 DLL 钩子失效，需升级最新版 Script Extender</p>
      </div>"""

new_card2 = """      <!-- Card 2: Amber Need Update -->
      <div onclick="filterByStatus('yellow')" class="cursor-pointer group relative overflow-hidden bg-[#12141a] hover:bg-[#161922] p-4 rounded-2xl border border-amber-500/20 hover:border-amber-500/40 transition-all glow-amber">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-medium text-amber-400 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
            <span id="metric-yellow-title">需更新前置 / 补丁对齐</span>
          </span>
          <span class="text-[10px] bg-amber-500/10 text-amber-300 px-2 py-0.5 rounded font-mono" id="metric-yellow-tag">注意前置</span>
        </div>
        <div class="flex items-baseline space-x-2">
          <span class="text-2xl sm:text-3xl font-black font-mono text-amber-400" id="stat-yellow">9</span>
          <span class="text-xs text-zinc-400" id="metric-yellow-unit">款需适配</span>
        </div>
        <p class="text-[11px] text-zinc-400 mt-1 line-clamp-1" id="metric-yellow-desc">老版 DLL 钩子失效，需升级最新版 Script Extender</p>
      </div>"""

if old_card2 in html:
    html = html.replace(old_card2, new_card2)
    print('✅ Updated Card 2 with i18n anchors')
else:
    print('⚠️ old_card2 not found directly')

# 2. Fix Card 4 Tag
old_card4_tag = '<span class="text-[10px] bg-cyan-500/10 text-cyan-300 px-2 py-0.5 rounded font-mono">LIVE</span>'
new_card4_tag = '<span class="text-[10px] bg-cyan-500/10 text-cyan-300 px-2 py-0.5 rounded font-mono" id="metric-inspection-tag">LIVE</span>'
if old_card4_tag in html:
    html = html.replace(old_card4_tag, new_card4_tag)
    print('✅ Updated Card 4 Tag anchor')

# 3. Fix Drawer titles
old_patch_check = '<span>🔍 补丁变动与最新版本核验</span>'
new_patch_check = '<span id="drawer-patch-check-title">🔍 补丁变动与最新版本核验</span>'
if old_patch_check in html:
    html = html.replace(old_patch_check, new_patch_check)
    print('✅ Updated drawer-patch-check-title anchor')

old_matrix_tag = '<span class="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-mono font-bold">小红书/B站对齐</span>'
new_matrix_tag = '<span class="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-mono font-bold" id="drawer-matrix-tag">社交媒体矩阵</span>'
if old_matrix_tag in html:
    html = html.replace(old_matrix_tag, new_matrix_tag)
    print('✅ Updated drawer-matrix-tag anchor')

# 4. Fix Image modal download button
old_img_dl = '下载 1080×1440 原图</a>'
new_img_dl = '<span id="image-modal-download-text">下载 1080×1440 原图</span></a>'
if old_img_dl in html:
    html = html.replace(old_img_dl, new_img_dl)
    print('✅ Updated image-modal-download-text anchor')

with open(RADAR_PATH, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML anchors fixed in radar.html')
