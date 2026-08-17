# 🔒 GitGuardian 安全警告处理指南

## 📧 问题诊断

GitGuardian 检测到仓库 `Harlan2025/hengseen` 中存在**高熵密钥**（Generic High Entropy Secret）。

**推送时间**: 2026-08-17T06:48:44Z

---

## ⚠️ 可能泄露的文件

根据推送记录，以下文件可能包含敏感信息：

1. **`backend/.env.fly`** - Fly.io Token
2. **`.env.production`** - 前端环境变量
3. **`.git-credentials`** - Git 凭证

---

## 🔧 解决方案

### 方案 1：从 Git 历史中删除（推荐）

如果密钥已泄露，必须立即：
1. **旋转密钥**（生成新的 API Key）
2. **从 Git 历史中删除**（使用 `git filter-branch` 或 BFG）
3. **更新远程仓库**

### 方案 2：标记为误报

如果确认不是真实密钥（如测试数据），可以：
1. 点击 **"Mark As False Positive"**
2. 添加说明：`This is a placeholder, not a real secret`

---

## 🚨 紧急处理步骤

### 1. 检查泄露的密钥

```bash
# 查看 commit 内容
git show 3239fe4:backend/.env.fly
```

### 2. 旋转泄露的密钥

**Fly.io Token**:
```bash
# 生成新 Token
fly auth token
```

**Supabase Key**:
- 访问 https://supabase.com/dashboard/project/rtmldrysnwzbkgiihnuc/settings/api
- 重新生成 Service Key

### 3. 从 Git 历史中删除

```bash
# 使用 BFG 清除敏感文件
bfg --delete-files .env.fly
git push --force origin deploy-railway
```

### 4. 添加 .gitignore

```gitignore
# 环境变量文件
.env
.env.*
!.env.example
!.env.production
!.env.development
backend/.env.fly
.git-credentials
```

---

## 📋 预防措施

### 1. 本地扫描

```bash
# 使用 ggshield
ggshield scan pre-push
```

### 2. Git Hooks

添加 pre-commit hook 自动扫描：
```bash
#!/bin/sh
ggshield scan pre-commit
```

### 3. GitHub Secrets Scanning

在仓库设置中启用：
- Settings → Code security → Secret scanning

---

## 🎯 立即行动

**请按以下顺序操作：**

1. ✅ **点击"Fix This Secret Leak"** - GitGuardian 会提供详细指引
2. ✅ **旋转所有相关密钥** - Fly.io、Supabase、JWT
3. ✅ **清理 Git 历史** - 确保密钥不再可访问
4. ✅ **更新远程仓库** - force push
5. ✅ **配置 .gitignore** - 防止再次提交

---

## 🔗 相关链接

- **GitGuardian**: https://www.gitguardian.com
- **GGShield**: https://github.com/GitGuardian/ggshield
- **Secret Scanning**: https://docs.github.com/en/code-security/secret-scanning

---

**⚠️ 重要提示**: 如果确认密钥已泄露，请立即旋转并通知相关人员！
