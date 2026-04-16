# 🔄 n8n + MCP 双向集成完整架构

## ✅ 你的理解完全正确！

### 🎯 三个核心能力

```
1️⃣ AI → n8n-mcp → 创建 n8n workflows
   ✅ AI 通过 n8n-mcp 工具自动创建 workflows

2️⃣ n8n workflows → HTTP API → 其他系统调用
   ✅ 通过 Webhook 或 API 调用 workflows

3️⃣ n8n workflows → MCP tools → AI 调用
   ✅ 将 workflows 暴露为 MCP 工具供 AI 使用
```

---

## 📊 完整的集成架构

```
┌─────────────────────────────────────────────────────────┐
│                   AI 助手                                │
│            (Claude, Cursor, ChatGPT)                    │
│                                                          │
│         📤 创建 workflows    📥 调用 workflows           │
└──────────────┬────────────────────────┬─────────────────┘
               ↓                        ↓
┌──────────────────────────┐  ┌──────────────────────────┐
│  n8n-mcp (创建)          │  │  n8n MCP Server (调用)   │
│  - search_nodes          │  │  - 自动发现 workflows    │
│  - n8n_create_workflow   │  │  - 暴露为 MCP 工具       │
└──────────────┬───────────┘  └──────────────┬───────────┘
               ↓                           ↓
               └───────────┬───────────────┘
                           ↓
               ┌───────────────────────┐
               │      n8n 平台         │
               │   (localhost:5678)    │
               │                       │
               │  📦 Workflows 存储    │
               │  ⚙️ 执行引擎          │
               └───────────┬───────────┘
                           ↓
               ┌───────────────────────┐
               │   三种调用方式         │
               ├───────────────────────┤
               │ 1. MCP 工具调用        │
               │ 2. HTTP API           │
               │ 3. Webhook            │
               └───────────────────────┘
```

---

## 🚀 场景 1: AI 创建 n8n Workflows

### 使用 n8n-mcp 让 AI 自动创建 workflows

