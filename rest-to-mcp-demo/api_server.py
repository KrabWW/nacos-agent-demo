"""
REST API 后端服务 - 模拟存量业务接口

提供以下 RESTful 接口：
  - GET  /api/weather?city=xxx          查询天气
  - GET  /api/products?keyword=xxx      搜索商品
  - POST /api/order/create              创建订单
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="REST API Demo", description="存量 REST API 示例")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 模拟数据 ==========

WEATHER_DATA = {
    "北京": {"city": "北京", "weather": "晴", "temp": "22", "humidity": "45%", "wind": "北风3级"},
    "上海": {"city": "上海", "weather": "多云", "temp": "25", "humidity": "68%", "wind": "东南风2级"},
    "深圳": {"city": "深圳", "weather": "阵雨", "temp": "28", "humidity": "82%", "wind": "南风4级"},
    "杭州": {"city": "杭州", "weather": "阴", "temp": "20", "humidity": "55%", "wind": "东风1级"},
    "成都": {"city": "成都", "weather": "小雨", "temp": "18", "humidity": "75%", "wind": "微风"},
}

PRODUCTS = [
    {"id": 1, "name": "iPhone 16", "price": 6999, "category": "手机", "stock": 100},
    {"id": 2, "name": "MacBook Pro", "price": 14999, "category": "电脑", "stock": 50},
    {"id": 3, "name": "AirPods Pro", "price": 1899, "category": "耳机", "stock": 200},
    {"id": 4, "name": "iPad Air", "price": 4799, "category": "平板", "stock": 80},
    {"id": 5, "name": "Apple Watch", "price": 2999, "category": "手表", "stock": 120},
    {"id": 6, "name": "iPhone 16 Pro Max", "price": 9999, "category": "手机", "stock": 60},
    {"id": 7, "name": "MacBook Air", "price": 8999, "category": "电脑", "stock": 70},
    {"id": 8, "name": "小米 15", "price": 3999, "category": "手机", "stock": 150},
    {"id": 9, "name": "华为 Mate 70", "price": 5999, "category": "手机", "stock": 90},
]

ORDERS = []


# ========== API 接口 ==========

@app.get("/")
def root():
    return {"message": "REST API Demo Service is running", "time": datetime.now().isoformat()}


@app.get("/api/weather")
def get_weather(city: str = Query(..., description="城市名称")):
    """查询天气信息"""
    data = WEATHER_DATA.get(city)
    if data:
        return {"code": 0, "message": "success", "data": data}
    return {
        "code": 0,
        "message": "success",
        "data": {"city": city, "weather": "晴", "temp": "24", "humidity": "50%", "wind": "微风"},
    }


@app.get("/api/products")
def search_products(keyword: str = Query("", description="搜索关键词")):
    """搜索商品"""
    results = [p for p in PRODUCTS if keyword.lower() in p["name"].lower()] if keyword else PRODUCTS
    return {"code": 0, "message": "success", "data": {"total": len(results), "items": results}}


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    """获取商品详情"""
    for p in PRODUCTS:
        if p["id"] == product_id:
            return {"code": 0, "message": "success", "data": p}
    return {"code": 404, "message": "商品不存在", "data": None}


class OrderCreate(BaseModel):
    product_id: int
    quantity: int = 1
    address: str = "默认地址"


@app.post("/api/order/create")
def create_order(order: OrderCreate):
    """创建订单"""
    product = next((p for p in PRODUCTS if p["id"] == order.product_id), None)
    if not product:
        return {"code": 404, "message": "商品不存在", "data": None}
    if product["stock"] < order.quantity:
        return {"code": 400, "message": "库存不足", "data": None}

    order_id = len(ORDERS) + 1
    order_data = {
        "order_id": order_id,
        "product_name": product["name"],
        "unit_price": product["price"],
        "quantity": order.quantity,
        "total_price": product["price"] * order.quantity,
        "address": order.address,
        "status": "已创建",
        "created_at": datetime.now().isoformat(),
    }
    ORDERS.append(order_data)
    return {"code": 0, "message": "success", "data": order_data}


@app.get("/api/time")
def get_time():
    """获取服务器时间"""
    return {
        "code": 0,
        "message": "success",
        "data": {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timestamp": int(datetime.now().timestamp()),
            "timezone": "Asia/Shanghai",
        },
    }


if __name__ == "__main__":
    print("=" * 50)
    print("REST API Demo Server")
    print("地址: http://127.0.0.1:19001")
    print("接口:")
    print("  GET  /api/weather?city=xxx")
    print("  GET  /api/products?keyword=xxx")
    print("  GET  /api/products/{id}")
    print("  POST /api/order/create")
    print("  GET  /api/time")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=19001)
