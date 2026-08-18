# 🔧 Restart 按钮使用指南

## 操作步骤

### 1. 点击 Restart 下拉按钮
在 Overview 页面的 Scale 部分，点击 **"Restart"** 按钮旁边的下拉箭头 ▼

### 2. 选择部署选项
下拉菜单中应该有以下选项：
- **Restart** - 仅重启容器（不会更新代码）
- **Redeploy** - 重新部署（会从 GitHub 拉取最新代码）
- **Redeploy from GitHub** - 从 GitHub 重新部署

### 3. 执行部署
- 选择 **"Redeploy"** 或 **"Redeploy from GitHub"**
- 等待部署完成（通常需要 2-5 分钟）
- 页面会显示部署进度

---

## 如果下拉菜单没有部署选项

说明应用没有连接 GitHub，需要：

### 方案 1：连接 GitHub
1. 访问 Settings 页面
2. 点击 **"Attach repository"**
3. 选择 `Harlan2025/hengseen`
4. 连接后自动触发部署

### 方案 2：使用 CLI 部署
```powershell
# 重新登录
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login

# 部署
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy
```

---

## 验证部署成功

部署完成后测试：
```bash
# 创建项目测试
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

## 请先尝试：
1. **点击 Restart 下拉箭头**
2. **看是否有 Redeploy 选项**
3. **如果有，选择它并等待部署完成**

请告诉我下拉菜单中有哪些选项！
