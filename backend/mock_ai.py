"""
模拟AI服务 - 用于测试模式
"""
import json
from typing import List, Dict, Any, Optional


class MockAIService:
    """模拟AI服务"""
    
    # 预定义的访谈问题模板
    INTERVIEW_QUESTIONS = {
        "A": [
            "请描述买卖双方的基本信息（姓名/公司名称、联系方式）",
            "请描述交易标的的具体信息（名称、规格、数量、质量标准）",
            "请说明价款及支付方式（总价、付款节点、支付方式）",
            "请说明交付方式和时间（交付地点、交付期限、运输方式）",
            "请说明验收标准和期限（验收时间、验收方法、异议期限）",
            "请说明违约责任（逾期交货、质量不合格、逾期付款的违约金）",
            "请说明争议解决方式（协商、仲裁、诉讼管辖）",
        ],
        "B": [
            "请描述各方当事人的基本信息",
            "请说明备忘录涉及的事项和背景",
            "请说明各方的意向和初步约定",
            "请说明后续正式合同的签订计划",
        ],
        "C": [
            "请描述股权转让方和受让方的基本信息",
            "请说明转让股权的比例和价格",
            "请说明付款方式和期限",
            "请说明交割条件和程序",
            "请说明陈述与保证条款",
        ],
        "D": [
            "请描述合作各方的基本信息",
            "请说明合作内容和范围",
            "请说明合作期限",
            "请说明投资金额和股权比例",
            "请说明利润分配和风险承担",
        ],
        "E": [
            "请描述用人单位和劳动者的基本信息",
            "请说明劳动合同期限",
            "请说明工作内容和工作地点",
            "请说明工作时间和休息休假",
            "请说明劳动报酬（工资数额、支付时间）",
            "请说明社会保险和福利待遇",
        ],
        "F": [
            "请描述许可方和被许可方的基本信息",
            "请说明知识产权的类型和范围",
            "请说明许可方式（独占、排他、普通）",
            "请说明许可期限和地域范围",
            "请说明许可费用和支付方式",
        ],
        "G": [
            "请描述债权人、债务人和担保人的基本信息",
            "请说明主债权的金额和性质",
            "请说明担保方式（保证、抵押、质押）",
            "请说明担保范围",
            "请说明担保期限",
        ],
        "H": [
            "请描述债权转让方和受让方的基本信息",
            "请说明债权的金额和性质",
            "请说明转让价格和支付方式",
            "请说明通知债务人的方式",
        ],
        "I": [
            "请描述委托方和居间方的基本信息",
            "请说明居间服务的内容",
            "请说明居间成功的标准",
            "请说明居间报酬的计算和支付",
        ],
        "J": [
            "请描述协议各方的基本信息",
            "请说明终止/解除的原因",
            "请说明财产分割方案",
            "请说明债务承担方案",
            "请说明违约责任",
        ],
    }
    
    # 默认风险提示
    DEFAULT_RISKS = [
        {"level": "medium", "description": "建议明确约定合同解除条件"},
        {"level": "low", "description": "建议增加不可抗力条款"},
        {"level": "medium", "description": "建议明确约定违约金计算方式"},
    ]
    
    async def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """模拟AI对话"""
        last_message = messages[-1]["content"] if messages else ""

        # 先检查是否是访谈问题生成请求（最精确的匹配）
        if "提出下一个需要澄清的关键问题" in last_message and "只返回JSON格式" in last_message:
            primary_type = "A"
            for line in last_message.split("\n"):
                if line.startswith("- 主类型："):
                    primary_type = line.replace("- 主类型：", "").strip()
                    break

            return json.dumps({
                "text": f"请描述{primary_type}交易的基本情况",
                "category": "fact_gathering",
                "required": True
            })

        # 检查是否是答案解析请求
        if "提取合同起草所需的关键信息" in last_message and "返回JSON格式" in last_message:
            return json.dumps({
                "confirmed_elements": [
                    {"element": "交易标的", "value": "待确认"}
                ],
                "pending_elements": [
                    {"element": "交货时间", "reason": "未明确"}
                ],
                "risks": [
                    {"level": "medium", "description": "交货时间不明确"}
                ]
            })
        
        if "大纲" in last_message or "outline" in last_message.lower():
            return json.dumps([
                {"title": "第一条 当事人", "content": ""},
                {"title": "第二条 标的", "content": ""},
                {"title": "第三条 价款", "content": ""},
                {"title": "第四条 履行", "content": ""},
                {"title": "第五条 违约责任", "content": ""},
                {"title": "第六条 争议解决", "content": ""},
            ])
        
        if "合同" in last_message or "contract" in last_message.lower():
            return json.dumps({
                "contract_text": """# 买卖合同

## 合同编号：HS-2026-001

**甲方（出卖人）：**[待填写]
**乙方（买受人）：**[待填写]

根据《中华人民共和国民法典》及相关法律法规，甲乙双方在平等、自愿的基础上，就买卖事宜达成如下协议：

### 第一条 标的
1.1 甲方同意出售，乙方同意购买以下货物：
- 货物名称：[待填写]
- 规格型号：[待填写]
- 数量：[待填写]
- 质量标准：[待填写]

### 第二条 价款
2.1 合同总价款为人民币（大写）[待填写]元整（¥[待填写]）。
2.2 付款方式：[待填写]

### 第三条 交付
3.1 交付时间：[待填写]
3.2 交付地点：[待填写]
3.3 运输方式：[待填写]

### 第四条 验收
4.1 验收期限：收货后[ ]日内
4.2 验收标准：按本合同第一条约定
4.3 异议处理：如有质量问题，乙方应在验收期限内书面通知甲方

### 第五条 违约责任
5.1 甲方逾期交货的，每日按合同总价款的[ ]%向乙方支付违约金
5.2 乙方逾期付款的，每日按应付未付金额的[ ]%向甲方支付违约金
⚠️ 5.3 建议明确约定违约金的具体比例和计算方式

### 第六条 争议解决
6.1 本合同履行过程中发生的争议，由双方协商解决
6.2 协商不成的，提交[甲方所在地/乙方所在地]人民法院诉讼解决

### 第七条 其他
7.1 本合同自双方签字盖章之日起生效
7.2 本合同一式两份，甲乙双方各执一份

**甲方（盖章）：**        **乙方（盖章）：**
**法定代表人：**          **法定代表人：**
**日期：**                **日期：**

---

## 风险提示
⚠️ 1. 建议明确约定交货时间和验收标准
⚠️ 2. 建议增加不可抗力条款
⚠️ 3. 建议明确违约金计算方式
⚠️ 4. 建议选择对自己有利的管辖法院

---

*本文档由衡简叙约AI生成，仅供参考，不构成法律意见。重大交易请咨询专业律师。*""",
                "risk_notes": [
                    "建议明确约定交货时间和验收标准",
                    "建议增加不可抗力条款",
                    "建议明确违约金计算方式",
                    "建议选择对自己有利的管辖法院"
                ]
            })
        
        # 默认响应
        return json.dumps({"text": "感谢您的回复，我已记录。"})
    
    async def generate_interview_question(
        self,
        project_info: dict,
        snapshot: Optional[dict] = None
    ) -> Dict[str, Any]:
        """生成访谈问题"""
        step = snapshot.get("step", 0) + 1 if snapshot else 1
        primary_type = project_info.get("primary_type", "A")
        
        questions = self.INTERVIEW_QUESTIONS.get(primary_type, self.INTERVIEW_QUESTIONS["A"])
        idx = (step - 1) % len(questions)
        
        return {
            "text": questions[idx],
            "category": "fact_gathering",
            "required": True
        }
    
    async def parse_interview_answer(
        self,
        project_info: dict,
        answer: str,
        step: int
    ) -> Dict[str, Any]:
        """解析用户回答"""
        return {
            "confirmed_elements": [
                {"element": f"第{step}项事实", "value": answer[:50] + "..." if len(answer) > 50 else answer}
            ],
            "pending_elements": [
                {"element": "待确认事项", "reason": "需要进一步澄清"}
            ],
            "risks": self.DEFAULT_RISKS[:step % 3]
        }
    
    async def generate_outline(
        self,
        project_info: dict,
        snapshot: Optional[dict] = None
    ) -> List[Dict[str, Any]]:
        """生成大纲"""
        return [
            {"chapter_id": str(i), "title": f"第{i}条", "content": "", "order": i}
            for i in range(1, 7)
        ]
    
    async def generate_contract_text(
        self,
        project_info: dict,
        outline: dict,
        snapshot: Optional[dict] = None,
        custom_contents: Optional[List[dict]] = None
    ) -> tuple:
        """生成合同文本"""
        contract = f"""# 合同文本

## 基本信息
- 类型：{project_info.get('primary_type', 'A')}
- 状态：已生成

## 合同正文
[此处为AI生成的合同文本]

---

*本文档由衡简叙约AI生成，仅供参考，不构成法律意见。*"""
        
        return contract, ["建议咨询专业律师审核"]


# 全局AI服务实例
ai_service = MockAIService()
