# 手动上传到 GitHub 指南

## 问题
网络连接 GitHub 失败，无法自动推送代码。

---

## 方案 1：使用浏览器上传（最简单）

### 步骤 1：打包项目

在 PowerShell 或 CMD 执行：

```powershell
cd "F:\hermes\2 Mike\衡简叙约"

# 方法 A：使用 PowerShell 压缩
Compress-Archive -Path . -DestinationPath hengseen-deploy.zip -Force

# 方法 B：使用 tar
tar -czf hengseen-deploy.tar.gz . --exclude='.git' --exclude='backend/venv' --exclude='frontend/node_modules'
```

### 步骤 2：上传到 GitHub

1. 打开 https://github.com/haiguang85/hengseen
2. 点击 **"Add file"** → **"Upload files"**
3. 拖拽或选择 `hengseen-deploy.zip`
4. 填写提交信息：`Initial commit`
5. 点击 **"Commit changes"**

---

## 方案 2：使用 GitHub Desktop

1. 下载 https://desktop.github.com
2. 登录你的 GitHub 账号
3. **File** → **Add local repository**
4. 选择文件夹：`F:\hermes\2 Mike\衡简叙约`
5. 点击 **Publish repository**
6. 推送分支到 GitHub

---

## 方案 3：配置代理后推送

如果你有 HTTP 代理（如 Clash、V2Ray）：

```bash
# 设置代理（替换为你的代理端口）
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 推送
cd "F:/hermes/2 Mike/衡简叙约"
git push -u origin deploy-railway

# 清除代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

## 方案 4：使用 Gitee 镜像

如果 GitHub 持续无法访问：

1. 注册 https://gitee.com
2. 创建仓库 `hengseen`
3. 推送代码：
   ```bash
   git remote add gitee https://gitee.com/haiguang85/hengseen.git
   git push -u gitee deploy-railway
   ```
4. Railway 支持 Gitee 仓库

---

## 上传成功后

### 1. 创建 Pull Request
访问：https://github.com/haiguang85/hengseen/pulls/new?compare=deploy-railway...master

### 2. Railway 部署
1. 访问 https://railway.app
2. New Project → Deploy from GitHub repo
3. 选择 `haiguang85/hengseen`
4. Root Directory: `backend`
5. 添加环境变量后部署

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| Git 本地提交 | ✅ 5 commits |
| GitHub 远程仓库 | ✅ 已创建 |
| 代码推送 | ❌ 网络失败 |
| 下一步 | 手动上传或配置代理 |
