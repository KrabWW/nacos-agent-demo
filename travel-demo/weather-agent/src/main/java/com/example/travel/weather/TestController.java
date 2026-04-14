package com.example.travel.weather;

import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TestController {

    private final ChatModel chatModel;

    public TestController(ChatModel chatModel) {
        this.chatModel = chatModel;
    }

    @GetMapping("/test")
    public String test(@RequestParam(defaultValue = "hello") String q) {
        try {
            ChatResponse response = chatModel.call(new Prompt(q));
            if (response == null) return "ChatResponse is null";
            if (response.getResult() == null) return "getResult() is null";
            return "OK: " + response.getResult().getOutput().getText();
        } catch (Exception e) {
            StringBuilder sb = new StringBuilder();
            sb.append("ERROR: ").append(e.getClass().getName()).append(": ").append(e.getMessage()).append("\n");
            Throwable cause = e.getCause();
            while (cause != null) {
                sb.append("  Caused by: ").append(cause.getClass().getName()).append(": ").append(cause.getMessage()).append("\n");
                cause = cause.getCause();
            }
            return sb.toString();
        }
    }
}
