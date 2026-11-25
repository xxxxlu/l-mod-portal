/**
 * L-MOD Vault Admin Auth & Web Crypto JWT Engine
 * Zero-dependency, stateless HMAC-SHA256 (HS256) JWT implementation
 * Runs natively on Cloudflare Pages Functions / V8 Edge Runtime
 */

// ---------------------------------------------------------------------------
// 凭据只认 Cloudflare 环境变量（或后台「修改密码」写进 D1 的口令），没有任何默认值。
//
// 以前这里写死了默认口令、一把永远有效的「万能钥匙」和默认 JWT 密钥，而本仓库是公开的，
// 等于谁都能登录后台。现在：
//   - ADMIN_JWT_SECRET 必须配置（至少 32 个字符），否则后台整体返回 503；
//   - 口令取 ADMIN_PASSWORD；没配时才用 D1 system_settings.admin_credentials（后台改密码写的）；
//   - 下面这些在仓库里公开过的值，无论配在哪里都视为「未配置」。
// ---------------------------------------------------------------------------
const TOKEN_TTL_SECONDS = 7 * 24 * 60 * 60; // 7 Days valid
const MIN_JWT_SECRET_LENGTH = 32;
const MIN_PASSWORD_LENGTH = 10;
const PUBLISHED_VALUES = new Set([
  'lmod2026!',
  'lmod_new_password_2026!',
  'lmod-vault-master-station-key-2026',
  'lmod-vault-jwt-hmac-sha256-edge-token-secret-2026'
]);

export function isPublishedValue(value) {
  return PUBLISHED_VALUES.has(String(value || ''));
}

export function isUsablePassword(value) {
  const v = String(value || '');
  return v.length >= MIN_PASSWORD_LENGTH && !PUBLISHED_VALUES.has(v);
}

/**
 * 返回 { username, password, configured, source }。
 * configured=false 时 password 为空字符串，调用方必须拒绝登录。
 * source: 'env' | 'db' | null —— 口令来自环境变量时，后台不能改密码（要去 Cloudflare 改）。
 */
export async function getAdminCredentials(env, db) {
  const envUser = (env && (env.ADMIN_USERNAME || env.ADMIN_USER)) || '';
  const envPass = (env && env.ADMIN_PASSWORD) || '';
  let username = envUser || 'admin';
  let password = '';
  let source = null;

  if (envPass) {
    password = envPass;
    source = 'env';
  } else if (db) {
    try {
      const row = await db.prepare("SELECT value FROM system_settings WHERE key = 'admin_credentials'").first();
      if (row && row.value) {
        const creds = JSON.parse(row.value);
        if (creds.password) {
          password = String(creds.password);
          source = 'db';
        }
        if (!envUser && creds.username) username = String(creds.username);
      }
    } catch (e) {}
  }

  const configured = isUsablePassword(password);
  return { username, password: configured ? password : '', configured, source: configured ? source : null };
}

/** 没配置或配的是公开过的值时返回空字符串，调用方必须拒绝签发 / 校验令牌。 */
export function getJwtSecret(env) {
  const secret = String((env && env.ADMIN_JWT_SECRET) || '');
  if (secret.length < MIN_JWT_SECRET_LENGTH || PUBLISHED_VALUES.has(secret)) return '';
  return secret;
}

/** 等长比较，避免按字节提前返回泄露口令长度以外的信息。 */
export function timingSafeEqualString(a, b) {
  const enc = new TextEncoder();
  const x = enc.encode(String(a || ''));
  const y = enc.encode(String(b || ''));
  let diff = x.length ^ y.length;
  const len = Math.max(x.length, y.length);
  for (let i = 0; i < len; i++) {
    diff |= (x[i] || 0) ^ (y[i] || 0);
  }
  return diff === 0;
}

