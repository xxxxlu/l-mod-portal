/**
 * L-MOD Vault - Player Auth, Web Crypto PBKDF2 & Edge JWT Security Engine
 * Zero external dependencies. 100% Native Web Crypto (SubtleCrypto) & Cloudflare Pages Functions compatible.
 */

const DEFAULT_JWT_SECRET = 'lmod-vault-player-jwt-secret-key-2026';
const TOKEN_TTL_SECONDS = 30 * 24 * 60 * 60; // 30 Days valid

export function getDatabase(env) {
  return (env && (env.DB || env.lmod_vault_db)) || null;
}

export function getPlayerJwtSecret(env) {
  return (env && (env.PLAYER_JWT_SECRET || env.JWT_SECRET || env.ADMIN_JWT_SECRET)) || DEFAULT_JWT_SECRET;
}

export const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

export function isValidEmail(email) {
  if (!email || typeof email !== 'string') return false;
  const trimmed = email.trim().toLowerCase();
  if (trimmed.length < 5 || trimmed.length > 128) return false;
  if (!EMAIL_REGEX.test(trimmed)) return false;
  const parts = trimmed.split('@');
  if (parts.length !== 2) return false;
  const [localPart, domainPart] = parts;
  if (!localPart || !domainPart) return false;
  if (!domainPart.includes('.')) return false;
  const domainSegments = domainPart.split('.');
  const tld = domainSegments[domainSegments.length - 1];
  if (tld.length < 2) return false;
  return true;
}

/**
 * Self-healing schema initialization: automatically creates email_verification_codes table
 * and adds email/password columns to users table if not already present in D1
 */
export async function ensureAuthSchema(db) {
  if (!db) return;
  try {
    await db.prepare(`
      CREATE TABLE IF NOT EXISTS email_verification_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        code TEXT NOT NULL,
        purpose TEXT NOT NULL DEFAULT 'login',
        expires_at DATETIME NOT NULL,
        attempts INTEGER DEFAULT 0,
        is_used BOOLEAN DEFAULT 0,
        client_ip TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `).run();

    try { await db.prepare("CREATE INDEX IF NOT EXISTS idx_email_codes_email ON email_verification_codes(email)").run(); } catch(e) {}
    try { await db.prepare("CREATE INDEX IF NOT EXISTS idx_email_codes_lookup ON email_verification_codes(email, code, purpose, is_used)").run(); } catch(e) {}
    try { await db.prepare("ALTER TABLE users ADD COLUMN email TEXT").run(); } catch(e) {}
    try { await db.prepare("ALTER TABLE users ADD COLUMN password_hash TEXT").run(); } catch(e) {}
    try { await db.prepare("ALTER TABLE users ADD COLUMN password_salt TEXT").run(); } catch(e) {}
    try { await db.prepare("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active'").run(); } catch(e) {}
    try { await db.prepare("ALTER TABLE users ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP").run(); } catch(e) {}
    try { await db.prepare("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email) WHERE email IS NOT NULL").run(); } catch(e) {}
    try { await db.prepare("ALTER TABLE community_feedback ADD COLUMN user_id TEXT").run(); } catch(e) {}
    try { await db.prepare("ALTER TABLE community_feedback ADD COLUMN player_email TEXT").run(); } catch(e) {}
  } catch (err) {
    console.warn('[ensureAuthSchema Auto-Init]', err.message);
  }
}

// -----------------------------------------------------------------------------
// 1. Base64URL Encoders / Decoders
// -----------------------------------------------------------------------------
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

// -----------------------------------------------------------------------------
// 2. Web Crypto PBKDF2 Password Hashing (HMAC-SHA256, 100,000 iterations)
// -----------------------------------------------------------------------------
export async function hashPassword(password, saltHex = null) {
  let saltBytes;
  if (saltHex) {
    const matches = saltHex.match(/.{1,2}/g) || [];
    saltBytes = new Uint8Array(matches.map(byte => parseInt(byte, 16)));
  } else {
    saltBytes = new Uint8Array(16);
    crypto.getRandomValues(saltBytes);
    saltHex = Array.from(saltBytes).map(b => b.toString(16).padStart(2, '0')).join('');
  }

  const enc = new TextEncoder();
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    enc.encode(password),
    'PBKDF2',
    false,
    ['deriveBits']
  );

  const derivedBits = await crypto.subtle.deriveBits(
    {
      name: 'PBKDF2',
      salt: saltBytes,
      iterations: 100000,
      hash: 'SHA-256'
    },
    keyMaterial,
    256 // 32 bytes (256 bits)
  );

  const hashHex = Array.from(new Uint8Array(derivedBits))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

  return { hashHex, saltHex };
}

