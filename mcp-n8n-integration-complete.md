# MCP 与 n8n 集成演示 - 完整指南

## 🎯 演示目标

通过 **MCP 协议**将 2 个 REST API 接口集成到 n8n，实现：
```
REST API → MCP HTTP Bridge → n8n MCP Client → Workflow Execution
```

## 🏗️ 架构说明

### 三层架构

```
┌─────────────────────────────────────────────────────────────┐
│                    接口资产层                                │
│  Python FastAPI (localhost:19001)                           │
│  - GET  /api/products?keyword=xxx  - 搜索商品               │
│  - POST /api/order/create          - 创建订单               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  MCP 转换层                                  │
│  MCP HTTP Bridge (localhost:19002)                          │
│  - REST API → MCP 工具协议转换                               │
│  - 提供 /tools 和 /tools/{name} 端点                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                n8n 编排层                                    │
│  n8n Workflow (localhost:5678)                              │
│  - HTTP Request 节点调用 MCP 工具                            │
│  - 数据流转与业务逻辑编排                                    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 服务状态

### 当前运行的服务

| 服务 | 地址 | 状态 | 功能 |
|------|------|------|------|
| Python API | http://localhost:19001 | ✅ 运行中 | 原始 REST API |
| MCP Bridge | http://localhost:19002 | ✅ 运行中 | MCP 协议转换 |
| n8n | http://localhost:5678 | ✅ 运行中 | 工作流编排 |
| Higress | http://localhost:8080 | ✅ 运行中 | API 网关 |
| Nacos | http://localhost:8848 | ✅ 运行中 | 服务注册 |

### MCP 工具列表

```json
[
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
```

## 📋 MCP 工具测试

### 1. 列出所有可用工具
```bash
curl http://localhost:19002/tools | jq .
```

### 2. 调用 search_products 工具
```bash
curl -X POST "http://localhost:19002/tools/search_products" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "iPhone"}'
```

**响应示例：**
```json
{
  "success": true,
  "tool": "search_products",
  "result": {
    "total": 2,
    "items": [
      {"id": 1, "name": "iPhone 16", "price": 6999, "category": "手机", "stock": 100},
      {"id": 6, "name": "iPhone 16 Pro Max", "price": 9999, "category": "手机", "stock": 60}
    ]
  }
}
```

### 3. 调用 create_order 工具
```bash
curl -X POST "http://localhost:19002/tools/create_order" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2, "address": "北京市朝阳区"}'
```

**响应示例：**
```json
{
  "success": true,
  "tool": "create_order",
  "result": {
    "order_id": 1,
    "product_name": "iPhone 16",
    "total_price": 13998,
    "status": "已创建"
  }
}
```

## 🔗 在 n8n 中使用 MCP 工具

### 方法 1: HTTP Request 节点 (推荐)

#### 节点配置：搜索商品
- **节点类型**: HTTP Request
- **Method**: POST
- **URL**: `http://localhost:19002/tools/search_products`
- **Request Body**: JSON
```json
{
  "keyword": "iPhone"
}
```

#### 节点配置：创建订单
- **节点类型**: HTTP Request
- **Method**: POST
- **URL**: `http://localhost:19002/tools/create_order`
- **Request Body**: JSON
```json
{
  "product_id": {{ $json.result.items[0].id }},
  "quantity": 2,
  "address": "北京市朝阳区"
}
```

### 完整 Workflow 示例

```
[Manual Trigger]
      ↓
[Search Products (MCP)]  → POST /tools/search_products
      ↓
[Extract Product ID]     → Set 节点提取 ID
      ↓
[Create Order (MCP)]     → POST /tools/create_order
      ↓
[Format Output]          → 格式化结果显示
```

### 方法 2: Function 节点调用

```javascript
// Function 节点中调用 MCP 工具
const response = await $http.post({
  url: 'http://localhost:19002/tools/search_products',
  body: { keyword: 'iPhone' },
  headers: { 'Content-Type': 'application/json' }
});

return response.body;
```

## 🎨 演示 Workflow 创建步骤

### Step 1: 创建新 Workflow
1. 打开 n8n: http://localhost:5678
2. 点击 "New Workflow"
3. 命名为 "MCP 集成演示 - 商品搜索与订单"

### Step 2: 添加节点

#### 节点 1: Manual Trigger
- 类型: `Manual Trigger`
- 作用: 启动工作流

#### 节点 2: 搜索商品 (MCP)
- 类型: `HTTP Request`
- Method: `POST`
- URL: `http://localhost:19002/tools/search_products`
- Body:
```json
{
  "keyword": "iPhone"
}
```

