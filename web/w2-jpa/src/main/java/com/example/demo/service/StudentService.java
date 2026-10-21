package com.example.demo.service;

import com.example.demo.entity.Student;
import java.util.List;

public interface StudentService {
    // 1件取得(見つからなければ null)
    Student selectOne(int id);

    // 全件取得
    List<Student> selectAll();

    // 新規登録(登録後の Student を返す。id が振られている)
    Student insert(Student student);

    // age 歳以上の学生
    List<Student> selectByMinAge(int age);
}
