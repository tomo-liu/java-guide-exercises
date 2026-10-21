package com.example.demo.dao;

import com.example.demo.entity.User;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserDao extends JpaRepository<User, Integer> {
    // 名前の一部で検索する(WHERE NAME LIKE '%…%')
    List<User> findByNameContaining(String keyword);
}
