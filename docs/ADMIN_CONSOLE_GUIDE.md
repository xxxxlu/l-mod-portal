# L-MOD Vault 站长专属管理中台与 AI 控制平面使用与架构手册
**L-MOD Vault Admin Console & AI Control Plane Architecture Guide (v3.0)**

---

## 一、系统架构与设计理念 (Architecture & Zero Trust)

L-MOD Vault 作为面向全球玩家的单机游戏纯净智库与避坑雷达，采用 **Cloudflare Pages + Cloudflare D1（分布式 SQLite）+ Pages Functions（边缘无服务器架构）** 构建。

为了在**不向普通玩家开放注册登录**的前提下，为**站长（超级管理员）**提供安全、隐蔽、功能强悍的运维中台，本中台基于 **零信任架构（Zero Trust Architecture）** 与 **Web Crypto 原生无状态 JWT** 机制打造，具备以下核心技术优势：

```
+-----------------------------------------------------------------------------------+
|                            L-MOD Vault 站长控制平面                                  |
+-----------------------------------------------------------------------------------+
         │
         ├── [隐蔽入口] Ctrl + Shift + L / Logo 5连击 / /admin 路由
         │
         ├── [认证层] POST /api/v1/admin/login 
         │      └─ Web Crypto HMAC-SHA256 签发 7天无状态 Admin JWT
         │
         ├── [安全守卫] functions/api/v1/admin/_middleware.js
         │      └─ 毫秒级验签 + 角色权限拦截 (非站长 403 Forbidden)
         │
         └── [四大核心中台模块]
                ├── 1. 玩家数据分析大盘 (PV/UV / 搜索热词 / 复制代码流 / 报错审核)
                ├── 2. 游戏与指令知识库动态运维 (100 款大作 / 补丁版本 / 代码即时同步)
                ├── 3. 老L·AI 顾问与 Skills 编排台 (人设调优 / 技能开关 / 沙盒测试)
                └── 4. Steam 补丁巡检哨兵机器人 (24h审计日志 / 手动触发 / 紧急熔断广播)
```

---

## 二、隐蔽入口与零信任鉴权机制 (Stealth Entrance & Auth)

### 1. 隐蔽入口触发方式 (三种通道)
1. **全局快捷键**：在站内任意页面（`index.html` 或 `radar.html`）按下 `Ctrl + Shift + L`（Mac 用户为 `Cmd + Shift + L`），立即唤出赛博毛玻璃认证视窗。
2. **品牌 Logo 5连击彩蛋**：在 3 秒内连续点击左上角 L-MOD 品牌 Logo 5次，激活站长特权认证通道。
3. **隐蔽路由直达**：直接访问 `https://lmod-vault.pages.dev/admin` 或 `/admin.html`。

### 2. 站长默认账号密码与 Web Crypto 原生 JWT 鉴权流程
- **预设初始凭据 (Default Credentials)**：
  - **站长管理账号 (Username)**：`admin`（同时支持别名 `laol`，大小写不敏感）
  - **站长初始密码 (Password)**：`lmod2026!`（或兼容历史密钥 `lmod-vault-master-station-key-2026`）
  - **登录界面提供一键自动填入按钮**，方便站长快速登录。
- **在线改密支持**：登录后在中台顶部点击【修改密码】按钮，输入原密码与新密码即可在线热更新，新密码即刻持久化到 D1 `system_settings` 的 `admin_credentials` 记录中。
- **环境变量托管**：亦可在 Cloudflare Pages 后台配置 `ADMIN_USERNAME` 与 `ADMIN_PASSWORD` 环境变量进行覆盖。
- **签名算法**：采用 V8 原生 `crypto.subtle` 的 HMAC-SHA256（HS256）算法签发，**零外部 npm 依赖，零安全漏洞引入**。
- **凭据保存**：签发的 JWT Token 有效期为 7 天，加密保存在浏览器安全隔离区（`localStorage.getItem('lmod_admin_token')`）。
- **中间件守卫**：`functions/api/v1/admin/_middleware.js` 统一拦截所有管理接口，Token 无效或过期直接熔断拦截。

---

## 三、四大核心管理中台模块详解

### 1. 玩家数据分析大盘 (Telemetry & Analytics Dashboard)
- **核心 KPI 监控**：实时展示全网总 PV、独立访客 UV、今日新增访客、搜索行为总次数、代码复制总次数、一键批处理包（`.bat`）下载总量。
- **高频搜索热词 Top 10**：按命中频次与占比排序，洞悉玩家最迫切的单机修改需求（如“2077 四季宝”、“法环 无敌”、“黑神话 避坑”）。
- **最受欢迎指令榜 Top 10**：展示被点击 `copy_code` 最多的控制台语法代码与对应游戏。
- **全息日志流水**：支持按事件类型（`copy_code`, `download_bat`, `search_query`, `ai_ask`, `view_game`）实时翻页筛选 D1 原始流水日志。
- **玩家报错与反馈审核流**：对玩家提交的代码失效、版本变动或 Mod 补充反馈进行在线审核，支持一键置为“已解决”、“已采纳”或“待查”，并同步记录管理员操作流水。

