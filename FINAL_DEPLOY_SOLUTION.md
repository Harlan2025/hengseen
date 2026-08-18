# 🚀 Fly.io 部署最终方案

## 问题总结
- ❌ Token 认证失败（需要 discharge token）
- ❌ CLI 无法直接使用 Token 部署
- ✅ `fly.toml` 配置正确
- ✅ GitHub 已连接

---

## 解决方案（按优先级）

### 方案 1：通过 Fly.io Dashboard 手动触发（最简单）

#### 步骤 1：访问 Activity 页面
```
https://fly.io/apps/hengseen-backend/activity
```

#### 步骤 2：查找 Deploy 按钮
在页面顶部寻找以下按钮之一：
- **"Deploy"**
- **"Redeploy"**  
- **"Trigger Deploy"**
- **"Manual Deploy"**

#### 步骤 3：点击部署
- 选择 **"Deploy from GitHub"**
- 分支选择 `main`
- 等待部署完成

---

### 方案 2：使用浏览器登录 CLI

#### 步骤 1：运行登录命令
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

#### 步骤 2：按提示操作
- 命令会打开浏览器让你登录 Fly.io
- 完成登录后自动返回终端
- 执行部署：
  ```powershell
  & "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy --strategy immediate
  ```

---

### 方案 3：生成 Discharge Token

#### 步骤 1：访问 Token 页面
```
https://fly.io/account/tokens
```

#### 步骤 2：生成带 Discharge 的 Token
1. 生成新 Token
2. 使用以下命令获取 discharge token：
   ```powershell
   & "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth token
   ```
3. 使用返回的 discharge token 进行部署

---

### 方案 4：临时本地测试

如果云端部署暂时无法完成，可以先用本地测试：

#### 1. 启动本地后端（已在运行）
```
http://localhost:8000
```

#### 2. 修改前端配置
编辑 `frontend/.env.development`：
```
VITE_API_URL=http://localhost:8000/api/v1
```

#### 3. 启动前端
```bash
cd frontend && npm run dev
```

#### 4. 访问
```
http://localhost:5173
```

---

## 验证本地修复成功

```bash
# 登录
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目（使用返回的 token）
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试项目","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

## 当前状态

| 项目 | 状态 |
|------|------|
| 本地后端 | ✅ 已修复，可正常创建项目 |
| GitHub | ✅ 最新代码已推送 |
| fly.toml | ✅ 配置正确 |
| 云端部署 | ⏳ 等待手动触发 |

---

**请先尝试方案 1：访问 Activity 页面，点击 Deploy 按钮！**

如果找不到 Deploy 按钮，请截图发给我，我帮你定位。
