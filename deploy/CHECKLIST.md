# 部署检查清单

## 后端 (Railway)
- [ ] 创建 Railway 项目
- [ ] 配置环境变量:
  - SUPABASE_URL
  - SUPABASE_SERVICE_KEY
  - JWT_SECRET_KEY
  - AI_PROVIDER=agnes
  - AI_AGNES_API_KEY
  - DOMAIN=https://api.hengseen.com
- [ ] 部署后端
- [ ] 验证 API: https://api.hengseen.com/health

## 前端 (Cloudflare Pages)
- [ ] 创建 Cloudflare Pages 项目
- [ ] 配置环境变量:
  - VITE_API_URL=https://api.hengseen.com/api/v1
- [ ] 构建并部署
- [ ] 验证网站: https://hengseen.pages.dev

## 域名配置 (可选)
- [ ] 添加自定义域名 A 记录
- [ ] 配置 SSL 证书
