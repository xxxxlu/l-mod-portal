/**
 * Masking helpers for admin views. The admin UI never needs a full email or IP to read a list,
 * so lists return masked values only.
 */

export function maskEmail(email) {
  if (!email || typeof email !== 'string' || !email.includes('@')) return email ? '***' : null;
  const [local, domain] = email.split('@');
  const keep = local.length <= 3 ? 1 : 2;
  const dot = domain.lastIndexOf('.');
  const name = dot > 0 ? domain.slice(0, dot) : domain;
  const tld = dot > 0 ? domain.slice(dot) : '';
  return `${local.slice(0, keep)}***@${name.slice(0, 1)}***${tld}`;
}

export function maskIp(ip) {
  if (!ip || typeof ip !== 'string') return null;
  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(ip)) return ip.replace(/\.\d{1,3}$/, '.x');
  if (ip.includes(':')) return ip.split(':').slice(0, 3).join(':') + ':…';
  return '***';
}

/** Mask IPv4 / IPv6 addresses that appear inside free text (e.g. audit log details). */
export function maskIpsInText(text) {
  if (!text || typeof text !== 'string') return text;
  return text
    .replace(/\b(\d{1,3}\.\d{1,3}\.\d{1,3})\.\d{1,3}\b/g, '$1.x')
    .replace(/\b([0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4})(:[0-9a-f]{0,4}){2,7}\b/gi, '$1:…');
}

export function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }
  });
}
