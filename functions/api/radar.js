/**
 * Cloudflare Pages Function: /api/radar（旧版接口，保留路径）
 * Steam 更新雷达状态。
 *
 * 数据来源：public/radar_status.json（每日巡检脚本生成，见 ./_radar_status.js），不读 D1 的旧雷达列。
 */

import { loadRadarStatus, radarCounts, radarList, RADAR_METHOD_NOTE } from './_radar_status.js';

export async function onRequestGet(context) {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'public, max-age=30, s-maxage=300'
  };

  const status = await loadRadarStatus(context);
  if (!status) {
    return new Response(JSON.stringify({
      status: 'unavailable',
      notice: 'Radar data unavailable (public/radar_status.json missing). See /radar.html for the static radar page.'
    }), { status: 503, headers: { ...corsHeaders, 'Cache-Control': 'no-store' } });
  }

  const counts = radarCounts(status);
  const games = radarList(status);

  return new Response(JSON.stringify({
    source: 'radar_status.json',
    updated_at: status.updatedAt,
    method: RADAR_METHOD_NOTE,
    metrics: { green: counts.green, yellow: counts.yellow, red: counts.red },
    total: games.length,
    games
  }), { headers: corsHeaders });
}
