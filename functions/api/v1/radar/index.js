/**
 * Cloudflare Pages Function: /api/v1/radar
 * Steam 更新雷达：全部有巡检记录的游戏（可按 ?status=red|yellow|green 过滤）。
 *
 * 数据来源：public/radar_status.json（每日巡检脚本生成，见 ../../_radar_status.js），不读 D1。
 */

import { loadRadarStatus, radarList, radarUnavailableResponse, RADAR_METHOD_NOTE, RADAR_STATUSES } from '../../_radar_status.js';

export async function onRequestGet(context) {
  const { request } = context;
  const url = new URL(request.url);
  const statusFilter = url.searchParams.get('status');
  const wanted = RADAR_STATUSES.includes(statusFilter) ? statusFilter : null;

  const status = await loadRadarStatus(context);
  if (!status) return radarUnavailableResponse();

  const items = radarList(status, wanted);

  return new Response(JSON.stringify({
    code: 0,
    message: 'success',
    data: {
      source: 'radar_status.json',
      updated_at: status.updatedAt,
      method: RADAR_METHOD_NOTE,
      filter: wanted || 'all',
      total: items.length,
      items
    }
  }), {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'public, max-age=60, s-maxage=300'
    }
  });
}
