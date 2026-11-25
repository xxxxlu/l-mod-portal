/**
 * 游戏数据「整份文档」的共用逻辑（公开目录接口 + 后台编辑接口共用）
 * ==============================================================================
 * 真源：D1 games.raw_json —— 和 public/data.js 里 GAMES_DATA 每一项同形的整份游戏数据。
 *   - 后台「游戏与指令运维」整份读写 raw_json；
 *   - games 表的其它列（title / has_console / pitfall_note …）、console_commands、scenario_bundles
 *     都是从 raw_json 派生出来的索引，每次保存在同一个 D1 batch（事务）里重建，给 AI 助手和旧接口查；
 *   - public/data.js 的 GAMES_DATA 只是快照（scripts/export_d1_snapshot.py 从 D1 导出），给前台兜底和定时任务用。
 *
 * 机器维护的字段不归后台改：
 *   - 雷达字段（steam_patch_monitor.py 每天写 data.js + public/radar_status.json）
 *   - 修改器字段（fling_trainer_sync.py 每天写 data.js + public/trainers.json）
 * 读的时候用 radar_status.json / trainers.json 叠加；后台保存时这些字段一律保留库里原值。
 */

import { withRadarRawGame } from '../../_radar_status.js';

// ---------------------------------------------------------------------------
// 字段划分
// ---------------------------------------------------------------------------

// 和 scripts/steam_patch_monitor.py RADAR_FIELDS 一致
export const RADAR_FIELDS = [
  'compatibilityStatus', 'radarReason', 'radarStatusText', 'latestSteamPatch', 'latestSteamPatchUrl',
  'steamBuildId', 'steamBuildUpdatedAt', 'steamLastChecked', 'radarFramework', 'radarAdvice',
  'radarSummary', 'radarRiskTitle', 'radarRiskDesc', 'emergencyAlert'
];
// 和 scripts/gamedata_guard.py TRAINER_FIELDS 一致
export const TRAINER_FIELDS = ['hasTrainer', 'trainerHotkeys', 'trainerInfo'];
export const MACHINE_FIELDS = [...RADAR_FIELDS, ...TRAINER_FIELDS];
const MACHINE_SET = new Set(MACHINE_FIELDS);

// 列表视图（首页卡片/列表/侧栏/搜索、雷达页）用不到的重字段：目录接口不返回，进详情再按需取整份。
// 雷达字段也先去掉，再由 radar_status.json 叠加回 v2 那几项。
export const LIST_OMITTED_FIELDS = [
  'consoleCategories', 'curatedMods', 'mustHaveMods', 'consoleEnableGuide', 'batScript',
  'scenarioBundles', 'pitfallNote', 'communityReviews', 'trainerInfo', 'trainerHotkeys',
  'latestPatch', 'verifiedPatch',
  ...RADAR_FIELDS
];

export const LANGS = ['zh-CN', 'en', 'zh-TW', 'ja', 'ko', 'ru', 'de', 'es'];
export const HEAT_TIERS = ['solar', 'violet', 'cyan', 'emerald'];
export const GAME_ID_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
export const MAX_DOC_BYTES = 300 * 1024;

// ---------------------------------------------------------------------------
// 目录版本号（system_settings.catalog_version）：后台每次保存 +1，接口的 ETag / 边缘缓存键都带它
// ---------------------------------------------------------------------------

export async function readCatalogVersion(db) {
  try {
    const row = await db.prepare("SELECT value FROM system_settings WHERE key = 'catalog_version'").first();
    if (row && row.value) {
      const v = JSON.parse(row.value);
      if (v && v.version !== undefined && v.version !== null) return String(v.version);
    }
  } catch (e) {}
  return '0';
}

export function bumpCatalogVersionStmt(db) {
  return db.prepare(
    `INSERT INTO system_settings (key, value, description, updated_at)
     VALUES ('catalog_version', json_object('version', 1, 'updated_at', strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
             '游戏目录版本号：后台保存游戏数据时 +1，公开目录接口靠它让缓存失效', CURRENT_TIMESTAMP)
     ON CONFLICT(key) DO UPDATE SET
       value = json_object('version', COALESCE(json_extract(system_settings.value, '$.version'), 0) + 1,
                           'updated_at', strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
       updated_at = CURRENT_TIMESTAMP`
  );
}

// ---------------------------------------------------------------------------
// trainers.json（风灵月影清单）：和 radar_status.json 一样从静态资源读，同一 isolate 缓存 60 秒
// ---------------------------------------------------------------------------

