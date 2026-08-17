# 衡简叙约 Hengseen - AI访谈式合同生成系统

> 基于 AI 访谈的智能化合同生成平台，支持买卖、劳动、知识产权等多种合同类型

## 技术栈

### 后端
- **框架**: FastAPI + Python 3.11
- **数据库**: Supabase (PostgreSQL)
- **认证**: JWT + passlib
- **AI服务**: DeepSeek API
- **支付**: 微信支付 + 支付宝

### 前端
- **框架**: Vue 3 + TypeScript
- **构建**: Vite
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP**: Axios

## 功能特性

- 🤖 AI 访谈式合同生成
- 📝 多种合同类型支持（买卖、劳动、知识产权等）
- 💳 在线支付集成
- 🔐 JWT 用户认证
- 📄 Word/Markdown 导出
- 🎨 响应式设计

## 快速开始

### 后端开发

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 填写配置
python main.py
# 访问 http://localhost:8000/docs
```

### 前端开发

```bash
cd frontend
npm install
cp .env.example .env.local
# 编辑 .env.local 填写配置
npm run dev
# 访问 http://localhost:3000
```

## 部署

详细部署文档请查看: [deploy/README.md](./deploy/README.md)

### 一键部署

- **后端**: Railway / Render
- **前端**: Vercel / Netlify
- **CI/CD**: GitHub Actions

## 环境变量

| 类别 | 必填 | 变量名 |
|------|------|--------|
| 后端 | ✅ | SUPABASE_URL, SUPABASE_SERVICE_KEY, JWT_SECRET_KEY |
| 后端 | ✅ | AI_API_KEY, AI_BASE_URL |
| 后端 | ❌ | WECHAT_PAY_*, ALIPAY_* |
| 前端 | ✅ | VITE_API_URL |
| 前端 | ❌ | VITE_SUPABASE_* |

详见 [deploy/ENVIRONMENT_VARIABLES.md](./deploy/ENVIRONMENT_VARIABLES.md)

## 项目结构

```
衡简叙约/
├── backend/              # FastAPI 后端
│   ├── main.py          # 入口文件
│   ├── config.py        # 配置管理
│   ├── database.py      # 数据库连接
│   ├── routers/         # API 路由
│   ├── services/        # 业务逻辑
│   └── models/          # 数据模型
│
├── frontend/            # Vue 3 前端
│   ├── src/
│   │   ├── views/      # 页面组件
│   │   ├── components/ # 通用组件
│   │   ├── stores/     # Pinia 状态
│   │   └── api/        # API 请求
│   └── vercel.json     # 部署配置
│
├── deploy/             # 部署文档
│   ├── README.md
│   └── ENVIRONMENT_VARIABLES.md
│
└── .github/workflows/  # CI/CD
    ├── ci-cd.yml
    └── docker-build.yml
```

## 许可证

MIT License
