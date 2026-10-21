package com.example.demo.service;

import com.example.demo.dao.UserDao;
import com.example.demo.model.User;
import java.util.List;
import org.springframework.stereotype.Service;

// UserService の中身を DB 版に作り直す。ArrayList は使わない。Controller は変えなくてよい
@Service
public class UserServiceImpl implements UserService {
    // TODO 5: UserDao をフィールドで持ち、コンストラクタで受け取る

    // TODO 6: findAll で全件を返す
    @Override
    public List<User> selectAll() {
        return List.of();
    }

    // TODO 7: findById で探し、見つからなければ null(Optional の orElse を使う)
    @Override
    public User selectOne(int id) {
        return null;
    }

    // TODO 8: id を null にしてから save する(id は DB に振らせる)
    @Override
    public User insert(User user) {
        return null;
    }

    // TODO 9: existsById でいなければ null。いれば id を入れてから save(UPDATE になる)
    @Override
    public User update(int id, User user) {
        return null;
    }

    // TODO 10: existsById でいなければ false。いれば deleteById して true
    @Override
    public boolean delete(int id) {
        return false;
    }
}
