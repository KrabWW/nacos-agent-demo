"""
MCP SSE Server - 包装 REST API 为 MCP 工具

将 REST API 的接口转换为 MCP Tool，通过 SSE 协议对外暴露。
后端 REST API: http://127.0.0.1:19001
"""

import requests
from mcp.server.fastmcp import FastMCP

REST_API_BASE = "http://127.0.0.1:19001"

mcp = FastMCP("rest-api-mcp-server")


@mcp.tool()
def query_weather(city: str) -> str:
    """查询指定城市的天气信息，包括温度、湿度、风力等"""
    resp = requests.get(f"{REST_API_BASE}/api/weather", params={"city": city}, timeout=5)
    result = resp.json()
    if result["code"] == 0:
        d = result["data"]
        return (
            f"城市: {d['city']}\n"
            f"天气: {d['weather']}\n"
            f"温度: {d['temp']}°C\n"
            f"湿度: {d['humidity']}\n"
            f"风力: {d['wind']}"
        )
    return f"查询失败: {result['message']}"


@mcp.tool()
def search_products(keyword: str) -> str:
    """根据关键词搜索商品，返回匹配的商品列表"""
    resp = requests.get(f"{REST_API_BASE}/api/products", params={"keyword": keyword}, timeout=5)
    result = resp.json()
    if result["code"] == 0:
        items = result["data"]["items"]
        if not items:
            return f"未找到与 '{keyword}' 相关的商品"
        lines = [f"共找到 {result['data']['total']} 个商品:\n"]
        for p in items:
            lines.append(f"  - [{p['id']}] {p['name']} | ¥{p['price']} | 库存:{p['stock']} | 分类:{p['category']}")
        return "\n".join(lines)
    return f"搜索失败: {result['message']}"


@mcp.tool()
def get_product_detail(product_id: int) -> str:
    """根据商品ID获取商品详细信息"""
    resp = requests.get(f"{REST_API_BASE}/api/products/{product_id}", timeout=5)
    result = resp.json()
    if result["code"] == 0 and result["data"]:
        p = result["data"]
        return (
            f"商品详情:\n"
            f"  ID: {p['id']}\n"
            f"  名称: {p['name']}\n"
            f"  价格: ¥{p['price']}\n"
            f"  分类: {p['category']}\n"
            f"  库存: {p['stock']}"
        )
    return f"商品不存在 (ID: {product_id})"


@mcp.tool()
def create_order(product_id: int, quantity: int = 1, address: str = "默认地址") -> str:
    """创建订单，需要指定商品ID和数量"""
    resp = requests.post(
        f"{REST_API_BASE}/api/order/create",
        json={"product_id": product_id, "quantity": quantity, "address": address},
        timeout=5,
    )
    result = resp.json()
    if result["code"] == 0 and result["data"]:
        d = result["data"]
        return (
            f"订单创建成功!\n"
            f"  订单号: {d['order_id']}\n"
            f"  商品: {d['product_name']}\n"
            f"  单价: ¥{d['unit_price']}\n"
            f"  数量: {d['quantity']}\n"
            f"  总价: ¥{d['total_price']}\n"
            f"  地址: {d['address']}\n"
            f"  状态: {d['status']}\n"
            f"  时间: {d['created_at']}"
        )
    return f"订单创建失败: {result['message']}"


@mcp.tool()
def get_server_time() -> str:
    """获取服务器当前时间"""
    resp = requests.get(f"{REST_API_BASE}/api/time", timeout=5)
    result = resp.json()
    if result["code"] == 0:
        d = result["data"]
        return f"服务器时间: {d['datetime']}\n时区: {d['timezone']}\n时间戳: {d['timestamp']}"
    return "获取时间失败"


if __name__ == "__main__":
    import uvicorn

    print("=" * 50)
    print("MCP SSE Server (REST API Wrapper)")
    print("REST API: http://127.0.0.1:19001")
    print("MCP SSE:  http://127.0.0.1:18002/sse")
    print("=" * 50)
    app = mcp.sse_app()
    uvicorn.run(app, host="0.0.0.0", port=18002)
