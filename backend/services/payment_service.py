"""
支付服务封装 - 微信支付和支付宝
"""
import httpx
from typing import Optional, Dict, Any
from config import settings


class WechatPayService:
    """微信支付服务"""
    
    def __init__(self):
        self.mchid = settings.WECHAT_PAY_MCHID
        self.api_key = settings.WECHAT_PAY_API_KEY
        self.notify_url = settings.WECHAT_PAY_NOTIFY_URL
    
    async def create_order(self, order_id: str, amount: float, description: str) -> Dict[str, Any]:
        """创建微信支付订单"""
        # TODO: 实现微信支付API调用
        return {
            "code_url": f"https://weixin.qq.com/api/qr/{order_id}",
            "prepay_id": None
        }
    
    async def verify_callback(self, notification: Dict[str, Any]) -> bool:
        """验证微信回调签名"""
        # TODO: 实现签名验证
        return True


class AlipayService:
    """支付宝服务"""
    
    def __init__(self):
        self.app_id = settings.ALIPAY_APP_ID
        self.private_key = settings.ALIPAY_PRIVATE_KEY
        self.public_key = settings.ALIPAY_PUBLIC_KEY
        self.notify_url = settings.ALIPAY_NOTIFY_URL
    
    async def create_order(self, order_id: str, amount: float, description: str) -> Dict[str, Any]:
        """创建支付宝订单"""
        # TODO: 实现支付宝API调用
        return {
            "qr_code": f"https://qr.alipay.com/{order_id}"
        }
    
    async def verify_callback(self, notification: Dict[str, Any]) -> bool:
        """验证支付宝回调签名"""
        # TODO: 实现签名验证
        return True


# 全局实例
wechat_pay = WechatPayService()
alipay = AlipayService()
