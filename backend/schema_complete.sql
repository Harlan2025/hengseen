-- 衡简叙约完整建表SQL - 按顺序执行
-- 复制到 Supabase SQL Editor

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth_id TEXT,
    phone TEXT UNIQUE,
    nickname TEXT,
    avatar_url TEXT,
    login_type TEXT DEFAULT 'phone',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 合同项目表
CREATE TABLE IF NOT EXISTS contract_projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    name TEXT NOT NULL,
    primary_type TEXT NOT NULL,
    secondary_types TEXT[] DEFAULT '{}',
    status TEXT DEFAULT 'init',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- 3. 访谈快照表
CREATE TABLE IF NOT EXISTS interview_snapshot (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    step INTEGER DEFAULT 0,
    confirmed_elements JSONB DEFAULT '[]',
    pending_elements JSONB DEFAULT '[]',
    risks JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 对话记录表
CREATE TABLE IF NOT EXISTS chat_history (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. 大纲表
CREATE TABLE IF NOT EXISTS outlines (
    outline_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    chapters JSONB DEFAULT '[]',
    risks JSONB DEFAULT '[]',
    generated_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

-- 6. 合同文本表
CREATE TABLE IF NOT EXISTS contract_texts (
    project_id UUID PRIMARY KEY REFERENCES contract_projects(project_id),
    contract_text TEXT,
    risk_notes JSONB DEFAULT '[]',
    has_custom_content BOOLEAN DEFAULT FALSE,
    generated_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ
);

-- 7. 导出文件表
CREATE TABLE IF NOT EXISTS export_files (
    export_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id),
    user_id UUID REFERENCES users(user_id),
    format TEXT,
    file_url TEXT,
    exported_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. 支付订单表
CREATE TABLE IF NOT EXISTS payment_orders (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id),
    user_id UUID REFERENCES users(user_id),
    amount DECIMAL(10,2) NOT NULL,
    payment_method TEXT,
    status TEXT DEFAULT 'pending',
    transaction_id TEXT,
    expire_at TIMESTAMPTZ,
    paid_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. 退款申请表
CREATE TABLE IF NOT EXISTS refund_applications (
    refund_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES payment_orders(order_id),
    user_id UUID REFERENCES users(user_id),
    reason TEXT,
    status TEXT DEFAULT 'pending',
    applied_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);

-- 10. 专家联系人表
CREATE TABLE IF NOT EXISTS project_experts (
    expert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    expert_name TEXT NOT NULL,
    title TEXT,
    wechat TEXT,
    qq TEXT,
    email TEXT,
    tags TEXT[] DEFAULT '{}',
    is_public BOOLEAN DEFAULT FALSE,
    added_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. 自定义内容表
CREATE TABLE IF NOT EXISTS custom_contents (
    custom_content_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    chapter_id TEXT,
    content_type TEXT DEFAULT 'custom',
    content TEXT NOT NULL,
    inserted_at TIMESTAMPTZ DEFAULT NOW(),
    inserted_by UUID REFERENCES users(user_id)
);

-- 12. 协议内容表 (V1.4新增)
CREATE TABLE IF NOT EXISTS agreements (
    agreement_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agreement_type TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    version TEXT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    updated_by UUID REFERENCES users(user_id)
);

-- 13. 用户协议同意记录表 (V1.4新增)
CREATE TABLE IF NOT EXISTS user_agreement_consents (
    consent_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    agreement_type TEXT NOT NULL,
    version TEXT NOT NULL,
    agreed_at TIMESTAMPTZ DEFAULT NOW(),
    ip_address TEXT,
    device_info TEXT,
    is_current BOOLEAN DEFAULT TRUE
);

-- 14. 定价配置表
CREATE TABLE IF NOT EXISTS pricing_config (
    key TEXT PRIMARY KEY,
    fixed_threshold DECIMAL(10,2) DEFAULT 2.0,
    fixed_price DECIMAL(10,2) DEFAULT 5.99,
    multiplier DECIMAL(10,2) DEFAULT 2.0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 15. 团队成员表
CREATE TABLE IF NOT EXISTS team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id),
    role TEXT DEFAULT 'viewer',
    invited_by UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 16. 审计日志表
CREATE TABLE IF NOT EXISTS audit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id),
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 初始化数据
INSERT INTO pricing_config (key, fixed_threshold, fixed_price, multiplier)
VALUES ('pricing', 2.0, 5.99, 2.0)
ON CONFLICT (key) DO NOTHING;

INSERT INTO agreements (agreement_type, title, content, version, is_active)
VALUES 
('user_agreement', '用户协议', '欢迎使用衡简叙约！

一、协议范围
本协议是您与衡简叙约之间关于使用本服务所订立的协议。

二、服务内容
衡简叙约提供AI访谈式合同生成服务，帮助用户快速起草各类商事合同。

三、用户权利
1. 用户有权随时删除自己的项目数据
2. 用户可申请导出个人数据
3. 用户可申请删除个人数据

四、隐私保护
我们重视您的隐私，仅收集必要信息，并采取加密措施保护数据安全。

五、免责声明
本平台生成的合同文本仅供参考，不构成法律意见。重大交易请咨询专业律师。

六、协议变更
我们可能会更新本协议，更新后的协议将在平台公示。

七、联系方式
如有疑问，请联系客服邮箱：support@hengseen.com', 'V1.0', TRUE),
('privacy_policy', '隐私政策', '衡简叙约隐私政策

一、信息收集
我们仅收集提供服务所必需的信息：
- 手机号（用于注册和登录）
- 昵称（可选）
- 项目数据（合同相关内容）

二、信息使用
收集的信息仅用于：
- 提供合同约定的服务
- 改进产品质量
- 发送服务通知

三、信息存储
- 所有数据加密存储
- 采用行级安全策略隔离用户数据
- 匿名用户数据7天后自动清理

四、信息共享
我们不会向第三方共享您的个人信息，除非：
- 获得您的明确同意
- 法律法规要求
- 必要的服务提供商（如支付渠道）

五、您的权利
- 访问您的个人信息
- 更正不准确的信息
- 删除您的账户和数据
- 撤回同意

六、数据安全
我们采取合理的安全措施保护您的数据，包括加密传输和存储。

七、未成年人保护
我们不会故意收集未成年人的个人信息。

八、政策更新
本政策可能会更新，更新后的政策将在平台公示。', 'V1.0', TRUE)
ON CONFLICT DO NOTHING;

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_projects_user_id ON contract_projects(user_id);
CREATE INDEX IF NOT EXISTS idx_snapshots_project_id ON interview_snapshot(project_id);
CREATE INDEX IF NOT EXISTS idx_chats_project_id ON chat_history(project_id);
CREATE INDEX IF NOT EXISTS idx_exports_project_id ON export_files(project_id);
CREATE INDEX IF NOT EXISTS idx_payments_order_id ON payment_orders(order_id);
CREATE INDEX IF NOT EXISTS idx_payments_project_id ON payment_orders(project_id);
CREATE INDEX IF NOT EXISTS idx_experts_project_id ON project_experts(project_id);
CREATE INDEX IF NOT EXISTS idx_custom_contents_project_id ON custom_contents(project_id);
CREATE INDEX IF NOT EXISTS idx_consents_user_id ON user_agreement_consents(user_id);
CREATE INDEX IF NOT EXISTS idx_consents_user_agreement ON user_agreement_consents(user_id, agreement_type);
CREATE INDEX IF NOT EXISTS idx_agreements_type ON agreements(agreement_type);
CREATE INDEX IF NOT EXISTS idx_agreements_active ON agreements(is_active);
