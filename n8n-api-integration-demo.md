# n8n API 集成演示 - 通过Swagger快速集成

## 演示场景
**业务流程：搜索商品 → 创建订单**

这个演示展示了如何利用OpenAPI/Swagger文档，在n8n中快速集成两个REST API接口。

---

## 第一步：了解API的Swagger信息

### API 1: 搜索商品 (GET /api/products)

**端点信息：**
```bash
URL: http://localhost:19001/api/products
Method: GET
参数: keyword (可选) - 搜索关键词
```

**Swagger/OpenAPI 定义：**
```json
{
  "get": {
    "summary": "Search Products",
    "description": "搜索商品",
    "operationId": "search_products_api_products_get",
    "parameters": [
      {
        "name": "keyword",
        "in": "query",
        "required": false,
        "schema": {
          "type": "string",
          "description": "搜索关键词",
          "default": "",
          "title": "Keyword"
        }
      }
    ],
    "responses": {
      "200": {
        "description": "Successful Response",
        "content": {
          "application/json": {
            "schema": {}
          }
        }
      }
    }
  }
}
```

**实际请求示例：**
```bash
curl "http://localhost:19001/api/products?keyword=iPhone"
```

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 2,
    "items": [
      {
        "id": 1,
        "name": "iPhone 16",
        "price": 6999,
        "category": "手机",
        "stock": 100
      },
      {
        "id": 6,
        "name": "iPhone 16 Pro Max",
        "price": 9999,
        "category": "手机",
        "stock": 60
      }
    ]
  }
}
```

---

### API 2: 创建订单 (POST /api/order/create)

**端点信息：**
```bash
URL: http://localhost:19001/api/order/create
Method: POST
Content-Type: application/json
```

**Swagger/OpenAPI 定义：**
```json
{
  "post": {
    "summary": "Create Order",
    "description": "创建订单",
    "operationId": "create_order_api_order_create_post",
    "requestBody": {
      "content": {
        "application/json": {
          "schema": {
            "type": "object",
            "properties": {
              "product_id": {"type": "integer"},
              "quantity": {"type": "integer", "default": 1},
              "address": {"type": "string", "default": "默认地址"}
            },
            "required": ["product_id"]
          }
        }
      }
    }
  }
}
```

**实际请求示例：**
```bash
curl -X POST "http://localhost:19001/api/order/create" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2,
    "address": "北京市朝阳区"
  }'
```

**响应示例：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": 1,
    "product_name": "iPhone 16",
    "unit_price": 6999,
    "quantity": 2,
    "total_price": 13998,
    "address": "北京市朝阳区",
    "status": "已创建",
    "created_at": "2026-04-14T14:18:05.299361"
  }
}
```

---

## 第二步：在 n8n 中创建集成 Workflow

### 访问 n8n
打开浏览器访问：http://localhost:5678

### 创建新的 Workflow
1. 点击右上角 "New Workflow"
2. 命名为 "商品搜索与订单创建"

### 添加节点

#### 节点 1: Manual Trigger (手动触发)
- 节点类型: `Manual Trigger`
- 用途: 启动工作流

#### 节点 2: HTTP Request - 搜索商品
- 节点类型: `HTTP Request`
- 配置:
  ```
  Method: GET
  URL: http://localhost:19001/api/products
  Query Parameters:
    keyword: iPhone
  ```

#### 节点 3: Set - 选择商品
- 节点类型: `Set`
- 配置:
  ```
  Keep Only Set: true
  Values:
    - product_id: {{ $json.data.items[0].id }}
    - product_name: {{ $json.data.items[0].name }}
    - quantity: 2
    - address: 北京市朝阳区
  ```

#### 节点 4: HTTP Request - 创建订单
- 节点类型: `HTTP Request`
- 配置:
  ```
  Method: POST
  URL: http://localhost:19001/api/order/create
  Authentication: None
  Request Body: JSON
  Body:
    {
      "product_id": {{ $json.product_id }},
      "quantity": {{ $json.quantity }},
      "address": "{{ $json.address }}"
    }
  ```

