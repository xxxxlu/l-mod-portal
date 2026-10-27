/**
 * L-MOD Vault Admin Auth & Web Crypto JWT Engine
 * Zero-dependency, stateless HMAC-SHA256 (HS256) JWT implementation
 * Runs natively on Cloudflare Pages Functions / V8 Edge Runtime
 */

const DEFAULT_ADMIN_USER = 'admin';
const DEFAULT_ADMIN_PASS = 'lmod2026!';
const LEGACY_MASTER_KEY = 'lmod-vault-master-station-key-2026';
const DEFAULT_JWT_SECRET = 'lmod-vault-jwt-hmac-sha256-edge-token-secret-2026';
const TOKEN_TTL_SECONDS = 7 * 24 * 60 * 60; // 7 Days valid

export async function getAdminCredentials(env, db) {
  let username = (env && (env.ADMIN_USERNAME || env.ADMIN_USER)) || DEFAULT_ADMIN_USER;
  let password = (env && (env.ADMIN_PASSWORD || env.ADMIN_SECRET_KEY || env.ADMIN_KEY)) || DEFAULT_ADMIN_PASS;

  // Check database override in system_settings if available
  if (db) {
    try {
      const row = await db.prepare('SELECT value FROM system_settings WHERE key = "admin_credentials"').first();
      if (row && row.value) {
        const creds = JSON.parse(row.value);
        if (creds.username) username = creds.username;
        if (creds.password) password = creds.password;
      }
    } catch (e) {}
  }

  return { username, password, legacyKey: LEGACY_MASTER_KEY };
}

export function getAdminSecret(env) {
  return (env && (env.ADMIN_PASSWORD || env.ADMIN_SECRET_KEY || env.ADMIN_KEY)) || DEFAULT_ADMIN_PASS;
}

export function getJwtSecret(env) {
  return (env && (env.ADMIN_JWT_SECRET || env.ADMIN_SECRET_KEY || env.ADMIN_KEY)) || DEFAULT_JWT_SECRET;
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
