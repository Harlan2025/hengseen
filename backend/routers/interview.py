"""
访谈模块 - AI对话访谈核心逻辑
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime
import uuid
import json

from config import settings
from database import supabase
import uuid
from datetime import datetime
from models.schemas import (
    InterviewQuestion, InterviewAnswer, InterviewSnapshot,
    ApiResponse, ProjectStatus
)
from utils.auth_utils import get_current_user

router = APIRouter(prefix="/interview", tags=["访谈"])


# ========== 获取当前问题 ==========
@router.get("/{project_id}/question", response_model=ApiResponse)
async def get_current_question(project_id: str, user_data: dict = Depends(get_current_user)):
    """
    获取当前访谈问题
    返回下一步应该问的问题
    """
    # 验证项目
    project = await get_project_check(user_id=user_data["sub"], project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "项目不存在"})
    
    if project["status"] != ProjectStatus.INTERVIEWING.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 4004, "msg": "项目当前状态不允许进行访谈"}
        )
    
    # 获取最新快照，确定当前步骤
    snapshot_result = supabase.table("interview_snapshot").select("*").eq("project_id", project_id).order("step", desc=True).limit(1).execute()
    latest_snapshot = snapshot_result.data[0] if snapshot_result.data else {}
    
    current_step = (latest_snapshot.get("step") or 0) + 1
    
    # 调用AI生成问题
    question = await generate_interview_question(project, current_step, latest_snapshot)
    
    return ApiResponse(data={
        "question_id": str(uuid.uuid4()),
        "step": current_step,
        "question_text": question["text"],
        "category": question["category"],
        "required": question.get("required", True),
        "context": question.get("context", {})
    })


# ========== 提交答案 ==========
@router.post("/{project_id}/answer", response_model=ApiResponse)
async def submit_answer(project_id: str, req: InterviewAnswer, user_data: dict = Depends(get_current_user)):
    """
    提交访谈答案
    AI解析回答，更新访谈快照
    """
    # 验证项目
    project = await get_project_check(user_id=user_data["sub"], project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "项目不存在"})
    
    # 获取最新快照
    snapshot_result = supabase.table("interview_snapshot").select("*").eq("project_id", project_id).order("step", desc=True).limit(1).execute()
    latest_snapshot = snapshot_result.data[0] if snapshot_result.data else {}
    
    current_step = (latest_snapshot.get("step") or 0) + 1
    
    # 调用AI解析回答
    result = await parse_interview_answer(project, latest_snapshot, req.answer, current_step)
    
    # 保存新快照
    snapshot_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    supabase.table("interview_snapshot").insert({
        "snapshot_id": snapshot_id,
        "project_id": project_id,
        "step": current_step,
        "confirmed_elements": result.get("confirmed_elements", []),
        "pending_elements": result.get("pending_elements", []),
        "risks": result.get("risks", []),
        "created_at": now.isoformat(),
    }).execute()
    
    # 检查是否完成所有访谈
    total_questions = calculate_total_questions(project)
    if current_step >= total_questions:
        # 访谈完成，自动生成大纲
        await generate_outline(project_id)
        project_status = ProjectStatus.OUTLINE_GENERATED.value
    else:
        project_status = ProjectStatus.INTERVIEWING.value
    
    # 更新项目状态
    supabase.table("contract_projects").update({
        "status": project_status,
        "updated_at": now.isoformat()
    }).eq("project_id", project_id).execute()
    
    return ApiResponse(data={
        "snapshot_id": snapshot_id,
        "step": current_step,
        "total_steps": total_questions,
        "project_status": project_status,
        "confirmed_elements": result.get("confirmed_elements", []),
        "pending_elements": result.get("pending_elements", []),
        "risks": result.get("risks", []),
    })


# ========== 获取快照列表 ==========
@router.get("/{project_id}/snapshots", response_model=ApiResponse)
async def list_snapshots(project_id: str, user_data: dict = Depends(get_current_user)):
    """获取访谈历史快照列表（用于回溯）"""
    result = supabase.table("interview_snapshot").select("*").eq("project_id", project_id).order("step", asc=True).execute()
    
    snapshots = []
    for row in result.data or []:
        snapshots.append(InterviewSnapshot(
            snapshot_id=row["snapshot_id"],
            step=row["step"],
            confirmed_elements=row.get("confirmed_elements", []),
            pending_elements=row.get("pending_elements", []),
            risks=row.get("risks", []),
            created_at=datetime.fromisoformat(row["created_at"])
        ))
    
    return ApiResponse(data=snapshots)


# ========== 回溯到指定快照 ==========
@router.post("/{project_id}/rollback", response_model=ApiResponse)
async def rollback_to_snapshot(
    project_id: str,
    snapshot_id: str,
    user_data: dict = Depends(get_current_user)
):
    """
    时光机模式：回退到指定历史节点
    """
    # 验证项目
    project = await get_project_check(user_id=user_data["sub"], project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "项目不存在"})
    
    # 验证快照存在
    snapshot_result = supabase.table("interview_snapshot").select("*").eq("snapshot_id", snapshot_id).single().execute()
    if not snapshot_result.data or snapshot_result.data.get("project_id") != project_id:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "快照不存在"})
    
    snapshot = snapshot_result.data
    
    # 删除当前快照之后的所有快照
    supabase.table("interview_snapshot").delete().gte("step", snapshot["step"] + 1).eq("project_id", project_id).execute()
    
    # 更新项目状态
    now = datetime.utcnow()
    supabase.table("contract_projects").update({
        "status": ProjectStatus.INTERVIEWING.value,
        "updated_at": now.isoformat()
    }).eq("project_id", project_id).execute()
    
    return ApiResponse(data={
        "rollback_to_step": snapshot["step"],
        "confirmed_elements": snapshot.get("confirmed_elements", []),
        "pending_elements": snapshot.get("pending_elements", []),
        "risks": snapshot.get("risks", [])
    })


# ========== 重置访谈 ==========
@router.post("/{project_id}/reset", response_model=ApiResponse)
async def reset_interview(project_id: str, user_data: dict = Depends(get_current_user)):
    """
    清空当前访谈状态，重新开始
    """
    project = await get_project_check(user_id=user_data["sub"], project_id=project_id)
    if not project:
        raise HTTPException(status_code=404, detail={"code": 1003, "msg": "项目不存在"})
    
    # 删除所有快照和对话记录
    supabase.table("interview_snapshot").delete().eq("project_id", project_id).execute()
    supabase.table("chat_history").delete().eq("project_id", project_id).execute()
    
    # 重置项目状态
    now = datetime.utcnow()
    supabase.table("contract_projects").update({
        "status": ProjectStatus.INIT.value,
        "updated_at": now.isoformat()
    }).eq("project_id", project_id).execute()
    
    return ApiResponse(msg="访谈已重置")


# ========== 辅助函数 ==========
async def get_project_check(user_id: str, project_id: str) -> dict:
    """验证项目归属"""
    result = supabase.table("contract_projects").select("*").eq("project_id", project_id).eq("user_id", user_id).single().execute()
    return result.data if result.data else None


async def generate_interview_question(project: dict, step: int, last_snapshot: dict = None) -> dict:
    """调用AI生成下一个访谈问题"""
    from services.ai_service import ai_service

    # 构建已确认要素的文本
    confirmed_text = ""
    if last_snapshot and last_snapshot.get("confirmed_elements"):
        confirmed_text = "\n已确认要素：\n"
        for elem in last_snapshot["confirmed_elements"]:
            confirmed_text += f"- {elem.get('element', '')}: {elem.get('value', '')}\n"

    # 构建待确认要素的文本
    pending_text = ""
    if last_snapshot and last_snapshot.get("pending_elements"):
        pending_text = "\n待确认要素：\n"
        for elem in last_snapshot["pending_elements"]:
            pending_text += f"- {elem.get('element', '')}: {elem.get('reason', '')}\n"

    prompt = f"""你是一位专业的法务访谈助手，正在帮助用户完成合同起草访谈。

