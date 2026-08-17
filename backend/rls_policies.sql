-- 衡简叙约 RLS 策略配置
-- 在 Supabase SQL Editor 中执行

-- 1. 为 agreements 表启用 RLS
ALTER TABLE agreements ENABLE ROW LEVEL SECURITY;

-- 2. 创建 agreements 表的 RLS 策略
DROP POLICY IF EXISTS "agreements_public_read" ON agreements;
CREATE POLICY "agreements_public_read" ON agreements
    FOR SELECT USING (is_active = true);

DROP POLICY IF EXISTS "agreements_admin_all" ON agreements;
CREATE POLICY "agreements_admin_all" ON agreements
    FOR ALL USING (auth.jwt() ->> 'role' = 'service_role');

-- 3. 为 users 表启用 RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 4. 创建 users 表的 RLS 策略
DROP POLICY IF EXISTS "users_public_read" ON users;
CREATE POLICY "users_public_read" ON users
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "users_insert" ON users;
CREATE POLICY "users_insert" ON users
    FOR INSERT WITH CHECK (true);

DROP POLICY IF EXISTS "users_update_own" ON users;
CREATE POLICY "users_update_own" ON users
    FOR UPDATE USING (auth.uid()::text = user_id::text);

DROP POLICY IF EXISTS "users_delete_own" ON users;
CREATE POLICY "users_delete_own" ON users
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- 5. 为 contract_projects 表启用 RLS
ALTER TABLE contract_projects ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "projects_select" ON contract_projects;
CREATE POLICY "projects_select" ON contract_projects
    FOR SELECT USING (
        user_id = auth.uid()::text OR
        status = 'public'
    );

DROP POLICY IF EXISTS "projects_insert" ON contract_projects;
CREATE POLICY "projects_insert" ON contract_projects
    FOR INSERT WITH CHECK (auth.uid()::text = user_id::text);

DROP POLICY IF EXISTS "projects_update" ON contract_projects;
CREATE POLICY "projects_update" ON contract_projects
    FOR UPDATE USING (auth.uid()::text = user_id::text);

DROP POLICY IF EXISTS "projects_delete" ON contract_projects;
CREATE POLICY "projects_delete" ON contract_projects
    FOR DELETE USING (auth.uid()::text = user_id::text);

-- 6. 为其他表启用 RLS 并设置基本策略
ALTER TABLE interview_snapshot ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE outlines ENABLE ROW LEVEL SECURITY;
ALTER TABLE contract_texts ENABLE ROW LEVEL SECURITY;
ALTER TABLE export_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE payment_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE refund_applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE project_experts ENABLE ROW LEVEL SECURITY;
ALTER TABLE custom_contents ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_agreement_consents ENABLE ROW LEVEL SECURITY;
ALTER TABLE pricing_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE team_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- 7. 为各个表创建统一的读写策略
DO $$
DECLARE
    r record;
BEGIN
    FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename NOT IN ('pg_catalog', 'information_schema')
    LOOP
        -- 删除已存在的策略
        EXECUTE format('DROP POLICY IF EXISTS "users_select_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('DROP POLICY IF EXISTS "users_insert_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('DROP POLICY IF EXISTS "users_update_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('DROP POLICY IF EXISTS "users_delete_%s" ON %I', r.tablename, r.tablename);
        
        -- 创建 SELECT 策略（有 user_id 字段的表）
        BEGIN
            EXECUTE format('CREATE POLICY "users_select_%s" ON %I FOR SELECT USING (user_id = auth.uid()::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            -- 没有 user_id 字段，允许所有读取
            EXECUTE format('CREATE POLICY "users_select_%s" ON %I FOR SELECT USING (true)', r.tablename, r.tablename);
        END;
        
        -- 创建 INSERT 策略
        BEGIN
            EXECUTE format('CREATE POLICY "users_insert_%s" ON %I FOR INSERT WITH CHECK (auth.uid()::text = user_id::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            EXECUTE format('CREATE POLICY "users_insert_%s" ON %I FOR INSERT WITH CHECK (true)', r.tablename, r.tablename);
        END;
        
        -- 创建 UPDATE 策略
        BEGIN
            EXECUTE format('CREATE POLICY "users_update_%s" ON %I FOR UPDATE USING (user_id = auth.uid()::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            EXECUTE format('CREATE POLICY "users_update_%s" ON %I FOR UPDATE USING (true)', r.tablename, r.tablename);
        END;
        
        -- 创建 DELETE 策略
        BEGIN
            EXECUTE format('CREATE POLICY "users_delete_%s" ON %I FOR DELETE USING (user_id = auth.uid()::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            EXECUTE format('CREATE POLICY "users_delete_%s" ON %I FOR DELETE USING (true)', r.tablename, r.tablename);
        END;
    END LOOP;
END $$;

-- 8. 创建 service_role 策略（允许服务端操作所有表）
DO $$
DECLARE
    r record;
BEGIN
    FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'public'
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS "service_role_all_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('CREATE POLICY "service_role_all_%s" ON %I FOR ALL USING (auth.jwt() ->> ''role'' = ''service_role'')', r.tablename, r.tablename);
    END LOOP;
END $$;
