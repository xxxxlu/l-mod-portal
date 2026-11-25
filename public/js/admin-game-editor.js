/**
 * L-MOD Vault 后台 ——「游戏数据」页签：游戏列表 + 按块编辑整份游戏数据
 * ==============================================================================
 * 真源是 D1 games.raw_json（和 data.js 的 GAMES_DATA 每一项同形）。编辑器在整份文档上改，保存时整份交给
 * POST /api/v1/admin/games/save；服务器校验、重建派生表、写审计日志、让公开目录的缓存失效 —— 刷新网站就能看到。
 *
 * - 雷达 / 修改器字段归每天的定时任务，这里只读显示；保存时服务器保留库里原值。
 * - 不认识的字段原样保留（表单直接改文档对象上的字段，不重新拼对象）；「整份 JSON」块能改任何字段。
 * - 只能隐藏游戏，不能删除（删 games 的行会连带删掉玩家收藏和订阅）。
 *
 * 依赖 admin.html 导出的 window.LmodAdminApi = { apiFetch, showToast }。
 */
(function () {
  'use strict';

  const LANGS = [
    ['zh-CN', '简体中文'], ['en', 'English'], ['zh-TW', '繁體中文'], ['ja', '日本語'],
    ['ko', '한국어'], ['ru', 'Русский'], ['de', 'Deutsch'], ['es', 'Español']
  ];
  const ZH_EN = LANGS.slice(0, 2);
  const HEAT_TIERS = [['solar', 'solar'], ['violet', 'violet'], ['cyan', 'cyan'], ['emerald', 'emerald']];
  const SYNTAX_TYPES = ['lua_function', 'redengine_cmd', 'creation_hex', 'gm_command', 'unity_dev', 'rage_cheat',
    'ue_console', 'engine_console'];
  const BLOCKS = [
    ['basic', '基本信息'], ['console', '控制台与指令'], ['bundles', '场景套餐'], ['mods', '精选 Mod'],
    ['trainer', '修改器（只读）'], ['pitfall', '避坑笔记'], ['radar', '雷达（只读）'], ['json', '整份 JSON']
  ];
  const RADAR_PILLS = {
    green: ['🟢 近期平稳', 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'],
    yellow: ['🟡 留意更新', 'bg-amber-500/10 text-amber-400 border-amber-500/20'],
    red: ['🔴 先别更新', 'bg-rose-500/10 text-rose-400 border-rose-500/20']
  };

  const INPUT = 'w-full bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-2 text-xs text-white ' +
    'placeholder-slate-600 focus:outline-none focus:border-purple-500';
  const BTN = 'px-3 py-1.5 rounded-lg text-xs font-semibold transition disabled:opacity-40 disabled:cursor-not-allowed';
  const BTN_GHOST = `${BTN} bg-slate-800 hover:bg-slate-700 text-slate-200`;
  const BTN_PRIMARY = `${BTN} bg-purple-600 hover:bg-purple-500 text-white shadow-md shadow-purple-600/30`;
  const BTN_DANGER = `${BTN} bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30`;

  const api = () => window.LmodAdminApi;
  let listCache = [];

  // 编辑器状态
  const ed = {
    create: false, id: null, rev: null, hidden: false, updatedAt: null,
    doc: null, baseline: '', machine: null, block: 'basic',
    errors: [], warnings: [], notice: null, jsonError: null, busy: false, history: null
  };
  const openItems = new WeakSet(); // 列表项展开状态（按对象记）

  // ---------------------------------------------------------------------------
  // DOM 小工具
  // ---------------------------------------------------------------------------
  function h(tag, attrs, ...children) {
    const el = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === null || v === undefined || v === false) continue;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k === 'value') el.value = v;
      else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? '' : v);
    }
    for (const c of children.flat(Infinity)) {
      if (c === null || c === undefined || c === false) continue;
      el.appendChild(typeof c === 'string' || typeof c === 'number' ? document.createTextNode(String(c)) : c);
    }
    return el;
  }

  const isObj = v => Boolean(v) && typeof v === 'object' && !Array.isArray(v);
  const textOf = v => (isObj(v) ? (v['zh-CN'] || v.en || '') : (v === null || v === undefined ? '' : String(v)));
  const today = () => new Date().toISOString().slice(0, 10);

  function section(title, hint, ...body) {
    return h('section', { class: 'space-y-3 rounded-xl border border-slate-800 bg-slate-900/40 p-4' },
      h('div', null,
        h('h4', { class: 'text-sm font-bold text-white', text: title }),
        hint ? h('p', { class: 'text-[11px] text-slate-500 mt-0.5', text: hint }) : null),
      ...body);
  }

  function grid(...cells) {
    return h('div', { class: 'grid grid-cols-1 sm:grid-cols-2 gap-3' }, ...cells);
  }

  function field(label, control, hint) {
    return h('label', { class: 'block space-y-1' },
      h('span', { class: 'block text-[11px] text-slate-400', text: label }),
      control,
      hint ? h('span', { class: 'block text-[10px] text-slate-500 leading-relaxed', text: hint }) : null);
  }

  // ---------------------------------------------------------------------------
  // 表单控件：直接读写文档对象上的字段
  // ---------------------------------------------------------------------------
  function changed() {
    scheduleHeader();
  }

  /** optional：清空时删掉这个字段（免得给原本没有的字段塞空串） */
  function textInput(obj, key, { mono = false, placeholder = '', type = 'text', optional = false, readonly = false } = {}) {
    const el = h('input', {
      type, class: INPUT + (mono ? ' font-mono' : '') + (readonly ? ' opacity-60' : ''),
      placeholder, value: obj[key] === undefined || obj[key] === null ? '' : String(obj[key]), readonly
    });
    el.addEventListener('input', () => {
      if (optional && el.value === '') delete obj[key];
      else obj[key] = el.value;
      changed();
    });
    return el;
  }

  function numberInput(obj, key, { nullable = false } = {}) {
    const el = h('input', { type: 'number', class: INPUT + ' font-mono', value: obj[key] === undefined || obj[key] === null ? '' : String(obj[key]) });
    el.addEventListener('input', () => {
      const v = el.value.trim();
      if (v === '') {
        if (nullable) obj[key] = null;
        else delete obj[key];
      } else {
        obj[key] = Number(v);
      }
      changed();
    });
    return el;
  }

  function textArea(obj, key, { rows = 3, mono = false, placeholder = '', optional = false } = {}) {
    const el = h('textarea', {
      rows, placeholder,
      class: INPUT + ' resize-y leading-relaxed' + (mono ? ' font-mono text-emerald-300' : '')
    });
    el.value = obj[key] === undefined || obj[key] === null ? '' : String(obj[key]);
    el.addEventListener('input', () => {
      if (optional && el.value === '') delete obj[key];
      else obj[key] = el.value;
      changed();
    });
    return el;
  }

  function checkbox(obj, key, label) {
    const el = h('input', { type: 'checkbox', class: 'accent-purple-500 w-4 h-4' });
    el.checked = Boolean(obj[key]);
    el.addEventListener('change', () => { obj[key] = el.checked; changed(); });
    return h('label', { class: 'flex items-center gap-2 text-xs text-slate-300 cursor-pointer' }, el, label);
  }

  function selectInput(obj, key, options, { allowEmpty = false } = {}) {
    const opts = options.map(o => (Array.isArray(o) ? o : [o, o]));
    if (obj[key] && !opts.some(([v]) => v === obj[key])) opts.push([obj[key], obj[key]]);
    const el = h('select', { class: INPUT + ' font-mono' },
      allowEmpty ? h('option', { value: '', text: '（不设置）' }) : null,
      opts.map(([v, label]) => h('option', { value: v, text: label })));
    el.value = obj[key] === undefined || obj[key] === null ? '' : obj[key];
    el.addEventListener('change', () => {
      if (allowEmpty && el.value === '') delete obj[key];
      else obj[key] = el.value;
      changed();
    });
    return el;
  }

  /** 多语言文字：{ "zh-CN": "…", "en": "…" }。原值是纯文字时只给一个框，不改变形状。 */
  function i18nInputs(obj, key, langs, { multiline = false, rows = 3 } = {}) {
    if (typeof obj[key] === 'string') {
      return multiline ? textArea(obj, key, { rows }) : textInput(obj, key);
    }
    if (!isObj(obj[key])) obj[key] = {};
    const target = obj[key];
    return h('div', { class: langs.length > 2 ? 'grid grid-cols-1 sm:grid-cols-2 gap-2' : 'space-y-2' },
      langs.map(([lang, label]) => h('div', { class: 'flex gap-2 items-start' },
        h('span', { class: 'shrink-0 w-14 pt-2 text-[10px] font-mono text-slate-500', text: label.length > 6 ? lang : label }),
        multiline ? textArea(target, lang, { rows }) : textInput(target, lang))));
  }

  /** 文字列表：一行一个 */
  function stringList(obj, key, { rows = 4, placeholder = '一行一个' } = {}) {
    const el = h('textarea', { rows, placeholder, class: INPUT + ' resize-y leading-relaxed' });
    el.value = Array.isArray(obj[key]) ? obj[key].join('\n') : '';
    el.addEventListener('input', () => {
      obj[key] = el.value.split('\n').map(s => s.trim()).filter(Boolean);
      changed();
    });
    return el;
  }

  /** 任意 JSON（如 nexusStats）；解析不了就标红，保存按钮会拦住 */
  function jsonInput(obj, key, { rows = 5, nullable = true } = {}) {
    const el = h('textarea', { rows, class: INPUT + ' font-mono resize-y' });
    const err = h('span', { class: 'hidden text-[10px] text-rose-400' });
    el.value = obj[key] === undefined ? '' : JSON.stringify(obj[key], null, 2);
    el.addEventListener('input', () => {
      const raw = el.value.trim();
      try {
        if (raw === '') {
          if (nullable) obj[key] = null;
          else delete obj[key];
        } else {
          obj[key] = JSON.parse(raw);
        }
        err.classList.add('hidden');
        el.classList.remove('border-rose-500');
        ed.jsonError = null;
      } catch (e) {
        err.textContent = `JSON 格式不对：${e.message}`;
        err.classList.remove('hidden');
        el.classList.add('border-rose-500');
        ed.jsonError = `${key}：JSON 格式不对`;
      }
      changed();
    });
    return h('div', { class: 'space-y-1' }, el, err);
  }

  /**
   * 对象列表（指令、Mod、套餐…）：每项一张可折叠卡片，可上移/下移/删除，底部「添加」。
   * render(item, index, arr) 返回卡片内容；字符串项（老数据里的纯文字常用指令）也能编辑。
   */
  function objectList(obj, key, { title, render, create, addLabel = '添加一项', empty = '还没有内容' }) {
    if (!Array.isArray(obj[key])) obj[key] = [];
    const wrap = h('div', { class: 'space-y-2' });

    function draw() {
      const arr = obj[key];
      wrap.replaceChildren();
      if (!arr.length) wrap.appendChild(h('p', { class: 'text-[11px] text-slate-500 italic', text: empty }));
      arr.forEach((item, i) => {
        const summaryText = h('span', { class: 'truncate', text: `${i + 1}. ${title(item, i) || '（未命名）'}` });
        const move = (delta, ev) => {
          ev.preventDefault();
          const j = i + delta;
          if (j < 0 || j >= arr.length) return;
          [arr[i], arr[j]] = [arr[j], arr[i]];
          changed();
          draw();
        };
        const remove = ev => {
          ev.preventDefault();
          if (!confirm(`删除「${title(item, i) || '这一项'}」？（保存前都可以关掉编辑器放弃）`)) return;
          arr.splice(i, 1);
          changed();
          draw();
        };
        const body = h('div', { class: 'p-3 space-y-3 border-t border-slate-800' }, render(item, i, arr));
        body.addEventListener('input', () => { summaryText.textContent = `${i + 1}. ${title(arr[i], i) || '（未命名）'}`; });
        const details = h('details', { class: 'rounded-lg border border-slate-800 bg-slate-950/60' },
          h('summary', { class: 'flex items-center gap-2 px-3 py-2 cursor-pointer text-xs text-slate-200 select-none' },
            summaryText,
            h('span', { class: 'ml-auto flex items-center gap-1 shrink-0' },
              h('button', { type: 'button', class: 'px-1.5 text-slate-400 hover:text-white', title: '上移', text: '↑', onclick: e => move(-1, e) }),
              h('button', { type: 'button', class: 'px-1.5 text-slate-400 hover:text-white', title: '下移', text: '↓', onclick: e => move(1, e) }),
              h('button', { type: 'button', class: 'px-1.5 text-rose-400 hover:text-rose-300', title: '删除', text: '✕', onclick: remove }))),
          body);
        if (typeof item === 'object' && item && openItems.has(item)) details.open = true;
        details.addEventListener('toggle', () => {
          if (typeof item !== 'object' || !item) return;
          if (details.open) openItems.add(item); else openItems.delete(item);
        });
        wrap.appendChild(details);
      });
      wrap.appendChild(h('button', {
        type: 'button', class: `${BTN_GHOST} border border-dashed border-slate-700`, text: `＋ ${addLabel}`,
        onclick: () => {
          const item = create();
          if (typeof item === 'object' && item) openItems.add(item);
          arr.push(item);
          changed();
          draw();
        }
      }));
    }
    draw();
    return wrap;
  }

  function newId(prefix) {
    return `${ed.doc.id || 'game'}_${prefix}_${Date.now().toString(36)}`;
  }

  // ---------------------------------------------------------------------------
  // 各个块
  // ---------------------------------------------------------------------------
  function blockBasic(doc) {
    return [
      section('基本信息', '首页卡片、列表、侧栏、搜索都用这里的字段。',
        grid(
          field('id', ed.create
            ? textInput(doc, 'id', { mono: true, placeholder: '如 hollow-knight' })
            : h('div', { class: INPUT + ' font-mono opacity-60', text: doc.id }),
          ed.create ? '小写字母、数字和连字符；建好以后不能改（收藏、订阅、链接都靠它）' : '建好以后不能改'),
          field('排名 rank', numberInput(doc, 'rank'), '1–14 是「重点整理」'),
          field('通用 / 英文标题 title', textInput(doc, 'title')),
          field('开发商 developer', textInput(doc, 'developer')),
          field('发行年份 releaseYear', numberInput(doc, 'releaseYear', { nullable: true })),
          field('类型 genre', textInput(doc, 'genre', { placeholder: '如 Open World Action RPG' })),
          field('Steam AppID', numberInput(doc, 'steamAppId', { nullable: true }), '不在 Steam 上填 0；雷达按它巡检'),
          field('Steam 评价 steamRating', textInput(doc, 'steamRating'), '如「92% Very Positive」；没有来源就留空'),
          field('热度档 heatTier', selectInput(doc, 'heatTier', HEAT_TIERS, { allowEmpty: true })),
          field('最近整理日期 lastUpdated', textInput(doc, 'lastUpdated', { type: 'date' }), '首页默认按它排序'),
          field('暗号 radarSecretCode', textInput(doc, 'radarSecretCode')),
          field('Mod 安装目录 modInstallPath', textInput(doc, 'modInstallPath', { mono: true }))
        ),
        h('div', { class: 'flex flex-wrap gap-5 pt-1' },
          checkbox(doc, 'hasConsole', '有原生 / 框架控制台（hasConsole）'),
          checkbox(doc, 'hasMods', '有 Mod 生态（hasMods）')),
        field('封面图 headerImage', textInput(doc, 'headerImage', { mono: true, placeholder: 'https://…/header.jpg' })),
        doc.headerImage ? h('img', { src: doc.headerImage, class: 'h-20 rounded-lg border border-slate-800', alt: '', loading: 'lazy' }) : null),
      section('8 语言标题 titles', '简体中文和英文必填；其它语言空着时页面显示英文标题。', i18nInputs(doc, 'titles', LANGS)),
      section('别名 aliases', '一行一个（如 老头环、法环、er）。首页搜索马上能用；AI 助手的别名表要导出快照后重新生成（scripts/build_game_aliases.py）。',
        stringList(doc, 'aliases', { rows: 4 })),
      section('N 网统计 nexusStats', '没有就清空（存成 null）。有数字就必须带取数日期 checkedAt。',
        jsonInput(doc, 'nexusStats', { rows: 6 }))
    ];
  }

  function commandFields(cmd) {
    return [
      grid(
        field('指令 id（全站唯一）', textInput(cmd, 'id', { mono: true })),
        field('语法类型 syntax_type', selectInput(cmd, 'syntax_type', SYNTAX_TYPES, { allowEmpty: true }))
      ),
      field('名称', i18nInputs(cmd, 'name', ZH_EN)),
      field('代码 code', textArea(cmd, 'code', { rows: 2, mono: true })),
      field('说明 desc', textArea(cmd, 'desc', { rows: 2 }), '写实际效果；不写「实测 / 100% 安全」这类保证'),
      grid(
        field('需要的框架 framework_required', textInput(cmd, 'framework_required', { optional: true })),
        field('出处 source（必填，https）', textInput(cmd, 'source', { mono: true, placeholder: 'https://wiki…' }))
      )
    ];
  }

  function blockConsole(doc) {
    return [
      section('控制台说明', '详情页「控制台」标签顶部的开启步骤。',
        field('呼出键 consoleShortcut', textInput(doc, 'consoleShortcut', { placeholder: '如 ~ (Cyber Engine Tweaks 快捷唤出)' })),
        field('开启步骤 consoleEnableGuide', i18nInputs(doc, 'consoleEnableGuide', ZH_EN, { multiline: true, rows: 5 }))),
      section('常用指令 popularCommands', '首页搜索的「第一条指令」和指令搜索会用到。',
        objectList(doc, 'popularCommands', {
          title: c => (typeof c === 'string' ? c : `${textOf(c.name)} · ${c.command || c.code || ''}`),
          addLabel: '添加常用指令',
          create: () => ({ name: { 'zh-CN': '', en: '' }, command: '', desc: '', source: '' }),
          render: (c, i, arr) => {
            if (typeof c === 'string') {
              const el = h('input', { class: INPUT + ' font-mono', value: c });
              el.addEventListener('input', () => { arr[i] = el.value; changed(); });
              return [field('指令（老数据里的纯文字写法）', el)];
            }
            return [
              field('名称', i18nInputs(c, 'name', ZH_EN)),
              field('指令 command', textArea(c, 'command', { rows: 2, mono: true })),
              field('说明 desc', textArea(c, 'desc', { rows: 2 })),
              field('出处 source', textInput(c, 'source', { mono: true, placeholder: 'https://…' }))
            ];
          }
        })),
      section('指令分类 consoleCategories', '每个分类至少一条指令；每条指令都要有 https 出处。',
        objectList(doc, 'consoleCategories', {
          title: cat => `${cat.category || textOf(cat.name)}（${(cat.commands || []).length} 条）`,
          addLabel: '添加指令分类',
          create: () => ({ category: '新分类', commands: [] }),
          render: cat => [
            field('分类名 category', textInput(cat, 'category')),
            objectList(cat, 'commands', {
              title: c => `${textOf(c.name) || '（未命名）'} · ${c.code || ''}`,
              addLabel: '添加指令',
              create: () => ({
                name: { 'zh-CN': '', en: '' }, code: '', desc: '', id: newId('cmd'),
                syntax_type: 'engine_console', source: ''
              }),
              render: c => commandFields(c)
            })
          ]
        })),
      section('控制台脚本 batScript', '详情页「下载 .bat」的内容。只写它真正做的事，别写「一键 / 零风险」。',
        textArea(doc, 'batScript', { rows: 14, mono: true, optional: true }))
    ];
  }

  function blockBundles(doc) {
    return [
      section('场景套餐 scenarioBundles', '套餐 id 全站唯一；code 每行一条指令。',
        objectList(doc, 'scenarioBundles', {
          title: b => b.name || b.id,
          addLabel: '添加套餐',
          create: () => ({ id: newId('bundle'), type: 'custom', name: '', tag: '', badge: '', desc: '', highlights: [], code: '' }),
          render: b => [
            grid(
              field('套餐 id', textInput(b, 'id', { mono: true })),
              field('类型 type', textInput(b, 'type', { mono: true })),
              field('名称 name', textInput(b, 'name')),
              field('标签 tag', textInput(b, 'tag')),
              field('角标 badge', textInput(b, 'badge'))
            ),
            field('说明 desc', textArea(b, 'desc', { rows: 3 })),
            field('要点 highlights（一行一条）', stringList(b, 'highlights', { rows: 5 })),
            field('指令 code（一行一条）', textArea(b, 'code', { rows: 8, mono: true }))
          ]
        }))
    ];
  }

  function blockMods(doc) {
    return [
      section('精选 Mod curatedMods', '每个 Mod 要有 id / 标题 / 作者和来源页面（nexusUrl，https）。',
        objectList(doc, 'curatedMods', {
          title: m => `${m.title || m.id || ''}${m.author ? ' · ' + m.author : ''}`,
          addLabel: '添加 Mod',
          create: () => ({
            id: '', title: '', author: '', category: '', desc: '', dependencies: [], installPath: '',
            installSteps: [], isDirect: false, nexusUrl: ''
          }),
          render: m => [
            grid(
              field('id', textInput(m, 'id', { mono: true })),
              field('标题 title', textInput(m, 'title')),
              field('作者 author', textInput(m, 'author')),
              field('分类 category', textInput(m, 'category')),
              field('版本 version', textInput(m, 'version', { optional: true })),
              field('核对日期 checkedAt', textInput(m, 'checkedAt', { optional: true, placeholder: 'YYYY-MM-DD' })),
              field('下载量 downloads', textInput(m, 'downloads', { optional: true })),
              field('点赞 endorsements', textInput(m, 'endorsements', { optional: true }))
            ),
            field('说明 desc', textArea(m, 'desc', { rows: 3 })),
            field('来源页面 nexusUrl', textInput(m, 'nexusUrl', { mono: true })),
            grid(
              field('直链 downloadUrl（作者 GitHub 等，可选）', textInput(m, 'downloadUrl', { mono: true, optional: true })),
              field('直链文件名 downloadFilename', textInput(m, 'downloadFilename', { mono: true, optional: true }))
            ),
            field('安装目录 installPath', textInput(m, 'installPath', { mono: true })),
            field('安装步骤 installSteps（一行一步）', stringList(m, 'installSteps', { rows: 4 })),
            field('前置 dependencies（一行一个）', stringList(m, 'dependencies', { rows: 2 })),
            checkbox(m, 'isDirect', '站内直接下载（isDirect）')
          ]
        })),
      section('必装 Mod mustHaveMods', '详情页侧栏的「必装」清单。',
        objectList(doc, 'mustHaveMods', {
          title: m => m.name,
          addLabel: '添加必装 Mod',
          create: () => ({ name: '', category: '', desc: '', url: '' }),
          render: m => [
            grid(field('名称 name', textInput(m, 'name')), field('分类 category', textInput(m, 'category'))),
            field('说明 desc', textInput(m, 'desc')),
            field('链接 url', textInput(m, 'url', { mono: true, optional: true }))
          ]
        }))
    ];
  }

  function readonlyRows(rows) {
    return h('dl', { class: 'grid grid-cols-[8rem_1fr] gap-x-3 gap-y-1.5 text-xs' },
      rows.filter(Boolean).map(([k, v]) => [
        h('dt', { class: 'text-slate-500', text: k }),
        h('dd', { class: 'text-slate-200 break-all' }, v === null || v === undefined || v === '' ? '—' : v)
      ]));
  }

  function link(url) {
    return url ? h('a', { href: url, target: '_blank', rel: 'noopener noreferrer', class: 'text-purple-300 hover:underline', text: url }) : '—';
  }

  function blockTrainer() {
    const m = ed.machine || {};
    const t = m.trainer;
    const info = (t && t.trainerInfo) || {};
    return [
      section('修改器（只读）', '这三个字段（hasTrainer / trainerHotkeys / trainerInfo）由每天的风灵月影同步任务维护（scripts/fling_trainer_sync.py → public/trainers.json），网站按 trainers.json 显示。在这里改了也会被忽略。匹配错了改脚本里的 MANUAL_SLUGS。',
        t ? readonlyRows([
          ['有没有修改器', t.hasTrainer ? '有' : '没有'],
          ['官方页面', link(info.officialUrl)],
          ['支持版本', info.version],
          ['功能数', info.optionsCount],
          ['最后更新', info.lastUpdated],
          ['平台', Array.isArray(info.platforms) ? info.platforms.join(' / ') : null],
          ['带反作弊', info.antiCheat ? '是（网站会显示警告）' : '否'],
          ['热键条数', Array.isArray(t.trainerHotkeys) ? t.trainerHotkeys.length : 0],
          ['清单时间', m.trainers_generated_at]
        ]) : h('p', { class: 'text-xs text-slate-500', text: 'trainers.json 读不到，网站暂时显示库里的值。' }))
    ];
  }

  function blockRadar() {
    const m = ed.machine || {};
    const r = m.radar;
    return [
      section('雷达（只读）', '雷达字段由每天的巡检任务维护（scripts/steam_patch_monitor.py → public/radar_status.json），网站按 radar_status.json 显示。在这里改了也会被忽略。',
        r ? readonlyRows([
          ['状态', (RADAR_PILLS[r.status] || ['⚪ 未巡检'])[0]],
          ['原因', r.reason_text],
          ['说明', r.summary],
          ['Steam build', r.steam_build_id],
          ['Steam 更新时间', r.steam_build_updated_at],
          ['上次巡检', r.last_checked_at],
          ['框架', r.framework ? r.framework.name : null],
          ['最新公告', r.latest_announcement ? link(r.latest_announcement.url) : null],
          ['雷达数据时间', m.radar_updated_at]
        ]) : h('p', { class: 'text-xs text-slate-500', text: '这款游戏还没有雷达巡检记录（新加的游戏要等导出快照、定时任务跑过之后才有）。' }))
    ];
  }

  function blockPitfall(doc) {
    if (!isObj(doc.pitfallNote)) {
      return [section('避坑笔记 pitfallNote', '详情页「控制台」标签里的避坑贴士。这款游戏还没有。',
        h('button', {
          type: 'button', class: BTN_GHOST, text: '＋ 添加避坑笔记',
          onclick: () => {
            doc.pitfallNote = { title: `老L避坑笔记 (${(doc.titles && doc.titles['zh-CN']) || doc.title || ''})`, tips: [] };
            changed();
            renderBody();
          }
        }))];
    }
    return [section('避坑笔记 pitfallNote', '一行一条贴士；写清楚出处能查到的事实，不写保证。',
      field('标题 title', textInput(doc.pitfallNote, 'title')),
      field('贴士 tips（一行一条）', stringList(doc.pitfallNote, 'tips', { rows: 8 })),
      h('button', {
        type: 'button', class: BTN_DANGER, text: '删除整份避坑笔记',
        onclick: () => {
          if (!confirm('删除这款游戏的避坑笔记？')) return;
          doc.pitfallNote = null;
          changed();
          renderBody();
        }
      }))];
  }

  function blockJson() {
    const area = h('textarea', { rows: 28, class: INPUT + ' font-mono text-[11px] leading-relaxed resize-y' });
    area.value = JSON.stringify(ed.doc, null, 2);
    const err = h('p', { class: 'hidden text-xs text-rose-400' });
    return [section('整份 JSON', '能改任何字段（包括表单里没有的）。改完点「应用到编辑器」，再保存。雷达 / 修改器字段保存时会被忽略。',
      area, err,
      h('div', { class: 'flex gap-2' },
        h('button', {
          type: 'button', class: BTN_PRIMARY, text: '应用到编辑器',
          onclick: () => {
            let parsed;
            try {
              parsed = JSON.parse(area.value);
            } catch (e) {
              err.textContent = `JSON 格式不对：${e.message}`;
              err.classList.remove('hidden');
              return;
            }
            if (!isObj(parsed)) {
              err.textContent = '必须是一个 JSON 对象';
              err.classList.remove('hidden');
              return;
            }
            if (!ed.create && parsed.id !== ed.id) {
              err.textContent = `id 不能改（应为 ${ed.id}）`;
              err.classList.remove('hidden');
              return;
            }
            err.classList.add('hidden');
            ed.doc = parsed;
            ed.jsonError = null;
            setNotice('已应用 JSON（尚未保存）', 'info');
            changed();
            render();
          }
        }),
        h('button', {
          type: 'button', class: BTN_GHOST, text: '重新从编辑器生成',
          onclick: () => { area.value = JSON.stringify(ed.doc, null, 2); err.classList.add('hidden'); }
        })))];
  }

  // ---------------------------------------------------------------------------
  // 编辑器外壳
  // ---------------------------------------------------------------------------
  function modal() {
    let el = document.getElementById('game-editor-modal');
    if (!el) {
      el = h('div', { id: 'game-editor-modal', class: 'fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-xl p-2 sm:p-6' });
      document.body.appendChild(el);
    }
    return el;
  }

  const isDirty = () => Boolean(ed.doc) && JSON.stringify(ed.doc) !== ed.baseline;

  let headerTimer = null;
  function scheduleHeader() {
    clearTimeout(headerTimer);
    headerTimer = setTimeout(renderHeader, 250);
  }

  function setNotice(text, type = 'info') {
    ed.notice = text ? { text, type } : null;
  }

  function renderHeader() {
    const box = document.getElementById('ge-header');
    if (!box || !ed.doc) return;
    const doc = ed.doc;
    const title = (doc.titles && doc.titles['zh-CN']) || doc.title || doc.id || '新游戏';
    const dirty = isDirty();
    box.replaceChildren(
      h('div', { class: 'min-w-0' },
        h('h3', { class: 'text-base font-bold text-white truncate', text: ed.create ? `新增游戏：${title}` : `编辑：${title}` }),
        h('p', { class: 'text-[11px] font-mono text-slate-400 flex flex-wrap gap-x-3' },
          h('span', { text: `id ${doc.id || '（未填）'}` }),
          ed.create ? null : h('span', { text: `版本 rev ${ed.rev}` }),
          ed.updatedAt ? h('span', { text: `上次保存 ${ed.updatedAt}` }) : null,
          ed.hidden ? h('span', { class: 'text-amber-400', text: '已隐藏（网站上看不到）' }) : null,
          dirty ? h('span', { class: 'text-purple-300', text: '● 有未保存的修改' }) : h('span', { class: 'text-slate-500', text: '没有未保存的修改' }))),
      h('div', { class: 'flex flex-wrap items-center gap-2 shrink-0' },
        ed.create ? null : h('a', {
          href: `/#/game/${encodeURIComponent(ed.id)}`, target: '_blank', rel: 'noopener',
          class: BTN_GHOST, text: '前台预览 ↗'
        }),
        ed.create ? null : h('button', { type: 'button', class: BTN_GHOST, text: '历史版本', onclick: toggleHistory }),
        h('button', { type: 'button', class: BTN_GHOST, text: '检查', disabled: ed.busy, onclick: () => save(true) }),
        h('button', { type: 'button', class: BTN_PRIMARY, text: ed.busy ? '处理中…' : (ed.create ? '新建并发布' : '保存（直接生效）'), disabled: ed.busy || (!dirty && !ed.create), onclick: () => save(false) }),
        h('button', { type: 'button', class: `${BTN} text-slate-400 hover:text-white`, text: '关闭', onclick: close })));
  }

  function renderMessages() {
    const box = document.getElementById('ge-messages');
    if (!box) return;
    const parts = [];
    if (ed.notice) {
      const cls = ed.notice.type === 'error' ? 'border-rose-500/40 bg-rose-950/40 text-rose-200'
        : ed.notice.type === 'success' ? 'border-emerald-500/40 bg-emerald-950/40 text-emerald-200'
          : 'border-purple-500/40 bg-purple-950/40 text-purple-200';
      parts.push(h('div', { class: `rounded-lg border px-3 py-2 text-xs ${cls}`, text: ed.notice.text }));
    }
    if (ed.errors.length) {
      parts.push(h('div', { class: 'rounded-lg border border-rose-500/40 bg-rose-950/30 px-3 py-2 text-xs text-rose-200 space-y-1' },
        h('p', { class: 'font-bold', text: `有 ${ed.errors.length} 处问题，改完才能保存：` }),
        h('ul', { class: 'list-disc pl-5 space-y-0.5' }, ed.errors.map(e => h('li', { text: e })))));
    }
    if (ed.warnings.length) {
      parts.push(h('details', { class: 'rounded-lg border border-amber-500/30 bg-amber-950/20 px-3 py-2 text-xs text-amber-200', open: ed.warnings.length <= 5 },
        h('summary', { class: 'cursor-pointer font-bold', text: `${ed.warnings.length} 条提醒（不影响保存）` }),
        h('ul', { class: 'list-disc pl-5 space-y-0.5 mt-1' }, ed.warnings.map(w => h('li', { text: w })))));
    }
    if (ed.history) parts.push(renderHistory());
    box.replaceChildren(...parts);
  }

  function renderHistory() {
    const list = ed.history;
    return h('div', { class: 'rounded-lg border border-slate-700 bg-slate-950/80 px-3 py-2 text-xs space-y-2' },
      h('div', { class: 'flex items-center justify-between' },
        h('p', { class: 'font-bold text-slate-200', text: '历史版本（每次保存前的整份数据）' }),
        h('button', { type: 'button', class: 'text-slate-400 hover:text-white', text: '收起', onclick: () => { ed.history = null; renderMessages(); } })),
      list === 'loading' ? h('p', { class: 'text-slate-500', text: '读取中…' })
        : !list.length ? h('p', { class: 'text-slate-500', text: '还没有历史版本（第一次保存后才有）。' })
          : h('ul', { class: 'divide-y divide-slate-800 max-h-56 overflow-y-auto' }, list.map(r => h('li', { class: 'flex items-center gap-3 py-1.5 font-mono' },
            h('span', { class: 'text-slate-300', text: `rev ${r.rev}` }),
            h('span', { class: 'text-slate-500', text: r.created_at }),
            h('span', { class: 'text-slate-500', text: r.admin_user || '' }),
            h('span', { class: 'text-slate-600', text: `${Math.round((r.bytes || 0) / 1024)} KB` }),
            h('button', { type: 'button', class: `${BTN_GHOST} ml-auto`, text: '载入到编辑器', onclick: () => loadRevision(r) })))));
  }

  async function toggleHistory() {
    if (ed.history) {
      ed.history = null;
      renderMessages();
      return;
    }
    ed.history = 'loading';
    renderMessages();
    try {
      const res = await api().apiFetch(`/games/${encodeURIComponent(ed.id)}/revisions`);
      ed.history = res.code === 0 ? res.data.revisions : [];
    } catch (e) {
      ed.history = [];
      api().showToast(e.message, 'error');
    }
    renderMessages();
  }

  async function loadRevision(r) {
    if (isDirty() && !confirm('载入历史版本会替换编辑器里未保存的修改，继续？')) return;
    try {
      const res = await api().apiFetch(`/games/${encodeURIComponent(ed.id)}/revisions?revision_id=${r.id}`);
      if (res.code !== 0) throw new Error(res.message || '读取失败');
      ed.doc = res.data.doc;
      ed.history = null;
      ed.errors = [];
      ed.warnings = [];
      setNotice(`已载入 rev ${r.rev}（${r.created_at}）的内容，尚未保存。点「保存」后它会成为新的版本。`, 'info');
      render();
    } catch (e) {
      api().showToast(e.message, 'error');
    }
  }

  function renderTabs() {
    const box = document.getElementById('ge-tabs');
    if (!box) return;
    box.replaceChildren(...BLOCKS.map(([key, label]) => h('button', {
      type: 'button',
      class: `px-3 py-1.5 rounded-lg text-xs whitespace-nowrap transition ${ed.block === key
        ? 'bg-purple-500/15 text-purple-300 border border-purple-500/30' : 'text-slate-400 hover:text-white hover:bg-slate-800/60 border border-transparent'}`,
      text: label,
      onclick: () => { ed.block = key; renderTabs(); renderBody(); }
    })));
  }

  function renderBody() {
    const box = document.getElementById('ge-body');
    if (!box || !ed.doc) return;
    const doc = ed.doc;
    const blocks = {
      basic: () => blockBasic(doc), console: () => blockConsole(doc), bundles: () => blockBundles(doc),
      mods: () => blockMods(doc), trainer: blockTrainer, pitfall: () => blockPitfall(doc), radar: blockRadar, json: blockJson
    };
    box.replaceChildren(...(blocks[ed.block] || blocks.basic)());
    box.scrollTop = 0;
  }

  function render() {
    const el = modal();
    el.replaceChildren(h('div', { class: 'mx-auto h-full max-w-5xl flex flex-col rounded-2xl border border-slate-800 bg-[#0d0f15] shadow-2xl overflow-hidden' },
      h('div', { id: 'ge-header', class: 'flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 px-4 sm:px-5 py-3' }),
      h('div', { id: 'ge-messages', class: 'px-4 sm:px-5 pt-3 space-y-2 empty:hidden empty:p-0' }),
      h('nav', { id: 'ge-tabs', class: 'flex gap-1 overflow-x-auto px-4 sm:px-5 py-3 border-b border-slate-800/70' }),
      h('div', { id: 'ge-body', class: 'flex-1 overflow-y-auto px-4 sm:px-5 py-4 space-y-4' })));
    el.classList.remove('hidden');
    renderHeader();
    renderMessages();
    renderTabs();
    renderBody();
  }

  function close() {
    if (isDirty() && !confirm('有未保存的修改，确定关闭？')) return;
    modal().classList.add('hidden');
    ed.doc = null;
  }

  async function openGame(id, { keepBlock = false, notice = null, warnings = [] } = {}) {
    try {
      const res = await api().apiFetch(`/games/${encodeURIComponent(id)}`);
      if (res.code !== 0 || !res.data || !isObj(res.data.doc)) throw new Error(res.message || '读取失败');
      const d = res.data;
      Object.assign(ed, {
        create: false, id: d.id, rev: d.rev, hidden: d.is_hidden, updatedAt: d.updated_at,
        doc: d.doc, baseline: JSON.stringify(d.doc), machine: d.machine,
        block: keepBlock ? ed.block : 'basic', errors: [], warnings, jsonError: null, busy: false, history: null
      });
      setNotice(notice ? notice.text : null, notice ? notice.type : 'info');
      render();
    } catch (e) {
      api().showToast(`无法读取游戏：${e.message}`, 'error');
    }
  }

  function openCreate() {
    const maxRank = listCache.reduce((m, g) => Math.max(m, g.rank || 0), 0);
    const doc = {
      id: '', rank: maxRank + 1, title: '',
      titles: Object.fromEntries(LANGS.map(([l]) => [l, ''])),
      aliases: [], developer: '', releaseYear: new Date().getFullYear(), genre: '', steamRating: '',
      hasConsole: false, consoleShortcut: '', consoleEnableGuide: { 'zh-CN': '', en: '' }, popularCommands: [],
      hasMods: false, modInstallPath: '', mustHaveMods: [], consoleCategories: [], curatedMods: [],
      communityReviews: [], steamAppId: 0, headerImage: '', radarSecretCode: '', lastUpdated: today(),
      heatTier: 'emerald', scenarioBundles: [], pitfallNote: null
    };
    Object.assign(ed, {
      create: true, id: null, rev: null, hidden: false, updatedAt: null, doc, baseline: JSON.stringify(doc),
      machine: null, block: 'basic', errors: [], warnings: [], jsonError: null, busy: false, history: null
    });
    setNotice('填好 id、标题（简体中文 + 英文）后点「新建并发布」；修改器和雷达由定时任务补上（要先导出快照，见 docs/DATABASE_GUIDE.md）。', 'info');
    render();
  }

  async function save(dryRun) {
    if (ed.busy || !ed.doc) return;
    if (ed.jsonError) {
      ed.errors = [ed.jsonError];
      renderMessages();
      return;
    }
    ed.busy = true;
    renderHeader();
    const payload = ed.create
      ? { doc: ed.doc, create: true, dry_run: dryRun }
      : { doc: ed.doc, base_rev: ed.rev, dry_run: dryRun };
    try {
      const res = await api().apiFetch('/games/save', { method: 'POST', body: JSON.stringify(payload) });
      const data = res.data || {};
      ed.errors = data.errors || [];
      ed.warnings = data.warnings || [];
      if (res.code === 0 && dryRun) {
        setNotice(`检查通过（没有保存）。会改动的字段：${(data.changed_fields || []).join('、') || '无'}`, 'success');
      } else if (res.code === 0) {
        api().showToast(res.message || '已保存', 'success');
        const id = ed.doc.id;
        ed.busy = false;
        loadList();
        await openGame(id, {
          keepBlock: true,
          notice: { text: `${res.message}（改了：${(data.changed_fields || []).join('、') || '无'}）`, type: 'success' },
          warnings: data.warnings || []
        });
        return;
      } else if (res.code === 40901) {
        setNotice(`${res.message}。你的修改还在编辑器里：可以先到「整份 JSON」复制出来，再重新打开这款游戏。`, 'error');
      } else {
        setNotice(res.message || '保存失败', 'error');
      }
    } catch (e) {
      setNotice(e.message, 'error');
    }
    ed.busy = false;
    renderHeader();
    renderMessages();
  }

  // ---------------------------------------------------------------------------
  // 列表
  // ---------------------------------------------------------------------------
  async function loadList() {
    const tbody = document.getElementById('cms-games-tbody');
    if (!tbody || !api()) return;
    const q = (document.getElementById('cms-search-input') || {}).value || '';
    const status = (document.getElementById('cms-status-filter') || {}).value || 'all';
    const visibility = (document.getElementById('cms-visibility-filter') || {}).value || 'all';
    const res = await api().apiFetch(`/games?q=${encodeURIComponent(q.trim())}&status=${status}&visibility=${visibility}`);
    const stats = document.getElementById('cms-games-stats');
    if (res.code !== 0 || !res.data) {
      tbody.replaceChildren(h('tr', null, h('td', { colspan: 7, class: 'py-8 text-center text-slate-500 font-mono', text: res.message || '读取失败' })));
      return;
    }
    const s = res.data.status_stats || {};
    if (stats) stats.textContent = `共 ${s.total || 0} 款 · 已隐藏 ${s.hidden || 0} 款 · 当前列出 ${res.data.games.length} 款`;
    if (!q && status === 'all' && visibility === 'all') listCache = res.data.games;
    if (!res.data.games.length) {
      tbody.replaceChildren(h('tr', null, h('td', { colspan: 7, class: 'py-8 text-center text-slate-500 font-mono', text: '没有匹配的游戏' })));
      return;
    }
    tbody.replaceChildren(...res.data.games.map(g => {
      const pill = RADAR_PILLS[g.compatibility_status] || ['⚪ 未巡检', 'bg-slate-500/10 text-slate-400 border-slate-500/20'];
      return h('tr', { class: `hover:bg-slate-800/40 transition ${g.is_hidden ? 'opacity-60' : ''}` },
        h('td', { class: 'py-3 px-4 font-mono text-purple-400 font-bold', text: `#${g.rank}` }),
        h('td', { class: 'py-3 px-4' },
          h('div', { class: 'font-bold text-white text-xs', text: g.title_zh || g.title }),
          h('div', { class: 'text-[10px] text-slate-500 font-mono', text: `${g.title} (${g.id})` })),
        h('td', { class: 'py-3 px-4' }, h('span', { class: `px-2 py-0.5 rounded-full text-[11px] border font-mono ${pill[1]}`, text: pill[0] })),
        h('td', { class: 'py-3 px-4 text-center font-mono text-slate-300', text: `${g.command_count} / ${g.bundle_count}` }),
        h('td', { class: 'py-3 px-4 font-mono text-[11px] text-slate-400' },
          h('div', { text: `rev ${g.content_rev}` }), h('div', { class: 'text-slate-600', text: g.updated_at || '' })),
        h('td', { class: 'py-3 px-4' }, g.is_hidden
          ? h('span', { class: 'px-2 py-0.5 rounded-full text-[11px] border bg-amber-500/10 text-amber-400 border-amber-500/20', text: '已隐藏' })
          : h('span', { class: 'px-2 py-0.5 rounded-full text-[11px] border bg-emerald-500/10 text-emerald-400 border-emerald-500/20', text: '公开' })),
        h('td', { class: 'py-3 px-4 text-right whitespace-nowrap space-x-1' },
          h('button', { type: 'button', class: `${BTN} bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30`, text: '编辑', onclick: () => openGame(g.id) }),
          h('button', {
            type: 'button', class: g.is_hidden ? BTN_GHOST : BTN_DANGER, text: g.is_hidden ? '恢复显示' : '隐藏',
            onclick: () => setHidden(g, !g.is_hidden)
          })));
    }));
  }

  async function setHidden(g, hidden) {
    const name = g.title_zh || g.title;
    const ask = hidden
      ? `隐藏「${name}」？\n\n网站、接口和快照里都不再显示它；玩家的收藏和订阅都会保留，随时可以恢复。（游戏不能删除，删除会连带删掉玩家数据。）`
      : `恢复显示「${name}」？`;
    if (!confirm(ask)) return;
    try {
      const res = await api().apiFetch('/games/visibility', { method: 'POST', body: JSON.stringify({ id: g.id, hidden }) });
      api().showToast(res.message || (res.code === 0 ? '已更新' : '操作失败'), res.code === 0 ? 'success' : 'error');
      loadList();
    } catch (e) {
      api().showToast(e.message, 'error');
    }
  }

  window.addEventListener('beforeunload', e => {
    if (ed.doc && isDirty()) {
      e.preventDefault();
      e.returnValue = '';
    }
  });

  window.LmodGameEditor = { loadList, openGame, openCreate };
})();
