# GitHub 推送问题与解决方案

## ⚠️ 问题诊断

所有 GitHub 访问方式都失败了：
- HTTPS: `Failed to connect to github.com:443`
- SSH: `Permission denied (publickey)`
- 代理: `Could not connect to server`

**原因**: 当前网络环境限制了 GitHub 访问

---

## 📋 解决方案

### 方案 1：使用浏览器手动上传（推荐）

#### 步骤 1：打包项目
```bash
cd "F:/hermes/2 Mike/衡简叙约"

# 创建干净的压缩包（排除不需要的文件）
tar -czf hengseen-deploy.tar.gz \
  --exclude='.git' \
  --exclude='backend/venv' \
  --exclude='frontend/node_modules' \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='deploy/*.zip' \
  .
```

#### 步骤 2：上传到 GitHub
1. 打开 https://github.com/haiguang85/hengseen
2. 点击 "Add file" → "Upload files"
3. 上传 `hengseen-deploy.tar.gz`
4. 添加提交信息："Initial commit"
5. 点击 "Commit changes"

---

### 方案 2：使用 GitHub Desktop

1. 下载 GitHub Desktop: https://desktop.github.com
2. 登录你的 GitHub 账号
3. File → Add Local Repository
4. 选择 `F:/hermes/2 Mike/衡简叙约`
5. 推送分支到 GitHub

---

### 方案 3：配置代理（如果你有代理）

```bash
# HTTP 代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 或者 SOCKS5 代理
git config --global http.proxy socks5://127.0.0.1:1080
git config --global https.proxy socks5://127.0.0.1:1080

# 推送
git push -u origin deploy-railway

# 完成后清除代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

### 方案 4：使用 Gitee 镜像

如果 GitHub 持续无法访问，可以考虑：

1. 在 Gitee 创建仓库
2. 推送到 Gitee
3. Railway 支持 Gitee 仓库

```bash
git remote add gitee https://gitee.com/haiguang85/hengseen.git
git push -u gitee deploy-railway
```

---

## 📝 推送成功后

### 1. 创建 Pull Request
```
https://github.com/haiguang85/hengseen/pulls/new?compare=deploy-railway...master
```

### 2. Railway 部署
1. 访问 https://railway.app
2. New Project → Deploy from GitHub repo
3. 选择 `hengseen` 仓库
4. Root Directory: `backend`
5. 添加环境变量：
   - SUPABASE_URL
   - SUPABASE_SERVICE_KEY
   - JWT_SECRET_KEY
   - AI_PROVIDER=agnes
   - AI_AGNES_API_KEY

---

## 🔗 相关文档

- GitHub 文档: https://docs.github.com
- Railway 文档: https://docs.railway.app
- Git 代理配置: https://git-scm.com/docs/git-config
