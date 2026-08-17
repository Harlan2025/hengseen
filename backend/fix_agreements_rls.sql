-- 为 agreements 表创建允许 anon 读取的 RLS 策略
-- 在 Supabase SQL Editor 中执行

-- 1. 启用 RLS
ALTER TABLE agreements ENABLE ROW LEVEL SECURITY;

-- 2. 删除旧策略（如果存在）
DROP POLICY IF EXISTS "allow_anon_read_agreements" ON agreements;
DROP POLICY IF EXISTS "allow_service_role_agreements" ON agreements;

-- 3. 创建策略：允许 anon 和 authenticated 用户读取 is_active=true 的协议
CREATE POLICY "allow_anon_read_agreements" ON agreements
    FOR SELECT
    TO anon, authenticated
    USING (is_active = true);

-- 4. 创建策略：允许 service_role 进行所有操作
CREATE POLICY "allow_service_role_agreements" ON agreements
    FOR ALL
    TO service_role
    USING (true);

-- 5. 验证策略已创建
SELECT polname, cmd, roles FROM pg_policies WHERE tablename = 'agreements';
