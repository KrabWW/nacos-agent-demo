"""
MCP HTTP Bridge - 为 n8n 提供 MCP 工具接口
将 REST API 包装成 MCP 协议格式，供 n8n MCP 客户端调用
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import httpx
import uvicorn

app = FastAPI(title="MCP HTTP Bridge for n8n")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 后端 API 地址
BACKEND_API = "http://localhost:19001"

# MCP 工具定义
MCP_TOOLS = [
    {
        "name": "search_products",
        "description": "根据关键词搜索商品",
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "搜索关键词"}
            }
        }
    },
    {
        "name": "create_order",
        "description": "创建订单，需要指定商品ID和数量",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "商品ID"},
                "quantity": {"type": "integer", "description": "购买数量"},
                "address": {"type": "string", "description": "收货地址"}
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "get_server_time",
        "description": "获取服务器当前时间",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    }
]


class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]


@app.get("/")
async def root():
    """MCP 服务信息"""
    return {
        "name": "MCP HTTP Bridge",
        "version": "1.0.0",
        "description": "将 REST API 包装成 MCP 工具供 n8n 使用",
        "backend_api": BACKEND_API,
        "tools_count": len(MCP_TOOLS)
    }


@app.get("/tools")
async def list_tools():
    """列出所有可用的 MCP 工具"""
    return {
        "tools": MCP_TOOLS
    }


@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, arguments: Dict[str, Any]):
    """调用指定的 MCP 工具"""

    if tool_name == "search_products":
        return await search_products(arguments.get("keyword", ""))
    elif tool_name == "create_order":
        return await create_order(arguments)
    elif tool_name == "get_server_time":
        return await get_server_time()
    else:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")


async def search_products(keyword: str) -> Dict[str, Any]:
    """搜索商品"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_API}/api/products", params={"keyword": keyword})
        data = response.json()

        return {
            "success": True,
            "tool": "search_products",
            "result": data["data"]
        }


async def create_order(args: Dict[str, Any]) -> Dict[str, Any]:
    """创建订单"""
    async with httpx.AsyncClient() as client:
        payload = {
            "product_id": args.get("product_id"),
            "quantity": args.get("quantity", 1),
            "address": args.get("address", "默认地址")
        }
        response = await client.post(f"{BACKEND_API}/api/order/create", json=payload)
        data = response.json()

        return {
            "success": True,
            "tool": "create_order",
            "result": data["data"]
        }


async def get_server_time() -> Dict[str, Any]:
    """获取服务器时间"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_API}/api/time")
        data = response.json()

        return {
            "success": True,
            "tool": "get_server_time",
            "result": data["data"]
        }


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
    print("=" * 60)
    print("MCP HTTP Bridge for n8n")
    print("=" * 60)
    print(f"服务地址: http://localhost:19002")
    print(f"后端 API: {BACKEND_API}")
    print(f"可用工具: {len(MCP_TOOLS)} 个")
    print("")
    print("MCP 端点:")
    print("  GET  /tools              - 列出所有工具")
    print("  POST /tools/{tool_name}  - 调用工具")
    print("  GET  /health             - 健康检查")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=19002)
