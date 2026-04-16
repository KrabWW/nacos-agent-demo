"""
直接在 n8n 中创建 workflow 的脚本
通过 n8n API 创建 workflow
"""

import json
import requests
import time

N8N_URL = "http://localhost:5678"
N8N_API_KEY = ""  # 如果需要 API key

def create_n8n_workflow(workflow_data: dict):
    """通过 API 创建 n8n workflow"""

    # n8n workflow 创建端点
    url = f"{N8N_URL}/rest/workflows"

    headers = {
        "Content-Type": "application/json"
    }

    # 如果有 API key，添加到 headers
    if N8N_API_KEY:
        headers["Authorization"] = f"Bearer {N8N_API_KEY}"

    try:
        print(f"📝 正在创建 n8n workflow...")
        response = requests.post(url, json=workflow_data, headers=headers)

        if response.status_code == 201:
            result = response.json()
            print(f"✅ Workflow 创建成功!")
            print(f"   ID: {result.get('id')}")
            print(f"   名称: {result.get('name')}")
            return result
        else:
            print(f"❌ 创建失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return None

    except Exception as e:
        print(f"❌ 创建 workflow 时出错: {e}")
        print(f"💡 提示: 请手动在 n8n 界面中创建 workflow")
        return None


def main():
    """创建 MCP 集成演示 workflow"""

    workflow = {
        "name": "MCP 集成演示 - 商品搜索与订单创建",
        "nodes": [
            {
                "parameters": {},
                "id": "manual-trigger",
                "name": "手动触发",
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [240, 300]
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "http://localhost:19003/tools/search_products_api_products_get",
                    "authentication": "none",
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": "={\n  \"keyword\": \"iPhone\"\n}",
                    "options": {}
                },
                "id": "search-products",
                "name": "搜索商品 (MCP)",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [460, 300]
            },
            {
                "parameters": {
                    "mode": "manual",
                    "duplicateItem": False,
                    "options": {}
                },
                "id": "extract-product",
                "name": "提取商品信息",
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.2,
                "position": [680, 300],
                "notesInFlow": True,
                "notes": "从搜索结果中提取第一个商品的 ID"
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "http://localhost:19003/tools/create_order_api_order_create_post",
                    "authentication": "none",
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": "={\n  \"product_id\": {{ $json.result.items[0].id }},\n  \"quantity\": 2,\n  \"address\": \"北京市朝阳区\"\n}",
                    "options": {}
                },
                "id": "create-order",
                "name": "创建订单 (MCP)",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [900, 300],
                "notesInFlow": True,
                "notes": "使用 MCP 工具创建订单"
            },
            {
                "parameters": {
                    "mode": "manual",
                    "duplicateItem": False,
                    "options": {}
                },
                "id": "format-output",
                "name": "格式化输出",
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.2,
                "position": [1120, 300],
                "notesInFlow": True,
                "notes": "格式化最终输出结果"
            }
        ],
        "connections": {
            "手动触发": {
                "main": [
                    [
                        {
                            "node": "搜索商品 (MCP)",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "搜索商品 (MCP)": {
                "main": [
                    [
                        {
                            "node": "提取商品信息",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "提取商品信息": {
                "main": [
                    [
                        {
                            "node": "创建订单 (MCP)",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "创建订单 (MCP)": {
                "main": [
                    [
                        {
                            "node": "格式化输出",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "pinData": {},
        "settings": {
            "executionOrder": "v1"
        },
        "staticData": None,
        "tags": [],
        "triggerCount": 1,
        "updatedAt": "2025-04-14T14:45:00.000Z",
        "versionId": "1"
    }

    # 尝试通过 API 创建
    result = create_n8n_workflow(workflow)

    if not result:
        # 如果 API 创建失败，提供手动创建指南
        print("\n" + "="*60)
        print("📋 手动在 n8n 中创建 workflow 的步骤:")
        print("="*60)
        print("1. 打开 n8n: http://localhost:5678")
        print("2. 点击 'New Workflow'")
        print("3. 添加以下节点:")
        print("   - Manual Trigger (手动触发)")
        print("   - HTTP Request → 搜索商品 (MCP)")
        print("     * URL: http://localhost:19003/tools/search_products_api_products_get")
        print("     * Method: POST")
        print("     * Body: {\"keyword\": \"iPhone\"}")
        print("   - Set → 提取商品信息")
        print("     * product_id: {{ $json.result.items[0].id }}")
        print("   - HTTP Request → 创建订单 (MCP)")
        print("     * URL: http://localhost:19003/tools/create_order_api_order_create_post")
        print("     * Method: POST")
        print("     * Body: {\"product_id\": {{ $json.product_id }}, \"quantity\": 2}")
        print("   - Set → 格式化输出")
        print("4. 连接所有节点")
        print("5. 点击 'Test workflow' 测试")
        print("="*60)

        # 保存 workflow 配置到文件
        with open("n8n-workflow-mcp-demo.json", "w") as f:
            json.dump(workflow, f, indent=2)
        print("\n💾 Workflow 配置已保存到: n8n-workflow-mcp-demo.json")
        print("   可以在 n8n 中导入此文件")

    return result


if __name__ == "__main__":
    print("🚀 n8n Workflow 创建脚本")
    print("="*60)

    result = main()

    if result:
        print("\n✅ Workflow 创建成功！")
        print(f"🔗 访问: {N8N_URL}/workflow/{result['id']}")
    else:
        print(f"\n💡 请手动访问 n8n 创建 workflow: {N8N_URL}")

    print("="*60)
