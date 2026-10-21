# 課題リポジトリ web/ を、研修(Day4〜8)に合わせた Spring Boot の課題に作り直す。
#   python tools/gen_web.py <リポジトリのルート> <initializr で作ったプロジェクト(pom・mvnwの元)>
#
#   w1-controller … Day4:Controller・@GetMapping・DI(Service と ServiceImpl)・Model
#   w2-jpa        … Day5〜6:Entity・DAO(JpaRepository)・Service で SELECT / INSERT
#   w3-rest       … Day7:REST API の CRUD(GET/POST/PUT/DELETE、200/201/204/400/404)
#   w4-form       … Day8:フォーム・Model・入力チェック
#   e1〜e3        … 第8部「課題文から実装する」の演習(README の課題文だけを渡し、ファイルは自分で作る)
#
# 各プロジェクトの「解答」は ANSWER、「開始コード」は ANSWER を START で上書きしたもの
# (e1〜e3 は START_ONLY のファイルだけ)。テストは開始・解答の両方に入れる。
import os, shutil, sys

ROOT = sys.argv[1]
BASE = sys.argv[2]
P = {}


def app_class(pkg, name):
    return f'''package {pkg};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class {name} {{

    public static void main(String[] args) {{
        SpringApplication.run({name}.class, args);
    }}
}}
'''


H2_PROPS = r'''spring.application.name=demo

# --- DB(手元では H2 を使う。アプリと一緒にメモリの中で動き、起動するたびに作り直される) ---
spring.datasource.url=jdbc:h2:mem:school
spring.datasource.username=sa
spring.datasource.password=
# Entity からテーブルを作り、そのあと data.sql で最初のデータを入れる
spring.jpa.hibernate.ddl-auto=create
spring.jpa.defer-datasource-initialization=true
spring.sql.init.encoding=UTF-8
# 実行された SQL をログに出す(学習用)
spring.jpa.show-sql=true

# --- 研修(MariaDB)の場合は、たとえば次のように書く(パスワードは Git に上げない) ---
# spring.datasource.url=jdbc:mariadb://localhost:3307/school
# spring.datasource.username=${DB_USERNAME}
# spring.datasource.password=${DB_PASSWORD}
# spring.jpa.hibernate.ddl-auto=none
'''

MOCKMVC_IMPORTS = r'''import static org.hamcrest.Matchers.containsString;
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
'''

J = "src/main/java/com/example/demo/"
T = "src/test/java/com/example/demo/"
R = "src/main/resources/"

