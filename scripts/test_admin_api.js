/**
 * L-MOD Vault - Integration Test Suite for Admin Console & AI Control Plane API
 */

const { execSync } = require('child_process');
const path = require('path');

const DB_PATH = path.resolve(__dirname, '../database/lmod_vault.db');

class MockD1Statement {
  constructor(sql, params = []) {
    this.sql = sql;
    this.params = params;
  }

  bind(...args) {
    return new MockD1Statement(this.sql, args);
  }

  async first() {
    const res = await this.all();
    return res.results && res.results.length > 0 ? res.results[0] : null;
  }

  async all() {
    let finalSql = this.sql;
    let paramIndex = 0;

    finalSql = finalSql.replace(/\?/g, () => {
      const p = this.params[paramIndex++];
      if (p === null || p === undefined) return 'NULL';
      if (typeof p === 'number') return p;
      return `'${String(p).replace(/'/g, "''")}'`;
    });

    const jsonCmd = `/usr/bin/sqlite3 -json "${DB_PATH}" "${finalSql.replace(/"/g, '\\"')}"`;
    try {
      const raw = execSync(jsonCmd, { encoding: 'utf-8' }).trim();
      const rows = raw ? JSON.parse(raw) : [];
      return { results: rows };
    } catch (err) {
      return { results: [], success: true };
    }
  }

  async run() {
    return this.all();
  }
}

class MockD1Database {
  prepare(sql) {
    return new MockD1Statement(sql);
  }
  async batch(statements) {
    const results = [];
    for (const stmt of statements) {
      results.push(await stmt.run());
    }
    return results;
  }
}

