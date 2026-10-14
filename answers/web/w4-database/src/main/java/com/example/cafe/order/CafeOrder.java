package com.example.cafe.order;

import com.example.cafe.menu.MenuItem;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import java.util.ArrayList;
import java.util.List;

// 1回の注文(orders テーブル)。注文明細(OrderLine)を複数持つ
@Entity
@Table(name = "orders")
public class CafeOrder {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int total;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL)
    private List<OrderLine> lines = new ArrayList<>();

    public void addLine(MenuItem item, int quantity) {
        lines.add(new OrderLine(this, item, quantity));
    }

    public Long getId() {
        return id;
    }

    public int getTotal() {
        return total;
    }

    public void setTotal(int total) {
        this.total = total;
    }

    public List<OrderLine> getLines() {
        return lines;
    }
}
