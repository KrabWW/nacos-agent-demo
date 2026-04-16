#!/usr/bin/env python3
"""
在 n8n 中创建 workflow 的演示脚本
"""

import json
import requests
import sys

N8N_URL = "http://localhost:5678"

def demonstrate_workflow_creation():
    """演示在 n8n 中创建 workflow 的步骤"""

    print("=" * 70)
    print("🚀 n8n Workflow 创建演示")
    print("=" * 70)
    print()

    print("📍 Step 1: 创建新 Workflow")
    print("-" * 70)
    print("1. 打开浏览器访问: http://localhost:5678")
    print("2. 点击右上角 'New Workflow' 按钮")
    print("3. 在弹出窗口中输入名称: 'MCP 集成演示 - 商品搜索与订单'")
    print("4. 点击 '创建' 或 'Create'")
    print()

    print("📍 Step 2: 添加节点")
    print("-" * 70)
    print()

    nodes = [
        {
            "step": 2,
            "name": "节点 1: Manual Trigger",
            "details": [
                "在节点搜索框中输入 'Manual Trigger'",
                "点击添加 'Manual Trigger' 节点",
                "作用: 启动工作流"
            ]
        },
        {
            "step": 2,
            "name": "节点 2: 搜索商品 (MCP)",
            "details": [
                "在节点搜索框中输入 'HTTP Request'",
                "点击添加 'HTTP Request' 节点",
                "配置参数:",
                "  Method: POST",
                "  URL: http://localhost:19002/tools/search_products",
                "  Authentication: None",
                "  Body Type: JSON",
                "  Body: {\"keyword\": \"iPhone\"}"
            ]
        },
        {
            "step": 2,
            "name": "节点 3: 提取商品信息",
            "details": [
                "在节点搜索框中输入 'Set'",
                "点击添加 'Set' 节点",
                "配置字段:",
                "  Name: product_id, Value: {{ $json.result.items[0].id }}",
                "  Name: product_name, Value: {{ $json.result.items[0].name }}",
                "  Name: price, Value: {{ $json.result.items[0].price }}",
                "  Name: quantity, Value: 2",
                "  Name: address, Value: 北京市朝阳区"
            ]
        },
        {
            "step": 2,
            "name": "节点 4: 创建订单 (MCP)",
            "details": [
                "再添加一个 'HTTP Request' 节点",
                "配置参数:",
                "  Method: POST",
                "  URL: http://localhost:19002/tools/create_order",
                "  Authentication: None",
                "  Body Type: JSON",
                "  Body: {",
                "    \"product_id\": {{ $json.product_id }},",
                "    \"quantity\": {{ $json.quantity }},",
                "    \"address\": \"{{ $json.address }}\"",
                "  }"
            ]
        },
        {
            "step": 2,
            "name": "节点 5: 格式化输出",
            "details": [
                "再添加一个 'Set' 节点",
                "配置字段:",
                "  Name: message, Value: 订单创建成功！",
                "  Name: order_id, Value: {{ $json.result.order_id }}",
                "  Name: product, Value: {{ $json.result.product_name }}",
                "  Name: total, Value: {{ $json.result.total_price }}"
            ]
        }
    ]

    for i, node in enumerate(nodes, 1):
        print(f"  {i}. {node['name']}")
        for detail in node['details']:
            print(f"     {detail}")
        print()

    print("📍 Step 3: 连接节点")
    print("-" * 70)
    print("按照以下顺序连接节点:")
    print("  1. 点击 'Manual Trigger' 节点的右侧连接点（小圆点）")
    print("  2. 拖动到 '搜索商品 (MCP)' 节点")
    print("  3. 依次连接: 搜索 → 提取 → 创建订单 → 格式化输出")
    print()

    print("📍 Step 4: 测试 Workflow")
    print("-" * 70)
    print("1. 点击界面右上角的 'Test workflow' 按钮")
    print("2. 点击 'Manual Trigger' 节点中的 'Execute Workflow'")
    print("3. 观察每个节点的执行结果")
    print()

    print("📍 Step 5: 预期结果")
    print("-" * 70)
    print("节点 2 - 搜索商品 (MCP):")
    print("  应该找到 2 个 iPhone 商品")
    print()
    print("节点 3 - 提取商品信息:")
    print("  应该提取出第一个商品的 ID 和名称")
    print()
    print("节点 4 - 创建订单 (MCP):")
    print("  应该成功创建订单，返回订单号")
    print()
    print("节点 5 - 格式化输出:")
    print("  应该显示: 订单创建成功！订单号: X, 总价: ¥XXXX")
    print()

    print("=" * 70)
    print("💡 快捷方式")
    print("=" * 70)
    print()
    print("方法 1: 导入 JSON 配置")
    print("  1. 在 n8n 界面中，点击右上角 '...' 菜单")
    print("  2. 选择 'Import from File'")
    print("  3. 选择文件: workflow-mcp-demo.json")
    print("  4. 点击导入")
    print()
    print("方法 2: 复制粘贴节点配置")
    print("  1. 创建 workflow-mcp-demo.json 文件")
    print("  2. 打开文件，复制内容")
    print("  3. 在 n8n 中创建新 workflow")
    print("  4. 粘贴 JSON 内容到编辑器")
    print()
    print("=" * 70)
    print("🎯 准备开始!")
    print("=" * 70)
    print()
    print("所有服务已就绪:")
    print("  ✅ MCP Bridge: http://localhost:19002")
    print("  ✅ n8n: http://localhost:5678")
    print()
    print("现在可以打开浏览器开始创建了！")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_workflow_creation()
