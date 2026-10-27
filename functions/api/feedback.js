/**
 * Cloudflare Pages Function: /api/feedback
 * Player Bug Report & Mod Request Submission API.
 */

export async function onRequestPost(context) {
  const { request, env } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json; charset=utf-8'
  };

  try {
    const body = await request.json();
    const { game_id, category, content, player_nickname } = body;

    if (!content || content.trim().length === 0) {
      return new Response(JSON.stringify({ error: 'Feedback content cannot be empty' }), {
        status: 400,
        headers: corsHeaders
      });
    }

    // IP geolocation from Cloudflare Headers
    const country = request.headers.get('cf-ipcountry') || 'Unknown';

    if (env.DB) {
      await env.DB.prepare(
        `INSERT INTO community_feedback (game_id, category, content, player_nickname, player_ip_country)
         VALUES (?, ?, ?, ?, ?)`
      ).bind(
        game_id || null,
        category || 'bug_report',
        content.trim().slice(0, 1000), // Max 1000 chars
        (player_nickname || '单机玩家').trim().slice(0, 50),
        country
      ).run();

      return new Response(JSON.stringify({
        success: true,
        message: '感谢反馈！老L智库实验室已收录排查。'
      }), { headers: corsHeaders });
    }

    // Fallback acknowledgment
    return new Response(JSON.stringify({
      success: true,
      notice: 'Received feedback (D1 logging pending).'
    }), { headers: corsHeaders });

  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: corsHeaders });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    }
  });
}