const TRAINERS_PATH = '/trainers.json';
const TRAINERS_TTL_MS = 60 * 1000;
let trainersCached = null; // { at, origin, data }

export async function loadTrainers(context) {
  const env = (context && context.env) || {};
  if (!env.ASSETS || typeof env.ASSETS.fetch !== 'function') return null;
  let origin = 'https://lmod.local';
  try {
    if (context.request && context.request.url) origin = new URL(context.request.url).origin;
  } catch (e) {}
  const now = Date.now();
  if (trainersCached && trainersCached.origin === origin && now - trainersCached.at < TRAINERS_TTL_MS) {
    return trainersCached.data;
  }
  let data = null;
  try {
    const res = await env.ASSETS.fetch(new Request(origin + TRAINERS_PATH));
    if (res.ok) {
      // 文件不存在时 SPA 兜底会回 index.html（200），所以要校验内容
      const parsed = JSON.parse(await res.text());
      if (parsed && parsed.games && typeof parsed.games === 'object' && !Array.isArray(parsed.games)) data = parsed;
    }
  } catch (e) {
    data = null;
  }
  trainersCached = { at: now, origin, data };
  return data;
}

// 以下照搬 scripts/fling_trainer_sync.py 的 CATEGORIES / categorize() / apply_to_game()，两边要一起改
const TRAINER_CATEGORIES = [
  ['combat', '⚔️ 战斗与生存 (Combat & Survival)',
    /health|\bhp\b|stamina|mana|\bmp\b|\bsp\b|\bfp\b|energy|god mode|damage|defen[cs]e|kill|ammo|reload|recoil|accuracy|spread|grenade|stealth|invisib|cooldown|shield|armor|oxygen|hunger|thirst|breath|sanity|rage|focus|adrenaline|durability|enemies|enemy|fall damage|healing|poison|bleed|status effect/],
  ['economy', '💰 资源与物品 (Resources & Items)',
    /money|gold|coin|cash|credit|item|resource|material|component|craft|currency|souls|runes|gems?|crystal|fuel|food|water|consumable|purchase|shop|build|upgrade|inventory|carry|weight|ram\b|lockpick|key/],
  ['progress', '📈 等级与属性 (Level & Stats)',
    /\bxp\b|\bexp\b|experience|level|skill|point|attribute|stat|perk|talent|ability|abilities|reputation|fame|cred|affinity|relationship|friendship|loyalty|prestige|influence|score/],
  ['world', '🌍 移动与世界 (Movement & World)',
    /speed|jump|fly|teleport|clip|time|day|weather|gravity|height|waypoint|location|position|map/]
];
const TRAINER_OTHER = ['other', '🧩 其他功能 (Other)'];

function categorizeHotkeys(hotkeys) {
  const groups = new Map();
  for (const hk of hotkeys) {
    const en = String(hk.en || '').toLowerCase();
    let cat = TRAINER_OTHER[0];
    for (const [cid, , re] of TRAINER_CATEGORIES) {
      if (re.test(en)) { cat = cid; break; }
    }
    if (!groups.has(cat)) groups.set(cat, []);
    groups.get(cat).push(hk);
  }
  const out = [];
  for (const [cid, label] of [...TRAINER_CATEGORIES.map(c => [c[0], c[1]]), TRAINER_OTHER]) {
    const items = groups.get(cid);
    if (!items) continue;
    out.push({
      category: label,
      items: items.map(h => ({
        key: h.key,
        action: h.zh ? `${h.zh} (${h.en})` : h.en,
        ...(h.tip ? { tip: h.tip } : {})
      }))
    });
  }
  return out;
}

/** 修改器三个字段（hasTrainer / trainerHotkeys / trainerInfo），和定时任务写进 data.js 的一致 */
export function trainerFieldsFor(gameId, trainers, { light = false } = {}) {
  const entry = trainers && Object.prototype.hasOwnProperty.call(trainers.games, gameId) ? trainers.games[gameId] : null;
  if (light) return { hasTrainer: Boolean(entry) };
  if (!entry) return { hasTrainer: false, trainerHotkeys: [], trainerInfo: {} };
  const hk = Array.isArray(entry.hotkeys) ? entry.hotkeys : [];
  return {
    hasTrainer: true,
    trainerHotkeys: hk.slice(0, 8).map(h => ({ key: h.key, action: h.zh ? `${h.en} (${h.zh})` : h.en })),
    trainerInfo: {
      author: '风灵月影 (FLiNG)',
      officialUrl: entry.url,
      version: entry.gameVersion || '见官方页面',
      optionsCount: entry.optionsCount,
      lastUpdated: entry.lastUpdated,
      platforms: entry.platforms,
      antiCheat: entry.antiCheat,
      offlineOnly: entry.offlineOnly,
      hotkeysCategorized: categorizeHotkeys(hk),
      source: 'trainers.json'
    }
  };
}

