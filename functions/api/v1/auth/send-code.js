/**
 * Cloudflare Pages Function: POST /api/v1/auth/send-code
 * Player Email OTP Dispatcher with Sliding Window Risk Control, 60s Cooldown & Self-Healing Schema
 */

import { getDatabase, generateOtpCode, sendOtpEmail, ensureAuthSchema } from './_crypto.js';

const EMAIL_REGEX = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;
const IP_HOURLY_LIMIT = 15;
const COOLDOWN_SECONDS = 60;

async function executeSendCode(context) {
  const { request, env } = context;
  const db = getDatabase(env);

  const body = await request.clone().json().catch(() => ({}));
  const rawEmail = (body.email || '').trim().toLowerCase();
  const rawPurpose = (body.purpose || 'login').trim().toLowerCase();

  // 1. Email Format Validation
  if (!rawEmail || !EMAIL_REGEX.test(rawEmail) || rawEmail.length > 128) {
    return new Response(JSON.stringify({
      code: 40001,
      message: '请输入格式正确的有效电子邮箱地址'
    }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }

  // 2. Purpose Validation
  const validPurposes = ['login', 'change_email', 'reset_pwd'];
  const purpose = validPurposes.includes(rawPurpose) ? rawPurpose : 'login';

  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  // 3. IP Sliding Window Hourly Rate Limiting
  const ipCheck = await db.prepare(
    `SELECT count(*) as count FROM email_verification_codes 
     WHERE client_ip = ? AND created_at >= datetime('now', '-1 hour')`
  ).bind(clientIP).first().catch(() => null);

  if (ipCheck && ipCheck.count >= IP_HOURLY_LIMIT) {
    return new Response(JSON.stringify({
      code: 42901,
      message: '当前 IP 请求验证码过于频繁，请 1 小时后再试。'
    }), { status: 429, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }

  // 4. Same Email 60s Cooldown Check
  const recentCode = await db.prepare(
    `SELECT created_at, (strftime('%s', 'now') - strftime('%s', created_at)) as elapsed_sec 
     FROM email_verification_codes 
     WHERE email = ? AND purpose = ? 
     ORDER BY id DESC LIMIT 1`
  ).bind(rawEmail, purpose).first().catch(() => null);

  if (recentCode && recentCode.elapsed_sec !== null && recentCode.elapsed_sec < COOLDOWN_SECONDS) {
    const waitTime = COOLDOWN_SECONDS - recentCode.elapsed_sec;
    return new Response(JSON.stringify({
      code: 42902,
      message: `发送过于频繁，请等待 ${waitTime} 秒后再试`,
      data: { cooldown_seconds: waitTime }
    }), { status: 429, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }

  // 5. If purpose is change_email, verify new email is not already taken
  if (purpose === 'change_email') {
    const existingUser = await db.prepare(
      'SELECT id FROM users WHERE email = ? LIMIT 1'
    ).bind(rawEmail).first().catch(() => null);

    if (existingUser) {
      return new Response(JSON.stringify({
        code: 40002,
        message: '该邮箱已被其他玩家账号绑定，请使用其他邮箱'
      }), { status: 400, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
    }
  }

  // 6. Generate 6-Digit OTP Code
  const code = generateOtpCode();

  // 7. Store into D1 Database (Expires in 10 minutes)
  await db.prepare(
    `INSERT INTO email_verification_codes 
     (email, code, purpose, expires_at, attempts, is_used, client_ip, created_at)
     VALUES (?, ?, ?, datetime('now', '+10 minutes'), 0, 0, ?, CURRENT_TIMESTAMP)`
  ).bind(rawEmail, code, purpose, clientIP).run();

  // 8. Dispatch Email via Resend
  const mailResult = await sendOtpEmail({
    env,
    db,
    toEmail: rawEmail,
    code,
    purpose
  });

  // If email dispatch failed, clean up the inserted code so player isn't stuck in 60s cooldown
  if (!mailResult.success) {
    await db.prepare(
      `DELETE FROM email_verification_codes WHERE email = ? AND code = ? AND is_used = 0`
    ).bind(rawEmail, code).run().catch(() => {});

    return new Response(JSON.stringify({
      code: 40003,
      message: mailResult.error || '邮件发送失败，请稍后重试',
      details: mailResult.raw_message || undefined
    }), {
      status: 400,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }

  return new Response(JSON.stringify({
    code: 0,
    message: '验证码已发送至您的邮箱，请在 10 分钟内填写',
    data: {
      cooldown_seconds: COOLDOWN_SECONDS,
      provider: mailResult.provider
    }
  }), {
    status: 200,
    headers: { 'Content-Type': 'application/json; charset=utf-8' }
  });
}

export async function onRequestPost(context) {
  const { env } = context;
  const db = getDatabase(env);

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }

  try {
    return await executeSendCode(context);
  } catch (err) {
    // Self-healing: if remote D1 hasn't had email_verification_codes table created yet, auto-create it and retry
    if (err.message && (err.message.includes('no such table') || err.message.includes('SQLITE_ERROR'))) {
      await ensureAuthSchema(db);
      try {
        return await executeSendCode(context);
      } catch (retryErr) {
        return new Response(JSON.stringify({
          code: 50000,
          message: '发送验证码失败，请稍后重试',
          details: retryErr.message
        }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }
    }

    return new Response(JSON.stringify({
      code: 50000,
      message: '发送验证码失败，请稍后重试',
      details: err.message
    }), { status: 500, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
  }
}
