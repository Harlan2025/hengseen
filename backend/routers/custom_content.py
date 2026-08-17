"""
自定义内容模块 - V1.3新增
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
    CustomContentCreateRequest, CustomContentItem,
    ApiResponse
)
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/custom-content", tags=["自定义内容"])


@router.get("/{project_id}", response_model=ApiResponse)
async def list_contents(project_id: str, user_data: dict = Depends(get_current_user)):
    """获取项目自定义内容列表"""
    await get_project_check(user_id=user_data["sub"], project_id=project_id)
    
    result = supabase.table("custom_contents").select("*").eq("project_id", project_id).execute()
    
    items = [CustomContentItem(**row) for row in (result.data or [])]
    return ApiResponse(data=items)


@router.post("/{project_id}", response_model=ApiResponse)
async def create_content(project_id: str, req: CustomContentCreateRequest, user_data: dict = Depends(get_current_user)):
    """创建自定义内容"""
    await get_project_check(user_id=user_data["sub"], project_id=project_id)
    
    # 检查数量限制
    count_result = supabase.table("custom_contents").select("*").eq("project_id", project_id).execute()
    if len(count_result.data or []) >= 10:
        raise HTTPException(status_code=400, detail={"code": 4003, "msg": "自定义内容已达上限（10条）"})
    
    content_id = str(uuid.uuid4())
    supabase.table("custom_contents").insert({
        "custom_content_id": content_id,
        "project_id": project_id,
        "chapter_id": req.chapter_id,
        "content_type": req.content_type,
        "content": req.content,
        "inserted_at": datetime.utcnow().isoformat(),
        "inserted_by": user_data["sub"],
    }).execute()
    
    return ApiResponse(data={"custom_content_id": content_id})


@router.put("/{project_id}/{content_id}", response_model=ApiResponse)
async def update_content(
    project_id: str,
    content_id: str,
    updates: dict,
    user_data: dict = Depends(get_current_user)
):
    """更新自定义内容"""
    result = supabase.table("custom_contents").select("*").eq("custom_content_id", content_id).eq("project_id", project_id).single().execute()
    if not result.data:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "内容不存在"})
    
    supabase.table("custom_contents").update(updates).eq("custom_content_id", content_id).execute()
    return ApiResponse(msg="更新成功")


@router.delete("/{project_id}/{content_id}", response_model=ApiResponse)
async def delete_content(project_id: str, content_id: str, user_data: dict = Depends(get_current_user)):
    """删除自定义内容"""
    supabase.table("custom_contents").delete().eq("custom_content_id", content_id).eq("project_id", project_id).execute()
    return ApiResponse(msg="删除成功")


async def get_project_check(user_id: str, project_id: str) -> dict:
    result = supabase.table("contract_projects").select("*").eq("project_id", project_id).eq("user_id", user_id).single().execute()
    return result.data if result.data else None


def get_auth_header(credentials: dict = Depends(HTTPBearer())) -> dict:
    """获取认证头"""
    from utils.auth_utils import get_current_user as auth_get_current_user
    return auth_get_current_user(credentials)
