package com.example.signup;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

// 演習3の採点テスト(画面の HTML の中身だけで確かめる)
@SpringBootTest
@AutoConfigureMockMvc
class E3SignupFormTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /signup:3つの入力欄がある")
    void form() throws Exception {
        mockMvc.perform(get("/signup"))
            .andExpect(status().isOk())
            .andExpect(content().string(containsString("name=\"name\"")))
            .andExpect(content().string(containsString("name=\"email\"")))
            .andExpect(content().string(containsString("name=\"age\"")));
    }

    @Test
    @DisplayName("POST /signup:正しく入力すると完了画面")
    void ok() throws Exception {
        mockMvc.perform(post("/signup").param("name", "佐藤 花子").param("email", "hanako@example.com").param("age", "20"))
            .andExpect(status().isOk())
            .andExpect(content().string(containsString("登録しました:佐藤 花子さん")));
    }

    @Test
    @DisplayName("POST /signup:名前が空・メールの形が違う・18歳未満なら、それぞれのメッセージ")
    void errors() throws Exception {
        mockMvc.perform(post("/signup").param("name", "").param("email", "not-an-email").param("age", "16"))
            .andExpect(status().isOk())
            .andExpect(content().string(containsString("名前を入力してください")))
            .andExpect(content().string(containsString("メールアドレスの形式が正しくありません")))
            .andExpect(content().string(containsString("18歳以上のみ登録できます")));
    }

    @Test
    @DisplayName("POST /signup:年齢が空でも 18歳以上のメッセージ")
    void ageBlank() throws Exception {
        mockMvc.perform(post("/signup").param("name", "佐藤 花子").param("email", "hanako@example.com").param("age", ""))
            .andExpect(content().string(containsString("18歳以上のみ登録できます")));
    }
}
