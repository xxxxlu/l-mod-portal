/**
 * L-MOD Vault - Stealth Admin Entrance & Quick Auth Overlay
 * Triggers:
 * 1. Hotkey: Ctrl + Shift + L (or Cmd + Shift + L on macOS)
 * 2. 5 Consecutive Clicks on Brand Logo within 3 seconds
 * 3. Secret trigger via window.LMOD_OPEN_ADMIN()
 */

(function (window) {
  'use strict';

  const TOKEN_KEY = 'lmod_admin_token';
  let clickCount = 0;
  let clickTimer = null;

  // 1. Create and inject modal dynamically when triggered
  function showStealthAuthModal() {
    // If already authenticated with valid token, navigate directly to /admin.html
    const existingToken = localStorage.getItem(TOKEN_KEY);
    if (existingToken) {
      window.location.href = '/admin.html';
      return;
    }

    if (document.getElementById('lmod-stealth-modal')) {
      document.getElementById('lmod-stealth-modal').classList.remove('hidden');
      document.getElementById('lmod-stealth-passkey').focus();
      return;
    }

    const modal = document.createElement('div');
    modal.id = 'lmod-stealth-modal';
    modal.className = 'fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-black/85 backdrop-blur-xl animate-fade-in font-sans';
    modal.innerHTML = `
      <div class="w-full max-w-md rounded-2xl bg-[#0d0f15]/95 border border-purple-500/30 p-6 shadow-2xl relative text-slate-200">
        <!-- Close button -->
        <button id="lmod-stealth-close" class="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-lg">
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>

        <div class="flex items-center gap-3 mb-4">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-indigo-700 flex items-center justify-center text-white shadow-lg shadow-purple-600/30 font-bold">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          </div>
          <div>
            <h3 class="text-sm font-bold text-white tracking-wide">站长特权认证通道</h3>
            <p class="text-[11px] text-purple-400 font-mono">Zero Trust Admin Gateway · L-MOD</p>
          </div>
        </div>

        <p class="text-xs text-slate-400 mb-3.5 leading-relaxed">
          检测到站长隐蔽交互指令，请输入站长账号与专属密码以签发特权凭据（7天免登）：
        </p>

        <form id="lmod-stealth-form" class="space-y-3">
          <div>
            <label class="block text-[11px] font-mono text-slate-400 mb-1">站长账号 (默认: admin)</label>
            <input 
              id="lmod-stealth-user" 
              type="text" 
              value="admin"
              placeholder="输入站长账号" 
              class="w-full bg-slate-950/90 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 font-mono"
              autocomplete="username"
              required
            >
          </div>

          <div>
            <label class="block text-[11px] font-mono text-slate-400 mb-1">站长密码 (初始默认: lmod2026!)</label>
            <input 
              id="lmod-stealth-passkey" 
              type="password" 
              placeholder="输入站长登录密码" 
              class="w-full bg-slate-950/90 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 font-mono"
              autocomplete="current-password"
              required
            >
          </div>

          <div id="lmod-stealth-error" class="hidden p-2 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-mono">
            账号或密码错误，特权通道拒绝访问
          </div>

          <button 
            type="submit" 
            id="lmod-stealth-submit"
            class="w-full py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white text-xs font-semibold shadow-lg shadow-purple-600/30 transition flex items-center justify-center gap-2 mt-1"
          >
            <span>验证凭据并进入管理中台</span>
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </form>
            <span>验证凭据并进入管理中台</span>
            <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
          </button>
        </form>

        <div class="mt-4 pt-3 border-t border-slate-800 text-center">
          <a href="/admin.html" class="text-[11px] text-slate-500 hover:text-purple-400 transition font-mono">
            直接访问专属管理入口 (/admin) →
          </a>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('lmod-stealth-close').addEventListener('click', () => {
      modal.classList.add('hidden');
    });

    document.getElementById('lmod-stealth-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      const errBox = document.getElementById('lmod-stealth-error');
      const submitBtn = document.getElementById('lmod-stealth-submit');
      const username = (document.getElementById('lmod-stealth-user')?.value || 'admin').trim();
      const passkey = document.getElementById('lmod-stealth-passkey').value.trim();

      errBox.classList.add('hidden');
      submitBtn.disabled = true;
      submitBtn.textContent = '正在核验站长特权凭据...';

      try {
        const res = await fetch('/api/v1/admin/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password: passkey })
        });
        const json = await res.json();

        if (res.ok && json.code === 0 && json.data.token) {
          localStorage.setItem(TOKEN_KEY, json.data.token);
          submitBtn.textContent = '认证成功！正在接入控制中台...';
          setTimeout(() => {
            window.location.href = '/admin.html';
          }, 400);
        } else {
          errBox.classList.remove('hidden');
          errBox.textContent = json.message || '通行口令错误';
          submitBtn.disabled = false;
          submitBtn.innerHTML = `<span>验证凭据并进入管理中台</span>`;
        }
      } catch (err) {
        errBox.classList.remove('hidden');
        errBox.textContent = '鉴权请求异常: ' + err.message;
        submitBtn.disabled = false;
        submitBtn.innerHTML = `<span>验证凭据并进入管理中台</span>`;
      }
    });

    document.getElementById('lmod-stealth-passkey').focus();
  }

  // 2. Hotkey Listener: Ctrl + Shift + L or Cmd + Shift + L
  window.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'L' || e.key === 'l')) {
      e.preventDefault();
      showStealthAuthModal();
    }
  });

  // 3. Multi-click listener on brand logo
  function registerLogoClickListener() {
    const logoSelectors = ['#lmod-brand-logo', 'aside a[href="#/"]', '.brand-logo', 'header a[href="/"]', 'header a[href="#/"]'];
    let logoEl = null;

    for (const sel of logoSelectors) {
      const el = document.querySelector(sel);
      if (el) {
        logoEl = el;
        break;
      }
    }

    if (logoEl) {
      logoEl.addEventListener('click', function (e) {
        clickCount++;
        clearTimeout(clickTimer);
        clickTimer = setTimeout(() => {
          clickCount = 0;
        }, 3000);

        if (clickCount >= 5) {
          e.preventDefault();
          clickCount = 0;
          showStealthAuthModal();
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', registerLogoClickListener);
  } else {
    registerLogoClickListener();
  }

  // Expose global trigger
  window.LMOD_OPEN_ADMIN = showStealthAuthModal;

  // 4. Global Emergency Broadcast Renderer
  function initEmergencyBroadcastCheck() {
    fetch('/api/v1/radar/overview')
      .then(function (res) { return res.json(); })
      .then(function (json) {
        if (json && json.data && json.data.emergency_broadcast && json.data.emergency_broadcast.enabled) {
          renderEmergencyBanner(json.data.emergency_broadcast);
        }
      })
      .catch(function () {});
  }

  function renderEmergencyBanner(broadcast) {
    if (document.getElementById('lmod-emergency-banner')) return;
    const isDismissed = sessionStorage.getItem('lmod_emergency_dismissed_' + broadcast.updated_at);
    if (isDismissed) return;

    const banner = document.createElement('div');
    banner.id = 'lmod-emergency-banner';
    const isRed = broadcast.level === 'red';
    
    banner.className = 'fixed top-0 left-0 right-0 z-[100] transform -translate-y-full transition-transform duration-500 ease-out font-sans';
    banner.innerHTML = `
      <div class="${isRed ? 'bg-gradient-to-r from-red-950 via-rose-900 to-red-950 border-rose-500/50 text-rose-100' : 'bg-gradient-to-r from-amber-950 via-yellow-900 to-amber-950 border-amber-500/50 text-amber-100'} backdrop-blur-xl border-b px-4 py-2.5 shadow-2xl">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-3 text-xs sm:text-sm">
          <div class="flex items-center space-x-2.5 min-w-0">
            <span class="w-6 h-6 rounded-full ${isRed ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'} flex items-center justify-center shrink-0 animate-pulse text-xs font-bold">
              ${isRed ? '🚨' : '⚠️'}
            </span>
            <div class="truncate">
              <span class="font-extrabold ${isRed ? 'text-white' : 'text-amber-200'}">【${broadcast.title || '站长紧急熔断广播'}】</span>
              <span class="opacity-95 font-medium">${broadcast.message}</span>
            </div>
          </div>
          <button id="lmod-dismiss-emergency" class="p-1 rounded-full hover:bg-white/10 text-white/80 hover:text-white transition" title="关闭广播">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
      </div>
    `;

    document.body.prepend(banner);

    requestAnimationFrame(function () {
      banner.classList.remove('-translate-y-full');
      banner.classList.add('translate-y-0');
    });

    document.getElementById('lmod-dismiss-emergency').addEventListener('click', function () {
      banner.classList.remove('translate-y-0');
      banner.classList.add('-translate-y-full');
      sessionStorage.setItem('lmod_emergency_dismissed_' + broadcast.updated_at, '1');
      setTimeout(function () { banner.remove(); }, 500);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initEmergencyBroadcastCheck);
  } else {
    initEmergencyBroadcastCheck();
  }

})(window);
