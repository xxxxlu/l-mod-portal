/**
 * Cloudflare Pages Function: GET /api/v1/admin/feedback?status=all|pending|verified|resolved&category=&page=&page_size=
 * Player bug reports & feedback, with the admin's handling note (migration v6: admin_note / handled_at).
 *
 * Emails: the list shows a masked address; `contact_email` is only set when the player left an address,
 * and the admin UI uses it solely as a mailto: link.
 * Seed rows: ids 101–105 dated before 2026-10-28 were inserted by migration_v3 and are flagged `is_seed`.
 */

import { maskEmail } from '../users/_mask.js';

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  try {
    const url = new URL(request.url);
    const status = url.searchParams.get('status');
    const category = url.searchParams.get('category');
    const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10) || 1);
    const pageSize = Math.min(50, Math.max(5, parseInt(url.searchParams.get('page_size') || '20', 10) || 20));
    const offset = (page - 1) * pageSize;

    const conditions = [];
    const params = [];
    if (status && status !== 'all') { conditions.push('cf.status = ?'); params.push(status); }
    if (category && category !== 'all') { conditions.push('cf.category = ?'); params.push(category); }
    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    const countRes = await db.prepare(`SELECT count(*) as total FROM community_feedback cf ${whereClause}`).bind(...params).first();
    const total = countRes?.total || 0;

    const listSql = (withNote) => `
      SELECT cf.id, cf.game_id, cf.category, cf.content, cf.player_nickname,
             cf.player_ip_country, cf.status, cf.created_at, cf.user_id, cf.player_email,
             ${withNote ? 'cf.admin_note, cf.handled_at,' : 'NULL AS admin_note, NULL AS handled_at,'}
             g.title as game_title, g.title_zh as game_title_zh,
             u.email as verified_email, u.nickname as registered_nickname
      FROM community_feedback cf
      LEFT JOIN games g ON cf.game_id = g.id
      LEFT JOIN users u ON cf.user_id = u.id
      ${whereClause}
      ORDER BY cf.id DESC
      LIMIT ? OFFSET ?`;

    let results;
    let notesAvailable = true;
    try {
      ({ results } = await db.prepare(listSql(true)).bind(...params, pageSize, offset).all());
    } catch (err) {
      // Before migration v6 the note columns do not exist yet; still show the list
      if (!/no such column/i.test(err.message || '')) throw err;
      notesAvailable = false;
      ({ results } = await db.prepare(listSql(false)).bind(...params, pageSize, offset).all());
    }

    const statusCounts = await db.prepare('SELECT status, count(*) as count FROM community_feedback GROUP BY status').all();
    const counts = { pending: 0, verified: 0, resolved: 0 };
    (statusCounts.results || []).forEach(r => { counts[r.status] = r.count; });

    return json({
      code: 0,
      message: 'success',
      data: {
        page,
        page_size: pageSize,
        total,
        total_pages: Math.ceil(total / pageSize),
        status_counts: counts,
        notes_available: notesAvailable,
        items: (results || []).map(r => {
          const email = r.verified_email || r.player_email || null;
          return {
            id: r.id,
            game_id: r.game_id,
            game_title: r.game_title_zh || r.game_title || null,
            category: r.category,
            content: r.content,
            player_nickname: r.player_nickname || r.registered_nickname || null,
            player_ip_country: r.player_ip_country,
            status: r.status,
            created_at: r.created_at,
            admin_note: r.admin_note,
            handled_at: r.handled_at,
            is_registered: Boolean(r.user_id || r.verified_email),
            email_masked: maskEmail(email),
            contact_email: email,
            is_seed: r.id >= 101 && r.id <= 105 && String(r.created_at || '') < '2026-10-28'
          };
        })
      }
    });
  } catch (err) {
    return json({ code: 50000, message: 'Failed to fetch community feedback', details: err.message }, 500);
  }
}
