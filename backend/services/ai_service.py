"""
AI服务封装 - 支持主流大模型、OpenRouter和Agnes
"""
import httpx
import json
import asyncio
from typing import List, Dict, Any, Optional, Literal
from config import settings


# 支持的模型提供商
ModelProvider = Literal["deepseek", "openrouter", "agnes", "siliconflow", "mock"]

# 默认模型配置
DEFAULT_MODELS = {
    "deepseek": "deepseek/deepseek-chat",
    "openrouter": "openrouter/gpt-4o-mini",
    "agnes": "agnes/agnes-2.5-flash",
    "siliconflow": "siliconflow/qwen-turbo",
    "mock": "mock/default",
}

# API端点配置
API_ENDPOINTS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "models": ["deepseek-chat", "deepseek-coder"],
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "models": [
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            "google/gemini-1.5-pro",
            "google/gemini-1.5-flash",
            "qwen/qwen-72b-chat",
            "qwen/qwen-32b-chat",
        ],
    },
    "agnes": {
        "base_url": lambda: settings.AI_AGNES_BASE_URL.rstrip('/') if hasattr(settings, 'AI_AGNES_BASE_URL') else settings.AI_BASE_URL.rstrip('/'),
        "models": ["agnes-2.5-flash", "agnes-1-flash"],
    },
    "siliconflow": {
        "base_url": "https://api.siliconflow.cn/v1",
        "models": [
            "qwen/qwen-72b-chat",
            "qwen/qwen-32b-chat",
            "deepseek/deepseek-chat",
            "deepseek/deepseek-coder",
        ],
    },
}


class AIService:
    """多模型AI服务客户端"""
    
    def __init__(self):
        self.provider = self._resolve_provider()
        self.model = self._resolve_model()
        self.base_url = self._resolve_base_url()
        self.api_key = self._resolve_api_key()
        self.max_tokens = settings.AI_MAX_TOKENS
    
    def _resolve_provider(self) -> ModelProvider:
        """解析模型提供商"""
        provider = settings.AI_PROVIDER.lower() if hasattr(settings, 'AI_PROVIDER') else 'mock'
        if provider not in DEFAULT_MODELS:
            provider = 'mock'
        return provider
    
    def _resolve_model(self) -> str:
        """解析模型名称"""
        model = settings.AI_MODEL
        if not model:
            model = DEFAULT_MODELS.get(self.provider, "mock/default")
        return model
    
    def _resolve_base_url(self) -> str:
        """解析API基础URL"""
        provider_config = API_ENDPOINTS.get(self.provider, {})
        base_url = provider_config.get("base_url", "")
        # 处理lambda表达式
        if callable(base_url):
            base_url = base_url()
        return base_url
    
    def _resolve_api_key(self) -> str:
        """解析API Key"""
        key_attr = f"AI_{self.provider.upper()}_API_KEY"
        return getattr(settings, key_attr, settings.AI_API_KEY)
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        model: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """调用AI对话接口"""
        if self.provider == "mock":
            return await self._mock_chat(messages, temperature)
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": model or self.model,
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": self.max_tokens,
                        "stream": stream,
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                print(f"AI API error: {e.response.text}")
                return await self._mock_chat(messages, temperature)
            except Exception as e:
                print(f"AI chat error: {e}")
                return await self._mock_chat(messages, temperature)
    
    async def _mock_chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Mock聊天响应（测试用）"""
        from mock_ai import ai_service
        return await ai_service.chat(messages, temperature)
    
    async def generate_interview_question(
        self,
        project_info: dict,
        snapshot: Optional[dict] = None
    ) -> Dict[str, Any]:
        """生成访谈问题"""
        prompt = f"""你是一位专业的法务访谈助手，正在帮助用户完成合同起草访谈。

项目类型: {project_info.get('primary_type', '未知')}
附属类型: {', '.join(project_info.get('secondary_types', [])) if project_info.get('secondary_types') else '无'}
当前步骤: {snapshot.get('step', 1)}

