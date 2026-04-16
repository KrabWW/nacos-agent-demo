# 🎯 你的 Workflow Webhook 信息

## ✅ 已添加 Webhook 支持！

### 📋 基本信息

**Workflow**: MCP 集成演示 - 商品搜索与订单 (Webhook)
**ID**: `eOPjpVDChTp8Eft5`

**Webhook URL**:
- **Production**: `http://localhost:5678/webhook/product-search-demo`
- **Test**: `http://localhost:5678/webhook/test-product-search-demo`

**HTTP Method**: POST

---

## 🚀 调用方式

### 方式 1: Test Webhook（无需激活 workflow）

```bash
curl -X POST 'http://localhost:5678/webhook/test-product-search-demo' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```

### 方式 2: Production Webhook（需要先激活 workflow）

**步骤 1: 激活 workflow**
```
1. 访问: http://localhost:5678/workflow/eOPjpVDChTp8Eft5
2. 点击右上角的 "Active" 开关
3. 等待激活完成
```

**步骤 2: 调用 production webhook**
```bash
curl -X POST 'http://localhost:5678/webhook/product-search-demo' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```

---

## 🧪 立即测试（使用 Test Webhook）

```bash
curl -X POST 'http://localhost:5678/webhook/test-product-search-demo' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```

**预期结果**:
```json
{
  "success": true,
  "search_result": {
    "total": 2,
    "items": [
      {"id": 1, "name": "iPhone 16", "price": 6999}
    ]
  },
  "order_created": {
    "order_id": 10,
    "total": 6999
  }
}
```

---

## 📊 三种调用方式对比

| 方式 | URL | 需要激活 | 适合场景 |
|------|-----|---------|---------|
| **Test Webhook** | `/webhook/test-product-search-demo` | ❌ | 测试、开发 |
| **Production Webhook** | `/webhook/product-search-demo` | ✅ | 生产环境 |
| **MCP 工具** | `http://localhost:19005/tools/...` | ❌ | AI 调用 |

---

## 🎯 快速开始

### 1. 测试 workflow（推荐）
```bash
curl -X POST 'http://localhost:5678/webhook/test-product-search-demo' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```

### 2. 查看执行结果
```
1. 访问: http://localhost:5678/workflow/eOPjpVDChTp8Eft5
2. 点击左侧 "Executions"
3. 查看最新的执行记录
```

### 3. 激活 production webhook（可选）
```
在 n8n UI 中点击 "Active" 开关
```

---

## 💡 从其他系统调用

### Python 示例
```python
import requests

response = requests.post(
    'http://localhost:5678/webhook/test-product-search-demo',
    json={'keyword': 'iPhone'}
)

result = response.json()
print(f"订单创建成功: {result['order_created']['order_id']}")
```

### JavaScript 示例
```javascript
fetch('http://localhost:5678/webhook/test-product-search-demo', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({keyword: 'iPhone'})
})
.then(res => res.json())
.then(data => console.log(data));
```

### curl 示例
```bash
curl -X POST \
  'http://localhost:5678/webhook/test-product-search-demo' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```

---

## 🎉 总结

**✅ 已完成**:
- Webhook 已添加到 workflow
- Test webhook 可立即使用
- Production webhook 需要激活

**🎯 推荐使用**:
- Test Webhook: `http://localhost:5678/webhook/test-product-search-demo`
- 最简单，无需激活

**🧪 立即测试**:
```bash
curl -X POST 'http://localhost:5678/webhook/test-product-search-demo' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```
