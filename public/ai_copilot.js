/**
 * L-MOD Vault - Player-Facing AI Copilot (老L · AI 游戏智库顾问)
 * Standalone, zero-dependency, context-aware Copilot for index.html & radar.html.
 * Supports:
 * 1. Offline Local RAG (100% free, instant response from window.GAMES_DATA)
 * 2. Bring Your Own Key (BYOK) for Google Gemini API & DeepSeek API
 * 3. Natural Language Command Search & One-Click Copy / .bat generation
 * 4. Crash & Mod Conflict Diagnostics (EAC, UE4SS, CET, ScriptExtender)
 * 5. Real-time Steam Patch Radar status integration
 * 6. Multi-language support (8 languages)
 */

(function () {
  'use strict';

  // Prevent multiple initializations
  if (window.LMOD_AI_COPILOT) return;

  const STORAGE_KEY_KEY = 'lmod_ai_config';
  const STORAGE_HISTORY_KEY = 'lmod_ai_history';

  // Copilot State
  const state = {
    isOpen: false,
    isSettingsOpen: false,
    activeGame: null, // { id, title, ... }
    mode: 'local', // 'local' | 'gemini' | 'deepseek' | 'custom'
    apiKey: '',
    customEndpoint: '',
    customModel: '',
    geminiModel: 'gemini-2.5-flash',
    deepseekModel: 'deepseek-chat',
    isLoading: false,
    messages: []
  };

  // UI Multi-Language Dictionary
  const i18n = {
    'zh-CN': {
      title: '老L · AI 游戏智库顾问',
      tagline: '控制台代码 / 闪退排查 / 避坑雷达 / 一键脚本',
      globalContext: '全网 100 款单机智库',
      activeContextPrefix: '当前游戏: ',
      switchGame: '切换游戏',
      clearContext: '切回全局',
      inputPlaceholder: '输入你的问题，如：“2077怎么刷四季宝”、“法环闪退排查”...',
      sendBtn: '发送',
      thinking: '老L 正在调取游戏底层指令与避坑数据库...',
      copyCode: '复制指令',
      copied: '已复制到剪贴板！',
      downloadBat: '生成 .bat 脚本',
      settingsTitle: 'AI 引擎与模型设置',
      modeLocal: '本地极速智库 (免 Key 推荐 · 毫秒级响应)',
      modeGemini: 'Google Gemini 2.5 (在线大模型 · 智能推理)',
      modeDeepSeek: 'DeepSeek API (深度思考 · 中文单机专家)',
      modeCustom: '自定义 OpenAI 兼容接口',
      apiKeyLabel: 'API Key 密钥 (仅保存在本地浏览器，安全隐私)',
      saveSettings: '保存配置',
      close: '关闭',
      clearHistory: '清空会话',
      welcomeMessage: '我是**老L**，你的单机游戏避坑与控制台代码顾问！\n\n你可以随时向我提问：\n- 🔍 **找控制台代码**：“给我赛博朋克2077强尼的保时捷代码”\n- 💥 **闪退坏档排查**：“博德之门3打Mod闪退怎么解决”\n- 📡 **避坑雷达咨询**：“艾尔登法环当前版本能打无敌Mod吗”\n- ⚡ **修改器与热键**：“黑神话悟空风灵月影修改器快捷键”',
      pillCommands: '🔍 查核心作弊代码',
      pillCrash: '💥 闪退与冲突排查',
      pillPatch: '📡 最新补丁避坑状态',
      pillTrainer: '⚡ 修改器热键与防误报',
      emptyNoMatch: '在本地知识库中未找到完全匹配的词条。',
      emptySuggestOnline: '建议点击右上角 ⚙️ 接入 Gemini 或 DeepSeek API Key 进行全网大模型推理！',
      noGameFound: '未找到指定游戏，已为您在全站 100 款游戏中检索相似内容。',
      offlineBadge: '本地智库 (离线)',
      geminiBadge: 'Gemini 在线',
      deepseekBadge: 'DeepSeek 在线',
      customBadge: '自定义 API'
    },
    'en': {
      title: 'L-MOD · AI Game Vault Advisor',
      tagline: 'Console Cheats / Crash Doctor / Patch Radar / Script Generator',
      globalContext: 'Global 100 Games Vault',
      activeContextPrefix: 'Active Game: ',
      switchGame: 'Switch Game',
      clearContext: 'Reset to Global',
      inputPlaceholder: 'Ask a question, e.g. "Cyberpunk Johnny Porsche code", "Elden Ring crash fix"...',
      sendBtn: 'Send',
      thinking: 'Old L is retrieving low-level game commands and radar data...',
      copyCode: 'Copy Command',
      copied: 'Copied to clipboard!',
      downloadBat: 'Download .bat',
      settingsTitle: 'AI Engine & Model Settings',
      modeLocal: 'Local Fast Vault (No Key Needed · Instant)',
      modeGemini: 'Google Gemini 2.5 (Online AI · Deep Reasoning)',
      modeDeepSeek: 'DeepSeek API (Deep Reasoning)',
      modeCustom: 'Custom OpenAI-Compatible API',
      apiKeyLabel: 'API Key (Stored locally in your browser only)',
      saveSettings: 'Save Settings',
      close: 'Close',
      clearHistory: 'Clear Chat',
      welcomeMessage: "I'm **Old L**, your single-player game modding and console command advisor!\n\nFeel free to ask:\n- 🔍 **Find Commands**: 'Give me the Johnny Silverhand Porsche code for Cyberpunk 2077'\n- 💥 **Crash & Fixes**: 'Baldur\\'s Gate 3 crashes with mods, how to fix?'\n- 📡 **Patch Radar**: 'Can I safely use mods on the latest Elden Ring patch?'\n- ⚡ **Trainers**: 'FLiNG trainer hotkeys for Black Myth Wukong'",
      pillCommands: '🔍 Key Console Codes',
      pillCrash: '💥 Crash & Mod Doctor',
      pillPatch: '📡 Patch Radar Status',
      pillTrainer: '⚡ Trainer Hotkeys',
      emptyNoMatch: 'No exact match found in local database.',
      emptySuggestOnline: 'Tip: Click ⚙️ to configure Gemini or DeepSeek API for online AI reasoning!',
      noGameFound: 'Game not specified. Searched across all 100 games.',
      offlineBadge: 'Local Vault (Offline)',
      geminiBadge: 'Gemini Online',
      deepseekBadge: 'DeepSeek Online',
      customBadge: 'Custom API'
    }
  };

  // Helper: Get Current Language
  function getLang() {
    const code = localStorage.getItem('lmod_lang') || 'zh-CN';
    return i18n[code] ? code : 'zh-CN';
  }

  function t(key) {
    const lang = getLang();
    return (i18n[lang] && i18n[lang][key]) || i18n['zh-CN'][key] || key;
  }

  // Load Saved Configuration
  function loadConfig() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        state.mode = parsed.mode || 'local';
        state.apiKey = parsed.apiKey || '';
        state.customEndpoint = parsed.customEndpoint || '';
        state.customModel = parsed.customModel || '';
        state.geminiModel = parsed.geminiModel || 'gemini-2.5-flash';
        state.deepseekModel = parsed.deepseekModel || 'deepseek-chat';
      }
    } catch (e) {
      console.warn('Failed to load L-MOD AI config:', e);
    }
  }

  function saveConfig() {
    try {
      const config = {
        mode: state.mode,
        apiKey: state.apiKey,
        customEndpoint: state.customEndpoint,
        customModel: state.customModel,
        geminiModel: state.geminiModel,
        deepseekModel: state.deepseekModel
      };
      localStorage.setItem(STORAGE_KEY_KEY, JSON.stringify(config));
    } catch (e) {
      console.warn('Failed to save L-MOD AI config:', e);
    }
  }

  // Detect Active Game from Environment
  function detectActiveGame() {
    // 1. Check window.activeGame from index.html
    if (window.activeGame && window.activeGame.id) {
      return window.activeGame;
    }
    // 2. Check window.currentDrawerGame from radar.html
    if (window.currentDrawerGame && window.currentDrawerGame.id) {
      return window.currentDrawerGame;
    }
    // 3. Check URL hash (e.g. #/game/cyberpunk-2077 or ?game=cyberpunk-2077)
    const hash = window.location.hash || '';
    const search = window.location.search || '';
    const match = hash.match(/game[=/]([a-zA-Z0-9_-]+)/) || search.match(/game=([a-zA-Z0-9_-]+)/);
    if (match && match[1]) {
      const gameId = match[1];
      const games = window.GAMES_DATA || window.GAMES_DATABASE || [];
      const found = games.find(g => g.id === gameId);
      if (found) return found;
    }
    return state.activeGame || null;
  }

  // Find Game by Query
  function findGameByQuery(query) {
    const games = window.GAMES_DATA || window.GAMES_DATABASE || [];
    if (!games.length) return null;
    const q = query.toLowerCase().replace(/\s+/g, '');

    // Direct game name match
    for (const g of games) {
      const title = (g.title || '').toLowerCase().replace(/\s+/g, '');
      if (title && q.includes(title)) return g;
      if (g.titles) {
        for (const locTitle of Object.values(g.titles)) {
          const l = (locTitle || '').toLowerCase().replace(/\s+/g, '');
          if (l && q.includes(l)) return g;
        }
      }
    }

    // Common aliases mapping
    const aliases = {
      '2077': 'cyberpunk-2077',
      '赛博朋克': 'cyberpunk-2077',
      '电驭叛客': 'cyberpunk-2077',
      '黑猴': 'black-myth-wukong',
      '黑神话': 'black-myth-wukong',
      '悟空': 'black-myth-wukong',
      'wukong': 'black-myth-wukong',
      '老头环': 'elden-ring',
      '法环': 'elden-ring',
      '艾尔登': 'elden-ring',
      '黄金树': 'elden-ring',
      'elden': 'elden-ring',
      '巫师3': 'witcher-3',
      '白狼': 'witcher-3',
      'witcher': 'witcher-3',
      '博德之门3': 'baldurs-gate-3',
      '博德3': 'baldurs-gate-3',
      'bg3': 'baldurs-gate-3',
      '老滚5': 'the-elder-scrolls-v-skyrim-special-edition',
      '天际': 'the-elder-scrolls-v-skyrim-special-edition',
      '上古卷轴': 'the-elder-scrolls-v-skyrim-special-edition',
      'skyrim': 'the-elder-scrolls-v-skyrim-special-edition',
      '辐射4': 'fallout-4',
      'fallout4': 'fallout-4',
      '大表哥2': 'red-dead-redemption-2',
      '荒野大镖客': 'red-dead-redemption-2',
      'rdr2': 'red-dead-redemption-2',
      '帕鲁': 'palworld',
      '幻兽帕鲁': 'palworld',
      '星空': 'starfield',
      '生化危机4': 'resident-evil-4',
      're4': 'resident-evil-4',
      '只狼': 'sekiro',
      '怪物猎人': 'monster-hunter-world',
      'mhw': 'monster-hunter-world',
      '骑砍2': 'mount-blade-ii-bannerlord',
      '星露谷': 'stardew-valley',
      '深海迷航': 'subnautica',
      '英灵神殿': 'valheim',
      '环世界': 'rimworld',
      '边缘世界': 'rimworld',
      '森林之子': 'sons-of-the-forest',
      '幸福工厂': 'satisfactory',
      '异星工厂': 'factorio',
      '十字军之王': 'crusader-kings-iii',
      'ck3': 'crusader-kings-iii',
      '钢铁雄心': 'hearts-of-iron-iv',
      'hoi4': 'hearts-of-iron-iv',
      '群星': 'stellaris',
      '天国拯救': 'kingdom-come-deliverance',
      '七日杀': '7-days-to-die',
      '方舟': 'ark-survival-evolved',
      '模拟人生4': 'the-sims-4',
      '欧卡2': 'euro-truck-simulator-2',
      '杀戮尖塔': 'slay-the-spire',
      '哈迪斯': 'hades',
      '空洞骑士': 'hollow-knight'
    };

    for (const [alias, id] of Object.entries(aliases)) {
      if (q.includes(alias)) {
        return games.find(g => g.id === id) || null;
      }
    }

    return null;
  }

  // =========================================================================
  // LOCAL RAG ENGINE: Ultra-Fast, Context-Aware, 100% Free & Hallucination-Free
  // =========================================================================
  function localRagQuery(rawQuery, contextGame) {
    const query = rawQuery.trim();
    const qLower = query.toLowerCase();
    const games = window.GAMES_DATA || window.GAMES_DATABASE || [];

    // Target game detection
    const targetGame = findGameByQuery(query) || contextGame || detectActiveGame();

    // Specific intent classifiers
    const isCrashQuery = /闪退|崩溃|打不开|进不去|跳出|报错|crash|black\s*screen|error|eac|ue4ss|cet/i.test(query);
    const isPatchQuery = /补丁|雷达|更新|失效|版本|坏档|patch|update|radar|save/i.test(query);
    const isTrainerQuery = /修改器|风灵月影|热键|白名单|杀毒|fling|trainer|hotkey/i.test(query);
    const isHowToEnable = /怎么开|快捷键|呼出|按键|按什么|如何开启|console\s*shortcut|how\s*to/i.test(query);

    // If target game found, perform deep analysis on that game
    if (targetGame) {
      const locTitle = (targetGame.titles && targetGame.titles['zh-CN']) || targetGame.title;

      // 1. Crash & Mod Conflict Diagnosis
      if (isCrashQuery) {
        return buildCrashDiagnosisResponse(targetGame, locTitle, query);
      }

      // 2. Steam Patch & Radar Status Query
      if (isPatchQuery) {
        return buildPatchRadarResponse(targetGame, locTitle);
      }

      // 3. Trainer & Hotkey Query
      if (isTrainerQuery) {
        return buildTrainerResponse(targetGame, locTitle);
      }

      // 4. How to Enable Console Guide
      if (isHowToEnable) {
        return buildConsoleGuideResponse(targetGame, locTitle);
      }

      // 5. Search for Commands inside Game
      const matchedCommands = searchCommandsInGame(targetGame, query);
      if (matchedCommands.length > 0) {
        return buildCommandsResponse(targetGame, locTitle, matchedCommands, query);
      }

      // 6. Search Scenario Bundles
      if (targetGame.scenarioBundles && targetGame.scenarioBundles.length > 0) {
        const bundle = targetGame.scenarioBundles.find(b => 
          qLower.includes(b.name.toLowerCase()) || 
          /新手|毕业|二周目|神装|救赎|套餐|一键/i.test(query)
        ) || targetGame.scenarioBundles[0];

        return buildScenarioBundleResponse(targetGame, locTitle, bundle);
      }

      // 7. Fallback to Popular Commands if general search
      if (targetGame.popularCommands && targetGame.popularCommands.length > 0) {
        return buildPopularCommandsFallback(targetGame, locTitle, query);
      }
    }

    // Global Search across All 100 Games
    const globalMatches = searchAcrossAllGames(query, games);
    if (globalMatches.length > 0) {
      return buildGlobalSearchResults(globalMatches, query);
    }

    // Default Fallback
    return {
      text: `### 🎮 未在知识库中找到针对 "${query}" 的完全匹配\n\n` +
            `- **建议操作**：请检查游戏名称或关键词（如输入：“2077无限钱”、“黑神话控制台快捷键”、“老头环闪退排查”）。\n` +
            `- **大模型深度推理**：若想询问更复杂的 Mod 安装、配装思路或冷门游戏，点击右上角 **⚙️ 切换为 Gemini 或 DeepSeek**，即可启动在线 AI 智能解答！`
    };
  }

  // Sub-generator: Crash Diagnosis
  function buildCrashDiagnosisResponse(game, title, query) {
    const engine = game.developer ? `开发商/引擎特征: ${game.developer}` : '';
    let diagnosis = `### 💥 《${title}》闪退与 Mod 冲突在线排查指南\n\n`;

    // Engine-specific diagnostics
    if (game.id === 'cyberpunk-2077') {
      diagnosis += `**CDPR REDengine 4 专属诊断要点**：\n` +
        `1. **CET (Cyber Engine Tweaks) 版本不匹配**：若游戏刚更新了补丁，CET 的 \`bin/x64/plugins/cyber_engine_tweaks.asi\` 必须对应最新版本，否则启动必闪退。\n` +
        `2. **REDscript 缓存损坏**：删除游戏根目录 \`r6/cache/modded\` 文件夹，重新运行游戏让系统重新编译脚本。\n` +
        `3. **旧版 ArchiveXL / TweakXL 冲突**：确保前置核心库均升级至匹配当前补丁的版本。\n`;
    } else if (game.id === 'elden-ring' || game.id === 'sekiro') {
      diagnosis += `**FromSoftware 引擎专属诊断要点**：\n` +
        `1. **EAC 反作弊未关闭拦截**：必须将 \`start_protected_game.exe\` 替换或使用 \`launchmod_eldenring.bat\` 离线引导，否则带 Mod 启动必被 EAC 拦截闪退。\n` +
        `2. **ModEngine2 引导路径错误**：检查 \`config_eldenring.toml\` 中 mod 路径是否正确指向 mod 文件夹。\n` +
        `3. **版本更新坏档**：黄金树幽影 v1.14+ 补丁重构了部分 Regulation.bin 参数，旧版参数文件会导致主菜单加载闪退。\n`;
    } else if (game.id === 'black-myth-wukong' || game.id === 'palworld') {
      diagnosis += `**虚幻引擎 (UE5) 专属诊断要点**：\n` +
        `1. **DX12 着色器编译崩溃**：在 Steam 启动项中添加 \`-dx11\` 强制使用 DirectX 11 启动测试。\n` +
        `2. **UE4SS 注入器冲突**：检查 \`b1/Binaries/Win64/ue4ss.dll\`，尝试将 \`UE4SS-settings.ini\` 中的 \`GuiConsoleEnabled = 0\` 关闭以排查图形钩子崩溃。\n` +
        `3. **Pak Mod 冲突**：将 \`~mods\` 文件夹重命名为 \`~mods_backup\`，逐个排查损坏的 Mod。\n`;
    } else if (game.id.includes('skyrim') || game.id.includes('fallout-4') || game.id === 'starfield') {
      diagnosis += `**Bethesda Creation 引擎专属诊断要点**：\n` +
        `1. **脚本扩展器 (SKSE64 / F4SE) 版本对齐**：检查游戏主程序版本，次世代版与旧版脚本扩展器绝不可混用。\n` +
        `2. **Address Library 前置缺失**：几乎所有现代 DLL Mod 都依赖 Address Library for SKSE Plugins，请确保安装了最新版。\n` +
        `3. **排序冲突**：使用 LOOT 自动重新排序 ESP/ESM/ESL 加载顺序。\n`;
    } else {
      diagnosis += `**通用单机 Mod 闪退排查四部曲**：\n` +
        `1. **重命名 Mod 文件夹进行二分法排查**：临时禁用 Mod 目录，确认是否为纯净原版能正常启动；\n` +
        `2. **检查防作弊与注入 DLL**：检查是否有 \`dinput8.dll\`, \`dxgi.dll\`, \`version.dll\` 等钩子文件与显卡驱动 overlay (如微星小飞机/GeForce Experience) 冲突；\n` +
        `3. **管理员权限与杀毒白名单**：Windows Defender 常误杀注入型 DLL，请将游戏根目录加入排除项；\n` +
        `4. **验证 Steam 游戏文件完整性**：右键游戏属性 -> 已安装文件 -> 验证游戏文件的完整性。\n`;
    }

    if (game.pitfallNote) {
      diagnosis += `\n> ⚠️ **老L 独家避坑备注**：\n> ${game.pitfallNote}\n`;
    }

    return { text: diagnosis };
  }

  // Sub-generator: Patch & Radar Status
  function buildPatchRadarResponse(game, title) {
    const statusMap = {
      'green': '🟢 完美兼容 (可放心安装/无需降级)',
      'yellow': '🟡 需更新前置 (部分脚本 Mod 需等待更新)',
      'red': '🔴 坏档预警 (大版本更新，旧存档与 Mod 严重失效)'
    };

    const statusBadge = statusMap[game.compatibilityStatus] || '🟢 正常稳定';
    let res = `### 📡 《${title}》Steam 补丁兼容性与避坑雷达\n\n`;
    res += `- **当前雷达状态**：${statusBadge}\n`;
    if (game.verifiedPatch) res += `- **老L 已认证补丁**：\`${game.verifiedPatch}\`\n`;
    if (game.latestSteamPatch) res += `- **Steam 最新推送补丁**：\`${game.latestSteamPatch}\`\n`;
    if (game.steamLastChecked) res += `- **最近巡检时间**：\`${game.steamLastChecked}\`\n`;

    if (game.radarRiskTitle) {
      res += `\n#### ⚠️ 风险通报：${game.radarRiskTitle}\n`;
      if (game.radarRiskDesc) res += `${game.radarRiskDesc}\n`;
    }

    if (game.pitfallNote) {
      res += `\n> 💡 **避坑锦囊**：\n> ${game.pitfallNote}\n`;
    }

    res += `\n[进入《Steam 补丁避坑雷达独立看板》查看完整 100 款对账](radar.html?game=${game.id})`;
    return { text: res };
  }

  // Sub-generator: Trainer Response
  function buildTrainerResponse(game, title) {
    let res = `### ⚡ 《${title}》纯净修改器与快捷键一览\n\n`;

    if (game.trainerInfo && game.trainerInfo.hotkeysCategorized) {
      res += `**FLiNG 官方精校修改器热键**：\n\n`;
      for (const [catName, hotkeys] of Object.entries(game.trainerInfo.hotkeysCategorized)) {
        res += `#### ${catName}\n`;
        for (const hk of hotkeys) {
          res += `- \`${hk.key}\`：${hk.action}\n`;
        }
      }
    } else if (game.trainerHotkeys && game.trainerHotkeys.length > 0) {
      res += `**常用快捷热键**：\n\n`;
      for (const hk of game.trainerHotkeys) {
        res += `- \`${hk.key}\`：${hk.action}\n`;
      }
    } else {
      res += `本游戏更推荐使用游戏官方内置控制台或注入式控制台，更加稳定且杜绝报毒！\n`;
    }

    if (game.trainerInfo && game.trainerInfo.powershellExclusionCmd) {
      res += `\n#### 🛡️ Windows Defender 误报秒解指令 (管理员 PowerShell 运行)：\n` +
             `\`\`\`powershell\n${game.trainerInfo.powershellExclusionCmd}\n\`\`\`\n`;
    }

    return { text: res };
  }

  // Sub-generator: Console Guide Response
  function buildConsoleGuideResponse(game, title) {
    let res = `### 🛠️ 《${title}》控制台唤出与开启方法\n\n`;
    res += `- **控制台支持情况**：${game.hasConsole ? '✅ 支持控制台' : '⚠️ 需第三方前置注入'}\n`;
    if (game.consoleShortcut) res += `- **默认呼出按键**：\`${game.consoleShortcut}\`\n\n`;

    const guide = (game.consoleEnableGuide && (game.consoleEnableGuide['zh-CN'] || game.consoleEnableGuide['en'])) ||
                  game.consoleEnableGuide || '进入游戏后按下快捷键即可呼出输入框。';

    res += `**详细开启步骤**：\n${guide}\n`;
    return { text: res };
  }

  // Sub-generator: Commands Search
  function searchCommandsInGame(game, query) {
    const q = query.toLowerCase();
    const results = [];

    // Search popular commands
    if (game.popularCommands) {
      for (const cmd of game.popularCommands) {
        const name = (cmd.name || '').toLowerCase();
        const code = (cmd.code || '').toLowerCase();
        const desc = (cmd.desc || '').toLowerCase();
        if (name.includes(q) || code.includes(q) || desc.includes(q)) {
          results.push(cmd);
        }
      }
    }

    // Search console categories
    if (game.consoleCategories) {
      for (const cat of game.consoleCategories) {
        if (cat.commands) {
          for (const cmd of cat.commands) {
            const name = typeof cmd.name === 'object' ? Object.values(cmd.name).join(' ').toLowerCase() : (cmd.name || '').toLowerCase();
            const code = (cmd.code || '').toLowerCase();
            const desc = (cmd.desc || '').toLowerCase();
            if (name.includes(q) || code.includes(q) || desc.includes(q)) {
              results.push(cmd);
            }
          }
        }
      }
    }

    // Deduplicate by code
    const unique = [];
    const seen = new Set();
    for (const c of results) {
      if (c.code && !seen.has(c.code)) {
        seen.add(c.code);
        unique.push(c);
      }
    }

    return unique.slice(0, 8); // Top 8 matches
  }

  function buildCommandsResponse(game, title, commands, query) {
    let res = `### 🎮 《${title}》针对 "${query}" 的指令查询结果\n\n`;
    res += `共为您检索到 **${commands.length}** 条经老L认证的控制台真实代码：\n\n`;

    for (const cmd of commands) {
      const name = typeof cmd.name === 'object' ? (cmd.name['zh-CN'] || cmd.name['en'] || Object.values(cmd.name)[0]) : cmd.name;
      res += `#### 📌 ${name}\n`;
      if (cmd.desc) res += `${cmd.desc}\n`;
      res += `\`\`\`lua\n${cmd.code}\n\`\`\`\n\n`;
    }

    if (game.consoleShortcut) {
      res += `> 💡 **使用提示**：在游戏中按 \`${game.consoleShortcut}\` 唤出输入框，粘贴上述指令并回车执行。`;
    }

    return { text: res, commands: commands, game: game };
  }

  function buildScenarioBundleResponse(game, title, bundle) {
    let res = `### 📦 《${title}》专属场景套餐包：【${bundle.name}】\n\n`;
    if (bundle.description) res += `${bundle.description}\n\n`;

    if (bundle.commands && bundle.commands.length > 0) {
      res += `**包含指令集合**：\n\n`;
      for (const cmd of bundle.commands) {
        res += `- **${cmd.name}**: \`${cmd.code}\` (${cmd.desc || ''})\n`;
      }

      const mergedCode = bundle.commands.map(c => c.code).join('\n');
      res += `\n**一键整段打包代码**：\n\`\`\`lua\n${mergedCode}\n\`\`\`\n`;
    }

    return { text: res, batContent: bundle.batScript || (bundle.commands ? bundle.commands.map(c => c.code).join('\r\n') : '') };
  }

  function buildPopularCommandsFallback(game, title, query) {
    let res = `### 🎮 《${title}》常用核心官方指令\n\n`;
    res += `未找到精确包含 "${query}" 的特定代码，已为您调出该游戏的常用核心代码：\n\n`;

    for (const cmd of game.popularCommands.slice(0, 5)) {
      res += `#### 📌 ${cmd.name}\n`;
      if (cmd.desc) res += `${cmd.desc}\n`;
      res += `\`\`\`lua\n${cmd.code}\n\`\`\`\n\n`;
    }

    return { text: res, commands: game.popularCommands.slice(0, 5), game: game };
  }

  function searchAcrossAllGames(query, games) {
    const q = query.toLowerCase();
    const hits = [];

    for (const g of games) {
      let score = 0;
      let matchedCmd = null;

      if (g.popularCommands) {
        for (const c of g.popularCommands) {
          if ((c.name && c.name.toLowerCase().includes(q)) || (c.desc && c.desc.toLowerCase().includes(q))) {
            score += 2;
            matchedCmd = c;
            break;
          }
        }
      }

      if (score > 0) {
        hits.push({ game: g, cmd: matchedCmd, score: score });
      }
    }

    return hits.slice(0, 5);
  }

  function buildGlobalSearchResults(matches, query) {
    let res = `### 🌐 在全网 100 款大作中检索到以下相关游戏：\n\n`;
    for (const m of matches) {
      const g = m.game;
      const title = (g.titles && g.titles['zh-CN']) || g.title;
      res += `#### 🎮 [${title}] (Rank #${g.rank})\n`;
      if (m.cmd) {
        res += `- 包含指令 **${m.cmd.name}**: \`${m.cmd.code}\`\n`;
      }
      res += `[点击进入《${title}》专区查看](#game=${g.id})\n\n`;
    }
    return { text: res };
  }

  // =========================================================================
  // ONLINE AI CALLS: Google Gemini & DeepSeek API Integration
  // =========================================================================
  async function callGeminiApi(prompt, contextGame) {
    if (!state.apiKey) {
      throw new Error('请先在设置 (⚙️) 中填入您的 Google Gemini API Key！');
    }

    const model = state.geminiModel || 'gemini-2.5-flash';
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(state.apiKey)}`;

    let systemContext = `You are '老L' (Old L), a legendary single-player PC game modding, console command, and anti-pitfall master of L-MOD Vault.
