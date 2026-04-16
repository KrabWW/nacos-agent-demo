#!/usr/bin/env python3
"""
MCP SSE Server - 支持 Server-Sent Events 的 MCP 服务器
用于连接 n8n MCP Client Tool 节点
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
import httpx
import json
import asyncio

app = FastAPI(title="MCP SSE Server for n8n")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_API = "http://localhost:19003"

# MCP 工具列表（从 OpenAPI 自动生成）
MCP_TOOLS = [
    {
        "name": "search_products_api_products_get",
        "description": "搜索商品",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "搜索关键词"}
            }
        }
    },
    {
        "name": "create_order_api_order_create_post",
        "description": "创建订单",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "商品ID"},
                "quantity": {"type": "integer", "description": "数量"},
                "address": {"type": "string", "description": "地址"}
            },
            "required": ["product_id"]
        }
    }
]


@app.get("/")
async def root():
    """服务器信息"""
    return {
        "name": "MCP SSE Server for n8n",
        "version": "1.0.0",
        "mcp_endpoint": "/sse",
        "tools_count": len(MCP_TOOLS)
    }


@app.get("/sse")
async def mcp_sse_endpoint():
    """MCP SSE 端点 - 连接 n8n MCP Client Tool"""

    async def event_stream():
        """SSE 事件流"""
        # 发送初始化消息
        yield f"event: tools\ndata: {json.dumps({'tools': MCP_TOOLS})}\n\n"

        # 保持连接
        try:
            while True:
                await asyncio.sleep(30)
                # 发送心跳
                yield f": keep-alive\n\n"
        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@app.post("/tools/{tool_name}")
async def execute_tool(tool_name: str, arguments: Dict[str, Any]):
    """执行 MCP 工具"""

    # 调用后端 MCP Bridge
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BACKEND_API}/tools/{tool_name}",
            json=arguments
        )
        return response.json()


@app.get("/tools")
async def list_tools():
    """列出可用工具"""
    return {"tools": MCP_TOOLS}


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("🚀 MCP SSE Server for n8n")
    print("=" * 60)
    print(f"MCP SSE Endpoint: http://localhost:19004/sse")
    print(f"Tools Endpoint: http://localhost:19004/tools")
    print(f"可用工具: {len(MCP_TOOLS)} 个")
    print("")
    print("📋 在 n8n 中配置 MCP Client Tool:")
    print("1. 添加 'MCP Client Tool' 节点")
    print("2. SSE Endpoint: http://localhost:19004/sse")
    print("3. Authentication: None")
    print("4. Tools to Include: All")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=19004)
