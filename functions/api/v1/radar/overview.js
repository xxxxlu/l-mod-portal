/**
 * Cloudflare Pages Function: /api/v1/radar/overview
 * Steam 更新雷达概况：红黄绿数量 + 需要留意的游戏 + 站长手动广播。
 *
 * 数据来源：public/radar_status.json（每日巡检脚本生成，见 ../../_radar_status.js），不读 D1 的旧雷达列。
 * D1 只用来读站长在后台设置的紧急广播（system_settings.emergency_broadcast）；没有 D1 时广播为 null，其余照常。
 */

import {
  loadRadarStatus, radarCounts, radarList, radarUnavailableResponse, RADAR_METHOD_NOTE
} from '../../_radar_status.js';

export async function onRequestGet(context) {
  const { env } = context;

  const status = await loadRadarStatus(context);
  if (!status) return radarUnavailableResponse();

  const counts = radarCounts(status);
  const alerts = radarList(status).filter(g => g.compatibility_status !== 'green');

  // 站长手动广播（后台 /api/v1/admin/radar/broadcast 写）；读不到不影响雷达数据
  let emergencyBroadcast = null;
  const db = env.DB || env.lmod_vault_db;
  if (db) {
    try {
      const bRow = await db.prepare("SELECT value FROM system_settings WHERE key = 'emergency_broadcast'").first();
      if (bRow?.value) emergencyBroadcast = JSON.parse(bRow.value);
    } catch (e) {}
  }

  return new Response(JSON.stringify({
    code: 0,
    message: 'success',
    data: {
      source: 'radar_status.json',
      updated_at: status.updatedAt,
      method: RADAR_METHOD_NOTE,
      metrics: { green: counts.green, yellow: counts.yellow, red: counts.red },
      total_tracked: counts.total,
      active_alerts_count: alerts.length,
      active_alerts: alerts,
      emergency_broadcast: emergencyBroadcast
    }
  }), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=60, s-maxage=300'
    }
  });
}
