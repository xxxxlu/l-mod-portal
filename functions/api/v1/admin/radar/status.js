/**
 * Cloudflare Pages Function: GET /api/v1/admin/radar/status
 * Steam Patch Radar Sentinel Mission Control & 24h Audit Logs
 */

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    // 1. Compatibility metrics
    const statusCounts = await db.prepare(
      'SELECT compatibility_status, count(*) as count FROM games GROUP BY compatibility_status'
    ).all();

    const counts = { green: 0, yellow: 0, red: 0, total: 100 };
    (statusCounts.results || []).forEach(r => {
      if (r.compatibility_status in counts) counts[r.compatibility_status] = r.count;
    });

    // 2. Recent 20 Patch Radar logs
    const logsRes = await db.prepare(`
      SELECT prl.id, prl.game_id, prl.patch_title, prl.patch_date, prl.build_id,
             prl.status, prl.risk_title, prl.risk_desc, prl.emergency_broadcast, prl.checked_at,
             g.title as game_title, g.title_zh as game_title_zh, g.steam_app_id
      FROM patch_radar_logs prl
      LEFT JOIN games g ON prl.game_id = g.id
      ORDER BY prl.checked_at DESC, prl.id DESC
      LIMIT 20
    `).all();

    // 3. Sentinel Config & Schedule
    const sentinelConfigRow = await db.prepare(
      'SELECT value FROM system_settings WHERE key = "sentinel_config"'
    ).first();

    let sentinelConfig = {
      auto_check_interval_hours: 6,
      flagships_only: false,
      last_scan_at: new Date().toISOString(),
      notify_on_break: true
    };

    if (sentinelConfigRow?.value) {
      try { sentinelConfig = JSON.parse(sentinelConfigRow.value); } catch (e) {}
    }

    // 4. Emergency broadcast status
    const broadcastRow = await db.prepare(
      'SELECT value FROM system_settings WHERE key = "emergency_broadcast"'
    ).first();
    let emergencyBroadcast = null;
    if (broadcastRow?.value) {
      try { emergencyBroadcast = JSON.parse(broadcastRow.value); } catch (e) {}
    }

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        radar_metrics: counts,
        sentinel_scheduler: sentinelConfig,
        emergency_broadcast: emergencyBroadcast,
        recent_logs: logsRes.results || [],
        total_logs_count: (logsRes.results || []).length
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
      message: 'Failed to retrieve radar status',
      details: err.message
    }), { status: 500 });
  }
}
