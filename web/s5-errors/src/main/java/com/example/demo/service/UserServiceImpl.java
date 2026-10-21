package com.example.demo.service;

import com.example.demo.dao.UserDao;
import com.example.demo.model.User;
import java.util.List;
import org.springframework.stereotype.Service;

// UserService の中身(DB 版)。ArrayList の代わりに UserDao を使う。Controller は変えなくてよい
@Service
public class UserServiceImpl implements UserService {
    private final UserDao userDao;

    public UserServiceImpl(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public List<User> selectAll() {
        return userDao.findAll();
    }

    @Override
    public User selectOne(int id) {
        // findById は Optional(中身があるかもしれない箱)を返す。見つからなければ null にする
        return userDao.findById(id).orElse(null);
    }

    @Override
    public User insert(User user) {
        user.setId(null); // 新規登録なので、id は DB に振らせる
        return userDao.save(user);
    }

    @Override
    public User update(int id, User user) {
        if (!userDao.existsById(id)) {
            return null;
        }
        user.setId(id); // id があるので、save は INSERT ではなく UPDATE になる
        return userDao.save(user);
    }

    @Override
    public boolean delete(int id) {
        if (!userDao.existsById(id)) {
            return false;
        }
        userDao.deleteById(id);
        return true;
    }

    // TODO 3: UserDao の findByNameContaining を使う
    @Override
    public List<User> search(String keyword) {
        return List.of();
    }
}
