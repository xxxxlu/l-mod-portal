/**
 * L-MOD Vault - Player-Facing AI Copilot (老L · 官方 AI 游戏智库顾问)
 * ==============================================================================
 * 首席架构师重构版：
 * 1. 【彻底修复回车双发 Bug】：
 *    - 严格监听中文拼音输入法组合状态 (compositionstart / compositionend / isComposing / keyCode === 229)
 *    - 状态机互斥锁 (state.isSending & state.isLoading) 彻底杜绝并发二次投递
 *    - Shift+Enter 正常换行，Enter 触发送，Textarea 弹性高度输入与发送后自适应回缩
 * 2. 【官方云端智能体 + 免 Key 体验】：
 *    - 默认直连官方中继 (/api/v1/ai/chat)，由站长后台统一配置 API Key，玩家免输密钥
 *    - Server-Sent Events (SSE) 极客级流式打字机逐字输出
 * 3. 【4 大专属 Agentic Skills 实时联动】：
 *    - 技能 A: 游戏指令与模组检索 (Game Vault RAG)
 *    - 技能 B: Steam 补丁哨兵巡检 (Patch Sentinel)
 *    - 技能 C: 报错闪退崩溃专家诊断 (Crash Diagnostic)
 *    - 技能 D: 全域单机智库通用问答 (General Gaming Oracle)
 * 4. 【多级容灾与离线保障】：
 *    - 云端网络异常或离线时，100% 优雅回退到本地极速 RAG 智库
 *    - 支持一键复制真实指令、一键生成 Windows .bat 批处理脚本
 */

