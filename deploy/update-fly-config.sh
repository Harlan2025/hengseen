#!/bin/bash
# 更新 Fly.io 应用配置

NEW_TOKEN="fm2_lJPECAAAAAAAF6HlxBBai7mclAQpZfSP+VEC4XjIwrVodHRwczovL2FwaS5mbHkuaW8vdjGWAJLOABynWB8Lk7lodHRwczovL2FwaS5mbHkuaW8vYWFhL3YxxDzMyFf7CuyNfoHPMOaS1g06Dj891uBp5sr+tnhGARhUfvA2cVB8E6p7fTwF1DtI8xXt4puMg26nB1Q596rETm07SsipNNfA7vh3EmrfOGDhY15pIFQ/taisafJp5j08rmUTVfebn2vVyKWM3HbBTMB/f3pn32B8h/m/100pc4NxMWggk5kqvTWxhufU3w2SlAORgc4Bc3mDHwWRgqdidWlsZGVyH6J3Zx8BxCDuN/W+vKxY85SSTDhgDH8gP4OkIibHlpKsmlmuFBO6Wg=="

echo "======================================"
echo "更新 Fly.io 应用配置"
echo "======================================"
echo ""

cd "F:/hermes/2 Mike/衡简叙约/backend"

# 使用新的 Token 认证
export FLY_API_TOKEN="$NEW_TOKEN"

echo "🔑 设置新 Token..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" auth whoami 2>&1

echo ""
echo "📋 更新应用配置..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set SUPABASE_SERVICE_KEY=*** 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set JWT_SECRET_KEY=your-secret-key-change-in-production 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set AI_PROVIDER=agnes 2>&1
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend secrets set AI_AGNES_API_KEY=sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5 2>&1

echo ""
echo "📦 重新部署应用..."
"C:/Users/haigu/AppData/Local/flyctl/flyctl.exe" --app hengseen-backend deploy 2>&1

echo ""
echo "======================================"
echo "✅ 配置更新完成！"
echo "======================================"
echo ""
echo "应用 URL: https://hengseen-backend.fly.dev"
