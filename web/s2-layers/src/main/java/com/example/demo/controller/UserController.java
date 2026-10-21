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

// TODO 4: JSON を返す Controller にし(@RestController)、URL の頭を /api/users にする(@RequestMapping)
public class UserController {
    // TODO 5: UserService をフィールドで持ち、コンストラクタで受け取る(自分で new しない)

    // TODO 6: GET /api/users で全件を返す(@GetMapping)
    public List<User> getAll() {
        return List.of();
    }

    // TODO 7: GET /api/users/{id} で1件を返す(@GetMapping・@PathVariable)。いなければ 404 Not Found
    public ResponseEntity<User> getOne(int id) {
        return null;
    }
}
