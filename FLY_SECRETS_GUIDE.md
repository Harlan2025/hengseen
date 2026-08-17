# Fly.io 环境变量设置指南

## 📍 环境变量的位置

### 方法 1：通过 App Settings（推荐）

1. **访问应用设置**
   ```
   https://fly.io/apps/hengseen-backend/settings
   ```

2. **找到环境变量区域**
   - 滚动到页面下方
   - 寻找 **"Secrets"** 或 **"Environment Variables"** 部分
   - 通常在 **"General"** 标签下

3. **添加 Secret**
   - 点击 **"Add secret"** 按钮
   - 输入 Key 和 Value
   - 点击 **"Save secrets"**

---

### 方法 2：通过 Secrets 管理页面

直接访问：
```
https://fly.io/apps/hengseen-backend/secrets
```

---

### 方法 3：通过 CLI（需要有效 Token）

如果 Web 界面找不到，可以使用命令：

```powershell
# 先登录
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login

# 然后设置 secrets
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co --app hengseen-backend
& "C:\Users\haigu\AppData\Local/flyctl\flyctl.exe" secrets set SUPABASE_SERVICE_KEY=*** --app hengseen-backend
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set JWT_SECRET_KEY=hengseen-jwt-secret-change-in-production-2024 --app hengseen-backend
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set AI_PROVIDER=agnes --app hengseen-backend
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set AI_AGNES_API_KEY=sk-lnv...5pp5 --app hengseen-backend
```

---

## 📋 需要设置的变量

| Key | Value | 说明 |
|-----|-------|------|
| `SUPABASE_URL` | `https://rtmldrysnwzbkgiihnuc.supabase.co` | Supabase 项目 URL |
| `SUPABASE_SERVICE_KEY` | (你的 Service Key) | Supabase 服务密钥 |
| `JWT_SECRET_KEY` | `hengseen-jwt-secret-change-in-production-2024` | JWT 签名密钥 |
| `AI_PROVIDER` | `agnes` | AI 提供商 |
| `AI_AGNES_API_KEY` | `sk-lnv...5pp5` | Agnes API Key |

---

## 🔍 如何找到 Supabase Service Key

1. 访问 https://supabase.com/dashboard/project/rtmldrysnwzbkgiihnuc/settings/api
2. 在 **"Project API keys"** 部分
3. 复制 **"service_role"** 密钥

---

## ⚠️ 重要提示

- Secrets 会触发自动重启
- 不需要重新部署应用
- 密钥不会出现在日志中

---

## 📸 操作截图指引

1. 打开 https://fly.io/apps/hengseen-backend
2. 左侧菜单点击 **"Settings"**
3. 找到 **"Secrets"** 部分
4. 点击 **"Manage secrets"** 或直接添加

---

**如果还是找不到，请告诉我你在页面看到了什么，我可以帮你定位！**
