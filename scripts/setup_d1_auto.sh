#!/usr/bin/env bash
# ==============================================================================
# scripts/setup_d1_auto.sh
# L-MOD Vault - Cloudflare D1 全球数据库极速一键自动化入库与绑定流水线
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

DB_NAME="lmod-vault-db"
PROJECT_NAME="lmod-vault"

echo "======================================================================"
echo "⚡ [L-MOD Vault] 正在启动 Cloudflare D1 全球数据库全自动化部署"
echo "======================================================================"

# 1. 查找 wrangler 或 npx
WRANGLER_BIN=""
if command -v wrangler &> /dev/null; then
    WRANGLER_BIN="wrangler"
elif command -v npx &> /dev/null; then
    WRANGLER_BIN="npx wrangler"
elif [ -x "/opt/homebrew/bin/npx" ]; then
    WRANGLER_BIN="/opt/homebrew/bin/npx wrangler"
elif [ -x "/usr/local/bin/npx" ]; then
    WRANGLER_BIN="/usr/local/bin/npx wrangler"
else
    echo "❌ 错误: 未检测到 Node.js 或 npx 命令！"
    echo "💡 提示: 请先安装 Node.js (推荐从 https://nodejs.org 下载安装)，然后重新运行此脚本。"
    exit 1
fi

echo "==> 探测到客户端: $WRANGLER_BIN"

# 2. 检查 Cloudflare 登录状态
echo "==> 步骤 1/4: 检查 Cloudflare 账号登录授权..."
if ! $WRANGLER_BIN whoami &> /dev/null; then
    echo "🔑 正在唤起浏览器授权登录（浏览器打开后只需点击【允许 / Authorize】即可）..."
    $WRANGLER_BIN login
else
    echo "✅ Cloudflare 账号已登录就绪！"
fi

# 3. 创建 Cloudflare D1 数据库
echo "==> 步骤 2/4: 正在全球 300+ 边缘机房创建 D1 分布式数据库 [$DB_NAME]..."
D1_OUTPUT=$($WRANGLER_BIN d1 create "$DB_NAME" 2>&1 || true)
echo "$D1_OUTPUT"

# 从输出中提取 database_id
DATABASE_ID=$(echo "$D1_OUTPUT" | grep -o 'database_id = "[^"]*"' | head -n 1 | cut -d'"' -f2 || true)

if [ -z "$DATABASE_ID" ]; then
    # 若数据库已存在，尝试从 d1 list 获取
    echo "ℹ️ 数据库可能已存在，正在获取现有数据库信息..."
    DATABASE_ID=$($WRANGLER_BIN d1 list --json 2>/dev/null | grep -o '"uuid":"[^"]*"' | head -n 1 | cut -d'"' -f4 || true)
fi

if [ -n "$DATABASE_ID" ]; then
    echo "✅ 获取到 D1 数据库唯一 ID: $DATABASE_ID"
    
    # 自动生成 / 更新 wrangler.toml
    echo "==> 正在自动生成 wrangler.toml 数据库绑定配置文件..."
    cat <<EOF > wrangler.toml
name = "$PROJECT_NAME"
pages_build_output_dir = "public"
compatibility_date = "2024-09-23"

[[d1_databases]]
binding = "DB"
database_name = "$DB_NAME"
database_id = "$DATABASE_ID"
EOF
    echo "✅ 已生成 wrangler.toml 配置！"
else
    echo "⚠️ 未能自动获取 database_id，请稍后在 wrangler.toml 中手动核对。"
fi

# 4. 灌入 Schema 表结构与 100 款游戏数据
echo "==> 步骤 3/4: 正在将 100 款游戏全量结构化数据灌入全球 D1 边缘节点..."
echo "   -> 执行 database/schema.sql (建表)..."
$WRANGLER_BIN d1 execute "$DB_NAME" --remote --file=database/schema.sql -y

echo "   -> 执行 database/seed_data.sql (灌入 1,093 条指令与 100 款大作)..."
$WRANGLER_BIN d1 execute "$DB_NAME" --remote --file=database/seed_data.sql -y

# 5. 一键发布部署到 Cloudflare Pages
echo "==> 步骤 4/4: 正在将最新全套代码与 Edge API 发布上线..."
$WRANGLER_BIN pages deploy public --project-name="$PROJECT_NAME" --commit-dirty=true

echo ""
echo "======================================================================"
echo "🎉 恭喜！全球分布式数据库与 L-MOD Vault 已全部部署上线成功！"
echo "🌐 线上访问地址: https://$PROJECT_NAME.pages.dev"
echo "📡 边缘数据库 API: https://$PROJECT_NAME.pages.dev/api/games"
echo "======================================================================"
