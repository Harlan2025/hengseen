"""
Supabase客户端 - 使用service_role key进行所有操作
"""
import httpx
from typing import Dict, List, Any, Optional


class SupabaseClient:
    """Supabase REST API客户端 - 使用service_role key"""
    
    def __init__(self):
        self.url = "https://rtmldrysnwzbkgiihnuc.supabase.co"
        self.service_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ0bWxkcnlzbnd6YmtnaWlobnVjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4Njg2OTQ0MiwiZXhwIjoyMTAyNDQ1NDQyfQ.shFfv9SInnRZ2BqlRkNQ2udIudkm2sSyvwkHz-m_3I4"
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头（使用service_role）"""
        return {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def table(self, table_name: str):
        """获取表对象"""
        return TableQuery(self, table_name)


class TableQuery:
    """表查询 - 支持链式调用"""
    
    def __init__(self, client: SupabaseClient, table_name: str):
        self._client = client
        self._table = table_name
        self._url = f"{client.url}/rest/v1/{table_name}"
        self._filters = []
        self._order_by = None
        self._order_desc = False
        self._limit = None
        self._offset = None
        self._select = "*"
        self._is_single = False
        self._operation = None
    
    def select(self, columns: str = "*"):
        """选择列"""
        self._select = columns
        return self
    
    def eq(self, column: str, value: Any):
        """等于过滤"""
        # 处理布尔值：Python的True/False需要转成小写
        if isinstance(value, bool):
            value = "true" if value else "false"
        self._filters.append(f"{column}=eq.{value}")
        return self
    
    def ne(self, column: str, value: Any):
        """不等于过滤"""
        self._filters.append(f"{column}=neq.{value}")
        return self
    
    def gte(self, column: str, value: Any):
        """大于等于"""
        self._filters.append(f"{column}=gte.{value}")
        return self
    
    def lt(self, column: str, value: Any):
        """小于"""
        self._filters.append(f"{column}=lt.{value}")
        return self
    
    def order(self, column: str, desc: bool = False):
        """排序"""
        self._order_by = column
        self._order_desc = desc
        return self
    
    def limit(self, count: int):
        """限制数量"""
        self._limit = count
        return self
    
    def offset(self, count: int):
        """偏移"""
        self._offset = count
        return self
    
    def single(self):
        """返回单条记录（设置标志）"""
        self._is_single = True
        return self
    
    def maybe_single(self):
        """可能返回单条"""
        return self
    
    def insert(self, data: Dict):
        """插入记录"""
        self._operation = ("insert", data)
        return self
    
    def upsert(self, data: Dict):
        """插入或更新"""
        self._operation = ("upsert", data)
        return self
    
    def update(self, data: Dict):
        """更新记录"""
        self._operation = ("update", data)
        return self
    
    def delete(self):
        """删除记录"""
        self._operation = ("delete", None)
        return self
    
    def execute(self):
        """执行查询/操作"""
        if self._operation:
            op_type, op_data = self._operation
            return self._execute_mutation(op_type, op_data)
        else:
            return self._execute_select()
    
    def _build_url(self) -> str:
        """构建查询URL"""
        url = self._url
        
        # 始终添加 select=* 以确保返回所有列
        params = []
        if self._select:
            params.append(f"select={self._select}")
        
        if self._filters:
            params.extend(self._filters)
        
        if self._is_single:
            params.append("limit=1")
        
        if self._order_by:
            order = f"{self._order_by}.asc"
            if self._order_desc:
                order = f"{self._order_by}.desc"
            params.append(f"order={order}")
        
        if self._limit:
            params.append(f"limit={self._limit}")
        
        if self._offset:
            params.append(f"offset={self._offset}")
        
        if params:
            url += "?" + "&".join(params)
        
        return url
    
    def _execute_select(self):
        """执行SELECT"""
        url = self._build_url()
        headers = self._client._get_headers()
        
        with httpx.Client() as client:
            resp = client.get(url, headers=headers)
            
            if resp.status_code == 404:
                return MockResult([])
            
            if resp.status_code != 200:
                print(f"Supabase error: {resp.status_code} {resp.text}")
                return MockResult([])
            
            try:
                data = resp.json()
                if self._is_single:
                    return MockSingleResult(data[0] if data else None)
                return MockResult(data if isinstance(data, list) else [data])
            except Exception as e:
                print(f"Parse error: {e}")
                return MockResult([])
    
    def _execute_mutation(self, op_type: str, data: Dict):
        """执行INSERT/UPDATE/DELETE"""
        url = self._build_url()
        headers = self._client._get_headers()
        
        with httpx.Client() as client:
            if op_type == "insert":
                headers["Prefer"] = "return=representation"
                resp = client.post(url, json=data, headers=headers)
            elif op_type == "upsert":
                headers["Prefer"] = "resolution=merge-duplicates,return=representation"
                resp = client.post(url, json=data, headers=headers)
            elif op_type == "update":
                headers["Prefer"] = "return=representation"
                resp = client.patch(url, json=data, headers=headers)
            elif op_type == "delete":
                resp = client.delete(url, headers=headers)
            else:
                return MockResult([])
            
            if resp.status_code in (200, 201, 204):
                try:
                    if resp.status_code == 204:
                        return MockResult([])
                    result_data = resp.json()
                    return MockResult(result_data if isinstance(result_data, list) else [result_data])
                except:
                    return MockResult([])
            
            print(f"Mutation error {resp.status_code}: {resp.text}")
            return MockResult([])


class MockSingleResult:
    """模拟单条查询结果"""
    def __init__(self, data):
        self.data = data
        self.count = 1 if data else 0
    
    def execute(self):
        return MockResult([self.data] if self.data else [])


class MockResult:
    """模拟查询结果"""
    def __init__(self, data):
        self.data = data
        self.count = len(data) if data else 0


# 创建全局实例
supabase = SupabaseClient()
