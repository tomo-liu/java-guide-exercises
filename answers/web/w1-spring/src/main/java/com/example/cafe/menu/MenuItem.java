package com.example.cafe.menu;

public class MenuItem {
    private final String name;
    private final int price;
    private final String category;

    public MenuItem(String name, int price, String category) {
        this.name = name;
        this.price = price;
        this.category = category;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public String getCategory() {
        return category;
    }
}
