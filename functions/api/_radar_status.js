/**
 * 补丁雷达 v2 结果读取（Cloudflare Pages Functions 共用）
 * ==============================================================================
 * 雷达结果的唯一来源是每天定时任务写的 public/data.js（GAMES_DATA）。脚本
 * scripts/steam_patch_monitor.py 写 data.js 的同时生成 public/radar_status.json
 * （游戏 id → v2 雷达字段，约 80 KB），Functions 只读这个小文件：
 *   - 不读 D1 games 表里的旧雷达列（compatibility_status / verified_patch / latest_steam_patch /
 *     radar_risk_title / radar_risk_desc / radar_summary）：那是早期手灌的数据，定时任务不写 D1；
 *   - 不在 Function 里解析 1.4 MB 的 data.js（免费版 CPU 时间不够）。
 * 字段含义见 docs/RADAR_V2_CONTRACT.md 和 docs/STEAM_PATCH_MONITOR_GUIDE.md。
 */

const RADAR_STATUS_PATH = '/radar_status.json';
const CACHE_TTL_MS = 60 * 1000;

export const RADAR_STATUSES = ['red', 'yellow', 'green'];

// 判定方法的一句话说明：AI 回答和公开接口都带上，防止被读成「实测结论」
export const RADAR_METHOD_NOTE =
  '雷达每天比对 Steam 公共分支的更新时间（build 发布时间），没有做实机测试；' +
  'Steam 的更新时间分不出这次改没改 exe，所以红灯也只说「可能」。';

// D1 games 表里的旧雷达列（snake_case）和 raw_json 里对应的旧字段（camelCase）：一律不再对外输出
export const LEGACY_RADAR_COLUMNS = [
  'verified_patch', 'latest_steam_patch', 'compatibility_status',
  'radar_risk_title', 'radar_risk_desc', 'radar_summary'
];
const LEGACY_RADAR_KEYS = [
  'verifiedPatch', 'compatibilityStatus', 'radarStatusText', 'radarSummary', 'radarRiskTitle', 'radarRiskDesc',
  'latestSteamPatch', 'latestSteamPatchUrl', 'steamBuildId', 'steamBuildUpdatedAt', 'steamLastChecked',
  'emergencyAlert', 'radarReason', 'radarFramework', 'radarAdvice'
];
// 从 radar_status.json 覆盖回 raw_json（data.js 形状）时用的字段
const V2_DATA_KEYS = [
  'compatibilityStatus', 'radarReason', 'radarStatusText', 'steamBuildId', 'steamBuildUpdatedAt', 'steamLastChecked',
  'latestSteamPatch', 'latestSteamPatchUrl', 'radarFramework', 'radarAdvice', 'radarSummary'
];

let cached = null; // { at, origin, data }

function isValidStatus(data) {
  return Boolean(data && data.version === 2 && data.games && typeof data.games === 'object' && !Array.isArray(data.games));
}

/**
 * 读 public/radar_status.json；读不到或格式不对返回 null（调用方按「雷达数据暂不可用」降级）。
 * 同一个 isolate 里缓存 60 秒：线上每次发版都是新 isolate，本地 pages dev 改了文件一分钟内生效。
 */
export async function loadRadarStatus(context) {
  const env = (context && context.env) || {};
  if (!env.ASSETS || typeof env.ASSETS.fetch !== 'function') return null;
  let origin = 'https://lmod.local';
  try {
    if (context.request && context.request.url) origin = new URL(context.request.url).origin;
  } catch (e) {}
  const now = Date.now();
  if (cached && cached.origin === origin && now - cached.at < CACHE_TTL_MS) return cached.data;

  let data = null;
  try {
    const res = await env.ASSETS.fetch(new Request(origin + RADAR_STATUS_PATH));
    if (res.ok) {
      // 文件不存在时 _redirects 的 SPA 兜底会回 index.html（200），所以必须校验内容
      const parsed = JSON.parse(await res.text());
      if (isValidStatus(parsed)) data = parsed;
    }
  } catch (e) {
    data = null;
  }
  cached = { at: now, origin, data };
  return data;
}

export function radarEntry(status, gameId) {
  if (!status || !gameId) return null;
  return Object.prototype.hasOwnProperty.call(status.games, gameId) ? status.games[gameId] : null;
}

export function radarCounts(status) {
  const counts = { green: 0, yellow: 0, red: 0 };
  if (!status) return { ...counts, total: 0 };
  for (const entry of Object.values(status.games)) {
    if (entry.compatibilityStatus in counts) counts[entry.compatibilityStatus]++;
  }
  return { ...counts, total: counts.green + counts.yellow + counts.red };
}

export function radarIdsWithStatus(status, wanted) {
  if (!status) return [];
  return Object.entries(status.games)
    .filter(([, e]) => e.compatibilityStatus === wanted)
    .map(([id]) => id);
}

/** 原因码 → 一句中文解释（给 AI 和公开接口用；和雷达页的判定规则一致） */
export function radarReasonText(entry, status) {
  if (!entry) return null;
  const days = (status && status.recentDays) || 14;
  const fw = entry.radarFramework && entry.radarFramework.name;
  switch (entry.radarReason) {
    case 'recent-update-hooks':
      return `Steam 近 ${days} 天推送了新版本，这款游戏常用的 ${fw || 'Mod 框架'} 按游戏 exe 的具体版本挂钩，可能要等作者发新版才能用。`;
    case 'recent-update':
      return `Steam 近 ${days} 天推送了新版本，依赖框架的 Mod 和修改器可能要等作者适配。`;
    case 'trainer-behind':
      return '游戏近 90 天内有更新，而风灵月影修改器的更新时间比当前游戏版本早，部分功能可能对不上。';
    case 'quiet':
      return `Steam 公共分支近 ${days} 天没有新版本（近 90 天内有更新的，修改器也不比游戏旧）。`;
    default:
      return null;
  }
}

