/**
 * Cloudflare Pages Function: GET / POST /api/v1/admin/analytics/config
 * The telemetry sampling switch (system_settings.telemetry_config). Default sample_rate 1 = record everything.
 * Lower it only when traffic nears the free D1 / Functions quotas; the dashboard weights counts back up.
 */

import { logAdminAction } from '../_auth.js';
import { readTelemetryConfig } from './_rollup.js';

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}

export async function onRequestGet(context) {
  const db = context.env.DB || context.env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);
  return json({ code: 0, message: 'success', data: await readTelemetryConfig(db) });
}

export async function onRequestPost(context) {
  const { request, env, data } = context;
  const db = env.DB || env.lmod_vault_db;
  if (!db) return json({ code: 50000, message: 'Database binding missing' }, 500);

  let body;
  try { body = await request.json(); } catch (e) { return json({ code: 40000, message: 'Invalid JSON' }, 400); }
  const rate = Number(body && body.sample_rate);
  if (!Number.isFinite(rate) || rate < 0.01 || rate > 1) {
    return json({ code: 40000, message: 'sample_rate 必须在 0.01 到 1 之间（1 = 全量）' }, 400);
  }

  const before = await readTelemetryConfig(db);
  const next = { ...before, sample_rate: Math.round(rate * 100) / 100 };
  await db.prepare(
    `INSERT INTO system_settings (key, value, description, updated_at)
     VALUES ('telemetry_config', ?1, '访客统计：sample_rate 采样比例（0.01–1，1 = 全量记录）；retention_days 明细保留天数（之后只留按天汇总）', CURRENT_TIMESTAMP)
     ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP`
  ).bind(JSON.stringify(next)).run();

  await logAdminAction(db, {
    action: 'update_telemetry_config',
    entity: 'system_settings',
    entity_id: 'telemetry_config',
    details: { previous: before.sample_rate, updated: next.sample_rate },
    admin_user: (data && data.admin && data.admin.username) || 'admin',
    client_ip: request.headers.get('cf-connecting-ip') || '127.0.0.1'
  });

  return json({ code: 0, message: `采样比例已设为 ${Math.round(next.sample_rate * 100)}%（约 1 分钟内各节点生效）`, data: next });
}
