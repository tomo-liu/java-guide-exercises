package com.example.demo.entity;

// TODO 1: STUDENT テーブルの1行を表す Entity にする(@Entity・@Table)
public class Student {
    // TODO 2: 主キーにする(@Id・@GeneratedValue(strategy = GenerationType.IDENTITY))。列名は ID
    private Integer id;

    // TODO 3: 列名を指定する(@Column)。NAME 列・AGE 列
    private String name;

    private Integer age;

    public Student() {
    }

    public Student(String name, Integer age) {
        this.name = name;
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

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
