# 🔧 后端重启问题修复

## 问题
- 旧的后端进程（PID 23264）还在运行
- 新进程启动失败，因为端口 8000 已被占用
- 需要重启后端以应用最新代码

---

## 解决方案

### 步骤 1：停止旧进程
```powershell
taskkill /PID 23264 /F
```

### 步骤 2：确认端口已释放
```powershell
netstat -ano | findstr :8000
```

### 步骤 3：重启后端
```powershell
cd "F:/hermes/2 Mike/衡简叙约/backend"
./venv/Scripts/python.exe main.py
```

### 步骤 4：测试
```powershell
# 获取 token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"13900139001","code":"123456","agree_user_agreement":true,"agree_privacy_policy":true,"agreement_version":"V1.0"}'

# 创建项目（使用返回的 token）
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ***" \
  -d '{"name":"测试","primary_type":"A","secondary_types":["B"]}'
```

---

## 预期结果

✅ 本地后端应该能正常创建项目
✅ 返回：`{"code":0,"msg":"成功","data":{"project_id":"..."}}`

---

**请执行上述步骤，重启后端并测试！**
