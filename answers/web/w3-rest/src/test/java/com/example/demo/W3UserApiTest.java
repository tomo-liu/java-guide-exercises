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

// Day7:REST API の CRUD とステータスコードを確かめる
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class W3UserApiTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /api/users:全件(200)")
    void getAll() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(3))
            .andExpect(jsonPath("$[0].name").value("佐藤 花子"));
    }

    @Test
    @DisplayName("GET /api/users/search?keyword=:名前で検索(200)")
    void search() throws Exception {
        mockMvc.perform(get("/api/users/search").param("keyword", "鈴木"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(1))
            .andExpect(jsonPath("$[0].email").value("ichiro@example.com"));
    }

    @Test
    @DisplayName("GET /api/users/{id}:1件(200)、いなければ 404")
    void getOne() throws Exception {
        mockMvc.perform(get("/api/users/2")).andExpect(status().isOk()).andExpect(jsonPath("$.name").value("鈴木 一郎"));
        mockMvc.perform(get("/api/users/99")).andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("POST /api/users:登録すると 201 と、id の振られた User")
    void create() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"田中 健\", \"email\": \"ken@example.com\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(4))
            .andExpect(jsonPath("$.name").value("田中 健"));
    }

    @Test
    @DisplayName("POST /api/users:名前が空なら 400 とエラーメッセージ")
    void createInvalid() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"\", \"email\": \"x@example.com\"}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("名前は必須です"));
    }

    @Test
    @DisplayName("PUT /api/users/{id}:更新(200)、いなければ 404")
    void update() throws Exception {
        mockMvc.perform(put("/api/users/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"佐藤 花子\", \"email\": \"hanako.new@example.com\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.email").value("hanako.new@example.com"));
        mockMvc.perform(put("/api/users/99")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\": \"だれか\", \"email\": \"x@example.com\"}"))
            .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("DELETE /api/users/{id}:削除は 204、いなければ 404")
    void deleteUser() throws Exception {
        mockMvc.perform(delete("/api/users/3")).andExpect(status().isNoContent());
        mockMvc.perform(get("/api/users/3")).andExpect(status().isNotFound());
        mockMvc.perform(delete("/api/users/99")).andExpect(status().isNotFound());
    }
}
