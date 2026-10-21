package com.example.demo.form;

// フォームの入力値を入れておくクラス
public class MyForm {
    // TODO 1: 空なら「名前を入力してください」で弾く(@NotBlank)
    private String name;

    // TODO 2: 空なら「年齢を入力してください」(@NotNull)、0未満なら「年齢は0以上にしてください」(@Min)、
    //         150より大きければ「年齢は150以下にしてください」(@Max)で弾く
    private Integer age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
