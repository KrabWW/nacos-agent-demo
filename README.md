# Nacos 3.x + Higress MCP 实战

Nacos MCP 生态实战项目，包含 MCP 自动注册、REST API 零代码转 MCP、A2A Agent 编排、n8n 工作流集成等多个场景的完整 Demo。

## 📋 项目结构

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
├── mcp-http-bridge.py         # MCP HTTP Bridge (端口 19002) - n8n 集成
├── create-n8n-workflow-api.py # n8n 工作流自动创建脚本
├── higress/                   # Higress AI 网关配置文件
├── nacos-docker-compose.yml   # Nacos 3.x Docker Compose
├── redis-docker-compose.yml   # Redis Docker Compose
└── pom.xml                    # Maven 父 POM (Spring Boot 3.4.3)
```

## 🚀 快速开始

### 1. 启动基础服务

```bash
# 启动 Nacos 3.x
docker compose -f nacos-docker-compose.yml up -d
# 控制台: http://localhost:8080/nacos  账号/密码: nacos/nacos

# 启动 Redis
docker compose -f redis-docker-compose.yml up -d
```

### 2. 启动 Higress AI 网关

```bash
cd higress
docker compose -f higress-docker-compose.yml up -d
# 控制台: http://localhost:8080
```

详细配置参考 [Higress 官方文档](https://higress.io/docs/latest/ops/deploy-by-docker/)

## 📚 Demo 演示

### Demo 1: Python MCP Server 自动注册到 Nacos

MCP Server 启动后自动注册到 Nacos，AI Agent 可直接发现并调用。

```bash
cd mcp-demo
pip install nacos-mcp-wrapper
python server.py
```

**提供的 MCP Tools：**

| Tool | 说明 |
|------|------|
| `get_weather` | 查询城市天气 |
| `add` | 加法运算 |
| `get_time` | 获取当前时间 |
| `search_products` | 搜索商品 |

### Demo 2: REST API 零代码转 MCP (Higress)

任意 REST API 通过 Higress MCP Server 插件转为 MCP Tool，无需改动后端代码。

```bash
# 1. 启动 REST API 后端
cd rest-to-mcp-demo
pip install -r requirements.txt
python api_server.py  # 端口 19001

# 2. 在 Higress 控制台配置 MCP Server 插件
#    详情见 TUTORIAL.md
```

### Demo 3: Agent Server (A2A)

Spring Boot Agent 通过 A2A 协议注册到 Nacos，支持 REST API 调用，可被 Higress 包装为 MCP Tool。

```bash
# 编译
mvn clean package -DskipTests

# 启动 agent-server（需要设置 MINIMAX_API_KEY 环境变量）
export MINIMAX_API_KEY=your-key
java -jar agent-server/target/agent-server-1.0.0.jar

# 启动 agent-client
java -jar agent-client/target/agent-client-1.0.0.jar
```

**REST API 接口：**

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/ask?question=xxx` | GET | 向 Agent 提问，返回同步响应 |
| `/api/faq?keyword=xxx` | GET | 搜索 Nacos FAQ |
| `/api/info` | GET | Agent 信息 & 健康检查 |

### Demo 4: n8n 工作流集成 (MCP HTTP Bridge)

通过 MCP HTTP Bridge 将 MCP 工具暴露为 REST API，供 n8n 工作流调用。

```bash
# 1. 启动 REST API 后端
cd rest-to-mcp-demo
python api_server.py  # 端口 19001

# 2. 启动 MCP HTTP Bridge
pip install fastapi uvicorn httpx pydantic
python mcp-http-bridge.py  # 端口 19002

# 3. 自动创建 n8n 工作流
pip install requests
python create-n8n-workflow-api.py
```

**MCP HTTP Bridge 端点：**

| 端点 | 方法 | 说明 |
|------|------|------|
| `http://localhost:19002/tools` | GET | 列出所有可用工具 |
| `http://localhost:19002/tools/search_products` | POST | 搜索商品 |
| `http://localhost:19002/tools/create_order` | POST | 创建订单 |
| `http://localhost:19002/health` | GET | 健康检查 |

**测试示例：**

```bash
# 列出所有工具
curl http://localhost:19002/tools | jq .

# 搜索商品
curl -X POST 'http://localhost:19002/tools/search_products' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "手机"}' | jq .

# 创建订单
curl -X POST 'http://localhost:19002/tools/create_order' \
  -H 'Content-Type: application/json' \
  -d '{"product_id": 1, "quantity": 2, "address": "北京市"}' | jq .
```

## 🔧 技术栈

| 组件 | 版本 |
|------|------|
| Java | 17 |
| Spring Boot | 3.4.3 |
| Spring AI | 1.0.3 |
| Spring AI Alibaba | 1.0.0.4 |
| Nacos | 3.x |
| Higress | 2.1.2+ |
| Python | 3.10+ |
| FastAPI | 0.104+ |
| n8n | Latest |

## 📖 参考资料

- [Nacos 官方文档](https://nacos.io/docs/latest/)
- [存量 API 转换 MCP 手册](https://nacos.io/docs/latest/manual/user/ai/api-to-mcp/)
- [Higress MCP Server 文档](https://higress.io/docs/latest/custom/mcp-server/)
- [Spring AI Alibaba](https://sca.aliyun.com/ai/)
- [n8n 官方文档](https://docs.n8n.io/)

## 🎯 核心特性

- ✅ **自动注册**：MCP Server 自动注册到 Nacos 服务发现
- ✅ **零代码转换**：REST API 通过 Higress 零代码转为 MCP Tool
- ✅ **A2A 协议**：支持 Agent-to-Agent 通信协议
- ✅ **工作流集成**：无缝集成 n8n 工作流引擎
- ✅ **多 Agent 协作**：支持多 Agent 编排和协作
- ✅ **生产就绪**：提供完整的 Docker Compose 配置

## 📝 许可证

本项目仅供学习和演示使用。
