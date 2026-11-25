-- ==============================================================================
-- L-MOD Vault - Migration v7: FLiNG trainer packages (site-hosted copies)
-- Compatible with: Cloudflare D1 (SQLite). Additive only: one new table + indexes.
--
-- File bodies live in Workers KV (binding TRAINER_FILES) under `<kv_prefix>/<n>`,
-- n = 0 .. chunks-1, each chunk at most 24 MiB. This table is the index the
-- manifest (/api/v1/trainers/manifest) and the download route (/dl/<game>/<file>)
-- read from.
--
-- status
--   uploading  row created, chunks still being written (never served)
--   active     served on the site; at most one per game (partial unique index)
--   withdrawn  taken down or replaced; its KV chunks are deleted
-- ==============================================================================

CREATE TABLE IF NOT EXISTS trainer_packages (
    id TEXT PRIMARY KEY,                        -- 'tp_' + 16 hex
    game_id TEXT NOT NULL,                      -- games.id, e.g. 'cyberpunk-2077'
    fling_page_url TEXT,                        -- official FLiNG page the file was taken from
    trainer_version TEXT,                       -- e.g. 'v1.03-v2.5+ Plus 46'
    game_version TEXT,                          -- game build the trainer targets
    file_name TEXT NOT NULL,                    -- original file name, served in Content-Disposition
    content_type TEXT NOT NULL DEFAULT 'application/octet-stream',
    size INTEGER NOT NULL,                      -- bytes
    sha256 TEXT NOT NULL,                       -- lower-case hex, computed in the admin's browser
    chunks INTEGER NOT NULL DEFAULT 1,          -- number of KV values
    kv_prefix TEXT NOT NULL,                    -- 'pkg/<id>'
    status TEXT NOT NULL DEFAULT 'uploading',   -- 'uploading' | 'active' | 'withdrawn'
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- set again when the package goes active
    note TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS uq_trainer_packages_one_active
    ON trainer_packages(game_id) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_trainer_packages_game ON trainer_packages(game_id, uploaded_at);
CREATE INDEX IF NOT EXISTS idx_trainer_packages_status ON trainer_packages(status);
