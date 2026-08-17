-- 衡简叙约 RLS 策略配置 - 简化版
-- 在 Supabase SQL Editor 中执行

-- 1. 为 agreements 表创建允许 anon 读取的策略
ALTER TABLE agreements ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "allow_anon_read_active_agreements" ON agreements;
CREATE POLICY "allow_anon_read_active_agreements" ON agreements
    FOR SELECT 
    TO anon, authenticated
    USING (is_active = true);

DROP POLICY IF EXISTS "allow_service_role_all" ON agreements;
CREATE POLICY "allow_service_role_all" ON agreements
    FOR ALL 
    TO service_role
    USING (true);

-- 2. 为 users 表创建策略
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "allow_user_read_own" ON users;
CREATE POLICY "allow_user_read_own" ON users
    FOR SELECT 
    TO anon, authenticated
    USING (auth.uid()::text = user_id::text OR auth.jwt() ->> 'role' = 'service_role');

DROP POLICY IF EXISTS "allow_user_insert" ON users;
CREATE POLICY "allow_user_insert" ON users
    FOR INSERT 
    TO anon, authenticated
    WITH CHECK (true);

-- 3. 为其他表创建统一策略
DO $$
DECLARE
    r record;
BEGIN
    FOR r IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename NOT IN ('agreements', 'users')
    LOOP
        -- 启用 RLS
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', r.tablename);
        
        -- 删除旧策略
        EXECUTE format('DROP POLICY IF EXISTS "allow_select_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('DROP POLICY IF EXISTS "allow_insert_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('DROP POLICY IF EXISTS "allow_update_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('DROP POLICY IF EXISTS "allow_delete_%s" ON %I', r.tablename, r.tablename);
        EXECUTE format('DROP POLICY IF EXISTS "allow_service_role_%s" ON %I', r.tablename, r.tablename);
        
        -- 创建 SELECT 策略
        BEGIN
            EXECUTE format('CREATE POLICY "allow_select_%s" ON %I FOR SELECT TO anon, authenticated USING (user_id = auth.uid()::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            -- 没有 user_id 字段，允许所有读取
            EXECUTE format('CREATE POLICY "allow_select_%s" ON %I FOR SELECT TO anon, authenticated USING (true)', r.tablename, r.tablename);
        END;
        
        -- 创建 INSERT 策略
        BEGIN
            EXECUTE format('CREATE POLICY "allow_insert_%s" ON %I FOR INSERT TO anon, authenticated WITH CHECK (auth.uid()::text = user_id::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            EXECUTE format('CREATE POLICY "allow_insert_%s" ON %I FOR INSERT TO anon, authenticated WITH CHECK (true)', r.tablename, r.tablename);
        END;
        
        -- 创建 UPDATE 策略
        BEGIN
            EXECUTE format('CREATE POLICY "allow_update_%s" ON %I FOR UPDATE TO anon, authenticated USING (user_id = auth.uid()::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            EXECUTE format('CREATE POLICY "allow_update_%s" ON %I FOR UPDATE TO anon, authenticated USING (true)', r.tablename, r.tablename);
        END;
        
        -- 创建 DELETE 策略
        BEGIN
            EXECUTE format('CREATE POLICY "allow_delete_%s" ON %I FOR DELETE TO anon, authenticated USING (user_id = auth.uid()::text)', r.tablename, r.tablename);
        EXCEPTION WHEN undefined_column THEN
            EXECUTE format('CREATE POLICY "allow_delete_%s" ON %I FOR DELETE TO anon, authenticated USING (true)', r.tablename, r.tablename);
        END;
        
        -- 创建 service_role 策略
        EXECUTE format('CREATE POLICY "allow_service_role_%s" ON %I FOR ALL TO service_role USING (true)', r.tablename, r.tablename);
    END LOOP;
END $$;
