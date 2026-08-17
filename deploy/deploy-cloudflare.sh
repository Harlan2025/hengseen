# 一键部署脚本

echo "======================================"
echo "衡简叙约 - Cloudflare Pages 部署"
echo "======================================"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    exit 1
fi

echo "✅ Node.js: $(node --version)"

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装"
    exit 1
fi

echo "✅ npm: $(npm --version)"

# 进入前端目录
cd "$(dirname "$0")/frontend" || exit 1

# 安装依赖
echo ""
echo "📦 安装依赖..."
npm install --legacy-peer-deps

# 构建
echo ""
echo "🔨 构建前端..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ 构建失败"
    exit 1
fi

echo "✅ 构建成功"

# 部署到Cloudflare Pages
echo ""
echo "☁️  部署到 Cloudflare Pages..."
npx wrangler pages deploy dist --project-name=hengseen --branch=main

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================"
    echo "✅ 部署成功！"
    echo "访问地址: https://hengseen.pages.dev"
    echo "======================================"
else
    echo ""
    echo "❌ 部署失败，请检查 Wrangler 配置"
    echo ""
    echo "手动部署步骤："
    echo "1. 登录 Cloudflare: wrangler login"
    echo "2. 部署: wrangler pages deploy dist --project-name=hengseen"
    exit 1
fi
