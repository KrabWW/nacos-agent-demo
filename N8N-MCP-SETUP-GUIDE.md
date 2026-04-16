# 在 n8n 中使用 MCP Client Tool 快速创建 Workflow

## 🚀 快速开始

### 第一步：添加 MCP Client Tool 节点

1. 打开 n8n: http://localhost:5678
2. 创建新 workflow: **"MCP 集成演示 - 商品搜索与订单"**
3. 添加 **Manual Trigger** 节点

### 第二步：配置 MCP Client Tool 节点

#### 添加第一个 MCP Client Tool - 搜索商品

1. **添加节点**: 搜索并添加 **"MCP Client Tool"** 节点
2. **配置参数**:
   ```
   SSE Endpoint: http://localhost:19004/sse
   Authentication: None
   Tools to Include: All
   ```
3. **在节点中配置工具调用**:
   ```
   Tool: search_products_api_products_get
   Arguments: {"keyword": "iPhone"}
   ```

#### 添加第二个 MCP Client Tool - 创建订单

1. **添加另一个 MCP Client Tool** 节点
2. **使用相同配置**:
   ```
   SSE Endpoint: http://localhost:19004/sse
   Authentication: None
   Tools to Include: All
   ```
3. **配置工具调用**:
   ```
   Tool: create_order_api_order_create_post
   Arguments: {
     "product_id": {{ $json.result.items[0].id }},
     "quantity": 2,
     "address": "北京市朝阳区"
   }
   ```

### 第三步：连接节点并执行

```
[Manual Trigger]
      ↓
[MCP Client Tool - 搜索商品]
      ↓
[Set - 提取商品ID]
      ↓
[MCP Client Tool - 创建订单]
      ↓
[Set - 格式化输出]
```

### 第四步：测试 Workflow

1. 点击 **"Test workflow"**
2. 手动触发 **Manual Trigger**
3. 观察 MCP Client Tool 节点自动调用工具

## 📊 预期结果

### 节点 1: MCP Client Tool - 搜索商品

**输出:**
```json
{
  "success": true,
  "tool": "search_products_api_products_get",
  "result": {
    "total": 2,
    "items": [
      {"id": 1, "name": "iPhone 16", "price": 6999}
    ]
  }
}
```

### 节点 2: Set - 提取商品ID

**配置:**
```javascript
{
  "product_id": {{ $json.result.items[0].id }},
  "product_name": {{ $json.result.items[0].name }},
  "quantity": 2,
  "address": "北京市朝阳区"
}
```

### 节点 3: MCP Client Tool - 创建订单

**输入:**
```json
{
  "product_id": 1,
  "quantity": 2,
  "address": "北京市朝阳区"
}
```

**输出:**
```json
{
  "success": true,
  "tool": "create_order_api_order_create_post",
  "result": {
    "order_id": 6,
    "product_name": "iPhone 16",
    "total_price": 13998,
    "status": "已创建"
  }
}
```

## 💡 关键优势

### ✅ 使用 n8n MCP Client Tool 的优势

1. **原生集成**
   - n8n 内置的 MCP Client 节点
   - 无需自定义代码
   - 标准化配置

2. **自动发现工具**
   - 自动从 MCP 服务器获取工具列表
   - 工具参数自动提示
   - 实时同步更新

3. **简化配置**
   - 只需配置 SSE Endpoint
   - 工具调用可视化
   - 数据流转直观

4. **AI Agent 就绪**
   - 符合 MCP 标准
   - 可被 Claude、ChatGPT 等调用
   - 标准化工具接口

## 🎯 完整流程总结

```
OpenAPI (localhost:19001)
    ↓ 自动解析
MCP Bridge (localhost:19003)
    ↓ SSE 协议
MCP SSE Server (localhost:19004)
    ↓ MCP Client Tool
n8n Workflow (localhost:5678)
    ↓ 业务执行
订单创建成功 ✅
```

## 📚 参考资源

- **n8n MCP Client Tool 文档**: [官方文档](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/)
- **MCP 协议规范**: [Model Context Protocol](https://modelcontextprotocol.io/)
- **n8n MCP 入门教程**: [Zeabur 博客](https://zeabur.com/blogs/use-mcp-tools-with-n8n)
- **视频教程**: [Setting Up MCP Nodes in n8n](https://www.youtube.com/watch?v=dRlOOiGOcMM)

---

**这就是通过 n8n 原生 MCP Client Tool 快速集成的方式！** 🚀

## 🔧 服务状态检查

```bash
# 检查所有服务状态
echo "=== 服务状态检查 ==="
echo "Python API: $(curl -s http://localhost:19001/ | jq -r '.message')"
echo "MCP Bridge: $(curl -s http://localhost:19003/ | jq -r '.name')"
echo "MCP SSE: $(curl -s http://localhost:19004/ | jq -r '.name')"
echo "n8n: 运行在 http://localhost:5678"
```

所有服务就绪后，在 n8n 中创建 workflow 即可！
