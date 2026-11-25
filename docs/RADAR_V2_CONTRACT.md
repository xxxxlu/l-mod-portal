# 补丁雷达 v2 · 分工契约

基线分支 `feat/radar-v2`（从 main `57f9be6` 切出，本地分支，不推送）。各会话都从这个分支切自己的工作树，
只在自己的分支上本地提交，由协调人逐个看完差异再合回 `feat/radar-v2`。本文件只有协调人能改。

## 1. 为什么要改

现在的雷达有三个问题：

1. **只巡检 14 款**（脚本里写死的 `TOP_14_REGISTRY`），另外 86 款在雷达页上的红黄绿是页面按开发商名字猜的
   （比如开发商含 Bethesda 就标黄）。
2. **误报**：判定方法是拿 Steam 最新公告标题里的数字，和脚本里写死、从来没人更新过的 `baseline_version` 比，
   只要不一样就报警。所以博德之门 3 出个「Hotfix #36」就判红（36 ≠ 「Patch 7」），每天都在预警单里追加评论。
3. **写了没人做过的事**：「🟢 完美兼容实测通过」「老L团队正真机实测」，实际上没有人去测。

v2 的目标：**全部 99 款上了 Steam 的游戏都巡检；只用能核实的信号判定；文案只说事实；只在「新变红」时才发预警。**

## 2. 判定规则（雷达脚本实现，雷达页展示）

### 2.1 每款游戏的输入

| 输入 | 来源 |
|---|---|
| Steam 公共分支当前 buildid 和它的发布时间 `timeupdated` | `https://api.steamcmd.net/v1/info/<appid>` → `data.<appid>.depots.branches.public` |
| 最新一条官方公告（标题 / 链接 / 时间），**只用来展示，不参与判定** | `ISteamNews/GetNewsForApp`，同现有脚本 |
| 这款游戏的 Mod 框架资料 | `scripts/radar_frameworks/part-*.json`（第 4 节；可能缺文件或缺条目） |
| 风灵月影修改器最后更新时间 | `public/trainers.json` → `games.<id>.modified`（站点本地时间、无时区；比较时按 UTC 看，留 1 天容差） |

### 2.2 状态和原因

常量 `RECENT_DAYS = 14`。`buildAge` = 现在 − Steam `timeupdated`。

| 优先级 | 条件 | `compatibilityStatus` | `radarReason` |
|---|---|---|---|
| 1 | `buildAge ≤ 14 天` 且框架资料 `hooksExe == true` | `red` | `recent-update-hooks` |
| 2 | `buildAge ≤ 14 天`（框架资料缺失或 `hooksExe` 为 false/null） | `yellow` | `recent-update` |
| 3 | 有修改器，且修改器更新时间早于 `timeupdated` 超过 1 天 | `yellow` | `trainer-behind` |
| 4 | 其余 | `green` | `quiet` |

- **这次没拿到 Steam 数据**（接口失败 / 超时）：这款游戏的雷达字段**全部保持上次的值不动**，报告里列为「本次未取到」。不许因为接口失败把状态翻掉。
- 非 Steam 游戏（`steamAppId` 为 0 或缺失，目前只有 `alan-wake-2`）：不巡检，不写字段。

### 2.3 写回 `public/data.js` 的 `GAMES_DATA` 字段

沿用的字段：`compatibilityStatus`、`radarStatusText`、`latestSteamPatch`、`steamBuildId`、`steamLastChecked`、
`radarSummary`、`radarRiskTitle`、`radarRiskDesc`、`emergencyAlert`。新增的字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `radarReason` | `'recent-update-hooks' \| 'recent-update' \| 'trainer-behind' \| 'quiet'` | 第 2.2 节的原因码；雷达页按它出 8 种语言的文案 |
| `steamBuildUpdatedAt` | ISO 8601 UTC 字符串，带 `Z` | Steam 当前 build 的发布时间 |
| `radarFramework` | `{ name: string, url: string } \| null` | 来自框架资料；没有就是 null |
| `latestSteamPatchUrl` | string | 最新公告链接；没有就用 `https://store.steampowered.com/news/app/<appid>` |

- `steamLastChecked` 改成 UTC、带 `Z`。
- `radarStatusText`（简体中文）固定四句，**不许出现「实测」「完美兼容」「老L团队」**：
  - `quiet` → `🟢 近 14 天无更新`
  - `recent-update` → `🟡 刚更新 · Mod/修改器可能要等适配`
  - `trainer-behind` → `🟡 修改器早于当前游戏版本`
  - `recent-update-hooks` → `🔴 刚更新 · <框架名> 待适配，先别更新`
