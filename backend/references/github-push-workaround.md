# GitHub 推送工作区

## 问题场景

当无法直接连接 GitHub 时（网络限制、代理问题等）。

## 解决方案

### 方案 1：使用 GitHub Proxy（推荐）
```powershell
# 测试可用代理
curl -s --connect-timeout 5 https://ghfast.top

# 使用代理推送
git remote set-url origin https://ghfast.top/https://github.com/user/repo.git
git push -u origin branch-name
```

### 方案 2：使用代理
```powershell
# 设置代理
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890

# 推送
git push -u origin branch-name

# 清除代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### 方案 3：手动上传
```powershell
# 打包项目（排除大文件）
Compress-Archive -Path "F:/hermes/2 Mike/衡简叙约" -DestinationPath "hengseen-deploy.zip" -Force

# 在 GitHub 网页上传
# 1. 打开 https://github.com/user/repo
# 2. Add file → Upload files
# 3. 拖拽 ZIP 文件
# 4. Commit changes
```

### 方案 4：GitHub Desktop
1. 下载 https://desktop.github.com
2. File → Add local repository
3. 选择项目目录
4. Publish repository

## 注意事项

- GitHub Desktop 会自动处理认证
- 手动上传后需要重新 git init 并推送
- 代理方案最稳定，推荐使用
