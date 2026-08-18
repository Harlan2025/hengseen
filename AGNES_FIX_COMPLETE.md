# 🎉 Agnes AI 响应格式修复完成

## 问题原因
Agnes AI 的响应格式特殊：
- `content` 字段为空字符串
- 实际内容在 `reasoning_content` 字段

---

## 修复内容
✅ 已修改 `ai_service.py`，优先读取 `reasoning_content`

---

## 当前状态
- 后端服务：正在重启
- AI Provider：agnes
- Model：agnes-2.5-flash

---

## 下一步
1. 等待后端重启完成
2. 测试访谈功能
3. 确认 AI 生成问题正常
