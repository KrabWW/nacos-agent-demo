package com.example.travel.planner;

import com.alibaba.cloud.ai.graph.OverAllState;
import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.CompletableFuture;

@RestController
@RequestMapping("/")
public class TravelController {

    private static final Logger log = LoggerFactory.getLogger(TravelController.class);

    private final BaseAgent weatherAgent;
    private final BaseAgent hotelAgent;
    private final BaseAgent flightAgent;

    public TravelController(
            @Qualifier("weatherAgent") BaseAgent weatherAgent,
            @Qualifier("hotelAgent") BaseAgent hotelAgent,
            @Qualifier("flightAgent") BaseAgent flightAgent) {
        this.weatherAgent = weatherAgent;
        this.hotelAgent = hotelAgent;
        this.flightAgent = flightAgent;
    }

    @GetMapping("/plan")
    public Map<String, String> plan(@RequestParam("question") String question) {
        log.info("收到旅行规划请求: {}", question);

        CompletableFuture<String> weatherFuture = CompletableFuture.supplyAsync(
                () -> callAgent(weatherAgent, "用户正在规划旅行：" + question + "，请提供目的地天气建议"));
        CompletableFuture<String> hotelFuture = CompletableFuture.supplyAsync(
                () -> callAgent(hotelAgent, "用户正在规划旅行：" + question + "，请推荐合适的酒店"));
        CompletableFuture<String> flightFuture = CompletableFuture.supplyAsync(
                () -> callAgent(flightAgent, "用户正在规划旅行：" + question + "，请推荐合适的航班"));

        CompletableFuture.allOf(weatherFuture, hotelFuture, flightFuture).join();

        Map<String, String> result = new LinkedHashMap<>();
        result.put("question", question);
        result.put("weather", weatherFuture.join());
        result.put("hotel", hotelFuture.join());
        result.put("flight", flightFuture.join());
        return result;
    }

    private String callAgent(BaseAgent agent, String question) {
        try {
            Optional<OverAllState> stateOpt = agent.invoke(Map.of("input", question));
            if (stateOpt.isPresent()) {
                Map<String, Object> data = stateOpt.get().data();
                // 尝试多种可能的 output key
                for (String key : new String[]{"output", "result", "messages", "input"}) {
                    Object val = data.get(key);
                    if (val != null) {
                        return val.toString();
                    }
                }
                return data.toString();
            }
            return "无返回结果";
        } catch (Exception e) {
            log.error("调用Agent失败", e);
            return "调用失败: " + e.getMessage();
        }
    }
}
