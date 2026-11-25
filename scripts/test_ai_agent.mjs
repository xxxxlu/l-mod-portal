/**
 * scripts/test_ai_agent.mjs
 * ==============================================================================
 * L-MOD Vault - AI Agent, Skills Orchestration & Admin Plane Unit Tests
 * ==============================================================================
 */

import { DatabaseSync } from 'node:sqlite';
import { onRequestPost as chatHandler } from '../functions/api/v1/ai/chat.js';
import { onRequestGet as configGetHandler, onRequestPost as configPostHandler } from '../functions/api/v1/admin/ai/config.js';
import { onRequestPost as testSandboxHandler } from '../functions/api/v1/admin/ai/test.js';

// 模拟 Cloudflare D1 驱动适配器 (基于 Node.js 原生 DatabaseSync)
class MockD1Database {
  constructor(dbPath) {
    this.sqlite = new DatabaseSync(dbPath);
  }

  prepare(sql) {
    const sqlite = this.sqlite;
    return {
      bind(...params) {
        return {
          async first() {
            const stmt = sqlite.prepare(sql);
            return stmt.get(...params);
          },
          async all() {
            const stmt = sqlite.prepare(sql);
            const rows = stmt.all(...params);
            return { results: rows };
          },
          async run() {
            const stmt = sqlite.prepare(sql);
            return stmt.run(...params);
          }
        };
      },
      async first() {
        const stmt = sqlite.prepare(sql);
        return stmt.get();
      },
      async all() {
        const stmt = sqlite.prepare(sql);
        const rows = stmt.all();
        return { results: rows };
      },
      async run() {
        const stmt = sqlite.prepare(sql);
        return stmt.run();
      }
    };
  }
}