# =====================================================================
# w1-controller(Day4)
# =====================================================================
w1 = {}
w1[J + "DemoApplication.java"] = app_class("com.example.demo", "DemoApplication")
w1[R + "application.properties"] = "spring.application.name=demo\n"
w1[J + "service/GreetingService.java"] = r'''package com.example.demo.service;

// あいさつの文を作る Service の「約束」(インターフェース)
public interface GreetingService {
    String greet(String name);
}
'''
w1[J + "service/GreetingServiceImpl.java"] = r'''package com.example.demo.service;

import org.springframework.stereotype.Service;

// GreetingService の実装。@Service を付けると、Spring が部品(Bean)として登録する
@Service
public class GreetingServiceImpl implements GreetingService {
    @Override
    public String greet(String name) {
        return "こんにちは、" + name + "さん";
    }
}
'''
w1[J + "controller/HelloController.java"] = r'''package com.example.demo.controller;

import com.example.demo.service.GreetingService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// 文字(や JSON)をそのまま返す Controller
@RestController
public class HelloController {
    private final GreetingService greetingService;

    // コンストラクタインジェクション:GreetingService の実装は Spring が渡してくれる
    public HelloController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }

    @GetMapping("/hello/{name}")
    public String helloName(@PathVariable String name) {
        return greetingService.greet(name);
    }
}
'''
w1[J + "controller/PageController.java"] = r'''package com.example.demo.controller;

import com.example.demo.service.GreetingService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

// HTML の画面を返す Controller
@Controller
public class PageController {
    private final GreetingService greetingService;

    public PageController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/welcome")
    public String welcome(Model model) {
        model.addAttribute("message", greetingService.greet("ゲスト"));
        return "welcome";
    }
}
'''
w1[R + "templates/welcome.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ようこそ</title>
</head>
<body>
<h1>ようこそ</h1>
<p th:text="${message}">ここにメッセージが入る</p>
</body>
</html>
'''
w1_start = {
    J + "service/GreetingServiceImpl.java": r'''package com.example.demo.service;

// TODO 1: Spring に部品(Bean)として登録するアノテーションを付ける
public class GreetingServiceImpl implements GreetingService {
    // TODO 2: 「こんにちは、田中さん」の形の文を返す
    @Override
    public String greet(String name) {
        return "";
    }
}
''',
    J + "controller/HelloController.java": r'''package com.example.demo.controller;

import com.example.demo.service.GreetingService;

// TODO 3: 文字をそのまま返す Controller にするアノテーションを付ける
public class HelloController {
    // TODO 4: GreetingService をフィールドで持ち、コンストラクタで受け取る(自分で new しない)

    // TODO 5: GET /hello で「Hello, Spring Boot!」を返す
    public String hello() {
        return "";
    }

    // TODO 6: GET /hello/{name} で、URL の {name} の部分を受け取り、greetingService.greet(name) の結果を返す
    public String helloName(String name) {
        return "";
    }
}
''',
    J + "controller/PageController.java": r'''package com.example.demo.controller;

import com.example.demo.service.GreetingService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;

@Controller
public class PageController {
    private final GreetingService greetingService;

    public PageController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    // TODO 7: GET /welcome で、Model に "message"(greetingService.greet("ゲスト") の結果)を入れ、welcome.html を表示する
    public String welcome(Model model) {
        return "welcome";
    }
}
''',
}
w1_tests = {
    T + "W1ControllerTest.java": r'''package com.example.demo;

''' + MOCKMVC_IMPORTS + r'''
import static org.junit.jupiter.api.Assertions.assertEquals;

import com.example.demo.service.GreetingService;

// Day4:Controller と DI を確かめる
@SpringBootTest
@AutoConfigureMockMvc
class W1ControllerTest {
    @Autowired
    MockMvc mockMvc;

    @Autowired
    GreetingService greetingService;

    @Test
    @DisplayName("GreetingService:Spring が GreetingServiceImpl を渡してくれる")
    void greetingService() {
        assertEquals("GreetingServiceImpl", greetingService.getClass().getSimpleName());
        assertEquals("こんにちは、田中さん", greetingService.greet("田中"));
    }

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

    @Test
    @DisplayName("GET /welcome:Model に入れたメッセージが HTML に表示される")
    void welcome() throws Exception {
        mockMvc.perform(get("/welcome"))
            .andExpect(status().isOk())
            .andExpect(view().name("welcome"))
            .andExpect(content().string(containsString("こんにちは、ゲストさん")));
    }
}
'''
}
P["w1-controller"] = dict(answer=w1, start=w1_start, tests=w1_tests)

# =====================================================================
# w2-jpa(Day5〜6)
# =====================================================================
w2 = {}
w2[J + "DemoApplication.java"] = app_class("com.example.demo", "DemoApplication")
w2[R + "application.properties"] = H2_PROPS
w2[R + "data.sql"] = r'''INSERT INTO STUDENT (NAME, AGE) VALUES ('佐藤 花子', 20);
INSERT INTO STUDENT (NAME, AGE) VALUES ('鈴木 一郎', 22);
INSERT INTO STUDENT (NAME, AGE) VALUES ('高橋 美咲', 19);
'''
w2[J + "entity/Student.java"] = r'''package com.example.demo.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

// STUDENT テーブルの1行を表すクラス(Entity)
@Entity
@Table(name = "STUDENT")
public class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    private Integer id;

    @Column(name = "NAME")
    private String name;

    @Column(name = "AGE")
    private Integer age;

    // JPA が DB から読み込むときに使う、引数なしのコンストラクタ
    public Student() {
    }

    public Student(String name, Integer age) {
        this.name = name;
        this.age = age;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
'''
w2[J + "dao/StudentDao.java"] = r'''package com.example.demo.dao;

import com.example.demo.entity.Student;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

// DB を直接操作する DAO。JpaRepository を継承するだけで findById・findAll・save・deleteById が使える
public interface StudentDao extends JpaRepository<Student, Integer> {
    // メソッド名から SQL が作られる(WHERE AGE >= ?)
    List<Student> findByAgeGreaterThanEqual(Integer age);
}
'''
w2[J + "service/StudentService.java"] = r'''package com.example.demo.service;

import com.example.demo.entity.Student;
import java.util.List;

public interface StudentService {
    // 1件取得(見つからなければ null)
    Student selectOne(int id);

    // 全件取得
    List<Student> selectAll();

    // 新規登録(登録後の Student を返す。id が振られている)
    Student insert(Student student);

    // age 歳以上の学生
    List<Student> selectByMinAge(int age);
}
'''
w2[J + "service/StudentServiceImpl.java"] = r'''package com.example.demo.service;

import com.example.demo.dao.StudentDao;
import com.example.demo.entity.Student;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class StudentServiceImpl implements StudentService {
    private final StudentDao studentDao;

    public StudentServiceImpl(StudentDao studentDao) {
        this.studentDao = studentDao;
    }

    @Override
    public Student selectOne(int id) {
        // findById は Optional を返す。見つからなければ null にする
        return studentDao.findById(id).orElse(null);
    }

    @Override
    public List<Student> selectAll() {
        return studentDao.findAll();
    }

    @Override
    public Student insert(Student student) {
        return studentDao.save(student);
    }

    @Override
    public List<Student> selectByMinAge(int age) {
        return studentDao.findByAgeGreaterThanEqual(age);
    }
}
'''
w2_start = {
    J + "entity/Student.java": r'''package com.example.demo.entity;

// TODO 1: STUDENT テーブルの1行を表す Entity にする(@Entity・@Table)
public class Student {
    // TODO 2: 主キーにする(@Id・@GeneratedValue(strategy = GenerationType.IDENTITY))。列名は ID
    private Integer id;

    // TODO 3: 列名を指定する(@Column)。NAME 列・AGE 列
    private String name;

    private Integer age;

    public Student() {
    }

    public Student(String name, Integer age) {
        this.name = name;
        this.age = age;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
''',
    J + "dao/StudentDao.java": r'''package com.example.demo.dao;

// TODO 4: JpaRepository<Student, Integer> を継承する
// TODO 5: age 歳以上の学生を探すメソッド findByAgeGreaterThanEqual(Integer age) を宣言する
public interface StudentDao {
}
''',
    J + "service/StudentServiceImpl.java": r'''package com.example.demo.service;

import com.example.demo.entity.Student;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class StudentServiceImpl implements StudentService {
    // TODO 6: StudentDao をフィールドで持ち、コンストラクタで受け取る

    // TODO 7: findById で探し、見つからなければ null を返す(Optional の orElse を使う)
    @Override
    public Student selectOne(int id) {
        return null;
    }

    // TODO 8: findAll で全件を返す
    @Override
    public List<Student> selectAll() {
        return List.of();
    }

    // TODO 9: save で登録し、登録後の Student を返す
    @Override
    public Student insert(Student student) {
        return null;
    }

    // TODO 10: findByAgeGreaterThanEqual を使う
    @Override
    public List<Student> selectByMinAge(int age) {
        return List.of();
    }
}
''',
}
w2_tests = {
    T + "W2StudentServiceTest.java": r'''package com.example.demo;

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
'''
}
P["w2-jpa"] = dict(answer=w2, start=w2_start, tests=w2_tests)

# =====================================================================
# w3-rest(Day7)
# =====================================================================
w3 = {}
w3[J + "DemoApplication.java"] = app_class("com.example.demo", "DemoApplication")
w3[R + "application.properties"] = H2_PROPS.replace("jdbc:h2:mem:school", "jdbc:h2:mem:users")
w3[R + "data.sql"] = r'''INSERT INTO USERS (NAME, EMAIL) VALUES ('佐藤 花子', 'hanako@example.com');
INSERT INTO USERS (NAME, EMAIL) VALUES ('鈴木 一郎', 'ichiro@example.com');
INSERT INTO USERS (NAME, EMAIL) VALUES ('高橋 美咲', 'misaki@example.com');
'''
w3[J + "entity/User.java"] = r'''package com.example.demo.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;

// USERS テーブルの1行(USER は多くの DB で予約語なので、テーブル名は USERS にしている)
@Entity
@Table(name = "USERS")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    private Integer id;

    @NotBlank(message = "名前は必須です")
    @Column(name = "NAME")
    private String name;

    @Column(name = "EMAIL")
    private String email;

    public User() {
    }

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
'''
w3[J + "dao/UserDao.java"] = r'''package com.example.demo.dao;

import com.example.demo.entity.User;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserDao extends JpaRepository<User, Integer> {
    // 名前の一部で検索する(WHERE NAME LIKE '%…%')
    List<User> findByNameContaining(String keyword);
}
'''
w3[J + "service/UserService.java"] = r'''package com.example.demo.service;

import com.example.demo.entity.User;
import java.util.List;

public interface UserService {
    User selectOne(int id);

    List<User> selectAll();

    List<User> search(String keyword);

    User insert(User user);

    // 更新。対象がなければ null
    User update(int id, User user);

    // 削除。削除できたら true、対象がなければ false
    boolean delete(int id);
}
'''
w3[J + "service/UserServiceImpl.java"] = r'''package com.example.demo.service;

import com.example.demo.dao.UserDao;
import com.example.demo.entity.User;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class UserServiceImpl implements UserService {
    private final UserDao userDao;

    public UserServiceImpl(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public User selectOne(int id) {
        return userDao.findById(id).orElse(null);
    }

    @Override
    public List<User> selectAll() {
        return userDao.findAll();
    }

    @Override
    public List<User> search(String keyword) {
        return userDao.findByNameContaining(keyword);
    }

    @Override
    public User insert(User user) {
        user.setId(null); // 新規登録なので、id は DB に振らせる
        return userDao.save(user);
    }

    @Override
    public User update(int id, User user) {
        if (!userDao.existsById(id)) {
            return null;
        }
        user.setId(id); // id があるので、save は INSERT ではなく UPDATE になる
        return userDao.save(user);
    }

    @Override
    public boolean delete(int id) {
        if (!userDao.existsById(id)) {
            return false;
        }
        userDao.deleteById(id);
        return true;
    }
}
'''
w3[J + "controller/UserController.java"] = r'''package com.example.demo.controller;

import com.example.demo.entity.User;
import com.example.demo.service.UserService;
import jakarta.validation.Valid;
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

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    // 全件取得:GET /api/users → 200
    @GetMapping
    public List<User> getAll() {
        return userService.selectAll();
    }

    // 名前で検索:GET /api/users/search?keyword=佐藤 → 200
    @GetMapping("/search")
    public List<User> search(@RequestParam String keyword) {
        return userService.search(keyword);
    }

    // 1件取得:GET /api/users/1 → 200(なければ 404)
    @GetMapping("/{id}")
    public ResponseEntity<User> getOne(@PathVariable int id) {
        User user = userService.selectOne(id);
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(user);
    }

    // 新規登録:POST /api/users → 201
    @PostMapping
    public ResponseEntity<User> create(@Valid @RequestBody User user) {
        User saved = userService.insert(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    // 更新:PUT /api/users/1 → 200(なければ 404)
    @PutMapping("/{id}")
    public ResponseEntity<User> update(@PathVariable int id, @Valid @RequestBody User user) {
        User updated = userService.update(id, user);
        if (updated == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }

    // 削除:DELETE /api/users/1 → 204(なければ 404)
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable int id) {
        if (!userService.delete(id)) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }
}
'''
w3[J + "controller/ErrorResponse.java"] = r'''package com.example.demo.controller;

// エラーのときに返す JSON:{"message": "…"}
public record ErrorResponse(String message) {
}
'''
w3[J + "controller/ApiExceptionHandler.java"] = r'''package com.example.demo.controller;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// どの Controller で起きた例外も、ここでまとめて受け止めて、エラーの JSON に変える
@RestControllerAdvice
public class ApiExceptionHandler {
    // 入力チェック(@Valid)に引っかかった → 400 Bad Request
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ErrorResponse badRequest(MethodArgumentNotValidException e) {
        return new ErrorResponse(e.getBindingResult().getFieldErrors().get(0).getDefaultMessage());
    }
}
'''
w3_start = {
    J + "controller/UserController.java": r'''package com.example.demo.controller;

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
''',
    J + "controller/ApiExceptionHandler.java": r'''package com.example.demo.controller;

import org.springframework.web.bind.MethodArgumentNotValidException;

// TODO 7: どの Controller の例外もまとめて受け止めるクラスにする(@RestControllerAdvice)
public class ApiExceptionHandler {
    // TODO 8: MethodArgumentNotValidException を受け止め、400 Bad Request と ErrorResponse を返す
    //         メッセージは e.getBindingResult().getFieldErrors().get(0).getDefaultMessage() で取れる
    public ErrorResponse badRequest(MethodArgumentNotValidException e) {
        return null;
    }
}
''',
}
w3_tests = {
    T + "W3UserApiTest.java": r'''package com.example.demo;

''' + MOCKMVC_IMPORTS + r'''
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
'''
}
P["w3-rest"] = dict(answer=w3, start=w3_start, tests=w3_tests)

# =====================================================================
# w4-form(Day8)
# =====================================================================
w4 = {}
w4[J + "DemoApplication.java"] = app_class("com.example.demo", "DemoApplication")
w4[R + "application.properties"] = "spring.application.name=demo\n"
w4[J + "form/MyForm.java"] = r'''package com.example.demo.form;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

// フォームの入力値を入れておくクラス。フィールド名はフォームの name 属性と同じにする
public class MyForm {
    @NotBlank(message = "名前を入力してください")
    private String name;

    @NotNull(message = "年齢を入力してください")
    @Min(value = 0, message = "年齢は0以上にしてください")
    @Max(value = 150, message = "年齢は150以下にしてください")
    private Integer age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
'''
w4[J + "controller/MyController.java"] = r'''package com.example.demo.controller;

import com.example.demo.form.MyForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class MyController {
    // 入力画面:空の MyForm を Model に入れて、form.html を表示する
    @GetMapping("/form")
    public String form(Model model) {
        model.addAttribute("myForm", new MyForm());
        return "form";
    }

    // 送信後:入力に誤りがあれば form.html に戻し、なければ result.html に結果を表示する
    @PostMapping("/form")
    public String submit(@Valid @ModelAttribute MyForm myForm, BindingResult result, Model model) {
        if (result.hasErrors()) {
            return "form";
        }
        model.addAttribute("message", myForm.getName() + "さん(" + myForm.getAge() + "歳)を受け付けました");
        return "result";
    }
}
'''
w4[R + "templates/form.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>入力</title>
</head>
<body>
<h1>入力</h1>
<form th:action="@{/form}" th:object="${myForm}" method="post">
    <p>
        <label>名前 <input type="text" th:field="*{name}"></label>
        <span th:if="${#fields.hasErrors('name')}" th:errors="*{name}">エラー</span>
    </p>
    <p>
        <label>年齢 <input type="number" th:field="*{age}"></label>
        <span th:if="${#fields.hasErrors('age')}" th:errors="*{age}">エラー</span>
    </p>
    <button type="submit">送信</button>
</form>
</body>
</html>
'''
w4[R + "templates/result.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>結果</title>
</head>
<body>
<h1>結果</h1>
<p th:text="${message}">ここに結果が入る</p>
<p><a th:href="@{/form}">入力に戻る</a></p>
</body>
</html>
'''
w4_start = {
    J + "form/MyForm.java": r'''package com.example.demo.form;

// フォームの入力値を入れておくクラス
public class MyForm {
    // TODO 1: 空なら「名前を入力してください」で弾く(@NotBlank)
    private String name;

    // TODO 2: 空なら「年齢を入力してください」(@NotNull)、0未満なら「年齢は0以上にしてください」(@Min)、
    //         150より大きければ「年齢は150以下にしてください」(@Max)で弾く
    private Integer age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
''',
    J + "controller/MyController.java": r'''package com.example.demo.controller;

import com.example.demo.form.MyForm;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;

@Controller
public class MyController {
    // TODO 3: GET /form で、空の MyForm を "myForm" という名前で Model に入れ、form.html を表示する
    public String form(Model model) {
        return "form";
    }

    // TODO 4: POST /form で MyForm を受け取って入力チェックし(@Valid @ModelAttribute)、
    //         誤りがあれば form.html に戻す。なければ Model に "message"(「田中さん(20歳)を受け付けました」の形)を入れ、result.html を表示する
    public String submit(MyForm myForm, BindingResult result, Model model) {
        return "form";
    }
}
''',
}
w4_tests = {
    T + "W4FormTest.java": r'''package com.example.demo;

''' + MOCKMVC_IMPORTS + r'''
// Day8:フォーム → Controller → Model → HTML の流れを確かめる
@SpringBootTest
@AutoConfigureMockMvc
class W4FormTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("GET /form:入力画面が表示される")
    void form() throws Exception {
        mockMvc.perform(get("/form"))
            .andExpect(status().isOk())
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("name=\"name\"")));
    }

    @Test
    @DisplayName("POST /form:正しく入力すると、結果の画面に表示される")
    void submit() throws Exception {
        mockMvc.perform(post("/form").param("name", "田中").param("age", "20"))
            .andExpect(status().isOk())
            .andExpect(view().name("result"))
            .andExpect(content().string(containsString("田中さん(20歳)を受け付けました")));
    }

    @Test
    @DisplayName("POST /form:名前が空なら入力画面に戻り、メッセージが出る")
    void nameBlank() throws Exception {
        mockMvc.perform(post("/form").param("name", "").param("age", "20"))
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("名前を入力してください")));
    }

    @Test
    @DisplayName("POST /form:年齢が範囲外なら入力画面に戻り、メッセージが出る")
    void ageOutOfRange() throws Exception {
        mockMvc.perform(post("/form").param("name", "田中").param("age", "200"))
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("年齢は150以下にしてください")));
        mockMvc.perform(post("/form").param("name", "田中").param("age", ""))
            .andExpect(view().name("form"))
            .andExpect(content().string(containsString("年齢を入力してください")));
    }
}
'''
}
P["w4-form"] = dict(answer=w4, start=w4_start, tests=w4_tests)

# =====================================================================
# e1〜e3:課題文から実装する演習
# =====================================================================
LJ = "src/main/java/com/example/library/"
LT = "src/test/java/com/example/library/"

E1_README = r'''# 演習1:書籍APIを作る(ArrayList)

## 課題文

図書室の本を管理する REST API を作成してください。今回は DB を使わず、**データはアプリの中の ArrayList に保存**します
(アプリを止めると消えてよい)。

本は次の項目を持ちます。

| 項目 | 型 | 説明 |
| --- | --- | --- |
| id | 整数 | 登録したときに 1, 2, 3 … と振る |
| title | 文字列 | 書名(必須) |
| author | 文字列 | 著者 |

次の API を実装してください。

| 操作 | メソッドとURL | 成功したとき | 失敗したとき |
| --- | --- | --- | --- |
| 一覧 | GET /api/books | 200 と本の配列(最初は空) | — |
| 1件 | GET /api/books/{id} | 200 と本 | ない id は 404 |
| 登録 | POST /api/books(JSON) | 201 と登録した本(id 付き) | title が空なら 400 |

## 進め方

第8部「課題文から実装する」の手順(扱うデータ → CRUD に分類 → 保存先 → ファイル → メソッド → 実装 → 確認)で進めてください。
パッケージは `com.example.library` の下に作ります(controller / service / entity など)。
`src/test` のテストがすべて通れば完成です。テストは HTTP のリクエストだけで確かめるので、クラス名は自由です。
'''

E2_README = r'''# 演習2:書籍APIを DB に置き換える(JPA)

## 課題文

演習1の書籍 API を、**H2 データベースに保存する形**に作り直し、更新と削除も追加してください。

テーブル名は `BOOK`、列は `ID`(自動採番の主キー)・`TITLE`・`AUTHOR` とします。最初のデータは `src/main/resources/data.sql`(用意済み)で入ります。

| 操作 | メソッドとURL | 成功したとき | 失敗したとき |
| --- | --- | --- | --- |
| 一覧 | GET /api/books | 200 と本の配列(最初は2冊) | — |
| 1件 | GET /api/books/{id} | 200 と本 | ない id は 404 |
| 登録 | POST /api/books(JSON) | 201 と登録した本(id 付き) | title が空なら 400 |
| 更新 | PUT /api/books/{id}(JSON) | 200 と更新後の本 | ない id は 404 |
| 削除 | DELETE /api/books/{id} | 204(本文なし) | ない id は 404 |

## 進め方

演習1のどのファイルを残し、どのファイルを書き換えるかを先に決めてから始めてください(Controller は、ほとんど変えなくて済むはずです)。
'''

E3_README = r'''# 演習3:会員登録フォームを作る(Thymeleaf)

## 課題文

カフェのメール会員の登録画面を作成してください。

- `GET /signup` で、名前(`name`)・メールアドレス(`email`)・年齢(`age`)の入力欄と「登録」ボタンのある画面を表示する
- `POST /signup` で入力を受け取り、次のチェックをする。誤りがあれば、入力画面にメッセージ付きで戻す

| 項目 | チェック | メッセージ |
| --- | --- | --- |
| name | 必須 | 名前を入力してください |
| email | メールアドレスの形 | メールアドレスの形式が正しくありません |
| age | 必須・18以上 | 18歳以上のみ登録できます |

- 誤りがなければ、完了画面に「登録しました:{名前}さん」と表示する(DB への保存は不要)

## 進め方

画面が2つ(入力・完了)あること、入力値を受け取る入れ物(フォームクラス)が要ることに注意して、必要なファイルを決めてから始めてください。
`src/test` のテストがすべて通れば完成です。
'''

e_tests_e1 = r'''package com.example.library;

''' + MOCKMVC_IMPORTS + r'''
import org.springframework.test.annotation.DirtiesContext;

// 演習1の採点テスト(HTTP のリクエストだけで確かめる。各テストの前にアプリを作り直すので、ArrayList は毎回空から始まる)
@SpringBootTest
@AutoConfigureMockMvc
@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)
class E1BookApiTest {
    @Autowired
    MockMvc mockMvc;

    private void register(String title, String author) throws Exception {
        mockMvc.perform(post("/api/books")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"title\": \"" + title + "\", \"author\": \"" + author + "\"}"));
    }

    @Test
    @DisplayName("一覧:最初は空の配列")
    void emptyAtFirst() throws Exception {
        mockMvc.perform(get("/api/books")).andExpect(status().isOk()).andExpect(jsonPath("$.length()").value(0));
    }

    @Test
    @DisplayName("登録:201 と、id=1 の振られた本")
    void create() throws Exception {
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"Java入門\", \"author\": \"山田 太郎\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.title").value("Java入門"));
    }

    @Test
    @DisplayName("登録して一覧・1件取得:id は 1, 2 と振られる。ない id は 404")
    void listAndGet() throws Exception {
        register("Java入門", "山田 太郎");
        register("SQLの基本", "佐藤 花子");
        mockMvc.perform(get("/api/books")).andExpect(jsonPath("$.length()").value(2));
        mockMvc.perform(get("/api/books/2")).andExpect(status().isOk()).andExpect(jsonPath("$.author").value("佐藤 花子"));
        mockMvc.perform(get("/api/books/99")).andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("登録:title が空なら 400")
    void createInvalid() throws Exception {
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"\", \"author\": \"山田 太郎\"}"))
            .andExpect(status().isBadRequest());
    }
}
'''

e_tests_e2 = r'''package com.example.library;