export async function verifyPassword(password, saltHex, targetHashHex) {
  if (!password || !saltHex || !targetHashHex) return false;
  try {
    const { hashHex } = await hashPassword(password, saltHex);
    return hashHex === targetHashHex;
  } catch (e) {
    return false;
  }
}

// -----------------------------------------------------------------------------
// 3. Web Crypto HS256 JWT Token Engine (Player Stateless Sessions)
// -----------------------------------------------------------------------------
async function getHmacKey(secret, usages) {
  const enc = new TextEncoder();
  return await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    usages
  );
}

export async function signUserJwt(customPayload, secret) {
  const header = { alg: 'HS256', typ: 'JWT' };
  const now = Math.floor(Date.now() / 1000);

  const payload = {
    iss: 'lmod-vault-auth',
    role: 'player',
    iat: now,
    exp: now + TOKEN_TTL_SECONDS,
    ...customPayload
  };

  const encodedHeader = base64UrlEncode(JSON.stringify(header));
  const encodedPayload = base64UrlEncode(JSON.stringify(payload));
  const message = `${encodedHeader}.${encodedPayload}`;

  const key = await getHmacKey(secret, ['sign']);
  const signatureBuffer = await crypto.subtle.sign(
    'HMAC',
    key,
    new TextEncoder().encode(message)
  );

  const encodedSignature = base64UrlEncode(signatureBuffer);
  return `${message}.${encodedSignature}`;
}

export async function verifyUserJwt(token, secret) {
  if (!token || typeof token !== 'string') {
    return { valid: false, error: 'Token missing or invalid' };
  }

  const parts = token.trim().split('.');
  if (parts.length !== 3) {
    return { valid: false, error: 'Malformed token structure' };
  }

  const [encodedHeader, encodedPayload, encodedSignature] = parts;

  try {
    const key = await getHmacKey(secret, ['verify']);
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

    const payload = JSON.parse(base64UrlDecode(encodedPayload));
    const now = Math.floor(Date.now() / 1000);

    if (payload.exp && payload.exp < now) {
      return { valid: false, error: 'Token has expired', expired: true };
    }

    if (payload.role !== 'player' && payload.role !== 'user' && payload.role !== 'super_admin') {
      return { valid: false, error: 'Invalid token role' };
    }

    return { valid: true, payload };
  } catch (err) {
    return { valid: false, error: err.message };
  }
}

export function extractUserToken(request) {
  // 1. Authorization: Bearer <token>
  const authHeader = request.headers.get('Authorization') || request.headers.get('authorization');
  if (authHeader && authHeader.toLowerCase().startsWith('bearer ')) {
    return authHeader.slice(7).trim();
  }

  // 2. Custom header: X-Player-Token
  const customHeader = request.headers.get('x-player-token') || request.headers.get('X-Player-Token');
  if (customHeader) {
    return customHeader.trim();
  }

  // 3. Cookie header: lmod_player_token
  const cookieHeader = request.headers.get('Cookie') || request.headers.get('cookie');
  if (cookieHeader) {
    const match = cookieHeader.match(/lmod_player_token=([^;]+)/);
    if (match) return decodeURIComponent(match[1].trim());
  }

  return null;
}

// -----------------------------------------------------------------------------
// 4. Cryptographically Secure 6-Digit OTP Generator
// -----------------------------------------------------------------------------
export function generateOtpCode() {
  const array = new Uint32Array(1);
  crypto.getRandomValues(array);
  return String((array[0] % 900000) + 100000); // Guarantees 100000 - 999999
}

