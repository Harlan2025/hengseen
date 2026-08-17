#!/bin/bash
# 提取 Fly.io Token 并部署

TOKEN=$(grep 'access_token:' "/c/Users/haigu/.fly/config.yml" | sed 's/access_token: //')

echo "Token extracted: ${TOKEN:0:20}..."
echo "Deploying to Fly.io..."

cd "F:/hermes/2 Mike/衡简叙约/backend"

# 设置环境变量
export FLY_API_TOKEN="$TOKEN"

# 列出已有应用
echo ""
echo "Existing apps:"
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" apps list

# 创建应用
echo ""
echo "Creating app hengseen-backend..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" apps create --name=hengseen-backend

# 设置环境变量
echo ""
echo "Setting secrets..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" secrets set SUPABASE_SERVICE_KEY=***
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" secrets set JWT_SECRET_KEY=***
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" secrets set AI_PROVIDER=agnes
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" secrets set AI_AGNES_API_KEY=***

# 部署
echo ""
echo "Deploying..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" deploy

echo ""
echo "✅ Deployment complete!"
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" status
