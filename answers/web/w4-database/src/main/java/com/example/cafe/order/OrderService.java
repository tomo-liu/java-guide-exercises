package com.example.cafe.order;

import com.example.cafe.api.OrderRequest;
import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuService;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

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

    // 在庫を減らし、注文を保存する。途中で在庫切れが起きたら、全部なかったことにする
    @Transactional
    public CafeOrder placeOrder(List<OrderRequest> requests) {
        CafeOrder order = new CafeOrder();
        int subtotal = 0;
        for (OrderRequest request : requests) {
            MenuItem item = menuService.findByName(request.name());
            item.reduceStock(request.quantity());
            order.addLine(item, request.quantity());
            subtotal += item.getPrice() * request.quantity();
        }
        order.setTotal(checkoutService.checkout(subtotal));
        return orderRepository.save(order);
    }
}
