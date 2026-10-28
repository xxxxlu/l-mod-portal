-- ==============================================================================
-- L-MOD Vault - Migration v4: Email OTP, Player Identity & User Lifecycle
-- Compatible with: Cloudflare D1 (SQLite)
-- ==============================================================================

-- 1. Email Verification Codes (OTP Engine) Table
CREATE TABLE IF NOT EXISTS email_verification_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    code TEXT NOT NULL,
    purpose TEXT NOT NULL DEFAULT 'login',     -- 'login' | 'change_email' | 'reset_pwd'
    expires_at DATETIME NOT NULL,
    attempts INTEGER DEFAULT 0,
    is_used BOOLEAN DEFAULT 0,
    client_ip TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_email_codes_email ON email_verification_codes(email);
CREATE INDEX IF NOT EXISTS idx_email_codes_lookup ON email_verification_codes(email, code, purpose, is_used);
CREATE INDEX IF NOT EXISTS idx_email_codes_created ON email_verification_codes(created_at);
CREATE INDEX IF NOT EXISTS idx_email_codes_ip ON email_verification_codes(client_ip);

-- 2. Enhance Existing users Table (Safely Alter Columns)
-- Note: SQLite supports ADD COLUMN. If running repeatedly, ensure columns exist.
ALTER TABLE users ADD COLUMN email TEXT;
ALTER TABLE users ADD COLUMN password_hash TEXT;
ALTER TABLE users ADD COLUMN password_salt TEXT;
ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active';
ALTER TABLE users ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP;

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email) WHERE email IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_users_last_login ON users(last_login_at);

-- 3. Enhance community_feedback Table for Player Association
ALTER TABLE community_feedback ADD COLUMN user_id TEXT;
ALTER TABLE community_feedback ADD COLUMN player_email TEXT;
CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON community_feedback(user_id);

-- 4. Initial Email Service Configuration in system_settings
INSERT OR REPLACE INTO system_settings (key, value, description, updated_at) VALUES
(
    'email_service_config',
    '{"provider":"resend","from_email":"L-MOD Vault <security@lmod.gg>","template_style":"cyber_dark","cooldown_seconds":60,"code_valid_minutes":10,"max_attempts":5,"dev_mode":false}',
    '玩家邮箱验证码与通知邮件服务参数配置',
    CURRENT_TIMESTAMP
);

-- 5. Seed Realistic Test Players (1 with password, 1 OTP only)
-- Salt (16 hex bytes) & PBKDF2 HMAC-SHA256 hash (100,000 iterations for password: 'PlayerPass2026!')
-- Salt: a1b2c3d4e5f60718293a4b5c6d7e8f90
-- Pre-computed PBKDF2 hash of 'PlayerPass2026!'
INSERT OR REPLACE INTO users (id, provider, email, nickname, avatar_url, password_hash, password_salt, status, created_at, last_login_at, updated_at) VALUES
(
    'usr_cyber_veteran_01',
    'email',
    'nightcity_runner@lmod.gg',
    '单机老炮#2077',
    'avatar.jpg',
    'f6f7bc224e75d04ca07d894bfa2d512ee1ca5814bf98a58a9e4d58064cfb0b3e',
    'a1b2c3d4e5f60718293a4b5c6d7e8f90',
    'active',
    datetime('now', '-5 days'),
    datetime('now', '-10 minutes'),
    datetime('now', '-5 days')
),
(
    'usr_destiny_player_02',
    'email',
    'wukong_destiny@lmod.gg',
    '天命玩家#8921',
    'avatar.jpg',
    NULL,
    NULL,
    'active',
    datetime('now', '-2 days'),
    datetime('now', '-1 hours'),
    datetime('now', '-2 days')
);

-- 6. Seed User Favorites for the seeded players
INSERT OR REPLACE INTO user_favorites (user_id, game_id, created_at) VALUES
('usr_cyber_veteran_01', 'cyberpunk-2077', datetime('now', '-4 days')),
('usr_cyber_veteran_01', 'witcher-3', datetime('now', '-3 days')),
('usr_destiny_player_02', 'black-myth-wukong', datetime('now', '-1 days')),
('usr_destiny_player_02', 'elden-ring', datetime('now', '-6 hours'));

-- 7. Seed User Radar Subscriptions
INSERT OR REPLACE INTO user_radar_subscriptions (user_id, game_id, notify_channel, notify_target, created_at) VALUES
('usr_cyber_veteran_01', 'cyberpunk-2077', 'email', 'nightcity_runner@lmod.gg', datetime('now', '-4 days')),
('usr_destiny_player_02', 'black-myth-wukong', 'email', 'wukong_destiny@lmod.gg', datetime('now', '-1 days'));

-- 8. Connect seeded feedback records to real registered users
UPDATE community_feedback 
SET user_id = 'usr_cyber_veteran_01', player_email = 'nightcity_runner@lmod.gg' 
WHERE id = 101;

UPDATE community_feedback 
SET user_id = 'usr_destiny_player_02', player_email = 'wukong_destiny@lmod.gg' 
WHERE id = 102;
