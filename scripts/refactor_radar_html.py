#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/refactor_radar_html.py
Comprehensive i18n Refactoring for public/radar.html
"""

RADAR_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/radar.html"

with open(RADAR_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Top Ticker Banner
html = html.replace(
    '<span>紧急巡检广播</span>',
    '<span id="ticker-badge-text">紧急巡检广播</span>'
)
html = html.replace(
    '<span class="hidden sm:inline">返回</span><span>主库</span>',
    '<span id="ticker-back-text">返回 L-MOD 主库</span>'
)

# 2. Update Header Brand
html = html.replace(
    '<span>Steam 补丁变动与 Mod 兼容性实时雷达</span>',
    '<span id="radar-header-title">Steam 补丁变动与 Mod 兼容性实时雷达</span>'
)
html = html.replace(
    '<span class="bg-blue-500/20 text-blue-400 text-[10px] font-mono px-2 py-0.5 rounded-full border border-blue-500/30 font-bold uppercase tracking-wider">v4.0 独立看板</span>',
    '<span class="bg-blue-500/20 text-blue-400 text-[10px] font-mono px-2 py-0.5 rounded-full border border-blue-500/30 font-bold uppercase tracking-wider" id="radar-header-version">v4.0 独立看板</span>'
)
html = html.replace(
    '<span>由 L-MOD Vault 避坑实验室驱动</span>',
    '<span id="radar-header-powered">由 L-MOD Vault 避坑实验室驱动</span>'
)
html = html.replace(
    '<span>24h 智能对齐巡检进行中</span>',
    '<span id="radar-header-live">24h 智能对齐巡检进行中</span>'
)
html = html.replace(
    '<span>进避坑互助群暗号:</span>',
    '<span id="radar-group-code-label">进避坑互助群暗号:</span>'
)
html = html.replace(
    '<span>返回 L-MOD 主库</span>\n        </a>',
    '<span id="radar-return-btn-text">返回 L-MOD 主库</span>\n        </a>'
)

# Inject Language Dropdown right before the "Return to Main Vault" button
old_return_btn = """        <a href="index.html" class="flex items-center space-x-2 bg-white/5 hover:bg-white/10 text-zinc-200 border border-white/10 px-3.5 py-2 rounded-xl text-xs font-semibold transition-all">
          <svg class="w-4 h-4 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>
          <span id="radar-return-btn-text">返回 L-MOD 主库</span>
        </a>"""

lang_dropdown_html = """        <!-- Custom Language Dropdown for Radar -->
        <div class="relative" id="custom-lang-dropdown">
          <button 
            onclick="toggleLangDropdown(event)" 
            class="flex items-center space-x-1.5 px-3 py-2 rounded-xl text-xs font-semibold bg-white/5 hover:bg-white/10 text-zinc-200 border border-white/10 transition-colors cursor-pointer"
            id="lang-trigger-btn"
          >
            <span id="current-lang-flag">🇨🇳</span>
            <span id="current-lang-name">简体中文</span>
            <svg class="w-3.5 h-3.5 text-zinc-400 transition-transform duration-200" id="lang-chevron" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
          </button>

          <div 
            id="lang-menu" 
            class="hidden absolute right-0 mt-2 w-48 bg-[#12141a] rounded-2xl shadow-2xl border border-white/10 p-1.5 z-50 text-xs backdrop-blur-xl animate-in fade-in zoom-in-95 duration-100"
          >
            <div class="px-3 py-1.5 text-[10px] text-zinc-400 font-bold border-b border-white/5 mb-1" id="lang-menu-title">
              选择语言 · Select Language
            </div>
            <div class="space-y-0.5">
              <button onclick="selectLanguage('zh-CN', '🇨🇳', '简体中文')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="zh-CN">
                <span class="flex items-center space-x-2"><span>🇨🇳</span><span>简体中文</span></span>
                <span class="lang-check text-blue-400 font-bold">✓</span>
              </button>
              <button onclick="selectLanguage('en', '🇺🇸', 'English')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="en">
                <span class="flex items-center space-x-2"><span>🇺🇸</span><span>English</span></span>
                <span class="lang-check hidden text-blue-400 font-bold">✓</span>
              </button>
              <button onclick="selectLanguage('zh-TW', '🇭🇰', '繁體中文')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="zh-TW">
                <span class="flex items-center space-x-2"><span>🇭🇰</span><span>繁體中文</span></span>
                <span class="lang-check hidden text-blue-400 font-bold">✓</span>
              </button>
              <button onclick="selectLanguage('ja', '🇯🇵', '日本語')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="ja">
                <span class="flex items-center space-x-2"><span>🇯🇵</span><span>日本語</span></span>
                <span class="lang-check hidden text-blue-400 font-bold">✓</span>
              </button>
              <button onclick="selectLanguage('ko', '🇰🇷', '한국어')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="ko">
                <span class="flex items-center space-x-2"><span>🇰🇷</span><span>한국어</span></span>
                <span class="lang-check hidden text-blue-400 font-bold">✓</span>
              </button>
              <button onclick="selectLanguage('ru', '🇷🇺', 'Русский')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="ru">
                <span class="flex items-center space-x-2"><span>🇷🇺</span><span>Русский</span></span>
                <span class="lang-check hidden text-blue-400 font-bold">✓</span>
              </button>
              <button onclick="selectLanguage('de', '🇩🇪', 'Deutsch')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="de">
                <span class="flex items-center space-x-2"><span>🇩🇪</span><span>Deutsch</span></span>
                <span class="lang-check hidden text-blue-400 font-bold">✓</span>
              </button>
              <button onclick="selectLanguage('es', '🇪🇸', 'Español')" class="lang-option w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-white/10 transition-colors text-zinc-200" data-lang="es">
                <span class="flex items-center space-x-2"><span>🇪🇸</span><span>Español</span></span>
                <span class="lang-check hidden text-blue-400 font-bold">✓</span>
              </button>
            </div>
          </div>
        </div>