/**
 * 库里的整份文档 → 对外输出：雷达字段换成 radar_status.json 的 v2 结果，修改器字段换成 trainers.json 的结果。
 * 两份文件读不到时保留库里原值（雷达旧字段照旧去掉，见 _radar_status.js）。
 */
export function overlayMachineFields(doc, radarStatus, trainers, { light = false } = {}) {
  const out = withRadarRawGame(doc, radarStatus);
  if (trainers) Object.assign(out, trainerFieldsFor(doc.id, trainers, { light }));
  return out;
}

/** ETag：目录版本 + 两份机器数据的生成时间。任何一项变了缓存就失效。 */
export function catalogEtag(version, radarStatus, trainers, extra = '') {
  const r = (radarStatus && radarStatus.updatedAt) || '-';
  const t = (trainers && trainers.generatedAt) || '-';
  return `"c${version}.r${r}.t${t}${extra ? '.' + extra : ''}"`;
}

export function etagMatches(request, etag) {
  const inm = request.headers.get('If-None-Match');
  if (!inm) return false;
  // Cloudflare 压缩时会把强 ETag 改成 W/"…"，比较时去掉 W/
  const strip = s => s.trim().replace(/^W\//, '');
  return inm.split(',').some(tag => strip(tag) === strip(etag));
}

// 公开 GET：给 GitHub Pages（https://xxxxlu.github.io）等站外页面读；数据是公开的、不带凭据，用 *
export const PUBLIC_CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Expose-Headers': 'ETag, X-Catalog-Version'
};

// ---------------------------------------------------------------------------
// 边缘缓存：同一 isolate 的内存 + Cloudflare Cache API（按 ETag 做键，约 60 秒）
// 版本号已经在键里，60 秒只是兜底（比如有人绕过后台直接改了 D1）。
// ---------------------------------------------------------------------------

const EDGE_TTL_SECONDS = 60;
const memoryCache = new Map(); // key -> { at, body }

export async function cachedBody(cacheKey, build) {
  const now = Date.now();
  const hit = memoryCache.get(cacheKey);
  if (hit && now - hit.at < EDGE_TTL_SECONDS * 1000) return hit.body;

  let cache = null;
  try {
    cache = (typeof caches !== 'undefined' && caches.default) ? caches.default : null;
  } catch (e) {
    cache = null;
  }
  const cacheReq = new Request(`https://lmod-catalog-cache.internal/${encodeURIComponent(cacheKey)}`);
  if (cache) {
    try {
      const res = await cache.match(cacheReq);
      if (res) {
        const body = await res.text();
        memoryCache.set(cacheKey, { at: now, body });
        return body;
      }
    } catch (e) {}
  }

  const body = await build();
  if (body === null) return null; // 没找到之类：不缓存
  if (memoryCache.size > 200) memoryCache.clear();
  memoryCache.set(cacheKey, { at: now, body });
  if (cache) {
    try {
      await cache.put(cacheReq, new Response(body, {
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': `public, max-age=${EDGE_TTL_SECONDS}` }
      }));
    } catch (e) {}
  }
  return body;
}

// ---------------------------------------------------------------------------
// 派生：games 表的列、console_commands、scenario_bundles
// 和 scripts/sync_to_database.py 的 game_values / command_rows / bundle_rows 一致，两边要一起改
// ---------------------------------------------------------------------------

function textOf(val, lang = 'zh-CN') {
  if (val && typeof val === 'object' && !Array.isArray(val)) return val[lang] || '';
  return val === null || val === undefined ? '' : String(val);
}

const isPlainObject = v => Boolean(v) && typeof v === 'object' && !Array.isArray(v);

