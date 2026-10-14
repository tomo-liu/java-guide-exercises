package com.example.cafe.menu;

import com.example.cafe.order.OutOfStockException;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

// menu_item テーブルの1行に対応するエンティティ
@Entity
public class MenuItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private int price;
    private String category;
    private int stock;

    // JPA がDBから読み込むときに使う(自分では使わない)
    protected MenuItem() {
    }

    public MenuItem(String name, int price, String category, int stock) {
        this.name = name;
        this.price = price;
        this.category = category;
        this.stock = stock;
    }

    // 在庫を減らす。足りなければ OutOfStockException
    public void reduceStock(int quantity) {
        if (quantity > stock) {
            throw new OutOfStockException(name, quantity, stock);
        }
        stock -= quantity;
    }

    public Long getId() {
        return id;
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

    public int getStock() {
        return stock;
    }
}
