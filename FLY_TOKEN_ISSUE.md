# Fly.io Token 问题诊断

## ⚠️ 问题

当前 Token 认证失败，返回错误：
```
Error: failed retrieving current user: You must be authenticated to view this.
```

---

## 🔍 原因分析

1. **Token 可能已过期** - Fly.io Token 有有效期
2. **Token 格式问题** - 提供的 Token 可能包含额外字符
3. **认证状态丢失** - 需要重新登录

---

## ✅ 解决方案

### 方案 1：重新登录（推荐）

**在 PowerShell 中运行：**
```powershell
# 清除旧认证
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth logout

# 重新登录
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

浏览器会打开，完成登录后自动保存新 Token。

### 方案 2：使用 Fly.io Dashboard

1. 访问 https://fly.io/dashboard
2. 点击右上角头像 → "Account Settings"
3. 找到 "API Tokens" 部分
4. 点击 "Generate new token"
5. 复制新生成的 Token
6. 提供给我继续部署

### 方案 3：网页直接部署（最简单）

1. 访问 https://fly.io/dashboard
2. 点击 "New App"
3. 选择 "Connect to Git"
4. 授权 GitHub 并选择 `haiguang85/hengseen` 仓库
5. 配置环境变量：
   - SUPABASE_URL
   - SUPABASE_SERVICE_KEY
   - JWT_SECRET_KEY
   - AI_PROVIDER=agnes
   - AI_AGNES_API_KEY
6. 点击 "Deploy App"

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| flyctl | ✅ 已安装 |
| Token | ❌ 过期/无效 |
| 下一步 | 重新登录或网页部署 |

---

## 💡 建议

由于 Token 认证问题，**建议使用网页部署**：
1. 最简单，无需命令行操作
2. 可视化配置环境变量
3. 实时查看部署日志
4. 自动处理认证问题

请访问：https://fly.io/dashboard
