/**
 * Cloudflare Pages Function: /api/v1/ai/context
 * High-density prompt context synthesizer for Lao-L AI Copilot
 */

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  try {
    const { query, game_id } = await request.json();
    if (!query || typeof query !== 'string') {
      return new Response(JSON.stringify({ code: 40000, message: 'Missing query parameter' }), { status: 400 });
    }

    const cleanQuery = query.trim().slice(0, 100);
    const cleanGameId = game_id && /^[a-z0-9-]+$/.test(game_id) ? game_id : null;

    if (!db) {
      return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
    }

    let gameInfo = null;
    if (cleanGameId) {
      gameInfo = await db.prepare(
        `SELECT id, title, title_zh, console_shortcut, verified_patch, latest_steam_patch,
                compatibility_status, radar_risk_title, pitfall_note
         FROM games
         WHERE id = ?`
      ).bind(cleanGameId).first();
    }

    // Match top 5 commands matching query keywords
    const keywords = cleanQuery.split(/\s+/).filter(k => k.length > 1).slice(0, 3);
    let matchedCommands = [];

    if (keywords.length > 0) {
      let conditions = [];
      let params = [];

      if (cleanGameId) {
        conditions.push('game_id = ?');
        params.push(cleanGameId);
      }

      const orTerms = keywords.map(() => '(name_zh LIKE ? OR name_en LIKE ? OR description LIKE ? OR code LIKE ?)').join(' OR ');
      conditions.push(`(${orTerms})`);

      keywords.forEach(kw => {
        const pattern = `%${kw}%`;
        params.push(pattern, pattern, pattern, pattern);
      });

      const sql = `
        SELECT game_id, name_zh, name_en, code, description, syntax_type
        FROM console_commands
        WHERE ${conditions.join(' AND ')}
        LIMIT 5
      `;
      const { results } = await db.prepare(sql).bind(...params).all();
      matchedCommands = results || [];
    }

    // Synthesize context block for LLM
    const contextPrompt = {
      game_focus: gameInfo ? {
        title: gameInfo.title_zh || gameInfo.title,
        shortcut: gameInfo.console_shortcut,
        patch_status: gameInfo.compatibility_status,
        pitfall: gameInfo.pitfall_note
      } : null,
      retrieved_commands: matchedCommands.map(c => ({
        name: c.name_zh || c.name_en,
        code: c.code,
        type: c.syntax_type,
        desc: c.description
      }))
    };

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        query: cleanQuery,
        context: contextPrompt
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({ code: 50000, message: 'Failed to synthesize AI context', details: err.message }), { status: 500 });
  }
}
