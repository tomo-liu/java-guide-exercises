package com.example.demo.service;

import org.springframework.stereotype.Service;

// GreetingService の実装。@Service を付けると、Spring が部品(Bean)として登録する
@Service
public class GreetingServiceImpl implements GreetingService {
    @Override
    public String greet(String name) {
        return "こんにちは、" + name + "さん";
    }
}
