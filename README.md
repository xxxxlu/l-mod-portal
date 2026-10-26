# L-MOD Vault (老L·单机游戏模组与避坑智库)

> 全球单机游戏 MOD · 纯净修改器 · 官方控制台代码库 · Steam 补丁变动实时避坑雷达  
> **Clean Global Hub for Single-Player Game Mods, Pure Trainers, Official Console Cheats & Patch Radar**

---

## 🌟 核心产品护城河与定位

针对国内传统下载站（流氓广告/假高速下载器/木马捆绑）与海外 Nexus Mods（强制登录/限速/纯英文门槛）的痛点，打造**极简、安全、零广告、中英双语首发、面向全球玩家的现代化游戏工具站与避坑智库**：

1. **多国语言国际化 (8 大热门国家原生支持)**：
   - 🇨🇳 简体中文 (`zh-CN`) ｜ 🇺🇸 English (`en`) ｜ 🇭🇰 繁體中文 (`zh-TW`)
   - 🇯🇵 日本語 (`ja`) ｜ 🇰🇷 한국어 (`ko`) ｜ 🇷🇺 Русский (`ru`)
   - 🇩🇪 Deutsch (`de`) ｜ 🇪🇸 Español (`es`)
2. **首发全量上线 Top 100 热门单机游戏 (前 7 款旗舰深度全息重构)**：
   - 严格按全网综合热度、Steam 评价数与 MOD 需求量降序排行（#1《赛博朋克2077》至 #100《杀戮尖塔》）。
   - **Rank 1~7 旗舰大作已 100% 对齐最新官方补丁**（含法环黄金树幽影 v1.14、辐射4次世代版、博德之门3 Patch 7、巫师3次世代完全版等），通过强类型 Schema 校验与语法 Linter。
3. **小白 10 秒一键爽到（场景化套餐与一键开门）**：
   - **极客推荐场景套餐**：【新手破荒包】、【隐藏结局救赎包】、【二周目全神装包】，一键整段打包复制；
   - **懒人双击一键开门**：自动生成极简 `.bat` 批处理，自动备份原文件，双击即搞定控制台注入；
   - **智能滚动无损复位**：从列表进入详情页返回时，精准复位到刚才点击时的滚动视口高度，并附带微光脉冲高亮。
4. **《Steam 补丁兼容性与坏档避坑实时雷达》(`public/radar.html`)**：
   - 独立产品化轻量看板，三色指示灯（🟢 完美兼容 / 🟡 需更新前置 / 🔴 坏档预警），内置紧急广播与一键救砖指南。
5. **社交平台工业级 5 联图出图与合规矩阵 (`social_distribution/`)**：
   - 自动化防限流脱敏词典，一键导出 1080×1440 高清 PNG 5 联图，配套小红书爆款文案与 B 站动态。
6. **零风险私域中转与商业闭环**：
   - 公众号纯文本安全自动回复 + 避坑互助群零 exe 防封群规 + 夸克网盘转存拉新与爱发电赞赏。

---

## 📂 项目工程结构

