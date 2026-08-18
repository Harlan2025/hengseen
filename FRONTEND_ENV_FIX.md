# 🔧 前端环境变量问题诊断

## 问题分析

前端部署到 Cloudflare Pages，后端部署到 Fly.io。需要确保前端正确配置了 API URL。

---

## 检查点

### 1. 前端环境变量配置

#### `.env.production`（生产环境）
```
VITE_API_URL=https://hengseen-backend.fly.dev/api/v1
```

#### `.env.development`（开发环境）
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 2. 前端 API 调用

查看 `frontend/src/utils/api.ts`:
```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000
})
```

✅ 使用正确的环境变量

---

## 解决方案

### 方案 1：重新部署前端

如果前端没有使用最新的 API URL，需要重新构建和部署：

```bash
cd frontend
npm run build
npx wrangler pages deploy dist --project-name=hengseen --branch=main
```

### 方案 2：检查前端部署状态

访问 Cloudflare Dashboard：
```
https://dash.cloudflare.com/pages
```

确认：
- 项目：hengseen
- 分支：main
- 构建命令：`npm run build`
- 输出目录：`dist`

### 方案 3：直接在浏览器测试

打开浏览器开发者工具 (F12)：
1. 访问前端应用
2. 打开 Console 标签
3. 执行以下测试：

```javascript
// 测试 API 连接
fetch('https://hengseen-backend.fly.dev/health')
  .then(r => r.json())
  .then(d => console.log('Health:', d))
  .catch(e => console.error('Error:', e))
```

---

## 立即行动

### 步骤 1：重新构建前端
```powershell
cd "F:/hermes/2 Mike/衡简叙约/frontend"
npm run build
```

### 步骤 2：重新部署到 Cloudflare Pages
```powershell
npx wrangler pages deploy dist --project-name=hengseen --branch=main
```

### 步骤 3：验证
访问前端应用并测试创建项目功能。

---

## 预期结果

✅ 前端应能成功调用后端 API
✅ 创建项目功能正常工作

---

**请重新构建和部署前端，然后测试！**
