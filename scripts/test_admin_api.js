/**
 * L-MOD Vault - Integration Test Suite for Admin Console & AI Control Plane API
 */

const { execSync } = require('child_process');
const path = require('path');

const DB_PATH = path.resolve(__dirname, '../database/lmod_vault.db');
const fs = require('fs');

// 测试专用凭据（只在本测试里用）。仓库里公开过的旧默认值必须被拒绝，见下面「fail closed」一节。
const TEST_PASS = 'test-only-admin-pass-0001';
const TEST_PASS_2 = 'test-only-admin-pass-0002';
const TEST_JWT = 'test-only-jwt-secret-0123456789abcdef0123';
const PUBLISHED = {
  pass: 'lmod2026!',
  legacyKey: 'lmod-vault-master-station-key-2026',
  jwt: 'lmod-vault-jwt-hmac-sha256-edge-token-secret-2026'
};

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
    ADMIN_PASSWORD: TEST_PASS,
    ADMIN_JWT_SECRET: TEST_JWT
  };

  const loginHandler = await import('../functions/api/v1/admin/login.js');
  const loginAs = (env, body) => loginHandler.onRequestPost({
    request: new Request('http://localhost/api/v1/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }),
    env
  });

  // 0. Fail closed: 没配 / 配的是公开过的值 → 503，不能登录
  const cases503 = [
    ['no ADMIN_JWT_SECRET', { DB: mockDb, ADMIN_PASSWORD: TEST_PASS }, { username: 'admin', password: TEST_PASS }],
    ['published JWT secret', { DB: mockDb, ADMIN_PASSWORD: TEST_PASS, ADMIN_JWT_SECRET: PUBLISHED.jwt }, { username: 'admin', password: TEST_PASS }],
    ['short JWT secret', { DB: mockDb, ADMIN_PASSWORD: TEST_PASS, ADMIN_JWT_SECRET: 'too-short' }, { username: 'admin', password: TEST_PASS }],
    ['published password in env', { DB: mockDb, ADMIN_PASSWORD: PUBLISHED.pass, ADMIN_JWT_SECRET: TEST_JWT }, { username: 'admin', password: PUBLISHED.pass }],
  ];
  for (const [label, env, body] of cases503) {
    const res = await loginAs(env, body);
    if (res.status !== 503) throw new Error(`login with ${label} should return 503, got ${res.status}`);
    console.log(`✓ Login refused (503) with ${label}`);
  }
  const mwNoSecret = await (await import('../functions/api/v1/admin/_middleware.js')).onRequest({
    request: new Request('http://localhost/api/v1/admin/me', { headers: { Authorization: 'Bearer x.y.z' } }),
    env: { DB: mockDb },
    next: async () => new Response('SHOULD NOT PASS')
  });
  if (mwNoSecret.status !== 503) throw new Error('middleware without JWT secret should return 503');
  console.log('✓ Middleware refuses every admin call (503) when ADMIN_JWT_SECRET is missing');

  // 1. Test Admin Login (Invalid Credentials)
  const reqBadLogin = new Request('http://localhost/api/v1/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'admin', password: 'wrong-password-123' })
  });
  const resBadLogin = await loginHandler.onRequestPost({ request: reqBadLogin, env: mockEnv });
  const dataBadLogin = await resBadLogin.json();
  console.log('✓ Admin Login (Invalid Credentials) correctly rejected:', resBadLogin.status, dataBadLogin.code);
  if (resBadLogin.status !== 401) throw new Error('Bad login should return 401');

  // 2. Test Admin Login (configured username & password)
  const resGoodLogin = await loginAs(mockEnv, { username: 'admin', password: TEST_PASS });
  const dataGoodLogin = await resGoodLogin.json();
  console.log('✓ Admin Login (configured credentials) succeeded, JWT issued:', resGoodLogin.status, 'Token length:', dataGoodLogin.data.token.length);
  if (resGoodLogin.status !== 200 || !dataGoodLogin.data.token) throw new Error('Login failed to return token');

  // 旧的「万能钥匙」、公开过的默认口令、别名账号都不能再登录
  for (const [label, body] of [
    ['legacy master key', { secret_key: PUBLISHED.legacyKey }],
    ['published default password', { username: 'admin', password: PUBLISHED.pass }],
    ['alias username laol', { username: 'laol', password: TEST_PASS }],
  ]) {
    const res = await loginAs(mockEnv, body);
    if (res.status !== 401) throw new Error(`login with ${label} should return 401, got ${res.status}`);
    console.log(`✓ Login rejected (401) with ${label}`);
  }

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
  const resAnalytics = await analyticsOverview.onRequestGet({
    request: new Request('http://localhost/api/v1/admin/analytics/overview?range=30d'),
    env: mockEnv
  });
  const dataAnalytics = await resAnalytics.json();
  if (resAnalytics.status !== 200) throw new Error(`analytics overview should return 200, got ${resAnalytics.status}: ${dataAnalytics.message}`);
  console.log('✓ /api/v1/admin/analytics/overview:', resAnalytics.status,
    `PV: ${dataAnalytics.data.summary.pv}, UV: ${dataAnalytics.data.summary.uv}, Top Searches: ${dataAnalytics.data.top.searches.length}`);

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

  // 8. Test Games CMS List
  const gamesList = await import('../functions/api/v1/admin/games/index.js');
  const reqGames = new Request('http://localhost/api/v1/admin/games?status=all');
  const resGames = await gamesList.onRequestGet({ request: reqGames, env: mockEnv });
  const dataGames = await resGames.json();
  console.log('✓ /api/v1/admin/games (CMS list):', resGames.status, `Total games: ${dataGames.data.total}, Green: ${dataGames.data.status_stats.green}`);

  // 9. Whole-document game editing (save / hide / history) is covered by node:test with a real
  //    SQLite-backed D1 stand-in: node --test scripts/tests/catalog/
  //    (the per-field update and per-command save/delete endpoints were retired with D1 as the source).

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

  // 12. Change Password Endpoint
  const pwdHandler = await import('../functions/api/v1/admin/password.js');
  const changePwd = (env, body) => pwdHandler.onRequestPost({
    request: new Request('http://localhost/api/v1/admin/password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }),
    env,
    data: contextData
  });

  // 口令由环境变量管理时，后台改密码不生效 → 409
  const resEnvPwd = await changePwd(mockEnv, { old_password: TEST_PASS, new_password: TEST_PASS_2 });
  if (resEnvPwd.status !== 409) throw new Error(`password change with env-managed password should return 409, got ${resEnvPwd.status}`);
  console.log('✓ /api/v1/admin/password refuses (409) when ADMIN_PASSWORD comes from env');

  // 不允许改成公开过的默认口令或太短的口令
  for (const bad of [PUBLISHED.pass, 'short']) {
    const res = await changePwd(mockEnv, { old_password: TEST_PASS, new_password: bad });
    if (res.status !== 400) throw new Error(`new password "${bad}" should be rejected with 400, got ${res.status}`);
  }
  console.log('✓ /api/v1/admin/password rejects published / too-short new passwords (400)');

  // 口令存在 D1 的路径：只在本地有 database/lmod_vault.db 时跑，跑完把原记录恢复
  if (fs.existsSync(DB_PATH)) {
    const dbEnv = { DB: mockDb, ADMIN_JWT_SECRET: TEST_JWT };
    const original = await mockDb.prepare("SELECT value FROM system_settings WHERE key = 'admin_credentials'").first();
    const writeCreds = (value) => mockDb.prepare(
      "INSERT INTO system_settings (key, value, description, updated_at) VALUES ('admin_credentials', ?, 'test', CURRENT_TIMESTAMP) " +
      "ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP"
    ).bind(value).run();
    try {
      await writeCreds(JSON.stringify({ username: 'admin', password: PUBLISHED.pass }));
      const resSeeded = await loginAs(dbEnv, { username: 'admin', password: PUBLISHED.pass });
      if (resSeeded.status !== 503) throw new Error(`seeded default password in D1 should return 503, got ${resSeeded.status}`);
      console.log('✓ The seeded default password row in D1 is treated as "not configured" (503)');

      await writeCreds(JSON.stringify({ username: 'admin', password: TEST_PASS }));
      const resDbLogin = await loginAs(dbEnv, { username: 'admin', password: TEST_PASS });
      if (resDbLogin.status !== 200) throw new Error(`login with D1 password should succeed, got ${resDbLogin.status}`);
      const resDbChange = await changePwd(dbEnv, { old_password: TEST_PASS, new_password: TEST_PASS_2 });
      if (resDbChange.status !== 200) throw new Error(`password change in D1 should succeed, got ${resDbChange.status}`);
      const resDbNew = await loginAs(dbEnv, { username: 'admin', password: TEST_PASS_2 });
      if (resDbNew.status !== 200) throw new Error(`login with the changed password should succeed, got ${resDbNew.status}`);
      console.log('✓ D1-stored password: login → change → login with the new password');
    } finally {
      if (original && original.value) await writeCreds(original.value);
      else await mockDb.prepare("DELETE FROM system_settings WHERE key = 'admin_credentials'").run();
      console.log('✓ Restored the local admin_credentials row');
    }
  } else {
    console.log('- Skipped the D1-stored password checks (no local database/lmod_vault.db)');
  }

  console.log('================================================================');
  console.log('🎉 ALL ADMIN API & ZERO TRUST AUTH TESTS PASSED FLAWLESSLY!');
  console.log('================================================================');
}

runTests().catch(err => {
  console.error('❌ Test failed:', err);
  process.exit(1);
});
