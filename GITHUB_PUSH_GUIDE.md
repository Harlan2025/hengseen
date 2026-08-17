# GitHub 推送指南 - 需要认证

## ⚠️ 问题
推送需要 GitHub 用户名/密码或 Token 认证。

---

## 方案 1：使用 Personal Access Token（推荐）

### 步骤 1：创建 GitHub Token
1. 打开 https://github.com/settings/tokens
2. 点击 **"Generate new token (classic)"**
3. 填写：
   - Note: `hengseen-deploy`
   - Expiration: `90 days`
   - 勾选 scopes: `repo` (全选)
4. 点击 **"Generate token"**
5. **复制 Token**（只显示一次！）

### 步骤 2：配置并推送
```bash
cd "F:/hermes/2 Mike/衡简叙约"

# 使用 Token 推送
git remote set-url origin https://你的Token@github.com/haiguang85/hengseen.git
git push -u origin deploy-railway

# 推送成功后清除 Token
git remote set-url origin https://github.com/haiguang85/hengseen.git
```

---

## 方案 2：手动上传（最简单）

### 步骤 1：打包项目
```powershell
cd "F:\hermes\2 Mike\衡简叙约"
Compress-Archive -Path . -DestinationPath hengseen-deploy.zip -Force
```

或排除大文件：
```bash
tar -czf hengseen-deploy.tar.gz . \
  --exclude='.git' \
  --exclude='backend/venv' \
  --exclude='frontend/node_modules' \
  --exclude='*.pyc' \
  --exclude='__pycache__'
```

### 步骤 2：上传到 GitHub
1. 打开 https://github.com/haiguang85/hengseen
2. 点击 **"Add file"** → **"Upload files"**
3. 拖拽 `hengseen-deploy.zip` 或 `.tar.gz`
4. 提交信息：`Initial commit from local`
5. 点击 **"Commit changes"**

### 步骤 3：从 ZIP 恢复 Git 仓库（可选）
```bash
# 下载 ZIP 并解压
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/haiguang85/hengseen.git
git push -u origin master
```

---

## 方案 3：使用浏览器推送（GitHub Desktop）

1. 下载 GitHub Desktop: https://desktop.github.com
2. 登录你的 GitHub 账号
3. **File** → **Add local repository**
4. 选择 `F:\hermes\2 Mike\衡简叙约`
5. 点击 **Publish repository**
6. 推送分支：`deploy-railway`

---

## 方案 4：使用 SSH（如果你有 SSH Key）

```bash
# 检查是否有 SSH key
ls ~/.ssh/id_rsa.pub 2>/dev/null || echo "No SSH key found"

# 如果有，使用 SSH 推送
git remote set-url origin git@github.com:haiguang85/hengseen.git
git push -u origin deploy-railway
```

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| Git 本地提交 | ✅ 5 commits |
| GitHub 仓库 | ✅ 已创建 |
| 远程配置 | ✅ ghfast.top 代理 |
| 认证 | ❌ 需要 Token 或手动上传 |

---

## 🔗 推送成功后

### 创建 Pull Request
```
https://github.com/haiguang85/hengseen/pulls/new?compare=deploy-railway...master
```

### Railway 部署
1. 访问 https://railway.app
2. New Project → Deploy from GitHub repo
3. 选择 `haiguang85/hengseen`
4. Root Directory: `backend`
5. 添加环境变量后部署
