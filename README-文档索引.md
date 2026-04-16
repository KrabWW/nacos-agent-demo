# n8n 工作流集成文档索引

> **AI 研发效能平台 - n8n 集成完整文档**
> **更新时间**: 2026-04-16

---

## 📚 核心文档

### 1. [技术架构与问题分析.md](./技术架构与问题分析.md)
**完整的技术架构文档**
- 问题总结与解决方案
- 系统架构图与数据流转
- 依赖组件与程序路径
- 工作流执行流程详解
- 配置要点与最佳实践
- 服务启动指南
- MCP Bridge 价值分析
- 故障排查手册

**适合**: 架构师、技术负责人、运维人员

---

### 2. [对话记录-问题排查与修复.md](./对话记录-问题排查与修复.md)
**实际问题的排查过程记录**
- 问题背景与症状
- 完整排查步骤（5步诊断法）
- 修复方案（代码级别）
- 验证测试结果
- 经验教训总结
- 命令速查表

**适合**: 开发者、运维人员、问题排查

---

### 3. [MCP-Bridge-深度分析.md](./MCP-Bridge-深度分析.md)
**MCP Bridge 技术深度解析**
- 性能测试数据（+25ms，2.6倍）
- 参数简化对比
- AI 友好的能力描述
- 稳定性测试（100%成功率）
- 架构优势分析
- 使用场景对比
- 决策树与最佳实践

**适合**: 架构师、技术决策者、AI 开发者

---

### 4. [服务启动完整指南.md](./服务启动完整指南.md)
**服务部署与运维手册**
- 一键启动脚本使用
- 分步启动详解
- 服务依赖关系图
- 健康检查脚本
- 常见问题与解决
- 停止与清理方法

**适合**: 运维人员、DevOps、开发者

---

## 🎯 快速导航

### 我想要...

**了解系统架构**
→ [技术架构与问题分析.md](./技术架构与问题分析.md) - 第2章

**排查问题**
→ [对话记录-问题排查与修复.md](./对话记录-问题排查与修复.md) - 排查过程

**理解 MCP Bridge**
→ [MCP-Bridge-深度分析.md](./MCP-Bridge-深度分析.md) - 核心结论

**启动服务**
→ [服务启动完整指南.md](./服务启动完整指南.md) - 一键启动

**配置工作流**
→ [技术架构与问题分析.md](./技术架构与问题分析.md) - 配置要点

**性能优化**
→ [MCP-Bridge-深度分析.md](./MCP-Bridge-深度分析.md) - 性能测试

---

## 📊 文档关系图

```
技术架构与问题分析.md (主文档)
    │
    ├─── 对话记录-问题排查与修复.md (实践案例)
    │
    ├─── MCP-Bridge-深度分析.md (技术深度)
    │
    └─── 服务启动完整指南.md (运维手册)
```

---

## 🔑 关键要点总结

### 核心问题

1. **JSON 表达式错误** ✅ 已修复
   - 使用 `JSON.stringify()` 确保有效 JSON
   - 正确引用数据路径

2. **SSRF 保护** ✅ 已修复
   - 配置环境变量允许内网访问
   - 修改 `docker-compose.yml`

### 性能数据

| 指标 | MCP Bridge | 直接 API | 差异 |
|------|-----------|---------|------|
| 平均响应时间 | 34.3ms | 9.5ms | +24.8ms |
| 成功率 | 100% | 100% | - |
| 参数复杂度 | 简单 | 复杂 | - |

### 核心价值

> **MCP Bridge 让后端 API 从"人类可读"进化到"AI 可理解"**

- ✅ 参数简化 5-10 倍
- ✅ AI 原生支持
- ✅ 统一错误处理
- ✅ 自动能力发现

---

## 🚀 快速开始

### 1. 启动服务

```bash
# 一键启动基础设施
cd /mnt/d/code/other/feilun
./deploy-all-in-one.sh

# 启动 n8n
cd /mnt/d/code/docker/n8n
docker-compose up -d
```

### 2. 测试工作流

```bash
curl -X POST "http://localhost:5678/webhook/product-search-demo" \
  -H "Content-Type: application/json" \
  -d '{"productName": "iPhone 16", "quantity": 1}'
```

### 3. 验证结果

```bash
# 预期返回
{
  "success": true,
  "tool": "create_order",
  "result": {
    "order_id": 24,
    "status": "已创建"
  }
}
```

---

## 📖 推荐阅读顺序

### 新手入门
1. 服务启动完整指南.md → 启动服务
2. 对话记录-问题排查与修复.md → 理解问题
3. 技术架构与问题分析.md → 掌握架构

### 深入学习
1. 技术架构与问题分析.md → 系统理解
2. MCP-Bridge-深度分析.md → 技术深度
3. 对话记录-问题排查与修复.md → 实践经验

### 问题排查
1. 对话记录-问题排查与修复.md → 排查方法
2. 服务启动完整指南.md → 健康检查
3. 技术架构与问题分析.md → 故障排查

---

## 🛠️ 实用脚本

### 健康检查

```bash
# 检查所有服务
curl -s http://localhost:5678/          # n8n
curl -s http://localhost:8081/healthz   # 后端
curl -s http://localhost:8848/nacos     # Nacos
curl -s http://localhost:8082/          # Higress
curl -s http://172.28.156.225:19002/health # MCP Bridge
```

### 测试工作流

```bash
# 基本测试
curl -X POST "http://localhost:5678/webhook/product-search-demo" \
  -H "Content-Type: application/json" \
  -d '{"productName": "iPhone", "quantity": 1}'

# 稳定性测试
for i in {1..10}; do
  curl -X POST "http://localhost:5678/webhook/product-search-demo" \
    -H "Content-Type: application/json" \
    -d "{\"productName\": \"Test-$i\", \"quantity\": $i}"
done
```

---

## 📞 获取帮助

### 文档问题
- 查看相关章节
- 检查故障排查手册
- 查看错误日志

### 技术支持
- 查看项目 README.md
- 提交 Issue
- 联系维护团队

---

## 📝 文档维护

### 更新记录
- **2026-04-16**: 创建完整文档体系
- **问题修复**: JSON 表达式、SSRF 保护
- **性能测试**: MCP Bridge vs 直接 API
- **稳定性测试**: 100% 成功率验证

### 贡献指南
欢迎补充和完善文档：
1. 保持文档结构清晰
2. 包含实际案例和数据
3. 更新日期和版本信息
4. 保持语言简洁准确

---

**文档维护**: AI 研发效能平台团队
**最后更新**: 2026-04-16
**文档版本**: v1.0.0
**适用项目**: nacos-agent-demo
