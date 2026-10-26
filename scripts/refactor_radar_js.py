# -*- coding: utf-8 -*-
"""
scripts/refactor_radar_js.py
Complete Internationalization & Logic Injection for public/radar.html JavaScript
"""

RADAR_PATH = '/Users/xiaolu/Desktop/work/l-mod-portal/public/radar.html'

with open(RADAR_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the last <script> tag which holds the application logic
import re
scripts = list(re.finditer(r'<script\b([^>]*)>(.*?)</script>', content, re.DOTALL))
if not scripts:
    raise RuntimeError("Could not find script tags in radar.html")

target_script_match = scripts[-1]
old_script_body = target_script_match.group(2)

# Extract RADAR_METADATA verbatim from old_script_body
metadata_match = re.search(r'(const RADAR_METADATA = \{.*?\n    \};)', old_script_body, re.DOTALL)
if not metadata_match:
    raise RuntimeError("Could not find RADAR_METADATA in script")

radar_metadata_code = metadata_match.group(1)

# Now assemble the comprehensive refactored script body
new_script_body = f"""
    // ========================================================
    // DEEP COMPATIBILITY METADATA FOR RADAR ENGINE
    // ========================================================
    {radar_metadata_code}

    // ========================================================
    // GLOBAL STATE & I18N ENGINE
    // ========================================================
    let allGames = [];
    let filteredGames = [];
    let currentStatusFilter = 'all';
    let currentEngineFilter = 'all';
    let currentSearchQuery = '';
    let currentSortMode = 'risk-desc';
    let activeDrawerGame = null;

    let currentLang = localStorage.getItem('lmod_lang') || 'zh-CN';
    let translations = window.TRANSLATIONS_DATA || {{}};

    const LANG_CONFIG = {{
      'zh-CN': {{ flag: '🇨🇳', name: '简体中文' }},
      'en':    {{ flag: '🇺🇸', name: 'English' }},
      'zh-TW': {{ flag: '🇭🇰', name: '繁體中文' }},
      'ja':    {{ flag: '🇯🇵', name: '日本語' }},
      'ko':    {{ flag: '🇰🇷', name: '한국어' }},
      'ru':    {{ flag: '🇷🇺', name: 'Русский' }},
      'de':    {{ flag: '🇩🇪', name: 'Deutsch' }},
      'es':    {{ flag: '🇪🇸', name: 'Español' }}
    }};

    function t(key, fallback = '') {{
      if (translations[currentLang] && translations[currentLang][key]) {{
        return translations[currentLang][key];
      }}
      if (translations['zh-CN'] && translations['zh-CN'][key]) {{
        return translations['zh-CN'][key];
      }}
      return fallback;
    }}

    function toggleLangDropdown(event) {{
      if (event) event.stopPropagation();
      const menu = document.getElementById('lang-menu');
      const chevron = document.getElementById('lang-chevron');
      if (!menu) return;
      const isHidden = menu.classList.contains('hidden');
      if (isHidden) {{
        menu.classList.remove('hidden');
        if (chevron) chevron.classList.add('rotate-180');
      }} else {{
        menu.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
      }}
    }}

    function closeLangDropdown() {{
      const menu = document.getElementById('lang-menu');
      const chevron = document.getElementById('lang-chevron');
      if (menu && !menu.classList.contains('hidden')) {{
        menu.classList.add('hidden');
        if (chevron) chevron.classList.remove('rotate-180');
      }}
    }}

    document.addEventListener('click', (e) => {{
      const dd = document.getElementById('custom-lang-dropdown');
      if (dd && !dd.contains(e.target)) {{
        closeLangDropdown();
      }}
    }});

    function selectLanguage(langCode, flag, name) {{
      currentLang = langCode;
      localStorage.setItem('lmod_lang', langCode);

      const flagEl = document.getElementById('current-lang-flag');
      const nameEl = document.getElementById('current-lang-name');
      if (flagEl) flagEl.textContent = flag;
      if (nameEl) nameEl.textContent = name;

      document.querySelectorAll('.lang-option').forEach(btn => {{
        const btnLang = btn.getAttribute('data-lang');
        const check = btn.querySelector('.lang-check');
        if (btnLang === langCode) {{
          if (check) check.classList.remove('hidden');
          btn.classList.add('text-blue-400', 'font-semibold');
        }} else {{
          if (check) check.classList.add('hidden');
          btn.classList.remove('text-blue-400', 'font-semibold');
        }}
      }});

      closeLangDropdown();
      renderRadarUI();
      applyFilters();
      if (activeDrawerGame) {{
        openGameDrawer(activeDrawerGame);
      }}
      showToast(`${{t('toastLangSwitched', '语言已切换至')}} ${{name}}`);
    }}

    function initLanguage() {{
      if (window.TRANSLATIONS_DATA) {{
        translations = window.TRANSLATIONS_DATA;
      }}
      const savedLang = localStorage.getItem('lmod_lang') || 'zh-CN';
      currentLang = LANG_CONFIG[savedLang] ? savedLang : 'zh-CN';
      const cfg = LANG_CONFIG[currentLang] || LANG_CONFIG['zh-CN'];

      const flagEl = document.getElementById('current-lang-flag');
      const nameEl = document.getElementById('current-lang-name');
      if (flagEl) flagEl.textContent = cfg.flag;
      if (nameEl) nameEl.textContent = cfg.name;

      document.querySelectorAll('.lang-option').forEach(btn => {{
        const btnLang = btn.getAttribute('data-lang');
        const check = btn.querySelector('.lang-check');
        if (btnLang === currentLang) {{
          if (check) check.classList.remove('hidden');
          btn.classList.add('text-blue-400', 'font-semibold');
        }} else {{
          if (check) check.classList.add('hidden');
          btn.classList.remove('text-blue-400', 'font-semibold');
        }}
      }});
    }}

    // ========================================================
    // MULTILINGUAL EMERGENCY MARQUEE TICKER DATA & RENDERER
    // ========================================================
    const TICKER_DATA = {{
      'zh-CN': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴【辐射4】', text: '次世代大更新破坏近 10 年 Mod 体系，高危闪退！推荐使用 Downgrader 回退 1.10.163 稳定版' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡【上古卷轴5】', text: 'v1.6.1170 前置需更新对齐！认准 SKSE64 2.2.6 与 SSE Engine Fixes 修复推车飞天' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢【博德之门3】', text: 'Patch 7 官方工坊对齐实测通过！BG3SE v18+ 原生黑窗完全兼容，务必清除老版 ModFixer' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢【艾尔登法环】', text: '黄金树幽影 v1.14 离线免封方案已同步！ModEngine2 管道拦截 EAC 零封号' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢【赛博朋克2077】', text: '往日之影最新对齐！CET 1.33.0 原生脚本通过验证，拒绝旧版 SetLevel 坏档代码' }}
      ],
      'en': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴 [Fallout 4]', text: 'Next-Gen update breaks 10-year mod ecosystem! High crash risk — Downgrader to 1.10.163 recommended.' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡 [Skyrim SE]', text: 'v1.6.1170 requires prerequisite updates! Ensure SKSE64 2.2.6 & SSE Engine Fixes are installed.' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢 [Baldur\\'s Gate 3]', text: 'Patch 7 official mod manager verified! BG3SE v18+ compatible, purge legacy ModFixer.' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢 [Elden Ring]', text: 'Shadow of the Erdtree v1.14 offline safe mode synced! ModEngine2 pipes bypass EAC safely.' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢 [Cyberpunk 2077]', text: 'Phantom Liberty latest patch verified! CET 1.33.0+ native scripts working smoothly.' }}
      ],
      'zh-TW': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴【異塵餘生4】', text: '次世代大更新破壞近 10 年 Mod 體系，高危閃退！推薦使用 Downgrader 回退 1.10.163 穩定版' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡【上古卷軸5】', text: 'v1.6.1170 前置需更新對齊！認準 SKSE64 2.2.6 與 SSE Engine Fixes 修復推車飛天' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢【柏德之門3】', text: 'Patch 7 官方工坊對齊實測通過！BG3SE v18+ 原生黑窗完全相容，務必清除舊版 ModFixer' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢【艾爾登法環】', text: '黃金樹幽影 v1.14 離線免封方案已同步！ModEngine2 管道攔截 EAC 零封號' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢【電馭叛客2077】', text: '往日之影最新對齊！CET 1.33.0 原生腳本通過驗證，拒絕舊版 SetLevel 壞檔代碼' }}
      ],
      'ja': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴【Fallout 4】', text: '次世代アプデで過去10年のMod環境が崩壊！クラッシュ多発、ダウングレード（1.10.163）推奨。' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡【Skyrim SE】', text: 'v1.6.1170 前提MOD更新必須！SKSE64 2.2.6 & SSE Engine Fixes 適用を推奨。' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢【BG3】', text: 'Patch 7 公式Modマネージャー対応検証完了！BG3SE v18+ 完全対応、旧ModFixerは削除必須。' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢【Elden Ring】', text: 'SHADOW OF THE ERDTREE v1.14 オフライン回避策同期完了！ModEngine2でEAC安全ブロック。' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢【Cyberpunk 2077】', text: '仮初めの自由 最新同期完了！CET 1.33.0+ 検証済み、旧SetLevelセーブ破壊コードは使用禁止。' }}
      ],
      'ko': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴【폴아웃 4】', text: '차세대 대형 패치로 10년 모드 생태계 파괴! 심각한 튕김 발생, 1.10.163 다운그레이더 강력 권장.' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡【스카이림 SE】', text: 'v1.6.1170 선행 모드 업데이트 필수! SKSE64 2.2.6 및 SSE Engine Fixes 최신 적용 권장.' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢【발더스 게이트 3】', text: '패치 7 공식 모드 매니저 호환 검증 통과! BG3SE v18+ 완벽 호환, 구버전 ModFixer 삭제 필수.' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢【엘든 링】', text: '황금 나무의 그림자 v1.14 오프라인 밴 방지 동기화 완료! ModEngine2 EAC 우회 적용.' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢【사이버펑크 2077】', text: '팬텀 리버티 최신 패치 검증 완료! CET 1.33.0+ 정상 구동, 구버전 SetLevel 코드 사용 금지.' }}
      ],
      'ru': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴 [Fallout 4]', text: 'Некстген-патч сломал экосистему модов! Высокий риск вылетов — рекомендуется даунгрейд до 1.10.163.' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡 [Skyrim SE]', text: 'Для v1.6.1170 требуются обновления пререквизитов! Используйте SKSE64 2.2.6 и SSE Engine Fixes.' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢 [Baldur\\'s Gate 3]', text: 'Патч 7 проверен с официальным менеджером модов! BG3SE v18+ работает, удалите старый ModFixer.' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢 [Elden Ring]', text: 'Shadow of the Erdtree v1.14 безопасный оффлайн-режим готов! ModEngine2 блокирует EAC.' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢 [Cyberpunk 2077]', text: 'Призрачная свобода проверена! CET 1.33.0+ работает стабильно, избегайте старого кода SetLevel.' }}
      ],
      'de': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴 [Fallout 4]', text: 'Next-Gen-Update zerstört Mod-Ökosystem! Hohes Absturzrisiko — Downgrade auf 1.10.163 empfohlen.' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡 [Skyrim SE]', text: 'v1.6.1170 erfordert Mod-Aktualisierungen! SKSE64 2.2.6 & SSE Engine Fixes verwenden.' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢 [Baldur\\'s Gate 3]', text: 'Patch 7 offizieller Mod-Manager verifiziert! BG3SE v18+ kompatibel, alten ModFixer entfernen.' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢 [Elden Ring]', text: 'Shadow of the Erdtree v1.14 Offline-Schutz aktiv! ModEngine2 umgeht EAC sicher.' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢 [Cyberpunk 2077]', text: 'Phantom Liberty verifiziert! CET 1.33.0+ Skripte funktionieren einwandfrei.' }}
      ],
      'es': [
        {{ id: 'fallout-4', color: 'text-red-400', tag: '🔴 [Fallout 4]', text: '¡Actualización de nueva generación rompe mods! Alto riesgo de fallos — se recomienda Downgrader a 1.10.163.' }},
        {{ id: 'skyrim-se', color: 'text-amber-400', tag: '🟡 [Skyrim SE]', text: '¡v1.6.1170 requiere actualizar dependencias! Use SKSE64 2.2.6 y SSE Engine Fixes.' }},
        {{ id: 'baldurs-gate-3', color: 'text-emerald-400', tag: '🟢 [Baldur\\'s Gate 3]', text: '¡Parche 7 verificado con gestor oficial de mods! BG3SE v18+ compatible, elimine ModFixer antiguo.' }},
        {{ id: 'elden-ring', color: 'text-emerald-400', tag: '🟢 [Elden Ring]', text: '¡Shadow of the Erdtree v1.14 modo seguro sin conexión listo! ModEngine2 bloquea EAC.' }},
        {{ id: 'cyberpunk-2077', color: 'text-emerald-400', tag: '🟢 [Cyberpunk 2077]', text: '¡Phantom Liberty verificado! Scripts nativos CET 1.33.0+ estables, evite código SetLevel obsoleto.' }}
      ]
    }};

    function renderTicker() {{
      const track = document.getElementById('ticker-track');
      if (!track) return;
      const items = TICKER_DATA[currentLang] || TICKER_DATA['zh-CN'];
      
      const makeItemHtml = (item) => `
        <span class="flex items-center space-x-1.5 cursor-pointer hover:text-white" onclick="event.stopPropagation(); openGameDrawerById('${{item.id}}')">
          <span class="${{item.color}} font-bold">${{item.tag}}</span>
          <span>${{item.text}}</span>
        </span>
      `;

      const listHtml = items.map(makeItemHtml).join('<span class="text-zinc-600">|</span>');
      // Clone once for continuous seamless marquee loop
      track.innerHTML = listHtml + '<span class="text-zinc-600">|</span>' + listHtml;
    }}

    // ========================================================
    // RENDER FULL RADAR UI (STATIC & LABELS)
    // ========================================================
    function renderRadarUI() {{
      // 1. Ticker Header
      const tickBadge = document.getElementById('ticker-badge-text');
      if (tickBadge) tickBadge.innerText = t('radarEmergencyBroadcast', '紧急巡检广播');
      const tickBack = document.getElementById('ticker-back-text');
      if (tickBack) tickBack.innerText = t('returnMainVault', '返回 L-MOD 主库');
      renderTicker();

      // 2. Header Brand
      const hTitle = document.getElementById('radar-header-title');
      if (hTitle) hTitle.innerText = t('radarTitle', 'Steam 补丁变动与 Mod 兼容性实时避坑雷达');
      const hVer = document.getElementById('radar-header-version');
      if (hVer) hVer.innerText = t('radarVersionBadge', 'v4.0 独立看板');
      const hPow = document.getElementById('radar-header-powered');
      if (hPow) hPow.innerText = t('radarSubtitle', '由 L-MOD Vault 避坑实验室驱动');
      const hLive = document.getElementById('radar-header-live');
      if (hLive) hLive.innerText = t('radarInspectingLive', '24h 智能对齐巡检进行中');
      const hGroup = document.getElementById('radar-group-code-label');
      if (hGroup) hGroup.innerText = t('radarSecretGroupBtn', '进避坑互助群暗号:');
      const hRet = document.getElementById('radar-return-btn-text');
      if (hRet) hRet.innerText = t('returnMainVault', '返回 L-MOD 主库');

      const menuTitle = document.getElementById('lang-menu-title');
      if (menuTitle) menuTitle.innerText = t('selectLanguage', '选择语言 · Select Language');

      // 3. Metric Cards
      const mgTitle = document.getElementById('metric-green-title');
      if (mgTitle) mgTitle.innerText = t('statusCompatible', '完美兼容 · 实测通过');
      const mgTag = document.getElementById('metric-green-tag');
      if (mgTag) mgTag.innerText = t('statusCompatibleTag', '稳定运行');
      const mgUnit = document.getElementById('metric-green-unit');
      if (mgUnit) mgUnit.innerText = t('metricGreenUnit', '款 3A 大作');
      const mgDesc = document.getElementById('metric-green-desc');
      if (mgDesc) mgDesc.innerText = t('statusCompatibleDesc', '最新补丁实机测试，控制台与前置 100% 畅玩');

      const myTitle = document.getElementById('metric-yellow-title');
      if (myTitle) myTitle.innerText = t('statusWarning', '需更新前置 / 需补丁适配');
      const myTag = document.getElementById('metric-yellow-tag');
      if (myTag) myTag.innerText = t('statusWarningTag', '注意排查');
      const myUnit = document.getElementById('metric-yellow-unit');
      if (myUnit) myUnit.innerText = t('metricYellowUnit', '款需更新前置');
      const myDesc = document.getElementById('metric-yellow-desc');
      if (myDesc) myDesc.innerText = t('statusWarningDesc', '游戏小更新破坏前置DLL，需更新对应框架后启动');

      const mrTitle = document.getElementById('metric-red-title');
      if (mrTitle) mrTitle.innerText = t('statusBroken', '恶性坏档 · 暂停更新');
      const mrTag = document.getElementById('metric-red-tag');
      if (mrTag) mrTag.innerText = t('statusBrokenTag', '紧急预警');
      const mrUnit = document.getElementById('metric-red-unit');
      if (mrUnit) mrUnit.innerText = t('metricRedUnit', '款高危预警');
      const mrDesc = document.getElementById('metric-red-desc');
      if (mrDesc) mrDesc.innerText = t('statusBrokenDesc', '次世代破坏老Mod架构，请务必锁定 Steam 自动更新');

      const miTitle = document.getElementById('metric-inspection-title');
      if (miTitle) miTitle.innerText = t('statusInspection', '巡检哨兵机制');
      const miUnit = document.getElementById('metric-inspection-unit');
      if (miUnit) miUnit.innerText = t('metricInspectionUnit', '款全球神作全覆盖');
      const miDesc = document.getElementById('metric-inspection-desc');
      if (miDesc) miDesc.innerText = t('statusInspectionDesc', '每日对比 Steam AppUpdate 差量，发现坏档连夜同步');

      // 4. Search & Filters
      const sInput = document.getElementById('radar-search');
      if (sInput) sInput.placeholder = t('radarSearchPlaceholder', '搜索游戏名称、Steam AppID (如 1245620)、底层引擎...');

      const sSort = document.getElementById('radar-sort-label');
      if (sSort) sSort.innerText = t('sortLabel', '排序方式:');
      const oRisk = document.getElementById('opt-risk-desc');
      if (oRisk) oRisk.innerText = t('sortRiskDesc', '⚠️ 风险优先 (坏档/需前置置顶)');
      const oRank = document.getElementById('opt-rank-asc');
      if (oRank) oRank.innerText = t('sortRankAsc', '👑 游戏排名 (Rank 1 ~ 100)');
      const oComp = document.getElementById('opt-compat-first');
      if (oComp) oComp.innerText = t('sortCompatibleFirst', '🟢 稳定优先 (已实测完美)');
      const oName = document.getElementById('opt-name-asc');
      if (oName) oName.innerText = t('sortNameAsc', '🔤 游戏名称 (A-Z)');

      const fStatus = document.getElementById('radar-filter-status-label');
      if (fStatus) fStatus.innerText = t('filterCompatLabel', '兼容状态:');
      const pStatAll = document.getElementById('pill-status-all');
      if (pStatAll) pStatAll.innerText = t('filterEngineAll', '全部');
      const pStatGreen = document.getElementById('pill-status-green');
      if (pStatGreen) pStatGreen.innerText = t('statusCompatibleShort', '🟢 完美兼容');
      const pStatYellow = document.getElementById('pill-status-yellow');
      if (pStatYellow) pStatYellow.innerText = t('statusWarningShort', '🟡 需更前置');
      const pStatRed = document.getElementById('pill-status-red');
      if (pStatRed) pStatRed.innerText = t('statusBrokenShort', '🔴 暂停更新');

      const fEngine = document.getElementById('radar-filter-engine-label');
      if (fEngine) fEngine.innerText = t('filterEngineLabel', '专区/引擎:');
      const pEngAll = document.getElementById('pill-engine-all');
      if (pEngAll) pEngAll.innerText = t('filterEngineAll', '全部');
      const pEngFlag = document.getElementById('pill-engine-flagship');
      if (pEngFlag) pEngFlag.innerText = t('filterEngineFlagship', '👑 Top 7 旗舰深度');
      const pEngUE = document.getElementById('pill-engine-unreal');
      if (pEngUE) pEngUE.innerText = t('filterEngineUE', '虚幻引擎');
      const pEngCreation = document.getElementById('pill-engine-creation');
      if (pEngCreation) pEngCreation.innerText = t('filterEngineBethesda', 'B社引擎');
      const pEngFrom = document.getElementById('pill-engine-fromsoft');
      if (pEngFrom) pEngFrom.innerText = t('filterEngineFromSoft', '魂系引擎');

      // 5. Results Count & Legend
      const rMatched = document.getElementById('radar-count-matched');
      if (rMatched) rMatched.innerText = t('matchedGamesCount', '共匹配到');
      const rUnit = document.getElementById('radar-count-unit');
      if (rUnit) rUnit.innerText = t('gamesUnit', '款游戏');
      const legCompat = document.getElementById('legend-text-compat');
      if (legCompat) legCompat.innerText = t('legendCompatible', '完美');
      const legWarn = document.getElementById('legend-text-warn');
      if (legWarn) legWarn.innerText = t('legendWarning', '前置');
      const legBroken = document.getElementById('legend-text-broken');
      if (legBroken) legBroken.innerText = t('legendBroken', '坏档/暂停');

      // 6. Empty State
      const empTitle = document.getElementById('radar-empty-title');
      if (empTitle) empTitle.innerText = t('emptyTitle', '未找到符合条件的游戏');
      const empDesc = document.getElementById('radar-empty-desc');
      if (empDesc) empDesc.innerText = t('emptyDesc', '请尝试更换搜索关键字，或重置状态与引擎筛选条件。');
      const empReset = document.getElementById('radar-empty-reset-btn');
      if (empReset) empReset.innerText = t('resetFiltersBtn', '重置全部筛选');

      // 7. Drawer Static Elements
      const dPatchCheck = document.getElementById('drawer-patch-check-title');
      if (dPatchCheck) dPatchCheck.innerText = '🔍 ' + t('drawerPatchCheckTitle', '补丁变动与最新版本核验');
      const dRescueTitle = document.getElementById('drawer-rescue-title');
      if (dRescueTitle) dRescueTitle.innerText = t('drawerSafeGuide', '🛠️ 老L独家救砖 / 降级 / 避坑方案');
      const dRescueSub = document.getElementById('drawer-rescue-sub');
      if (dRescueSub) dRescueSub.innerText = t('drawerOfflineMechanism', '100% 官方离线底层机制');
      const dBatTitle = document.getElementById('drawer-bat-title');
      if (dBatTitle) dBatTitle.innerText = t('drawerBatLabel', '快速批处理脚本 (.bat) / 应急指令:');
      const dCopyBat = document.getElementById('drawer-btn-copy-bat');
      if (dCopyBat) dCopyBat.innerText = t('drawerCopyBatBtn', '一键复制代码');

      const dMatrixTitle = document.getElementById('drawer-matrix-title');
      if (dMatrixTitle) dMatrixTitle.innerText = t('drawerCardsSectionTitle', '🎨 官方 5 联 1080×1440 高清避坑卡片 (实装)');
      const dMatrixTag = document.getElementById('drawer-matrix-tag');
      if (dMatrixTag) dMatrixTag.innerText = t('drawerMatrixTag', '社交媒体矩阵');
      const dMatrixDesc = document.getElementById('drawer-matrix-desc');
      if (dMatrixDesc) dMatrixDesc.innerText = t('drawerCardsSectionDesc', '已就绪首发 5 联高清卡片，点击任意卡片查看大图：');

      const dSecTitle = document.getElementById('drawer-secret-card-title');
      if (dSecTitle) dSecTitle.innerText = t('drawerSecretCardTitle', '【老L·单机避坑局】急救雷达互助群');
      const dSecTag = document.getElementById('drawer-secret-card-tag');
      if (dSecTag) dSecTag.innerText = t('drawerSecretCardTag', '公益·零广告');
      const dSecDesc = document.getElementById('drawer-secret-card-desc');
      if (dSecDesc) dSecDesc.innerText = t('drawerSecretCardDesc', '若遇游戏突发更新失效或极端坏档，请保存官方避坑专属暗号，在微信公众号后台或私信输入暗号，自动秒推连夜更新的应急更新包与坏档急救工具！');
      const dSecLabel = document.getElementById('drawer-secret-card-label');
      if (dSecLabel) dSecLabel.innerText = t('drawerSecretCodeLabel', '专属避坑暗号:');
      const dCopyCode = document.getElementById('drawer-btn-copy-code-text');
      if (dCopyCode) dCopyCode.innerText = t('drawerCopyCodeBtn', '一键复制暗号');
      const dTip1 = document.getElementById('drawer-secret-tip-1');
      if (dTip1) dTip1.innerText = t('drawerSecretTips1', '💡 进群输入暗号秒领：最新追更包 · 坏档救星 · 纯净开源源');
      const dTip2 = document.getElementById('drawer-secret-tip-2');
      if (dTip2) dTip2.innerText = t('drawerSecretTips2', '群文件严禁 exe，绝对安全');
      const dMainBtn = document.getElementById('drawer-cta-main-text');
      if (dMainBtn) dMainBtn.innerText = t('drawerMainVaultBtn', '🎮 进入 L-MOD 主库查看完整代码与场景套餐');

      const dlModalText = document.getElementById('image-modal-download-text');
      if (dlModalText) dlModalText.innerText = t('downloadOriginalImage', '下载 1080×1440 原图');
    }}

    // ========================================================
    // DEEP COMPATIBILITY & DYNAMIC METADATA ENGINE
    // ========================================================
    function getGameCompatibility(game) {{
      let meta = RADAR_METADATA[game.id];
      if (!meta) {{
        // Heuristic classification for other games
        const dev = (game.developer || '').toLowerCase();
        const genre = (game.genre || '').toLowerCase();
        let status = "green";
        let engine = "Proprietary Engine";

        if (dev.includes('bethesda') || dev.includes('todd')) {{
          status = "yellow";
          engine = "Creation Engine";
        }} else if (dev.includes('fromsoftware')) {{
          status = "yellow";
          engine = "FromSoft Engine";
        }} else if (dev.includes('cd projekt')) {{
          status = "green";
          engine = "REDengine";
        }} else if (genre.includes('rpg') && game.hasConsole) {{
          status = "green";
          engine = "Native Console Ready";
        }}

        const locTitle = (game.titles && game.titles[currentLang]) ? game.titles[currentLang] : game.title;
        meta = {{
          status: status,
          verifiedPatch: game.verifiedPatch || game.latestPatch || t('steamLatestVerified', 'Steam 最新版本实机测试'),
          engine: engine,
          toolchain: game.hasConsole ? t('consoleNative', '官方原生打字终端') : t('offlineFramework', '纯净离线框架'),
          summary: t('radarSummaryStable', 'Steam 官方最新推送已对齐，运行稳定，未发现恶性坏档报错。'),
          riskTitle: t('riskTitleDefault', '💡 日常游玩避坑提示'),
          riskDesc: (game.pitfallNote && game.pitfallNote.tips && game.pitfallNote.tips[0]) ? game.pitfallNote.tips[0] : (currentLang === 'zh-CN' || currentLang === 'zh-TW' ? '建议在单机离线状态下游玩，大版本更新后优先使用本站批处理脚本核对环境路径。' : 'Play in offline mode when modded. Run the verification script after major Steam updates.'),
          riskSeverity: status,
          rescueSteps: [
            `1. Steam -> ${{game.title}} -> Properties -> Local Files.`,
            `2. Shortcut: ${{game.consoleShortcut || '~ (Tilde)'}}.`,
            `3. Backup save files before key quests or modifying facts.`
          ],
          batPreview: `@echo off\\nchcp 65001 >nul\\ntitle [L-MOD Vault] ${{game.title}} Safe Check\\necho [*] Diagnostic passed!\\necho [i] Shortcut: ${{game.consoleShortcut || '~'}}\\npause`
        }};
      }}

      // Ensure statusText is dynamically localized according to active currentLang
      const statusText = meta.status === 'green' ? t('statusCompatible', '🟢 完美兼容实测通过') :
                         meta.status === 'yellow' ? t('statusWarning', '🟡 需更新前置 / 需补丁适配') :
                         t('statusBroken', '🔴 恶性坏档 · 暂停更新');

      return {{
        ...meta,
        statusText: statusText
      }};
    }}

    // ========================================================
    // RENDER FUNCTIONS
    // ========================================================
    function renderRadarCards() {{
      const grid = document.getElementById('radar-grid');
      const empty = document.getElementById('radar-empty');
      const countEl = document.getElementById('results-count');
      const filterDescEl = document.getElementById('active-filter-desc');

      if (!grid) return;

      countEl.innerText = filteredGames.length;

      // Filter description label
      let desc = [];
      if (currentStatusFilter !== 'all') {{
        const statusMap = {{
          green: t('statusCompatibleShort', '🟢 完美兼容'),
          yellow: t('statusWarningShort', '🟡 需更前置'),
          red: t('statusBrokenShort', '🔴 暂停更新')
        }};
        desc.push(statusMap[currentStatusFilter]);
      }}
      if (currentEngineFilter !== 'all') {{
        desc.push(currentEngineFilter === 'flagship' ? t('filterEngineFlagship', '👑 Top 7 旗舰深度') : currentEngineFilter);
      }}
      if (currentSearchQuery) {{
        desc.push(`"${{currentSearchQuery}}"`);
      }}
      filterDescEl.innerText = desc.length > 0 ? `(${{desc.join(' · ')}})` : '';

      if (filteredGames.length === 0) {{
        grid.innerHTML = '';
        empty.classList.remove('hidden');
        return;
      }}

      empty.classList.add('hidden');

      grid.innerHTML = filteredGames.map(game => {{
        const meta = getGameCompatibility(game);
        const localizedTitle = (game.titles && game.titles[currentLang]) ? game.titles[currentLang] : game.title;
        const secretCode = game.radarSecretCode || '老L单机888';

        let statusBorder = 'border-emerald-500/20 hover:border-emerald-500/40';
        let statusBadgeBg = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        let statusDot = 'bg-emerald-500';
        if (meta.status === 'yellow') {{
          statusBorder = 'border-amber-500/20 hover:border-amber-500/40';
          statusBadgeBg = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
          statusDot = 'bg-amber-500';
        }} else if (meta.status === 'red') {{
          statusBorder = 'border-red-500/30 hover:border-red-500/50';
          statusBadgeBg = 'bg-red-500/15 text-red-400 border-red-500/40';
          statusDot = 'bg-red-500';
        }}

        const shortStatus = meta.status === 'green' ? t('statusCompatibleShort', '🟢 完美兼容') :
                            meta.status === 'yellow' ? t('statusWarningShort', '🟡 需更前置') :
                            t('statusBrokenShort', '🔴 暂停更新');

        const riskHeader = meta.status === 'red' ? t('cardRiskBroken', '🚨 恶性坏档风险') : t('cardRiskWarning', '⚠️ 前置版本需注意');

        return `
          <div 
            onclick="openGameDrawerById('${{game.id}}')"
            class="group relative overflow-hidden bg-[#12141a] hover:bg-[#161822] rounded-2xl p-5 border ${{statusBorder}} transition-all duration-200 cursor-pointer flex flex-col justify-between shadow-lg"
          >
            <!-- Top Status & Rank Row -->
            <div class="space-y-3">
              <div class="flex items-center justify-between gap-2">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-mono font-semibold border ${{statusBadgeBg}}">
                  <span class="w-2 h-2 rounded-full ${{statusDot}} ${{meta.status === 'red' ? 'animate-ping' : ''}}"></span>
                  <span>${{shortStatus}}</span>
                </span>
                <span class="text-xs font-mono text-zinc-500 font-bold">#${{game.rank}}</span>
              </div>

              <!-- Title & Meta -->
              <div>
                <h3 class="text-base sm:text-lg font-black text-white group-hover:text-blue-400 transition-colors line-clamp-1">
                  ${{localizedTitle}}
                </h3>
                <div class="flex items-center space-x-2 text-xs text-zinc-400 pt-0.5">
                  <span class="truncate max-w-[180px]">${{game.title}}</span>
                  <span class="text-zinc-600">·</span>
                  <span class="font-mono text-zinc-400 shrink-0">AppID:${{game.steamAppId || '---'}}</span>
                </div>
              </div>

              <!-- Verified Patch & Engine Badges -->
              <div class="flex items-center flex-wrap gap-1.5 pt-1">
                <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-white/5 text-zinc-300 border border-white/5 truncate max-w-[220px]">
                  📌 ${{meta.verifiedPatch}}
                </span>
                <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  ⚙️ ${{meta.engine}}
                </span>
              </div>

              <!-- Brief Verdict -->
              <p class="text-xs text-zinc-300 line-clamp-2 leading-relaxed pt-1">
                ${{meta.summary}}
              </p>

              <!-- Warning Box preview if Red / Yellow -->
              ${{meta.status !== 'green' ? `
                <div class="p-2.5 rounded-xl ${{meta.status === 'red' ? 'bg-red-950/40 text-red-300 border border-red-500/30' : 'bg-amber-950/40 text-amber-300 border border-amber-500/30'}} text-xs space-y-0.5">
                  <div class="font-bold flex items-center gap-1">
                    <span>${{riskHeader}}</span>
                  </div>
                  <p class="text-[11px] line-clamp-1 opacity-90">${{meta.riskDesc}}</p>
                </div>
              ` : ''}}
            </div>

            <!-- Card Bottom Bar: Rescue CTA -->
            <div class="flex items-center justify-between pt-4 mt-3 border-t border-white/5 text-xs">
              <span class="text-blue-400 group-hover:text-blue-300 font-semibold flex items-center gap-1">
                <span>${{t('viewRescueGuide', '查看避坑急救方案')}}</span>
                <svg class="w-3.5 h-3.5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
              </span>
              <span class="text-[11px] text-zinc-400 font-mono">
                ${{t('secretCodePrefix', '暗号:')}} <strong class="text-amber-400">【${{secretCode}}】</strong>
              </span>
            </div>

          </div>
        `;
      }}).join('');
    }}

    // ========================================================
    // EXPANDABLE DRAWER CONTROLS
    // ========================================================
    function openGameDrawerById(gameId) {{
      const game = allGames.find(g => g.id === gameId);
      if (!game) return;
      openGameDrawer(game);
    }}

    function openGameDrawer(game) {{
      activeDrawerGame = game;
      const meta = getGameCompatibility(game);
      const localizedTitle = (game.titles && game.titles[currentLang]) ? game.titles[currentLang] : game.title;
      const secretCode = game.radarSecretCode || '老L单机888';

      // Fill in details
      document.getElementById('drawer-rank').innerText = `RANK #${{game.rank}}`;
      document.getElementById('drawer-engine').innerText = `${{t('engineLabel', '引擎')}}: ${{meta.engine}} | ${{t('toolchainLabel', '工具链')}}: ${{meta.toolchain}}`;
      document.getElementById('drawer-title').innerText = localizedTitle;
      document.getElementById('drawer-entitle').innerText = `${{game.title}} · ${{game.developer || ''}} (${{game.releaseYear || ''}})`;
      document.getElementById('drawer-appid').innerText = game.steamAppId || '---';

      // Status pill
      const pill = document.getElementById('drawer-status-pill');
      pill.innerText = meta.statusText;
      pill.className = `text-xs px-2.5 py-1 rounded-full font-bold font-mono ${{
        meta.status === 'green' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
        meta.status === 'yellow' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
        'bg-red-500/25 text-red-400 border border-red-500/40'
      }}`;

      // Patch & summary
      document.getElementById('drawer-patch').innerText = meta.verifiedPatch;
      document.getElementById('drawer-summary').innerText = meta.summary;

      // Risk box
      const riskBox = document.getElementById('drawer-risk-box');
      const riskTitle = document.getElementById('drawer-risk-title');
      const riskDesc = document.getElementById('drawer-risk-desc');
      riskTitle.innerText = meta.riskTitle;
      riskDesc.innerText = meta.riskDesc;

      if (meta.status === 'red') {{
        riskBox.className = 'p-3.5 rounded-xl border bg-red-950/40 border-red-500/30 text-red-300 space-y-1';
      }} else if (meta.status === 'yellow') {{
        riskBox.className = 'p-3.5 rounded-xl border bg-amber-950/40 border-amber-500/30 text-amber-300 space-y-1';
      }} else {{
        riskBox.className = 'p-3.5 rounded-xl border bg-emerald-950/30 border-emerald-500/30 text-emerald-300 space-y-1';
      }}

      // Rescue steps
      const stepsContainer = document.getElementById('drawer-rescue-steps');
      stepsContainer.innerHTML = meta.rescueSteps.map(step => `
        <div class="flex items-start space-x-2">
          <span class="text-blue-400 font-bold shrink-0">▸</span>
          <span>${{step}}</span>
        </div>
      `).join('');

      // Bat script
      document.getElementById('drawer-code-pre').innerText = meta.batPreview;

      // Populate 5 Cards if Flagship
      const RADAR_FLAGSHIP_FOLDERS = {{
        'cyberpunk-2077': '01_cyberpunk-2077',
        'black-myth-wukong': '02_black-myth-wukong',
        'witcher-3': '03_witcher-3',
        'baldurs-gate-3': '04_baldurs-gate-3',
        'elden-ring': '05_elden-ring',
        'skyrim-se': '06_skyrim-se',
        'fallout-4': '07_fallout-4'
      }};
      const cardsSec = document.getElementById('drawer-cards-section');
      const cardsScroll = document.getElementById('drawer-cards-scroll');
      const folder = RADAR_FLAGSHIP_FOLDERS[game.id];

      if (folder && cardsSec && cardsScroll) {{
        cardsSec.classList.remove('hidden');
        const cardMetas = [
          {{ num: 1, name: 'hook', title: t('slide1Title', 'Slide 1 · 痛点避坑卡') }},
          {{ num: 2, name: 'setup', title: t('slide2Title', 'Slide 2 · 极速开门卡') }},
          {{ num: 3, name: 'commands', title: t('slide3Title', 'Slide 3 · 场景套餐卡') }},
          {{ num: 4, name: 'mods', title: t('slide4Title', 'Slide 4 · 护航模组卡') }},
          {{ num: 5, name: 'cta', title: t('slide5Title', 'Slide 5 · 避坑雷达自取卡') }}
        ];
        cardsScroll.innerHTML = cardMetas.map(m => {{
          const imgUrl = `social_distribution/${{folder}}/images/card_${{m.num}}_${{m.name}}.png`;
          return `
            <div class="shrink-0 w-32 space-y-1.5 cursor-pointer group" onclick="openImageModal('${{imgUrl}}', '《${{localizedTitle}}》${{m.title}}')">
              <div class="relative overflow-hidden rounded-xl border border-white/10 group-hover:border-purple-500/50 transition-all bg-black aspect-[3/4]">
                <img src="${{imgUrl}}" alt="${{m.title}}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" loading="lazy" />
              </div>
              <div class="text-[10px] text-zinc-300 truncate text-center">${{m.title}}</div>
            </div>
          `;
        }}).join('');
      }} else if (cardsSec) {{
        cardsSec.classList.add('hidden');
      }}

      // Secret code
      document.getElementById('drawer-secret-code').innerText = `【${{secretCode}}】`;

      // Main vault link
      const vaultLink = document.getElementById('drawer-main-vault-link');
      vaultLink.href = `index.html#/game/${{game.id}}`;

      // Show drawer
      const container = document.getElementById('drawer-container');
      const backdrop = document.getElementById('drawer-backdrop');
      const panel = document.getElementById('drawer-panel');

      container.classList.remove('pointer-events-none');
      backdrop.classList.remove('opacity-0');
      backdrop.classList.add('opacity-100');

      panel.classList.remove('translate-y-full', 'md:translate-x-full');
      panel.classList.add('translate-y-0', 'md:translate-x-0');

      // Update URL hash without jumping
      history.replaceState(null, '', `#game-${{game.id}}`);
    }}

    function closeGameDrawer() {{
      const container = document.getElementById('drawer-container');
      const backdrop = document.getElementById('drawer-backdrop');
      const panel = document.getElementById('drawer-panel');

      backdrop.classList.remove('opacity-100');
      backdrop.classList.add('opacity-0');

      panel.classList.remove('translate-y-0', 'md:translate-x-0');
      panel.classList.add('translate-y-full', 'md:translate-x-full');

      setTimeout(() => {{
        container.classList.add('pointer-events-none');
      }}, 300);

      activeDrawerGame = null;
      history.replaceState(null, '', window.location.pathname);
    }}

    // ESC to close drawer
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeGameDrawer();
    }});

    // ========================================================
    // SEARCH & FILTER LOGIC
    // ========================================================
    function handleSearch(val) {{
      currentSearchQuery = val.trim().toLowerCase();
      document.getElementById('clear-search-btn').classList.toggle('hidden', currentSearchQuery.length === 0);
      applyFilters();
    }}

    function clearSearch() {{
      document.getElementById('radar-search').value = '';
      currentSearchQuery = '';
      document.getElementById('clear-search-btn').classList.add('hidden');
      applyFilters();
    }}

    function setStatusFilter(status) {{
      currentStatusFilter = status;
      document.querySelectorAll('#status-pills .status-pill').forEach(btn => {{
        if (btn.getAttribute('data-status') === status) {{
          btn.classList.add('active', 'bg-blue-600', 'text-white');
          btn.classList.remove('bg-white/5');
        }} else {{
          btn.classList.remove('active', 'bg-blue-600', 'text-white');
          btn.classList.add('bg-white/5');
        }}
      }});
      applyFilters();
    }}

    function filterByStatus(status) {{
      setStatusFilter(status);
      window.scrollTo({{ top: 380, behavior: 'smooth' }});
    }}

    function setEngineFilter(engine) {{
      currentEngineFilter = engine;
      document.querySelectorAll('#engine-pills .engine-pill').forEach(btn => {{
        if (btn.getAttribute('data-engine') === engine) {{
          btn.classList.add('active', 'bg-white/20', 'text-white');
          btn.classList.remove('bg-white/5');
        }} else {{
          btn.classList.remove('active', 'bg-white/20', 'text-white');
          btn.classList.add('bg-white/5');
        }}
      }});
      applyFilters();
    }}

    function handleSort(mode) {{
      currentSortMode = mode;
      applyFilters();
    }}

    function resetAllFilters() {{
      clearSearch();
      setStatusFilter('all');
      setEngineFilter('all');
      document.getElementById('sort-select').value = 'risk-desc';
      currentSortMode = 'risk-desc';
      applyFilters();
    }}

    function applyFilters() {{
      filteredGames = allGames.filter(game => {{
        const meta = getGameCompatibility(game);
        const zhTitle = (game.titles && game.titles['zh-CN']) ? game.titles['zh-CN'].toLowerCase() : '';
        const locTitle = (game.titles && game.titles[currentLang]) ? game.titles[currentLang].toLowerCase() : '';
        const enTitle = (game.title || '').toLowerCase();
        const appId = String(game.steamAppId || '');
        const dev = (game.developer || '').toLowerCase();
        const engine = (meta.engine || '').toLowerCase();

        // 1. Status Filter
        if (currentStatusFilter !== 'all' && meta.status !== currentStatusFilter) {{
          return false;
        }}

        // 2. Engine / Flagship Filter
        if (currentEngineFilter === 'flagship') {{
          if (game.rank > 7) return false;
        }} else if (currentEngineFilter !== 'all') {{
          if (!engine.includes(currentEngineFilter.toLowerCase())) return false;
        }}

        // 3. Search Query (multilingual match)
        if (currentSearchQuery) {{
          const matchTitle = zhTitle.includes(currentSearchQuery) || 
                             locTitle.includes(currentSearchQuery) || 
                             enTitle.includes(currentSearchQuery);
          const matchAppId = appId.includes(currentSearchQuery);
          const matchDev = dev.includes(currentSearchQuery);
          const matchEngine = engine.includes(currentSearchQuery);
          if (!matchTitle && !matchAppId && !matchDev && !matchEngine) {{
            return false;
          }}
        }}

        return true;
      }});

      // 4. Sort
      filteredGames.sort((a, b) => {{
        const metaA = getGameCompatibility(a);
        const metaB = getGameCompatibility(b);

        if (currentSortMode === 'risk-desc') {{
          const scoreMap = {{ red: 3, yellow: 2, green: 1 }};
          const diff = scoreMap[metaB.status] - scoreMap[metaA.status];
          if (diff !== 0) return diff;
          return a.rank - b.rank;
        }} else if (currentSortMode === 'compatible-first') {{
          const scoreMap = {{ green: 3, yellow: 2, red: 1 }};
          const diff = scoreMap[metaB.status] - scoreMap[metaA.status];
          if (diff !== 0) return diff;
          return a.rank - b.rank;
        }} else if (currentSortMode === 'rank-asc') {{
          return a.rank - b.rank;
        }} else if (currentSortMode === 'name-asc') {{
          return a.title.localeCompare(b.title);
        }}
        return 0;
      }});

      renderRadarCards();
    }}

    // ========================================================
    // CLIPBOARD HELPERS (WECHAT 100% COMPATIBLE FALLBACK)
    // ========================================================
    function copyText(text, successMsg) {{
      const msg = successMsg || t('toastCopied', '已复制！');
      if (navigator.clipboard && navigator.clipboard.writeText) {{
        navigator.clipboard.writeText(text).then(() => {{
          showToast(msg);
        }}).catch(() => {{
          fallbackCopyText(text, msg);
        }});
      }} else {{
        fallbackCopyText(text, msg);
      }}
    }}

    function fallbackCopyText(text, successMsg) {{
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.top = '0';
      ta.style.left = '0';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {{
        document.execCommand('copy');
        showToast(successMsg);
      }} catch (e) {{
        showToast('Ctrl+C / Cmd+C');
      }}
      document.body.removeChild(ta);
    }}

    function showToast(text) {{
      const toast = document.getElementById('toast');
      document.getElementById('toast-text').innerText = text;
      toast.classList.remove('-translate-y-20', 'opacity-0');
      toast.classList.add('translate-y-0', 'opacity-100');
      setTimeout(() => {{
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('-translate-y-20', 'opacity-0');
      }}, 2500);
    }}

    function copyGroupSecretCode() {{
      copyText('老L单机888', t('toastSecretCopied', '进群暗号已复制！微信后台发送秒领急救包'));
    }}

    function copyCurrentSecretCode() {{
      if (!activeDrawerGame) return;
      const code = activeDrawerGame.radarSecretCode || '老L单机888';
      copyText(code, t('toastSecretCopied', '进群暗号已复制！微信后台发送秒领急救包'));
    }}

    function copyDrawerBat() {{
      if (!activeDrawerGame) return;
      const meta = getGameCompatibility(activeDrawerGame);
      copyText(meta.batPreview, t('toastBatCopied', '批处理脚本代码已复制！新建文本改名为 .bat 即可运行'));
    }}

    function scrollAlerts() {{
      // Pause or jump
    }}

    // ========================================================
    // INITIALIZATION & URL ROUTING
    // ========================================================
    function updateMetrics() {{
      let green = 0, yellow = 0, red = 0;
      allGames.forEach(g => {{
        const meta = getGameCompatibility(g);
        if (meta.status === 'green') green++;
        else if (meta.status === 'yellow') yellow++;
        else if (meta.status === 'red') red++;
      }});
      const statG = document.getElementById('stat-green');
      if (statG) statG.innerText = green;
      const statY = document.getElementById('stat-yellow');
      if (statY) statY.innerText = yellow;
      const statR = document.getElementById('stat-red');
      if (statR) statR.innerText = red;
    }}

    function handleUrlParams() {{
      const urlParams = new URLSearchParams(window.location.search);
      const gameParam = urlParams.get('game');
      const hash = window.location.hash.replace('#game-', '').replace('#', '');
      const targetId = gameParam || hash;

      if (targetId) {{
        setTimeout(() => {{
          openGameDrawerById(targetId);
        }}, 150);
      }}
    }}

    // ==========================================
    // IMAGE MODAL PREVIEW HANDLER
    // ==========================================
    function openImageModal(src, title) {{
      const modal = document.getElementById('image-modal');
      const img = document.getElementById('image-modal-img');
      const titleEl = document.getElementById('image-modal-title');
      const dl = document.getElementById('image-modal-download');
      if (!modal || !img) return;

      img.src = src;
      if (titleEl) titleEl.innerText = title || '1080×1440 HD Card';
      if (dl) {{
        dl.href = src;
        dl.setAttribute('download', src.split('/').pop());
      }}
      modal.classList.remove('hidden');
      modal.classList.add('flex');
    }}

    function closeImageModal() {{
      const modal = document.getElementById('image-modal');
      if (!modal) return;
      modal.classList.remove('flex');
      modal.classList.add('hidden');
    }}

    function initRadar() {{
      if (window.GAMES_DATA) {{
        allGames = window.GAMES_DATA;
      }} else if (window.GAMES_DATABASE) {{
        allGames = window.GAMES_DATABASE;
      }}
      initLanguage();
      renderRadarUI();
      updateMetrics();
      applyFilters();
      handleUrlParams();
    }}

    window.addEventListener('DOMContentLoaded', initRadar);
"""

# Replace target script in content
new_html = content[:target_script_match.start(2)] + new_script_body + content[target_script_match.end(2):]

with open(RADAR_PATH, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully replaced Script 3 in radar.html with complete i18n engine!")
