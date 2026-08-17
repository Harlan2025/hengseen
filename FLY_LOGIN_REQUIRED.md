# Fly.io Token 问题 - 需要重新认证

## ⚠️ 问题

之前提供的 Token 已失效。Fly.io Token 有效期通常为 7 天。

---

## ✅ 解决方案

### 方案 1：在 PowerShell 中重新登录（推荐）

**请打开一个新的 PowerShell 窗口**，运行以下命令：

```powershell
# 登录 Fly.io
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

浏览器会打开，完成登录后，告诉我"已登录"，我会继续部署。

---

### 方案 2：从 Fly.io Dashboard 获取新 Token

1. 访问 https://fly.io/account/tokens
2. 点击 **"Generate new token"**
3. 设置：
   - Name: `hengseen-deploy`
   - Expiration: `7 days`
   - Scopes: 全选
4. 复制新生成的 Token
5. 提供给我

---

### 方案 3：使用网页直接部署（最简单）

1. 访问 https://fly.io/dashboard
2. 点击 **"New App"**
3. 选择 **"Connect to Git"**
4. 授权 GitHub，选择 `haiguang85/hengseen` 仓库
5. 配置环境变量：
   - SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
   - SUPABASE_SERVICE_KEY=***
   - JWT_SECRET_KEY=(随机生成)
   - AI_PROVIDER=agnes
   - AI_AGNES_API_KEY=***
6. 点击 **"Deploy App"**

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| flyctl | ✅ 已安装 (v0.4.83) |
| 配置文件 | ✅ fly.toml 已创建 |
| Token | ❌ 已失效 |
| 下一步 | 需要重新登录 |

---

请选择一个方案，完成后告诉我！
