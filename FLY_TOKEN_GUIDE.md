# Fly.io Token 使用指南

## ⚠️ 问题诊断

Token 认证失败。可能原因：
1. Token 已过期
2. Token 格式不正确
3. Token 权限不足

---

## 解决方案

### 方案 1：重新生成 Token（推荐）

1. **访问 Fly.io Dashboard**
   ```
   https://fly.io/dashboard
   ```

2. **生成新 Token**
   - 点击右上角头像 → "Account Settings"
   - 或访问：https://fly.io/account/tokens
   - 点击 "Generate new token"
   - 设置名称和过期时间
   - **复制新生成的 Token**

3. **使用新 Token 部署**
   ```powershell
   cd "F:/hermes/2 Mike/衡简叙约/backend"
   $env:FLY_API_TOKEN = "你的新token"
   fly launch --no-deploy
   fly deploy
   ```

---

### 方案 2：使用浏览器登录（最简单）

1. 打开新终端（PowerShell）
2. 运行：
   ```powershell
   & "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
   ```
3. 浏览器会打开，完成登录
4. 然后运行部署脚本：
   ```powershell
   cd "F:/hermes/2 Mike/衡简叙约"
   .\deploy\deploy-fly.ps1
   ```

---

### 方案 3：直接访问 Fly.io 网页部署

1. 打开 https://fly.io/dashboard
2. 点击 "New App"
3. 选择 Git 仓库（GitHub/GitLab）
4. 配置环境变量
5. 点击 "Deploy"

---

## 🔑 当前状态

| 项目 | 状态 |
|------|------|
| flyctl 安装 | ✅ 已完成 |
| Token 认证 | ❌ 失败 |
| 下一步 | 重新登录或生成新 Token |

---

## 💡 建议

由于当前 Token 可能已过期，建议：

1. **最简单**：运行 `fly auth login`，用浏览器登录
2. **最安全**：生成新的 Token（设置较短过期时间）
3. **最快捷**：直接访问 fly.io/dashboard 网页部署

---

## 🔗 相关文档

- Fly.io 文档: https://fly.io/docs/
- flyctl 命令: https://fly.io/docs/flyctl/
- 账户设置: https://fly.io/account
