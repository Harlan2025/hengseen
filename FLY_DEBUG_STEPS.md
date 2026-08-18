# 🔧 Fly.io 云端代码版本问题诊断

## 当前状态
- ✅ 健康检查通过: `{"status":"ok","mode":"production"}`
- ✅ 登录功能正常
- ❌ 创建项目失败: `{"detail":"There was an error parsing the body"}`

---

## 问题分析

**错误信息**: "There was an error parsing the body"

这通常意味着：
1. **请求体格式与后端期望不符**
2. **云端运行的是旧版本代码**
3. **Pydantic 模型验证失败**

---

## 解决方案

### 方案 1：检查 Fly.io 部署日志

访问 Fly.io Logs 页面查看详细信息：
```
https://fly.io/apps/hengseen-backend/logs
```

### 方案 2：使用 Web Terminal 检查代码

1. 访问：**https://fly.io/apps/hengseen-backend/terminal**
2. 执行以下命令检查项目路由代码：
   ```bash
   cd /app/backend/routers
   cat projects.py | head -50
   ```
3. 确认是否是最新代码

### 方案 3：检查环境变量

访问：**https://fly.io/apps/hengseen-backend/secrets**

确保以下变量已设置：
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `JWT_SECRET_KEY`
- `AI_PROVIDER=agnes`
- `AI_AGNES_API_KEY`

### 方案 4：强制重新构建

在 Fly.io Dashboard：
1. 访问：**https://fly.io/apps/hengseen-backend**
2. 点击 **"Overview"**
3. 找到 **"Deploy"** 按钮
4. 选择 **"Deploy now"**
5. 确认分支为 `main`，commit 应为 `c9df9b7`
6. 等待部署完成

### 方案 5：添加详细错误日志

如果问题持续，可以添加更详细的错误处理：

编辑 `backend/routers/projects.py`：
```python
@router.post("", response_model=ApiResponse)
async def create_project(req: ProjectCreateRequest, user_data: dict = Depends(get_current_user)):
    """创建新项目"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Received request: name={req.name}, primary_type={req.primary_type}, secondary_types={req.secondary_types}")
        
        # 验证文件类型
        primary_type = validate_file_type(req.primary_type)
        secondary_types = [validate_file_type(t) for t in req.secondary_types]
        
        # 验证组合合法性
        valid_combinations = get_valid_combinations()
        combination_key = f"{primary_type['code']}_{sorted([t['code'] for t in secondary_types])}"
        
        if primary_type['code'] not in valid_combinations or \
           sorted([t['code'] for t in secondary_types]) not in valid_combinations.get(primary_type['code'], []):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": 4002, "msg": "非法类型组合"}
            )
        
        # 创建项目
        project_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        supabase.table("contract_projects").insert({
            "project_id": project_id,
            "user_id": user_data["sub"],
            "name": req.name,
            "primary_type": primary_type["code"],
            "secondary_types": [t["code"] for t in secondary_types],
            "status": ProjectStatus.INIT.value,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }).execute()
        
        logger.info(f"Project created: {project_id}")
        return ApiResponse(data={"project_id": project_id})
        
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 5000, "msg": f"服务器内部错误: {str(e)}"}
        )
```

---

## 立即行动

### 步骤 1：检查日志
访问：**https://fly.io/apps/hengseen-backend/logs**
查看创建项目时的详细错误信息

### 步骤 2：强制重新构建
访问：**https://fly.io/apps/hengseen-backend**
点击 **"Deploy"** → **"Deploy now"**

### 步骤 3：验证
部署完成后测试：
```bash
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ***" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

---

## 预期结果

✅ 应该返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

**请访问 Fly.io Logs 页面，查看详细错误信息！**
