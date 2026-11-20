/**
 * Cloudflare Pages Function: GET /api/v1/admin/radar/status
 * 后台雷达面板：红黄绿数量、最近 Steam 有更新的游戏、巡检计划、站长广播。
 *
 * 雷达数据来自 public/radar_status.json 的 v2 结果（见 ../../../_radar_status.js）：
 *   - 不再按 D1 旧雷达列统计；
 *   - recent_logs 改为「Steam 最近更新的 20 款」（字段沿用旧的日志行形状，后台表格不用改），
 *     不再读 patch_radar_logs（那张表是早期灌库和旧「手动巡检」随机生成的模拟记录）。
 * D1 只用来读站长广播。
 */

import { loadRadarStatus, radarCounts, RADAR_METHOD_NOTE } from '../../../_radar_status.js';

export async function onRequestGet(context) {
  const { env } = context;
  const db = env.DB || env.lmod_vault_db;

  try {
    const radarStatus = await loadRadarStatus(context);
    const counts = radarCounts(radarStatus);

    let totalGames = null;
    let emergencyBroadcast = null;
    if (db) {
      try {
        const totalRow = await db.prepare('SELECT count(*) AS total FROM games').first();
        totalGames = totalRow ? totalRow.total : null;
      } catch (e) {}
      try {
        const broadcastRow = await db.prepare("SELECT value FROM system_settings WHERE key = 'emergency_broadcast'").first();
        if (broadcastRow?.value) emergencyBroadcast = JSON.parse(broadcastRow.value);
      } catch (e) {}
    }

    const recent = radarStatus
      ? Object.entries(radarStatus.games)
        .filter(([, e]) => e.steamBuildUpdatedAt)
        .sort(([, a], [, b]) => String(b.steamBuildUpdatedAt).localeCompare(String(a.steamBuildUpdatedAt)))
        .slice(0, 20)
        .map(([id, e]) => ({
          game_id: id,
          game_title: e.title,
          game_title_zh: e.titleZh || e.title,
          steam_app_id: e.steamAppId,
          patch_title: e.latestSteamPatch || '（没有官方公告标题）',
          patch_date: e.steamBuildUpdatedAt,
          build_id: e.steamBuildId || null,
          status: e.compatibilityStatus,
          risk_title: e.radarStatusText || null,
          risk_desc: e.radarSummary || null,
          checked_at: e.steamLastChecked || null
        }))
      : [];

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        radar_source: radarStatus ? 'radar_status.json' : null,
        radar_method: RADAR_METHOD_NOTE,
        radar_metrics: {
          green: counts.green,
          yellow: counts.yellow,
          red: counts.red,
          tracked: counts.total,
          unchecked: totalGames !== null ? Math.max(0, totalGames - counts.total) : null,
          total: totalGames !== null ? totalGames : counts.total
        },
        sentinel_scheduler: {
          runner: 'GitHub Actions · .github/workflows/patch_radar_cron.yml',
          schedule: '每天 UTC 02:00（北京时间 10:00）',
          last_scan_at: radarStatus ? radarStatus.updatedAt : null,
          scope: '全部带 Steam AppID 的游戏',
          notify_on_break: '只在「新变红」时开 GitHub Issue 或评论'
        },
        emergency_broadcast: emergencyBroadcast,
        recent_logs: recent,
        total_logs_count: recent.length
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'no-store'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to retrieve radar status',
      details: err.message
    }), { status: 500 });
  }
}
