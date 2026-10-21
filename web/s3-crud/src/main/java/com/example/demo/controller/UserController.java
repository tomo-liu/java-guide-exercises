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

    // TODO 4: POST /api/users で JSON を受け取って(@PostMapping・@RequestBody)登録し、201 Created と登録後の User を返す
    public ResponseEntity<User> create(User user) {
        return null;
    }

    // TODO 5: PUT /api/users/{id} で更新し(@PutMapping)、200 と更新後の User を返す。いなければ 404
    public ResponseEntity<User> update(int id, User user) {
        return null;
    }

    // TODO 6: DELETE /api/users/{id} で削除し(@DeleteMapping)、204 No Content を返す。いなければ 404
    public ResponseEntity<Void> delete(int id) {
        return null;
    }
}
