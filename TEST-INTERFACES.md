# 🧪 Workflow 测试接口

## 🎯 可以直接测试的 MCP 接口

### 接口 1: 搜索商品

**端点**: `POST http://localhost:19002/tools/search_products`

**请求**:
```bash
curl -X POST 'http://localhost:19002/tools/search_products' \
  -H 'Content-Type: application/json' \
  -d '{
    "keyword": "iPhone"
  }'
```

**响应示例**:
```json
{
  "success": true,
  "tool": "search_products_api_products_get",
  "result": {
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

### 接口 2: 创建订单

**端点**: `POST http://localhost:19002/tools/create_order`

**请求**:
```bash
curl -X POST 'http://localhost:19002/tools/create_order' \
  -H 'Content-Type: application/json' \
  -d '{
    "product_id": 1,
    "quantity": 2,
    "address": "北京市朝阳区"
  }'
```

**响应示例**:
```json
{
  "success": true,
  "tool": "create_order_api_order_create_post",
  "result": {
    "order_id": 6,
    "product_name": "iPhone 16",
    "unit_price": 6999,
    "quantity": 2,
    "total_price": 13998,
    "address": "北京市朝阳区",
    "status": "已创建"
  }
}
```

### 接口 3: 查看所有工具

**端点**: `GET http://localhost:19002/tools`

**请求**:
```bash
curl 'http://localhost:19002/tools' | jq .
```

**响应**:
```json
{
  "tools": [
    {
      "name": "search_products_api_products_get",
      "description": "搜索商品",
      "inputSchema": {...}
    },
    {
      "name": "create_order_api_order_create_post",
      "description": "创建订单",
      "inputSchema": {...}
    }
  ]
}
```

## 🚀 在 n8n 中创建 Workflow

### 方法 1: 导入 JSON（最快）

1. **打开 n8n**: http://localhost:5678
2. **点击菜单**: 右上角 '...' → 'Import from File'
3. **选择文件**: `workflow-mcp-demo.json`
4. **点击导入**

### 方法 2: 手动创建

#### 步骤 1: 添加 Manual Trigger
- 搜索 "Manual Trigger"
- 点击添加

#### 步骤 2: 添加 HTTP Request（搜索商品）
- 搜索 "HTTP Request"
- 配置:
  - Method: `POST`
  - URL: `http://localhost:19002/tools/search_products`
  - Body > JSON:
    ```json
    {"keyword": "iPhone"}
    ```

#### 步骤 3: 添加 Set（提取商品信息）
- 搜索 "Set"
- 添加字段:
  - `product_id`: `{{ $json.result.items[0].id }}`
  - `product_name`: `{{ $json.result.items[0].name }}`
  - `quantity`: `2`
  - `address`: `北京市朝阳区`

#### 步骤 4: 添加 HTTP Request（创建订单）
- 配置:
  - Method: `POST`
  - URL: `http://localhost:19002/tools/create_order`
  - Body > JSON:
    ```json
    {
      "product_id": {{ $json.product_id }},
      "quantity": {{ $json.quantity }},
      "address": "{{ $json.address }}"
    }
    ```

#### 步骤 5: 添加 Set（格式化输出）
- 添加字段:
  - `message`: `订单创建成功！`
  - `order_id`: `{{ $json.result.order_id }}`
  - `product`: `{{ $json.result.product_name }}`
  - `total`: `{{ $json.result.total_price }}`

#### 步骤 6: 连接节点
- Manual Trigger → 搜索商品
- 搜索商品 → 提取商品信息
- 提取商品信息 → 创建订单
- 创建订单 → 格式化输出

## 🧪 测试 Workflow

### 在 n8n 中测试
1. 点击 'Test workflow'
2. 点击 'Manual Trigger' 执行
3. 查看每个节点的输出

### 预期结果
- **搜索商品**: 找到 2 个 iPhone
- **提取信息**: 提取商品 ID=1
- **创建订单**: 订单 #6，总价 ¥13,998
- **格式化输出**: 显示成功信息

## 📊 完整流程图

```
[Manual Trigger]
      ↓
[HTTP Request - 搜索商品]
      URL: /tools/search_products
      ↓
[Set - 提取商品信息]
      product_id: {{ $json.result.items[0].id }}
      ↓
[HTTP Request - 创建订单]
      URL: /tools/create_order
      ↓
[Set - 格式化输出]
      订单创建成功！
```

---

**现在你可以：**
1. ✅ 直接测试 MCP 接口
2. ✅ 在 n8n 中创建 workflow
3. ✅ 验证完整的业务流程
