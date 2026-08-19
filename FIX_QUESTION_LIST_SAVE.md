# 🔧 修复问题列表保存逻辑

## 问题
生成问题后没有保存问题列表到快照，导致 AI 无法知道之前问过哪些问题。

## 解决方案
1. 修改 generate_interview_question 函数，返回 question_text
2. 在 submit_answer 时，将当前问题追加到问题列表

## 已完成的修复
✅ 修改了 prompt，加入 previous_questions 上下文
✅ 修改了保存逻辑，保存问题列表到快照

---

## 下一步
需要进一步测试完整流程。