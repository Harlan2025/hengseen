# 一键部署脚本 (PowerShell)

param(
    [ValidateSet("railway", "fly")]
    [string]$Target = "railway"
)

Write-Host "======================================"
Write-Host "衡简叙约 - 一键部署脚本"
Write-Host "======================================"

switch ($Target) {
    "railway" {
        Write-Host ""
        Write-Host "🚀 部署到 Railway..."
        Write-Host ""
        Write-Host "请访问: https://railway.app"
        Write-Host "New Project → Deploy from GitHub repo"
        Write-Host "Root Directory: backend"
        Write-Host ""
        Write-Host "环境变量:"
        Write-Host "  SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co"
        Write-Host "  SUPABASE_SERVICE_KEY=***"
        Write-Host "  JWT_SECRET_KEY=***"
        Write-Host "  AI_PROVIDER=agnes"
        Write-Host "  AI_AGNES_API_KEY=***"
    }
    "fly" {
        Write-Host ""
        Write-Host "🚀 部署到 Fly.io..."
        Set-Location backend
        & fly launch --no-deploy
        & fly secrets set SUPABASE_URL=https://rtmldrysnwzbkgiihnuc.supabase.co
        & fly secrets set AI_PROVIDER=agnes
        & fly deploy
    }
}

Write-Host ""
Write-Host "✅ 部署完成！"
Write-Host ""
Write-Host "使用帮助: .\deploy\scripts\deploy.ps1 [railway|fly]"