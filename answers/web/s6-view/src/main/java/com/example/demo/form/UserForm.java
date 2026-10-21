package com.example.demo.form;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

// 登録フォームの入力値を入れておくクラス。フィールド名はフォームの入力欄の name 属性と同じにする
public class UserForm {
    @NotBlank(message = "名前を入力してください")
    private String name;

    @Email(message = "メールアドレスの形式が正しくありません")
    private String email;

    @NotNull(message = "年齢を入力してください")
    @Min(value = 0, message = "年齢は0以上にしてください")
    @Max(value = 150, message = "年齢は150以下にしてください")
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
