# Nacos + Higress MCP 实战教程

本教程包含两个 Demo：

1. **Demo 1**：Python MCP Server 自动注册到 Nacos（`mcp-demo/`）
2. **Demo 2**：REST API 零代码转换为 MCP Server（`rest-to-mcp-demo/` + Higress）

## 目录结构

```
nacos/
├── mcp-demo/                    # Demo 1: Nacos MCP 自动注册
│   └── server.py
├── rest-to-mcp-demo/            # Demo 2: REST API 后端
│   ├── api_server.py            #   REST API 服务 (端口 19001)
│   ├── mcp_server.py            #   [可选] MCP SSE 包装层 (端口 18002)
│   └── requirements.txt
├── higress/                     # Higress 网关配置目录
│   └── configmaps/
│       └── higress-config.yaml
└── nacos-docker-compose.yml     # Nacos Docker 配置
```

---

## 环境准备

### 1. 启动 Nacos (3.x)

```bash
docker compose -f nacos-docker-compose.yml up -d
```

`nacos-docker-compose.yml` 内容：

```yaml
version: '3.9'
services:
    nacos-server:
        image: 'nacos/nacos-server:latest'   # 当前为 3.2.1
        ports:
            - '9848:9848'
            - '8848:8848'
            - '8083:8080'
        environment:
            - NACOS_AUTH_IDENTITY_VALUE=SecretValue2025!
            - NACOS_AUTH_IDENTITY_KEY=ServerIdentity
            - NACOS_AUTH_TOKEN=SecretKey012345678901234567890123456789012345678901234567890123456789012
            - MODE=standalone
        container_name: nacos-standalone-derby
```

- Nacos 控制台：http://localhost:8083
- Nacos gRPC：8848、9848

> **注意**：Nacos 3.x 默认关闭了服务端 API 鉴权（`nacos.core.auth.enabled=false`），管理端 API 鉴权开启，访问管理 API 需要携带 `ServerIdentity` Header。

### 2. 启动 Higress

```bash
mkdir higress && cd higress

docker pull higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/all-in-one:latest

docker run -d --rm --name higress-ai -v ${PWD}:/data \
  -p 8001:8001 -p 8080:8080 -p 8443:8443 \
  higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/all-in-one:latest
```

- Higress 控制台：http://localhost:8001
- Higress 网关：http://localhost:8080

### 3. 启动 Redis（MCP SSE 模式必需）

```bash
docker run -d --rm --name higress-redis -p 6379:6379 \
  higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/redis-stack-server:7.4.0-v3
```

> SSE 协议中，工具调用（POST）和响应推送（SSE）是不同的 HTTP 请求，Redis 负责将它们关联到同一个会话。

---

## Demo 1: Nacos MCP 自动注册

### 原理

Python MCP Server 启动时，通过 `nacos-mcp-wrapper-python` 库自动向 Nacos 注册，Nacos 控制台的 **MCP 管理** 页面可以看到注册的 MCP Server。

```
┌──────────────┐  注册  ┌─────────┐  发现  ┌─────────┐
│ Python MCP   │ ────→ │  Nacos  │ ←──── │ Higress │ → MCP 客户端
│ Server       │       │  3.x    │       │ 网关    │
│ (SSE :18001) │       │         │       │         │
└──────────────┘       └─────────┘       └─────────┘
```

### 代码（mcp-demo/server.py）

```python
"""
Nacos MCP Server Demo - 自动注册到 Nacos
"""
from nacos_mcp_wrapper.server.nacos_mcp import NacosMCP
from nacos_mcp_wrapper.server.nacos_settings import NacosSettings
from datetime import datetime

# Nacos 连接配置
nacos_settings = NacosSettings()
nacos_settings.SERVER_ADDR = "127.0.0.1:8848"
nacos_settings.NAMESPACE = "public"
# Nacos 3.x: 服务端 API 鉴权默认关闭，不需要 username/password

mcp = NacosMCP(
    "nacos-mcp-python-demo",
    nacos_settings=nacos_settings,
    version="1.0.0",
    port=18001,
)

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
        # ... 更多商品
    ]
    results = [p for p in products if keyword.lower() in p["name"].lower()]
    if not results:
        return f"未找到与 '{keyword}' 相关的商品"
    output = [f"  - {p['name']}: ¥{p['price']}" for p in results[:max_results]]
    return f"搜索 '{keyword}' 结果:\n" + "\n".join(output)

if __name__ == "__main__":
    mcp.run(transport="sse")
```

### 安装依赖并启动

```bash
pip install nacos-mcp-wrapper-python

cd mcp-demo
python server.py
```

