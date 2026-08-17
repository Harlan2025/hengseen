# 衡简叙约 - Cloudflare Pages 部署配置

## 方式一：使用 Wrangler CLI（推荐）

### 1. 安装 Wrangler
```bash
npm install -g wrangler
```

### 2. 登录 Cloudflare
```bash
wrangler login
```

### 3. 配置项目
```bash
cd frontend
wrangler pages project create hengseen
```

### 4. 构建并部署
```bash
npm run build
wrangler pages deploy dist --project-name=hengseen
```

## 方式二：GitHub Actions 自动部署

1. 在 GitHub 创建仓库
2. 推送代码
3. 在 Cloudflare Dashboard 连接仓库
4. 设置环境变量

## 环境变量配置

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `VITE_API_URL` | 后端API地址 | `https://api.hengseen.com/api/v1` |

## 自定义域名

在 Cloudflare Dashboard:
1. 进入 Pages 项目
2. 点击 "Custom Domains"
3. 添加你的域名

## 访问地址

部署成功后访问：
- https://hengseen.pages.dev
- 或自定义域名: https://hengseen.com
