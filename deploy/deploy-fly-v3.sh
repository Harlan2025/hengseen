#!/bin/bash
# Fly.io 部署脚本 v3

TOKEN=$(grep 'access_token:' "/c/Users/haigu/.fly/config.yml" | sed 's/access_token: //')

echo "======================================"
echo "衡简叙约 - Fly.io 部署 v3"
echo "======================================"
echo ""

cd "F:/hermes/2 Mike/衡简叙约/backend"

export FLY_API_TOKEN="$TOKEN"

echo "📦 开始部署到 Fly.io..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend --yes deploy 2>&1

echo ""
echo "======================================"
echo "✅ 部署完成！"
echo "======================================"
echo ""
echo "应用 URL: https://hengseen-backend.fly.dev"
echo ""
echo "查看日志: fly logs --app hengseen-backend"
