# 部署到Cloudflare Pages指南

## 前置条件

1. 注册 Cloudflare 账号: https://dash.cloudflare.com
2. 创建 Pages 项目
3. 获取 API Token

## 部署步骤

### 方法一：手动部署（推荐）

```bash
# 1. 安装 Wrangler CLI
npm install -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 构建前端
cd frontend
npm install
npm run build

# 4. 部署到 Cloudflare Pages
wrangler pages deploy dist --project-name=hengseen
```

### 方法二：GitHub Actions 自动部署

1. 在 GitHub 创建仓库并推送代码
2. 在 Cloudflare Dashboard 绑定仓库
3. 配置环境变量：
   - `VITE_API_URL`: 后端API地址
4. 启用 CI/CD

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `VITE_API_URL` | 后端API地址 | `https://api.hengseen.com/api/v1` |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API Token | `***` |
| `CLOUDFLARE_ACCOUNT_ID` | Cloudflare Account ID | `***` |

## 自定义域名

1. 在 Cloudflare Dashboard → Pages → 项目设置
2. 添加自定义域名
3. 配置 DNS 记录

## 回滚

```bash
wrangler pages deployment rollback <deployment-id>
```
