package com.example.cafe.api;

import com.example.cafe.menu.MenuItem;
import com.example.cafe.menu.MenuService;
import com.example.cafe.order.CheckoutService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MenuApiController {
    private final MenuService menuService;
    private final CheckoutService checkoutService;

    public MenuApiController(MenuService menuService, CheckoutService checkoutService) {
        this.menuService = menuService;
        this.checkoutService = checkoutService;
    }

    @GetMapping("/menu")
    public List<MenuItem> menu() {
        return menuService.findAll();
    }

    @GetMapping("/menu/{name}")
    public MenuItem item(@PathVariable String name) {
        return menuService.findByName(name);
    }

    @PostMapping("/orders")
    public ResponseEntity<OrderResponse> order(@Valid @RequestBody OrderRequest request) {
        int subtotal = menuService.priceOf(request.name()) * request.quantity();
        int total = checkoutService.checkout(subtotal);
        return ResponseEntity.status(HttpStatus.CREATED).body(new OrderResponse(request.name(), request.quantity(), total));
    }
}
