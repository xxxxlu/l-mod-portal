-- ==============================================================================
-- L-MOD Vault - Migration v6: 访客统计维度 + 按天汇总 + 反馈处理备注
-- Compatible with: Cloudflare D1 (SQLite)
--
-- 只做加法：加列、加索引、建新表、插一条默认配置（INSERT OR IGNORE，不覆盖已有值）。
-- 不删表、不删行、不改已有数据。
--
-- ⚠️ ALTER TABLE ... ADD COLUMN 不能重复执行（列已存在会报 duplicate column）。
--    执行前先确认还没跑过：
--      SELECT name FROM pragma_table_info('telemetry_events') WHERE name = 'page_path';
--    返回空 = 没跑过，可以执行；返回一行 = 已经跑过，不要再跑。
--
-- 隐私：新增的列都不含 IP。来源只记外站域名（host），不记完整 URL；
--       设备只分 mobile / tablet / desktop；不新增任何能识别个人的字段。
-- ==============================================================================

-- 1. telemetry_events 新维度（旧行这些列为 NULL，sample_rate 为 1）
ALTER TABLE telemetry_events ADD COLUMN page_path TEXT;        -- 页面路径，如 '/'、'/#/game/elden-ring'、'/radar'（不含 query）
ALTER TABLE telemetry_events ADD COLUMN referrer_host TEXT;    -- 外站来源域名，如 'www.bilibili.com'；站内跳转 / 直接打开为 NULL
ALTER TABLE telemetry_events ADD COLUMN device_type TEXT;      -- 'mobile' | 'tablet' | 'desktop'（按 UA 粗分）
ALTER TABLE telemetry_events ADD COLUMN ui_lang TEXT;          -- 界面语言，如 'zh-CN' / 'en'
ALTER TABLE telemetry_events ADD COLUMN site_host TEXT;        -- 事件来自哪个站：'lmod-vault.pages.dev' / 'xxxxlu.github.io'
ALTER TABLE telemetry_events ADD COLUMN sample_rate REAL DEFAULT 1;  -- 写入时生效的采样比例（统计时按 1/sample_rate 加权还原）

-- 2. 大盘按时间段 + 事件类型查询用的复合索引
CREATE INDEX IF NOT EXISTS idx_telemetry_created_type ON telemetry_events(created_at, event_type);

-- 3. 按天汇总表（明细只留 90 天，之后只剩这张表）
--    day 按北京时间（UTC+8）切分，和后台「今日」口径一致。
--    metric / dim 取值见 functions/api/v1/admin/analytics/_rollup.js 顶部注释。
CREATE TABLE IF NOT EXISTS telemetry_daily (
    day TEXT NOT NULL,                 -- 'YYYY-MM-DD'（UTC+8）
    metric TEXT NOT NULL,              -- 'pv' | 'uv' | 'events' | 'event' | 'country' | 'device' | 'lang' | 'referrer' | 'site' | 'page' | 'game' | 'search' | ...
    dim TEXT NOT NULL DEFAULT '',      -- 维度值（国家代码 / 事件类型 / 游戏 ID / 搜索词 ...），总量类指标为 ''
    value INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (day, metric, dim)
) WITHOUT ROWID;

-- 4. 汇总进度：一天汇总完写一行；已汇总的天才允许清理明细，没写过的天才会被汇总（保证幂等）
CREATE TABLE IF NOT EXISTS telemetry_rollup_days (
    day TEXT PRIMARY KEY,              -- 'YYYY-MM-DD'（UTC+8）
    raw_events INTEGER NOT NULL DEFAULT 0,   -- 汇总时这一天的明细行数（核对用）
    rolled_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. 反馈处理备注（后台「反馈」页签写）
ALTER TABLE community_feedback ADD COLUMN admin_note TEXT;
ALTER TABLE community_feedback ADD COLUMN handled_at DATETIME;

-- 6. 采样开关（默认 100% 全量）。已存在就不动。
INSERT OR IGNORE INTO system_settings (key, value, description, updated_at) VALUES (
    'telemetry_config',
    '{"sample_rate":1,"retention_days":90}',
    '访客统计：sample_rate 采样比例（0.01–1，1 = 全量记录）；retention_days 明细保留天数（之后只留按天汇总）',
    CURRENT_TIMESTAMP
);
