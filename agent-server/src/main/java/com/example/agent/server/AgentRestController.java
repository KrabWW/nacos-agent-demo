package com.example.agent.server;

import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import com.alibaba.cloud.ai.graph.exception.GraphRunnerException;
import com.alibaba.cloud.ai.graph.exception.GraphStateException;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class AgentRestController {

    private final BaseAgent rootAgent;

    public AgentRestController(BaseAgent rootAgent) {
        this.rootAgent = rootAgent;
    }

    /**
     * 向 Agent 提问，返回同步文本响应
     * 适合被 Higress MCP Server 包装为 MCP Tool
     */
    @GetMapping("/ask")
    public Map<String, Object> ask(@RequestParam("question") String question)
            throws GraphStateException, GraphRunnerException {
        var result = rootAgent.invoke(Map.of("messages", List.of(new UserMessage(question))));
        String answer = result.map(state -> {
            var data = state.data();
            // 从 state data 中提取最后一条消息作为回答
            Object messages = data.get("messages");
            if (messages instanceof List<?> list && !list.isEmpty()) {
                return list.get(list.size() - 1).toString();
            }
            return data.toString();
        }).orElse("No response from agent");
        return Map.of(
                "question", question,
                "answer", answer,
                "agent", "nacos-helper-agent"
        );
    }

    /**
     * 获取 Nacos 常见问题列表
     */
    @GetMapping("/faq")
    public Map<String, Object> faq(@RequestParam(value = "keyword", required = false) String keyword) {
        var faqs = List.of(
                Map.of("q", "What is Nacos?", "a", "Nacos is a dynamic naming, configuration and service management platform."),
                Map.of("q", "How to deploy Nacos cluster?", "a", "Use Docker Compose or Kubernetes with MySQL as persistent storage."),
                Map.of("q", "What is the difference between Nacos 2.x and 3.x?", "a", "Nacos 3.x adds MCP management, A2A agent registry, and improved AI gateway integration."),
                Map.of("q", "How to integrate Nacos with Spring Cloud?", "a", "Add spring-cloud-starter-alibaba-nacos-discovery and spring-cloud-starter-alibaba-nacos-config dependencies."),
                Map.of("q", "How to convert REST API to MCP Server?", "a", "Use Nacos + Higress AI gateway for zero-code REST-to-MCP conversion via protocol translation.")
        );
        if (keyword != null && !keyword.isBlank()) {
            faqs = faqs.stream()
                    .filter(f -> f.get("q").toString().toLowerCase().contains(keyword.toLowerCase())
                            || f.get("a").toString().toLowerCase().contains(keyword.toLowerCase()))
                    .toList();
        }
        return Map.of("faqs", faqs, "total", faqs.size());
    }

    /**
     * Agent 服务健康检查 & 能力信息
     */
    @GetMapping("/info")
    public Map<String, Object> info() {
        return Map.of(
                "name", "nacos-helper-agent",
                "version", "1.0.0",
                "description", "A helpful agent that answers questions about Nacos",
                "skills", List.of("Nacos FAQ", "General Q&A"),
                "endpoints", List.of(
                        "GET /api/ask?question=xxx  - Ask the agent a question",
                        "GET /faq?keyword=xxx       - Search Nacos FAQ",
                        "GET /info                   - Agent info & health check"
                )
        );
    }
}
