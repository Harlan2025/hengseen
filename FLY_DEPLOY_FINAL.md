# 🚀 Fly.io 部署指南

## 当前状态
- ✅ GitHub 代码已推送
- ⚠️ Fly.io Token 需要重新认证
- ⚠️ CLI 部署失败（需要 discharge token）

---

## 方法 1：通过 Fly.io Web Dashboard 部署（最简单）

### 步骤 1：访问应用页面
```
https://fly.io/apps/hengseen-backend
```

### 步骤 2：触发部署
1. 点击左侧菜单 **"Activity"**
2. 在页面顶部找 **"Deploy"** 或 **"Redeploy"** 按钮
3. **重要**：选择 **"Deploy from GitHub"** 或 **"Manual Deploy"**
4. 等待构建完成

---

## 方法 2：重新登录 Fly.io CLI

### 步骤 1：登录
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

### 步骤 2：部署
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy
```

---

## 方法 3：使用 Fly.io API 触发部署

如果你有有效的 API Token，可以使用 GraphQL API：

```bash
curl -X POST https://api.fly.io/graphql \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { appDeploy(input: {appId: \"hengseen-backend\", strategy: \"immediate\"}) { deployment { id status } } }"
  }'
```

---

## 验证部署成功

部署完成后测试：
```bash
# 健康检查
curl https://hengseen-backend.fly.dev/health

# 创建项目测试
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

---

## 临时解决方案

如果云端部署暂时无法完成：

### 本地测试
1. 后端已在本地运行：http://localhost:8000
2. 修改前端配置：
   ```bash
   # 编辑 frontend/.env.development
   VITE_API_URL=http://localhost:8000/api/v1
   ```
3. 启动前端：
   ```bash
   cd frontend && npm run dev
   ```
4. 访问：http://localhost:5173

---

**请尝试方法 1 或方法 2！**
