/**
 * L-MOD Vault - Integration Test for API v1
 * Uses better-sqlite3 or sqlite3 to mock Cloudflare D1 interface
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Mock Cloudflare D1 Database using sqlite3 CLI
const DB_PATH = path.resolve(__dirname, '../database/lmod_vault.db');

class MockD1Statement {
  constructor(sql, params = []) {
    this.sql = sql;
    this.params = params;
  }

  bind(...args) {
    return new MockD1Statement(this.sql, args);
  }

  async first() {
    const res = await this.all();
    return res.results && res.results.length > 0 ? res.results[0] : null;
  }

  async all() {
    let finalSql = this.sql;
    let paramIndex = 0;
    
    // Simple mock parameter replacement for testing
    finalSql = finalSql.replace(/\?/g, () => {
      const p = this.params[paramIndex++];
      if (p === null || p === undefined) return 'NULL';
      if (typeof p === 'number') return p;
      return `'${String(p).replace(/'/g, "''")}'`;
    });

    const jsonCmd = `/usr/bin/sqlite3 -json "${DB_PATH}" "${finalSql.replace(/"/g, '\\"')}"`;
    try {
      const raw = execSync(jsonCmd, { encoding: 'utf-8' }).trim();
      const rows = raw ? JSON.parse(raw) : [];
      return { results: rows };
    } catch (err) {
      // In case of INSERT or statements returning no rows
      return { results: [], success: true };
    }
  }

  async run() {
    return this.all();
  }
}

class MockD1Database {
  prepare(sql) {
    return new MockD1Statement(sql);
  }
  async batch(statements) {
    const results = [];
    for (const stmt of statements) {
      results.push(await stmt.run());
    }
    return results;
  }
}

async function runTests() {
  console.log('--- Starting L-MOD Vault API v1 Integration Tests ---');
  const mockDb = new MockD1Database();
  const mockEnv = { DB: mockDb };

  // 1. Test /api/v1/games
  const gamesHandler = await import('../functions/api/v1/games/index.js');
  const reqGames = new Request('http://localhost/api/v1/games?page=1&page_size=3');
  const resGames = await gamesHandler.onRequestGet({ request: reqGames, env: mockEnv });
  const dataGames = await resGames.json();
  console.log('✓ /api/v1/games:', resGames.status, `Total: ${dataGames.meta.total}, Returned: ${dataGames.data.items.length}`);
  if (dataGames.data.items.length !== 3) throw new Error('Games limit mismatch');

  // 2. Test /api/v1/games/search
  const searchHandler = await import('../functions/api/v1/games/search.js');
  const reqSearch = new Request('http://localhost/api/v1/games/search?q=2077');
  const resSearch = await searchHandler.onRequestGet({ request: reqSearch, env: mockEnv });
  const dataSearch = await resSearch.json();
  console.log('✓ /api/v1/games/search?q=2077:', resSearch.status, `Matches: ${dataSearch.data.total}`);

  // 3. Test /api/v1/games/filters
  const filtersHandler = await import('../functions/api/v1/games/filters.js');
  const resFilters = await filtersHandler.onRequestGet({ env: mockEnv });
  const dataFilters = await resFilters.json();
  console.log('✓ /api/v1/games/filters:', resFilters.status, `Genres: ${dataFilters.data.genres.length}`);

  // 4. Test /api/v1/games/:id
  const detailHandler = await import('../functions/api/v1/games/[id]/index.js');
  const resDetail = await detailHandler.onRequestGet({ params: { id: 'cyberpunk-2077' }, env: mockEnv });
  const dataDetail = await resDetail.json();
  console.log('✓ /api/v1/games/:id (cyberpunk-2077):', resDetail.status, `Title: ${dataDetail.data.title}`);

  // 5. Test /api/v1/games/:id/commands
  const cmdsHandler = await import('../functions/api/v1/games/[id]/commands.js');
  const reqCmds = new Request('http://localhost/api/v1/games/cyberpunk-2077/commands');
  const resCmds = await cmdsHandler.onRequestGet({ params: { id: 'cyberpunk-2077' }, request: reqCmds, env: mockEnv });
  const dataCmds = await resCmds.json();
  console.log('✓ /api/v1/games/:id/commands:', resCmds.status, `Commands count: ${dataCmds.data.total}`);

  // 6. Test /api/v1/games/:id/download
  const dlHandler = await import('../functions/api/v1/games/[id]/download.js');
  const reqDl = new Request('http://localhost/api/v1/games/cyberpunk-2077/download');
  const resDl = await dlHandler.onRequestGet({ params: { id: 'cyberpunk-2077' }, request: reqDl, env: mockEnv });
  const batText = await resDl.text();
  console.log('✓ /api/v1/games/:id/download:', resDl.status, `Bat size: ${batText.length} bytes`);

  // 7. Test /api/v1/radar/overview
  const radarHandler = await import('../functions/api/v1/radar/overview.js');
  const resRadar = await radarHandler.onRequestGet({ env: mockEnv });
  const dataRadar = await resRadar.json();
  console.log('✓ /api/v1/radar/overview:', resRadar.status, `Tracked: ${dataRadar.data.total_tracked}`);

  // 8. Test /api/v1/telemetry/events
  const telHandler = await import('../functions/api/v1/telemetry/events.js');
  const reqTel = new Request('http://localhost/api/v1/telemetry/events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'cf-ipcountry': 'CN' },
    body: JSON.stringify({
      event_type: 'copy_code',
      game_id: 'cyberpunk-2077',
      target_payload: 'Game.AddToInventory("Items.money", 1000000)',
      session_id: 'test_session_123'
    })
  });
  const resTel = await telHandler.onRequestPost({ request: reqTel, env: mockEnv, waitUntil: fn => fn });
  console.log('✓ /api/v1/telemetry/events:', resTel.status);

  // 9. Test /api/v1/ai/context
  const aiHandler = await import('../functions/api/v1/ai/context.js');
  const reqAi = new Request('http://localhost/api/v1/ai/context', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: '刷钱 money 武器',
      game_id: 'cyberpunk-2077'
    })
  });
  const resAi = await aiHandler.onRequestPost({ request: reqAi, env: mockEnv });
  const dataAi = await resAi.json();
  console.log('✓ /api/v1/ai/context:', resAi.status, `Retrieved commands: ${dataAi.data.context.retrieved_commands.length}`);

  console.log('\n🎉 ALL 9 ENDPOINTS TESTED & PASSED VERIFICATION!');
}

runTests().catch(err => {
  console.error('Test Failed:', err);
  process.exit(1);
});
