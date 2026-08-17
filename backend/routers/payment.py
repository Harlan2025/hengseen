"""
支付模块 - 订单创建/查询/回调
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
import uuid

from config import settings
from database import supabase
import uuid
from datetime import datetime, timedelta
from models.schemas import (
    PaymentCreateRequest, PaymentQRCode, PaymentStatusResponse,
    RefundRequest, RefundStatusResponse, ApiResponse, PaymentStatus
)
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/payment", tags=["支付"])


@router.post("/create", response_model=ApiResponse)
async def create_payment(req: PaymentCreateRequest, user_data: dict = Depends(get_current_user)):
    """创建支付订单"""
    project = await get_project_check(user_id=user_data["sub"], project_id=req.project_id)
    if not project:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "项目不存在"})
    
    # 计算金额（读取定价配置）
    amount = calculate_price(project)
    
    order_id = str(uuid.uuid4())
    expire_at = datetime.utcnow() + timedelta(minutes=30)
    
    supabase.table("payment_orders").insert({
        "order_id": order_id,
        "project_id": req.project_id,
        "user_id": user_data["sub"],
        "amount": amount,
        "payment_method": req.payment_method,
        "status": PaymentStatus.PENDING.value,
        "expire_at": expire_at.isoformat(),
        "created_at": datetime.utcnow().isoformat(),
    }).execute()
    
    # 生成二维码
    qr_url = await generate_qr_code(order_id, amount, req.payment_method)
    
    return ApiResponse(data=PaymentQRCode(
        order_id=order_id,
        qr_code_url=qr_url,
        amount=amount,
        expire_at=expire_at,
        payment_method=req.payment_method
    ))


@router.get("/{order_id}/status", response_model=ApiResponse)
async def get_payment_status(order_id: str, user_data: dict = Depends(get_current_user)):
    """查询订单状态"""
    result = supabase.table("payment_orders").select("*").eq("order_id", order_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "订单不存在"})
    
    order = result.data
    return ApiResponse(data=PaymentStatusResponse(
        order_id=order["order_id"],
        status=PaymentStatus(order["status"]),
        amount=order["amount"],
        paid_at=datetime.fromisoformat(order["paid_at"]) if order.get("paid_at") else None
    ))


@router.post("/wechat/callback")
async def wechat_callback(request: dict):
    """微信支付回调"""
    # TODO: 验证签名
    order_id = request.get("out_trade_no")
    transaction_id = request.get("transaction_id")
    
    supabase.table("payment_orders").update({
        "status": PaymentStatus.PAID.value,
        "paid_at": datetime.utcnow().isoformat(),
        "transaction_id": transaction_id,
    }).eq("order_id", order_id).execute()
    
    return {"code": "SUCCESS", "message": "成功"}


@router.post("/alipay/callback")
async def alipay_callback(request: dict):
    """支付宝回调"""
    # TODO: 验证签名
    order_id = request.get("out_trade_no")
    
    supabase.table("payment_orders").update({
        "status": PaymentStatus.PAID.value,
        "paid_at": datetime.utcnow().isoformat(),
    }).eq("order_id", order_id).execute()
    
    return "success"


@router.post("/cancel/{order_id}", response_model=ApiResponse)
async def cancel_payment(order_id: str, user_data: dict = Depends(get_current_user)):
    """取消订单"""
    supabase.table("payment_orders").update({
        "status": PaymentStatus.CANCELLED.value,
    }).eq("order_id", order_id).execute()
    return ApiResponse(msg="订单已取消")


@router.post("/refund", response_model=ApiResponse)
async def request_refund(req: RefundRequest, user_data: dict = Depends(get_current_user)):
    """申请退款"""
    order = await get_order_check(user_id=user_data["sub"], order_id=req.order_id)
    if not order:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "订单不存在"})
    
    if order["status"] != PaymentStatus.PAID.value:
        raise HTTPException(status_code=400, detail={"code": 6002, "msg": "订单状态不允许退款"})
    
    refund_id = str(uuid.uuid4())
    supabase.table("refund_applications").insert({
        "refund_id": refund_id,
        "order_id": req.order_id,
        "user_id": user_data["sub"],
        "reason": req.reason,
        "status": RefundStatus.PENDING.value,
        "applied_at": datetime.utcnow().isoformat(),
    }).execute()
    
    return ApiResponse(data={"refund_id": refund_id})


def calculate_price(project: dict) -> float:
    """计算支付金额"""
    # TODO: 根据Token成本计算
    return settings.PRICING_FIXED_PRICE


async def generate_qr_code(order_id: str, amount: float, method: str) -> str:
    """生成支付二维码"""
    # TODO: 调用微信/支付宝API生成二维码
    return f"https://example.com/qr/{order_id}"


async def get_project_check(user_id: str, project_id: str) -> dict:
    result = supabase.table("contract_projects").select("*").eq("project_id", project_id).eq("user_id", user_id).single().execute()
    return result.data if result.data else None


async def get_order_check(user_id: str, order_id: str) -> dict:
    result = supabase.table("payment_orders").select("*").eq("order_id", order_id).eq("user_id", user_id).single().execute()
    return result.data if result.data else None


def get_auth_header(credentials: dict = Depends(HTTPBearer())) -> dict:
    """获取认证头"""
    from utils.auth_utils import get_current_user as auth_get_current_user
    return auth_get_current_user(credentials)
