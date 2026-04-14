package com.example.agent.client;

import com.alibaba.cloud.ai.graph.agent.BaseAgent;
import com.alibaba.cloud.ai.graph.exception.GraphRunnerException;
import com.alibaba.cloud.ai.graph.exception.GraphStateException;
import com.alibaba.cloud.ai.graph.streaming.StreamingOutput;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.scheduler.Schedulers;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/")
public class AgentCallController {

    private final BaseAgent remoteAgent;

    public AgentCallController(BaseAgent remoteAgent) {
        this.remoteAgent = remoteAgent;
    }

    @GetMapping("/ask")
    public Flux<String> ask(@RequestParam("question") String question)
            throws GraphStateException, GraphRunnerException {
        return remoteAgent
                .stream(Map.of("messages", List.of(new UserMessage(question))))
                .mapNotNull(output -> {
                    if (output.isSTART() || output.isEND()) {
                        return null;
                    }
                    if (output instanceof StreamingOutput streamingOutput) {
                        return streamingOutput.chunk();
                    }
                    return null;
                })
                .publishOn(Schedulers.parallel());
    }
}
