"""
从 OpenAPI 自动生成的 MCP Bridge
生成时间: "http://localhost:19001/openapi.json"
后端 API: http://localhost:19001
可用工具: 6 个
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

BACKEND_API = "http://localhost:19001"

MCP_TOOLS = [
  {
    "name": "root__get",
    "description": "Root",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    },
    "metadata": {
      "path": "/",
      "method": "GET",
      "openapi_operationId": "root__get"
    }
  },
  {
    "name": "get_weather_api_weather_get",
    "description": "查询天气信息",
    "inputSchema": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "城市名称"
        }
      },
      "required": [
        "city"
      ]
    },
    "metadata": {
      "path": "/api/weather",
      "method": "GET",
      "openapi_operationId": "get_weather_api_weather_get"
    }
  },
  {
    "name": "search_products_api_products_get",
    "description": "搜索商品",
    "inputSchema": {
      "type": "object",
      "properties": {
        "keyword": {
          "type": "string",
          "description": "搜索关键词"
        }
      },
      "required": []
    },
    "metadata": {
      "path": "/api/products",
      "method": "GET",
      "openapi_operationId": "search_products_api_products_get"
    }
  },
  {
    "name": "get_product_api_products__product_id__get",
    "description": "获取商品详情",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    },
    "metadata": {
      "path": "/api/products/{product_id}",
      "method": "GET",
      "openapi_operationId": "get_product_api_products__product_id__get"
    }
  },
  {
    "name": "create_order_api_order_create_post",
    "description": "创建订单",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    },
    "metadata": {
      "path": "/api/order/create",
      "method": "POST",
      "openapi_operationId": "create_order_api_order_create_post"
    }
  },
  {
    "name": "get_time_api_time_get",
    "description": "获取服务器时间",
    "inputSchema": {
      "type": "object",
      "properties": {},
      "required": []
    },
    "metadata": {
      "path": "/api/time",
      "method": "GET",
      "openapi_operationId": "get_time_api_time_get"
    }
  }
]


async def root__get(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Root"""
    async with httpx.AsyncClient() as client:
        params = {k: v for k, v in arguments.items() if v is not None}
        response = await client.get(f"{BACKEND_API}/", params=params)
        data = response.json()
        return {
            "success": True,
            "tool": "root__get",
            "result": data.get("data", data)
        }

async def get_weather_api_weather_get(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """查询天气信息"""
    async with httpx.AsyncClient() as client:
        params = {k: v for k, v in arguments.items() if v is not None}
        response = await client.get(f"{BACKEND_API}/api/weather", params=params)
        data = response.json()
        return {
            "success": True,
            "tool": "get_weather_api_weather_get",
            "result": data.get("data", data)
        }

async def search_products_api_products_get(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """搜索商品"""
    async with httpx.AsyncClient() as client:
        params = {k: v for k, v in arguments.items() if v is not None}
        response = await client.get(f"{BACKEND_API}/api/products", params=params)
        data = response.json()
        return {
            "success": True,
            "tool": "search_products_api_products_get",
            "result": data.get("data", data)
        }

async def get_product_api_products__product_id__get(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """获取商品详情"""
    async with httpx.AsyncClient() as client:
        params = {k: v for k, v in arguments.items() if v is not None}
        response = await client.get(f"{BACKEND_API}/api/products/{product_id}", params=params)
        data = response.json()
        return {
            "success": True,
            "tool": "get_product_api_products__product_id__get",
            "result": data.get("data", data)
        }

async def create_order_api_order_create_post(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """创建订单"""
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_API}/api/order/create", json=arguments)
        data = response.json()
        return {
            "success": True,
            "tool": "create_order_api_order_create_post",
            "result": data.get("data", data)
        }

async def get_time_api_time_get(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """获取服务器时间"""
    async with httpx.AsyncClient() as client:
        params = {k: v for k, v in arguments.items() if v is not None}
        response = await client.get(f"{BACKEND_API}/api/time", params=params)
        data = response.json()
        return {
            "success": True,
            "tool": "get_time_api_time_get",
            "result": data.get("data", data)
        }

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
        "root__get": root__get,
        "get_weather_api_weather_get": get_weather_api_weather_get,
        "search_products_api_products_get": search_products_api_products_get,
        "get_product_api_products__product_id__get": get_product_api_products__product_id__get,
        "create_order_api_order_create_post": create_order_api_order_create_post,
        "get_time_api_time_get": get_time_api_time_get,
    }

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
