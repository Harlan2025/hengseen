"""
测试脚本 - 验证衡简叙约后端接口
"""
import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(__file__))

from test_db import db
from mock_ai import ai_service
from main import app
from fastapi.testclient import TestClient

# 创建测试客户端
client = TestClient(app)


def test_health():
    """测试健康检查"""
    print("\n=== 测试健康检查 ===")
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("✅ 健康检查通过")


def test_get_agreements():
    """测试获取协议内容"""
    print("\n=== 测试获取协议内容 ===")
    response = client.get("/api/v1/auth/agreements")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "user_agreement" in data["data"]
    assert "privacy_policy" in data["data"]
    print(f"✅ 获取协议成功，版本：{data['data']['user_agreement']['version']}")


def test_register_without_agreement():
    """测试未勾选协议注册失败"""
    print("\n=== 测试未勾选协议注册 ===")
    response = client.post("/api/v1/auth/register", json={
        "phone": "13800138001",
        "code": "123456",
        "nickname": "测试用户",
        "agree_user_agreement": False,
        "agree_privacy_policy": True,
        "agreement_version": "V1.0"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["code"] == 7001
    print(f"✅ 未勾选协议注册被拒绝：{data['detail']['msg']}")


def test_login_without_agreement():
    """测试未勾选协议登录失败"""
    print("\n=== 测试未勾选协议登录 ===")
    response = client.post("/api/v1/auth/login", json={
        "phone": "13800138001",
        "code": "123456",
        "agree_user_agreement": False,
        "agree_privacy_policy": True,
        "agreement_version": "V1.0"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["detail"]["code"] == 7001
    print(f"✅ 未勾选协议登录被拒绝：{data['detail']['msg']}")


def test_create_project():
    """测试创建项目"""
    print("\n=== 测试创建项目 ===")
    # 先获取JWT token（模拟登录）
    response = client.post("/api/v1/auth/login", json={
        "phone": "13800138001",
        "code": "123456",
        "agree_user_agreement": True,
        "agree_privacy_policy": True,
        "agreement_version": "V1.0"
    })
    
    if response.status_code == 200:
        token = response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 创建项目
        response = client.post("/api/v1/projects", 
                              json={"name": "测试买卖合同", "primary_type": "A", "secondary_types": []},
                              headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 0
        print(f"✅ 项目创建成功，ID：{data['data']['project_id']}")
        return data["data"]["project_id"]
    else:
        print("⚠️ 登录失败，跳过项目创建测试")
        return None


def test_interview_flow(project_id: str):
    """测试访谈流程"""
    print("\n=== 测试访谈流程 ===")
    if not project_id:
        print("⚠️ 跳过访谈测试（无项目ID）")
        return
    
    # 获取问题
    response = client.get(f"/api/v1/interview/{project_id}/question")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 获取访谈问题：{data['data']['question_text'][:30]}...")
    
    # 提交答案
    response = client.post(f"/api/v1/interview/{project_id}/answer",
                          json={"answer": "这是测试回答内容"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 提交答案成功，步骤：{data['data']['step']}")


def test_outline_generation(project_id: str):
    """测试大纲生成"""
    print("\n=== 测试大纲生成 ===")
    if not project_id:
        print("⚠️ 跳过大纲测试（无项目ID）")
        return
    
    response = client.post(f"/api/v1/outline/generate?project_id={project_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 大纲生成成功，章节数：{len(data['data']['chapters'])}")
    else:
        print(f"⚠️ 大纲生成失败：{response.status_code}")


def test_contract_generation(project_id: str):
    """测试合同生成"""
    print("\n=== 测试合同生成 ===")
    if not project_id:
        print("⚠️ 跳过合同生成测试（无项目ID）")
        return
    
    response = client.post("/api/v1/contract/generate",
                          json={"project_id": project_id})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 合同生成成功，长度：{len(data['data']['contract_text'])} 字符")
    else:
        print(f"⚠️ 合同生成失败：{response.status_code}")


def test_payment_flow(project_id: str):
    """测试支付流程"""
    print("\n=== 测试支付流程 ===")
    if not project_id:
        print("⚠️ 跳过支付测试（无项目ID）")
        return
    
    response = client.post("/api/v1/payment/create",
                          json={"project_id": project_id, "payment_method": "wechat"})
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 支付订单创建成功，金额：¥{data['data']['amount']}")
    else:
        print(f"⚠️ 支付订单创建失败：{response.status_code}")


def test_admin_agreement_management():
    """测试后台协议管理"""
    print("\n=== 测试后台协议管理 ===")
    
    # 获取协议列表
    response = client.get("/api/v1/admin/agreements")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 获取协议列表成功，共 {len(data['data']['list'])} 条")
    
    # 获取协议详情
    if data["data"]["list"]:
        agreement_id = data["data"]["list"][0]["agreement_id"]
        response = client.get(f"/api/v1/admin/agreements/{agreement_id}")
        if response.status_code == 200:
            print(f"✅ 获取协议详情成功：{response.json()['data']['title']}")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("衡简叙约后端功能测试")
    print("=" * 60)
    
    # 重置数据库
    db.reset_all()
    print("\n✅ 数据库已重置")
    
    tests = [
        ("健康检查", test_health),
        ("获取协议", test_get_agreements),
        ("未勾选协议注册", test_register_without_agreement),
        ("未勾选协议登录", test_login_without_agreement),
    ]
    
    for name, test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"❌ {name} 测试失败：{e}")
    
    # 动态测试（需要登录）
    project_id = None
    try:
        project_id = test_create_project()
        test_interview_flow(project_id)
        test_outline_generation(project_id)
        test_contract_generation(project_id)
        test_payment_flow(project_id)
        test_admin_agreement_management()
    except Exception as e:
        print(f"❌ 动态测试失败：{e}")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
