# 🚀 重新部署到 Fly.io

## 当前状态
- ✅ GitHub 代码已更新（包含修复）
- ⚠️ 云端后端需要重新构建部署最新代码

---

## 方法 1：通过 Fly.io Dashboard 重新部署

### 步骤 1：访问应用页面
```
https://fly.io/apps/hengseen-backend
```

### 步骤 2：点击 Overview 页面的 "Restart" 按钮
- 找到紫色的 **"Restart"** 下拉按钮
- 点击下拉箭头 ▼

### 步骤 3：选择部署选项
如果下拉菜单中有：
- **"Redeploy"** - 选择它
- **"Deploy from GitHub"** - 选择它

如果没有部署选项，只有 Restart/Stop，请尝试方法 2。

---

## 方法 2：使用 flyctl 命令行

### 步骤 1：登录 Fly.io
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

### 步骤 2：部署
```powershell
cd "F:/hermes/2 Mike/衡简叙约"
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy
```

---

## 方法 3：通过 GitHub Actions 触发（如果可用）

1. 访问：**https://github.com/Harlan2025/hengseen/actions**
2. 找到 "Deploy to Fly.io" workflow
3. 点击 **"Run workflow"**
4. 选择分支 `main`
5. 点击绿色按钮 **"Run workflow"**

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

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

**请尝试以上任一方法触发重新部署！**