### 2. 游戏与指令知识库动态运维 (Game & Vault CMS)
- **100 款游戏全局状态监控**：按 Rank 排序，一览所有游戏的 L-MOD 验证基准补丁、Steam 最新补丁、指令收录条数与兼容指示灯（🟢 完美适配 / 🟡 部分失效 / 🔴 高危熔断）。
- **在线编辑与一键保存**：无需手写 SQL，直接在线修改游戏版本、避坑短评、详细防坏档指南与控制台快捷键，毫秒级同步至 D1 数据库。
- **指令集专属运维抽屉**：
  - 支持按游戏查看名下所有控制台指令；
  - 支持新增指令（中文名、英文名、可执行语法、分类、语法类型 `cet_lua`/`engine_console`/`ue_console`、热门置顶）；
  - 支持在线修改已有指令或带防护删除指令。

### 3. 老L·AI 顾问与 Skills 机器人编排台 (AI Copilot Studio)
- **系统提示词 (System Prompt) 热更新**：在线调优老L·AI 的人设风格与知识召回边界，提供“资深单机老炮”、“极客严谨工程师”、“新手友好导师”三种一键预设。
- **推理超参数调节**：
  - 语气风格 (Tone)
  - 知识召回相似度阈值 (Recall Threshold: 0.3 ~ 0.95)
  - 单次最大注入指令数 (Max Context Commands: 2 ~ 15)
- **AI Skills 扩展能力开关 (Agentic Tools)**：
  - 🛡️ **智能代码查重 (`code_dedup`)**：防止生成相似重复代码
  - ⚡ **语法自检修复 (`syntax_validator`)**：校验引号、变量缺失并自动补齐
  - 🔍 **Steam 补丁语义对比 (`steam_diff`)**：自动比对版本偏差并标明兼容性
  - 💾 **坏档预防拦截 (`save_backup_guard`)**：涉及大改存档的高危指令强制前置红色警示
- **大模型路由与环境状态**：支持在线查看与切换主选推理模型（Google Gemini 2.5 Flash / DeepSeek-Chat / Gemini 1.5 Pro）。
- **交互式技能沙盒测试器 (Interactive Playground)**：站长可在后台输入玩家测试提问（如“2077 怎么刷钱”），一键查看上下文召回命中数、坏档守卫拦截结果与模拟回复。

### 4. Steam 补丁巡检哨兵机器人中台 (Patch Radar Sentinel Control)
- **巡检任务看板**：实时汇总当前 100 款游戏的绿/黄/红状态分布，并展示近 24 小时内的自动化巡检审计存证（`patch_radar_logs`）。
- **手动触发巡检**：提供“立即巡检”交互终端，可随时一键全网抓取 Steam 官方 Patch API 与 Build ID，与 L-MOD 基准进行差分比对。
- **全网紧急熔断跑马灯广播 (Emergency Circuit-Breaker)**：
  - 当某款大作突发破坏性更新时，站长可在后台一键开启紧急广播；
  - 支持设置预警等级（🔴 红色高危熔断 / 🟡 黄色更新注意 / ℹ️ 蓝色公告）、关联特定游戏与自定义警示文案；
  - 开启后，玩家端顶部将立即弹出呼吸高亮跑马灯，防范大规模玩家坏档。

---

## 四、安全与生产部署指引 (Production Deployment)

### 1. Cloudflare 环境变量配置
在 Cloudflare Pages 项目后台的 **Settings -> Environment variables** 中配置以下变量：
- `ADMIN_USERNAME`：站长登录账号（默认: `admin`）
- `ADMIN_PASSWORD`：站长登录密码（默认: `lmod2026!`）
- `ADMIN_JWT_SECRET`：Web Crypto JWT 签名私钥（若未指定则自动回退使用 `ADMIN_PASSWORD`）

### 2. 数据库迁移脚本应用 (D1)
若在本地或线上初始化，执行：
```bash
# 本地 SQLite 测试
sqlite3 database/lmod_vault.db < database/migration_v3_admin.sql

# 线上 Cloudflare D1 部署
npx wrangler d1 execute lmod-vault-db --file=database/migration_v3_admin.sql
```

### 3. 本地与线上自动化测试
运行中台集成测试脚本：
```bash
node scripts/test_admin_api.js
```
全部 18 项鉴权与业务接口校验将自动通过。