(function () {
  'use strict';

  // 防止重复初始化
  if (window.LMOD_AI_COPILOT) return;

  const STORAGE_KEY_KEY = 'lmod_ai_config';
  const STORAGE_HISTORY_KEY = 'lmod_ai_history';

  // 状态机核心定义
  const state = {
    isOpen: false,
    isSettingsOpen: false,
    activeGame: null, // 当前锚定游戏 { id, title, rank, ... }
    mode: 'cloud', // 'cloud' (官方云端免Key推荐) | 'local' (离线智库) | 'byok' (自带Key调试)
    isSending: false, // 发送互斥锁 (防抖/防并发)
    isLoading: false, // 网络加载/流式中继锁
    byokProvider: 'gemini', // 'gemini' | 'deepseek' | 'custom'
    byokKey: '',
    customEndpoint: '',
    customModel: '',
    messages: []
  };

  // 多语言文案字典
  const i18n = {
    'zh-CN': {
      title: '老L · AI 官方智库顾问',
      tagline: '控制台代码 · 闪退排查 · 补丁雷达 · 一键脚本',
      globalContext: '全网 100 款单机大作智库',
      activeContextPrefix: '当前游戏: ',
      switchGame: '切换游戏',
      clearContext: '切回全局',
      inputPlaceholder: '输入你的问题，如：“2077怎么刷四季宝”、“法环闪退排查”、“黑神话广智怎么打”...',
      sendBtn: '发送',
      thinking: '老L 正在调取 D1 智库底层指令与 4 大专属 Skills...',
      copyCode: '复制指令',
      copied: '已复制到剪贴板！',
      downloadBat: '生成 .bat 脚本',
      settingsTitle: 'AI 引擎与官方智能体配置',
      modeCloud: '⚡ 官方统一云端智能体 (免 Key 推荐 · 4大Skills编排)',
      modeLocal: '📦 本地极速智库 (离线模式 · 零延迟)',
      modeByok: '🛠️ 自定义/开发者自带密钥 (BYOK)',
      byokKeyLabel: '私有 API Key (若填写将覆盖官方配置，仅存本地)',
      saveSettings: '保存配置',
      close: '关闭',
      clearHistory: '清空会话',
      welcomeMessage: '我是**老L**，L-MOD Vault 官方单机游戏智库首席顾问！\n\n已为你接入**官方云端智能体**与 **4 大专属 Skills 技能链**：\n- 🔍 **查核心控制台代码**：“给我赛博朋克2077强尼的保时捷代码”\n- 💥 **闪退坏档逃课排查**：“博德之门3打Mod闪退怎么解决”\n- 📡 **Steam 补丁避坑雷达**：“艾尔登法环当前版本能打Mod吗”\n- 🎮 **单机攻略与配置通识**：“黑神话悟空推荐画质设置”',
      pillCommands: '🔍 查核心作弊代码',
      pillCrash: '💥 闪退与冲突排查',
      pillPatch: '📡 最新补丁避坑状态',
      pillTrainer: '⚡ 修改器热键与防误报',
      cloudBadge: '官方云端智能体',
      offlineBadge: '本地智库 (离线)',
      byokBadge: '自带 Key (私有)'
    },
    'en': {
      title: 'Old L · Official AI Vault Advisor',
      tagline: 'Console Codes / Crash Doctor / Patch Radar / Script Gen',
      globalContext: 'Global 100 Games Vault',
      activeContextPrefix: 'Active Game: ',
      switchGame: 'Switch Game',
      clearContext: 'Reset to Global',
      inputPlaceholder: 'Ask a question, e.g. "Cyberpunk Johnny Porsche code", "Elden Ring crash fix"...',
      sendBtn: 'Send',
      thinking: 'Old L is orchestrating D1 commands & 4 agentic skills...',
      copyCode: 'Copy Code',
      copied: 'Copied to clipboard!',
      downloadBat: 'Download .bat',
      settingsTitle: 'AI Engine & Agent Configuration',
      modeCloud: '⚡ Official Cloud Agent (Recommended · No Key Needed)',
      modeLocal: '📦 Offline Local Vault (Zero Latency)',
      modeByok: '🛠️ Developer / Bring Your Own Key (BYOK)',
      byokKeyLabel: 'Private API Key (Stored in browser only)',
      saveSettings: 'Save Settings',
      close: 'Close',
      clearHistory: 'Clear Chat',
      welcomeMessage: "I'm **Old L**, your official single-player game modding and console command advisor!\n\nArmed with **Cloud Agent + 4 Exclusive Skills**:\n- 🔍 **Find Real Commands**: 'Johnny Silverhand Porsche code for Cyberpunk 2077'\n- 💥 **Crash & Mod Fixes**: 'Baldur\\'s Gate 3 crashes with mods, how to fix?'\n- 📡 **Patch Radar**: 'Can I safely mod on the latest Elden Ring patch?'\n- 🎮 **General Guide**: 'Best graphics settings for Black Myth: Wukong'",
      pillCommands: '🔍 Key Console Codes',
      pillCrash: '💥 Crash & Mod Doctor',
      pillPatch: '📡 Patch Radar Status',
      pillTrainer: '⚡ Trainer Hotkeys',
      cloudBadge: 'Official Cloud Agent',
      offlineBadge: 'Local Vault (Offline)',
      byokBadge: 'Private Key (BYOK)'
    }
  };

  function getLang() {
    const code = localStorage.getItem('lmod_lang') || 'zh-CN';
    return i18n[code] ? code : 'zh-CN';
  }

  function t(key) {
    const lang = getLang();
    return (i18n[lang] && i18n[lang][key]) || i18n['zh-CN'][key] || key;
  }

  // 加载与保存配置
  function loadConfig() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        state.mode = parsed.mode || 'cloud';
        state.byokProvider = parsed.byokProvider || 'gemini';
        state.byokKey = parsed.byokKey || '';
        state.customEndpoint = parsed.customEndpoint || '';
        state.customModel = parsed.customModel || '';
      }
    } catch (e) {
      console.warn('Failed to load L-MOD AI config:', e);
    }
  }

  function saveConfig() {
    try {
      const config = {
        mode: state.mode,
        byokProvider: state.byokProvider,
        byokKey: state.byokKey,
        customEndpoint: state.customEndpoint,
        customModel: state.customModel
      };
      localStorage.setItem(STORAGE_KEY_KEY, JSON.stringify(config));
    } catch (e) {
      console.warn('Failed to save L-MOD AI config:', e);
    }
  }

  // 智能环境探测：获取当前网页锚定的游戏
  function detectActiveGame() {
    if (window.activeGame && window.activeGame.id) return window.activeGame;
    if (window.currentDrawerGame && window.currentDrawerGame.id) return window.currentDrawerGame;

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

  // 根据 Query 推导目标游戏
  function findGameByQuery(query) {
    const games = window.GAMES_DATA || window.GAMES_DATABASE || [];
    if (!games.length) return null;
    const q = query.toLowerCase().replace(/\s+/g, '');

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
  // 核心样式注入
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
        max-width: 500px;
        background: rgba(14, 16, 22, 0.98);
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
      .lmod-skill-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 10px;
        padding: 2px 7px;
        border-radius: 6px;
        background: rgba(168, 85, 247, 0.15);
        color: #d8b4fe;
        border: 1px solid rgba(168, 85, 247, 0.3);
        margin-right: 4px;
        margin-bottom: 4px;
      }
      .lmod-typing-cursor::after {
        content: '▋';
        display: inline-block;
        color: #A855F7;
        animation: lmodBlink 1s infinite;
        margin-left: 2px;
      }
      @keyframes lmodBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }

  // =========================================================================
  // DOM 抽屉渲染与事件绑定 (包含中文拼音防抖与回车双发彻底修复)
  // =========================================================================
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
    fab.title = '老L · AI 官方智库顾问 (Cmd+K / Ctrl+K)';
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
          <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #8b5cf6, #ec4899); display: flex; align-items: center; justify-content: center; font-size: 18px; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);">
            🤖
          </div>
          <div>
            <div style="font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
              <span>${t('title')}</span>
              <span id="lmod-mode-badge" style="font-size: 9px; padding: 2px 6px; border-radius: 4px; background: rgba(168, 85, 247, 0.2); color: #c084fc; font-weight: 600;">${t('cloudBadge')}</span>
            </div>
            <div style="font-size: 11px; color: #9ca3af; margin-top: 1px;" id="lmod-tagline">${t('tagline')}</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <button id="lmod-btn-settings" title="查看智能体引擎设置" style="background: none; border: none; color: #9ca3af; cursor: pointer; padding: 6px; border-radius: 8px; transition: color 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#9ca3af'">
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
          <textarea id="lmod-chat-input" rows="1" placeholder="${t('inputPlaceholder')}" style="flex: 1; resize: none; max-height: 120px; min-height: 40px; background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 10px 14px; color: #ffffff; font-size: 13px; outline: none; font-family: inherit; line-height: 1.4; transition: border-color 0.2s; box-sizing: border-box;"></textarea>
          <button id="lmod-btn-send" style="background: linear-gradient(135deg, #8b5cf6, #A855F7); border: none; border-radius: 12px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; color: #fff; cursor: pointer; flex-shrink: 0; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3); transition: transform 0.2s;">
            <svg style="width: 18px; height: 18px; fill: currentColor;" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
          </button>
        </div>
        <div style="font-size: 10px; color: #6b7280; text-align: center; display: flex; justify-content: space-between; align-items: center;">
          <span>Enter 发送 / Shift+Enter 换行 (已做拼音防抖保护)</span>
          <span style="color: #8b5cf6; cursor: pointer;" onclick="window.LMOD_AI_COPILOT.openSettings()">⚡ 官方智库中继 · 已就绪</span>
        </div>
      </div>

      <!-- SETTINGS MODAL -->
      <div id="lmod-settings-modal" style="display: none; position: absolute; inset: 0; background: rgba(10, 12, 16, 0.98); z-index: 10001; padding: 24px; flex-direction: column; gap: 16px; overflow-y: auto;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 12px;">
          <h3 style="margin: 0; font-size: 15px; font-weight: 700; color: #fff;">${t('settingsTitle')}</h3>
          <button id="lmod-settings-close" style="background: none; border: none; color: #9ca3af; font-size: 16px; cursor: pointer;">✕</button>
        </div>

        <div style="display: flex; flex-direction: column; gap: 14px; font-size: 12px;">
          <div style="padding: 12px; border-radius: 10px; background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.2); line-height: 1.5; color: #d8b4fe;">
            <strong style="color: #fff;">💡 官方统一云端智能体已上线：</strong><br>
            前台玩家无需配置任何 API Key，由站长后台统一调配 Google Gemini 2.5 旗舰推理与 D1 智库 4 大专属 Skills 技能链。
          </div>

          <div>
            <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">选择运行模式</label>
            <select id="lmod-cfg-mode" style="width: 100%; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px; color: #fff; font-size: 12px;">
              <option value="cloud">${t('modeCloud')}</option>
              <option value="local">${t('modeLocal')}</option>
              <option value="byok">${t('modeByok')}</option>
            </select>
          </div>

          <!-- BYOK Developer Fields -->
          <div id="lmod-cfg-byok-box" style="display: none; flex-direction: column; gap: 10px;">
            <div>
              <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">私有模型供应商</label>
              <select id="lmod-cfg-byok-provider" style="width: 100%; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px; color: #fff; font-size: 12px;">
                <option value="gemini">Google Gemini (Gemini 2.5 Flash)</option>
                <option value="deepseek">DeepSeek API (DeepSeek-Chat)</option>
                <option value="custom">自定义 OpenAI 规范端点</option>
              </select>
            </div>

            <div>
              <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">${t('byokKeyLabel')}</label>
              <input type="password" id="lmod-cfg-byok-key" placeholder="AIzaSy... 或 sk-..." style="width: 100%; box-sizing: border-box; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; color: #fff; font-size: 12px; font-family: monospace;">
            </div>

            <div id="lmod-cfg-custom-endpoint-box" style="display: none;">
              <label style="display: block; font-weight: 600; color: #e5e7eb; margin-bottom: 6px;">自定义端点 URL</label>
              <input type="text" id="lmod-cfg-endpoint" placeholder="https://api.example.com/v1/chat/completions" style="width: 100%; box-sizing: border-box; background: #1c1f26; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 12px; color: #fff; font-size: 12px;">
            </div>
          </div>
        </div>

        <div style="margin-top: auto; padding-top: 16px; border-top: 1px solid rgba(255, 255, 255, 0.1); display: flex; justify-content: flex-end; gap: 8px;">
          <button id="lmod-btn-save-cfg" style="background: #A855F7; color: #fff; border: none; border-radius: 8px; padding: 8px 16px; font-weight: 600; cursor: pointer; font-size: 12px;">${t('saveSettings')}</button>
        </div>
      </div>
    `;
    document.body.appendChild(drawer);

    // 绑定基础关闭与清空事件
    document.getElementById('lmod-btn-close').onclick = closeDrawer;
    document.getElementById('lmod-btn-clear').onclick = clearChatHistory;
    document.getElementById('lmod-btn-settings').onclick = openSettings;
    document.getElementById('lmod-settings-close').onclick = closeSettings;
    document.getElementById('lmod-btn-save-cfg').onclick = handleSaveSettings;
    document.getElementById('lmod-btn-send').onclick = handleSendUserMessage;

    // 快捷胶囊点击事件
    document.querySelectorAll('#lmod-quick-pills .lmod-pill').forEach(btn => {
      btn.onclick = function () {
        const prompt = this.getAttribute('data-prompt');
        sendUserMessage(prompt);
      };
    });

    // 模式切换监听
    document.getElementById('lmod-cfg-mode').onchange = function (e) {
      updateSettingsFormVisibility(e.target.value);
    };

    document.getElementById('lmod-cfg-byok-provider').onchange = function (e) {
      const endpointBox = document.getElementById('lmod-cfg-custom-endpoint-box');
      endpointBox.style.display = e.target.value === 'custom' ? 'block' : 'none';
    };

    // -----------------------------------------------------------------------
    // 关键核心：中文拼音输入法状态机 + 彻底根治回车双发 Bug
    // -----------------------------------------------------------------------
    const input = document.getElementById('lmod-chat-input');
    let isComposing = false; // 中文拼音组合上屏状态机

    input.addEventListener('compositionstart', function () {
      isComposing = true;
    });

    input.addEventListener('compositionend', function () {
      // 部分浏览器在 compositionend 后立即触发一次 keydown，延迟 50ms 释放状态
      setTimeout(() => {
        isComposing = false;
      }, 50);
    });

    // Textarea 自适应弹性高度扩展
    input.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // 严格键盘拦截：杜绝回车二次触发
    input.addEventListener('keydown', function (e) {
      // 1. 若处于中文输入法选词组合状态，或按键码为 229，坚决拦截
      if (e.isComposing || isComposing || e.keyCode === 229) {
        return;
      }

      // 2. Shift + Enter 正常多行换行，单按 Enter 且非组合键触发发送
      if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        e.stopPropagation();
        handleSendUserMessage();
      }
    });

    // 清除游戏锚定上下文
    document.getElementById('lmod-context-clear').onclick = function () {
      state.activeGame = null;
      updateContextBar();
    };

    updateContextBar();
    updateModeBadge();
  }

  function updateSettingsFormVisibility(mode) {
    const byokBox = document.getElementById('lmod-cfg-byok-box');
    const endpointBox = document.getElementById('lmod-cfg-custom-endpoint-box');
    const provider = document.getElementById('lmod-cfg-byok-provider').value;

    if (mode === 'byok') {
      byokBox.style.display = 'flex';
      endpointBox.style.display = provider === 'custom' ? 'block' : 'none';
    } else {
      byokBox.style.display = 'none';
    }
  }

  function updateModeBadge() {
    const badge = document.getElementById('lmod-mode-badge');
    if (!badge) return;

    if (state.mode === 'cloud') {
      badge.textContent = t('cloudBadge');
      badge.style.background = 'rgba(168, 85, 247, 0.2)';
      badge.style.color = '#c084fc';
    } else if (state.mode === 'byok') {
      badge.textContent = t('byokBadge');
      badge.style.background = 'rgba(59, 130, 246, 0.2)';
      badge.style.color = '#60a5fa';
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
  // 发送消息处理引擎 (防抖互斥锁 + SSE 流式解析 + 本地优雅容灾)
  // =========================================================================
  async function handleSendUserMessage() {
    // 状态机互斥锁校验：若正在发送或正在加载，坚决拒绝任何并发执行
    if (state.isSending || state.isLoading) return;

    const input = document.getElementById('lmod-chat-input');
    const query = input.value.trim();
    if (!query) return;

    // 立即加锁并清空输入框，自适应高度回缩至单行
    state.isSending = true;
    input.value = '';
    input.style.height = 'auto';

    try {
      await sendUserMessage(query);
    } finally {
      // 无论成功还是失败，最终释放发送互斥锁
      state.isSending = false;
    }
  }

  async function sendUserMessage(query) {
    if (state.isLoading) return;

    // 记录用户消息并渲染到列表
    state.messages.push({ role: 'user', text: query });
    appendUserMessageDom(query);

    const container = document.getElementById('lmod-chat-body');
    container.scrollTop = container.scrollHeight;

    // 开启加载指示器
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
      // 1. 若选用了本地离线模式，直接本地 RAG 计算
      if (state.mode === 'local') {
        await new Promise(r => setTimeout(r, 150));
        const result = localRagQuery(query, activeGame);
        removeLoadingIndicator();
        pushAndRenderAssistantMessage(result.text, result.commands, result.batContent);
        return;
      }

      // 2. 若选用开发者自带 Key (BYOK) 模式，直接调用第三方
      if (state.mode === 'byok' && state.byokKey) {
        let result = null;
        if (state.byokProvider === 'gemini') {
          result = await callGeminiApiByok(query, activeGame);
        } else {
          result = await callDeepSeekApiByok(query, activeGame);
        }
        removeLoadingIndicator();
        pushAndRenderAssistantMessage(result.text, result.commands, result.batContent);
        return;
      }

      // 3. 官方云端智能体核心链路：调用 /api/v1/ai/chat (支持 SSE 流式打字机)
      await streamCloudAiChat(query, activeGame);

    } catch (err) {
      console.warn('Official cloud AI error, falling back to local vault:', err);
      removeLoadingIndicator();

      // 零失败容灾机制：自动无缝回退至本地 100 款大作离线知识库
      const fallback = localRagQuery(query, activeGame);
      const fallbackNotice = `> 💡 **老L 提示**：官方云端中继发生轻微网络波动，已无缝切换为**本地高保真离线智库**为您解答：\n\n`;

      pushAndRenderAssistantMessage(fallbackNotice + fallback.text, fallback.commands, fallback.batContent);

    } finally {
      removeLoadingIndicator();
      state.isLoading = false;
      const finalInput = document.getElementById('lmod-chat-input');
      if (finalInput) finalInput.focus();
    }
  }

  function removeLoadingIndicator() {
    const loading = document.getElementById('lmod-loading-indicator');
    if (loading) loading.remove();
  }

  // =========================================================================
  // 官方中继 SSE 流式打字机处理器
  // =========================================================================
  async function streamCloudAiChat(query, activeGame) {
    const container = document.getElementById('lmod-chat-body');

    // 构造请求上下文
    const historyPayload = state.messages.slice(-5).map(m => ({
      role: m.role,
      content: m.text
    }));

    const resp = await fetch('/api/v1/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify({
        query: query,
        game_id: activeGame ? activeGame.id : null,
        history: historyPayload,
        stream: true
      })
    });

    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status} ${resp.statusText}`);
    }

    removeLoadingIndicator();

    // 创建当前流式消息节点
    const msgDiv = document.createElement('div');
    msgDiv.className = 'lmod-msg';
    msgDiv.style.alignSelf = 'flex-start';
    msgDiv.style.maxWidth = '92%';
    msgDiv.style.background = 'rgba(255, 255, 255, 0.05)';
    msgDiv.style.border = '1px solid rgba(255, 255, 255, 0.08)';
    msgDiv.style.color = '#e2e8f0';
    msgDiv.style.padding = '14px';
    msgDiv.style.borderRadius = '14px 14px 14px 2px';
    msgDiv.style.fontSize = '12.5px';
    msgDiv.style.lineHeight = '1.6';
    msgDiv.style.wordBreak = 'break-word';

    // 技能徽章槽位
    const skillsBar = document.createElement('div');
    skillsBar.style.marginBottom = '8px';
    skillsBar.style.display = 'none';
    msgDiv.appendChild(skillsBar);

    // 正文内容槽位 (带打字机光标)
    const contentSpan = document.createElement('div');
    contentSpan.className = 'lmod-typing-cursor';
    msgDiv.appendChild(contentSpan);

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;

    let accumulatedText = '';
    const reader = resp.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split('\n\n');
      buffer = events.pop() || '';

      for (const ev of events) {
        if (!ev.trim()) continue;
        const lines = ev.split('\n');
        let eventType = 'message';
        let dataStr = '';

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            eventType = line.slice(7).trim();
          } else if (line.startsWith('data: ')) {
            dataStr = line.slice(6).trim();
          }
        }

        if (dataStr === '[DONE]') break;

        try {
          const parsed = JSON.parse(dataStr);

          // 1. 元数据包：渲染已激活动态技能徽章
          if (eventType === 'meta' || parsed.type === 'meta') {
            const skills = parsed.skills_triggered || [];
            if (skills.length > 0) {
              skillsBar.innerHTML = skills.map(s => 
                `<span class="lmod-skill-badge" title="${s.detail || ''}">⚡ ${s.name}</span>`
              ).join('');
              skillsBar.style.display = 'block';
            }
          }

          // 2. 增量字符包：累加并实时格式化 Markdown
          if (eventType === 'delta' || parsed.type === 'delta' || parsed.text) {
            const chunk = parsed.text || '';
            accumulatedText += chunk;
            contentSpan.innerHTML = formatMarkdown(accumulatedText);
            container.scrollTop = container.scrollHeight;
          }
        } catch (e) {
          // 非 JSON delta 文本兜底
          if (dataStr) {
            accumulatedText += dataStr;
            contentSpan.innerHTML = formatMarkdown(accumulatedText);
            container.scrollTop = container.scrollHeight;
          }
        }
      }
    }

    // 流式打字完成，移除打字机光标
    contentSpan.classList.remove('lmod-typing-cursor');

    // 挂载代码复制和 .bat 生成动作按钮
    attachCodeActionButtons(msgDiv, null);

    state.messages.push({
      role: 'assistant',
      text: accumulatedText
    });
  }

  function pushAndRenderAssistantMessage(text, commands, batContent) {
    state.messages.push({
      role: 'assistant',
      text: text,
      commands: commands,
      batContent: batContent
    });
    appendAssistantMessageDom(text, commands, batContent);
    const container = document.getElementById('lmod-chat-body');
    if (container) container.scrollTop = container.scrollHeight;
  }

  // =========================================================================
  // 离线 Local RAG 规则引擎 (零延迟 · 100% 免费离线兜底)
  // =========================================================================
  function localRagQuery(rawQuery, contextGame) {
    const query = rawQuery.trim();
    const qLower = query.toLowerCase();
    const games = window.GAMES_DATA || window.GAMES_DATABASE || [];

    const targetGame = findGameByQuery(query) || contextGame || detectActiveGame();

    const isCrashQuery = /闪退|崩溃|打不开|进不去|跳出|报错|crash|black\s*screen|error|eac|ue4ss|cet/i.test(query);
    const isPatchQuery = /补丁|雷达|更新|失效|版本|坏档|patch|update|radar|save/i.test(query);
    const isTrainerQuery = /修改器|风灵月影|热键|白名单|杀毒|fling|trainer|hotkey/i.test(query);
    const isHowToEnable = /怎么开|快捷键|呼出|按键|按什么|如何开启|console\s*shortcut|how\s*to/i.test(query);

    if (targetGame) {
      const locTitle = (targetGame.titles && targetGame.titles['zh-CN']) || targetGame.title;

      if (isCrashQuery) {
        return buildCrashDiagnosisResponse(targetGame, locTitle, query);
      }
      if (isPatchQuery) {
        return buildPatchRadarResponse(targetGame, locTitle);
      }
      if (isTrainerQuery) {
        return buildTrainerResponse(targetGame, locTitle);
      }
      if (isHowToEnable) {
        return buildConsoleGuideResponse(targetGame, locTitle);
      }

      const matchedCommands = searchCommandsInGame(targetGame, query);
      if (matchedCommands.length > 0) {
        return buildCommandsResponse(targetGame, locTitle, matchedCommands, query);
      }

      if (targetGame.scenarioBundles && targetGame.scenarioBundles.length > 0) {
        const bundle = targetGame.scenarioBundles.find(b => 
          qLower.includes(b.name.toLowerCase()) || 
          /新手|毕业|二周目|神装|救赎|套餐|一键/i.test(query)
        ) || targetGame.scenarioBundles[0];

        return buildScenarioBundleResponse(targetGame, locTitle, bundle);
      }

      if (targetGame.popularCommands && targetGame.popularCommands.length > 0) {
        return buildPopularCommandsFallback(targetGame, locTitle, query);
      }
    }

    const globalMatches = searchAcrossAllGames(query, games);
    if (globalMatches.length > 0) {
      return buildGlobalSearchResults(globalMatches, query);
    }

    return {
      text: `### 🎮 未在知识库中找到针对 "${query}" 的完全匹配\n\n` +
            `- **建议操作**：请检查游戏名称或关键词（如输入：“2077无限钱”、“黑神话控制台快捷键”、“老头环闪退排查”）。\n` +
            `- **智能推理**：你也可以直接提问任何游戏攻略或报错现象，老L 将依托全网单机通识库为你实时推导解答！`
    };
  }

  function buildCrashDiagnosisResponse(game, title, query) {
    let diagnosis = `### 💥 《${title}》闪退与 Mod 冲突在线排查指南\n\n`;

    if (game.id === 'cyberpunk-2077') {
      diagnosis += `**CDPR REDengine 4 专属诊断要点**：\n` +
        `1. **CET (Cyber Engine Tweaks) 版本不匹配**：若游戏刚更新了补丁，CET 的 \`bin/x64/plugins/cyber_engine_tweaks.asi\` 必须对应最新版本，否则启动必闪退。\n` +
        `2. **REDscript 缓存损坏**：删除游戏根目录 \`r6/cache/modded\` 文件夹，重新运行游戏让系统重新编译脚本。\n` +
        `3. **旧版 ArchiveXL / TweakXL 冲突**：确保前置核心库均升级至匹配当前补丁的版本。\n`;
    } else if (game.id === 'elden-ring' || game.id === 'sekiro') {
      diagnosis += `**FromSoftware 引擎专属诊断要点**：\n` +
        `1. **EAC 反作弊未关闭拦截**：必须将 \`start_protected_game.exe\` 替换或使用离线引导，否则带 Mod 启动必被 EAC 拦截闪退。\n` +
        `2. **ModEngine2 引导路径错误**：检查 \`config_eldenring.toml\` 中 mod 路径是否正确指向 mod 文件夹。\n` +
        `3. **版本更新坏档**：黄金树幽影 v1.14+ 补丁重构了部分 Regulation.bin 参数，旧版参数文件会导致主菜单加载闪退。\n`;
    } else if (game.id === 'black-myth-wukong' || game.id === 'palworld') {
      diagnosis += `**虚幻引擎 (UE5) 专属诊断要点**：\n` +
        `1. **DX12 着色器编译崩溃**：在 Steam 启动项中添加 \`-dx11\` 强制使用 DirectX 11 启动测试。\n` +
        `2. **UE4SS 注入器冲突**：检查 \`ue4ss.ini\`，尝试将 \`GuiConsoleEnabled = 0\` 关闭以排查图形钩子崩溃。\n` +
        `3. **Pak Mod 冲突**：将 \`~mods\` 文件夹重命名为 \`~mods_backup\`，逐个排查损坏的 Mod。\n`;
    } else if (game.id.includes('skyrim') || game.id.includes('fallout-4') || game.id === 'starfield') {
      diagnosis += `**Bethesda Creation 引擎专属诊断要点**：\n` +
        `1. **脚本扩展器 (SKSE64 / F4SE) 版本对齐**：检查游戏主程序版本，次世代版与旧版脚本扩展器绝不可混用。\n` +
        `2. **Address Library 前置缺失**：几乎所有现代 DLL Mod 都依赖 Address Library for SKSE Plugins，请确保安装了最新版。\n` +
        `3. **排序冲突**：使用 LOOT 自动重新排序 ESP/ESM/ESL 加载顺序。\n`;
    } else {
      diagnosis += `**通用单机 Mod 闪退排查四部曲**：\n` +
        `1. **重命名 Mod 文件夹进行二分法排查**：临时禁用 Mod 目录，确认是否为纯净原版能正常启动；\n` +
        `2. **检查防作弊与注入 DLL**：检查是否有 \`dinput8.dll\`, \`dxgi.dll\`, \`version.dll\` 等钩子文件与显卡驱动 overlay 冲突；\n` +
        `3. **管理员权限与杀毒白名单**：Windows Defender 常误杀注入型 DLL，请将游戏根目录加入排除项；\n` +
        `4. **验证 Steam 游戏文件完整性**：右键游戏属性 -> 已安装文件 -> 验证游戏文件的完整性。\n`;
    }

    if (game.pitfallNote) {
      diagnosis += `\n> ⚠️ **老L 独家避坑备注**：\n> ${game.pitfallNote}\n`;
    }

    return { text: diagnosis };
  }

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
      res += `本游戏更推荐使用官方内置或注入式控制台，更加稳定且杜绝报毒！\n`;
    }

    if (game.trainerInfo && game.trainerInfo.powershellExclusionCmd) {
      res += `\n#### 🛡️ Windows Defender 误报秒解指令 (管理员 PowerShell 运行)：\n` +
             `\`\`\`powershell\n${game.trainerInfo.powershellExclusionCmd}\n\`\`\`\n`;
    }

    return { text: res };
  }

  function buildConsoleGuideResponse(game, title) {
    let res = `### 🛠️ 《${title}》控制台唤出与开启方法\n\n`;
    res += `- **控制台支持情况**：${game.hasConsole ? '✅ 支持控制台' : '⚠️ 需第三方前置注入'}\n`;
    if (game.consoleShortcut) res += `- **默认呼出按键**：\`${game.consoleShortcut}\`\n\n`;

    const guide = (game.consoleEnableGuide && (game.consoleEnableGuide['zh-CN'] || game.consoleEnableGuide['en'])) ||
                  game.consoleEnableGuide || '进入游戏后按下快捷键即可呼出输入框。';

    res += `**详细开启步骤**：\n${guide}\n`;
    return { text: res };
  }

  function searchCommandsInGame(game, query) {
    const q = query.toLowerCase();
    const results = [];

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

    const unique = [];
    const seen = new Set();
    for (const c of results) {
      if (c.code && !seen.has(c.code)) {
        seen.add(c.code);
        unique.push(c);
      }
    }

    return unique.slice(0, 8);
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
  // BYOK 私有 API 调用支持 (开发者调试)
  // =========================================================================
  async function callGeminiApiByok(prompt, contextGame) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${encodeURIComponent(state.byokKey)}`;
    let sysContext = `你是老L，L-MOD Vault 官方单机游戏智库顾问。请严格给出真实底层指令，代码用 Markdown 代码块包裹。`;
    if (contextGame) sysContext += `当前游戏: ${contextGame.title}`;

    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: `${sysContext}\n\n用户问题: ${prompt}` }] }],
        generationConfig: { temperature: 0.3 }
      })
    });
    if (!resp.ok) throw new Error(`Gemini BYOK 响应异常: ${resp.status}`);
    const data = await resp.json();
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text || '无返回';
    return { text };
  }

  async function callDeepSeekApiByok(prompt, contextGame) {
    const endpoint = state.customEndpoint || 'https://api.deepseek.com/chat/completions';
    const resp = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${state.byokKey}`
      },
      body: JSON.stringify({
        model: state.customModel || 'deepseek-chat',
        messages: [{ role: 'user', content: prompt }],
        temperature: 0.3
      })
    });
    if (!resp.ok) throw new Error(`DeepSeek BYOK 响应异常: ${resp.status}`);
    const data = await resp.json();
    const text = data.choices?.[0]?.message?.content || '无返回';
    return { text };
  }

  // =========================================================================
  // DOM 节点追加与 Markdown 渲染
  // =========================================================================
  function renderMessages() {
    const container = document.getElementById('lmod-chat-body');
    if (!container) return;

    container.innerHTML = '';
    if (state.messages.length === 0) {
      appendAssistantMessageDom(t('welcomeMessage'));
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

    div.innerHTML = formatMarkdown(text);
    attachCodeActionButtons(div, batContent);

    container.appendChild(div);
  }

  function formatMarkdown(md) {
    if (!md) return '';

    let html = md
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/^### (.*$)/gim, '<div style="font-weight: 700; font-size: 14px; color: #a78bfa; margin: 8px 0 4px 0;">$1</div>')
      .replace(/^#### (.*$)/gim, '<div style="font-weight: 600; font-size: 13px; color: #f3f4f6; margin: 6px 0 2px 0;">$1</div>')
      .replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, function (match, lang, code) {
        return `<div class="lmod-code-box" data-code="${encodeURIComponent(code)}">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; font-size: 10px; color: #9ca3af; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 4px;">
            <span>${lang || 'CODE'}</span>
            <button class="lmod-btn-action lmod-btn-copy" onclick="window.LMOD_AI_COPILOT.copyCode(this)">📋 ${t('copyCode')}</button>
          </div>
          <pre style="margin: 0; white-space: pre-wrap; word-break: break-all; color: #a5f3fc;">${code}</pre>
        </div>`;
      })
      .replace(/`([^`]+)`/g, '<code style="background: rgba(168,85,247,0.15); color: #d8b4fe; padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 11.5px;">$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong style="color: #ffffff; font-weight: 600;">$1</strong>')
      .replace(/^> (.*$)/gim, '<div style="border-left: 3px solid #A855F7; padding-left: 8px; margin: 6px 0; color: #cbd5e1; font-style: italic; background: rgba(168,85,247,0.05); padding: 6px 10px; border-radius: 0 6px 6px 0;">$1</div>')
      .replace(/^\s*-\s+(.*$)/gim, '<div style="display: flex; gap: 6px; margin: 2px 0;"><span style="color: #A855F7;">•</span><span>$1</span></div>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" style="color: #c084fc; text-decoration: underline;">$1</a>')
      .replace(/\n\n/g, '<div style="height: 8px;"></div>');

    return html;
  }

  function attachCodeActionButtons(div, batContent) {
    // 自动为所有代码块挂载点击复制支持
    div.querySelectorAll('.lmod-code-box').forEach(box => {
      const copyBtn = box.querySelector('.lmod-btn-copy');
      if (copyBtn) {
        copyBtn.onclick = function (e) {
          e.stopPropagation();
          copyCode(this);
        };
      }
    });

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
      window.showToast('已生成并下载 .bat 批处理脚本！');
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
      const ta = document.createElement('textarea');
      ta.value = code;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      if (window.showToast) window.showToast(t('copied'));
    });
  }

  // =========================================================================
  // 抽屉与界面控制
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
    document.getElementById('lmod-cfg-byok-provider').value = state.byokProvider;
    document.getElementById('lmod-cfg-byok-key').value = state.byokKey;
    document.getElementById('lmod-cfg-endpoint').value = state.customEndpoint;

    updateSettingsFormVisibility(state.mode);
    modal.style.display = 'flex';
  }

  function closeSettings() {
    const modal = document.getElementById('lmod-settings-modal');
    if (modal) modal.style.display = 'none';
  }

  function handleSaveSettings() {
    state.mode = document.getElementById('lmod-cfg-mode').value;
    state.byokProvider = document.getElementById('lmod-cfg-byok-provider').value;
    state.byokKey = document.getElementById('lmod-cfg-byok-key').value.trim();
    state.customEndpoint = document.getElementById('lmod-cfg-endpoint').value.trim();

    saveConfig();
    updateModeBadge();
    closeSettings();

    if (window.showToast) {
      window.showToast('AI 引擎配置已更新！');
    }
  }

  function clearChatHistory() {
    state.messages = [];
    renderMessages();
  }

  // 全局快捷键 Cmd+K / Ctrl+K 呼出，Esc 关闭
  window.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
      e.preventDefault();
      toggleDrawer();
    } else if (e.key === 'Escape' && state.isOpen) {
      closeDrawer();
    }
  });

  // 全局暴露 API
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

  // 页面就绪自动初始化
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
