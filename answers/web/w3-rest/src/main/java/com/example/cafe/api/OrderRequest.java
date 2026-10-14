package com.example.cafe.api;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

// POST /api/orders で受け取るJSON
public record OrderRequest(
    @NotBlank(message = "品を選んでください") String name,
    @Min(value = 1, message = "個数は1以上にしてください") @Max(value = 10, message = "個数は10以下にしてください") int quantity) {
}
