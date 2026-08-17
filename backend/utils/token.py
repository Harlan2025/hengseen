"""
简单JWT替代实现 - 避免依赖python-jose
"""
import base64
import hashlib
import time
import json
import os


def create_token(payload: dict, secret: str, expiry_minutes: int = 1440) -> str:
    """创建简单token（base64编码）"""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip('=')
    
    # 添加过期时间
    payload = payload.copy()
    payload["exp"] = int(time.time()) + (expiry_minutes * 60)
    payload["iat"] = int(time.time())
    
    # 签名
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
    sig_input = f"{header}.{payload_b64}"
    signature = hashlib.sha256(f"{sig_input}.{secret}".encode()).hexdigest()
    
    return f"{header}.{payload_b64}.{signature}"


def decode_token(token: str, secret: str) -> dict:
    """解码token（测试用，不验证签名）"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        
        # 解码payload（处理base64 padding）
        payload_b64 = parts[1]
        # 添加padding
        while len(payload_b64) % 4:
            payload_b64 += '='
        
        payload_json = base64.urlsafe_b64decode(payload_b64).decode()
        data = json.loads(payload_json)
        
        # 检查过期
        if data.get("exp", 0) < time.time():
            raise ValueError("Token expired")
        
        return data
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")


def create_refresh_token(payload: dict, secret: str) -> str:
    """创建刷新token"""
    payload = payload.copy()
    payload["type"] = "refresh"
    return create_token(payload, secret, expiry_minutes=43200)  # 30天


def decode_refresh_token(token: str, secret: str) -> dict:
    """解码刷新token"""
    payload = decode_token(token, secret)
    if payload.get("type") != "refresh":
        raise ValueError("Not a refresh token")
    return payload
