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
import static org.junit.jupiter.api.Assertions.assertEquals;

import com.example.demo.service.UserService;

// s2:Controller → Service → ServiceImpl の層で、全件取得と1件取得
@SpringBootTest
@AutoConfigureMockMvc
class S2LayersTest {
    @Autowired
    MockMvc mockMvc;

    @Autowired
    UserService userService;

    @Test
    @DisplayName("UserService:Spring が UserServiceImpl を渡してくれる")
    void service() {
        assertEquals("UserServiceImpl", userService.getClass().getSimpleName());
    }

    @Test
    @DisplayName("GET /api/users:全件(200、最初は3人)")
    void getAll() throws Exception {
        mockMvc.perform(get("/api/users"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(3))
            .andExpect(jsonPath("$[0].name").value("佐藤 花子"));
    }

    @Test
    @DisplayName("GET /api/users/{id}:1件(200)、いなければ 404")
    void getOne() throws Exception {
        mockMvc.perform(get("/api/users/2"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("鈴木 一郎"))
            .andExpect(jsonPath("$.age").value(22));
        mockMvc.perform(get("/api/users/99")).andExpect(status().isNotFound());
    }
}
