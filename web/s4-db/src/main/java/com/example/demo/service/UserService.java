package com.example.demo.service;

import com.example.demo.model.User;
import java.util.List;

// ユーザーを扱う処理の「約束」(インターフェース)。Controller はこの約束だけを知っている
public interface UserService {
    // 全件取得
    List<User> selectAll();

    // 1件取得(見つからなければ null)
    User selectOne(int id);

    // 登録(id を振って、登録後の User を返す)
    User insert(User user);

    // 更新(対象がいなければ null)
    User update(int id, User user);

    // 削除(削除できたら true、対象がいなければ false)
    boolean delete(int id);
}
