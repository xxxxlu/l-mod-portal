/**
 * L-MOD Vault - Player-Facing AI Copilot (老L · 官方 AI 游戏智库顾问)
 * ==============================================================================
 * 纯净前台对话架构 (Zero-Config, Pure Chat Experience)：
 * 1. 【彻底移除前台 API Key 设置】：
 *    - 前台玩家端绝不暴露任何 API Key 输入框或设置弹窗
 *    - 站长在中台 (/admin) 统一配置云端大模型，前台只负责纯粹、高效的游戏智库对话
 * 2. 【彻底修复回车双发 Bug】：
 *    - 严格监听中文拼音组合状态 (isComposing / compositionstart / compositionend / keyCode === 229)
 *    - 状态机双重互斥锁 (state.isSending & state.isLoading)，彻底杜绝连续并发误投递
 *    - Shift+Enter 换行，单 Enter 发送，Textarea 自适应高度弹性回缩
 * 3. 【官方中继流式打字机 + 本地双层容灾】：
 *    - 直连官方 Edge 中继 (/api/v1/ai/chat)，Server-Sent Events (SSE) 逐字极客流式打字
 *    - 包含“你能干什么”等通用意图及网络断开时的 100% 本地极速兜底，绝不卡顿或白屏
 * 4. 【高可用工具链】：
 *    - 真实代码一键复制、一键生成 Windows .bat 批处理注入脚本
 */

