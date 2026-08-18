"""
模拟AI服务 - 用于测试模式
"""
import json
from typing import List, Dict, Any, Optional


class MockAIService:
    """模拟AI服务"""
    
    # 预定义的访谈问题模板（按类型和步骤）
    INTERVIEW_QUESTIONS = {
        "A": [
            {"text": "请描述买卖双方的基本信息（姓名/公司名称、联系方式）", "risk": "需确认双方主体资格"},
            {"text": "请描述交易标的的具体信息（名称、规格、数量、质量标准）", "risk": "标的信息不明确易引发纠纷"},
            {"text": "请说明价款及支付方式（总价、付款节点、支付方式）", "risk": "价款约定不明可能导致违约争议"},
            {"text": "请说明交付方式和时间（交付地点、交付期限、运输方式）", "risk": "交货时间不明确影响合同履行"},
            {"text": "请说明验收标准和期限（验收时间、验收方法、异议期限）", "risk": "验收标准缺失可能导致质量争议"},
            {"text": "请说明违约责任（逾期交货、质量不合格、逾期付款的违约金）", "risk": "违约责任不明影响维权"},
            {"text": "请说明争议解决方式（协商、仲裁、诉讼管辖）", "risk": "争议解决方式不明确增加维权成本"},
        ],
        "B": [
            {"text": "请描述各方当事人的基本信息", "risk": "需确认各方主体资格"},
            {"text": "请说明备忘录涉及的事项和背景", "risk": "事项不明确影响备忘录效力"},
            {"text": "请说明各方的意向和初步约定", "risk": "意向表述需清晰避免歧义"},
            {"text": "请说明后续正式合同的签订计划", "risk": "缺乏后续安排可能导致意向落空"},
        ],
        "C": [
            {"text": "请描述股权转让方和受让方的基本信息", "risk": "需确认股权权属清晰"},
            {"text": "请说明转让股权的比例和价格", "risk": "股权价格需合理评估"},
            {"text": "请说明付款方式和期限", "risk": "付款期限需明确约定"},
            {"text": "请说明交割条件和程序", "risk": "交割程序需符合法律规定"},
            {"text": "请说明陈述与保证条款", "risk": "陈述保证不实可能承担违约责任"},
        ],
        "D": [
            {"text": "请描述合作各方的基本信息", "risk": "需确认各方合作能力"},
            {"text": "请说明合作内容和范围", "risk": "合作范围不明易生争议"},
            {"text": "请说明合作期限", "risk": "合作期限需明确约定"},
            {"text": "请说明投资金额和股权比例", "risk": "投资比例需公平合理"},
            {"text": "请说明利润分配和风险承担", "risk": "分配机制需明确"},
        ],
        "E": [
            {"text": "请描述用人单位和劳动者的基本信息", "risk": "需确认主体资格"},
            {"text": "请说明劳动合同期限", "risk": "合同期限影响双方权益"},
            {"text": "请说明工作内容和工作地点", "risk": "工作内容需明确具体"},
            {"text": "请说明工作时间和休息休假", "risk": "工时制度需符合法规"},
            {"text": "请说明劳动报酬（工资数额、支付时间）", "risk": "薪酬约定需明确"},
            {"text": "请说明社会保险和福利待遇", "risk": "社保缴纳需依法进行"},
        ],
        "F": [
            {"text": "请描述许可方和被许可方的基本信息", "risk": "需确认知识产权权属"},
            {"text": "请说明知识产权的类型和范围", "risk": "授权范围需明确界定"},
            {"text": "请说明许可方式（独占、排他、普通）", "risk": "许可方式影响双方权益"},
            {"text": "请说明许可期限和地域范围", "risk": "期限地域需明确约定"},
            {"text": "请说明许可费用和支付方式", "risk": "费用支付需明确约定"},
        ],
        "G": [
            {"text": "请描述债权人、债务人和担保人的基本信息", "risk": "需确认担保主体资格"},
            {"text": "请说明主债权的金额和性质", "risk": "主债权信息需完整"},
            {"text": "请说明担保方式（保证、抵押、质押）", "risk": "担保方式影响担保效力"},
            {"text": "请说明担保范围", "risk": "担保范围需明确约定"},
            {"text": "请说明担保期限", "risk": "担保期限需符合法律规定"},
        ],
        "H": [
            {"text": "请描述债权转让方和受让方的基本信息", "risk": "需确认债权真实性"},
            {"text": "请说明债权的金额和性质", "risk": "债权信息需完整准确"},
            {"text": "请说明转让价格和支付方式", "risk": "转让价格需合理确定"},
            {"text": "请说明通知债务人的方式", "risk": "通知债务人影响转让效力"},
        ],
        "I": [
            {"text": "请描述委托方和居间方的基本信息", "risk": "需确认居间方资质"},
            {"text": "请说明居间服务的内容", "risk": "服务内容需明确具体"},
            {"text": "请说明居间成功的标准", "risk": "成功标准需客观可衡量"},
            {"text": "请说明居间报酬的计算和支付", "risk": "报酬约定需明确合法"},
        ],
        "J": [
            {"text": "请描述协议各方的基本信息", "risk": "需确认各方主体资格"},
            {"text": "请说明终止/解除的原因", "risk": "终止原因需符合法律规定"},
            {"text": "请说明财产分割方案", "risk": "财产分割需公平合理"},
            {"text": "请说明债务承担方案", "risk": "债务承担需明确约定"},
            {"text": "请说明违约责任", "risk": "违约责任需明确约定"},
        ],
    }
    
    # 交易架构风险分析模板
    ARCHITECTURE_RISKS = {
        "A": {
            "parties": "建议确认双方主体资格及履约能力",
            "subject": "建议明确标的物的具体范围和交付标准",
            "price": "建议约定价格调整机制和支付保障",
            "delivery": "建议明确交付节点和风险转移时点",
            "liability": "建议设置合理的违约金上限",
        },
        "C": {
            "equity": "建议进行股权尽职调查",
            "price": "建议引入第三方评估机构",
            "closing": "建议设置交割先决条件",
        },
    }
    
    async def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """模拟AI对话"""
        last_message = messages[-1]["content"] if messages else ""

        # 访谈问题生成（需要根据步骤返回不同问题）
        if "提出下一个需要澄清的关键问题" in last_message and "只返回JSON格式" in last_message:
            # 提取主类型
            primary_type = "A"
            step = 1
            for line in last_message.split("\n"):
                if line.startswith("- 主类型："):
                    primary_type = line.replace("- 主类型：", "").strip()
                elif line.startswith("【当前步骤】"):
                    # 提取步骤号
                    try:
                        step = int(line.split("第")[1].split("个")[0])
                    except:
                        pass
            
            # 根据步骤返回不同的问题
            questions = self.INTERVIEW_QUESTIONS.get(primary_type, self.INTERVIEW_QUESTIONS["A"])
            idx = (step - 1) % len(questions)
            question = questions[idx]
            
            return json.dumps({
                "text": question["text"],
                "category": "fact_gathering",
                "required": True
            })

        # 答案解析（需要根据回答内容返回动态结果）
        if "提取合同起草所需的关键信息" in last_message and "返回JSON格式" in last_message:
            # 从prompt中获取用户回答
            answer = ""
            for line in last_message.split("\n"):
                if line.startswith("【用户回答】"):
                    # 获取后续内容作为回答
                    answer_idx = last_message.find(line)
                    answer = last_message[answer_idx + len(line):].strip()
                    break
            
            # 根据回答内容动态生成已确认要素
            confirmed = []
            pending = []
            risks = []
            
            # 简单分析回答内容
            if answer:
                if "双方" in answer or "公司" in answer:
                    confirmed.append({"element": "交易主体", "value": "已确认"})
                if "金额" in answer or "价格" in answer or "元" in answer:
                    confirmed.append({"element": "交易价款", "value": "已确认"})
                if "交货" in answer or "交付" in answer:
                    confirmed.append({"element": "交付方式", "value": "已确认"})
                if "验收" in answer or "标准" in answer:
                    confirmed.append({"element": "验收标准", "value": "已确认"})
                if "违约" in answer or "责任" in answer:
                    confirmed.append({"element": "违约责任", "value": "已确认"})
            
            # 添加待确认事项
            if not confirmed:
                pending.append({"element": "交易标的", "reason": "尚未明确具体内容"})
                pending.append({"element": "交易价款", "reason": "尚未明确金额"})
            elif len(confirmed) < 3:
                pending.append({"element": "违约责任", "reason": "尚未明确违约情形和后果"})
                pending.append({"element": "争议解决", "reason": "尚未明确争议处理方式"})
            
            # 添加风险提醒
            if not confirmed:
                risks.append({"level": "high", "description": "关键交易要素尚未确认，建议优先明确标的和价款"})
            elif len(confirmed) < 3:
                risks.append({"level": "medium", "description": "部分关键要素尚未确认，存在履约风险"})
            
            return json.dumps({
                "confirmed_elements": confirmed,
                "pending_elements": pending,
                "risks": risks
            })
        
        # 大纲生成
        if "大纲" in last_message or "outline" in last_message.lower():
            return json.dumps([
                {"title": "第一条 当事人", "content": ""},
                {"title": "第二条 标的", "content": ""},
                {"title": "第三条 价款", "content": ""},
                {"title": "第四条 履行", "content": ""},
                {"title": "第五条 违约责任", "content": ""},
                {"title": "第六条 争议解决", "content": ""},
            ])
        
        # 合同生成
        if "合同" in last_message or "contract" in last_message.lower():
            return json.dumps({
                "contract_text": "# 买卖合同\n\n## 合同编号：HS-2026-001\n\n**甲方（出卖人）：**[待填写]\n**乙方（买受人）：**[待填写]\n\n根据《中华人民共和国民法典》及相关法律法规，甲乙双方在平等、自愿的基础上，就买卖事宜达成如下协议：\n\n### 第一条 标的\n1.1 甲方同意出售，乙方同意购买以下货物：\n- 货物名称：[待填写]\n- 规格型号：[待填写]\n- 数量：[待填写]\n- 质量标准：[待填写]\n\n### 第二条 价款\n2.1 合同总价款为人民币（大写）[待填写]元整（¥[待填写]）。\n2.2 付款方式：[待填写]\n\n### 第三条 交付\n3.1 交付时间：[待填写]\n3.2 交付地点：[待填写]\n3.3 运输方式：[待填写]\n\n### 第四条 验收\n4.1 验收期限：收货后[ ]日内\n4.2 验收标准：按本合同第一条约定\n4.3 异议处理：如有质量问题，乙方应在验收期限内书面通知甲方\n\n### 第五条 违约责任\n5.1 甲方逾期交货的，每日按合同总价款的[ ]%向乙方支付违约金\n5.2 乙方逾期付款的，每日按应付未付金额的[ ]%向甲方支付违约金\n⚠️ 5.3 建议明确约定违约金的具体比例和计算方式\n\n### 第六条 争议解决\n6.1 本合同履行过程中发生的争议，由双方协商解决\n6.2 协商不成的，提交[甲方所在地/乙方所在地]人民法院诉讼解决\n\n### 第七条 其他\n7.1 本合同自双方签字盖章之日起生效\n7.2 本合同一式两份，甲乙双方各执一份\n\n**甲方（盖章）：**        **乙方（盖章）：**\n**法定代表人：**          **法定代表人：**\n**日期：**                **日期：**\n\n---\n\n## 风险提示\n⚠️ 1. 建议明确约定交货时间和验收标准\n⚠️ 2. 建议增加不可抗力条款\n⚠️ 3. 建议明确违约金计算方式\n⚠️ 4. 建议选择对自己有利的管辖法院\n\n---\n\n*本文档由衡简叙约AI生成，仅供参考，不构成法律意见。重大交易请咨询专业律师。*",
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
            "text": questions[idx]["text"],
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
        confirmed = []
        pending = []
        risks = []
        
        # 简单分析回答内容
        if answer:
            if "双方" in answer or "公司" in answer:
                confirmed.append({"element": "交易主体", "value": "已确认"})
            if "金额" in answer or "价格" in answer or "元" in answer:
                confirmed.append({"element": "交易价款", "value": "已确认"})
            if "交货" in answer or "交付" in answer:
                confirmed.append({"element": "交付方式", "value": "已确认"})
            if "验收" in answer or "标准" in answer:
                confirmed.append({"element": "验收标准", "value": "已确认"})
            if "违约" in answer or "责任" in answer:
                confirmed.append({"element": "违约责任", "value": "已确认"})
        
        # 添加待确认事项
        if not confirmed:
            pending.append({"element": "交易标的", "reason": "尚未明确具体内容"})
            pending.append({"element": "交易价款", "reason": "尚未明确金额"})
        elif len(confirmed) < 3:
            pending.append({"element": "违约责任", "reason": "尚未明确违约情形和后果"})
            pending.append({"element": "争议解决", "reason": "尚未明确争议处理方式"})
        
        # 添加风险提醒
        if not confirmed:
            risks.append({"level": "high", "description": "关键交易要素尚未确认，建议优先明确标的和价款"})
        elif len(confirmed) < 3:
            risks.append({"level": "medium", "description": "部分关键要素尚未确认，存在履约风险"})
        
        return {
            "confirmed_elements": confirmed,
            "pending_elements": pending,
            "risks": risks
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
