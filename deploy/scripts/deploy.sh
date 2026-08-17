# 一键部署脚本

#!/bin/bash
set -e

echo "======================================"
echo "衡简叙约 - 一键部署脚本"
echo "======================================"

# 参数
DEPLOY_TARGET=${1:-"railway"}

case $DEPLOY_TARGET in
  "railway")
    echo "🚀 部署到 Railway..."
    echo "请访问 https://railway.app"
    echo "New Project → Deploy from GitHub repo"
    echo "Root Directory: backend"
    echo ""
    echo "环境变量:"
    echo "  SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co"
    echo "  SUPABASE_SERVICE_KEY=***"
    echo "  JWT_SECRET_KEY=***"
    echo "  AI_PROVIDER=agnes"
    echo "  AI_AGNES_API_KEY=***"
    ;;
  "fly")
    echo "🚀 部署到 Fly.io..."
    cd backend
    fly launch --no-deploy
    fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
    fly secrets set AI_PROVIDER=agnes
    fly deploy
    ;;
  *)
    echo "用法: $0 [railway|fly]"
    echo ""
    echo "  railway - 部署到 Railway"
    echo "  fly     - 部署到 Fly.io"
    exit 1
    ;;
esac

echo ""
echo "✅ 部署完成！"