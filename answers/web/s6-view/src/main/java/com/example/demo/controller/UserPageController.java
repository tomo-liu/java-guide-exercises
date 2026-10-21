package com.example.demo.controller;

import com.example.demo.form.UserForm;
import com.example.demo.model.User;
import com.example.demo.service.UserService;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

// 画面(HTML)を返す Controller。処理は REST の UserController と同じ UserService に頼む
@Controller
@RequestMapping("/users")
public class UserPageController {
    private final UserService userService;

    public UserPageController(UserService userService) {
        this.userService = userService;
    }

    // 一覧画面:GET /users → users.html
    @GetMapping
    public String list(Model model) {
        model.addAttribute("users", userService.selectAll());
        return "users";
    }

    // 登録画面:GET /users/new → 空の UserForm を Model に入れて user-form.html
    @GetMapping("/new")
    public String form(Model model) {
        model.addAttribute("userForm", new UserForm());
        return "user-form";
    }

    // 登録:POST /users → 誤りがあれば user-form.html に戻し、なければ登録して result.html
    @PostMapping
    public String create(@Valid @ModelAttribute UserForm userForm, BindingResult result, Model model) {
        if (result.hasErrors()) {
            return "user-form";
        }
        User saved = userService.insert(new User(userForm.getName(), userForm.getEmail(), userForm.getAge()));
        model.addAttribute("message", saved.getName() + "さん(" + saved.getAge() + "歳)を登録しました");
        return "result";
    }
}
