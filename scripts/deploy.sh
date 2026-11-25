#!/usr/bin/env bash
# ==============================================================================
# scripts/deploy.sh
# L-MOD Vault: 工业级多平台一键自动化发布与自检入口调度脚本
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

# Detect operable Python3 binary (auto fallback for pyenv sandbox shims)
PYTHON_BIN="python3"
if ! python3 -c "import sys" 2>/dev/null; then
    for py in "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3" "/usr/bin/python3" "/usr/local/bin/python3"; do
        if [ -x "$py" ]; then
            PYTHON_BIN="$py"
            break
        fi
    done
fi

ACTION="${1:-help}"

case "$ACTION" in
    build)
        echo "🚀 正在运行生产构建与规范门禁..."
        "$PYTHON_BIN" "$SCRIPT_DIR/build_prod.py"
        ;;
    cf|cloudflare)
        shift || true
        echo "⚡ 正在调用 Cloudflare Pages 直推流水线..."
        bash "$SCRIPT_DIR/deploy_cloudflare.sh" "$@"
        ;;
    verify|check|test)
        shift || true
        echo "🔍 正在运行部署健康度巡检..."
        "$PYTHON_BIN" "$SCRIPT_DIR/verify_deployment.py" "$@"
        ;;
    all)
        echo "🌟 正在执行全套生产发布自检流水线 (Build -> Verify)..."
        "$PYTHON_BIN" "$SCRIPT_DIR/build_prod.py"
        "$PYTHON_BIN" "$SCRIPT_DIR/verify_deployment.py"
        echo ""
        echo "✅ 本地与静态门禁全部通过！输入 './scripts/deploy.sh cf' 即可推送到公网。"
        ;;
    help|*)
        echo "======================================================================"
        echo "🎮 L-MOD Vault 生产环境一键发布控制台"
        echo "======================================================================"
        echo "用法: ./scripts/deploy.sh <command> [options]"
        echo ""
        echo "可用命令:"
        echo "  build                 执行生产打包优化与静态门禁核验"
        echo "  cf | cloudflare       直推部署到 Cloudflare Pages 全球 CDN"
        echo "  verify | check [URL]  公网可访问性与 14 款旗舰大作深度健康自检"
        echo "  all                   一键运行构建检测与全量健康核验"
        echo "  help                  查看本帮助指南"
        echo "======================================================================"
        ;;
esac
