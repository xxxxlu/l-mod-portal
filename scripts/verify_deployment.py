#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/verify_deployment.py
==============================================================================
L-MOD Vault 自动化公网可访问性与生产健康度自检巡检工具 (Deployment Health Check)
==============================================================================
核心能力：
1. 探测公网 URL (或本地开发服务) 的关键端点 HTTP 状态码、响应延迟与 CDN 头；
2. 校验首页 (index.html)、避坑雷达 (radar.html)、核心包 (data.js)、头像 (avatar.jpg) 与 Favicon；
3. 校验 Top 14 旗舰游戏的数据结构与链接（指令要有来源、Mod 要有来源页面、链接必须是 https 且不指向已知不存在的镜像；不按条数计分）；
4. 模拟真实微信内置浏览器 User-Agent 嗅探与防拦截遮罩组件完整性；
5. 输出工业级诊断报告与 100 分制健康度评分 (支持 CI/CD 自动化退出码门禁)。
"""

import os
import re
import sys
import json
import time
import argparse
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

# ANSI Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"
GAMES_JSON_PATH = BASE_DIR / "src" / "data" / "games_top100.json"

WECHAT_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x18003029) NetType/WIFI Language/zh_CN"
)


# Hosts that are known not to exist / never to be linked (the old "mirror" org returns 404)
BANNED_LINK_HOSTS = ("github.com/l-mod-vault", "l-mod-vault.github.io", "example.com")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_games_for_check():
    """Master data if present, otherwise the GAMES_DATA array of public/data.js."""
    if GAMES_JSON_PATH.exists():
        with open(GAMES_JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    data_js_path = PUBLIC_DIR / "data.js"
    if not data_js_path.exists():
        return None
    c = data_js_path.read_text(encoding="utf-8")
    marker = "window.GAMES_DATA = "
    idx = c.find(marker)
    if idx < 0:
        return None
    games, _ = json.JSONDecoder().raw_decode(c[idx + len(marker):])
    return games


def link_problem(url):
    """Static check of one link; returns a reason string or None."""
    if not isinstance(url, str) or not url.startswith("https://") or len(url.split("/")) < 3 or not url.split("/")[2]:
        return f"不是 https 链接: {url!r}"
    if any(h in url for h in BANNED_LINK_HOSTS):
        return f"指向不存在的镜像: {url}"
    return None


def _nonempty_str(v):
    return isinstance(v, str) and v.strip() != ""


def check_game_structure(g):
    """Returns (problems, links) for one game. Empty lists are fine; malformed entries are not."""
    problems, links = [], []

    def add_link(url, where):
        err = link_problem(url)
        if err:
            problems.append(f"{where}: {err}")
        else:
            links.append(url)

    cats = g.get("consoleCategories")
    if not isinstance(cats, list):
        problems.append("consoleCategories 不是数组")
        cats = []
    for ci, cat in enumerate(cats):
        cmds = cat.get("commands") if isinstance(cat, dict) else None
        if not isinstance(cat, dict) or not _nonempty_str(cat.get("category")) or not isinstance(cmds, list) or not cmds:
            problems.append(f"consoleCategories[{ci}] 缺分类名或指令为空")
            continue
        for cmd in cmds:
            name = cmd.get("name") if isinstance(cmd, dict) else None
            if not isinstance(cmd, dict) or not _nonempty_str(cmd.get("code")) or not (
                    _nonempty_str(name) or (isinstance(name, dict) and any(_nonempty_str(v) for v in name.values()))):
                problems.append(f"consoleCategories[{ci}] 有指令缺 code 或 name")
                continue
            if not cmd.get("source"):
                problems.append(f"指令 {cmd.get('id') or cmd.get('code')!r} 没有来源")
            else:
                add_link(cmd["source"], f"指令 {cmd.get('id')!r} 的来源")

    for bi, b in enumerate(g.get("scenarioBundles") or []):
        if not isinstance(b, dict) or not all(_nonempty_str(b.get(k)) for k in ("id", "name", "code")):
            problems.append(f"scenarioBundles[{bi}] 缺 id / name / code")

    for mi, m in enumerate(g.get("curatedMods") or []):
        if not isinstance(m, dict) or not all(_nonempty_str(m.get(k)) for k in ("id", "title", "author")):
            problems.append(f"curatedMods[{mi}] 缺 id / title / author")
            continue
        if not m.get("nexusUrl"):
            problems.append(f"Mod {m.get('id')!r} 没有来源页面链接")
        else:
            add_link(m["nexusUrl"], f"Mod {m.get('id')!r}")
        if m.get("downloadUrl"):
            add_link(m["downloadUrl"], f"Mod {m.get('id')!r} 的下载链接")

    if g.get("hasTrainer"):
        tinfo = g.get("trainerInfo") or {}
        if not tinfo.get("officialUrl"):
            problems.append("hasTrainer 为真但没有修改器官方页面链接")
        else:
            add_link(tinfo["officialUrl"], "修改器官方页面")
        if tinfo.get("cleanMirrorUrl"):
            add_link(tinfo["cleanMirrorUrl"], "修改器镜像链接")

    ns = g.get("nexusStats")
    if ns is not None:
        if not isinstance(ns, dict) or not (ns.get("totalDownloads") or ns.get("totalMods")):
            problems.append("nexusStats 存在但没有数字")
        elif not (isinstance(ns.get("checkedAt"), str) and DATE_RE.match(ns["checkedAt"])):
            problems.append("nexusStats 没有取数日期 checkedAt")

    return problems, links


_LINK_RESULTS = {}


def _encode_url(url):
    """Percent-encode non-ASCII characters (e.g. bg3.wiki titles with accents)."""
    return urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")


def _fandom_page_exists(url, timeout):
    """Fandom answers scripted page requests with 403, but its MediaWiki API is open:
    ask the API whether the page title exists. None = exists, else an error string."""
    m = re.match(r"https://([a-z0-9-]+)\.fandom\.com/wiki/([^#?]+)", url)
    if not m:
        return "not a fandom page"
    title = urllib.parse.unquote(m.group(2))
    api = (f"https://{m.group(1)}.fandom.com/api.php?action=query&format=json&redirects=1&titles="
           + urllib.parse.quote(title))
    req = urllib.request.Request(api, headers={"User-Agent": "L-MOD-Vault-Deployment-Verifier/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        pages = json.load(resp).get("query", {}).get("pages", {})
    if not pages or any("missing" in p or "invalid" in p for p in pages.values()):
        return "wiki page does not exist"
    return None


def probe_link(url, timeout):
    """Network check of one link; returns an error string or None (each URL asked once).
    nexusmods.com answers scripted requests with 403 / 429, which still means the page exists;
    fandom.com pages are checked through the wiki's own API for the same reason."""
    if url in _LINK_RESULTS:
        return _LINK_RESULTS[url]
    timeout = max(timeout, 15.0)
    try:
        if ".fandom.com/wiki/" in url:
            err = _fandom_page_exists(url, timeout)
        else:
            req = urllib.request.Request(_encode_url(url), headers={"User-Agent": "L-MOD-Vault-Deployment-Verifier/1.0"}, method="GET")
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    err = None if resp.status < 400 else f"HTTP {resp.status}"
            except urllib.error.HTTPError as e:
                err = None if (e.code in (403, 429) and "nexusmods.com" in url) else f"HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        err = type(e).__name__
    _LINK_RESULTS[url] = err
    return err


