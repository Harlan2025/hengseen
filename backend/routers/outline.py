"""
大纲模块 - 合同大纲生成与管理
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
    OutlineChapter, OutlineResponse,
    ApiResponse, ProjectStatus
)
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/outline", tags=["大纲"])


# ========== 生成大纲 ==========
@router.post("/generate", response_model=ApiResponse)
async def generate_outline(project_id: str, user_data: dict = Depends(get_current_user)):
    """
    生成合同大纲
    根据访谈快照数据，调用AI生成结构化大纲
    """
    # 验证项目
    project = await get_project_check(user_id=user_data["sub"], project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "项目不存在"})
    
    if project["status"] not in [ProjectStatus.INTERVIEWING.value, ProjectStatus.OUTLINE_GENERATED.value]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 4004, "msg": "项目状态不允许生成大纲"}
        )
    
    # 获取最新访谈快照
    snapshot_result = supabase.table("interview_snapshot").select("*").eq("project_id", project_id).order("step", desc=True).limit(1).execute()
    latest_snapshot = snapshot_result.data[0] if snapshot_result.data else None
    
    # 获取风险库
    risks = await get_risks_for_project(project, latest_snapshot)
    
    # 调用AI生成大纲
    chapters = await generate_outline_chapters(project, latest_snapshot)
    
    # 保存大纲
    outline_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    supabase.table("outlines").upsert({
        "outline_id": outline_id,
        "project_id": project_id,
        "chapters": chapters,
        "risks": risks,
        "generated_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }).execute()
    
    # 更新项目状态
    supabase.table("contract_projects").update({
        "status": ProjectStatus.OUTLINE_GENERATED.value,
        "updated_at": now.isoformat()
    }).eq("project_id", project_id).execute()
    
    return ApiResponse(data=OutlineResponse(
        project_id=project_id,
        chapters=[OutlineChapter(**c) for c in chapters],
        risks=risks,
        generated_at=now
    ))


# ========== 获取大纲 ==========
@router.get("/{project_id}", response_model=ApiResponse)
async def get_outline(project_id: str, user_data: dict = Depends(get_current_user)):
    """获取项目大纲"""
    result = supabase.table("outlines").select("*").eq("project_id", project_id).single().execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "大纲尚未生成"})
    
    outline = result.data
    
    return ApiResponse(data={
        "project_id": outline["project_id"],
        "chapters": outline.get("chapters", []),
        "risks": outline.get("risks", []),
        "generated_at": outline.get("generated_at"),
        "updated_at": outline.get("updated_at")
    })


# ========== 编辑大纲章节 ==========
@router.put("/{project_id}/chapters/{chapter_id}", response_model=ApiResponse)
async def edit_chapter(
    project_id: str,
    chapter_id: str,
    updates: dict,
    user_data: dict = Depends(get_current_user)
):
    """编辑大纲章节"""
    outline = await get_outline_check(user_id=user_data["sub"], project_id=project_id)
    if not outline:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "大纲不存在"})
    
    chapters = outline.get("chapters", [])
    found = False
    for i, ch in enumerate(chapters):
        if ch.get("chapter_id") == chapter_id:
            chapters[i].update(updates)
            found = True
            break
    
    if not found:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "章节不存在"})
    
    supabase.table("outlines").update({
        "chapters": chapters,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("outline_id", outline["outline_id"]).execute()
    
    return ApiResponse(msg="章节已更新")


# ========== 调整章节顺序 ==========
@router.post("/{project_id}/reorder", response_model=ApiResponse)
async def reorder_chapters(
    project_id: str,
    chapter_order: list,
    user_data: dict = Depends(get_current_user)
):
    """调整章节顺序"""
    outline = await get_outline_check(user_id=user_data["sub"], project_id=project_id)
    if not outline:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "大纲不存在"})
    
    chapters = outline.get("chapters", [])
    reordered = []
    
    for cid in chapter_order:
        for ch in chapters:
            if ch.get("chapter_id") == cid:
                reordered.append(ch)
                break
    
    supabase.table("outlines").update({
        "chapters": reordered,
        "updated_at": datetime.utcnow().isoformat()
    }).eq("outline_id", outline["outline_id"]).execute()
    
    return ApiResponse(msg="章节顺序已更新")


# ========== 辅助函数 ==========
async def get_project_check(user_id: str, project_id: str) -> dict:
    """验证项目归属"""
    result = supabase.table("contract_projects").select("*").eq("project_id", project_id).eq("user_id", user_id).single().execute()
    return result.data if result.data else None


async def get_outline_check(user_id: str, project_id: str) -> dict:
    """验证大纲归属"""
    outline = await get_project_check(user_id, project_id)
    if not outline:
        return None
    
    result = supabase.table("outlines").select("*").eq("project_id", project_id).single().execute()
    return result.data if result.data else None


async def generate_outline_chapters(project: dict, snapshot: dict) -> list:
    """调用AI生成大纲章节"""
    # TODO: 实现AI调用逻辑
    return [
        {"chapter_id": str(uuid.uuid4()), "title": "第一条 合同当事人", "content": "", "order": 1},
        {"chapter_id": str(uuid.uuid4()), "title": "第二条 标的", "content": "", "order": 2},
        {"chapter_id": str(uuid.uuid4()), "title": "第三条 价款及支付", "content": "", "order": 3},
        {"chapter_id": str(uuid.uuid4()), "title": "第四条 履行期限、地点和方式", "content": "", "order": 4},
        {"chapter_id": str(uuid.uuid4()), "title": "第五条 违约责任", "content": "", "order": 5},
        {"chapter_id": str(uuid.uuid4()), "title": "第六条 争议解决", "content": "", "order": 6},
    ]


async def get_risks_for_project(project: dict, snapshot: dict) -> list:
    """获取项目风险清单"""
    # 从风险库匹配风险
    risks = []
    
    # TODO: 实现风险匹配逻辑
    return risks


def get_auth_header(credentials: dict = Depends(HTTPBearer())) -> dict:
    """获取认证头"""
    from utils.auth_utils import get_current_user as auth_get_current_user
    return auth_get_current_user(credentials)
