#!/usr/bin/env python3
"""
使用 n8n-mcp 创建 workflow 的示例脚本
"""

import json
import subprocess
import sys

def create_workflow_with_n8n_mcp():
    """使用 n8n-mcp 工具创建 workflow"""

    print("=" * 70)
    print("🚀 使用 n8n-mcp 在本地 n8n 中创建 Workflow")
    print("=" * 70)
    print()

    # 检查 n8n-mcp 是否启动
    try:
        response = subprocess.run(
            ["curl", "-s", "http://localhost:3000/health"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if response.returncode == 0:
            print("✅ n8n-mcp MCP 服务器已启动")
            print(f"   健康检查: {response.stdout.strip()}")
        else:
            print("⚠️  n8n-mcp 正在启动中...")
            print("   请稍等片刻后再试")
            return
    except Exception as e:
        print(f"❌ n8n-mcp 未启动: {e}")
        return

    print()
    print("=" * 70)
    print("📋 在 Claude Desktop 中配置 n8n-mcp")
    print("=" * 70)
    print()

    config_guide = """
1. 打开 Claude Desktop
2. 点击左下角 ⚙️ 设置 → Configurations
3. 找到 "MCP Servers" 或 "Model Context Protocol"
4. 添加新服务器：
   - Name: n8n-mcp
   - Command: npx
   - Arguments: -y @czlonkowski/n8n-mcp@latest
   - Environment:
     - N8N_API_URL: http://localhost:5678
     - N8N_API_KEY: (留空，如果需要的话)
5. 保存并重启 Claude Desktop
"""

    print(config_guide)
    print()

    print("=" * 70)
    print("🎯 在 Claude 中使用 n8n-mcp 创建 workflow")
    print("=" * 70)
    print()

    claude_prompt = """
在 Claude 中输入以下提示词：

---

我需要在本地 n8n (http://localhost:5678) 中创建一个 workflow：

需求：商品搜索与订单创建

步骤：
1. 使用 search_templates 搜索相关模板
2. 或直接创建包含以下节点的 workflow：
   - Manual Trigger 节点
   - HTTP Request 节点（调用 http://localhost:19002/tools/search_products）
   - Set 节点（提取 product_id）
   - HTTP Request 节点（调用 http://localhost:19002/tools/create_order）
   - Set 节点（格式化输出）

配置参考：
- HTTP Request 1: POST http://localhost:19002/tools/search_products
  Body: {"keyword": "iPhone"}

- HTTP Request 2: POST http://localhost:19002/tools/create_order
  Body: {"product_id": {{ $json.product_id }}, "quantity": 2, "address": "北京市"}

请使用 n8n-mcp 工具：
1. search_nodes({query: "http request"})
2. get_node({nodeType: "n8n-nodes-base.httpRequest"})
3. validate_node({...})
4. n8n_create_workflow({...})

---

"""

    print(claude_prompt)
    print()

    print("=" * 70)
    print("📚 n8n-mcp 可用的工具")
    print("=" * 70)
    print()

    tools_list = """
核心工具：
- search_nodes({query: "http"}) - 搜索 HTTP Request 节点
- get_node({nodeType: "n8n-nodes-base.httpRequest"}) - 获取节点详情
- validate_node({nodeType, config}) - 验证节点配置
- search_templates({query: "api integration"}) - 搜索模板

n8n 管理工具（需要 API key）：
- n8n_create_workflow({workflow}) - 创建 workflow
- n8n_update_partial_workflow({id, operations}) - 更新 workflow
- n8n_test_workflow({id}) - 测试 workflow
- n8n_list_workflows() - 列出所有 workflows
"""

    print(tools_list)
    print()

    print("=" * 70)
    print("💡 提示")
    print("=" * 70)
    print()
    print("1. 确保 n8n-mcp 已启动（端口 3000）")
    print("2. 在 Claude Desktop 中配置 n8n-mcp 连接")
    print("3. 在 Claude 中使用上述提示词创建 workflow")
    print("4. n8n-mcp 会自动调用 n8n API 创建 workflow")
    print()
    print("=" * 70)


if __name__ == "__main__":
    create_workflow_with_n8n_mcp()
