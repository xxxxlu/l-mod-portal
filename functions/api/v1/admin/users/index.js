/**
 * Cloudflare Pages Function: GET /api/v1/admin/users?page=1&page_size=20&q=
 * Read-only player list: masked email, sign-up / last login, favorites and radar subscription counts.
 * `q` matches nickname or email (the match runs on the full value; the response is still masked).
 */

import { maskEmail, json } from './_mask.js';

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  try {
    const url = new URL(request.url);
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10) || 1);
    const pageSize = Math.min(100, Math.max(5, parseInt(url.searchParams.get('page_size') || '20', 10) || 20));
    const q = (url.searchParams.get('q') || '').trim().slice(0, 50);

    const where = q ? 'WHERE (u.nickname LIKE ?1 OR u.email LIKE ?1)' : '';
    const params = q ? [`%${q}%`] : [];

    const totalRow = await db.prepare(`SELECT count(*) AS total FROM users u ${where}`).bind(...params).first();
    const { results } = await db.prepare(
      `SELECT u.id, u.provider, u.nickname, u.email, u.status, u.created_at, u.last_login_at,
              (u.password_hash IS NOT NULL AND u.password_hash != '') AS has_password,
              (SELECT count(*) FROM user_favorites f WHERE f.user_id = u.id) AS favorites,
              (SELECT count(*) FROM user_radar_subscriptions s WHERE s.user_id = u.id) AS subscriptions
       FROM users u ${where}
       ORDER BY u.created_at DESC
       LIMIT ${pageSize} OFFSET ${(page - 1) * pageSize}`
    ).bind(...params).all();

    const summary = await db.prepare(
      `SELECT (SELECT count(*) FROM users) AS users,
              (SELECT count(*) FROM user_favorites) AS favorites,
              (SELECT count(DISTINCT user_id) FROM user_favorites) AS users_with_favorites,
              (SELECT count(*) FROM user_radar_subscriptions) AS subscriptions,
              (SELECT count(DISTINCT user_id) FROM user_radar_subscriptions) AS users_with_subscriptions`
    ).first();

    const total = (totalRow && totalRow.total) || 0;
    return json({
      code: 0,
      message: 'success',
      data: {
        page,
        page_size: pageSize,
        total,
        total_pages: Math.ceil(total / pageSize),
        summary,
        items: (results || []).map(u => ({
          id: u.id,
          provider: u.provider,
          nickname: u.nickname,
          email_masked: maskEmail(u.email),
          status: u.status || 'active',
          has_password: Boolean(u.has_password),
          created_at: u.created_at,
          last_login_at: u.last_login_at,
          favorites: u.favorites || 0,
          subscriptions: u.subscriptions || 0
        }))
      }
    });
  } catch (err) {
    return json({ code: 50000, message: 'Failed to list users', details: err.message }, 500);
  }
}
