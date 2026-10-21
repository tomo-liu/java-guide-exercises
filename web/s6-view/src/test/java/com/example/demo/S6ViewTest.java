package com.example.demo;

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
import org.springframework.transaction.annotation.Transactional;

// s6:一覧画面と登録フォーム(フォーム → Controller → Form → Model → HTML)
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class S6ViewTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /users:一覧画面に3人が表示される")
    void list() throws Exception {
        mockMvc.perform(get("/users"))
            .andExpect(status().isOk())
            .andExpect(view().name("users"))
            .andExpect(content().string(containsString("佐藤 花子")))
            .andExpect(content().string(containsString("misaki@example.com")));
    }

    @Test
    @DisplayName("GET /users/new:3つの入力欄がある登録画面")
    void form() throws Exception {
        mockMvc.perform(get("/users/new"))
            .andExpect(status().isOk())
            .andExpect(view().name("user-form"))
            .andExpect(content().string(containsString("name=\"name\"")))
            .andExpect(content().string(containsString("name=\"email\"")))
            .andExpect(content().string(containsString("name=\"age\"")));
    }

    @Test
    @DisplayName("POST /users:正しく入力すると登録され、結果の画面に表示される")
    void create() throws Exception {
        mockMvc.perform(post("/users").param("name", "田中 健").param("email", "ken@example.com").param("age", "21"))
            .andExpect(status().isOk())
            .andExpect(view().name("result"))
            .andExpect(content().string(containsString("田中 健さん(21歳)を登録しました")));
        mockMvc.perform(get("/users")).andExpect(content().string(containsString("ken@example.com")));
    }

    @Test
    @DisplayName("POST /users:誤りがあれば登録画面に戻り、メッセージが出る")
    void createInvalid() throws Exception {
        mockMvc.perform(post("/users").param("name", "").param("email", "abc").param("age", "200"))
            .andExpect(view().name("user-form"))
            .andExpect(content().string(containsString("名前を入力してください")))
            .andExpect(content().string(containsString("メールアドレスの形式が正しくありません")))
            .andExpect(content().string(containsString("年齢は150以下にしてください")));
        mockMvc.perform(post("/users").param("name", "田中 健").param("email", "ken@example.com").param("age", ""))
            .andExpect(view().name("user-form"))
            .andExpect(content().string(containsString("年齢を入力してください")));
    }
}
