-- ==============================================================================
-- L-MOD Vault - Migration v3: Admin Console & AI Control Plane Schema
-- Compatible with: Cloudflare D1 (SQLite)
-- ==============================================================================

-- 1. System Settings & AI Configuration Store (Key-Value)
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Administrator Audit Logs
CREATE TABLE IF NOT EXISTS admin_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,                      -- e.g. 'update_game', 'update_command', 'change_ai_config', 'trigger_radar', 'admin_login'
    entity TEXT,                               -- e.g. 'games', 'console_commands', 'system_settings', 'auth'
    entity_id TEXT,                            -- e.g. 'cyberpunk-2077', 'ai_config'
    details TEXT,                              -- JSON or text summary of change
    admin_user TEXT DEFAULT 'admin',
    client_ip TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON admin_audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON admin_audit_logs(created_at);

-- 3. Initial System Settings Seeds
INSERT OR REPLACE INTO system_settings (key, value, description, updated_at) VALUES
(
    'admin_credentials',
    '{"username":"admin","password":"lmod2026!","updated_at":"2026-10-27T12:00:00Z"}',
    '站长后台登录账号与密码配置 (默认: admin / lmod2026!)',
    CURRENT_TIMESTAMP
),
(
    'ai_config',
    '{"system_prompt":"你是由 L-MOD Vault 官方研发的‘老L’——全球单机游戏底层指令与避坑智库首席顾问。你精通 CET Lua、UE4SS、Creation Engine 控制台语法与反作弊机制。你的回答风格：言简意赅、老练严谨、绝不废话、直击痛点。遇到破坏存档或与补丁冲突的高危指令，必须第一时间发出红色预警并给出备份方案。","tone":"hardcore_veteran","tone_label":"资深单机老炮 / 严谨避坑顾问","temperature":0.3,"recall_threshold":0.65,"max_context_commands":6,"primary_model":"gemini-2.5-flash","fallback_model":"deepseek-chat","skills":{"code_dedup":true,"syntax_validator":true,"steam_diff":true,"downgrade_wizard":true,"save_backup_guard":true},"custom_rules":["所有控制台代码必须经过真实游戏版本与引擎测试，严禁杜撰幻觉指令","对于赛博朋克2077等使用CET框架的游戏，明确区分Lua代码与原生控制台代码","对涉及等级、金钱过亿、跳过主线等高危指令，强制添加【坏档警示】"],"updated_at":"2026-10-27T12:00:00Z"}',
    '老L·AI Copilot 智库系统人设、技能编排与大模型路由配置',
    CURRENT_TIMESTAMP
),
(
    'emergency_broadcast',
    '{"enabled":false,"level":"yellow","title":"Steam 补丁兼容性预警","message":"近期 Steam 推出部分游戏热更新，请注意查看指令与前置框架适配指示灯。","target_game_id":null,"updated_at":"2026-10-27T12:00:00Z"}',
    '全站紧急熔断与补丁警示跑马灯广播配置',
    CURRENT_TIMESTAMP
),
(
    'sentinel_config',
    '{"auto_check_interval_hours":6,"flagships_only":false,"last_scan_at":"2026-10-27T10:00:00Z","notify_on_break":true}',
    'Steam 补丁巡检哨兵机器人自动化调度参数',
    CURRENT_TIMESTAMP
);

-- 4. Initial Audit Log
INSERT INTO admin_audit_logs (action, entity, entity_id, details, admin_user, client_ip)
VALUES ('system_init', 'migration', 'v3', 'Initialized Admin Console, Zero Trust Auth & AI Control Plane schema', '老L·站长', '127.0.0.1');

