package com.example.demo.form;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

// 登録フォームの入力値を入れておくクラス。フィールド名はフォームの入力欄の name 属性と同じにする
public class UserForm {
    // TODO 1: 空なら「名前を入力してください」(@NotBlank)
    private String name;

    // TODO 2: メールアドレスの形でなければ「メールアドレスの形式が正しくありません」(@Email)
    private String email;

    // TODO 3: 空なら「年齢を入力してください」(@NotNull)、0未満なら「年齢は0以上にしてください」(@Min)、
    //         150より大きければ「年齢は150以下にしてください」(@Max)
    private Integer age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
