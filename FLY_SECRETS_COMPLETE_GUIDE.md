# 🎯 Fly.io 环境变量设置完整指南

## 方法 1：通过 Web Dashboard（最简单）

### 步骤 1：访问应用页面
```
https://fly.io/apps/hengseen-backend
```

### 步骤 2：找到 Secrets 管理
在页面左侧菜单，找到并点击：
- **"Settings"** → 滚动到 **"Secrets"** 部分
- 或者直接访问：**https://fly.io/apps/hengseen-backend/secrets**

### 步骤 3：添加 Secret
点击 **"Add secret"** 按钮，逐个添加：

| 步骤 | Key | Value |
|------|-----|-------|
| 1 | SUPABASE_URL | https://rtmldrysnwzbkgiihnuc.supabase.co |
| 2 | SUPABASE_SERVICE_KEY | (从 Supabase Dashboard 复制) |
| 3 | JWT_SECRET_KEY | hengseen-jwt-secret-change-in-production-2024 |
| 4 | AI_PROVIDER | agnes |
| 5 | AI_AGNES_API_KEY | sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5 |

### 步骤 4：保存
点击 **"Save secrets"**，应用会自动重启

---

## 方法 2：通过 Fly.io Dashboard 主页

1. 访问 https://fly.io/dashboard
2. 点击应用 **"hengseen-backend"**
3. 点击右上角 **"Settings"** 按钮
4. 在左侧菜单找到 **"Environment Variables"** 或 **"Secrets"**
5. 点击 **"Manage secrets"**
6. 添加上述环境变量

---

## 方法 3：使用 CLI（如果有有效的 Token）

### 第一步：登录 Fly.io
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

### 第二步：设置 Secrets
```powershell
# 设置环境变量
$env:FLY_API_TOKEN = "你的新Token"

# 添加 Supabase URL
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co --app hengseen-backend

# 添加其他变量...
```

---

## 获取 Supabase Service Key

1. 访问 https://supabase.com/dashboard
2. 选择项目：**rtmldrysnwzbkgiihnuc**
3. 点击左侧 **"Settings"** → **"API"**
4. 在 **"Project API keys"** 部分
5. 复制 **"service_role"** 密钥

---

## 验证配置

添加所有 Secrets 后，测试 API：

```bash
curl https://hengseen-backend.fly.dev/health
```

应该返回：
```json
{"status":"ok","mode":"production"}
```

---

## 常见问题

### Q: 找不到 "Secrets" 选项？
- 确保你有应用的访问权限
- 尝试直接访问：https://fly.io/apps/hengseen-backend/secrets

### Q: Secrets 设置后没有生效？
- 等待几秒钟让应用重启
- 检查日志：https://fly.io/apps/hengseen-backend/activity

### Q: Token 认证失败？
- 可能需要重新登录：`fly auth login`
- 或生成新 Token：https://fly.io/account/tokens

---

## 快速链接

| 页面 | URL |
|------|-----|
| 应用主页 | https://fly.io/apps/hengseen-backend |
| Secrets 管理 | https://fly.io/apps/hengseen-backend/secrets |
| 活动日志 | https://fly.io/apps/hengseen-backend/activity |
| 设置 | https://fly.io/apps/hengseen-backend/settings |

---

**按照步骤操作，应该能找到 Secrets 设置位置！如果还是找不到，请截图告诉我你看到了什么页面。**
