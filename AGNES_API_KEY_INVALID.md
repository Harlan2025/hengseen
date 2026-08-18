# ❌ Agnes AI API Key 无效

## 问题诊断
API 返回错误：
```
"无效的令牌 (request id: 20260818093038645968281zmifA3JE)"
```

## 可能原因
1. **API Key 格式错误** - 需要重新生成
2. **API Key 已过期或被删除** - 需要重新生成
3. **API Key 不属于当前项目** - 需要检查项目绑定

---

## 解决方案

### 步骤 1：登录 Agnes AI 控制台
访问：https://platform.agnes-ai.com

### 步骤 2：获取正确的 API Key
1. 登录后进入 **"API Key"** 管理页面
2. 创建新的 API Key 或复制已有的 Key
3. 确保 API Key 格式正确（通常是以 `sk-` 开头的长字符串）

### 步骤 3：更新配置
将正确的 API Key 填入 `.env` 文件：
```bash
AI_AGNES_API_KEY=你的正确API Key
```

### 步骤 4：测试 API Key
使用以下命令测试：
```bash
curl -s "https://apihub.agnes-ai.com/v1/chat/completions" \
  -H "Authorization: Bearer 你的API Key" \
  -H "Content-Type: application/json" \
  -d '{"model":"agnes-2.5-flash","messages":[{"role":"user","content":"你好"}],"max_tokens":10}'
```

---

## 当前配置状态

| 配置项 | 值 | 状态 |
|--------|-----|------|
| Base URL | https://apihub.agnes-ai.com/v1 | ✅ 正确 |
| Provider | agnes | ✅ 正确 |
| Model | agnes-2.5-flash | ✅ 正确 |
| API Key | sk-lnvzK2l... | ❌ **无效** |

---

## 下一步
请重新获取有效的 Agnes AI API Key，然后更新 `.env` 文件。
