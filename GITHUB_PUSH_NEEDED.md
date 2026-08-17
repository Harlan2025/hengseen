# GitHub 推送指南 - 需要 Token

## ⚠️ 问题
当前网络无法直接访问 GitHub，需要有效的认证 Token。

---

## 解决方案

### 方法 1：使用 GitHub Personal Access Token

**请提供你的 GitHub Token：**

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. Note: `hengseen-deploy`
4. 勾选 `repo` 权限
5. 点击 "Generate token"
6. 复制 Token 给我

**然后执行：**
```bash
cd "F:/hermes/2 Mike/衡简叙约"
git remote set-url origin https://YOUR_TOKEN@github.com/haiguang85/hengseen.git
git push -u origin deploy-railway
```

---

### 方法 2：手动上传 ZIP

如果网络问题持续，可以手动上传：

**步骤 1：打包项目**
```powershell
cd "F:\hermes\2 Mike\衡简叙约"
Compress-Archive -Path . -DestinationPath hengseen-deploy.zip -Force
```

**步骤 2：上传到 GitHub**
1. 打开 https://github.com/haiguang85/hengseen
2. 点击 "Add file" → "Upload files"
3. 拖拽 `hengseen-deploy.zip`
4. 提交信息：`Initial commit`
5. 点击 "Commit changes"

---

### 方法 3：使用 SSH（如果有 SSH Key）

```bash
# 检查是否有 SSH Key
ls ~/.ssh/id_rsa.pub

# 如果没有，生成 SSH Key
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 添加 SSH Key 到 GitHub
# 访问 https://github.com/settings/keys
# 点击 "New SSH key"，粘贴以下内容：
cat ~/.ssh/id_rsa.pub

# 配置 Git 使用 SSH
git remote set-url origin git@github.com:haiguang85/hengseen.git
git push -u origin deploy-railway
```

---

## 📊 当前状态

| 项目 | 状态 |
|------|------|
| Git 提交 | ✅ 已完成 (aaf6a54) |
| Remote URL | ⚠️ 需要更新 Token |
| GitHub 推送 | ❌ 认证失败 |
| 下一步 | 提供 GitHub Token |

---

请选择一种方法，完成后告诉我！