''' + MOCKMVC_IMPORTS + r'''
import org.springframework.transaction.annotation.Transactional;

// 演習2の採点テスト(HTTP のリクエストだけで確かめる)
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class E2BookDbApiTest {
    @Autowired
    MockMvc mockMvc;

    @Test
    @DisplayName("一覧:data.sql の2冊")
    void list() throws Exception {
        mockMvc.perform(get("/api/books")).andExpect(status().isOk()).andExpect(jsonPath("$.length()").value(2));
    }

    @Test
    @DisplayName("1件:200、ない id は 404")
    void getOne() throws Exception {
        mockMvc.perform(get("/api/books/1")).andExpect(status().isOk()).andExpect(jsonPath("$.title").value("Java入門"));
        mockMvc.perform(get("/api/books/99")).andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("登録:201 と id=3、title が空なら 400")
    void create() throws Exception {
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"Spring Boot入門\", \"author\": \"鈴木 一郎\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(3));
        mockMvc.perform(post("/api/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"\", \"author\": \"鈴木 一郎\"}"))
            .andExpect(status().isBadRequest());
        mockMvc.perform(get("/api/books")).andExpect(jsonPath("$.length()").value(3));
    }

    @Test
    @DisplayName("更新:200、ない id は 404")
    void update() throws Exception {
        mockMvc.perform(put("/api/books/2")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"SQLの基本 第2版\", \"author\": \"佐藤 花子\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.title").value("SQLの基本 第2版"));
        mockMvc.perform(get("/api/books/2")).andExpect(jsonPath("$.title").value("SQLの基本 第2版"));
        mockMvc.perform(put("/api/books/99")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"title\": \"だれか\", \"author\": \"だれか\"}"))
            .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("削除:204、ない id は 404")
    void deleteBook() throws Exception {
        mockMvc.perform(delete("/api/books/1")).andExpect(status().isNoContent());
        mockMvc.perform(get("/api/books/1")).andExpect(status().isNotFound());
        mockMvc.perform(delete("/api/books/1")).andExpect(status().isNotFound());
    }
}
'''

SJ = "src/main/java/com/example/signup/"
ST = "src/test/java/com/example/signup/"
e_tests_e3 = r'''package com.example.signup;