【项目信息】
- 主类型：{project.get('primary_type', '未知')}
- 附属类型：{', '.join(project.get('secondary_types', [])) if project.get('secondary_types') else '无'}

【已确认的事实】{confirmed_text if confirmed_text else '无'}

【待确认的事项】{pending_text if pending_text else '无'}

【当前步骤】第 {step} 个问题

请根据已确认的事实，提出下一个需要澄清的关键问题。问题应该：
1. 针对当前交易架构中的关键要素
2. 避免重复已确认的信息
3. 帮助用户补充缺失的必要信息

只返回JSON格式，不要其他内容：
{{
    "text": "问题内容",
    "category": "fact_gathering|risk_identification|clarification",
    "required": true
}}"""

    try:
        result = await ai_service.chat([{"role": "user", "content": prompt}])
        # 清理可能的markdown代码块
        result = result.strip()
        if result.startswith("```"):
            # 去除开头的 ```json 或 ```
            lines = result.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            # 去除结尾的 ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            result = "\n".join(lines)
        return json.loads(result)
    except Exception as e:
        print(f"Generate interview question error: {e}")
        return {"text": f"请描述{project.get('primary_type', '')}交易的具体情况...", "category": "fact_gathering", "required": True}


async def parse_interview_answer(
    project: dict,
    last_snapshot: dict,
    answer: str,
    step: int
) -> dict:
    """调用AI解析用户回答，提取结构化信息"""
    from services.ai_service import ai_service

    prompt = f"""请分析用户的回答，提取合同起草所需的关键信息。

【交易类型】
- 主类型：{project.get('primary_type', '未知')}
- 附属类型：{', '.join(project.get('secondary_types', [])) if project.get('secondary_types') else '无'}

【用户回答】
{answer}

【之前已确认的要素】
{json.dumps(last_snapshot.get('confirmed_elements', []), ensure_ascii=False) if last_snapshot else '无'}

请提取以下信息并返回JSON格式：
{{
    "confirmed_elements": [
        {{"element": "要素名称", "value": "要素内容"}}
    ],
    "pending_elements": [
        {{"element": "待确认要素", "reason": "原因说明"}}
    ],
    "risks": [
        {{"level": "high|medium|low", "description": "风险描述"}}
    ]
}}"""

    try:
        result = await ai_service.chat([{"role": "user", "content": prompt}])
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n")[1].rstrip("```")
        return json.loads(result)
    except Exception as e:
        print(f"Parse interview answer error: {e}")
        return {"confirmed_elements": [], "pending_elements": [], "risks": []}


def calculate_total_questions(project: dict) -> int:
    """计算总访谈问题数"""
    # 简化处理，默认20个问题
    return 20


async def generate_outline(project_id: str):
    """生成合同大纲"""
    from routers.outline import generate_outline as outline_service
    await outline_service(project_id)


def get_auth_header(credentials: dict = Depends(HTTPBearer())) -> dict:
    """获取认证头"""
    from utils.auth_utils import get_current_user as auth_get_current_user
    return auth_get_current_user(credentials)
