package com.example.cafe;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

// application.yml に書いたお店の情報
@Component
public class ShopInfo {
    private final String name;
    private final String hours;

    public ShopInfo(@Value("${cafe.name}") String name, @Value("${cafe.hours}") String hours) {
        this.name = name;
        this.hours = hours;
    }

    public String getName() {
        return name;
    }

    public String getHours() {
        return hours;
    }
}
