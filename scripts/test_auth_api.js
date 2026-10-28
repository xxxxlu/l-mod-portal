/**
 * L-MOD Vault - Integration Test Suite for Email OTP, PBKDF2 & Player Auth APIs
 */

const { execSync } = require('child_process');
const path = require('path');
const assert = require('assert');

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
    let finalSql = this.sql;
    let paramIndex = 0;

    finalSql = finalSql.replace(/\?/g, () => {
      const p = this.params[paramIndex++];
      if (p === null || p === undefined) return 'NULL';
      if (typeof p === 'number') return p;
      return `'${String(p).replace(/'/g, "''")}'`;
    });

    const cmd = `/usr/bin/sqlite3 "${DB_PATH}" "${finalSql.replace(/"/g, '\\"')}"`;
    try {
      execSync(cmd, { encoding: 'utf-8' });
      return { success: true };
    } catch (err) {
      throw err;
    }
  }
}

class MockD1Database {
  prepare(sql) {
    return new MockD1Statement(sql);
  }

  async batch(statements) {
    for (const stmt of statements) {
      await stmt.run();
    }
    return { success: true };
  }
}

async function runTests() {
  console.log('🧪 [TEST] Starting L-MOD Vault Player Auth & OTP Integration Test Suite...');

  const {
    hashPassword,
    verifyPassword,
    signUserJwt,
    verifyUserJwt,
    generateOtpCode,
    isValidEmail
  } = await import('../functions/api/v1/auth/_crypto.js');

  const { onRequestPost: sendCodeHandler } = await import('../functions/api/v1/auth/send-code.js');
  const { onRequestPost: verifyCodeHandler } = await import('../functions/api/v1/auth/verify-code.js');
  const { onRequestPost: setPasswordHandler } = await import('../functions/api/v1/auth/set-password.js');
  const { onRequestPost: loginPasswordHandler } = await import('../functions/api/v1/auth/login-password.js');
  const { onRequestPost: registerPasswordHandler } = await import('../functions/api/v1/auth/register-password.js');
  const { onRequestPost: changeEmailHandler } = await import('../functions/api/v1/auth/change-email.js');
  const { onRequestGet: meHandler } = await import('../functions/api/v1/auth/me.js');
  const { onRequestPost: favoritesPostHandler, onRequestGet: favoritesGetHandler } = await import('../functions/api/v1/auth/favorites.js');

  const db = new MockD1Database();
  const env = { DB: db, PLAYER_JWT_SECRET: 'test-jwt-secret-for-integration-tests', TEST_MOCK_MAIL: '1' };

  // TEST 1: Web Crypto PBKDF2 Hashing
  console.log('\n--- 1. Testing Web Crypto PBKDF2 Password Hashing (100k Iterations) ---');
  const testPassword = 'GamerMaster#2026';
  const { hashHex, saltHex } = await hashPassword(testPassword);
  assert(hashHex && hashHex.length === 64, 'PBKDF2 hash should be 64-char hex string (256 bits)');
  assert(saltHex && saltHex.length === 32, 'Salt should be 32-char hex string (16 bytes)');
  const isValidPwd = await verifyPassword(testPassword, saltHex, hashHex);
  assert(isValidPwd === true, 'Original password should verify against salt and hash');
  const isInvalidPwd = await verifyPassword('WrongPassword123', saltHex, hashHex);
  assert(isInvalidPwd === false, 'Wrong password should fail verification');
  console.log('✅ Web Crypto PBKDF2 hashing & verification passed!');

  // TEST 2: Web Crypto JWT Signing & Verification
  console.log('\n--- 2. Testing Player JWT Stateless Token Sign & Verify ---');
  const tokenPayload = { id: 'usr_test_player_99', email: 'test_player@lmod.gg', nickname: '测试老玩家' };
  const token = await signUserJwt(tokenPayload, env.PLAYER_JWT_SECRET);
  assert(typeof token === 'string' && token.split('.').length === 3, 'JWT should have 3 segments');
  const verified = await verifyUserJwt(token, env.PLAYER_JWT_SECRET);
  assert(verified.valid === true, 'Token should verify successfully');
  assert(verified.payload.email === 'test_player@lmod.gg', 'Token payload email should match');
  console.log('✅ Web Crypto JWT token signing & verification passed!');

  // TEST 3: Strict Email Regex Validation
  console.log('\n--- 3. Testing Strict Email Format Regex Validation ---');
  assert.strictEqual(isValidEmail('gamer@qq.com'), true, 'Standard QQ email should pass');
  assert.strictEqual(isValidEmail('player_2026@163.com'), true, '163 email should pass');
  assert.strictEqual(isValidEmail('master.chief@gmail.com'), true, 'Gmail with dot should pass');
  assert.strictEqual(isValidEmail('cyber-pro@vip.126.net'), true, 'Multi-level domain email should pass');
  assert.strictEqual(isValidEmail('not-an-email'), false, 'Plain string should fail');
  assert.strictEqual(isValidEmail('missing-at-sign.com'), false, 'Missing @ should fail');
  assert.strictEqual(isValidEmail('missing@domain'), false, 'Domain without dot should fail');
  assert.strictEqual(isValidEmail('@no-local-part.com'), false, 'Missing username should fail');
  assert.strictEqual(isValidEmail('spaces in@email.com'), false, 'Spaces should fail');
  console.log('✅ Strict email regex validation passed (100% compliant)!');

  // TEST 3.5: Direct Password-Based Registration API
  console.log('\n--- 3.5. Testing POST /api/v1/auth/register-password ---');
  const directEmail = `direct_player_${Date.now()}@gamer.vip`;
  const invalidEmailReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/register-password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: 'bad-email-format', password: 'ValidPassword123' })
  });
  const invalidEmailRes = await registerPasswordHandler({ request: invalidEmailReq, env });
  assert.strictEqual(invalidEmailRes.status, 400, 'Invalid email must return 400');

  const validRegReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/register-password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: directEmail, password: 'StrongPassword#2026', confirm_password: 'StrongPassword#2026' })
  });
  const validRegRes = await registerPasswordHandler({ request: validRegReq, env });
  assert.strictEqual(validRegRes.status, 200, 'Valid registration must return 200');
  const validRegData = await validRegRes.json();
  assert.strictEqual(validRegData.code, 0);
  assert(validRegData.data.token, 'Should issue JWT token upon registration');
  assert.strictEqual(validRegData.data.user.email, directEmail);
  console.log(`✅ register-password passed! Auto created user: ${validRegData.data.user.id}`);

  // Duplicate registration check
  const dupRegReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/register-password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: directEmail, password: 'StrongPassword#2026', confirm_password: 'StrongPassword#2026' })
  });
  const dupRegRes = await registerPasswordHandler({ request: dupRegReq, env });
  assert.strictEqual(dupRegRes.status, 400, 'Duplicate registration must be rejected');
  const dupData = await dupRegRes.json();
  assert.strictEqual(dupData.code, 40005, 'Duplicate email error code');
  console.log('✅ Duplicate email registration guard verified!');

  // TEST 4: OTP Code Generation
  console.log('\n--- 3. Testing 6-Digit Cryptographic OTP Generator ---');
  for (let i = 0; i < 20; i++) {
    const code = generateOtpCode();
    assert(/^\d{6}$/.test(code), `OTP code must be 6 digits, got: ${code}`);
  }
  console.log('✅ 6-digit OTP generation passed!');

  // TEST 4: Send OTP Code API
  console.log('\n--- 4. Testing POST /api/v1/auth/send-code ---');
  const testEmail = `player_${Date.now()}@test-vault.gg`;
  const sendReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'cf-connecting-ip': '1.2.3.4' },
    body: JSON.stringify({ email: testEmail, purpose: 'login' })
  });
  const sendRes = await sendCodeHandler({ request: sendReq, env });
  assert.strictEqual(sendRes.status, 200, 'send-code should return HTTP 200');
  const sendData = await sendRes.json();
  assert.strictEqual(sendData.code, 0, 'Response code should be 0');
  assert.strictEqual(sendData.data.dev_code, undefined, 'dev_code must NOT leak in API response');
  const codeRow = await db.prepare(
    'SELECT code FROM email_verification_codes WHERE email = ? ORDER BY id DESC LIMIT 1'
  ).bind(testEmail).first();
  assert(codeRow && codeRow.code, 'Database should contain generated OTP code');
  const generatedCode = codeRow.code;
  console.log(`✅ send-code passed! Real DB code: ${generatedCode}`);

  // TEST 5: Cooldown Enforcement (Immediate retry should be blocked)
  console.log('\n--- 5. Testing 60s Cooldown Enforcement ---');
  const repeatReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'cf-connecting-ip': '1.2.3.4' },
    body: JSON.stringify({ email: testEmail, purpose: 'login' })
  });
  const repeatRes = await sendCodeHandler({ request: repeatReq, env });
  assert.strictEqual(repeatRes.status, 429, 'send-code should return HTTP 429 on cooldown');
  const repeatData = await repeatRes.json();
  assert.strictEqual(repeatData.code, 42902, 'Should return cooldown error code');
  console.log('✅ 60s Cooldown protection verified!');

  // TEST 6: Verify Code API (Wrong Code then Correct Code)
  console.log('\n--- 6. Testing POST /api/v1/auth/verify-code (Wrong Code & Correct Code) ---');
  const wrongReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/verify-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: testEmail, code: '000000', purpose: 'login' })
  });
  const wrongRes = await verifyCodeHandler({ request: wrongReq, env });
  assert.strictEqual(wrongRes.status, 400, 'Wrong code should return HTTP 400');
  const wrongData = await wrongRes.json();
  assert.strictEqual(wrongData.code, 40015, 'Should return invalid code error with remaining attempts');

  // Now submit the correct code
  const correctReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/verify-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: testEmail, code: generatedCode, purpose: 'login' })
  });
  const correctRes = await verifyCodeHandler({ request: correctReq, env });
  assert.strictEqual(correctRes.status, 200, 'Correct code should return HTTP 200');
  const loginData = await correctRes.json();
  assert.strictEqual(loginData.code, 0);
  assert.strictEqual(loginData.data.is_first_login, true, 'New email must be flagged as is_first_login');
  assert.strictEqual(loginData.data.has_password, false, 'New user must not have password set');
  assert(loginData.data.token, 'Should return valid player JWT token');
  const playerToken = loginData.data.token;
  const newUserId = loginData.data.user.id;
  console.log(`✅ verify-code passed! User auto-registered: ${newUserId}`);

  // TEST 7: Set Password API
  console.log('\n--- 7. Testing POST /api/v1/auth/set-password ---');
  const setPwdReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/set-password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${playerToken}`
    },
    body: JSON.stringify({ password: 'MyVaultPassword#2026' })
  });
  const setPwdRes = await setPasswordHandler({ request: setPwdReq, env });
  assert.strictEqual(setPwdRes.status, 200, 'set-password should return HTTP 200');
  const setPwdData = await setPwdRes.json();
  assert.strictEqual(setPwdData.code, 0);
  assert.strictEqual(setPwdData.data.has_password, true);
  console.log('✅ set-password passed! Password successfully set');

  // TEST 8: Login with Password API
  console.log('\n--- 8. Testing POST /api/v1/auth/login-password ---');
  const loginPwdReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/login-password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: testEmail, password: 'MyVaultPassword#2026' })
  });
  const loginPwdRes = await loginPasswordHandler({ request: loginPwdReq, env });
  assert.strictEqual(loginPwdRes.status, 200, 'login-password should return HTTP 200');
  const loginPwdData = await loginPwdRes.json();
  assert.strictEqual(loginPwdData.code, 0);
  assert.strictEqual(loginPwdData.data.has_password, true);
  assert(loginPwdData.data.token, 'Should return fresh JWT token');
  console.log('✅ login-password passed! Direct email + password authentication verified');

  // TEST 9: Add and Query Favorites API
  console.log('\n--- 9. Testing /api/v1/auth/favorites (Toggle & List) ---');
  const favReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/favorites', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${playerToken}`
    },
    body: JSON.stringify({ game_id: 'cyberpunk-2077', action: 'toggle' })
  });
  const favRes = await favoritesPostHandler({ request: favReq, env, waitUntil: () => {} });
  assert.strictEqual(favRes.status, 200);
  const favData = await favRes.json();
  assert.strictEqual(favData.code, 0);
  assert.strictEqual(favData.data.is_favorited, true, 'Cyberpunk 2077 should be favorited');

  const getFavReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/favorites', {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${playerToken}` }
  });
  const getFavRes = await favoritesGetHandler({ request: getFavReq, env });
  const getFavData = await getFavRes.json();
  assert(getFavData.data.game_ids.includes('cyberpunk-2077'), 'Favorites list should contain cyberpunk-2077');
  console.log('✅ Favorites toggle & persistence verified!');

  // TEST 10: GET /api/v1/auth/me Profile
  console.log('\n--- 10. Testing GET /api/v1/auth/me Comprehensive Profile ---');
  const meReq = new Request('https://lmod-vault.pages.dev/api/v1/auth/me', {
    method: 'GET',
    headers: { 'Authorization': `Bearer ${playerToken}` }
  });
  const meRes = await meHandler({ request: meReq, env });
  assert.strictEqual(meRes.status, 200);
  const meData = await meRes.json();
  assert.strictEqual(meData.code, 0);
  assert.strictEqual(meData.data.user.email, testEmail);
  assert.strictEqual(meData.data.user.has_password, true);
  assert.strictEqual(meData.data.favorites.length, 1);
  console.log('✅ GET /api/v1/auth/me verified successfully!');

  console.log('\n🎉 ALL 10 AUTH INTEGRATION TESTS PASSED WITH 100% SUCCESS!');
}

runTests().catch(err => {
  console.error('\n❌ TEST FAILED:', err);
  process.exit(1);
});
