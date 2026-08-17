# ✅ Fly.io 部署就绪

## 📊 当前状态

| 项目 | 状态 | 说明 |
|------|------|------|
| flyctl 安装 | ✅ | v0.4.83 已安装 |
| 后端配置 | ✅ | fly.toml 已创建 |
| 部署脚本 | ✅ | deploy-fly.ps1 已创建 |
| Token 认证 | ❌ | 提供的 Token 已过期 |
| GitHub 推送 | ⏳ | 需要手动上传 |

---

## 🚀 下一步：登录 Fly.io

由于提供的 Token 已过期，请使用以下任一方法：

### 方法 1：浏览器登录（推荐）

在 **PowerShell** 中运行：
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```
浏览器会打开，完成登录后自动认证。

### 方法 2：生成新 Token

1. 访问 https://fly.io/account/tokens
2. 点击 "Generate new token"
3. 设置名称和过期时间
4. 复制新 Token

然后运行：
```powershell
$env:FLY_API_TOKEN = "你的新token"
cd "F:/hermes/2 Mike/衡简叙约/backend"
fly launch --no-deploy
fly deploy
```

### 方法 3：网页部署（最简单）

1. 访问 https://fly.io/dashboard
2. 点击 "New App"
3. 选择你的 GitHub 仓库
4. 配置环境变量
5. 点击 "Deploy"

---

## 📁 已完成的配置

### Fly.io 配置文件
- `backend/fly.toml` - 应用配置
- `deploy/deploy-fly.ps1` - Windows 一键部署脚本
- `deploy/deploy-fly.sh` - Linux/Mac 脚本

### 环境变量（需要设置）
```bash
SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
SUPABASE_SERVICE_KEY=***
JWT_SECRET_KEY=***
AI_PROVIDER=agnes
AI_AGNES_API_KEY=***
```

---

## 💰 成本预估

| 项目 | 费用 |
|------|------|
| 免费额度 | 256MB RAM × 3 台 VM |
| 预计月费 | **$0** |

---

## 🔗 快速链接

- Fly.io Dashboard: https://fly.io/dashboard
- API 文档: http://localhost:8000/docs (本地)
- 前端地址: https://124223bb.hengseen.pages.dev
