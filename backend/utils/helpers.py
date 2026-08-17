"""
工具函数集合
"""
import uuid
from datetime import datetime
from typing import Optional, List


def generate_id() -> str:
    """生成UUID"""
    return str(uuid.uuid4())


def format_datetime(dt: datetime) -> str:
    """格式化日期时间"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
    """解析日期时间"""
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except:
        return None


def calculate_price_by_tokens(token_cost: float) -> float:
    """根据Token成本计算用户价格"""
    from config import settings
    if token_cost <= settings.PRICING_FIXED_THRESHOLD:
        return settings.PRICING_FIXED_PRICE
    return token_cost * settings.PRICING_MULTIPLIER


def validate_phone(phone: str) -> bool:
    """验证手机号格式"""
    import re
    return bool(re.match(r"^1[3-9]\d{9}$", phone))


def validate_code(code: str) -> bool:
    """验证码格式验证"""
    return code.isdigit() and 4 <= len(code) <= 6


def mask_phone(phone: str) -> str:
    """手机号脱敏"""
    if len(phone) == 11:
        return phone[:3] + "****" + phone[7:]
    return phone


def mask_wechat(wechat: str) -> str:
    """微信号脱敏"""
    if wechat and len(wechat) > 4:
        return wechat[:2] + "****" + wechat[-2:]
    return wechat or ""


def get_client_ip(request) -> str:
    """获取客户端IP"""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def get_user_agent(request) -> str:
    """获取用户代理"""
    return request.headers.get("user-agent", "unknown")
