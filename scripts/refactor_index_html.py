#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/refactor_index_html.py
Comprehensive i18n Refactoring for public/index.html
"""

import os
import re

INDEX_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Sidebar Nav Items with IDs
html = html.replace(
    '<span>探索全部 100 款游戏</span>',
    '<span id="sidebar-explore-label">探索全部 100 款游戏</span>'
)
html = html.replace(
    '<span>全部 100 款神作排行</span>',
    '<span id="sidebar-nav-all">全部 100 款神作排行</span>'
)
html = html.replace(
    '<span class="font-bold text-amber-500 dark:text-amber-400">老L全息精测认证 (前14款)</span>',
    '<span id="sidebar-nav-certified" class="font-bold text-amber-500 dark:text-amber-400">老L全息精测认证 (前14款)</span>'
)
html = html.replace(
    '<span>持续排雷采掘中 (后续单机)</span>',
    '<span id="sidebar-nav-mining">持续排雷采掘中 (后续单机)</span>'
)
html = html.replace(
    '<span>官方控制台作弊代码</span>',
    '<span id="sidebar-nav-console">官方控制台作弊代码</span>'
)
html = html.replace(
    '<span>N网爆款 MOD 与补丁</span>',
    '<span id="sidebar-nav-mods">N网爆款 MOD 与补丁</span>'
)
html = html.replace(
    '<span>纯净修改器 (Verified Clean)</span>',
    '<span id="sidebar-nav-trainers">纯净修改器 (Verified Clean)</span>'
)
html = html.replace(
    '<span class="font-bold text-amber-500 dark:text-amber-400">Steam 避坑实时雷达</span>',
    '<span id="sidebar-nav-radar" class="font-bold text-amber-500 dark:text-amber-400">Steam 避坑实时雷达</span>'
)
html = html.replace(
    '<div class="px-3 text-zinc-400 dark:text-zinc-500 font-semibold tracking-wider uppercase text-[10px]">\n          最近浏览历史\n        </div>',
    '<div class="px-3 text-zinc-400 dark:text-zinc-500 font-semibold tracking-wider uppercase text-[10px]" id="sidebar-recents-label">\n          最近浏览历史\n        </div>'
)

# 2. Update Ticker bar & Header Breadcrumb
html = html.replace(
    '<span>Steam 补丁避坑紧急广播</span>',
    '<span id="broadcast-bar-title">Steam 补丁避坑紧急广播</span>'
)
html = html.replace(
    '<span>进入避坑雷达看板</span>',
    '<span id="broadcast-bar-btn">进入避坑雷达看板</span>'
)
html = html.replace(
    '<span class="tracking-tight">📡 避坑雷达</span>',
    '<span class="tracking-tight" id="header-radar-btn-text">📡 避坑雷达</span>'
)
html = html.replace(
    '<span class="hidden sm:inline">画廊</span>',
    '<span class="hidden sm:inline" id="view-mode-gallery-text">画廊</span>'
)
html = html.replace(
    '<span class="hidden sm:inline">极简</span>',
    '<span class="hidden sm:inline" id="view-mode-list-text">极简</span>'
)
html = html.replace(
    '<span class="text-zinc-400 font-medium shrink-0 pl-1">快速检索：</span>',
    '<span class="text-zinc-400 font-medium shrink-0 pl-1" id="quick-search-label">快速检索：</span>'
)

# 3. Update Detail view static labels
html = html.replace(
    '<span>返回全部游戏库</span>',
    '<span id="detail-back-text">返回全部游戏库</span>'
)
html = html.replace(
    '<span>老L·单机避坑局认证</span>',
    '<span id="detail-cert-text">老L·单机避坑局认证</span>'
)
html = html.replace(
    '<span>🚫 拒绝流氓木马 · 官方底层机制</span>',
    '<span id="detail-clean-guarantee">🚫 拒绝流氓木马 · 官方底层机制</span>'
)
html = html.replace(
    '<div class="text-[10px] text-zinc-400 font-medium">N网总下载</div>',
    '<div class="text-[10px] text-zinc-400 font-medium" id="stat-label-downloads">N网总下载</div>'
)
html = html.replace(
    '<div class="text-[10px] text-zinc-400 font-medium">玩家推荐</div>',
    '<div class="text-[10px] text-zinc-400 font-medium" id="stat-label-endorsements">玩家推荐</div>'
)
html = html.replace(
    '<div class="text-[10px] text-zinc-400 font-medium">精选模组</div>',
    '<div class="text-[10px] text-zinc-400 font-medium" id="stat-label-mods">精选模组</div>'
)
html = html.replace(
    '🎮 官方控制台与代码',
    '<span id="tab-text-console">🎮 官方控制台与代码</span>'
)
html = html.replace(
    '📦 N网精选 MOD 库',
    '<span id="tab-text-mods">📦 N网精选 MOD 库</span>'
)
html = html.replace(
    '⚡ 纯净修改器与热键',
    '<span id="tab-text-trainers">⚡ 纯净修改器与热键</span>'
)
html = html.replace(
    '💬 玩家讨论与排错',
    '<span id="tab-text-reviews">💬 玩家讨论与排错</span>'
)
html = html.replace(
    '<span>官方 5 联高清卡片 (1080×1440)</span>',
    '<span id="tab-text-social-cards">官方 5 联高清卡片 (1080×1440)</span>'
)
html = html.replace(
    '<span>控制台开启手把手教学 (官方原生 · 无封号风险)</span>',
    '<span id="detail-console-guide-title">控制台开启手把手教学 (官方原生 · 无封号风险)</span>'
)
html = html.replace(
    '<span>🚀 懒人双击一键开门 (生成 .bat)</span>',
    '<span id="detail-btn-lazy-door">🚀 懒人双击一键开门 (生成 .bat)</span>'
)
html = html.replace(
    '<span class="text-[11px] text-zinc-400">呼出键:</span>',
    '<span class="text-[11px] text-zinc-400" id="detail-shortcut-label">呼出键:</span>'
)
html = html.replace(
    '<h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white">常用快捷指令 (点击一键复制)</h3>',
    '<h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white" id="detail-popular-cmd-title">常用快捷指令 (点击一键复制)</h3>'
)
html = html.replace(
    '<span class="text-zinc-400 font-medium">MOD 安装目录:</span>',
    '<span class="text-zinc-400 font-medium" id="detail-mod-path-title">MOD 安装目录:</span>'
)
html = html.replace(
    '<h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white">精选必备社区 MOD</h3>',
    '<h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white" id="detail-musthave-mods-title">精选必备社区 MOD</h3>'
)
html = html.replace(
    '<h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white">纯净修改器与热键一览</h3>',
    '<h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white" id="detail-trainer-title">纯净修改器与热键一览</h3>'
)

# Trainer section in Detail View
html = html.replace(
    '<h4 class="font-extrabold text-sm sm:text-base text-zinc-900 dark:text-white flex items-center gap-1.5">\n                  风灵月影 (FLiNG) 官方直连\n                </h4>',
    '<h4 class="font-extrabold text-sm sm:text-base text-zinc-900 dark:text-white flex items-center gap-1.5" id="trainer-sec-title">\n                  风灵月影 (FLiNG) 官方直连\n                </h4>'
)
html = html.replace(
    '<div class="font-bold text-xs text-zinc-800 dark:text-zinc-200">纯净单文件修改器 · 告别流氓捆绑</div>',
    '<div class="font-bold text-xs text-zinc-800 dark:text-zinc-200" id="trainer-sec-sub">纯净单文件修改器 · 告别流氓捆绑</div>'
)
html = html.replace(
    '<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">本站坚决抵制任何第三方恶意全家桶下载器与弹窗推广！提供原作者官方直源与经过 MD5 校验的纯净单文件。</p>',
    '<p class="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed" id="trainer-sec-desc">本站坚决抵制任何第三方恶意全家桶下载器与弹窗推广！提供原作者官方直源与经过 MD5 校验的纯净单文件。</p>'
)
html = html.replace(
    '<span>⚡ 极速纯净一键直接下载 (ZIP)</span>',
    '<span id="trainer-btn-direct-dl">⚡ 极速纯净一键直接下载 (ZIP)</span>'
)
html = html.replace(
    '<span>风灵月影官方页面 (备用通道)</span>',
    '<span id="trainer-btn-official-page">风灵月影官方页面 (备用通道)</span>'
)
html = html.replace(
    '<div class="font-bold text-amber-800 dark:text-amber-300 text-xs sm:text-sm">防杀毒软件误报拦截 · 10 秒放行指南 (Windows Defender)</div>',
    '<div class="font-bold text-amber-800 dark:text-amber-300 text-xs sm:text-sm" id="trainer-def-title">防杀毒软件误报拦截 · 10 秒放行指南 (Windows Defender)</div>'
)
html = html.replace(
    '<p class="text-amber-700/80 dark:text-amber-400/80 leading-relaxed text-[11px] sm:text-xs">修改器通过系统内存注入数值，所有主流杀毒软件均会触发特征误报（显示为 HackTool:Win32/GameHack），这属于游戏内存修改的通用机制，绝非病毒。</p>',
    '<p class="text-amber-700/80 dark:text-amber-400/80 leading-relaxed text-[11px] sm:text-xs" id="trainer-def-desc">修改器通过系统内存注入数值，所有主流杀毒软件均会触发特征误报（显示为 HackTool:Win32/GameHack），这属于游戏内存修改的通用机制，绝非病毒。</p>'
)
html = html.replace(
    '<div>1. 打开【Windows 安全中心】 -> 点击【病毒和威胁防护】 -> 【管理设置】</div>',
    '<div id="trainer-def-step1">1. 打开【Windows 安全中心】 -> 点击【病毒和威胁防护】 -> 【管理设置】</div>'
)
html = html.replace(
    '<div>2. 向下滑动找到【排除项】 -> 点击【添加或删除排除项】</div>',
    '<div id="trainer-def-step2">2. 向下滑动找到【排除项】 -> 点击【添加或删除排除项】</div>'
)
html = html.replace(
    '<div>3. 添加文件夹 -> 选择你存放修改器的目录，即可一劳永逸正常运行不被误杀！</div>',
    '<div id="trainer-def-step3">3. 添加文件夹 -> 选择你存放修改器的目录，即可一劳永逸正常运行不被误杀！</div>'
)
html = html.replace(
    '<span class="font-mono text-[11px] text-zinc-500 dark:text-zinc-400">PowerShell 一键放行指令:</span>',
    '<span class="font-mono text-[11px] text-zinc-500 dark:text-zinc-400" id="trainer-def-cmd-label">PowerShell 一键放行指令:</span>'
)
html = html.replace(
    '<span>复制一键放行命令</span>',
    '<span id="trainer-btn-copy-def">复制一键放行命令</span>'
)

# 4. Update Lazy Door Modal Elements
html = html.replace(
    '<h3 class="text-lg sm:text-xl font-extrabold text-zinc-900 dark:text-white">10秒懒人开门 · 游戏控制台一键激活器</h3>',
    '<h3 class="text-lg sm:text-xl font-extrabold text-zinc-900 dark:text-white" id="lazy-modal-title">10秒懒人开门 · 游戏控制台一键激活器</h3>'
)
html = html.replace(
    '<span class="text-[10px] bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-0.5 rounded-full font-bold border border-emerald-500/20">100% 开源纯批处理</span>',
    '<span class="text-[10px] bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-0.5 rounded-full font-bold border border-emerald-500/20" id="lazy-modal-tag">100% 开源纯批处理</span>'
)
html = html.replace(
    '<span>老L承诺：100% 原生纯净 · 自动备份原文件 (.bak) · 绝无木马捆绑</span>',
    '<span id="lazy-safe-title">老L承诺：100% 原生纯净 · 自动备份原文件 (.bak) · 绝无木马捆绑</span>'
)
html = html.replace(
    '<p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-[11px] sm:text-xs">\n          本脚本为标准 Windows 批处理源码，仅修改游戏官方原生配置文件或预设快捷键，运行时自动生成 <code>.bak</code> 备份文件。代码完全公开透明，可用记事本随时查验，绝不写入任何未知可执行文件！\n        </p>',
    '<p class="text-zinc-600 dark:text-zinc-400 leading-relaxed text-[11px] sm:text-xs" id="lazy-safe-desc">\n          本脚本为标准 Windows 批处理源码，仅修改游戏官方原生配置文件或预设快捷键，运行时自动生成 <code>.bak</code> 备份文件。代码完全公开透明，可用记事本随时查验，绝不写入任何未知可执行文件！\n        </p>'
)
html = html.replace(
    '<div class="font-bold text-zinc-800 dark:text-zinc-200">极简 3 步使用指引：</div>',
    '<div class="font-bold text-zinc-800 dark:text-zinc-200" id="lazy-steps-title">极简 3 步使用指引：</div>'
)
html = html.replace(
    '<span>点击下方【下载 .bat 脚本】将文件保存（或复制代码存为 <code>一键开门.bat</code>）；</span>',
    '<span id="lazy-step-1">点击下方【下载 .bat 脚本】将文件保存（或复制代码存为 <code>一键开门.bat</code>）；</span>'
)
html = html.replace(
    '<span>将 <code>.bat</code> 放置在该游戏安装根目录，双击运行（脚本自动备份并注入配置）；</span>',
    '<span id="lazy-step-2">将 <code>.bat</code> 放置在该游戏安装根目录，双击运行（脚本自动备份并注入配置）；</span>'
)
html = html.replace(
    '<span>启动游戏，按快捷键呼出控制台，直接粘贴老L推荐套餐即可爽玩！</span>',
    '<span id="lazy-step-3">启动游戏，按快捷键呼出控制台，直接粘贴老L推荐套餐即可爽玩！</span>'
)
html = html.replace(
    '已自动适配当前游戏：<span id="lazy-modal-game-name"',
    '<span id="lazy-adapted-label">已自动适配当前游戏：</span><span id="lazy-modal-game-name"'
)
html = html.replace(
    '<span>复制代码</span>\n        </button>\n        <button onclick="downloadBatScript()"',
    '<span id="lazy-btn-copy">复制代码</span>\n        </button>\n        <button onclick="downloadBatScript()"'
)
html = html.replace(
    '<span>下载 .bat 脚本</span>\n        </button>\n        <button onclick="closeLazyDoorModal()"',
    '<span id="lazy-btn-download">下载 .bat 脚本</span>\n        </button>\n        <button onclick="closeLazyDoorModal()"'
)
html = html.replace(
    '<button onclick="closeLazyDoorModal()" class="w-full sm:w-auto px-5 py-2.5 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-bold transition-all shadow-sm cursor-pointer">\n          我知道了\n        </button>',
    '<button onclick="closeLazyDoorModal()" id="lazy-btn-close" class="w-full sm:w-auto px-5 py-2.5 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-bold transition-all shadow-sm cursor-pointer">\n          我知道了\n        </button>'
)

# 5. Trainer Download Modal
html = html.replace(
    '<span class="text-[10px] bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-0.5 rounded-full font-bold border border-emerald-500/20">纯净单文件</span>',
    '<span class="text-[10px] bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-0.5 rounded-full font-bold border border-emerald-500/20" id="trainer-modal-clean-tag">纯净单文件</span>'
)
html = html.replace(
    '<p class="text-xs text-zinc-500 dark:text-zinc-400 mt-1">若浏览器弹出下载确认，请点击【保留 / 允许下载】· 零捆绑 · 零广告</p>',
    '<p class="text-xs text-zinc-500 dark:text-zinc-400 mt-1" id="trainer-modal-subtitle">若浏览器弹出下载确认，请点击【保留 / 允许下载】· 零捆绑 · 零广告</p>'
)
html = html.replace(
    '<span class="font-bold text-amber-800 dark:text-amber-300 text-xs sm:text-sm">附赠：Windows Defender 10秒一键放行指令</span>',
    '<span class="font-bold text-amber-800 dark:text-amber-300 text-xs sm:text-sm" id="trainer-ex-title">附赠：Windows Defender 10秒一键放行指令</span>'
)
html = html.replace(
    '<p class="text-amber-700/80 dark:text-amber-400/80 leading-relaxed text-[11px] sm:text-xs">\n            修改器修改游戏内存会触发杀软特征误报 (HackTool:Win32)。以管理员权限运行 PowerShell 贴入下方指令，即可 10 秒彻底放行：\n          </p>',
    '<p class="text-amber-700/80 dark:text-amber-400/80 leading-relaxed text-[11px] sm:text-xs" id="trainer-ex-desc">\n            修改器修改游戏内存会触发杀软特征误报 (HackTool:Win32)。以管理员权限运行 PowerShell 贴入下方指令，即可 10 秒彻底放行：\n          </p>'
)
html = html.replace(
    '<span class="font-mono text-[11px] text-zinc-500 dark:text-zinc-400">推荐放行命令 (PowerShell):</span>',
    '<span class="font-mono text-[11px] text-zinc-500 dark:text-zinc-400" id="trainer-ex-cmd-label">推荐放行命令 (PowerShell):</span>'
)
html = html.replace(
    '<span>一键复制指令</span>',
    '<span id="trainer-btn-copy-cmd">一键复制指令</span>'
)
html = html.replace(
    '<div class="text-xs font-bold text-zinc-800 dark:text-zinc-200">双通道下载保障：</div>',
    '<div class="text-xs font-bold text-zinc-800 dark:text-zinc-200" id="trainer-dual-label">双通道下载保障：</div>'
)
html = html.replace(
    '<span>重新拉起直接下载 (ZIP)</span>',
    '<span id="trainer-btn-retrigger">重新拉起直接下载 (ZIP)</span>'
)
html = html.replace(
    '<span>直达风灵月影官方页面 (备用)</span>',
    '<span id="trainer-btn-backup">直达风灵月影官方页面 (备用)</span>'
)
html = html.replace(
    '<span>极简 3 步：保持单机离线 -> 运行放行指令 -> 解压启动即享</span>',
    '<span id="trainer-3step-hint">极简 3 步：保持单机离线 -> 运行放行指令 -> 解压启动即享</span>'
)
html = html.replace(
    '<button onclick="closeTrainerModal()" class="w-full sm:w-auto px-5 py-2.5 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-bold transition-all shadow-sm cursor-pointer">\n          我知道了\n        </button>',
    '<button onclick="closeTrainerModal()" id="trainer-btn-close" class="w-full sm:w-auto px-5 py-2.5 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-bold transition-all shadow-sm cursor-pointer">\n          我知道了\n        </button>'
)

# 6. Mod Download Modal
html = html.replace(
    '<span class="text-zinc-500 dark:text-zinc-400">下载目标文件:</span>',
    '<span class="text-zinc-500 dark:text-zinc-400" id="mod-modal-label-file">下载目标文件:</span>'
)
html = html.replace(
    '<span class="text-zinc-500 dark:text-zinc-400">建议安装路径:</span>',
    '<span class="text-zinc-500 dark:text-zinc-400" id="mod-modal-label-path">建议安装路径:</span>'
)
html = html.replace(
    '<button onclick="copyModInstallPath()" class="text-blue-600 hover:underline text-[11px] shrink-0 font-sans">复制路径</button>',
    '<button onclick="copyModInstallPath()" id="mod-modal-btn-copy-path" class="text-blue-600 hover:underline text-[11px] shrink-0 font-sans">复制路径</button>'
)
html = html.replace(
    '<span>🛠️ 老L傻瓜式安装指引：</span>',
    '<span id="mod-modal-steps-title">🛠️ 老L傻瓜式安装指引：</span>'
)
html = html.replace(
    '<span>重新拉起下载</span>\n        </button>\n        <div class="flex items-center gap-2 w-full sm:w-auto">\n          <a id="mod-modal-nexus-link"',
    '<span id="mod-modal-btn-retrigger">重新拉起下载</span>\n        </button>\n        <div class="flex items-center gap-2 w-full sm:w-auto">\n          <a id="mod-modal-nexus-link"'
)
html = html.replace(
    '<span>访问 Nexus 原页</span>',
    '<span id="mod-modal-btn-nexus">访问 Nexus 原页</span>'
)
html = html.replace(
    '<button onclick="closeModModal()" class="flex-1 sm:flex-none px-5 py-2.5 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-bold transition-all shadow-sm cursor-pointer">\n            我知道了\n          </button>',
    '<button onclick="closeModModal()" id="mod-modal-btn-close" class="flex-1 sm:flex-none px-5 py-2.5 rounded-full bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 text-xs font-bold transition-all shadow-sm cursor-pointer">\n            我知道了\n          </button>'
)
html = html.replace(
    '下载 1080×1440 原图</a>',
    '<span id="image-modal-dl-text">下载 1080×1440 原图</span></a>'
)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Updated public/index.html HTML elements with dynamic i18n anchors.")
