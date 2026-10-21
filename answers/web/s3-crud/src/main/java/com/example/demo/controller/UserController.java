package com.example.demo.controller;

import com.example.demo.model.User;
import com.example.demo.service.UserService;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// /api/users へのリクエストを受ける Controller。処理は UserService に頼む
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    // コンストラクタインジェクション:UserService の中身(UserServiceImpl)は Spring が渡してくれる
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 全件取得:GET /api/users → 200
    @GetMapping
    public List<User> getAll() {
        return userService.selectAll();
    }

    // 1件取得:GET /api/users/1 → 200(いなければ 404)
    @GetMapping("/{id}")
    public ResponseEntity<User> getOne(@PathVariable int id) {
        User user = userService.selectOne(id);
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(user);
    }

    // 登録:POST /api/users → 201
    @PostMapping
    public ResponseEntity<User> create(@RequestBody User user) {
        User saved = userService.insert(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    // 更新:PUT /api/users/1 → 200(いなければ 404)
    @PutMapping("/{id}")
    public ResponseEntity<User> update(@PathVariable int id, @RequestBody User user) {
        User updated = userService.update(id, user);
        if (updated == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }

    // 削除:DELETE /api/users/1 → 204(いなければ 404)
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable int id) {
        if (!userService.delete(id)) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }
}
