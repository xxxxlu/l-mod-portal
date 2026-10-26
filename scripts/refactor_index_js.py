#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/refactor_index_js.py
Inject dynamic i18n logic into public/index.html
"""

INDEX_PATH = "/Users/xiaolu/Desktop/work/l-mod-portal/public/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update LANG_CONFIG and t() helper and initLanguage()
old_select_lang = """    function selectLanguage(langCode, flag, name) {
      currentLang = langCode;
      document.getElementById('current-lang-flag').innerText = flag;
      document.getElementById('current-lang-name').innerText = name;
      
      // Update checkmark
      document.querySelectorAll('.lang-option').forEach(btn => {
        const check = btn.querySelector('.lang-check');
        if (btn.dataset.lang === langCode) {
          check.classList.remove('hidden');
        } else {
          check.classList.add('hidden');
        }
      });

      closeLangDropdown();
      renderUI();
      renderGames();
      renderRecentSidebar();
      if (activeGame) {
        renderGameDetailView(activeGame);
      }
      showToast(`语言已切换至 ${name}`);
    }"""

new_select_lang = """    const LANG_CONFIG = {
      'zh-CN': { flag: '🇨🇳', name: '简体中文' },
      'en': { flag: '🇺🇸', name: 'English' },
      'zh-TW': { flag: '🇭🇰', name: '繁體中文' },
      'ja': { flag: '🇯🇵', name: '日本語' },
      'ko': { flag: '🇰🇷', name: '한국어' },
      'ru': { flag: '🇷🇺', name: 'Русский' },
      'de': { flag: '🇩🇪', name: 'Deutsch' },
      'es': { flag: '🇪🇸', name: 'Español' }
    };

    function t(key, fallback = '') {
      if (translations[currentLang] && translations[currentLang][key] !== undefined) {
        return translations[currentLang][key];
      }
      if (translations['zh-CN'] && translations['zh-CN'][key] !== undefined) {
        return translations['zh-CN'][key];
      }
      return fallback || key;
    }

    function initLanguage() {
      const savedLang = localStorage.getItem('lmod_lang');
      if (savedLang && LANG_CONFIG[savedLang]) {
        currentLang = savedLang;
        const flagEl = document.getElementById('current-lang-flag');
        const nameEl = document.getElementById('current-lang-name');
        if (flagEl) flagEl.innerText = LANG_CONFIG[savedLang].flag;
        if (nameEl) nameEl.innerText = LANG_CONFIG[savedLang].name;
        document.querySelectorAll('.lang-option').forEach(btn => {
          const check = btn.querySelector('.lang-check');
          if (check) {
            if (btn.dataset.lang === savedLang) {
              check.classList.remove('hidden');
            } else {
              check.classList.add('hidden');
            }
          }
        });
      }
    }

    function selectLanguage(langCode, flag, name) {
      currentLang = langCode;
      try {
        localStorage.setItem('lmod_lang', langCode);
      } catch (e) {}
      
      const flagEl = document.getElementById('current-lang-flag');
      const nameEl = document.getElementById('current-lang-name');
      if (flagEl) flagEl.innerText = flag;
      if (nameEl) nameEl.innerText = name;
      
      // Update checkmark
      document.querySelectorAll('.lang-option').forEach(btn => {
        const check = btn.querySelector('.lang-check');
        if (check) {
          if (btn.dataset.lang === langCode) {
            check.classList.remove('hidden');
          } else {
            check.classList.add('hidden');
          }
        }
      });

      closeLangDropdown();
      renderUI();
      renderGames();
      renderRecentSidebar();
      if (activeGame) {
        renderGameDetailView(activeGame);
      }
      showToast((t('toastLangSwitched') || '语言已切换至') + ` ${name}`);
    }"""

if old_select_lang in content:
    content = content.replace(old_select_lang, new_select_lang)
    print("✅ Injected LANG_CONFIG, t() and updated selectLanguage")
else:
    print("⚠️ Could not find exact old_select_lang")

# 2. Update renderUI()
old_render_ui = """    function renderUI() {
      const t = translations[currentLang] || translations['zh-CN'];
      if (!t) return;

      document.getElementById('hero-subtitle').innerText = t.heroSubtitle;
      document.getElementById('search-input').placeholder = t.searchPlaceholder;
      document.getElementById('btn-filter-all').innerText = t.filterAll;
      document.getElementById('btn-filter-console').innerText = t.filterConsole;
      document.getElementById('btn-filter-mods').innerText = t.filterMods;
      document.getElementById('btn-filter-trainers').innerText = t.filterTrainers;
      document.getElementById('footer-note').innerText = t.footerNote;
    }"""

new_render_ui = """    function renderUI() {
      document.title = `${t('siteName')} | ${t('siteTagline')}`;

      const setElText = (id, text) => {
        const el = document.getElementById(id);
        if (el && text !== undefined) el.innerText = text;
      };

      // Sidebar
      setElText('sidebar-explore-label', t('navExplore'));
      setElText('sidebar-nav-all', t('navAllRank'));
      setElText('sidebar-nav-certified', t('filterCertified'));
      setElText('sidebar-nav-mining', t('filterMining'));
      setElText('sidebar-nav-console', t('navConsole'));
      setElText('sidebar-nav-mods', t('navMods'));
      setElText('sidebar-nav-trainers', t('navTrainers'));
      setElText('sidebar-nav-radar', t('navRadar'));
      setElText('sidebar-recents-label', t('navRecents'));

      // Ticker & Header
      setElText('broadcast-bar-title', t('broadcastTitle'));
      setElText('broadcast-bar-btn', t('broadcastRadarBtn'));
      setElText('header-breadcrumb-title', t('headerBreadcrumb'));
      setElText('header-radar-btn-text', t('radarBtnHeader'));
      setElText('view-mode-gallery-text', t('viewGallery'));
      setElText('view-mode-list-text', t('viewList'));

      // Hero
      setElText('hero-subtitle', t('heroSubtitle'));
      const searchInput = document.getElementById('search-input');
      if (searchInput) searchInput.placeholder = t('searchPlaceholder');
      setElText('quick-search-label', t('quickSearchLabel'));

      // Filter Buttons
      setElText('btn-filter-all', t('filterAll'));
      setElText('btn-filter-certified', t('filterCertified'));
      setElText('btn-filter-mining', t('filterMining'));
      setElText('btn-filter-console', t('filterConsole'));
      setElText('btn-filter-mods', t('filterMods'));
      setElText('btn-filter-trainers', t('filterTrainers'));

      // Detail Static Labels
      setElText('detail-back-text', t('btnBackToCatalog'));
      setElText('detail-cert-text', t('certificationText'));
      setElText('detail-clean-guarantee', t('cleanGuarantee'));
      setElText('stat-label-downloads', t('statNexusDownloads'));
      setElText('stat-label-endorsements', t('statPlayerRec'));
      setElText('stat-label-mods', t('statCuratedMods'));

      // Detail Tabs
      setElText('tab-text-console', t('tabConsole'));
      setElText('tab-text-mods', t('tabMods'));
      setElText('tab-text-trainers', t('tabTrainers'));
      setElText('tab-text-reviews', t('tabReviews'));
      setElText('tab-text-social-cards', t('tabSocialCards'));

      // Detail Sub-sections
      setElText('detail-console-guide-title', t('consoleGuideTitle'));
      setElText('detail-btn-lazy-door', t('btnOpenLazyDoor'));
      setElText('detail-shortcut-label', t('consoleShortcutLabel'));
      setElText('detail-popular-cmd-title', t('popularCommandsTitle'));
      setElText('detail-mod-path-title', t('modPathTitle'));
      setElText('detail-musthave-mods-title', t('mustHaveModsTitle'));
      setElText('detail-trainer-title', t('trainerTitle'));

      // Trainer section in detail
      setElText('trainer-sec-title', t('trainerHeaderTitle'));
      setElText('trainer-sec-sub', t('trainerHeaderSubtitle'));
      setElText('trainer-sec-desc', t('trainerHeaderDesc'));
      setElText('trainer-btn-direct-dl', t('trainerDirectDownloadBtn'));
      setElText('trainer-btn-official-page', t('trainerOfficialPageBtn'));
      setElText('trainer-def-title', t('trainerDefenderTitle'));
      setElText('trainer-def-desc', t('trainerDefenderDesc'));
      setElText('trainer-def-step1', t('trainerDefenderStep1'));
      setElText('trainer-def-step2', t('trainerDefenderStep2'));
      setElText('trainer-def-step3', t('trainerDefenderStep3'));
      setElText('trainer-def-cmd-label', t('trainerDefenderCmdLabel'));
      setElText('trainer-btn-copy-def', t('trainerDefenderCopyCmdBtn'));

      const hotkeysInput = document.getElementById('hotkeys-search-input');
      if (hotkeysInput) hotkeysInput.placeholder = t('trainerSearchPlaceholder');

      // Modals: Lazy Door
      setElText('lazy-modal-title', t('activatorTitle'));
      setElText('lazy-modal-tag', t('activatorTag'));
      setElText('lazy-modal-subtitle', t('activatorDesc'));
      setElText('lazy-safe-title', t('activatorSafeNotice'));
      setElText('lazy-safe-desc', t('activatorSafeDesc'));
      setElText('lazy-steps-title', t('activatorGuideTitle'));
      setElText('lazy-step-1', t('activatorStep1'));
      setElText('lazy-step-2', t('activatorStep2'));
      setElText('lazy-step-3', t('activatorStep3'));
      setElText('lazy-adapted-label', t('activatorAdapted'));
      setElText('lazy-btn-copy', t('activatorCopyCode'));
      setElText('lazy-btn-download', t('activatorDownloadBat'));
      setElText('lazy-btn-close', t('activatorClose'));

      // Modals: Trainer Download
      setElText('trainer-modal-clean-tag', t('trainerModalCleanTag'));
      setElText('trainer-modal-subtitle', t('trainerModalStarted'));
      setElText('trainer-ex-title', t('trainerExclusionTitle'));
      setElText('trainer-ex-desc', t('trainerExclusionDesc'));
      setElText('trainer-ex-cmd-label', t('trainerExclusionCmdLabel'));
      setElText('trainer-btn-copy-cmd', t('copyCmdBtn'));
      setElText('trainer-dual-label', t('trainerDualChannels'));
      setElText('trainer-btn-retrigger', t('trainerRetriggerBtn'));
      setElText('trainer-btn-backup', t('trainerBackupMirror'));
      setElText('trainer-3step-hint', t('trainer3StepHint'));
      setElText('trainer-btn-close', t('trainerClose'));

      // Modals: Mod Download
      setElText('mod-modal-label-file', t('modModalTargetFile'));
      setElText('mod-modal-label-path', t('modModalInstallPath'));
      setElText('mod-modal-btn-copy-path', t('copyPathBtn'));
      setElText('mod-modal-steps-title', t('modInstallStepsTitle'));
      setElText('mod-modal-btn-retrigger', t('modRetriggerBtn'));
      setElText('mod-modal-btn-nexus', t('modNexusBtn'));
      setElText('mod-modal-btn-close', t('modClose'));

      // Image Modal
      setElText('image-modal-dl-text', t('downloadHdCard'));

      // Footer
      setElText('footer-note', t('footerNote'));
    }"""

if old_render_ui in content:
    content = content.replace(old_render_ui, new_render_ui)
    print("✅ Injected comprehensive renderUI()")
else:
    print("⚠️ Could not find exact old_render_ui")

# 3. Update renderRecentSidebar empty message
content = content.replace(
    'container.innerHTML = \'<div class="px-3 py-2 text-zinc-400 dark:text-zinc-600 italic text-xs">暂无历史记录</div>\';',
    'container.innerHTML = `<div class="px-3 py-2 text-zinc-400 dark:text-zinc-600 italic text-xs">${t(\'recentsEmpty\')}</div>`;'
)

# 4. Update count display and badges in renderGames()
old_filter_tags = """      let filterTag = '';
      if (currentFilter === 'certified') filterTag = ' (👑 老L全息精测认证)';
      else if (currentFilter === 'mining') filterTag = ' (🛠️ 持续排雷采掘中)';
      else if (currentFilter === 'console') filterTag = ' (⚡ 官方控制台支持)';
      else if (currentFilter === 'mods') filterTag = ' (📦 N网精选 MOD)';
      else if (currentFilter === 'trainers') filterTag = ' (🛡️ 纯净修改器)';

      document.getElementById('games-count-display').innerText = 
        `共收录 ${allGames.length} 款单机神作 • 当前显示 ${filtered.length} 款${filterTag}`;"""

new_filter_tags = """      let filterTag = '';
      if (currentFilter === 'certified') filterTag = ` (${t('filterCertified')})`;
      else if (currentFilter === 'mining') filterTag = ` (${t('filterMining')})`;
      else if (currentFilter === 'console') filterTag = ` (${t('filterConsole')})`;
      else if (currentFilter === 'mods') filterTag = ` (${t('filterMods')})`;
      else if (currentFilter === 'trainers') filterTag = ` (${t('filterTrainers')})`;

      const countBadgeTemplate = t('catalogCountBadge') || '共收录 {total} 款单机神作 • 当前显示 {count} 款{filter}';
      document.getElementById('games-count-display').innerText = countBadgeTemplate
        .replace('{total}', allGames.length)
        .replace('{count}', filtered.length)
        .replace('{filter}', filterTag);"""

if old_filter_tags in content:
    content = content.replace(old_filter_tags, new_filter_tags)
    print("✅ Updated filterTag and games-count-display in renderGames()")
else:
    print("⚠️ Could not find exact old_filter_tags")

# Update card badges in renderGames()
content = content.replace(
    '`<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500 text-zinc-950 shadow-md flex items-center gap-1"><span>👑</span><span>精测认证</span></span>` \n                  : `<span class="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-zinc-900/80 text-zinc-300 backdrop-blur-md border border-white/10 flex items-center gap-1"><span>🛠️</span><span>排雷采掘中</span></span>`',
    '`<span class="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-500 text-zinc-950 shadow-md flex items-center gap-1"><span>👑</span><span>${t(\'cardCertifiedBadge\')}</span></span>` \n                  : `<span class="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-zinc-900/80 text-zinc-300 backdrop-blur-md border border-white/10 flex items-center gap-1"><span>🛠️</span><span>${t(\'cardMiningBadge\')}</span></span>`'
)

content = content.replace(
    '<span class="truncate">${game.verifiedPatch || \'最新补丁实测\'} · 全前置全指令实测</span>',
    '<span class="truncate">${game.verifiedPatch || t(\'detailTestedPatch\')} · ${t(\'cardTestedBadge\')}</span>'
)
content = content.replace(
    '<span class="truncate">老L正在实测最新补丁兼容性中</span>',
    '<span class="truncate">${t(\'cardTestingBadge\')}</span>'
)
content = content.replace(
    '${game.hasConsole ? `<span class="text-[10px] bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 px-2 py-0.5 rounded-full font-semibold">⚡ 控制台</span>` : \'\'}',
    '${game.hasConsole ? `<span class="text-[10px] bg-blue-50 dark:bg-blue-500/10 text-blue-600 dark:text-blue-400 px-2 py-0.5 rounded-full font-semibold">⚡ ${t(\'tabConsole\')}</span>` : \'\'}'
)
content = content.replace(
    '${game.hasMods ? `<span class="text-[10px] bg-purple-50 dark:bg-purple-500/10 text-purple-600 dark:text-purple-400 px-2 py-0.5 rounded-full font-semibold">📦 N网MOD</span>` : \'\'}',
    '${game.hasMods ? `<span class="text-[10px] bg-purple-50 dark:bg-purple-500/10 text-purple-600 dark:text-purple-400 px-2 py-0.5 rounded-full font-semibold">📦 ${t(\'tabMods\')}</span>` : \'\'}'
)
content = content.replace(
    '${game.hasTrainer ? `<span class="text-[10px] bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2 py-0.5 rounded-full font-semibold">🛡️ 纯净修改</span>` : \'\'}',
    '${game.hasTrainer ? `<span class="text-[10px] bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2 py-0.5 rounded-full font-semibold">🛡️ ${t(\'filterTrainers\')}</span>` : \'\'}'
)

# 5. Detail View console badge and patch badge
content = content.replace(
    'document.getElementById(\'detail-console-badge\').innerText = game.hasConsole ? "官方控制台支持" : "MOD/修改器支持";',
    'document.getElementById(\'detail-console-badge\').innerText = game.hasConsole ? t(\'consoleStatusAvailable\') : t(\'consoleStatusNone\');'
)
content = content.replace(
    'patchBadgeElem.innerText = `👑 老L全息精测认证 (${game.verifiedPatch || \'最新补丁实测\'} · 全前置/全指令实测通过)`;',
    'patchBadgeElem.innerText = `${t(\'cardCertifiedBadge\')} (${game.verifiedPatch || t(\'detailTestedPatch\')} · ${t(\'cardTestedBadge\')})`;'
)
content = content.replace(
    'patchBadgeElem.innerText = `🛠️ 持续排雷采掘中 · 老L正在实测最新补丁兼容性中`;',
    'patchBadgeElem.innerText = `${t(\'cardMiningBadge\')} · ${t(\'cardTestingBadge\')}`;'
)

# 6. Detail View Console Categories Copy button
content = content.replace(
    '<span>复制指令</span>\n                </button>',
    '<span>${t(\'btnCopyCode\')}</span>\n                </button>'
)

# 7. Curated Mods rendering labels
content = content.replace(
    '<div class="font-bold text-zinc-800 dark:text-zinc-200 mb-1">傻瓜安装指引:</div>',
    '<div class="font-bold text-zinc-800 dark:text-zinc-200 mb-1">${t(\'modInstallStepsGuide\')}</div>'
)
content = content.replace(
    '<div class="text-xs text-zinc-400">前置依赖: <span class="text-zinc-700 dark:text-zinc-300 font-medium">',
    '<div class="text-xs text-zinc-400">${t(\'modDependencyLabel\')} <span class="text-zinc-700 dark:text-zinc-300 font-medium">'
)
content = content.replace(
    '<span>原页</span>\n                  </a>',
    '<span>${t(\'modOriginPageBtn\')}</span>\n                  </a>'
)
content = content.replace(
    '<span>${mod.isDirect !== false ? \'⚡ 直连安全下载 (ZIP)\' : \'🚀 官方精选转存直达\'}</span>',
    '<span>${mod.isDirect !== false ? t(\'modDirectBtn\') : t(\'modMirrorBtn\')}</span>'
)

# 8. Scenario Bundles
old_scenario_bundles = """    function renderScenarioBundles(game) {
      const container = document.getElementById('detail-scenario-bundles-container');
      if (!container) return;

      if (!game.hasConsole) {
        container.innerHTML = `
          <div class="bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-emerald-500/10 rounded-[28px] p-6 border border-blue-500/20 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center space-x-3.5">
              <div class="w-10 h-10 rounded-2xl bg-blue-600/20 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0">
                <span class="text-xl">⚡</span>
              </div>
              <div>
                <div class="font-extrabold text-sm sm:text-base text-zinc-900 dark:text-white">本游戏官方无原生内置控制台 · 老L避坑指南</div>
                <div class="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">已为你全面匹配 100% 纯净安全的【风灵月影 FLiNG 修改器】与【N网精选 MOD】</div>
              </div>
            </div>
            <button onclick="setDetailTab('trainers')" class="px-5 py-2.5 rounded-full bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition-all shadow-md shrink-0 flex items-center gap-1.5 cursor-pointer">
              <span>⚡ 前往【纯净修改器】专区</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
            </button>
          </div>
        `;
        return;
      }

      const bundles = (game.scenarioBundles && game.scenarioBundles.length > 0)
        ? game.scenarioBundles
        : generateDynamicBundles(game);

      if (!bundles || bundles.length === 0) {
        container.innerHTML = '';
        return;
      }

      const shortcutKey = (game.consoleShortcut || '~').split(' ')[0] || '~';

      let cardsHtml = '';
      bundles.forEach((b, idx) => {
        let gradientBorder = 'border-blue-500/30 hover:border-blue-500';
        let gradientBg = 'from-blue-500/5 to-cyan-500/5';
        let badgeColor = 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20';
        let btnGradient = 'from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-blue-500/25';
        let icon = '🚀';

        if (b.type === 'salvation' || idx === 1) {
          gradientBorder = 'border-purple-500/30 hover:border-purple-500';
          gradientBg = 'from-purple-500/5 to-pink-500/5';
          badgeColor = 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20';
          btnGradient = 'from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 shadow-purple-500/25';
          icon = '💖';
        } else if (b.type === 'arsenal' || idx === 2) {
          gradientBorder = 'border-amber-500/30 hover:border-amber-500';
          gradientBg = 'from-amber-500/5 to-orange-500/5';
          badgeColor = 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
          btnGradient = 'from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 shadow-amber-500/25';
          icon = '⚔️';
        }

        const highlightsList = (b.highlights || []).map(hl => `
          <div class="flex items-start gap-1.5 text-xs text-zinc-700 dark:text-zinc-300">
            <svg class="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
            <span class="leading-snug">${hl}</span>
          </div>
        `).join('');

        const previewLines = b.code ? b.code.split('\\n').filter(l => l.trim() && !l.trim().startsWith('--') && !l.trim().startsWith('//') && !l.trim().startsWith('#')).slice(0, 3) : [];

        cardsHtml += `
          <div class="bg-gradient-to-b ${gradientBg} bg-white dark:bg-[#141518] rounded-[24px] p-5 sm:p-6 border ${gradientBorder} shadow-sm hover:shadow-md transition-all flex flex-col justify-between space-y-4 group">
            <div class="space-y-3">
              <div class="flex items-center justify-between gap-2 flex-wrap">
                <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${badgeColor}">
                  ${b.tag || '老L极客推荐'}
                </span>
                <span class="text-[10px] text-zinc-400 font-mono">1-Click Bundle</span>
              </div>
              <div>
                <h4 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white flex items-center gap-1.5">
                  <span>${icon}</span>
                  <span>${b.name}</span>
                </h4>
                <p class="text-xs text-zinc-500 dark:text-zinc-400 mt-1 leading-relaxed min-h-[36px]">
                  ${b.desc}
                </p>
              </div>
              <div class="pt-2 border-t border-zinc-100 dark:border-white/5 space-y-2">
                <div class="text-[11px] font-bold text-zinc-400 uppercase tracking-wider">套餐包含特性：</div>
                <div class="space-y-1.5">
                  ${highlightsList}
                </div>
              </div>
              ${previewLines.length > 0 ? `
                <div class="bg-zinc-100/80 dark:bg-black/40 rounded-xl p-2.5 font-mono text-[10px] text-zinc-600 dark:text-zinc-400 border border-zinc-200/60 dark:border-white/5 overflow-hidden">
                  <div class="text-[9px] text-zinc-400 mb-1 font-sans">代码预演:</div>
                  ${previewLines.map(pl => `<div class="truncate text-blue-600 dark:text-blue-400 font-semibold">${pl}</div>`).join('')}
                  <div class="text-[9px] text-zinc-400 mt-1 italic font-sans">+ 完整多行自动打包</div>
                </div>
              ` : ''}
            </div>

            <div class="pt-2">
              <button 
                onclick="copyScenarioBundle('${game.id}', '${b.id}')"
                class="w-full py-3 px-4 rounded-xl font-bold text-xs text-white bg-gradient-to-r ${btnGradient} shadow-md flex items-center justify-center gap-2 transition-all transform group-hover:scale-[1.02] active:scale-95 cursor-pointer"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                <span>一键打包复制完整脚本</span>
              </button>
            </div>
          </div>
        `;
      });

      container.innerHTML = `
        <div class="bg-white dark:bg-[#141518] rounded-[28px] p-6 border border-zinc-200/80 dark:border-white/10 shadow-sm space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-zinc-100 dark:border-white/5">
            <div>
              <div class="flex items-center gap-2 flex-wrap mb-1">
                <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                <h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white">
                  老L·极客推荐场景套餐 (小白 10 秒一键爽到)
                </h3>
                <span class="text-xs bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-0.5 rounded-full font-bold border border-emerald-500/20">
                  100% 官方最新补丁实测
                </span>
              </div>
              <p class="text-xs text-zinc-500 dark:text-zinc-400">
                拒绝繁琐一条条敲代码！针对不同游玩场景整套打包，进游戏呼出控制台粘贴一次即可整套生效。
              </p>
            </div>
            <div class="flex items-center gap-2 text-xs text-zinc-400 shrink-0">
              <span>呼出键:</span>
              <code class="px-2 py-1 rounded-md bg-zinc-100 dark:bg-white/10 text-blue-600 dark:text-blue-400 font-mono font-bold">${shortcutKey}</code>
            </div>
          </div>

          <!-- 3-Column Responsive Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            ${cardsHtml}
          </div>

          <!-- Advanced usage tip -->
          <div class="flex items-center gap-2 text-xs text-zinc-500 dark:text-zinc-400 bg-zinc-50 dark:bg-black/30 p-3 rounded-xl border border-zinc-200/60 dark:border-white/5">
            <svg class="w-4 h-4 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>极客贴士：代码按官方控制台语法封装，点击按钮直接复制后，在游戏里呼出控制台按 <b>Ctrl+V</b>（或右键）回车执行即可！</span>
          </div>
        </div>
      `;
    }"""

new_scenario_bundles = """    function renderScenarioBundles(game) {
      const container = document.getElementById('detail-scenario-bundles-container');
      if (!container) return;

      if (!game.hasConsole) {
        container.innerHTML = `
          <div class="bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-emerald-500/10 rounded-[28px] p-6 border border-blue-500/20 shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center space-x-3.5">
              <div class="w-10 h-10 rounded-2xl bg-blue-600/20 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0">
                <span class="text-xl">⚡</span>
              </div>
              <div>
                <div class="font-extrabold text-sm sm:text-base text-zinc-900 dark:text-white">${t('noConsoleTitle')}</div>
                <div class="text-xs text-zinc-500 dark:text-zinc-400 mt-0.5">${t('noConsoleDesc')}</div>
              </div>
            </div>
            <button onclick="setDetailTab('trainers')" class="px-5 py-2.5 rounded-full bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition-all shadow-md shrink-0 flex items-center gap-1.5 cursor-pointer">
              <span>${t('goToTrainers')}</span>
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
            </button>
          </div>
        `;
        return;
      }

      const bundles = (game.scenarioBundles && game.scenarioBundles.length > 0)
        ? game.scenarioBundles
        : generateDynamicBundles(game);

      if (!bundles || bundles.length === 0) {
        container.innerHTML = '';
        return;
      }

      const shortcutKey = (game.consoleShortcut || '~').split(' ')[0] || '~';

      let cardsHtml = '';
      bundles.forEach((b, idx) => {
        let gradientBorder = 'border-blue-500/30 hover:border-blue-500';
        let gradientBg = 'from-blue-500/5 to-cyan-500/5';
        let badgeColor = 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20';
        let btnGradient = 'from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 shadow-blue-500/25';
        let icon = '🚀';
        let bName = b.name;
        let bTag = b.tag || 'L-MOD';
        let bDesc = b.desc;

        if (b.type === 'starter' || idx === 0) {
          bName = t('scenarioStarterPack');
          bTag = t('scenarioStarterTag');
          bDesc = t('scenarioStarterDesc');
        } else if (b.type === 'salvation' || idx === 1) {
          gradientBorder = 'border-purple-500/30 hover:border-purple-500';
          gradientBg = 'from-purple-500/5 to-pink-500/5';
          badgeColor = 'bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20';
          btnGradient = 'from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 shadow-purple-500/25';
          icon = '💖';
          bName = t('scenarioStoryRedeem');
          bTag = t('scenarioStoryTag');
          bDesc = t('scenarioStoryDesc');
        } else if (b.type === 'arsenal' || idx === 2) {
          gradientBorder = 'border-amber-500/30 hover:border-amber-500';
          gradientBg = 'from-amber-500/5 to-orange-500/5';
          badgeColor = 'bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20';
          btnGradient = 'from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 shadow-amber-500/25';
          icon = '⚔️';
          bName = t('scenarioEndgameArsenal');
          bTag = t('scenarioEndgameTag');
          bDesc = t('scenarioEndgameDesc');
        }

        const highlightsList = (b.highlights || []).map(hl => `
          <div class="flex items-start gap-1.5 text-xs text-zinc-700 dark:text-zinc-300">
            <svg class="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
            <span class="leading-snug">${hl}</span>
          </div>
        `).join('');

        const previewLines = b.code ? b.code.split('\\n').filter(l => l.trim() && !l.trim().startsWith('--') && !l.trim().startsWith('//') && !l.trim().startsWith('#')).slice(0, 3) : [];

        cardsHtml += `
          <div class="bg-gradient-to-b ${gradientBg} bg-white dark:bg-[#141518] rounded-[24px] p-5 sm:p-6 border ${gradientBorder} shadow-sm hover:shadow-md transition-all flex flex-col justify-between space-y-4 group">
            <div class="space-y-3">
              <div class="flex items-center justify-between gap-2 flex-wrap">
                <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${badgeColor}">
                  ${bTag}
                </span>
                <span class="text-[10px] text-zinc-400 font-mono">1-Click Bundle</span>
              </div>
              <div>
                <h4 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white flex items-center gap-1.5">
                  <span>${icon}</span>
                  <span>${bName}</span>
                </h4>
                <p class="text-xs text-zinc-500 dark:text-zinc-400 mt-1 leading-relaxed min-h-[36px]">
                  ${bDesc}
                </p>
              </div>
              <div class="pt-2 border-t border-zinc-100 dark:border-white/5 space-y-2">
                <div class="text-[11px] font-bold text-zinc-400 uppercase tracking-wider">${t('scenarioFeaturesLabel') || 'Features Included:'}</div>
                <div class="space-y-1.5">
                  ${highlightsList}
                </div>
              </div>
              ${previewLines.length > 0 ? `
                <div class="bg-zinc-100/80 dark:bg-black/40 rounded-xl p-2.5 font-mono text-[10px] text-zinc-600 dark:text-zinc-400 border border-zinc-200/60 dark:border-white/5 overflow-hidden">
                  <div class="text-[9px] text-zinc-400 mb-1 font-sans">${t('codePreviewLabel') || 'Preview:'}</div>
                  ${previewLines.map(pl => `<div class="truncate text-blue-600 dark:text-blue-400 font-semibold">${pl}</div>`).join('')}
                  <div class="text-[9px] text-zinc-400 mt-1 italic font-sans">${t('codeFullBundlePack') || '+ Complete Bundle Script'}</div>
                </div>
              ` : ''}
            </div>

            <div class="pt-2">
              <button 
                onclick="copyScenarioBundle('${game.id}', '${b.id}')"
                class="w-full py-3 px-4 rounded-xl font-bold text-xs text-white bg-gradient-to-r ${btnGradient} shadow-md flex items-center justify-center gap-2 transition-all transform group-hover:scale-[1.02] active:scale-95 cursor-pointer"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"></path></svg>
                <span>${t('copyBundleBtn')}</span>
              </button>
            </div>
          </div>
        `;
      });

      container.innerHTML = `
        <div class="bg-white dark:bg-[#141518] rounded-[28px] p-6 border border-zinc-200/80 dark:border-white/10 shadow-sm space-y-5">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-zinc-100 dark:border-white/5">
            <div>
              <div class="flex items-center gap-2 flex-wrap mb-1">
                <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
                <h3 class="text-base sm:text-lg font-extrabold text-zinc-900 dark:text-white">
                  ${t('scenarioTitle') || '老L·极客推荐场景套餐 (小白 10 秒一键爽到)'}
                </h3>
                <span class="text-xs bg-emerald-50 dark:bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2.5 py-0.5 rounded-full font-bold border border-emerald-500/20">
                  ${t('scenarioPatchTag') || '100% 官方最新补丁实测'}
                </span>
              </div>
              <p class="text-xs text-zinc-500 dark:text-zinc-400">
                ${t('scenarioSubtitle') || '针对不同游玩场景整套打包，进游戏呼出控制台粘贴一次即可整套生效。'}
              </p>
            </div>
            <div class="flex items-center gap-2 text-xs text-zinc-400 shrink-0">
              <span>${t('consoleShortcutLabel') || '呼出键:'}</span>
              <code class="px-2 py-1 rounded-md bg-zinc-100 dark:bg-white/10 text-blue-600 dark:text-blue-400 font-mono font-bold">${shortcutKey}</code>
            </div>
          </div>

          <!-- 3-Column Responsive Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            ${cardsHtml}
          </div>

          <!-- Advanced usage tip -->
          <div class="flex items-center gap-2 text-xs text-zinc-500 dark:text-zinc-400 bg-zinc-50 dark:bg-black/30 p-3 rounded-xl border border-zinc-200/60 dark:border-white/5">
            <svg class="w-4 h-4 text-blue-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <span>${t('scenarioAdvancedTip') || '极客贴士：代码按官方控制台语法封装，点击按钮直接复制后，在游戏里呼出控制台按 <b>Ctrl+V</b>（或右键）回车执行即可！'}</span>
          </div>
        </div>
      `;
    }"""

if old_scenario_bundles in content:
    content = content.replace(old_scenario_bundles, new_scenario_bundles)
    print("✅ Injected dynamic renderScenarioBundles()")
else:
    print("⚠️ Could not find exact old_scenario_bundles")

# 9. copyScenarioBundle toast
content = content.replace(
    'copyText(bundle.code, `【${bundle.name}】已复制！进入游戏按 ${shortcutKey} 键直接粘贴一次即可整套生效！`);',
    'copyText(bundle.code, t(\'bundleCopiedToast\'));'
)

# 10. Trainer Modal & Mod Modal dynamic titles & subtitles
content = content.replace(
    'if (titleEl) titleEl.innerText = `《${locTitle}》修改器下载已在浏览器拉起`;',
    'if (titleEl) titleEl.innerText = (t(\'trainerModalTitle\') || \'《{title}》修改器下载已在浏览器拉起\').replace(\'{title}\', locTitle);'
)
content = content.replace(
    "if (titleEl) titleEl.innerText = `《${mod.title}》${isDirect ? '下载已在浏览器拉起' : '转存与官方页面已直达'}`;",
    "if (titleEl) titleEl.innerText = isDirect ? (t('modModalDirectTitle') || '《{title}》下载已在浏览器拉起').replace('{title}', mod.title) : (t('modModalOfficialTitle') || '《{title}》转存与官方页面已直达').replace('{title}', mod.title);"
)
content = content.replace(
    "badgeEl.innerText = isDirect ? '极速真直连 (免科学上网)' : '精选转存 / 官方源';",
    "badgeEl.innerText = isDirect ? t('modModalDirectBadge') : t('modModalOfficialBadge');"
)
content = content.replace(
    "subtitleEl.innerText = isDirect ? '文件正在保存中 · 附全中文安装路径与部署指引' : '已为你直达安全下载源 · 附全中文部署指引';",
    "subtitleEl.innerText = isDirect ? t('modModalDirectSubtitle') : t('modModalOfficialSubtitle');"
)

# 11. Toasts in actions
content = content.replace(
    "showToast('已重新拉起修改器压缩包下载！');",
    "showToast(t('trainerRetriggerToast'));"
)
content = content.replace(
    "copyText(cmd, 'Windows Defender 10秒放行指令已复制！以管理员身份运行 PowerShell 粘贴回车即可。');",
    "copyText(cmd, t('cmdCopiedToast'));"
)
content = content.replace(
    "showToast('已重新拉起 MOD 文件下载！');",
    "showToast(t('modRetriggerToast'));"
)
content = content.replace(
    "copyText(p, 'MOD 部署路径已复制到剪贴板！可在资源管理器地址栏粘贴直达。');",
    "copyText(p, t('pathCopiedToast'));"
)
content = content.replace(
    "showToast('已开始下载一键开门脚本！放入游戏根目录双击即可');",
    "showToast(t('batDownloadedToast'));"
)
content = content.replace(
    "copyText(batCode, '批处理代码已复制！新建文本文件粘贴并改名为 .bat 即可使用');",
    "copyText(batCode, t('batCopiedToast'));"
)
content = content.replace(
    "copyText(secret, `暗号【${secret}】已复制！请前往避坑雷达群获取连夜更新包与坏档急救！`);",
    "copyText(secret, t('toastSecretCopied'));"
)

# 12. Dynamic Bat generator
old_bat_generator = """    function generateDynamicBatScript(game) {
      if (game.batScript) return game.batScript;
      const shortcut = game.consoleShortcut || '~ (波浪键)';
      return `@echo off
chcp 65001 >nul
title 【老L·单机避坑局】${game.title} 控制台排错与激活助手
echo ========================================================
echo   【老L·单机避坑局】《${game.title}》控制台助手
echo   官方底层机制 · 100%% 开源透明 · 零木马报毒
echo ========================================================
echo.
echo [*] 正在检查当前游戏运行环境...
echo [i] 请将本脚本放在游戏安装根目录运行。
echo [i] 常用控制台呼出快捷键：${shortcut}
echo.
echo ========================================================
echo  [√] 准备就绪！启动游戏后按下 ${shortcut}
echo      直接粘贴老L推荐套餐指令即可畅享！
echo ========================================================
echo.
pause`;
    }"""

new_bat_generator = """    function generateDynamicBatScript(game) {
      if (game.batScript && currentLang.startsWith('zh')) return game.batScript;
      const shortcut = game.consoleShortcut ? game.consoleShortcut.split(' ')[0] : '~';
      const locTitle = (game.titles && game.titles[currentLang]) ? game.titles[currentLang] : game.title;
      if (currentLang.startsWith('zh')) {
        return `@echo off
chcp 65001 >nul
title 【老L·单机避坑局】${locTitle} 控制台排错与激活助手
echo ========================================================
echo   【老L·单机避坑局】《${locTitle}》控制台助手
echo   官方底层机制 · 100%% 开源透明 · 零木马报毒
echo ========================================================
echo.
echo [*] 正在检查当前游戏运行环境...
echo [i] 请将本脚本放在游戏安装根目录运行。
echo [i] 常用控制台呼出快捷键：${shortcut}
echo.
echo ========================================================
echo  [√] 准备就绪！启动游戏后按下 ${shortcut}
echo      直接粘贴老L推荐套餐指令即可畅享！
echo ========================================================
echo.
pause`;
      } else {
        return `@echo off
chcp 65001 >nul
title [L-MOD Vault] ${locTitle} Console Setup Helper
echo ========================================================
echo   [L-MOD Vault] ${locTitle} Console Activator
echo   Official Native Engine - 100%% Open Source - Zero Malware
echo ========================================================
echo.
echo [*] Verifying game installation directory...
echo [i] Please run this batch script inside the game root directory.
echo [i] Console activation hotkey: ${shortcut}
echo.
echo ========================================================
echo  [√] Environment Ready! Launch game, press ${shortcut}
echo      and paste L-MOD bundle commands to enjoy!
echo ========================================================
echo.
pause`;
      }
    }"""

if old_bat_generator in content:
    content = content.replace(old_bat_generator, new_bat_generator)
    print("✅ Injected dynamic generateDynamicBatScript()")
else:
    print("⚠️ Could not find exact old_bat_generator")

# 13. Update init() to call initLanguage()
old_init = """    function init() {
      initTheme();
      if (window.GAMES_DATA) allGames = window.GAMES_DATA;
      else if (window.GAMES_DATABASE) allGames = window.GAMES_DATABASE;
      if (window.TRANSLATIONS_DATA) translations = window.TRANSLATIONS_DATA;
      renderUI();
      renderGames();
      renderRecentSidebar();
      handleRouting();
    }"""

new_init = """    function init() {
      initTheme();
      if (window.GAMES_DATA) allGames = window.GAMES_DATA;
      else if (window.GAMES_DATABASE) allGames = window.GAMES_DATABASE;
      if (window.TRANSLATIONS_DATA) translations = window.TRANSLATIONS_DATA;
      initLanguage();
      renderUI();
      renderGames();
      renderRecentSidebar();
      handleRouting();
    }"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("✅ Updated init() with initLanguage()")
else:
    print("⚠️ Could not find exact old_init")

# 14. Update Status Filter Toasts
content = content.replace(
    "showToast('已筛选：🔴 坏档暂停更新高危游戏');",
    "showToast(t('filterToastRed'));"
)
content = content.replace(
    "showToast('已筛选：🟡 需更新前置/补丁适配游戏');",
    "showToast(t('filterToastYellow'));"
)
content = content.replace(
    "showToast('已筛选：🟢 完美兼容实测通过游戏');",
    "showToast(t('filterToastGreen'));"
)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Finished refactoring public/index.html JavaScript.")