**在 Claude Desktop 中配置 n8n-mcp**:
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["-y", "@czlonkowski/n8n-mcp@latest"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

**在 Claude 中让 AI 创建 workflow**:
```
请使用 n8n-mcp 创建一个 workflow：
1. 从 GitHub API 获取用户信息
2. 发送到 Slack 通知
3. 将数据存储到 Google Sheets
```

**AI 会自动调用**:
- `search_nodes({query: "github api"})`
- `search_nodes({query: "slack"})`
- `search_nodes({query: "google sheets"})`
- `n8n_create_workflow({workflow})`

**结果**: ✅ AI 自动在 n8n 中创建了完整的 workflow！

---

## 🚀 场景 2: n8n Workflows 作为 HTTP API

### 方式 1: 通过 n8n Webhook

**创建 Webhook 触发的 workflow**:
```bash
# 在 n8n 中创建 workflow，使用 Webhook 触发
# Webhook URL: http://localhost:5678/webhook/your-webhook-path
```

**其他系统调用**:
```bash
curl -X POST 'http://localhost:5678/webhook/your-webhook-path' \
  -H 'Content-Type: application/json' \
  -d '{"user_id": 123, "action": "process"}'
```

**使用场景**:
- SaaS 系统事件通知
- 第三方服务回调
- 定时任务触发

### 方式 2: 通过 n8n API 执行

**直接通过 API 调用 workflow**:
```python
import requests

headers = {
    "X-N8N-API-KEY": "your-api-key"
}

# 执行 workflow
response = requests.post(
    "http://localhost:5678/api/v1/workflows/{workflow_id}/execute",
    headers=headers,
    json={"data": {"input": "data"}}
)

result = response.json()
```

**使用场景**:
- 内部系统集成
- 微服务架构
- 后台任务处理

---

## 🚀 场景 3: n8n Workflows 作为 MCP Tools

### 使用自定义 MCP Server

**启动 n8n → MCP 转换服务器**:
```bash
python3 n8n-to-mcp-server.py 19005
```

**自动暴露所有 workflows 为 MCP 工具**:
```json
{
  "tools": [
    {
      "name": "n8n_workflow_process_github_events",
      "description": "处理 GitHub 事件并发送 Slack 通知",
      "metadata": {
        "workflow_id": "abc123",
        "has_webhook": true
      }
    }
  ]
}
```

**在 Claude Desktop 中配置**:
```json
{
  "mcpServers": {
    "n8n-workflows": {
      "command": "python3",
      "args": ["/path/to/n8n-to-mcp-server.py", "19005"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

**AI 可以直接调用 workflows**:
```
用户: 处理这个 GitHub push 事件
AI: 调用 n8n_workflow_process_github_events 工具
AI: ✅ 已处理，Slack 通知已发送
```

---

## 🎯 完整的使用流程

### 步骤 1: AI 创建 Workflow

```
开发者: "创建一个监控 CPU 并发送告警的 workflow"
    ↓
Claude + n8n-mcp
    ↓
n8n: 创建 workflow (包含 HTTP Request, Set, Email 节点)
```

### 步骤 2: Workflow 被暴露为 API

```
n8n workflow: "CPU 监控告警"
    ↓
方式 1: Webhook URL → 其他系统调用
方式 2: n8n API → 内部服务调用
方式 3: MCP Tool → AI 调用
```

### 步骤 3: 被其他系统/AI 调用

```
监控服务器 → Webhook → n8n workflow → 发送邮件告警
    或
AI 助手 → MCP Tool → n8n workflow → 处理任务
    或
内部服务 → n8n API → n8n workflow → 执行自动化
```

---

## 🔄 真实场景示例

### 场景: 电商平台订单处理

**1. AI 创建 Workflow**
```
提示: "创建一个订单处理 workflow：
      - 监听新订单
      - 检查库存
      - 创建发货单
      - 发送确认邮件"
```

**2. n8n-mcp 自动创建**
```yaml
nodes:
  - Webhook: 接收订单事件
  - HTTP Request: 检查库存 API
  - Set: 提取订单数据
  - HTTP Request: 创建发货单
  - SendGrid: 发送确认邮件
```

**3. 三种调用方式**

**方式 A: 电商系统调用**
```bash
curl -X POST 'http://localhost:5678/webhook/order-created' \
  -d '{"order_id": 123, "items": [...]}'
```

**方式 B: AI 助手调用**
```
用户: "处理订单 #123"
AI: 调用 n8n_workflow_process_order 工具
AI: "订单已处理，库存已扣减，发货单已创建"
```

**方式 C: 内部服务调用**
```python
orders_api.execute_workflow(
    workflow_id="order-processing",
    data={"order_id": 123}
)
```

---

## 🎁 优势总结

### ✅ 双向集成
- AI 可以创建 workflows
- Workflows 可以被 AI 调用

### ✅ 多种调用方式
- HTTP API (标准 REST)
- Webhook (事件驱动)
- MCP Tool (AI 原生)

### ✅ 低代码 + AI
- 可视化设计 (n8n)
- AI 辅助创建 (n8n-mcp)
- 自动化执行 (任意触发方式)

### ✅ 企业级
- 可扩展
- 可监控
- 可集成

---

## 🚀 立即开始

### 1. 配置 n8n-mcp（AI 创建 workflows）
```bash
# 在 Claude Desktop 中配置
npx -y @czlonkowski/n8n-mcp@latest
```

### 2. 暴露 workflows 为 MCP（AI 调用 workflows）
```bash
# 启动转换服务器
python3 n8n-to-mcp-server.py 19005
```

### 3. 通过 HTTP 调用 workflows（系统调用）
```bash
# 使用 Webhook 或 n8n API
curl http://localhost:5678/webhook/your-webhook
```

---

## 🎉 总结

**是的！你的理解完全正确！**

✅ AI 通过 n8n-mcp 创建 workflows
✅ Workflows 作为 HTTP API 被调用
✅ Workflows 作为 MCP tools 被 AI 调用

**这是一个完整的 AI + 自动化闭环！** 🚀
