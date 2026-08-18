# 🔧 修复 Agnes AI API 地址

## 问题原因
`.env` 文件中的 API 地址配置错误：
- 错误地址：`https://api.sapiens.ai/v1`
- 正确地址：`https://apihub.agnes-ai.com/v1`（从官方文档获取）

## 修复内容
✅ 已更新 `.env` 文件中的 `AI_AGNES_BASE_URL` 配置

---

## Agnes AI 官方文档
- 文档地址：https://www.agnes-ai.com/zh-Hans/docs/overview
- API 端点：https://apihub.agnes-ai.com/v1
- 控制台：https://platform.agnes-ai.com

---

## 下一步
1. 重启后端服务
2. 测试访谈功能
3. 确认 AI 调用成功
