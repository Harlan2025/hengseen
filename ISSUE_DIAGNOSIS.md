# 问题诊断报告

## 问题1：创建项目提示"非法类型组合"

### 原因分析
后端 `projects.py` 第33-38行验证逻辑：
```python
valid_combinations = {
    "A": [["B"], ["G"], ["H"], ["I"], ["B", "G"]],
    "B": [["A"], ["C"], ["D"]],
    ...
}
```

当前只允许特定组合，例如：
- 主类型 A（买卖）只能搭配：B、G、H、I、或 B+G
- 不能随意搭配其他类型

### 前端问题
前端 `ProjectList.vue` 第97-108行，附属类型显示所有选项（A-J），导致用户可能选择不合法的组合。

---

## 问题2：登录只显示基本信息

### 后端正常
`https://hengseen-backend.fly.dev/` 返回：
```json
{"name":"衡简叙约","version":"1.4.0","mode":"production","status":"running"}
```
这是 **health check** 端点，正常！

### 登录接口正常
`POST /api/v1/auth/login` 返回：
```json
{"code":0,"msg":"成功","data":{"user_id":"ca090bc0-...","access_token":"eyJhbG..."}}
```
登录接口正常工作！

### 可能原因
前端 `.env.production` 配置的 API 地址可能不正确，导致请求失败。

---

## 解决方案

### 1. 修复类型组合验证（放宽限制）

修改后端允许更多组合：
```python
valid_combinations = {
    "A": [["B"], ["G"], ["H"], ["I"], ["B", "G"], []],  # 允许空
    "B": [["A"], ["C"], ["D"], []],
    "C": [["D"], ["G"], ["A"], ["I"], []],
    # ... 其他类型也允许空
}
```

### 2. 更新前端环境变量

检查 `.env.production` 配置：
```
VITE_API_URL=https://hengseen-backend.fly.dev/api/v1
```

---

请告诉我：
1. 你选择的是什么类型组合？（例如：主类型A + 附属类型B）
2. 前端访问地址是什么？（哪个域名？）

这样我可以精确定位问题。
