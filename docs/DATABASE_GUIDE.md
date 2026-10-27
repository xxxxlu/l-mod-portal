# L-MOD Vault - 全球免费数据库架构与上线部署指南 (Global Free DB Guide)

> **目标**：为全球玩家（国内外直连、零服务器成本）提供高性能、高并发、免翻墙的分布式数据库支撑。

---

## 📊 一、全球免费数据库横向评测与选型

针对我们项目的需求（**免费**、**全球任何地方都能秒开**、**与单机智库架构契合**），对目前市面上主流的 Serverless 数据库进行对比：

| 数据库平台 | 底层引擎 | 全球节点与架构 | 免费额度配额 | 国内外访问可用性 | 与 L-MOD Vault 契合度 |
|---|---|---|---|---|---|
| **🥇 Cloudflare D1**<br/>*(强烈首选推荐)* | 分布式 SQLite | 依托 Cloudflare **300+ 边缘机房** (Anycast 智能就近路由) | **5 GB 存储**<br/>每天 **500 万次读**<br/>每天 **10 万次写** | 🇨🇳 国内直连香港/日本节点<br/>🌍 全球超低延迟 (10~50ms) | ⭐⭐⭐⭐⭐ **100% 完美契合**<br/>(项目已配置 Cloudflare Pages 部署，同一控制台零成本原生联动) |
| **🥈 Supabase**<br/>*(全功能备选)* | PostgreSQL | AWS 亚太机房 (东京/新加坡) 或欧美 | **500 MB 存储**<br/>50,000 月活用户<br/>无限 API 请求 | 自定义域名反代后国内极稳；官方默认域名偶有波动 | ⭐⭐⭐⭐ **极佳**<br/>(自带 PostgREST，前端可直接写 SQL，带用户鉴权) |
| **🥉 Turso**<br/>*(极客分布式)* | LibSQL (SQLite) | 全球 30+ 区域边缘多副本 | **9 GB 存储**<br/>每月 **10 亿次读**<br/>500 个数据库 | 支持 HTTP/WebSocket 直连 | ⭐⭐⭐⭐ **优秀**<br/>(跨区域多活写入能力强) |
| **4. Neon** | Serverless Postgres | AWS 区域 | **0.5 GB 存储**<br/>无限分支 | 欧美极快，国内偶需边缘代理 | ⭐⭐⭐ **良好** |

---

## 🏆 为什么 Cloudflare D1 是终极首选？

1. **零成本与天量配额**：
   - 我们的单机游戏智库（100 款大作全量分类与指令）全部 SQL 种子数据仅 **1.9 MB**；
   - Cloudflare D1 免费版赠送 **5 GB**（相当于可容纳 2,500 倍的数据量！）；
   - 每天 **500 万次免费行读取**，即便每天有几十万玩家同时在线查代码，也不会产生一分钱账单。
2. **全球 300+ 边缘机房极速访问**：
   - 无论玩家身处国内北上广深，还是海外欧美、东南亚、日韩，流量自动命中离他物理距离最近的边缘节点，杜绝任何跨境网络阻塞。
3. **独家双轨高可用架构 (High Availability)**：
   - **线上网络畅通时**：通过 `/api/games` 与 `/api/radar` 读取 D1 最新动态；
   - **弱网/离线/纯本地打开时**：自动无缝降级使用打包在本地的 `public/data.js`，**保证 100% 永远不宕机、不白屏！**

---

## 🚀 二、Cloudflare D1 极速上线实操步骤（耗时 < 3 分钟）

工程内已准备好全自动建表与种子数据脚本：
- 表结构文件：[`database/schema.sql`](file:///Users/xiaolu/Desktop/work/l-mod-portal/database/schema.sql)
- 种子数据文件：[`database/seed_data.sql`](file:///Users/xiaolu/Desktop/work/l-mod-portal/database/seed_data.sql) (1.9MB / 100款游戏 / 1,093条指令 / 42个场景包)
- 边缘 API：[`functions/api/games.js`](file:///Users/xiaolu/Desktop/work/l-mod-portal/functions/api/games.js) 与 [`functions/api/radar.js`](file:///Users/xiaolu/Desktop/work/l-mod-portal/functions/api/radar.js)

### 第一步：在终端创建 D1 免费数据库
在项目根目录下执行：
```bash
npx wrangler d1 create lmod-vault-db
```
执行完毕后，控制台会输出类似如下的数据库配置信息：
```toml
[[d1_databases]]
binding = "DB"
database_name = "lmod-vault-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 第二步：一键导入 Schema 与全量数据
依次执行以下命令，将 100 款游戏与全息指令灌入全球边缘节点：
```bash
# 1. 创建数据表 (games, console_commands, scenario_bundles, patch_radar_logs)
npx wrangler d1 execute lmod-vault-db --remote --file=database/schema.sql

# 2. 导入全量种子数据
npx wrangler d1 execute lmod-vault-db --remote --file=database/seed_data.sql
```

### 第三步：在 Cloudflare Pages 绑定数据库
1. 登录 [Cloudflare 控制台](https://dash.cloudflare.com/)；
2. 进入 **Workers & Pages** -> 找到我们的项目 `lmod-vault`；
3. 点击 **Settings (设置)** -> **Functions (函数)** -> **D1 database bindings (D1 数据库绑定)**；
4. 点击 **Add binding**：
   - **Variable name (变量名)**：填写 `DB`
   - **D1 database**：选择刚才创建的 `lmod-vault-db`；
5. 点击 **Save (保存)**。

---

## 🛠️ 三、若选用 Supabase 上线方案

如果您更习惯使用 PostgreSQL 或喜欢 Supabase 的图形化数据浏览器：

1. 打开 [supabase.com](https://supabase.com/) 免费注册并创建组织；
2. 新建项目（区域推荐选择靠近国内的 **Tokyo** 或 **Singapore**）；
3. 进入左侧菜单的 **SQL Editor**；
4. 直接复制项目内 [`database/schema.sql`](file:///Users/xiaolu/Desktop/work/l-mod-portal/database/schema.sql) 的内容粘贴运行；
5. 复制 [`database/seed_data.sql`](file:///Users/xiaolu/Desktop/work/l-mod-portal/database/seed_data.sql) 的内容粘贴运行；
6. 即可在 **Table Editor** 中直观浏览与编辑 100 款游戏和全部 1,093 条指令！

---

## 📦 四、本地调试与重新生成数据种子

若后续通过 `scripts/ai_enrich_engine.py` 或 `games_top100.json` 更新了游戏数据，只需运行：

```bash
# 自动重新生成 database/seed_data.sql 并在本地 SQLite 中进行入库验证
python3 scripts/sync_to_database.py
```
终端会输出验证指标并提示一键推送到线上 D1 数据库！
