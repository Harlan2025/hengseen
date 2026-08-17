"""
配置管理模块 - 支持测试模式
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "衡简叙约"
    APP_VERSION: str = "1.4.0"
    DEBUG: bool = False
    
    # 测试模式
    TEST_MODE: bool = False
    
    # Supabase配置
    SUPABASE_URL: str = "http://localhost:8000"
    SUPABASE_ANON_KEY: str = "test-anon-key"
    SUPABASE_SERVICE_KEY: str = "test-service-key"
    
    # JWT配置
    JWT_SECRET_KEY: str = "test-jwt-secret-key-for-development-only"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # AI服务配置
    AI_BASE_URL: str = "http://localhost:8000"
    AI_API_KEY: str = "test-api-key"
    AI_MODEL: str = "test-model"
    AI_MAX_TOKENS: int = 4096
    AI_MODE: str = "mock"  # mock | real
    
    # 定价配置
    PRICING_FIXED_THRESHOLD: float = 2.0
    PRICING_FIXED_PRICE: float = 5.99
    PRICING_MULTIPLIER: float = 2.0
    
    # 微信支付配置
    WECHAT_PAY_MCHID: Optional[str] = None
    WECHAT_PAY_API_KEY: Optional[str] = None
    WECHAT_PAY_CERT_PATH: Optional[str] = None
    WECHAT_PAY_PRIVATE_KEY_PATH: Optional[str] = None
    WECHAT_PAY_NOTIFY_URL: Optional[str] = None
    
    # 支付宝配置
    ALIPAY_APP_ID: Optional[str] = None
    ALIPAY_PRIVATE_KEY: Optional[str] = None
    ALIPAY_PUBLIC_KEY: Optional[str] = None
    ALIPAY_NOTIFY_URL: Optional[str] = None
    
    # 域名配置
    DOMAIN: str = "http://localhost:8000"
    
    # 协议版本
    AGREEMENT_VERSION: str = "V1.0"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"


# 全局配置实例
settings = Settings()


def is_test_mode() -> bool:
    """检查是否测试模式"""
    return settings.TEST_MODE or os.getenv("TEST_MODE", "false").lower() == "true"


def get_ai_service():
    """获取AI服务实例"""
    if is_test_mode() or settings.AI_MODE == "mock":
        from mock_ai import ai_service
        return ai_service
    else:
        from services.ai_service import ai_service
        return ai_service