- `radarSummary` / `radarRiskTitle` / `radarRiskDesc`：简体中文。`radarRiskDesc` 优先用框架资料里的 `afterUpdate["zh-CN"]`，没有就用通用的一句。其它语言由雷达页按 `radarReason` 自己出，不读这三个字段。
- `emergencyAlert`：`{ "zh-CN": ..., "en": ... }`，只在 `red` 和 `recent-update` 时写；其余状态**删掉这个字段**（现在的代码会把旧预警留着不删）。
- `verifiedPatch` 这个字段雷达脚本不碰。

### 2.4 预警单（GitHub Issue）

只有**本次新变红**的游戏才开单或评论。新变红是指这次是 `red`，并且满足下面任意一条：上次不是 `red`；或者上次的 `steamBuildId` 和这次不一样。
脚本在 `docs/PATCH_MONITOR_LATEST.md` 里写一行 `<!-- radar-new-red: <数量> -->`，工作流的 `check_risk` 步骤改成读这一行，数量大于 0 才开单或评论。
已经红着、build 也没变的，不再每天评论。

### 2.5 巡检范围

定时任务默认巡检**全部带 `steamAppId` 的游戏**（99 款），去掉 `TOP_14_REGISTRY` 这套写死的数据。
两个接口加起来每款大约 2 次请求，请求之间要留间隔（≥0.5 秒），单个请求失败按 2.2 节「没拿到」处理，不能让整个任务挂掉。

## 3. 文件归属（每个文件只有一个主人）

| 会话 | 只能改 | 不许碰 |
|---|---|---|
| **radar-engine** | `scripts/steam_patch_monitor.py`、`.github/workflows/patch_radar_cron.yml`、`docs/STEAM_PATCH_MONITOR_GUIDE.md`；新建测试放 `scripts/tests/radar/`（含假数据） | `public/data.js` 和 `docs/PATCH_MONITOR_LATEST.md`（这两个由定时任务写，**改了也别提交**）、`scripts/radar_frameworks/part-*.json` |
| **radar-page** | `public/radar.html`（`public/radar/index.html` 由 `scripts/build_prod.py` 从它生成，跟着提交）、`src/i18n/translations.json`、`public/data.js` 里**只限** `TRANSLATIONS_DATA` 段、`public/ai_copilot.js` 里雷达状态那几句文案 | `public/data.js` 的 `GAMES_DATA` 段、雷达脚本、框架资料 |
| **radar-data-1** | 只建 `scripts/radar_frameworks/part-1.json`（排名 1–34） | 其它一切 |
| **radar-data-2** | 只建 `scripts/radar_frameworks/part-2.json`（排名 35–67） | 其它一切 |
| **radar-data-3** | 只建 `scripts/radar_frameworks/part-3.json`（排名 68–100） | 其它一切 |
| 协调人 | 本文件、合并 | — |

⚠️ `scripts/build_i18n_matrix.py` 里还存着一份旧文案，重跑会把 8 语言词条改回假的说法，**谁都别跑它**。

## 4. 框架资料格式（`scripts/radar_frameworks/part-N.json`）

每个文件是一个 JSON 数组，按 `rank` 升序，正好覆盖自己那段排名的**全部**游戏（包括没上 Steam 的）。
游戏的 id、排名、appid 以 `public/data.js` 的 `GAMES_DATA` 为准。

```json
{
  "id": "skyrim-se",
  "rank": 6,
  "steamAppId": 489830,
  "framework": { "name": "SKSE64", "url": "https://skse.silverlock.org/" },
  "hooksExe": true,
  "modSupport": "community",
  "afterUpdate": {
    "zh-CN": "游戏更新后先别急着进，等 SKSE64 和 Address Library 出对应版本再玩。",
    "en": "After a game update, wait for matching SKSE64 and Address Library builds before playing."
  },
  "sources": ["https://skse.silverlock.org/"],
  "checkedAt": "2026-11-19"
}
```

| 字段 | 含义 |
|---|---|
| `framework` | 这款游戏大多数 Mod 依赖的脚本扩展或加载器，比如 SKSE64、F4SE、Cyber Engine Tweaks / RED4ext、REFramework、BG3 Script Extender、UE4SS、ScriptHookV、SMAPI、BepInEx、MelonLoader。大部分 Mod 只是替换数据、或主要走创意工坊 / 官方工具的，填 `null` |
| `hooksExe` | 这个框架是不是按游戏 exe 的具体版本注入或挂钩，导致游戏一更新就基本必坏、要等框架作者发新版。`true` / `false`；查不实就填 `null`（脚本按 false 处理，只亮黄不亮红） |
| `modSupport` | `official`（官方 Mod 工具或内置 Mod 管理器）/ `workshop`（Steam 创意工坊）/ `community`（主要靠社区框架）/ `none`（基本没有 Mod 生态）/ `null`（查不实） |
| `afterUpdate` | 游戏更新后玩家该怎么做，一两句大白话：中文 ≤ 60 字，英文 ≤ 120 字符。没有可靠建议就填 `null` |
| `sources` | **每个非 null 的判断至少要有一个来源链接**：框架官网或仓库、N 网框架页、PCGamingWiki、开发商公告。必须是本会话真的打开看过的页面 |
| `checkedAt` | 查证日期 |

