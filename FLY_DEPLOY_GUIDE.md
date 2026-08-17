# Fly.io 部署指南

## 问题诊断
Web Terminal 链接返回 404，可能是：
1. 应用没有运行中的机器
2. Web Terminal 功能未启用
3. URL 格式不对

---

## 方法 1：通过 Fly Dashboard 重新部署（推荐）

### 步骤 1：访问应用页面
打开：https://fly.io/apps/hengseen-backend

### 步骤 2：查找部署选项
在左侧菜单找以下之一：
- **"Deploy"** 按钮（通常在右上角）
- **"Settings"** → **"General"** → **"Deploy"**
- **"Activity"** 页面 → 找 "Redeploy" 按钮

### 步骤 3：触发部署
点击部署按钮，系统会重新构建和部署应用。

---

## 方法 2：通过 GraphQL API 获取应用状态

访问：https://fly.io/apps/hengseen-backend

如果能看到应用信息，说明应用存在。

---

## 方法 3：使用 Fly CLI（需要有效 Token）

### 重新登录 Fly.io
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

### 重新部署
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy
```

---

## 方法 4：通过 GitHub Actions 部署

由于 GitHub push 成功，可以手动触发 GitHub Actions。

### 检查 Workflows
访问：https://github.com/Harlan2025/hengseen/actions

如果有 workflow，点击 **"Run workflow"**。

---

## 方法 5：等待自动部署

如果 GitHub Actions 已配置，push 代码后应该会自动部署。

检查：https://github.com/Harlan2025/hengseen/actions

---

## 临时方案：本地测试

如果云端部署暂时无法完成，可以先测试本地版本：

### 1. 启动本地后端
```bash
cd "F:/hermes/2 Mike/衡简叙约/backend"
.\venv\Scripts\python.exe main.py
```

### 2. 修改前端配置
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

## 验证当前状态

### 后端健康检查
```bash
curl https://hengseen-backend.fly.dev/health
```

### 前端访问
```
https://3c3d590c.hengseen.pages.dev
```

---

## 下一步行动

1. **首选**：访问 https://fly.io/apps/hengseen-backend，找部署按钮
2. **备选**：重新生成 Fly.io Token 发给我
3. **临时**：使用本地测试

请告诉我你看到了什么界面！
