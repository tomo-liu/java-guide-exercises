package com.example.demo.dao;

import com.example.demo.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

// DB を操作する DAO。JpaRepository を継承するだけで findAll・findById・save・deleteById などが使える
// TODO 2: 名前の一部で検索するメソッド findByNameContaining(String keyword) を宣言する(List<User> を返す)
public interface UserDao extends JpaRepository<User, Integer> {
}
