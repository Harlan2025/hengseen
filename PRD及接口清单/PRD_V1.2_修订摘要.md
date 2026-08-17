# 衡简叙约 PRD V1.2 修订摘要

## 修订时间
2026-08-16

---

## 一、新增功能概览

| 功能模块 | 变更类型 | 核心内容 |
|---------|---------|---------|
| 人工服务 | 新增 | 专家联系方式管理、一键复制、引导提示 |
| 付费下载 | 新增 | 定价策略、支付流程、微信/支付宝对接 |
| AI集成方案 | 新增 | OpenAI兼容接口、模型选型、调用规范 |

---

## 二、人工服务模块详解

### 2.1 功能设计

**使用场景：**
1. 访谈前：提示用户可添加专家微信进行预咨询
2. 生成合同后：建议用户联系专业律师审核条款
3. 导出时：展示已绑定的专家联系方式

**数据结构：**
```json
{
  "expert_id": "uuid",
  "project_id": "uuid",
  "expert_name": "张律师",
  "title": "商事合同专家",
  "wechat": "zhang_lawyer",
  "qq": "123456789",
  "email": "zhang@example.com",
  "tags": ["合同纠纷", "股权投资"]
}
```

**接口列表（5个）：**
- `GET /projects/:id/experts` — 获取专家列表
- `POST /projects/:id/experts` — 添加专家
- `PATCH /projects/:id/experts/:expert_id` — 修改信息
- `DELETE /projects/:id/experts/:expert_id` — 删除专家
- `POST /projects/:id/experts/:expert_id/copy` — 复制联系方式

---

## 三、付费下载机制详解

### 3.1 定价策略

| Token成本 | 用户支付金额 | 示例 |
|-----------|-------------|------|
| ≤ 2元 | 5.99元（固定价） | 简单买卖合同 |
| > 2元 | 成本的2倍 | 复杂股权交易 |

### 3.2 支付流程

```
用户点击「下载合同」
    ↓
系统计算Token成本 → 判断价格档位
    ↓
创建支付订单 → 返回金额和二维码
    ↓
展示支付二维码（微信/支付宝）
    ↓
用户扫码支付
    ↓
支付回调 → 更新订单状态
    ↓
解锁下载/复制权限
```

### 3.3 支付状态机

```
pending（待支付，30分钟）
    ↓ 用户扫码
paid（已支付）→ 解锁下载
    ↓
expired（已过期）
```

### 3.4 接口列表（6个）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/projects/:id/orders` | POST | 创建订单 |
| `/orders/:id` | GET | 查询订单状态 |
| `/orders/:id/qr` | GET | 获取二维码 |
| `/orders/:id/cancel` | POST | 取消订单 |
| `/payments/wechat/callback` | POST | 微信回调 |
| `/payments/alipay/callback` | POST | 支付宝回调 |

### 3.5 收益预估

| 指标 | 数值 |
|------|------|
| 月订单数 | 400单 |
| 平均客单价 | 5.99元 |
| 月营收 | 2400元 |
| AI成本 | 52元（400×0.13元） |
| **月毛利** | **2348元** |

---

## 四、AI服务对接方案

### 4.1 技术选型

**核心决策：使用OpenAI兼容接口**

所有主流大模型厂商均提供OpenAI兼容接口，系统统一标准调用，便于切换模型。

| 模型 | 厂商 | 适用场景 | 成本 |
|------|------|---------|------|
| deepseek-chat | DeepSeek | 访谈对话、合同生成 | 极低 |
| deepseek-coder | DeepSeek | 结构化解析、JSON输出 | 极低 |
| qwen-plus | 阿里云 | 风险识别 | 低 |

**推荐配置：**
- **主模型**：deepseek-chat
- **备用模型**：qwen-plus
- **结构化输出**：deepseek-coder

### 4.2 接口对接方式

#### 环境变量配置
```bash
AI_API_KEY=sk-xxxxx
AI_BASE_URL=https://api.deepseek.com/v1
AI_MODEL=deepseek-chat
AI_FALLBACK_MODEL=qwen-plus
AI_FALLBACK_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

#### Python调用示例
```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.getenv("AI_API_KEY"),
    base_url=os.getenv("AI_BASE_URL")
)

# 通用对话接口
response = await client.chat.completions.create(
    model=os.getenv("AI_MODEL"),
    messages=[
        {"role": "system", "content": "You are a legal assistant..."},
        {"role": "user", "content": user_answer}
    ],
    temperature=0.3,
    max_tokens=2000
)
```

### 4.3 访谈对话流程

```
用户回答
    ↓
