/**
 * Cloudflare Pages Function: /api/v1/ai/context
 * High-density prompt context synthesizer for Lao-L AI Copilot
 *
 * 雷达信息来自 public/radar_status.json 的 v2 结果（见 ../../_radar_status.js），不读 D1 的旧雷达列。
 * 没有 D1 时只是查不到游戏资料和指令，雷达部分照常返回。
 */

import { loadRadarStatus, radarEntry, radarContextFor } from '../../_radar_status.js';

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

    const radarStatus = cleanGameId ? await loadRadarStatus(context) : null;

    let gameInfo = null;
    let matchedCommands = [];
    let dbAvailable = Boolean(db);

    if (db) {
      try {
        if (cleanGameId) {
          gameInfo = await db.prepare(
            `SELECT id, title, title_zh, steam_app_id, console_shortcut, pitfall_note
             FROM games
             WHERE id = ?`
          ).bind(cleanGameId).first();
        }

        // Match top 5 commands matching query keywords
        const keywords = cleanQuery.split(/\s+/).filter(k => k.length > 1).slice(0, 3);
        if (keywords.length > 0) {
          const conditions = [];
          const params = [];

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
      } catch (e) {
        // D1 绑定在但表不在（例如本地空库）：按没有 D1 处理，雷达部分照常
        dbAvailable = false;
        gameInfo = null;
        matchedCommands = [];
      }
    }

    const entry = radarEntry(radarStatus, cleanGameId);
    let gameFocus = null;
    if (gameInfo || entry) {
      gameFocus = {
        title: gameInfo ? (gameInfo.title_zh || gameInfo.title) : (entry.titleZh || entry.title),
        shortcut: gameInfo ? gameInfo.console_shortcut : null,
        patch_status: entry ? entry.compatibilityStatus : null,
        radar: radarContextFor(cleanGameId, radarStatus, gameInfo ? gameInfo.steam_app_id : undefined),
        pitfall: gameInfo ? gameInfo.pitfall_note : null
      };
    }

    // Synthesize context block for LLM
    const contextPrompt = {
      game_focus: gameFocus,
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
        context: contextPrompt,
        sources: {
          game_vault: dbAvailable ? 'd1' : null,
          radar: radarStatus ? 'radar_status.json' : null
        }
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
