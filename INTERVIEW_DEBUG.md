# 🔍 访谈功能问题诊断

## 当前状态
- ❌ 前端：进入访谈页面后显示"获取问题失败"
- ✅ 后端访谈 API 路由存在：`GET /interview/{project_id}/question`

---

## 可能原因
1. **项目状态不正确** - 项目状态必须是 `interviewing` 才能进行访谈
2. **项目不存在** - 需要先创建项目
3. **Token 未正确传递** - 前端可能没有发送认证头
4. **API URL 配置错误** - 前端可能调用的是错误的 API 地址

---

## 解决方案

### 方案 1：检查项目状态
1. 创建项目后，需要先将项目状态更新为 `interviewing`
2. 检查数据库中 `contract_projects` 表的 `status` 字段

### 方案 2：测试访谈 API
请在浏览器控制台 (F12 → Console) 执行以下测试：

```javascript
// 获取 token
fetch('https://hengseen-backend.fly.dev/api/v1/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    phone: '13900139001',
    code: '123456',
    agree_user_agreement: true,
    agree_privacy_policy: true,
    agreement_version: 'V1.0'
  })
})
.then(r => r.json())
.then(d => {
  console.log('Login:', d);
  const token = d.data.access_token;
  
  // 先创建项目
  return fetch('https://hengseen-backend.fly.dev/api/v1/projects', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      name: '测试访谈项目',
      primary_type: 'A',
      secondary_types: ['B']
    })
  });
})
.then(r => r.json())
.then(d => {
  console.log('Create Project:', d);
  const projectId = d.data.project_id;
  
  // 更新项目状态为 interviewing
  return fetch(`https://hengseen-backend.fly.dev/api/v1/projects/${projectId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({status: 'interviewing'})
  });
})
.then(r => r.json())
.then(d => {
  console.log('Update Status:', d);
  
  // 获取访谈问题
  return fetch('https://hengseen-backend.fly.dev/api/v1/interview/' + projectId + '/question', {
    headers: {'Authorization': `Bearer ${token}`}
  });
})
.then(r => r.json())
.then(d => console.log('Get Question:', d))
.catch(e => console.error('Error:', e));
```

### 方案 3：检查前端代码
确认前端是否正确传递了项目 ID 和 Token。

---

## 立即行动
1. **清除浏览器缓存**（Ctrl+Shift+Delete）
2. **执行上述控制台测试**
3. **截图发送给我查看结果**