// -----------------------------------------------------------------------------
// 5. Cyber Dark HTML Email Template Generator (With Inline CSS & Custom Styling)
// -----------------------------------------------------------------------------
export function renderOtpEmailHtml({ code, purpose = 'login', email, options = {} }) {
  const purposeMap = {
    login: '账号快速登录 / 首次注册',
    change_email: '更换安全绑定邮箱',
    reset_pwd: '重置登录独立密码'
  };
  const purposeText = purposeMap[purpose] || '安全身份验证';

  const brandName = options.brandName || 'L-MOD Vault';
  const brandUrl = options.brandUrl || 'https://lmod-vault.pages.dev';
  const primaryColor = options.primaryColor || '#a855f7'; // Cyber Violet
  const accentColor = options.accentColor || '#38bdf8';   // Cyan
  const footerNote = options.footerNote || '全球单机游戏模组与避坑智库 · L-MOD 核心安全团队';

  return `
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${brandName} 安全验证码</title>
</head>
<body style="margin: 0; padding: 0; background-color: #07080c; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; -webkit-font-smoothing: antialiased;">
  
  <!-- Inbox Preheader Preview Text (Visible in push notifications and inbox snippets) -->
  <div style="display: none; font-size: 1px; color: #07080c; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
    【${brandName}】您的验证码是 ${code} (10分钟内有效)。如非本人操作请忽略此邮件。
  </div>

  <!-- Outer Full Width Wrapper -->
  <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #07080c; table-layout: fixed;">
    <tr>
      <td align="center" style="padding: 35px 15px 45px 15px;">
        
        <!-- Main Email Container -->
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 580px; background-color: #11131c; border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 18px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.85);">
          
          <!-- Top Neon Edge Gradient Accent Line -->
          <tr>
            <td height="3" style="background: linear-gradient(90deg, #9333ea 0%, #38bdf8 50%, #ec4899 100%); line-height: 3px; font-size: 3px;">&nbsp;</td>
          </tr>

          <!-- Header Section -->
          <tr>
            <td style="padding: 28px 32px 20px 32px; background-color: #141724; border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
              <table border="0" cellpadding="0" cellspacing="0" width="100%">
                <tr>
                  <td align="left">
                    <span style="font-size: 22px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;">
                      L-MOD <span style="color: ${primaryColor};">Vault</span>
                    </span>
                    <div style="font-size: 11px; color: #94a3b8; font-family: monospace; margin-top: 3px;">
                      Single-Player Game Mod & Sentinel Wiki
                    </div>
                  </td>
                  <td align="right">
                    <span style="display: inline-block; padding: 4px 10px; background-color: rgba(168, 85, 247, 0.18); border: 1px solid rgba(168, 85, 247, 0.45); border-radius: 9999px; font-size: 10px; font-weight: 700; color: #d8b4fe; font-family: monospace; text-transform: uppercase;">
                      OFFICIAL SENTINEL
                    </span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body Content -->
          <tr>
            <td style="padding: 32px 32px 24px 32px;">
              
              <!-- Greeting & Operation Badge -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 18px;">
                <tr>
                  <td>
                    <div style="font-size: 15px; color: #f1f5f9; font-weight: 600; margin-bottom: 6px;">
                      亲爱的单机玩家：
                    </div>
                    <div style="font-size: 13px; color: #94a3b8; line-height: 1.6;">
                      您正在进行【<strong style="color: #e2e8f0;">${purposeText}</strong>】操作。请在页面中输入下方 6 位数字验证码完成身份验证：
                    </div>
                  </td>
                </tr>
              </table>

              <!-- 6-Digit Monospace Highlight Box -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 24px 0;">
                <tr>
                  <td align="center" style="background-color: #08090f; border: 1px dashed rgba(168, 85, 247, 0.55); border-radius: 14px; padding: 26px 15px;">
                    <div style="font-family: 'JetBrains Mono', Consolas, Monaco, monospace; font-size: 40px; font-weight: 800; letter-spacing: 12px; color: #c084fc; text-indent: 12px; line-height: 1.1;">
                      ${code}
                    </div>
                    <div style="font-size: 12px; color: #94a3b8; margin-top: 12px; font-family: monospace;">
                      ⏱️ 验证码在 10 分钟内有效，请在有效期内输入
                    </div>
                  </td>
                </tr>
              </table>

              <!-- Security Precaution Banner -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                <tr>
                  <td style="background-color: rgba(239, 68, 68, 0.08); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 12px; padding: 14px 16px;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                      <tr>
                        <td style="font-size: 12px; color: #fca5a5; line-height: 1.6;">
                          🛡️ <strong>安全警示</strong>：L-MOD Vault 官方人员绝不会以任何理由向您索取此验证码。如非您本人操作，请勿理会本邮件，您的账号依然安全。
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <!-- Action Link Button -->
              <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 12px;">
                <tr>
                  <td align="center">
                    <a href="${brandUrl}" target="_blank" style="display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #9333ea 0%, #6366f1 100%); color: #ffffff; text-decoration: none; border-radius: 12px; font-size: 13px; font-weight: 700; box-shadow: 0 4px 15px rgba(147, 51, 234, 0.35);">
                      前往 L-MOD Vault 游戏智库空间 →
                    </a>
                  </td>
                </tr>
              </table>

            </td>
          </tr>

          <!-- Footer Section -->
          <tr>
            <td style="padding: 22px 32px; background-color: #0b0c13; border-top: 1px solid rgba(255, 255, 255, 0.06); text-align: center;">
              <div style="font-size: 12px; color: #64748b; line-height: 1.8;">
                <div>${footerNote}</div>
                <div>官方域名: <a href="${brandUrl}" target="_blank" style="color: ${primaryColor}; text-decoration: none;">lmod-vault.pages.dev</a> · 官方指令与补丁全息矩阵</div>
              </div>
            </td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>
  `.trim();
}

