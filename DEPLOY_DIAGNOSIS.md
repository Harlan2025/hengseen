# 🔧 Fly.io 部署问题诊断

## 当前状态
- ✅ GitHub 最新代码已拉取（commit `2de3e96`）
- ✅ `fly.toml` 配置正确（使用 nixpacks）
- ❌ 构建失败：`unauthorized`

## 错误原因
Token 权限不足或需要重新认证。

---

## 解决方案

### 方案 1：重新登录 Fly.io CLI（推荐）

运行以下命令，会打开浏览器让你登录：
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

登录后执行部署：
```powershell
cd "F:/hermes/2 Mike/衡简叙约"
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy --strategy immediate
```

### 方案 2：生成新的 Full Access Token

1. 访问：**https://fly.io/account/tokens**
2. 删除旧 Token
3. 生成新 Token：
   - Name: `hengseen-full-access-2`
   - **权限**: 选择 **"Full access"**
   - Expiry: `30 days`
4. 复制新 Token 发给我

### 方案 3：通过 Dashboard 手动部署

1. 访问：**https://fly.io/apps/hengseen-backend**
2. 点击左侧菜单 **"Settings"**
3. 找到 **"Deploy"** 部分
4. 点击 **"Redeploy"** 按钮

---

## 当前配置

```toml
app = "hengseen-backend"

[build]
  builder = "nixpacks"  # 已使用 nixpacks

[deploy]
  health_check_path = "/health"
  health_check_timeout_seconds = 30
```

---

## 验证本地修复成功

```bash
# 登录测试
curl http://localhost:8000/api/v1/auth/login \
  -X POST -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目测试
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

✅ 应该返回成功

---

**请尝试方案 1：运行 `flyctl auth login` 重新登录，然后重试部署！**
