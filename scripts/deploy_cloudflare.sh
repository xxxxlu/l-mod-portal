#!/usr/bin/env bash
# ==============================================================================
# scripts/deploy_cloudflare.sh
# L-MOD Vault: Cloudflare Pages 全球免费直连部署脚本 (通道 A 首选方案)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

echo "======================================================================"
echo "⚡ [L-MOD Vault] 启动 Cloudflare Pages 全球直连秒级发布流水线"
echo "======================================================================"

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

# 1. 运行生产构建门禁
echo "==> 步骤 1/3: 触发生产静态构建与门禁检测..."
"$PYTHON_BIN" "$SCRIPT_DIR/build_prod.py"

# 2. 检查 Wrangler CLI
echo "==> 步骤 2/3: 探测 Cloudflare Pages 部署客户端..."
if command -v wrangler &> /dev/null; then
    WRANGLER_CMD="wrangler"
elif command -v npx &> /dev/null; then
    WRANGLER_CMD="npx wrangler"
else
    echo "❌ 未检测到 wrangler 或 npx 命令！请先安装 Node.js 环境或运行: npm install -g wrangler"
    exit 1
fi

PROJECT_NAME="lmod-vault"

# 3. 部署到 Cloudflare Pages
echo "==> 步骤 3/3: 正在通过 $WRANGLER_CMD 将 public 目录直推全球 CDN..."
echo "目标项目: $PROJECT_NAME"
echo ""

$WRANGLER_CMD pages deploy public --project-name="$PROJECT_NAME" --commit-dirty=true "$@"

echo ""
echo "======================================================================"
echo "🎉 Cloudflare Pages 部署指令执行完成！"
echo "🌐 默认访问域名: https://$PROJECT_NAME.pages.dev"
echo "💡 提示: 首次推送请在浏览器完成 Cloudflare 账号授权 (npx wrangler login)"
echo "💡 自定义域名: 前往 Cloudflare Dashboard -> Workers & Pages -> $PROJECT_NAME -> Custom domains 即可秒级绑定"
echo "======================================================================"
