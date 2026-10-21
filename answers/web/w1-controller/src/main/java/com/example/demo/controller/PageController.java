package com.example.demo.controller;

import com.example.demo.service.GreetingService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

// HTML の画面を返す Controller
@Controller
public class PageController {
    private final GreetingService greetingService;

    public PageController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/welcome")
    public String welcome(Model model) {
        model.addAttribute("message", greetingService.greet("ゲスト"));
        return "welcome";
    }
}
