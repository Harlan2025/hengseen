# 🔒 Fly.io Token 更新指南

## ⚠️ 问题诊断

**GitGuardian 警告**: `backend/.env.fly` 文件包含泄露的 API Token

**已执行的操作**:
- ✅ 从 Git 追踪中移除敏感文件
- ✅ 更新 .gitignore
- ✅ 推送修复到 GitHub (Commit: `89b13fe`)

---

## 🔄 Token 问题

新提供的 Token 认证失败：
```
Error: Authenticate: token validation error
```

**可能原因**:
1. Token 格式不正确（需要完整的 FlyV1 前缀）
2. Token 还未生效（需要等待几秒钟）
3. Token 在生成时选择了错误的权限范围

---

## ✅ 解决方案

### 方案 1：使用 Fly.io Dashboard（推荐）

1. **访问 Dashboard**
   ```
   https://fly.io/apps/hengseen-backend/secrets
   ```

2. **添加环境变量**
   | Key | Value |
   |-----|-------|
   | SUPABASE_URL | https://rtmldrysnwzbkgiihnuc.supabase.co |
   | SUPABASE_SERVICE_KEY | (你的 Supabase Service Key) |
   | JWT_SECRET_KEY | (随机生成一个长字符串) |
   | AI_PROVIDER | agnes |
   | AI_AGNES_API_KEY | sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5 |

3. **保存并重启应用**
   - 点击 "Save secrets"
   - 应用会自动重启

### 方案 2：重新生成 Token

1. 访问 https://fly.io/account/tokens
2. 点击 "Generate new token"
3. **重要**: 确保选择以下权限：
   - ✅ `read`
   - ✅ `write`
   - ✅ `full` (如果可用)
4. 复制完整 Token（包括 `FlyV1` 前缀）
5. 重新尝试部署

### 方案 3：使用网页重新部署

1. 访问 https://fly.io/apps/hengseen-backend
2. 点击 "Settings" → "Environment variables"
3. 添加所有必需的环境变量
4. 点击 "Deploy" 重新部署

---

## 🛡️ 安全检查清单

- [ ] 从 Git 追踪中移除敏感文件 ✅
- [ ] 更新 .gitignore ✅
- [ ] 推送修复到 GitHub ✅
- [ ] 旋转泄露的 Token ⏳ (进行中)
- [ ] 更新 Fly.io 应用配置 ⏳
- [ ] 验证应用正常运行 ⏳

---

## 🔧 本地测试

更新配置后，可以测试应用：

```bash
# 健康检查
curl https://hengseen-backend.fly.dev/health

# 登录测试
curl -X POST https://hengseen-backend.fly.dev/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'
```

---

## 📋 后续步骤

1. **立即**: 访问 Fly.io Dashboard 更新环境变量
2. **验证**: 测试 API 是否正常工作
3. **清理**: 考虑使用 BFG 清除 Git 历史中的泄露密钥
4. **预防**: 安装 ggshield 防止未来泄露

---

## 🔗 相关链接

- **Fly.io Secrets**: https://fly.io/docs/reference/secrets/
- **GitGuardian 文档**: https://docs.gitguardian.com
- **安全最佳实践**: https://docs.github.com/en/code-security/secret-scanning