硬规则：

- 查不实就填 `null`，**不许猜，不许编版本号**。
- 带反作弊的游戏，`afterUpdate` 只写「联机模式别用 Mod/修改器」这一类提醒，**不写任何绕过方法**。
- 不写「老L团队实测」「完美兼容」这类没做过的事。

## 5. 完成标准

- **radar-engine**：
  - 用标准库 `unittest` 写测试，覆盖 2.2 节四种状态、接口失败保持原值、2.4 节「新变红」判定、`emergencyAlert` 清理、框架资料文件缺失或只有一部分时照常跑。
  - 离线用假数据跑通一遍。
  - 联网真跑一次，**不带** `--update-radar`，报告输出到临时目录，交付时贴 99 款的红 / 黄 / 绿 / 未取到数量。
  - `python3 scripts/build_prod.py`、`python3 scripts/verify_i18n_dual_pages.py`、`python3 scripts/verify_deployment.py` 全绿。
- **radar-page**：
  - 页面上不再有「实测通过」「完美兼容」「老L团队」的说法。
  - 卡片和抽屉里能看到原因、Steam 最近一次更新时间、上次巡检时间、框架名和链接；新字段缺失时（定时任务还没跑新版）照旧能显示。
  - 8 种语言都有词条，`verify_i18n_dual_pages.py` 绿。
  - 本地起静态服务器用真实 `data.js` 看一遍；新字段用浏览器控制台临时塞假数据看效果，**不提交假数据**。交付附截图。
- **radar-data-N**：
  - 文件是合法 JSON，条目数正好等于自己那段排名的游戏数。
  - 交付时给一张表：每款的框架、`hooksExe`、来源域名，以及 true / false / null 各有几款。

## 6. 红线

- 只在自己的分支本地提交；**不推送、不合并、不部署、不手动触发 Actions、不在 GitHub 上评论或开单**。
- 仓库是公开的：提交里不写真名，不放任何密钥。
- 不下载修改器或任何可执行文件。
- 提交信息结尾带 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`。

## 7. 第一轮交付后的决定（v2.1，11-19，协调人定）

以下条款覆盖前文。

1. **`trainer-behind` 只看近 90 天**：只有 `buildAge ≤ 90 天` 时才判这一条。build 更老的，修改器早一点也算 `quiet`。
   这样做是因为长期不更新的老游戏，修改器早几周发布基本不影响使用；不加这个限制，99 款里有 52 款会常亮黄灯，黄灯就失去提醒作用了。
2. **跑马灯和 `emergencyAlert` 只给红灯**：`recent-update`（黄）不写 `emergencyAlert`，雷达页的滚动预警条只放红灯。
3. **公告取不到不影响判定**：只有 Steam build 信息取不到时，才算「本次未取到」并保持原值。
   公告接口失败时照常判定，`latestSteamPatch` 和 `latestSteamPatchUrl` 保留上次的值；如果上次也没有，就用 Steam 新闻页链接。
4. **红灯说法要留余地**：Steam 的 `timeupdated` 分不出这次改没改 exe，只更新资源也会刷新。所以红灯文案改成
   `🔴 刚更新 · <框架名> 可能要等适配，先别更新`，摘要里也写「可能」，不写「已失效」。
5. **新增字段 `radarAdvice`**：类型是 `{ "zh-CN": string, "en": string } | null`，原样取框架资料里的 `afterUpdate`。
   雷达页在简体中文和繁体中文界面显示 zh-CN，其它语言显示 en；为 null 时用通用建议。`radarRiskDesc` 仍按 2.3 节写简体中文。
6. **修改器更新时间**：页面直接读 `GAMES_DATA` 里已有的 `trainerInfo.lastUpdated`，不新增字段。
7. **`hooksExe` 为 true 但 `framework` 为 null 的条目**：整条跳过，并在报告里列出（radar-engine 的做法，确认采用）。
8. **演练模式**：不改 `data.js`、不推送、不部署，只走开单流程，标题加「【演练】」（radar-engine 的做法，确认采用）。
9. **radar-page 第二轮新增归属**：`public/index.html`（雷达状态相关的写死名单和说法、「100% / 零木马」这类没做过的承诺、不再展示 `verifiedPatch`）、
   `README.md` 里讲雷达的段落、`scripts/build_i18n_matrix.py` 里的旧词条（改成和现行词条一致，防止重跑把假文案写回来）。
