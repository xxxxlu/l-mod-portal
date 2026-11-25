/**
 * L-MOD Vault - Client-Side API & Telemetry SDK (v2.1)
 * Modern asynchronous client with offline fallback & non-blocking telemetry.
 *
 * Telemetry privacy (v2.1):
 *   - No IP is sent or stored. Visitors are counted by a random per-browser id (localStorage `lmod_sid`).
 *   - Each event carries: page path (no query string), the external referrer's host only, a coarse
 *     device type (mobile / tablet / desktop), and the site language. Nothing else about the visitor.
 *   - `ai_ask` carries only the game id, never the question.
 *   - The GitHub Pages copy reports to https://lmod-vault.pages.dev (the only copy with an API).
 *
 * Public API (window.LModTracker):
 *   track(eventType, gameId, payload)   any event, e.g. track('trainer_download', gameId, version)
 *   trackPageView(gameId)               page_view for the current page (gameId on a game detail view)
 *   trackSearch(query)                  debounced; only the final query (<= 100 chars) is sent
 *   Links to flingtrainer.com / nexusmods.com are tracked automatically (trainer_official_click /
 *   mod_download_click), and so is any element with data-lmod-track="<event>" [data-lmod-game] [data-lmod-payload].
 */

(function (window) {
  'use strict';

  // 1. Unified Telemetry Engine (anonymous, batched, de-duplicated)
  var TELEMETRY_PATH = '/api/v1/telemetry/events';
  var CF_ORIGIN = 'https://lmod-vault.pages.dev';
  var OWN_HOSTS = ['lmod-vault.pages.dev', 'xxxxlu.github.io'];
  var UI_LANGS = ['zh-CN', 'zh-TW', 'en', 'ja', 'ko', 'ru', 'de', 'es'];
  var DEDUPE_MS = 2000;      // same event fired twice within 2s (e.g. double routing) counts once
  var FLUSH_MS = 2000;       // batch events for 2s so one visit costs ~1 request
  var SEARCH_IDLE_MS = 1200; // a search is "final" after 1.2s without typing
  var RATE_TTL_MS = 6 * 60 * 60 * 1000;

  function lsGet(key) { try { return window.localStorage.getItem(key); } catch (e) { return null; } }
  function lsSet(key, val) { try { window.localStorage.setItem(key, val); } catch (e) {} }

  function telemetryEndpoint() {
    if (window.LMOD_TELEMETRY_ENDPOINT) return window.LMOD_TELEMETRY_ENDPOINT;
    if (location.protocol !== 'http:' && location.protocol !== 'https:') return null; // file:// previews
    if (/\.github\.io$/i.test(location.hostname)) return CF_ORIGIN + TELEMETRY_PATH;
    return TELEMETRY_PATH;
  }

  function isOwnHost(hostname) {
    hostname = String(hostname || '').toLowerCase();
    if (hostname === location.hostname.toLowerCase()) return true;
    for (var i = 0; i < OWN_HOSTS.length; i++) {
      if (hostname === OWN_HOSTS[i] || hostname.slice(-(OWN_HOSTS[i].length + 1)) === '.' + OWN_HOSTS[i]) return true;
    }
    return false;
  }

  function deviceType() {
    var ua = navigator.userAgent || '';
    var iPadOS = /Macintosh/.test(ua) && navigator.maxTouchPoints > 1;
    if (iPadOS || /iPad|Tablet|PlayBook|Silk|Kindle/i.test(ua) || (/Android/i.test(ua) && !/Mobile/i.test(ua))) return 'tablet';
    if (/Mobi|iPhone|iPod|Android|Windows Phone|HarmonyOS/i.test(ua)) return 'mobile';
    return 'desktop';
  }

  function uiLang() {
    var saved = lsGet('lmod_lang');
    return UI_LANGS.indexOf(saved) >= 0 ? saved : 'zh-CN'; // pages fall back to zh-CN when nothing is saved
  }

  function currentGameId() {
    var m = (location.hash || '').match(/^#\/game\/([A-Za-z0-9-]{1,64})/) || (location.hash || '').match(/^#game-([A-Za-z0-9-]{1,64})/);
    return m ? m[1] : null;
  }

  function pagePath() {
    var path = location.pathname || '/';
    path = path.replace(/^\/l-mod-portal(?=\/|$)/, '') || '/';           // GitHub Pages project prefix
    path = path.replace(/\/index(\.html)?$/, '/').replace(/\.html$/, '');  // '/radar.html' -> '/radar'
    var gid = currentGameId();
    if (gid) path += '#/game/' + gid;
    return path.slice(0, 160);
  }

  function referrerHost() {
    try {
      if (!document.referrer) return null;
      var host = new URL(document.referrer).hostname.toLowerCase();
      return isOwnHost(host) ? null : host.slice(0, 100);
    } catch (e) { return null; }
  }

  // Sampling is per visitor (same hash on the server), so a sampled-out visitor sends nothing at all.
  function fnv1a(str) {
    var h = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = Math.imul(h, 0x01000193) >>> 0;
    }
    return h >>> 0;
  }
  function cachedSampleRate() {
    try {
      var o = JSON.parse(lsGet('lmod_tsr') || 'null');
      if (o && typeof o.r === 'number' && Date.now() - o.t < RATE_TTL_MS) return o.r;
    } catch (e) {}
    return 1;
  }

  var queue = [];
  var flushTimer = null;
  var lastSent = {};
  var pendingSearch = null;
  var searchTimer = null;
  var lastSearch = '';

  function flush(unloading) {
    if (flushTimer) { clearTimeout(flushTimer); flushTimer = null; }
    if (unloading) commitPendingSearch();
    if (!queue.length) return;
    var url = telemetryEndpoint();
    var batch = queue.splice(0, 50);
    if (!url) return;
    var body = JSON.stringify(batch.length === 1 ? batch[0] : batch);
    try {
      if ((unloading || typeof fetch !== 'function') && navigator.sendBeacon &&
          navigator.sendBeacon(url, new Blob([body], { type: 'text/plain;charset=UTF-8' }))) {
        return;
      }
      if (typeof fetch !== 'function') return;
      // text/plain keeps this a "simple" request: no CORS preflight from the GitHub Pages copy
      fetch(url, {
        method: 'POST',
        body: body,
        keepalive: true,
        credentials: 'omit',
        headers: { 'Content-Type': 'text/plain;charset=UTF-8' }
      }).then(function (r) { return r.ok ? r.json() : null; })
        .then(function (j) {
          if (j && typeof j.sample_rate === 'number') lsSet('lmod_tsr', JSON.stringify({ r: j.sample_rate, t: Date.now() }));
        })
        .catch(function () {});
    } catch (e) {}
    if (queue.length) flush(unloading);
  }

  function commitPendingSearch() {
    if (searchTimer) { clearTimeout(searchTimer); searchTimer = null; }
    if (!pendingSearch) return;
    var p = pendingSearch;
    pendingSearch = null;
    if (p.q === lastSearch) return;
    lastSearch = p.q;
    LModTracker.track('search_query', p.gameId, p.q);
  }

  const LModTracker = {
    sessionId: (function () {
      let sid = lsGet('lmod_sid');
      if (!sid) {
        sid = 'sid_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 9);
        lsSet('lmod_sid', sid);
      }
      return sid;
    })(),

    userId: (function () {
      try {
        const u = lsGet('lmod_player_user');
        if (u) {
          const parsed = JSON.parse(u);
          return parsed.id || null;
        }
      } catch (e) {}
      return null;
    })(),

    setUserId: function (uid) {
      this.userId = uid || null;
    },

    getUserId: function () {
      if (this.userId) return this.userId;
      if (window.LModAuth && typeof window.LModAuth.getUserId === 'function') {
        const id = window.LModAuth.getUserId();
        if (id) {
          this.userId = id;
          return id;
        }
      }
      return null;
    },

    track: function (eventType, gameId, targetPayload) {
      try {
        if (!eventType) return;
        if (eventType !== 'search_query' && pendingSearch) commitPendingSearch();
        if (fnv1a(this.sessionId) / 4294967296 >= cachedSampleRate()) return;

        const payloadText = (targetPayload === undefined || targetPayload === null || targetPayload === '')
          ? null : String(targetPayload).slice(0, 255);
        const path = pagePath();
        const sig = eventType + '|' + (gameId || '') + '|' + (payloadText || '') + '|' + path;
        const now = Date.now();
        if (lastSent[sig] && now - lastSent[sig] < DEDUPE_MS) return;
        lastSent[sig] = now;

        queue.push({
          event_type: eventType,
          game_id: gameId || null,
          target_payload: eventType === 'ai_ask' ? null : payloadText,
          session_id: this.sessionId,
          user_id: this.getUserId(),
          page_path: path,
          referrer_host: referrerHost(),
          device_type: deviceType(),
          ui_lang: uiLang(),
          site_host: location.hostname
        });
        if (queue.length >= 20) flush(false);
        else if (!flushTimer) flushTimer = setTimeout(function () { flush(false); }, FLUSH_MS);
      } catch (err) {
        // Silent fail for analytics
      }
    },

    trackPageView: function (gameId) {
      this.track('page_view', gameId || null, null);
    },

    trackSearch: function (query, gameId) {
      const q = String(query == null ? '' : query).replace(/\s+/g, ' ').trim().toLowerCase().slice(0, 100);
      if (searchTimer) { clearTimeout(searchTimer); searchTimer = null; }
      if (!q) { pendingSearch = null; return; }
      pendingSearch = { q: q, gameId: gameId || null };
      searchTimer = setTimeout(commitPendingSearch, SEARCH_IDLE_MS);
    },

    flush: function () { flush(false); }
  };

  // Outbound links and declarative tracking, caught in the capture phase so page handlers can't swallow them
  document.addEventListener('click', function (e) {
    try {
      const el = e.target && e.target.closest ? e.target.closest('[data-lmod-track], a[href]') : null;
      if (!el) return;
      const holder = el.closest('[data-game-id]');
      const gid = el.getAttribute('data-lmod-game') || (holder && holder.getAttribute('data-game-id')) || currentGameId();
      const declared = el.getAttribute('data-lmod-track');
      if (declared) {
        LModTracker.track(declared, gid, el.getAttribute('data-lmod-payload'));
        return;
      }
      const host = new URL(el.getAttribute('href'), location.href).hostname.toLowerCase();
      if (/(^|\.)flingtrainer\.com$/.test(host)) LModTracker.track('trainer_official_click', gid, host);
      else if (/(^|\.)nexusmods\.com$/.test(host)) LModTracker.track('mod_download_click', gid, 'nexus_page');
    } catch (err) {}
  }, true);

  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') flush(true);
  });
  window.addEventListener('pagehide', function () { flush(true); });

  // 2. High-Performance API Client with In-Memory Cache
  const memoryCache = new Map();

  const LModAPI = {
    baseUrl: '/api/v1',

    // Fetch lightweight catalog with offline fallback
    fetchGames: async function (options) {
      options = options || {};
      const page = options.page || 1;
      const pageSize = options.pageSize || 24;
      const genre = options.genre || 'all';
      const compatStatus = options.compatStatus || 'all';
      const sortBy = options.sortBy || 'rank';

      const cacheKey = `games_${page}_${pageSize}_${genre}_${compatStatus}_${sortBy}`;
      if (memoryCache.has(cacheKey)) {
        return memoryCache.get(cacheKey);
      }

      try {
        const query = new URLSearchParams({
          page: String(page),
          page_size: String(pageSize),
          genre: genre,
          compat_status: compatStatus,
          sort_by: sortBy
        });

        const res = await fetch(`${this.baseUrl}/games?${query.toString()}`);
        if (!res.ok) throw new Error(`HTTP error ${res.status}`);
        const json = await res.json();
        if (json.code === 0 && json.data && json.data.items) {
          memoryCache.set(cacheKey, json);
          return json;
        }
        throw new Error(json.message || 'API error');
      } catch (err) {
        console.warn('[L-MOD API] Live edge fetch failed, falling back to local dataset:', err.message);
        // Fallback to local window.GAMES_DATA
        const local = (window.GAMES_DATA || window.GAMES_DATABASE || []);
        return {
          code: 0,
          fallback: true,
          data: {
            items: local
          },
          meta: {
            page: 1,
            page_size: local.length,
            total: local.length,
            has_more: false
          }
        };
      }
    },

    // Fetch single game full metadata
    fetchGameDetail: async function (gameId) {
      if (!gameId) return null;
      const cacheKey = `game_${gameId}`;
      if (memoryCache.has(cacheKey)) return memoryCache.get(cacheKey);

      try {
        const res = await fetch(`${this.baseUrl}/games/${encodeURIComponent(gameId)}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (json.code === 0 && json.data) {
          memoryCache.set(cacheKey, json.data);
          return json.data;
        }
      } catch (err) {
        console.warn(`[L-MOD API] Fallback for game detail: ${gameId}`);
      }

      // Local fallback
      const local = (window.GAMES_DATA || window.GAMES_DATABASE || []).find(g => g.id === gameId);
      return local || null;
    },

    // Asynchronously fetch commands by category for a specific game
    fetchGameCommands: async function (gameId, options) {
      options = options || {};
      const cacheKey = `cmds_${gameId}_${options.categoryId || 'all'}_${options.popularOnly ? 'pop' : 'all'}`;
      if (memoryCache.has(cacheKey)) return memoryCache.get(cacheKey);

      try {
        const params = new URLSearchParams();
        if (options.categoryId) params.set('category_id', options.categoryId);
        if (options.popularOnly) params.set('popular_only', 'true');
        if (options.query) params.set('q', options.query);

        const res = await fetch(`${this.baseUrl}/games/${encodeURIComponent(gameId)}/commands?${params.toString()}`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (json.code === 0 && json.data) {
          memoryCache.set(cacheKey, json.data);
          return json.data;
        }
      } catch (err) {
        console.warn(`[L-MOD API] Commands API failed for ${gameId}, checking local fallback`);
      }

      // Local fallback extraction
      const game = (window.GAMES_DATA || window.GAMES_DATABASE || []).find(g => g.id === gameId);
      if (game && game.consoleCategories) {
        const flatCmds = [];
        game.consoleCategories.forEach(cat => {
          (cat.commands || []).forEach(c => {
            flatCmds.push({
              name_zh: c.name?.['zh-CN'] || c.name,
              name_en: c.name?.['en'] || c.name,
              code: c.code,
              description: c.desc,
              category_name_zh: cat.category,
              category_name_en: cat.category
            });
          });
        });
        return {
          game_id: gameId,
          total: flatCmds.length,
          commands: flatCmds,
          categories: game.consoleCategories.map(c => ({ category_name_zh: c.category, count: c.commands?.length || 0 }))
        };
      }
      return { game_id: gameId, total: 0, commands: [], categories: [] };
    },

    // Fast typeahead search
    searchGames: async function (query) {
      if (!query || !query.trim()) return [];
      try {
        const res = await fetch(`${this.baseUrl}/games/search?q=${encodeURIComponent(query.trim())}`);
        if (!res.ok) throw new Error();
        const json = await res.json();
        if (json.code === 0 && json.data) return json.data.items || [];
      } catch (e) {}

      // Local search fallback
      const q = query.toLowerCase();
      const local = (window.GAMES_DATA || window.GAMES_DATABASE || []);
      return local.filter(g =>
        g.title.toLowerCase().includes(q) ||
        (g.titles && Object.values(g.titles).some(t => t.toLowerCase().includes(q))) ||
        (g.developer && g.developer.toLowerCase().includes(q))
      ).slice(0, 8);
    },

    // Download URL generator for .bat scripts
    getDownloadBatUrl: function (gameId, bundleId) {
      let url = `${this.baseUrl}/games/${encodeURIComponent(gameId)}/download`;
      if (bundleId) url += `?bundle_id=${encodeURIComponent(bundleId)}`;
      return url;
    }
  };

  // Expose to window
  window.LModTracker = LModTracker;
  window.LModAPI = LModAPI;

})(window);
