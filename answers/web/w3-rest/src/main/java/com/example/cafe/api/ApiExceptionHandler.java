package com.example.cafe.api;

import com.example.cafe.menu.MenuNotFoundException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// API で起きた例外を、まとめてエラーのJSONに変える
@RestControllerAdvice
public class ApiExceptionHandler {
    @ExceptionHandler(MenuNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse notFound(MenuNotFoundException e) {
        return new ErrorResponse(e.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse invalid(MethodArgumentNotValidException e) {
        return new ErrorResponse(e.getBindingResult().getFieldErrors().get(0).getDefaultMessage());
    }
}