''' + MOCKMVC_IMPORTS + r'''
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
'''

# ----- e1 解答 -----
e1 = {}
e1[LJ + "LibraryApplication.java"] = app_class("com.example.library", "LibraryApplication")
e1[R + "application.properties"] = "spring.application.name=library\n"
e1[LJ + "entity/Book.java"] = r'''package com.example.library.entity;

import jakarta.validation.constraints.NotBlank;

// 本(今回は DB を使わないので、@Entity は付けない)
public class Book {
    private Integer id;

    @NotBlank(message = "書名は必須です")
    private String title;

    private String author;

    public Book() {
    }

    public Book(Integer id, String title, String author) {
        this.id = id;
        this.title = title;
        this.author = author;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
}
'''
e1[LJ + "service/BookService.java"] = r'''package com.example.library.service;

import com.example.library.entity.Book;
import java.util.List;

public interface BookService {
    List<Book> selectAll();

    Book selectOne(int id);

    Book insert(Book book);
}
'''
e1[LJ + "service/BookServiceImpl.java"] = r'''package com.example.library.service;

import com.example.library.entity.Book;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

// 保存先は ArrayList(DB を使わない)。Bean は1つだけ作られるので、アプリが動いている間は中身が残る
@Service
public class BookServiceImpl implements BookService {
    private final List<Book> books = new ArrayList<>();
    private int nextId = 1;

