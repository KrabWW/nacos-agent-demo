# Nacos 3.x + Higress MCP 实战

Nacos MCP 生态实战项目，包含 MCP 自动注册、REST API 零代码转 MCP、A2A Agent 编排等多个场景的完整 Demo。

## 项目结构

```
├── agent-server/              # Spring Boot A2A Agent 服务 (端口 9999)
│   └── REST API: /api/ask, /api/faq, /api/info
├── agent-client/              # A2A 客户端，调用远程 Agent
├── mcp-demo/                  # Demo 1: Python MCP Server 自动注册到 Nacos
│   └── server.py
├── rest-to-mcp-demo/          # Demo 2: REST API 通过 Higress 转 MCP
│   ├── api_server.py          #   REST API 后端 (端口 19001)
│   ├── mcp_server.py          #   [可选] MCP SSE 包装层 (端口 18002)
│   └── requirements.txt
├── travel-demo/               # Demo 3: 多 Agent 旅行规划
│   ├── flight-agent/          #   航班 Agent
│   ├── hotel-agent/           #   酒店 Agent
│   ├── weather-agent/         #   天气 Agent
│   └── travel-planner/        #   旅行规划调度
├── higress/                   # Higress AI 网关配置
├── nacos-docker-compose.yml   # Nacos 3.x Docker Compose
├── redis-docker-compose.yml   # Redis Docker Compose
└── pom.xml                    # Maven 父 POM (Spring Boot 3.4.3)
```

## 环境准备

### 1. 启动 Nacos 3.x

```bash
docker compose -f nacos-docker-compose.yml up -d
# 控制台: http://localhost:8080  账号/密码: nacos/nacos
```

### 2. 启动 Redis（Higress MCP 协议转换需要）

```bash
docker compose -f redis-docker-compose.yml up -d
```

### 3. 启动 Higress AI 网关

参考 [Higress Docker 快速开始](https://higress.io/docs/latest/ops/deploy-by-docker/)，确保 MCP Server 功能已开启。

## Demo 1: Python MCP Server 自动注册到 Nacos

> MCP Server 启动后自动注册到 Nacos，AI Agent 可直接发现并调用。

```bash
cd mcp-demo
pip install nacos-mcp-wrapper
python server.py
```

提供的 MCP Tools：

| Tool | 说明 |
|------|------|
| `get_weather` | 查询城市天气 |
| `add` | 加法运算 |
| `get_time` | 获取当前时间 |
| `search_products` | 搜索商品 |

## Demo 2: REST API 零代码转 MCP (Higress)

> 任意 REST API 通过 Higress MCP Server 插件转为 MCP Tool，无需改动后端代码。

```bash
# 1. 启动 REST API 后端
cd rest-to-mcp-demo
pip install -r requirements.txt
python api_server.py  # 端口 19001

# 2. 在 Higress 控制台配置 MCP Server 插件
#    详情见 TUTORIAL.md
```

## Demo 3: Agent Server (A2A)

> Spring Boot Agent 通过 A2A 协议注册到 Nacos，支持 REST API 调用，可被 Higress 包装为 MCP Tool。

```bash
# 编译
mvn clean package -DskipTests

# 启动 agent-server（需要设置 MINIMAX_API_KEY 环境变量）
MINIMAX_API_KEY=your-key java -jar agent-server/target/agent-server-1.0.0.jar

# 启动 agent-client
java -jar agent-client/target/agent-client-1.0.0.jar
```

REST API 接口：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/ask?question=xxx` | GET | 向 Agent 提问，返回同步响应 |
| `/api/faq?keyword=xxx` | GET | 搜索 Nacos FAQ |
| `/api/info` | GET | Agent 信息 & 健康检查 |

Higress MCP Server 插件配置参考：

```yaml
server:
  name: "agent-server-mcp"
tools:
  - name: "ask-agent"
    description: "向 Nacos 助手 Agent 提问"
    requestTemplate:
      method: "GET"
      url: "http://agent-server-demo:9999/api/ask?question={question}"
    responseTemplate:
      body: "{{.answer}}"
  - name: "search-nacos-faq"
    description: "搜索 Nacos 常见问题"
    requestTemplate:
      method: "GET"
      url: "http://agent-server-demo:9999/api/faq?keyword={keyword}"
    responseTemplate:
      body: |-
        {{range .faqs}}
        - **Q**: {{.q}}  **A**: {{.a}}
        {{end}}
```

## Demo 4: 多 Agent 旅行规划

> 基于 A2A 协议的多 Agent 协作，包含航班、酒店、天气三个专业 Agent，由 Travel Planner 统一编排。

```bash
cd travel-demo
mvn clean package -DskipTests

# 分别启动各 Agent（需要 MINIMAX_API_KEY）
java -jar flight-agent/target/flight-agent-1.0.0.jar
java -jar hotel-agent/target/hotel-agent-1.0.0.jar
java -jar weather-agent/target/weather-agent-1.0.0.jar
java -jar travel-planner/target/travel-planner-1.0.0.jar
```

## 技术栈

| 组件 | 版本 |
|------|------|
| Java | 17 |
| Spring Boot | 3.4.3 |
| Spring AI | 1.0.3 |
| Spring AI Alibaba | 1.0.0.4 |
| Nacos | 3.x |
| Higress | 2.1.2+ |
| Python | 3.10+ |

## 参考资料

- [Nacos 官方文档](https://nacos.io/docs/latest/)
- [存量 API 转换 MCP 手册](https://nacos.io/docs/latest/manual/user/ai/api-to-mcp/)
- [Higress MCP Server 文档](https://higress.io/docs/latest/custom/mcp-server/)
- [Spring AI Alibaba](https://sca.aliyun.com/ai/)
