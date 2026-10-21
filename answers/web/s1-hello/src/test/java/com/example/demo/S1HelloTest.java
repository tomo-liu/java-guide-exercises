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

// s1:Controller で文字を返す
@SpringBootTest
@AutoConfigureMockMvc
class S1HelloTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /hello:文字をそのまま返す")
    void hello() throws Exception {
        mockMvc.perform(get("/hello"))
            .andExpect(status().isOk())
            .andExpect(content().string("Hello, Spring Boot!"));
    }

    @Test
    @DisplayName("GET /hello/{name}:URL の一部を受け取って、あいさつを返す")
    void helloName() throws Exception {
        mockMvc.perform(get("/hello/{name}", "田中"))
            .andExpect(status().isOk())
            .andExpect(content().string("こんにちは、田中さん"));
    }
}
