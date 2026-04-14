"""
Nacos MCP Server Demo - 自动注册到 Nacos

启动后自动注册到 Nacos，提供以下工具：
  - get_weather: 查询城市天气
  - add: 加法运算
  - get_time: 获取当前时间
  - search_products: 搜索商品
"""

from nacos_mcp_wrapper.server.nacos_mcp import NacosMCP
from nacos_mcp_wrapper.server.nacos_settings import NacosSettings
from datetime import datetime


# ========== Nacos 连接配置 ==========
nacos_settings = NacosSettings()
nacos_settings.SERVER_ADDR = "127.0.0.1:8848"
nacos_settings.NAMESPACE = "public"
# Nacos 3.x: server API auth disabled, skip username/password
# nacos_settings.USERNAME = "nacos"
# nacos_settings.PASSWORD = "nacos"

# ========== 创建 MCP Server 实例 ==========
mcp = NacosMCP(
    "nacos-mcp-python-demo",
    nacos_settings=nacos_settings,
    version="1.0.0",
    port=18001,
)


# ========== 注册工具 ==========

@mcp.tool()
def get_weather(city_name: str) -> str:
    """根据城市名称查询天气信息"""
    mock_data = {
        "北京": "晴天，气温 22°C，空气质量良好",
        "上海": "多云，气温 25°C，有轻微雾霾",
        "深圳": "阵雨，气温 28°C，湿度较高",
        "杭州": "阴天，气温 20°C，适合出行",
    }
    return mock_data.get(city_name, f"{city_name}: 晴，气温 24°C (模拟数据)")


@mcp.tool()
def add(a: int, b: int) -> int:
    """计算两个整数的加法"""
    return a + b


@mcp.tool()
def get_time(timezone_name: str = "Asia/Shanghai") -> str:
    """获取当前时间，可指定时区"""
    now = datetime.now()
    return f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')} (时区: {timezone_name})"


@mcp.tool()
def search_products(keyword: str, max_results: int = 5) -> str:
    """根据关键词搜索商品"""
    products = [
        {"name": "iPhone 16", "price": 6999},
        {"name": "MacBook Pro", "price": 14999},
        {"name": "AirPods Pro", "price": 1899},
        {"name": "iPad Air", "price": 4799},
        {"name": "Apple Watch", "price": 2999},
        {"name": "iPhone 16 Pro Max", "price": 9999},
        {"name": "MacBook Air", "price": 8999},
        {"name": "AirPods Max", "price": 4399},
    ]
    results = [p for p in products if keyword.lower() in p["name"].lower()]
    if not results:
        return f"未找到与 '{keyword}' 相关的商品"
    output = []
    for p in results[:max_results]:
        output.append(f"  - {p['name']}: ¥{p['price']}")
    return f"搜索 '{keyword}' 结果:\n" + "\n".join(output)


# ========== 启动服务 ==========
if __name__ == "__main__":
    print("=" * 50)
    print("Nacos MCP Python Demo Server")
    print("服务名: nacos-mcp-python-demo")
    print("Nacos地址: 127.0.0.1:8848")
    print("端口: 18001")
    print("协议: SSE")
    print("=" * 50)
    try:
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"运行错误: {e}")