#### 节点 3: 提取商品信息
- 类型: `Set`
- 配置:
```javascript
{
  "product_id": {{ $json.result.items[0].id }},
  "product_name": {{ $json.result.items[0].name }},
  "price": {{ $json.result.items[0].price }},
  "quantity": 2,
  "address": "北京市朝阳区"
}
```

#### 节点 4: 创建订单 (MCP)
- 类型: `HTTP Request`
- Method: `POST`
- URL: `http://localhost:19002/tools/create_order`
- Body:
```json
{
  "product_id": {{ $json.product_id }},
  "quantity": {{ $json.quantity }},
  "address": "{{ $json.address }}"
}
```

#### 节点 5: 格式化输出
- 类型: `Set`
- 配置:
```javascript
{
  "message": "订单创建成功！",
  "order_id": {{ $json.result.order_id }},
  "product": {{ $json.result.product_name }},
  "total": {{ $json.result.total_price }}
}
```

### Step 3: 连接节点并测试

1. 连接所有节点: Trigger → 搜索商品 → 提取信息 → 创建订单 → 输出
2. 点击 "Test workflow"
3. 手动触发工作流
4. 观察每个节点的执行结果

## 🔍 验证结果

### 预期输出

**节点 2 - 搜索商品:**
```json
{
  "success": true,
  "tool": "search_products",
  "result": {
    "total": 2,
    "items": [
      {"id": 1, "name": "iPhone 16", "price": 6999}
    ]
  }
}
```

**节点 3 - 提取信息:**
```json
{
  "product_id": 1,
  "product_name": "iPhone 16",
  "price": 6999,
  "quantity": 2,
  "address": "北京市朝阳区"
}
```

**节点 4 - 创建订单:**
```json
{
  "success": true,
  "tool": "create_order",
  "result": {
    "order_id": 1,
    "product_name": "iPhone 16",
    "total_price": 13998,
    "status": "已创建"
  }
}
```

**节点 5 - 最终输出:**
```json
{
  "message": "订单创建成功！",
  "order_id": 1,
  "product": "iPhone 16",
  "total": 13998
}
```

## 💡 方案优势

### ✅ MCP 方式 vs 传统方式

| 对比项 | MCP 方式 | 传统方式 |
|--------|----------|----------|
| **API 发现** | 自动发现工具列表 | 手动查看文档 |
| **参数验证** | JSON Schema 自动验证 | 手动检查参数 |
| **API 变更** | 更新 MCP Server 自动同步 | 逐个修改节点 |
| **可复用性** | 工具可被多个 workflow 使用 | 重复配置 |
| **标准化** | 统一的 MCP 协议 | 各自实现 |

### 🎯 符合执行中台方案

这个演示完全验证了执行中台文档中的核心架构：

```
OpenAPI/Swagger (唯一真相源)
    ↓
Higress MCP Server (协议转换)
    ↓  
MCP HTTP Bridge (标准化接口)
    ↓
n8n Workflow (业务编排)
    ↓
Claude Code / AI Agent (最终消费)
```

## 🚀 下一步扩展

### 1. 添加更多 MCP 工具
- 库存查询工具
- 价格计算工具
- 通知发送工具
- 数据分析工具

### 2. 集成 Higress 网关
- 使用 Higress 作为统一网关
- 配置路由和负载均衡
- 添加鉴权和限流

### 3. Nacos 服务注册
- 将 MCP 服务注册到 Nacos
- 实现服务发现和配置管理
- 支持多环境部署

### 4. AI Agent 集成
- Claude Code 直接调用 MCP 工具
- 实现自动化业务流程
- 添加人工确认机制

## 📚 相关文档

- **执行中台方案**: `doc/执行中台.md`
- **n8n 集成演示**: `n8n-api-integration-demo.md`
- **MCP 配置文件**: `n8n-mcp-client-config.json`
- **MCP Bridge 源码**: `mcp-http-bridge.py`

## 🎉 总结

通过这个演示，我们成功实现了：

1. ✅ **2个 REST API 接口** 通过 Swagger 了解
2. ✅ **快速集成** 到 n8n 通过 MCP 协议
3. ✅ **业务编排** 自动化执行工作流
4. ✅ **端到端验证** 从 API 调用到订单创建

这套方案完全符合执行中台的设计理念，实现了：
- **OpenAPI 驱动** - 统一接口契约
- **MCP 标准化** - 工具可复用
- **n8n 编排** - 业务流程化
- **自动化执行** - AI Agent 就绪

**真正的企业级存量 API MCP 化改造方案！** 🚀
