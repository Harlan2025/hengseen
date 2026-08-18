# 🔧 解决方案：简化访谈启动流程

## 问题分析
1. 云端后端不稳定（有时返回"解析错误"）
2. 前端需要在进入访谈前更新项目状态
3. 但 PUT API 可能失败

---

## 解决方案：修改访谈页面自动初始化

与其在项目详情页更新状态，不如让访谈页面自己处理。这样更简单可靠。

### 修改 Interview.vue

```typescript
onMounted(async () => {
  try {
    // 先更新项目状态为 interviewing
    await api.put(`/projects/${projectId.value}`, {
      status: 'interviewing'
    })
    // 获取访谈问题
    await fetchQuestion()
  } catch (e: any) {
    ElMessage.error('获取问题失败')
  }
})
```

### 修改 ProjectDetail.vue
移除状态更新逻辑，直接跳转：

```typescript
function startInterview() {
  router.push(`/interview/${projectId.value}`)
}
```

---

## 立即执行

请让我来修改代码并重新部署。
