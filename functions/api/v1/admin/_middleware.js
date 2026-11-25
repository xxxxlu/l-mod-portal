/**
 * Cloudflare Pages Function Middleware: /api/v1/admin/*
 * Zero Trust Security Perimeter & Admin JWT Authenticator
 */

import { verifyAdminJwt, getJwtSecret, extractAdminToken, adminNotConfiguredResponse } from './_auth.js';

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const pathname = url.pathname;

  // 1. Allow Preflight OPTIONS
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-admin-token',
        'Access-Control-Max-Age': '86400'
      }
    });
  }

  // 2. 没配 JWT 密钥（或配的是仓库里公开过的值）时，整个后台不可用，登录接口也一样
  const jwtSecret = getJwtSecret(env);
  if (!jwtSecret) {
    return adminNotConfiguredResponse('没有配置 ADMIN_JWT_SECRET');
  }

  // 3. Allow Admin Login Endpoint to pass through
  if (pathname.endsWith('/admin/login')) {
    return await next();
  }

  // 3. Admin JWT Token Extraction & Verification
  const token = extractAdminToken(request);
  if (!token) {
    return new Response(JSON.stringify({
      code: 40101,
      message: '站长特权通道拒绝访问：缺少管理员身份凭据 (Missing Bearer Token)',
      error_type: 'UNAUTHORIZED_ADMIN'
    }), {
      status: 401,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }

  const result = await verifyAdminJwt(token, jwtSecret);

  if (!result.valid) {
    return new Response(JSON.stringify({
      code: 40301,
      message: `站长鉴权失败：${result.error || '凭证无效或已失效'}`,
      error_type: 'FORBIDDEN_ADMIN_ACCESS',
      expired: Boolean(result.expired)
    }), {
      status: 403,
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }

  // Inject admin context into downstream request handlers
  context.data = context.data || {};
  context.data.admin = result.payload;

  return await next();
}
