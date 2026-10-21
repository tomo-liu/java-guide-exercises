package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.UserService;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    // TODO 1: GET /api/users で全件を返す(200)
    public List<User> getAll() {
        return List.of();
    }

    // TODO 2: GET /api/users/search?keyword=… で、名前に keyword を含む人を返す(@RequestParam)
    public List<User> search(String keyword) {
        return List.of();
    }

    // TODO 3: GET /api/users/{id} で1件を返す。いなければ 404 Not Found
    public ResponseEntity<User> getOne(int id) {
        return null;
    }

    // TODO 4: POST /api/users で JSON を受け取って登録し、201 Created と登録後の User を返す。
    //         名前が空なら 400(@Valid を付けると、User の @NotBlank がチェックされる)
    public ResponseEntity<User> create(User user) {
        return null;
    }

    // TODO 5: PUT /api/users/{id} で更新し、200 と更新後の User を返す。いなければ 404
    public ResponseEntity<User> update(int id, User user) {
        return null;
    }

    // TODO 6: DELETE /api/users/{id} で削除し、204 No Content を返す。いなければ 404
    public ResponseEntity<Void> delete(int id) {
        return null;
    }
}
