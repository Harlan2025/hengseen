# 📋 部署问题总结

## 根本原因
Fly.io Dashboard 部署时需要将构建的镜像推送到容器注册表，但当前 Fly.io Token 没有此权限（缺少 discharge token）。

---

## 已尝试的解决方案

| 方案 | 结果 |
|------|------|
| ✅ 修改 fly.toml 字段名 | 完成 |
| ✅ 移动 fly.toml 到根目录 | 完成 |
| ✅ 切换到 nixpacks builder | 完成 |
| ✅ 创建 Dockerfile | 完成 |
| ✅ 移除 [build] 部分 | 完成 |
| ❌ CLI 部署 | Token 认证失败 |
| ❌ Dashboard 自动部署 | `unauthorized` 错误 |

---

## 当前状态

| 项目 | 状态 |
|------|------|
| 本地后端 | ✅ 已修复，可正常创建项目 |
| GitHub 代码 | ⏳ 等待推送（commit `78b0b8e`） |
| fly.toml | ✅ 已移除 [build] 部分 |
| 云端部署 | ⏳ 等待 Token 权限问题解决 |

---

## 推荐解决方案

### 方案 1：联系 Fly.io 支持（推荐）
1. 访问：**https://fly.io/support**
2. 描述问题：
   - 错误：`unauthorized` when deploying
   - 请求：帮助为应用 `hengseen-backend` 配置完整的容器注册表访问权限
3. 等待回复

### 方案 2：使用替代云平台
如果 Fly.io 暂时无法解决，可以考虑：
- **Railway**：https://railway.app
- **Render**：https://render.com
- **Heroku**：https://heroku.com

### 方案 3：本地测试
如果云端部署暂时无法完成，可以先用本地测试：
```bash
# 后端已在本地运行
http://localhost:8000

# 前端配置
frontend/.env.development:
VITE_API_URL=http://localhost:8000/api/v1

# 启动前端
cd frontend && npm run dev
# 访问：http://localhost:5173
```

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

**请决定下一步行动：**
1. 联系 Fly.io 支持
2. 尝试其他云平台
3. 继续本地测试
