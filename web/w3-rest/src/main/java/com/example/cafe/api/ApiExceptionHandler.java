package com.example.cafe.api;

import com.example.cafe.menu.MenuNotFoundException;
import org.springframework.web.bind.MethodArgumentNotValidException;

// TODO: API で起きた例外をまとめて受け止めるクラスにする
public class ApiExceptionHandler {
    // TODO: MenuNotFoundException を 404 Not Found と ErrorResponse(例外のメッセージ)にする
    public ErrorResponse notFound(MenuNotFoundException e) {
        return null;
    }

    // TODO: 入力チェックの失敗を 400 Bad Request と ErrorResponse(最初の項目のメッセージ)にする
    //       メッセージは e.getBindingResult().getFieldErrors().get(0).getDefaultMessage() で取れる
    public ErrorResponse invalid(MethodArgumentNotValidException e) {
        return null;
    }
}