// -----------------------------------------------------------------------------
// 6. Resend API Mail Dispatcher (With Smart Sender Fallback & Sandbox Mode)
// -----------------------------------------------------------------------------
export async function sendOtpEmail({ env, db, toEmail, code, purpose = 'login' }) {
  let resendApiKey = env && env.RESEND_API_KEY;
  let fromEmail = env && env.EMAIL_FROM;
  let templateOptions = {};

  // Check database configuration override in system_settings if available
  if (db) {
    try {
      const row = await db.prepare("SELECT value FROM system_settings WHERE key = 'email_service_config'").first();
      if (row && row.value) {
        const conf = JSON.parse(row.value);
        if (!resendApiKey && conf.resend_api_key) resendApiKey = conf.resend_api_key;
        if (!fromEmail && conf.from_email) fromEmail = conf.from_email;
        if (conf.brand_name) templateOptions.brandName = conf.brand_name;
        if (conf.primary_color) templateOptions.primaryColor = conf.primary_color;
        if (conf.footer_note) templateOptions.footerNote = conf.footer_note;
      }
    } catch (e) {}
  }

  // Fallback to default if neither env nor database provided from_email
  if (!fromEmail) {
    fromEmail = 'L-MOD Vault <onboarding@resend.dev>';
  }

  const html = renderOtpEmailHtml({ code, purpose, email: toEmail, options: templateOptions });
  const subjectMap = {
    login: `【L-MOD Vault】登录验证码：${code} (10分钟内有效)`,
    change_email: `【L-MOD Vault】更换邮箱验证码：${code}`,
    reset_pwd: `【L-MOD Vault】重置密码验证码：${code}`
  };
  const subject = subjectMap[purpose] || `【L-MOD Vault】安全验证码：${code}`;

  // If live Resend API key is present, dispatch to Resend API
  if (resendApiKey) {
    try {
      // First attempt with configured fromEmail
      let res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${resendApiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: fromEmail,
          to: [toEmail],
          subject: subject,
          html: html
        })
      });

      let json = await res.json().catch(() => ({}));

      // If failed due to unverified custom domain in Resend, automatically retry with official onboarding@resend.dev
      if (!res.ok && json.message && (json.message.includes('not verified') || json.message.includes('domain')) && fromEmail !== 'L-MOD Vault <onboarding@resend.dev>') {
        console.warn(`[Resend Notice] Custom domain not verified yet (${fromEmail}). Retrying with default sandbox: L-MOD Vault <onboarding@resend.dev>`);
        
        res = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${resendApiKey}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            from: 'L-MOD Vault <onboarding@resend.dev>',
            to: [toEmail],
            subject: subject,
            html: html
          })
        });
        json = await res.json().catch(() => ({}));
      }

      if (res.ok) {
        return { success: true, provider: 'resend', id: json.id };
      } else {
        console.warn('[Resend API Error]', json);
        let userFriendlyError = '邮件发送失败，请稍后重试';
        const msg = json.message || '';

        if (msg.includes('only send testing emails to your own email address')) {
          userFriendlyError = '【Resend 测试阶段限制】未绑定独立域名时，Resend 仅允许向您注册 Resend 账号时填写的邮箱发信。若需向此邮箱发信，请在 resend.com/domains 绑定并验证您的独立域名。';
        } else if (msg.includes('Domain not verified') || msg.includes('not verified') || msg.includes('domain')) {
          userFriendlyError = '【发信域名未验证】当前配置的发信域名未在 Resend 通过 DNS 验证，请前往 resend.com/domains 完成解析验证。';
        } else if (res.status === 401 || msg.includes('API key')) {
          userFriendlyError = '【发信密钥无效】RESEND_API_KEY 验证失败，请检查 Cloudflare Pages 环境变量配置。';
        } else if (msg) {
          userFriendlyError = `邮件发送失败：${msg}`;
        }

        return {
          success: false,
          provider: 'resend',
          error: userFriendlyError,
          raw_message: msg,
          status: res.status
        };
      }
    } catch (err) {
      console.error('[Resend Dispatch Failed]', err);
      return {
        success: false,
        provider: 'resend',
        error: `邮件发送网络异常：${err.message || '请稍后重试'}`
      };
    }
  }

  // If no RESEND_API_KEY is configured:
  // In automated test environment (NODE_ENV=test or TEST_MOCK_MAIL=1)
  if (
    env.TEST_MOCK_MAIL === '1' ||
    env.NODE_ENV === 'test' ||
    (typeof process !== 'undefined' && process.env && process.env.NODE_ENV === 'test')
  ) {
    console.log(`[TEST MOCK] Mock email dispatch to ${toEmail}`);
    return {
      success: true,
      provider: 'test_mock'
    };
  }

  // Production without RESEND_API_KEY configured:
  return {
    success: false,
    provider: 'none',
    error: '系统未检测到邮件发信密钥 (RESEND_API_KEY)。请在 Cloudflare Pages 设置环境变量或在后台配置邮件服务。'
  };
}
