/**
 * Cloudflare Pages Function: GET /api/v1/admin/analytics/overview
 * Real-time Telemetry & Analytics Overview Dashboard
 */

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    // 1. Core KPIs
    const [pvTotalRes, uvTotalRes, pvTodayRes, uvTodayRes] = await Promise.all([
      db.prepare('SELECT count(*) as count FROM telemetry_events').first(),
      db.prepare('SELECT count(DISTINCT session_id) as count FROM telemetry_events').first(),
      db.prepare("SELECT count(*) as count FROM telemetry_events WHERE DATE(created_at) = DATE('now')").first(),
      db.prepare("SELECT count(DISTINCT session_id) as count FROM telemetry_events WHERE DATE(created_at) = DATE('now')").first()
    ]);

    // 2. Events breakdown by type
    const eventTypesRes = await db.prepare(
      `SELECT event_type, count(*) as count
       FROM telemetry_events
       GROUP BY event_type
       ORDER BY count DESC`
    ).all();

    // 3. Top 10 Search Queries
    const topSearchesRes = await db.prepare(
      `SELECT target_payload as query, count(*) as count, MAX(created_at) as last_searched
       FROM telemetry_events
       WHERE event_type = 'search_query' AND target_payload IS NOT NULL AND target_payload != ''
       GROUP BY target_payload
       ORDER BY count DESC
       LIMIT 10`
    ).all();

    // 4. Top 10 Copied Console Commands
    const topCommandsRes = await db.prepare(
      `SELECT target_payload as code, game_id, count(*) as count
       FROM telemetry_events
       WHERE event_type = 'copy_code' AND target_payload IS NOT NULL AND target_payload != ''
       GROUP BY target_payload
       ORDER BY count DESC
       LIMIT 10`
    ).all();

    // 5. Top Downloaded .bat Packages
    const topDownloadsRes = await db.prepare(
      `SELECT target_payload as filename, game_id, count(*) as count
       FROM telemetry_events
       WHERE event_type = 'download_bat' AND target_payload IS NOT NULL AND target_payload != ''
       GROUP BY target_payload
       ORDER BY count DESC
       LIMIT 10`
    ).all();

    // 6. Client Country Distribution
    const countryRes = await db.prepare(
      `SELECT client_country, count(*) as count
       FROM telemetry_events
       WHERE client_country IS NOT NULL AND client_country != ''
       GROUP BY client_country
       ORDER BY count DESC
       LIMIT 10`
    ).all();

    // 7. Recent Days Activity Trend
    const trendRes = await db.prepare(
      `SELECT DATE(created_at) as date, count(*) as pv, count(DISTINCT session_id) as uv
       FROM telemetry_events
       GROUP BY DATE(created_at)
       ORDER BY date DESC
       LIMIT 7`
    ).all();

    const eventBreakdown = {};
    (eventTypesRes.results || []).forEach(r => {
      eventBreakdown[r.event_type] = r.count;
    });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        summary: {
          total_pv: pvTotalRes?.count || 0,
          total_uv: uvTotalRes?.count || 0,
          today_pv: pvTodayRes?.count || 0,
          today_uv: uvTodayRes?.count || 0,
          copy_code_count: eventBreakdown['copy_code'] || 0,
          download_bat_count: eventBreakdown['download_bat'] || 0,
          search_query_count: eventBreakdown['search_query'] || 0,
          ai_ask_count: eventBreakdown['ai_ask'] || 0,
          view_game_count: eventBreakdown['view_game'] || 0
        },
        event_breakdown: eventBreakdown,
        top_searches: topSearchesRes.results || [],
        top_commands: topCommandsRes.results || [],
        top_downloads: topDownloadsRes.results || [],
        country_distribution: countryRes.results || [],
        activity_trend: trendRes.results || [],
        generated_at: new Date().toISOString()
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
      message: 'Failed to aggregate telemetry metrics',
      details: err.message
    }), { status: 500 });
  }
}
