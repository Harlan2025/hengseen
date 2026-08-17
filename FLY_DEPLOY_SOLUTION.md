# Fly.io 部署问题解决

## 📍 找到 "Deploy" 按钮的方法

### 方法 1：通过 Activity 页面
1. 访问：https://fly.io/apps/hengseen-backend/activity
2. 页面顶部应该有 **"Deploy"** 或 **"Redeploy"** 按钮

### 方法 2：通过 Web Terminal
1. 访问：https://fly.io/apps/hengseen-backend/terminal
2. 执行命令：`fly deploy`

### 方法 3：使用 Git Push
如果你有 GitHub 集成：
```bash
git push origin main
```

---

## 🔧 替代方案：重新生成 Token

如果找不到按钮，请：

1. 访问 https://fly.io/account/tokens
2. 点击 **"Generate new token"**
3. **权限选择**：
   - 选择 **"Full access"** 或勾选：
     - ✅ read
     - ✅ write
     - ✅ full
4. **过期时间**：7 days
5. 复制新 Token 发给我

---

## 🧪 验证当前状态

后端 API 测试：
```bash
# 健康检查 - 应该返回 ok
curl https://hengseen-backend.fly.dev/health

# 登录测试 - 应该返回 token
curl -X POST https://hengseen-backend.fly.dev/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'
```

前端测试：
- 访问：https://3c3d590c.hengseen.pages.dev
- 尝试创建项目：主类型A + 附属类型B

---

**请告诉我：**
1. 你在 Fly.io Dashboard 看到了什么？
2. 能否找到 Web Terminal？
3. 或者提供新的 Token？
