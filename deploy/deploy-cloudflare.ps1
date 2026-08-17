# 一键部署脚本 (Windows PowerShell)

Write-Host "======================================"
Write-Host "衡简叙约 - Cloudflare Pages 部署"
Write-Host "======================================"

# 检查Node.js
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Host "❌ Node.js 未安装"
    exit 1
}
Write-Host "✅ Node.js: $(node --version)"

# 检查npm
$npm = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npm) {
    Write-Host "❌ npm 未安装"
    exit 1
}
Write-Host "✅ npm: $(npm --version)"

# 进入前端目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendPath = Join-Path $scriptPath "..\frontend"
Set-Location $frontendPath

# 安装依赖
Write-Host ""
Write-Host "📦 安装依赖..."
npm install --legacy-peer-deps

# 构建
Write-Host ""
Write-Host "🔨 构建前端..."
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 构建失败"
    exit 1
}
Write-Host "✅ 构建成功"

# 部署到Cloudflare Pages
Write-Host ""
Write-Host "☁️  部署到 Cloudflare Pages..."
npx wrangler pages deploy dist --project-name=hengseen --branch=main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================"
    Write-Host "✅ 部署成功！"
    Write-Host "访问地址: https://hengseen.pages.dev"
    Write-Host "======================================"
} else {
    Write-Host ""
    Write-Host "❌ 部署失败，请检查 Wrangler 配置"
    Write-Host ""
    Write-Host "手动部署步骤："
    Write-Host "1. 登录 Cloudflare: wrangler login"
    Write-Host "2. 部署: wrangler pages deploy dist --project-name=hengseen"
    exit 1
}
