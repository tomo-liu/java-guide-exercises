package com.example.demo.service;

import com.example.demo.dao.UserDao;
import com.example.demo.entity.User;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {
    private final UserDao userDao;

    public UserServiceImpl(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public User selectOne(int id) {
        return userDao.findById(id).orElse(null);
    }

    @Override
    public List<User> selectAll() {
        return userDao.findAll();
    }

    @Override
    public List<User> search(String keyword) {
        return userDao.findByNameContaining(keyword);
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
}
