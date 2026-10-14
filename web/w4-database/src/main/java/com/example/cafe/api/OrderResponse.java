package com.example.cafe.api;

// POST /api/orders が返すJSON
public record OrderResponse(String name, int quantity, int total) {
}
