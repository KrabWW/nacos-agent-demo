package com.example.travel.weather;

import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.exception.GraphStateException;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;

@Configuration
@Import(MiniMaxChatModelConfig.class)
public class WeatherAgentConfig {

    @Bean
    public BaseAgent weatherAgent(ChatModel chatModel) throws GraphStateException {
        return ReactAgent.builder()
                .name("travel-weather-agent")
                .description("查询城市天气信息，提供出行天气建议")
                .model(chatModel)
                .instruction("你是一个天气查询助手。根据用户提供的城市和日期，给出天气情况的建议。"
                        + "用中文回答，简洁明了。如果没有真实天气数据，请根据季节和城市特点给出合理推测。")
                .build();
    }
}
