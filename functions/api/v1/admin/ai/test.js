/**
 * Cloudflare Pages Function: POST /api/v1/admin/ai/test
 * AI Skills Studio Interactive Sandbox & Diagnostic Simulator
 * ==============================================================================
 * 升级特性：
 * 完整模拟 4 大专属核心技能（Game Vault RAG, Patch Sentinel, Crash Diagnostic, General Oracle）
 * 与安全守卫拦截链的实际执行与决策结果
 */

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const { query, game_id } = await request.json();

    if (!query || typeof query !== 'string') {
      return new Response(JSON.stringify({ code: 40000, message: 'Missing query parameter' }), { status: 400 });
    }

    // 1. 获取 AI 系统配置
    const aiConfigRow = await db.prepare("SELECT value FROM system_settings WHERE key = 'ai_config'").first();
    let aiConfig = null;
    if (aiConfigRow?.value) {
      try { aiConfig = JSON.parse(aiConfigRow.value); } catch (e) {}
    }

    const cleanGameId = game_id && /^[a-z0-9-]+$/.test(game_id) ? game_id : null;

    // 2. 获取游戏信息
    let game = null;
    if (cleanGameId) {
      game = await db.prepare(
        `SELECT id, title, title_zh, console_shortcut, verified_patch, latest_steam_patch,
                compatibility_status, radar_risk_title, radar_risk_desc, pitfall_note
         FROM games WHERE id = ?`
      ).bind(cleanGameId).first();
    }

    // 3. 指令检索 (Game Vault RAG 模拟)
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

    // 4. 判断崩溃与报错特征
    const isCrashQuery = /闪退|崩溃|打不开|进不去|跳出|报错|crash|black\s*screen|error|eac|ue4ss|cet|0xc0000005/i.test(query);

    // 5. 4 大核心 Skills 拦截链模拟
    const skillsAnalysis = {
      game_vault_rag: {
        executed: true,
        status: matchedCommands.length > 0 ? 'HIT' : 'FALLBACK',
        verdict: matchedCommands.length > 0 
          ? `【技能 A 命中】从 D1 库精确召回 ${matchedCommands.length} 条已核验控制台真实底层代码。`
          : '未在 D1 库检索到精确代码，将使用该游戏热门指令或大模型通用知识库。'
      },
      patch_sentinel: {
        executed: !!game,
        status: game ? (game.compatibility_status === 'green' ? 'COMPATIBLE' : 'WARNING') : 'SKIPPED',
        verdict: game
          ? `【技能 B 巡检】基于 Steam ${game.latest_steam_patch || '最新'} 对账基准 ${game.verified_patch || '认证'}：当前雷达状态【${game.compatibility_status.toUpperCase()}】。`
          : '全局模式，未指定单游，跳过补丁比对。'
      },
      crash_diagnostic: {
        executed: isCrashQuery,
        status: isCrashQuery ? 'ACTIVATED' : 'PASSIVE',
        verdict: isCrashQuery
          ? `【技能 C 激活】检测到报错崩溃语义，已注入底层引擎 (CET/UE5/EAC/Creation) 专属防闪退逃课排查链路。`
          : '未检测到崩溃报错关键词。'
      },
      general_oracle: {
        executed: true,
        status: 'READY',
        verdict: '【技能 D 就绪】全域单机游戏常识与攻略推理链处于热备就绪状态。'
      },
      save_backup_guard: {
        executed: true,
        status: (query.includes('钱') || query.includes('等级') || query.includes('无敌') || query.includes('全收集')) ? 'ALERT_ATTACHED' : 'SAFE',
        verdict: (query.includes('钱') || query.includes('等级') || query.includes('无敌') || query.includes('全收集'))
          ? '触发破坏性高危指令防御：强制前置注入【老L 独家存档备份红线警示】。'
          : '常规指令，低风险。'
      }
    };

    // 6. 构造合成提示词
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
        simulated_response: `【老L · 避坑核验通过】针对“${query}”，已通过 4 大 Skills 编排流水线：检索到 ${matchedCommands.length} 条真实代码，补丁哨兵状态【${game ? game.compatibility_status.toUpperCase() : 'PASS'}】，防坏档机制就绪。`
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
