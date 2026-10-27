/**
 * Cloudflare Pages Function: /api/v1/telemetry/events
 * Low-latency Non-blocking Telemetry Ingestion API
 */

export async function onRequestPost(context) {
  const { request, env } = context;
  const db = env.DB || env.lmod_vault_db;

  try {
    const payload = await request.json();
    const clientCountry = request.headers.get('cf-ipcountry') || 'Unknown';

    // Support single event object or array batch
    const events = Array.isArray(payload) ? payload : [payload];

    if (events.length === 0 || events.length > 50) {
      return new Response(JSON.stringify({ code: 40000, message: 'Batch size must be between 1 and 50' }), { status: 400 });
    }

    if (db) {
      const statements = events.map(evt => {
        return db.prepare(
          `INSERT INTO telemetry_events 
           (event_type, game_id, target_payload, session_id, user_id, client_country)
           VALUES (?, ?, ?, ?, ?, ?)`
        ).bind(
          String(evt.event_type || 'unknown').slice(0, 32),
          evt.game_id ? String(evt.game_id).slice(0, 64) : null,
          evt.target_payload ? String(evt.target_payload).slice(0, 255) : null,
          String(evt.session_id || 'anonymous').slice(0, 64),
          evt.user_id ? String(evt.user_id).slice(0, 64) : null,
          clientCountry
        );
      });

      // Execute in background without blocking response
      context.waitUntil(db.batch(statements));
    }

    return new Response(JSON.stringify({ code: 0, message: 'accepted' }), {
      status: 202,
      headers: { 'Content-Type': 'application/json; charset=utf-8' }
    });

  } catch (err) {
    return new Response(JSON.stringify({ code: 40000, message: 'Invalid JSON payload' }), { status: 400 });
  }
}
