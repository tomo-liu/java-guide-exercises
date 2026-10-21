package com.example.demo.controller;

import com.example.demo.service.GreetingService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

@Controller
public class PageController {
    private final GreetingService greetingService;

    public PageController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    // TODO 7: GET /welcome で、Model に "message"(greetingService.greet("ゲスト") の結果)を入れ、welcome.html を表示する
    public String welcome(Model model) {
        return "welcome";
    }
}
