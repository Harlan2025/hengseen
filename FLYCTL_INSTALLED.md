# Fly.io 部署指南 - flyctl 已安装

## ✅ flyctl 已安装

| 项目 | 状态 |
|------|------|
| 版本 | v0.4.83 |
| 路径 | `C:\Users\haigu\AppData\Local\flyctl\flyctl.exe` |

---

## 🚀 快速部署

### 方法 1：使用完整路径（当前终端）
```powershell
# 登录 Fly.io
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login

# 进入 backend 目录
cd "F:/hermes/2 Mike/衡简叙约/backend"

# 创建应用
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" launch --no-deploy

# 设置环境变量
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set SUPABASE_SERVICE_KEY=***
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set JWT_SECRET_KEY=***
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set AI_PROVIDER=agnes
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" secrets set AI_AGNES_API_KEY=***

# 部署
"C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" deploy
```

### 方法 2：添加到 PATH（永久）
```powershell
# 添加 flyctl 到用户 PATH
[Environment]::SetEnvironmentVariable(
    "Path", 
    $env:Path + ";C:\Users\haigu\AppData\Local\flyctl", 
    "User"
)

# 重启终端后，直接使用 fly 命令
fly --version
```

---

## 📝 一键部署脚本

运行以下 PowerShell 脚本：
```powershell
cd "F:/hermes/2 Mike/衡简叙约"
.\deploy\deploy-fly.ps1
```

---

## 💰 成本

| 项目 | 费用 |
|------|------|
| 免费额度 | 256MB RAM × 3 台 VM（永久） |
| 预计月费 | **$0** |

---

## 🔗 相关链接

- Fly.io 控制台: https://fly.io/dashboard
- 应用日志: `fly logs`
- 应用列表: `fly apps list`
