# 🚀 使用 n8n-mcp 快速创建 Workflow 指南

## 📚 n8n-mcp 是什么？

**n8n-mcp** 是一个 MCP 服务器，让 AI（如 Claude）能够：
- 理解 n8n 的 1,396 个节点
- 访问 2,709+ workflow 模板
- 构建生产级别的 n8n workflows
- 验证和部署 workflows

## 🎯 快速开始

### 方法 1: 使用 Hosted 服务（推荐 - 最快）

1. **访问**: [dashboard.n8n-mcp.com](https://dashboard.n8n-mcp.com)
2. **免费试用**: 100 tool calls/day
3. **获取 API key**: 注册后获取密钥

### 方法 2: 自托管（完全免费）

```bash
# 使用 npx 快速安装
npx -y @czlonkowski/n8n-mcp@latest

# 或克隆仓库
git clone https://github.com/czlonkowski/n8n-mcp.git
cd n8n-mcp
npm install
npm start
```

## 🔧 配置 n8n MCP Client Tool

### 在 n8n 中配置 MCP 连接

1. **打开 n8n**: http://localhost:5678
2. **添加 MCP Client Tool 节点**
3. **配置参数**:
   ```
   SSE Endpoint: http://localhost:19004/sse
   或者使用 n8n-mcp 的 endpoint:
   SSE Endpoint: http://localhost:3000/sse (如果自托管)
   ```

### 使用 n8n-mcp 创建 workflow

#### 步骤 1: 配置 MCP 连接（如果使用 n8n-mcp）

如果你安装了 n8n-mcp，在 Claude Desktop 中配置：

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["-y", "@czlonkowski/n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### 步骤 2: 在 Claude 中使用 n8n-mcp 工具

**提示词**:
```
使用 n8n-mcp 创建一个 workflow：
1. 搜索商品（使用 MCP 工具）
2. 创建订单（使用 MCP 工具）
3. 使用 Manual Trigger 启动
```

**n8n-mcp 会自动**:
1. 搜索相关节点
2. 验证配置
3. 创建 workflow
4. 部署到 n8n

#### 步骤 3: n8n-mcp 可用的工具

**核心工具**:
- `search_nodes` - 搜索 n8n 节点
- `get_node` - 获取节点详细信息
- `validate_node` - 验证节点配置
- `search_templates` - 搜索 workflow 模板
- `validate_workflow` - 验证 workflow

**n8n 管理工具**:
- `n8n_create_workflow` - 创建 workflow
- `n8n_update_workflow` - 更新 workflow
- `n8n_test_workflow` - 测试 workflow
- `n8n_list_workflows` - 列出 workflows

## 💡 最佳实践

### 使用 n8n-mcp 的正确姿势

1. **先搜索模板**: `search_templates({query: "http api"})`
2. **找到节点**: `search_nodes({query: "http request"})`
3. **验证配置**: `validate_node({nodeType, config})`
4. **创建 workflow**: `n8n_create_workflow(workflow)`
5. **测试执行**: `n8n_test_workflow({id})`

### 常见场景

#### 场景 1: HTTP API 集成
```
1. search_templates({query: "http api integration"})
2. get_template({id})
3. 修改配置
4. n8n_create_workflow
```

#### 场景 2: Webhook 处理
```
1. search_nodes({query: "webhook"})
2. get_node({nodeType: "n8n-nodes-base.webhook"})
3. 构建响应流程
4. validate_workflow
5. n8n_create_workflow
```

#### 场景 3: AI Agent Workflow
```
1. search_templates({searchMode: 'by_task', task: 'ai_agent'})
2. 选择合适的模板
3. 配置 AI 模型
4. 验证 AI 工具配置
5. 部署测试
```

## 🎯 与我们当前演示的结合

### 使用 n8n-mcp 创建 MCP 集成 workflow

**提示词**:
```
使用 n8n-mcp 创建一个 workflow：

需求：
1. 使用 MCP Client Tool 节点
2. SSE Endpoint: http://localhost:19004/sse
3. 调用 search_products_api_products_get 工具
4. 调用 create_order_api_order_create_post 工具
5. 使用 Manual Trigger

步骤：
1. search_nodes({query: "MCP Client Tool"})
2. get_node({nodeType: "n8n-nodes-base.mcpClientTool"})
3. validate_node({config: {...}})
4. n8n_create_workflow({...})
```

**预期结果**:
- n8n-mcp 自动创建 workflow
- 验证所有节点配置
- 部署到 n8n 实例
- 可直接执行

## 📚 参考资源

### 官方资源
- **n8n-mcp GitHub**: [github.com/czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp)
- **n8n-skills GitHub**: [github.com/czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills)
- **Hosted Dashboard**: [dashboard.n8n-mcp.com](https://dashboard.n8n-mcp.com)
- **官方文档**: [docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/](https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/)

### 视频教程
- ["Claude Just Became an n8n Expert"](https://www.youtube.com/watch?v=5CccjiLLyaY)
- ["Connect n8n-mcp to Claude.ai"](https://www.youtube.com/watch?v=qWDN969QBOA)

### Skills 安装
```bash
# Claude Code 插件安装
/plugin install czlonkowski/n8n-skills

# 或手动安装
git clone https://github.com/czlonkowski/n8n-skills.git
cp -r n8n-skills/skills/* ~/.claude/skills/
```

---

**现在你可以使用 n8n-mcp + n8n-skills 让 Claude 自动创建 n8n workflows！** 🚀

Sources:
- [n8n-mcp GitHub](https://github.com/czlonkowski/n8n-mcp)
- [n8n-skills GitHub](https://github.com/czlonkowski/n8n-skills)
- [n8n MCP Documentation](https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/)
- [dashboard.n8n-mcp.com](https://dashboard.n8n-mcp.com)
