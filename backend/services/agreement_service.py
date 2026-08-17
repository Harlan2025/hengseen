"""
协议管理服务 - V1.4新增
"""
from typing import Optional, List
from datetime import datetime
from database import supabase


class AgreementService:
    """协议管理服务"""
    
    @staticmethod
    async def get_active_agreement(agreement_type: str) -> Optional[dict]:
        """获取当前生效的协议"""
        result = supabase.table("agreements").select("*").eq(
            "agreement_type", agreement_type
        ).eq("is_active", True).single().execute()
        return result.data if result.data else None
    
    @staticmethod
    async def get_all_agreements() -> List[dict]:
        """获取所有协议版本"""
        result = supabase.table("agreements").select("*").order(
            "created_at", desc=True
        ).execute()
        return result.data or []
    
    @staticmethod
    async def create_agreement(
        agreement_type: str,
        title: str,
        content: str,
        version: str,
        updated_by: Optional[str] = None
    ) -> dict:
        """创建新协议版本"""
        import uuid
        from datetime import datetime
        
        # 停用旧版本
        supabase.table("agreements").update({
            "is_active": False
        }).eq("agreement_type", agreement_type).execute()
        
        # 创建新版本
        agreement_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        result = supabase.table("agreements").insert({
            "agreement_id": agreement_id,
            "agreement_type": agreement_type,
            "title": title,
            "content": content,
            "version": version,
            "is_active": True,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "updated_by": updated_by,
        }).execute()
        
        return result.data
    
    @staticmethod
    async def record_consent(
        user_id: str,
        agreement_type: str,
        version: str,
        ip_address: str = "",
        device_info: str = ""
    ) -> bool:
        """记录用户协议同意"""
        import uuid
        from datetime import datetime
        
        # 更新旧记录
        supabase.table("user_agreement_consents").update({
            "is_current": False
        }).eq("user_id", user_id).eq("agreement_type", agreement_type).execute()
        
        # 插入新记录
        consent_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        result = supabase.table("user_agreement_consents").insert({
            "consent_id": consent_id,
            "user_id": user_id,
            "agreement_type": agreement_type,
            "version": version,
            "agreed_at": now.isoformat(),
            "ip_address": ip_address,
            "device_info": device_info,
            "is_current": True,
        }).execute()
        
        return bool(result.data)
    
    @staticmethod
    async def get_user_consents(user_id: str) -> dict:
        """获取用户协议同意记录"""
        result = supabase.table("user_agreement_consents").select("*").eq(
            "user_id", user_id
        ).execute()
        
        consents = {}
        for record in result.data or []:
            if record.get("is_current"):
                consents[record["agreement_type"]] = {
                    "version": record["version"],
                    "agreed_at": record["agreed_at"]
                }
        
        # 检查是否需要重新同意
        current = await AgreementService.get_active_agreement("user_agreement")
        needs_reagree = False
        if current:
            user_consent = consents.get("user_agreement")
            if not user_consent or user_consent.get("version") != current.get("version"):
                needs_reagree = True
        
        return {
            "user_agreement": consents.get("user_agreement"),
            "privacy_policy": consents.get("privacy_policy"),
            "needs_reagree": needs_reagree
        }


# 全局实例
agreement_service = AgreementService()