-- 5. Seed Historical Patch Radar Audit Logs
INSERT OR IGNORE INTO patch_radar_logs (game_id, patch_title, patch_date, build_id, status, risk_title, risk_desc, emergency_broadcast, checked_at) VALUES
('cyberpunk-2077', 'Cyberpunk 2077 Patch 2.13', '2026-10-25', '13982104', 'green', '完美兼容', 'CET v1.33.0 验证通过，所有基础与高级Lua控制台指令正常生效，无坏档风险。', NULL, datetime('now', '-2 hours')),
('black-myth-wukong', 'Black Myth: Wukong Hotfix 1.0.10', '2026-10-26', '14210982', 'green', '完美兼容', 'UE4SS 3.0.1 框架稳定，虚幻5控制台指令全部通过沙盒验证。', NULL, datetime('now', '-4 hours')),
('witcher-3', 'The Witcher 3: Wild Hunt Hotfix 4.04c', '2026-10-24', '13109281', 'green', '完美兼容', 'REDengine 3 原生控制台完美兼容，无前置依赖冲突。', NULL, datetime('now', '-18 hours')),
('baldurs-gate-3', 'Baldurs Gate 3 Patch 7 Hotfix 28', '2026-10-26', '14890123', 'yellow', '脚本扩展需注意', 'BG3 Script Extender v18 已发布适配，使用旧版前置可能导致控制台呼出闪退。', '请使用BG3 Mod Manager更新Script Extender至最新版本。', datetime('now', '-1 hours')),
('elden-ring', 'ELDEN RING App Ver. 1.14 / Calibrations 1.14.1', '2026-10-27', '14992810', 'green', '全指令与修改器正常', '离线防封启动器与常用Hex指令已完成双重验证。', NULL, datetime('now', '-30 minutes'));

-- 6. Seed Realistic Community Feedback Records for Moderation
INSERT OR IGNORE INTO community_feedback (id, game_id, category, content, player_nickname, player_ip_country, status, created_at) VALUES
(101, 'cyberpunk-2077', 'bug_report', '在最新2.13补丁中，控制台输入Game.AddToInventory("Items.Preset_Lexington_Toy", 1)提示找不到预设，建议核对代码字典。', '夜之城老司机', 'CN', 'pending', datetime('now', '-3 hours')),
(102, 'black-myth-wukong', 'mod_request', '希望站长能补充大圣套全套获取的一键bat脚本，目前单个指令复制稍显繁琐。', '天命人007', 'CN', 'pending', datetime('now', '-5 hours')),
(103, 'witcher-3', 'comment', '站长整理的昆特牌全套收集代码亲测好用！拯救了全成就强迫症，支持L-MOD智库！', '利维亚的猎魔人', 'HK', 'verified', datetime('now', '-1 day')),
(104, 'starfield', 'bug_report', '星空代码 player.additem 0000000F 100000 正常生效，但飞船改装代码有些失效了。', 'StarExplorer', 'US', 'pending', datetime('now', '-2 days')),
(105, 'baldurs-gate-3', 'bug_report', 'Patch 7 更新后官方内置了模组管理器，旧版Script Extender的控制台指令需要重新激活。', '阿斯代伦狂粉', 'JP', 'resolved', datetime('now', '-3 days'));

-- 7. Seed Diverse Realistic Telemetry Events for Analytics Dashboard
INSERT INTO telemetry_events (event_type, game_id, target_payload, session_id, user_id, client_country, created_at) VALUES
('search_query', 'cyberpunk-2077', '2077 四季宝', 'sess_cn_001', NULL, 'CN', datetime('now', '-10 minutes')),
('search_query', 'black-myth-wukong', '黑神话 避坑', 'sess_cn_002', NULL, 'CN', datetime('now', '-15 minutes')),
('search_query', 'elden-ring', '法环 无敌锁血', 'sess_us_001', NULL, 'US', datetime('now', '-20 minutes')),
('search_query', 'cyberpunk-2077', '强尼银手手枪', 'sess_cn_003', NULL, 'CN', datetime('now', '-25 minutes')),
('search_query', 'witcher-3', '昆特牌全套代码', 'sess_hk_001', NULL, 'HK', datetime('now', '-35 minutes')),
('search_query', 'baldurs-gate-3', '博德之门3 属性点', 'sess_jp_001', NULL, 'JP', datetime('now', '-45 minutes')),
('search_query', 'starfield', '星空 飞船部件', 'sess_de_001', NULL, 'DE', datetime('now', '-50 minutes')),
('search_query', 'cyberpunk-2077', '钱 金币 100万', 'sess_cn_004', NULL, 'CN', datetime('now', '-55 minutes')),
('search_query', 'red-dead-redemption-2', '大表哥2 传送代码', 'sess_cn_005', NULL, 'CN', datetime('now', '-60 minutes')),
('search_query', 'skyrim-se', '上古卷轴5 控制台启动', 'sess_us_002', NULL, 'US', datetime('now', '-70 minutes')),

