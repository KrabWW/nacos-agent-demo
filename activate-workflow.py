#!/usr/bin/env python3
"""
通过 API 激活 n8n workflow
"""
import requests
import json

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiNTMwMjZmNS02ZTIyLTQyMzMtOTVkMi05NWRiMTFlOWU3MGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWE0NzIyNDktMjBhNC00Y2MwLTg1ZDUtMTVmYWRiZTI0OTJmIiwiaWF0IjoxNzc2MTQ5NzY2LCJleHAiOjE3Nzg3MzEyMDB9.Rdkn1U-HeZBqpWqsufGfL3B8YhhHrKa5humU-oCMA5c"
WORKFLOW_ID = "eOPjpVDChTp8Eft5"

def activate_workflow():
    """激活 workflow"""

    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }

    print("🔄 激活 workflow...")
    print(f"   Workflow ID: {WORKFLOW_ID}")
    print()

    # 获取当前 workflow
    response = requests.get(
        f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
        headers=headers
    )

    if response.status_code != 200:
        print(f"❌ 获取 workflow 失败: {response.status_code}")
        return False

    workflow = response.json()

    # 更新 workflow 数据，将 active 设为 true
    workflow_data = {
        "name": workflow['name'],
        "nodes": workflow['nodes'],
        "connections": workflow['connections'],
        "settings": workflow.get('settings', {}),
        "active": True,
        "staticData": workflow.get('staticData', None)
    }

    # 尝试不同的激活方法
    methods = [
        ("PATCH", f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}"),
        ("PUT", f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}"),
    ]

    for method, url in methods:
        print(f"📡 尝试 {method} 方法...")

        try:
            if method == "PATCH":
                response = requests.patch(url, json={"active": True}, headers=headers)
            else:
                response = requests.put(url, json=workflow_data, headers=headers)

            if response.status_code in [200, 204]:
                print(f"✅ {method} 方法成功!")

                # 验证激活状态
                verify_response = requests.get(
                    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
                    headers=headers
                )

                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    is_active = verify_data.get('active', False)

                    if is_active:
                        print("✅ Workflow 已激活!")
                        print()
                        print("🎯 Webhook 信息:")
                        print(f"   URL: http://localhost:5678/webhook/product-search-demo")
                        print(f"   方法: POST")
                        print()
                        print("🧪 测试命令:")
                        print('curl -X POST \'http://localhost:5678/webhook/product-search-demo\' \\')
                        print('  -H \'Content-Type: application/json\' \\')
                        print('  -d \'{"keyword": "iPhone"}\'')
                        return True
                    else:
                        print("⚠️  激活请求已发送，但状态未更新")
                        print("   可能需要在 n8n UI 中手动激活")
            else:
                print(f"   ❌ {method} 失败: {response.status_code}")
                if response.text:
                    print(f"   响应: {response.text[:200]}")

        except Exception as e:
            print(f"   ❌ {method} 异常: {e}")

        print()

    print("=" * 70)
    print("📍 备用方案：在 n8n UI 中手动激活")
    print("=" * 70)
    print()
    print("1. 访问: http://localhost:5678/workflow/eOPjpVDChTp8Eft5")
    print("2. 查看右上角的开关（当前显示为 'Inactive'）")
    print("3. 点击开关，变为 'Active'")
    print("4. 等待激活完成（约 2-3 秒）")
    print()
    print("激活后就可以使用 webhook 了！")
    print()

    return False

if __name__ == "__main__":
    activate_workflow()
