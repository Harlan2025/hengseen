# FastAPI 中间件配置

## CORS 配置
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 请求体解析问题

### 问题现象
创建项目返回 "There was an error parsing the body"

### 可能原因
1. Content-Type 未正确设置
2. JSON 格式错误
3. Pydantic 模型验证失败

### 解决方案
在路由处理函数中添加调试日志：
```python
@router.post("", response_model=ApiResponse)
async def create_project(req: ProjectCreateRequest, user_data: dict = Depends(get_current_user)):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Request body: {req}")
    logger.info(f"Primary type: {req.primary_type}")
    logger.info(f"Secondary types: {req.secondary_types}")
    # ...
```

## 建议的调试步骤

1. 检查请求头：
   - Content-Type: application/json
   - Authorization: Bearer <token>

2. 检查请求体格式：
   ```json
   {
     "name": "测试项目",
     "primary_type": "A",
     "secondary_types": ["B"]
   }
   ```

3. 查看后端完整日志输出
