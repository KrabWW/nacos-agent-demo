# 🔧 Docker 网络问题修复指南

## 问题描述

在 n8n 容器中执行 workflow 时遇到错误：
```
Problem in node '搜索商品 (MCP)'
The service refused the connection - perhaps it is offline
```

## 根本原因

**Docker 网络隔离问题**：
- n8n 运行在 Docker 容器中
- MCP Bridge 运行在 WSL 宿主机上（端口 19002）
- 容器内的 `localhost` 指向容器本身，不是宿主机
- 因此 n8n 容器无法访问 `localhost:19002`

## 解决方案

### 方案 1: 使用宿主机 IP（推荐）✅

**步骤**：

1. **获取 WSL 宿主机 IP**
```bash
hostname -I | awk '{print $1}'
# 输出示例: 172.28.156.225
```

2. **更新 workflow 中的 URL**
```python
# 从: http://localhost:19002/tools/search_products
# 到: http://172.28.156.225:19002/tools/search_products
```

3. **通过 n8n API 更新 workflow**
```bash
python3 /tmp/fix_workflow_urls.py
```

**已修复的 workflow**:
- 搜索商品: `http://172.28.156.225:19002/tools/search_products`
- 创建订单: `http://172.28.156.225:19002/tools/create_order`

### 方案 2: 使用 Docker host 网络模式

修改 `docker-compose.yml`:
```yaml
services:
  n8n:
    network_mode: "host"  # 使用宿主机网络
```

**注意**: 这会移除网络隔离，容器直接使用宿主机网络。

### 方案 3: 添加 host.docker.internal（Docker Desktop）

如果在 Docker Desktop for Windows/Mac 中：
```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

然后在 workflow 中使用:
```
http://host.docker.internal:19002
```

## 验证修复

### 1. 从 n8n 容器内测试连接
```bash
docker exec n8n wget -qO- http://172.28.156.225:19002/tools
```

### 2. 在 n8n UI 中测试 workflow
1. 访问: http://localhost:5678/workflow/eOPjpVDChTp8Eft5
2. 点击 "Test workflow"
3. 点击 "Manual Trigger" 执行
4. 查看节点输出

### 3. 直接测试 MCP 接口
```bash
curl -X POST 'http://172.28.156.225:19002/tools/search_products' \
  -H 'Content-Type: application/json' \
  -d '{"keyword": "iPhone"}'
```

## 自动化修复脚本

创建 `/tmp/fix_workflow_urls.py`:
```python
import requests

HOST_IP = "172.28.156.225"  # WSL 宿主机 IP
N8N_API_KEY = "your-api-key"
WORKFLOW_ID = "workflow-id"

headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

# 获取 workflow
response = requests.get(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    headers=headers
)
workflow = response.json()

# 替换 URL
for node in workflow['nodes']:
    if 'parameters' in node and 'url' in node['parameters']:
        node['parameters']['url'] = node['parameters']['url'].replace(
            'localhost:19002',
            f'{HOST_IP}:19002'
        )

# 更新 workflow
update_data = {
    "name": workflow['name'],
    "nodes": workflow['nodes'],
    "connections": workflow['connections'],
    "settings": workflow.get('settings', {})
}

requests.put(
    f"http://localhost:5678/api/v1/workflows/{WORKFLOW_ID}",
    json=update_data,
    headers=headers
)
```

运行:
```bash
python3 /tmp/fix_workflow_urls.py
```

## 网络架构

```
┌─────────────────────────────────────────┐
│  WSL2 宿主机 (172.28.156.225)            │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ MCP Bridge (19002)               │   │
│  │ - search_products                │   │
│  │ - create_order                   │   │
│  └──────────────────────────────────┘   │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │ Docker 容器                      │   │
│  │                                  │   │
│  │  ┌────────────────────────────┐ │   │
│  │  │ n8n (端口 5678)            │ │   │
│  │  │                           │ │   │
│  │  │ Workflow 访问:             │ │   │
│  │  │ http://172.28.156.225:19002│ │   │
│  │  └────────────────────────────┘ │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 常用 IP 地址查询命令

```bash
# WSL 宿主机 IP
hostname -I | awk '{print $1}'

# Docker bridge 网关
ip route | grep docker0 | awk '{print $9}'

# 从容器内访问宿主机
docker exec n8n wget -qO- http://172.28.156.225:19002/tools
```

## 总结

✅ **已修复**: Workflow 现在使用宿主机 IP (172.28.156.225)
✅ **可以测试**: n8n 容器能够正常访问 MCP Bridge
✅ **自动化**: 提供了自动修复脚本

**下一步**: 在 n8n UI 中执行 workflow 测试！🚀
