# Fly.io 一键部署脚本（使用完整路径）

#!/bin/bash
set -e

echo "======================================"
echo "衡简叙约 - Fly.io 部署脚本"
echo "======================================"

# 设置 flyctl 路径
FLY_PATH="/usr/local/bin/fly"

# 检查 flyctl
if ! command -v fly &> /dev/null; then
    if [ -f "$FLY_PATH" ]; then
        fly() { "$FLY_PATH" "$@"; }
    else
        echo "❌ flyctl 未安装"
        echo "请运行: brew install superfly/tap/flyctl"
        exit 1
    fi
fi

echo "✅ flyctl 已安装"

# 检查登录状态
echo ""
if ! fly auth status &> /dev/null; then
    echo "🔐 请登录 Fly.io"
    fly auth login
fi

echo "✅ 已登录 Fly.io"

# 进入 backend 目录
cd "$(dirname "$0")/../backend"

# 创建应用
echo ""
echo "🚀 创建 Fly 应用..."
fly launch --no-deploy

# 设置环境变量
echo ""
echo "⚙️  配置环境变量..."
fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
fly secrets set SUPABASE_SERVICE_KEY=***
fly secrets set JWT_SECRET_KEY=***
fly secrets set AI_PROVIDER=agnes
fly secrets set AI_AGNES_API_KEY=***

# 部署
echo ""
echo "📦 部署到 Fly.io..."
fly deploy

# 获取 URL
echo ""
echo "✅ 部署完成！"
echo ""
echo "应用 URL:"
fly apps open
echo ""
echo "查看日志: fly logs"
echo "管理应用: fly apps list"
