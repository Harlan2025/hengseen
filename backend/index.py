"""
Cloudflare Workers 入口文件
需要导出 fetch 事件处理器
"""
import os
import sys

# 设置环境变量（如果未设置）
os.environ.setdefault("AI_PROVIDER", "mock")
os.environ.setdefault("DEBUG", "false")

# Cloudflare Workers 响应类
class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}
    
    def json(self, data):
        import json
        return Response(
            body=json.dumps(data).encode(),
            status=self.status,
            headers={"Content-Type": "application/json"}
        )

# 导入 FastAPI 应用
from main import app
from starlette.requests import Request
from starlette.datastructures import Headers

async def fetch(request):
    """Cloudflare Workers 入口函数 - 必须命名为 fetch"""
    try:
        # 构建 Starlette Request
        headers_list = []
        for key, value in request.headers.items():
            headers_list.append((key.encode(), value.encode()))
        
        starlette_headers = Headers(raw=headers_list)
        
        # 读取请求体
        body = await request.text()
        
        starlette_request = Request({
            "type": "http",
            "method": request.method,
            "path": request.url.path,
            "headers": starlette_headers,
            "query_string": request.url.query.encode(),
            "server": (request.url.host, 443),
            "client": None,
            "scheme": "https",
            "root_path": "",
        })
        
        # 调用 FastAPI
        response = await app(starlette_request, lambda: None)
        
        # 读取响应体
        body_bytes = b""
        if hasattr(response, 'body_iterator'):
            async for chunk in response.body_iterator:
                if isinstance(chunk, str):
                    body_bytes += chunk.encode()
                else:
                    body_bytes += chunk
        
        # 返回响应
        return Response(
            body=body_bytes,
            status=response.status_code,
            headers=dict(response.headers)
        )
        
    except Exception as e:
        import traceback
        return Response(
            body=f"Error: {str(e)}\n{traceback.format_exc()}".encode(),
            status=500,
            headers={"Content-Type": "text/plain"}
        )

# 导出供 Cloudflare Workers 使用
__all__ = ["fetch"]
