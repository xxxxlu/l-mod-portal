# 📡 补丁雷达巡检脚本使用说明（v2）

> 适用：`scripts/steam_patch_monitor.py` ｜ `.github/workflows/patch_radar_cron.yml` ｜ 测试 `scripts/tests/radar/`
> 规则真源：`docs/RADAR_V2_CONTRACT.md` 第 2 节。本文和契约冲突时以契约为准。

---

## 一、它做什么

每天 UTC 02:00，定时任务对**全部带 `steamAppId` 的游戏**（目前 99 款）各取两样 Steam 数据：

| 数据 | 接口 | 用途 |
|---|---|---|
| 公共分支当前 build 号和发布时间 `timeupdated` | `https://api.steamcmd.net/v1/info/<appid>` → `data.<appid>.depots.branches.public` | **判定** |
| 最新一条官方公告（标题 / 链接） | `ISteamNews/GetNewsForApp`，只读 `steam_community_announcements` | 只展示，**不参与判定** |

再加两份本地资料：

| 资料 | 位置 | 用途 |
|---|---|---|
| Mod 框架资料 | `scripts/radar_frameworks/part-*.json`（可能缺文件、缺条目） | `hooksExe`、框架名和链接、`afterUpdate` 建议 |
| 风灵月影修改器最后更新时间 | `public/trainers.json` → `games.<id>.modified` | 判断修改器是否早于当前 build |

然后按下面的规则给每款游戏定状态，写进 `public/data.js` 的 `GAMES_DATA`，生成报告 `docs/PATCH_MONITOR_LATEST.md`；
只有出现**新变红**的游戏时才开预警单或在已开的预警单下评论。

旧版那套「写死 14 款 + 拿公告标题里的版本号比基线」已经删掉：博德之门 3 出个 Hotfix #36 就判红、每天追加评论，就是那套规则造成的。

---

## 二、判定规则

`RECENT_DAYS = 14`，`buildAge = 现在 − Steam timeupdated`。按优先级从上往下，命中即停：

| 优先级 | 条件 | `compatibilityStatus` | `radarReason` | `radarStatusText` |
|---|---|---|---|---|
| 1 | `buildAge ≤ 14 天` 且框架资料 `hooksExe == true` | `red` | `recent-update-hooks` | `🔴 刚更新 · <框架名> 待适配，先别更新` |
| 2 | `buildAge ≤ 14 天`（没有框架资料，或 `hooksExe` 为 false / null） | `yellow` | `recent-update` | `🟡 刚更新 · Mod/修改器可能要等适配` |
| 3 | 有修改器，且修改器更新时间早于 `timeupdated` 超过 1 天 | `yellow` | `trainer-behind` | `🟡 修改器早于当前游戏版本` |
| 4 | 其余 | `green` | `quiet` | `🟢 近 14 天无更新` |

- 修改器的 `modified` 是站点本地时间、不带时区，脚本按 UTC 看，所以留了 1 天容差。
- **没取到 Steam 数据**：任何一个请求失败（超时、HTTP 错误、返回格式不对，公告接口失败也算），
  这款游戏的雷达字段**一个都不动**（`steamLastChecked` 也不动），报告里列在「本次未取到」。不会因为接口抽风把状态翻掉。
- **非 Steam 游戏**（`steamAppId` 为 0 或缺失，目前只有 `alan-wake-2`）：不巡检，不写字段。
- 请求之间至少隔 0.5 秒（默认 0.6 秒）；超时、429、5xx 会隔 3 秒重试一次，再失败就按「没取到」处理。99 款大约 200 次请求、2～3 分钟。

### 新变红（决定要不要开单）

这次是 `red`，并且满足任意一条：上次不是 `red`；或者上次的 `steamBuildId` 和这次不一样。
已经红着、build 也没变的，不算新变红，不会每天评论。

---

## 三、写回 `public/data.js` 的字段

只改 `GAMES_DATA` 段；`TRANSLATIONS_DATA` 等其它部分一个字节都不动；`verifiedPatch` 和修改器字段不碰。

