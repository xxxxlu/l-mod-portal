/**
 * Cloudflare Pages Function: /api/v1/admin/ai/config
 * Lao-L AI Copilot & Skills Studio Configuration Plane
 */

import { logAdminAction } from '../_auth.js';

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  if (!db) {
    return new Response(JSON.stringify({ code: 50000, message: 'Database binding missing' }), { status: 500 });
  }

  try {
    const row = await db.prepare(
      'SELECT value, updated_at FROM system_settings WHERE key = "ai_config"'
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
      // Default fallback
      config = {
        system_prompt: '你是由 L-MOD Vault 官方研发的‘老L’——全球单机游戏底层指令与避坑智库首席顾问。你精通 CET Lua、UE4SS、Creation Engine 控制台语法与反作弊机制。你的回答风格：言简意赅、老练严谨、绝不废话、直击痛点。遇到破坏存档或与补丁冲突的高危指令，必须第一时间发出红色预警并给出备份方案。',
        tone: 'hardcore_veteran',
        tone_label: '资深单机老炮 / 严谨避坑顾问',
        temperature: 0.3,
        recall_threshold: 0.65,
        max_context_commands: 6,
        primary_model: 'gemini-2.5-flash',
        fallback_model: 'deepseek-chat',
        skills: {
          code_dedup: true,
          syntax_validator: true,
          steam_diff: true,
          downgrade_wizard: true,
          save_backup_guard: true
        },
        custom_rules: [
          '所有控制台代码必须经过真实游戏版本与引擎测试，严禁杜撰幻觉指令',
          '对于赛博朋克2077等使用CET框架的游戏，明确区分Lua代码与原生控制台代码',
          '对涉及等级、金钱过亿、跳过主线等高危指令，强制添加【坏档警示】'
        ],
        updated_at: new Date().toISOString()
      };
    }

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: config
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
      return new Response(JSON.stringify({ code: 40000, message: 'System prompt cannot be empty' }), { status: 400 });
    }

    newConfig.updated_at = new Date().toISOString();
    const configJson = JSON.stringify(newConfig);

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
        tone: newConfig.tone,
        primary_model: newConfig.primary_model,
        recall_threshold: newConfig.recall_threshold,
        active_skills: Object.keys(newConfig.skills || {}).filter(k => newConfig.skills[k])
      },
      admin_user: admin.username,
      client_ip: clientIP
    });

    return new Response(JSON.stringify({
      code: 0,
      message: '老L·AI 智库顾问人设与技能编排已热更新！即刻全网生效',
      data: newConfig
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
