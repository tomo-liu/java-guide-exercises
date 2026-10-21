package com.example.demo.model;

// ユーザー1人分のデータ(Model)。id・名前・メールアドレス・年齢を持つ
public class User {
    private Integer id;
    private String name;
    private String email;
    private Integer age;

    // 引数なしのコンストラクタ(JSON や DB から User を作るときに使われる)
    public User() {
    }

    public User(String name, String email, Integer age) {
        this.name = name;
        this.email = email;
        this.age = age;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

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
