"""
衡简叙约后端 - API 接口清单
"""

# 认证模块
AUTH_ROUTES = [
    ("POST", "/api/v1/auth/register", "用户注册"),
    ("POST", "/api/v1/auth/login", "用户登录"),
    ("POST", "/api/v1/auth/wechat", "微信授权登录"),
    ("POST", "/api/v1/auth/refresh", "刷新Token"),
    ("POST", "/api/v1/auth/logout", "退出登录"),
    ("GET", "/api/v1/auth/me", "获取当前用户信息"),
    ("GET", "/api/v1/auth/agreements", "获取协议内容"),
    ("GET", "/api/v1/auth/agreement-consent", "获取用户协议同意记录"),
]

# 项目模块
PROJECT_ROUTES = [
    ("POST", "/api/v1/projects", "创建项目"),
    ("GET", "/api/v1/projects/list", "项目列表"),
    ("GET", "/api/v1/projects/{project_id}", "项目详情"),
    ("PUT", "/api/v1/projects/{project_id}", "更新项目"),
    ("DELETE", "/api/v1/projects/{project_id}", "删除项目"),
    ("POST", "/api/v1/projects/{project_id}/restore", "恢复项目"),
]

# 访谈模块
INTERVIEW_ROUTES = [
    ("GET", "/api/v1/interview/{project_id}/question", "获取访谈问题"),
    ("POST", "/api/v1/interview/{project_id}/answer", "提交答案"),
    ("GET", "/api/v1/interview/{project_id}/snapshots", "获取快照列表"),
    ("POST", "/api/v1/interview/{project_id}/rollback", "回溯到指定快照"),
    ("POST", "/api/v1/interview/{project_id}/reset", "重置访谈"),
]

# 大纲模块
OUTLINE_ROUTES = [
    ("POST", "/api/v1/outline/generate", "生成大纲"),
    ("GET", "/api/v1/outline/{project_id}", "获取大纲"),
    ("PUT", "/api/v1/outline/{project_id}/chapters/{chapter_id}", "编辑章节"),
    ("POST", "/api/v1/outline/{project_id}/reorder", "调整章节顺序"),
]

# 合同文本模块
CONTRACT_ROUTES = [
    ("POST", "/api/v1/contract/generate", "生成合同文本"),
    ("GET", "/api/v1/contract/{project_id}", "获取合同文本"),
    ("POST", "/api/v1/contract/{project_id}/copy", "复制合同文本"),
]

# 导出模块
EXPORT_ROUTES = [
    ("POST", "/api/v1/export", "导出文档"),
    ("GET", "/api/v1/export/history/{project_id}", "导出历史"),
    ("GET", "/api/v1/export/{export_id}/download", "下载导出文件"),
]

# 支付模块
PAYMENT_ROUTES = [
    ("POST", "/api/v1/payment/create", "创建支付订单"),
    ("GET", "/api/v1/payment/{order_id}/status", "查询订单状态"),
    ("POST", "/api/v1/payment/wechat/callback", "微信支付回调"),
    ("POST", "/api/v1/payment/alipay/callback", "支付宝回调"),
    ("POST", "/api/v1/payment/cancel/{order_id}", "取消订单"),
    ("POST", "/api/v1/payment/refund", "申请退款"),
]

# 自定义内容模块
CUSTOM_CONTENT_ROUTES = [
    ("GET", "/api/v1/custom-content/{project_id}", "获取自定义内容列表"),
    ("POST", "/api/v1/custom-content/{project_id}", "创建自定义内容"),
    ("PUT", "/api/v1/custom-content/{project_id}/{content_id}", "更新自定义内容"),
    ("DELETE", "/api/v1/custom-content/{project_id}/{content_id}", "删除自定义内容"),
]

# 人工服务模块
EXPERT_ROUTES = [
    ("GET", "/api/v1/experts/{project_id}", "获取专家列表"),
    ("POST", "/api/v1/experts/{project_id}", "添加专家"),
    ("DELETE", "/api/v1/experts/{project_id}/{expert_id}", "删除专家"),
]

# 后台管理模块
ADMIN_ROUTES = [
    ("GET", "/api/v1/admin/pricing", "获取定价配置"),
    ("POST", "/api/v1/admin/pricing", "更新定价配置"),
    ("GET", "/api/v1/admin/agreements", "获取协议列表"),
    ("GET", "/api/v1/admin/agreements/{agreement_id}", "获取协议详情"),
    ("POST", "/api/v1/admin/agreements", "创建协议版本"),
    ("PUT", "/api/v1/admin/agreements/{agreement_id}", "更新协议内容"),
    ("DELETE", "/api/v1/admin/agreements/{agreement_id}", "删除协议版本"),
    ("GET", "/api/v1/admin/agreements/{agreement_id}/consents", "获取同意统计"),
]

# 测试接口
TEST_ROUTES = [
    ("GET", "/api/v1/test/reset", "重置测试数据库"),
]

# 汇总所有路由
ALL_ROUTES = (
    AUTH_ROUTES + PROJECT_ROUTES + INTERVIEW_ROUTES + OUTLINE_ROUTES +
    CONTRACT_ROUTES + EXPORT_ROUTES + PAYMENT_ROUTES + CUSTOM_CONTENT_ROUTES +
    EXPERT_ROUTES + ADMIN_ROUTES + TEST_ROUTES
)

if __name__ == "__main__":
    print("=" * 70)
    print("衡简叙约 Hengseen API 接口清单")
    print("=" * 70)
    
    for method, path, desc in ALL_ROUTES:
        print(f"{method:6} {path:<50} {desc}")
    
    print("\n" + "=" * 70)
    print(f"总计: {len(ALL_ROUTES)} 个接口")
    print("=" * 70)
