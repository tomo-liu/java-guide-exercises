package com.example.demo.dao;

import com.example.demo.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

// DB を操作する DAO。JpaRepository を継承するだけで findAll・findById・save・deleteById などが使える
public interface UserDao extends JpaRepository<User, Integer> {
}
