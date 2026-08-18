# 🔧 Fly.io 重新部署指南

## 当前状态
- ✅ GitHub 代码已推送（包含修复）
- ❌ 云端后端需要重新构建部署
- ❌ Fly.io CLI 认证失败

---

## 方法 1：通过 Activity 页面触发部署（推荐）

### 步骤：
1. 在左侧菜单点击 **"Activity"**
2. 在页面顶部找 **"Deploy"** 按钮
3. 如果看到 "Deploy from GitHub" 选项，点击它
4. 等待部署完成

---

## 方法 2：连接 GitHub 仓库

你当前在 Settings 页面，可以看到 **"Attach existing repository"** 卡片：

### 步骤：
1. 点击 **"Attach repository"** 按钮
2. 选择 GitHub 仓库：`Harlan2025/hengseen`
3. 确认连接
4. 连接成功后，GitHub push 会自动触发部署

---

## 方法 3：生成有效 Token

由于当前 Token 需要 discharge token，请尝试：

### 步骤 1：访问 Token 页面
```
https://fly.io/account/tokens
```

### 步骤 2：生成新 Token
1. 点击 **"Generate new token"**
2. **重要**：
   - Name: `hengseen-deploy`
   - Expiry: `7 days`
   - **权限**：选择 **"Full access"** 或勾选所有选项
3. 点击 **"Generate token"**
4. 复制完整 Token

### 步骤 3：重新登录
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

然后执行部署：
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy
```

---

## 方法 4：使用 Fly.io Web Terminal

### 步骤：
1. 访问应用主页：**https://fly.io/apps/hengseen-backend**
2. 在左侧菜单点击 **"Machines"**
3. 找到运行中的机器
4. 点击 **"Web shell"** 或 **"Terminal"** 按钮
5. 在终端中执行：
   ```bash
   cd /app
   fly deploy
   ```

---

## 验证当前状态

### 测试本地后端（已修复）
```bash
# 登录
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回成功

---

## 请尝试以下操作：

1. **首选**：点击左侧菜单 **"Activity"**，找 Deploy 按钮
2. **备选**：点击 **"Attach repository"** 连接 GitHub
3. **临时方案**：使用本地测试

请告诉我你在 Activity 页面看到了什么！
