"""
认证辅助函数 - 所有路由共享
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from config import settings
from utils.token import decode_token


security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """获取当前登录用户"""
    try:
        token = credentials.credentials
        payload = decode_token(token, settings.JWT_SECRET_KEY)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌已过期或无效"
        )


def require_admin(user_data: Optional[dict] = None) -> bool:
    """检查是否为管理员"""
    # TODO: 实现管理员权限检查
    return True
