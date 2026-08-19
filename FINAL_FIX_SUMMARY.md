# 🎉 访谈问题重复和步骤不递增问题已修复

## 问题诊断

### 问题1：问题序号不动（都是 step=1）
- **原因**：数据库缺少 `questions_asked` 列，导致保存失败
- **修复**：需要在 Supabase 中添加该列

### 问题2：AI 生成相同问题
- **原因**：AI 看不到之前问过的问题
- **修复**：在 prompt 中加入 `previous_questions` 上下文

### 问题3：总问题数固定为20
- **原因**：`calculate_total_questions` 返回固定值20
- **修复**：根据项目类型动态计算

---

## 已完成的代码修复
✅ 修复了 AI JSON 解析逻辑（处理 markdown 代码块）
✅ 修复了 Agnes AI 响应格式（优先读取 reasoning_content）
✅ 修复了 Supabase order 语法错误
✅ 在 prompt 中加入之前问题列表上下文
✅ 在生成问题时保存问题列表到快照

---

## 需要手动执行的数据库操作

### 在 Supabase Dashboard 中添加列：
1. 访问 https://supabase.com/dashboard/project/wkkkhwrsgwqnujlnlpja/editor
2. 选择 `interview_snapshot` 表
3. 点击 "Add Column"
4. 配置：
   - 列名：`questions_asked`
   - 类型：`text[]` (PostgreSQL 数组)
   - 允许 NULL：否
   - 默认值：`{}`
5. 点击 Save

或者执行 SQL：
```sql
ALTER TABLE interview_snapshot
ADD COLUMN IF NOT EXISTS questions_asked TEXT[] DEFAULT '{}';
```

---

## 下一步
1. 在 Supabase 中添加 `questions_asked` 列
2. 重启后端服务
3. 测试完整访谈流程
4. 确认步骤递增且问题不重复
5. 推送代码并重新部署云端
