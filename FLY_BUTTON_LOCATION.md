# Fly.io 部署按钮位置图解

## 📍 位置 1：顶部导航栏

```
https://fly.io/apps/hengseen-backend
```

在页面右上角，寻找：
- **"Deploy"** 按钮（蓝色）
- 或 **"+"** 按钮 → 选择 "Deploy"

---

## 📍 位置 2：左侧菜单

左侧菜单包含：
```
├── Overview
├── Activity          ← 点击这里
├── Resources
├── Metrics
├── Configuration
│   ├── Environment Variables
│   └── Secrets
├── Settings
│   └── General
└── ...
```

**点击 "Activity"** → 页面顶部会有 **"Redeploy"** 按钮

---

## 📍 位置 3：直接访问 Activity 页面

```
https://fly.io/apps/hengseen-backend/activity
```

这个页面会显示所有部署记录，顶部有：
- **"Deploy app"** 按钮
- 或 **"Redeploy latest commit"**

---

## 📍 位置 4：Web Terminal

```
https://fly.io/apps/hengseen-backend/terminal
```

打开后执行：
```bash
cd /app/backend
fly deploy
```

---

## 🎯 最快的方法

直接访问这个链接：
```
https://fly.io/apps/hengseen-backend/activity
```

然后找页面上的 **"Deploy"** 或 **"Redeploy"** 按钮。

---

**如果还是找不到，请截图告诉我你看到了什么界面！**
