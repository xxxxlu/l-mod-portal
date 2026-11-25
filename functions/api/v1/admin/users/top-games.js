/**
 * Cloudflare Pages Function: GET /api/v1/admin/users/top-games
 * Games ranked by how many players favorited them, and by radar subscriptions (distinct players).
 */

import { json } from './_mask.js';

export async function onRequestGet(context) {
  const db = context.env.DB || context.env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  try {
    const [fav, subs] = await Promise.all([
      db.prepare(
        `SELECT f.game_id, g.title, g.title_zh, count(*) AS players, MAX(f.created_at) AS last_at
         FROM user_favorites f LEFT JOIN games g ON g.id = f.game_id
         GROUP BY f.game_id ORDER BY players DESC, last_at DESC LIMIT 20`
      ).all(),
      db.prepare(
        `SELECT s.game_id, g.title, g.title_zh, count(DISTINCT s.user_id) AS players, MAX(s.created_at) AS last_at
         FROM user_radar_subscriptions s LEFT JOIN games g ON g.id = s.game_id
         GROUP BY s.game_id ORDER BY players DESC, last_at DESC LIMIT 20`
      ).all()
    ]);
    const shape = r => ({ game_id: r.game_id, title: r.title_zh || r.title || null, players: r.players, last_at: r.last_at });
    return json({
      code: 0,
      message: 'success',
      data: {
        favorites: (fav.results || []).map(shape),
        subscriptions: (subs.results || []).map(shape)
      }
    });
  } catch (err) {
    return json({ code: 50000, message: 'Failed to rank games', details: err.message }, 500);
  }
}
