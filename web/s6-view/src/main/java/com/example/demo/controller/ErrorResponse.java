package com.example.demo.controller;

// エラーのときに返す JSON:{"message": "…"}
public record ErrorResponse(String message) {
}