/** games 表除 id / raw_json 之外的列 */
export function gameColumns(doc) {
  const guide = doc.consoleEnableGuide;
  const titles = isPlainObject(doc.titles) ? doc.titles : {};
  const pit = doc.pitfallNote;
  return {
    rank: Number.isInteger(doc.rank) ? doc.rank : 99,
    title: doc.title || 'Unknown',
    title_zh: titles['zh-CN'] || doc.title || 'Unknown',
    titles_json: JSON.stringify(titles),
    developer: doc.developer || '',
    release_year: Number.isInteger(doc.releaseYear) ? doc.releaseYear : null,
    genre: doc.genre || '',
    steam_rating: doc.steamRating || '',
    steam_app_id: Number.isInteger(doc.steamAppId) ? doc.steamAppId : null,
    header_image: doc.headerImage || '',
    has_console: doc.hasConsole ? 1 : 0,
    console_shortcut: doc.consoleShortcut || '',
    console_guide_zh: textOf(guide, 'zh-CN'),
    console_guide_en: isPlainObject(guide) ? textOf(guide, 'en') : '',
    has_mods: doc.hasMods ? 1 : 0,
    mod_install_path: doc.modInstallPath || '',
    has_trainer: doc.hasTrainer ? 1 : 0,
    // pitfall_note 列只是给旧接口看的文字版
    pitfall_note: isPlainObject(pit)
      ? [pit.title, ...(Array.isArray(pit.tips) ? pit.tips : [])].filter(Boolean).join('\n')
      : (typeof pit === 'string' ? pit : '')
  };
}

export function commandRows(doc) {
  const gid = doc.id;
  const rows = [];
  (Array.isArray(doc.popularCommands) ? doc.popularCommands : []).forEach((c, idx) => {
    if (isPlainObject(c)) {
      rows.push({
        id: `${gid}_pop_${idx + 1}`, game_id: gid, category_id: 'popular',
        category_name_zh: '常用指令', category_name_en: 'Popular',
        name_zh: textOf(c.name, 'zh-CN') || '常用指令',
        name_en: isPlainObject(c.name) ? textOf(c.name, 'en') : '',
        code: c.code || c.command || '',
        description: textOf(c.desc, 'zh-CN'),
        syntax_type: c.syntax_type || 'engine_console', is_popular: 1
      });
    } else {
      rows.push({
        id: `${gid}_pop_${idx + 1}`, game_id: gid, category_id: 'popular',
        category_name_zh: '常用指令', category_name_en: 'Popular',
        name_zh: String(c), name_en: String(c), code: String(c), description: '',
        syntax_type: 'engine_console', is_popular: 1
      });
    }
  });
  (Array.isArray(doc.consoleCategories) ? doc.consoleCategories : []).forEach((cat, ci) => {
    if (!isPlainObject(cat)) return;
    const catId = cat.id || `cat${ci + 1}`;
    const catName = cat.name || cat.category;
    (Array.isArray(cat.commands) ? cat.commands : []).forEach((c, idx) => {
      if (!isPlainObject(c)) return;
      rows.push({
        id: c.id || `${gid}_${catId}_${idx + 1}`, game_id: gid, category_id: catId,
        category_name_zh: textOf(catName, 'zh-CN') || '指令分类',
        category_name_en: isPlainObject(catName) ? textOf(catName, 'en') : '',
        name_zh: textOf(c.name, 'zh-CN') || '指令',
        name_en: isPlainObject(c.name) ? textOf(c.name, 'en') : '',
        code: c.code || c.command || '',
        description: textOf(c.desc, 'zh-CN'),
        syntax_type: c.syntax_type || 'engine_console', is_popular: 0
      });
    });
  });
  return rows;
}

export function bundleRows(doc) {
  const gid = doc.id;
  return (Array.isArray(doc.scenarioBundles) ? doc.scenarioBundles : []).filter(isPlainObject).map((b, idx) => {
    let commands = b.commands;
    if ((!Array.isArray(commands) || !commands.length) && b.code) {
      commands = String(b.code).split('\n').filter(line => line.trim());
    }
    return {
      id: b.id || `${gid}_bundle_${idx + 1}`, game_id: gid,
      name: textOf(b.name, 'zh-CN') || '指令套餐',
      description: textOf(b.desc || b.description, 'zh-CN'),
      commands_json: JSON.stringify(commands || []),
      bat_script: b.batScript || ''
    };
  });
}

// ---------------------------------------------------------------------------
// 校验（参考 scripts/gamedata_guard.py + verify_deployment.py check_game_structure + 雷达脚本的 BANNED_PHRASES）
// 结构问题和「新写进去的」保证类说法 → 错误，拒绝保存；
// 老数据里原样留着的说法、夸张词、缺出处 → 警告，能保存但会列出来。
// ---------------------------------------------------------------------------

