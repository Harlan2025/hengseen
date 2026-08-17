# 衡简叙约 - Railway 部署脚本 (Windows PowerShell)

Write-Host "======================================"
Write-Host "衡简叙约 - Railway 部署脚本"
Write-Host "======================================"

# 检查 git
$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Host "❌ git 未安装"
    exit 1
}
Write-Host "✅ Git 已安装"

# 初始化 git（如果未初始化）
if (-not (Test-Path ".git")) {
    Write-Host ""
    Write-Host "📦 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit"
}

# 添加 remote（如果未添加）
$remote = git remote get-url origin 2>$null
if (-not $remote) {
    Write-Host ""
    Write-Host "❌ 请先配置 GitHub remote"
    Write-Host ""
    Write-Host "执行以下命令："
    Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/hengseen.git"
    Write-Host "  git push -u origin main"
    exit 1
}
Write-Host "✅ Git 仓库已配置"

# 推送代码
Write-Host ""
Write-Host "📤 推送代码到 GitHub..."
git add .
git commit -m "Deploy to Railway" 2>$null
git push origin main

Write-Host "✅ 代码已推送"

Write-Host ""
Write-Host "======================================"
Write-Host "🎉 部署步骤完成！"
Write-Host "======================================"
Write-Host ""
Write-Host "下一步："
Write-Host "1. 访问 https://railway.app"
Write-Host "2. 点击 'New Project'"
Write-Host "3. 选择 'Deploy from GitHub repo'"
Write-Host "4. 选择 hengseen 仓库"
Write-Host "5. 在 Settings 中添加环境变量"
Write-Host ""
Write-Host "详细指南见: deploy/RAILWAY_GUIDE.md"
Write-Host ""
