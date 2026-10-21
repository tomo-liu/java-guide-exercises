package com.example.demo.controller;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// TODO 6: どの Controller の例外もまとめて受け止めるクラスにする(@RestControllerAdvice)
public class ApiExceptionHandler {
    // TODO 7: MethodArgumentNotValidException を受け止め(@ExceptionHandler)、400 Bad Request(@ResponseStatus)と ErrorResponse を返す
    //         メッセージは e.getBindingResult().getFieldErrors().get(0).getDefaultMessage() で取れる
    public ErrorResponse badRequest(MethodArgumentNotValidException e) {
        return null;
    }
}