(function () {
  'use strict';

  // 防止重复初始化
  if (window.LMOD_AI_COPILOT) return;

  // 对话状态机
  const state = {
    isOpen: false,
    activeGame: null,
    isSending: false, // 发送互斥锁 (防抖/防连击)
    isLoading: false, // 网络加载/流式输出锁
    messages: []
  };

  // 国际化文字字典
  const i18n = {
    'zh-CN': {
      title: '老L · 官方 AI 智库顾问',
      tagline: '控制台代码 · 闪退排查 · 补丁雷达 · 一键脚本',
      globalContext: '全网 100 款单机大作智库',
      activeContextPrefix: '当前游戏: ',
      clearContext: '切回全局',
      inputPlaceholder: '输入你的问题，如：“2077怎么刷四季宝”、“法环闪退排查”、“黑神话广智怎么打”...',
      sendBtn: '发送',
      thinking: '老L 正在调取 D1 智库底层指令与 4 大专属 Skills...',
      copyCode: '复制指令',
      copied: '已复制到剪贴板！',
      downloadBat: '生成 .bat 脚本',
      close: '关闭',
      clearHistory: '清空会话',
      welcomeMessage: '我是**老L**，L-MOD Vault 官方单机游戏智库首席顾问！\n\n已为你接入**官方统一云端智能体**与 **4 大专属 Skills 技能链**：\n- 🔍 **查核心控制台代码**：“给我赛博朋克2077强尼的保时捷代码”\n- 💥 **闪退坏档逃课排查**：“博德之门3打Mod闪退怎么解决”\n- 📡 **Steam 补丁避坑雷达**：“艾尔登法环当前版本能打Mod吗”\n- 🎮 **单机攻略与配置通识**：“黑神话悟空推荐画质设置”',
      pillCommands: '🔍 查核心作弊代码',
      pillCrash: '💥 闪退与冲突排查',
      pillPatch: '📡 最新补丁避坑状态',
      pillTrainer: '⚡ 修改器热键与防误报',
      cloudBadge: '官方云端驱动'
    },
    'en': {
      title: 'Old L · Official AI Vault Advisor',
      tagline: 'Console Codes / Crash Doctor / Patch Radar / Script Gen',
      globalContext: 'Global 100 Games Vault',
      activeContextPrefix: 'Active Game: ',
      clearContext: 'Reset to Global',
      inputPlaceholder: 'Ask a question, e.g. "Cyberpunk Johnny Porsche code", "Elden Ring crash fix"...',
      sendBtn: 'Send',
      thinking: 'Old L is orchestrating D1 commands & 4 agentic skills...',
      copyCode: 'Copy Code',
      copied: 'Copied to clipboard!',
      downloadBat: 'Download .bat',
      close: 'Close',
      clearHistory: 'Clear Chat',
      welcomeMessage: "I'm **Old L**, your official single-player game modding and console command advisor!\n\nArmed with **Official Cloud Agent + 4 Exclusive Skills**:\n- 🔍 **Find Real Commands**: 'Johnny Silverhand Porsche code for Cyberpunk 2077'\n- 💥 **Crash & Mod Fixes**: 'Baldur\\'s Gate 3 crashes with mods, how to fix?'\n- 📡 **Patch Radar**: 'Can I safely mod on the latest Elden Ring patch?'\n- 🎮 **General Guide**: 'Best graphics settings for Black Myth: Wukong'",
      pillCommands: '🔍 Key Console Codes',
      pillCrash: '💥 Crash & Mod Doctor',
      pillPatch: '📡 Patch Radar Status',
      pillTrainer: '⚡ Trainer Hotkeys',
      cloudBadge: 'Official Cloud Agent'
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

  // 智能环境探测：获取当前页面锚定的单机游戏
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
      '艾尔登法环': 'elden-ring',
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
  // DOM 抽屉渲染与事件绑定 (纯净对话交互 · 无任何设置弹窗)
  // =========================================================================
  function injectDrawerHtml() {
    if (document.getElementById('lmod-ai-drawer')) return;

    // 1. 背景遮罩
    const backdrop = document.createElement('div');
    backdrop.id = 'lmod-ai-backdrop';
    backdrop.onclick = closeDrawer;
    document.body.appendChild(backdrop);

    // 2. 右下角悬浮入口按钮
    const fab = document.createElement('div');
    fab.id = 'lmod-ai-fab';
    fab.title = '老L · 官方 AI 智库顾问 (Cmd+K / Ctrl+K)';
    fab.innerHTML = `
      <span class="fab-ping"></span>
      <span style="font-size: 16px;">🤖</span>
      <span style="font-weight: 700; font-size: 13px; letter-spacing: 0.2px;">AI 顾问</span>
      <span style="font-size: 10px; opacity: 0.7; font-family: monospace; background: rgba(0,0,0,0.2); padding: 1px 5px; border-radius: 4px;">⌘K</span>
    `;
    fab.onclick = toggleDrawer;
    document.body.appendChild(fab);

    // 3. 抽屉容器 (纯净无设置按钮)
    const drawer = document.createElement('div');
    drawer.id = 'lmod-ai-drawer';
    drawer.innerHTML = `
      <!-- 头部：标题与状态微标 (仅保留清空与关闭) -->
      <div style="padding: 16px 20px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; background: rgba(255, 255, 255, 0.02);">
        <div style="display: flex; align-items: center; gap: 10px;">
          <div style="width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #8b5cf6, #ec4899); display: flex; align-items: center; justify-content: center; font-size: 18px; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.4);">
            🤖
          </div>
          <div>
            <div style="font-weight: 700; font-size: 14px; display: flex; align-items: center; gap: 6px;">
              <span>${t('title')}</span>
              <span id="lmod-mode-badge" style="font-size: 9px; padding: 2px 6px; border-radius: 4px; background: rgba(168, 85, 247, 0.2); color: #c084fc; font-weight: 600;">⚡ 官方云端驱动</span>
            </div>
            <div style="font-size: 11px; color: #9ca3af; margin-top: 1px;" id="lmod-tagline">${t('tagline')}</div>
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <button id="lmod-btn-clear" title="清空对话" style="background: none; border: none; color: #9ca3af; cursor: pointer; padding: 6px; border-radius: 8px; transition: color 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#9ca3af'">
            🗑️
          </button>
          <button id="lmod-btn-close" title="关闭 (Esc)" style="background: none; border: none; color: #9ca3af; cursor: pointer; padding: 6px; border-radius: 8px; transition: color 0.2s;" onmouseover="this.style.color='#fff'" onmouseout="this.style.color='#9ca3af'">
            ✕
          </button>
        </div>
      </div>

      <!-- 游戏上下文锚定条 -->
      <div id="lmod-context-bar" style="padding: 8px 16px; background: rgba(168, 85, 247, 0.08); border-bottom: 1px solid rgba(168, 85, 247, 0.15); font-size: 11px; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 6px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
          <span style="color: #A855F7;">🎮</span>
          <span id="lmod-context-text" style="color: #d8b4fe; font-weight: 600;">${t('globalContext')}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
          <button id="lmod-context-clear" style="display: none; background: rgba(255,255,255,0.06); border: none; color: #cbd5e1; font-size: 10px; padding: 2px 6px; border-radius: 4px; cursor: pointer;">${t('clearContext')}</button>
        </div>
      </div>

      <!-- 快捷问题胶囊 -->
      <div id="lmod-quick-pills" style="padding: 10px 16px; display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; border-bottom: 1px solid rgba(255, 255, 255, 0.05); background: rgba(0,0,0,0.15);">
        <button class="lmod-pill" data-prompt="${t('pillCommands')}">${t('pillCommands')}</button>
        <button class="lmod-pill" data-prompt="${t('pillCrash')}">${t('pillCrash')}</button>
        <button class="lmod-pill" data-prompt="${t('pillPatch')}">${t('pillPatch')}</button>
        <button class="lmod-pill" data-prompt="${t('pillTrainer')}">${t('pillTrainer')}</button>
      </div>

      <!-- 对话消息列表 -->
      <div id="lmod-chat-body" style="flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 14px; scroll-behavior: smooth;">
        <!-- 动态消息节点 -->
      </div>

      <!-- 输入栏 (纯对话交互，彻底去除引擎配置) -->
      <div style="padding: 14px 16px; border-top: 1px solid rgba(255, 255, 255, 0.08); background: rgba(14, 16, 22, 0.98); display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; gap: 8px; align-items: flex-end;">
          <textarea id="lmod-chat-input" rows="1" placeholder="${t('inputPlaceholder')}" style="flex: 1; resize: none; max-height: 120px; min-height: 40px; background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 12px; padding: 10px 14px; color: #ffffff; font-size: 13px; outline: none; font-family: inherit; line-height: 1.4; transition: border-color 0.2s; box-sizing: border-box;"></textarea>
          <button id="lmod-btn-send" style="background: linear-gradient(135deg, #8b5cf6, #A855F7); border: none; border-radius: 12px; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; color: #fff; cursor: pointer; flex-shrink: 0; box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3); transition: transform 0.2s;">
            <svg style="width: 18px; height: 18px; fill: currentColor;" viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
          </button>
        </div>
        <div style="font-size: 11px; color: #6b7280; text-align: center; display: flex; justify-content: space-between; align-items: center;">
          <span>Enter 发送 / Shift+Enter 换行</span>
          <span style="color: #a78bfa; font-size: 10px;">⚡ 4 大 Skills 实时守护</span>
        </div>
      </div>
    `;
    document.body.appendChild(drawer);

    // 绑定基础事件
    document.getElementById('lmod-btn-close').onclick = closeDrawer;
    document.getElementById('lmod-btn-clear').onclick = clearChatHistory;
    document.getElementById('lmod-btn-send').onclick = handleSendUserMessage;

    // 快捷胶囊点击事件
    document.querySelectorAll('#lmod-quick-pills .lmod-pill').forEach(btn => {
      btn.onclick = function () {
        const prompt = this.getAttribute('data-prompt');
        sendUserMessage(prompt);
      };
    });

    // -----------------------------------------------------------------------
    // 中文拼音输入法状态机 + 彻底根治回车双发 Bug
    // -----------------------------------------------------------------------
    const input = document.getElementById('lmod-chat-input');
    let isComposing = false;

    input.addEventListener('compositionstart', function () {
      isComposing = true;
    });

    input.addEventListener('compositionend', function () {
      setTimeout(() => {
        isComposing = false;
      }, 50);
    });

    // Textarea 自适应弹性高度扩展
    input.addEventListener('input', function () {
      this.style.height = 'auto';
      this.style.height = Math.min(this.scrollHeight, 120) + 'px';
    });

    // 严格键盘拦截：杜绝拼音上屏回车误触发与连发
    input.addEventListener('keydown', function (e) {
      if (e.isComposing || isComposing || e.keyCode === 229) {
        return;
      }

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
  // 发送消息处理引擎 (防抖互斥锁 + 官方云端中继 SSE 流式打字机 + 本地兜底)
  // =========================================================================
  async function handleSendUserMessage() {
    if (state.isSending || state.isLoading) return;

    const input = document.getElementById('lmod-chat-input');
    const query = input.value.trim();
    if (!query) return;

    state.isSending = true;
    input.value = '';
    input.style.height = 'auto';

    try {
      await sendUserMessage(query);
    } finally {
      state.isSending = false;
    }
  }

  async function sendUserMessage(query) {
    if (state.isLoading) return;

    // 记录用户消息并展示
    state.messages.push({ role: 'user', text: query });
    appendUserMessageDom(query);

    const container = document.getElementById('lmod-chat-body');
    container.scrollTop = container.scrollHeight;

    // 开启 loading 指示器
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
      // 官方云端中继链路 (SSE 流式打字机输出)
      await streamCloudAiChat(query, activeGame);

    } catch (err) {
      console.warn('Official cloud AI stream error, falling back to instant local vault:', err);
      removeLoadingIndicator();

      // 双层高可用容灾：发生网络断网或接口异常时，本地知识库秒级兜底解答
      const fallback = localRagQuery(query, activeGame);
      pushAndRenderAssistantMessage(fallback.text, fallback.commands, fallback.batContent);

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

    // 创建当前流式输出节点
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

    const skillsBar = document.createElement('div');
    skillsBar.style.marginBottom = '8px';
    skillsBar.style.display = 'none';
    msgDiv.appendChild(skillsBar);

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

          // 1. 元数据包：渲染已激活技能徽章
          if (eventType === 'meta' || parsed.type === 'meta') {
            const skills = parsed.skills_triggered || [];
            if (skills.length > 0) {
              skillsBar.innerHTML = skills.map(s => 
                `<span class="lmod-skill-badge" title="${s.detail || ''}">⚡ ${s.name}</span>`
              ).join('');
              skillsBar.style.display = 'block';
            }
          }

          // 2. 增量字符包：实时打字机
          if (eventType === 'delta' || parsed.type === 'delta' || parsed.text) {
            const chunk = parsed.text || '';
            accumulatedText += chunk;
            contentSpan.innerHTML = formatMarkdown(accumulatedText);
            container.scrollTop = container.scrollHeight;
          }
        } catch (e) {
          if (dataStr) {
            accumulatedText += dataStr;
            contentSpan.innerHTML = formatMarkdown(accumulatedText);
            container.scrollTop = container.scrollHeight;
          }
        }
      }
    }

    // 打字完成，移除光标并挂载操作按钮
    contentSpan.classList.remove('lmod-typing-cursor');
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
  // 本地极速兜底知识库 (断网容灾保障，包含“你能干什么”等自我介绍)
  // =========================================================================
  function localRagQuery(rawQuery, contextGame) {
    const query = rawQuery.trim();
    const qLower = query.toLowerCase();
    const games = window.GAMES_DATA || window.GAMES_DATABASE || [];

    // 通用功能介绍与问候处理
    if (/你能干什么|有什么用|你是谁|功能|帮助|help|who are you|what can you do/i.test(query)) {
      return {
        text: `### 🤖 我是老L，你的官方单机游戏智库顾问！\n\n` +
              `我由 **L-MOD Vault 官方 D1 分布式智库 + 4 大专属 Skills** 统一驱动，专为单机玩家解决一切疑难杂症：\n\n` +
              `- 🔍 **【查游戏核心代码】**：秒级调取 2077、黑神话、老头环、博德之门3 等 100 款大作已核验真实控制台代码；\n` +
              `- 💥 **【闪退报错逃课诊断】**：针对 EAC 反作弊、UE4SS、CET、DirectX、0xc0000005 闪退等给出硬核解决方案；\n` +
              `- 📡 **【Steam 避坑雷达】**：实时检测游戏最新推送补丁是否会导致 Mod 失效或破坏存档；\n` +
              `- ⚡ **【纯净修改器与脚本】**：提供一键复制命令、Windows .bat 批处理注入脚本与热键说明。\n\n` +
              `你可以直接向我提问，如：“2077怎么刷四季宝”、“法环闪退排查”、“黑神话广智代码”！`
      };
    }

    const targetGame = findGameByQuery(query) || contextGame || detectActiveGame();

    const isCrashQuery = /闪退|崩溃|打不开|进不去|跳出|报错|crash|black\s*screen|error|eac|ue4ss|cet/i.test(query);
    const isPatchQuery = /补丁|雷达|更新|失效|版本|坏档|patch|update|radar|save/i.test(query);
    const isTrainerQuery = /修改器|风灵月影|热键|白名单|杀毒|fling|trainer|hotkey/i.test(query);
    const isHowToEnable = /怎么开|快捷键|呼出|按键|按什么|如何开启|console\s*shortcut|how\s*to/i.test(query);

    if (targetGame) {
      const locTitle = (targetGame.titles && targetGame.titles['zh-CN']) || targetGame.title;

      if (isCrashQuery) return buildCrashDiagnosisResponse(targetGame, locTitle, query);
      if (isPatchQuery) return buildPatchRadarResponse(targetGame, locTitle);
      if (isTrainerQuery) return buildTrainerResponse(targetGame, locTitle);
      if (isHowToEnable) return buildConsoleGuideResponse(targetGame, locTitle);

      const matchedCommands = searchCommandsInGame(targetGame, query);
      if (matchedCommands.length > 0) return buildCommandsResponse(targetGame, locTitle, matchedCommands, query);

      if (targetGame.popularCommands && targetGame.popularCommands.length > 0) {
        return buildPopularCommandsFallback(targetGame, locTitle, query);
      }
    }

    const globalMatches = searchAcrossAllGames(query, games);
    if (globalMatches.length > 0) {
      return buildGlobalSearchResults(globalMatches, query);
    }

    return {
      text: `### 🎮 老L 已收到你的提问：“${query}”\n\n` +
            `- **提问建议**：推荐带上具体游戏名称或关键词（如输入：“2077无限钱”、“黑神话控制台快捷键”、“老头环闪退排查”）。\n` +
            `- 也可以直接询问游戏通关攻略、画质优化、MO2 模组工具等任何单机话题！`
    };
  }

  function buildCrashDiagnosisResponse(game, title, query) {
    let diagnosis = `### 💥 《${title}》闪退与 Mod 冲突在线排查指南\n\n`;

    if (game.id === 'cyberpunk-2077') {
      diagnosis += `**CDPR REDengine 4 专属诊断要点**：\n` +
        `1. **CET 版本不匹配**：若游戏刚更新了补丁，CET 的 \`cyber_engine_tweaks.asi\` 必须对应最新版本，否则启动必闪退。\n` +
        `2. **REDscript 缓存损坏**：彻底删除游戏根目录 \`r6/cache/modded\` 文件夹让引擎重新编译脚本。\n` +
        `3. **旧版 ArchiveXL / TweakXL 冲突**：确保前置核心库均升级至匹配当前补丁的版本。\n`;
    } else if (game.id === 'elden-ring' || game.id === 'sekiro') {
      diagnosis += `**FromSoftware 引擎专属诊断要点**：\n` +
        `1. **EAC 反作弊未关闭拦截**：必须替换 \`start_protected_game.exe\` 或离线引导，否则带 Mod 启动必被 EAC 拦截闪退。\n` +
        `2. **ModEngine2 引导路径错误**：检查 \`config_eldenring.toml\` 中 mod 路径是否正确指向 mod 文件夹。\n` +
        `3. **版本更新坏档**：黄金树幽影大补丁重构了 Regulation.bin，旧版参数文件会导致主菜单加载闪退。\n`;
    } else if (game.id === 'black-myth-wukong' || game.id === 'palworld') {
      diagnosis += `**虚幻引擎 (UE5) 专属诊断要点**：\n` +
        `1. **DX12 着色器编译崩溃**：在 Steam 启动项中添加 \`-dx11\` 强制使用 DirectX 11 启动测试。\n` +
        `2. **UE4SS 注入器冲突**：检查 \`ue4ss.ini\`，设置 \`GuiConsoleEnabled = 0\` 关闭图形钩子以排查崩溃。\n` +
        `3. **Pak Mod 冲突**：将 \`~mods\` 文件夹重命名为 \`~mods_backup\`，逐步二分法排查损坏的 Mod。\n`;
    } else {
      diagnosis += `**通用单机 Mod 闪退排查要点**：\n` +
        `1. **二分法排查 Mod**：临时重命名 Mod 目录，验证纯净原版能否正常启动；\n` +
        `2. **排查杀毒误杀**：Windows Defender 常误杀注入型 DLL (dinput8.dll, dxgi.dll)，将游戏根目录添加至安全白名单；\n` +
        `3. **验证游戏完整性**：右键 Steam 游戏属性 -> 已安装文件 -> 验证游戏文件的完整性。\n`;
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
    if (game.radarRiskTitle) res += `\n#### ⚠️ 风险通报：${game.radarRiskTitle}\n`;
    if (game.pitfallNote) res += `\n> 💡 **避坑锦囊**：\n> ${game.pitfallNote}\n`;

    res += `\n[进入《Steam 补丁避坑雷达独立看板》查看完整 100 款对账](radar?game=${game.id})`;
    return { text: res };
  }

  function buildTrainerResponse(game, title) {
    let res = `### ⚡ 《${title}》纯净修改器与快捷键一览\n\n`;
    if (game.trainerHotkeys && game.trainerHotkeys.length > 0) {
      res += `**常用快捷热键**：\n\n`;
      for (const hk of game.trainerHotkeys) {
        res += `- \`${hk.key}\`：${hk.action}\n`;
      }
    } else {
      res += `本游戏更推荐使用官方内置或注入式控制台，更加稳定且杜绝误报报毒！\n`;
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
      if (m.cmd) res += `- 包含指令 **${m.cmd.name}**: \`${m.cmd.code}\`\n`;
      res += `[点击进入《${title}》专区查看](#game=${g.id})\n\n`;
    }
    return { text: res };
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

  // 全局暴露 API (无任何 openSettings)
  window.LMOD_AI_COPILOT = {
    openDrawer: openDrawer,
    closeDrawer: closeDrawer,
    toggleDrawer: toggleDrawer,
    sendUserMessage: sendUserMessage,
    copyCode: copyCode,
    downloadBatchFile: downloadBatchFile,
    setActiveGame: function (game) {
      state.activeGame = game;
      updateContextBar();
    }
  };

  // 页面就绪自动初始化
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
