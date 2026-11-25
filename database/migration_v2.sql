-- ==============================================================================
-- L-MOD Vault - Migration v2: Telemetry, User Auth & Favorites
-- Compatible with: Cloudflare D1 (SQLite)
-- ==============================================================================

-- 1. Lightweight Telemetry Events Table (Player interaction tracing)
CREATE TABLE IF NOT EXISTS telemetry_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,         -- 'copy_code' | 'download_bat' | 'search_query' | 'ai_ask' | 'view_game'
    game_id TEXT,                     -- e.g. 'cyberpunk-2077', nullable
    target_payload TEXT,              -- interaction context (e.g. command snippet, search query, capped to 255 chars)
    session_id TEXT NOT NULL,         -- frontend anonymous UUID
    user_id TEXT,                     -- authenticated user ID if logged in, otherwise NULL
    client_country TEXT,              -- from Cloudflare Header cf-ipcountry
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_telemetry_event_type ON telemetry_events(event_type);
CREATE INDEX IF NOT EXISTS idx_telemetry_game_id ON telemetry_events(game_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_created_at ON telemetry_events(created_at);

-- 2. User Authentication Subject Table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,                       -- e.g. 'steam_76561198000000000' or UUID
    provider TEXT NOT NULL DEFAULT 'steam',    -- 'steam' | 'email' | 'guest'
    nickname TEXT NOT NULL,                    -- Player Nickname
    avatar_url TEXT,                           -- Avatar Image URL
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. User Favorites Table
CREATE TABLE IF NOT EXISTS user_favorites (
    user_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, game_id),
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);

-- 4. User Radar Subscriptions Table
CREATE TABLE IF NOT EXISTS user_radar_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    game_id TEXT NOT NULL,
    notify_channel TEXT DEFAULT 'webhook',     -- 'webhook' | 'email' | 'webpush'
    notify_target TEXT NOT NULL,               -- Webhook URL or Email address
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_user_radar_sub ON user_radar_subscriptions(user_id, game_id);
