# L-MOD Vault 游戏采掘与内容生产五步作业流水线 SOP (Pipeline SOP)

> **版本**：v3.0 (Milestone 3 工业级标准落地版)  
> **制定部门**：L-MOD Vault 数据挖掘与极客运营工程组  
> **执行口径**：每款新收录游戏从立项挖掘到上线发布全生命周期必须严格执行五步闭环，严禁跨门禁推进！

---

## 🎯 流水线全景作业看板 (Timeline & Gateways)

```mermaid
flowchart LR
    subgraph T4 ["T-4: 技术采掘"]
        A1["四级精准检索"] --> A2["八大系统维度对账"]
        A2 --> A3["零假代码核验"]
    end

    subgraph T3 ["T-3: 门禁质检"]
        B1["validate_game.py 校验"] --> B2["audit_game_data.py 校验"]
        B2 --> B3["双 [PASS] 强制门禁"]
    end

    subgraph T2 ["T-2: 视觉出图"]
        C1["游戏数据"] --> C2["generate_social_matrix.py"]
        C2 --> C3["1080x1440 5联图高清导出"]
    end

    subgraph T1 ["T-1: 矩阵发布"]
        D1["小红书/B站黄金时段"] --> D2["SEO关键词布局"]
        D2 --> D3["发布"]
    end

    subgraph T0 ["T+0: 社群沉淀"]
        E1["玩家反馈"] --> E2["更新资料"]
        E2 --> E3["补丁变动雷达监控"]
    end

    T4 ==> T3 ==> T2 ==> T1 ==> T0
```

---

## 步骤一：技术采掘 (T-4 节点 · 深度反编译与全息对账)

### 1.1 核心目标
建立对目标游戏引擎与版本底层机理的绝对认知，通过权威四级检索挖掘全部可用调试接口，落实 8 大系统维度，彻底杜绝通用模板化假指令与占位符。

### 1.2 四级精准检索工作流 (4-Tier Retrieval)
1. **Tier 1 (官方/开发者拆包数据源)**：
   - 优先查阅官方/社区逆向 Wiki（如 UESP、The Vault Fallout Wiki、Fandom 魂系数据库、RedModding、ParadoxWikis）；
   - 获取内部原生 FormID、Lua 函数签名、Papyrus 脚本名与事件标志位。
2. **Tier 2 (专有底层框架与 GitHub 核心库)**：
   - 查阅各引擎前置官方仓库（UE4SS、Cyber Engine Tweaks、SKSE64、F4SE、ModEngine2、REFramework、BepInEx）；
   - 确认当前官方最新补丁是否引发偏移量失效，锁定对应兼容框架版本。
3. **Tier 3 (Nexus Mods 权威专区分析)**：
   - 按照 **Downloads** 与 **Endorsements** 进行全周期与 30 天倒排；
   - 提炼排名前 10 的前置必备补丁（如 Engine Fixes、Crash Logger、SkyUI），杜绝推荐年久失修弃坑 Mod。
4. **Tier 4 (社区痛点排查与死循环 Bug 梳理)**：
   - 检索 Reddit `r/skyrimmods`、`r/eldenring` 与 Steam 讨论区高频求助贴；
   - 归纳 3~5 个因原版任务触发器损坏导致的死循环坏档卡关点，提取对应 `setstage` 或 Fact 代码。

### 1.3 八大系统维度硬性对账清单 (Checklist)
每款游戏入库必须 100% 覆盖以下八大维度：
- [ ] **维度 1：核心生存与状态锁死** (无敌模式、锁血不死、无限法力/精力、全局慢动作识破)；
- [ ] **维度 2：货币、负重、技能成长与洗点** (货币注入、背包负重解限、技能满级、免材料重铸)；
- [ ] **维度 3：官方最新大型 DLC 专属机制** (如黄金树幽影庇护点数、往日之影遗物点数、远港聚落)；
- [ ] **维度 4：全套传奇/不朽毕业神装** (全追忆武器、16大魔神器、X-01动力装甲、专属 Hex ID)；
- [ ] **维度 5：专属特色机制** (骨灰/战灰、传奇词条附魔、义体过载、龙吼铭文)；
- [ ] **维度 6：恶性死循环任务急救与 NPC 救赎** (任务强制跳转 stage、误杀 NPC 绝对赎罪复活)；
- [ ] **维度 7：专属建造/坐骑/特权直装** (聚落建造空间无限解除、炉火建材直装、灵马复活)；
- [ ] **维度 8：场景探索、全地图地标与摄影运镜** (全图赐福/地标一秒点亮、开发者房间传送、360°自由运镜)。