### Workflow 连接图
```
[Manual Trigger]
      ↓
[Search Products (HTTP)]
      ↓
[Select Product (Set)]
      ↓
[Create Order (HTTP)]
```

---

## 第三步：测试 Workflow

### 执行步骤
1. 在 n8n 中点击 "Test workflow"
2. 手动触发节点 "Manual Trigger"
3. 观察每个节点的执行结果

### 预期结果
**节点 2 - 搜索商品:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "total": 2,
    "items": [
      {
        "id": 1,
        "name": "iPhone 16",
        "price": 6999,
        "category": "手机",
        "stock": 100
      }
    ]
  }
}
```

**节点 3 - 选择商品:**
```json
{
  "product_id": 1,
  "product_name": "iPhone 16",
  "quantity": 2,
  "address": "北京市朝阳区"
}
```

**节点 4 - 创建订单:**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": 1,
    "product_name": "iPhone 16",
    "unit_price": 6999,
    "quantity": 2,
    "total_price": 13998,
    "address": "北京市朝阳区",
    "status": "已创建",
    "created_at": "2026-04-14T14:18:05.299361"
  }
}
```

---

## 第四步：进阶 - 使用 OpenAPI 规范快速生成 n8n 节点

### 方法 1: 从 Swagger UI 直接复制
1. 访问 Swagger UI: http://localhost:19001/docs
2. 选择需要的接口
3. 点击 "Try it out"
4. 复制请求URL和参数到 n8n HTTP Request 节点

### 方法 2: 使用 OpenAPI JSON 生成
1. 获取 OpenAPI 规范:
   ```bash
   curl http://localhost:19001/openapi.json > api-spec.json
   ```

2. 从规范中提取关键信息:
   ```bash
   cat api-spec.json | jq '.paths | keys'
   ```

3. 根据规范配置 n8n HTTP Request 节点

### 方法 3: 使用 n8n 的 OpenAPI 导入功能
n8n 支持从 OpenAPI 规范导入节点：
- Workflow → Import from URL
- 输入: http://localhost:19001/openapi.json
- 自动生成可用节点列表

---

## 演示总结

### 关键要点
1. **OpenAPI/Swagger 是唯一真相源**
   - 所有接口信息来自统一的 OpenAPI 规范
   - 避免手工配置和猜测参数

2. **从 OpenAPI 到 n8n 的快速路径**
   - Swagger UI 可视化测试
   - OpenAPI JSON 机器可读
   - n8n HTTP Request 节点直接调用

3. **业务编排的价值**
   - 将多个原子API组合成业务流程
   - 在 n8n 中添加逻辑判断、数据转换
   - 对 AI Agent 更友好的高层工具

### 扩展示例
可以继续添加更多节点：
- **库存检查**: 验证库存是否充足
- **价格计算**: 应用折扣规则
- **通知触发**: 发送订单确认邮件
- **数据存储**: 将订单信息保存到数据库

---

## 相关资源

- **Python API 服务**: http://localhost:19001
- **Swagger UI**: http://localhost:19001/docs
- **OpenAPI JSON**: http://localhost:19001/openapi.json
- **n8n 工作区**: http://localhost:5678
- **演示方案文档**: doc/执行中台.md

---

## 下一步

按照执行中台方案，后续可以：
1. 使用 **openapi-to-mcp** 工具将 API 转换为 MCP 工具
2. 通过 **Higress** 网关统一暴露 MCP
3. 在 **Nacos** 中注册和治理这些 MCP 工具
4. 让 **Claude Code** 或其他 AI Agent 直接使用这些工具

这就形成了完整的：
**OpenAPI → n8n Workflow → MCP Tool → AI Agent**
的自动化链路。
