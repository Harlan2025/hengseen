"""
人工服务模块 - 专家联系方式管理
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
    ExpertCreateRequest, ExpertInfo, ApiResponse
)
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/experts", tags=["人工服务"])


@router.get("/{project_id}", response_model=ApiResponse)
async def list_experts(project_id: str, user_data: dict = Depends(get_current_user)):
    """获取项目专家列表"""
    await get_project_check(user_id=user_data["sub"], project_id=project_id)
    
    result = supabase.table("project_experts").select("*").eq("project_id", project_id).execute()
    items = [ExpertInfo(**row) for row in (result.data or [])]
    return ApiResponse(data=items)


@router.post("/{project_id}", response_model=ApiResponse)
async def create_expert(project_id: str, req: ExpertCreateRequest, user_data: dict = Depends(get_current_user)):
    """添加专家联系人"""
    await get_project_check(user_id=user_data["sub"], project_id=project_id)
    
    expert_id = str(uuid.uuid4())
    supabase.table("project_experts").insert({
        "expert_id": expert_id,
        "project_id": project_id,
        "expert_name": req.expert_name,
        "title": req.title,
        "wechat": req.wechat,
        "qq": req.qq,
        "email": req.email,
        "tags": req.tags,
        "is_public": req.is_public,
        "added_by": user_data["sub"],
        "created_at": datetime.utcnow().isoformat(),
    }).execute()
    
    return ApiResponse(data={"expert_id": expert_id})


@router.delete("/{project_id}/{expert_id}", response_model=ApiResponse)
async def delete_expert(project_id: str, expert_id: str, user_data: dict = Depends(get_current_user)):
    """删除专家联系人"""
    supabase.table("project_experts").delete().eq("expert_id", expert_id).eq("project_id", project_id).execute()
    return ApiResponse(msg="删除成功")


async def get_project_check(user_id: str, project_id: str) -> dict:
    result = supabase.table("contract_projects").select("*").eq("project_id", project_id).eq("user_id", user_id).single().execute()
    return result.data if result.data else None


def get_auth_header(credentials: dict = Depends(HTTPBearer())) -> dict:
    """获取认证头"""
    from utils.auth_utils import get_current_user as auth_get_current_user
    return auth_get_current_user(credentials)
