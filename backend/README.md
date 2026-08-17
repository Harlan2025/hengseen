# 衡简叙约 Hengseen — 后端项目

## 技术栈
- **框架**: FastAPI (Python 3.11+)
- **数据库**: Supabase (PostgreSQL)
- **认证**: Supabase Auth (JWT)
- **AI服务**: OpenAI兼容接口 (DeepSeek/Qwen)
- **支付**: 微信支付 + 支付宝

## 项目结构
```
backend/
├── main.py                 # FastAPI入口
├── config.py               # 配置管理
├── database.py             # Supabase客户端
├── dependencies.py         # 依赖注入（用户认证等）
├── routers/
│   ├── auth.py             # 认证模块（注册/登录/协议同意）
│   ├── projects.py         # 项目模块
│   ├── interview.py        # 访谈模块
│   ├── outline.py          # 大纲模块
│   ├── contract.py         # 合同文本模块
│   ├── export.py           # 导出模块
│   ├── payment.py          # 支付模块
│   ├── custom_content.py   # 自定义内容模块
│   ├── experts.py          # 人工服务模块
│   └── admin.py            # 后台管理模块
├── services/
│   ├── ai_service.py       # AI服务封装
│   ├── wechat_pay.py       # 微信支付
│   ├── alipay_service.py   # 支付宝
│   └── agreement_service.py # 协议管理
├── models/
│   └── schemas.py          # Pydantic模型
├── middleware/
│   └── auth.py             # JWT认证中间件
└── utils/
    └── helpers.py          # 工具函数
```

## 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
cp .env.example .env
# 编辑.env填写配置

# 运行开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
