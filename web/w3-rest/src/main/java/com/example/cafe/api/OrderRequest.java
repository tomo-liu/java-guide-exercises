package com.example.cafe.api;

// POST /api/orders で受け取るJSON
// TODO: OrderForm と同じ入力チェック(品は必須、個数は1〜10)を付ける
public record OrderRequest(String name, int quantity) {
}