---

## 步骤二：门禁质检 (T-3 节点 · 强类型与语法 Linter 双重把关)

### 2.1 核心目标
数据持久化后，执行本地自动化双重门禁质检，不放过任何一个格式缺陷与语法伪指令，**必须双 `[PASS]` 方可流转至下一步**。

### 2.2 双重门禁执行标准
在本地终端执行以下质检命令：

```bash
# 门禁 1：强类型 Schema 静态严苛校验
python3 scripts/validate_game.py <game_id>

# 门禁 2：引擎语法 Linter 与规模门禁
python3 scripts/audit_game_data.py <game_id>

# 或一键执行流水线全链路自检调度器
python3 scripts/pipeline_gate.py <game_id>
```

### 2.3 验收标准细则
1. **Schema 校验规范**：
   - `game_full.schema.json`、`game_command.schema.json`、`trainer_info.schema.json`、`curated_mod.schema.json` 零字段缺失；
   - 指令必须包含合规的 `id`、双语名称（`zh-CN`, `en`）、`syntax_type`、真实可执行 `code`、详细 `desc`（长度 ≥ 5 字符）、`min_version`、`framework_required`；
   - 修改器必须包含 `author`、`version`、官方 `flingtrainer.com` 直连地址、`cleanMirrorUrl` 与分类热键（不生成杀软排除命令，被拦截时只引导用户在「保护历史记录」里放行那一个文件）；
   - 精选 Mod 必须包含下载量、大小、真实作者、依赖链与清晰的分步安装步骤（不少于 2 步）。
2. **语法与规模门禁**：
   - Top 10 核心大作：分类数 ≥ 8，指令总数 ≥ 40 条；
   - Top 30 热门单机：分类数 ≥ 4，指令总数 ≥ 15 条；
   - 严禁出现 `god`, `addmoney`, `noclip` 等无对应引擎支持的通用假占位符；
   - 语法严格符合对应引擎规则（Creation 引擎 FormID/指令、FromSoftware 热键与 CT 规范、CET Lua、UE4SS GM 命令、WitcherScript 等）。

---

## 步骤三：视觉出图 (T-2 节点 · 5 联图卡片渲染)

### 3.1 核心目标
将技术采掘产出的高价值数据，转化为适合小红书/B站传播的高清视觉卡片与文案包，构建专业避坑极客视觉壁垒。

### 3.2 发布文案
`render_cards_png.py` 同时生成小红书 / B 站发布文案和运营手册，写到 `private/social_ops/`（不进仓库）。发布排期、首评话术等运营资料不放在公开仓库里。

### 3.3 自动化出图作业
```bash
# 1. 生成社交矩阵 HTML 预览页
python3 scripts/generate_social_matrix.py <game_id>

# 2. 批量渲染 1080x1440 3:4 比例高清 5 联图
python3 scripts/render_cards_png.py <game_id>
```

#### 5 联图标准结构
- **Card 1 (黄金爆款封面)**：痛点大标题 + 游戏高清名片 + 官方最新补丁实测印章 + 老L避坑人设标；
- **Card 2 (小白避坑与环境配置)**：前置框架一键配置 + 零报毒信赖交付 + PowerShell 防误杀一键白名单；
- **Card 3 (核心场景套餐 A)**：手残救星 / 战斗减负 / 剧情体验模式代码组合；
- **Card 4 (核心场景套餐 B)**：全套毕业神装 / 稀缺资源 / 恶性卡关修复代码表；
- **Card 5 (避坑雷达自取卡)**：Steam 更新提醒 + 网站入口与自取暗号。

---

## 步骤四、五：发布与社群

运营资料（发布排期、首评话术、社群规则）不放在公开仓库里。

### 5.3 补丁变动雷达监控 (Patch Radar)
- 开启 SteamDB 与 Steam 官方公告 RSS 订阅；
- 一旦监测到目标游戏推送小更新导致框架失效，立即触发 **“雷达紧急响应机制”**：
  1. 在旧笔记置顶评论更新【版本雷达声明】；
  2. 受影响的前置框架（如 F4SE、SKSE、CET）等作者发新版，网站游戏页标出「先别更新」；
  3. 不提供打包下载，资料都在网站对应游戏页。
