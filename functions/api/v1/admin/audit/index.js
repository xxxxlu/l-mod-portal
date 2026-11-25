/**
 * Cloudflare Pages Function: GET /api/v1/admin/audit?page=1&page_size=30&action=all
 * Admin operation log (admin_audit_logs), newest first. IPs are masked, including inside details text.
 */

import { maskIp, maskIpsInText, json } from '../users/_mask.js';

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  try {
    const url = new URL(request.url);
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10) || 1);
    const pageSize = Math.min(100, Math.max(10, parseInt(url.searchParams.get('page_size') || '30', 10) || 30));
    const action = (url.searchParams.get('action') || 'all').slice(0, 64);

    const where = action !== 'all' ? 'WHERE action = ?1' : '';
    const params = action !== 'all' ? [action] : [];

    const [totalRow, rows, actions] = await Promise.all([
      db.prepare(`SELECT count(*) AS total FROM admin_audit_logs ${where}`).bind(...params).first(),
      db.prepare(
        `SELECT id, action, entity, entity_id, details, admin_user, client_ip, created_at
         FROM admin_audit_logs ${where}
         ORDER BY id DESC LIMIT ${pageSize} OFFSET ${(page - 1) * pageSize}`
      ).bind(...params).all(),
      db.prepare('SELECT action, count(*) AS count FROM admin_audit_logs GROUP BY action ORDER BY count DESC').all()
    ]);

    const total = (totalRow && totalRow.total) || 0;
    return json({
      code: 0,
      message: 'success',
      data: {
        page,
        page_size: pageSize,
        total,
        total_pages: Math.ceil(total / pageSize),
        actions: actions.results || [],
        items: (rows.results || []).map(r => ({
          ...r,
          client_ip: maskIp(r.client_ip),
          details: maskIpsInText(r.details)
        }))
      }
    });
  } catch (err) {
    return json({ code: 50000, message: 'Failed to read audit log', details: err.message }, 500);
  }
}
