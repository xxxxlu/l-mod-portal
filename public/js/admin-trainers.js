/**
 * Admin「修改器包」tab: upload FLiNG trainer packages into Workers KV (via /api/v1/admin/trainers/*),
 * list / replace / withdraw them, show KV usage against the 1 GB free quota.
 *
 * Upload flow (keeps every request inside the free plan's 10 ms CPU budget):
 *   1. SHA-256 is computed here with crypto.subtle (the server never hashes);
 *   2. POST /init with the metadata → { id, chunks, chunkSize };
 *   3. PUT /:id/chunk/:n for each slice (streamed straight into KV);
 *   4. POST /:id/commit → active (a previous active package for the game is withdrawn and deleted).
 * Loaded by admin.html as a separate file so the tab stays independent of the main admin script.
 */
(function () {
  'use strict';

  const API = '/api/v1/admin/trainers';
  const TOKEN_KEY = 'lmod_admin_token';
  const GB = 1024 * 1024 * 1024;

  const $ = id => document.getElementById(id);
  const state = {
    fling: {},        // trainers.json games: id → entry
    packages: [],
    storage: null,
    file: null,       // { file, sha256 }
    hashing: false,
    busy: false,
    autofill: { version: '', page: '' }
  };

  function esc(v) {
    return String(v == null ? '' : v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  function fmtBytes(n) {
    n = Number(n) || 0;
    if (n >= GB) return (n / GB).toFixed(2) + ' GB';
    if (n >= 1048576) return (n / 1048576).toFixed(1) + ' MB';
    if (n >= 1024) return (n / 1024).toFixed(1) + ' KB';
    return n + ' B';
  }

  function fmtTime(iso) {
    return iso ? String(iso).replace('T', ' ').replace(/:\d\d(\.\d+)?Z$/, '') : '--';
  }

  function token() {
    try { return localStorage.getItem(TOKEN_KEY) || ''; } catch (e) { return ''; }
  }

  function toast(message, type) {
    const box = $('toast-container');
    if (!box) return;
    const colors = {
      success: 'bg-emerald-950/90 border-emerald-500/40 text-emerald-300',
      error: 'bg-rose-950/90 border-rose-500/40 text-rose-300',
      info: 'bg-purple-950/90 border-purple-500/40 text-purple-300'
    };
    const el = document.createElement('div');
    el.className = `p-3 rounded-xl border text-xs font-mono shadow-2xl backdrop-blur-md pointer-events-auto ${colors[type] || colors.info}`;
    el.textContent = message;
    box.appendChild(el);
    setTimeout(() => el.remove(), 4000);
  }

  function copy(text, label) {
    const done = () => toast(`已复制${label}`, 'success');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, () => fallbackCopy(text, done));
    } else {
      fallbackCopy(text, done);
    }
  }

  function fallbackCopy(text, done) {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) { toast('复制失败，请手动复制', 'error'); }
    ta.remove();
  }

  async function call(path, options = {}) {
    const res = await fetch(API + path, {
      ...options,
      headers: { Authorization: `Bearer ${token()}`, ...(options.headers || {}) }
    });
    if (res.status === 401 || res.status === 403) throw new Error('站长会话已过期，请刷新页面重新登录');
    let body;
    try { body = await res.json(); } catch (e) { throw new Error(`接口返回 ${res.status}`); }
    body.httpStatus = res.status;
    return body;
  }

  // ---------------------------------------------------------------- data

  async function loadFling() {
    if (Object.keys(state.fling).length) return;
    const res = await fetch('/trainers.json', { cache: 'no-cache' });
    const json = await res.json();
    state.fling = json.games || {};
    const select = $('tp-game-select');
    const entries = Object.entries(state.fling)
      .filter(([, g]) => g && g.url)
      .sort((a, b) => String(a[1].title || a[0]).localeCompare(String(b[1].title || b[0])));
    select.innerHTML = '<option value="">选择游戏…</option>' + entries.map(([id, g]) =>
      `<option value="${esc(id)}">${esc((g.title || id).replace(/\s*Trainer$/i, ''))}${g.antiCheat ? '（反作弊）' : ''} · ${esc(id)}</option>`
    ).join('');
  }

  async function loadPackages() {
    const res = await call('');
    if (res.code !== 0) throw new Error(res.message || '读取列表失败');
    state.storage = res.data.storage;
    state.packages = res.data.packages || [];
  }

  async function refresh() {
    try {
      await Promise.all([loadFling(), loadPackages()]);
    } catch (err) {
      toast(err.message, 'error');
    }
    renderStorage();
    renderTable();
    renderGameInfo();
    syncUploadButton();
  }

  // ---------------------------------------------------------------- render

  function renderStorage() {
    const s = state.storage;
    const chip = $('tp-storage-chip');
    const off = $('tp-storage-off');
    if (!s) {
      chip.textContent = '读取失败';
      return;
    }
    const used = Number(s.usedBytes) || 0;
    const quota = Number(s.quotaBytes) || GB;
    const pct = Math.min(100, (used / quota) * 100);
    $('tp-storage-text').textContent = `${fmtBytes(used)} / ${fmtBytes(quota)}`;
    $('tp-storage-bar').style.width = `${pct.toFixed(1)}%`;
    $('tp-storage-bar').className = `h-full transition-all ${pct > 90 ? 'bg-rose-500' : pct > 70 ? 'bg-amber-500' : 'bg-purple-500'}`;
    $('tp-active-count').textContent = `上架 ${s.activeCount || 0} 个`;

    if (!s.enabled) {
      chip.className = 'text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono';
      chip.textContent = '存储未开通';
      off.classList.remove('hidden');
      off.innerHTML = '存储未开通：这个站点还没有绑定名为 <code>TRAINER_FILES</code> 的 Workers KV，暂时不能上传。'
        + '前台不受影响，修改器区照常只显示「去风灵月影官网」。';
    } else if (!s.tableReady) {
      chip.className = 'text-xs px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 font-mono';
      chip.textContent = '数据表未建';
      off.classList.remove('hidden');
      off.innerHTML = 'KV 已绑定，但 D1 里还没有 <code>trainer_packages</code> 表（<code>database/migration_v7_trainer_packages.sql</code> 未执行）。';
    } else {
      chip.className = 'text-xs px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-mono';
      chip.textContent = '存储已开通';
      off.classList.add('hidden');
    }
  }

  function statusChip(status) {
    if (status === 'active') return '<span class="px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300">已上架</span>';
    if (status === 'uploading') return '<span class="px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300">上传未完成</span>';
    return '<span class="px-2 py-0.5 rounded-full bg-slate-700/50 text-slate-400">已下架</span>';
  }

  function renderTable() {
    const tbody = $('tp-tbody');
    if (!state.packages.length) {
      tbody.innerHTML = '<tr><td colspan="8" class="py-8 text-center text-slate-500 font-mono">还没有上传过修改器包</td></tr>';
      return;
    }
    tbody.innerHTML = state.packages.map(p => {
      const dim = p.status === 'withdrawn' ? ' opacity-50' : '';
      const title = state.fling[p.game_id] ? String(state.fling[p.game_id].title || p.game_id).replace(/\s*Trainer$/i, '') : p.game_id;
      let actions = '';
      if (p.status === 'active') {
        actions = `
          <button data-act="copy-link" data-id="${esc(p.id)}" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200">复制下载链接</button>
          <button data-act="replace" data-id="${esc(p.id)}" class="px-2 py-1 rounded-lg bg-purple-500/15 hover:bg-purple-500/25 text-purple-200">替换</button>
          <button data-act="withdraw" data-id="${esc(p.id)}" class="px-2 py-1 rounded-lg bg-rose-500/15 hover:bg-rose-500/25 text-rose-300">下架</button>`;
      } else if (p.status === 'uploading') {
        actions = `<button data-act="withdraw" data-id="${esc(p.id)}" class="px-2 py-1 rounded-lg bg-rose-500/15 hover:bg-rose-500/25 text-rose-300">丢弃</button>`;
      }
      return `
        <tr class="hover:bg-slate-800/30${dim}">
          <td class="py-3 px-4"><div class="text-slate-100">${esc(title)}</div><div class="text-[11px] text-slate-500 font-mono">${esc(p.game_id)}</div></td>
          <td class="py-3 px-4 font-mono text-slate-300 break-all max-w-[220px]">${esc(p.file_name)}${p.note ? `<div class="text-[11px] text-slate-500 font-sans">${esc(p.note)}</div>` : ''}</td>
          <td class="py-3 px-4 font-mono text-slate-300">${esc(p.trainer_version || '--')}${p.game_version ? `<div class="text-[11px] text-slate-500">游戏 ${esc(p.game_version)}</div>` : ''}</td>
          <td class="py-3 px-4 font-mono text-right text-slate-300 whitespace-nowrap">${fmtBytes(p.size)}<div class="text-[11px] text-slate-500">${esc(p.chunks)} 片</div></td>
          <td class="py-3 px-4 font-mono"><button data-act="copy-sha" data-id="${esc(p.id)}" title="${esc(p.sha256)}" class="text-purple-300 hover:text-purple-200">${esc(String(p.sha256).slice(0, 12))}…</button></td>
          <td class="py-3 px-4 whitespace-nowrap">${statusChip(p.status)}</td>
          <td class="py-3 px-4 font-mono text-slate-400 whitespace-nowrap">${esc(fmtTime(p.uploaded_at))}</td>
          <td class="py-3 px-4 text-right whitespace-nowrap space-x-1">${actions}</td>
        </tr>`;
    }).join('');
  }

  function activeFor(gameId) {
    return state.packages.find(p => p.game_id === gameId && p.status === 'active') || null;
  }

  function renderGameInfo() {
    const gameId = $('tp-game-select').value;
    const box = $('tp-game-info');
    const g = state.fling[gameId];
    if (!gameId || !g) {
      box.classList.add('hidden');
      return;
    }
    const active = activeFor(gameId);
    box.classList.remove('hidden');
    box.innerHTML = `
      <div>官网页面：<a href="${esc(g.url)}" target="_blank" rel="noopener noreferrer" class="text-purple-300 hover:underline break-all">${esc(g.url)}</a></div>
      <div>适配版本：${esc(g.gameVersion || '--')} · 功能 ${esc(g.optionsCount || '?')} 项</div>
      <div>官网更新：${esc(g.lastUpdated || '--')}</div>
      ${g.antiCheat ? '<div class="text-rose-300 font-sans font-semibold">这款游戏带反作弊，前台不提供本站下载，这里也不允许上传。</div>' : ''}
      ${active ? `<div class="text-amber-300 font-sans">当前已上架：${esc(active.file_name)}（${esc(active.trainer_version || '--')} · ${fmtBytes(active.size)}）。上传新文件会替换它，旧文件下架并删除。</div>` : '<div class="text-slate-500 font-sans">这款游戏还没有本站包。</div>'}`;
  }

  function syncUploadButton() {
    const s = state.storage;
    const gameId = $('tp-game-select').value;
    const g = state.fling[gameId];
    const ready = Boolean(s && s.enabled && s.tableReady && g && !g.antiCheat && state.file && state.file.sha256);
    $('tp-upload-btn').disabled = !ready || state.busy || state.hashing;
    $('tp-upload-btn').textContent = activeFor(gameId) ? '上传并替换' : '上传并上架';
  }

  function setStatus(text, tone) {
    const el = $('tp-upload-status');
    el.textContent = text || '';
    el.className = `text-xs font-mono mt-1 ${tone === 'error' ? 'text-rose-300' : tone === 'ok' ? 'text-emerald-300' : 'text-slate-400'}`;
  }

  function setProgress(fraction) {
    const wrap = $('tp-progress-wrap');
    if (fraction == null) { wrap.classList.add('hidden'); return; }
    wrap.classList.remove('hidden');
    $('tp-progress-bar').style.width = `${Math.max(0, Math.min(100, fraction * 100)).toFixed(1)}%`;
  }

  // ---------------------------------------------------------------- form

  function onGameChange() {
    const g = state.fling[$('tp-game-select').value];
    const versionInput = $('tp-trainer-version');
    const pageInput = $('tp-page-url');
    // Prefill from trainers.json, but never overwrite something typed by hand.
    if (g) {
      if (!versionInput.value || versionInput.value === state.autofill.version) {
        versionInput.value = g.gameVersion || '';
        state.autofill.version = versionInput.value;
      }
      if (!pageInput.value || pageInput.value === state.autofill.page) {
        pageInput.value = g.url || '';
        state.autofill.page = pageInput.value;
      }
    }
    renderGameInfo();
    syncUploadButton();
  }

  async function sha256Hex(file) {
    const digest = await crypto.subtle.digest('SHA-256', await file.arrayBuffer());
    return Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2, '0')).join('');
  }

  async function onFileChange() {
    const input = $('tp-file-input');
    const info = $('tp-file-info');
    const file = input.files && input.files[0];
    state.file = null;
    syncUploadButton();
    if (!file) { info.classList.add('hidden'); return; }

    const ext = (/\.[^.]+$/.exec(file.name.toLowerCase()) || [''])[0];
    const allowed = (state.storage && state.storage.allowedExtensions) || ['.zip', '.exe', '.rar', '.7z'];
    const max = (state.storage && state.storage.maxFileBytes) || 95 * 1048576;
    info.classList.remove('hidden');
    if (!allowed.includes(ext)) {
      info.innerHTML = `<span class="text-rose-300">只接受 ${esc(allowed.join(' / '))}</span>`;
      return;
    }
    if (file.size > max) {
      info.innerHTML = `<span class="text-rose-300">${fmtBytes(file.size)}，超过 ${fmtBytes(max)} 上限</span>`;
      return;
    }
    if (!window.crypto || !crypto.subtle) {
      info.innerHTML = '<span class="text-rose-300">浏览器不支持 crypto.subtle（需要 https），没法算 SHA-256</span>';
      return;
    }

    state.hashing = true;
    syncUploadButton();
    info.innerHTML = `${esc(file.name)} · ${fmtBytes(file.size)}<div class="text-slate-500">正在本地计算 SHA-256…</div>`;
    try {
      const sha256 = await sha256Hex(file);
      const current = input.files && input.files[0];
      if (!current || current.name !== file.name || current.size !== file.size || current.lastModified !== file.lastModified) {
        return; // a different file was picked meanwhile; its own change handler takes over
      }
      state.file = { file, sha256 };
      const chunkBytes = (state.storage && state.storage.chunkBytes) || 24 * 1048576;
      info.innerHTML = `${esc(file.name)} · ${fmtBytes(file.size)} · 分 ${Math.max(1, Math.ceil(file.size / chunkBytes))} 片
        <div>SHA-256：<span class="text-purple-300">${esc(sha256)}</span></div>`;
    } catch (err) {
      info.innerHTML = `<span class="text-rose-300">计算 SHA-256 失败：${esc(err.message)}</span>`;
    } finally {
      state.hashing = false;
      syncUploadButton();
    }
  }

  function putChunk(id, n, blob, onProgress) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest();
      xhr.open('PUT', `${API}/${encodeURIComponent(id)}/chunk/${n}`);
      xhr.setRequestHeader('Authorization', `Bearer ${token()}`);
      xhr.setRequestHeader('Content-Type', 'application/octet-stream');
      xhr.upload.onprogress = e => { if (e.lengthComputable) onProgress(e.loaded); };
      xhr.onload = () => {
        let body = {};
        try { body = JSON.parse(xhr.responseText); } catch (e) { /* keep empty */ }
        if (xhr.status >= 200 && xhr.status < 300 && body.code === 0) resolve(body);
        else reject(new Error(body.message || `分片 ${n} 上传失败（HTTP ${xhr.status}）`));
      };
      xhr.onerror = () => reject(new Error(`分片 ${n} 上传失败（网络错误）`));
      xhr.send(blob);
    });
  }

  const sleep = ms => new Promise(r => setTimeout(r, ms));

  async function commitWithRetry(id) {
    for (let attempt = 1; ; attempt++) {
      const res = await call(`/${encodeURIComponent(id)}/commit`, { method: 'POST' });
      if (res.code === 0) return res;
      const missing = res.data && res.data.missing && res.data.missing.length;
      if (!missing || attempt >= 3) throw new Error(res.message || '提交上架失败');
      setStatus(`${res.message}（${attempt}/3，2 秒后重试）`);
      await sleep(2000);
    }
  }

  async function upload() {
    const gameId = $('tp-game-select').value;
    const g = state.fling[gameId];
    if (!g || g.antiCheat || !state.file || state.busy) return;
    const { file, sha256 } = state.file;
    const active = activeFor(gameId);
    if (active && !confirm(`《${(g.title || gameId).replace(/\s*Trainer$/i, '')}》已有上架包 ${active.file_name}。\n上传后会替换它，旧文件下架并从 KV 删除。继续？`)) return;

    state.busy = true;
    syncUploadButton();
    setProgress(0);
    setStatus('登记上传…');
    let id = null;
    try {
      const init = await call('/init', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          game_id: gameId,
          file_name: file.name,
          size: file.size,
          sha256,
          trainer_version: $('tp-trainer-version').value,
          game_version: $('tp-game-version').value,
          fling_page_url: $('tp-page-url').value,
          note: $('tp-note').value
        })
      });
      if (init.code !== 0) throw new Error(init.message || '登记失败');
      id = init.data.id;
      const { chunks, chunkSize } = init.data;

      for (let n = 0; n < chunks; n++) {
        const start = n * chunkSize;
        const blob = file.slice(start, Math.min(file.size, start + chunkSize));
        setStatus(`上传分片 ${n + 1}/${chunks}…`);
        await putChunk(id, n, blob, loaded => setProgress((start + loaded) / file.size));
      }
      setProgress(1);
      setStatus('校验分片并上架…');
      const done = await commitWithRetry(id);
      setStatus(done.message || '已上架', 'ok');
      toast(`${done.message}：${file.name}`, 'success');
      $('tp-file-input').value = '';
      $('tp-file-info').classList.add('hidden');
      $('tp-note').value = '';
      state.file = null;
    } catch (err) {
      setStatus(err.message, 'error');
      toast(err.message, 'error');
      if (id) {
        // Free whatever chunks made it into KV; the row stays as a withdrawn record.
        try { await call(`/${encodeURIComponent(id)}/withdraw`, { method: 'POST' }); } catch (e) { /* listed as 上传未完成 */ }
      }
    } finally {
      state.busy = false;
      setTimeout(() => setProgress(null), 1500);
      await refresh();
    }
  }

  async function withdraw(p) {
    const label = p.status === 'uploading' ? '丢弃这次未完成的上传' : `下架 ${p.file_name}`;
    if (!confirm(`${label}？\n文件会从 KV 删除，要恢复只能重新上传。`)) return;
    try {
      const res = await call(`/${encodeURIComponent(p.id)}/withdraw`, { method: 'POST' });
      if (res.code !== 0) throw new Error(res.message || '下架失败');
      toast(res.message, 'success');
    } catch (err) {
      toast(err.message, 'error');
    }
    await refresh();
  }

  function onTableClick(e) {
    const btn = e.target.closest('button[data-act]');
    if (!btn) return;
    const p = state.packages.find(x => x.id === btn.dataset.id);
    if (!p) return;
    const act = btn.dataset.act;
    if (act === 'copy-link' && p.download_path) copy(location.origin + p.download_path, '下载链接');
    else if (act === 'copy-sha') copy(p.sha256, '完整 SHA-256');
    else if (act === 'withdraw') withdraw(p);
    else if (act === 'replace') {
      $('tp-game-select').value = p.game_id;
      onGameChange();
      $('tp-upload-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
      $('tp-file-input').focus();
    }
  }

  function init() {
    const tab = document.querySelector('.nav-tab[data-tab="trainers"]');
    if (!tab || !$('panel-trainers')) return;
    tab.addEventListener('click', refresh);
    $('tp-refresh-btn').addEventListener('click', refresh);
    $('tp-game-select').addEventListener('change', onGameChange);
    $('tp-file-input').addEventListener('change', onFileChange);
    $('tp-upload-btn').addEventListener('click', upload);
    $('tp-tbody').addEventListener('click', onTableClick);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
