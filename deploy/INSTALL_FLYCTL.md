# flyctl 安装指南

## 方法 1：winget（推荐，最简单）

```powershell
winget install Fly.io.flyctl
```

验证安装：
```powershell
fly --version
```

---

## 方法 2：直接下载可执行文件

### Windows
1. 访问：https://github.com/superfly/flyctl/releases
2. 下载最新版本的 `flyctl_windows_amd64.zip`
3. 解压到任意目录，例如：`C:\Tools\flyctl\`
4. 将文件夹添加到 PATH：
   ```powershell
   [Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Tools\flyctl", "User")
   ```
5. 重启终端，验证：
   ```powershell
   fly --version
   ```

---

## 方法 3：Scoop

```powershell
scoop install fly
```

---

## 方法 4：Chocolatey

```powershell
choco install fly
```

---

## 验证安装

```powershell
# 检查版本
fly --version

# 输出示例：
# flyctl version v0.1.234
```

---

## 常见问题

### Q: winget 找不到包？
A: 更新 winget：
```powershell
winget upgrade Microsoft.Winget.Source
winget install Fly.io.flyctl
```

### Q: 安装后命令找不到？
A: 重启终端或重新加载 PATH：
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
```

### Q: 需要管理员权限？
A: 以管理员身份运行 PowerShell，然后执行安装命令。

---

## 安装后下一步

```powershell
# 1. 登录 Fly.io
fly auth login

# 2. 部署后端
cd "F:/hermes/2 Mike/衡简叙约/backend"
fly launch --no-deploy
fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
fly secrets set JWT_SECRET_KEY=your-secret-key
fly secrets set AI_PROVIDER=agnes
fly secrets set AI_AGNES_API_KEY=***
fly deploy

# 3. 查看日志
fly logs
```
