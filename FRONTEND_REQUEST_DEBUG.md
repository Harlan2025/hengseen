# 🔧 前端请求格式问题诊断

## 问题现象
- ✅ 本地后端: 创建项目成功
- ❌ 云端后端: `{"detail":"There was an error parsing the body"}`

---

## 问题分析

**错误信息**: "There was an error parsing the body"

这通常意味着：
1. **请求体格式与 Pydantic 模型不匹配**
2. **Content-Type 头缺失或错误**
3. **JSON 格式有问题**

---

## 检查点

### 1. 前端发送的数据格式

查看 `frontend/src/stores/project.ts`:
```typescript
async function createProject(name: string, primaryType: string, secondaryTypes: string[]) {
  const res = await api.post('/projects', {
    name,
    primary_type: primaryType,
    secondary_types: secondaryTypes
  })
  ...
}
```

✅ 格式正确，使用 snake_case

### 2. 后端期望的格式

查看 `backend/models/schemas.py`:
```python
class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    primary_type: str = Field(..., description="主类型代码：A-J")
    secondary_types: List[str] = Field(default=[], max_length=2, description="附属类型代码列表，最多2个")
```

✅ 应该能匹配

### 3. 可能的区别

**本地 vs 云端**:
- 本地使用测试模式（可能有不同的验证）
- 云端使用生产模式
- 环境变量可能不同

---

## 解决方案

### 方案 1：检查 Cloudflare Workers 中间层

如果前端通过 Cloudflare Pages 部署，可能有 Workers 代理。检查：
- `frontend/cloudflare.config.js` 或类似文件
- 确认 API 请求直接发送到 Fly.io

### 方案 2：添加详细错误日志

在 `backend/routers/projects.py` 中添加：
```python
@router.post("", response_model=ApiResponse)
async def create_project(req: ProjectCreateRequest, user_data: dict = Depends(get_current_user)):
    """创建新项目"""
    import logging
    logger = logging.getLogger(__name__)
    
    # 记录请求详情
    logger.info(f"Request body: name={req.name}, primary_type={req.primary_type}, secondary_types={req.secondary_types}")
    
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
```

### 方案 3：检查环境变量差异

访问 Fly.io Secrets 页面：
```
https://fly.io/apps/hengseen-backend/secrets
```

对比本地 `.env` 文件，确保所有必需的环境变量都已设置。

### 方案 4：测试不同的请求格式

尝试发送不同的请求格式：
```bash
# 格式 1: 标准 JSON
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ***" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'

# 格式 2: 空 secondary_types
curl -X POST https://hengseen-backend.fly.dev/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ***" \
  -d '{"name":"测试","primary_type":"A","secondary_types":[]}'
```

---

## 立即行动

1. **检查前端 Network 请求**
   - 打开浏览器开发者工具 (F12)
   - 访问前端应用
   - 尝试创建项目
   - 查看 Network 面板中的请求详情

2. **对比本地和云端的差异**
   - 检查环境变量
   - 检查代码版本
   - 检查请求格式

3. **添加调试日志**
   - 修改代码添加详细日志
   - 重新部署
   - 查看日志输出

---

**请访问浏览器开发者工具，查看前端实际发送的请求格式！**
