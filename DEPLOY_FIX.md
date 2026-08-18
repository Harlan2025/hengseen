# 🔧 Fly.io 部署失败 - 权限问题修复

## 错误原因
```
Error: failed to fetch an image or build from source: unauthorized
```

**问题**：Fly.io Token 权限不足，无法推送构建的镜像

---

## 解决方案

### 方案 1：重新生成完整权限的 Token（推荐）

#### 步骤 1：访问 Token 管理页面
```
https://fly.io/account/tokens
```

#### 步骤 2：删除旧 Token
- 找到当前使用的 Token
- 点击删除或标记为过期

#### 步骤 3：生成新 Token
1. 点击 **"Generate new token"**
2. **Name**: `hengseen-full-access`
3. **Expiry**: `30 days`（更长有效期）
4. **权限设置**（重要）：
   - ✅ Read
   - ✅ Write  
   - ✅ Full access（如果有这个选项）
   - ✅ 勾选所有可用的权限
5. 点击 **"Generate token"**
6. 复制完整的 Token（包括 `FlyV1` 前缀）

#### 步骤 4：测试新 Token
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```
选择手动输入 Token，粘贴新生成的 Token

---

### 方案 2：使用 Buildpacks 而不是 Docker

修改 `fly.toml` 使用 Buildpacks 方式构建：

```toml
app = "hengseen-backend"

[build]
  builder = "paketobuildpacks/builder:full"
  
[deploy]
  health_check_path = "/health"
  health_check_timeout_seconds = 30
```

然后重新部署：
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy --strategy immediate
```

---

### 方案 3：通过 Dashboard 手动触发（无需 CLI）

1. 访问：**https://fly.io/apps/hengseen-backend**
2. 点击 **"Overview"**
3. 找到 **"Deploy"** 按钮（如果有）
4. 选择 **"Deploy now"**
5. 等待自动构建

---

## 验证当前配置

### 检查 GitHub 连接状态
```
https://fly.io/apps/hengseen-backend/settings
```

确认：
- Repository: `Harlan2025/hengseen` ✅
- Branch: `main` ✅
- Deploy mode: Automatic ✅

---

## 临时解决方案

如果云端部署暂时无法完成，可以先用本地测试：

### 1. 后端已在本地运行
```
http://localhost:8000
```

### 2. 修改前端配置
编辑 `frontend/.env.development`：
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. 启动前端
```bash
cd frontend && npm run dev
```

### 4. 访问
```
http://localhost:5173
```

---

## 下一步

**请重新生成一个 Full access 权限的 Token，发给我！**

或者尝试方案 3 的 Dashboard 手动部署方式。
