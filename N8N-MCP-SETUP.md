# 使用 n8n-mcp 自动创建 Workflow

## 📋 在 Claude Desktop 中配置 n8n-mcp

### 步骤 1: 打开 Claude Desktop 配置

**macOS**:
```bash
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**:
```bash
notepad %APPDATA%\Claude\claude_desktop_config.json
```

### 步骤 2: 添加 n8n-mcp 配置

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["-y", "@czlonkowski/n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": ""
      }
    }
  }
}
```

### 步骤 3: 重启 Claude Desktop

完全退出并重启 Claude Desktop

### 步骤 4: 在 Claude 中使用 n8n-mcp 创建 Workflow

在 Claude Desktop 中输入以下提示词：

```
我需要在本地 n8n (http://localhost:5678) 中创建一个 workflow：

需求：商品搜索与订单创建

工作流步骤：
1. Manual Trigger 节点
2. HTTP Request 节点（调用 http://localhost:19002/tools/search_products）
3. Set 节点（提取 product_id, product_name, quantity, address）
4. HTTP Request 节点（调用 http://localhost:19002/tools/create_order）
5. Set 节点（格式化输出）

请使用 n8n-mcp 工具：
1. search_nodes({query: "http request"}) - 搜索 HTTP Request 节点
2. get_node({nodeType: "n8n-nodes-base.httpRequest"}) - 获取节点详情
3. validate_node({nodeType, config}) - 验证节点配置
4. n8n_create_workflow({workflow}) - 创建 workflow

节点配置参考：
- HTTP Request 1: POST http://localhost:19002/tools/search_products
  Body: {"keyword": "iPhone"}

- HTTP Request 2: POST http://localhost:19002/tools/create_order
  Body: {"product_id": {{ $json.product_id }}, "quantity": {{ $json.quantity }}, "address": "{{ $json.address }}"}
```

## 🎯 n8n-mcp 可用工具

### 核心工具
- `search_nodes({query})` - 搜索节点类型
- `get_node({nodeType})` - 获取节点详情
- `validate_node({nodeType, config})` - 验证节点配置
- `search_templates({query})` - 搜索工作流模板

### Workflow 管理（需要 API Key）
- `n8n_create_workflow({workflow})` - 创建工作流
- `n8n_update_partial_workflow({id, operations})` - 更新工作流
- `n8n_test_workflow({id})` - 测试工作流
- `n8n_list_workflows()` - 列出所有工作流

## 💡 提示

1. **n8n-mcp 是一个 MCP 服务器**，需要在 Claude Desktop 中配置使用
2. **不能在 Claude Code CLI 中直接使用** n8n-mcp
3. **n8n API Key**: 如果 n8n 没有设置认证，N8N_API_KEY 留空即可
4. **替代方案**: 可以直接导入 `workflow-mcp-demo.json` 到 n8n

## 📚 参考资源

- n8n-mcp GitHub: https://github.com/czlonkowski/n8n-mcp
- n8n-skills GitHub: https://github.com/czlonkowski/n8n-skills
- n8n 官方文档: https://docs.n8n.io
