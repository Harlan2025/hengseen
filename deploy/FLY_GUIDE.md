# Fly.io 部署指南

## Fly.io vs Railway 对比

| 特性 | Fly.io | Railway |
|------|--------|---------|
| **免费额度** | 256MB RAM × 3 台机器（永久免费） | $5 免费额度/月 |
| **按需付费** | 按实际使用计费 | 超出后 $5/月起 |
| **冷启动** | 约 10-30 秒 | 较快 |
| **自定义域名** | ✅ 支持 | ✅ 支持 |
| **内部网络** | ✅ Fly Virtual Network | ❌ 不支持 |
| **Postgres** | ✅ 内置集群 | ✅ 集成 Supabase |
| **部署速度** | 中等 | 快 |
| **日志** | fly logs | Railway Dashboard |
| **适合场景** | 生产环境、高可用 | 快速原型、小项目 |

---

## 前置条件

### 1. 安装 Fly CLI
```bash
# Windows (使用 winget)
winget install Fly.io.flyctl

# 或下载可执行文件
# https://fly.io/docs/hands-on/install-flyctl/
```

### 2. 登录 Fly.io
```bash
fly auth login
```
浏览器会打开登录页面，完成认证。

### 3. 创建 Fly 应用
```bash
cd backend
fly launch
```

---

## 部署步骤

### 步骤 1：初始化 Fly 应用
```bash
cd "F:/hermes/2 Mike/衡简叙约/backend"
fly launch --no-deploy
```

这会自动检测 FastAPI 项目并生成 `fly.toml`。

### 步骤 2：配置环境变量
```bash
fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
fly secrets set SUPABASE_SERVICE_KEY=***
fly secrets set JWT_SECRET_KEY=***
fly secrets set AI_PROVIDER=agnes
fly secrets set AI_AGNES_API_KEY=***
```

### 步骤 3：部署
```bash
fly deploy
```

### 步骤 4：获取应用 URL
```bash
fly apps list
fly apps open
```

---

## 成本估算

### 免费额度
- 256MB RAM × 3 台共享 VM
- 每月 3GB 出站流量
- 足够个人项目和小流量应用

### 付费方案
- Shared CPU: $0.007/小时 (~$5/月)
- Dedicated CPU: $0.05/小时 (~$36/月)

**预计月费用**: $0-5（根据访问量）

---

## 优点

1. **永久免费额度**：比 Railway 更慷慨
2. **全球边缘部署**：34 个数据中心
3. **真正的容器隔离**：每实例独立 VM
4. **Fly Machine API**：可以运行长期任务
5. **成熟的 Postgres 集群**：内置复制和备份

---

## 缺点

1. **学习曲线较陡**：需要理解 Fly 概念
2. **冷启动较慢**：首次请求可能慢 30 秒
3. **配置文件复杂**：fly.toml 需要手动调整
4. **国内访问慢**：服务器主要在海外

---

## 迁移建议

| 场景 | 推荐平台 |
|------|----------|
| 个人项目/原型 | Railway（简单快速） |
| 生产环境 | Fly.io（免费额度大） |
| 需要低延迟 | Cloudflare Workers（边缘计算） |
| 需要完整 Postgres | Supabase + Railway |

---

## 快速开始

```bash
# 1. 安装 flyctl
winget install Fly.io.flyctl

# 2. 登录
fly auth login

# 3. 部署后端
cd backend
fly launch --no-deploy
fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
fly secrets set SUPABASE_SERVICE_KEY=***
fly secrets set JWT_SECRET_KEY=***
fly secrets set AI_PROVIDER=agnes
fly secrets set AI_AGNES_API_KEY=***
fly deploy

# 4. 获取 URL
fly apps open
```
