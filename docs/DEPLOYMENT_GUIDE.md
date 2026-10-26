# 🚀 L-MOD Vault 生产环境一键部署与全球 CDN 极速上线操作手册 (5-Minute Deployment Guide)

> **项目代号**：L-MOD Vault (单机游戏纯净智库与避坑雷达)  
> **架构定位**：工业级纯静态 Jamstack / 零后端 / 全球 Anycast CDN 极速分发 / 微信防拦截生态网关  
> **生产就绪度**：Grade A+ (100/100 全项门禁合格)

---

## 📑 目录索引
1. [生产发布架构与核心优势](#1-生产发布架构与核心优势)
2. [通道 A (首选推荐)：Cloudflare Pages 全球免费直连部署](#2-通道-a-首选推荐cloudflare-pages-全球免费直连部署)
3. [通道 B：GitHub Actions 自动化 CI/CD 部署流水线](#3-通道-bgithub-actions-自动化-cicd-部署流水线)
4. [CDN 缓存规范、SPA 路由与安全头配置详解](#4-cdn-缓存规范spa-路由与安全头配置详解)
5. [微信内置浏览器防拦截安全网关 (WeChat Safe Gateway)](#5-微信内置浏览器防拦截安全网关-wechat-safe-gateway)
6. [自定义个性化域名绑定与全球免费 SSL/TLS 配置](#6-自定义个性化域名绑定与全球免费-ssltls-配置)
7. [生产健康度巡检与自动化门禁自测](#7-生产健康度巡检与自动化门禁自测)

---

## 1. 生产发布架构与核心优势

`L-MOD Vault` 采用了现代高可用 Web 架构中极致的**纯静态离线全息包 + 边缘 CDN 方案 (Zero-Server Architecture)**：

```
                    ┌────────────────────────────────────────┐
                    │       全球玩家 / 社交矩阵引流流量       │
                    └───────────────────┬────────────────────┘
                                        │
                         [DNS Anycast 智能就近解析]
                                        │
           ┌────────────────────────────┴───────────────────────────┐
           ▼                                                        ▼
┌─────────────────────────────┐                         ┌─────────────────────────────┐
│   微信内置浏览器生态 (Mobile)  │                         │ 外部浏览器 / PC / 客户端     │
│   触发 WeChat Safe Gateway  │                         │ 完整体验全功能与极速直接下载 │
│   指引【在浏览器打开】       │                         └──────────────┬──────────────┘
└──────────┬──────────────────┘                                        │
           │                                                           │
           └────────────────────────────┬──────────────────────────────┘
                                        ▼
                      ┌───────────────────────────────────┐
                      │    Cloudflare Pages 全球边缘 CDN   │
                      │  (300+ 边缘节点 / DDoS 40Tbps 防护)│
                      └─────────────────┬─────────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 │                                             │
      [长缓存 Cache-Control]                        [协商缓存 max-age=0]
   • public/data.js (1.6MB 数据库)               • public/index.html (主站)
   • public/avatar.jpg (高清头像)                • public/radar.html (避坑雷达)
   • public/favicon.svg (品牌标)                  • public/_redirects (SPA 路由)
   • public/social_distribution (35张原图)
```

### 核心工业级优势：
1. **零服务器成本 (Zero Server Cost)**：无需购买与维护任何云服务器 (ECS / CVM)，完全依托 Cloudflare Pages 与 GitHub Pages 免费无限流量配额；
2. **极速首屏与高并发防护**：全网 300+ 边缘 POP 节点秒级就近命中，天然免疫 CC/DDoS 流量洪峰；
3. **零假链接与纯净体验**：FLiNG 官方免翻镜像直链 + Nexus Mods 精选前置框架，免除外部恶意广告弹窗；
4. **微信生态高转化**：内置轻量防红与浏览器跳转指引条，避免微信无备案拦截与下载阻断。

---

## 2. 通道 A (首选推荐)：Cloudflare Pages 全球免费直连部署

Cloudflare Pages 是目前全球最快、对中国大陆直连优化最佳的免费静态托管平台。

### 方式 1：本地终端一键直推 (推荐，耗时 < 30 秒)
在项目根目录下，直接执行我们准备好的发布脚本：

```bash
# 1. 一键触发静态构建门禁与 Cloudflare 直推
./scripts/deploy.sh cf
```

**底层执行流程**：
1. 自动执行 `python3 scripts/build_prod.py`，核验静态资产、注入 `_headers` 与 `_redirects`；
2. 自动探测 `wrangler` CLI（支持全局安装或通过 `npx wrangler` 免安装调用）；
3. 执行直推发布指令：
   ```bash
   npx wrangler pages deploy public --project-name=lmod-vault --commit-dirty=true
   ```
4. 控制台将即刻输出公网测试链接（如 `https://lmod-vault.pages.dev`）。

> 💡 **初次使用说明**：若本机未登录 Cloudflare，终端会自动拉起浏览器授权窗口，点击 `Allow` 即可完成账号授权。

---

### 方式 2：GitHub 仓库关联合并自动发布 (Git-Connected Continuous Delivery)
若将代码托管至 GitHub 仓库，可设置每次推送代码自动部署：

1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)；
2. 依次进入 **Workers & Pages** -> **Create application** -> **Pages** -> **Connect to Git**；
3. 选择关联的 `l-mod-portal` 仓库；
4. 配置构建预设 (Build Settings)：
   - **Framework preset (框架预设)**: `None`
   - **Build command (构建命令)**: `python3 scripts/build_prod.py` (亦可留空)
   - **Build output directory (构建输出目录)**: `public`
5. 点击 **Save and Deploy**，30 秒内即可全球自动上线！后续只要往主分支 push 代码，Cloudflare 都会自动完成打包发布。

---

## 3. 通道 B：GitHub Actions 自动化 CI/CD 部署流水线

项目已内置 `.github/workflows/deploy.yml`，为 GitHub 原生 Pages 提供全自动持续集成：

### 1. 开启 GitHub Pages 权限
1. 打开 GitHub 仓库首页，点击 **Settings** -> **Pages**；
2. 在 **Build and deployment** 下方的 **Source** 下拉菜单中，选择：
   👉 **`GitHub Actions`**。

### 2. CI/CD 流水线作业步骤：
每次 push 代码至 `main` 或 `master` 分支，流水线将自动运行：
- **步骤 1：国际化与多语言对称性核验** (`python3 scripts/verify_i18n_dual_pages.py`)；
- **步骤 2：生产打包优化与规范头注入** (`python3 scripts/build_prod.py`)；
- **步骤 3：部署健康度与 14 款旗舰大作深度巡检** (`python3 scripts/verify_deployment.py`)；
- **步骤 4：无缝上传并部署至 GitHub Pages**。

---

## 4. CDN 缓存规范、SPA 路由与安全头配置详解

在 `public/` 目录下，发布构建流水线已自动生成符合工业级规范的边缘配置文件：

### 1. `public/_headers` (高性能缓存与现代安全策略)
```http
# HTML 页面采用协商缓存，确保用户随时加载到最新版代码与补丁数据
/*.html
  Cache-Control: public, max-age=0, must-revalidate
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

# 核心全息数据库与静态图片采用最高级不可变长缓存 (1年)，全球 CDN 极速秒开
/data.js
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
  X-Content-Type-Options: nosniff

/*.jpg
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *

# 全局安全响应头
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Access-Control-Allow-Origin: *
```

### 2. `public/_redirects` (SPA Hash 路由兜底与友好短链)
```http
/radar          /radar.html       200
/index          /index.html       200
/home           /index.html       200
/*              /index.html       200
```

### 3. `public/.nojekyll`
防止 GitHub Pages 内部的 Jekyll 静态解析引擎误过滤以 `_` 开头的目录或文件（如 `_headers`、`_redirects`）。

---

## 5. 微信内置浏览器防拦截安全网关 (WeChat Safe Gateway)

为解决国内微信环境拦截未备案域名以及限制大文件直链下载的痛点，项目实现了智能防拦截安全网关组件：

```
+-----------------------------------------------------------------------------------------+
| 💡【防拦截指引】为保证修改器与 Mod 正常下载，建议点击右上角 [···] 选择 [在浏览器打开]     ↗  ✕  |
+-----------------------------------------------------------------------------------------+
```

### 交互机制与技术实现：
1. **智能内核探测**：
   ```javascript
   const ua = (navigator.userAgent || '').toLowerCase();
   const isWeChat = ua.includes('micromessenger') || window.location.search.includes('wechat=1');
   ```
2. **优雅浮动展现**：
   - 当微信用户访问时，顶部以平滑动画滑出带有琥珀金磨砂质感的安全网关提示条；
   - 提示条绝对不遮挡页面下方正常的内容阅读、控制台代码复制与避坑雷达浏览；
3. **单会话免打扰 (Session Storage)**：
   - 点击右侧 `[✕]` 关闭按钮后，系统将在当前会话中记入 `sessionStorage.setItem('lmod_wx_dismissed', '1')`，用户在本次访问内浏览多款游戏均不会被二次打扰；
4. **微信分享底包缩略图**：
   - 页面顶层挂载不可见的 300×300 `avatar.jpg` 缩略图标签，配合标准 Open Graph Meta，确保微信群或朋友圈分享时自动抓取精美品牌卡片封面。

### 微信环境模拟测试方法：
无需打开真机微信，只需在浏览器地址栏附加测试参数即可验证：
- 访问：`http://localhost:18088/?wechat=1` 或 `https://lmod-vault.pages.dev/?wechat=1`
- 避坑雷达测试：`http://localhost:18088/radar.html?wechat=1`

---

## 6. 自定义个性化域名绑定与全球免费 SSL/TLS 配置

Cloudflare Pages 支持为项目免费绑定自己的顶级域名，并由 Cloudflare 自动签发免费的 ECC/RSA 双证书：

1. 进入 [Cloudflare 控制台](https://dash.cloudflare.com/)；
2. 点击 **Workers & Pages** -> 选择 **`lmod-vault`** 项目；
3. 切换至 **Custom domains** 标签页，点击 **Set up a custom domain**；
4. 输入你的域名（例如 `vault.yourdomain.com` 或 `lmod.cc`）；
5. **DNS 自动对齐**：
   - 若域名已由 Cloudflare DNS 托管，系统会自动插入一条 CNAME 记录，状态秒级变为 `Active`；
   - 若域名在腾讯云/阿里云/万网，只需在你的 DNS 解析面板添加一条记录：
     - **记录类型**: `CNAME`
     - **主机记录**: `vault` (或 `@`)
     - **记录值**: `lmod-vault.pages.dev`
6. **SSL 加密模式推荐**：
   - 在 Cloudflare 域名主页 -> **SSL/TLS** 中选择 **Full (严格/Full)**；
   - 开启 **Always Use HTTPS**（始终使用 HTTPS）与 **Automatic HTTPS Rewrites**。

---

## 7. 生产健康度巡检与自动化门禁自测

在推送至公网前后，随时可调用内置的健康巡检调度器对生产环境进行全息健康体检：

```bash
# 1. 运行本地完整健康自检 (耗时 ~20ms)
./scripts/deploy.sh verify

# 2. 或者检测部署后的公网 URL (例如 Cloudflare Pages 或自定义域名)
python3 scripts/verify_deployment.py https://lmod-vault.pages.dev
```

### 巡检报告示例 (100 分满分制)：

```text
======================================================================
📊 L-MOD Vault 生产环境发布健康度综合诊断评级报告
======================================================================
  • 检测目标: 本地静态工程包 (public/ 生产镜像)
  • 架构模式: 纯静态 Jamstack / 零后端 / 全球 CDN 分发

  [细项健康度评分看板]
    • 核心端点与CDN规范      : 30.0 / 30 [██████████] 100.0%
    • Top14旗舰数据资产     : 40.0 / 40 [██████████] 100.0%
    • 微信安全网关防拦截       : 15.0 / 15 [██████████] 100.0%
    • SEO社交卡片与图标      : 15.0 / 15 [██████████] 100.0%

  ------------------------------------------------------------
  • 生产综合健康总分: 100.0 / 100
  • 诊断结论评级: 🏆 卓越 (GRADE A+) - 100% 具备工业级公网发布资质
======================================================================
```

---

## 🎯 总结与发布就绪清单 (Release Checklist)

| 检查项 | 状态 | 验证方法 |
|---|:---:|---|
| **全量 100 款游戏数据库与双向深链接** | 🟢 就绪 | `python3 scripts/verify_i18n_dual_pages.py` |
| **Top 14 旗舰大作修改器与 Mod 直链** | 🟢 就绪 | `python3 scripts/verify_deployment.py` |
| **Cloudflare Pages `_headers` 与 `_redirects`** | 🟢 就绪 | `public/_headers` & `public/_redirects` |
| **GitHub Pages `.nojekyll` 旁路声明** | 🟢 就绪 | `public/.nojekyll` |
| **Open Graph / Twitter Card / Favicon 规范** | 🟢 就绪 | `public/index.html` & `public/radar.html` |
| **微信防拦截安全网关 (WeChat Overlay)** | 🟢 就绪 | 页面附带 `?wechat=1` 验证无侵入展示 |
| **GitHub Actions 生产流水线配置** | 🟢 就绪 | `.github/workflows/deploy.yml` |
| **一键发布调度工具** | 🟢 就绪 | `./scripts/deploy.sh` |

随时执行 `./scripts/deploy.sh cf`，即可完成全球秒级发布上线！
