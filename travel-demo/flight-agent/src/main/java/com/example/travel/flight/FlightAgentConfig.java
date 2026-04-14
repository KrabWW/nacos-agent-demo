package com.example.travel.flight;

import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.exception.GraphStateException;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class FlightAgentConfig {

    @Bean
    @Primary
    public BaseAgent flightAgent(ChatModel chatModel) throws GraphStateException {
        return ReactAgent.builder()
                .name("travel-flight-agent")
                .description("查询航班信息，提供机票和出行建议")
                .model(chatModel)
                .instruction("你是一个机票查询助手。根据用户提供的出发地、目的地和日期，推荐合适的航班。"
                        + "用中文回答，给出航班号、大致价格、出发时间和推荐理由。")
                .build();
    }
}
