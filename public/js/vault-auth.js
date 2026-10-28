/**
 * L-MOD Vault - Player Authentication & Identity SDK (v1.0)
 * Handles Email OTP Login, Web Crypto PBKDF2 Password Setup Wizard,
 * Real-time Favorites Synchronization & Community Feedback Association.
 */

(function (window) {
  'use strict';

  const STORAGE_KEY_TOKEN = 'lmod_player_token';
  const STORAGE_KEY_USER = 'lmod_player_user';
  const STORAGE_KEY_FAVORITES = 'lmod_user_favorites';

  const LModAuth = {
    token: localStorage.getItem(STORAGE_KEY_TOKEN) || null,
    user: (function () {
      try {
        const raw = localStorage.getItem(STORAGE_KEY_USER);
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    })(),
    favorites: new Set((function () {
      try {
        const raw = localStorage.getItem(STORAGE_KEY_FAVORITES);
        return raw ? JSON.parse(raw) : [];
      } catch (e) {
        return [];
      }
    })()),

    cooldownTimer: null,
    cooldownRemaining: 0,
    changeEmailCooldownTimer: null,
    changeEmailCooldownRemaining: 0,

    init: function () {
      this.injectAuthModals();
      this.bindGlobalEvents();
      this.updateNavbarAuthUI();

      if (this.isLoggedIn()) {
        this.syncProfile();
      }
    },

    isLoggedIn: function () {
      return Boolean(this.token && this.user && this.user.id);
    },

    getUserId: function () {
      return this.user ? this.user.id : null;
    },

    getUser: function () {
      return this.user;
    },

    getToken: function () {
      return this.token;
    },

    toast: function (msg) {
      if (typeof window.showToast === 'function') {
        window.showToast(msg);
      } else {
        alert(msg);
      }
    },

    // -------------------------------------------------------------------------
    // API Client with Auth Header
    // -------------------------------------------------------------------------
    apiFetch: async function (path, options = {}) {
      const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {})
      };

      if (this.token) {
        headers['Authorization'] = `Bearer ${this.token}`;
        headers['X-Player-Token'] = this.token;
      }

      const res = await fetch(`/api/v1/auth${path}`, {
        ...options,
        headers
      });

      const json = await res.json().catch(() => ({}));
      if (!res.ok) {
        throw new Error(json.message || `Request failed with status ${res.status}`);
      }
      return json;
    },

    // -------------------------------------------------------------------------
    // Auth Lifecycle Methods
    // -------------------------------------------------------------------------
    sendOtpCode: async function (email, purpose = 'login') {
      if (!email) throw new Error('请输入有效的邮箱地址');
      const res = await this.apiFetch('/send-code', {
        method: 'POST',
        body: JSON.stringify({ email, purpose })
      });
      return res;
    },

    verifyOtpCode: async function (email, code, purpose = 'login') {
      const res = await this.apiFetch('/verify-code', {
        method: 'POST',
        body: JSON.stringify({ email, code, purpose })
      });

      if (res.code === 0 && res.data && res.data.token) {
        this.saveSession(res.data.token, res.data.user);
        this.toast(res.data.is_first_login ? '🎉 欢迎新玩家！账号已自动建立' : '✅ 登录成功！');
        this.closeAuthModal();

        // Check if password setup wizard should be prompted
        if (!res.data.has_password) {
          setTimeout(() => {
            this.openPasswordWizardModal();
          }, 400);
        }

        // Sync fresh profile & favorites
        this.syncProfile();
      }
      return res;
    },

    loginWithPassword: async function (email, password) {
      const res = await this.apiFetch('/login-password', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      });

      if (res.code === 0 && res.data && res.data.token) {
        this.saveSession(res.data.token, res.data.user);
        this.toast('✅ 密码核验成功，欢迎回到 L-MOD Vault！');
        this.closeAuthModal();
        this.syncProfile();
      }
      return res;
    },

    setPassword: async function (password, oldPassword = null) {
      const res = await this.apiFetch('/set-password', {
        method: 'POST',
        body: JSON.stringify({
          password,
          old_password: oldPassword || undefined
        })
      });

      if (res.code === 0) {
        if (this.user) {
          this.user.has_password = true;
          localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(this.user));
        }
        this.toast('🛡️ 独立登录密码保存成功！');
        this.closePasswordWizardModal();
        this.closeSecurityModal();
      }
      return res;
    },

    changeEmail: async function (newEmail, code) {
      const res = await this.apiFetch('/change-email', {
        method: 'POST',
        body: JSON.stringify({ new_email: newEmail, code })
      });

      if (res.code === 0 && res.data) {
        if (res.data.token) this.token = res.data.token;
        if (this.user) {
          this.user.email = res.data.email;
          localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(this.user));
          localStorage.setItem(STORAGE_KEY_TOKEN, this.token);
        }
        this.toast('✅ 安全绑定邮箱已成功更换！');
        this.closeSecurityModal();
        this.updateNavbarAuthUI();
      }
      return res;
    },

    syncProfile: async function () {
      if (!this.token) return;
      try {
        const res = await this.apiFetch('/me', { method: 'GET' });
        if (res.code === 0 && res.data && res.data.user) {
          this.user = {
            ...this.user,
            ...res.data.user
          };
          localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(this.user));

          // Sync Favorites
          const favIds = (res.data.favorites || []).map(f => f.game_id);
          this.favorites = new Set(favIds);
          localStorage.setItem(STORAGE_KEY_FAVORITES, JSON.stringify(favIds));

          this.updateNavbarAuthUI();
          this.updateHeartVisuals();
        }
      } catch (e) {
        console.warn('[L-MOD Auth] Sync profile warning:', e.message);
        if (e.message.includes('401') || e.message.includes('过期')) {
          this.logout(false);
        }
      }
    },

    saveSession: function (token, user) {
      this.token = token;
      this.user = user;
      localStorage.setItem(STORAGE_KEY_TOKEN, token);
      localStorage.setItem(STORAGE_KEY_USER, JSON.stringify(user));

      if (window.LModTracker && typeof window.LModTracker.setUserId === 'function') {
        window.LModTracker.setUserId(user.id);
      }

      this.updateNavbarAuthUI();
    },

    logout: function (showNotification = true) {
      this.token = null;
      this.user = null;
      this.favorites.clear();
      localStorage.removeItem(STORAGE_KEY_TOKEN);
      localStorage.removeItem(STORAGE_KEY_USER);
      localStorage.removeItem(STORAGE_KEY_FAVORITES);

      if (window.LModTracker && typeof window.LModTracker.setUserId === 'function') {
        window.LModTracker.setUserId(null);
      }

      this.updateNavbarAuthUI();
      this.updateHeartVisuals();
      this.closeProfileDrawer();

      if (showNotification) {
        this.toast('已安全退出登录');
      }
    },

    // -------------------------------------------------------------------------
    // Favorites Subsystem
    // -------------------------------------------------------------------------
    isFavorited: function (gameId) {
      return this.favorites.has(gameId);
    },

    toggleFavorite: async function (gameId, e) {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }

      if (!this.isLoggedIn()) {
        this.toast('🔒 请先登录，以便将单机神作收藏永久保存至云端');
        this.openAuthModal();
        return;
      }

      // Optimistic update
      const willFavorite = !this.favorites.has(gameId);
      if (willFavorite) {
        this.favorites.add(gameId);
      } else {
        this.favorites.delete(gameId);
      }

      localStorage.setItem(STORAGE_KEY_FAVORITES, JSON.stringify(Array.from(this.favorites)));
      this.updateHeartVisuals(gameId);

      try {
        const res = await this.apiFetch('/favorites', {
          method: 'POST',
          body: JSON.stringify({ game_id: gameId, action: willFavorite ? 'add' : 'remove' })
        });
        if (res.code === 0) {
          this.toast(willFavorite ? '💖 已收藏至我的单机宝库' : '已从收藏中移除');
        }
      } catch (err) {
        // Rollback on network error
        if (willFavorite) this.favorites.delete(gameId);
        else this.favorites.add(gameId);
        localStorage.setItem(STORAGE_KEY_FAVORITES, JSON.stringify(Array.from(this.favorites)));
        this.updateHeartVisuals(gameId);
        this.toast('收藏操作失败，请检查网络');
      }
    },

    updateHeartVisuals: function (targetGameId = null) {
      const selector = targetGameId 
        ? `[data-fav-btn="${targetGameId}"]`
        : `[data-fav-btn]`;

      document.querySelectorAll(selector).forEach(btn => {
        const gid = btn.getAttribute('data-fav-btn');
        const isFav = this.favorites.has(gid);
        const icon = btn.querySelector('.fav-heart-icon');

        if (isFav) {
          btn.classList.add('is-favorited', 'text-purple-500', 'dark:text-purple-400');
          btn.classList.remove('text-zinc-400', 'dark:text-zinc-500');
          if (icon) {
            icon.setAttribute('fill', 'currentColor');
            icon.classList.add('scale-110');
          }
        } else {
          btn.classList.remove('is-favorited', 'text-purple-500', 'dark:text-purple-400');
          btn.classList.add('text-zinc-400', 'dark:text-zinc-500');
          if (icon) {
            icon.setAttribute('fill', 'none');
            icon.classList.remove('scale-110');
          }
        }
      });
    },

    // -------------------------------------------------------------------------
    // UI Renderers & Navbar Sync
    // -------------------------------------------------------------------------
    updateNavbarAuthUI: function () {
      const container = document.getElementById('navbar-auth-container');
      const mobileContainer = document.getElementById('sidebar-auth-container');

      if (!container) return;

      if (this.isLoggedIn()) {
        const user = this.user;
        const avatarUrl = user.avatar_url || 'avatar.jpg';
        const nickname = user.nickname || '单机玩家';
        const isSuperAdmin = Boolean(user && user.email && user.email.toLowerCase().trim() === 'xlu021104@gmail.com');

        const userHtml = `
          <div class="flex items-center space-x-2">
            ${isSuperAdmin ? `
              <a 
                href="admin" 
                target="_blank" 
                class="hidden sm:flex items-center space-x-1.5 bg-gradient-to-r from-purple-600/30 via-pink-600/30 to-purple-600/30 hover:from-purple-600/50 hover:to-pink-600/50 text-purple-200 px-2.5 py-1 rounded-full text-xs font-bold border border-purple-500/40 shadow-sm transition-all" 
                title="站长管理中台 (特权通道)"
              >
                <span>👑</span>
                <span class="font-mono">中台管理</span>
              </a>
            ` : ''}

            <div class="relative" id="user-profile-menu-wrap">
              <button 
                type="button" 
                onclick="window.LModAuth.toggleProfileDropdown(event)"
                class="flex items-center space-x-2 bg-purple-500/10 hover:bg-purple-500/20 text-purple-700 dark:text-purple-300 px-3 py-1 rounded-full text-xs font-semibold border border-purple-500/30 transition-all cursor-pointer shadow-sm group"
                id="user-profile-btn"
              >
                <img src="${avatarUrl}" alt="Avatar" class="w-5 h-5 rounded-full object-cover border border-purple-400/50">
                <span class="max-w-[100px] truncate tracking-tight font-mono-tech">${nickname}</span>
                <svg class="w-3 h-3 text-purple-400 group-hover:translate-y-0.5 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
              </button>

              <!-- Floating Popover Panel -->
              <div 
                id="user-profile-popover" 
                class="hidden absolute right-0 mt-2 w-72 bg-white/95 dark:bg-[#12141a]/95 backdrop-blur-2xl rounded-2xl p-3 shadow-2xl border border-zinc-200/80 dark:border-white/10 z-50 text-xs"
              >
                <div class="p-3 bg-purple-500/10 dark:bg-purple-500/15 rounded-xl border border-purple-500/20 mb-3 flex items-center space-x-3">
                  <img src="${avatarUrl}" class="w-10 h-10 rounded-full border border-purple-400/50 object-cover shrink-0">
                  <div class="overflow-hidden min-w-0 flex-1">
                    <div class="font-bold text-zinc-900 dark:text-white truncate flex items-center gap-1.5">
                      <span>${nickname}</span>
                      ${isSuperAdmin ? '<span class="text-[9px] font-mono px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 font-bold border border-amber-500/30">👑 站长</span>' : ''}
                    </div>
                    <div class="text-[11px] text-zinc-500 dark:text-zinc-400 font-mono-tech truncate">${user.email || '未绑定'}</div>
                    <div class="mt-1 flex items-center gap-1.5">
                      <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-400 font-bold">已认证玩家</span>
                      ${user.has_password ? '<span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-400">已设密码</span>' : '<span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-400 cursor-pointer" onclick="window.LModAuth.openPasswordWizardModal()">未设密码⚡</span>'}
                    </div>
                  </div>
                </div>

                <div class="space-y-1">
                  ${isSuperAdmin ? `
                    <a href="admin" target="_blank" class="w-full flex items-center justify-between px-3 py-2 rounded-xl text-left bg-gradient-to-r from-purple-500/15 to-pink-500/15 hover:from-purple-500/25 hover:to-pink-500/25 border border-purple-500/30 transition text-purple-200 font-bold mb-1 group">
                      <span class="flex items-center space-x-2">
                        <span>👑</span>
                        <span>站长管理中台 (Admin)</span>
                      </span>
                      <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-purple-500/30 text-purple-300 group-hover:translate-x-0.5 transition-transform">进入 →</span>
                    </a>
                  ` : ''}

                  <button onclick="window.LModAuth.filterMyFavorites()" class="w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-zinc-100 dark:hover:bg-white/5 transition text-zinc-700 dark:text-zinc-300">
                    <span class="flex items-center space-x-2"><span>⭐</span><span>我的单机收藏</span></span>
                    <span class="font-mono-tech font-bold text-purple-500 bg-purple-500/10 px-2 py-0.5 rounded-full text-[10px]" id="user-popover-fav-count">${this.favorites.size} 款</span>
                  </button>

                  <a href="radar" class="w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-zinc-100 dark:hover:bg-white/5 transition text-zinc-700 dark:text-zinc-300">
                    <span class="flex items-center space-x-2"><span>📡</span><span>Steam 避坑雷达</span></span>
                    <span class="text-[10px] text-zinc-400">巡检</span>
                  </a>

                  <button onclick="window.LModAuth.openSecurityModal()" class="w-full flex items-center justify-between px-3 py-2 rounded-xl text-left hover:bg-zinc-100 dark:hover:bg-white/5 transition text-zinc-700 dark:text-zinc-300">
                    <span class="flex items-center space-x-2"><span>🔒</span><span>账号安全设置</span></span>
                    <span class="text-[10px] text-zinc-400">改密/改绑</span>
                  </button>

                  <div class="my-1 border-t border-zinc-200/60 dark:border-white/5"></div>

                  <button onclick="window.LModAuth.logout()" class="w-full flex items-center space-x-2 px-3 py-2 rounded-xl text-left hover:bg-red-500/10 text-red-500 dark:text-red-400 transition">
                    <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
                    <span>退出登录</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        `;

        container.innerHTML = userHtml;
        if (mobileContainer) {
          mobileContainer.innerHTML = `
            <div class="space-y-2">
              <div class="px-3 py-2 bg-purple-500/10 rounded-xl border border-purple-500/20 flex items-center justify-between cursor-pointer" onclick="window.LModAuth.toggleProfileDropdown(event)">
                <div class="flex items-center space-x-2.5 truncate">
                  <img src="${avatarUrl}" class="w-7 h-7 rounded-full object-cover">
                  <div class="truncate">
                    <div class="font-bold text-xs text-white truncate flex items-center gap-1">
                      <span>${nickname}</span>
                      ${isSuperAdmin ? '<span class="text-[8px] bg-amber-500/20 text-amber-300 px-1 rounded font-mono">👑 站长</span>' : ''}
                    </div>
                    <div class="text-[10px] text-purple-400 font-mono">${isSuperAdmin ? '站长特权账号' : '已登录玩家'}</div>
                  </div>
                </div>
                <span class="text-xs text-purple-400 font-bold">${this.favorites.size} 收藏</span>
              </div>
              ${isSuperAdmin ? `
                <a href="admin" target="_blank" class="w-full flex items-center justify-center space-x-2 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-2 rounded-xl text-xs font-bold shadow-md transition">
                  <span>👑</span>
                  <span>进入站长管理中台</span>
                </a>
              ` : ''}
            </div>
          `;
        }
      } else {
        const guestHtml = `
          <button 
            type="button" 
            onclick="window.LModAuth.openAuthModal()"
            class="flex items-center space-x-1.5 bg-gradient-to-r from-purple-600/90 to-indigo-600/90 hover:from-purple-600 hover:to-indigo-600 text-white px-3.5 py-1.5 rounded-full text-xs font-semibold shadow-md shadow-purple-500/20 transition-all cursor-pointer"
            id="nav-login-btn"
          >
            <span>🔑</span>
            <span>登录 / 注册</span>
          </button>
        `;

        container.innerHTML = guestHtml;
        if (mobileContainer) {
          mobileContainer.innerHTML = `
            <button onclick="window.LModAuth.openAuthModal()" class="w-full flex items-center justify-center space-x-2 bg-purple-600 hover:bg-purple-700 text-white py-2.5 rounded-xl text-xs font-bold transition shadow-md shadow-purple-600/30">
              <span>🔑</span>
              <span>登录 / 注册开启云端收藏</span>
            </button>
          `;
        }
      }
    },

    toggleProfileDropdown: function (e) {
      if (e) e.stopPropagation();
      const popover = document.getElementById('user-profile-popover');
      if (popover) {
        popover.classList.toggle('hidden');
      }
    },

    closeProfileDrawer: function () {
      const popover = document.getElementById('user-profile-popover');
      if (popover) popover.classList.add('hidden');
    },

    filterMyFavorites: function () {
      this.closeProfileDrawer();
      if (!this.favorites.size) {
        this.toast('您暂未收藏任何单机游戏，点击卡片右上角心形即可收藏！');
        return;
      }

      // Filter in allGames if available
      if (window.allGames && typeof window.renderGames === 'function') {
        const favIds = Array.from(this.favorites);
        window.currentFilter = 'all';
        const galleryCon = document.getElementById('games-gallery-container');
        if (galleryCon) {
          // Temporarily show favorited
          this.toast(`🔍 已为您筛选出 ${favIds.length} 款单机神作收藏！`);
          window.location.hash = '#/';
          // Highlight
          setTimeout(() => {
            document.querySelectorAll('[data-holo-card]').forEach(cardWrap => {
              const link = cardWrap.querySelector('.pokemon-card');
              if (link) {
                const id = link.id.replace('game-card-', '');
                if (favIds.includes(id)) {
                  cardWrap.style.display = 'block';
                  cardWrap.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                } else {
                  cardWrap.style.display = 'none';
                }
              }
            });
            const countElem = document.getElementById('games-count-display');
            if (countElem) {
              countElem.innerHTML = `⭐ <span class="text-purple-400 font-bold">我的专属单机收藏</span> · 共 ${favIds.length} 款 · <button onclick="window.setFilterAndNavigate('all')" class="text-purple-400 underline ml-2">恢复全部显示</button>`;
            }
          }, 100);
        }
      }
    },

    // -------------------------------------------------------------------------
    // Modal Openers / Closers
    // -------------------------------------------------------------------------
    isValidEmail: function (email) {
      if (!email || typeof email !== 'string') return false;
      const trimmed = email.trim().toLowerCase();
      if (trimmed.length < 5 || trimmed.length > 128) return false;
      const regex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
      if (!regex.test(trimmed)) return false;
      const parts = trimmed.split('@');
      if (parts.length !== 2) return false;
      const [localPart, domainPart] = parts;
      if (!localPart || !domainPart) return false;
      if (!domainPart.includes('.')) return false;
      const domainSegments = domainPart.split('.');
      const tld = domainSegments[domainSegments.length - 1];
      if (tld.length < 2) return false;
      return true;
    },

    openAuthModal: function (initialTab = 'login') {
      const modal = document.getElementById('cyber-auth-modal');
      if (modal) {
        modal.classList.remove('hidden');
        this.switchAuthTab(initialTab);
        setTimeout(() => {
          const input = document.getElementById(initialTab === 'login' ? 'auth-login-email' : 'auth-reg-email');
          if (input) input.focus();
        }, 100);
      }
    },

    closeAuthModal: function () {
      const modal = document.getElementById('cyber-auth-modal');
      if (modal) modal.classList.add('hidden');
    },

    openPasswordWizardModal: function () {
      const modal = document.getElementById('password-wizard-modal');
      if (modal) {
        modal.classList.remove('hidden');
        setTimeout(() => {
          const input = document.getElementById('wizard-pwd-input');
          if (input) input.focus();
        }, 100);
      }
    },

    closePasswordWizardModal: function () {
      const modal = document.getElementById('password-wizard-modal');
      if (modal) modal.classList.add('hidden');
    },

    openSecurityModal: function (tab = 'pwd') {
      this.closeProfileDrawer();
      const modal = document.getElementById('security-settings-modal');
      if (modal) {
        modal.classList.remove('hidden');
        this.switchSecurityTab(tab);
      }
    },

    closeSecurityModal: function () {
      const modal = document.getElementById('security-settings-modal');
      if (modal) modal.classList.add('hidden');
    },

    switchAuthTab: function (tab) {
      const tabLoginBtn = document.getElementById('tab-btn-login');
      const tabRegBtn = document.getElementById('tab-btn-reg');
      const panelLogin = document.getElementById('auth-panel-login');
      const panelReg = document.getElementById('auth-panel-reg');

      if (tab === 'login' || tab === 'pwd' || tab === 'otp') {
        if (tabLoginBtn) tabLoginBtn.className = 'flex-1 py-2 text-xs font-bold rounded-xl bg-purple-600 text-white shadow-md shadow-purple-600/30 transition cursor-pointer';
        if (tabRegBtn) tabRegBtn.className = 'flex-1 py-2 text-xs font-semibold rounded-xl text-zinc-400 hover:text-white transition cursor-pointer';
        if (panelLogin) panelLogin.classList.remove('hidden');
        if (panelReg) panelReg.classList.add('hidden');
      } else {
        if (tabRegBtn) tabRegBtn.className = 'flex-1 py-2 text-xs font-bold rounded-xl bg-purple-600 text-white shadow-md shadow-purple-600/30 transition cursor-pointer';
        if (tabLoginBtn) tabLoginBtn.className = 'flex-1 py-2 text-xs font-semibold rounded-xl text-zinc-400 hover:text-white transition cursor-pointer';
        if (panelReg) panelReg.classList.remove('hidden');
        if (panelLogin) panelLogin.classList.add('hidden');
      }
    },

    switchSecurityTab: function (tab) {
      const btnPwd = document.getElementById('sec-tab-btn-pwd');
      const btnEmail = document.getElementById('sec-tab-btn-email');
      const panelPwd = document.getElementById('sec-panel-pwd');
      const panelEmail = document.getElementById('sec-panel-email');

      if (tab === 'pwd') {
        btnPwd.className = 'flex-1 py-2 text-xs font-bold rounded-xl bg-purple-600 text-white transition';
        btnEmail.className = 'flex-1 py-2 text-xs font-semibold rounded-xl text-zinc-400 hover:text-white transition';
        panelPwd.classList.remove('hidden');
        panelEmail.classList.add('hidden');
      } else {
        btnEmail.className = 'flex-1 py-2 text-xs font-bold rounded-xl bg-purple-600 text-white transition';
        btnPwd.className = 'flex-1 py-2 text-xs font-semibold rounded-xl text-zinc-400 hover:text-white transition';
        panelEmail.classList.remove('hidden');
        panelPwd.classList.add('hidden');
      }
    },

    // -------------------------------------------------------------------------
    // Injection of High-Tech Frosted Modals
    // -------------------------------------------------------------------------
    injectAuthModals: function () {
      if (document.getElementById('lmod-auth-modals-root')) return;

      const root = document.createElement('div');
      root.id = 'lmod-auth-modals-root';

      root.innerHTML = `
        <!-- ======================================================== -->
        <!-- 1. CYBER FROSTED AUTH MODAL (PASSWORD LOGIN & REGISTER)  -->
        <!-- ======================================================== -->
        <div id="cyber-auth-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-fade-in">
          <div class="relative w-full max-w-md bg-[#0f1117] border border-purple-500/30 rounded-3xl p-6 sm:p-8 shadow-2xl shadow-purple-950/50 text-white overflow-hidden">
            <!-- Neon Foil Glow Background Top Arc -->
            <div class="absolute -top-24 left-1/2 -translate-x-1/2 w-64 h-32 bg-purple-600/25 blur-3xl rounded-full pointer-events-none"></div>

            <!-- Close Button -->
            <button onclick="window.LModAuth.closeAuthModal()" class="absolute top-5 right-5 text-zinc-400 hover:text-white p-2 rounded-full hover:bg-white/10 transition cursor-pointer">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>

            <!-- Brand Header -->
            <div class="text-center mb-6">
              <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 text-[11px] font-mono-tech font-bold uppercase mb-2">
                <span class="w-1.5 h-1.5 rounded-full bg-purple-400 animate-ping"></span>
                <span>L-MOD Identity Engine</span>
              </div>
              <h2 class="text-2xl font-extrabold tracking-tight">玩家身份认证</h2>
              <p class="text-xs text-zinc-400 mt-1">登录即享全站单机收藏同步、避坑雷达专线与专属画像</p>
            </div>

            <!-- Tabs Switcher -->
            <div class="flex items-center p-1 bg-zinc-900/80 rounded-2xl border border-white/5 mb-6">
              <button id="tab-btn-login" onclick="window.LModAuth.switchAuthTab('login')" class="flex-1 py-2 text-xs font-bold rounded-xl bg-purple-600 text-white shadow-md shadow-purple-600/30 transition cursor-pointer">
                🔑 账号密码登录
              </button>
              <button id="tab-btn-reg" onclick="window.LModAuth.switchAuthTab('register')" class="flex-1 py-2 text-xs font-semibold rounded-xl text-zinc-400 hover:text-white transition cursor-pointer">
                ✨ 注册新账号
              </button>
            </div>

            <!-- PANEL 1: PASSWORD LOGIN -->
            <div id="auth-panel-login" class="space-y-4">
              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1.5">电子邮箱 · EMAIL (支持QQ/163/Gmail等正规邮箱)</label>
                <input 
                  type="email" 
                  id="auth-login-email" 
                  placeholder="例如：gamer@qq.com、xxx@163.com、xxx@gmail.com" 
                  class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-purple-500 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-purple-500 transition font-mono-tech"
                >
              </div>

              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1.5">登录密码 · PASSWORD</label>
                <div class="relative">
                  <input 
                    type="password" 
                    id="auth-login-pwd" 
                    placeholder="输入您的独立登录密码" 
                    class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-purple-500 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-purple-500 transition font-mono-tech pr-10"
                  >
                  <button type="button" onclick="window.LModAuth.togglePasswordVisibility('auth-login-pwd', this)" class="absolute right-3 top-3 text-zinc-500 hover:text-zinc-300">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  </button>
                </div>
              </div>

              <div class="flex items-center justify-between text-xs text-zinc-400">
                <label class="flex items-center space-x-2 cursor-pointer">
                  <input type="checkbox" id="auth-auto-register-check" checked class="rounded bg-zinc-900 border-zinc-700 text-purple-600">
                  <span>未注册自动建号</span>
                </label>
                <button type="button" onclick="window.LModAuth.switchAuthTab('register')" class="text-purple-400 hover:underline">
                  没有账号？前往注册 →
                </button>
              </div>

              <button 
                type="button" 
                id="auth-btn-login-submit" 
                onclick="window.LModAuth.handleLoginSubmit()"
                class="w-full mt-2 py-3.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold rounded-xl text-sm transition shadow-lg shadow-purple-600/30 flex items-center justify-center space-x-2 cursor-pointer"
              >
                <span>🔑 立即登录</span>
              </button>
            </div>

            <!-- PANEL 2: PASSWORD REGISTER -->
            <div id="auth-panel-reg" class="hidden space-y-4">
              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1.5">电子邮箱 · EMAIL (仅限正规合规邮箱)</label>
                <input 
                  type="email" 
                  id="auth-reg-email" 
                  placeholder="例如：your_name@qq.com、163.com、gmail.com" 
                  class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-purple-500 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-purple-500 transition font-mono-tech"
                >
              </div>

              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1.5">设置登录密码 · PASSWORD (至少 6 位)</label>
                <div class="relative">
                  <input 
                    type="password" 
                    id="auth-reg-pwd" 
                    oninput="window.LModAuth.evalPasswordStrength(this.value, 'auth-reg-strength-bar', 'auth-reg-strength-text')"
                    placeholder="设置您的独立登录密码" 
                    class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-purple-500 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-purple-500 transition font-mono-tech pr-10"
                  >
                  <button type="button" onclick="window.LModAuth.togglePasswordVisibility('auth-reg-pwd', this)" class="absolute right-3 top-3 text-zinc-500 hover:text-zinc-300">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                  </button>
                </div>
                <!-- Password Strength Indicator -->
                <div class="mt-2 flex items-center gap-2">
                  <div class="flex-1 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                    <div id="auth-reg-strength-bar" class="h-full w-0 bg-red-500 transition-all duration-300"></div>
                  </div>
                  <span id="auth-reg-strength-text" class="text-[10px] text-zinc-500 font-mono">强度: 未输入</span>
                </div>
              </div>

              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1.5">确认密码 · CONFIRM PASSWORD</label>
                <input 
                  type="password" 
                  id="auth-reg-confirm-pwd" 
                  placeholder="再次输入上述密码以确认" 
                  class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-purple-500 rounded-xl px-4 py-3 text-sm text-white placeholder-zinc-600 focus:outline-none focus:ring-1 focus:ring-purple-500 transition font-mono-tech"
                >
              </div>

              <button 
                type="button" 
                id="auth-btn-reg-submit" 
                onclick="window.LModAuth.handleRegisterSubmit()"
                class="w-full mt-2 py-3.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold rounded-xl text-sm transition shadow-lg shadow-purple-600/30 flex items-center justify-center space-x-2 cursor-pointer"
              >
                <span>🚀 立即注册并进入智库</span>
              </button>

              <div class="text-center text-[11px] text-zinc-500">
                * 密码基于原生 Web Crypto PBKDF2 (10万次运算+独立Salt) 密文存储
              </div>
            </div>

          </div>
        </div>

        <!-- ======================================================== -->
        <!-- 2. FIRST-LOGIN SET PASSWORD WIZARD MODAL                 -->
        <!-- ======================================================== -->
        <div id="password-wizard-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
          <div class="relative w-full max-w-md bg-[#0f1117] border border-amber-500/30 rounded-3xl p-6 sm:p-8 shadow-2xl text-white overflow-hidden">
            <div class="text-center mb-5">
              <div class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-amber-500/15 border border-amber-500/30 text-amber-300 text-xs font-bold uppercase mb-2">
                <span>🛡️ 新手向导 · 安全加固</span>
              </div>
              <h2 class="text-xl font-bold">设置您的独立登录密码</h2>
              <p class="text-xs text-zinc-400 mt-1">设置后后续无需查收邮件即可秒级登录。基于 Web Crypto PBKDF2 10万次运算加密。</p>
            </div>

            <div class="space-y-4">
              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">新密码 · PASSWORD (至少 6 位)</label>
                <input 
                  type="password" 
                  id="wizard-pwd-input" 
                  oninput="window.LModAuth.evalPasswordStrength(this.value, 'wizard-strength-bar', 'wizard-strength-text')"
                  placeholder="请输入您的专属独立密码" 
                  class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-amber-400 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-amber-400 font-mono-tech"
                >
                <!-- Strength indicator -->
                <div class="mt-2 flex items-center gap-2">
                  <div class="flex-1 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
                    <div id="wizard-strength-bar" class="h-full w-0 bg-red-500 transition-all duration-300"></div>
                  </div>
                  <span id="wizard-strength-text" class="text-[10px] text-zinc-500 font-mono">强度: 未输入</span>
                </div>
              </div>

              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">确认新密码 · CONFIRM PASSWORD</label>
                <input 
                  type="password" 
                  id="wizard-pwd-confirm" 
                  placeholder="再次输入以确认" 
                  class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-amber-400 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-amber-400 font-mono-tech"
                >
              </div>

              <div class="pt-2 flex flex-col gap-2">
                <button 
                  type="button" 
                  onclick="window.LModAuth.handleWizardSetPassword()"
                  class="w-full py-3.5 bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-400 hover:to-yellow-400 text-zinc-950 font-bold rounded-xl text-sm transition shadow-lg shadow-amber-500/20"
                >
                  ✓ 立即保存独立密码
                </button>
                <button 
                  type="button" 
                  onclick="window.LModAuth.closePasswordWizardModal()"
                  class="w-full py-2.5 text-xs text-zinc-400 hover:text-white transition"
                >
                  稍后再说 (随时在个人中心开启)
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ======================================================== -->
        <!-- 3. SECURITY SETTINGS MODAL (CHANGE PASSWORD / EMAIL)      -->
        <!-- ======================================================== -->
        <div id="security-settings-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
          <div class="relative w-full max-w-md bg-[#0f1117] border border-zinc-800 rounded-3xl p-6 sm:p-8 shadow-2xl text-white">
            <button onclick="window.LModAuth.closeSecurityModal()" class="absolute top-5 right-5 text-zinc-400 hover:text-white p-2 rounded-full hover:bg-white/10 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>

            <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
              <span>🔒 账户安全与隐私控制</span>
            </h2>

            <div class="flex items-center p-1 bg-zinc-900/80 rounded-2xl border border-white/5 mb-5">
              <button id="sec-tab-btn-pwd" onclick="window.LModAuth.switchSecurityTab('pwd')" class="flex-1 py-2 text-xs font-bold rounded-xl bg-purple-600 text-white transition">
                修改登录密码
              </button>
              <button id="sec-tab-btn-email" onclick="window.LModAuth.switchSecurityTab('email')" class="flex-1 py-2 text-xs font-semibold rounded-xl text-zinc-400 hover:text-white transition">
                更换绑定邮箱
              </button>
            </div>

            <!-- SUBPANEL A: CHANGE PASSWORD -->
            <div id="sec-panel-pwd" class="space-y-3.5">
              <div id="sec-old-pwd-wrap">
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">当前原密码 · CURRENT PASSWORD</label>
                <input type="password" id="sec-old-pwd" placeholder="若未设密码可留空" class="w-full bg-zinc-950/80 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500 font-mono-tech">
              </div>
              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">新密码 · NEW PASSWORD</label>
                <input type="password" id="sec-new-pwd" placeholder="至少 6 位新密码" class="w-full bg-zinc-950/80 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500 font-mono-tech">
              </div>
              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">确认新密码 · CONFIRM PASSWORD</label>
                <input type="password" id="sec-confirm-pwd" placeholder="再次输入新密码" class="w-full bg-zinc-950/80 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500 font-mono-tech">
              </div>
              <button onclick="window.LModAuth.handleSecurityChangePassword()" class="w-full py-3 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-xl text-sm transition mt-2">
                保存密码更改
              </button>
            </div>

            <!-- SUBPANEL B: CHANGE EMAIL -->
            <div id="sec-panel-email" class="hidden space-y-3.5">
              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">新电子邮箱 · NEW EMAIL</label>
                <div class="relative">
                  <input type="email" id="sec-new-email" placeholder="new_email@lmod.gg" class="w-full bg-zinc-950/80 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500 font-mono-tech">
                  <button type="button" id="sec-btn-send-email-code" onclick="window.LModAuth.handleSendChangeEmailOtp()" class="absolute right-1.5 top-1.5 bottom-1.5 px-3 bg-purple-500/20 text-purple-300 rounded-lg text-xs font-bold font-mono-tech border border-purple-500/30">
                    发验证码
                  </button>
                </div>
              </div>
              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">新邮箱验证码 · 6 DIGIT CODE</label>
                <input type="text" id="sec-email-code" maxlength="6" placeholder="输入6位数字" class="w-full bg-zinc-950/80 border border-zinc-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-purple-500 font-mono-tech tracking-widest text-center">
              </div>
              <button onclick="window.LModAuth.handleSecurityChangeEmailSubmit()" class="w-full py-3 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-xl text-sm transition mt-2">
                确认更换绑定
              </button>
            </div>

          </div>
        </div>

        <!-- ======================================================== -->
        <!-- 4. COMMUNITY FEEDBACK MODAL                              -->
        <!-- ======================================================== -->
        <div id="community-feedback-modal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
          <div class="relative w-full max-w-lg bg-[#0f1117] border border-purple-500/30 rounded-3xl p-6 sm:p-8 shadow-2xl text-white">
            <button onclick="window.LModAuth.closeFeedbackModal()" class="absolute top-5 right-5 text-zinc-400 hover:text-white p-2 rounded-full hover:bg-white/10 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
            </button>

            <div class="mb-4">
              <div class="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-purple-500/15 border border-purple-500/30 text-purple-300 text-xs font-bold uppercase mb-2">
                <span>🐞 玩家避坑建议与报错上报</span>
              </div>
              <h2 class="text-xl font-bold">提交避坑排查工单</h2>
              <p class="text-xs text-zinc-400 mt-1">老L实验室站长团队将第一时间在实机沙盒中复现核实。</p>
            </div>

            <div class="space-y-3.5">
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-mono-tech text-zinc-400 mb-1">所属单机游戏</label>
                  <input type="text" id="feedback-game-id" readonly class="w-full bg-zinc-950/80 border border-zinc-800 rounded-xl px-3 py-2 text-xs text-purple-300 font-mono-tech">
                </div>
                <div>
                  <label class="block text-xs font-mono-tech text-zinc-400 mb-1">工单分类</label>
                  <select id="feedback-category" class="w-full bg-zinc-950/80 border border-zinc-800 rounded-xl px-3 py-2 text-xs text-white">
                    <option value="bug_report">代码/指令失效报错</option>
                    <option value="mod_request">急需某补丁/Mod一键包</option>
                    <option value="comment">避坑心得或修改建议</option>
                  </select>
                </div>
              </div>

              <div>
                <label class="block text-xs font-mono-tech text-zinc-400 mb-1">反馈详情与报错现象 (必填)</label>
                <textarea id="feedback-content" rows="4" placeholder="例如：最新 2.13 补丁更新后，输入此代码无反应，或某武器词条已失效..." class="w-full bg-zinc-950/80 border border-zinc-800 focus:border-purple-500 rounded-xl p-3 text-xs text-white placeholder-zinc-600 focus:outline-none"></textarea>
              </div>

              <!-- Bound Player Info Pill -->
              <div id="feedback-player-status-pill" class="p-2.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-xs text-purple-300 flex items-center justify-between">
                <span id="feedback-player-status-text">以单机玩家身份提交</span>
                <span class="text-[10px] font-mono text-zinc-400">将推送站长中台审核</span>
              </div>

              <button onclick="window.LModAuth.submitFeedbackForm()" id="feedback-submit-btn" class="w-full py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-bold rounded-xl text-xs transition shadow-lg shadow-purple-600/30">
                立即提交至老L中台排查
              </button>
            </div>
          </div>
        </div>
      `;

      document.body.appendChild(root);
      this.bindOtpBoxNavigation();
    },

    // -------------------------------------------------------------------------
    // OTP Box Auto-Focus, Backspace & Paste Routing
    // -------------------------------------------------------------------------
    bindOtpBoxNavigation: function () {
      const boxes = document.querySelectorAll('.otp-box');
      boxes.forEach((box, idx) => {
        box.addEventListener('input', (e) => {
          const val = box.value.replace(/\D/g, '');
          box.value = val ? val[0] : '';
          if (box.value && idx < boxes.length - 1) {
            boxes[idx + 1].focus();
            boxes[idx + 1].select();
          }
          if (Array.from(boxes).every(b => b.value.length === 1)) {
            // Auto trigger verification if all 6 filled
            this.handleVerifyOtpClick();
          }
        });

        box.addEventListener('keydown', (e) => {
          if (e.key === 'Backspace' && !box.value && idx > 0) {
            boxes[idx - 1].focus();
          } else if (e.key === 'Enter') {
            this.handleVerifyOtpClick();
          }
        });

        box.addEventListener('paste', (e) => {
          e.preventDefault();
          const paste = (e.clipboardData || window.clipboardData).getData('text');
          const digits = paste.replace(/\D/g, '').slice(0, 6);
          if (digits) {
            digits.split('').forEach((d, i) => {
              if (boxes[i]) boxes[i].value = d;
            });
            const nextIdx = Math.min(digits.length, boxes.length - 1);
            boxes[nextIdx].focus();
            if (digits.length === 6) {
              this.handleVerifyOtpClick();
            }
          }
        });
      });
    },

    getOtpBoxValue: function () {
      let code = '';
      document.querySelectorAll('.otp-box').forEach(b => {
        code += (b.value || '').trim();
      });
      return code;
    },

    clearOtpBoxes: function () {
      document.querySelectorAll('.otp-box').forEach(b => {
        b.value = '';
      });
    },

    // -------------------------------------------------------------------------
    // Form Action Handlers
    // -------------------------------------------------------------------------
    handleSendOtpClick: async function () {
      const emailInput = document.getElementById('auth-email-input');
      const sendBtn = document.getElementById('auth-btn-send-code');
      const email = (emailInput ? emailInput.value : '').trim().toLowerCase();

      if (!email || !email.includes('@')) {
        this.toast('请输入格式正确的邮箱地址');
        if (emailInput) emailInput.focus();
        return;
      }

      sendBtn.disabled = true;
      sendBtn.innerText = '发送中...';

      try {
        const res = await this.sendOtpCode(email, 'login');
        this.toast(res.message || '验证码已发送至您的邮箱');

        // Focus first OTP box
        const firstBox = document.querySelector('.otp-box[data-idx="0"]');
        if (firstBox) firstBox.focus();

        // Start 60s cooldown
        this.startOtpCooldown(res.data?.cooldown_seconds || 60);

      } catch (err) {
        this.toast(err.message);
        sendBtn.disabled = false;
        sendBtn.innerText = '获取验证码';
      }
    },

    startOtpCooldown: function (seconds) {
      const sendBtn = document.getElementById('auth-btn-send-code');
      if (!sendBtn) return;

      clearInterval(this.cooldownTimer);
      this.cooldownRemaining = seconds;
      sendBtn.disabled = true;

      this.cooldownTimer = setInterval(() => {
        this.cooldownRemaining--;
        if (this.cooldownRemaining <= 0) {
          clearInterval(this.cooldownTimer);
          sendBtn.disabled = false;
          sendBtn.innerText = '重新获取';
        } else {
          sendBtn.innerText = `${this.cooldownRemaining}s 后重发`;
        }
      }, 1000);
    },

    handleVerifyOtpClick: async function () {
      const emailInput = document.getElementById('auth-email-input');
      const email = (emailInput ? emailInput.value : '').trim().toLowerCase();
      const code = this.getOtpBoxValue();

      if (!email) {
        this.toast('请输入您的邮箱地址');
        return;
      }

      if (code.length !== 6) {
        this.toast('请输入完整的 6 位验证码');
        return;
      }

      const verifyBtn = document.getElementById('auth-btn-verify');
      if (verifyBtn) {
        verifyBtn.disabled = true;
        verifyBtn.innerText = '正在核验中...';
      }

      try {
        await this.verifyOtpCode(email, code, 'login');
      } catch (err) {
        this.toast(err.message);
      } finally {
        if (verifyBtn) {
          verifyBtn.disabled = false;
          verifyBtn.innerText = '🚀 验证并进入智库空间';
        }
      }
    },

    handleLoginSubmit: async function () {
      const email = (document.getElementById('auth-login-email')?.value || document.getElementById('auth-pwd-email-input')?.value || '').trim();
      const pwd = (document.getElementById('auth-login-pwd')?.value || document.getElementById('auth-pwd-input')?.value || '').trim();
      const autoRegister = Boolean(document.getElementById('auth-auto-register-check')?.checked);

      if (!this.isValidEmail(email)) {
        this.toast('请输入有效合规的正规电子邮箱（例如 yourname@qq.com、gamer@163.com、xxx@gmail.com）');
        const input = document.getElementById('auth-login-email') || document.getElementById('auth-pwd-email-input');
        if (input) input.focus();
        return;
      }

      if (!pwd || pwd.length < 6) {
        this.toast('密码长度至少需要 6 位字符');
        const input = document.getElementById('auth-login-pwd') || document.getElementById('auth-pwd-input');
        if (input) input.focus();
        return;
      }

      const btn = document.getElementById('auth-btn-login-submit') || document.getElementById('auth-btn-pwd-login');
      if (btn) {
        btn.disabled = true;
        btn.innerText = '登录验证中...';
      }

      try {
        const res = await this.apiFetch('/login-password', {
          method: 'POST',
          body: JSON.stringify({ email, password: pwd, auto_register: autoRegister })
        });

        if (res.code === 0 && res.data && res.data.token) {
          this.saveSession(res.data.token, res.data.user);
          this.toast(res.message || '✅ 登录成功，欢迎回到 L-MOD Vault！');
          this.closeAuthModal();
          this.syncProfile();
        }
      } catch (err) {
        this.toast(err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerText = '🔑 立即登录';
        }
      }
    },

    handlePasswordLoginClick: async function () {
      return this.handleLoginSubmit();
    },

    handleRegisterSubmit: async function () {
      const email = (document.getElementById('auth-reg-email')?.value || '').trim();
      const pwd = (document.getElementById('auth-reg-pwd')?.value || '').trim();
      const confirmPwd = (document.getElementById('auth-reg-confirm-pwd')?.value || '').trim();

      if (!this.isValidEmail(email)) {
        this.toast('请输入有效合规的正规电子邮箱（例如 yourname@qq.com、gamer@163.com、xxx@gmail.com）');
        const input = document.getElementById('auth-reg-email');
        if (input) input.focus();
        return;
      }

      if (!pwd || pwd.length < 6) {
        this.toast('注册密码长度至少需要 6 位字符');
        const input = document.getElementById('auth-reg-pwd');
        if (input) input.focus();
        return;
      }

      if (confirmPwd && pwd !== confirmPwd) {
        this.toast('两次输入的密码不一致，请仔细核对');
        const input = document.getElementById('auth-reg-confirm-pwd');
        if (input) input.focus();
        return;
      }

      const btn = document.getElementById('auth-btn-reg-submit');
      if (btn) {
        btn.disabled = true;
        btn.innerText = '账号创建中...';
      }

      try {
        const res = await this.apiFetch('/register-password', {
          method: 'POST',
          body: JSON.stringify({ email, password: pwd, confirm_password: confirmPwd })
        });

        if (res.code === 0 && res.data && res.data.token) {
          this.saveSession(res.data.token, res.data.user);
          this.toast(res.message || '🎉 恭喜！账号注册成功，已自动登录');
          this.closeAuthModal();
          this.syncProfile();
        }
      } catch (err) {
        this.toast(err.message);
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerText = '🚀 立即注册并进入智库';
        }
      }
    },

    handleWizardSetPassword: async function () {
      const pwd = (document.getElementById('wizard-pwd-input')?.value || '').trim();
      const confirm = (document.getElementById('wizard-pwd-confirm')?.value || '').trim();

      if (!pwd || pwd.length < 6) {
        this.toast('密码长度至少需要 6 个字符');
        return;
      }

      if (pwd !== confirm) {
        this.toast('两次输入的密码不一致，请重新核对');
        return;
      }

      try {
        await this.setPassword(pwd);
      } catch (err) {
        this.toast(err.message);
      }
    },

    handleSecurityChangePassword: async function () {
      const oldPwd = (document.getElementById('sec-old-pwd')?.value || '').trim();
      const newPwd = (document.getElementById('sec-new-pwd')?.value || '').trim();
      const confirmPwd = (document.getElementById('sec-confirm-pwd')?.value || '').trim();

      if (!newPwd || newPwd.length < 6) {
        this.toast('新密码至少需要 6 位字符');
        return;
      }

      if (newPwd !== confirmPwd) {
        this.toast('两次输入的新密码不一致');
        return;
      }

      try {
        await this.setPassword(newPwd, oldPwd);
      } catch (err) {
        this.toast(err.message);
      }
    },

    handleSendChangeEmailOtp: async function () {
      const emailInput = document.getElementById('sec-new-email');
      const btn = document.getElementById('sec-btn-send-email-code');
      const email = (emailInput ? emailInput.value : '').trim().toLowerCase();

      if (!email || !email.includes('@')) {
        this.toast('请输入有效的新邮箱地址');
        return;
      }

      btn.disabled = true;
      btn.innerText = '发送中...';

      try {
        const res = await this.sendOtpCode(email, 'change_email');
        this.toast(res.message || '验证码已发送至新邮箱');

        let cd = 60;
        clearInterval(this.changeEmailCooldownTimer);
        this.changeEmailCooldownTimer = setInterval(() => {
          cd--;
          if (cd <= 0) {
            clearInterval(this.changeEmailCooldownTimer);
            btn.disabled = false;
            btn.innerText = '发验证码';
          } else {
            btn.innerText = `${cd}s`;
          }
        }, 1000);

      } catch (err) {
        this.toast(err.message);
        btn.disabled = false;
        btn.innerText = '发验证码';
      }
    },

    handleSecurityChangeEmailSubmit: async function () {
      const newEmail = (document.getElementById('sec-new-email')?.value || '').trim().toLowerCase();
      const code = (document.getElementById('sec-email-code')?.value || '').trim();

      if (!newEmail || code.length !== 6) {
        this.toast('请输入完整的新邮箱与 6 位验证码');
        return;
      }

      try {
        await this.changeEmail(newEmail, code);
      } catch (err) {
        this.toast(err.message);
      }
    },

    // -------------------------------------------------------------------------
    // Community Feedback Modal Integration
    // -------------------------------------------------------------------------
    openFeedbackModal: function (gameId) {
      const modal = document.getElementById('community-feedback-modal');
      const gameInput = document.getElementById('feedback-game-id');
      const pillText = document.getElementById('feedback-player-status-text');

      if (gameInput) gameInput.value = gameId || (window.currentGame ? window.currentGame.id : 'global');
      if (pillText) {
        if (this.isLoggedIn()) {
          pillText.innerHTML = `已自动关联玩家: <span class="font-bold text-purple-300">${this.user.nickname}</span> (${this.user.email})`;
        } else {
          pillText.innerHTML = `当前未登录（将以匿名玩家身份提交，登录可追踪处理状态）`;
        }
      }

      if (modal) modal.classList.remove('hidden');
    },

    closeFeedbackModal: function () {
      const modal = document.getElementById('community-feedback-modal');
      if (modal) modal.classList.add('hidden');
    },

    submitFeedbackForm: async function () {
      const gameId = document.getElementById('feedback-game-id')?.value || null;
      const category = document.getElementById('feedback-category')?.value || 'bug_report';
      const content = (document.getElementById('feedback-content')?.value || '').trim();

      if (!content) {
        this.toast('请填写具体的报错反馈或建议描述');
        return;
      }

      const btn = document.getElementById('feedback-submit-btn');
      if (btn) {
        btn.disabled = true;
        btn.innerText = '正在提交至老L中台...';
      }

      try {
        const headers = { 'Content-Type': 'application/json' };
        if (this.token) {
          headers['Authorization'] = `Bearer ${this.token}`;
          headers['X-Player-Token'] = this.token;
        }

        const res = await fetch('/api/v1/community/feedback', {
          method: 'POST',
          headers,
          body: JSON.stringify({
            game_id: gameId,
            category,
            content,
            user_id: this.getUserId(),
            player_email: this.user ? this.user.email : null,
            player_nickname: this.user ? this.user.nickname : '单机玩家'
          })
        });

        const json = await res.json();
        if (json.code === 0) {
          this.toast('✅ 感谢反馈！工单已实时同步至站长中台排查。');
          this.closeFeedbackModal();
          const contentArea = document.getElementById('feedback-content');
          if (contentArea) contentArea.value = '';
        } else {
          this.toast(json.message || '提交失败');
        }
      } catch (err) {
        this.toast('网络提交异常，请重试');
      } finally {
        if (btn) {
          btn.disabled = false;
          btn.innerText = '立即提交至老L中台排查';
        }
      }
    },

    // -------------------------------------------------------------------------
    // Utilities
    // -------------------------------------------------------------------------
    togglePasswordVisibility: function (inputId, triggerElem) {
      const input = document.getElementById(inputId);
      if (!input) return;
      if (input.type === 'password') {
        input.type = 'text';
      } else {
        input.type = 'password';
      }
    },

    evalPasswordStrength: function (val, barId, textId) {
      const bar = document.getElementById(barId);
      const text = document.getElementById(textId);
      if (!bar || !text) return;

      if (!val) {
        bar.style.width = '0%';
        text.innerText = '强度: 未输入';
        return;
      }

      let score = 0;
      if (val.length >= 6) score += 1;
      if (val.length >= 10) score += 1;
      if (/[A-Z]/.test(val)) score += 1;
      if (/[0-9]/.test(val)) score += 1;
      if (/[^A-Za-z0-9]/.test(val)) score += 1;

      if (score <= 2) {
        bar.style.width = '33%';
        bar.className = 'h-full bg-red-500 transition-all duration-300';
        text.innerText = '强度: 弱';
        text.className = 'text-[10px] text-red-400 font-mono';
      } else if (score <= 4) {
        bar.style.width = '66%';
        bar.className = 'h-full bg-amber-500 transition-all duration-300';
        text.innerText = '强度: 中等';
        text.className = 'text-[10px] text-amber-400 font-mono';
      } else {
        bar.style.width = '100%';
        bar.className = 'h-full bg-emerald-500 transition-all duration-300';
        text.innerText = '强度: 极强 (安全推荐)';
        text.className = 'text-[10px] text-emerald-400 font-mono font-bold';
      }
    },

    bindGlobalEvents: function () {
      // Close popover when clicking outside
      document.addEventListener('click', (e) => {
        const wrap = document.getElementById('user-profile-menu-wrap');
        const popover = document.getElementById('user-profile-popover');
        if (wrap && popover && !wrap.contains(e.target)) {
          popover.classList.add('hidden');
        }
      });
    }
  };

  // Expose to window
  window.LModAuth = LModAuth;

  // Auto initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => LModAuth.init());
  } else {
    LModAuth.init();
  }

})(window);
