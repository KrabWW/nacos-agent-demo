#!/usr/bin/env python3
"""
在 n8n 中创建 API key 的自动化脚本
"""
import subprocess
import json
import time

def create_n8n_api_key():
    print("=" * 70)
    print("🔑 在 n8n 中创建 API Key")
    print("=" * 70)
    print()

    print("📍 方法 1: 通过 n8n Web UI 创建 (推荐)")
    print("-" * 70)
    print("1. 打开浏览器访问: http://localhost:5678")
    print("2. 点击右上角用户头像 → Settings")
    print("3. 点击 'API'")
    print("4. 点击 'Create API Key'")
    print("5. 输入名称（如：mcp-automation）")
    print("6. 复制生成的 API key")
    print()

    print("📍 方法 2: 通过 n8n CLI 创建")
    print("-" * 70)
    print("运行以下命令在 n8n 容器中创建 API key:")
    print()
    print("  docker exec -it n8n n8n user:reset-password [email]")
    print("  # 然后在 UI 中登录并创建 API key")
    print()

    print("📍 方法 3: 绕过 API Key（仅用于演示）")
    print("-" * 70)
    print("如果 n8n 没有启用认证，可以直接使用以下方式:")
    print()
    print("1. 直接导入 workflow JSON")
    print("2. 使用 n8n 内置的 workflow 导入功能")
    print()

    print("=" * 70)
    print("📋 获取 API Key 后的配置步骤")
    print("=" * 70)
    print()
    print("1. 更新 n8n-mcp 配置:")
    print('   export N8N_API_KEY="你的API_KEY"')
    print()
    print("2. 重启 n8n-mcp:")
    print("   pkill -f n8n-mcp")
    print("   npx -y @czlonkowski/n8n-mcp@latest")
    print()
    print("3. 在 Claude Desktop 中配置 n8n-mcp")
    print()

    print("=" * 70)
    print("🚀 临时方案：直接导入 workflow")
    print("=" * 70)
    print()
    print("如果暂时无法获取 API key，可以:")
    print("1. 打开 n8n: http://localhost:5678")
    print("2. 点击右上角 '...' → 'Import from File'")
    print("3. 选择 'workflow-mcp-demo.json'")
    print("4. 立即开始测试！")
    print()

if __name__ == "__main__":
    create_n8n_api_key()
