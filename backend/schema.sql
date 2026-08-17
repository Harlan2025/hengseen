-- 衡简叙约数据库Schema
-- Supabase PostgreSQL

-- 1. 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
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
    project_id UUID PRIMARY KEY,
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
    snapshot_id UUID PRIMARY KEY,
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    step INTEGER DEFAULT 0,
    confirmed_elements JSONB DEFAULT '[]',
    pending_elements JSONB DEFAULT '[]',
    risks JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. 对话记录表
CREATE TABLE IF NOT EXISTS chat_history (
    message_id UUID PRIMARY KEY,
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. 大纲表
CREATE TABLE IF NOT EXISTS outlines (
    outline_id UUID PRIMARY KEY,
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
    export_id UUID PRIMARY KEY,
    project_id UUID REFERENCES contract_projects(project_id),
    user_id UUID REFERENCES users(user_id),
    format TEXT,
    file_url TEXT,
    exported_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. 支付订单表
CREATE TABLE IF NOT EXISTS payment_orders (
    order_id UUID PRIMARY KEY,
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
    refund_id UUID PRIMARY KEY,
    order_id UUID REFERENCES payment_orders(order_id),
    user_id UUID REFERENCES users(user_id),
    reason TEXT,
    status TEXT DEFAULT 'pending',
    applied_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ
);

-- 10. 专家联系人表
CREATE TABLE IF NOT EXISTS project_experts (
    expert_id UUID PRIMARY KEY,
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
    custom_content_id UUID PRIMARY KEY,
    project_id UUID REFERENCES contract_projects(project_id) ON DELETE CASCADE,
    chapter_id TEXT,
    content_type TEXT DEFAULT 'custom',
    content TEXT NOT NULL,
    inserted_at TIMESTAMPTZ DEFAULT NOW(),
    inserted_by UUID REFERENCES users(user_id)
);

-- 12. 协议内容表 (V1.4新增)
CREATE TABLE IF NOT EXISTS agreements (
    agreement_id UUID PRIMARY KEY,
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
    consent_id UUID PRIMARY KEY,
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

-- 初始化定价配置
INSERT INTO pricing_config (key, fixed_threshold, fixed_price, multiplier)
VALUES ('pricing', 2.0, 5.99, 2.0)
ON CONFLICT (key) DO NOTHING;

-- 初始化默认协议
INSERT INTO agreements (agreement_id, agreement_type, title, content, version, is_active)
VALUES 
('ua-default', 'user_agreement', '用户协议', '欢迎使用衡简叙约...\n\n一、协议范围\n本服务协议...', 'V1.0', TRUE),
('pp-default', 'privacy_policy', '隐私政策', '我们重视您的隐私...\n\n一、信息收集\n...', 'V1.0', TRUE)
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
