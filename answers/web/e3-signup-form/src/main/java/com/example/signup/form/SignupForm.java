package com.example.signup.form;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class SignupForm {
    @NotBlank(message = "名前を入力してください")
    private String name;

    @Email(message = "メールアドレスの形式が正しくありません")
    private String email;

    @NotNull(message = "18歳以上のみ登録できます")
    @Min(value = 18, message = "18歳以上のみ登録できます")
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
