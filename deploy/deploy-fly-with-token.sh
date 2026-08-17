#!/bin/bash
export FLY_API_TOKEN="fm2_lJPECAAAAAAAF6HlxBDaRTLHN5KiyhXWL5Ed2s5bwrVodHRwczovL2FwaS5mbHkuaW8vdjGUAJLOABynWB8Lk7lodHRwczovL2FwaS5mbHkuaW8vYWFhL3YxxDx4RqNE53VOOAB9tn94+BqZuouyJFLgLxf+XZdu13yWFySuKWGv8Nsn8A8d91k0ngx3AKig2GEv2mgV17/ETvjSAxopByn4NuAC6XPJ//Dg5AEegDrmFjNdDa5RHFS4n2AMbCssb5+LJplWAn918nlg+DCVqRmy3cORXjQLAV7k40gwBHYCIhINVmtNxcQgpajYUZpBw66kdbt3zCPra2ljtNTehMN3szHuCEmCq30=fm2_lJPETvjSAxopByn4NuAC6XPJ//Dg5AEegDrmFjNdDa5RHFS4n2AMbCssb5+LJplWAn918nlg+DCVqRmy3cORXjQLAV7k40gwBHYCIhINVmtNxcQQHeAmB9UE4bMVGAPsGFv5D8O5aHR0cHM6Ly9hcGkuZmx5LmlvL2FhYS92MZgEks5qgn22zwAAAAEmepvUF84AG22+CpHOABttvgzEEEMO4cvpMrqqoY/3By8mTaXEIEXsywugJoXE0ZfLnlNxMWFj2R+jCSDPZYXzqWQ9hKEn"

cd "F:/hermes/2 Mike/衡简叙约/backend"

echo "🔐 检查登录状态..."
fly auth whoami

echo ""
echo "🚀 创建 Fly 应用..."
fly launch --no-deploy

echo ""
echo "⚙️  设置环境变量..."
fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
fly secrets set SUPABASE_SERVICE_KEY=***
fly secrets set JWT_SECRET_KEY=***
fly secrets set AI_PROVIDER=agnes
fly secrets set AI_AGNES_API_KEY=***

echo ""
echo "📦 部署到 Fly.io..."
fly deploy

echo ""
echo "✅ 部署完成！"
echo ""
echo "应用 URL:"
fly apps open
