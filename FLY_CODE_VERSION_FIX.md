# 🔧 Fly.io 云端代码版本问题

## 当前状态
- ✅ GitHub 最新代码: commit `8fa817d` (fix: widen type combination validation)
- ✅ 本地后端: 正常工作
- ❌ 云端后端: 仍然返回 "There was an error parsing the body"

---

## 问题分析

**可能原因**：
1. Fly.io 部署使用的是旧版本代码（缓存或旧镜像）
2. 部署过程中有错误但没有完全失败
3. 环境变量或配置问题

---

## 解决方案

### 方案 1：强制重新部署（推荐）

#### 步骤 1：推送空提交触发重新构建
```bash
git commit --allow-empty -m "trigger redeploy with latest code"
git push origin main
```

#### 步骤 2：等待 GitHub Actions 或手动触发
如果配置了自动部署，会自动触发。
否则访问 Fly.io Dashboard 手动触发。

### 方案 2：使用 Web Terminal 检查

1. 访问：**https://fly.io/apps/hengseen-backend/terminal**
2. 执行以下命令检查代码版本：
   ```bash
   cd /app/backend/routers
   cat projects.py | grep -A 20 "get_valid_combinations"
   ```
3. 确认是否是最新代码

### 方案 3：检查 Fly.io 部署历史

1. 访问：**https://fly.io/apps/hengseen-backend/activity**
2. 查看最近的部署记录
3. 确认部署使用的是哪个 commit

### 方案 4：添加调试日志

在 `projects.py` 中添加临时调试日志，帮助定位问题：

```python
@router.post("", response_model=ApiResponse)
async def create_project(req: ProjectCreateRequest, user_data: dict = Depends(get_current_user)):
    """创建新项目"""
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Creating project with req: {req}")
    
    # 验证文件类型
    primary_type = validate_file_type(req.primary_type)
    secondary_types = [validate_file_type(t) for t in req.secondary_types]
    
    # 验证组合合法性
    valid_combinations = get_valid_combinations()
    combination_key = f"{primary_type['code']}_{sorted([t['code'] for t in secondary_types])}"
    logger.info(f"Combination key: {combination_key}")
    
    # ... 其余代码
```

---

## 立即尝试

### 步骤 1：推送空提交
```powershell
cd "F:/hermes/2 Mike/衡简叙约"
git commit --allow-empty -m "trigger redeploy with latest code"
git push origin main
```

### 步骤 2：重新触发 Fly.io 部署
访问：**https://fly.io/apps/hengseen-backend/activity**
点击 **"Deploy"** 按钮

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

**请执行上述步骤，推送空提交并重新触发部署！**