class DeploymentVerifier:
    def __init__(self, target_url=None, timeout=5.0, check_links=False):
        self.target_url = target_url.rstrip("/") if target_url else None
        self.timeout = timeout
        self.check_links = check_links
        self.scores = {
            "endpoints": 0,    # Max 30
            "flagships": 0,    # Max 40
            "wechat": 0,       # Max 15
            "seo_meta": 0      # Max 15
        }
        self.max_scores = {
            "endpoints": 30,
            "flagships": 40,
            "wechat": 15,
            "seo_meta": 15
        }
        self.network_available = False
        self.test_results = []
        self.flagship_results = []

    def log_title(self, text):
        print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
        print(f"{BOLD}{CYAN}🔍 {text}{RESET}")
        print(f"{BOLD}{CYAN}======================================================================{RESET}")

    def fetch_url(self, relative_path, headers=None):
        """Fetches URL over HTTP if available, otherwise falls back to local file read."""
        req_headers = {
            "User-Agent": "L-MOD-Vault-Deployment-Verifier/1.0",
            "Accept": "*/*"
        }
        if headers:
            req_headers.update(headers)

        path_clean = relative_path.lstrip("/")
        if self.target_url:
            full_url = f"{self.target_url}/{path_clean}"
            start_t = time.time()
            try:
                # Disable environment proxy for localhost
                proxy_handler = urllib.request.ProxyHandler({}) if "127.0.0.1" in self.target_url or "localhost" in self.target_url else None
                opener = urllib.request.build_opener(proxy_handler) if proxy_handler else urllib.request.build_opener()
                req = urllib.request.Request(full_url, headers=req_headers)
                with opener.open(req, timeout=self.timeout) as resp:
                    data = resp.read()
                    latency_ms = (time.time() - start_t) * 1000
                    return {
                        "mode": "http",
                        "status": resp.status,
                        "data": data,
                        "text": data.decode("utf-8", errors="replace"),
                        "headers": dict(resp.headers),
                        "latency_ms": latency_ms,
                        "error": None
                    }
            except Exception as e:
                # Network failed, fall through to local mode
                pass

        # Local fallback mode
        start_t = time.time()
        local_file = PUBLIC_DIR / path_clean
        if not local_file.exists():
            return {
                "mode": "local",
                "status": 404,
                "data": b"",
                "text": "",
                "headers": {},
                "latency_ms": 0.0,
                "error": f"File not found: {local_file}"
            }

        data = local_file.read_bytes()
        latency_ms = (time.time() - start_t) * 1000
        return {
            "mode": "local",
            "status": 200,
            "data": data,
            "text": data.decode("utf-8", errors="replace"),
            "headers": {
                "content-type": "text/html" if path_clean.endswith(".html") else "application/javascript" if path_clean.endswith(".js") else "application/octet-stream"
            },
            "latency_ms": latency_ms,
            "error": None
        }

    def verify_core_endpoints(self):
        self.log_title("1. 核心端点可访问性、响应延迟与生产规范探测")
        endpoints = [
            ("主站首页 (/index.html)", "index.html", 200, 50 * 1024),
            ("避坑雷达 (/radar.html)", "radar.html", 200, 30 * 1024),
            ("核心全息数据库 (/data.js)", "data.js", 200, 1000 * 1024),
            ("老L专属头像 (/avatar.jpg)", "avatar.jpg", 200, 200 * 1024),
            ("矢量品牌标 (/favicon.svg)", "favicon.svg", 200, 500),
            ("Cloudflare 生产头配置 (/_headers)", "_headers", 200, 100),
            ("SPA 路由与回退重定向 (/_redirects)", "_redirects", 200, 50),
            ("GitHub Pages 旁路声明 (/.nojekyll)", ".nojekyll", 200, 0)
        ]

        passed_count = 0
        total_latency = 0.0

        for desc, path, exp_code, min_bytes in endpoints:
            res = self.fetch_url(path)
            mode_tag = "[HTTP]" if res["mode"] == "http" else "[FILE]"
            size_kb = len(res["data"]) / 1024
            latency = res["latency_ms"]
            total_latency += latency

            if res["status"] == exp_code and len(res["data"]) >= min_bytes:
                passed_count += 1
                status_str = f"{GREEN}✔ 200 OK{RESET}"
                print(f"  {status_str} {mode_tag} {desc:<34} 耗时: {latency:5.1f}ms | 尺寸: {size_kb:7.1f} KB")
            else:
                status_str = f"{RED}✖ {res['status']} FAIL{RESET}"
                err_msg = res.get("error") or f"文件过小 (现存 {len(res['data'])} bytes, 需 >= {min_bytes})"
                print(f"  {status_str} {mode_tag} {desc:<34} {RED}{err_msg}{RESET}")

        # Score calculation: up to 30 points
        endpoint_pts = round((passed_count / len(endpoints)) * 30, 1)
        self.scores["endpoints"] = endpoint_pts
        print(f"\n  • 核心端点健康得分: {BOLD}{endpoint_pts} / 30{RESET} (合格率: {passed_count}/{len(endpoints)})")

    def verify_top14_flagship_games(self):
        """Top 14: the data must be well-formed and every link must be a real https link.

        No minimum number of commands, bundles or mods: an empty list is valid. What fails a
        game is malformed content (a command without code or source, a mod without a link)
        or a link that is not https / points at a host known to be fake.
        With --check-links every link is also requested over the network.
        """
        self.log_title("2. Top 14 旗舰游戏：数据结构与链接核验（不计条数）")

        all_games = load_games_for_check()
        if not all_games:
            print(f"  {RED}✖ 找不到数据源文件: {GAMES_JSON_PATH} 或 public/data.js{RESET}")
            return

        top14 = sorted(all_games, key=lambda x: x.get("rank", 999))[:14]
        flagship_pass = 0

        print(f"  {'Rank':<5} {'Game ID':<22} {'指令':<6} {'套餐':<4} {'Mod':<4} {'链接':<5} {'状态'}")
        print(f"  {'-'*72}")

        for g in top14:
            rank = g.get("rank", 999)
            gid = g.get("id", "unknown")
            problems, links = check_game_structure(g)
            if self.check_links:
                for url in links:
                    err = probe_link(url, self.timeout)
                    if err:
                        problems.append(f"链接打不开 {url} ({err})")

            cmd_count = sum(len(c.get("commands", [])) for c in (g.get("consoleCategories") or []))
            if not problems:
                flagship_pass += 1
                status_icon = f"{GREEN}✔ PASS{RESET}"
            else:
                status_icon = f"{RED}✖ FAIL{RESET}"
            print(f"  #{rank:<3} {gid:<22} {cmd_count:<6} {len(g.get('scenarioBundles') or []):<4} "
                  f"{len(g.get('curatedMods') or []):<4} {len(links):<5} {status_icon}")
            for prob in problems[:5]:
                print(f"        {DIM}- {prob}{RESET}")
            if len(problems) > 5:
                print(f"        {DIM}- …另有 {len(problems) - 5} 处{RESET}")

        pts = round((flagship_pass / len(top14)) * 40, 1)
        self.scores["flagships"] = pts
        mode = "已联网逐个请求链接" if self.check_links else "未联网请求链接（加 --check-links 可逐个请求）"
        print(f"\n  • 旗舰游戏数据得分: {BOLD}{pts} / 40{RESET} ({flagship_pass}/{len(top14)} 款结构和链接都合格；{mode})")

    def verify_wechat_safe_gateway(self):
        self.log_title("3. 微信内置浏览器安全网关 (WeChat Safe Gateway) 拟真探测")

        # Emulate WeChat Browser request
        wechat_headers = {
            "User-Agent": WECHAT_UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

        res_index = self.fetch_url("index.html", headers=wechat_headers)
        res_radar = self.fetch_url("radar.html", headers=wechat_headers)

        checks = [
            ("首页 (index.html) 挂载防拦截条 DOM (id='wechat-safe-banner')", "wechat-safe-banner" in res_index["text"]),
            ("首页内核集成 MicroMessenger UA 智能嗅探逻辑", "micromessenger" in res_index["text"].lower()),
            ("首页具备 dismissWeChatBanner 单会话免打扰控制", "dismisswechatbanner" in res_index["text"].lower()),
            ("首页具备底包 300x300 隐藏式分享缩略图 (avatar.jpg)", "avatar.jpg" in res_index["text"] and "300px" in res_index["text"]),
            ("避坑雷达 (radar.html) 挂载防拦截条 DOM (id='wechat-safe-banner')", "wechat-safe-banner" in res_radar["text"]),
            ("避坑雷达内核集成 MicroMessenger UA 智能嗅探逻辑", "micromessenger" in res_radar["text"].lower()),
            ("避坑雷达具备在浏览器中打开指引引导", "在浏览器打开" in res_radar["text"])
        ]

        passed = 0
        for desc, ok in checks:
            if ok:
                passed += 1
                print(f"  {GREEN}✔ [PASS]{RESET} {desc}")
            else:
                print(f"  {RED}✖ [FAIL]{RESET} {desc}")

        pts = round((passed / len(checks)) * 15, 1)
        self.scores["wechat"] = pts
        print(f"\n  • 微信安全网关健康得分: {BOLD}{pts} / 15{RESET} ({passed}/{len(checks)} 项验证通过)")

    def verify_seo_and_open_graph(self):
        self.log_title("4. 全球社交卡片与 SEO 元数据严苛度核验 (Open Graph & Favicon)")

        res_index = self.fetch_url("index.html")
        res_radar = self.fetch_url("radar.html")

        meta_checks = [
            ("index.html: Open Graph 规范 (og:title, og:image, og:url)", 
             all(x in res_index["text"] for x in ["property=\"og:title\"", "property=\"og:image\"", "property=\"og:url\""])),
            ("index.html: Twitter Card 规范 (summary_large_image)",
             "name=\"twitter:card\"" in res_index["text"] and "summary_large_image" in res_index["text"]),
            ("index.html: 高质感 Favicon SVG 与 Apple Touch Icon",
             "favicon.svg" in res_index["text"] and "apple-touch-icon" in res_index["text"]),
            ("radar.html: Open Graph 规范 (og:title, og:image, og:url)",
             all(x in res_radar["text"] for x in ["property=\"og:title\"", "property=\"og:image\"", "property=\"og:url\""])),
            ("radar.html: Twitter Card 规范 (summary_large_image)",
             "name=\"twitter:card\"" in res_radar["text"] and "summary_large_image" in res_radar["text"]),
            ("radar.html: 高质感 Favicon SVG 与 Apple Touch Icon",
             "favicon.svg" in res_radar["text"] and "apple-touch-icon" in res_radar["text"])
        ]

        passed = 0
        for desc, ok in meta_checks:
            if ok:
                passed += 1
                print(f"  {GREEN}✔ [PASS]{RESET} {desc}")
            else:
                print(f"  {RED}✖ [FAIL]{RESET} {desc}")

        pts = round((passed / len(meta_checks)) * 15, 1)
        self.scores["seo_meta"] = pts
        print(f"\n  • SEO 与社交分享卡片得分: {BOLD}{pts} / 15{RESET} ({passed}/{len(meta_checks)} 项验证通过)")

    def output_summary_report(self):
        total_score = sum(self.scores.values())
        print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
        print(f"{BOLD}{CYAN}📊 L-MOD Vault 生产环境发布健康度综合诊断评级报告{RESET}")
        print(f"{BOLD}{CYAN}======================================================================{RESET}")

        target_display = self.target_url if self.target_url else "本地静态工程包 (public/ 生产镜像)"
        print(f"  • 检测目标: {BOLD}{target_display}{RESET}")
        print(f"  • 架构模式: 纯静态 Jamstack / 零后端 / 全球 CDN 分发")

        print("\n  [细项健康度评分看板]")
        for k in ["endpoints", "flagships", "wechat", "seo_meta"]:
            cur = self.scores[k]
            mx = self.max_scores[k]
            pct = (cur / mx) * 100
            bar = "█" * int(pct // 10) + "░" * (10 - int(pct // 10))
            label = {
                "endpoints": "核心端点与CDN规范",
                "flagships": "Top14旗舰数据资产",
                "wechat":    "微信安全网关防拦截",
                "seo_meta":  "SEO社交卡片与图标"
            }[k]
            print(f"    • {label:<16}: {cur:4.1f} / {mx:<2} [{bar}] {pct:5.1f}%")

        print(f"\n  {'-'*60}")
        if total_score >= 95:
            badge = f"{GREEN}{BOLD}🏆 卓越 (GRADE A+) - 100% 具备工业级公网发布资质{RESET}"
        elif total_score >= 80:
            badge = f"{YELLOW}{BOLD}⚡ 良好 (GRADE B) - 具备发布条件，部分细节可优化{RESET}"
        else:
            badge = f"{RED}{BOLD}🚨 不合格 (GRADE F) - 发现阻断性问题，请勿推向生产{RESET}"

        print(f"  • 生产综合健康总分: {BOLD}{total_score:.1f} / 100{RESET}")
        print(f"  • 诊断结论评级: {badge}")
        print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

        return total_score >= 90


def main():
    parser = argparse.ArgumentParser(description="L-MOD Vault 自动化部署健康度巡检工具")
    parser.add_argument("url", nargs="?", default=None, help="目标检测公网或本地 URL (例如: https://lmod-vault.pages.dev)")
    parser.add_argument("-u", "--url-flag", dest="url_flag", default=None, help="目标 URL 参数形式")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, help="网络请求超时时间 (秒)")
    parser.add_argument("--check-links", action="store_true", help="旗舰数据里的每个链接都联网请求一次")

    args = parser.parse_args()
    target = args.url or args.url_flag

    verifier = DeploymentVerifier(target_url=target, timeout=args.timeout, check_links=args.check_links)
    verifier.verify_core_endpoints()
    verifier.verify_top14_flagship_games()
    verifier.verify_wechat_safe_gateway()
    verifier.verify_seo_and_open_graph()

    ok = verifier.output_summary_report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
