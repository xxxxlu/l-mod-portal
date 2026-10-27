/**
 * Cloudflare Pages Function: GET /api/v1/admin/me
 * Station Master Session Verification & System Health
 */

export async function onRequestGet(context) {
  const { env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  const admin = data?.admin || { username: '老L·站长', role: 'super_admin' };

  try {
    let stats = {
      games_count: 0,
      commands_count: 0,
      feedback_pending: 0,
      emergency_broadcast: null
    };

    if (db) {
      const gameRes = await db.prepare('SELECT count(*) as cnt FROM games').first();
      const cmdRes = await db.prepare('SELECT count(*) as cnt FROM console_commands').first();
      const fbRes = await db.prepare('SELECT count(*) as cnt FROM community_feedback WHERE status = "pending"').first();
      const broadcastRes = await db.prepare('SELECT value FROM system_settings WHERE key = "emergency_broadcast"').first();

      stats.games_count = gameRes?.cnt || 0;
      stats.commands_count = cmdRes?.cnt || 0;
      stats.feedback_pending = fbRes?.cnt || 0;
      if (broadcastRes?.value) {
        try {
          stats.emergency_broadcast = JSON.parse(broadcastRes.value);
        } catch (e) {}
      }
    }

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        admin,
        status: 'online',
        edge_runtime: 'Cloudflare Pages / V8 Edge',
        timestamp: new Date().toISOString(),
        system_stats: stats
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to inspect admin session',
      details: err.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }
}
