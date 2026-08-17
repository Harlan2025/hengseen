# 衡简叙约 V1.4 部署环境变量清单
# ==============================

## 后端环境变量 (.env)
# 复制到 backend/.env 并填写实际值

# Supabase 数据库配置（必需）
SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
SUPABASE_ANON_KEY=【从Supabase控制台获取】
SUPABASE_SERVICE_KEY=【从Supabase控制台获取，service_role密钥】

# JWT 认证配置（必需）
JWT_SECRET_KEY=【生成随机密钥：python -c "import secrets; print(secrets.token_urlsafe(32))"】
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI 服务配置（必需）
AI_BASE_URL=https://api.deepseek.com/v1
AI_API_KEY=【DeepSeek API密钥】
AI_MODEL=deepseek-chat
AI_MAX_TOKENS=4096
AI_MODE=real

# 域名配置（生产环境必需）
DOMAIN=https://hengseen.com

# 微信支付配置（可选，如需支付功能）
WECHAT_PAY_MCHID=
WECHAT_PAY_API_KEY=
WECHAT_PAY_CERT_PATH=/path/to/cert.pem
WECHAT_PAY_PRIVATE_KEY_PATH=/path/to/private_key.pem
WECHAT_PAY_NOTIFY_URL=https://api.hengseen.com/api/v1/payment/wechat/notify

# 支付宝配置（可选，如需支付功能）
ALIPAY_APP_ID=
ALIPAY_PRIVATE_KEY=
ALIPAY_PUBLIC_KEY=
ALIPAY_NOTIFY_URL=https://api.hengseen.com/api/v1/payment/alipay/notify

# 调试配置（开发环境设为true）
DEBUG=false


## 前端环境变量 (.env.local 或 Vercel/Netlify环境变量)
# 复制到 frontend/.env.local 或平台后台配置

# API 地址（必需）
VITE_API_URL=https://api.hengseen.com/api/v1

# 应用信息
VITE_APP_NAME=衡简叙约
VITE_APP_VERSION=1.4.0

# Supabase配置（如前端直接访问）
VITE_SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
VITE_SUPABASE_ANON_KEY=【与后端相同】

# 功能开关
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_DEBUG_LOGS=false


## 平台特定配置
# ==========================

### Railway 部署
# 在 Railway Dashboard → Variables 中设置：
# SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY
# JWT_SECRET_KEY, AI_API_KEY, AI_BASE_URL, AI_MODEL
# DOMAIN

### Render 部署
# 在 Render Dashboard → Environment 中设置相同变量

### Vercel 部署
# 在项目 Settings → Environment Variables 中设置前端变量
# VITE_API_URL, VITE_APP_NAME, VITE_APP_VERSION
# （注意：Vercel会自动将 .env.production 中的变量注入构建环境）

### Netlify 部署
# 在 Site Settings → Build & Deploy → Environment 中设置
# VITE_API_URL, VITE_APP_NAME


## 安全建议
# ==========================
# 1. JWT_SECRET_KEY 使用强随机密钥，至少32字符
# 2. 不要将 .env 文件提交到 Git
# 3. 生产环境关闭 DEBUG 模式
# 4. AI_API_KEY 定期轮换
# 5. 使用 HTTPS 域名
# 6. 定期备份数据库


## 验证清单
# ==========================
# [ ] 后端能正常启动并响应 /health 端点
# [ ] Supabase 连接成功，能查询数据
# [ ] AI 服务能正常调用
# [ ] JWT 认证成功/失败流程正常
# [ ] 前端能访问后端 API
# [ ] 所有环境变量已正确配置
