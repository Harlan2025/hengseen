"""
Pydantic数据模型定义
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ========== 枚举类型 ==========
class AgreementType(str, Enum):
    USER_AGREEMENT = "user_agreement"
    PRIVACY_POLICY = "privacy_policy"


class ProjectStatus(str, Enum):
    INIT = "init"
    INTERVIEWING = "interviewing"
    OUTLINE_GENERATED = "outline_generated"
    CONTRACT_GENERATED = "contract_generated"
    READY_EXPORT = "ready_export"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class RefundStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class ExportFormat(str, Enum):
    WORD = "word"
    MARKDOWN = "markdown"


# ========== 认证相关 ==========
class RegisterRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    code: str = Field(..., min_length=4, max_length=6, description="验证码")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    agree_user_agreement: bool = Field(..., description="是否同意用户协议")
    agree_privacy_policy: bool = Field(..., description="是否同意隐私政策")
    agreement_version: str = Field(..., description="协议版本号")


class LoginRequest(BaseModel):
    phone: str = Field(..., min_length=11, max_length=11)
    code: str = Field(..., min_length=4, max_length=6)
    agree_user_agreement: bool = Field(..., description="是否同意用户协议")
    agree_privacy_policy: bool = Field(..., description="是否同意隐私政策")
    agreement_version: str = Field(..., description="协议版本号")


class WechatLoginRequest(BaseModel):
    code: str = Field(..., description="微信授权码")
    platform: str = Field(..., description="平台：wechat_miniapp/wechat_app")
    agree_user_agreement: bool = Field(..., description="是否同意用户协议")
    agree_privacy_policy: bool = Field(..., description="是否同意隐私政策")
    agreement_version: str = Field(..., description="协议版本号")


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserProfile(BaseModel):
    user_id: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    login_type: str = "phone"
    created_at: datetime
    agreed_at: Optional[datetime] = None
    agreement_version: Optional[str] = None


# ========== 协议相关 ==========
class AgreementContent(BaseModel):
    agreement_id: str
    agreement_type: AgreementType
    title: str
    content: str
    version: str
    is_active: bool
    updated_at: datetime


class AgreementsResponse(BaseModel):
    user_agreement: AgreementContent
    privacy_policy: AgreementContent


class AgreementConsent(BaseModel):
    version: str
    agreed_at: datetime


class ConsentResponse(BaseModel):
    user_agreement: Optional[AgreementConsent] = None
    privacy_policy: Optional[AgreementConsent] = None
    needs_reagree: bool = False


# ========== 项目相关 ==========
class FileTypeChoice(BaseModel):
    code: str  # A-J
    name: str
    description: str


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    primary_type: str = Field(..., description="主类型代码：A-J")
    secondary_types: List[str] = Field(default=[], max_length=2, description="附属类型代码列表，最多2个")


class ProjectInfo(BaseModel):
    project_id: str
    name: str
    primary_type: str
    secondary_types: List[str]
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    total: int
    items: List[ProjectInfo]


# ========== 访谈相关 ==========
class InterviewQuestion(BaseModel):
    question_id: str
    question_text: str
    category: str  # 已确认要素/待确认要素/风险
    required: bool = True


class InterviewAnswer(BaseModel):
    answer: str


class InterviewSnapshot(BaseModel):
    snapshot_id: str
    step: int
    confirmed_elements: List[Dict[str, Any]]
    pending_elements: List[Dict[str, Any]]
    risks: List[Dict[str, Any]]
    created_at: datetime


# ========== 大纲相关 ==========
class OutlineChapter(BaseModel):
    chapter_id: str
    title: str
    content: str
    order: int


class OutlineGenerateRequest(BaseModel):
    project_id: str


class OutlineResponse(BaseModel):
    project_id: str
    chapters: List[OutlineChapter]
    risks: List[Dict[str, Any]]
    generated_at: datetime


# ========== 合同文本相关 ==========
class ContractGenerateRequest(BaseModel):
    project_id: str
    custom_contents: Optional[List[Dict[str, Any]]] = None


class ContractTextResponse(BaseModel):
    project_id: str
    contract_text: str
    risk_notes: List[str]
    generated_at: datetime
    has_custom_content: bool = False


# ========== 导出相关 ==========
class ExportRequest(BaseModel):
    project_id: str
    format: ExportFormat


class ExportHistoryItem(BaseModel):
    export_id: str
    project_id: str
    format: str
    file_url: str
    exported_at: datetime


# ========== 支付相关 ==========
class PaymentCreateRequest(BaseModel):
    project_id: str
    payment_method: str = Field(..., description="wechat/alipay")


class PaymentQRCode(BaseModel):
    order_id: str
    qr_code_url: str
    amount: float
    expire_at: datetime
    payment_method: str


class PaymentStatusResponse(BaseModel):
    order_id: str
    status: PaymentStatus
    amount: float
    paid_at: Optional[datetime] = None


# ========== 退款相关 ==========
class RefundRequest(BaseModel):
    order_id: str
    reason: str = Field(..., min_length=10, max_length=500)


class RefundStatusResponse(BaseModel):
    refund_id: str
    order_id: str
    status: RefundStatus
    amount: float
    applied_at: datetime
    processed_at: Optional[datetime] = None


# ========== 人工服务相关 ==========
class ExpertCreateRequest(BaseModel):
    expert_name: str
    title: Optional[str] = None
    wechat: Optional[str] = None
    qq: Optional[str] = None
    email: Optional[str] = None
    tags: List[str] = []
    is_public: bool = False


class ExpertInfo(BaseModel):
    expert_id: str
    project_id: str
    expert_name: str
    title: Optional[str] = None
    wechat: Optional[str] = None
    qq: Optional[str] = None
    email: Optional[str] = None
    tags: List[str]
    is_public: bool
    added_by: str
    created_at: datetime


# ========== 自定义内容相关 ==========
class CustomContentCreateRequest(BaseModel):
    chapter_id: Optional[str] = None
    content: str = Field(..., min_length=1)
    content_type: str = "custom"  # custom/fragment


class CustomContentItem(BaseModel):
    custom_content_id: str
    project_id: str
    chapter_id: Optional[str] = None
    content_type: str
    content: str
    inserted_at: datetime
    inserted_by: str


# ========== 后台管理相关 ==========
class PricingConfigUpdate(BaseModel):
    fixed_threshold: Optional[float] = None
    fixed_price: Optional[float] = None
    multiplier: Optional[float] = None


class AgreementAdminCreateRequest(BaseModel):
    agreement_type: AgreementType
    title: str
    content: str
    version: str


class AgreementAdminUpdateRequest(BaseModel):
    content: str
    version: str


class AgreementAdminListResponse(BaseModel):
    list: List[Dict[str, Any]]


class AgreementAdminDetailResponse(BaseModel):
    agreement_id: str
    agreement_type: str
    title: str
    content: str
    version: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    updated_by: Optional[str] = None


class ConsentStatistics(BaseModel):
    agreement_id: str
    version: str
    total_users: int
    agreed_users: int
    pending_users: int
    agreement_rate: float


# ========== 通用响应格式 ==========
class ApiResponse(BaseModel):
    code: int = 0
    msg: str = "成功"
    data: Optional[Any] = None