请根据已确认的事实，提出下一个需要澄清的问题。只返回JSON格式：
{{
    "text": "问题内容",
    "category": "fact_gathering|risk_identification|clarification",
    "required": true
}}"""
        
        try:
            result = await self.chat([{"role": "user", "content": prompt}])
            # 清理可能的markdown代码块
            result = result.strip()
            if result.startswith("```"):
                result = result.split("\n")[1].rstrip("```")
            return json.loads(result)
        except Exception as e:
            print(f"Generate interview question error: {e}")
            return {"text": "请描述交易的具体情况...", "category": "fact_gathering", "required": True}
    
    async def parse_interview_answer(
        self,
        project_info: dict,
        answer: str,
        last_snapshot: Optional[dict] = None
    ) -> Dict[str, Any]:
        """解析用户回答，提取结构化信息"""
        prompt = f"""请分析用户的回答，提取合同起草所需的关键信息。

交易类型: {project_info.get('primary_type', '未知')}
用户回答: {answer}

返回JSON格式：
{{
    "confirmed_elements": [{"element": "...", "value": "..."}],
    "pending_elements": [{"element": "...", "reason": "..."}],
    "risks": [{"level": "high|medium|low", "description": "..."}]
}}"""
        
        try:
            result = await self.chat([{"role": "user", "content": prompt}])
            result = result.strip()
            if result.startswith("```"):
                result = result.split("\n")[1].rstrip("```")
            return json.loads(result)
        except Exception as e:
            print(f"Parse interview answer error: {e}")
            return {"confirmed_elements": [], "pending_elements": [], "risks": []}
    
    async def generate_outline(
        self,
        project_info: dict,
        snapshot: Optional[dict] = None
    ) -> List[Dict[str, Any]]:
        """生成合同大纲"""
        prompt = f"""请为以下交易类型生成合同大纲章节结构。

主类型: {project_info.get('primary_type', '未知')}
附属类型: {', '.join(project_info.get('secondary_types', [])) if project_info.get('secondary_types') else '无'}

已确认要素: {json.dumps(snapshot.get('confirmed_elements', []), ensure_ascii=False) if snapshot else '无'}

返回JSON数组格式：
[{{"title": "章节标题", "content": "章节说明"}}]"""
        
        try:
            result = await self.chat([{"role": "user", "content": prompt}])
            result = result.strip()
            if result.startswith("```"):
                result = result.split("\n")[1].rstrip("```")
            return json.loads(result)
        except Exception as e:
            print(f"Generate outline error: {e}")
            return [{"title": "当事人", "content": ""}, {"title": "标的", "content": ""}]
    
    async def generate_contract_text(
        self,
        project_info: dict,
        outline: dict,
        snapshot: Optional[dict] = None,
        custom_contents: Optional[List[dict]] = None
    ) -> tuple:
        """生成完整合同文本"""
        prompt = f"""请根据以下信息生成完整的合同文本。

合同类型: {project_info.get('primary_type', '未知')}
大纲结构: {json.dumps(outline, ensure_ascii=False) if outline else '标准结构'}
已确认事实: {json.dumps(snapshot.get('confirmed_elements', []) if snapshot else [], ensure_ascii=False)}
自定义内容: {json.dumps(custom_contents, ensure_ascii=False) if custom_contents else '无'}

要求：
1. 使用规范的法律语言
2. 条款完整、逻辑清晰
3. 高风险条款标注⚠️
4. 文末包含风险提示章节

返回JSON格式：
{{
    "contract_text": "完整合同文本",
    "risk_notes": ["风险提示1", "风险提示2"]
}}"""
        
        try:
            result = await self.chat([{"role": "user", "content": prompt}], temperature=0.3)
            result = result.strip()
            if result.startswith("```"):
                result = result.split("\n")[1].rstrip("```")
            data = json.loads(result)
            return data.get("contract_text", ""), data.get("risk_notes", [])
        except Exception as e:
            print(f"Generate contract text error: {e}")
            return "# 合同文本\n\n[生成失败，请重试]", ["生成失败"]
    
    async def list_models(self) -> List[Dict[str, str]]:
        """获取可用模型列表"""
        if self.provider == "mock":
            return [{"id": "mock/default", "name": "Mock模型（测试用）"}]
        
        models = API_ENDPOINTS.get(self.provider, {}).get("models", [])
        return [{"id": m, "name": m} for m in models]


# 全局AI服务实例
ai_service = AIService()


def get_ai_service() -> AIService:
    """获取AI服务实例（支持动态配置）"""
    return ai_service
