# L-MOD Vault 游戏数据与 Cloudflare D1 指南

> **2026-11-23 起：D1 是游戏数据的真源。**
> 后台「游戏与指令运维」直接改 D1 `games.raw_json`，网站通过 `/api/v1/catalog` 读，保存后刷新页面就能看到。
> `public/data.js` 里的 `GAMES_DATA` 只是从 D1 导出的快照，用来先渲染和兜底。
> 本机主数据 `src/data/games_top100.json` 和「改 JSON → 生成 data.js → 灌 D1」的老流程已经退役（见第八节）。

---

## 一、数据怎么流

```
后台编辑器 ──POST /api/v1/admin/games/save──▶ D1 games.raw_json（整份游戏文档）
                                              ├─ 同一个事务里重算：games 平铺列、console_commands、scenario_bundles
                                              ├─ 旧版本存进 game_doc_revisions，写 admin_audit_logs
                                              └─ system_settings.catalog_version +1（接口缓存按它失效）

网站（index.html / radar.html）
  1. 先用 data.js 快照渲染（不等网络）
  2. GET /api/v1/catalog        轻字段目录 → 有变化才重画
  3. 进详情 GET /api/v1/catalog/:id   整份数据 → 有变化才重画
  接口拿不到（GitHub Pages 跨域失败、断网、8 秒超时）就一直用快照。

GitHub Pages（xxxxlu.github.io）跨域调 https://lmod-vault.pages.dev；Cloudflare Pages 上同源调。
```

**机器字段**（雷达 14 个字段、修改器 `hasTrainer` / `trainerHotkeys` / `trainerInfo`）不归后台管：

- 每天的雷达 / 修改器定时任务照旧写 `public/data.js`、`public/radar_status.json`、`public/trainers.json`；
- 接口读的时候用 `radar_status.json` / `trainers.json` 叠加（和 `functions/api/_radar_status.js` 同一套）；
- 后台保存时保留库里原来的值，编辑器里这两块只读；
- 前台对快照里已有的游戏不用接口覆盖这些字段（快照和两个 JSON 是同一次部署发出去的）。

字段清单在 `functions/api/v1/catalog/_game_doc.js`（`RADAR_FIELDS` / `TRAINER_FIELDS`）和 `public/js/catalog-live.js`，两边一起改。

## 二、表和字段

| 表 / 字段 | 是什么 | 谁写 |
|---|---|---|
| `games.raw_json` | 整份游戏文档，**唯一真源** | 后台保存 |
| `games` 的平铺列（`title`、`rank`、`titles_json`、`pitfall_note` …） | 从 `raw_json` 算出来的，给搜索和旧接口用 | 后台保存时重算 |
| `console_commands` / `scenario_bundles` | 派生索引，给 AI 助手和 `/api/v1/games/:id/commands`、`bundles`、`download` 用 | 后台保存时按游戏整组重建，**别直接改** |
| `games.is_hidden` | 隐藏（代替删除）：前台、目录、旧的公开接口都不返回 | 后台「隐藏 / 恢复显示」 |
| `games.content_rev` | 乐观锁：两个人同时改，后保存的那个会收到「已被别人改过」 | 每次保存 +1 |
| `game_doc_revisions` | 每次保存前的旧版本，编辑器「历史版本」能载入 | 后台保存 |
| `system_settings.catalog_version` | 目录版本号，接口的 ETag 和缓存键里都有它 | 后台保存 / 隐藏时 +1 |
| `admin_audit_logs` | 每次保存（`create_game_doc` / `update_game_doc`，带改了哪些字段）和隐藏都记一条 | 后台 |

`is_hidden`、`content_rev`、`game_doc_revisions`、`catalog_version` 来自 `database/migration_v5_game_docs.sql`。

**为什么派生表留着、不改成只读 `raw_json`**：AI 助手（`ai/chat.js`、`ai/context.js`、`admin/ai/test.js`）、
`games/:id/commands|bundles|download`、`meta/version`、`admin/me` 都按行查它们；改成每次请求解析 `raw_json`
会在免费版 10ms CPU 限额里吃紧，也要改一批 AI 文件。所以保留成索引，保存时在同一个事务里从 `raw_json` 重建，内容永远一致。
后台原来单条改指令 / 改游戏行的接口（`admin/commands/save`、`admin/commands/delete`、`admin/games/update`）已删除。

## 三、铁律

- ⛔ **绝不 `DELETE FROM games`，也不 `INSERT OR REPLACE INTO games`。** `user_favorites`、`user_radar_subscriptions`
  对 `games(id)` 是 `ON DELETE CASCADE`，删一行（REPLACE 也是先删再插）就连带删掉所有用户对这款游戏的收藏和订阅。
  不要的游戏用「隐藏」。
