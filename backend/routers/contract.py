"""
合同文本模块 - AI生成合同文本
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
    ContractGenerateRequest, ContractTextResponse,
    ApiResponse, ProjectStatus
)
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/contract", tags=["合同文本"])


# ========== 生成合同文本 ==========
@router.post("/generate", response_model=ApiResponse)
async def generate_contract(req: ContractGenerateRequest, user_data: dict = Depends(get_current_user)):
    """
    生成完整合同文本
    V1.3新增：支持自定义内容插入
    """
    # 验证项目
    project = await get_project_check(user_id=user_data["sub"], project_id=req.project_id)
    if not project:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "项目不存在"})
    
    if project["status"] not in [
        ProjectStatus.OUTLINE_GENERATED.value,
        ProjectStatus.CONTRACT_GENERATED.value,
        ProjectStatus.READY_EXPORT.value
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 4004, "msg": "项目状态不允许生成合同文本"}
        )
    
    # 获取访谈快照
    snapshot_result = supabase.table("interview_snapshot").select("*").eq("project_id", req.project_id).order("step", desc=True).limit(1).execute()
    latest_snapshot = snapshot_result.data[0] if snapshot_result.data else None
    
    # 获取大纲
    outline_result = supabase.table("outlines").select("*").eq("project_id", req.project_id).single().execute()
    outline = outline_result.data if outline_result.data else None
    
    # 获取自定义内容
    custom_contents = []
    if req.custom_contents:
        # 保存自定义内容
        for cc in req.custom_contents:
            custom_content_id = str(uuid.uuid4())
            supabase.table("custom_contents").insert({
                "custom_content_id": custom_content_id,
                "project_id": req.project_id,
                "chapter_id": cc.get("chapter_id"),
                "content_type": cc.get("content_type", "custom"),
                "content": cc.get("content"),
                "inserted_at": datetime.utcnow().isoformat(),
                "inserted_by": user_data["sub"],
            }).execute()
            custom_contents.append({
                "custom_content_id": custom_content_id,
                **cc
            })
    
    # 调用AI生成合同文本
    contract_text, risk_notes = await generate_contract_text(
        project=project,
        snapshot=latest_snapshot,
        outline=outline,
        custom_contents=custom_contents
    )
    
    # 保存合同文本
    now = datetime.utcnow()
    supabase.table("contract_texts").upsert({
        "project_id": req.project_id,
        "contract_text": contract_text,
        "risk_notes": risk_notes,
        "has_custom_content": len(custom_contents) > 0,
        "generated_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }).execute()
    
    # 更新项目状态
    supabase.table("contract_projects").update({
        "status": ProjectStatus.CONTRACT_GENERATED.value,
        "updated_at": now.isoformat()
    }).eq("project_id", req.project_id).execute()
    
    return ApiResponse(data=ContractTextResponse(
        project_id=req.project_id,
        contract_text=contract_text,
        risk_notes=risk_notes,
        generated_at=now,
        has_custom_content=len(custom_contents) > 0
    ))


# ========== 获取合同文本 ==========
@router.get("/{project_id}", response_model=ApiResponse)
async def get_contract(project_id: str, user_data: dict = Depends(get_current_user)):
    """获取已生成的合同文本"""
    result = supabase.table("contract_texts").select("*").eq("project_id", project_id).single().execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "合同文本尚未生成"})
    
    contract = result.data
    
    return ApiResponse(data={
        "project_id": contract["project_id"],
        "contract_text": contract.get("contract_text", ""),
        "risk_notes": contract.get("risk_notes", []),
        "generated_at": contract.get("generated_at"),
        "has_custom_content": contract.get("has_custom_content", False)
    })


# ========== 复制合同文本 ==========
@router.post("/{project_id}/copy", response_model=ApiResponse)
async def copy_contract(project_id: str, user_data: dict = Depends(get_current_user)):
    """复制合同文本到剪贴板"""
    # 需要登录用户才能复制
    contract_result = supabase.table("contract_texts").select("*").eq("project_id", project_id).single().execute()
    if not contract_result.data:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "合同文本不存在"})
    
    # 检查是否有支付记录
    payment_check = await check_payment_status(project_id, user_data["sub"])
    if not payment_check.get("paid", False):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={"code": 5002, "msg": "需要支付后才能复制合同文本"}
        )
    
    return ApiResponse(data={
        "contract_text": contract_result.data.get("contract_text", "")
    })


# ========== 辅助函数 ==========
async def get_project_check(user_id: str, project_id: str) -> dict:
    """验证项目归属"""
    result = supabase.table("contract_projects").select("*").eq("project_id", project_id).eq("user_id", user_id).single().execute()
    return result.data if result.data else None


async def generate_contract_text(
    project: dict,
    snapshot: dict,
    outline: dict,
    custom_contents: list
) -> tuple:
    """调用AI生成合同文本"""
    # TODO: 实现AI调用逻辑
    contract_text = "# 合同文本\n\n这是一份示例合同文本。\n\n## 第一条 当事人\n\n..."
    risk_notes = ["请注意：本合同为AI生成，仅供参考，不构成法律意见。"]
    return contract_text, risk_notes


async def check_payment_status(project_id: str, user_id: str) -> dict:
    """检查支付状态"""
    result = supabase.table("payment_orders").select("*").eq("project_id", project_id).eq("user_id", user_id).eq("status", "paid").single().execute()
    return {"paid": bool(result.data)}


def get_auth_header(credentials: dict = Depends(HTTPBearer())) -> dict:
    """获取认证头"""
    from utils.auth_utils import get_current_user as auth_get_current_user
    return auth_get_current_user(credentials)