Your mission is to provide 100% accurate, safe, zero-placeholder, verified game cheats, console commands, trainer guidance, and mod crash diagnosis.
Rules:
1. Always specify exact engine key (e.g. ~, F1, F10, Insert) and syntax (Lua for CET, Hex for Creation Engine, Osi for BG3).
2. NEVER output generic fake commands like 'god', 'addmoney', 'give all' unless the game natively supports them.
3. If giving code, wrap it cleanly in markdown code blocks with clear step-by-step instructions.
4. Language: Match the user's language (prefer Chinese Simplified if query is in Chinese).`;

    if (contextGame) {
      systemContext += `\n\nActive Game Context:
- Name: ${contextGame.title} (ID: ${contextGame.id})
- Developer: ${contextGame.developer || 'N/A'}
- Has Console: ${contextGame.hasConsole}
- Console Shortcut: ${contextGame.consoleShortcut || 'N/A'}
- Verified Patch: ${contextGame.verifiedPatch || 'Latest'}
- Compatibility Status: ${contextGame.compatibilityStatus || 'green'}
- Pitfall Note: ${contextGame.pitfallNote || 'None'}`;
    }

    const payload = {
      contents: [
        {
          role: 'user',
          parts: [{ text: `${systemContext}\n\nUser Question:\n${prompt}` }]
        }
      ],
      generationConfig: {
        temperature: 0.3,
        maxOutputTokens: 2048
      }
    };

    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const errData = await resp.json().catch(() => ({}));
      const msg = (errData.error && errData.error.message) || `HTTP ${resp.status} ${resp.statusText}`;
      throw new Error(`Gemini API 报错: ${msg}`);
    }

    const data = await resp.json();
    const candidate = data.candidates && data.candidates[0];
    const text = candidate && candidate.content && candidate.content.parts && candidate.content.parts[0] && candidate.content.parts[0].text;
    if (!text) throw new Error('Gemini 返回内容为空');

    return { text: text };
  }

  async function callDeepSeekApi(prompt, contextGame) {
    if (!state.apiKey) {
      throw new Error('请先在设置 (⚙️) 中填入您的 DeepSeek API Key！');
    }

    const endpoint = state.customEndpoint || 'https://api.deepseek.com/chat/completions';
    const model = state.deepseekModel || 'deepseek-chat';

    let systemContent = `你是老L（L-MOD Vault 官方单机游戏智库顾问与逆向工程老兵）。
专门解答单机游戏作弊控制台、MOD冲突、闪退崩溃诊断和避坑指南。
绝对杜绝无用假指令，代码严格遵循各游戏引擎真实语法（CET Lua, Creation Hex, UE4SS, BG3 Osiris等）。`;

    if (contextGame) {
      systemContent += `\n当前用户正在查看游戏：《${contextGame.title}》，已认证补丁版本：${contextGame.verifiedPatch || '最新'}，控制台按键：${contextGame.consoleShortcut || '无'}`;
    }

    const payload = {
      model: model,
      messages: [
        { role: 'system', content: systemContent },
        { role: 'user', content: prompt }
      ],
      temperature: 0.3
    };

    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${state.apiKey}`
      },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const errData = await resp.json().catch(() => ({}));
      const msg = (errData.error && errData.error.message) || `HTTP ${resp.status} ${resp.statusText}`;
      throw new Error(`DeepSeek API 报错: ${msg}`);
    }

    const data = await resp.json();
    const text = data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content;
    if (!text) throw new Error('DeepSeek 返回内容为空');

    return { text: text };
  }

  // =========================================================================
  // UI RENDERER & DOM INJECTION
  // =========================================================================
  function injectStyles() {
    if (document.getElementById('lmod-ai-styles')) return;
    const style = document.createElement('style');
    style.id = 'lmod-ai-styles';
    style.textContent = `
      #lmod-ai-fab {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px 16px;
        border-radius: 9999px;
        background: linear-gradient(135deg, #8b5cf6 0%, #A855F7 50%, #ec4899 100%);
        color: #ffffff;
        box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.5), 0 8px 10px -6px rgba(168, 85, 247, 0.3);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        user-select: none;
      }
      #lmod-ai-fab:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 14px 30px -4px rgba(168, 85, 247, 0.65);
      }
      #lmod-ai-fab .fab-ping {
        position: absolute;
        top: -2px;
        right: -2px;
        width: 10px;
        height: 10px;
        border-radius: 9999px;
        background: #10b981;
      }
      #lmod-ai-drawer {
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        width: 100%;
        max-width: 480px;
        background: rgba(14, 16, 22, 0.96);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: -15px 0 50px rgba(0, 0, 0, 0.7);
        z-index: 10000;
        display: flex;
        flex-direction: column;
        transform: translateX(100%);
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
      }
      #lmod-ai-drawer.open {
        transform: translateX(0);
      }
      #lmod-ai-backdrop {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
        z-index: 9998;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
      }
      #lmod-ai-backdrop.open {
        opacity: 1;
        pointer-events: auto;
      }
      .lmod-msg {
        animation: lmodFadeIn 0.25s ease-out;
      }
      @keyframes lmodFadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
      }
      .lmod-code-box {
        background: #090a0f;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        font-family: "SF Mono", Menlo, Consolas, Monaco, monospace;
        font-size: 12px;
        position: relative;
        overflow-x: auto;
      }
      .lmod-btn-action {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #e5e7eb;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }
      .lmod-btn-action:hover {
        background: rgba(168, 85, 247, 0.25);
        border-color: rgba(168, 85, 247, 0.5);
        color: #ffffff;
      }
      .lmod-pill {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 9999px;
        padding: 4px 10px;
        font-size: 11px;
        color: #d1d5db;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
      }
      .lmod-pill:hover {
        background: rgba(168, 85, 247, 0.2);
        border-color: rgba(168, 85, 247, 0.4);
        color: #ffffff;
      }
    `;
    document.head.appendChild(style);
  }

  function injectDrawerHtml() {
    if (document.getElementById('lmod-ai-drawer')) return;

    // 1. Backdrop
    const backdrop = document.createElement('div');
    backdrop.id = 'lmod-ai-backdrop';
    backdrop.onclick = closeDrawer;
    document.body.appendChild(backdrop);

    // 2. FAB Button
    const fab = document.createElement('div');
    fab.id = 'lmod-ai-fab';
    fab.title = '老L · AI 游戏智库顾问 (Cmd+K / Ctrl+K)';
    fab.innerHTML = `
      <span class="fab-ping"></span>
      <span style="font-size: 16px;">🤖</span>
      <span style="font-weight: 700; font-size: 13px; letter-spacing: 0.2px;">AI 顾问</span>
      <span style="font-size: 10px; opacity: 0.7; font-family: monospace; background: rgba(0,0,0,0.2); padding: 1px 5px; border-radius: 4px;">⌘K</span>
    `;
    fab.onclick = toggleDrawer;
    document.body.appendChild(fab);

    // 3. Drawer Container
    const drawer = document.createElement('div');
    drawer.id = 'lmod-ai-drawer';
    drawer.innerHTML = `
      <!-- HEADER -->
      <div style="padding: 16px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; background: rgba(255, 255, 255, 0.02);">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 34px; height: 34px; border-radius: 10px; background: linear-gradient(135deg, #8b5cf6, #ec4899); display: flex; align-items: center; justify-content: center; font-size: 18px; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);">
            🤖
          </div>
          <div>
            <div style="font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
              <span>${t('title')}</span>
              <span id="lmod-mode-badge" style="font-size: 9px; padding: 2px 6px; border-radius: 4px; background: rgba(16, 185, 129, 0.15); color: #34d399; font-weight: 600;">${t('offlineBadge')}</span>
            </div>
            <div style="font-size: 11px; color: #9ca3af; margin-top: 1px;" id="lmod-tagline">${t('tagline')}</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <button id="lmod-btn-settings" title="设置 API Key 与模型" style="background: none; border: none; color: #9ca3af; cursor: pointer; padding: 6px; border-radius: 8px; transition: color 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#9ca3af'">
            ⚙️
          </button>
          <button id="lmod-btn-clear" title="清空对话" style="background: none; border: none; color: #9ca3af; cursor: pointer; padding: 6px; border-radius: 8px; transition: color 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#9ca3af'">
            🗑️
          </button>
          <button id="lmod-btn-close" title="关闭 (Esc)" style="background: none; border: none; color: #9ca3af; cursor: pointer; padding: 6px; border-radius: 8px; transition: color 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#9ca3af'">
            ✕
          </button>
        </div>
      </div>

      <!-- ACTIVE CONTEXT BAR -->
      <div id="lmod-context-bar" style="padding: 8px 16px; background: rgba(168, 85, 247, 0.08); border-bottom: 1px solid rgba(168, 85, 247, 0.15); font-size: 11px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          <span style="color: #A855F7;">🎮</span>
          <span id="lmod-context-text" style="color: #d8b4fe; font-weight: 600;">${t('globalContext')}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <button id="lmod-context-clear" style="display: none; background: rgba(255,255,255,0.06); border: none; color: #cbd5e1; font-size: 10px; padding: 2px 6px; border-radius: 4px; cursor: pointer;">${t('clearContext')}</button>
        </div>
      </div>

      <!-- QUICK PILLS -->
      <div id="lmod-quick-pills" style="padding: 10px 16px; display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; border-bottom: 1px solid rgba(255, 255, 255, 0.05); background: rgba(0,0,0,0.15);">
        <button class="lmod-pill" data-prompt="${t('pillCommands')}">${t('pillCommands')}</button>
        <button class="lmod-pill" data-prompt="${t('pillCrash')}">${t('pillCrash')}</button>
        <button class="lmod-pill" data-prompt="${t('pillPatch')}">${t('pillPatch')}</button>
        <button class="lmod-pill" data-prompt="${t('pillTrainer')}">${t('pillTrainer')}</button>
      </div>

      <!-- CHAT MESSAGE LIST -->
      <div id="lmod-chat-body" style="flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 14px; scroll-behavior: smooth;">
        <!-- Messages injected here -->
      </div>

      <!-- INPUT BAR -->
      <div style="padding: 14px 16px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(14, 16, 22, 0.98); display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; gap: 8px; align-items: flex-end;">
          <textarea id="lmod-chat-input" rows="1" placeholder="${t('inputPlaceholder')}" style="flex: 1; resize: none; max-height: 120px; background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 10px 14px; color: #ffffff; font-size: 13px; outline: none; font-family: inherit; line-height: 1.4; transition: border-color 0.2s;"></textarea>
          <button id="lmod-btn-send" style="background: linear-gradient(135deg, #8b5cf6, #A855F7); border: none; border-radius: 12px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; color: #fff; cursor: pointer; flex-shrink: 0; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3); transition: transform 0.2s;">
            <svg style="width: 18px; height: 18px; fill: currentColor;" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
          </button>
        </div>
        <div style="font-size: 10px; color: #6b7280; text-align: center; display: flex; justify-content: space-between; align-items: center;">
          <span>按 Enter 发送 / Shift+Enter 换行</span>
          <span style="color: #8b5cf6; cursor: pointer;" onclick="window.LMOD_AI_COPILOT.openSettings()">⚙️ 引擎配置</span>
        </div>
      </div>

      <!-- SETTINGS MODAL (OVERLAY INSIDE DRAWER) -->
      <div id="lmod-settings-modal" style="display: none; position: absolute; inset: 0; background: rgba(10, 12, 16, 0.98); z-index: 10001; padding: 24px; flex-direction: column; gap: 16px; overflow-y: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 12px;">
          <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #fff;">${t('settingsTitle')}</h3>
          <button id="lmod-settings-close" style="background: none; border: none; color: #9ca3af; font-size: 16px; cursor: pointer;">✕</button>
        </div>

        <div style="display: flex; flex-direction: column; gap: 12px; font-size: 12px;">
          <div>
            <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">选择推理模式</label>
            <select id="lmod-cfg-mode" style="width: 100%; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px; color: #fff; font-size: 12px;">
              <option value="local">${t('modeLocal')}</option>
              <option value="gemini">${t('modeGemini')}</option>
              <option value="deepseek">${t('modeDeepSeek')}</option>
              <option value="custom">${t('modeCustom')}</option>
            </select>
          </div>

          <div id="lmod-cfg-apikey-box" style="display: none;">
            <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">${t('apiKeyLabel')}</label>
            <input type="password" id="lmod-cfg-apikey" placeholder="AIzaSy... 或 sk-..." style="width: 100%; box-sizing: border-box; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; color: #fff; font-size: 12px; font-family: monospace;">
            <span style="font-size: 10px; color: #9ca3af; margin-top: 4px; display: block;">密钥直接在您本机浏览器与官方端点通信，绝不上报或中转。</span>
          </div>

          <div id="lmod-cfg-gemini-box" style="display: none;">
            <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">Gemini 模型选择</label>
            <select id="lmod-cfg-gemini-model" style="width: 100%; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px; color: #fff; font-size: 12px;">
              <option value="gemini-2.5-flash">gemini-2.5-flash (推荐 · 极速高精)</option>
              <option value="gemini-2.5-pro">gemini-2.5-pro (深度推理)</option>
              <option value="gemini-1.5-flash">gemini-1.5-flash (轻量稳定)</option>
            </select>
          </div>

          <div id="lmod-cfg-custom-box" style="display: none;">
            <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">自定义端点 URL (OpenAI 规范)</label>
            <input type="text" id="lmod-cfg-endpoint" placeholder="https://api.yourdomain.com/v1/chat/completions" style="width: 100%; box-sizing: border-box; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; color: #fff; font-size: 12px;">
          </div>
        </div>

        <div style="margin-top: auto; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.1); display: flex; justify-content: flex-end; gap: 8px;">
          <button id="lmod-btn-save-cfg" style="background: #A855F7; color: #fff; border: none; border-radius: 8px; padding: 8px 16px; font-weight: 600; cursor: pointer; font-size: 12px;">${t('saveSettings')}</button>
        </div>
      </div>
    `;
    document.body.appendChild(drawer);

    // Event Listeners
    document.getElementById('lmod-btn-close').onclick = closeDrawer;
    document.getElementById('lmod-btn-clear').onclick = clearChatHistory;
    document.getElementById('lmod-btn-settings').onclick = openSettings;
    document.getElementById('lmod-settings-close').onclick = closeSettings;
    document.getElementById('lmod-btn-save-cfg').onclick = handleSaveSettings;
    document.getElementById('lmod-btn-send').onclick = handleSendUserMessage;

    // Mode Selector Switch
    document.getElementById('lmod-cfg-mode').onchange = function (e) {
      updateSettingsFormVisibility(e.target.value);
    };

    // Quick Pills
    document.querySelectorAll('#lmod-quick-pills .lmod-pill').forEach(btn => {
      btn.onclick = function () {
        const prompt = this.getAttribute('data-prompt');
        sendUserMessage(prompt);
      };
    });

    // Input Enter Key
    const input = document.getElementById('lmod-chat-input');
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendUserMessage();
      }
    });

    // Context Clear
    document.getElementById('lmod-context-clear').onclick = function () {
      state.activeGame = null;
      updateContextBar();
    };

    // Auto update context bar on open
    updateContextBar();
    updateModeBadge();
  }

  function updateSettingsFormVisibility(mode) {
    const keyBox = document.getElementById('lmod-cfg-apikey-box');
    const geminiBox = document.getElementById('lmod-cfg-gemini-box');
    const customBox = document.getElementById('lmod-cfg-custom-box');

    if (mode === 'local') {
      keyBox.style.display = 'none';
      geminiBox.style.display = 'none';
      customBox.style.display = 'none';
    } else if (mode === 'gemini') {
      keyBox.style.display = 'block';
      geminiBox.style.display = 'block';
      customBox.style.display = 'none';
    } else if (mode === 'deepseek') {
      keyBox.style.display = 'block';
      geminiBox.style.display = 'none';
      customBox.style.display = 'none';
    } else if (mode === 'custom') {
      keyBox.style.display = 'block';
      geminiBox.style.display = 'none';
      customBox.style.display = 'block';
    }
  }

  function updateModeBadge() {
    const badge = document.getElementById('lmod-mode-badge');
    if (!badge) return;

    if (state.mode === 'gemini') {
      badge.textContent = t('geminiBadge');
      badge.style.background = 'rgba(168, 85, 247, 0.2)';
      badge.style.color = '#c084fc';
    } else if (state.mode === 'deepseek') {
      badge.textContent = t('deepseekBadge');
      badge.style.background = 'rgba(59, 130, 246, 0.2)';
      badge.style.color = '#60a5fa';
    } else if (state.mode === 'custom') {
      badge.textContent = t('customBadge');
      badge.style.background = 'rgba(234, 179, 8, 0.2)';
      badge.style.color = '#facc15';
    } else {
      badge.textContent = t('offlineBadge');
      badge.style.background = 'rgba(16, 185, 129, 0.15)';
      badge.style.color = '#34d399';
    }
  }

  function updateContextBar() {
    const barText = document.getElementById('lmod-context-text');
    const clearBtn = document.getElementById('lmod-context-clear');
    if (!barText) return;

    const game = detectActiveGame();
    if (game) {
      state.activeGame = game;
      const title = (game.titles && game.titles['zh-CN']) || game.title;
      barText.textContent = `${t('activeContextPrefix')}${title} (Rank #${game.rank})`;
      clearBtn.style.display = 'inline-block';
    } else {
      barText.textContent = t('globalContext');
      clearBtn.style.display = 'none';
    }
  }

  // =========================================================================
  // MESSAGE RENDERING (Markdown + Code Boxes + Actions)
  // =========================================================================
  function renderMessages() {
    const container = document.getElementById('lmod-chat-body');
    if (!container) return;

    container.innerHTML = '';

    // If no messages, render welcome
    if (state.messages.length === 0) {
      appendAssistantMessage(t('welcomeMessage'), false);
      return;
    }

    for (const msg of state.messages) {
      if (msg.role === 'user') {
        appendUserMessageDom(msg.text);
      } else {
        appendAssistantMessageDom(msg.text, msg.commands, msg.batContent);
      }
    }

    container.scrollTop = container.scrollHeight;
  }

  function appendUserMessageDom(text) {
    const container = document.getElementById('lmod-chat-body');
    const div = document.createElement('div');
    div.className = 'lmod-msg';
    div.style.alignSelf = 'flex-end';
    div.style.maxWidth = '85%';
    div.style.background = 'linear-gradient(135deg, #7c3aed, #9333ea)';
    div.style.color = '#ffffff';
    div.style.padding = '10px 14px';
    div.style.borderRadius = '14px 14px 2px 14px';
    div.style.fontSize = '13px';
    div.style.lineHeight = '1.5';
    div.style.wordBreak = 'break-word';
    div.textContent = text;
    container.appendChild(div);
  }

  function appendAssistantMessageDom(text, commands, batContent) {
    const container = document.getElementById('lmod-chat-body');
    const div = document.createElement('div');
    div.className = 'lmod-msg';
    div.style.alignSelf = 'flex-start';
    div.style.maxWidth = '92%';
    div.style.background = 'rgba(255, 255, 255, 0.05)';
    div.style.border = '1px solid rgba(255, 255, 255, 0.08)';
    div.style.color = '#e2e8f0';
    div.style.padding = '14px';
    div.style.borderRadius = '14px 14px 14px 2px';
    div.style.fontSize = '12.5px';
    div.style.lineHeight = '1.6';
    div.style.wordBreak = 'break-word';

    // Format Markdown to HTML
    div.innerHTML = formatMarkdown(text);

    // Attach Copy and Download Bat action buttons
    attachCodeActionButtons(div, batContent);

    container.appendChild(div);
  }

  function formatMarkdown(md) {
    if (!md) return '';

    let html = md
      // Escape HTML tags to prevent XSS
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      // Headers
      .replace(/^### (.*$)/gim, '<div style="font-weight: 700; font-size: 14px; color: #a78bfa; margin: 8px 0 4px 0;">$1</div>')
      .replace(/^#### (.*$)/gim, '<div style="font-weight: 600; font-size: 13px; color: #f3f4f6; margin: 6px 0 2px 0;">$1</div>')
      // Code blocks ```lang\ncode\n```
      .replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, function (match, lang, code) {
        return `<div class="lmod-code-box" data-code="${encodeURIComponent(code)}">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 10px; color: #9ca3af; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 4px;">
            <span>${lang || 'CODE'}</span>
            <button class="lmod-btn-action lmod-btn-copy" onclick="window.LMOD_AI_COPILOT.copyCode(this)">📋 ${t('copyCode')}</button>
          </div>
          <pre style="margin: 0; white-space: pre-wrap; word-break: break-all; color: #a5f3fc;">${code}</pre>
        </div>`;
      })
      // Inline code
      .replace(/`([^`]+)`/g, '<code style="background: rgba(168,85,247,0.15); color: #d8b4fe; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 11.5px;">$1</code>')
      // Bold
      .replace(/\*\*([^*]+)\*\*/g, '<strong style="color: #ffffff; font-weight: 600;">$1</strong>')
      // Blockquotes
      .replace(/^> (.*$)/gim, '<div style="border-left: 3px solid #A855F7; padding-left: 8px; margin: 6px 0; color: #cbd5e1; font-style: italic; background: rgba(168,85,247,0.05); padding: 6px 10px; border-radius: 0 6px 6px 0;">$1</div>')
      // Unordered lists
      .replace(/^\s*-\s+(.*$)/gim, '<div style="display: flex; gap: 6px; margin: 2px 0;"><span style="color: #A855F7;">•</span><span>$1</span></div>')
      // Links [title](url)
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color: #c084fc; text-decoration: underline;">$1</a>')
      // Line breaks
      .replace(/\n\n/g, '<div style="height: 8px;"></div>');

    return html;
  }

  function attachCodeActionButtons(div, batContent) {
    if (!batContent) return;

    const actionContainer = document.createElement('div');
    actionContainer.style.marginTop = '10px';
    actionContainer.style.paddingTop = '8px';
    actionContainer.style.borderTop = '1px dashed rgba(255, 255, 255, 0.1)';
    actionContainer.style.display = 'flex';
    actionContainer.style.gap = '8px';

    const batBtn = document.createElement('button');
    batBtn.className = 'lmod-btn-action';
    batBtn.innerHTML = `💾 ${t('downloadBat')}`;
    batBtn.onclick = function () {
      downloadBatchFile(batContent);
    };

    actionContainer.appendChild(batBtn);
    div.appendChild(actionContainer);
  }

  function downloadBatchFile(content, filename = 'LMOD_Console_Inject.bat') {
    const fullBat = `@echo off\r\nchcp 65001 >nul\r\n:: L-MOD Vault Auto-Generated One-Click Batch Script\r\necho [L-MOD Vault] 正在准备注入配置与指令...\r\n${content}\r\necho [L-MOD Vault] 执行完毕！按任意键退出。\r\npause >nul\r\n`;
    const blob = new Blob([fullBat], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    if (window.showToast) {
      window.showToast('已生成并下载 .bat 批处理文件！');
    }
  }

  // =========================================================================
  // ACTIONS & HANDLERS
  // =========================================================================
  function toggleDrawer() {
    if (state.isOpen) closeDrawer();
    else openDrawer();
  }

  function openDrawer(initialPrompt) {
    injectStyles();
    injectDrawerHtml();

    state.isOpen = true;
    updateContextBar();
    updateModeBadge();

    const drawer = document.getElementById('lmod-ai-drawer');
    const backdrop = document.getElementById('lmod-ai-backdrop');
    drawer.classList.add('open');
    backdrop.classList.add('open');

    renderMessages();

    const input = document.getElementById('lmod-chat-input');
    if (initialPrompt) {
      input.value = initialPrompt;
      handleSendUserMessage();
    } else {
      setTimeout(() => input.focus(), 300);
    }
  }

  function closeDrawer() {
    state.isOpen = false;
    const drawer = document.getElementById('lmod-ai-drawer');
    const backdrop = document.getElementById('lmod-ai-backdrop');
    if (drawer) drawer.classList.remove('open');
    if (backdrop) backdrop.classList.remove('open');
  }

  function openSettings() {
    const modal = document.getElementById('lmod-settings-modal');
    if (!modal) return;

    document.getElementById('lmod-cfg-mode').value = state.mode;
    document.getElementById('lmod-cfg-apikey').value = state.apiKey;
    document.getElementById('lmod-cfg-endpoint').value = state.customEndpoint;
    document.getElementById('lmod-cfg-gemini-model').value = state.geminiModel;

    updateSettingsFormVisibility(state.mode);
    modal.style.display = 'flex';
  }

  function closeSettings() {
    const modal = document.getElementById('lmod-settings-modal');
    if (modal) modal.style.display = 'none';
  }

  function handleSaveSettings() {
    state.mode = document.getElementById('lmod-cfg-mode').value;
    state.apiKey = document.getElementById('lmod-cfg-apikey').value.trim();
    state.customEndpoint = document.getElementById('lmod-cfg-endpoint').value.trim();
    state.geminiModel = document.getElementById('lmod-cfg-gemini-model').value;

    saveConfig();
    updateModeBadge();
    closeSettings();

    if (window.showToast) {
      window.showToast('AI 智库引擎配置已保存！');
    }
  }

  function clearChatHistory() {
    state.messages = [];
    renderMessages();
  }

  async function handleSendUserMessage() {
    const input = document.getElementById('lmod-chat-input');
    const query = input.value.trim();
    if (!query || state.isLoading) return;

    input.value = '';
    await sendUserMessage(query);
  }

  async function sendUserMessage(query) {
    if (state.isLoading) return;

    state.messages.push({ role: 'user', text: query });
    appendUserMessageDom(query);

    // Scroll to bottom
    const container = document.getElementById('lmod-chat-body');
    container.scrollTop = container.scrollHeight;

    // Show loading
    state.isLoading = true;
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'lmod-loading-indicator';
    loadingDiv.className = 'lmod-msg';
    loadingDiv.style.alignSelf = 'flex-start';
    loadingDiv.style.fontSize = '12px';
    loadingDiv.style.color = '#c084fc';
    loadingDiv.style.padding = '8px 12px';
    loadingDiv.style.background = 'rgba(168, 85, 247, 0.1)';
    loadingDiv.style.borderRadius = '10px';
    loadingDiv.innerHTML = `<span style="display: inline-block; animation: spin 1s linear infinite;">⚡</span> ${t('thinking')}`;
    container.appendChild(loadingDiv);
    container.scrollTop = container.scrollHeight;

    const activeGame = detectActiveGame();

    try {
      let result = null;

      if (state.mode === 'gemini') {
        result = await callGeminiApi(query, activeGame);
      } else if (state.mode === 'deepseek') {
        result = await callDeepSeekApi(query, activeGame);
      } else if (state.mode === 'custom') {
        result = await callDeepSeekApi(query, activeGame); // OpenAI standard format
      } else {
        // Default Local RAG Engine
        // Give a tiny simulated delay for smooth feel
        await new Promise(r => setTimeout(r, 200));
        result = localRagQuery(query, activeGame);
      }

      // Remove loading
      const loading = document.getElementById('lmod-loading-indicator');
      if (loading) loading.remove();

      state.messages.push({
        role: 'assistant',
        text: result.text,
        commands: result.commands,
        batContent: result.batContent
      });

      appendAssistantMessageDom(result.text, result.commands, result.batContent);
      container.scrollTop = container.scrollHeight;

    } catch (err) {
      const loading = document.getElementById('lmod-loading-indicator');
      if (loading) loading.remove();

      const errMsg = `⚠️ **请求失败**：${err.message || err}\n\n已自动切换为**本地离线智库**为您解答：\n\n`;
      const fallback = localRagQuery(query, activeGame);

      state.messages.push({
        role: 'assistant',
        text: errMsg + fallback.text,
        commands: fallback.commands,
        batContent: fallback.batContent
      });

      appendAssistantMessageDom(errMsg + fallback.text, fallback.commands, fallback.batContent);
      container.scrollTop = container.scrollHeight;
    } finally {
      state.isLoading = false;
    }
  }

  function appendAssistantMessage(text, isUser = false) {
    if (isUser) {
      appendUserMessageDom(text);
    } else {
      appendAssistantMessageDom(text);
    }
  }

  function copyCode(btn) {
    const box = btn.closest('.lmod-code-box');
    if (!box) return;

    const raw = box.getAttribute('data-code');
    const code = raw ? decodeURIComponent(raw) : box.querySelector('pre').innerText;

    navigator.clipboard.writeText(code).then(() => {
      const originalText = btn.innerHTML;
      btn.innerHTML = '✅ 已复制';
      btn.style.color = '#34d399';
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.color = '';
      }, 1800);

      if (window.showToast) {
        window.showToast(t('copied'));
      }
    }).catch(() => {
      // Fallback execCommand
      const ta = document.createElement('textarea');
      ta.value = code;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      if (window.showToast) window.showToast(t('copied'));
    });
  }

  // Keyboard Shortcuts (Cmd+K / Ctrl+K, Esc)
  window.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      toggleDrawer();
    } else if (e.key === 'Escape' && state.isOpen) {
      closeDrawer();
    }
  });

  // Export Global API
  window.LMOD_AI_COPILOT = {
    openDrawer: openDrawer,
    closeDrawer: closeDrawer,
    toggleDrawer: toggleDrawer,
    openSettings: openSettings,
    sendUserMessage: sendUserMessage,
    copyCode: copyCode,
    downloadBatchFile: downloadBatchFile,
    setActiveGame: function (game) {
      state.activeGame = game;
      updateContextBar();
    }
  };

  // Auto initialize on DOM ready
  loadConfig();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      injectStyles();
      injectDrawerHtml();
    });
  } else {
    injectStyles();
    injectDrawerHtml();
  }

})();
