# 🔧 重新部署指南

## 当前状态
- ❌ Restart 只是重启容器，**代码还是旧的**
- ✅ 本地代码已修复
- ⚠️ 云端需要重新构建和部署

---

## 方法 1：通过 GitHub Actions 触发部署（推荐）

### 步骤 1：访问 GitHub Actions
打开：**https://github.com/Harlan2025/hengseen/actions**

### 步骤 2：手动触发 workflow
1. 找到 **"Deploy to Fly.io"** 或类似的 workflow
2. 点击 **"Run workflow"** 按钮
3. 选择分支：`main`
4. 点击绿色 **"Run workflow"** 按钮

### 步骤 3：等待部署完成
- GitHub Actions 会自动构建和部署
- 完成后会在 Action 页面显示成功/失败

---

## 方法 2：重新生成 Fly.io Token

由于 CLI Token 已过期，需要生成新的：

### 步骤 1：访问 Token 管理
打开：**https://fly.io/account/tokens**

### 步骤 2：生成新 Token
1. 点击 **"Generate new token"**
2. **权限选择**（重要）：
   - ✅ Read
   - ✅ Write
   - ✅ Full access
3. **过期时间**：`7 days`
4. 点击 **"Generate token"**
5. 复制完整的 Token（以 `FlyV1` 开头）

### 步骤 3：发送给我
把新 Token 发给我，我帮你执行：
```bash
fly deploy --app hengseen-backend
```

---

## 方法 3：临时本地测试

如果云端部署暂时无法完成，可以先用本地测试：

### 1. 修改前端配置
编辑 `frontend/.env.development`：
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 2. 启动本地前端
```bash
cd "F:/hermes/2 Mike/衡简叙约/frontend"
npm run dev
```

### 3. 访问
```
http://localhost:5173
```

---

## 验证修复成功

部署成功后测试：
```bash
# 1. 登录
curl -X POST https://hengseen-backend.fly.dev/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 2. 使用返回的 token 创建项目
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试项目","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

## 下一步

请尝试：
1. **首选**：方法 1 - 通过 GitHub Actions 触发部署
2. **备选**：方法 2 - 生成新 Token 发给我
3. **临时**：方法 3 - 本地测试

**请选择一种方式继续！**
