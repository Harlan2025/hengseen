# 🔧 Fly.io 部署问题 - 移除 Builder 方案

## 问题诊断
错误：`unauthorized` - Token 无法推送到容器注册表

**原因**：Fly.io Dashboard 部署时使用 Buildpacks，需要推送镜像到 registry，但 Token 没有此权限。

---

## 已执行的修复

### 修改 fly.toml
移除了 `[build]` 部分，让 Fly.io 使用默认构建方式：

**之前**：
```toml
[build]
  builder = "nixpacks"
```

**之后**：
```toml
# 移除 [build] 部分
```

---

## 🔧 下一步操作

### 步骤 1：等待 Git 推送完成
已经执行：
```bash
git add -A
git commit -m "fix: remove builder section to use default build"
git push origin main
```

### 步骤 2：重试部署
1. 访问：**https://fly.io/apps/hengseen-backend/activity**
2. 点击 **"Deploy"** 按钮
3. 选择分支 `main`
4. 等待部署完成

---

## 📋 当前状态

| 项目 | 状态 |
|------|------|
| GitHub 代码 | ✅ 最新（即将推送） |
| fly.toml | ✅ 已移除 [build] 部分 |
| Dockerfile | ✅ 保留作为备选 |
| 本地后端 | ✅ 运行中 |
| 云端部署 | ⏳ 等待重试 |

---

## 🧪 验证本地修复成功

```bash
# 登录测试
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目测试（使用返回的 token）
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回成功

---

**请等待 Git 推送完成后，点击重试按钮！**
