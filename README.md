# L-MOD Vault

单机游戏控制台指令、Mod 与修改器资料站，附带每天比对一次 Steam 更新时间的「补丁雷达」。

A reference site for single-player games: console commands, curated mods, trainer links, and a daily Steam patch radar. UI in 8 languages.

- 主站（Cloudflare Pages，带接口和后台）：<https://lmod-vault.pages.dev>
- 静态镜像（GitHub Pages）：<https://xxxxlu.github.io/l-mod-portal/>

## 有什么

- **游戏目录**：100 款热门单机游戏的控制台指令、精选 Mod、版本说明、避坑笔记。资料来自公开文档和社区，**没有逐条在游戏里实测**，用之前先备份存档。
- **控制台脚本 (.bat)**：纯文本，可以用记事本看全部内容；只做它显示的检查和改动。
- **修改器**：只链接风灵月影官网原版。站长可以在后台上传安装包；没上传的、或下载失败时，跳转到官网。带反作弊的联机游戏标「不支持」，本站不提供任何绕过方法。
- **补丁雷达**（`/radar`）：每天比对一次 Steam 公共分支的更新时间和修改器更新时间。只比对时间、不做实机测试，所以结论都是「可能」。规则见 [`docs/RADAR_V2_CONTRACT.md`](docs/RADAR_V2_CONTRACT.md)。
- **8 种界面语言**：简体中文、English、繁體中文、日本語、한국어、Русский、Deutsch、Español。
- **站长后台**（`/admin`）：编辑游戏资料、查看访问统计、上传修改器安装包、配置 AI 助手。

## 目录结构

```
public/                 静态站点（Cloudflare Pages / GitHub Pages 都发这个目录）
  index.html            主站
  radar.html            补丁雷达页
  admin.html            站长后台
  data.js               游戏数据快照 + 8 语言词条（从 D1 导出，接口不可用时兜底）
  radar_status.json     雷达结果
  trainers.json         风灵月影修改器清单（每天同步）
  social_distribution/  社媒卡片 PNG
functions/              Cloudflare Pages Functions（/api/v1/*、/dl/*）
database/               D1 表结构和迁移（migration_vN_*.sql，只加不删）
scripts/                数据同步、雷达巡检、构建与门禁脚本
  steam_patch_monitor.py  补丁雷达巡检
  fling_trainer_sync.py   风灵月影清单同步
  export_d1_snapshot.py   从 D1 导出 data.js 快照
  build_i18n_matrix.py    多语言词条的真源
  build_prod.py           生产构建 + 静态门禁
docs/                   开发文档
.github/workflows/      定时任务与 GitHub Pages 部署
```

## 本地运行

只看静态页面：

```bash
cd public && python3 -m http.server 8791 --bind 127.0.0.1
```

带接口和 D1（需要 Node）：

```bash
npx --yes wrangler@4.154.0 pages dev public --port 8788
```

后台需要两个环境变量，本地写在 `.dev.vars`（已在 `.gitignore` 里，不要提交）：

```
ADMIN_JWT_SECRET=<至少 32 个字符的随机串>
ADMIN_PASSWORD=<至少 10 个字符>
```

没配或不合格时后台整体返回 503。线上在 Cloudflare Pages 的 Secrets 里配置，**改完要重新部署才生效**。

## 数据从哪来

- 游戏资料的真源是 Cloudflare D1（`games.raw_json`），后台保存即生效；`public/data.js` 是导出的快照。详见 [`docs/DATABASE_GUIDE.md`](docs/DATABASE_GUIDE.md)。
- 界面词条改 `scripts/build_i18n_matrix.py` 再运行它，会同时更新 `src/i18n/translations.json` 和 `data.js` 的词条段。
- 修改器清单来自风灵月影官网的公开接口，每天同步（`.github/workflows/trainer_sync_cron.yml`，UTC 03:00）。
- 雷达数据来自 Steam 公开接口，每天巡检（`.github/workflows/patch_radar_cron.yml`，UTC 02:00）。GitHub 定时任务常有延迟。

## 部署

- **GitHub Pages**：推到 `main` 自动部署。
- **Cloudflare Pages**：手动发版，`./scripts/deploy_cloudflare.sh`。脚本只发已经推到 `origin/main` 的提交，在临时的干净工作树里构建，本地未提交的改动不会被发上去。
- 发版前跑一遍门禁：

```bash
python3 scripts/build_prod.py
python3 scripts/verify_deployment.py
```

## 文档

| 文档 | 内容 |
|---|---|
| [`docs/DATABASE_GUIDE.md`](docs/DATABASE_GUIDE.md) | D1 表结构、快照导出、备份与迁移流程 |
| [`docs/ADMIN_CONSOLE_GUIDE.md`](docs/ADMIN_CONSOLE_GUIDE.md) | 后台鉴权与功能 |
| [`docs/RADAR_V2_CONTRACT.md`](docs/RADAR_V2_CONTRACT.md) | 补丁雷达判定规则 |
| [`docs/STEAM_PATCH_MONITOR_GUIDE.md`](docs/STEAM_PATCH_MONITOR_GUIDE.md) | 巡检脚本参数与演练 |
| [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) | 部署说明 |
| [`docs/AI_INTEGRATION_GUIDE.md`](docs/AI_INTEGRATION_GUIDE.md) | AI 助手与内容脚本 |
| [`docs/PIPELINE_SOP.md`](docs/PIPELINE_SOP.md) | 游戏资料整理流程 |

## 说明

- 本站不托管游戏文件。修改器、Mod、工具的版权归原作者，链接只指向作者官网或官方发布页。
- 游戏名称、商标归各自权利人所有。
- 安全问题请按 [`SECURITY.md`](SECURITY.md) 私密报告，不要开公开 Issue。
- 本仓库暂未附带开源许可证。
