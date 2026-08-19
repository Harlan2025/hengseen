# 🔧 修复 interview.py 中的 Supabase 语法错误

## 问题
```python
result = supabase.table("interview_snapshot").select("*").eq("project_id", project_id).order("step", asc=True).execute()
```

错误：`TypeError: TableQuery.order() got an unexpected keyword argument 'asc'`

---

## 修复
```python
result = supabase.table("interview_snapshot").select("*").eq("project_id", project_id).order("step").execute()
```

---

## 下一步
重启后端服务测试。
