package com.example.cafe.menu;

// メニューにない品を指定されたときの例外
public class MenuNotFoundException extends RuntimeException {
    public MenuNotFoundException(String name) {
        super(name + " はメニューにありません");
    }
}
