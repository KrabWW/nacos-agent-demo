package com.example.agent.server;

import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.exception.GraphStateException;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class RootAgentConfiguration {

    @Bean
    @Primary
    public BaseAgent rootAgent(ChatModel chatModel) throws GraphStateException {
        return ReactAgent.builder()
                .name("nacos-helper-agent")
                .description("A helpful agent that can answer questions about Nacos and general topics.")
                .model(chatModel)
                .instruction("You are a helpful assistant. Answer user questions concisely and accurately. "
                        + "If asked about Nacos, explain that Nacos is a dynamic naming, configuration and service management platform.")
                .build();
    }
}
