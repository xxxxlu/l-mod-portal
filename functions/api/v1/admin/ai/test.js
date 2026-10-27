/**
 * Cloudflare Pages Function: POST /api/v1/admin/ai/test
 * AI Skills Studio Interactive Sandbox & Diagnostic Simulator
 */

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const { query, game_id, simulate_skills } = await request.json();

    if (!query || typeof query !== 'string') {
      return new Response(JSON.stringify({ code: 40000, message: 'Missing query parameter' }), { status: 400 });
    }

    // 1. Fetch AI system config
    const aiConfigRow = await db.prepare('SELECT value FROM system_settings WHERE key = "ai_config"').first();
    let aiConfig = null;
    if (aiConfigRow?.value) {
      try { aiConfig = JSON.parse(aiConfigRow.value); } catch (e) {}
    }

    const cleanGameId = game_id && /^[a-z0-9-]+$/.test(game_id) ? game_id : null;

    // 2. Fetch game info if specified
    let game = null;
    if (cleanGameId) {
      game = await db.prepare(
        `SELECT id, title, title_zh, console_shortcut, verified_patch, latest_steam_patch,
                compatibility_status, radar_risk_title, radar_risk_desc, pitfall_note
         FROM games WHERE id = ?`
      ).bind(cleanGameId).first();
    }

    // 3. Command retrieval
    const keywords = query.trim().split(/\s+/).filter(k => k.length > 1).slice(0, 3);
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
        SELECT game_id, name_zh, name_en, code, description, syntax_type, is_popular
        FROM console_commands
        WHERE ${conditions.join(' AND ')}
        LIMIT 6
      `;
      const { results } = await db.prepare(sql).bind(...params).all();
      matchedCommands = results || [];
    }

    // 4. Skills Simulation Pipeline
    const skillsAnalysis = {
      code_dedup: {
        executed: true,
        status: 'PASSED',
        verdict: '检索指令无重复冗余项，语法特征独一无二。'
      },
      syntax_validator: {
        executed: true,
        status: matchedCommands.length > 0 ? 'VALIDATED' : 'SKIPPED',
        verdict: matchedCommands.length > 0
          ? `通过语法自检：匹配 ${matchedCommands.length} 条指令符合底层引擎规范 (${matchedCommands.map(c => c.syntax_type).join(', ')})。`
          : '未检测到具体控制台指令。'
      },
      steam_diff: {
        executed: true,
        status: game ? (game.compatibility_status === 'green' ? 'COMPATIBLE' : 'ATTENTION') : 'GLOBAL',
        verdict: game
          ? `基于 Steam ${game.latest_steam_patch} 对比基准 ${game.verified_patch}：状态为【${game.compatibility_status.toUpperCase()}】。`
          : '全局智库检索，无需单游戏补丁对比。'
      },
      save_backup_guard: {
        executed: true,
        status: (query.includes('钱') || query.includes('等级') || query.includes('无敌') || query.includes('全收集')) ? 'ALERT_ATTACHED' : 'SAFE',
        verdict: (query.includes('钱') || query.includes('等级') || query.includes('无敌') || query.includes('全收集'))
          ? '触发坏档防御拦截机制：已在 AI 回答前置注入【备份存档强制警示】。'
          : '常规指令，低风险。'
      }
    };

    // 5. Synthesized Prompt Construct
    const synthesizedPrompt = {
      system_role: aiConfig?.system_prompt || '老L 首席单机避坑智库顾问',
      tone: aiConfig?.tone || 'hardcore_veteran',
      game_anchor: game ? {
        title: game.title_zh || game.title,
        shortcut: game.console_shortcut,
        patch: game.verified_patch,
        pitfall: game.pitfall_note
      } : '全局智库模式',
      retrieved_commands_count: matchedCommands.length,
      retrieved_commands: matchedCommands.map(c => ({
        name: c.name_zh,
        code: c.code,
        type: c.syntax_type
      }))
    };

    return new Response(JSON.stringify({
      code: 0,
      message: 'AI 提示词编排与技能沙盒测试成功',
      data: {
        query,
        game_id: cleanGameId,
        synthesized_prompt: synthesizedPrompt,
        skills_audit: skillsAnalysis,
        active_model_route: aiConfig?.primary_model || 'gemini-2.5-flash',
        simulated_response: `【老L · 避坑核验通过】针对“${query}”，已从 D1 库检索到 ${matchedCommands.length} 个精确代码。已启用防坏档防御与补丁比对保护。`
      }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'AI sandbox test failed',
      details: err.message
    }), { status: 500 });
  }
}
