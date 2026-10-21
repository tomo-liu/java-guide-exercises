package com.example.demo.service;

import com.example.demo.model.User;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

// UserService の中身。データはアプリの中の ArrayList に入れておく(アプリを止めると最初の3人に戻る)
// TODO 1: Spring に部品(Bean)として登録するアノテーションを付ける(@Service)
public class UserServiceImpl implements UserService {
    private final List<User> users = new ArrayList<>();
    private int nextId = 1;

    // 最初のデータを3人分入れておく
    public UserServiceImpl() {
        add(new User("佐藤 花子", "hanako@example.com", 20));
        add(new User("鈴木 一郎", "ichiro@example.com", 22));
        add(new User("高橋 美咲", "misaki@example.com", 19));
    }

    // id を振ってリストに追加する
    private User add(User user) {
        user.setId(nextId);
        nextId++;
        users.add(user);
        return user;
    }

    // TODO 2: users をそのまま返す
    @Override
    public List<User> selectAll() {
        return List.of();
    }

    // TODO 3: users の中から id が一致する User を探して返す。見つからなければ null
    @Override
    public User selectOne(int id) {
        return null;
    }
}
