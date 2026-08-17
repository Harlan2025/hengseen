# 衡简叙约 Hengseen — 项目开发文档

## 项目概述

**衡简叙约** 是一款AI访谈式智能合同生成系统，面向企业法务、经营者、商务人员，覆盖全部常见民商事协议场景。

### 版本信息
- **PRD版本**: V1.4
- **原型版本**: V2
- **开发状态**: 后端框架已搭建

---

## 一、已完成工作

### 1.1 后端项目结构

```
backend/
├── main.py                      # FastAPI入口
├── config.py                    # 配置管理
├── database.py                  # Supabase客户端
├── requirements.txt             # Python依赖
├── .env.example                 # 环境变量模板
├── README.md                    # 项目说明
├── schema.sql                   # 数据库建表语句
│
├── models/
│   ├── __init__.py
│   └── schemas.py               # Pydantic数据模型
│
├── routers/
│   ├── __init__.py
│   ├── auth.py                  # 认证模块（注册/登录/协议同意）
│   ├── projects.py              # 项目模块
│   ├── interview.py             # 访谈模块
│   ├── outline.py               # 大纲模块
│   ├── contract.py              # 合同文本模块
│   ├── export.py                # 导出模块
│   ├── payment.py               # 支付模块
│   ├── custom_content.py        # 自定义内容模块
│   ├── experts.py               # 人工服务模块
│   └── admin.py                 # 后台管理模块
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py            # AI服务封装
│   ├── payment_service.py       # 支付服务封装
│   └── agreement_service.py     # 协议管理服务（V1.4新增）
│
├── middleware/
│   ├── __init__.py
│   └── auth.py                  # JWT认证中间件
│
└── utils/
    ├── __init__.py
    └── helpers.py               # 工具函数
```

### 1.2 核心功能模块

| 模块 | 接口数 | 核心功能 | V1.4新增 |
|------|--------|----------|----------|
| 认证 | 8 | 注册/登录/微信授权/Token刷新/协议同意 | ✅ 协议勾选 |
| 项目 | 7 | 创建/列表/详情/更新/删除/恢复/快照 | |
| 访谈 | 5 | 问答/解析/快照/重置/回溯 | |
| 大纲 | 4 | 生成/获取/编辑/排序 | |
| 合同 | 4 | 生成/获取/编辑/复制 | ✅ 自定义内容 |
| 导出 | 2 | 导出/历史记录 | |
| 支付 | 8 | 创建/查询/微信回调/支付宝回调/二维码/取消/退款 | |
| 自定义内容 | 4 | 列表/创建/更新/删除 | ✅ V1.3新增 |
| 人工服务 | 3 | 列表/创建/删除 | ✅ 公开可见 |
| 后台管理 | 10+ | 定价/模板/专家/退款/协议管理 | ✅ 协议管理 |

### 1.3 数据库表设计（16张表）

| 表名 | 说明 | V1.4新增 |
|------|------|----------|
| users | 用户表 | |
| contract_projects | 项目主表 | |
| interview_snapshot | 访谈快照表 | |
| chat_history | 对话记录表 | |
| outlines | 大纲表 | |
| contract_texts | 合同文本表 | |
| export_files | 导出文件表 | |
| payment_orders | 支付订单表 | |
| refund_applications | 退款申请表 | |
| project_experts | 专家联系人表 | |
| custom_contents | 自定义内容表 | ✅ V1.3 |
| agreements | 协议内容表 | ✅ V1.4 |
| user_agreement_consents | 用户协议同意记录表 | ✅ V1.4 |
| pricing_config | 定价配置表 | |
| team_members | 团队成员表 | |
| audit_logs | 审计日志表 | |

---

## 二、V1.4新增功能：用户协议与隐私政策勾选

### 2.1 核心变更

#### 注册流程
```
用户输入手机号 + 验证码 + 昵称
    ↓
勾选【我已阅读并同意《用户协议》和《隐私政策》】
    ↓
点击注册 → 验证协议勾选 → 创建用户 → 记录同意时间
    ↓
返回 Token
```

#### 登录流程
```
用户输入手机号 + 验证码
    ↓
勾选【我已阅读并同意《用户协议》和《隐私政策》】
    ↓
点击登录 → 验证协议勾选 → 检查协议版本 → 登录成功
    ↓
返回 Token
```

### 2.2 错误码定义

| 错误码 | 含义 | 触发场景 |
|--------|------|----------|
| 7001 | 未同意用户协议 | 注册/登录时未勾选用户协议 |
| 7002 | 未同意隐私政策 | 注册/登录时未勾选隐私政策 |
| 7003 | 协议版本过期 | 协议已更新，需重新同意 |
| 7004 | 协议内容获取失败 | 系统异常 |
| 7005 | 不允许删除激活版本 | 尝试删除当前生效协议 |

### 2.3 数据结构

**协议内容表 (agreements)**
```json
{
  "agreement_id": "uuid",
  "agreement_type": "user_agreement|privacy_policy",
  "title": "用户协议",
  "content": "完整协议文本...",
  "version": "V1.0",
  "is_active": true,
  "created_at": "2026-08-16T10:00:00Z",
  "updated_at": "2026-08-16T12:00:00Z",
  "updated_by": "admin_id"
}
```

**用户同意记录表 (user_agreement_consents)**
```json
{
  "consent_id": "uuid",
  "user_id": "uuid",
  "agreement_type": "user_agreement",
  "version": "V1.0",
  "agreed_at": "2026-08-16T10:00:00Z",
  "ip_address": "192.168.1.1",
  "device_info": "Mozilla/5.0...",
  "is_current": true
}
```

