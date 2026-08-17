"""
Cloudflare Workers 适配层 - 将 FastAPI 转换为 Worker 格式
"""
import os
import sys
from io import BytesIO
from typing import AsyncGenerator
import asyncio

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 模拟 Cloudflare Events API
class CfEvent:
    def __init__(self, request):
        self.request = request
        
class CfContext:
    pass

def create_runner():
    """创建 FastAPI Runner 适配 Cloudflare Workers"""
    from main import app
    from starlette.routing import Route
    
    async def handle_event(event: CfEvent, context: CfContext):
        request = event.request
        
        # 转换请求
        method = request.method
        url = request.url
        headers = dict(request.headers)
        body = await request.text()
        
        # 调用 FastAPI
        from starlette.requests import Request
        from starlette.datastructures import Headers
        
        starlette_headers = Headers(raw=[
            (k.encode(), v.encode()) for k, v in headers.items()
        ])
        
        starlette_request = Request({
            "type": "http",
            "method": method,
            "path": url.path,
            "headers": starlette_headers,
            "query_string": url.query.encode(),
            "server": (url.host, 443),
            "client": None,
            "scheme": "https",
        })
        
        # 处理请求
        response = await app(starlette_request, lambda: None)
        
        # 转换响应
        status = response.status_code
        resp_headers = dict(response.headers)
        
        # 读取响应体
        body_bytes = b""
        if hasattr(response, 'body_iterator'):
            async for chunk in response.body_iterator:
                body_bytes += chunk
        
        return {
            "status": status,
            "headers": resp_headers,
            "body": body_bytes.decode('utf-8', errors='ignore')
        }
    
    return handle_event

# 导出适合 Cloudflare Workers 的入口
async def fetch(request):
    """Cloudflare Workers 入口函数"""
    try:
        # 导入并运行应用
        from main import app
        from starlette.requests import Request
        from starlette.datastructures import Headers
        
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
        
        # 构建返回响应
        return Response(
            body=body_bytes,
            status=response.status_code,
            headers=dict(response.headers)
        )
        
    except Exception as e:
        import traceback
        return Response(
            body=f"Error: {str(e)}\n{traceback.format_exc()}",
            status=500,
            headers={"Content-Type": "text/plain"}
        )

# Cloudflare Workers 需要的 Response 类
class Response:
    def __init__(self, body, status=200, headers=None):
        self.body = body
        self.status = status
        self.headers = headers or {}
    
    def __await__(self):
        async def await_response():
            return self
        return await_response()

# 导出
exported_fetch = fetch
