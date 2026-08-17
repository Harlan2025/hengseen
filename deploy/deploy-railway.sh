# 衡简叙约 - 一键部署脚本

#!/bin/bash
set -e

echo "======================================"
echo "衡简叙约 - Railway 部署脚本"
echo "======================================"

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ git 未安装"
    exit 1
fi

# 初始化 git（如果未初始化）
if [ ! -d ".git" ]; then
    echo ""
    echo "📦 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# 添加 remote（如果未添加）
if ! git remote get-url origin &> /dev/null; then
    echo ""
    echo "❌ 请先配置 GitHub remote"
    echo ""
    echo "执行以下命令："
    echo "  git remote add origin https://github.com/YOUR_USERNAME/hengseen.git"
    echo "  git push -u origin main"
    exit 1
fi

echo "✅ Git 仓库已配置"

# 推送代码
echo ""
echo "📤 推送代码到 GitHub..."
git add .
git commit -m "Deploy to Railway" 2>/dev/null || true
git push origin main

echo "✅ 代码已推送"

echo ""
echo "======================================"
echo "🎉 部署步骤完成！"
echo "======================================"
echo ""
echo "下一步："
echo "1. 访问 https://railway.app"
echo "2. 点击 'New Project'"
echo "3. 选择 'Deploy from GitHub repo'"
echo "4. 选择 hengseen 仓库"
echo "5. 在 Settings 中添加环境变量："
echo "   - SUPABASE_URL"
echo "   - SUPABASE_SERVICE_KEY"
echo "   - JWT_SECRET_KEY"
echo "   - AI_PROVIDER=agnes"
echo "   - AI_AGNES_API_KEY"
echo ""
echo "详细指南见: deploy/RAILWAY_GUIDE.md"
echo ""
