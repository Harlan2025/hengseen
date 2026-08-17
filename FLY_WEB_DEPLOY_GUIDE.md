# Fly.io 网页部署指南

## 🚀 最简单的部署方式

### 步骤 1：访问 Fly.io Dashboard
```
https://fly.io/dashboard
```

### 步骤 2：创建新应用
1. 点击 **"New App"**
2. 选择 **"Connect to Git"**
3. 授权 GitHub（如果未授权）
4. 选择仓库：`haiguang85/hengseen`
5. 选择分支：`master`（或 `deploy-railway`）

### 步骤 3：配置应用
1. **App name**: `hengseen-backend`
2. **Region**: 选择最近的区域（如 Tokyo）
3. **Root directory**: `backend`
4. **Build pack**: 自动检测（Nixpacks）

### 步骤 4：设置环境变量
在 "Environment Variables" 页面添加：

| 变量名 | 值 |
|--------|-----|
| SUPABASE_URL | https://rtmldrysnwzbkgiihnuc.supabase.co |
| SUPABASE_SERVICE_KEY | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... |
| JWT_SECRET_KEY | (生成随机字符串) |
| AI_PROVIDER | agnes |
| AI_AGNES_API_KEY | sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5 |

### 步骤 5：部署
1. 点击 **"Deploy App"**
2. 等待部署完成（约 2-5 分钟）
3. 获取应用 URL：`https://hengseen-backend.fly.dev`

---

## 📝 环境变量生成

### JWT_SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## ✅ 验证部署

部署完成后：
```bash
# 测试健康检查
curl https://hengseen-backend.fly.dev/health

# 测试登录
curl -X POST https://hengseen-backend.fly.dev/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'
```

---

## 📊 更新前端 API 地址

部署成功后，编辑 `frontend/.env.production`：
```bash
VITE_API_URL=https://hengseen-backend.fly.dev/api/v1
```

重新构建并部署前端：
```bash
cd frontend
npm run build
wrangler pages deploy dist --project-name=hengseen
```
