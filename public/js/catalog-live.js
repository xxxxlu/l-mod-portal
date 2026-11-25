/**
 * L-MOD Vault —— 游戏数据实时刷新（数据真源是 Cloudflare D1，后台改了直接生效）
 * ==============================================================================
 * 页面照旧先用 data.js 里的 GAMES_DATA 快照渲染（不等网络、不闪），然后：
 *   - refresh(games)        向 /api/v1/catalog 要最新目录（轻字段），合进 games；有变化才返回 true，页面再重画
 *   - loadGame(games, id)   进详情时向 /api/v1/catalog/:id 要这款游戏的整份数据，合进去；有变化才返回 true
 * games 原地修改（就是 window.GAMES_DATA 那个数组），ai_copilot.js 等读 window.GAMES_DATA 的地方自动拿到新数据。
 *
 * 接口拿不到（GitHub Pages 跨域失败、断网、8 秒超时、接口还没上线）就什么都不改，页面一直用快照。
 *
 * 机器维护的字段（雷达 / 修改器）不从接口覆盖快照里已有的游戏：快照 data.js 和 radar_status.json /
 * trainers.json 是同一次部署发出去的，Cloudflare 上两边一样新；GitHub Pages 的 data.js 每天由定时任务更新，
 * 比 Cloudflare 上的还新。只有快照里没有的新游戏才用接口给的雷达/修改器字段。
 * 字段清单和 functions/api/v1/catalog/_game_doc.js 的 MACHINE_FIELDS 一致，两边一起改。
 */