/** 「更新后怎么办」：优先用框架资料里的建议，没有就用和脚本同源的通用建议 */
export function radarAfterUpdate(entry, status, lang = 'zh-CN') {
  if (!entry) return null;
  const advice = entry.radarAdvice;
  if (advice && advice[lang]) return advice[lang];
  if (lang !== 'zh-CN') return null;
  const generic = (status && status.genericAdvice) || {};
  return generic[entry.radarReason] || generic.default || null;
}

/** UTC ISO → 'YYYY-MM-DD'（UTC 日期） */
export function radarDay(iso) {
  if (!iso || typeof iso !== 'string') return null;
  const d = new Date(iso);
  return isNaN(d.getTime()) ? null : d.toISOString().slice(0, 10);
}

export function radarDaysAgo(iso, now = Date.now()) {
  if (!iso) return null;
  const t = new Date(iso).getTime();
  if (isNaN(t)) return null;
  return Math.max(0, Math.floor((now - t) / 86400000));
}

/** 对外接口里的 radar 对象（snake_case）；没有 v2 巡检记录时为 null */
export function radarApiObject(entry, status) {
  if (!entry) return null;
  return {
    status: entry.compatibilityStatus,
    reason: entry.radarReason,
    status_text: entry.radarStatusText || null,
    reason_text: radarReasonText(entry, status),
    summary: entry.radarSummary || null,
    steam_build_id: entry.steamBuildId || null,
    steam_build_updated_at: entry.steamBuildUpdatedAt || null,
    last_checked_at: entry.steamLastChecked || null,
    framework: entry.radarFramework || null,
    after_update: radarAfterUpdate(entry, status, 'zh-CN'),
    after_update_en: radarAfterUpdate(entry, status, 'en'),
    latest_announcement: entry.latestSteamPatchUrl
      ? { title: entry.latestSteamPatch || null, url: entry.latestSteamPatchUrl }
      : null
  };
}

/** 给大模型的雷达块：原因、Steam 更新时间、框架、更新后怎么办都在里面 */
export function radarContextFor(gameId, status, steamAppId) {
  const entry = radarEntry(status, gameId);
  if (!entry) {
    if (!status) return { tracked: false, note: '雷达数据暂时读不到，不要猜测这款游戏的更新状态。' };
    if (steamAppId === 0 || steamAppId === '0') return { tracked: false, note: '这款游戏不在 Steam 上，雷达不巡检。' };
    return { tracked: false, note: '这款游戏还没有雷达巡检记录。' };
  }
  return {
    tracked: true,
    status: entry.compatibilityStatus,
    status_text: entry.radarStatusText || null,
    reason: entry.radarReason,
    reason_text: radarReasonText(entry, status),
    summary: entry.radarSummary || null,
    steam_build_id: entry.steamBuildId || null,
    steam_updated_on: radarDay(entry.steamBuildUpdatedAt),
    steam_build_updated_at: entry.steamBuildUpdatedAt || null,
    last_checked_on: radarDay(entry.steamLastChecked),
    framework: entry.radarFramework || null,
    after_update: radarAfterUpdate(entry, status, 'zh-CN'),
    latest_announcement: entry.latestSteamPatchUrl
      ? { title: entry.latestSteamPatch || null, url: entry.latestSteamPatchUrl }
      : null,
    method_note: RADAR_METHOD_NOTE
  };
}

/** 一款游戏在雷达列表接口里的样子 */
export function radarListItem(id, entry, status) {
  return {
    id,
    rank: entry.rank,
    title: entry.title,
    title_zh: entry.titleZh || entry.title,
    steam_app_id: entry.steamAppId,
    compatibility_status: entry.compatibilityStatus,
    radar: radarApiObject(entry, status)
  };
}

/** 全部有记录的游戏，红 → 黄 → 绿，同色按排名 */
export function radarList(status, wanted = null) {
  if (!status) return [];
  const order = { red: 0, yellow: 1, green: 2 };
  return Object.entries(status.games)
    .filter(([, e]) => !wanted || e.compatibilityStatus === wanted)
    .sort(([, a], [, b]) => (order[a.compatibilityStatus] ?? 3) - (order[b.compatibilityStatus] ?? 3) || (a.rank || 0) - (b.rank || 0))
    .map(([id, e]) => radarListItem(id, e, status));
}

/** D1 行：去掉旧雷达列，换成 v2 的 compatibility_status + radar（没有记录时都是 null） */
export function withRadar(row, status) {
  if (!row) return row;
  const out = { ...row };
  for (const col of LEGACY_RADAR_COLUMNS) delete out[col];
  const entry = radarEntry(status, row.id);
  out.compatibility_status = entry ? entry.compatibilityStatus : null;
  out.radar = radarApiObject(entry, status);
  return out;
}

/** raw_json（data.js 形状的整份游戏数据）：去掉旧雷达字段，换成 v2 字段 */
export function withRadarRawGame(game, status) {
  if (!game || typeof game !== 'object') return game;
  const out = { ...game };
  for (const key of LEGACY_RADAR_KEYS) delete out[key];
  const entry = radarEntry(status, game.id);
  if (entry) {
    for (const key of V2_DATA_KEYS) {
      if (entry[key] !== undefined) out[key] = entry[key];
    }
  }
  return out;
}

export function radarUnavailableResponse(extraHeaders = {}) {
  return new Response(JSON.stringify({
    code: 50300,
    message: 'Radar data unavailable: public/radar_status.json is missing or invalid'
  }), {
    status: 503,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...extraHeaders }
  });
}
