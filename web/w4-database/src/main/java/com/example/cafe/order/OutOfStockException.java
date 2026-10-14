package com.example.cafe.order;

// 在庫切れ(RuntimeException なので、@Transactional のメソッドから投げられるとロールバックされる)
public class OutOfStockException extends RuntimeException {
    public OutOfStockException(String name, int requested, int remaining) {
        super(name + "の在庫が足りません(注文" + requested + "、残り" + remaining + ")");
    }
}
