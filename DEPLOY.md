# 衡简叙约 - 快速部署指南

## 系统架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Cloudflare    │────▶│   Railway       │────▶│   Supabase      │
│    Pages        │     │   (Backend)     │     │   (Database)    │
│   (Frontend)    │     │   :8000         │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## 一键部署

### 1. 克隆代码
```bash
git clone <your-repo-url>
cd 衡简叙约
```

### 2. 配置环境变量

#### 后端 (.env)
```bash
cd backend
cp .env.example .env
# 编辑 .env 填写配置
```

#### 前端 (.env.production)
```bash
cd ../frontend
cp .env.example .env.production
# 编辑 .env.production
```

### 3. 部署前端到 Cloudflare

```bash
# 安装 Wrangler
npm install -g wrangler

# 登录
wrangler login

# 构建并部署
cd frontend
npm install
npm run build
wrangler pages deploy dist --project-name=hengseen
```

### 4. 部署后端到 Railway

1. 访问 https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 连接你的仓库
5. 添加环境变量：
   - SUPABASE_URL
   - SUPABASE_SERVICE_KEY
   - JWT_SECRET_KEY
   - AI_PROVIDER=agnes
   - AI_AGNES_API_KEY
   - DOMAIN=https://api.hengseen.com

### 5. 配置DNS（可选）

在 Cloudflare Dashboard 添加 DNS 记录：
- A记录: henggseen.com → Pages IP
- CNAME: api.hengseen.com → Railway endpoint

## 验证部署

```bash
# 测试后端
curl https://api.hengseen.com/health

# 测试前端
open https://hengseen.com
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| CORS错误 | 检查后端 CORS 配置 |
| 401 Unauthorized | 检查 JWT_SECRET_KEY |
| 数据库连接失败 | 检查 Supabase 配置 |
| 前端构建失败 | 检查 Node.js 版本 |
