"""
认证模块 - 注册/登录/协议同意
V1.4新增：协议勾选功能
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime
import uuid
import os

from config import settings, is_test_mode
from database import supabase
from models.schemas import (
    RegisterRequest, LoginRequest, WechatLoginRequest,
    TokenResponse, UserProfile, AgreementsResponse,
    ConsentResponse, ApiResponse, RefreshTokenRequest,
    AgreementContent
)
from utils.auth_utils import get_current_user
from utils.token import create_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["认证"])
security = HTTPBearer()


# ========== 用户注册 ==========
@router.post("/register", response_model=ApiResponse)
async def register(req: RegisterRequest):
    """
    手机号注册
    V1.4: 必须勾选用户协议和隐私政策
    """
    # 验证协议勾选
    if not req.agree_user_agreement:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 7001, "msg": "请先阅读并同意用户协议"}
        )
    if not req.agree_privacy_policy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 7002, "msg": "请先阅读并同意隐私政策"}
        )
    
    # 验证协议版本
    current_agreement = get_current_agreement("user_agreement")
    if current_agreement and req.agreement_version != current_agreement.get("version"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 7003, "msg": "协议版本已更新，请重新阅读并同意"}
        )
    
    # 检查手机号是否已注册
    existing = supabase.table("users").select("user_id").eq("phone", req.phone).single().execute()
    if existing.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1004, "msg": "该手机号已注册"}
        )
    
    # 创建用户记录
    user_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    supabase.table("users").insert({
        "user_id": user_id,
        "auth_id": user_id,
        "phone": req.phone,
        "nickname": req.nickname or req.phone[:6] + "****",
        "login_type": "phone",
        "created_at": now.isoformat(),
    }).execute()
    
    # 记录协议同意
    record_agreement_consent(user_id, "user_agreement", req.agreement_version)
    record_agreement_consent(user_id, "privacy_policy", req.agreement_version)
    
    # 创建JWT
    access_token = create_token({"sub": user_id, "phone": req.phone}, settings.JWT_SECRET_KEY)
    refresh_token = create_refresh_token({"sub": user_id}, settings.JWT_SECRET_KEY)
    
    return ApiResponse(data=TokenResponse(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token
    ))


# ========== 用户登录 ==========
@router.post("/login", response_model=ApiResponse)
async def login(req: LoginRequest):
    """
    手机号+验证码登录
    V1.4: 必须勾选用户协议和隐私政策
    """
    # 验证协议勾选
    if not req.agree_user_agreement:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 7001, "msg": "请先阅读并同意用户协议"}
        )
    if not req.agree_privacy_policy:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 7002, "msg": "请先阅读并同意隐私政策"}
        )
    
    # 验证协议版本
    current_agreement = get_current_agreement("user_agreement")
    if current_agreement and req.agreement_version != current_agreement.get("version"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 7003, "msg": "协议版本已更新，请重新阅读并同意"}
        )
    
    # 查找用户
    result = supabase.table("users").select("*").eq("phone", req.phone).single().execute()
    if not result.data:
        # 测试模式下自动创建用户
        if is_test_mode():
            user_id = str(uuid.uuid4())
            now = datetime.utcnow()
            supabase.table("users").insert({
                "user_id": user_id,
                "auth_id": user_id,
                "phone": req.phone,
                "nickname": req.phone[:6] + "****",
                "login_type": "phone",
                "created_at": now.isoformat(),
            }).execute()
            record_agreement_consent(user_id, "user_agreement", req.agreement_version)
            record_agreement_consent(user_id, "privacy_policy", req.agreement_version)
            result.data = {"user_id": user_id, "phone": req.phone}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 2002, "msg": "手机号或验证码错误"}
            )
    
    user = result.data
    
    # 生成JWT
    access_token = create_token({"sub": user["user_id"], "phone": user["phone"]}, settings.JWT_SECRET_KEY)
    refresh_token = create_refresh_token({"sub": user["user_id"]}, settings.JWT_SECRET_KEY)
    
    return ApiResponse(data=TokenResponse(
        user_id=user["user_id"],
        access_token=access_token,
        refresh_token=refresh_token
    ))


# ========== 获取协议内容 ==========
@router.get("/agreements", response_model=ApiResponse)
async def get_agreements():
    """获取当前生效的用户协议和隐私政策内容"""
    user_agreement = get_current_agreement("user_agreement")
    privacy_policy = get_current_agreement("privacy_policy")
    
    if not user_agreement or not privacy_policy:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": 7004, "msg": "协议内容获取失败"}
        )
    
    return ApiResponse(data=AgreementsResponse(
        user_agreement=AgreementContent(**user_agreement),
        privacy_policy=AgreementContent(**privacy_policy)
    ))


# ========== 获取用户协议同意记录 ==========
@router.get("/agreement-consent", response_model=ApiResponse)
async def get_agreement_consent(user_data: dict = Depends(get_current_user)):
    """获取当前用户的协议同意记录"""
    user_id = user_data["sub"]
    consents = get_user_agreement_consents(user_id)
    return ApiResponse(data=ConsentResponse(**consents))


# ========== 获取当前用户信息 ==========
@router.get("/me", response_model=ApiResponse)
async def get_me(user_data: dict = Depends(get_current_user)):
    """获取当前登录用户信息"""
    user_id = user_data["sub"]
    
    result = supabase.table("users").select("*").eq("user_id", user_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "用户不存在"})
    
    user = result.data
    
    return ApiResponse(data=UserProfile(
        user_id=user["user_id"],
        nickname=user.get("nickname"),
        login_type=user.get("login_type", "phone"),
        created_at=datetime.fromisoformat(user["created_at"]),
    ))


# ========== 刷新Token ==========
@router.post("/refresh", response_model=ApiResponse)
async def refresh_token(req: RefreshTokenRequest):
    """使用refresh_token换取新access_token"""
    try:
        payload = decode_refresh_token(req.refresh_token)
        user_id = payload.get("sub")
        
        access_token = create_access_token({"sub": user_id})
        new_refresh_token = create_refresh_token({"sub": user_id})
        
        return ApiResponse(data=TokenResponse(
            user_id=user_id,
            access_token=access_token,
            refresh_token=new_refresh_token
        ))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# ========== 退出登录 ==========
@router.post("/logout")
async def logout(user_data: dict = Depends(get_current_user)):
    """退出登录"""
    return ApiResponse(msg="退出成功")


# ========== 辅助函数 ==========
def get_current_agreement(agreement_type: str) -> dict:
    """获取当前生效的协议内容"""
    result = supabase.table("agreements").select("*").eq("agreement_type", agreement_type).eq("is_active", True).single().execute()
    return result.data if result.data else None


def record_agreement_consent(user_id: str, agreement_type: str, version: str):
    """记录用户协议同意"""
    # 更新旧记录
    supabase.table("user_agreement_consents").update({"is_current": False}).eq("user_id", user_id).eq("agreement_type", agreement_type).execute()
    
    # 插入新记录
    supabase.table("user_agreement_consents").insert({
        "consent_id": str(uuid.uuid4()),
        "user_id": user_id,
        "agreement_type": agreement_type,
        "version": version,
        "agreed_at": datetime.utcnow().isoformat(),
        "ip_address": "127.0.0.1",
        "device_info": "Test Browser",
        "is_current": True,
    }).execute()


def get_user_agreement_consents(user_id: str) -> dict:
    """获取用户协议同意记录"""
    result = supabase.table("user_agreement_consents").select("*").eq("user_id", user_id).execute()
    
    consents = {}
    for record in result.data or []:
        if record.get("is_current"):
            consents[record["agreement_type"]] = {
                "version": record["version"],
                "agreed_at": record["agreed_at"]
            }
    
    # 检查是否需要重新同意
    current_agreement = get_current_agreement("user_agreement")
    needs_reagree = False
    if current_agreement:
        user_consent = consents.get("user_agreement")
        if not user_consent or user_consent.get("version") != current_agreement.get("version"):
            needs_reagree = True
    
    return {
        "user_agreement": consents.get("user_agreement"),
        "privacy_policy": consents.get("privacy_policy"),
        "needs_reagree": needs_reagree
    }
