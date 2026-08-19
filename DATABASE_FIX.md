# 🔧 修复数据库缺少列问题

## 问题
Supabase 数据库中 `interview_snapshot` 表缺少 `questions_asked` 列。

错误信息：
```
Mutation error 400: Could not find the 'questions_asked' column of 'interview_snapshot' in the schema cache
```

## 解决方案
需要在 Supabase 数据库中执行以下 SQL：

```sql
ALTER TABLE interview_snapshot
ADD COLUMN IF NOT EXISTS questions_asked TEXT[] DEFAULT '{}';
```

或者在 Supabase Dashboard 中添加列：
1. 进入 Supabase Dashboard → Table Editor
2. 选择 `interview_snapshot` 表
3. 点击 "Add Column"
4. 列名：`questions_asked`
5. 类型：`text[]` (PostgreSQL 数组)
6. 默认值：`{}`
7. 点击 Save

---

## 已完成的修复
✅ 后端代码已修改，支持保存问题列表

## 下一步
1. 在 Supabase 中添加 `questions_asked` 列
2. 测试完整访谈流程
3. 确认问题不重复且步骤递增
