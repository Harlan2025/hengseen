# 🔍 API Key 测试报告

## 测试结果
```
curl -s "https://apihub.agnes-ai.com/v1/chat/completions" \
  -H "Authorization: Bearer sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5" \
  -H "Content-Type: application/json" \
  -d '{"model":"agnes-2.5-flash","messages":[{"role":"user","content":"你好"}],"max_tokens":10}'
```

## 返回结果
```json
{
  "error": {
    "code": "",
    "message": "无效的令牌 (request id: 20260818093220701784713BlWFOUvr)",
    "type": "AgnesAI_error"
  }
}
```

---

## 问题分析
API Key `sk-lnvzK2lomTYJcD18T86jMBZFhLozEs2swl0IgmnGMJgq5pp5` **无效**。

可能原因：
1. **Key 格式错误** - 复制时可能有遗漏
2. **Key 已过期** - 需要在控制台重新生成
3. **Key 不属于此项目** - 需要检查项目绑定

---

## 解决方案

### 方案 1：重新获取 API Key（推荐）
1. 访问 https://platform.agnes-ai.com
2. 进入 **"API Key"** 管理页面
3. 创建新的 API Key（确保账户有余额）
4. 复制完整的 Key（以 `sk-` 开头，约 50+ 字符）

### 方案 2：使用其他 AI 提供商
如果 Agnes AI 暂时无法使用，可以切换到其他提供商：

| 提供商 | Base URL | 说明 |
|--------|----------|------|
| DeepSeek | https://api.deepseek.com/v1 | 中文优化，性价比高 |
| SiliconFlow | https://api.siliconflow.cn/v1 | 免费额度可用 |
| OpenRouter | https://openrouter.ai/api/v1 | 多模型支持 |

---

## 建议
请先确认 API Key 是否正确。如果确实有效，请提供以下信息：
1. Agnes AI 账户登录邮箱
2. 项目 ID（如有）

这样我可以进一步排查问题。
