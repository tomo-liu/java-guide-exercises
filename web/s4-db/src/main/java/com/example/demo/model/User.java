package com.example.demo.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

// TODO 1: USERS テーブルの1行と対応する Entity にする(@Entity・@Table(name = "USERS"))
public class User {
    // TODO 2: 主キーにする(@Id・@GeneratedValue(strategy = GenerationType.IDENTITY)・@Column(name = "ID"))
    private Integer id;

    // TODO 3: 列名を指定する(@Column)。NAME・EMAIL・AGE
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