    @Override
    public List<Book> selectAll() {
        return books;
    }

    @Override
    public Book selectOne(int id) {
        for (Book book : books) {
            if (book.getId() == id) {
                return book;
            }
        }
        return null;
    }

    @Override
    public Book insert(Book book) {
        book.setId(nextId);
        nextId++;
        books.add(book);
        return book;
    }
}
'''
e1[LJ + "controller/BookController.java"] = r'''package com.example.library.controller;

import com.example.library.entity.Book;
import com.example.library.service.BookService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/books")
public class BookController {
    private final BookService bookService;

    public BookController(BookService bookService) {
        this.bookService = bookService;
    }

    @GetMapping
    public List<Book> getAll() {
        return bookService.selectAll();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Book> getOne(@PathVariable int id) {
        Book book = bookService.selectOne(id);
        if (book == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(book);
    }

    @PostMapping
    public ResponseEntity<Book> create(@Valid @RequestBody Book book) {
        return ResponseEntity.status(HttpStatus.CREATED).body(bookService.insert(book));
    }
}
'''
P["e1-book-arraylist"] = dict(
    answer=e1,
    start_only={
        LJ + "LibraryApplication.java": e1[LJ + "LibraryApplication.java"],
        R + "application.properties": e1[R + "application.properties"],
        "README.md": E1_README,
    },
    tests={LT + "E1BookApiTest.java": e_tests_e1},
    readme=E1_README,
)

# ----- e2 解答 -----
e2 = {}
e2[LJ + "LibraryApplication.java"] = app_class("com.example.library", "LibraryApplication")
e2[R + "application.properties"] = H2_PROPS.replace("spring.application.name=demo", "spring.application.name=library").replace("jdbc:h2:mem:school", "jdbc:h2:mem:library")
e2[R + "data.sql"] = r'''INSERT INTO BOOK (TITLE, AUTHOR) VALUES ('Java入門', '山田 太郎');
INSERT INTO BOOK (TITLE, AUTHOR) VALUES ('SQLの基本', '佐藤 花子');
'''
e2[LJ + "entity/Book.java"] = r'''package com.example.library.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotBlank;

// 演習1の Book に、DB と対応させるアノテーションを足した
@Entity
@Table(name = "BOOK")
public class Book {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    private Integer id;

    @NotBlank(message = "書名は必須です")
    @Column(name = "TITLE")
    private String title;

    @Column(name = "AUTHOR")
    private String author;

    public Book() {
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }
}
'''
e2[LJ + "dao/BookDao.java"] = r'''package com.example.library.dao;

import com.example.library.entity.Book;
import org.springframework.data.jpa.repository.JpaRepository;

public interface BookDao extends JpaRepository<Book, Integer> {
}
'''
e2[LJ + "service/BookService.java"] = r'''package com.example.library.service;

import com.example.library.entity.Book;
import java.util.List;

public interface BookService {
    List<Book> selectAll();

    Book selectOne(int id);

    Book insert(Book book);

    Book update(int id, Book book);

    boolean delete(int id);
}
'''
e2[LJ + "service/BookServiceImpl.java"] = r'''package com.example.library.service;

import com.example.library.dao.BookDao;
import com.example.library.entity.Book;
import java.util.List;
import org.springframework.stereotype.Service;

// 保存先を ArrayList から DB(BookDao)に置き換えた。BookService の約束は同じなので、Controller はそのまま使える
@Service
public class BookServiceImpl implements BookService {
    private final BookDao bookDao;

    public BookServiceImpl(BookDao bookDao) {
        this.bookDao = bookDao;
    }

    @Override
    public List<Book> selectAll() {
        return bookDao.findAll();
    }

    @Override
    public Book selectOne(int id) {
        return bookDao.findById(id).orElse(null);
    }

    @Override
    public Book insert(Book book) {
        book.setId(null);
        return bookDao.save(book);
    }

    @Override
    public Book update(int id, Book book) {
        if (!bookDao.existsById(id)) {
            return null;
        }
        book.setId(id);
        return bookDao.save(book);
    }

    @Override
    public boolean delete(int id) {
        if (!bookDao.existsById(id)) {
            return false;
        }
        bookDao.deleteById(id);
        return true;
    }
}
'''
e2[LJ + "controller/BookController.java"] = e1[LJ + "controller/BookController.java"].replace(
    "import org.springframework.web.bind.annotation.GetMapping;",
    "import org.springframework.web.bind.annotation.DeleteMapping;\nimport org.springframework.web.bind.annotation.GetMapping;",
).replace(
    "import org.springframework.web.bind.annotation.PostMapping;",
    "import org.springframework.web.bind.annotation.PostMapping;\nimport org.springframework.web.bind.annotation.PutMapping;",
).replace(
    '''    @PostMapping
    public ResponseEntity<Book> create(@Valid @RequestBody Book book) {
        return ResponseEntity.status(HttpStatus.CREATED).body(bookService.insert(book));
    }
}''',
    '''    @PostMapping
    public ResponseEntity<Book> create(@Valid @RequestBody Book book) {
        return ResponseEntity.status(HttpStatus.CREATED).body(bookService.insert(book));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Book> update(@PathVariable int id, @Valid @RequestBody Book book) {
        Book updated = bookService.update(id, book);
        if (updated == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable int id) {
        if (!bookService.delete(id)) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }
}''',
)
P["e2-book-db"] = dict(
    answer=e2,
    start_only={
        LJ + "LibraryApplication.java": e2[LJ + "LibraryApplication.java"],
        R + "application.properties": e2[R + "application.properties"],
        R + "data.sql": e2[R + "data.sql"],
        "README.md": E2_README,
    },
    tests={LT + "E2BookDbApiTest.java": e_tests_e2},
    readme=E2_README,
)

# ----- e3 解答 -----
e3 = {}
e3[SJ + "SignupApplication.java"] = app_class("com.example.signup", "SignupApplication")
e3[R + "application.properties"] = "spring.application.name=signup\n"
e3[SJ + "form/SignupForm.java"] = r'''package com.example.signup.form;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public class SignupForm {
    @NotBlank(message = "名前を入力してください")
    private String name;

    @Email(message = "メールアドレスの形式が正しくありません")
    private String email;

    @NotNull(message = "18歳以上のみ登録できます")
    @Min(value = 18, message = "18歳以上のみ登録できます")
    private Integer age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
'''
e3[SJ + "controller/SignupController.java"] = r'''package com.example.signup.controller;

import com.example.signup.form.SignupForm;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class SignupController {
    @GetMapping("/signup")
    public String form(Model model) {
        model.addAttribute("signupForm", new SignupForm());
        return "signup";
    }

    @PostMapping("/signup")
    public String submit(@Valid @ModelAttribute SignupForm signupForm, BindingResult result, Model model) {
        if (result.hasErrors()) {
            return "signup";
        }
        model.addAttribute("name", signupForm.getName());
        return "signup-complete";
    }
}
'''
e3[R + "templates/signup.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>会員登録</title>
</head>
<body>
<h1>会員登録</h1>
<form th:action="@{/signup}" th:object="${signupForm}" method="post">
    <p>
        <label>名前 <input type="text" th:field="*{name}"></label>
        <span th:if="${#fields.hasErrors('name')}" th:errors="*{name}">エラー</span>
    </p>
    <p>
        <label>メールアドレス <input type="text" th:field="*{email}"></label>
        <span th:if="${#fields.hasErrors('email')}" th:errors="*{email}">エラー</span>
    </p>
    <p>
        <label>年齢 <input type="number" th:field="*{age}"></label>
        <span th:if="${#fields.hasErrors('age')}" th:errors="*{age}">エラー</span>
    </p>
    <button type="submit">登録</button>
</form>
</body>
</html>
'''
e3[R + "templates/signup-complete.html"] = r'''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>登録完了</title>
</head>
<body>
<h1>登録完了</h1>
<p th:text="'登録しました:' + ${name} + 'さん'">登録しました</p>
</body>
</html>
'''
P["e3-signup-form"] = dict(
    answer=e3,
    start_only={
        SJ + "SignupApplication.java": e3[SJ + "SignupApplication.java"],
        R + "application.properties": e3[R + "application.properties"],
        "README.md": E3_README,
    },
    tests={ST + "E3SignupFormTest.java": e_tests_e3},
    readme=E3_README,
)


# =====================================================================
def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def copy_base(dest, artifact):
    os.makedirs(dest, exist_ok=True)
    for name in ["mvnw", "mvnw.cmd"]:
        shutil.copy(os.path.join(BASE, name), os.path.join(dest, name))
    shutil.copytree(os.path.join(BASE, ".mvn"), os.path.join(dest, ".mvn"), dirs_exist_ok=True)
    pom = open(os.path.join(BASE, "pom.xml"), encoding="utf-8").read()
    pom = pom.replace("<artifactId>cafe</artifactId>", f"<artifactId>{artifact}</artifactId>").replace("<name>cafe</name>", f"<name>{artifact}</name>")
    write(os.path.join(dest, "pom.xml"), pom)


for old in ["w1-spring", "w2-thymeleaf", "w3-rest", "w4-database"]:
    for d in (os.path.join(ROOT, "web", old), os.path.join(ROOT, "answers", "web", old)):
        if os.path.exists(d):
            shutil.rmtree(d)

for name, proj in P.items():
    artifact = name.split("-", 1)[1]
    start_dir = os.path.join(ROOT, "web", name)
    answer_dir = os.path.join(ROOT, "answers", "web", name)
    for d in (start_dir, answer_dir):
        if os.path.exists(d):
            shutil.rmtree(d)
        copy_base(d, artifact)
    if "start_only" in proj:
        start = dict(proj["start_only"])
    else:
        start = dict(proj["answer"])
        start.update(proj["start"])
    answer = dict(proj["answer"])
    if "readme" in proj:
        answer["README.md"] = proj["readme"]
    for path, content in {**start, **proj["tests"]}.items():
        write(os.path.join(start_dir, path), content)
    for path, content in {**answer, **proj["tests"]}.items():
        write(os.path.join(answer_dir, path), content)
    print("wrote", name)
