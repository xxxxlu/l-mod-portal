/**
 * Cloudflare Pages Function: POST /api/v1/admin/radar/inspect
 * 后台「手动巡检」：返回每日巡检的最新结果。
 *
 * 以前这里会给每款游戏随机生成 build 号、写「全域验证通过 / 校验一致」并插进 D1 patch_radar_logs——
 * 那是模拟数据，不是真的巡检。现在真正的巡检只由 GitHub Actions 每天跑 scripts/steam_patch_monitor.py，
 * 结果在 public/radar_status.json（见 ../../../_radar_status.js）；这里只读它，不写 D1。
 * 返回字段沿用旧形状，后台终端显示不用改。
 */

import { loadRadarStatus, radarDay, radarList, radarEntry, radarListItem, radarUnavailableResponse } from '../../../_radar_status.js';

export async function onRequestPost(context) {
  const { request } = context;

  try {
    const body = await request.json().catch(() => ({}));
    const targetGameId = String(body.game_id || 'all').trim();

    const radarStatus = await loadRadarStatus(context);
    if (!radarStatus) return radarUnavailableResponse();

    let items;
    if (targetGameId === 'all') {
      items = radarList(radarStatus);
    } else {
      const entry = radarEntry(radarStatus, targetGameId);
      if (!entry) {
        return new Response(JSON.stringify({
          code: 40400,
          message: `「${targetGameId}」没有雷达巡检记录（不在 Steam 上，或 id 不存在）`
        }), { status: 404, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
      }
      items = [radarListItem(targetGameId, entry, radarStatus)];
    }

    const results = items.map(item => ({
      game_id: item.id,
      title_zh: item.title_zh,
      steam_app_id: item.steam_app_id,
      status: item.compatibility_status,
      verified_patch: null,
      latest_steam_patch: item.radar.steam_build_id
        ? `build ${item.radar.steam_build_id}（${radarDay(item.radar.steam_build_updated_at) || '日期未知'}）`
        : null,
      build_id: item.radar.steam_build_id,
      verdict: item.radar.status_text || item.radar.reason_text,
      reason: item.radar.reason,
      checked_at: item.radar.last_checked_at
    }));

    return new Response(JSON.stringify({
      code: 0,
      message: `已读取每日巡检结果（上次巡检 ${radarStatus.updatedAt || '未知'}，共 ${results.length} 款）。` +
        '实际巡检由 GitHub Actions 每天 UTC 02:00 运行，后台不再生成模拟记录。',
      data: {
        target: targetGameId,
        inspected_count: results.length,
        timestamp: radarStatus.updatedAt,
        source: 'radar_status.json',
        results
      }
    }), {
      headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to read radar inspection results',
      details: err.message
    }), { status: 500 });
  }
}
