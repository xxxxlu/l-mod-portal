/**
 * Cloudflare Pages Function: /api/v1/community/feedback
 * Player bug reports & mod feedback endpoint with strict sanitization
 */

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  try {
    const body = await request.json();
    const { game_id, category, content, player_nickname } = body;

    if (!content || typeof content !== 'string' || content.trim().length === 0) {
      return new Response(JSON.stringify({
        code: 40000,
        message: 'Feedback content cannot be empty'
      }), { status: 400 });
    }

    const country = request.headers.get('cf-ipcountry') || 'Unknown';
    const sanitizedGameId = game_id ? String(game_id).slice(0, 64) : null;
    const sanitizedCategory = ['bug_report', 'mod_request', 'comment'].includes(category) ? category : 'bug_report';
    const sanitizedContent = content.trim().slice(0, 1000);
    const sanitizedNickname = (player_nickname || '单机玩家').trim().slice(0, 50);

    if (db) {
      await db.prepare(
        `INSERT INTO community_feedback (game_id, category, content, player_nickname, player_ip_country)
         VALUES (?, ?, ?, ?, ?)`
      ).bind(
        sanitizedGameId,
        sanitizedCategory,
        sanitizedContent,
        sanitizedNickname,
        country
      ).run();

      return new Response(JSON.stringify({
        code: 0,
        message: 'success',
        data: {
          submitted: true,
          notice: '感谢反馈！老L智库实验室已收录排查。'
        }
      }), {
        headers: { 'Content-Type': 'application/json; charset=utf-8' }
      });
    }

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: { submitted: true, notice: 'Feedback received (staging mode)' }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to process feedback',
      details: err.message
    }), { status: 500 });
  }
}