```
l-mod-portal/
├── public/
│   ├── index.html        # 主应用：响应式极简暗黑单页应用 (Tailwind + Vanilla JS, 零配置秒开)
│   ├── radar.html        # 独立看板：《Steam 补丁变动与 Mod 兼容性实时避坑雷达》
│   ├── data.js           # 100 款游戏数据与 8 语言多语言词条离线脚本 (支持 file:// 与 http://)
│   ├── avatar.jpg        # 品牌官方主理人「老L」头像
│   ├── social_distribution/ # 7 款旗舰大作多平台 35 张高清 PNG 卡片与文案包
│   └── social_matrix/    # 社交矩阵 HTML 预览页面
├── src/
│   ├── data/
│   │   ├── games_top100.json     # 100 款游戏完整结构化数据库 (支持持续扩充)
│   │   └── production_schedule.json # 游戏采掘与内容生产量化周排期跟踪表
│   └── i18n/
│       └── translations.json     # 8 大热门游戏国家完整 UI 翻译矩阵
├── docs/
│   ├── FLAGSHIP_MINING_GUIDE_RANK5_7.md # Rank 5~7 旗舰攻坚技术手册 (法环/老滚5/辐射4)
│   ├── PIPELINE_SOP.md                  # 工业级标准化五步流水线 SOP 规范
│   ├── PRODUCTION_SCHEDULE.md           # 周节奏排期时间线矩阵与工时规划
│   └── PRIVATE_TRAFFIC_BLUEPRINT.md     # 零风险私域转化中转与商业闭环全案
├── scripts/
│   ├── audit_game_data.py               # 游戏数据完整性、引擎语法合法性与真实性门禁
│   ├── validate_game.py                 # Schema 强类型离线自动化验证工具
│   ├── generate_social_matrix.py        # 社交素材合规脱敏与 HTML 卡片渲染引擎
│   ├── render_cards_png.py              # 1080×1440 高清 PNG 工业级出图脚本
│   └── enrich_rank5_7_flagships.py      # Rank 5~7 旗舰全息数据注入脚本
├── scripts/
│   ├── steam_patch_monitor.py # 24h Steam 补丁自动化巡检机器人与突发坏档实时预警哨兵
│   ├── build_i18n_matrix.py   # 多语言矩阵与离线 data.js 自动化打包器
│   └── verify_i18n_dual_pages.py # 双页面 8 语言完整性 E2E 质检门禁
├── .github/
│   └── workflows/
│       └── patch_radar_cron.yml # GitHub Actions 每日 10:00 CST 定时巡检自动化流水线
├── docs/
│   ├── STEAM_PATCH_MONITOR_GUIDE.md # 补丁巡检机器人完整操作手册与演练指南
│   ├── PATCH_MONITOR_LATEST.md    # 巡检机器人最新生成的官方版本对账简报与群公告
│   └── DEPLOYMENT_GUIDE.md        # 独立站全球 CDN 极速部署指南
└── README.md
```

---

## 🤖 Steam 补丁变动自动化巡检机器人 (Milestone 3)

通过 Steam 官方公共 API 自动化对账各单机大作的官方补丁动向与 Build ID，解决官方突发推送更新导致 Mod 失效和坏档问题：

```bash
# 1. 执行巡检并同步至避坑雷达看板
python3 scripts/steam_patch_monitor.py --update-radar

# 2. 模拟官方突发大更新（演练避坑预警与群公告生成）
python3 scripts/steam_patch_monitor.py --simulate-patch cyberpunk-2077 --simulate-version "Update 2.5 (Edgerunners 2)" --simulate-risk red --update-radar

# 3. 运行双页面与多语言全量门禁校验
python3 scripts/verify_i18n_dual_pages.py
```

---

## 🚀 启动与预览方式

- **本地主站访问**：
  直接在浏览器打开：
  `file:///Users/xiaolu/Desktop/work/l-mod-portal/public/index.html`
- **本地补丁雷达看板**：
  直接在浏览器打开：
  `file:///Users/xiaolu/Desktop/work/l-mod-portal/public/radar.html`
- **本地 HTTP 服务预览**：
  本地服务常驻于端口 `18088`：
  - 主站：`http://localhost:18088/index.html`
  - 雷达：`http://localhost:18088/radar.html`
- **一键全球 CDN 部署**：
  可将 `public/` 目录直接推送到 Cloudflare Pages、Vercel 或 GitHub Pages，实现零成本全球高速直连。

---

## 🔄 社交媒体与私域飞轮

由主理人 **`老L`**（老L·单机避坑局）在小红书、B 站发布避坑与隐藏机制爆款图文：
- **公域内容**：发布 1080×1440 高清 5 联图，痛批流氓捆绑外挂，揭秘官方底层隐藏调试与逃课机制；
- **合规中转**：评论区置顶暗号，引导至公众号自动获取免配置脚本与独立雷达看板直达；
- **私域留存**：沉淀至避坑互助群，第一时间同步 Steam 补丁更新与坏档急救，形成“**公域引流 ➔ 独立站体验 ➔ 私域留存 ➔ 良性变现**”的坚实商业闭环。
