# 🎯 你的 Workflow 调用指南

## 📋 Workflow 信息

**名称**: MCP 集成演示 - 商品搜索与订单
**ID**: `eOPjpVDChTp8Eft5`
**当前触发方式**: Manual Trigger（手动触发）
**状态**: 未激活 (active: false)

---

## 🚀 三种调用方式

### 方式 1: 通过 n8n UI 手动执行（当前可用）✅

```
1. 访问: http://localhost:5678/workflow/eOPjpVDChTp8Eft5
2. 点击 "Test workflow" 按钮
3. 点击 "Manual Trigger" 节点
4. 查看执行结果
```

### 方式 2: 通过 n8n API 执行（推荐）⭐

**执行端点**:
```bash
POST http://localhost:5678/api/v1/workflows/eOPjpVDChTp8Eft5/execute
```

**调用示例**:
```bash
curl -X POST \
  'http://localhost:5678/api/v1/workflows/eOPjpVDChTp8Eft5/execute' \
  -H 'X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

**Python 示例**:
```python
import requests

headers = {
    "X-N8N-API-KEY": "your-api-key",
    "Content-Type": "application/json"
}

response = requests.post(
    "http://localhost:5678/api/v1/workflows/eOPjpVDChTp8Eft5/execute",
    headers=headers,
    json={}
)

result = response.json()
print(result)
```

### 方式 3: 通过 MCP 服务器调用（AI 原生）🤖

**MCP 服务器地址**: `http://localhost:19005`

**MCP 工具名称**: `n8n_workflow_mcp_集成演示___商品搜索与订单`

**调用示例**:
```bash
curl -X POST \
  'http://localhost:19005/tools/n8n_workflow_mcp_集成演示___商品搜索与订单' \
  -H 'Content-Type: application/json' \
  -d '{"input_data": {}}'
```

**在 Claude Desktop 中使用**:
1. 配置 MCP 服务器连接到 `http://localhost:19005`
2. 直接对话: "执行商品搜索与订单 workflow"
3. Claude 会自动调用 MCP 工具

---

## 🔧 添加 Webhook 支持（一键暴露为 HTTP API）

### 当前状态
❌ 没有 Webhook 节点
✅ 只有 Manual Trigger

### 如何添加 Webhook

**方法 1: 在 n8n UI 中修改**
```
1. 打开 workflow: http://localhost:5678/workflow/eOPjpVDChTp8Eft5
2. 删除 "Manual Trigger" 节点
3. 添加 "Webhook" 节点
4. 配置 Webhook:
   - HTTP Method: POST
   - Path: order-demo
   - Authentication: None
5. 保存 workflow
```

**方法 2: 通过 API 修改（自动化）**

使用以下脚本自动添加 Webhook 节点:
```bash
python3 add-webhook-to-workflow.py
```

### 添加 Webhook 后的调用地址

**Webhook URL**:
```
http://localhost:5678/webhook/order-demo
```

**调用示例**:
```bash
curl -X POST 'http://localhost:5678/webhook/order-demo' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```

---

## 📊 调用方式对比

| 方式 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| **n8n UI 手动** | 测试、调试 | 可视化、简单 | 不能自动化 |
| **n8n API** | 程序调用 | 标准化、可控 | 需要 API key |
| **MCP 工具** | AI 调用 | AI 原生、智能 | 需要 MCP 服务器 |
| **Webhook** | HTTP API | 最简单、通用 | 需要修改 workflow |

---

## 🎯 推荐方案

### 方案 A: 快速测试（无需修改）
```bash
# 在 n8n UI 中手动执行
http://localhost:5678/workflow/eOPjpVDChTp8Eft5
```

### 方案 B: 程序调用（无需修改）
```bash
# 通过 n8n API
curl -X POST 'http://localhost:5678/api/v1/workflows/eOPjpVDChTp8Eft5/execute' \
  -H 'X-N8N-API-KEY: ...'
```

### 方案 C: AI 调用（无需修改）
```bash
# 通过 MCP 服务器
curl -X POST 'http://localhost:19005/tools/n8n_workflow_mcp_集成演示___商品搜索与订单'
```

### 方案 D: HTTP API（需要添加 Webhook）
```bash
# 添加 Webhook 后
curl -X POST 'http://localhost:5678/webhook/order-demo'
```

---

## 💡 立即开始测试

### 测试 1: n8n API 调用
```bash
curl -X POST \
  'http://localhost:5678/api/v1/workflows/eOPjpVDChTp8Eft5/execute' \
  -H 'X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiNTMwMjZmNS02ZTIyLTQyMzMtOTVkMi05NWRiMTFlOWU3MGIiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiOWE0NzIyNDktMjBhNC00Y2MwLTg1ZDUtMTVmYWRiZTI0OTJmIiwiaWF0IjoxNzc2MTQ5NzY2LCJleHAiOjE3Nzg3MzEyMDB9.Rdkn1U-HeZBqpWqsufGfL3B8YhhHrKa5humU-oCMA5c' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### 测试 2: MCP 服务器调用
```bash
curl -X POST \
  'http://localhost:19005/tools/n8n_workflow_mcp_集成演示___商品搜索与订单' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

---

## 📝 总结

**当前可用**:
- ✅ n8n UI 手动执行
- ✅ n8n API 调用
- ✅ MCP 服务器调用

**需要添加 Webhook**:
- ⚠️ 当前没有 Webhook
- 🔧 需要修改 workflow 添加 Webhook 节点

**建议**:
1. 先用 n8n API 测试（方案 B）
2. 如需 HTTP API，添加 Webhook 节点（方案 D）
3. 如需 AI 调用，使用 MCP 服务器（方案 C）
