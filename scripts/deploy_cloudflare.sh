#!/usr/bin/env bash
# ==============================================================================
# scripts/deploy_cloudflare.sh
# 发布 Cloudflare Pages 生产环境（lmod-vault.pages.dev）。
#
# 只发「已经推到 origin/main 的提交」，并且在一个临时的干净工作树里构建：
#   - 本地没提交的改动、没推送的提交都不会被发上去；
#   - 以前这里直接发 public/ 并带 --commit-dirty=true，会把本机的设计稿、草稿一起发出去。
#
# 用法：
#   ./scripts/deploy_cloudflare.sh            # 发 origin/main 当前的提交
#   ./scripts/deploy_cloudflare.sh <commit>   # 发某个提交，但它必须已经在 origin/main 里
#
# 需要本机已登录 wrangler（npx wrangler login）。
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

PROJECT_NAME="lmod-vault"
WRANGLER_VERSION="4.154.0"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "==> 拉取 origin/main ..."
git fetch origin --quiet

REF="${1:-origin/main}"
SHA="$(git rev-parse --verify "${REF}^{commit}")"

if ! git merge-base --is-ancestor "$SHA" origin/main; then
  echo "❌ $SHA 不在 origin/main 里。生产环境只发已经推到 main 的提交，请先推送。" >&2
  exit 1
fi

TMP_PARENT="$(mktemp -d "${TMPDIR:-/tmp}/lmod-deploy.XXXXXX")"
WORKTREE="$TMP_PARENT/tree"
cleanup() {
  git -C "$ROOT_DIR" worktree remove --force "$WORKTREE" >/dev/null 2>&1 || true
  rmdir "$TMP_PARENT" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "==> 在干净工作树里检出 ${SHA:0:12} ..."
git worktree add --quiet --detach "$WORKTREE" "$SHA"
cd "$WORKTREE"

echo "==> 构建与门禁 ..."
"$PYTHON_BIN" scripts/build_prod.py
"$PYTHON_BIN" scripts/verify_deployment.py

echo "==> 发布到 Cloudflare Pages（$PROJECT_NAME / main / ${SHA:0:12}）..."
# Cloudflare 接口偶尔超时，重试是安全的（同一个提交重复发布只会多一条部署记录）
for attempt in 1 2 3; do
  if npx --yes "wrangler@${WRANGLER_VERSION}" pages deploy public \
      --project-name="$PROJECT_NAME" \
      --branch=main \
      --commit-hash="$SHA" \
      --commit-dirty=false; then
    echo "✅ 已发布 ${SHA:0:12}。核对线上文件时记得用 curl -L（.html 会跳转到无后缀地址）。"
    exit 0
  fi
  echo "⚠️ 第 $attempt 次发布失败，10 秒后重试 ..." >&2
  sleep 10
done

echo "❌ 连续 3 次发布失败。" >&2
exit 1
