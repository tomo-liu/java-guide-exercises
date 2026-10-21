package com.example.demo.controller;

import org.springframework.web.bind.MethodArgumentNotValidException;

// TODO 7: どの Controller の例外もまとめて受け止めるクラスにする(@RestControllerAdvice)
public class ApiExceptionHandler {
    // TODO 8: MethodArgumentNotValidException を受け止め、400 Bad Request と ErrorResponse を返す
    //         メッセージは e.getBindingResult().getFieldErrors().get(0).getDefaultMessage() で取れる
    public ErrorResponse badRequest(MethodArgumentNotValidException e) {
        return null;
    }
}