async function runTests() {
  console.log('\n======================================================');
  console.log('🧪 开始运行 L-MOD Vault AI 官方智能体与 Skills 单元测试');
  console.log('======================================================\n');

  const mockDb = new MockD1Database('./database/lmod_vault.db');
  const mockEnv = {
    DB: mockDb,
    lmod_vault_db: mockDb
  };

  let totalTests = 0;
  let passedTests = 0;

  function assert(condition, message) {
    totalTests++;
    if (condition) {
      console.log(`  ✔ [PASS] ${message}`);
      passedTests++;
    } else {
      console.error(`  ✖ [FAIL] ${message}`);
      process.exitCode = 1;
    }
  }

  // ---------------------------------------------------------------------------
  // 测试用例 1: GET /api/v1/admin/ai/config 密钥脱敏与配置读取
  // ---------------------------------------------------------------------------
  console.log('==> 测试 1: 中台 AI 配置获取与密钥脱敏测试 (GET /api/v1/admin/ai/config)');
  {
    const req = new Request('https://lmod-vault.pages.dev/api/v1/admin/ai/config', { method: 'GET' });
    const res = await configGetHandler({ request: req, env: mockEnv });
    assert(res.status === 200, 'HTTP 响应状态码应为 200');

    const json = await res.json();
    assert(json.code === 0, '业务响应 code 应为 0');
    assert(json.data && json.data.system_prompt, '系统提示词配置应存在');
    assert(json.data.skills && json.data.skills.game_vault_rag !== undefined, 'skills 字典应包含 4 大专属核心技能');
    assert(typeof json.data.gemini_api_key === 'string', 'gemini_api_key 应为字符串格式');
    if (json.data.gemini_api_key) {
      assert(json.data.gemini_api_key.includes('****'), 'API Key 必须脱敏为 **** 掩码');
    }
  }

  // ---------------------------------------------------------------------------
  // 测试用例 2: POST /api/v1/admin/ai/config 保存配置与掩码保护
  // ---------------------------------------------------------------------------
  console.log('\n==> 测试 2: 中台 AI 配置热更新与技能开关测试 (POST /api/v1/admin/ai/config)');
  {
    const newConfigPayload = {
      system_prompt: '你是由 L-MOD Vault 官方研发的‘老L’——首席单机游戏指令与避坑顾问。',
      tone: 'hardcore_veteran',
      primary_model: 'gemini-2.5-flash',
      fallback_model: 'deepseek-chat',
      gemini_api_key: 'AIzaSyFakeKeyForTest1234567890',
      deepseek_api_key: 'sk-fakeDeepSeekKey1234567890',
      skills: {
        game_vault_rag: true,
        patch_sentinel: true,
        crash_diagnostic: true,
        general_oracle: true,
        save_backup_guard: true,
        syntax_validator: true,
        code_dedup: true
      }
    };

    const req = new Request('https://lmod-vault.pages.dev/api/v1/admin/ai/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newConfigPayload)
    });

    const res = await configPostHandler({ request: req, env: mockEnv, data: { admin: { username: 'test_admin' } } });
    assert(res.status === 200, '保存配置 HTTP 状态应为 200');
    const json = await res.json();
    assert(json.code === 0, '保存成功返回 code === 0');
    assert(json.data.has_gemini_key === true, '应标识 gemini_api_key 已挂载');
    assert(json.data.gemini_api_key.includes('****'), '返回给前端的 key 依然做安全脱敏');

    // 再次提交原脱敏掩码，验证真实 key 不会被冲掉
    const keepMaskPayload = {
      ...newConfigPayload,
      gemini_api_key: json.data.gemini_api_key // 携带掩码
    };
    const req2 = new Request('https://lmod-vault.pages.dev/api/v1/admin/ai/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(keepMaskPayload)
    });
    const res2 = await configPostHandler({ request: req2, env: mockEnv, data: { admin: { username: 'test_admin' } } });
    const json2 = await res2.json();
    assert(json2.data.has_gemini_key === true, '携带掩码更新时真实 key 应保留未丢失');
  }

  // ---------------------------------------------------------------------------
  // 测试用例 3: POST /api/v1/admin/ai/test 沙盒 4 大 Skills 模拟
  // ---------------------------------------------------------------------------
  console.log('\n==> 测试 3: 中台 4 大 Skills 沙盒诊断测试 (POST /api/v1/admin/ai/test)');
  {
    const req = new Request('https://lmod-vault.pages.dev/api/v1/admin/ai/test', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: '2077 怎么刷钱和强尼银手手枪？',
        game_id: 'cyberpunk-2077'
      })
    });

    const res = await testSandboxHandler({ request: req, env: mockEnv });
    assert(res.status === 200, '沙盒测试接口状态为 200');
    const json = await res.json();
    assert(json.code === 0, '沙盒测试返回成功');
    assert(json.data.skills_audit.game_vault_rag.status === 'HIT', '技能 A (Game Vault RAG) 应当精准命中代码');
    assert(json.data.skills_audit.patch_sentinel.status === 'COMPATIBLE', '技能 B (Patch Sentinel) 应当输出补丁兼容状态');
    assert(json.data.skills_audit.save_backup_guard.status === 'ALERT_ATTACHED', '坏档预防守卫应当触发警告');
  }

  // ---------------------------------------------------------------------------
  // 测试用例 4: POST /api/v1/ai/chat 官方智能体流式输出与 RAG 技能编排
  // ---------------------------------------------------------------------------
  console.log('\n==> 测试 4: 官方智能体流式聊天接口测试 (POST /api/v1/ai/chat - SSE Stream)');
  {
    const req = new Request('https://lmod-vault.pages.dev/api/v1/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: '赛博朋克2077无限金币代码',
        game_id: 'cyberpunk-2077',
        stream: true
      })
    });

    const res = await chatHandler({ request: req, env: mockEnv });
    assert(res.status === 200, 'SSE 流式接口响应状态应为 200');
    assert(res.headers.get('Content-Type').includes('text/event-stream'), 'Content-Type 应为 text/event-stream');

    // 读取 ReadableStream 并验证 SSE 事件包
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let accumulated = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      accumulated += decoder.decode(value);
    }

    assert(accumulated.includes('event: meta'), 'SSE 应首先推送包含技能元数据的 meta 事件');
    assert(accumulated.includes('event: delta'), 'SSE 应持续推送 delta 打字机字符事件');
    assert(accumulated.includes('event: done'), 'SSE 传输完毕后应推送 done 事件');
    assert(accumulated.includes('Game.AddToInventory') || accumulated.includes('money') || accumulated.includes('金币'), '流式回复应包含 2077 真实金币指令代码');
    assert(accumulated.includes('避坑警示') || accumulated.includes('备份'), '流式回复应包含高危坏档避坑警示');
  }

  // ---------------------------------------------------------------------------
  // 测试用例 5: 崩溃报错与闪退诊断 (技能 C: Crash Diagnostic)
  // ---------------------------------------------------------------------------
  console.log('\n==> 测试 5: 崩溃报错语义触发 (技能 C: Crash Diagnostic)');
  {
    const req = new Request('https://lmod-vault.pages.dev/api/v1/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: '黑神话悟空打mod闪退报错0xc0000005怎么办',
        game_id: 'black-myth-wukong',
        stream: false
      })
    });

    const res = await chatHandler({ request: req, env: mockEnv });
    assert(res.status === 200, '非流式接口响应状态应为 200');
    const json = await res.json();
    assert(json.code === 0, '非流式响应成功');
    assert(json.data.skills_triggered.some(s => s.id === 'crash_diagnostic'), '应成功触发技能 C: 报错闪退崩溃诊断');
    assert(json.data.text.includes('DX12') || json.data.text.includes('UE4SS') || json.data.text.includes('着色器') || json.data.text.includes('-dx11'), '回复应包含虚幻引擎 5 专属 DX12/-dx11 逃课排查要点');
  }

  // ---------------------------------------------------------------------------
  // 测试用例 6: 全域通识问答 (技能 D: General Gaming Oracle)
  // ---------------------------------------------------------------------------
  console.log('\n==> 测试 6: 全域单机通识问答 (技能 D: General Gaming Oracle)');
  {
    const req = new Request('https://lmod-vault.pages.dev/api/v1/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: 'Mod Organizer 2 和 Vortex 哪个更好用？如何配置虚拟文件树？',
        stream: false
      })
    });

    const res = await chatHandler({ request: req, env: mockEnv });
    const json = await res.json();
    assert(json.code === 0, '通识提问响应成功');
    assert(json.data.skills_triggered.some(s => s.id === 'general_oracle'), '未收录特定游戏时应触发技能 D: 全域通识问答');
  }

  console.log('\n======================================================');
  console.log(`🎉 全部测试完成: ${passedTests} / ${totalTests} 通过！`);
  console.log('======================================================\n');
}

runTests().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
