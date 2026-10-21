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
// TODO 4: 画面を返す Controller にし(@Controller)、URL の頭を /users にする(@RequestMapping)
public class UserPageController {
    // TODO 5: UserService をフィールドで持ち、コンストラクタで受け取る

    // TODO 6: GET /users で、Model に "users"(全件)を入れて users.html を表示する
    public String list(Model model) {
        return "users";
    }

    // TODO 7: GET /users/new で、空の UserForm を "userForm" という名前で Model に入れて user-form.html を表示する
    public String form(Model model) {
        return "user-form";
    }

    // TODO 8: POST /users で UserForm を受け取って入力チェックし(@Valid @ModelAttribute)、誤りがあれば user-form.html に戻す。
    //         なければ User を作って登録し、Model に "message"(「田中 健さん(21歳)を登録しました」の形)を入れ、result.html を表示する
    public String create(UserForm userForm, BindingResult result, Model model) {
        return "user-form";
    }
}
