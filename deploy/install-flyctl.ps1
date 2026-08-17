# Fly.io 安装脚本

Write-Host "======================================"
Write-Host "安装 flyctl"
Write-Host "======================================"

# 检查是否已安装
$flyPath = "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe"
if (Test-Path $flyPath) {
    Write-Host "✅ flyctl 已安装"
    & $flyPath --version
    exit 0
}

Write-Host "📥 下载 flyctl..."

# 创建目录
New-Item -ItemType Directory -Force -Path "C:\Users\haigu\AppData\Local\flyctl" | Out-Null

# 下载
$zipUrl = "https://github.com/superfly/flyctl/releases/download/v0.4.83/flyctl_0.4.83_Windows_x86_64.zip"
$zipPath = "C:\Users\haigu\AppData\Local\flyctl\flyctl.zip"

Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath
Write-Host "✅ 下载完成"

# 解压
Expand-Archive -Path $zipPath -DestinationPath "C:\Users\haigu\AppData\Local\flyctl" -Force
Remove-Item $zipPath -Force

Write-Host "✅ 安装完成"

# 添加到 PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*flyctl*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;C:\Users\haigu\AppData\Local\flyctl", "User")
    Write-Host "✅ 已添加到 PATH"
}

Write-Host ""
Write-Host "请重启终端后运行："
Write-Host "  fly --version"
Write-Host ""
