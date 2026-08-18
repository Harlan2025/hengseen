# 🔧 Agnes AI 响应格式修复

## 问题原因
Agnes AI 的响应格式与标准 OpenAI 格式不同：
- 标准格式：`{"choices": [{"message": {"content": "..."}}]}`
- Agnes 格式：`{"choices": [{"message": {"content": "", "reasoning_content": "..."}}]}`

当 `content` 为空时，代码直接返回空字符串，导致 JSON 解析失败。

---

## 修复内容
✅ 已修改 `ai_service.py`，优先使用 `reasoning_content` 作为内容

---

## 下一步
1. 重启后端服务
2. 测试访谈功能
3. 确认 AI 生成问题正常
