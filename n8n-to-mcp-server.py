#!/usr/bin/env python3
"""
n8n Workflows → MCP Tools 自动转换器
一键将 n8n workflows 暴露为 MCP 工具
"""

import json
import requests
from typing import Dict, Any, List
from fastapi import FastAPI
import uvicorn

N8N_API_URL = "http://localhost:5678/api/v1"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiNTMwMjZmNS02ZTIyLTQyMzMtOTVkMi05NWRiMTFlOWU3MGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWE0NzIyNDktMjBhNC00Y2MwLTg1ZDUtMTVmYWRiZTI0OTJmIiwiaWF0IjoxNzc2MTQ5NzY2LCJleHAiOjE3Nzg3MzEyMDB9.Rdkn1U-HeZBqpWqsufGfL3B8YhhHrKa5humU-oCMA5c"

app = FastAPI(title="n8n MCP Server")

# 缓存 workflows 数据
workflows_cache = {}
tools_cache = []

def fetch_n8n_workflows() -> List[Dict[str, Any]]:
    """获取所有 n8n workflows"""
    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(
        f"{N8N_API_URL}/workflows",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        return data.get('data', [])
    else:
        print(f"❌ 获取 workflows 失败: {response.status_code}")
        return []

def workflow_to_mcp_tool(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """将 n8n workflow 转换为 MCP 工具定义"""

    workflow_id = workflow.get('id')
    workflow_name = workflow.get('name', 'unnamed')
    workflow_name_slug = workflow_name.lower().replace(' ', '_').replace('-', '_')

    # 尝试从 workflow 中提取输入参数
    input_schema = {
        "type": "object",
        "properties": {
            "input_data": {
                "type": "object",
                "description": "输入数据传递给 workflow"
            }
        }
    }

    # 检查是否有 webhook 节点
    nodes = workflow.get('nodes', [])
    has_webhook = any(node.get('type', '').startswith('n8n-nodes-base.webhook') for node in nodes)

    # 检查是否有 manual trigger
    has_manual_trigger = any(node.get('type') == 'n8n-nodes-base.manualTrigger' for node in nodes)

    description = f"执行 n8n workflow: {workflow_name}"
    if has_webhook:
        description += " (支持 Webhook 触发)"
    if has_manual_trigger:
        description += " (支持手动触发)"

    return {
        "name": f"n8n_workflow_{workflow_name_slug}",
        "description": description,
        "inputSchema": input_schema,
        "metadata": {
            "workflow_id": workflow_id,
            "workflow_name": workflow_name,
            "has_webhook": has_webhook,
            "has_manual_trigger": has_manual_trigger
        }
    }

def execute_workflow(workflow_id: str, input_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """执行 n8n workflow"""

    headers = {
        "X-N8N-API-KEY": N8N_API_KEY,
        "Content-Type": "application/json"
    }

    # 方式 1: 通过 API 执行（需要 workflow 有 production execution）
    execute_url = f"{N8N_API_URL}/workflows/{workflow_id}/execute"

    try:
        response = requests.post(
            execute_url,
            json={"data": input_data or {}},
            headers=headers
        )

        if response.status_code in [200, 201]:
            return {
                "success": True,
                "workflow_id": workflow_id,
                "result": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"执行失败: {response.status_code}",
                "message": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def refresh_workflows():
    """刷新 workflows 缓存"""
    global workflows_cache, tools_cache

    workflows = fetch_n8n_workflows()
    workflows_cache = {wf['id']: wf for wf in workflows}

    tools_cache = [workflow_to_mcp_tool(wf) for wf in workflows]

    print(f"✅ 已加载 {len(workflows)} 个 n8n workflows")
    for tool in tools_cache:
        print(f"   - {tool['name']}: {tool['metadata']['workflow_name']}")

@app.get("/")
async def root():
    """健康检查"""
    return {
        "service": "n8n MCP Server",
        "status": "running",
        "workflows_count": len(workflows_cache)
    }

@app.get("/tools")
async def list_tools():
    """列出所有可用的 MCP 工具（n8n workflows）"""
    return {
        "tools": tools_cache
    }

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, arguments: Dict[str, Any] = None):
    """调用 n8n workflow 工具"""

    # 查找对应的 workflow
    tool = next((t for t in tools_cache if t['name'] == tool_name), None)

    if not tool:
        return {
            "success": False,
            "error": f"工具未找到: {tool_name}"
        }

    workflow_id = tool['metadata']['workflow_id']

    # 执行 workflow
    result = execute_workflow(workflow_id, arguments)

    return {
        "success": result.get('success', False),
        "tool": tool_name,
        "workflow_id": workflow_id,
        "workflow_name": tool['metadata']['workflow_name'],
        "result": result.get('result'),
        "error": result.get('error')
    }

@app.post("/refresh")
async def refresh():
    """刷新 workflows 列表"""
    refresh_workflows()
    return {
        "success": True,
        "message": f"已刷新 {len(tools_cache)} 个 workflows"
    }

def start_server(port: int = 19005):
    """启动 n8n MCP Server"""

    print("=" * 70)
    print("🚀 n8n Workflows → MCP Tools Server")
    print("=" * 70)
    print()

    # 初始化 workflows
    refresh_workflows()

    print()
    print("=" * 70)
    print("📋 可用的 MCP 工具（n8n Workflows）")
    print("=" * 70)
    print()

    for tool in tools_cache:
        print(f"工具名称: {tool['name']}")
        print(f"描述: {tool['description']}")
        print(f"Workflow ID: {tool['metadata']['workflow_id']}")
        print()

    print("=" * 70)
    print(f"🌐 服务器启动: http://localhost:{port}")
    print("=" * 70)
    print()
    print("端点:")
    print(f"  GET  /tools - 列出所有工具")
    print(f"  POST /tools/{{tool_name}} - 调用工具")
    print(f"  POST /refresh - 刷新 workflows")
    print()

    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 19005
    start_server(port)