(function () {
  'use strict';

  var PROD_API = 'https://lmod-vault.pages.dev';
  var TIMEOUT_MS = 8000;
  var DETAIL_TTL_MS = 60 * 1000;

  var MACHINE_FIELDS = [
    'compatibilityStatus', 'radarReason', 'radarStatusText', 'latestSteamPatch', 'latestSteamPatchUrl',
    'steamBuildId', 'steamBuildUpdatedAt', 'steamLastChecked', 'radarFramework', 'radarAdvice',
    'radarSummary', 'radarRiskTitle', 'radarRiskDesc', 'emergencyAlert',
    'hasTrainer', 'trainerHotkeys', 'trainerInfo'
  ];
  // 接口从不返回的旧字段（见 functions/api/_radar_status.js），快照里有也别当成「被删了」
  var NEVER_FROM_API = ['verifiedPatch'];
  // 目录接口附带的统计，不是游戏数据，不算变化
  var LIST_SUMMARY = ['commandCount', 'modCount'];

  var state = { listOk: null, loadedAt: {} };

  function inList(list, key) {
    return list.indexOf(key) !== -1;
  }

  function isInternal(key) {
    return key.charAt(0) === '_';
  }

  function same(a, b) {
    return JSON.stringify(a) === JSON.stringify(b);
  }

  /** 接口地址：GitHub Pages / 本地文件去调 Cloudflare 主站；其它（Cloudflare Pages、自定义域名、wrangler pages dev）同源 */
  function apiBase() {
    try {
      var override = window.localStorage.getItem('lmod_api_base'); // 调试用：模拟 GitHub Pages 或接口挂掉
      if (override !== null) return override.replace(/\/$/, '');
    } catch (e) {}
    var host = window.location.hostname || '';
    if (window.location.protocol === 'file:' || /\.github\.io$/i.test(host)) return PROD_API;
    return '';
  }

  function getJson(path) {
    var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, TIMEOUT_MS) : null;
    return fetch(apiBase() + path, {
      signal: ctrl ? ctrl.signal : undefined,
      credentials: 'omit',
      headers: { 'Accept': 'application/json' }
    }).then(function (res) {
      var type = res.headers.get('Content-Type') || '';
      // 接口没上线时 SPA 兜底会回 index.html（200），所以要看类型
      if (!res.ok || type.indexOf('application/json') === -1) return null;
      return res.json().then(function (body) {
        return body && body.code === 0 ? body.data : null;
      });
    }).catch(function () {
      return null;
    }).then(function (data) {
      if (timer) clearTimeout(timer);
      return data;
    });
  }

  /** 把目录合进 games（原地）：改内容字段、补新游戏、去掉已隐藏的。返回是否有变化。 */
  function applyList(games, data) {
    var omitted = data.omitted_fields || [];
    var current = {};
    games.forEach(function (g) { current[g.id] = g; });
    var next = [];
    var seen = {};
    var changed = false;

    data.games.forEach(function (item) {
      seen[item.id] = true;
      var cur = current[item.id];
      if (!cur) {
        // 快照里没有的新游戏：先只有轻字段，进详情时再取整份
        var fresh = { _partial: true };
        Object.keys(item).forEach(function (k) { fresh[k] = item[k]; });
        next.push(fresh);
        changed = true;
        return;
      }
      var fromSnapshot = !cur._partial;
      Object.keys(item).forEach(function (k) {
        if (fromSnapshot && inList(MACHINE_FIELDS, k)) return;
        if (same(cur[k], item[k])) return;
        cur[k] = item[k];
        if (!inList(LIST_SUMMARY, k)) changed = true;
      });
      // 接口里没有、也不属于「列表不带的重字段」的内容字段 = 后台删掉了
      Object.keys(cur).forEach(function (k) {
        if (k in item || isInternal(k) || inList(omitted, k) || inList(MACHINE_FIELDS, k) ||
            inList(NEVER_FROM_API, k) || inList(LIST_SUMMARY, k)) return;
        delete cur[k];
        changed = true;
      });
      next.push(cur);
    });

    // 后台隐藏的游戏：从页面去掉（快照里的顺序保留，新游戏排在后面；页面本来就按自己的规则排序）
    var kept = games.filter(function (g) { return seen[g.id]; });
    if (kept.length !== games.length) changed = true;
    var ordered = kept.concat(next.filter(function (g) { return !current[g.id]; }));
    games.splice.apply(games, [0, games.length].concat(ordered));
    return changed;
  }

  /** 把一款游戏的整份数据合进 games（原地）。返回是否有变化。 */
  function applyGame(games, full) {
    var cur = null;
    for (var i = 0; i < games.length; i++) {
      if (games[i].id === full.id) { cur = games[i]; break; }
    }
    if (!cur) return false;
    var fromSnapshot = !cur._partial;
    var changed = false;
    Object.keys(full).forEach(function (k) {
      if (fromSnapshot && inList(MACHINE_FIELDS, k)) return;
      if (same(cur[k], full[k])) return;
      cur[k] = full[k];
      changed = true;
    });
    Object.keys(cur).forEach(function (k) {
      if (k in full || isInternal(k) || inList(MACHINE_FIELDS, k) || inList(NEVER_FROM_API, k) ||
          inList(LIST_SUMMARY, k)) return;
      delete cur[k];
      changed = true;
    });
    if (cur._partial) {
      delete cur._partial;
      changed = true;
    }
    return changed;
  }

  window.LmodCatalog = {
    apiBase: apiBase,

    /** 目录接口是否可用：null = 还没问过，true / false */
    available: function () {
      return state.listOk;
    },

    refresh: function (games) {
      return getJson('/api/v1/catalog').then(function (data) {
        if (!data || !Array.isArray(data.games)) {
          state.listOk = false;
          return false;
        }
        state.listOk = true;
        return applyList(games, data);
      });
    },

    loadGame: function (games, id) {
      if (state.listOk === false || !id) return Promise.resolve(false);
      var last = state.loadedAt[id];
      if (last && Date.now() - last < DETAIL_TTL_MS) return Promise.resolve(false);
      return getJson('/api/v1/catalog/' + encodeURIComponent(id)).then(function (data) {
        if (!data || !data.game) return false;
        state.loadedAt[id] = Date.now();
        return applyGame(games, data.game);
      });
    },

    // 给测试用
    _applyList: applyList,
    _applyGame: applyGame
  };
})();
