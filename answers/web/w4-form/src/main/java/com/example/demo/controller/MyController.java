package com.example.demo.controller;

import com.example.demo.form.MyForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class MyController {
    // 入力画面:空の MyForm を Model に入れて、form.html を表示する
    @GetMapping("/form")
    public String form(Model model) {
        model.addAttribute("myForm", new MyForm());
        return "form";
    }

    // 送信後:入力に誤りがあれば form.html に戻し、なければ result.html に結果を表示する
    @PostMapping("/form")
    public String submit(@Valid @ModelAttribute MyForm myForm, BindingResult result, Model model) {
        if (result.hasErrors()) {
            return "form";
        }
        model.addAttribute("message", myForm.getName() + "さん(" + myForm.getAge() + "歳)を受け付けました");
        return "result";
    }
}
