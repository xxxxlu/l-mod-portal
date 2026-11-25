-- ==============================================================================
-- L-MOD Vault - Migration v5: D1 is the source of truth for game data
-- Compatible with: Cloudflare D1 (SQLite)
--
-- Additive only (ADD COLUMN / new table / new index / new settings row); no row is
-- deleted or rewritten. Run it once, before deploying the Functions that read
-- games.is_hidden (the public catalog and the admin game editor).
--
--   Local:      npx wrangler@4.154.0 d1 execute lmod-vault-db --local  --file=database/migration_v5_game_docs.sql
--   Production: npx wrangler@4.154.0 d1 execute lmod-vault-db --remote --file=database/migration_v5_game_docs.sql
--               (production needs the owner's go-ahead and a fresh backup first; see docs/DATABASE_GUIDE.md)
--
-- Running it a second time fails on the ALTER TABLE lines ("duplicate column name")
-- and changes nothing; that is expected.
-- ==============================================================================

-- 1. Hide a game instead of deleting it.
--    user_favorites / user_radar_subscriptions reference games(id) ON DELETE CASCADE, so
--    deleting a games row silently deletes players' favorites and subscriptions.
--    Hidden games are left out of the public catalog, the old /api/v1/games* endpoints
--    and the data.js snapshot; their row, favorites and subscriptions stay.
ALTER TABLE games ADD COLUMN is_hidden INTEGER NOT NULL DEFAULT 0;

-- 2. Per-game revision counter for the admin editor (optimistic locking: a save that was
--    started from an older revision is rejected instead of overwriting newer changes).
ALTER TABLE games ADD COLUMN content_rev INTEGER NOT NULL DEFAULT 1;

CREATE INDEX IF NOT EXISTS idx_games_hidden_rank ON games(is_hidden, rank);

-- 3. Every admin save keeps the previous raw_json here, so a bad save can be rolled back
--    from the editor's history list. No foreign key on purpose: history outlives anything.
CREATE TABLE IF NOT EXISTS game_doc_revisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id TEXT NOT NULL,
    rev INTEGER NOT NULL,                      -- games.content_rev of the stored version
    raw_json TEXT NOT NULL,                    -- the whole game document as it was before the save
    admin_user TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_game_doc_revisions_game ON game_doc_revisions(game_id, id);

-- 4. Catalog version: bumped by every admin save; the public catalog endpoints put it
--    into their ETag and edge-cache key, so a save is visible on the next page load.
INSERT OR IGNORE INTO system_settings (key, value, description, updated_at) VALUES (
    'catalog_version',
    json_object('version', 1, 'updated_at', strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    '游戏目录版本号：后台保存游戏数据时 +1，公开目录接口靠它让缓存失效',
    CURRENT_TIMESTAMP
);
