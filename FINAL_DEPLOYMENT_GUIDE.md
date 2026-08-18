# 🚀 Fly.io 部署最终解决方案

## 问题总结
- ✅ GitHub 代码已更新（commit `9beab33`）
- ✅ Dockerfile 已创建
- ❌ 构建失败：`unauthorized` - 镜像推送权限问题

---

## 解决方案

### 方案 1：添加 Docker Registry 凭据（推荐）

#### 步骤 1：访问 Secrets 页面
```
https://fly.io/apps/hengseen-backend/secrets
```

#### 步骤 2：添加环境变量
点击 **"Add secret"**，添加以下变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `DOCKER_REGISTRY_URL` | `registry.fly.io` | Fly.io 容器注册表 |
| `DOCKER_REGISTRY_USER` | `x-token` | 固定值 |
| `DOCKER_REGISTRY_PASSWORD` | 你的 Fly.io Token | 从下面获取 |

#### 步骤 3：获取 Token
1. 访问：**https://fly.io/account/tokens**
2. 复制任意一个有效 Token
3. 粘贴到 `DOCKER_REGISTRY_PASSWORD` 字段

#### 步骤 4：重新触发部署
1. 访问：**https://fly.io/apps/hengseen-backend/activity**
2. 点击 **"Deploy"** 按钮
3. 等待部署完成

---

### 方案 2：通过 GitHub Actions 部署

#### 步骤 1：创建 Workflow 文件
在 GitHub 仓库中创建 `.github/workflows/deploy-fly.yml`：

```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [main]

jobs:
  deploy:
    name: Deploy to Fly.io
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

#### 步骤 2：在 GitHub 添加 Secret
1. 访问：**https://github.com/Harlan2025/hengseen/settings/secrets/actions**
2. 点击 **"New repository secret"**
3. Name: `FLY_API_TOKEN`
4. Value: 你的 Fly.io Token
5. 点击 **"Add secret"**

#### 步骤 3：触发部署
推送新提交到 main 分支会自动触发部署。

---

### 方案 3：联系 Fly.io 支持

如果以上方法都不行，可能是账户权限问题：
1. 访问：**https://fly.io/support**
2. 描述问题：`unauthorized` 错误，无法推送镜像
3. 请求帮助

---

## 当前状态

| 项目 | 状态 |
|------|------|
| GitHub 代码 | ✅ 最新（commit `9beab33`） |
| Dockerfile | ✅ 已创建 |
| fly.toml | ✅ 配置正确 |
| 本地后端 | ✅ 运行中 |
| 云端部署 | ⏳ 等待添加 Registry 凭据 |

---

## 验证本地修复成功

后端已在本地运行：
```
http://localhost:8000
```

测试：
```bash
# 登录
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目（使用返回的 token）
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ***" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

**请尝试方案 1：在 Secrets 页面添加 Docker Registry 凭据！**
