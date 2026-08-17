# 衡简叙约 - Cloudflare Workers 部署指南

## 方案对比

| 方案 | 优点 | 缺点 |
|------|------|------|
| **Cloudflare Workers** | 免费额度大，边缘计算快 | 需要适配代码，不支持所有库 |
| **Railway** | 完全兼容，部署简单 | 需要付费（$5/月起） |
| **Render** | 免费额度 | 冷启动慢 |

## Cloudflare Workers 部署

### 前置条件
- 已登录 Wrangler CLI: `wrangler login`
- 已创建 Cloudflare 账号

### 步骤

```bash
# 1. 进入后端目录
cd backend

# 2. 创建/更新 Workers 项目
wrangler pages project create hengseen-backend --production-branch=main

# 3. 构建并部署
wrangler deploy
```

### 环境变量配置

在 Cloudflare Dashboard:
1. 进入 Workers & Pages
2. 选择 hengseen-backend
3. 点击 "Settings" → "Variables"
4. 添加以下变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| SUPABASE_URL | Supabase URL | https://rtmldrysnwzbkgiihnuc.supabase.co |
| SUPABASE_SERVICE_KEY | 服务密钥 | *** |
| JWT_SECRET_KEY | JWT 密钥 | *** |
| AI_PROVIDER | AI 提供商 | agnes |
| AI_AGNES_API_KEY | Agnes API 密钥 | *** |
| DOMAIN | 域名 | https://api.hengseen.com |

### 验证部署

```bash
# 测试健康检查
curl https://hengseen-backend.your-account.workers.dev/health

# 测试登录
curl -X POST https://hengseen-backend.your-account.workers.dev/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'
```

## Railway 部署（推荐）

如果 Cloudflare Workers 有问题，推荐使用 Railway：

```bash
# 1. 访问 https://railway.app
# 2. 新建项目 → Deploy from GitHub repo
# 3. 添加环境变量
# 4. 等待部署完成
```

环境变量清单：
```
SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
SUPABASE_SERVICE_KEY=***
JWT_SECRET_KEY=***
AI_PROVIDER=agnes
AI_AGNES_API_KEY=***
DOMAIN=https://hengseen.com
```

## 更新前端 API 地址

部署成功后，更新前端环境变量：

```bash
# frontend/.env.production
VITE_API_URL=https://hengseen-backend.your-account.workers.dev/api/v1
```

重新构建并部署前端：
```bash
cd frontend
npm run build
wrangler pages deploy dist --project-name=hengseen
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 导入错误 | 检查 requirements.txt 中的依赖 |
| 环境变量未生效 | 在 Dashboard 中检查变量设置 |
| CORS 错误 | 检查 CORS 配置中间件 |
| 数据库连接失败 | 检查 SUPABASE_URL 和 SERVICE_KEY |