const BANNED_LINK_HOSTS = ['github.com/l-mod-vault', 'l-mod-vault.github.io', 'example.com'];
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

// 保证类说法：站里没人做过实机测试，也担保不了封号/兼容。negatable = 同一分句里前面有否定词时放行（「未实测」「没有办法保证」）
const CLAIM_RULES = [
  { re: /实测|亲测|实机测试|真机测试|真实校验|逐条验证|验证通过|测试通过/g, negatable: true,
    msg: '「实测 / 亲测 / 验证通过」：站里没有做过实机测试，只能写「未实测」' },
  { re: /100\s*[%％]\s*(?:安全|防封|免封|兼容|适配|成功|有效|可用|稳定|生效|纯净|无毒|不封|离线防封|保证|确保)/g,
    msg: '「100% 安全 / 兼容 / 有效」这类保证' },
  { re: /(?:安全|兼容|成功率|有效率|生效率|通过率)\s*(?:达)?\s*100\s*[%％]/g, msg: '「兼容 / 成功率 100%」这类保证' },
  { re: /零(?:风险|封号|冲突|广告|捆绑|木马|病毒|报错|失败)/g, msg: '「零风险 / 零封号 / 零冲突」这类保证' },
  { re: /完美(?:兼容|适配|运行|支持|修复|生效|对齐)/g, msg: '「完美兼容」这类保证' },
  { re: /全版本兼容|全面兼容|完全兼容|完全对齐|绝对兼容/g, msg: '「全版本兼容 / 完全兼容」这类保证' },
  { re: /绝无|绝不会|绝对(?:安全|不会|不封|兼容|无毒)|永不封号|无封号风险|免封号?/g, msg: '「绝无风险 / 不会被封」这类保证' },
  // 「会不会被封号没有人能担保」「没有人能担保不会被封号」是如实说法，放行
  { re: /(?<!会)不会被封|防封|保证/g, negatable: true, msg: '「不会被封 / 防封 / 保证」：封号和效果没人能担保' },
  { re: /老L团队|已失效/g, msg: '「老L团队 / 已失效」（雷达脚本也禁用）' },
  { re: /100%\s*(?:safe|working|compatible|undetect\w*)|zero[- ]risk|ban[- ]?proof|guaranteed|fully tested|tested and verified|verified working|(?:no|without(?: any)?) ban risk|undetectable/gi,
    negatable: true, msg: 'English guarantee wording (100% safe / guaranteed / ban-proof / tested and verified)' }
];
const NEGATION_ZH = /未|没有|没|不是|并非|无法|不能|不/;
const NEGATION_EN = /\b(?:not|no|never|cannot|can't|nothing|nobody|without)\b/i;
const CLAUSE_SPLIT = /[。；;！!？?\n，,、]/;

// 夸张词：只提醒（数据清理时定的口径，见 gamedata-claims 第四、五轮）
const HYPE_RE = /零门槛|绝对|彻底|一键|终极|最强|必备|顶级|完美|史诗级|秒杀|秒级|秒开|瞬间|丝滑|无敌版|！|(?<!魔)神器/g;

function clauseBefore(text, index) {
  let start = index;
  while (start > 0 && !CLAUSE_SPLIT.test(text[start - 1])) start--;
  return text.slice(start, index);
}

function isNegated(text, index) {
  const clause = clauseBefore(text, index);
  return NEGATION_ZH.test(clause) || NEGATION_EN.test(clause);
}

/** 找出一段文字里的保证类说法：[{ phrase, msg }] */
export function findClaims(text) {
  const hits = [];
  if (typeof text !== 'string' || !text) return hits;
  for (const rule of CLAIM_RULES) {
    rule.re.lastIndex = 0;
    let m;
    while ((m = rule.re.exec(text)) !== null) {
      if (rule.negatable && isNegated(text, m.index)) continue;
      hits.push({ phrase: m[0], msg: rule.msg });
    }
  }
  return hits;
}

function findHype(text) {
  if (typeof text !== 'string' || !text) return [];
  HYPE_RE.lastIndex = 0;
  return [...new Set(text.match(HYPE_RE) || [])];
}

/** 文档里所有字符串（跳过机器字段和链接）：[[路径, 文字]] */
function walkStrings(value, path, out) {
  if (typeof value === 'string') {
    if (!/^https?:\/\//i.test(value)) out.push([path, value]);
  } else if (Array.isArray(value)) {
    value.forEach((v, i) => walkStrings(v, `${path}[${i}]`, out));
  } else if (isPlainObject(value)) {
    for (const [k, v] of Object.entries(value)) {
      if (!path && MACHINE_SET.has(k)) continue;
      walkStrings(v, path ? `${path}.${k}` : k, out);
    }
  }
  return out;
}

function nonEmptyStr(v) {
  return typeof v === 'string' && v.trim() !== '';
}

function linkProblem(url) {
  if (typeof url !== 'string' || !/^https:\/\/[^/\s]+/.test(url)) return `不是 https 链接：${JSON.stringify(url)}`;
  if (BANNED_LINK_HOSTS.some(h => url.includes(h))) return `指向不存在的镜像：${url}`;
  return null;
}

/**
 * 校验一份游戏文档。
 * @param {object} doc 要保存的文档（机器字段已经换成库里的原值）
 * @param {object|null} oldDoc 库里原来的文档（新建时为 null）；用来区分「新写进去的说法」和「老数据里原样留着的」
 * @returns {{errors: string[], warnings: string[]}}
 */
export function validateGameDoc(doc, oldDoc = null) {
  const errors = [];
  const warnings = [];
  const err = m => errors.push(m);
  const warn = m => warnings.push(m);

  if (!isPlainObject(doc)) return { errors: ['游戏数据必须是一个 JSON 对象'], warnings };

  const bytes = new TextEncoder().encode(JSON.stringify(doc)).length;
  if (bytes > MAX_DOC_BYTES) err(`整份数据 ${Math.round(bytes / 1024)} KB，超过上限 ${MAX_DOC_BYTES / 1024} KB`);

  // 基本信息
  if (typeof doc.id !== 'string' || !GAME_ID_RE.test(doc.id) || doc.id.length > 64) {
    err('id 只能用小写字母、数字和连字符（如 elden-ring），不超过 64 个字符');
  }
  if (!nonEmptyStr(doc.title)) err('title（英文/通用标题）不能为空');
  if (!isPlainObject(doc.titles)) {
    err('titles 必须是 8 种语言的标题对象');
  } else {
    if (!nonEmptyStr(doc.titles['zh-CN'])) err('titles.zh-CN（简体中文标题）不能为空');
    if (!nonEmptyStr(doc.titles.en)) err('titles.en（英文标题）不能为空');
    for (const [k, v] of Object.entries(doc.titles)) {
      if (!LANGS.includes(k)) err(`titles 里有不认识的语言：${k}`);
      else if (typeof v !== 'string') err(`titles.${k} 必须是文字`);
    }
    const missing = LANGS.filter(l => !nonEmptyStr(doc.titles[l]));
    if (missing.length) warn(`这些语言的标题是空的，页面会退回英文标题：${missing.join(' / ')}`);
  }
  if (!Number.isInteger(doc.rank) || doc.rank < 1 || doc.rank > 9999) err('rank（排名）必须是 1–9999 的整数');
  if (doc.steamAppId !== undefined && doc.steamAppId !== null && (!Number.isInteger(doc.steamAppId) || doc.steamAppId < 0)) {
    err('steamAppId 必须是非负整数（不在 Steam 上填 0）');
  }
  if (doc.releaseYear !== undefined && doc.releaseYear !== null &&
      (!Number.isInteger(doc.releaseYear) || doc.releaseYear < 1970 || doc.releaseYear > 2100)) {
    err('releaseYear 必须是 1970–2100 的年份');
  }
  for (const key of ['hasConsole', 'hasMods']) {
    if (doc[key] !== undefined && typeof doc[key] !== 'boolean') err(`${key} 只能是 true / false`);
  }
  for (const key of ['developer', 'genre', 'steamRating', 'consoleShortcut', 'modInstallPath', 'radarSecretCode', 'batScript']) {
    if (doc[key] !== undefined && doc[key] !== null && typeof doc[key] !== 'string') err(`${key} 必须是文字`);
  }
  if (doc.headerImage && linkProblem(doc.headerImage)) err(`headerImage：${linkProblem(doc.headerImage)}`);
  if (doc.heatTier !== undefined && !HEAT_TIERS.includes(doc.heatTier)) err(`heatTier 只能是 ${HEAT_TIERS.join(' / ')}`);
  if (doc.lastUpdated !== undefined && !(typeof doc.lastUpdated === 'string' && DATE_RE.test(doc.lastUpdated))) {
    err('lastUpdated 必须是 YYYY-MM-DD 日期');
  }
  if (doc.aliases !== undefined && !(Array.isArray(doc.aliases) && doc.aliases.every(a => typeof a === 'string'))) {
    err('aliases（别名）必须是文字列表');
  }
  if (doc.consoleEnableGuide !== undefined && doc.consoleEnableGuide !== null) {
    if (!isPlainObject(doc.consoleEnableGuide) || !Object.values(doc.consoleEnableGuide).every(v => typeof v === 'string')) {
      err('consoleEnableGuide 必须是 { "zh-CN": "…", "en": "…" } 形式的说明');
    }
  }

  // 常用指令
  const pops = doc.popularCommands;
  if (pops !== undefined && !Array.isArray(pops)) err('popularCommands 必须是数组');
  (Array.isArray(pops) ? pops : []).forEach((c, i) => {
    if (typeof c === 'string') {
      if (!c.trim()) err(`popularCommands[${i}] 是空字符串`);
      return;
    }
    if (!isPlainObject(c) || !nonEmptyStr(c.command || c.code)) { err(`popularCommands[${i}] 缺 command`); return; }
    if (!c.source) warn(`常用指令「${textOf(c.name) || c.command}」没写出处（source）`);
    else if (linkProblem(c.source)) err(`常用指令「${textOf(c.name) || c.command}」的出处：${linkProblem(c.source)}`);
  });

  // 指令分类（和 verify_deployment.py check_game_structure 一致）
  const cats = doc.consoleCategories;
  if (cats !== undefined && !Array.isArray(cats)) err('consoleCategories 必须是数组');
  const commandIds = new Set();
  (Array.isArray(cats) ? cats : []).forEach((cat, ci) => {
    const cmds = isPlainObject(cat) ? cat.commands : null;
    if (!isPlainObject(cat) || !nonEmptyStr(cat.category || textOf(cat.name)) || !Array.isArray(cmds) || !cmds.length) {
      err(`指令分类第 ${ci + 1} 个缺分类名，或者里面一条指令都没有`);
      return;
    }
    cmds.forEach((cmd, i) => {
      const where = `分类「${cat.category || textOf(cat.name)}」第 ${i + 1} 条指令`;
      const name = isPlainObject(cmd) ? cmd.name : null;
      if (!isPlainObject(cmd) || !nonEmptyStr(cmd.code) ||
          !(nonEmptyStr(name) || (isPlainObject(name) && Object.values(name).some(nonEmptyStr)))) {
        err(`${where}缺 code 或名称`);
        return;
      }
      if (cmd.id !== undefined) {
        if (!nonEmptyStr(cmd.id)) err(`${where}的 id 是空的`);
        else if (commandIds.has(cmd.id)) err(`指令 id 重复：${cmd.id}`);
        else commandIds.add(cmd.id);
      }
      if (!cmd.source) err(`${where}「${textOf(cmd.name)}」没写出处（source）`);
      else if (linkProblem(cmd.source)) err(`${where}的出处：${linkProblem(cmd.source)}`);
    });
  });

  // 套餐
  const bundles = doc.scenarioBundles;
  if (bundles !== undefined && !Array.isArray(bundles)) err('scenarioBundles 必须是数组');
  const bundleIds = new Set();
  (Array.isArray(bundles) ? bundles : []).forEach((b, i) => {
    if (!isPlainObject(b) || !['id', 'name', 'code'].every(k => nonEmptyStr(b[k]))) {
      err(`场景套餐第 ${i + 1} 个缺 id / name / code`);
      return;
    }
    if (bundleIds.has(b.id)) err(`套餐 id 重复：${b.id}`);
    bundleIds.add(b.id);
    if (b.highlights !== undefined && !(Array.isArray(b.highlights) && b.highlights.every(h => typeof h === 'string'))) {
      err(`套餐「${b.name}」的 highlights 必须是文字列表`);
    }
  });

  // 精选 Mod
  const mods = doc.curatedMods;
  if (mods !== undefined && !Array.isArray(mods)) err('curatedMods 必须是数组');
  const modIds = new Set();
  (Array.isArray(mods) ? mods : []).forEach((m, i) => {
    if (!isPlainObject(m) || !['id', 'title', 'author'].every(k => nonEmptyStr(m[k]))) {
      err(`精选 Mod 第 ${i + 1} 个缺 id / title / author`);
      return;
    }
    if (modIds.has(m.id)) err(`Mod id 重复：${m.id}`);
    modIds.add(m.id);
    if (!m.nexusUrl) err(`Mod「${m.title}」没有来源页面链接（nexusUrl）`);
    else if (linkProblem(m.nexusUrl)) err(`Mod「${m.title}」：${linkProblem(m.nexusUrl)}`);
    if (m.downloadUrl && linkProblem(m.downloadUrl)) err(`Mod「${m.title}」的下载链接：${linkProblem(m.downloadUrl)}`);
    for (const k of ['dependencies', 'installSteps']) {
      if (m[k] !== undefined && !(Array.isArray(m[k]) && m[k].every(s => typeof s === 'string'))) err(`Mod「${m.title}」的 ${k} 必须是文字列表`);
    }
  });
  const must = doc.mustHaveMods;
  if (must !== undefined && !Array.isArray(must)) err('mustHaveMods 必须是数组');
  (Array.isArray(must) ? must : []).forEach((m, i) => {
    if (!isPlainObject(m) || !nonEmptyStr(m.name)) { err(`必装 Mod 第 ${i + 1} 个缺 name`); return; }
    if (m.url && linkProblem(m.url)) err(`必装 Mod「${m.name}」：${linkProblem(m.url)}`);
  });

  // 避坑笔记
  const pit = doc.pitfallNote;
  if (pit !== undefined && pit !== null) {
    if (!isPlainObject(pit) || typeof pit.title !== 'string' || !Array.isArray(pit.tips) || !pit.tips.every(t => typeof t === 'string')) {
      err('pitfallNote 必须是 { "title": "…", "tips": ["…"] }，没有就留空（null）');
    }
  }

  // N 网数字
  const ns = doc.nexusStats;
  if (ns !== undefined && ns !== null) {
    if (!isPlainObject(ns) || !(ns.totalDownloads || ns.totalMods)) err('nexusStats 存在但没有数字');
    else if (!(typeof ns.checkedAt === 'string' && DATE_RE.test(ns.checkedAt))) err('nexusStats 没有取数日期 checkedAt（YYYY-MM-DD）');
  }

  // 说法检查
  const oldStrings = new Map(oldDoc ? walkStrings(oldDoc, '', []) : []);
  const hypeSeen = new Set();
  for (const [path, text] of walkStrings(doc, '', [])) {
    const unchanged = oldStrings.get(path) === text;
    for (const hit of findClaims(text)) {
      const line = `${path}：「${hit.phrase}」—— ${hit.msg}`;
      if (unchanged) warn(`老数据里的说法（这次没改，建议顺手改掉）${line}`);
      else err(line);
    }
    for (const word of findHype(text)) {
      if (unchanged || hypeSeen.has(`${path}|${word}`)) continue;
      hypeSeen.add(`${path}|${word}`);
      warn(`${path}：有夸张词「${word}」，确认是实际效果名而不是宣传话`);
    }
  }

  return { errors, warnings };
}

const hasOwn = (o, k) => Object.prototype.hasOwnProperty.call(o, k);

/**
 * 保存前整理：机器字段一律用库里的原值（新建游戏给修改器三个字段安全的空值），其它照收。
 * 字段顺序跟着编辑器交回来的文档走（编辑器是在库里那份上改的），快照导出时 diff 才干净。
 */
export function mergeMachineFields(incoming, storedDoc) {
  const out = {};
  for (const [k, v] of Object.entries(incoming)) {
    if (!MACHINE_SET.has(k)) out[k] = v;
    else if (storedDoc && hasOwn(storedDoc, k)) out[k] = storedDoc[k];
  }
  if (storedDoc) {
    for (const k of MACHINE_FIELDS) {
      if (!hasOwn(out, k) && hasOwn(storedDoc, k)) out[k] = storedDoc[k];
    }
  } else {
    out.hasTrainer = false;
    out.trainerHotkeys = [];
    out.trainerInfo = {};
  }
  return out;
}

/** 两份文档之间变了的顶层字段（审计日志用） */
export function changedFields(before, after) {
  const keys = new Set([...Object.keys(before || {}), ...Object.keys(after || {})]);
  return [...keys].filter(k => JSON.stringify((before || {})[k]) !== JSON.stringify((after || {})[k])).sort();
}

export function jsonResponse(payload, status = 200, headers = {}) {
  return new Response(JSON.stringify(payload), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...headers }
  });
}
