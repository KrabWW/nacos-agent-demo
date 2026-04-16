#!/usr/bin/env python3
"""
为 workflow 添加 Webhook 支持，使其可以通过 API 调用
"""
import json
import requests

N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiNTMwMjZmNS02ZTIyLTQyMzMtOTVkMi05NWRiMTFlOWU3MGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWE0NzIyNDktMjBhNC00Y2MwLTg1ZDUtMTVmYWRiZTI0OTJmIiwiaWF0IjoxNzc2MTQ5NzY2LCJleHAiOjE3Nzg3MzEyMDB9.Rdkn1U-HeZBqpWqsufGfL3B8YhhHrKa5humU-oCMA5c"
WORKFLOW_ID = "eOPjpVDChTp8Eft5"
HOST_IP = "172.28.156.225"

def add_webhook_to_workflow():
    """将 Manual Trigger 替换为 Webhook"""

    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }

    # 获取当前 workflow
    print("📥 获取当前 workflow...")
    response = requests.get(
        f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
        headers=headers
    )

    if response.status_code != 200:
        print(f"❌ 获取失败: {response.status_code}")
        return

    workflow = response.json()
    print(f"✅ 获取成功: {workflow['name']}\n")

    # 找到并替换 Manual Trigger 节点
    print("🔧 替换 Manual Trigger 为 Webhook...")

    for i, node in enumerate(workflow['nodes']):
        if node['type'] == 'n8n-nodes-base.manualTrigger':
            # 替换为 Webhook 节点
            workflow['nodes'][i] = {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "product-search-demo",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": node['position'],
                "webhookId": "auto-generated-webhook"
            }
            print(f"   ✓ 替换节点: {node['name']} → Webhook")
            break

    # 更新 workflow 名称
    workflow['name'] = "MCP 集成演示 - 商品搜索与订单 (Webhook)"

    # 更新 connections
    if 'Manual Trigger' in workflow['connections']:
        workflow['connections']['Webhook'] = workflow['connections']['Manual Trigger']
        del workflow['connections']['Manual Trigger']

    # 更新 workflow
    print("\n📤 更新 workflow...")

    update_data = {
        "name": workflow['name'],
        "nodes": workflow['nodes'],
        "connections": workflow['connections'],
        "settings": workflow.get('settings', {})
    }

    response = requests.put(
        f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
        json=update_data,
        headers=headers
    )

    if response.status_code in [200, 204]:
        print("✅ Workflow 更新成功!")
        print("\n🎯 Webhook 信息:")
        print(f"   URL: http://localhost:5678/webhook/product-search-demo")
        print(f"   方法: POST")
        print(f"   访问: http://localhost:5678/workflow/{WORKFLOW_ID}")
        print("\n🧪 测试命令:")
        print('curl -X POST \'http://localhost:5678/webhook/product-search-demo\' \\')
        print('  -H \'Content-Type: application/json\' \\')
        print('  -d \'{"keyword": "iPhone"}\'')
    else:
        print(f"❌ 更新失败: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    add_webhook_to_workflow()
