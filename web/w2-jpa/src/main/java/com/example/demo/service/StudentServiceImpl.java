package com.example.demo.service;

import com.example.demo.entity.Student;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class StudentServiceImpl implements StudentService {
    // TODO 6: StudentDao をフィールドで持ち、コンストラクタで受け取る

    // TODO 7: findById で探し、見つからなければ null を返す(Optional の orElse を使う)
    @Override
    public Student selectOne(int id) {
        return null;
    }

    // TODO 8: findAll で全件を返す
    @Override
    public List<Student> selectAll() {
        return List.of();
    }

    // TODO 9: save で登録し、登録後の Student を返す
    @Override
    public Student insert(Student student) {
        return null;
    }

    // TODO 10: findByAgeGreaterThanEqual を使う
    @Override
    public List<Student> selectByMinAge(int age) {
        return List.of();
    }
}