- 写线上 D1（迁移、导入、手工 SQL）之前：先问站长 → 整库备份 → 本地演练 → 再执行（第七节）。
- 游戏文案不写「实测 / 亲测 / 100% / 零风险 / 防封 / 完美兼容」这类说法。后台保存时会校验：
  新写进去的这类说法直接拦下（错误），库里原有的只提示（警告）；「一键 / 绝对 / 神器」这类夸张词只提示。
  校验规则在 `_game_doc.js` 的 `validateGameDoc`，结构规则和 `scripts/verify_deployment.py` 一致。

## 四、日常：在后台改游戏数据

后台 → 「游戏与指令运维」：

- **编辑**：分块改基本信息 / 8 语言标题、控制台与指令、场景套餐、精选 Mod、避坑笔记；「整份 JSON」可以直接改原文。
  「检查」只校验不保存；「保存」后版本号 +1，接口缓存随之失效，前台刷新就是新内容。
- **历史版本**：每次保存前的版本都留着，可以载入编辑器再保存回去（等于回滚，也会留一条新记录）。
- **新增游戏**：id 只能是小写字母、数字和 `-`。新游戏的雷达字段要等下一次导出快照 + 雷达定时任务才有；修改器字段按 `trainers.json` 算。
- **隐藏 / 恢复显示**：不删数据，用户的收藏和订阅都还在。

注意：AI 助手的游戏别名表（`build_game_aliases.py`）跟着快照走，改了标题 / 别名要等下一次导出快照才进 AI。

## 五、发版：把 D1 的改动带进快照

`data.js` 快照还要用（先渲染、GitHub Pages 兜底、定时任务读写、AI 别名表），所以发版前从 D1 导一次：

```bash
# 只执行 SELECT；--remote 用的是本机的 Cloudflare 登录，照样先问站长
python3 scripts/export_d1_snapshot.py --remote --dry-run   # 先看会改什么（新增 / 隐藏 / 哪些游戏哪些字段变了）
python3 scripts/export_d1_snapshot.py --remote             # 只替换 data.js 的 GAMES_DATA 一段，并重写 radar_status.json
python3 scripts/build_game_aliases.py
python3 scripts/build_prod.py && python3 scripts/verify_deployment.py && python3 scripts/verify_i18n_dual_pages.py
```

规则：隐藏的游戏不进快照；机器字段以现在的 `data.js` 为准（定时任务每天写的比库里新）。
`--local` 读本地开发库，`--sqlite <文件>` 读一个 SQLite 文件，`--output <目录>` 写到别处、不动仓库文件。

## 六、本地开发

```bash
# 1. 生成种子 SQL（database/seed_data.sql，不进仓库），顺带在 database/lmod_vault.db 里试灌一遍
python3 scripts/sync_to_database.py --one-time-import

# 2. 建本地开发库：建表 + 全部迁移 + 种子拼成一个文件执行。
#    迁移里有引用游戏的演示数据，D1 总是检查外键，所以开头要 defer_foreign_keys，种子灌完时外键才对得上。
rm -rf .wrangler/state/v3/d1      # 只删本机的本地开发库
{ echo "PRAGMA defer_foreign_keys = true;"
  for f in schema migration_v2 migration_v3_admin migration_v4_users migration_v5_game_docs migration_v6_telemetry migration_v7_trainer_packages; do cat database/$f.sql; echo; done
  cat database/seed_data.sql; } > .wrangler/local_bootstrap.sql
npx --yes wrangler@4.154.0 d1 execute lmod-vault-db --local --file .wrangler/local_bootstrap.sql

# 3. 起本地站点（带 Functions 和本地 D1）
npx --yes wrangler@4.154.0 pages dev public --port 8788
```

调试：浏览器里 `localStorage.setItem('lmod_api_base', 'http://127.0.0.1:8788')` 可以让别的端口的静态页去调本地接口
（模拟 GitHub Pages）；设成一个打不开的地址可以模拟接口挂掉。用完 `localStorage.removeItem('lmod_api_base')`。

测试：

```bash
node --test scripts/tests/catalog/                     # 目录接口、后台保存 / 隐藏 / 校验、和 Python 派生结果对齐
python3 -m unittest discover -s scripts/tests/db -v    # 种子 SQL、导出快照
node scripts/test_admin_api.js                          # 后台其它接口（要先跑第 1 步生成 database/lmod_vault.db）
```

## 七、改线上 D1 结构（迁移）

- 迁移只加不删：新文件 `database/migration_vN_*.sql`，只 `ADD COLUMN` / `CREATE TABLE IF NOT EXISTS` / `INSERT OR IGNORE`。
- 先迁移再部署代码（例如 v5：新代码读 `is_hidden`，库里没这个列接口会报错）。
- 每一步都要站长点头：

