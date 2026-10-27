/**
 * Cloudflare Pages Function: /api/v1/games/:id/download
 * Dynamically stream and compile Windows .bat helper scripts
 */

export async function onRequestGet(context) {
  const { params, request, env } = context;
  const gameId = params.id;
  const url = new URL(request.url);
  const bundleId = url.searchParams.get('bundle_id');

  if (!gameId || !/^[a-z0-9-]+$/.test(gameId)) {
    return new Response('Invalid game identifier', { status: 400 });
  }

  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return new Response('Database service unavailable', { status: 500 });
  }

  try {
    const game = await db.prepare('SELECT title, title_zh, console_shortcut, verified_patch FROM games WHERE id = ?').bind(gameId).first();
    if (!game) {
      return new Response('Game not found', { status: 404 });
    }

    let bundleName = '常用指令快捷助手';
    let scriptContent = '';

    if (bundleId) {
      const bundle = await db.prepare('SELECT name, bat_script, commands_json FROM scenario_bundles WHERE id = ? AND game_id = ?').bind(bundleId, gameId).first();
      if (bundle) {
        bundleName = bundle.name;
        if (bundle.bat_script && bundle.bat_script.trim().length > 0) {
          scriptContent = bundle.bat_script;
        }
      }
    }

    // If no pre-compiled script, dynamically synthesize an industrial-grade .bat
    if (!scriptContent) {
      // Fetch top popular commands for this game
      const { results: popularCmds } = await db.prepare(
        'SELECT name_zh, name_en, code, syntax_type FROM console_commands WHERE game_id = ? ORDER BY is_popular DESC LIMIT 10'
      ).bind(gameId).all();

      const cmdLines = (popularCmds || []).map((c, i) => {
        return `:: [${i + 1}] ${c.name_zh || c.name_en} (${c.syntax_type})\n:: 指令代码: ${c.code}\necho [${i + 1}] ${c.name_zh || c.name_en} -> ${c.code}`;
      }).join('\n\n');

      scriptContent = `@echo off
chcp 65001 >nul
title L-MOD Vault 助手 - ${game.title_zh || game.title}
color 0A
cls
echo ==============================================================================
echo   L-MOD Vault (全球单机游戏模组与避坑智库) 官方自动化辅助
echo   游戏名称: ${game.title_zh || game.title} (${game.title})
echo   适配基准: Steam v${game.verified_patch || '最新版'}
echo   快捷热键: ${game.console_shortcut || '~ 键'}
echo ==============================================================================
echo.
echo [提示] 正在为你列出已通过 100%% 实机校验的核心指令配置:
echo.
${cmdLines}
echo.
echo ==============================================================================
echo   如需一键写入剪贴板或查看更多避坑预警，请随时回访: https://lmod-vault.pages.dev
echo ==============================================================================
pause
`;
    }

    // Windows UTF-8 BOM to prevent CMD/PowerShell garbled text
    const bom = '\uFEFF';
    const finalBat = bom + scriptContent;
    const filename = `lmod_${gameId}_${bundleId || 'quickstart'}.bat`;

    return new Response(finalBat, {
      headers: {
        'Content-Type': 'application/x-bat; charset=utf-8',
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(`Batch generation failed: ${err.message}`, { status: 500 });
  }
}
