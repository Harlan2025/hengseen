# 🔧 Fly.io 部署问题 - 镜像推送权限修复

## 问题诊断
错误：`failed to fetch an image or build from source: unauthorized`

**原因**：Fly.io Dashboard 部署时使用 `--build-only --push` 命令，需要推送镜像到容器注册表的权限，但当前 Token 没有此权限。

---

## 解决方案

### 方案 1：添加 Docker Registry 凭据（推荐）

在 Fly.io Dashboard 中添加 Docker Hub 或 Container Registry 的凭据：

1. **访问 Secrets 页面**：
   ```
   https://fly.io/apps/hengseen-backend/secrets
   ```

2. **添加以下环境变量**：
   - `DOCKER_REGISTRY_URL` = `registry.fly.io`
   - `DOCKER_REGISTRY_USER` = `x-token`（固定值）
   - `DOCKER_REGISTRY_PASSWORD` = 你的 Fly.io Token

3. **重新触发部署**

### 方案 2：使用自定义 Dockerfile（绕过 Buildpacks）

创建一个简单的 Dockerfile，使用官方 Python 镜像：

1. **访问 GitHub 仓库**：
   ```
   https://github.com/Harlan2025/hengseen
   ```

2. **创建 Dockerfile**：
   - 点击 "Add file" → "Create new file"
   - 文件名：`Dockerfile`
   - 内容：
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY backend/requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY backend/ .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **修改 fly.toml**，移除 build 部分：
   ```toml
   app = "hengseen-backend"
   
   [deploy]
     health_check_path = "/health"
     health_check_timeout_seconds = 30
   
   [env]
     PORT = "8000"
   ```

4. **提交更改并重新部署**

### 方案 3：通过 GitHub Actions 部署

创建一个简单的 workflow：

1. **访问 GitHub Actions**：
   ```
   https://github.com/Harlan2025/hengseen/actions
   ```

2. **创建新 workflow**：
   ```yaml
   name: Deploy to Fly.io
   
   on:
     push:
       branches: [main]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: superfly/flyctl-actions/setup-flyctl@master
         - run: flyctl deploy --remote-only
       env:
         FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
   ```

3. **在 Fly.io 添加 GitHub App 集成**：
   - 访问：https://fly.io/apps/hengseen-backend/settings
   - 找到 "GitHub" 部分
   - 点击 "Configure" 或 "Connect"

---

## 当前状态

| 项目 | 状态 |
|------|------|
| GitHub 代码 | ✅ 最新 |
| fly.toml | ✅ 配置正确 |
| 本地后端 | ✅ 运行中 |
| Docker 认证 | ❌ 需要配置 |
| 云端部署 | ⏳ 等待修复 |

---

## 建议

**首选方案 2**：创建自定义 Dockerfile，这样可以完全控制构建过程，避免 Buildpacks 的权限问题。

**备选方案**：联系 Fly.io 支持，询问如何为应用添加完整的容器注册表访问权限。

---

**请尝试方案 2：在 GitHub 上创建 Dockerfile！**
