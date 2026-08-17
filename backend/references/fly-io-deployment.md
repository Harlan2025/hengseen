# Fly.io 部署记录

## 安装 flyctl

```powershell
# 方法 1: winget（推荐）
winget install Fly-io.flyctl

# 方法 2: 直接下载
# https://github.com/superfly/flyctl/releases
# 下载 flyctl_0.4.83_Windows_x86_64.zip
# 解压到 C:\Users\haigu\AppData\Local\flyctl\
```

## 登录

```powershell
fly auth login
# 浏览器会打开登录页面
```

## 部署流程

```powershell
# 1. 进入 backend 目录
cd backend

# 2. 创建应用（不自动部署）
fly launch --no-deploy

# 3. 设置环境变量
fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
fly secrets set SUPABASE_SERVICE_KEY=<your-service-key>
fly secrets set JWT_SECRET_KEY=<your-secret>
fly secrets set AI_PROVIDER=agnes
fly secrets set AI_AGNES_API_KEY=<your-api-key>

# 4. 部署
fly deploy

# 5. 查看状态
fly status

# 6. 查看日志
fly logs

# 7. 打开应用
fly apps open
```

## 常见问题

### fly auth login 需要交互式终端
- 错误: `Error: fly auth login requires an interactive terminal`
- 解决: 在非交互环境使用 API Token
  ```powershell
  # 创建 Token
  fly tokens create
  
  # 设置环境变量
  $env:FLY_API_TOKEN="your-token"
  fly auth docker  # 或使用 token 直接操作
  ```

### 部署后访问慢
- Fly.io 服务器在海外，国内访问可能较慢
- 考虑使用 Cloudflare Tunnel 或 CDN 加速

## 成本

| 项目 | 费用 |
|------|------|
| 免费额度 | 256MB RAM × 3 台 VM（永久） |
| 超出后 | $0.004/GB/小时 |

预计月费用: $0（个人项目）