```bash
# 1. 整库备份到仓库外（导出里有 users 表，别提交）
npx --yes wrangler@4.154.0 d1 export lmod-vault-db --remote --output <仓库外的备份目录>/lmod-vault-db-<日期>.sql

# 2. 本地演练：备份灌进一个临时库，跑迁移，核对用户数据行数不变
npx --yes wrangler@4.154.0 d1 execute lmod-vault-db --local --persist-to /tmp/d1-rehearsal --file <仓库外的备份目录>/lmod-vault-db-<日期>.sql
npx --yes wrangler@4.154.0 d1 execute lmod-vault-db --local --persist-to /tmp/d1-rehearsal --file database/migration_vN_xxx.sql
npx --yes wrangler@4.154.0 d1 execute lmod-vault-db --local --persist-to /tmp/d1-rehearsal --command \
  "SELECT (SELECT count(*) FROM games) games, (SELECT count(*) FROM users) users, (SELECT count(*) FROM user_favorites) favs, (SELECT count(*) FROM user_radar_subscriptions) subs"
#    顺便对一下线上内容和 data.js 有没有出入（演练库文件在 <persist-to>/v3/d1/miniflare-D1DatabaseObject/<一串哈希>.sqlite）
python3 scripts/export_d1_snapshot.py --sqlite /tmp/d1-rehearsal/v3/d1/miniflare-D1DatabaseObject/<哈希>.sqlite --dry-run

# 3. 正式执行
npx --yes wrangler@4.154.0 d1 execute lmod-vault-db --remote --file database/migration_vN_xxx.sql
```

`migration_v5_game_docs.sql` 第一句是 `ALTER TABLE ADD COLUMN`，重复执行会报「duplicate column」。本地验证过整份不生效、数据不变；
线上照样别重复跑，跑之前用 `PRAGMA table_info(games)` 看一眼有没有 `is_hidden`。

## 八、已退役 / 待定

- `src/data/games_top100.json`（本机主数据）：退役。`export_d1_snapshot.py` 发现它还在会提醒改名备份，免得老脚本拿它覆盖 `data.js`。
- `scripts/sync_to_database.py`：**只用于一次性导入**（线上 2026-11-20 已导入过）和建本地开发库，不带 `--one-time-import` 不运行。
  它生成的 SQL 灌到哪个库，就会覆盖那个库里后台保存过的内容。
- 后台旧接口 `admin/games/update`、`admin/commands/save`、`admin/commands/delete`：已删除，改用整份文档保存。
- 生成 / 补全数据的老脚本（直接写 JSON 或 data.js、绕过 D1）：是否删除待站长定，在那之前**别跑**：
  `enrich_database_v2.py`、`enrich_database_v3.py`、`enrich_flagship_scenarios.py`、`enrich_rank5_7_flagships.py`、
  `enrich_rank8_14_tier2.py`、`deep_enrich_game.py`、`deep_enrich_witcher3.py`、`deep_enrich_wukong.py`、
  `rebuild_bg3_flagship.py`、`rebuild_witcher3_flagship.py`、`generate_games_data.py`、`sanitize_database_bulk.py`、
  `upgrade_cyberpunk_schema.py`、`build_full_database.py`、`setup_d1_auto.sh`、`ai_enrich_engine.py`。
  定时任务（`patch_radar_cron.yml`、`trainer_sync_cron.yml`）只写机器字段，不受影响，照常跑。

## 九、额度（Cloudflare 免费版）

| 项 | 免费额度 | 这里怎么用 |
|---|---|---|
| Pages Functions 请求 | 每天 10 万次 | 每次打开页面 1 次目录请求（多数是 304），每进一个详情 1 次 |
| D1 读 | 每天 500 万行 | 目录请求先读 1 行版本号；缓存没命中时再读 100 行 |
| D1 写 | 每天 10 万行 | 后台保存一次写的行数约为这款游戏指令数 + 套餐数的两倍（整组先删后插） |
| D1 存储 | 单库 500 MB（账号合计 5 GB） | 游戏数据约 2 MB；大头会是访客统计明细 |
| 单次调用 | CPU 10ms、最多 50 条查询 | 目录在 SQL 里裁字段，Worker 里只做叠加；保存的查询条数测试里卡在 50 以内 |

接口缓存：ETag 由版本号 + `radar_status.json` / `trainers.json` 的更新时间组成，浏览器每次都回源校验（304 不带正文）；
边缘用 Cache API 缓存 60 秒，缓存键里带版本号，所以后台保存后立刻生效。