""" + old_return_btn

if old_return_btn in html:
    html = html.replace(old_return_btn, lang_dropdown_html)
    print("✅ Injected custom language dropdown into radar.html header")
else:
    print("⚠️ Could not find old_return_btn in radar.html")

# 3. Update Metric Cards
html = html.replace(
    '<span>完美兼容 · 实测通过</span>',
    '<span id="metric-green-title">完美兼容 · 实测通过</span>'
)
html = html.replace(
    '<span class="text-[10px] bg-emerald-500/10 text-emerald-300 px-2 py-0.5 rounded font-mono">稳定运行</span>',
    '<span class="text-[10px] bg-emerald-500/10 text-emerald-300 px-2 py-0.5 rounded font-mono" id="metric-green-tag">稳定运行</span>'
)
html = html.replace(
    '<span class="text-xs text-zinc-400">款 3A 大作</span>',
    '<span class="text-xs text-zinc-400" id="metric-green-unit">款 3A 大作</span>'
)
html = html.replace(
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1">最新补丁实机测试，控制台与前置 100% 畅玩</p>',
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1" id="metric-green-desc">最新补丁实机测试，控制台与前置 100% 畅玩</p>'
)

html = html.replace(
    '<span>需更新前置 / 需补丁适配</span>',
    '<span id="metric-yellow-title">需更新前置 / 需补丁适配</span>'
)
html = html.replace(
    '<span class="text-[10px] bg-amber-500/10 text-amber-300 px-2 py-0.5 rounded font-mono">注意排查</span>',
    '<span class="text-[10px] bg-amber-500/10 text-amber-300 px-2 py-0.5 rounded font-mono" id="metric-yellow-tag">注意排查</span>'
)
html = html.replace(
    '<span class="text-xs text-zinc-400">款需更新前置</span>',
    '<span class="text-xs text-zinc-400" id="metric-yellow-unit">款需更新前置</span>'
)
html = html.replace(
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1">游戏小更新破坏前置DLL，需更新对应框架后启动</p>',
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1" id="metric-yellow-desc">游戏小更新破坏前置DLL，需更新对应框架后启动</p>'
)

html = html.replace(
    '<span>恶性坏档 · 暂停更新</span>',
    '<span id="metric-red-title">恶性坏档 · 暂停更新</span>'
)
html = html.replace(
    '<span class="text-[10px] bg-red-500/10 text-red-300 px-2 py-0.5 rounded font-mono">紧急预警</span>',
    '<span class="text-[10px] bg-red-500/10 text-red-300 px-2 py-0.5 rounded font-mono" id="metric-red-tag">紧急预警</span>'
)
html = html.replace(
    '<span class="text-xs text-zinc-400">款高危预警</span>',
    '<span class="text-xs text-zinc-400" id="metric-red-unit">款高危预警</span>'
)
html = html.replace(
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1">次世代破坏老Mod架构，请务必锁定 Steam 自动更新</p>',
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1" id="metric-red-desc">次世代破坏老Mod架构，请务必锁定 Steam 自动更新</p>'
)

html = html.replace(
    '<span>巡检哨兵机制</span>',
    '<span id="metric-inspection-title">巡检哨兵机制</span>'
)
html = html.replace(
    '<span class="text-xs text-zinc-400">款全球神作全覆盖</span>',
    '<span class="text-xs text-zinc-400" id="metric-inspection-unit">款全球神作全覆盖</span>'
)
html = html.replace(
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1">每日对比 Steam AppUpdate 差量，发现坏档连夜同步</p>',
    '<p class="text-[11px] text-zinc-400 mt-1 line-clamp-1" id="metric-inspection-desc">每日对比 Steam AppUpdate 差量，发现坏档连夜同步</p>'
)

# 4. Search and Filters
html = html.replace(
    '<span class="text-xs text-zinc-400 whitespace-nowrap hidden sm:inline">排序方式:</span>',
    '<span class="text-xs text-zinc-400 whitespace-nowrap hidden sm:inline" id="radar-sort-label">排序方式:</span>'
)
html = html.replace(
    '<option value="risk-desc">⚠️ 风险优先 (坏档/需前置置顶)</option>',
    '<option value="risk-desc" id="opt-risk-desc">⚠️ 风险优先 (坏档/需前置置顶)</option>'
)
html = html.replace(
    '<option value="rank-asc">👑 游戏排名 (Rank 1 ~ 100)</option>',
    '<option value="rank-asc" id="opt-rank-asc">👑 游戏排名 (Rank 1 ~ 100)</option>'
)
html = html.replace(
    '<option value="compatible-first">🟢 稳定优先 (已实测完美)</option>',
    '<option value="compatible-first" id="opt-compat-first">🟢 稳定优先 (已实测完美)</option>'
)
html = html.replace(
    '<option value="name-asc">🔤 游戏名称 (A-Z)</option>',
    '<option value="name-asc" id="opt-name-asc">🔤 游戏名称 (A-Z)</option>'
)

html = html.replace(
    '<span class="text-xs text-zinc-400 mr-1 font-medium">兼容状态:</span>',
    '<span class="text-xs text-zinc-400 mr-1 font-medium" id="radar-filter-status-label">兼容状态:</span>'
)
html = html.replace(
    '<button onclick="setStatusFilter(\'all\')" class="status-pill active px-3 py-1 rounded-full text-xs font-medium bg-blue-600 text-white transition-all cursor-pointer" data-status="all">全部</button>',
    '<button onclick="setStatusFilter(\'all\')" class="status-pill active px-3 py-1 rounded-full text-xs font-medium bg-blue-600 text-white transition-all cursor-pointer" data-status="all" id="pill-status-all">全部</button>'
)
html = html.replace(
    '<button onclick="setStatusFilter(\'green\')" class="status-pill px-3 py-1 rounded-full text-xs font-medium bg-white/5 text-emerald-400 hover:bg-emerald-500/10 border border-emerald-500/20 transition-all cursor-pointer" data-status="green">🟢 完美兼容</button>',
    '<button onclick="setStatusFilter(\'green\')" class="status-pill px-3 py-1 rounded-full text-xs font-medium bg-white/5 text-emerald-400 hover:bg-emerald-500/10 border border-emerald-500/20 transition-all cursor-pointer" data-status="green" id="pill-status-green">🟢 完美兼容</button>'
)
html = html.replace(
    '<button onclick="setStatusFilter(\'yellow\')" class="status-pill px-3 py-1 rounded-full text-xs font-medium bg-white/5 text-amber-400 hover:bg-amber-500/10 border border-amber-500/20 transition-all cursor-pointer" data-status="yellow">🟡 需更前置</button>',
    '<button onclick="setStatusFilter(\'yellow\')" class="status-pill px-3 py-1 rounded-full text-xs font-medium bg-white/5 text-amber-400 hover:bg-amber-500/10 border border-amber-500/20 transition-all cursor-pointer" data-status="yellow" id="pill-status-yellow">🟡 需更前置</button>'
)
html = html.replace(
    '<button onclick="setStatusFilter(\'red\')" class="status-pill px-3 py-1 rounded-full text-xs font-medium bg-white/5 text-red-400 hover:bg-red-500/10 border border-red-500/20 transition-all cursor-pointer" data-status="red">🔴 暂停更新</button>',
    '<button onclick="setStatusFilter(\'red\')" class="status-pill px-3 py-1 rounded-full text-xs font-medium bg-white/5 text-red-400 hover:bg-red-500/10 border border-red-500/20 transition-all cursor-pointer" data-status="red" id="pill-status-red">🔴 暂停更新</button>'
)

html = html.replace(
    '<span class="text-xs text-zinc-400 mr-1 font-medium">专区/引擎:</span>',
    '<span class="text-xs text-zinc-400 mr-1 font-medium" id="radar-filter-engine-label">专区/引擎:</span>'
)
html = html.replace(
    '<button onclick="setEngineFilter(\'all\')" class="engine-pill active px-2.5 py-1 rounded-full text-xs bg-white/10 text-white cursor-pointer" data-engine="all">全部</button>',
    '<button onclick="setEngineFilter(\'all\')" class="engine-pill active px-2.5 py-1 rounded-full text-xs bg-white/10 text-white cursor-pointer" data-engine="all" id="pill-engine-all">全部</button>'
)
html = html.replace(
    '<button onclick="setEngineFilter(\'flagship\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-purple-300 hover:bg-purple-500/20 border border-purple-500/30 cursor-pointer" data-engine="flagship">👑 Top 7 旗舰深度</button>',
    '<button onclick="setEngineFilter(\'flagship\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-purple-300 hover:bg-purple-500/20 border border-purple-500/30 cursor-pointer" data-engine="flagship" id="pill-engine-flagship">👑 Top 7 旗舰深度</button>'
)
html = html.replace(
    '<button onclick="setEngineFilter(\'Unreal\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-zinc-300 hover:bg-white/10 cursor-pointer" data-engine="Unreal">虚幻引擎</button>',
    '<button onclick="setEngineFilter(\'Unreal\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-zinc-300 hover:bg-white/10 cursor-pointer" data-engine="Unreal" id="pill-engine-unreal">虚幻引擎</button>'
)
html = html.replace(
    '<button onclick="setEngineFilter(\'Creation\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-zinc-300 hover:bg-white/10 cursor-pointer" data-engine="Creation">B社引擎</button>',
    '<button onclick="setEngineFilter(\'Creation\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-zinc-300 hover:bg-white/10 cursor-pointer" data-engine="Creation" id="pill-engine-creation">B社引擎</button>'
)
html = html.replace(
    '<button onclick="setEngineFilter(\'FromSoft\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-zinc-300 hover:bg-white/10 cursor-pointer" data-engine="FromSoft">魂系引擎</button>',
    '<button onclick="setEngineFilter(\'FromSoft\')" class="engine-pill px-2.5 py-1 rounded-full text-xs bg-white/5 text-zinc-300 hover:bg-white/10 cursor-pointer" data-engine="FromSoft" id="pill-engine-fromsoft">魂系引擎</button>'
)

# 5. Legend and Empty State
html = html.replace(
    '<span>共匹配到 <strong class="text-white font-mono" id="results-count">0</strong> 款游戏</span>',
    '<span><span id="radar-count-matched">共匹配到</span> <strong class="text-white font-mono" id="results-count">0</strong> <span id="radar-count-unit">款游戏</span></span>'
)
html = html.replace(
    '<span class="inline-block w-2 h-2 rounded-full bg-emerald-500"></span><span>完美</span>',
    '<span class="inline-block w-2 h-2 rounded-full bg-emerald-500"></span><span id="legend-text-compat">完美</span>'
)
html = html.replace(
    '<span class="inline-block w-2 h-2 rounded-full bg-amber-500 ml-2"></span><span>前置</span>',
    '<span class="inline-block w-2 h-2 rounded-full bg-amber-500 ml-2"></span><span id="legend-text-warn">前置</span>'
)
html = html.replace(
    '<span class="inline-block w-2 h-2 rounded-full bg-red-500 ml-2"></span><span>坏档/暂停</span>',
    '<span class="inline-block w-2 h-2 rounded-full bg-red-500 ml-2"></span><span id="legend-text-broken">坏档/暂停</span>'
)

html = html.replace(
    '<h3 class="text-base font-bold text-zinc-300">未找到符合条件的游戏</h3>',
    '<h3 class="text-base font-bold text-zinc-300" id="radar-empty-title">未找到符合条件的游戏</h3>'
)
html = html.replace(
    '<p class="text-xs text-zinc-500 max-w-sm mx-auto">请尝试更换搜索关键字，或重置状态与引擎筛选条件。</p>',
    '<p class="text-xs text-zinc-500 max-w-sm mx-auto" id="radar-empty-desc">请尝试更换搜索关键字，或重置状态与引擎筛选条件。</p>'
)
html = html.replace(
    '<button onclick="resetAllFilters()" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold">\n        重置全部筛选\n      </button>',
    '<button onclick="resetAllFilters()" id="radar-empty-reset-btn" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold">\n        重置全部筛选\n      </button>'
)

# 6. Expandable Drawer
html = html.replace(
    '<span>🛠️ 老L独家救砖 / 降级 / 避坑方案</span>',
    '<span id="drawer-rescue-title">🛠️ 老L独家救砖 / 降级 / 避坑方案</span>'
)
html = html.replace(
    '<span class="text-[11px] text-zinc-400">100% 官方离线底层机制</span>',
    '<span class="text-[11px] text-zinc-400" id="drawer-rescue-sub">100% 官方离线底层机制</span>'
)
html = html.replace(
    '<span class="font-mono">快速批处理脚本 (.bat) / 应急指令:</span>',
    '<span class="font-mono" id="drawer-bat-title">快速批处理脚本 (.bat) / 应急指令:</span>'
)
html = html.replace(
    '<button onclick="copyDrawerBat()" class="text-blue-400 hover:text-blue-300 font-semibold cursor-pointer">一键复制代码</button>',
    '<button onclick="copyDrawerBat()" id="drawer-btn-copy-bat" class="text-blue-400 hover:text-blue-300 font-semibold cursor-pointer">一键复制代码</button>'
)

html = html.replace(
    '<span>🎨 官方 5 联 1080×1440 高清避坑卡片 (实装)</span>',
    '<span id="drawer-matrix-title">🎨 官方 5 联 1080×1440 高清避坑卡片 (实装)</span>'
)
html = html.replace(
    '<p class="text-[11px] text-zinc-400">已就绪首发 5 联高清卡片，点击任意卡片查看大图：</p>',
    '<p class="text-[11px] text-zinc-400" id="drawer-matrix-desc">已就绪首发 5 联高清卡片，点击任意卡片查看大图：</p>'
)

html = html.replace(
    '<span>【老L·单机避坑局】急救雷达互助群</span>',
    '<span id="drawer-secret-card-title">【老L·单机避坑局】急救雷达互助群</span>'
)
html = html.replace(
    '<span class="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded-full font-mono">公益·零广告</span>',
    '<span class="text-[10px] bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded-full font-mono" id="drawer-secret-card-tag">公益·零广告</span>'
)
html = html.replace(
    '<p class="text-xs text-zinc-300 leading-relaxed">\n            若遇游戏突发更新失效或极端坏档，请保存官方避坑专属暗号，在微信公众号后台或私信输入暗号，自动秒推连夜更新的应急更新包与坏档急救工具！\n          </p>',
    '<p class="text-xs text-zinc-300 leading-relaxed" id="drawer-secret-card-desc">\n            若遇游戏突发更新失效或极端坏档，请保存官方避坑专属暗号，在微信公众号后台或私信输入暗号，自动秒推连夜更新的应急更新包与坏档急救工具！\n          </p>'
)
html = html.replace(
    '<span class="text-xs text-zinc-400">专属避坑暗号:</span>',
    '<span class="text-xs text-zinc-400" id="drawer-secret-card-label">专属避坑暗号:</span>'
)
html = html.replace(
    '<span>一键复制暗号</span>',
    '<span id="drawer-btn-copy-code-text">一键复制暗号</span>'
)
html = html.replace(
    '<span>💡 进群输入暗号秒领：最新追更包 · 坏档救星 · 纯净开源源</span>',
    '<span id="drawer-secret-tip-1">💡 进群输入暗号秒领：最新追更包 · 坏档救星 · 纯净开源源</span>'
)
html = html.replace(
    '<span>群文件严禁 exe，绝对安全</span>',
    '<span id="drawer-secret-tip-2">群文件严禁 exe，绝对安全</span>'
)
html = html.replace(
    '<span>🎮 进入 L-MOD 主库查看完整代码与场景套餐</span>',
    '<span id="drawer-cta-main-text">🎮 进入 L-MOD 主库查看完整代码与场景套餐</span>'
)

with open(RADAR_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Finished adding i18n anchors and language dropdown to radar.html.")