export function adminNotConfiguredResponse(what) {
  return new Response(JSON.stringify({
    code: 50301,
    message: `后台未开通：${what}。请在 Cloudflare Pages 的环境变量里配置 ADMIN_JWT_SECRET（至少 32 个字符）和 ADMIN_PASSWORD（至少 10 个字符，不能用仓库里公开过的默认值）。`,
    error_type: 'ADMIN_NOT_CONFIGURED'
  }), {
    status: 503,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}

// Base64URL string & buffer utilities
export function base64UrlEncode(input) {
  let base64 = '';
  if (typeof input === 'string') {
    const bytes = new TextEncoder().encode(input);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    base64 = btoa(binary);
  } else {
    const bytes = new Uint8Array(input);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    base64 = btoa(binary);
  }
  return base64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function base64UrlDecode(input) {
  let base64 = input.replace(/-/g, '+').replace(/_/g, '/');
  while (base64.length % 4) {
    base64 += '=';
  }
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return new TextDecoder().decode(bytes);
}

export function base64UrlToBuffer(input) {
  let base64 = input.replace(/-/g, '+').replace(/_/g, '/');
  while (base64.length % 4) {
    base64 += '=';
  }
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}

/**
 * Generate HMAC-SHA256 CryptoKey
 */
async function getCryptoKey(secret, usages) {
  const enc = new TextEncoder();
  return await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    usages
  );
}

/**
 * Sign JWT Token with HMAC-SHA256
 */
export async function signAdminJwt(customPayload, secret) {
  const header = {
    alg: 'HS256',
    typ: 'JWT'
  };

  const nowSeconds = Math.floor(Date.now() / 1000);
  const payload = {
    iss: 'lmod-vault-sentinel',
    sub: 'station_master',
    role: 'super_admin',
    iat: nowSeconds,
    exp: nowSeconds + TOKEN_TTL_SECONDS,
    ...customPayload
  };

  const encodedHeader = base64UrlEncode(JSON.stringify(header));
  const encodedPayload = base64UrlEncode(JSON.stringify(payload));
  const message = `${encodedHeader}.${encodedPayload}`;

  const key = await getCryptoKey(secret, ['sign']);
  const signatureBuffer = await crypto.subtle.sign(
    'HMAC',
    key,
    new TextEncoder().encode(message)
  );

  const encodedSignature = base64UrlEncode(signatureBuffer);
  return `${message}.${encodedSignature}`;
}

/**
 * Verify JWT Token and check signature & expiry
 */
export async function verifyAdminJwt(token, secret) {
  if (!token || typeof token !== 'string') {
    return { valid: false, error: 'Token missing or invalid format' };
  }

  const parts = token.trim().split('.');
  if (parts.length !== 3) {
    return { valid: false, error: 'Malformed JWT structure' };
  }

  const [encodedHeader, encodedPayload, encodedSignature] = parts;

  try {
    const key = await getCryptoKey(secret, ['verify']);
    const message = `${encodedHeader}.${encodedPayload}`;
    const signatureBuffer = base64UrlToBuffer(encodedSignature);

    const isSignatureValid = await crypto.subtle.verify(
      'HMAC',
      key,
      signatureBuffer,
      new TextEncoder().encode(message)
    );

    if (!isSignatureValid) {
      return { valid: false, error: 'Invalid token signature' };
    }

    const payloadJson = base64UrlDecode(encodedPayload);
    const payload = JSON.parse(payloadJson);

    const nowSeconds = Math.floor(Date.now() / 1000);
    if (payload.exp && payload.exp < nowSeconds) {
      return { valid: false, error: 'Token has expired', expired: true };
    }

    if (payload.role !== 'super_admin') {
      return { valid: false, error: 'Insufficient administrative privileges' };
    }

    return { valid: true, payload };
  } catch (err) {
    return { valid: false, error: err.message };
  }
}

/**
 * Extract token from request headers or query or cookies
 */
export function extractAdminToken(request) {
  const authHeader = request.headers.get('Authorization') || request.headers.get('authorization');
  if (authHeader && authHeader.toLowerCase().startsWith('bearer ')) {
    return authHeader.slice(7).trim();
  }

  const customHeader = request.headers.get('x-admin-token');
  if (customHeader) {
    return customHeader.trim();
  }

  const cookieHeader = request.headers.get('Cookie') || request.headers.get('cookie');
  if (cookieHeader) {
    const match = cookieHeader.match(/lmod_admin_token=([^;]+)/);
    if (match) return decodeURIComponent(match[1].trim());
  }

  return null;
}

/**
 * Helper to record audit log in D1
 */
export async function logAdminAction(db, { action, entity, entity_id, details, admin_user = '老L·站长', client_ip = '127.0.0.1' }) {
  if (!db) return;
  try {
    const detailsStr = typeof details === 'object' ? JSON.stringify(details) : String(details || '');
    await db.prepare(
      `INSERT INTO admin_audit_logs (action, entity, entity_id, details, admin_user, client_ip)
       VALUES (?, ?, ?, ?, ?, ?)`
    ).bind(action, entity, entity_id || null, detailsStr, admin_user, client_ip).run();
  } catch (e) {
    console.error('Failed to log admin action:', e);
  }
}