| 字段 | 说明 |
|---|---|
| `compatibilityStatus` | `red` / `yellow` / `green` |
| `radarReason` | `recent-update-hooks` / `recent-update` / `trainer-behind` / `quiet`（雷达页按它出 8 种语言文案） |
| `radarStatusText` | 上表的四句简体中文 |
| `steamBuildId` | 字符串 |
| `steamBuildUpdatedAt` | Steam 当前 build 的发布时间，ISO 8601 UTC，带 `Z` |
| `steamLastChecked` | 这次巡检时间，UTC，带 `Z` |
| `radarFramework` | `{ name, url }`，来自框架资料；没有就是 `null` |
| `latestSteamPatch` | 最新官方公告标题；这款游戏没有官方公告时删掉这个字段 |
| `latestSteamPatchUrl` | 最新公告链接；没有就用 `https://store.steampowered.com/news/app/<appid>` |
| `radarSummary` / `radarRiskTitle` | 简体中文，只写事实（build 日期、build 号、框架名、修改器日期） |
| `radarRiskDesc` | 优先用框架资料的 `afterUpdate["zh-CN"]`，没有就用通用的一句 |
| `emergencyAlert` | `{ "zh-CN", "en" }`，**只在 `red` 和 `recent-update` 时写**，其余状态删掉 |

文案里不出现「实测」「完美兼容」「老L团队」——没人测过的事不写（测试里有检查）。

---

## 四、框架资料（`scripts/radar_frameworks/part-*.json`）

格式见契约第 4 节。脚本把所有 `part-*.json` 按编号合起来；**缺目录、缺文件、缺条目都照常跑**，缺资料的游戏最多亮黄、不亮红。

格式校验：

- **整条跳过**（报告「🧩 框架资料 → ❌ 跳过」里列出）：缺字段；`id` 不是非空字符串；`rank` 不是整数；
  `framework` 不是 `null` 也不是 `{name, url}`；`hooksExe` 不是 true / false / null；`hooksExe` 为 true 但 `framework` 为 null；
  `modSupport` 不在枚举里；`afterUpdate` 缺 `zh-CN` / `en`；`sources` 不是链接数组，或有非 null 的判断但 `sources` 为空；
  `GAMES_DATA` 里没有这个 id；id 在前面的文件里已经出现过。整份文件不是合法 JSON 或顶层不是数组时，整份跳过。
- **照用但提醒**（报告里「⚠️ 提醒」）：`afterUpdate` 中文超过 60 字或英文超过 120 字符；`checkedAt` 不是 `YYYY-MM-DD`；
  `rank` / `steamAppId` 和 `GAMES_DATA` 对不上（以 `GAMES_DATA` 为准，按 id 匹配）。

格式问题不会让任务挂掉。

---

## 五、命令行

纯标准库，零依赖。在仓库根目录跑。

```bash
# 联网巡检全部带 steamAppId 的游戏，只写报告（不改 data.js）
python3 scripts/steam_patch_monitor.py

# 联网巡检并写回 public/data.js（定时任务就是这么跑的）
python3 scripts/steam_patch_monitor.py --update-radar

# 只看一款
python3 scripts/steam_patch_monitor.py --game baldurs-gate-3
python3 scripts/steam_patch_monitor.py --appid 1086940
```

⚠️ 本地跑默认会覆盖 `docs/PATCH_MONITOR_LATEST.md`，带 `--update-radar` 还会改 `public/data.js`。
这两个文件由定时任务维护，本地试跑请用 `--output-report` 指到临时目录、不带 `--update-radar`，或者跑完 `git checkout` 还原。

