/**
 * Cloudflare Pages Function: /api/v1/ai/chat
 * ==============================================================================
 * L-MOD Vault - Official Cloud AI Copilot Relay & Agentic Skills Orchestrator
 * ==============================================================================
 * 核心架构特性：
 * 1. 统一后台配置与密钥安全脱敏：玩家端零门槛免 Key，站长中台安全配置集中管控
 * 2. 4 大专属 Agentic Skills 拦截链：
 *    - 技能 A【Game Vault RAG】：从 D1 库检索 100% 真实的底层控制台代码与语法
 *    - 技能 B【Patch Sentinel】：读每日 Steam 更新雷达结果（public/radar_status.json，不读 D1 旧雷达列），
 *      讲清原因、Steam 更新时间、常用 Mod 框架和更新后怎么办
 *    - 技能 C【Crash Diagnostic】：针对各引擎 (CET/UE5/EAC/Creation) 闪退报错权威诊断
 *    - 技能 D【General Gaming Oracle】：全域单机智库通用问答与逃课攻略
 * 3. 高性能 Server-Sent Events (SSE) 流式打字机逐字输出
 * 4. 多路由智能容灾降级：Gemini 2.5 Flash -> DeepSeek-Chat -> D1 本地知识库智能兜底
 */

// 游戏别名统一来自游戏数据的 aliases 字段（scripts/build_game_aliases.py 生成），按长度从长到短排好
import { GAME_ALIASES } from './_game_aliases.js';
import { loadRadarStatus, radarEntry, radarContextFor, radarDaysAgo, RADAR_METHOD_NOTE } from '../../_radar_status.js';

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  try {
    const payload = await request.json().catch(() => ({}));
    const rawQuery = (payload.query || payload.message || '').trim();
    const clientGameId = payload.game_id && /^[a-z0-9-]+$/.test(payload.game_id) ? payload.game_id : null;
    const history = Array.isArray(payload.history) ? payload.history.slice(-6) : [];
    const isStream = payload.stream !== false; // 默认采用 SSE 流式

    if (!rawQuery) {
      return new Response(JSON.stringify({ code: 40000, message: '提问内容不能为空' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json; charset=utf-8' }
      });
    }

    // 1. 读取站长后台系统级 AI 编排配置
    let aiConfig = null;
    if (db) {
      try {
        const configRow = await db.prepare("SELECT value FROM system_settings WHERE key = 'ai_config'").first();
        if (configRow?.value) {
          aiConfig = JSON.parse(configRow.value);
        }
      } catch (e) {
        console.warn('Failed to load ai_config from DB:', e);
      }
    }

    // 合并默认配置
    const config = {
      system_prompt: aiConfig?.system_prompt || '你是由 L-MOD Vault 官方研发的‘老L’——全球单机游戏底层指令与避坑智库首席顾问。你精通 CET Lua、UE4SS、Creation Engine 控制台语法与反作弊机制。你的回答风格：言简意赅、老练严谨、绝不废话、直击痛点。遇到破坏存档或与补丁冲突的高危指令，必须第一时间发出红色预警并给出备份方案。',
      tone: aiConfig?.tone || 'hardcore_veteran',
      temperature: aiConfig?.temperature ?? 0.3,
      primary_model: aiConfig?.primary_model || 'gemini-2.5-flash',
      fallback_model: aiConfig?.fallback_model || 'deepseek-chat',
      skills: {
        game_vault_rag: true,
        patch_sentinel: true,
        crash_diagnostic: true,
        general_oracle: true,
        save_backup_guard: true,
        syntax_validator: true,
        code_dedup: true,
        ...(aiConfig?.skills || {})
      },
      gemini_api_key: env.GEMINI_API_KEY || aiConfig?.gemini_api_key || '',
      deepseek_api_key: env.DEEPSEEK_API_KEY || aiConfig?.deepseek_api_key || '',
      custom_endpoint: aiConfig?.custom_endpoint || '',
      custom_api_key: aiConfig?.custom_api_key || '',
      custom_model: aiConfig?.custom_model || ''
    };

    // 2. 智能探测与定位目标游戏
    let matchedGame = null;
    let targetGameId = clientGameId;

    if (!targetGameId) {
      // 从用户 query 中按别名精准推导
      const qLower = rawQuery.toLowerCase().replace(/\s+/g, '');
      for (const [alias, id] of Object.entries(GAME_ALIASES)) {
        if (qLower.includes(alias.toLowerCase())) {
          targetGameId = id;
          break;
        }
      }
    }

    if (db && targetGameId) {
      try {
        matchedGame = await db.prepare(
          `SELECT id, rank, title, title_zh, developer, release_year,
                  steam_app_id, has_console, console_shortcut, console_guide_zh,
                  pitfall_note
           FROM games WHERE id = ?`
        ).bind(targetGameId).first();
      } catch (e) {
        console.warn('Game query error:', e);
      }
    }

    // 若按别名未查到但有 db，尝试通过游戏标题前缀或全称模糊匹配
    if (db && !matchedGame && rawQuery.length >= 2) {
      try {
        const gamesList = await db.prepare("SELECT id, rank, title, title_zh FROM games ORDER BY rank ASC").all();
        if (gamesList?.results) {
          const qNorm = rawQuery.toLowerCase().replace(/[\s:：·\-]/g, '');
          for (const g of gamesList.results) {
            const mainZh = (g.title_zh || '').split(/[:：\(\)（）\s]/)[0].toLowerCase().replace(/[\s:：·\-]/g, '');
            const mainEn = (g.title || '').split(/[:：\(\)（）\s\-]/)[0].toLowerCase().replace(/[\s:：·\-]/g, '');
            if ((mainZh.length >= 2 && qNorm.includes(mainZh)) || (mainEn.length >= 4 && qNorm.includes(mainEn))) {
              targetGameId = g.id;
              matchedGame = await db.prepare(
                `SELECT id, rank, title, title_zh, developer, release_year,
                        steam_app_id, has_console, console_shortcut, console_guide_zh,
                        pitfall_note
                 FROM games WHERE id = ?`
              ).bind(g.id).first();
              break;
            }
          }
        }
      } catch (e) {}
    }

    // D1 不可用（没绑定 / 空库）时，按 radar_status.json 里的游戏名做同样的匹配，雷达问答照常可用
    if (!targetGameId && rawQuery.length >= 2) {
      const radarForMatch = await loadRadarStatus(context);
      if (radarForMatch) {
        const qNorm = rawQuery.toLowerCase().replace(/[\s:：·\-]/g, '');
        const entries = Object.entries(radarForMatch.games).sort(([, a], [, b]) => (a.rank || 0) - (b.rank || 0));
        for (const [id, e] of entries) {
          const mainZh = (e.titleZh || '').split(/[:：\(\)（）\s]/)[0].toLowerCase().replace(/[\s:：·\-]/g, '');
          const mainEn = (e.title || '').split(/[:：\(\)（）\s\-]/)[0].toLowerCase().replace(/[\s:：·\-]/g, '');
          if ((mainZh.length >= 2 && qNorm.includes(mainZh)) || (mainEn.length >= 4 && qNorm.includes(mainEn))) {
            targetGameId = id;
            break;
          }
        }
      }
    }

    // 3. 执行 4 大专属 Agentic Skills 技能拦截链
    const skillsTriggered = [];
    let retrievedCommands = [];
    let radarStatusInfo = null;
    let crashGuideInfo = null;
    let isHighRiskQuery = false;

    // -------------------------------------------------------------------------
    // 技能 A【Game Vault RAG 游戏指令与模组检索器】
    // -------------------------------------------------------------------------
    const hasCommandIntent = /代码|指令|控制台|作弊|秘籍|cheat|command|console|lua|bat/i.test(rawQuery);

    if (config.skills.game_vault_rag && db && (targetGameId || hasCommandIntent)) {
      // 提取核心查询关键词（支持中文自然句式智能分词与特征挖掘）
      let cleanQuery = rawQuery;
      if (matchedGame) {
        // 剔除已识别的游戏名词，避免污染具体指令关键词
        const namesToStrip = [
          matchedGame.title_zh,
          matchedGame.title,
          (matchedGame.title_zh || '').split(/[:：\(\)（）\s]/)[0],
          (matchedGame.title || '').split(/[:：\(\)（）\s\-]/)[0]
        ].filter(Boolean);
        for (const n of namesToStrip) {
          if (n.length >= 2) {
            cleanQuery = cleanQuery.replace(new RegExp(n.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi'), ' ');
          }
        }
      }

      // 去除常见停用词与虚词
      const stopPattern = /请问|怎么|如何|想要|要|给|加|增加|获取|获得|刷|搞|弄|把|的|了|啊|吗|呢|一下|一个|这个|那个|有没有|谁有|是啥|什么|修改|怎么弄|教程|方法/gi;
      const filteredText = cleanQuery.replace(stopPattern, ' ').replace(/[，。？！、\?,\!]/g, ' ');

      // 提取独立语义单元
      let searchTerms = filteredText
        .split(/\s+/)
        .map(t => t.trim())
        .filter(t => t.length >= 1);

      // 高频特征词挖掘（声望、家族、影响力、金币、属性点、武器等）
      const FEATURE_REGEX = /声望|家族|影响力|第纳尔|兵种|具装|可汗|骑兵|步兵|射手|钱|金币|金钱|刷钱|属性|属性点|专精|技能点|特警|四季宝|保时捷|觉|不朽|武器|枪|刀|剑|护甲|防具|衣服|装扮|道具|物品|无敌|不死|锁血|秒杀|一击必杀|霸体|无限|等级|经验|升级|满级|升满|重置|洗点|传送|坐标|瞬移|飞天|穿墙|血量|生命|生命值|体力|法力|蓝量|耐力|全收集|解锁|跳过|通关|好感|羁绊|控制台|代码|指令|作弊|秘籍/g;
      const matchedFeatures = rawQuery.match(FEATURE_REGEX);
      if (matchedFeatures && matchedFeatures.length > 0) {
        searchTerms = Array.from(new Set([...matchedFeatures, ...searchTerms]));
      }

      let conditions = [];
      let params = [];

      if (targetGameId) {
        conditions.push('game_id = ?');
        params.push(targetGameId);
      }

      if (searchTerms.length > 0) {
        const orClauses = searchTerms.map(() => '(name_zh LIKE ? OR name_en LIKE ? OR description LIKE ? OR code LIKE ?)');
        conditions.push(`(${orClauses.join(' OR ')})`);
        searchTerms.forEach(term => {
          const pat = `%${term}%`;
          params.push(pat, pat, pat, pat);
        });
      }

      try {
        let sql = `
          SELECT game_id, name_zh, name_en, code, description, syntax_type, is_popular
          FROM console_commands
          ${conditions.length > 0 ? 'WHERE ' + conditions.join(' AND ') : ''}
          ORDER BY is_popular DESC, id ASC
          LIMIT 8
        `;
        const { results } = await db.prepare(sql).bind(...params).all();
        retrievedCommands = results || [];

        // 若针对特定游戏未搜到具体词条，回退为该游戏的热门高频指令
        if (retrievedCommands.length === 0 && targetGameId) {
          const popularRes = await db.prepare(`
            SELECT game_id, name_zh, name_en, code, description, syntax_type, is_popular
            FROM console_commands
            WHERE game_id = ? AND is_popular = 1
            LIMIT 5
          `).bind(targetGameId).all();
          retrievedCommands = popularRes.results || [];
        }

        // 技能：代码查重 (Code De-dup)
        if (config.skills.code_dedup && retrievedCommands.length > 0) {
          const seenCode = new Set();
          retrievedCommands = retrievedCommands.filter(c => {
            const clean = (c.code || '').trim();
            if (!clean || seenCode.has(clean)) return false;
            seenCode.add(clean);
            return true;
          });
        }

        if (retrievedCommands.length > 0) {
          skillsTriggered.push({
            id: 'game_vault_rag',
            name: '游戏指令与模组检索器',
            detail: `从 D1 库召回 ${retrievedCommands.length} 条站内整理的指令`
          });
        }
      } catch (err) {
        console.warn('Game Vault RAG query error:', err);
      }
    }

    // -------------------------------------------------------------------------
    // 技能 B【Steam 更新雷达 · Patch Sentinel】
    // 只读每日巡检结果 public/radar_status.json；不读 D1 旧雷达列和 patch_radar_logs（都是早期手灌/模拟的数据）。
    // 没有 D1 时也能按别名认出游戏并回答雷达状态。
    // -------------------------------------------------------------------------
    if (config.skills.patch_sentinel && targetGameId) {
      const radarStatus = await loadRadarStatus(context);
      const entry = radarEntry(radarStatus, targetGameId);
      if (matchedGame || entry) {
        const radar = radarContextFor(targetGameId, radarStatus, matchedGame ? matchedGame.steam_app_id : undefined);
        radarStatusInfo = {
          game_id: targetGameId,
          game_title: matchedGame ? (matchedGame.title_zh || matchedGame.title) : (entry.titleZh || entry.title),
          rank: matchedGame ? matchedGame.rank : entry.rank,
          days_since_update: entry ? radarDaysAgo(entry.steamBuildUpdatedAt) : null,
          ...radar
        };

        skillsTriggered.push({
          id: 'patch_sentinel',
          name: 'Steam 更新雷达',
          detail: radar.tracked
            ? `Steam build ${radar.steam_build_id || '-'}（${radar.steam_updated_on || '日期未知'} 更新）· ${radar.status_text || radar.status}`
            : radar.note
        });
      }
    }

    // -------------------------------------------------------------------------
    // 技能 C【游戏报错与崩溃诊断专家 · Crash Diagnostic】
    // -------------------------------------------------------------------------
    const isCrashQuery = /闪退|崩溃|打不开|进不去|跳出|报错|黑屏|无响应|crash|freeze|error|0xc0000005|dinput8|dxgi|version\.dll|ue4ss|cet|skse|f4se|eac|easyanticheat|c\+\+|directx|dx11|dx12|regulation\.bin/i.test(rawQuery);
    if (config.skills.crash_diagnostic && isCrashQuery) {
      crashGuideInfo = buildEngineCrashKnowledge(matchedGame?.id || targetGameId, rawQuery);
      skillsTriggered.push({
        id: 'crash_diagnostic',
        name: '游戏报错与崩溃诊断专家',
        detail: `已激活专属引擎故障知识库与排查链路 (${crashGuideInfo.engine_name})`
      });
    }

    // -------------------------------------------------------------------------
    // 技能 D【全域单机智库通识问答 · General Gaming Oracle】
    // -------------------------------------------------------------------------
    if (config.skills.general_oracle && !matchedGame && retrievedCommands.length === 0 && !isCrashQuery) {
      skillsTriggered.push({
        id: 'general_oracle',
        name: '全域单机智库通识问答',
        detail: '依托老L深厚单机逆向经验与全网通识库进行老道推理'
      });
    }

    // -------------------------------------------------------------------------
    // 辅助守卫【高危坏档预防拦截 · Save Backup Guard】
    // -------------------------------------------------------------------------
    if (config.skills.save_backup_guard && /钱|金币|亿|等级|999|无敌|跳过|全收集|通关|秒杀/i.test(rawQuery)) {
      isHighRiskQuery = true;
      skillsTriggered.push({
        id: 'save_backup_guard',
        name: '坏档预防防御守卫',
        detail: '触发高危破坏性指令保护，强制前置注入存档备份红线警示'
      });
    }

    // 4. 合成高密度、无幻觉的 System Prompt
    const synthesizedPrompt = buildSynthesizedPrompt({
      systemRole: config.system_prompt,
      tone: config.tone,
      matchedGame,
      retrievedCommands,
      radarStatusInfo,
      crashGuideInfo,
      isHighRiskQuery,
      skillsTriggered
    });

    // 5. 组装多轮对话历史
    const conversationMessages = [
      ...history.map(h => ({
        role: h.role === 'assistant' ? 'assistant' : 'user',
        content: String(h.text || h.content || '')
      })),
      { role: 'user', content: rawQuery }
    ];

    // 6. 确定可用大模型路由与轮换池优先级 (支持 Gemini + OpenRouter + DeepSeek 智能热备轮换)
    const availableRoutes = resolveAvailableModelRoutes(config);
    const primaryRoute = availableRoutes[0] || {
      type: 'local_d1_engine',
      modelName: 'LMOD-Edge-RAG-v4.0',
      reason: '当前未配置外部大模型 API Key，已切换为 D1 智库底层原生规则引擎输出'
    };

    // 7. 执行大模型流式调用或智能兜底
    if (isStream) {
      const { readable, writable } = new TransformStream();
      const writer = writable.getWriter();
      const encoder = new TextEncoder();

      // 后台异步任务执行流推送，避免阻塞边缘连接
      (async () => {
        try {
          // 推送第一包：Meta 信息（触发的技能、目标游戏、命中代码数）
          const metaEvent = `event: meta\ndata: ${JSON.stringify({
            game: matchedGame ? {
              id: matchedGame.id,
              title: matchedGame.title_zh || matchedGame.title,
              rank: matchedGame.rank
            } : (radarStatusInfo ? {
              id: radarStatusInfo.game_id,
              title: radarStatusInfo.game_title,
              rank: radarStatusInfo.rank
            } : null),
            skills_triggered: skillsTriggered,
            commands_count: retrievedCommands.length,
            model_route: primaryRoute.modelName,
            status: 'streaming'
          })}\n\n`;
          await writer.write(encoder.encode(metaEvent));

          let streamSuccess = false;
          let activeRoute = null;

          // 循环尝试可用路由池 (若主力遇到 429 或故障则秒级故障转移至备选)
          for (const route of availableRoutes) {
            try {
              if (route.type === 'gemini') {
                streamSuccess = await streamGemini(
                  route.key,
                  route.modelName,
                  synthesizedPrompt,
                  conversationMessages,
                  config.temperature,
                  writer,
                  encoder
                );
              } else if (route.type === 'openai_compatible') {
                streamSuccess = await streamOpenAiCompatible(
                  route.endpoint,
                  route.key,
                  route.modelName,
                  synthesizedPrompt,
                  conversationMessages,
                  config.temperature,
                  writer,
                  encoder
                );
              }
              if (streamSuccess) {
                activeRoute = route;
                break;
              }
            } catch (errRoute) {
              console.warn(`Model route ${route.reason} attempt failed:`, errRoute);
            }
          }

          // 若大模型未配置或在线流式调用全部失败，使用边缘本地规则引擎合成高质感回答兜底
          if (!streamSuccess) {
            const fallbackText = generateEdgeEngineFallbackAnswer({
              query: rawQuery,
              matchedGame,
              retrievedCommands,
              radarStatusInfo,
              crashGuideInfo,
              isHighRiskQuery,
              skillsTriggered,
              routeMsg: availableRoutes.length > 0 ? '外部大模型调用超时或受限，已切换为 D1 智库底层原生规则引擎输出' : '当前未配置外部大模型 API Key，已切换为 D1 智库底层原生规则引擎输出'
            });

            // 模拟极客打字机效果切块推送
            const chunks = splitTextIntoChunks(fallbackText, 12);
            for (const chunk of chunks) {
              const deltaEvent = `event: delta\ndata: ${JSON.stringify({ text: chunk })}\n\n`;
              await writer.write(encoder.encode(deltaEvent));
              await delay(20);
            }
          }

          // 推送完成事件
          const doneEvent = `event: done\ndata: ${JSON.stringify({
            status: 'completed',
            tokens_generated: streamSuccess ? 'llm_stream' : 'edge_engine',
            active_model: activeRoute ? activeRoute.modelName : primaryRoute.modelName
          })}\n\n`;
          await writer.write(encoder.encode(doneEvent));
          await writer.write(encoder.encode('data: [DONE]\n\n'));

        } catch (streamErr) {
          console.error('Edge SSE stream error:', streamErr);
          const errEvent = `event: delta\ndata: ${JSON.stringify({ text: `\n\n> ⚠️ [老L 提示] 流式中继传输中断: ${streamErr.message}` })}\n\n`;
          await writer.write(encoder.encode(errEvent));
          await writer.write(encoder.encode('data: [DONE]\n\n'));
        } finally {
          await writer.close();
        }
      })();

      return new Response(readable, {
        headers: {
          'Content-Type': 'text/event-stream; charset=utf-8',
          'Cache-Control': 'no-cache, no-transform',
          'Connection': 'keep-alive',
          'X-Accel-Buffering': 'no'
        }
      });

    } else {
      // 非流式普通 JSON 响应
      let fullText = '';
      let activeRoute = null;

      for (const route of availableRoutes) {
        try {
          if (route.type === 'gemini') {
            fullText = await fetchGeminiSync(route.key, route.modelName, synthesizedPrompt, conversationMessages, config.temperature);
          } else if (route.type === 'openai_compatible') {
            fullText = await fetchOpenAiSync(route.endpoint, route.key, route.modelName, synthesizedPrompt, conversationMessages, config.temperature);
          }
          if (fullText) {
            activeRoute = route;
            break;
          }
        } catch (errRoute) {
          console.warn(`Sync model route ${route.reason} attempt failed:`, errRoute);
        }
      }

      if (!fullText) {
        fullText = generateEdgeEngineFallbackAnswer({
          query: rawQuery,
          matchedGame,
          retrievedCommands,
          radarStatusInfo,
          crashGuideInfo,
          isHighRiskQuery,
          skillsTriggered,
          routeMsg: availableRoutes.length > 0 ? '外部大模型调用超时或受限，已切换为 D1 智库底层原生规则引擎输出' : '当前未配置外部大模型 API Key，已切换为 D1 智库底层原生规则引擎输出'
        });
      }

      return new Response(JSON.stringify({
        code: 0,
        message: 'success',
        data: {
          text: fullText,
          game: matchedGame,
          radar: radarStatusInfo,
          skills_triggered: skillsTriggered,
          retrieved_commands: retrievedCommands,
          model_route: activeRoute ? activeRoute.modelName : primaryRoute.modelName
        }
      }), {
        headers: { 'Content-Type': 'application/json; charset=utf-8' }
      });
    }

  } catch (error) {
    console.error('Unhandled AI chat exception:', error);
    return new Response(JSON.stringify({
      code: 50000,
      message: '老L·AI 智能体服务异常，请稍后重试',
      details: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });
  }
}

// =============================================================================
// 模型路由判定与轮换池解析器 (Multi-Provider Priority Resolver)
// =============================================================================
function resolveAvailableModelRoutes(config) {
  const routes = [];

  const addRoute = (type, key, model, endpoint, reason) => {
    if (!key) return;
    routes.push({
      type,
      key,
      modelName: model,
      endpoint,
      reason
    });
  };

  // 1. Google Gemini (官方免费 1.5 Flash / 1.5 Pro)
  if (config.gemini_api_key) {
    let gModel = config.primary_model?.startsWith('gemini') ? config.primary_model : 'gemini-1.5-flash';
    if (gModel === 'gemini-2.5-flash') gModel = 'gemini-1.5-flash';
    addRoute('gemini', config.gemini_api_key, gModel, null, `Google Gemini 官方免费大模型 (${gModel})`);
  }

  // 2. OpenRouter / 自定义 OpenAI 兼容端点 (支持免费模型池轮换)
  if (config.custom_api_key) {
    const isOrKey = config.custom_api_key.startsWith('sk-or-');
    let endpoint = (config.custom_endpoint || '').trim();
    if (!endpoint && isOrKey) {
      endpoint = 'https://openrouter.ai/api/v1/chat/completions';
    }
    let cModel = config.custom_model || (config.primary_model?.includes('/') ? config.primary_model : 'google/gemini-2.0-flash-exp:free');
    if (cModel === 'openrouter/free') cModel = 'google/gemini-2.0-flash-exp:free';
    if (endpoint) {
      addRoute('openai_compatible', config.custom_api_key, cModel, endpoint, isOrKey ? `OpenRouter 免费轮换模型 (${cModel})` : `自定义端点 (${cModel})`);
    }
  }

  // 3. DeepSeek 官方
  if (config.deepseek_api_key) {
    addRoute('openai_compatible', config.deepseek_api_key, 'deepseek-chat', 'https://api.deepseek.com/chat/completions', 'DeepSeek-V3 官方大模型');
  }

  // 依据站长配置的主选偏好排序路由池
  if (config.primary_model && (config.primary_model.includes('openrouter') || config.primary_model.includes('/') || config.primary_model === 'custom')) {
    routes.sort((a, b) => (a.reason.includes('OpenRouter') || a.reason.includes('自定义') ? -1 : 1));
  } else if (config.primary_model?.includes('deepseek')) {
    routes.sort((a, b) => (a.reason.includes('DeepSeek') ? -1 : 1));
  } else {
    // 默认 Gemini 优先
    routes.sort((a, b) => (a.type === 'gemini' ? -1 : 1));
  }

  return routes;
}

// =============================================================================
// 高密度系统 Prompt 合成器 (Agentic Synthesizer)
// =============================================================================
function buildSynthesizedPrompt({
  systemRole,
  tone,
  matchedGame,
  retrievedCommands,
  radarStatusInfo,
  crashGuideInfo,
  isHighRiskQuery,
  skillsTriggered
}) {
  let prompt = `${systemRole}\n\n`;

  prompt += `### 【老L·当前推理规范与铁律】\n`;
  prompt += `1. **真实指令第一原则**：代码严禁杜撰幻觉！必须严格按照各游戏引擎的真实底层语法（如 CET Lua、UE4SS/虚幻控制台、Creation Engine Hex、BG3 Osiris 等）给出。\n`;
  prompt += `2. **格式要求**：指令必须放在 Markdown 代码块内，并在上方明确标明开启按键（如 ~、F1、F10、Insert）。\n`;
  prompt += `3. **避坑与坏档警示**：对修改金币数亿、直接满级、跳过剧情等高危指令，必须用 '> ⚠️ **老L 独家避坑警示**：' 强提示备份存档！\n\n`;

  if (matchedGame) {
    prompt += `### 【当前锚定游戏画像 (站内资料)】\n`;
    prompt += `- 游戏名称: 《${matchedGame.title_zh || matchedGame.title}》 (${matchedGame.title})\n`;
    prompt += `- 排名与开发商: 全网 Rank #${matchedGame.rank} · ${matchedGame.developer || '未知'}\n`;
    prompt += `- 控制台快捷键: \`${matchedGame.console_shortcut || '无原生控制台/需前置注入'}\`\n`;
    if (matchedGame.console_guide_zh) {
      prompt += `- 控制台呼出步骤: ${matchedGame.console_guide_zh}\n`;
    }
    if (matchedGame.pitfall_note) {
      prompt += `- 老L 独家避坑锦囊: ${matchedGame.pitfall_note}\n`;
    }
    prompt += `\n`;
  }

  if (retrievedCommands && retrievedCommands.length > 0) {
    prompt += `### 【D1 智库检索命中的真实指令 (绝对事实，优先采纳)】\n`;
    for (const cmd of retrievedCommands) {
      prompt += `- 【${cmd.name_zh || cmd.name_en}】(语法: ${cmd.syntax_type})\n`;
      if (cmd.description) prompt += `  说明: ${cmd.description}\n`;
      prompt += `  代码: \`${cmd.code}\`\n`;
    }
    prompt += `\n`;
  }

  if (radarStatusInfo) {
    const r = radarStatusInfo;
    prompt += `### 【Steam 更新雷达（每日巡检结果）】\n`;
    if (!r.tracked) {
      prompt += `- ${r.note}\n`;
    } else {
      prompt += `- 雷达状态: ${r.status_text || r.status}\n`;
      prompt += `- 原因: ${r.reason_text}\n`;
      if (r.summary) prompt += `- 巡检摘要: ${r.summary}\n`;
      prompt += `- Steam 当前版本: build ${r.steam_build_id || '未知'}，${r.steam_updated_on || '日期未知'} 发布`;
      prompt += r.days_since_update !== null && r.days_since_update !== undefined ? `（距今 ${r.days_since_update} 天）\n` : `\n`;
      prompt += `- 上次巡检: ${r.last_checked_on || '未知'}\n`;
      prompt += r.framework
        ? `- 常用 Mod 框架: ${r.framework.name}（${r.framework.url}）\n`
        : `- 常用 Mod 框架: 资料里没有记录这款游戏依赖的 Mod 框架\n`;
      prompt += `- 更新后怎么办: ${r.after_update || '先备份存档，等 Mod 和修改器作者适配新版本再用。'}\n`;
      if (r.latest_announcement) {
        prompt += `- 最新官方公告: ${r.latest_announcement.title || '（无标题）'} ${r.latest_announcement.url}\n`;
      }
    }
    prompt += `- 判定方法: ${RADAR_METHOD_NOTE}\n`;
    prompt += `- 回答要求: 玩家问到更新、补丁、版本、能不能装 Mod/修改器时，按上面的数据讲清楚原因、Steam 更新时间、常用框架和更新后怎么办；`;
    prompt += `只说「可能」，不要说「实测」「已认证补丁」「完美兼容」，不要编造版本号或兼容结论。\n\n`;
  }

  if (crashGuideInfo) {
    prompt += `### 【报错与崩溃排查知识库注入】\n`;
    prompt += `- 引擎类型: ${crashGuideInfo.engine_name}\n`;
    prompt += `- 核心排查要点:\n${crashGuideInfo.troubleshooting_steps}\n\n`;
  }

  if (isHighRiskQuery) {
    prompt += `### 【高危防御守卫已激活】\n`;
    prompt += `此提问涉及巨额属性或数值破坏，你必须在回答第一行醒目加入存档备份路径提示与坏档警告！\n\n`;
  }

  return prompt;
}

// =============================================================================
// 各游戏引擎专属崩溃排查知识库
// =============================================================================
function buildEngineCrashKnowledge(gameId, query) {
  if (gameId === 'cyberpunk-2077') {
    return {
      engine_name: 'CDPR REDengine 4 (Cyberpunk 2077)',
      troubleshooting_steps: `1. **CET (Cyber Engine Tweaks) 版本过旧**：升级至适配当前版本的 CET，检查 \`bin/x64/plugins/cyber_engine_tweaks.asi\`。\n2. **REDscript 脚本缓存冲突**：彻底删除 \`r6/cache/modded\` 目录让引擎自动重新编译。\n3. **TweakXL / ArchiveXL 核心库未对齐**：必须更新所有前置 DLL。\n4. **排查微星小飞机/GeForce Experience**：关闭第三方 OSD 显卡浮窗。`
    };
  }

  if (gameId === 'black-myth-wukong' || gameId === 'palworld') {
    return {
      engine_name: 'Unreal Engine 5 (虚幻5引擎)',
      troubleshooting_steps: `1. **DX12 着色器编译崩掉 (0xc0000005)**：在 Steam 启动项添加 \`-dx11\` 或升级显卡驱动彻底重装。\n2. **UE4SS 注入器图形钩子崩溃**：打开 \`ue4ss.ini\`，设置 \`GuiConsoleEnabled = 0\`。\n3. **Pak Mod 版本过期**：将 \`~mods\` 文件夹更名为 \`~mods_bak\` 逐步二分法排查损坏模型或资产。`
    };
  }

  if (gameId === 'elden-ring' || gameId === 'sekiro') {
    return {
      engine_name: 'FromSoftware 专属自研引擎',
      troubleshooting_steps: `1. **EAC 反作弊未关闭**：不可直接通过 Steam 启动游戏，必须使用离线补丁或 \`start_protected_game.exe\` 替换法。\n2. **ModEngine2 路径配置错误**：检查 \`config_eldenring.toml\` 引导路径是否指向正确目录。\n3. **Regulation.bin 损坏**：版本更新后大参数文件常引起主菜单跳出，需等待作者适配新版本。`
    };
  }

  if (gameId?.includes('skyrim') || gameId?.includes('fallout') || gameId === 'starfield') {
    return {
      engine_name: 'Bethesda Creation Engine (老滚/辐射/星空)',
      troubleshooting_steps: `1. **SKSE / F4SE 版本与主程序未对齐**：检查游戏 EXE 属性详细信息版本号，不可混用新旧版本脚本扩展器。\n2. **Address Library 缺失**：缺少对应版本的 Address Library for SKSE Plugins 会直接引发 0xc0000005 闪退。\n3. **ESP 加载顺序冲突**：使用 LOOT 自动重排插件顺序，并使用 SSEEdit 清理冲突脏记录。`
    };
  }

  return {
    engine_name: '通用 PC 单机游戏环境',
    troubleshooting_steps: `1. **排查杀毒软件误杀**：Windows Defender 常误杀注入型 DLL (dinput8.dll, dxgi.dll)，将游戏根目录添加至安全白名单。\n2. **二分法排查 Mod 目录**：临时重命名 Mods 或 Plugins 文件夹，验证原版游戏能否正常启动。\n3. **修复微软常用运行库**：安装完整的 Visual C++ 2015-2022 x86/x64 Redistributable。\n4. **Steam 验证游戏文件完整性**：右键游戏 -> 属性 -> 本地已安装文件 -> 验证游戏完整性。`
  };
}

// =============================================================================
// Google Gemini API 流式调用实现
// =============================================================================
async function streamGemini(apiKey, modelName, systemPrompt, messages, temperature, writer, encoder) {
  try {
    // 兼容映射：防止历史配置或误填导致 404
    let targetModel = modelName;
    if (!targetModel || targetModel === 'gemini-2.5-flash') {
      targetModel = 'gemini-1.5-flash';
    }
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${targetModel}:streamGenerateContent?alt=sse&key=${apiKey}`;

    // 格式化 Gemini 历史与当前提问
    const geminiContents = messages.map(m => ({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }]
    }));

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        systemInstruction: {
          parts: [{ text: systemPrompt }]
        },
        contents: geminiContents,
        generationConfig: {
          temperature: temperature || 0.3,
          maxOutputTokens: 2500
        }
      })
    });

    if (!response.ok) {
      console.warn(`Gemini API error status: ${response.status}`);
      return false;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('data: ')) {
          const jsonStr = trimmed.slice(6);
          if (jsonStr === '[DONE]') continue;

          try {
            const parsed = JSON.parse(jsonStr);
            const textChunk = parsed.candidates?.[0]?.content?.parts?.[0]?.text;
            if (textChunk) {
              const deltaEvent = `event: delta\ndata: ${JSON.stringify({ text: textChunk })}\n\n`;
              await writer.write(encoder.encode(deltaEvent));
            }
          } catch (e) {}
        }
      }
    }

    return true;
  } catch (err) {
    console.warn('Gemini stream failed:', err);
    return false;
  }
}

// =============================================================================
// OpenAI / OpenRouter / DeepSeek 兼容端点流式调用实现
// =============================================================================
async function streamOpenAiCompatible(endpoint, apiKey, modelName, systemPrompt, messages, temperature, writer, encoder) {
  try {
    let targetUrl = (endpoint || 'https://openrouter.ai/api/v1/chat/completions').trim();
    if (!targetUrl.endsWith('/chat/completions')) {
      targetUrl = targetUrl.replace(/\/+$/, '') + '/chat/completions';
    }

    let targetModel = modelName && modelName !== 'custom' ? modelName : 'google/gemini-2.0-flash-exp:free';
    if (targetModel === 'openrouter/free') {
      targetModel = 'google/gemini-2.0-flash-exp:free';
    }

    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': 'https://lmod-vault.pages.dev',
        'X-Title': 'L-MOD Vault'
      },
      body: JSON.stringify({
        model: targetModel,
        messages: [
          { role: 'system', content: systemPrompt },
          ...messages
        ],
        temperature: temperature || 0.3,
        stream: true
      })
    });

    if (!response.ok) {
      console.warn(`OpenAI compatible API error status: ${response.status}`);
      return false;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('data: ')) {
          const jsonStr = trimmed.slice(6);
          if (jsonStr === '[DONE]') continue;

          try {
            const parsed = JSON.parse(jsonStr);
            const textChunk = parsed.choices?.[0]?.delta?.content;
            if (textChunk) {
              const deltaEvent = `event: delta\ndata: ${JSON.stringify({ text: textChunk })}\n\n`;
              await writer.write(encoder.encode(deltaEvent));
            }
          } catch (e) {}
        }
      }
    }

    return true;
  } catch (err) {
    console.warn('OpenAI stream failed:', err);
    return false;
  }
}

// =============================================================================
// 同步请求辅助函数 (非流式普通调用)
// =============================================================================
async function fetchGeminiSync(apiKey, modelName, systemPrompt, messages, temperature) {
  try {
    let targetModel = modelName;
    if (!targetModel || targetModel === 'gemini-2.5-flash') {
      targetModel = 'gemini-1.5-flash';
    }
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${targetModel}:generateContent?key=${apiKey}`;
    const geminiContents = messages.map(m => ({
      role: m.role === 'assistant' ? 'model' : 'user',
      parts: [{ text: m.content }]
    }));
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        systemInstruction: { parts: [{ text: systemPrompt }] },
        contents: geminiContents,
        generationConfig: { temperature: temperature || 0.3, maxOutputTokens: 2500 }
      })
    });
    if (!response.ok) return '';
    const data = await response.json();
    return data.candidates?.[0]?.content?.parts?.[0]?.text || '';
  } catch (err) {
    console.warn('Gemini sync call failed:', err);
    return '';
  }
}

