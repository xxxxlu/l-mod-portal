/**
 * Cloudflare Pages Function Middleware: /api/v1/*
 * Global API Governance, Edge Rate Limiting, Security Headers & Error Envelope
 */

const ALLOWED_ORIGINS = [
  'https://lmod-vault.pages.dev',
  'https://lmod.gg',
  'http://localhost:8788',
  'http://127.0.0.1:8788',
  'http://localhost:3000',
  'http://127.0.0.1:5500'
];

// In-Memory sliding window rate limiting per edge instance
const IP_REQUEST_LOG = new Map();
const RATE_LIMIT_WINDOW_MS = 60 * 1000; // 1 minute window

const RATE_LIMITS = {
  DEFAULT: 120,      // standard read API: 120 req/min
  FEEDBACK: 10,      // feedback submission: 10 req/min
  TELEMETRY: 240     // lightweight analytics: 240 req/min
};

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';
  const rayId = request.headers.get('cf-ray') || `lmod-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
  const origin = request.headers.get('Origin');

  // 1. CORS Dynamic Origin Validation
  let corsOrigin = '*';
  if (origin) {
    if (ALLOWED_ORIGINS.includes(origin) || origin.endsWith('.pages.dev')) {
      corsOrigin = origin;
    }
  }

  const baseHeaders = {
    'Access-Control-Allow-Origin': corsOrigin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Session-Id, X-Player-Token, x-player-token',
    'Access-Control-Max-Age': '86400',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'SAMEORIGIN',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    'X-Request-Id': rayId
  };

  // Handle preflight OPTIONS request
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: baseHeaders });
  }

  // 2. Edge Sliding Window IP Rate Limiting
  let limit = RATE_LIMITS.DEFAULT;
  if (url.pathname.includes('/feedback')) limit = RATE_LIMITS.FEEDBACK;
  if (url.pathname.includes('/telemetry')) limit = RATE_LIMITS.TELEMETRY;

  const now = Date.now();
  const segment = url.pathname.split('/')[4] || 'root';
  const clientKey = `${clientIP}:${segment}`;
  const record = IP_REQUEST_LOG.get(clientKey) || { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };

  if (now > record.resetAt) {
    record.count = 1;
    record.resetAt = now + RATE_LIMIT_WINDOW_MS;
  } else {
    record.count++;
  }
  IP_REQUEST_LOG.set(clientKey, record);

  // Periodic cleanup of expired cache to prevent memory creep
  if (IP_REQUEST_LOG.size > 5000) {
    for (const [k, v] of IP_REQUEST_LOG.entries()) {
      if (now > v.resetAt) IP_REQUEST_LOG.delete(k);
    }
  }

  if (record.count > limit) {
    return new Response(
      JSON.stringify({
        code: 42900,
        message: 'Too many requests. Please slow down and try again later.',
        error_type: 'RATE_LIMIT_EXCEEDED',
        request_id: rayId,
        timestamp: now
      }),
      {
        status: 429,
        headers: {
          ...baseHeaders,
          'Content-Type': 'application/json; charset=utf-8',
          'Retry-After': '60'
        }
      }
    );
  }

  // 3. Chain Downstream Handler with Error Protection
  try {
    const response = await next();
    
    // Merge base security headers into outgoing response
    const newHeaders = new Headers(response.headers);
    Object.entries(baseHeaders).forEach(([k, v]) => {
      if (!newHeaders.has(k)) newHeaders.set(k, v);
    });
    newHeaders.set('X-Request-Id', rayId);

    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: newHeaders
    });
  } catch (err) {
    return new Response(
      JSON.stringify({
        code: 50000,
        message: 'Internal edge server error.',
        details: err.message,
        request_id: rayId,
        timestamp: Date.now()
      }),
      {
        status: 500,
        headers: {
          ...baseHeaders,
          'Content-Type': 'application/json; charset=utf-8'
        }
      }
    );
  }
}
