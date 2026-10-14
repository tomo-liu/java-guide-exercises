package com.example.cafe;

// TODO: Spring に部品として登録するアノテーションを付ける
public class ShopInfo {
    private final String name;
    private final String hours;

    // TODO: @Value を使い、application.yml の cafe.name と cafe.hours を受け取る
    public ShopInfo(String name, String hours) {
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
