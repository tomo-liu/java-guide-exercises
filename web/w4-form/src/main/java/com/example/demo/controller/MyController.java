package com.example.demo.controller;

import com.example.demo.form.MyForm;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;

@Controller
public class MyController {
    // TODO 3: GET /form で、空の MyForm を "myForm" という名前で Model に入れ、form.html を表示する
    public String form(Model model) {
        return "form";
    }

    // TODO 4: POST /form で MyForm を受け取って入力チェックし(@Valid @ModelAttribute)、
    //         誤りがあれば form.html に戻す。なければ Model に "message"(「田中さん(20歳)を受け付けました」の形)を入れ、result.html を表示する
    public String submit(MyForm myForm, BindingResult result, Model model) {
        return "form";
    }
}
