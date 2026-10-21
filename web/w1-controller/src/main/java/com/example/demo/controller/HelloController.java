package com.example.demo.controller;

import com.example.demo.service.GreetingService;

// TODO 3: 文字をそのまま返す Controller にするアノテーションを付ける
public class HelloController {
    // TODO 4: GreetingService をフィールドで持ち、コンストラクタで受け取る(自分で new しない)

    // TODO 5: GET /hello で「Hello, Spring Boot!」を返す
    public String hello() {
        return "";
    }

    // TODO 6: GET /hello/{name} で、URL の {name} の部分を受け取り、greetingService.greet(name) の結果を返す
    public String helloName(String name) {
        return "";
    }
}
