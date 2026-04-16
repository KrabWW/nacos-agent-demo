#!/usr/bin/env python3
"""
模拟 n8n Workflow 的完整执行
验证从 OpenAPI → MCP → n8n 的完整链路
"""

import json
import requests
import sys

MCP_BRIDGE_URL = "http://localhost:19003"

class WorkflowExecution:
    """模拟 n8n Workflow 执行"""

    def __init__(self):
        self.context = {}
        self.execution_log = []

    def log(self, node_name, message, data=None):
        """记录执行日志"""
        log_entry = {
            "node": node_name,
            "message": message,
            "data": data
        }
        self.execution_log.append(log_entry)
        print(f"📍 [{node_name}] {message}")
        if data:
            print(f"   数据: {json.dumps(data, ensure_ascii=False, indent=2)}")

    def node_1_manual_trigger(self):
        """节点 1: 手动触发"""
        self.log("Manual Trigger", "Workflow 开始执行")
        return {"triggered": True, "timestamp": "2025-04-14T14:45:00"}

    def node_2_search_products(self):
        """节点 2: 搜索商品 (MCP)"""
        self.log("搜索商品 (MCP)", "调用 MCP 工具搜索商品")

        try:
            response = requests.post(
                f"{MCP_BRIDGE_URL}/tools/search_products_api_products_get",
                json={"keyword": "iPhone"}
            )
            response.raise_for_status()
            data = response.json()

            self.log("搜索商品 (MCP)", "✅ 搜索成功", data)

            # 模拟 n8n 的数据传递
            self.context["search_result"] = data
            return data

        except Exception as e:
            self.log("搜索商品 (MCP)", f"❌ 搜索失败: {e}")
            raise

    def node_3_extract_product_info(self, search_result):
        """节点 3: 提取商品信息"""
        self.log("提取商品信息", "从搜索结果中提取第一个商品")

        if not search_result.get("success"):
            raise ValueError("搜索失败，无法提取商品信息")

        items = search_result.get("result", {}).get("items", [])
        if not items:
            raise ValueError("没有找到商品")

        first_product = items[0]

        extracted_data = {
            "product_id": first_product["id"],
            "product_name": first_product["name"],
            "price": first_product["price"],
            "quantity": 2,
            "address": "北京市朝阳区"
        }

        self.log("提取商品信息", "✅ 提取成功", extracted_data)

        self.context["product"] = extracted_data
        return extracted_data

    def node_4_create_order(self, product_data):
        """节点 4: 创建订单 (MCP)"""
        self.log("创建订单 (MCP)", "调用 MCP 工具创建订单")

        try:
            order_request = {
                "product_id": product_data["product_id"],
                "quantity": product_data["quantity"],
                "address": product_data["address"]
            }

            response = requests.post(
                f"{MCP_BRIDGE_URL}/tools/create_order_api_order_create_post",
                json=order_request
            )
            response.raise_for_status()
            data = response.json()

            self.log("创建订单 (MCP)", "✅ 订单创建成功", data)

            self.context["order"] = data
            return data

        except Exception as e:
            self.log("创建订单 (MCP)", f"❌ 创建失败: {e}")
            raise

    def node_5_format_output(self, order_result):
        """节点 5: 格式化输出"""
        self.log("格式化输出", "格式化最终输出")

        if not order_result.get("success"):
            raise ValueError("订单创建失败")

        result = order_result.get("result", {})

        formatted_output = {
            "message": "🎉 Workflow 执行成功！",
            "workflow": "MCP 集成演示 - 商品搜索与订单创建",
            "result": {
                "商品": result.get("product_name"),
                "订单号": result.get("order_id"),
                "总价": f"¥{result.get('total_price')}",
                "状态": result.get("status"),
                "收货地址": result.get("address")
            },
            "execution_path": "OpenAPI → MCP Tools → n8n Workflow → Success"
        }

        self.log("格式化输出", "✅ 输出格式化完成", formatted_output)
        return formatted_output

    def execute_workflow(self):
        """执行完整的 workflow"""
        print("=" * 70)
        print("🚀 n8n Workflow 执行模拟")
        print("📋 Workflow: MCP 集成演示 - 商品搜索与订单创建")
        print("=" * 70)
        print()

        try:
            # 节点 1: 手动触发
            print("▶️  节点 1: Manual Trigger")
            trigger_data = self.node_1_manual_trigger()
            print()

            # 节点 2: 搜索商品
            print("▶️  节点 2: 搜索商品 (MCP)")
            search_result = self.node_2_search_products()
            print()

            # 节点 3: 提取商品信息
            print("▶️  节点 3: 提取商品信息")
            product_data = self.node_3_extract_product_info(search_result)
            print()

            # 节点 4: 创建订单
            print("▶️  节点 4: 创建订单 (MCP)")
            order_result = self.node_4_create_order(product_data)
            print()

            # 节点 5: 格式化输出
            print("▶️  节点 5: 格式化输出")
            final_output = self.node_5_format_output(order_result)
            print()

            # 执行总结
            print("=" * 70)
            print("✅ Workflow 执行成功！")
            print("=" * 70)
            print(json.dumps(final_output, ensure_ascii=False, indent=2))
            print()
            print("📊 执行统计:")
            print(f"   - 执行节点数: {len(self.execution_log)}")
            print(f"   - 执行状态: 成功")
            print(f"   - 数据流向: OpenAPI → MCP → n8n → 完成")
            print("=" * 70)

            return final_output

        except Exception as e:
            print()
            print("=" * 70)
            print(f"❌ Workflow 执行失败: {e}")
            print("=" * 70)
            print("📋 执行日志:")
            for log in self.execution_log:
                print(f"   [{log['node']}] {log['message']}")
            print("=" * 70)
            sys.exit(1)


def main():
    """主函数"""
    print("🔍 检查 MCP Bridge 服务状态...")
    try:
        response = requests.get(f"{MCP_BRIDGE_URL}/health", timeout=2)
        health_data = response.json()
        print(f"✅ MCP Bridge 状态: {health_data.get('status', 'unknown')}")
        print()
    except Exception as e:
        print(f"❌ MCP Bridge 不可用: {e}")
        print("💡 请先启动 MCP Bridge: python3 mcp-bridge-from-openapi.py")
        sys.exit(1)

    # 创建并执行 workflow
    workflow = WorkflowExecution()
    result = workflow.execute_workflow()

    # 保存执行结果
    with open("workflow-execution-result.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print()
    print("💾 执行结果已保存到: workflow-execution-result.json")


if __name__ == "__main__":
    main()
