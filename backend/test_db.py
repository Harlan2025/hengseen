"""
内存数据库 - 用于测试模式
替代 Supabase，支持 CRUD 操作
"""
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
import copy


class InMemoryDB:
    """内存数据库实现"""
    
    def __init__(self):
        self.tables: Dict[str, List[Dict]] = {}
        self._init_defaults()
    
    def _init_defaults(self):
        """初始化默认数据"""
        # 协议数据
        self.tables["agreements"] = [
            {
                "agreement_id": str(uuid.uuid4()),
                "agreement_type": "user_agreement",
                "title": "用户协议",
                "content": """欢迎使用衡简叙约！

一、协议范围
本协议是您与衡简叙约之间关于使用本服务所订立的协议。

二、服务内容
衡简叙约提供AI访谈式合同生成服务，帮助用户快速起草各类商事合同。

三、用户权利
1. 用户有权随时删除自己的项目数据
2. 用户可申请导出个人数据
3. 用户可申请删除个人数据

四、隐私保护
我们重视您的隐私，仅收集必要信息，并采取加密措施保护数据安全。

五、免责声明
本平台生成的合同文本仅供参考，不构成法律意见。重大交易请咨询专业律师。

六、协议变更
我们可能会更新本协议，更新后的协议将在平台公示。

七、联系方式
如有疑问，请联系客服邮箱：support@hengseen.com""",
                "version": "V1.0",
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "updated_by": None,
            },
            {
                "agreement_id": str(uuid.uuid4()),
                "agreement_type": "privacy_policy",
                "title": "隐私政策",
                "content": """衡简叙约隐私政策

一、信息收集
我们仅收集提供服务所必需的信息：
- 手机号（用于注册和登录）
- 昵称（可选）
- 项目数据（合同相关内容）

二、信息使用
收集的信息仅用于：
- 提供合同约定的服务
- 改进产品质量
- 发送服务通知

三、信息存储
- 所有数据加密存储
- 采用行级安全策略隔离用户数据
- 匿名用户数据7天后自动清理

四、信息共享
我们不会向第三方共享您的个人信息，除非：
- 获得您的明确同意
- 法律法规要求
- 必要的服务提供商（如支付渠道）

五、您的权利
- 访问您的个人信息
- 更正不准确的信息
- 删除您的账户和数据
- 撤回同意

六、数据安全
我们采取合理的安全措施保护您的数据，包括加密传输和存储。

七、未成年人保护
我们不会故意收集未成年人的个人信息。

八、政策更新
本政策可能会更新，更新后的政策将在平台公示。""",
                "version": "V1.0",
                "is_active": True,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "updated_by": None,
            }
        ]
        
        # 定价配置
        self.tables["pricing_config"] = [
            {
                "key": "pricing",
                "fixed_threshold": 2.0,
                "fixed_price": 5.99,
                "multiplier": 2.0,
                "updated_at": datetime.utcnow().isoformat()
            }
        ]
        
        # 空表初始化
        for table in ["users", "contract_projects", "interview_snapshot", 
                      "chat_history", "outlines", "contract_texts",
                      "export_files", "payment_orders", "refund_applications",
                      "project_experts", "custom_contents", "user_agreement_consents",
                      "team_members", "audit_logs"]:
            self.tables[table] = []
    
    def table(self, name: str):
        """获取表对象"""
        if name not in self.tables:
            self.tables[name] = []
        return TableProxy(self.tables[name])
    
    def get_table(self, name: str) -> List[Dict]:
        """直接获取表数据"""
        return self.tables.get(name, [])
    
    def clear_table(self, name: str):
        """清空表"""
        self.tables[name] = []
    
    def reset_all(self):
        """重置所有数据"""
        self.__init__()


