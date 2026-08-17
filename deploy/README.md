# 衡简叙约 V1.4 部署指南

## 目录结构

```
衡简叙约/
├── backend/                    # FastAPI 后端
│   ├── Procfile               # Railway/Render 启动配置
│   ├── Dockerfile             # Docker 构建配置
│   ├── docker-compose.yml     # 本地开发容器配置
│   ├── requirements.txt       # Python 依赖
│   ├── .env.example          # 环境变量模板
│   └── .env.production.example # 生产环境变量示例
│
├── frontend/                   # Vue 3 + TypeScript 前端
│   ├── vercel.json            # Vercel 部署配置
│   ├── netlify.toml           # Netlify 部署配置
│   ├── vite.config.ts         # Vite 构建配置（含代理）
│   ├── vite.config.prod.ts    # 生产环境构建配置
│   ├── .env.example           # 前端环境变量模板
│   └── .gitignore
│
├── deploy/                     # 部署文档
│   └── ENVIRONMENT_VARIABLES.md # 环境变量详细说明
│
└── .github/workflows/          # CI/CD 配置
    ├── ci-cd.yml              # 主 CI/CD 流程
    └── docker-build.yml       # Docker 镜像构建
```

## 快速部署

### 1. 后端部署（推荐 Railway）

#### 方式一：Railway（一键部署）
```bash
# 1. 注册 Railway 账号
# 2. 连接 GitHub 仓库
# 3. 选择 backend 目录作为服务
# 4. 在 Railway Dashboard 设置环境变量（见 deploy/ENVIRONMENT_VARIABLES.md）
# 5. Railway 会自动从 Procfile 读取启动命令
```

#### 方式二：Render
```bash
# 1. 注册 Render 账号
# 2. 创建 Web Service
# 3. 选择后端仓库，设置以下配置：
#    - Build Command: pip install -r backend/requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 4. 添加环境变量
```

#### 方式三：Docker 部署
```bash
# 本地构建
docker build -t hengseen-backend ./backend

# 运行
docker run -p 8000:8000 --env-file .env hengseen-backend
```

### 2. 前端部署（推荐 Vercel）

#### 方式一：Vercel（一键部署）
```bash
# 1. 注册 Vercel 账号
# 2. 导入 GitHub 仓库
# 3. 设置环境变量（Settings → Environment Variables）：
#    - VITE_API_URL=https://api.hengseen.com/api/v1
#    - VITE_APP_NAME=衡简叙约
# 4. Vercel 会自动识别 vercel.json 配置
# 5. 部署完成后获取 https://xxx.vercel.app
```

#### 方式二：Netlify
```bash
# 1. 注册 Netlify 账号
# 2. 导入 GitHub 仓库
# 3. 设置构建命令：npm run build
# 4. 设置发布目录：dist
# 5. 添加环境变量
```

### 3. 数据库配置（Supabase）

```sql
-- 已在 Supabase 项目 rtmldrysnwzbkgiihnuc
-- 执行以下 SQL 文件：
-- 1. backend/schema_complete.sql
-- 2. backend/rls_policies.sql
-- 3. backend/fix_agreements_rls.sql
```

## 环境变量配置

### 后端环境变量（必需）
| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| SUPABASE_URL | Supabase 项目 URL | https://rtmldrysnwzbkgiihnuc.supabase.co |
| SUPABASE_ANON_KEY | 匿名密钥 | eyJ... |
| SUPABASE_SERVICE_KEY | 服务密钥 | eyJ... |
| JWT_SECRET_KEY | JWT 签名密钥 | 随机生成32+字符 |
| AI_API_KEY | DeepSeek API Key | sk-... |
| AI_BASE_URL | AI 服务地址 | https://api.deepseek.com/v1 |
| DOMAIN | 生产域名 | https://hengseen.com |

### 前端环境变量（必需）
| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| VITE_API_URL | 后端 API 地址 | https://api.hengseen.com/api/v1 |
| VITE_APP_NAME | 应用名称 | 衡简叙约 |
| VITE_SUPABASE_URL | Supabase URL | https://rtmldrysnwzbkgiihnuc.supabase.co |

**完整清单请查看**: [deploy/ENVIRONMENT_VARIABLES.md](./deploy/ENVIRONMENT_VARIABLES.md)

## CI/CD 配置

### GitHub Actions 工作流程

1. **主流程** (`.github/workflows/ci-cd.yml`)
   - 触发：push 到 main/master 分支
   - 步骤：测试 → 构建 → 部署
   - 自动部署到 Railway（后端）和 Vercel（前端）

2. **Docker 镜像构建** (`.github/workflows/docker-build.yml`)
   - 触发：release 发布或 push 到 main
   - 构建并推送 Docker 镜像到 GitHub Container Registry

### 需要配置的 GitHub Secrets

```bash
# 在仓库 Settings → Secrets and variables → Actions 中设置：
RAILWAY_API_KEY          # Railway API 密钥
RAILWAY_BACKEND_PROJECT_ID # Railway 后端项目 ID
VERCEL_TOKEN             # Vercel API Token
VERCEL_ORG_ID            # Vercel Organization ID
VERCEL_PROJECT_ID        # Vercel 前端项目 ID
SUPABASE_TEST_URL        # 测试环境 Supabase URL
SUPABASE_TEST_ANON_KEY   # 测试环境匿名密钥
SUPABASE_TEST_SERVICE_KEY # 测试环境服务密钥
```

## 部署检查清单

### 后端部署后验证
- [ ] `/health` 端点返回 `{"status": "ok"}`
- [ ] `/api/v1/auth/login` 能正常登录
- [ ] Supabase 数据库连接正常
- [ ] AI 服务能正常调用（生成合同）
- [ ] JWT 认证正常工作

### 前端部署后验证
- [ ] 页面能正常加载
- [ ] 能访问后端 API
- [ ] 登录/注册功能正常
- [ ] 合同生成流程可正常运行

### 安全加固建议
- [ ] 启用 HTTPS
- [ ] 设置合理的 CORS 策略
- [ ] 定期轮换 API Key
- [ ] 启用 Supabase RLS 策略
- [ ] 限制 API 访问频率

## 故障排查

### 常见问题

1. **后端启动失败**
   ```bash
   # 检查环境变量是否完整
   # 查看 Railway/Render 日志
   railway logs
   ```

2. **前端无法访问 API**
   ```bash
   # 检查 VITE_API_URL 是否正确
   # 确认后端 CORS 配置允许前端域名
   ```

3. **Supabase 连接失败**
   ```bash
   # 验证 SUPABASE_URL 和密钥
   # 检查 RLS 策略是否正确配置
   ```

4. **AI 服务调用失败**
   ```bash
   # 验证 AI_API_KEY 是否有效
   # 检查 AI_BASE_URL 和 AI_MODEL 配置
   ```

## 自定义域名

### 后端域名（Railway/Render）
```bash
# Railway: Settings → Domains → Add Custom Domain
# Render: Settings → Custom Domains
```

### 前端域名（Vercel/Netlify）
```bash
# Vercel: Project Settings → Domains
# Netlify: Site settings → Domain management
```

## 更新记录

- **V1.4** (2026-08): 初始部署配置，支持 Railway/Vercel 一键部署