启动后在 Nacos 控制台 (http://localhost:8083) 的 **MCP 管理** 页面可以看到 `nacos-mcp-python-demo`。

---

## Demo 2: REST API 零代码转 MCP（核心）

### 原理

Higress 的 **MCP Server 插件** 充当协议转换层，通过 YAML 模板配置将 MCP 工具调用翻译为 REST API 请求，**不需要写任何 MCP 封装代码**。

```
┌─────────────┐    SSE 连接     ┌──────────────────────┐    HTTP 请求    ┌───────────┐
│ Cherry Studio│ ─────────────→ │     Higress 网关      │ ─────────────→ │ REST API  │
│  (MCP 客户端) │ ←───────────── │  (MCP Server 插件)    │ ←───────────── │ (19001)   │
└─────────────┘   SSE 推送结果   └──────────────────────┘   HTTP 响应    └───────────┘
                                       │
                                       ↓
                                  ┌──────────┐
                                  │  Redis   │
                                  │ (会话管理) │
                                  └──────────┘
```

### 三个关键配置组件

| 组件 | 文件 | 作用 |
|------|------|------|
| **higress-config.yaml** | `configmaps/higress-config.yaml` | 全局：Redis 地址 + SSE 路径匹配规则 |
| **McpBridge + Ingress** | 控制台配置 | 路由：将请求转发到 REST API 后端 |
| **WasmPlugin (MCP Server)** | 控制台配置 | 核心：协议转换，MCP ↔ REST |

### Step 1: 启动 REST API 后端

REST API 是存量服务，不需要做任何修改。

```python
# rest-to-mcp-demo/api_server.py (FastAPI, 端口 19001)
# 提供: GET /api/weather, GET /api/products, POST /api/order/create, GET /api/time
```

```bash
cd rest-to-mcp-demo
pip install fastapi uvicorn requests
python api_server.py
```

### Step 2: 配置 higress-config.yaml

```yaml
# higress/configmaps/higress-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: higress-config
  namespace: higress-system
data:
  higress: |-
    mcpServer:
      sse_path_suffix: /sse
      enable: true
      redis:
        address: 192.168.31.155:6379    # 本机内网 IP，不能用 127.0.0.1
        username: ""
        password: ""
        db: 0
      match_list:
        - match_rule_domain: "*"
          match_rule_path: /mcp         # MCP 会话路径前缀
          match_rule_type: "prefix"
      servers: []
    downstream:
```

### Step 3: Higress 控制台配置

#### 3.1 添加服务来源

**服务来源** → **添加服务来源**：
- 类型：**DNS**
- 名称：`rest-api-server`
- 域名：`host.docker.internal`
- 端口：`19001`
- 协议：HTTP

#### 3.2 创建路由

**路由配置** → **创建路由**：
- 路由名称：`ceshi`
- 路径：`/mcp`
- 匹配类型：**Prefix**
- 目标服务：选择上面创建的 `rest-api-server`

#### 3.3 配置 MCP Server 插件（核心）

点击路由的 **"策略"** → 找到 **"MCP 服务器"** 插件 → 开启 → 切换到 **YAML 视图**，填入：

```yaml
server:
  name: "rest-api-server"
tools:
  - name: "query_weather"
    description: "查询指定城市的天气信息，包括温度、湿度、风力等"
    requestTemplate:
      method: "GET"
      url: "http://host.docker.internal:19001/api/weather?city={{.city}}"
    responseTemplate:
      body: |-
        {{- with .data }}
        城市: {{.city}}
        天气: {{.weather}}
        温度: {{.temp}}°C
        湿度: {{.humidity}}
        风力: {{.wind}}
        {{- end }}

  - name: "search_products"
    description: "根据关键词搜索商品"
    requestTemplate:
      method: "GET"
      url: "http://host.docker.internal:19001/api/products?keyword={{.keyword}}"
    responseTemplate:
      body: |-
        {{- with .data }}
        共找到 {{.total}} 个商品:
        {{- range .items }}
        - [{{.id}}] {{.name}} | ¥{{.price}} | 库存:{{.stock}} | 分类:{{.category}}
        {{- end }}
        {{- end }}

  - name: "get_product_detail"
    description: "根据商品ID获取商品详细信息"
    requestTemplate:
      method: "GET"
      url: "http://host.docker.internal:19001/api/products/{{.product_id}}"
    responseTemplate:
      body: |-
        {{- with .data }}
        商品详情:
          ID: {{.id}}
          名称: {{.name}}
          价格: ¥{{.price}}
          分类: {{.category}}
          库存: {{.stock}}
        {{- end }}

  - name: "create_order"
    description: "创建订单，需要指定商品ID和数量"
    requestTemplate:
      method: "POST"
      url: "http://host.docker.internal:19001/api/order/create"
      body: '{"product_id": {{.product_id}}, "quantity": {{.quantity}}, "address": "{{.address}}"}'
    responseTemplate:
      body: |-
        {{- with .data }}
        订单创建成功!
          订单号: {{.order_id}}
          商品: {{.product_name}}
          总价: ¥{{.total_price}}
          状态: {{.status}}
        {{- end }}

  - name: "get_server_time"
    description: "获取服务器当前时间"
    requestTemplate:
      method: "GET"
      url: "http://host.docker.internal:19001/api/time"
    responseTemplate:
      body: |-
        {{- with .data }}
        服务器时间: {{.datetime}}
        时区: {{.timezone}}
        时间戳: {{.timestamp}}
        {{- end }}
```

点击 **保存**。

### Step 4: Cherry Studio 配置

1. **设置** → **MCP 服务器** → **添加**
2. 类型：**服务器发送事件 (SSE)**
3. URL：`http://localhost:8080/mcp/sse`
4. 保存后在对话中激活该 MCP 服务

### 验证

```bash
# 测试 SSE 连接（应返回 session endpoint）
curl -s -m 3 -N http://localhost:8080/mcp/sse
# 预期输出: event: endpoint \n data: /mcp?sessionId=xxxxx
```

---

## 模板语法说明

### requestTemplate

| 字段 | 说明 |
|------|------|
| `method` | HTTP 方法：GET / POST / PUT / DELETE |
| `url` | 请求 URL，用 `{{.参数名}}` 做变量替换 |
| `body` | POST 请求体，支持 JSON 模板 |

### responseTemplate

使用 Go 模板语法处理 REST API 返回的 JSON：

```yaml
# 访问嵌套字段
{{.data.city}}

# with 块简化嵌套访问
{{- with .data }}
  城市: {{.city}}
{{- end }}

# range 遍历数组
{{- range .items }}
  - {{.name}}: ¥{{.price}}
{{- end }}
```

---

## 踪坑记录

### 1. Nacos 3.x 鉴权变化

Nacos 3.x 默认关闭服务端 API 鉴权，`nacos-mcp-wrapper-python` 的 `NacosSettings` 不需要设置 `USERNAME` 和 `PASSWORD`，否则会报 403。

### 2. higress-config.yaml 中的 Redis 地址

必须使用**本机内网 IP**（如 `192.168.31.155`），不能用 `127.0.0.1` 或 `localhost`，因为 Higress 运行在 Docker 容器内。

```bash
# macOS 获取内网 IP
ipconfig getifaddr en0
```

### 3. MCP Server 插件 configDisable

通过控制台配置时，确认 WasmPlugin 的 `configDisable` 为 `false`。如果工具列表获取不到，检查 `wasmplugins/mcp-server-1.0.0.yaml`：

```yaml
matchRules:
  - configDisable: false    # 必须是 false！
    ingress:
    - ceshi                  # 关联的路由名
```

### 4. Higress 路由 rewrite-path

路由的 `rewrite-path` 不要随意设置。MCP SSE 模式下，Higress 会自动处理路径重写，不需要手动配 `rewrite-path`。

### 5. FastMCP SSE 模式不支持异步 HTTP 客户端

如果使用 FastMCP 编写 MCP SSE 包装层（`mcp_server.py`），工具函数内**不能使用 `httpx.AsyncClient`**，会导致 "Server disconnected" 错误。必须使用同步的 `requests` 库。

### 6. Docker 域名截断问题

Higress McpBridge 配置 DNS 服务来源时，域名 `host.docker.internal` 可能被截断为 `host.docker.interna`（少了个 `l`）。检查 `mcpbridges/default.yaml` 确认域名完整。

### 7. 配置修改后生效方式

非 Linux 系统（macOS/Windows）修改 yaml 配置后需要等待一段时间才能生效。如需立即生效：

```bash
docker stop higress-ai
docker rm higress-ai
docker run -d --rm --name higress-ai -v ${PWD}:/data \
  -p 8001:8001 -p 8080:8080 -p 8443:8443 \
  higress-registry.cn-hangzhou.cr.aliyuncs.com/higress/all-in-one:latest
```

---

## 两种方案对比

| | 方案一：MCP 代码封装 | 方案二：Higress 零代码转换 |
|---|---|---|
| **需要写代码** | 需要（FastMCP wrapper） | 不需要 |
| **转换层** | `mcp_server.py` (Python) | Higress WasmPlugin (YAML) |
| **灵活性** | 高，可做复杂逻辑 | 中，模板语法有限制 |
| **运维** | 多一个服务要维护 | 全在网关层，统一管理 |
| **适用场景** | 需要复杂参数处理/聚合 | 标准 REST API 快速接入 |

---

## 参考文档

- [Nacos MCP 自动注册](https://nacos.io/docs/latest/manual/admin/mcp-server/)
- [Higress MCP Server 快速开始](https://higress.cn/docs/ai/mcp-quick-start_docker/)
- [Higress MCP SSE 代理](https://higress.cn/docs/ai/mcp-with-sse/)
- [nacos-mcp-wrapper-python](https://github.com/nacos-group/nacos-mcp-wrapper-python)
