package com.example.demo.dao;

import com.example.demo.entity.Student;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

// DB を直接操作する DAO。JpaRepository を継承するだけで findById・findAll・save・deleteById が使える
public interface StudentDao extends JpaRepository<Student, Integer> {
    // メソッド名から SQL が作られる(WHERE AGE >= ?)
    List<Student> findByAgeGreaterThanEqual(Integer age);
}
