# 🔧 替代方案：手动修改 GitHub 上的 fly.toml

## 问题
git push 失败，但 Fly.io 需要从 GitHub 拉取最新代码。

---

## 解决方案：直接在 GitHub 网页上修改 fly.toml

### 步骤 1：访问 GitHub 仓库
```
https://github.com/Harlan2025/hengseen
```

### 步骤 2：找到 fly.toml 文件
1. 点击 **"main"** 分支（确保在 main 分支）
2. 找到 **`fly.toml`** 文件（在根目录）
3. 点击文件进入详情页

### 步骤 3：编辑文件
1. 点击右上角的 **"Edit"** 按钮（铅笔图标）
2. 将以下内容替换现有的 fly.toml：

```toml
app = "hengseen-backend"

[build]
  builder = "nixpacks"

[deploy]
  health_check_path = "/health"
  health_check_timeout_seconds = 30
  restart_policy_type = "on_failure"
  restart_policy_max_retries = 10

[env]
  PORT = "8000"
  PYTHON_VERSION = "3.11"

[mounts]
  source = "data"
  destination = "/data"

[[services]]
  protocol = "tcp"
  internal_port = 8000
  processes = ["app"]

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20

  [[services.tcp_checks]]
    interval = "10s"
    timeout = "2s"
    grace_period = "5s"
```

### 步骤 4：提交更改
1. 滚动到页面底部
2. 点击 **"Commit changes"** 按钮
3. 选择 **"Direct commit"**
4. 点击确认提交

### 步骤 5：回到 Fly.io 重试部署
1. 访问：https://fly.io/apps/hengseen-backend/activity
2. 找到失败的部署
3. 点击 **"I've fixed this on GitHub, retry"** 按钮
4. 等待重新部署

---

## 为什么需要修改 fly.toml？

**原配置**：
```toml
[build]
  builder = "paketobuildpacks/builder:full"
```

**问题**：Buildpacks builder 需要访问外部镜像仓库，但认证失败。

**新配置**：
```toml
[build]
  builder = "nixpacks"
```

**优势**：
- ✅ Nixpacks 由 Fly.io 原生支持
- ✅ 不需要外部镜像认证
- ✅ 自动检测 Python 项目
- ✅ 构建更快更可靠

---

## 验证本地修复成功

在本地测试创建项目：
```bash
# 登录
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目（使用返回的 token）
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

**请按照上述步骤在 GitHub 网页上修改 fly.toml，然后回到 Fly.io 重试部署！**
