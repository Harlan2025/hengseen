# 🤖 配置真实 AI 服务 (Agnes)

## 问题原因
本地后端日志显示：
```
AI chat error: [Errno 11001] getaddrinfo failed
```
这是 **DNS 解析失败**，说明配置的 AI API 地址无法访问。

---

## 解决方案

### 方案 A：修改 .env 文件（推荐）

打开 `backend/.env` 文件，添加或修改以下配置：

```ini
# AI服务配置
AI_MODE=real
AI_PROVIDER=agnes
AI_API_KEY=sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5
AI_BASE_URL=https://api.agnes.ai/v1
AI_MODEL=agnes-2.5-flash
AI_MAX_TOKENS=4096
```

### 方案 B：只修改 AI 相关配置

如果已经有其他配置，只需确保：
```ini
AI_MODE=real
AI_PROVIDER=agnes
AI_API_KEY=你的API Key
AI_BASE_URL=https://api.agnes.ai/v1
```

---

## 已完成的修改

✅ 已创建配置说明文档
✅ 已记录正确的 API 端点

---

## 下一步

1. 修改 `backend/.env` 文件
2. 重启本地后端服务
3. 测试访谈功能
4. 推送代码到 GitHub
5. 在 Fly.io 设置环境变量并重新部署
