#!/usr/bin/env python3
"""
从 OpenAPI 规范自动生成 MCP 工具配置
真正实现 OpenAPI 驱动的 MCP 转换
"""

import json
import sys
import requests
from typing import Dict, List, Any

def fetch_openapi_spec(url: str) -> Dict[str, Any]:
    """获取 OpenAPI 规范"""
    print(f"📖 正在获取 OpenAPI 规范: {url}")
    response = requests.get(url)
    response.raise_for_status()
    spec = response.json()
    print(f"✅ OpenAPI 规范获取成功: {spec['info']['title']} {spec['info']['version']}")
    return spec

def openapi_operation_to_mcp_tool(
    path: str,
    method: str,
    operation: Dict[str, Any],
    base_url: str
) -> Dict[str, Any]:
    """将 OpenAPI 操作转换为 MCP 工具定义"""

    operation_id = operation.get('operationId', f"{method}_{path.replace('/', '_')}")
    summary = operation.get('summary', operation.get('description', f"{method.upper()} {path}"))
    description = operation.get('description', summary)

    # 构建输入参数 Schema
    properties = {}
    required = []

    # 从 query parameters 提取参数
    parameters = operation.get('parameters', [])
    for param in parameters:
        if param.get('in') == 'query':
            param_name = param['name']
            param_schema = param.get('schema', {})
            properties[param_name] = {
                "type": param_schema.get('type', 'string'),
                "description": param.get('description', param_schema.get('title', ''))
            }
            if param.get('required', False):
                required.append(param_name)

    # 从 requestBody 提取参数 (仅支持 JSON)
    if 'requestBody' in operation:
        request_body = operation['requestBody']
        content = request_body.get('content', {})
        json_content = content.get('application/json', {})
        schema = json_content.get('schema', {})

        if 'properties' in schema:
            for prop_name, prop_schema in schema['properties'].items():
                properties[prop_name] = {
                    "type": prop_schema.get('type', 'string'),
                    "description": prop_schema.get('description', '')
                }
                if prop_name in schema.get('required', []):
                    required.append(prop_name)

    return {
        "name": operation_id,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required
        },
        "metadata": {
            "path": path,
            "method": method.upper(),
            "openapi_operationId": operation_id
        }
    }

def generate_mcp_tools_from_openapi(openapi_url: str, base_url: str) -> List[Dict[str, Any]]:
    """从 OpenAPI 规范生成 MCP 工具列表"""

    spec = fetch_openapi_spec(openapi_url)
    paths = spec.get('paths', {})

    mcp_tools = []

    print(f"\n🔧 开始解析 OpenAPI 路径...")
    for path, path_item in paths.items():
        for method, operation in path_item.items():
            if method in ['get', 'post', 'put', 'delete']:
                tool = openapi_operation_to_mcp_tool(path, method, operation, base_url)
                mcp_tools.append(tool)
                print(f"  ✓ {method.upper():6} {path:30} → {tool['name']}")

    print(f"\n✅ 成功生成 {len(mcp_tools)} 个 MCP 工具")
    return mcp_tools

def generate_mcp_bridge_code(mcp_tools: List[Dict[str, Any]], base_url: str) -> str:
    """生成 MCP Bridge Python 代码"""

    code_template = f'''"""
从 OpenAPI 自动生成的 MCP Bridge
生成时间: {json.dumps(openapi_url)}
后端 API: {base_url}
可用工具: {len(mcp_tools)} 个
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
import httpx
import uvicorn

app = FastAPI(title="Auto-generated MCP Bridge from OpenAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_API = "{base_url}"

MCP_TOOLS = {json.dumps(mcp_tools, indent=2, ensure_ascii=False)}

'''

    # 为每个工具生成处理函数
    for tool in mcp_tools:
        operation_id = tool['name']
        path = tool['metadata']['path']
        method = tool['metadata']['method']

        # 生成请求处理逻辑
        if method == 'GET':
            handler_code = f'''
async def {operation_id}(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """{tool['description']}"""
    async with httpx.AsyncClient() as client:
        params = {{k: v for k, v in arguments.items() if v is not None}}
        response = await client.get(f"{{BACKEND_API}}{path}", params=params)
        data = response.json()
        return {{
            "success": True,
            "tool": "{operation_id}",
            "result": data.get("data", data)
        }}
'''
        elif method == 'POST':
            handler_code = f'''
async def {operation_id}(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """{tool['description']}"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{{BACKEND_API}}{path}", json=arguments)
        data = response.json()
        return {{
            "success": True,
            "tool": "{operation_id}",
            "result": data.get("data", data)
        }}
'''
        else:
            handler_code = f'''
async def {operation_id}(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """{tool['description']}"""
    raise HTTPException(status_code=501, detail="Method {method} not implemented")
'''

        code_template += handler_code

    # 生成主逻辑
    code_template += '''
@app.get("/")
async def root():
    """MCP 服务信息"""
    return {
        "name": "Auto-generated MCP Bridge",
        "version": "1.0.0",
        "description": "从 OpenAPI 自动生成的 MCP 工具服务",
        "backend_api": BACKEND_API,
        "tools_count": len(MCP_TOOLS),
        "source": "OpenAPI"
    }

@app.get("/tools")
async def list_tools():
    """列出所有可用的 MCP 工具"""
    return {"tools": MCP_TOOLS}

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, arguments: Dict[str, Any]):
    """调用指定的 MCP 工具"""
    tool_map = {
'''

    # 添加工具映射
    for tool in mcp_tools:
        code_template += f'        "{tool["name"]}": {tool["name"]},\n'

    code_template += '''    }

    if tool_name not in tool_map:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    return await tool_map[tool_name](arguments)

@app.get("/health")
async def health():
    """健康检查"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BACKEND_API}/", timeout=2.0)
            return {"status": "healthy", "backend": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🚀 Auto-generated MCP Bridge from OpenAPI")
    print("=" * 60)
    print(f"后端 API: {BACKEND_API}")
    print(f"可用工具: {len(MCP_TOOLS)} 个")
    print(f"端口: 19003")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=19003)
'''

    return code_template

if __name__ == "__main__":
    # 配置
    openapi_url = "http://localhost:19001/openapi.json"
    base_url = "http://localhost:19001"

    print("🚀 OpenAPI 到 MCP 工具生成器")
    print("=" * 60)

    # 步骤 1: 从 OpenAPI 生成 MCP 工具定义
    mcp_tools = generate_mcp_tools_from_openapi(openapi_url, base_url)

    # 步骤 2: 生成 MCP Bridge 代码
    print(f"\n📝 正在生成 MCP Bridge 代码...")
    bridge_code = generate_mcp_bridge_code(mcp_tools, base_url)

    # 步骤 3: 保存生成的代码
    output_file = "mcp-bridge-from-openapi.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(bridge_code)

    print(f"✅ MCP Bridge 代码已生成: {output_file}")

    # 步骤 4: 输出 MCP 工具定义
    tools_file = "mcp-tools-from-openapi.json"
    with open(tools_file, "w", encoding="utf-8") as f:
        json.dump({"tools": mcp_tools}, f, indent=2, ensure_ascii=False)

    print(f"✅ MCP 工具定义已保存: {tools_file}")
    print(f"\n🎯 运行生成服务: python3 {output_file}")
    print("=" * 60)