后端组装Prompt（含系统提示词+历史上下文）
    ↓
调用AI接口 → 返回结构化JSON
    ↓
解析确认事实、待确认事项、新风险
    ↓
更新快照 → 返回下一轮问题
```

### 4.4 合同生成流程

```
收集访谈快照
    ↓
组装完整上下文（压缩后的要素+大纲+风险）
    ↓
调用AI生成合同文本
    ↓
插入风险标注（⚠️标记）
    ↓
返回合同内容+风险提示章节
```

### 4.5 成本优化策略

1. **上下文压缩**：只保留关键要素，去除冗余对话
   - 效果：减少约40% Token消耗

2. **分段生成**：先主体后附录，单次Prompt控制在6000 tokens内
   - 效果：避免超长Prompt导致的成本激增

3. **冷启动预加载**：行业通用条款预置
   - 效果：减少约30%生成长度

### 4.6 Token成本对比

| 模型 | 单合同成本 | 月成本（400单） |
|------|-----------|----------------|
| deepseek-chat | 0.13元 | 52元 |
| qwen-plus | 0.40元 | 160元 |
| GPT-4o | 2.60元 | 1040元 |

**结论：推荐使用DeepSeek模型，成本仅为GPT-4的1/20**

### 4.7 故障转移机制

```
主模型调用成功 → 返回结果
    ↓ 超时/报错
备用模型调用
    ↓ 仍然失败
返回错误码3001，提示「AI服务繁忙」
```

### 4.8 监控指标

| 指标 | 告警阈值 |
|------|---------|
| 单次调用成本 | > 0.5元 |
| 日总成本 | > 100元 |
| 超时率 | > 5% |
| 错误率 | > 2% |

---

## 五、支付接入说明

### 5.1 微信支付接入

**必要条件：**
- 微信公众号或小程序已认证
- 开通微信支付功能
- 获取商户号（mch_id）
- 配置API密钥（v3版本）

**核心流程：**
```
1. 后端调用微信统一下单API
2. 获取prepay_id
3. 生成二维码（内容为微信支付码）
4. 前端展示二维码
5. 用户扫码支付
6. 微信异步回调通知
7. 后端验证签名，更新订单
8. 解锁下载权限
```

### 5.2 支付宝接入

**必要条件：**
- 支付宝商家账号
- 开通当面付/电脑网站支付
- 获取APPID和私钥
- 配置支付宝公钥

**核心流程：**
```
1. 后端调用支付宝统一收单API
2. 生成支付字符串
3. 前端展示二维码
4. 用户扫码支付
5. 支付宝异步通知
6. 后端验签，更新订单
7. 解锁下载权限
```

### 5.3 安全注意事项

1. **签名验证**：所有回调必须验证签名
2. **幂等处理**：同一订单重复回调只处理一次
3. **金额校验**：回调金额必须与订单一致
4. **日志记录**：完整记录支付流水
5. **异常监控**：支付失败率、回调延迟监控

---

## 六、新增数据表

### 6.1 project_experts（项目专家联系人表）

| 字段 | 类型 | 说明 |
|------|------|------|
| expert_id | uuid | 主键 |
| project_id | uuid | 关联项目 |
| expert_name | text | 专家姓名 |
| wechat | text | 微信号 |
| qq | text | QQ号 |
| email | text | 邮箱 |
| tags | text[] | 专业领域标签 |

### 6.2 payment_orders（支付订单表）

| 字段 | 类型 | 说明 |
|------|------|------|
| order_id | uuid | 主键 |
| amount | numeric | 应付金额 |
| token_cost | numeric | Token成本 |
| status | text | pending/paid/expired |
| pay_channel | text | wechat/alipay |
| transaction_id | text | 第三方流水号 |

### 6.3 payment_logs（支付日志表）

记录每次支付事件（创建、成功、过期、回调），便于对账。

---

## 七、文件清单

| 文件名 | 说明 |
|--------|------|
| PRD_V1.2_新增人工服务与付费机制.md | 完整PRD文档（V1.2） |
| 接口清单_V1.2_新增人工服务与支付.md | 46个接口完整定义 |
| PRD_V1.2_修订摘要.md | 本文件 |

---

## 八、待确认事项

1. **专家联系方式使用范围**：是否允许用户公开分享专家信息？
2. **支付退款策略**：用户不满意合同质量，是否支持退款？
3. **订单过期后数据**：过期订单的合同是否保留？保留多久？
4. **专家资质审核**：是否需要人工审核专家资质？
5. **定价调整机制**：是否允许后台动态调整定价策略？
