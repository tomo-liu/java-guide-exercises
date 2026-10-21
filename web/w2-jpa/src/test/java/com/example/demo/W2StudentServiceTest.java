package com.example.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertNull;

import com.example.demo.entity.Student;
import com.example.demo.service.StudentService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

// Day5〜6:Entity・DAO・Service で SELECT と INSERT を確かめる
// (@Transactional を付けたテストは、終わると DB の変更が取り消されるので、テストどうしが影響し合わない)
@SpringBootTest
@Transactional
class W2StudentServiceTest {
    @Autowired
    StudentService studentService;

    @Test
    @DisplayName("selectOne:id で1件取得できる")
    void selectOne() {
        Student student = studentService.selectOne(1);
        assertNotNull(student, "id=1 の学生がいない(Entity と data.sql を確かめよう)");
        assertEquals("佐藤 花子", student.getName());
        assertEquals(20, student.getAge());
    }

    @Test
    @DisplayName("selectOne:ない id なら null")
    void selectOneNotFound() {
        assertNull(studentService.selectOne(99));
    }

    @Test
    @DisplayName("selectAll:3件")
    void selectAll() {
        assertEquals(3, studentService.selectAll().size());
    }

    @Test
    @DisplayName("insert → 再 SELECT:登録したデータが DB に入っている")
    void insertThenSelect() {
        Student saved = studentService.insert(new Student("田中 健", 21));
        assertNotNull(saved.getId(), "保存すると id が振られる");
        assertEquals("田中 健", studentService.selectOne(saved.getId()).getName());
        assertEquals(4, studentService.selectAll().size());
    }

    @Test
    @DisplayName("selectByMinAge:20歳以上は2人")
    void selectByMinAge() {
        assertEquals(2, studentService.selectByMinAge(20).size());
    }
}
