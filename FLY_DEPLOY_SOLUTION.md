# 🔧 Fly.io 部署问题诊断

## 错误信息
```
Error: invalid token: all tokens missing third-party discharge tokens
```

## 问题原因
Fly.io 的 API Token 需要经过 **discharge**（放电/认证）过程才能用于部署操作。直接复制 Token 使用会失败。

---

## 解决方案

### 方法 1：使用浏览器登录（推荐）

运行以下命令，会打开浏览器让你登录：
```powershell
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
```

登录后自动完成认证，然后执行：
```powershell
cd "F:/hermes/2 Mike/衡简叙约"
& "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" --app hengseen-backend deploy --strategy immediate
```

---

### 方法 2：通过 Fly.io Dashboard 手动触发

由于 CLI 认证问题，可以通过网页部署：

1. **访问**: https://fly.io/apps/hengseen-backend/activity
2. 在页面顶部找 **"Deploy"** 按钮
3. 点击触发部署

---

### 方法 3：使用 GitHub Actions 自动部署

如果已连接 GitHub，可以手动触发 workflow：

1. **访问**: https://github.com/Harlan2025/hengseen/actions
2. 找到 "Deploy to Fly.io" workflow
3. 点击 **"Run workflow"**
4. 选择分支 `main`
5. 点击绿色按钮

---

## 当前状态

| 项目 | 状态 |
|------|------|
| `fly.toml` 配置 | ✅ 正确 |
| GitHub 连接 | ✅ 已连接 |
| CLI 认证 | ❌ Token 需要 discharge |
| Dashboard 部署 | ⏳ 待尝试 |

---

## 下一步行动

**请选择一种方式：**

1. **运行浏览器登录命令**（推荐）
   ```powershell
   & "C:\Users\haigu\AppData\Local\flyctl\flyctl.exe" auth login
   ```

2. **通过 Dashboard 手动部署**
   - 访问 Activity 页面
   - 点击 Deploy 按钮

3. **通过 GitHub Actions 部署**
   - 访问 Actions 页面
   - 运行 workflow

请告诉我你选择哪种方式，或者运行后遇到什么问题！
