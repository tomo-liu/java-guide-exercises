package com.example.cafe.web;

// 注文フォームの入力を受け取る入れ物
public class OrderForm {
    // TODO: 空なら「品を選んでください」というメッセージで弾く
    private String name;

    // TODO: 1未満なら「個数は1以上にしてください」、10より大きければ「個数は10以下にしてください」で弾く
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
