# Fly.io 一键部署脚本

Write-Host "======================================"
Write-Host "衡简叙约 - Fly.io 部署脚本"
Write-Host "======================================"

# 设置 flyctl 路径
$flyPath = "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe"

# 检查 flyctl 是否存在
if (-not (Test-Path $flyPath)) {
    Write-Host "❌ flyctl 未找到"
    Write-Host ""
    Write-Host "请运行安装脚本："
    Write-Host "  .\deploy\install-flyctl.ps1"
    exit 1
}

Write-Host "✅ flyctl 已安装: $flyPath"

# 检查登录状态
Write-Host ""
$auth = & $flyPath auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "🔐 请登录 Fly.io"
    & $flyPath auth login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 登录失败"
        exit 1
    }
} else {
    Write-Host "✅ 已登录 Fly.io"
}

# 进入 backend 目录
$backendDir = Join-Path $PSScriptRoot "..\backend"
Set-Location $backendDir

# 检查 fly.toml
if (-not (Test-Path "fly.toml")) {
    Write-Host ""
    Write-Host "🚀 创建 Fly 应用..."
    & $flyPath launch --no-deploy
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 创建应用失败"
        exit 1
    }
}

# 设置环境变量
Write-Host ""
Write-Host "⚙️  配置环境变量..."
& $flyPath secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
& $flyPath secrets set SUPABASE_SERVICE_KEY=***
& $flyPath secrets set JWT_SECRET_KEY=***
& $flyPath secrets set AI_PROVIDER=agnes
& $flyPath secrets set AI_AGNES_API_KEY=***

# 部署
Write-Host ""
Write-Host "📦 部署到 Fly.io..."
& $flyPath deploy
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 部署失败，请查看日志"
    exit 1
}

# 获取 URL
Write-Host ""
Write-Host "✅ 部署完成！"
Write-Host ""
Write-Host "应用 URL:"
& $flyPath apps open
Write-Host ""
Write-Host "查看日志: $flyPath logs"
Write-Host "管理应用: $flyPath apps list"
Write-Host ""
