# 🔧 Fly.io 重新部署步骤

## 根据你提供的截图，有以下方法：

---

## 方法 1：通过 Activity 页面触发部署（最简单）

### 步骤：
1. 点击左侧菜单的 **"Activity"**
2. 在 Activity 页面顶部找 **"Deploy"** 或 **"Redeploy"** 按钮
3. 点击按钮触发重新部署

---

## 方法 2：通过 GitHub 触发部署

如果应用已连接 GitHub：
1. 点击左侧菜单 **"Activity"**
2. 找到 **"Connect to GitHub"** 或查看部署历史
3. 如果有 GitHub 连接，可以：
   - 直接访问 https://github.com/Harlan2025/hengseen
   - 代码已推送，应该会自动触发部署
   - 或手动运行 GitHub Actions

---

## 方法 3：使用 Secrets 页面的重启功能

你截图显示 **Secrets 有橙色通知 (8)**：
1. 点击左侧菜单 **"Secrets"**
2. 查看是否有部署相关的提示
3. 点击 **"Restart"** 按钮（Scale 部分右上角的紫色按钮）
4. 选择 **"Restart"** 或 **"Redeploy"**

---

## 方法 4：通过 GitHub Actions 手动触发

访问：**https://github.com/Harlan2025/hengseen/actions**

1. 找到 "Deploy to Fly.io" workflow
2. 点击 **"Run workflow"**
3. 选择分支 `main`
4. 点击绿色按钮 **"Run workflow"**

---

## 临时方案：本地测试

云端部署暂时无法完成，可以先用本地版本测试：

### 1. 本地后端已在运行
```
http://localhost:8000
```

### 2. 修改前端配置
编辑 `frontend/.env.development`：
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. 启动前端开发服务器
```bash
cd "F:/hermes/2 Mike/衡简叙约/frontend"
npm run dev
```

### 4. 访问
```
http://localhost:5173
```

---

## 验证本地修复成功

本地后端创建项目测试：
```bash
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

**请先尝试方法 1 或方法 4，如果不行就用本地测试！**
