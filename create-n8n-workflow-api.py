#!/usr/bin/env python3
"""
在 n8n 中创建 workflow 并返回测试接口
"""

import json
import requests
import time

N8N_URL = "http://localhost:5678"
N8N_API_URL = f"{N8N_URL}/api/v1"

# Workflow 配置
workflow_config = {
    "name": "MCP 集成演示 - 商品搜索与订单",
    "nodes": [
        {
            "parameters": {},
            "name": "Manual Trigger",
            "type": "n8n-nodes-base.manualTrigger",
            "typeVersion": 1,
            "position": [240, 300]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "http://localhost:19002/tools/search_products",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={\n  \"keyword\": \"iPhone\"\n}"
            },
            "name": "搜索商品",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [460, 300]
        },
        {
            "parameters": {
                "mode": "manual",
                "duplicateItem": False
            },
            "name": "提取商品信息",
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.2,
            "position": [680, 300]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "http://localhost:19002/tools/create_order",
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": "={\n  \"product_id\": {{ $json.product_id }},\n  \"quantity\": {{ $json.quantity }},\n  \"address\": \"{{ $json.address }}\"\n}"
            },
            "name": "创建订单",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [900, 300]
        },
        {
            "parameters": {
                "mode": "manual",
                "duplicateItem": False
            },
            "name": "格式化输出",
            "type": "n8n-nodes-base.set",
            "typeVersion": 3.2,
            "position": [1120, 300]
        }
    ],
    "connections": {
        "Manual Trigger": {
            "main": [[{"node": "搜索商品", "type": "main", "index": 0}]]
        },
        "搜索商品": {
            "main": [[{"node": "提取商品信息", "type": "main", "index": 0}]]
        },
        "提取商品信息": {
            "main": [[{"node": "创建订单", "type": "main", "index": 0}]]
        },
        "创建订单": {
            "main": [[{"node": "格式化输出", "type": "main", "index": 0}]]
        }
    }
}

def create_n8n_workflow():
    """在 n8n 中创建 workflow"""

    print("=" * 70)
    print("🚀 在 n8n 中创建 Workflow")
    print("=" * 70)
    print()

    # 尝试通过 n8n API 创建
    try:
        print("📝 尝试通过 n8n API 创建 workflow...")

        # n8n API endpoint (可能需要认证)
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(
            f"{N8N_API_URL}/workflows",
            json=workflow_config,
            headers=headers,
            timeout=10
        )

        if response.status_code == 201:
            result = response.json()
            print("✅ Workflow 创建成功!")
            print(f"   ID: {result.get('id')}")
            print(f"   访问: {N8N_URL}/workflow/{result.get('id')}")
            print()
            provide_test_instructions(result.get('id'))
            return result
        else:
            print(f"⚠️  API 返回: {response.status_code}")
            print(f"   响应: {response.text[:200]}")

    except Exception as e:
        print(f"❌ API 调用失败: {e}")

    # 提供手动创建方案
    print()
    print("=" * 70)
    print("📋 手动创建指南")
    print("=" * 70)
    print()

    print("📍 方法 1: 通过 n8n 界面手动创建")
    print("-" * 70)
    print("1. 打开浏览器: http://localhost:5678")
    print("2. 点击 'New Workflow'")
    print("3. 按照 demonstrate-workflow-creation.py 中的步骤操作")
    print()

    print("📍 方法 2: 导入 JSON 配置（推荐）")
    print("-" * 70)
    print("1. 在 n8n 界面中，点击右上角 '...'")
    print("2. 选择 'Import from File'")
    print("3. 选择文件: workflow-mcp-demo.json")
    print("4. 点击导入")
    print()

    print("=" * 70)
    print("🧪 测试接口（无需 n8n，直接调用 MCP）")
    print("=" * 70)
    print()

    provide_test_instructions(None)

    return None


def provide_test_instructions(workflow_id):
    """提供测试接口说明"""

    print("🎯 可以直接测试的 MCP 接口:")
    print()
    print("1️⃣  搜索商品接口:")
    print("   curl -X POST 'http://localhost:19002/tools/search_products' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"keyword\": \"iPhone\"}'")
    print()

    print("2️⃣  创建订单接口:")
    print("   curl -X POST 'http://localhost:19002/tools/create_order' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"product_id\": 1, \"quantity\": 2, \"address\": \"北京市\"}'")
    print()

    print("3️⃣  查看所有可用工具:")
    print("   curl 'http://localhost:19002/tools' | jq .")
    print()

    print("=" * 70)
    print("📊 工作流执行说明")
    print("=" * 70)
    print()

    if workflow_id:
        print(f"方式 1: 在 n8n 中执行")
        print(f"  1. 访问: {N8N_URL}/workflow/{workflow_id}")
        print(f"  2. 点击 'Test workflow'")
        print(f"  3. 点击 'Manual Trigger' 节点执行")
        print()
    else:
        print("方式 1: 在 n8n 中执行")
        print("  1. 创建 workflow 后，打开 workflow 编辑界面")
        print("  2. 点击 'Test workflow'")
        print("  3. 点击 'Manual Trigger' 节点执行")
        print()

    print("方式 2: 直接调用 MCP 接口（推荐）")
    print("  使用上面提供的 curl 命令直接测试")
    print()

    print("=" * 70)


if __name__ == "__main__":
    create_n8n_workflow()
