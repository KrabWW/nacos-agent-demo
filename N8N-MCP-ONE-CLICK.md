# 🚀 n8n Workflows → MCP Tools 一键暴露方案

## ✅ 是的！n8n workflows 可以被当做 MCP 工具！

### 方案对比

| 方案 | 优势 | 劣势 | 推荐度 |
|------|------|------|--------|
| **自定义 Python MCP Server** | 完全控制，自动发现所有 workflows | 需要自己维护 | ⭐⭐⭐⭐⭐ |
| **n8n-mcp (npm)** | 官方支持，功能强大 | 需要配置，主要在 Claude Desktop 中使用 | ⭐⭐⭐⭐ |
| **n8n-mcp-server** | GitHub 开源项目 | 需要部署 | ⭐⭐⭐ |

---

## 🎯 方案 1: 自定义 Python MCP Server（已实现）✅

### 已启动服务
- **服务**: n8n MCP Server
- **端口**: 19005
- **状态**: ✅ 运行中
- **自动发现**: 2 个 workflows

### 已暴露的 MCP 工具

#### 1. n8n_workflow_mcp_集成演示___商品搜索与订单
```
描述: 执行 n8n workflow: MCP 集成演示 - 商品搜索与订单 (支持手动触发)
Workflow ID: eOPjpVDChTp8Eft5
```

#### 2. n8n_workflow_webhook___parallel_fetch_&_merge
```
描述: 执行 n8n workflow: Webhook - Parallel Fetch & Merge (支持 Webhook 触发)
Workflow ID: 0TXoxoX8g28tZ0WG
```

### 使用方式

#### 方式 1: HTTP API 调用
```bash
# 列出所有工具
curl http://localhost:19005/tools | jq .

# 调用 workflow 工具
curl -X POST 'http://localhost:19005/tools/n8n_workflow_mcp_集成演示___商品搜索与订单' \
  -H 'Content-Type: application/json' \
  -d '{"input_data": {"test": true}}' | jq .
```

#### 方式 2: 在 Claude Desktop 中配置
```json
{
  "mcpServers": {
    "n8n-workflows": {
      "command": "python3",
      "args": ["/mnt/d/code/other/nacos-agent-demo/n8n-to-mcp-server.py", "19005"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### 方式 3: 作为 SSE MCP Server
可以轻松改造为 SSE MCP Server，让 n8n workflows 作为标准 MCP 工具使用。

---

## 🔧 方案 2: 使用现有 npm 包

### n8n-mcp
```bash
# 安装
npm install -g @czlonkowski/n8n-mcp

# 启动
npx -y @czlonkowski/n8n-mcp@latest
```

**功能**:
- ✅ 搜索 n8n 节点
- ✅ 验证 workflow 配置
- ✅ 创建/更新 workflows
- ✅ 测试 workflows

### @path58/p58-n8n
```bash
# 安装
npm install -g @path58/p58-n8n

# 更智能的 n8n MCP server
p58-n8n
```

**功能**:
- ✅ 自动修复 workflows
- ✅ 发现 workflows
- ✅ 验证 workflows

---

## 🚀 方案 3: GitHub 开源项目

### leonardsellem/n8n-mcp-server
```bash
git clone https://github.com/leonardsellem/n8n-mcp-server.git
cd n8n-mcp-server
npm install
npm start
```

**链接**: [n8n-mcp-server GitHub](https://github.com/leonardsellem/n8n-mcp-server)

---

## 🎯 一键启动脚本

创建 `start-n8n-mcp.sh`:
```bash
#!/bin/bash

echo "🚀 启动 n8n Workflows → MCP Server"

# 检查依赖
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装 Python 3"
    exit 1
fi

# 启动服务器
python3 n8n-to-mcp-server.py 19005

echo "✅ n8n MCP Server 已启动"
echo "📍 端口: 19005"
echo "🌐 访问: http://localhost:19005"
```

使用:
```bash
chmod +x start-n8n-mcp.sh
./start-n8n-mcp.sh
```

---

## 📊 完整的集成架构

```
┌─────────────────────────────────────────┐
│  AI Assistant (Claude, Cursor, etc.)    │
│                                          │
│  通过 MCP 协议访问工具                   │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  MCP Server (19005)                      │
│                                          │
│  自动发现 n8n workflows                  │
│  暴露为 MCP 工具                         │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│  n8n API (localhost:5678)               │
│                                          │
│  管理 workflows                          │
│  执行自动化任务                          │
└─────────────────────────────────────────┘
```

---

## 🎯 核心优势

### ✅ 完全自动化
- 自动发现所有 n8n workflows
- 自动生成 MCP 工具定义
- 无需手工配置

### ✅ 双向集成
- AI 可以调用 n8n workflows
- n8n 可以调用 MCP servers

### ✅ 标准化
- 使用 MCP 标准协议
- 支持所有 MCP 客户端

### ✅ 可扩展
- 支持任意数量的 workflows
- 动态添加新 workflows

---

## 🧪 测试命令

```bash
# 1. 检查服务状态
curl http://localhost:19005/ | jq .

# 2. 列出所有工具
curl http://localhost:19005/tools | jq .

# 3. 调用 workflow
curl -X POST 'http://localhost:19005/tools/n8n_workflow_mcp_集成演示___商品搜索与订单' \
  -H 'Content-Type: application/json' \
  -d '{}' | jq .

# 4. 刷新 workflows（添加新 workflow 后）
curl -X POST http://localhost:19005/refresh | jq .
```

---

## 📚 相关资源

### 现有项目
- [n8n-mcp npm 包](https://npm.im/n8n-mcp)
- [n8n-mcp-server GitHub](https://github.com/leonardsellem/n8n-mcp-server)
- [n8n MCP Guide](https://www.leanware.co/insights/n8n-mcp-guide)
- [MCP Market - n8n](https://mcpmarket.com/server/n8n-mcp-client-1)

### 社区讨论
- [n8n Community - MCP](https://community.n8n.io/t/provide-and-use-model-context-protocol/63799)
- [MCP vs n8n 讨论](https://community.n8n.io/t/are-mcp-servers-alternatives-to-n8n/138615)

---

## 🎉 总结

**是的！n8n workflows 可以被当做 MCP 工具！**

✅ **已实现**: 自定义 Python MCP Server
✅ **已启动**: 端口 19005
✅ **已暴露**: 2 个 n8n workflows 作为 MCP 工具
✅ **一键启动**: `python3 n8n-to-mcp-server.py 19005`

**下一步**:
1. 在 Claude Desktop 中配置这个 MCP server
2. 让 AI 直接调用你的 n8n workflows
3. 实现真正的 AI + n8n 自动化集成！🚀
