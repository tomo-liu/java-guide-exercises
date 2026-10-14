package com.example.cafe.order;

import com.example.cafe.menu.MenuItem;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

// 注文明細(order_line テーブル)。どの注文の、どの品を、何個か
@Entity
public class OrderLine {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    private CafeOrder order;

    @ManyToOne
    private MenuItem item;

    private int quantity;

    protected OrderLine() {
    }

    public OrderLine(CafeOrder order, MenuItem item, int quantity) {
        this.order = order;
        this.item = item;
        this.quantity = quantity;
    }

    public MenuItem getItem() {
        return item;
    }

    public int getQuantity() {
        return quantity;
    }

    public int subtotal() {
        return item.getPrice() * quantity;
    }
}
