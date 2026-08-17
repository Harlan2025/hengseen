# 🔧 部署后端到 Fly.io 的步骤

## 当前状态
- ✅ 本地后端代码已修复（创建项目成功）
- ⚠️ 云端后端还是旧代码（需要重新部署）

---

## 方法 1：使用 Web Terminal（最简单）

### 步骤 1：访问 Web Terminal
打开这个链接：
```
https://fly.io/apps/hengseen-backend/terminal
```

### 步骤 2：执行部署命令
在终端中输入以下命令：
```bash
cd /app
fly deploy
```

或者如果没有 Git：
```bash
cd /app
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 方法 2：通过 Dashboard 重新部署

### 步骤 1：访问 Activity 页面
```
https://fly.io/apps/hengseen-backend/activity
```

### 步骤 2：找到 Deploy 按钮
在这个页面的右上角，应该有一个 **"Deploy"** 或 **"Redeploy"** 按钮。

如果没有看到，尝试：
- 点击页面上方的 **"Actions"** 菜单
- 或者点击 **"..."** 更多选项

---

## 方法 3：重新生成 Token

如果以上方法都不行，请重新生成 Fly.io Token：

### 步骤 1：访问 Token 管理页面
```
https://fly.io/account/tokens
```

### 步骤 2：生成新 Token
1. 点击 **"Generate new token"**
2. **重要**：选择以下权限：
   - ✅ Read
   - ✅ Write
   - ✅ Full access（如果可用）
3. 设置过期时间：`7 days`
4. 复制新生成的 Token（以 `FlyV1` 开头）

### 步骤 3：发送给我
把新生成的 Token 发给我，我帮你部署。

---

## 验证部署成功

部署完成后，测试：
```bash
# 健康检查
curl https://hengseen-backend.fly.dev/health

# 登录
curl -X POST https://hengseen-backend.fly.dev/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目（使用上面登录返回的 token）
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

---

## 临时解决方案

如果需要立即测试，可以：
1. 修改前端 `.env.development` 指向本地后端
2. 本地运行前端开发服务器

但生产环境必须部署更新后的后端。

---

**请尝试方法 1 或方法 3，如果有问题截图发给我！**
