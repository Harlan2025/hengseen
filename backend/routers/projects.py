"""
项目模块 - 项目创建/列表/详情/状态管理
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
    ProjectCreateRequest, ProjectInfo, ProjectListResponse,
    ApiResponse, ProjectStatus
)
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/projects", tags=["项目"])


# ========== 创建项目 ==========
@router.post("", response_model=ApiResponse)
async def create_project(req: ProjectCreateRequest, user_data: dict = Depends(get_current_user)):
    """创建新项目"""
    # 验证文件类型
    primary_type = validate_file_type(req.primary_type)
    secondary_types = [validate_file_type(t) for t in req.secondary_types]
    
    # 验证组合合法性
    valid_combinations = get_valid_combinations()
    combination_key = f"{primary_type['code']}_{sorted([t['code'] for t in secondary_types])}"
    if primary_type['code'] not in valid_combinations or \
       sorted([t['code'] for t in secondary_types]) not in valid_combinations.get(primary_type['code'], []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 4002, "msg": "非法类型组合"}
        )
    
    # 创建项目
    project_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    supabase.table("contract_projects").insert({
        "project_id": project_id,
        "user_id": user_data["sub"],
        "name": req.name,
        "primary_type": primary_type["code"],
        "secondary_types": [t["code"] for t in secondary_types],
        "status": ProjectStatus.INIT.value,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
    }).execute()
    
    return ApiResponse(data={"project_id": project_id})


# ========== 项目列表 ==========
@router.get("/list", response_model=ApiResponse)
async def list_projects(
    page: int = 1,
    page_size: int = 20,
    status_filter: str = None,
    user_data: dict = Depends(get_current_user)
):
    """获取用户项目列表"""
    user_id = user_data["sub"]
    
    query = supabase.table("contract_projects").select("*").eq("user_id", user_id)
    
    if status_filter:
        query = query.eq("status", status_filter)
    
    # 分页
    from_num = (page - 1) * page_size
    to_num = from_num + page_size - 1
    query = query.limit(to_num - from_num + 1).offset(from_num).order("updated_at", desc=True)
    
    result = query.execute()
    
    items = []
    for row in result.data or []:
        items.append(ProjectInfo(
            project_id=row["project_id"],
            name=row["name"],
            primary_type=row["primary_type"],
            secondary_types=row.get("secondary_types", []),
            status=ProjectStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        ))
    
    # 获取总数（简化处理）
    total_result = supabase.table("contract_projects").select("*").eq("user_id", user_id).execute()
    total = len(total_result.data or [])
    
    return ApiResponse(data=ProjectListResponse(total=total, items=items))


# ========== 项目详情 ==========
@router.get("/{project_id}", response_model=ApiResponse)
async def get_project(project_id: str, user_data: dict = Depends(get_current_user)):
    """获取项目详情"""
    result = supabase.table("contract_projects").select("*").eq("project_id", project_id).eq("user_id", user_data["sub"]).single().execute()
    
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 1003, "msg": "项目不存在"}
        )
    
    project = result.data
    
    # 获取访谈快照
    snapshot_result = supabase.table("interview_snapshot").select("*").eq("project_id", project_id).order("step", desc=True).limit(1).execute()
    latest_snapshot = snapshot_result.data[0] if snapshot_result.data else None
    
    return ApiResponse(data={
        **project,
        "latest_snapshot": latest_snapshot
    })


# ========== 更新项目 ==========
@router.put("/{project_id}", response_model=ApiResponse)
async def update_project(
    project_id: str,
    updates: dict,
    user_data: dict = Depends(get_current_user)
):
    """更新项目信息"""
    # 验证项目存在且属于当前用户
    result = supabase.table("contract_projects").select("project_id").eq("project_id", project_id).eq("user_id", user_data["sub"]).single().execute()
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 1003, "msg": "项目不存在"}
        )
    
    # 更新
    updates["updated_at"] = datetime.utcnow().isoformat()
    supabase.table("contract_projects").update(updates).eq("project_id", project_id).execute()
    
    return ApiResponse(msg="更新成功")


# ========== 删除项目 ==========
@router.delete("/{project_id}", response_model=ApiResponse)
async def delete_project(project_id: str, user_data: dict = Depends(get_current_user)):
    """软删除项目"""
    # 验证项目存在且属于当前用户
    result = supabase.table("contract_projects").select("project_id").eq("project_id", project_id).eq("user_id", user_data["sub"]).single().execute()
    if not result.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 1003, "msg": "项目不存在"}
        )
    
    # 软删除
    supabase.table("contract_projects").update({
        "status": "deleted",
        "deleted_at": datetime.utcnow().isoformat()
    }).eq("project_id", project_id).execute()
    
    return ApiResponse(msg="删除成功")


# ========== 恢复项目 ==========
@router.post("/{project_id}/restore", response_model=ApiResponse)
async def restore_project(project_id: str, user_data: dict = Depends(get_current_user)):
    """恢复已删除项目"""
    supabase.table("contract_projects").update({
        "status": "init",
        "deleted_at": None
    }).eq("project_id", project_id).execute()
    
    return ApiResponse(msg="恢复成功")


# ========== 辅助函数 ==========
def validate_file_type(code: str) -> dict:
    """验证文件类型代码"""
    file_types = {
        "A": {"code": "A", "name": "买卖", "description": "普通商事交易合同"},
        "B": {"code": "B", "name": "备忘录", "description": "确认/意向类文件"},
        "C": {"code": "C", "name": "股权转让", "description": "资本类交易"},
        "D": {"code": "D", "name": "合作", "description": "合作类协议"},
        "E": {"code": "E", "name": "劳动", "description": "人事劳务类"},
        "F": {"code": "F", "name": "知识产权", "description": "知识产权授权许可"},
        "G": {"code": "G", "name": "担保", "description": "担保类文件"},
        "H": {"code": "H", "name": "债权", "description": "债权债务处置类"},
        "I": {"code": "I", "name": "居间", "description": "委托居间代理协议"},
        "J": {"code": "J", "name": "终止", "description": "终止清算类"},
    }
    
    if code not in file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1001, "msg": f"无效的文件类型: {code}"}
        )
    
    return file_types[code]


def get_valid_combinations() -> dict:
    """获取合法组合规则"""
    return {
        "A": [["B"], ["G"], ["H"], ["I"], ["B", "G"]],
        "B": [["A"], ["C"], ["D"]],
        "C": [["D"], ["G"], ["A"], ["I"]],
        "D": [["C"], ["F"], ["A"]],
        "E": [["F"], ["G"]],
        "F": [["G"], ["H"]],
        "G": [["C"], ["H"]],
        "I": [["A"], ["D"]],
    }


def get_auth_header(credentials: dict = Depends(HTTPBearer())) -> dict:
    """获取认证头"""
    from utils.auth_utils import get_current_user as auth_get_current_user
    return auth_get_current_user(credentials)


# 重命名为项目路由使用
get_project_user = get_auth_header
