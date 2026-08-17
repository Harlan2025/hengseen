# 衡简叙约前端开发任务分配

## 技术栈选择
- **框架**: Vue 3 + TypeScript + Vite
- **UI库**: Element Plus
- **状态管理**: Pinia
- **路由**: Vue Router 4
- **HTTP**: Axios
- **构建**: Vite
- **部署**: Vercel (推荐) / Netlify

## 项目结构
```
frontend/
├── src/
│   ├── views/           # 页面
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── ProjectList.vue
│   │   ├── ProjectDetail.vue
│   │   ├── Interview.vue
│   │   ├── Outline.vue
│   │   └── Contract.vue
│   ├── components/      # 组件
│   ├── stores/          # Pinia状态
│   ├── api/             # API接口
│   ├── utils/           # 工具函数
│   └── types/           # TypeScript类型
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## API端点清单
| 方法 | 路径 | 说明 | 需要认证 |
|------|------|------|----------|
| POST | /api/v1/auth/login | 登录 | 否 |
| POST | /api/v1/auth/register | 注册 | 否 |
| GET | /api/v1/auth/me | 获取用户信息 | 是 |
| GET | /api/v1/auth/agreements | 获取协议内容 | 否 |
| GET | /api/v1/projects/list | 项目列表 | 是 |
| POST | /api/v1/projects | 创建项目 | 是 |
| GET | /api/v1/projects/{id} | 项目详情 | 是 |
| PUT | /api/v1/projects/{id} | 更新项目 | 是 |
| GET | /api/v1/interview/{id}/question | 获取访谈问题 | 是 |
| POST | /api/v1/interview/{id}/answer | 提交答案 | 是 |
| POST | /api/v1/outline/generate | 生成大纲 | 是 |
| POST | /api/v1/contract/generate | 生成合同 | 是 |
| POST | /api/v1/export | 导出文档 | 是 |

## 用户流程
1. 登录/注册 → 同意协议
2. 创建项目 → 选择文件类型(A-J组合)
3. AI访谈 → 逐步问答
4. 生成大纲 → 确认/修改
5. 生成合同 → 查看/编辑
6. 导出文档 → 下载Word/Markdown

## 后端API信息
- Base URL: http://localhost:8000/api/v1
- 生产环境: 待部署
- JWT认证: Bearer Token
- 测试账号: 13900139001 / 123456

## 文件类型代码
- A: 买卖, B: 备忘录, C: 股权转让, D: 合作
- E: 劳动, F: 知识产权, G: 担保, H: 债权
- I: 居间, J: 终止

## 合法组合示例
- A + B (买卖+备忘录)
- A + G (买卖+担保)
- B + A (备忘录+买卖)
- 详细见后端 get_valid_combinations()
