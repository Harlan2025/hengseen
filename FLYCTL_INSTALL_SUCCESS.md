# ✅ flyctl 安装成功！

## 安装状态

| 项目 | 状态 |
|------|------|
| 包名 | Fly-io.flyctl |
| 版本 | 0.4.83 |
| 安装位置 | C:\Program Files\f\yctl\ |
| PATH 更新 | ✅ 已添加 |

---

## 🚀 下一步：登录并部署

### 1. 重启终端或刷新 PATH

当前终端还需要刷新环境变量：

```powershell
# 方法 1：重启终端（推荐）
# 关闭当前终端，重新打开

# 方法 2：手动刷新 PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
```

### 2. 验证安装

```powershell
fly --version
# 应该输出：flyctl version v0.4.83
```

### 3. 登录 Fly.io

```powershell
fly auth login
```
浏览器会打开登录页面，完成认证。

### 4. 部署后端

```powershell
cd "F:/hermes/2 Mike/衡简叙约/backend"

# 创建应用
fly launch --no-deploy

# 设置环境变量
fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
fly secrets set SUPABASE_SERVICE_KEY=***
fly secrets set JWT_SECRET_KEY=***
fly secrets set AI_PROVIDER=agnes
fly secrets set AI_AGNES_API_KEY=***

# 部署
fly deploy
```

### 5. 查看日志和状态

```powershell
# 查看应用状态
fly status

# 查看实时日志
fly logs

# 打开应用
fly apps open
```

---

## 🔗 快速命令

```powershell
# 安装验证
"C:/Program Files/flyctl/flyctl.exe" --version

# 登录
"C:/Program Files/flyctl/flyctl.exe" auth login

# 部署
cd "F:/hermes/2 Mike/衡简叙约/backend"
"C:/Program Files/flyctl/flyctl.exe" launch --no-deploy
"C:/Program Files/flyctl/flyctl.exe" deploy
```

---

## 💡 提示

- 安装成功后，**必须重启终端**才能使用 `fly` 命令
- 如果不想重启，可以使用完整路径：`C:\Program Files\f\yctl\f\yctl.exe`
- Fly.io 免费额度：256MB RAM × 3 台 VM（永久免费）