async function fetchOpenAiSync(endpoint, apiKey, modelName, systemPrompt, messages, temperature) {
  try {
    let targetUrl = (endpoint || 'https://openrouter.ai/api/v1/chat/completions').trim();
    if (!targetUrl.endsWith('/chat/completions')) {
      targetUrl = targetUrl.replace(/\/+$/, '') + '/chat/completions';
    }

    let targetModel = modelName && modelName !== 'custom' ? modelName : 'google/gemini-2.0-flash-exp:free';
    if (targetModel === 'openrouter/free') {
      targetModel = 'google/gemini-2.0-flash-exp:free';
    }

    const response = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'HTTP-Referer': 'https://lmod-vault.pages.dev',
        'X-Title': 'L-MOD Vault'
      },
      body: JSON.stringify({
        model: targetModel,
        messages: [{ role: 'system', content: systemPrompt }, ...messages],
        temperature: temperature || 0.3
      })
    });
    if (!response.ok) return '';
    const data = await response.json();
    return data.choices?.[0]?.message?.content || '';
  } catch (err) {
    console.warn('OpenAI sync call failed:', err);
    return '';
  }
}

// =============================================================================
// 本地 Edge 规则引擎智能合成回答 (零 Key / 容灾兜底)
// =============================================================================
function generateEdgeEngineFallbackAnswer({
  query,
  matchedGame,
  retrievedCommands,
  radarStatusInfo,
  crashGuideInfo,
  isHighRiskQuery,
  skillsTriggered,
  routeMsg
}) {
  let res = '';

  const gameTitle = matchedGame
    ? (matchedGame.title_zh || matchedGame.title)
    : ((radarStatusInfo && radarStatusInfo.game_title) || '单机游戏');

  // 1. 高危坏档提示
  if (isHighRiskQuery) {
    res += `> ⚠️ **老L 独家避坑警示**：检测到涉及核心数值修改操作！执行前务必进入存档目录备份你的本地 Save 文件，防止破坏主线任务脚本导致不可逆坏档！\n\n`;
  }

  // 2. 闪退崩溃诊断
  if (crashGuideInfo) {
    res += `### 💥 《${gameTitle}》闪退报错与运行库逃课诊断\n\n`;
    res += `已调取针对 **${crashGuideInfo.engine_name}** 的工业级排查方案：\n\n`;
    res += `${crashGuideInfo.troubleshooting_steps}\n\n`;
    if (matchedGame?.pitfall_note) {
      res += `> 💡 **老L 独家防坑提醒**：${matchedGame.pitfall_note}\n\n`;
    }
  }

  // 3. 指令召回结果
  if (retrievedCommands && retrievedCommands.length > 0) {
    res += `### 🎮 《${gameTitle}》针对 "${query}" 的指令检索结果\n\n`;
    res += `从 L-MOD 站内资料里找到 **${retrievedCommands.length}** 条相关的控制台指令（站内整理，游戏更新后可能失效，用前先备份存档）：\n\n`;

    for (const cmd of retrievedCommands) {
      const name = cmd.name_zh || cmd.name_en;
      res += `#### 📌 ${name}\n`;
      if (cmd.description) res += `${cmd.description}\n`;
      res += `\`\`\`lua\n${cmd.code}\n\`\`\`\n\n`;
    }

    if (matchedGame?.console_shortcut) {
      res += `> 🛠️ **控制台呼出**：在游戏中按 \`${matchedGame.console_shortcut}\` 唤出控制台输入框，粘贴上述代码执行。\n\n`;
    }
  }

  // 4. Steam 更新雷达（每日巡检结果）
  if (radarStatusInfo && (/补丁|雷达|更新|版本|能玩|兼容|patch|update/i.test(query) || !retrievedCommands.length)) {
    const r = radarStatusInfo;
    const mdText = (t) => String(t || '').replace(/[\[\]]/g, ' ').trim();
    res += `### 📡 《${gameTitle}》Steam 更新雷达\n\n`;
    if (!r.tracked) {
      res += `- **雷达状态**：⚪ ${r.note}\n\n`;
    } else {
      res += `- **雷达状态**：${r.status_text || r.status}\n`;
      res += `- **原因**：${r.reason_text}\n`;
      const ago = r.days_since_update !== null && r.days_since_update !== undefined ? `，${r.days_since_update} 天前` : '';
      res += `- **Steam 最近更新**：${r.steam_updated_on || '日期未知'}（build ${r.steam_build_id || '-'}${ago}）\n`;
      res += r.framework
        ? `- **常用 Mod 框架**：[${mdText(r.framework.name)}](${r.framework.url})\n`
        : `- **常用 Mod 框架**：资料里没有记录\n`;
      res += `- **更新后怎么办**：${r.after_update || '先备份存档，等 Mod 和修改器作者适配新版本再用。'}\n`;
      if (r.latest_announcement) {
        res += `- **最新官方公告**：[${mdText(r.latest_announcement.title) || '查看公告'}](${r.latest_announcement.url})\n`;
      }
      res += `- **上次巡检**：${r.last_checked_on || '未知'}\n\n`;
      res += `> ${RADAR_METHOD_NOTE}\n\n`;
    }
  }

  // 5. 若既无指令也无报错但有游戏
  if (!retrievedCommands.length && !crashGuideInfo && matchedGame) {
    res += `### 🎮 《${gameTitle}》智库基础档案\n\n`;
    res += `- **开发商/引擎**：${matchedGame.developer || 'N/A'}\n`;
    res += `- **控制台开启**：${matchedGame.has_console ? `支持快捷键 \`${matchedGame.console_shortcut}\`` : '需第三方注入工具'}\n`;
    if (matchedGame.console_guide_zh) res += `- **开启方法**：${matchedGame.console_guide_zh}\n`;
    if (matchedGame.pitfall_note) res += `- **避坑提示**：${matchedGame.pitfall_note}\n\n`;
    res += `你可以直接向我询问具体代码需求（如“给我${gameTitle}刷金币代码”、“控制台怎么开”、“打mod闪退怎么解决”）。\n\n`;
  }

  // 6. 全局兜底
  if (!res) {
    res += `### 🤖 老L·AI 官方智库顾问已收到你的提问：“${query}”\n\n`;
    res += `当前已激活 **4 大专属 Skills** 联动检索：\n`;
    res += `- 🔍 **Game Vault RAG**：D1 智库 1093+ 条真实控制台代码\n`;
    res += `- 📡 **Steam 更新雷达**：每天巡检站内 Steam 游戏的更新时间，提醒哪些 Mod 框架可能要等适配\n`;
    res += `- 💥 **Crash 故障专家**：覆盖 CET、UE5、EAC、Creation 等主流引擎\n\n`;
    res += `💡 **提问建议**：推荐带上具体游戏名称或报错特征，例如：\n`;
    res += `- “2077怎么刷四季宝和强尼保时捷”\n`;
    res += `- “黑神话虚幻5着色器报错0xc0000005怎么修”\n`;
    res += `- “法环最近更新了吗，现在装 Mod 要注意什么”\n`;
  }

  if (routeMsg) {
    res += `\n---\n*⚡ 驱动状态: ${routeMsg}*`;
  }

  return res;
}

// 辅助工具函数
function splitTextIntoChunks(text, chunkSize = 16) {
  const chunks = [];
  for (let i = 0; i < text.length; i += chunkSize) {
    chunks.push(text.slice(i, i + chunkSize));
  }
  return chunks;
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
