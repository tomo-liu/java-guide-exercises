package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// 文字をそのまま返す Controller(リクエストの窓口)
@RestController
public class HelloController {
    // GET /hello → 「Hello, Spring Boot!」
    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }

    // GET /hello/田中 → 「こんにちは、田中さん」
    @GetMapping("/hello/{name}")
    public String helloName(@PathVariable String name) {
        return "こんにちは、" + name + "さん";
    }
}
