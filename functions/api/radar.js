/**
 * Cloudflare Pages Function: /api/radar
 * Real-time Steam Patch Radar status API.
 */

export async function onRequestGet(context) {
  const { env } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'public, max-age=30, s-maxage=300'
  };

  try {
    if (env.DB) {
      const { results } = await env.DB.prepare(
        `SELECT id, rank, title, title_zh, steam_app_id, verified_patch, latest_steam_patch,
                compatibility_status, radar_risk_title, radar_risk_desc, radar_summary, pitfall_note
         FROM games
         WHERE steam_app_id IS NOT NULL
         ORDER BY rank ASC`
      ).all();

      const counts = { green: 0, yellow: 0, red: 0 };
      results.forEach(g => {
        if (g.compatibility_status in counts) {
          counts[g.compatibility_status]++;
        }
      });

      return new Response(JSON.stringify({
        updated_at: new Date().toISOString(),
        metrics: counts,
        total: results.length,
        games: results
      }), { headers: corsHeaders });
    }

    return new Response(JSON.stringify({
      status: 'active',
      notice: 'D1 binding pending. Live radar fallback to static public/radar.html'
    }), { headers: corsHeaders });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: corsHeaders });
  }
}
