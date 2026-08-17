#!/bin/bash
# Fly.io 部署脚本 - 使用 Token 环境变量

TOKEN=$(grep 'access_token:' "/c/Users/haigu/.fly/config.yml" | sed 's/access_token: //')

echo "======================================"
echo "衡简叙约 - Fly.io 部署"
echo "======================================"
echo ""
echo "Token: ${TOKEN:0:20}..."
echo ""

cd "F:/hermes/2 Mike/衡简叙约/backend"

# 设置环境变量
export FLY_API_TOKEN="$TOKEN"
export FLY_ORG="haiguang_85@126.com"

echo "📋 应用信息："
echo "   App Name: hengseen-backend"
echo "   Organization: $FLY_ORG"
echo ""

# 列出已有应用
echo "📱 检查应用..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" apps list 2>&1 || echo "无法列出应用"

# 设置环境变量
echo ""
echo "⚙️  设置环境变量..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set SUPABASE_SERVICE_KEY=*** 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set JWT_SECRET_KEY=your-secret-key-change-in-production 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set AI_PROVIDER=agnes 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set AI_AGNES_API_KEY=sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5 2>&1

# 部署
echo ""
echo "📦 开始部署..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend deploy 2>&1

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "======================================"
echo ""
echo "应用 URL: https://hengseen-backend.fly.dev"
echo ""
echo "查看日志: fly logs --app hengseen-backend"
echo "查看状态: fly status --app hengseen-backend"
