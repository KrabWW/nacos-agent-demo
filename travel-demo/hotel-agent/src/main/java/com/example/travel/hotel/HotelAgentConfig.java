package com.example.travel.hotel;

import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import com.alibaba.cloud.ai.graph.agent.ReactAgent;
import com.alibaba.cloud.ai.graph.exception.GraphStateException;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class HotelAgentConfig {

    @Bean
    @Primary
    public BaseAgent hotelAgent(ChatModel chatModel) throws GraphStateException {
        return ReactAgent.builder()
                .name("travel-hotel-agent")
                .description("查询和推荐酒店，提供住宿建议")
                .model(chatModel)
                .instruction("你是一个酒店预订助手。根据用户提供的城市、日期和预算，推荐合适的酒店。"
                        + "用中文回答，给出酒店名称、价格区间、位置优势和推荐理由。")
                .build();
    }
}
