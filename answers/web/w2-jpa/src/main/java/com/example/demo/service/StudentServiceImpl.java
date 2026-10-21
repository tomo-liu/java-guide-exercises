package com.example.demo.service;

import com.example.demo.dao.StudentDao;
import com.example.demo.entity.Student;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class StudentServiceImpl implements StudentService {
    private final StudentDao studentDao;

    public StudentServiceImpl(StudentDao studentDao) {
        this.studentDao = studentDao;
    }

    @Override
    public Student selectOne(int id) {
        // findById は Optional を返す。見つからなければ null にする
        return studentDao.findById(id).orElse(null);
    }

    @Override
    public List<Student> selectAll() {
        return studentDao.findAll();
    }

    @Override
    public Student insert(Student student) {
        return studentDao.save(student);
    }

    @Override
    public List<Student> selectByMinAge(int age) {
        return studentDao.findByAgeGreaterThanEqual(age);
    }
}
