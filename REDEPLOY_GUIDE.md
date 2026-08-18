# 🚀 重新部署指南

## 当前状态
- ✅ GitHub 代码已更新
- ✅ Fly.io 已连接到 GitHub
- ⚠️ 云端后端需要重新构建部署最新代码

---

## 方法 1：通过 Activity 页面触发部署（推荐）

### 步骤 1：访问 Activity 页面
```
https://fly.io/apps/hengseen-backend/activity
```

### 步骤 2：点击顶部按钮
在页面顶部找以下按钮之一：
- **"Deploy"**
- **"Redeploy"**
- **"Trigger Deploy"**

### 步骤 3：选择部署来源
- 选择 **"Deploy from GitHub"**
- 分支选择 `main`
- 点击确认

---

## 方法 2：使用 flyctl 命令行

### 步骤 1：登录
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

### 步骤 2：部署
```powershell
cd "F:/hermes/2 Mike/衡简叙约"
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy
```

---

## 方法 3：通过 Web Terminal 部署

### 步骤 1：访问 Web Terminal
```
https://fly.io/apps/hengseen-backend/terminal
```

### 步骤 2：执行部署命令
```bash
cd /app
fly deploy
```

---

## 验证部署成功

部署完成后测试创建项目：
```bash
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

**请尝试以上任一方法触发重新部署！**
