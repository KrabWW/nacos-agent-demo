package com.example.travel.planner;

import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.agent.a2a.A2aRemoteAgent;
import com.alibaba.cloud.ai.graph.agent.a2a.AgentCardProvider;
import com.alibaba.cloud.ai.graph.exception.GraphStateException;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class RemoteAgentsConfig {

    /**
     * Planner 自身的 Agent（作为 A2A Server 暴露）
     * 必须标记 @Primary，让 A2A Server 自动配置使用它创建 AgentCard
     */
    @Bean
    @Primary
    public BaseAgent plannerAgent(ChatModel chatModel) throws GraphStateException {
        return ReactAgent.builder()
                .name("travel-planner-agent")
                .description("旅行规划编排者，协调天气、酒店、机票 Agent")
                .model(chatModel)
                .instruction("你是一个旅行规划助手，负责协调天气、酒店、机票三个专业 Agent。用中文回答。")
                .build();
    }

    /** 远程天气 Agent（从 Nacos 发现） */
    @Bean
    public BaseAgent weatherAgent(AgentCardProvider provider) throws GraphStateException {
        return A2aRemoteAgent.builder()
                .agentCardProvider(provider)
                .name("travel-weather-agent")
                .description("远程天气查询Agent")
                .build();
    }

    /** 远程酒店 Agent（从 Nacos 发现） */
    @Bean
    public BaseAgent hotelAgent(AgentCardProvider provider) throws GraphStateException {
        return A2aRemoteAgent.builder()
                .agentCardProvider(provider)
                .name("travel-hotel-agent")
                .description("远程酒店推荐Agent")
                .build();
    }

    /** 远程机票 Agent（从 Nacos 发现） */
    @Bean
    public BaseAgent flightAgent(AgentCardProvider provider) throws GraphStateException {
        return A2aRemoteAgent.builder()
                .agentCardProvider(provider)
                .name("travel-flight-agent")
                .description("远程机票查询Agent")
                .build();
    }
}
