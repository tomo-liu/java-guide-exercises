package com.example.demo.dao;

import com.example.demo.model.User;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

// DB を操作する DAO。JpaRepository を継承するだけで findAll・findById・save・deleteById などが使える
public interface UserDao extends JpaRepository<User, Integer> {
    // 名前の一部で検索する(メソッド名から WHERE NAME LIKE '%…%' の SQL が作られる)
    List<User> findByNameContaining(String keyword);
}
