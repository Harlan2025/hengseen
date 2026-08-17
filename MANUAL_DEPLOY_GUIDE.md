# 🚀 手动部署到 Fly.io 指南

## 当前问题
- ❌ Fly.io Token 已过期/无效
- ❌ Web Terminal 无法访问（404）
- ✅ 本地代码已修复

---

## 方法 1：通过 Fly.io Dashboard 手动部署

### 步骤 1：登录 Fly.io
打开：**https://fly.io/login**
用你的账号登录

### 步骤 2：访问应用
打开：**https://fly.io/apps/hengseen-backend**

### 步骤 3：重新部署
在页面顶部或右侧找以下按钮之一：
- **"Deploy"** 按钮
- **"Redeploy"** 按钮
- **"Actions"** → 选择 "Deploy"

如果没有找到，尝试：
1. 点击左侧菜单 **"Settings"**
2. 滚动到 **"Deploy"** 部分
3. 点击 **"Redeploy"**

### 步骤 4：选择部署来源
如果询问部署来源：
- 选择 **"From GitHub"** 或 **"Manual Deploy"**
- 如果是 GitHub，选择 `Harlan2025/hengseen` 仓库
- 分支选择：`main`

---

## 方法 2：重新生成 Fly.io Token

### 步骤 1：访问 Token 页面
```
https://fly.io/account/tokens
```

### 步骤 2：生成新 Token
1. 点击 **"Generate new token"**
2. 填写：
   - Name: `hengseen-deploy`
   - Expiry: `7 days`
3. **重要**：权限选择
   - ✅ Read
   - ✅ Write
   - ✅ Full access（如果可用）
4. 点击 **"Generate token"**
5. 复制完整的 Token（以 `FlyV1` 开头）

### 步骤 3：发送 Token 给我
把新生成的 Token 发给我，我帮你通过命令行部署。

---

## 方法 3：使用 GitHub Actions（如果已配置）

### 检查 GitHub Actions
访问：**https://github.com/Harlan2025/hengseen/actions**

如果有 workflow：
1. 点击 **"Deploy to Fly.io"**
2. 点击 **"Run workflow"**
3. 选择分支 `main`
4. 点击 **"Run workflow"**

---

## 临时测试方案

如果云端部署暂时无法完成，可以先测试本地版本：

### 1. 启动本地后端（已运行中）
后端已在本地运行：http://localhost:8000

### 2. 修改前端配置指向本地
编辑 `frontend/.env.development`：
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. 启动本地前端
```bash
cd "F:/hermes/2 Mike/衡简叙约/frontend"
npm run dev
```

### 4. 访问本地前端
http://localhost:5173

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

## 请告诉我

1. **你在 Fly.io Dashboard 看到了什么？** （截图或描述）
2. **能否找到 Deploy/Redeploy 按钮？**
3. **或者是否愿意生成新 Token 发给我？**
