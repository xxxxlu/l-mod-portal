-- ==============================================================================
-- L-MOD Vault - Global Gaming Database Schema (v1.0)
-- Compatible with: Cloudflare D1 (SQLite), Turso (libSQL), Supabase (PostgreSQL)
-- ==============================================================================

-- 1. Main Games Table (100 Flagship Single-Player Games)
CREATE TABLE IF NOT EXISTS games (
    id TEXT PRIMARY KEY,                       -- e.g. 'cyberpunk-2077'
    rank INTEGER NOT NULL,                     -- 1 to 100
    title TEXT NOT NULL,                       -- Primary English/Universal Title
    title_zh TEXT,                             -- Simplified Chinese Title
    titles_json TEXT,                          -- 8 Languages JSON: {"en": "...", "zh-CN": "...", ...}
    developer TEXT,                            -- Developer / Engine Studio
    release_year INTEGER,                      -- e.g. 2020
    genre TEXT,                                -- Genre e.g. 'Open World Action RPG'
    steam_rating TEXT,                         -- e.g. '92% Very Positive'
    steam_app_id INTEGER,                      -- e.g. 1091500
    header_image TEXT,                         -- Official Banner / Capsule URL
    has_console BOOLEAN DEFAULT 1,             -- Whether console commands exist
    console_shortcut TEXT,                     -- e.g. '~ (Cyber Engine Tweaks)'
    console_guide_zh TEXT,                     -- Detailed guide in Chinese
    console_guide_en TEXT,                     -- Detailed guide in English
    has_mods BOOLEAN DEFAULT 1,                -- Whether mods exist
    mod_install_path TEXT,                     -- Local mod installation path
    has_trainer BOOLEAN DEFAULT 1,             -- Whether FLiNG trainer exists
    verified_patch TEXT,                       -- L-MOD Verified baseline patch
    latest_steam_patch TEXT,                   -- Latest official Steam patch
    compatibility_status TEXT DEFAULT 'green', -- 'green' | 'yellow' | 'red'
    radar_risk_title TEXT,                     -- Short risk summary
    radar_risk_desc TEXT,                      -- Detailed compatibility impact
    radar_summary TEXT,                        -- Player-friendly verdict
    pitfall_note TEXT,                         -- Anti-pitfall and save backup note
    raw_json TEXT,                             -- Complete holographic JSON backup
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_games_rank ON games(rank);
CREATE INDEX IF NOT EXISTS idx_games_compat ON games(compatibility_status);
CREATE INDEX IF NOT EXISTS idx_games_appid ON games(steam_app_id);

-- 2. Console Commands Table (Detailed Normalized Commands)
CREATE TABLE IF NOT EXISTS console_commands (
    id TEXT PRIMARY KEY,                       -- e.g. 'cp_money_1m'
    game_id TEXT NOT NULL,                     -- Foreign reference to games(id)
    category_id TEXT,                          -- e.g. 'god_mode', 'weapons'
    category_name_zh TEXT,                     -- Chinese Category Title
    category_name_en TEXT,                     -- English Category Title
    name_zh TEXT NOT NULL,                     -- Command Name in Chinese
    name_en TEXT,                              -- Command Name in English
    code TEXT NOT NULL,                        -- Executable Syntax Code
    description TEXT,                          -- Usage explanation & parameter docs
    syntax_type TEXT DEFAULT 'engine_console', -- 'cet_lua', 'creation_hex', 'ue_console', etc.
    is_popular BOOLEAN DEFAULT 0,              -- Whether pinned to popular shortcuts
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_commands_game ON console_commands(game_id);
CREATE INDEX IF NOT EXISTS idx_commands_cat ON console_commands(category_id);
CREATE INDEX IF NOT EXISTS idx_commands_popular ON console_commands(is_popular);

-- 3. Scenario Bundles Table (One-Click Bat Packages)
CREATE TABLE IF NOT EXISTS scenario_bundles (
    id TEXT PRIMARY KEY,                       -- e.g. 'cp_bundle_starter'
    game_id TEXT NOT NULL,                     -- Foreign reference to games(id)
    name TEXT NOT NULL,                        -- e.g. '新手破荒避坑包'
    description TEXT,                          -- Bundle description
    commands_json TEXT,                        -- Array of bundled commands
    bat_script TEXT,                           -- Pre-compiled Windows .bat script
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_bundles_game ON scenario_bundles(game_id);

-- 4. Steam Patch Radar Log Table (Historical Audit Trail)
CREATE TABLE IF NOT EXISTS patch_radar_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT NOT NULL,
    patch_title TEXT NOT NULL,
    patch_date TEXT,
    build_id TEXT,
    status TEXT NOT NULL,                      -- 'green' | 'yellow' | 'red'
    risk_title TEXT,
    risk_desc TEXT,
    emergency_broadcast TEXT,
    checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_radar_logs_game ON patch_radar_logs(game_id);

-- 5. Community Bug Reports & Feedback Table (Ready for Player Interactions)
CREATE TABLE IF NOT EXISTS community_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT,
    category TEXT DEFAULT 'bug_report',        -- 'bug_report' | 'mod_request' | 'comment'
    content TEXT NOT NULL,
    player_nickname TEXT,
    player_ip_country TEXT,
    status TEXT DEFAULT 'pending',             -- 'pending' | 'verified' | 'resolved'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
