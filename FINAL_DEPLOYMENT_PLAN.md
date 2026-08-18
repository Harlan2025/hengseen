# 🚀 Fly.io 最终部署方案

## 问题总结
- ✅ GitHub 代码已更新（commit `2de3e96`，使用 nixpacks）
- ❌ CLI Token 认证失败（需要 discharge token）
- ❌ 自动部署失败（unauthorized 错误）

---

## 方案 1：通过 Fly.io Dashboard 手动部署（最简单）

### 步骤 1：访问 Activity 页面
```
https://fly.io/apps/hengseen-backend/activity
```

### 步骤 2：点击 Deploy 按钮
在页面顶部应该能看到：
- **"Deploy"** 按钮（蓝色）
- 或 **"Redeploy"** 按钮

### 步骤 3：配置部署
- 选择分支：`main`
- 确认设置正确
- 点击确认部署

---

## 方案 2：生成新的 Full Access Token

### 步骤 1：访问 Token 管理
```
https://fly.io/account/tokens
```

### 步骤 2：删除旧 Token
- 找到当前使用的 Token
- 点击删除或标记为过期

### 步骤 3：生成新 Token
1. 点击 **"Generate new token"**
2. 填写：
   - **Name**: `hengseen-full-access-final`
   - **Expiry**: `30 days`
3. **重要**：权限选择
   - ✅ Read
   - ✅ Write
   - ✅ **Full access**（必须勾选）
4. 点击 **"Generate token"**
5. **复制完整 Token**（包括 `FlyV1` 前缀）

### 步骤 4：发送给我
把新生成的 Token 发给我，我帮你通过 CLI 部署。

---

## 方案 3：临时本地测试

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

## 验证本地修复成功

```bash
# 登录测试
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目测试（使用返回的 token）
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

## 当前状态

| 组件 | 状态 |
|------|------|
| 本地后端 | ✅ 已修复 |
| GitHub | ✅ 最新代码 |
| fly.toml | ✅ 配置正确 |
| 云端部署 | ⏳ 等待手动触发 |

---

**请选择一种方案：**
1. **首选**：方案 1 - 通过 Dashboard 手动部署
2. **备选**：方案 2 - 生成新 Token 发给我
3. **临时**：方案 3 - 本地测试

请告诉我你选择哪种方式！
