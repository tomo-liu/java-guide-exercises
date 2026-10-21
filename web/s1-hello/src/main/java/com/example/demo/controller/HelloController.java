package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// TODO 1: このクラスを、文字をそのまま返す Controller にする(@RestController)
public class HelloController {
    // TODO 2: GET /hello で「Hello, Spring Boot!」を返す(@GetMapping)
    public String hello() {
        return "";
    }

    // TODO 3: GET /hello/{name} で、URL の {name} の部分を受け取り(@PathVariable)、「こんにちは、〇〇さん」を返す
    public String helloName(String name) {
        return "";
    }
}
