package com.example.demo.controller;

import com.example.demo.service.GreetingService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// 文字(や JSON)をそのまま返す Controller
@RestController
public class HelloController {
    private final GreetingService greetingService;

    // コンストラクタインジェクション:GreetingService の実装は Spring が渡してくれる
    public HelloController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }

    @GetMapping("/hello/{name}")
    public String helloName(@PathVariable String name) {
        return greetingService.greet(name);
    }
}
