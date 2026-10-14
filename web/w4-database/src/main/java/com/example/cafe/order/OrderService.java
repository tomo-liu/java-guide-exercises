package com.example.cafe.order;

import com.example.cafe.api.OrderRequest;
import com.example.cafe.menu.MenuService;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final MenuService menuService;
    private final CheckoutService checkoutService;
    private final CafeOrderRepository orderRepository;

    public OrderService(MenuService menuService, CheckoutService checkoutService, CafeOrderRepository orderRepository) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
        this.orderRepository = orderRepository;
    }

    // TODO: 注文を受け付ける。途中で在庫切れが起きたら、それまでの在庫の減少も全部取り消されるようにする
    //   1. new CafeOrder() を作る
    //   2. 注文の品ごとに、menuService.findByName で品を探し、item.reduceStock(個数) で在庫を減らし、
    //      order.addLine(品, 個数) で明細を足し、価格 × 個数 を小計に足す
    //   3. order.setTotal(checkoutService.checkout(小計)) で割引後の金額を入れる
    //   4. orderRepository.save(order) で保存して返す
    public CafeOrder placeOrder(List<OrderRequest> requests) {
        throw new UnsupportedOperationException("TODO");
    }
}
