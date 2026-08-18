# 🔍 前端请求调试指南

## 问题
云端后端返回：`{"detail":"There was an error parsing the body"}`

## 诊断步骤

### 步骤 1：打开浏览器开发者工具
1. 访问：https://3c3d590c.hengseen.pages.dev
2. 按 **F12** 打开开发者工具
3. 切换到 **Network（网络）** 标签

### 步骤 2：测试创建项目
1. 点击 **"新建项目"** 按钮
2. 填写项目名称
3. 选择主类型（如：买卖）
4. 选择附属类型（如：备忘录）
5. 点击 **"创建"** 按钮

### 步骤 3：查看请求详情
在 Network 面板中：
1. 找到 `POST /api/v1/projects` 请求
2. 点击该请求
3. 查看右侧的详细信息：
   - **Headers（请求头）**：确认 Content-Type
   - **Payload（请求体）**：确认发送的数据格式
   - **Response（响应）**：确认错误信息

### 步骤 4：截图发送给我
请截图 Network 面板中的请求详情，特别是：
- Request Headers
- Request Payload
- Response Body

---

## 可能的原因

### 1. 前端发送了错误的字段名
检查是否发送了驼峰命名（camelCase）而不是蛇形命名（snake_case）：
- ❌ `primaryType` 应该是 `primary_type`
- ❌ `secondaryTypes` 应该是 `secondary_types`

### 2. 前端发送了额外的字段
检查是否有额外的字段被发送

### 3. 前端 API URL 配置错误
检查 `.env.production` 是否正确配置：
```
VITE_API_URL=https://hengseen-backend.fly.dev/api/v1
```

### 4. 后端代码版本问题
确认云端运行的是最新代码

---

## 立即行动

**请打开浏览器开发者工具，测试创建项目，然后截图发给我！**
