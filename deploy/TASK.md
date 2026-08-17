# 部署配置任务

## 后端部署方案
- **平台**: Railway / Render / 阿里云
- **运行时**: Python 3.11 + Uvicorn
- **数据库**: Supabase (已配置)
- **AI服务**: Agnes API

## 前端部署方案
- **平台**: Vercel (推荐) / Netlify
- **静态构建**: npm run build
- **环境变量**: NEXT_PUBLIC_API_URL
- **域名**: 自定义域名或平台域名

## CI/CD配置
- GitHub Actions自动构建
- 代码推送触发部署
- 环境变量管理

## 数据库
- Supabase项目: rtmldrysnwzbkgiihnuc
- 需要执行的SQL: schema_complete.sql, rls_policies.sql

## 环境变量清单

### 后端 (.env.production)
```
SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
SUPABASE_ANON_KEY=***
SUPABASE_SERVICE_KEY=***
JWT_SECRET_KEY=***
AI_PROVIDER=agnes
AI_AGNES_API_KEY=***
DOMAIN=https://hengseen.com
```

### 前端 (Vercel环境变量)
```
NEXT_PUBLIC_API_URL=https://api.hengseen.com
NEXT_PUBLIC_APP_NAME=衡简叙约
```

## 部署检查清单
- [ ] 后端API可访问
- [ ] 数据库连接正常
- [ ] AI服务可调用
- [ ] 前端构建成功
- [ ] 跨域配置正确
- [ ] 环境变量已配置
- [ ] 域名绑定完成
