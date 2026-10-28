/**
 * Cloudflare Pages Function: /api/v1/admin/ai/config
 * Lao-L AI Copilot & Agentic Skills Studio Configuration Plane
 * ==============================================================================
 * 升级特性：
 * 1. 站长统一管理 API 密钥（Google Gemini、DeepSeek、自定义 OpenAI 兼容接口）
 * 2. 密钥脱敏安全防泄露：GET 接口掩码返回，POST 接口智能保留未变动的真实密钥
 * 3. 4 大专属 Skills（Game Vault RAG, Patch Sentinel, Crash Diagnostic, General Oracle）及守卫开关配置
 */

import { logAdminAction } from '../_auth.js';

// 密钥脱敏辅助工具
function maskKey(key) {
  if (!key || typeof key !== 'string') return '';
  const clean = key.trim();
  if (clean.length <= 8) return '****';
  const prefix = clean.slice(0, 6);
  const suffix = clean.slice(-4);
  return `${prefix}...****...${suffix}`;
}

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const row = await db.prepare(
      "SELECT value, updated_at FROM system_settings WHERE key = 'ai_config'"
    ).first();

    let config = null;
    if (row && row.value) {
      try {
        config = JSON.parse(row.value);
      } catch (e) {
        config = null;
      }
    }

    if (!config) {
      // 默认系统人设与技能配置
      config = {
        system_prompt: '你是由 L-MOD Vault 官方研发的‘老L’——全球单机游戏底层指令与避坑智库首席顾问。你精通 CET Lua、UE4SS、Creation Engine 控制台语法与反作弊机制。你的回答风格：言简意赅、老练严谨、绝不废话、直击痛点。遇到破坏存档或与补丁冲突的高危指令，必须第一时间发出红色预警并给出备份方案。',
        tone: 'hardcore_veteran',
        tone_label: '资深单机老炮 / 严谨避坑顾问',
        temperature: 0.3,
        recall_threshold: 0.65,
        max_context_commands: 6,
        primary_model: 'gemini-1.5-flash',
        fallback_model: 'deepseek-chat',
        skills: {
          game_vault_rag: true,
          patch_sentinel: true,
          crash_diagnostic: true,
          general_oracle: true,
          save_backup_guard: true,
          syntax_validator: true,
          code_dedup: true,
          downgrade_wizard: true
        },
        gemini_api_key: '',
        deepseek_api_key: '',
        custom_endpoint: '',
        custom_api_key: '',
        custom_model: '',
        updated_at: new Date().toISOString()
      };
    }

    // 确保 skills 字段包含 4 大专属核心技能
    config.skills = {
      game_vault_rag: true,
      patch_sentinel: true,
      crash_diagnostic: true,
      general_oracle: true,
      save_backup_guard: true,
      syntax_validator: true,
      code_dedup: true,
      downgrade_wizard: true,
      ...(config.skills || {})
    };

    // 密钥安全脱敏处理 (对外仅暴露掩码与挂载状态)
    const clientSafeConfig = {
      ...config,
      gemini_api_key: maskKey(config.gemini_api_key || env.GEMINI_API_KEY),
      has_gemini_key: !!(config.gemini_api_key || env.GEMINI_API_KEY),
      is_gemini_env: !!env.GEMINI_API_KEY && !config.gemini_api_key,
      deepseek_api_key: maskKey(config.deepseek_api_key || env.DEEPSEEK_API_KEY),
      has_deepseek_key: !!(config.deepseek_api_key || env.DEEPSEEK_API_KEY),
      is_deepseek_env: !!env.DEEPSEEK_API_KEY && !config.deepseek_api_key,
      custom_api_key: maskKey(config.custom_api_key),
      has_custom_key: !!config.custom_api_key
    };

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: clientSafeConfig
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to retrieve AI configuration',
      details: err.message
    }), { status: 500 });
  }
}

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  const admin = data?.admin || { username: '老L·站长' };
  const clientIP = request.headers.get('cf-connecting-ip') || '127.0.0.1';

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const newConfig = await request.json();

    if (!newConfig.system_prompt || typeof newConfig.system_prompt !== 'string') {
      return new Response(JSON.stringify({ code: 40000, message: '系统提示词 (System Prompt) 不能为空' }), { status: 400 });
    }

    // 1. 读取数据库中已有的旧配置，用于保持未修改的真实密钥
    let existingConfig = {};
    const existingRow = await db.prepare("SELECT value FROM system_settings WHERE key = 'ai_config'").first();
    if (existingRow?.value) {
      try { existingConfig = JSON.parse(existingRow.value); } catch (e) {}
    }

    // 2. 智能更新密钥：如果提交的是掩码 (包含 '****' 或 '...*')，则保留原有真实密钥；否则更新新值
    function resolveKey(incomingKey, originalKey) {
      if (incomingKey === undefined || incomingKey === null) return originalKey || '';
      const trimmed = String(incomingKey).trim();
      if (trimmed.includes('****') || trimmed.includes('...')) {
        return originalKey || ''; // 用户未修改密钥，保留真实 key
      }
      return trimmed;
    }

    const mergedGeminiKey = resolveKey(newConfig.gemini_api_key, existingConfig.gemini_api_key);
    const mergedDeepSeekKey = resolveKey(newConfig.deepseek_api_key, existingConfig.deepseek_api_key);
    const mergedCustomKey = resolveKey(newConfig.custom_api_key, existingConfig.custom_api_key);

    const updatedConfig = {
      system_prompt: newConfig.system_prompt.trim(),
      tone: newConfig.tone || existingConfig.tone || 'hardcore_veteran',
      tone_label: newConfig.tone_label || '资深单机老炮 / 严谨避坑顾问',
      temperature: typeof newConfig.temperature === 'number' ? newConfig.temperature : (existingConfig.temperature ?? 0.3),
      recall_threshold: typeof newConfig.recall_threshold === 'number' ? newConfig.recall_threshold : (existingConfig.recall_threshold ?? 0.65),
      max_context_commands: parseInt(newConfig.max_context_commands || existingConfig.max_context_commands || 6, 10),
      primary_model: newConfig.primary_model || existingConfig.primary_model || 'gemini-2.5-flash',
      fallback_model: newConfig.fallback_model || existingConfig.fallback_model || 'deepseek-chat',
      skills: {
        game_vault_rag: newConfig.skills?.game_vault_rag ?? true,
        patch_sentinel: newConfig.skills?.patch_sentinel ?? true,
        crash_diagnostic: newConfig.skills?.crash_diagnostic ?? true,
        general_oracle: newConfig.skills?.general_oracle ?? true,
        save_backup_guard: newConfig.skills?.save_backup_guard ?? true,
        syntax_validator: newConfig.skills?.syntax_validator ?? true,
        code_dedup: newConfig.skills?.code_dedup ?? true,
        downgrade_wizard: newConfig.skills?.downgrade_wizard ?? true
      },
      gemini_api_key: mergedGeminiKey,
      deepseek_api_key: mergedDeepSeekKey,
      custom_endpoint: (newConfig.custom_endpoint || existingConfig.custom_endpoint || '').trim(),
      custom_api_key: mergedCustomKey,
      custom_model: (newConfig.custom_model || existingConfig.custom_model || '').trim(),
      updated_at: new Date().toISOString()
    };

    const configJson = JSON.stringify(updatedConfig);

    await db.prepare(`
      INSERT INTO system_settings (key, value, description, updated_at)
      VALUES ('ai_config', ?, '老L·AI Copilot 智库系统人设、技能编排与大模型路由配置', CURRENT_TIMESTAMP)
      ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
    `).bind(configJson).run();

    await logAdminAction(db, {
      action: 'update_ai_config',
      entity: 'system_settings',
      entity_id: 'ai_config',
      details: {
        tone: updatedConfig.tone,
        primary_model: updatedConfig.primary_model,
        skills: Object.keys(updatedConfig.skills).filter(k => updatedConfig.skills[k]),
        has_gemini_key: !!updatedConfig.gemini_api_key,
        has_deepseek_key: !!updatedConfig.deepseek_api_key
      },
      admin_user: admin.username,
      client_ip: clientIP
    });

    // 返回脱敏后的安全配置对象
    const clientSafeResponse = {
      ...updatedConfig,
      gemini_api_key: maskKey(updatedConfig.gemini_api_key || env.GEMINI_API_KEY),
      has_gemini_key: !!(updatedConfig.gemini_api_key || env.GEMINI_API_KEY),
      deepseek_api_key: maskKey(updatedConfig.deepseek_api_key || env.DEEPSEEK_API_KEY),
      has_deepseek_key: !!(updatedConfig.deepseek_api_key || env.DEEPSEEK_API_KEY),
      custom_api_key: maskKey(updatedConfig.custom_api_key),
      has_custom_key: !!updatedConfig.custom_api_key
    };

    return new Response(JSON.stringify({
      code: 0,
      message: '老L·AI 官方智库顾问人设、模型路由与 Skills 技能编排已热更新！即刻全网生效',
      data: clientSafeResponse
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to save AI configuration',
      details: err.message
    }), { status: 500 });
  }
}
