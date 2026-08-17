"""
后台管理模块 - 定价/模板/协议管理
V1.4新增：协议管理
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime
import uuid

from config import settings
from database import supabase
import uuid
from datetime import datetime
from models.schemas import (
    PricingConfigUpdate, AgreementAdminCreateRequest,
    AgreementAdminUpdateRequest, AgreementAdminListResponse,
    ApiResponse
)
from utils.auth_utils import get_current_user, require_admin

router = APIRouter(prefix="/admin", tags=["后台管理"])


# ========== 定价配置 ==========
@router.get("/pricing")
async def get_pricing(admin: dict = Depends(require_admin)):
    """获取定价配置"""
    result = supabase.table("pricing_config").select("*").single().execute()
    if result.data:
        return {"data": result.data}
    return {"data": {
        "fixed_threshold": settings.PRICING_FIXED_THRESHOLD,
        "fixed_price": settings.PRICING_FIXED_PRICE,
        "multiplier": settings.PRICING_MULTIPLIER,
    }}


@router.post("/pricing", response_model=ApiResponse)
async def update_pricing(req: PricingConfigUpdate, admin: dict = Depends(require_admin)):
    """更新定价配置"""
    supabase.table("pricing_config").upsert({
        "key": "pricing",
        "fixed_threshold": req.fixed_threshold or settings.PRICING_FIXED_THRESHOLD,
        "fixed_price": req.fixed_price or settings.PRICING_FIXED_PRICE,
        "multiplier": req.multiplier or settings.PRICING_MULTIPLIER,
        "updated_at": datetime.utcnow().isoformat(),
    }).execute()
    return ApiResponse(msg="定价配置已更新")


# ========== 协议管理 ==========
@router.get("/agreements", response_model=ApiResponse)
async def list_agreements(admin: dict = Depends(require_admin)):
    """获取协议列表"""
    result = supabase.table("agreements").select("*").order("created_at", desc=True).execute()
    return ApiResponse(data={"list": result.data or []})


@router.get("/agreements/{agreement_id}", response_model=ApiResponse)
async def get_agreement(agreement_id: str, admin: dict = Depends(require_admin)):
    """获取协议详情"""
    result = supabase.table("agreements").select("*").eq("agreement_id", agreement_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "协议不存在"})
    return ApiResponse(data=result.data)


@router.post("/agreements", response_model=ApiResponse)
async def create_agreement(req: AgreementAdminCreateRequest, admin: dict = Depends(require_admin)):
    """创建新协议版本"""
    # 先停用旧版本
    supabase.table("agreements").update({"is_active": False}).eq("agreement_type", req.agreement_type).execute()
    
    agreement_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    supabase.table("agreements").insert({
        "agreement_id": agreement_id,
        "agreement_type": req.agreement_type.value,
        "title": req.title,
        "content": req.content,
        "version": req.version,
        "is_active": True,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "updated_by": admin.get("sub"),
    }).execute()
    
    return ApiResponse(data={"agreement_id": agreement_id, "version": req.version, "is_active": True})


@router.put("/agreements/{agreement_id}", response_model=ApiResponse)
async def update_agreement(agreement_id: str, req: AgreementAdminUpdateRequest, admin: dict = Depends(require_admin)):
    """更新协议内容（生成新版本）"""
    supabase.table("agreements").update({
        "content": req.content,
        "version": req.version,
        "updated_at": datetime.utcnow().isoformat(),
        "updated_by": admin.get("sub"),
    }).eq("agreement_id", agreement_id).execute()
    
    return ApiResponse(msg="协议已更新")


@router.delete("/agreements/{agreement_id}", response_model=ApiResponse)
async def delete_agreement(agreement_id: str, admin: dict = Depends(require_admin)):
    """删除协议版本"""
    # 检查是否为激活版本
    result = supabase.table("agreements").select("is_active").eq("agreement_id", agreement_id).single().execute()
    if result.data and result.data.get("is_active"):
        raise HTTPException(status_code=400, detail={"code": 7005, "msg": "不允许删除激活版本"})
    
    supabase.table("agreements").delete().eq("agreement_id", agreement_id).execute()
    return ApiResponse(msg="删除成功")


@router.get("/agreements/{agreement_id}/consents", response_model=ApiResponse)
async def get_agreement_consents(agreement_id: str, admin: dict = Depends(require_admin)):
    """获取协议同意统计"""
    # TODO: 实现统计逻辑
    return ApiResponse(data=ConsentStatistics(
        agreement_id=agreement_id,
        version="V1.0",
        total_users=1000,
        agreed_users=950,
        pending_users=50,
        agreement_rate=95.0
    ))


# ========== 辅助函数 ==========
def require_admin(admin: dict = Depends(get_current_user)) -> bool:
    """检查管理员权限"""
    # TODO: 实现管理员权限检查
    return True


def get_current_user(credentials: dict = Depends(HTTPBearer())) -> dict:
    from utils.auth_utils import get_current_user, require_admin
