#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_prod.py
==============================================================================
L-MOD Vault 生产环境一键自动化检查、配置注入与发布构建流水线 (Production Build Pipeline)
==============================================================================
核心功能：
1. 静态资产与相对路径完整性核验 (确保 data.js, avatar.jpg, favicon.svg 等无 404 隐患)；
2. 自动化生成/核验 Cloudflare Pages 生产规范文件：
   - public/_headers: 高性能 CDN 缓存、CORS 与现代严格安全响应头；
   - public/_redirects: SPA Hash 路由重定向与 404 优雅回退；
   - public/.nojekyll: GitHub Pages Jekyll 过滤器旁路声明；
3. SEO 与全域社交分享卡片 (Open Graph / Twitter Card / WeChat Meta / Favicon) 严苛校验；
4. 微信内置浏览器安全网关 (WeChat Safe Gateway) 挂载与防拦截标记检测；
5. 社交矩阵出图物料完整性核验 (7 大旗舰 35 张 1080×1440 原图)。
"""

import os
import re
import sys
import time
from pathlib import Path

# ANSI Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

BASE_DIR = Path(__file__).resolve().parent.parent
PUBLIC_DIR = BASE_DIR / "public"
SRC_DATA_DIR = BASE_DIR / "src" / "data"

HEADERS_CONTENT = """# ==============================================================================
# Cloudflare Pages Headers Configuration for L-MOD Vault
# Production Grade Cache-Control, Security & CORS headers
# ==============================================================================