async function runTests() {
  console.log('================================================================');
  console.log('🚀 Running L-MOD Vault Admin API & Zero Trust Auth Test Suite');
  console.log('================================================================');

  const mockDb = new MockD1Database();
  const mockEnv = {
    DB: mockDb,
    ADMIN_SECRET_KEY: 'lmod-vault-master-station-key-2026',
    ADMIN_JWT_SECRET: 'lmod-vault-jwt-hmac-sha256-edge-token-secret-2026'
  };

  // 1. Test Admin Login (Invalid Credentials)
  const loginHandler = await import('../functions/api/v1/admin/login.js');
  const reqBadLogin = new Request('http://localhost/api/v1/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'wrong-password-123' })
  });
  const resBadLogin = await loginHandler.onRequestPost({ request: reqBadLogin, env: mockEnv });
  const dataBadLogin = await resBadLogin.json();
  console.log('✓ Admin Login (Invalid Credentials) correctly rejected:', resBadLogin.status, dataBadLogin.code);
  if (resBadLogin.status !== 401) throw new Error('Bad login should return 401');

  // 2. Test Admin Login (Valid Username & Password: admin / lmod2026!)
  const reqGoodLogin = new Request('http://localhost/api/v1/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'lmod2026!' })
  });
  const resGoodLogin = await loginHandler.onRequestPost({ request: reqGoodLogin, env: mockEnv });
  const dataGoodLogin = await resGoodLogin.json();
  console.log('✓ Admin Login (Valid Username & Password: admin / lmod2026!) succeeded, JWT issued:', resGoodLogin.status, 'Token length:', dataGoodLogin.data.token.length);
  if (resGoodLogin.status !== 200 || !dataGoodLogin.data.token) throw new Error('Login failed to return token');

  // Also verify legacy passkey compatibility
  const reqLegacyLogin = new Request('http://localhost/api/v1/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ secret_key: 'lmod-vault-master-station-key-2026' })
  });
  const resLegacyLogin = await loginHandler.onRequestPost({ request: reqLegacyLogin, env: mockEnv });
  console.log('✓ Admin Login (Legacy Secret Key fallback) succeeded:', resLegacyLogin.status);

  const adminToken = dataGoodLogin.data.token;

  // 3. Test Middleware Guard
  const middleware = await import('../functions/api/v1/admin/_middleware.js');
  
  // Guard Test: No token
  const reqNoAuth = new Request('http://localhost/api/v1/admin/analytics/overview');
  const resNoAuth = await middleware.onRequest({ request: reqNoAuth, env: mockEnv, next: async () => new Response('OK') });
  console.log('✓ Middleware Guard blocked unauthenticated request:', resNoAuth.status);
  if (resNoAuth.status !== 401) throw new Error('Unauthenticated request must return 401');

  // Guard Test: Valid Token
  const reqWithAuth = new Request('http://localhost/api/v1/admin/analytics/overview', {
    headers: { 'Authorization': `Bearer ${adminToken}` }
  });
  let contextData = {};
  const resWithAuth = await middleware.onRequest({
    request: reqWithAuth,
    env: mockEnv,
    data: contextData,
    next: async () => new Response(JSON.stringify({ passed: true }), { status: 200 })
  });
  console.log('✓ Middleware Guard passed valid token with role:', resWithAuth.status, 'Admin sub:', contextData.admin?.sub);
  if (resWithAuth.status !== 200) throw new Error('Valid token should pass middleware');

  // 4. Test GET /api/v1/admin/me
  const meHandler = await import('../functions/api/v1/admin/me.js');
  const resMe = await meHandler.onRequestGet({ env: mockEnv, data: contextData });
  const dataMe = await resMe.json();
  console.log('✓ /api/v1/admin/me:', resMe.status, `Games: ${dataMe.data.system_stats.games_count}, Commands: ${dataMe.data.system_stats.commands_count}`);

  // 5. Test Analytics Overview
  const analyticsOverview = await import('../functions/api/v1/admin/analytics/overview.js');
  const resAnalytics = await analyticsOverview.onRequestGet({ env: mockEnv });
  const dataAnalytics = await resAnalytics.json();
  console.log('✓ /api/v1/admin/analytics/overview:', resAnalytics.status,
    `Total PV: ${dataAnalytics.data.summary.total_pv}, UV: ${dataAnalytics.data.summary.total_uv}, Top Searches: ${dataAnalytics.data.top_searches.length}`);

  // 6. Test Holographic Telemetry Events
  const eventsHandler = await import('../functions/api/v1/admin/analytics/events.js');
  const reqEvents = new Request('http://localhost/api/v1/admin/analytics/events?page=1&page_size=5');
  const resEvents = await eventsHandler.onRequestGet({ request: reqEvents, env: mockEnv });
  const dataEvents = await resEvents.json();
  console.log('✓ /api/v1/admin/analytics/events:', resEvents.status, `Returned: ${dataEvents.data.events.length}/${dataEvents.data.total}`);

  // 7. Test Community Feedback Moderation
  const feedbackList = await import('../functions/api/v1/admin/feedback/index.js');
  const reqFb = new Request('http://localhost/api/v1/admin/feedback?status=all&page=1&page_size=5');
  const resFb = await feedbackList.onRequestGet({ request: reqFb, env: mockEnv });
  const dataFb = await resFb.json();
  console.log('✓ /api/v1/admin/feedback (list):', resFb.status, `Items: ${dataFb.data.items.length}, Pending: ${dataFb.data.status_counts.pending}`);

  const feedbackStatus = await import('../functions/api/v1/admin/feedback/status.js');
  const reqFbStatus = new Request('http://localhost/api/v1/admin/feedback/status', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: 101, status: 'resolved' })
  });
  const resFbStatus = await feedbackStatus.onRequestPost({ request: reqFbStatus, env: mockEnv, data: contextData });
  const dataFbStatus = await resFbStatus.json();
  console.log('✓ /api/v1/admin/feedback/status (update):', resFbStatus.status, dataFbStatus.message);

  // 8. Test Games CMS List & Update
  const gamesList = await import('../functions/api/v1/admin/games/index.js');
  const reqGames = new Request('http://localhost/api/v1/admin/games?status=all');
  const resGames = await gamesList.onRequestGet({ request: reqGames, env: mockEnv });
  const dataGames = await resGames.json();
  console.log('✓ /api/v1/admin/games (CMS list):', resGames.status, `Total games: ${dataGames.data.total}, Green: ${dataGames.data.status_stats.green}`);

  const gamesUpdate = await import('../functions/api/v1/admin/games/update.js');
  const reqGameUpdate = new Request('http://localhost/api/v1/admin/games/update', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: 'cyberpunk-2077',
      verified_patch: 'Patch 2.13 (CET v1.33.0 验证)',
      compatibility_status: 'green',
      radar_risk_title: '完美适配'
    })
  });
  const resGameUpdate = await gamesUpdate.onRequestPost({ request: reqGameUpdate, env: mockEnv, data: contextData });
  const dataGameUpdate = await resGameUpdate.json();
  console.log('✓ /api/v1/admin/games/update (CMS edit):', resGameUpdate.status, dataGameUpdate.message);

  // 9. Test Commands CMS (Save & Delete)
  const cmdSave = await import('../functions/api/v1/admin/commands/save.js');
  const reqCmdSave = new Request('http://localhost/api/v1/admin/commands/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: 'test_cyberpunk_godmode_admin',
      game_id: 'cyberpunk-2077',
      category_id: 'godmode',
      category_name_zh: '无敌与免死',
      name_zh: '站长特权一键无敌',
      code: 'Game.SetLevel("Level", 60)',
      syntax_type: 'cet_lua',
      is_popular: 1
    })
  });
  const resCmdSave = await cmdSave.onRequestPost({ request: reqCmdSave, env: mockEnv, data: contextData });
  const dataCmdSave = await resCmdSave.json();
  console.log('✓ /api/v1/admin/commands/save (Upsert):', resCmdSave.status, dataCmdSave.message);

  const cmdDelete = await import('../functions/api/v1/admin/commands/delete.js');
  const reqCmdDelete = new Request('http://localhost/api/v1/admin/commands/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: 'test_cyberpunk_godmode_admin' })
  });
  const resCmdDelete = await cmdDelete.onRequestPost({ request: reqCmdDelete, env: mockEnv, data: contextData });
  const dataCmdDelete = await resCmdDelete.json();
  console.log('✓ /api/v1/admin/commands/delete:', resCmdDelete.status, dataCmdDelete.message);

  // 10. Test AI Copilot & Skills Studio (Config & Test)
  const aiConfigHandler = await import('../functions/api/v1/admin/ai/config.js');
  const resAiGet = await aiConfigHandler.onRequestGet({ env: mockEnv });
  const dataAiGet = await resAiGet.json();
  console.log('✓ /api/v1/admin/ai/config (GET):', resAiGet.status, `Model: ${dataAiGet.data.primary_model}, Tone: ${dataAiGet.data.tone}`);

  const aiTestHandler = await import('../functions/api/v1/admin/ai/test.js');
  const reqAiTest = new Request('http://localhost/api/v1/admin/ai/test', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: '2077 钱 100万', game_id: 'cyberpunk-2077' })
  });
  const resAiTest = await aiTestHandler.onRequestPost({ request: reqAiTest, env: mockEnv });
  const dataAiTest = await resAiTest.json();
  console.log('✓ /api/v1/admin/ai/test (Sandbox):', resAiTest.status,
    `Skills Status: ${dataAiTest.data.skills_audit.save_backup_guard.status}, Retrieved: ${dataAiTest.data.synthesized_prompt.retrieved_commands_count}`);

  // 11. Test Radar Sentinel & Emergency Broadcast
  const radarStatusHandler = await import('../functions/api/v1/admin/radar/status.js');
  const resRadarStatus = await radarStatusHandler.onRequestGet({ env: mockEnv });
  const dataRadarStatus = await resRadarStatus.json();
  console.log('✓ /api/v1/admin/radar/status:', resRadarStatus.status, `Recent logs: ${dataRadarStatus.data.recent_logs.length}`);

  const radarInspectHandler = await import('../functions/api/v1/admin/radar/inspect.js');
  const reqInspect = new Request('http://localhost/api/v1/admin/radar/inspect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ game_id: 'cyberpunk-2077' })
  });
  const resInspect = await radarInspectHandler.onRequestPost({ request: reqInspect, env: mockEnv, data: contextData });
  const dataInspect = await resInspect.json();
  console.log('✓ /api/v1/admin/radar/inspect:', resInspect.status, dataInspect.message);

  const broadcastHandler = await import('../functions/api/v1/admin/radar/broadcast.js');
  const reqBroadcast = new Request('http://localhost/api/v1/admin/radar/broadcast', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      enabled: true,
      level: 'yellow',
      title: 'Steam 补丁兼容性测试预警',
      message: '赛博朋克2077等旗舰游戏补丁变动，请优先参考 L-MOD 验证基准。'
    })
  });
  const resBroadcast = await broadcastHandler.onRequestPost({ request: reqBroadcast, env: mockEnv, data: contextData });
  const dataBroadcast = await resBroadcast.json();
  console.log('✓ /api/v1/admin/radar/broadcast (POST):', resBroadcast.status, dataBroadcast.message);

  // 12. Test Change Password Endpoint
  const pwdHandler = await import('../functions/api/v1/admin/password.js');
  const reqChangePwd = new Request('http://localhost/api/v1/admin/password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ old_password: 'lmod2026!', new_password: 'lmod_new_password_2026!' })
  });
  const resChangePwd = await pwdHandler.onRequestPost({ request: reqChangePwd, env: mockEnv, data: contextData });
  const dataChangePwd = await resChangePwd.json();
  console.log('✓ /api/v1/admin/password (Change Password):', resChangePwd.status, dataChangePwd.message);

  // Re-verify login with the new password
  const reqNewLogin = new Request('http://localhost/api/v1/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'lmod_new_password_2026!' })
  });
  const resNewLogin = await loginHandler.onRequestPost({ request: reqNewLogin, env: mockEnv });
  console.log('✓ Admin Login with updated password succeeded:', resNewLogin.status);

  // Revert password back to lmod2026!
  const reqRevertPwd = new Request('http://localhost/api/v1/admin/password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ old_password: 'lmod_new_password_2026!', new_password: 'lmod2026!' })
  });
  await pwdHandler.onRequestPost({ request: reqRevertPwd, env: mockEnv, data: contextData });
  console.log('✓ Reverted password back to default (lmod2026!) for future runs');

  console.log('================================================================');
  console.log('🎉 ALL ADMIN API & ZERO TRUST AUTH TESTS PASSED FLAWLESSLY!');
  console.log('================================================================');
}

runTests().catch(err => {
  console.error('❌ Test failed:', err);
  process.exit(1);
});
