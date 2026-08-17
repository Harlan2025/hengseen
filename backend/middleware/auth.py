"""
认证中间件 - JWT验证（使用自定义token实现）
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from config import settings
from utils.token import decode_token


security = HTTPBearer()


async def get_current_user(request: Request) -> Optional[dict]:
    """从请求中获取当前用户信息"""
    credentials = await security.get_security(request)
    
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = decode_token(token, settings.JWT_SECRET_KEY)
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_auth(request: Request) -> dict:
    """要求必须登录"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="需要登录",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def optional_auth(request: Request) -> Optional[dict]:
    """可选登录（匿名也可访问）"""
    try:
        return await get_current_user(request)
    except:
        return None


# 导出中间件
auth_middleware = {
    "require_auth": require_auth,
    "optional_auth": optional_auth,
}