class TableProxy:
    """表查询代理"""
    
    def __init__(self, data: List[Dict]):
        self._data = data
        self._filters = []
        self._order_by = None
        self._order_desc = False
        self._limit_count = None
        self._range_start = None
        self._range_end = None
        self._select_columns = None
        self._count_requested = False
    
    def select(self, *columns):
        """选择列"""
        if len(columns) == 1 and columns[0] == "*":
            self._select_columns = None
        else:
            self._select_columns = columns
        return self
    
    def eq(self, column: str, value: Any):
        """等于条件"""
        self._filters.append({"type": "eq", "column": column, "value": value})
        return self
    
    def ne(self, column: str, value: Any):
        """不等于条件"""
        self._filters.append({"type": "ne", "column": column, "value": value})
        return self
    
    def gte(self, column: str, value: Any):
        """大于等于"""
        self._filters.append({"type": "gte", "column": column, "value": value})
        return self
    
    def lt(self, column: str, value: Any):
        """小于"""
        self._filters.append({"type": "lt", "column": column, "value": value})
        return self
    
    def order(self, column: str, desc: bool = False):
        """排序"""
        self._order_by = column
        self._order_desc = desc
        return self
    
    def limit(self, count: int):
        """限制数量"""
        self._limit_count = count
        return self
    
    def range(self, start: int, end: int):
        """范围查询"""
        self._range_start = start
        self._range_end = end
        return self
    
    def single(self):
        """返回单条记录"""
        return MockSingleQuery(self._execute())
    
    def execute(self):
        """执行查询"""
        results = self._execute()
        return MockExecuteResult(results)
    
    def _execute(self) -> List[Dict]:
        """执行查询逻辑"""
        data = self._data.copy()
        
        # 应用过滤器
        for f in self._filters:
            if f["type"] == "eq":
                data = [r for r in data if r.get(f["column"]) == f["value"]]
            elif f["type"] == "ne":
                data = [r for r in data if r.get(f["column"]) != f["value"]]
            elif f["type"] == "gte":
                data = [r for r in data if r.get(f["column"]) >= f["value"]]
            elif f["type"] == "lt":
                data = [r for r in data if r.get(f["column"]) < f["value"]]
        
        # 排序
        if self._order_by:
            data.sort(key=lambda x: x.get(self._order_by, ""), reverse=self._order_desc)
        
        # 范围
        if self._range_start is not None and self._range_end is not None:
            data = data[self._range_start:self._range_end + 1]
        elif self._limit_count is not None:
            data = data[:self._limit_count]
        
        # 选择列
        if self._select_columns and self._select_columns != ("*",):
            data = [{k: r.get(k) for k in self._select_columns if k in r} for r in data]
        
        return data
    
    def insert(self, data: Dict):
        """插入记录"""
        if "id" not in data and "project_id" not in data and "user_id" not in data:
            data["id"] = str(uuid.uuid4())
        self._data.append(data)
        return MockExecuteResult([data])
    
    def update(self, data: Dict):
        """更新记录"""
        updated = []
        for i, row in enumerate(self._data):
            # 检查过滤器
            match = True
            for f in self._filters:
                if f["type"] == "eq" and row.get(f["column"]) != f["value"]:
                    match = False
                    break
            if match:
                self._data[i].update(data)
                updated.append(self._data[i])
        return MockExecuteResult(updated)
    
    def delete(self):
        """删除记录"""
        to_remove = []
        for i, row in enumerate(self._data):
            match = True
            for f in self._filters:
                if f["type"] == "eq" and row.get(f["column"]) != f["value"]:
                    match = False
                    break
            if match:
                to_remove.append(i)
        for i in reversed(to_remove):
            self._data.pop(i)
        return MockExecuteResult([])
    
    def upsert(self, data: Dict):
        """插入或更新"""
        # 检查是否存在
        existing = self._execute()
        if existing:
            # 更新
            for i, row in enumerate(self._data):
                if row.get("project_id") == data.get("project_id"):
                    self._data[i].update(data)
                    return MockExecuteResult([self._data[i]])
        # 插入
        data["id"] = str(uuid.uuid4())
        self._data.append(data)
        return MockExecuteResult([data])


class MockResponse:
    """模拟单条响应"""
    def __init__(self, data):
        self.data = data


class MockExecuteResult:
    """模拟执行结果"""
    def __init__(self, data):
        self.data = data
        self.count = len(data) if data else 0


class MockSingleQuery:
    """模拟单条记录查询"""
    def __init__(self, data):
        self.data = data[0] if data else None
    
    def execute(self):
        """执行并返回"""
        return MockExecuteResult([self.data] if self.data else [])


# 全局数据库实例
db = InMemoryDB()
