/**
 * Cloudflare Pages Function: /api/v1/radar/overview
 * Steam Patch Radar Status Summary & Emergency Broadcast
 */

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const { results } = await db.prepare(
      `SELECT compatibility_status, count(*) as count
       FROM games
       GROUP BY compatibility_status`
    ).all();

    const counts = { green: 0, yellow: 0, red: 0 };
    (results || []).forEach(r => {
      if (r.compatibility_status in counts) {
        counts[r.compatibility_status] = r.count;
      }
    });

    // Fetch games with warnings (Yellow or Red)
    const alertGames = await db.prepare(
      `SELECT id, rank, title, title_zh, compatibility_status, verified_patch, latest_steam_patch, radar_risk_title, radar_risk_desc
       FROM games
       WHERE compatibility_status IN ('yellow', 'red')
       ORDER BY CASE compatibility_status WHEN 'red' THEN 1 WHEN 'yellow' THEN 2 ELSE 3 END, rank ASC`
    ).all();

    // Check emergency broadcast from system_settings
    let emergencyBroadcast = null;
    try {
      const bRow = await db.prepare('SELECT value FROM system_settings WHERE key = "emergency_broadcast"').first();
      if (bRow?.value) {
        emergencyBroadcast = JSON.parse(bRow.value);
      }
    } catch (e) {}

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        updated_at: new Date().toISOString(),
        metrics: counts,
        total_tracked: counts.green + counts.yellow + counts.red,
        active_alerts_count: alertGames.results ? alertGames.results.length : 0,
        active_alerts: alertGames.results || [],
        emergency_broadcast: emergencyBroadcast
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=60, s-maxage=300'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to retrieve radar overview',
      details: err.message
    }), { status: 500 });
  }
}
