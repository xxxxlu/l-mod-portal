/**
 * L-MOD Vault - Client-Side API & Telemetry SDK (v2.0)
 * Modern asynchronous client with offline fallback & non-blocking telemetry.
 */

(function (window) {
  'use strict';

  // 1. Unified Telemetry Engine
  const LModTracker = {
    sessionId: (function () {
      let sid = localStorage.getItem('lmod_sid');
      if (!sid) {
        sid = 'sid_' + Date.now().toString(36) + '_' + Math.random().toString(36).slice(2, 9);
        try { localStorage.setItem('lmod_sid', sid); } catch (e) {}
      }
      return sid;
    })(),

    track: function (eventType, gameId, targetPayload) {
      try {
        const payload = JSON.stringify({
          event_type: eventType,
          game_id: gameId || null,
          target_payload: targetPayload ? String(targetPayload).slice(0, 255) : null,
          session_id: this.sessionId,
          timestamp: Date.now()
        });

        if (navigator.sendBeacon) {
          navigator.sendBeacon('/api/v1/telemetry/events', payload);
        } else {
          fetch('/api/v1/telemetry/events', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: payload,
            keepalive: true
          }).catch(function () {});
        }
      } catch (err) {
        // Silent fail for analytics
      }
    }
  };

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
