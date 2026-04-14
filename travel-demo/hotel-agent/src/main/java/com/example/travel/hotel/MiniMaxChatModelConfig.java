package com.example.travel.hotel;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.model.Generation;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Custom ChatModel that calls MiniMax's Anthropic-compatible API directly
 * using Java's HttpClient, bypassing Spring AI's Anthropic client which
 * truncates responses containing extended thinking blocks.
 */
@Configuration
public class MiniMaxChatModelConfig {

    @Bean
    @Primary
    ChatModel minimaxChatModel(@Value("${spring.ai.anthropic.api-key}") String apiKey,
                               @Value("${spring.ai.anthropic.base-url}") String baseUrl,
                               @Value("${spring.ai.anthropic.chat.options.model}") String model) {
        String url = baseUrl + "/v1/messages";
        HttpClient httpClient = HttpClient.newHttpClient();
        ObjectMapper objectMapper = new ObjectMapper();

        return new ChatModel() {
            @Override
            public ChatResponse call(Prompt prompt) {
                try {
                    List<Map<String, Object>> messages = new ArrayList<>();
                    for (Message msg : prompt.getInstructions()) {
                        String role = "user";
                        if (msg instanceof SystemMessage) role = "system";
                        else if (msg instanceof AssistantMessage) role = "assistant";
                        Map<String, Object> m = new LinkedHashMap<>();
                        m.put("role", role);
                        m.put("content", msg.getText());
                        messages.add(m);
                    }

                    Map<String, Object> body = new LinkedHashMap<>();
                    body.put("model", model);
                    body.put("max_tokens", 512);
                    body.put("messages", messages);

                    String jsonBody = objectMapper.writeValueAsString(body);

                    HttpRequest request = HttpRequest.newBuilder()
                            .uri(URI.create(url))
                            .header("Content-Type", "application/json")
                            .header("x-api-key", apiKey)
                            .header("anthropic-version", "2023-06-01")
                            .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                            .build();

                    HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
                    String responseBody = response.body();

                    String text = extractText(objectMapper, responseBody);
                    AssistantMessage assistantMessage = new AssistantMessage(text);
                    Generation generation = new Generation(assistantMessage);
                    return new ChatResponse(List.of(generation));
                } catch (Exception e) {
                    throw new RuntimeException("MiniMax ChatModel call failed: " + e.getMessage(), e);
                }
            }

            private String extractText(ObjectMapper mapper, String json) throws Exception {
                JsonNode root = mapper.readTree(json);
                JsonNode content = root.get("content");
                if (content != null && content.isArray()) {
                    StringBuilder sb = new StringBuilder();
                    for (JsonNode block : content) {
                        if ("text".equals(block.get("type").asText())) {
                            if (sb.length() > 0) sb.append("\n");
                            sb.append(block.get("text").asText());
                        }
                    }
                    if (sb.length() > 0) return sb.toString();
                }
                return json;
            }
        };
    }
}
