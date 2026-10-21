package com.example.demo.service;

import com.example.demo.entity.User;
import java.util.List;

public interface UserService {
    User selectOne(int id);

    List<User> selectAll();

    List<User> search(String keyword);

    User insert(User user);

    // 更新。対象がなければ null
    User update(int id, User user);

    // 削除。削除できたら true、対象がなければ false
    boolean delete(int id);
}
