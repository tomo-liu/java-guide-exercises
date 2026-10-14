package com.example.cafe.web;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

// 注文フォームの入力を受け取る入れ物
public class OrderForm {
    @NotBlank(message = "品を選んでください")
    private String name;

    @Min(value = 1, message = "個数は1以上にしてください")
    @Max(value = 10, message = "個数は10以下にしてください")
    private int quantity = 1;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }
}
