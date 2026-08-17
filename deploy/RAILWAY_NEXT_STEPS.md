# 衡简叙约 - Railway 部署最后一步

## ✅ 已完成

1. **前端部署到 Cloudflare Pages**
   - 访问地址: https://124223bb.hengseen.pages.dev
   - 状态: ✅ 正常

2. **后端配置 Railway 部署文件**
   - Railway.toml 已创建
   - Git 仓库已初始化

---

## 📋 下一步：推送到 GitHub

### 1. 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名: `hengseen`
3. 设为公开 (Public)
4. 不要初始化 README
5. 点击 "Create repository"

### 2. 推送代码

在终端执行：
```bash
cd "F:/hermes/2 Mike/衡简叙约"

# 添加 remote（替换 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/hengseen.git

# 推送到 GitHub
git push -u origin main
```

### 3. 部署到 Railway

1. 访问 https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"
4. 选择 `hengseen` 仓库
5. 选择 `backend` 文件夹作为 root
6. 添加环境变量（见下方）

---

## 🔑 环境变量配置

在 Railway Dashboard → Settings → Variables 中添加：

| 变量名 | 值 |
|--------|-----|
| SUPABASE_URL | https://rtmldrysnwzbkgiihnuc.supabase.co |
| SUPABASE_SERVICE_KEY | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... |
| JWT_SECRET_KEY | 运行 `python -c "import secrets; print(secrets.token_urlsafe(32))"` 生成 |
| AI_PROVIDER | agnes |
| AI_AGNES_API_KEY | sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5 |
| AI_AGNES_BASE_URL | https://api.sapiens.ai/v1 |
| DOMAIN | https://hengseen.com |

---

## 🌐 获取 Railway URL

部署成功后，Railway 会提供 URL：
```
https://hengseen-backend-xxx.up.railway.app
```

---

## 📝 更新前端 API 地址

编辑 `frontend/.env.production`：
```bash
VITE_API_URL=https://hengseen-backend-xxx.up.railway.app/api/v1
```

重新构建并部署前端：
```bash
cd frontend
npm run build
wrangler pages deploy dist --project-name=hengseen
```
