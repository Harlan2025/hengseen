# 🔧 Fly.io Build Image 问题修复

## 问题
部署失败：`Error: failed to fetch an image or build from source: unauthorized`

**原因**: Buildpacks builder (`paketobuildpacks/builder:full`) 需要访问外部镜像仓库，但认证失败。

---

## 已执行的修复

### 1. 切换到 Nixpacks Builder
将 `fly.toml` 中的 builder 从 `paketobuildpacks/builder:full` 改为 `nixpacks`

**Nixpacks 优势**:
- ✅ 由 Fly.io 原生支持
- ✅ 不需要外部镜像仓库认证
- ✅ 自动检测 Python 项目
- ✅ 构建更快更可靠

### 2. 已推送到 GitHub
Commit: `fix: switch to nixpacks builder to avoid build authentication issues`

---

## 🔧 下一步操作

### 请点击重试部署

在 Fly.io 部署失败页面，点击：
**🔁 I've fixed this on GitHub, retry**

或者：
1. 访问：https://fly.io/apps/hengseen-backend/activity
2. 找到最新的失败部署
3. 点击 **"Retry"** 或 **"Deploy again"**

---

## 📋 当前配置

```toml
[build]
  builder = "nixpacks"  # 新配置
```

---

## 预期结果

使用 Nixpacks 构建应该：
1. ✅ 不需要外部镜像认证
2. ✅ 自动检测 Python 项目
3. ✅ 安装依赖（requirements.txt）
4. ✅ 构建成功并部署

---

**请点击重试按钮，等待新的部署结果！**