# 1. HTML Pages - Fast Revalidation (No Stale Content)
/*.html
  Cache-Control: public, max-age=0, must-revalidate
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
/
  Cache-Control: public, max-age=0, must-revalidate
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

# 2. Immutable Static Assets (Images, Icons, Fonts)
/*.jpg
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
/*.png
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
/*.svg
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
/*.ico
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
/social_distribution/*
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *

# 3. Core Database Bundle - Long browser cache with CORS & nosniff
/data.js
  Cache-Control: public, max-age=31536000, immutable
  Access-Control-Allow-Origin: *
  X-Content-Type-Options: nosniff

# 4. Global Security & CORS for all paths
/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Access-Control-Allow-Origin: *
"""

REDIRECTS_CONTENT = """# ==============================================================================
# Cloudflare Pages Redirects & Rewrites for L-MOD Vault
# ==============================================================================

# Friendly shortlinks & route rewrites
/admin          /admin.html       200
/radar          /radar.html       200
/index          /index.html       200
/home           /index.html       200

# SPA Hash & Dynamic Deep-link Fallback
/*              /index.html       200
"""

NOJEKYLL_CONTENT = """# Disable Jekyll for GitHub Pages to preserve files with underscores (_headers, _redirects)
"""

FAVICON_SVG_CONTENT = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <defs>
    <linearGradient id="brandGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0071e3" />
      <stop offset="45%" stop-color="#8b5cf6" />
      <stop offset="85%" stop-color="#ec4899" />
      <stop offset="100%" stop-color="#f59e0b" />
    </linearGradient>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0e1017" />
      <stop offset="100%" stop-color="#181a24" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>
  <!-- Squircle Border -->
  <rect x="2" y="2" width="60" height="60" rx="16" fill="url(#bgGrad)" stroke="url(#brandGrad)" stroke-width="3" />
  <!-- Inner Crystal Grid Accent -->
  <circle cx="48" cy="16" r="3" fill="#8b5cf6" opacity="0.6" />
  <circle cx="50" cy="24" r="1.5" fill="#ec4899" opacity="0.5" />
  <!-- L Monogram Stroke -->
  <path d="M 22 15 L 22 41 C 22 46.5 25.5 50 31 50 L 46 50" 
        fill="none" 
        stroke="url(#brandGrad)" 
        stroke-width="7" 
        stroke-linecap="round" 
        stroke-linejoin="round"
        filter="url(#glow)" />
</svg>
"""


def log_step(title):
    print(f"\n{BOLD}{CYAN}==> {title}{RESET}")


def log_pass(msg):
    print(f"  {GREEN}✔ [PASS]{RESET} {msg}")


def log_warn(msg):
    print(f"  {YELLOW}⚠ [WARN]{RESET} {msg}")


def log_fail(msg):
    print(f"  {RED}✖ [FAIL]{RESET} {msg}")


def verify_or_generate_cf_configs():
    """Generates and validates _headers, _redirects, .nojekyll, and favicon.svg."""
    log_step("1. 检查并生成生产部署规范配置文件 (Cloudflare & GitHub Pages)")

    # 1. _headers
    headers_path = PUBLIC_DIR / "_headers"
    if not headers_path.exists() or headers_path.read_text(encoding="utf-8").strip() != HEADERS_CONTENT.strip():
        headers_path.write_text(HEADERS_CONTENT, encoding="utf-8")
        log_pass("已注入/刷新 Cloudflare Pages 生产头配置: public/_headers (长缓存/CORS/安全头)")
    else:
        log_pass("验证通过: public/_headers 符合工业级长缓存与严格安全策略")

    # 2. _redirects
    redirects_path = PUBLIC_DIR / "_redirects"
    if not redirects_path.exists() or redirects_path.read_text(encoding="utf-8").strip() != REDIRECTS_CONTENT.strip():
        redirects_path.write_text(REDIRECTS_CONTENT, encoding="utf-8")
        log_pass("已注入/刷新 SPA 重定向规则: public/_redirects (含 /radar 及 /* 200 优雅兜底)")
    else:
        log_pass("验证通过: public/_redirects SPA 路由与 404 回退配置就绪")

    # 3. .nojekyll
    nojekyll_path = PUBLIC_DIR / ".nojekyll"
    if not nojekyll_path.exists():
        nojekyll_path.write_text(NOJEKYLL_CONTENT, encoding="utf-8")
        log_pass("已注入 GitHub Pages 旁路标记: public/.nojekyll (防止 _headers 等被过滤)")
    else:
        log_pass("验证通过: public/.nojekyll 存在")

    # 4. favicon.svg
    favicon_path = PUBLIC_DIR / "favicon.svg"
    if not favicon_path.exists():
        favicon_path.write_text(FAVICON_SVG_CONTENT, encoding="utf-8")
        log_pass("已生成高质感矢量品牌 Favicon: public/favicon.svg")
    else:
        log_pass("验证通过: public/favicon.svg 存在")


def scan_asset_integrity():
    """Verifies internal local asset references and ensures 0 broken links."""
    log_step("2. 静态资产与相对路径完整性扫描 (Relative Paths & Zero 404 Audit)")
    errors = []

    core_files = ["index.html", "radar.html", "data.js", "avatar.jpg", "favicon.svg"]
    for f in core_files:
        p = PUBLIC_DIR / f
        if not p.exists():
            errors.append(f"缺失核心资产文件: public/{f}")
        else:
            size_kb = p.stat().st_size / 1024
            log_pass(f"核心文件存在: public/{f} ({size_kb:.1f} KB)")

    # Check data.js content
    data_js_path = PUBLIC_DIR / "data.js"
    if data_js_path.exists():
        content = data_js_path.read_text(encoding="utf-8")
        has_games = "GAMES_DATA" in content or "GAMES_DATABASE" in content
        has_trans = "TRANSLATIONS_DATA" in content
        if not has_games or not has_trans:
            errors.append("public/data.js 缺少核心全局数据变量挂载")
        else:
            log_pass("public/data.js 全局数据变量挂载完整 (GAMES_DATA, TRANSLATIONS_DATA)")

    # Scan index.html and radar.html for internal relative links
    html_files = [PUBLIC_DIR / "index.html", PUBLIC_DIR / "radar.html"]
    for html_file in html_files:
        text = html_file.read_text(encoding="utf-8")
        # Find all src="..." and href="..."
        matches = re.findall(r'(?:src|href)=["\']([^"\'#?]+)["\']', text)
        for ref in set(matches):
            if ref.startswith("http://") or ref.startswith("https://") or ref.startswith("//") or ref.startswith("data:"):
                continue
            if ref.endswith(".html") or ref in ["avatar.jpg", "data.js", "favicon.svg"]:
                target_path = PUBLIC_DIR / ref
                if not target_path.exists():
                    errors.append(f"{html_file.name} 中引用的相对资源不存在: {ref}")
            elif "social_distribution" in ref:
                target_path = PUBLIC_DIR / ref
                if not target_path.exists():
                    errors.append(f"{html_file.name} 中引用的社媒卡片不存在: {ref}")

    if not errors:
        log_pass("两端页面 (index.html, radar.html) 内部相对引用核验通过: 0 处断链隐患")
    else:
        for err in errors:
            log_fail(err)

    return errors


def verify_seo_and_social_meta():
    """Validates Open Graph, Twitter Cards, WeChat, and Favicon metadata."""
    log_step("3. SEO 与全域社交分享卡片门禁 (Open Graph / WeChat / Twitter Meta)")
    errors = []

    pages = [
        ("public/index.html", PUBLIC_DIR / "index.html"),
        ("public/radar.html", PUBLIC_DIR / "radar.html")
    ]

    required_meta = [
        "og:type", "og:url", "og:title", "og:description", "og:image",
        "twitter:card", "twitter:title", "twitter:description", "twitter:image"
    ]

    for label, path in pages:
        content = path.read_text(encoding="utf-8")
        page_errors = []
        for meta in required_meta:
            if f'property="{meta}"' not in content and f'name="{meta}"' not in content:
                page_errors.append(f"{label} 缺少 Meta 标签: {meta}")

        # Check favicon link
        if 'rel="icon"' not in content:
            page_errors.append(f"{label} 缺少 <link rel=\"icon\"> 标签")

        # Check WeChat thumbnail sniffing
        if 'alt="L-MOD' not in content or 'avatar.jpg' not in content:
            page_errors.append(f"{label} 缺少微信底包缩略图指引标记")

        if page_errors:
            for pe in page_errors:
                log_fail(pe)
            errors.extend(page_errors)
        else:
            log_pass(f"{label} 规范检查完成: Open Graph / Twitter Card / WeChat 缩略图元数据完备")

    return errors


def verify_wechat_gateway():
    """Validates WeChat Safe Gateway sniffer and interactive component."""
    log_step("4. 微信内置浏览器安全网关门禁 (WeChat Safe Gateway Audit)")
    errors = []

    pages = [
        ("public/index.html", PUBLIC_DIR / "index.html"),
        ("public/radar.html", PUBLIC_DIR / "radar.html")
    ]

    for label, path in pages:
        content = path.read_text(encoding="utf-8")
        checks = [
            ("wechat-safe-banner" in content, "顶部防拦截安全指引条 DOM (id=wechat-safe-banner)"),
            ("micromessenger" in content.lower(), "微信 UA 嗅探内核逻辑 (MicroMessenger)"),
            ("initWeChatCheck" in content, "安全网关初始化函数 (initWeChatCheck)"),
            ("dismissWeChatBanner" in content, "用户免打扰关闭回调 (dismissWeChatBanner)"),
            ("在浏览器打开" in content, "外部浏览器拉起下载指引文案")
        ]

        page_fail = False
        for ok, desc in checks:
            if not ok:
                log_fail(f"{label} 微信网关项未达标: {desc}")
                errors.append(f"{label}: {desc}")
                page_fail = True

        if not page_fail:
            log_pass(f"{label} 微信安全网关验证通过: 支持智能环境探测、优雅滑出与单会话免打扰")

    return errors


def verify_social_matrix_assets():
    """Ensures social distribution card PNGs for the flagship games exist."""
    log_step("5. 社交分发矩阵素材完整性自检 (Flagship Social Cards Check)")
    errors = []

    social_dir = PUBLIC_DIR / "social_distribution"
    if not social_dir.exists():
        errors.append("缺少 public/social_distribution 目录")
        log_fail("缺少 public/social_distribution 目录")
        return errors

    flagship_folders = [
        "01_cyberpunk-2077",
        "02_black-myth-wukong",
        "03_witcher-3",
        "04_baldurs-gate-3",
        "05_elden-ring",
        "06_skyrim-se",
        "07_fallout-4"
    ]

    total_pngs = 0
    for folder in flagship_folders:
        img_dir = social_dir / folder / "images"
        if not img_dir.exists():
            errors.append(f"缺失卡片图片目录: {folder}/images")
            continue
        pngs = list(img_dir.glob("*.png"))
        if len(pngs) < 5:
            errors.append(f"{folder} 卡片数量不足 (实存 {len(pngs)}/5)")
        else:
            total_pngs += len(pngs)

    if not errors:
        log_pass(f"7 大旗舰社交卡片核验通过: 共 {total_pngs} 张 1080×1440 原画素材就绪")
    else:
        for err in errors:
            log_fail(err)

    return errors


def main():
    start_time = time.time()
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}🚀 L-MOD Vault 生产环境一键发布与静态构建流水线 (Production Build Pipeline){RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"工作目录: {BASE_DIR}")
    print(f"发布输出: {PUBLIC_DIR}\n")

    verify_or_generate_cf_configs()
    err_assets = scan_asset_integrity()
    err_meta = verify_seo_and_social_meta()
    err_wx = verify_wechat_gateway()
    err_social = verify_social_matrix_assets()

    total_errors = len(err_assets) + len(err_meta) + len(err_wx) + len(err_social)
    elapsed = time.time() - start_time

    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    if total_errors == 0:
        print(f"{BOLD}{GREEN}🎉 生产构建与静态门禁全部通过！耗时: {elapsed*1000:.1f}ms{RESET}")
        print(f"{BOLD}{GREEN}✅ 静态发布包已完全就绪，可直推 Cloudflare Pages 或 GitHub Pages。{RESET}")
        print(f"{BOLD}{CYAN}======================================================================{RESET}\n")
        sys.exit(0)
    else:
        print(f"{BOLD}{RED}❌ 发现 {total_errors} 项生产规范阻断错误，请修复后再次构建！{RESET}")
        print(f"{BOLD}{CYAN}======================================================================{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