| 参数 | 说明 |
|---|---|
| `--update-radar` | 写回 `public/data.js` 的 `GAMES_DATA` 段（本地有 `src/data/games_top100.json` 时写主数据并整份重建 data.js） |
| `--output-report PATH` | 报告路径，默认 `docs/PATCH_MONITOR_LATEST.md` |
| `--game ID` / `--appid N` | 只巡检一款 |
| `--offline` | 不联网；配 `--steam-snapshot` 用快照数据，否则全部算「本次未取到」 |
| `--steam-snapshot PATH` | 离线快照 JSON，格式见脚本里 `SnapshotClient` 的说明；样例 `scripts/tests/radar/fixtures/steam_snapshot.json` |
| `--save-snapshot PATH` | 把这次联网取到的数据存成快照，之后可以离线复跑（比如换一批框架资料看效果，不用再请求 Steam） |
| `--simulate-patch ID` | 演练：把这款游戏模拟成「刚更新」 |
| `--simulate-risk red\|yellow` | 演练风险，默认 `red`：当作框架挂钩 exe，必定产生一个新变红；`yellow` 只亮黄 |
| `--simulate-version TEXT` | 演练公告标题里显示的版本名 |
| `--simulate-build-id N` | 演练用的 build 号，默认按当前时间生成 |
| `--data-js` / `--frameworks-dir` / `--trainers` | 换输入文件（测试、离线演练用） |
| `--now ISO` | 把「现在」固定成某个时间（离线复现用） |
| `--timeout` / `--interval` | 单个请求超时（默认 10 秒）/ 请求间隔（默认 0.6 秒，不小于 0.5） |

旧参数 `--all` 还认，但现在默认就是全部。

### 离线演练（不联网、不碰真实文件）

```bash
F=scripts/tests/radar/fixtures
cp $F/data_min.js /tmp/radar_data.js
python3 scripts/steam_patch_monitor.py --offline --steam-snapshot $F/steam_snapshot.json \
  --frameworks-dir $F/frameworks --trainers $F/trainers.json \
  --data-js /tmp/radar_data.js --output-report /tmp/radar_report.md \
  --now 2026-11-19T00:00:00Z --update-radar
```

---

## 六、报告（`docs/PATCH_MONITOR_LATEST.md`）

报告同时是预警单的正文。开头有一行给工作流读的标记：

```html
<!-- radar-new-red: 1 -->
```

接着是：概览（红 / 黄 / 绿 / 本次未取到 / 新变红）、新变红名单（附一段只写事实、可直接转发的提醒）、
红灯表、黄灯表（带原因码、build 时间、修改器时间、框架）、本次未取到（带失败原因）、绿灯名单、
框架资料体检（读到哪些文件、覆盖多少款、跳过和提醒的条目）、折叠起来的全量明细。

---

## 七、定时任务（`.github/workflows/patch_radar_cron.yml`）

1. 每天 UTC 02:00（北京时间 10:00）跑 `python3 scripts/steam_patch_monitor.py --update-radar`；
2. 跑 `scripts/verify_i18n_dual_pages.py` 门禁；
3. `public/data.js` 或报告有变化就提交推送，并派发一次 `deploy.yml`；
4. **`check_risk` 只读报告里的 `<!-- radar-new-red: N -->`**：`N > 0` 才开单（已有未关闭的 `radar-alert` 单就在下面评论），
   `N = 0` 什么都不做。读不到这一行按 0 处理并在日志里给警告。

### 手动演练（workflow_dispatch）

Actions → Steam Patch Sentinel Cron → Run workflow，填 `simulate_game`（如 `cyberpunk-2077`）：

- 照常联网巡检全部游戏，但把这款模拟成刚更新；`simulate_risk = red` 时必定产生一个新变红；
- 报告写到运行器临时目录，**不带 `--update-radar`**：`public/data.js` 和 `docs/` 都不变，所以不会提交推送、不会派发部署；
- `check_risk` → 开单 / 评论这一段照常走，预警单正文开头会写明「本次是演练」。

---

## 八、测试

```bash
python3 -m unittest discover -s scripts/tests/radar -v
```

覆盖：四种状态和边界（正好 14 天、修改器 1 天容差、优先级）、接口失败保持原值（build 接口和公告接口各一种）、
新变红判定、`emergencyAlert` 的写入和清理、框架资料缺目录 / 只有部分文件 / 坏文件 / 坏条目 / 重复 id / 未知 id、
请求间隔与重试、离线端到端（含 `GAMES_DATA` 之外一个字节不动）、演练产生新变红、工作流 `check_risk` 那段 shell。
假数据都在 `scripts/tests/radar/fixtures/`，测试不联网、不改真实文件。

改完雷达脚本或工作流，再跑一遍门禁：

```bash
python3 scripts/build_prod.py
python3 scripts/verify_i18n_dual_pages.py
python3 scripts/verify_deployment.py
```