('copy_code', 'cyberpunk-2077', 'Game.AddToInventory("Items.money", 1000000)', 'sess_cn_001', NULL, 'CN', datetime('now', '-8 minutes')),
('copy_code', 'cyberpunk-2077', 'Game.AddToInventory("Items.Preset_Silverhand_3516", 1)', 'sess_cn_003', NULL, 'CN', datetime('now', '-22 minutes')),
('copy_code', 'cyberpunk-2077', 'Game.SetLevel("Level", 50)', 'sess_cn_004', NULL, 'CN', datetime('now', '-30 minutes')),
('copy_code', 'witcher-3', 'additem(''gwint_card_geralt'')', 'sess_hk_001', NULL, 'HK', datetime('now', '-32 minutes')),
('copy_code', 'witcher-3', 'addmoney(50000)', 'sess_hk_001', NULL, 'HK', datetime('now', '-33 minutes')),
('copy_code', 'starfield', 'player.additem 0000000F 100000', 'sess_de_001', NULL, 'DE', datetime('now', '-48 minutes')),
('copy_code', 'skyrim-se', 'tgm', 'sess_us_002', NULL, 'US', datetime('now', '-65 minutes')),
('copy_code', 'skyrim-se', 'player.setav speedmult 150', 'sess_us_002', NULL, 'US', datetime('now', '-66 minutes')),
('copy_code', 'elden-ring', 'CheatEngine_Offline_Invulnerable', 'sess_us_001', NULL, 'US', datetime('now', '-18 minutes')),
('copy_code', 'cyberpunk-2077', 'Game.AddToInventory("Items.money", 1000000)', 'sess_cn_006', NULL, 'CN', datetime('now', '-5 minutes')),

('download_bat', 'cyberpunk-2077', '新手破荒启动批处理包.bat', 'sess_cn_001', NULL, 'CN', datetime('now', '-7 minutes')),
('download_bat', 'black-myth-wukong', '大圣全套珍玩直达包.bat', 'sess_cn_002', NULL, 'CN', datetime('now', '-12 minutes')),
('download_bat', 'witcher-3', '全昆特牌神级卡组注入.bat', 'sess_hk_001', NULL, 'HK', datetime('now', '-28 minutes')),
('download_bat', 'cyberpunk-2077', '夜之城全义体橙装解锁.bat', 'sess_cn_004', NULL, 'CN', datetime('now', '-40 minutes')),
('download_bat', 'baldurs-gate-3', '博德之门3无压力剧情启动包.bat', 'sess_jp_001', NULL, 'JP', datetime('now', '-42 minutes')),

('ai_ask', 'cyberpunk-2077', '2077 怎么用 CET 调出不朽武器四季宝？', 'sess_cn_001', NULL, 'CN', datetime('now', '-9 minutes')),
('ai_ask', 'black-myth-wukong', '黑神话打不过虎先锋怎么调攻击力？', 'sess_cn_002', NULL, 'CN', datetime('now', '-14 minutes')),
('ai_ask', 'elden-ring', '法环DLC补丁更新后CE修改器会不会被EAC封号？', 'sess_us_001', NULL, 'US', datetime('now', '-19 minutes')),

('view_game', 'cyberpunk-2077', 'view_detail', 'sess_cn_001', NULL, 'CN', datetime('now', '-10 minutes')),
('view_game', 'black-myth-wukong', 'view_detail', 'sess_cn_002', NULL, 'CN', datetime('now', '-16 minutes')),
('view_game', 'witcher-3', 'view_detail', 'sess_hk_001', NULL, 'HK', datetime('now', '-36 minutes')),
('view_game', 'baldurs-gate-3', 'view_detail', 'sess_jp_001', NULL, 'JP', datetime('now', '-46 minutes')),
('view_game', 'elden-ring', 'view_detail', 'sess_us_001', NULL, 'US', datetime('now', '-21 minutes')),
('view_game', 'starfield', 'view_detail', 'sess_de_001', NULL, 'DE', datetime('now', '-51 minutes')),
('view_game', 'red-dead-redemption-2', 'view_detail', 'sess_cn_005', NULL, 'CN', datetime('now', '-61 minutes')),
('view_game', 'skyrim-se', 'view_detail', 'sess_us_002', NULL, 'US', datetime('now', '-71 minutes'));