### 2.4 API接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/auth/register` | POST | 用户注册（必须勾选协议） |
| `/api/v1/auth/login` | POST | 用户登录（必须勾选协议） |
| `/api/v1/auth/wechat` | POST | 微信授权登录 |
| `/api/v1/auth/refresh` | POST | 刷新Token |
| `/api/v1/auth/logout` | POST | 退出登录 |
| `/api/v1/auth/me` | GET | 获取当前用户信息 |
| `/api/v1/auth/agreements` | GET | 获取当前协议内容 |
| `/api/v1/auth/agreement-consent` | GET | 获取用户协议同意记录 |

**后台管理接口**
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/admin/agreements` | GET | 获取协议列表 |
| `/api/v1/admin/agreements/:id` | GET | 获取协议详情 |
| `/api/v1/admin/agreements` | POST | 创建新协议版本 |
| `/api/v1/admin/agreements/:id` | PUT | 更新协议内容 |
| `/api/v1/admin/agreements/:id` | DELETE | 删除协议版本 |
| `/api/v1/admin/agreements/:id/consents` | GET | 获取同意统计 |

---

## 三、技术架构

### 3.1 整体架构
```
前端三端（Web/APP/小程序）
        ↓
Cloudflare（CDN、边缘路由、安全防护）
        ↓
FastAPI后端（本仓库）
        ↓
Supabase（认证、数据库、存储、实时通信）
        ↓
AI服务（DeepSeek/Qwen）
        ↓
微信支付 / 支付宝
```

### 3.2 技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| 前端 | React/Vue3 + TypeScript | Web端；Flutter跨端；原生小程序 |
| 后端 | FastAPI + Python 3.11 | 高性能异步框架 |
| 数据库 | Supabase (PostgreSQL) | 自带认证、实时订阅、存储 |
| 认证 | Supabase Auth + JWT | 手机号、微信授权 |
| AI | DeepSeek/Qwen (OpenAI兼容) | 访谈生成、合同起草 |
| 支付 | 微信支付 + 支付宝 | 扫码支付 |
| CDN | Cloudflare | 边缘缓存、DDoS防护 |

### 3.3 关键设计决策

1. **边缘层优先**：Cloudflare处理静态资源、安全防护、边缘路由
2. **RLS行级安全**：Supabase强制数据隔离，用户只能访问自己的数据
3. **AI服务解耦**：AI不掌控业务流程，只负责内容生成
4. **Token成本控制**：单份合同生成目标 ≤ 5元
5. **匿名先用**：降低使用门槛，付费前可自由体验

---

## 四、部署指南

### 4.1 本地开发环境

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑.env填写：
#   - SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_KEY
#   - JWT_SECRET_KEY
#   - AI_API_KEY (DeepSeek)
#   - WECHAT_PAY_MCHID / WECHAT_PAY_API_KEY
#   - ALIPAY_APP_ID / ALIPAY_PRIVATE_KEY

# 3. 初始化数据库
# 在Supabase控制台执行 schema.sql

# 4. 运行开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4.2 生产部署

```bash
# 使用Docker部署
docker build -t hengseen-backend .
docker run -p 8000:8000 --env-file .env hengseen-backend
```

### 4.3 环境变量清单

| 变量名 | 说明 | 必填 |
|--------|------|------|
| SUPABASE_URL | Supabase项目URL | ✅ |
| SUPABASE_ANON_KEY | 公开密钥 | ✅ |
| SUPABASE_SERVICE_KEY | 服务角色密钥 | ✅ |
| JWT_SECRET_KEY | JWT签名密钥 | ✅ |
| AI_BASE_URL | AI服务地址 | ✅ |
| AI_API_KEY | AI服务API密钥 | ✅ |
| WECHAT_PAY_MCHID | 商户号 | 条件 |
| ALIPAY_APP_ID | 应用ID | 条件 |

---

## 五、待办事项

### 5.1 后端开发（高优先级）

- [ ] 实现完整的JWT认证逻辑
- [ ] 对接Supabase Auth（手机号短信验证码）
- [ ] 实现微信授权登录
- [ ] 集成DeepSeek/Qwen AI服务
- [ ] 实现微信支付完整流程
- [ ] 实现支付宝完整流程
- [ ] 添加请求限流中间件
- [ ] 实现审计日志自动写入

### 5.2 前端开发

- [ ] 搭建React/Vue3项目
- [ ] 实现登录注册页面（含协议勾选）
- [ ] 实现首页仪表盘
- [ ] 实现项目列表页
- [ ] 实现访谈对话界面
- [ ] 实现大纲编辑页
- [ ] 实现合同预览页
- [ ] 实现支付页面
- [ ] 实现个人中心页

### 5.3 运营配置

- [ ] 编写用户协议和隐私政策正文
- [ ] 配置定价策略
- [ ] 审核风险知识库
- [ ] 配置AI Prompt模板

---

## 六、参考资料

- [PRD V1.4](../PRD及接口清单/PRD_V1.4_新增协议勾选功能.md)
- [接口清单 V1.4](../PRD及接口清单/接口清单_V1.4_新增协议勾选功能.md)
- [原型 V2](../原型_Hengseen_Proto_v2.html)
- [品牌VI](../品牌LOGO及VI/)

---

## 七、版本历史

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-08-16 | V0.1 | 搭建后端框架，完成V1.4核心模块 |
