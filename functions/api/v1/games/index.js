/**
 * Cloudflare Pages Function: /api/v1/games
 * Lightweight Catalog Pagination with Edge Projection
 */

export async function onRequestGet(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // Pagination parameters validation
  const page = Math.max(parseInt(url.searchParams.get('page') || '1', 10), 1);
  const pageSize = Math.min(Math.max(parseInt(url.searchParams.get('page_size') || '24', 10), 1), 50);
  const offset = (page - 1) * pageSize;

  const genre = url.searchParams.get('genre');
  const compatStatus = url.searchParams.get('compat_status');
  const hasConsole = url.searchParams.get('has_console');
  const hasMods = url.searchParams.get('has_mods');
  const sortBy = url.searchParams.get('sort_by') || 'rank';

  const db = env.DB || env.lmod_vault_db;
  if (!db) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Database binding missing. Ensure D1 is bound in Pages settings.'
    }), { status: 500 });
  }

  try {
    // Dynamic Parameterized SQL Query
    const conditions = [];
    const params = [];

    if (genre && genre !== 'all') {
      conditions.push('genre = ?');
      params.push(genre);
    }
    if (compatStatus && compatStatus !== 'all') {
      conditions.push('compatibility_status = ?');
      params.push(compatStatus);
    }
    if (hasConsole !== null && hasConsole !== undefined) {
      conditions.push('has_console = ?');
      params.push(hasConsole === 'true' || hasConsole === '1' ? 1 : 0);
    }
    if (hasMods !== null && hasMods !== undefined) {
      conditions.push('has_mods = ?');
      params.push(hasMods === 'true' || hasMods === '1' ? 1 : 0);
    }

    const whereClause = conditions.length > 0 ? `WHERE ${conditions.join(' AND ')}` : '';

    // 1. Get count for pagination
    const countSql = `SELECT COUNT(*) AS total FROM games ${whereClause}`;
    const totalRow = await db.prepare(countSql).bind(...params).first();
    const total = totalRow ? totalRow.total : 0;

    // 2. Projected lightweight fields query
    let orderClause = 'ORDER BY rank ASC';
    if (sortBy === 'release_year') orderClause = 'ORDER BY release_year DESC, rank ASC';
    if (sortBy === 'title') orderClause = 'ORDER BY title ASC';

    const querySql = `
      SELECT id, rank, title, title_zh, titles_json, developer, release_year, 
             genre, steam_rating, steam_app_id, header_image,
             has_console, console_shortcut, has_mods, has_trainer,
             compatibility_status, verified_patch, latest_steam_patch, radar_risk_title
      FROM games
      ${whereClause}
      ${orderClause}
      LIMIT ? OFFSET ?
    `;

    const queryParams = [...params, pageSize, offset];
    const { results } = await db.prepare(querySql).bind(...queryParams).all();

    // Map titles_json to clean object
    const sanitizedResults = (results || []).map(row => {
      let titles = {};
      try {
        titles = row.titles_json ? JSON.parse(row.titles_json) : {};
      } catch (e) {}
      const { titles_json, ...rest } = row;
      return {
        ...rest,
        titles
      };
    });

    return new Response(JSON.stringify({
      code: 0,
      message: 'success',
      data: {
        items: sanitizedResults
      },
      meta: {
        page,
        page_size: pageSize,
        total,
        has_more: offset + sanitizedResults.length < total
      }
    }), {
      headers: {
        'Content-Type': 'application/json; charset=utf-8',
        'Cache-Control': 'public, max-age=60, s-maxage=3600, stale-while-revalidate=86400'
      }
    });

  } catch (err) {
    return new Response(JSON.stringify({
      code: 50000,
      message: 'Failed to query games catalog',
      details: err.message
    }), { status: 500 });
  }
}
