# 🔧 Fly.io 部署修复指南

## 当前状态
- ✅ GitHub 代码已推送（commit `78b0b8e`）
- ✅ `fly.toml` 已移除 `[build]` 部分
- ⏳ 需要重新触发部署

---

## 解决方案

### 方法 1：通过 Fly.io Dashboard 重试（推荐）

#### 步骤 1：访问 Activity 页面
```
https://fly.io/apps/hengseen-backend/activity
```

#### 步骤 2：点击 Deploy 按钮
在页面顶部找到 **"Deploy"** 按钮（蓝色）

#### 步骤 3：配置部署
- 分支选择：`main`
- 确认设置正确
- 点击确认部署

#### 步骤 4：等待完成
部署应该需要 3-5 分钟

---

### 方法 2：使用 Web Terminal 手动部署

#### 步骤 1：访问 Web Terminal
```
https://fly.io/apps/hengseen-backend/terminal
```

#### 步骤 2：执行部署命令
```bash
cd /app
fly deploy --strategy immediate
```

---

### 方法 3：添加 Docker Registry 凭据

如果仍然失败，可能需要添加凭据：

#### 步骤 1：访问 Secrets 页面
```
https://fly.io/apps/hengseen-backend/secrets
```

#### 步骤 2：添加以下变量
| 变量名 | 值 |
|--------|-----|
| `DOCKER_REGISTRY_URL` | `registry.fly.io` |
| `DOCKER_REGISTRY_USER` | `x-token` |
| `DOCKER_REGISTRY_PASSWORD` | 你的 Fly.io Token |

#### 步骤 3：重新触发部署

---

## 当前 fly.toml 配置

```toml
app = "hengseen-backend"

[deploy]
  health_check_path = "/health"
  health_check_timeout_seconds = 30
  restart_policy_type = "on_failure"
  restart_policy_max_retries = 10

[env]
  PORT = "8000"
  PYTHON_VERSION = "3.11"
```

**注意**：已移除 `[build]` 部分，使用 Fly.io 默认构建方式。

---

## 验证本地修复成功

```bash
# 登录测试
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目测试
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ***" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

## 预期结果

移除 `[build]` 部分后：
- Fly.io 会使用默认构建器
- 不需要手动指定 registry
- 应该能成功构建并部署

---

**请点击 Fly.io Activity 页面的 "Deploy" 按钮重试部署！**
