package com.example.cafe.api;

import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import java.util.List;
import org.springframework.http.ResponseEntity;

// TODO: JSON を返すコントローラーにし、URL の先頭を /api にそろえる
public class MenuApiController {
    private final MenuService menuService;
    private final CheckoutService checkoutService;

    public MenuApiController(MenuService menuService, CheckoutService checkoutService) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
    }

    // TODO: GET /api/menu で全メニューを返す
    public List<MenuItem> menu() {
        return List.of();
    }

    // TODO: GET /api/menu/{name} で1品を返す(ない名前なら MenuNotFoundException がそのまま投げられてよい)
    public MenuItem item(String name) {
        return null;
    }

    // TODO: POST /api/orders で JSON を受け取って入力をチェックし、
    //       201 Created と OrderResponse(品名・個数・割引後の金額)を返す
    public ResponseEntity<OrderResponse> order(OrderRequest request) {
        return null;
    }
}
