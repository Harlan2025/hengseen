# 🔧 Fly.io 部署问题 - Token 认证解决方案

## 问题诊断
错误：`unauthorized` - Token 需要重新认证（discharge token）

---

## 解决方案

### 方案 1：使用浏览器登录（推荐）

运行以下命令，会打开浏览器让你登录：
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

**步骤**：
1. 运行上面的命令
2. 浏览器会打开 Fly.io 登录页面
3. 使用你的账号登录
4. 登录后自动返回终端
5. 执行部署：
   ```powershell
   cd "F:/hermes/2 Mike/衡简叙约"
   & "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy --strategy immediate
   ```

---

### 方案 2：生成新 Token 并手动设置

1. **访问 Token 页面**：https://fly.io/account/tokens
2. **生成新 Token**：
   - Name: `hengseen-full-access-2`
   - **权限**：选择 **"Full access"**（最重要）
   - Expiry: `30 days`
3. **复制完整 Token**（包括 `FlyV1` 前缀）
4. **发送给我**，我帮你配置

---

### 方案 3：通过 Dashboard 手动部署

由于 CLI 认证问题，可以通过网页手动触发：

1. **访问**：https://fly.io/apps/hengseen-backend/activity
2. **点击**：页面上方的 **"Deploy"** 按钮
3. **选择**：分支 `main`
4. **等待**：部署完成

---

## 当前状态

| 项目 | 状态 |
|------|------|
| GitHub 代码 | ✅ 最新（commit `2de3e96`） |
| fly.toml 配置 | ✅ 使用 nixpacks |
| CLI 认证 | ❌ Token 需要重新认证 |
| Dashboard 部署 | ⏳ 待尝试 |

---

## 临时测试方案

如果云端部署暂时无法完成，可以先用本地测试：

### 1. 修改前端配置
编辑 `frontend/.env.development`：
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 2. 启动前端
```bash
cd frontend && npm run dev
```

### 3. 访问
```
http://localhost:5173
```

---

**请尝试方案 1：运行 `flyctl auth login` 使用浏览器登录！**

如果不行，请使用方案 3：通过 Dashboard 手动部署。
