# 衡简叙约 - Railway 部署指南

## 一键部署步骤

### 1. 准备代码

确保代码已推送到 GitHub：
```bash
cd "F:/hermes/2 Mike/衡简叙约"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/hengseen.git
git push -u origin main
```

### 2. Railway 部署

1. 访问 https://railway.app
2. 登录（支持 GitHub 登录）
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择 `hengseen` 仓库
6. 选择 `backend` 文件夹作为 root

### 3. 配置环境变量

在 Railway Dashboard 中添加以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| SUPABASE_URL | https://rtmldrysnwzbkgiihnuc.supabase.co | Supabase 地址 |
| SUPABASE_SERVICE_KEY | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... | Supabase 服务密钥 |
| JWT_SECRET_KEY | your-secret-key-here | JWT 签名密钥（随机生成） |
| AI_PROVIDER | agnes | AI 提供商 |
| AI_AGNES_API_KEY | sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5 | Agnes API 密钥 |
| AI_AGNES_BASE_URL | https://api.sapiens.ai/v1 | Agnes API 地址 |
| DOMAIN | https://api.hengseen.com | 后端域名 |
| PORT | 8000 | 端口号 |

**JWT_SECRET_KEY 生成方法**：
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. 等待部署完成

- Railway 会自动检测 FastAPI 项目
- 自动安装依赖（requirements.txt）
- 自动启动服务
- 部署完成后会提供 URL：`https://hengseen-backend-xxx.up.railway.app`

### 5. 验证部署

```bash
# 测试健康检查
curl https://hengseen-backend-xxx.up.railway.app/health

# 测试登录
curl -X POST https://hengseen-backend-xxx.up.railway.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'
```

### 6. 更新前端 API 地址

编辑 `frontend/.env.production`：
```bash
VITE_API_URL=https://hengseen-backend-xxx.up.railway.app/api/v1
```

重新构建并部署前端：
```bash
cd frontend
npm run build
wrangler pages deploy dist --project-name=hengseen
```

---

## Railway 控制台操作

### 查看日志
1. 进入项目
2. 点击 Service
3. 点击 "Logs" 标签

### 重启服务
1. 点击 "Actions"
2. 选择 "Restart"

### 添加自定义域名（可选）
1. 进入 Settings
2. 点击 "Domains"
3. 添加自定义域名
4. 配置 DNS CNAME 记录

---

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 构建失败 | 检查 requirements.txt 是否完整 |
| 启动失败 | 检查环境变量是否正确配置 |
| CORS 错误 | 检查 CORS 中间件配置 |
| 数据库连接失败 | 检查 SUPABASE_URL 和 SERVICE_KEY |
| AI 调用失败 | 检查 AI_API_KEY 是否正确 |

---

## 费用说明

Railway 免费额度：
- 512 MB 内存
- 200 GB 出站流量/月
- 5 GB 磁盘空间

超出后按量计费：
- 内存：$0.50/GB/小时
- 流量：$0.10/GB

预计月费用：$5-10（根据访问量）
