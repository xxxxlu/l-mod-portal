/**
 * Shared helpers for FLiNG trainer packages (Workers KV binding `TRAINER_FILES` + D1 table `trainer_packages`).
 *
 * Storage layout
 *   D1  trainer_packages         one row per uploaded file; at most one `active` row per game
 *   KV  pkg/<id>/<n>             the file body, split into CHUNK_SIZE pieces (KV values max out at 25 MiB)
 *
 * Free-plan constraints this module is built around
 *   - 10 ms CPU per request: the server never hashes or copies file bytes in JS. The admin page computes
 *     SHA-256 in the browser; uploads stream request bodies straight into KV; downloads pipe KV streams
 *     into a FixedLengthStream.
 *   - KV: 1 GB total, 25 MiB per value, 1,000 writes / deletes / lists per day.
 *
 * When the KV binding is missing (namespace not created yet) everything degrades to "no packages":
 * the manifest is empty, /dl/ answers 503 and the admin tab shows "存储未开通".
 */

export const CHUNK_SIZE = 24 * 1024 * 1024; // below the 25 MiB KV value cap, with headroom
export const MAX_FILE_SIZE = 95 * 1024 * 1024; // Pages free plan caps request bodies at 100 MB
export const KV_QUOTA_BYTES = 1024 * 1024 * 1024; // KV free plan: 1 GB stored
export const ALLOWED_EXTENSIONS = ['.zip', '.exe', '.rar', '.7z'];
export const PUBLIC_ORIGIN = 'https://lmod-vault.pages.dev';

const GAME_ID_RE = /^[a-z0-9][a-z0-9-]{0,79}$/;
const PKG_ID_RE = /^tp_[0-9a-f]{16}$/;
const SHA256_RE = /^[0-9a-f]{64}$/;

// Sites allowed to read the manifest and preflight /dl/ from the browser
const CORS_ORIGINS = new Set([
  'https://xxxxlu.github.io',
  'https://lmod-vault.pages.dev',
  'http://localhost:8788',
  'http://127.0.0.1:8788'
]);
const PREVIEW_ORIGIN_RE = /^https:\/\/[a-z0-9-]+\.lmod-vault\.pages\.dev$/;

export function getDb(env) {
  return (env && (env.DB || env.lmod_vault_db)) || null;
}

export function getKv(env) {
  const kv = env && env.TRAINER_FILES;
  return kv && typeof kv.get === 'function' && typeof kv.put === 'function' ? kv : null;
}

export function isGameId(v) {
  return typeof v === 'string' && GAME_ID_RE.test(v);
}

export function isPackageId(v) {
  return typeof v === 'string' && PKG_ID_RE.test(v);
}

export function isSha256(v) {
  return typeof v === 'string' && SHA256_RE.test(v);
}

export function newPackageId() {
  const bytes = crypto.getRandomValues(new Uint8Array(8));
  return 'tp_' + Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
}

export function chunkCount(size) {
  return Math.max(1, Math.ceil(size / CHUNK_SIZE));
}

/** Exact byte length of chunk `n` for a file of `size` bytes. */
export function chunkLength(size, n) {
  const chunks = chunkCount(size);
  if (n < 0 || n >= chunks) return -1;
  return n < chunks - 1 ? CHUNK_SIZE : size - CHUNK_SIZE * (chunks - 1);
}

export function chunkKey(prefix, n) {
  return `${prefix}/${n}`;
}

export function fileExtension(name) {
  const m = /\.[^.]+$/.exec(String(name || '').toLowerCase());
  return m ? m[0] : '';
}

/**
 * Keep the original FLiNG file name readable but safe for a URL path segment and Content-Disposition:
 * strip path separators, control characters and quotes; collapse whitespace.
 */
export function cleanFileName(name) {
  const base = String(name || '').split(/[\\/]/).pop();
  return base
    .replace(/[\u0000-\u001f\u007f"<>|*?:]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 160);
}

export function downloadPath(gameId, fileName) {
  return `/dl/${encodeURIComponent(gameId)}/${encodeURIComponent(fileName)}`;
}

/** D1 `datetime('now')` text ("YYYY-MM-DD HH:MM:SS", UTC) → ISO 8601. */
export function toIso(d1Time) {
  if (!d1Time) return null;
  const s = String(d1Time);
  return /T/.test(s) ? s : s.replace(' ', 'T') + 'Z';
}

/** Echo the Origin back when it is one of ours (manifest + /dl/ preflight from GitHub Pages). */
export function corsHeaders(request, extra = {}) {
  const origin = request.headers.get('Origin');
  const headers = { Vary: 'Origin', ...extra };
  if (origin && (CORS_ORIGINS.has(origin) || PREVIEW_ORIGIN_RE.test(origin))) {
    headers['Access-Control-Allow-Origin'] = origin;
  }
  return headers;
}

export function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', ...headers }
  });
}

/** True when the migration has not been applied (local or remote) yet. */
export function isMissingTable(err) {
  return /no such table/i.test(String(err && err.message));
}

/** Remove every chunk of a package from KV. Returns the number of keys deleted. */
export async function deleteChunks(kv, row) {
  if (!kv || !row || !row.kv_prefix) return 0;
  const n = Number(row.chunks) || 0;
  const keys = [];
  for (let i = 0; i < n; i++) keys.push(chunkKey(row.kv_prefix, i));
  await Promise.all(keys.map(k => kv.delete(k)));
  return keys.length;
}
