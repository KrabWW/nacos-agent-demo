#!/usr/bin/env python3
"""
在 n8n 中真正创建 workflow 的脚本
"""

import json
import requests

N8N_URL = "http://localhost:5678"

def create_workflow_in_n8n():
    """在 n8n 中创建 workflow"""

    # 读取 workflow 配置
    with open("n8n-workflow-mcp-client.json", "r") as f:
        workflow_config = json.load(f)

    # 尝试通过 API 创建
    # 注意：n8n 的 API 可能需要认证
    try:
        print("📝 尝试通过 API 创建 workflow...")

        # n8n API endpoint
        api_url = f"{N8N_URL}/rest/workflows"

        # 如果 n8n 需要认证，这里需要添加 session cookie 或 API key
        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(api_url, json=workflow_config, headers=headers)

        if response.status_code == 201:
            result = response.json()
            print("✅ Workflow 创建成功!")
            print(f"   ID: {result.get('id')}")
            print(f"   名称: {result.get('name')}")
            print(f"   访问: {N8N_URL}/workflow/{result.get('id')}")
            return result
        else:
            print(f"❌ API 创建失败: {response.status_code}")
            print(f"   可能需要登录 n8n 或配置 API 认证")

    except Exception as e:
        print(f"❌ API 调用失败: {e}")

    # 提供手动创建的详细步骤
    print("\n" + "="*70)
    print("📋 手动在 n8n 中创建 workflow 的步骤:")
    print("="*70)
    print()
    print("1️⃣  打开 n8n")
    print("   URL: http://localhost:5678")
    print()
    print("2️⃣  创建新 workflow")
    print("   点击右上角 'New Workflow'")
    print()
    print("3️⃣  添加节点（按顺序）:")
    print()
    print("   节点 1: Manual Trigger")
    print("   ├─ 类型: n8n-nodes-base.manualTrigger")
    print("   └─ 位置: (240, 300)")
    print()
    print("   节点 2: MCP Client Tool - 搜索商品")
    print("   ├─ 类型: MCP Client Tool")
    print("   ├─ SSE Endpoint: http://localhost:19004/sse")
    print("   ├─ Authentication: None")
    print("   ├─ Tools to Include: All")
    print("   └─ 选择工具: search_products_api_products_get")
    print()
    print("   节点 3: Set - 提取数据")
    print("   ├─ 类型: n8n-nodes-base.set")
    print("   └─ 配置: product_id = {{ $json.result.items[0].id }}")
    print()
    print("   节点 4: MCP Client Tool - 创建订单")
    print("   ├─ 类型: MCP Client Tool")
    print("   ├─ SSE Endpoint: http://localhost:19004/sse")
    print("   ├─ Authentication: None")
    print("   └─ 选择工具: create_order_api_order_create_post")
    print()
    print("   节点 5: Set - 格式化输出")
    print("   └─ 类型: n8n-nodes-base.set")
    print()
    print("4️⃣  连接所有节点")
    print("   从上到下: Trigger → 搜索 → 提取 → 创建订单 → 输出")
    print()
    print("5️⃣  测试 workflow")
    print("   点击 'Test workflow' → 手动触发 'Execute Workflow'")
    print()
    print("="*70)
    print()
    print("💡 提示: 可以导入配置文件")
    print("   文件: n8n-workflow-mcp-client.json")
    print("   操作: Workflow 菜单 → Import from File")
    print()
    print("="*70)

    return None


if __name__ == "__main__":
    print("🚀 在 n8n 中创建 MCP Workflow")
    print("="*70)
    print()

    result = create_workflow_in_n8n()

    if result:
        print("\n✅ Workflow 创建成功！可以在 n8n 中查看和测试")
    else:
        print("\n📝 请按照上述步骤在 n8n 界面中手动创建 workflow")
