# 課題リポジトリ web/ の Spring Boot の課題(第4部 基礎・第5部 応用)を作る。
#   python tools/gen_web.py <リポジトリのルート> <initializr で作ったプロジェクト(pom・mvnwの元)>
#
# 1つの User アプリを、ステップごとに育てる(研修 Day4〜8 に対応)。
#   s1-hello  … Controller で文字を返す(Day4)
#   s2-layers … Model・Service・ServiceImpl(ArrayList)・Controller の層で、全件取得と1件取得
#   s3-crud   … 登録・更新・削除を足して CRUD の5つの操作(GET 全件・GET 1件・POST・PUT・DELETE)
#   s4-db     … ServiceImpl を DB 版(Entity・DAO)に差し替える。Controller は変えない(Day5〜7)
#   s5-errors … 入力チェック(400)・エラーの JSON・メソッド名で検索
#   s6-view   … Thymeleaf の一覧画面と登録フォーム(Day8)
#   e1〜e3    … 第5部「課題文から実装する」の演習(README の課題文だけを渡し、ファイルは自分で作る)
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
# User アプリを s1〜s6 で育てる(第4部 基礎 → 第5部 応用)
#   各ステップの開始コードは「前のステップの解答」に、そのステップの TODO 入りのファイルを重ねたもの
# =====================================================================
APP = {J + "DemoApplication.java": app_class("com.example.demo", "DemoApplication")}
PLAIN_PROPS = {R + "application.properties": "spring.application.name=demo\n"}
DB_PROPS = {R + "application.properties": H2_PROPS.replace("jdbc:h2:mem:school", "jdbc:h2:mem:users")}

USER_DATA_SQL = '''INSERT INTO USERS (NAME, EMAIL, AGE) VALUES ('佐藤 花子', 'hanako@example.com', 20);
INSERT INTO USERS (NAME, EMAIL, AGE) VALUES ('鈴木 一郎', 'ichiro@example.com', 22);
INSERT INTO USERS (NAME, EMAIL, AGE) VALUES ('高橋 美咲', 'misaki@example.com', 19);
'''

USER_ACCESSORS = '''    public Integer getId() {
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

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }
}
'''

USER_CONSTRUCTORS = '''    // 引数なしのコンストラクタ(JSON や DB から User を作るときに使われる)
    public User() {
    }

    public User(String name, String email, Integer age) {
        this.name = name;
        this.email = email;
        this.age = age;
    }

'''


def test_class(name, comment, annotations, body, extra_imports=""):
    return f'''package com.example.demo;

{MOCKMVC_IMPORTS}{extra_imports}
// {comment}
@SpringBootTest
@AutoConfigureMockMvc
{annotations}class {name} {{
    @Autowired
    MockMvc mockMvc;
{body}}}
'''


# ------------------------------- s1-hello(第4部「最初の一歩」・研修 Day4) -------------------------------
s1 = {
    **APP,
    **PLAIN_PROPS,
    J + "controller/HelloController.java": '''package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// 文字をそのまま返す Controller(リクエストの窓口)
@RestController
public class HelloController {
    // GET /hello → 「Hello, Spring Boot!」
    @GetMapping("/hello")
    public String hello() {
        return "Hello, Spring Boot!";
    }

    // GET /hello/田中 → 「こんにちは、田中さん」
    @GetMapping("/hello/{name}")
    public String helloName(@PathVariable String name) {
        return "こんにちは、" + name + "さん";
    }
}
''',
}
s1_start = {
    J + "controller/HelloController.java": '''package com.example.demo.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// TODO 1: このクラスを、文字をそのまま返す Controller にする(@RestController)
public class HelloController {
    // TODO 2: GET /hello で「Hello, Spring Boot!」を返す(@GetMapping)
    public String hello() {
        return "";
    }

    // TODO 3: GET /hello/{name} で、URL の {name} の部分を受け取り(@PathVariable)、「こんにちは、〇〇さん」を返す
    public String helloName(String name) {
        return "";
    }
}
''',
}
s1_tests = {
    T + "S1HelloTest.java": test_class(
        "S1HelloTest",
        "s1:Controller で文字を返す",
        "",
        '''
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
''',
    )
}
P["s1-hello"] = dict(answer=s1, start=s1_start, tests=s1_tests)

# ------------------------------- s2-layers(第4部「層をつくる」:全件・1件取得) -------------------------------
S2_USER = '''package com.example.demo.model;

// ユーザー1人分のデータ(Model)。id・名前・メールアドレス・年齢を持つ
public class User {
    private Integer id;
    private String name;
    private String email;
    private Integer age;

''' + USER_CONSTRUCTORS + USER_ACCESSORS

S2_SERVICE = '''package com.example.demo.service;

import com.example.demo.model.User;
import java.util.List;

// ユーザーを扱う処理の「約束」(インターフェース)。Controller はこの約束だけを知っている
public interface UserService {
    // 全件取得
    List<User> selectAll();

    // 1件取得(見つからなければ null)
    User selectOne(int id);
}
'''

ARRAYLIST_HEAD = '''package com.example.demo.service;

import com.example.demo.model.User;
import java.util.ArrayList;
import java.util.List;
import org.springframework.stereotype.Service;

// UserService の中身。データはアプリの中の ArrayList に入れておく(アプリを止めると最初の3人に戻る)
{ann}public class UserServiceImpl implements UserService {{
    private final List<User> users = new ArrayList<>();
    private int nextId = 1;

    // 最初のデータを3人分入れておく
    public UserServiceImpl() {{
        add(new User("佐藤 花子", "hanako@example.com", 20));
        add(new User("鈴木 一郎", "ichiro@example.com", 22));
        add(new User("高橋 美咲", "misaki@example.com", 19));
    }}

    // id を振ってリストに追加する
    private User add(User user) {{
        user.setId(nextId);
        nextId++;
        users.add(user);
        return user;
    }}
'''

S2_IMPL_READ = '''
    @Override
    public List<User> selectAll() {
        return users;
    }

    @Override
    public User selectOne(int id) {
        for (User user : users) {
            if (user.getId() == id) {
                return user;
            }
        }
        return null;
    }
'''

CONTROLLER_IMPORTS = '''package com.example.demo.controller;

import com.example.demo.model.User;
import com.example.demo.service.UserService;
{valid}import java.util.List;
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
'''

CONTROLLER_HEAD = '''
// /api/users へのリクエストを受ける Controller。処理は UserService に頼む
@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserService userService;

    // コンストラクタインジェクション:UserService の中身(UserServiceImpl)は Spring が渡してくれる
    public UserController(UserService userService) {
        this.userService = userService;
    }
'''

CONTROLLER_READ = '''
    // 全件取得:GET /api/users → 200
    @GetMapping
    public List<User> getAll() {
        return userService.selectAll();
    }

    // 1件取得:GET /api/users/1 → 200(いなければ 404)
    @GetMapping("/{id}")
    public ResponseEntity<User> getOne(@PathVariable int id) {
        User user = userService.selectOne(id);
        if (user == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(user);
    }
'''


def controller_write(valid):
    v = "@Valid " if valid else ""
    return f'''
    // 登録:POST /api/users → 201
    @PostMapping
    public ResponseEntity<User> create({v}@RequestBody User user) {{
        User saved = userService.insert(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }}

    // 更新:PUT /api/users/1 → 200(いなければ 404)
    @PutMapping("/{{id}}")
    public ResponseEntity<User> update(@PathVariable int id, {v}@RequestBody User user) {{
        User updated = userService.update(id, user);
        if (updated == null) {{
            return ResponseEntity.notFound().build();
        }}
        return ResponseEntity.ok(updated);
    }}

    // 削除:DELETE /api/users/1 → 204(いなければ 404)
    @DeleteMapping("/{{id}}")
    public ResponseEntity<Void> delete(@PathVariable int id) {{
        if (!userService.delete(id)) {{
            return ResponseEntity.notFound().build();
        }}
        return ResponseEntity.noContent().build();
    }}
'''


s2 = {
    **APP,
    **PLAIN_PROPS,
    J + "model/User.java": S2_USER,
    J + "service/UserService.java": S2_SERVICE,
    J + "service/UserServiceImpl.java": ARRAYLIST_HEAD.format(ann="@Service\n") + S2_IMPL_READ + "}\n",
    J + "controller/UserController.java": CONTROLLER_IMPORTS.format(valid="") + CONTROLLER_HEAD + CONTROLLER_READ + "}\n",
}
s2_start = {
    J + "service/UserServiceImpl.java": ARRAYLIST_HEAD.format(
        ann="// TODO 1: Spring に部品(Bean)として登録するアノテーションを付ける(@Service)\n"
    )
    + '''
    // TODO 2: users をそのまま返す
    @Override
    public List<User> selectAll() {
        return List.of();
    }

    // TODO 3: users の中から id が一致する User を探して返す。見つからなければ null
    @Override
    public User selectOne(int id) {
        return null;
    }
}
''',
    J + "controller/UserController.java": CONTROLLER_IMPORTS.format(valid="")
    + '''
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
''',
}

READ_TESTS = '''
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
'''

WRITE_TESTS = '''
    @Test
    @DisplayName("POST /api/users:登録すると 201 と、id の振られた User。一覧が4人になる")
    void create() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\\"name\\": \\"田中 健\\", \\"email\\": \\"ken@example.com\\", \\"age\\": 21}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(4))
            .andExpect(jsonPath("$.name").value("田中 健"));
        mockMvc.perform(get("/api/users")).andExpect(jsonPath("$.length()").value(4));
    }

    @Test
    @DisplayName("PUT /api/users/{id}:更新(200)、いなければ 404")
    void update() throws Exception {
        mockMvc.perform(put("/api/users/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\\"name\\": \\"佐藤 花子\\", \\"email\\": \\"hanako.new@example.com\\", \\"age\\": 21}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.email").value("hanako.new@example.com"));
        mockMvc.perform(get("/api/users/1")).andExpect(jsonPath("$.age").value(21));
        mockMvc.perform(put("/api/users/99")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\\"name\\": \\"だれか\\", \\"email\\": \\"x@example.com\\", \\"age\\": 30}"))
            .andExpect(status().isNotFound());
    }

    @Test
    @DisplayName("DELETE /api/users/{id}:削除は 204、いなければ 404")
    void deleteUser() throws Exception {
        mockMvc.perform(delete("/api/users/3")).andExpect(status().isNoContent());
        mockMvc.perform(get("/api/users/3")).andExpect(status().isNotFound());
        mockMvc.perform(delete("/api/users/99")).andExpect(status().isNotFound());
    }
'''

DIRTIES = "@DirtiesContext(classMode = DirtiesContext.ClassMode.BEFORE_EACH_TEST_METHOD)\n"
DIRTIES_IMPORT = "import org.springframework.test.annotation.DirtiesContext;\n"
TX = "@Transactional\n"
TX_IMPORT = "import org.springframework.transaction.annotation.Transactional;\n"

s2_tests = {
    T + "S2LayersTest.java": test_class(
        "S2LayersTest",
        "s2:Controller → Service → ServiceImpl の層で、全件取得と1件取得",
        "",
        '''
    @Autowired
    UserService userService;

    @Test
    @DisplayName("UserService:Spring が UserServiceImpl を渡してくれる")
    void service() {
        assertEquals("UserServiceImpl", userService.getClass().getSimpleName());
    }
''' + READ_TESTS,
        "import static org.junit.jupiter.api.Assertions.assertEquals;\n\nimport com.example.demo.service.UserService;\n",
    )
}
P["s2-layers"] = dict(answer=s2, start=s2_start, tests=s2_tests)

# ------------------------------- s3-crud(第4部「CRUD 5操作」:登録・更新・削除) -------------------------------
S3_SERVICE = '''package com.example.demo.service;

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
'''

S3_IMPL_WRITE = '''
    @Override
    public User insert(User user) {
        return add(user); // id は add の中で振る
    }

    @Override
    public User update(int id, User user) {
        User target = selectOne(id);
        if (target == null) {
            return null;
        }
        target.setName(user.getName());
        target.setEmail(user.getEmail());
        target.setAge(user.getAge());
        return target;
    }

    @Override
    public boolean delete(int id) {
        User target = selectOne(id);
        if (target == null) {
            return false;
        }
        users.remove(target);
        return true;
    }
'''

s3 = {
    **s2,
    J + "service/UserService.java": S3_SERVICE,
    J + "service/UserServiceImpl.java": ARRAYLIST_HEAD.format(ann="@Service\n") + S2_IMPL_READ + S3_IMPL_WRITE + "}\n",
    J + "controller/UserController.java": CONTROLLER_IMPORTS.format(valid="")
    + CONTROLLER_HEAD
    + CONTROLLER_READ
    + controller_write(False)
    + "}\n",
}
s3_start = {
    J + "service/UserServiceImpl.java": ARRAYLIST_HEAD.format(ann="@Service\n")
    + S2_IMPL_READ
    + '''
    // TODO 1: add を使って登録し、登録後の User を返す
    @Override
    public User insert(User user) {
        return null;
    }

    // TODO 2: id の User を探し、いなければ null。いれば name・email・age を書き換えて返す
    @Override
    public User update(int id, User user) {
        return null;
    }

    // TODO 3: id の User を探し、いなければ false。いれば users から取り除いて true
    @Override
    public boolean delete(int id) {
        return false;
    }
}
''',
    J + "controller/UserController.java": CONTROLLER_IMPORTS.format(valid="")
    + CONTROLLER_HEAD
    + CONTROLLER_READ
    + '''
    // TODO 4: POST /api/users で JSON を受け取って(@PostMapping・@RequestBody)登録し、201 Created と登録後の User を返す
    public ResponseEntity<User> create(User user) {
        return null;
    }

    // TODO 5: PUT /api/users/{id} で更新し(@PutMapping)、200 と更新後の User を返す。いなければ 404
    public ResponseEntity<User> update(int id, User user) {
        return null;
    }

    // TODO 6: DELETE /api/users/{id} で削除し(@DeleteMapping)、204 No Content を返す。いなければ 404
    public ResponseEntity<Void> delete(int id) {
        return null;
    }
}
''',
}
s3_tests = {
    T + "S3CrudTest.java": test_class(
        "S3CrudTest",
        "s3:CRUD の5つの操作(ArrayList)。テストごとにアプリを作り直し、最初の3人から始める",
        DIRTIES,
        READ_TESTS + WRITE_TESTS,
        DIRTIES_IMPORT,
    )
}
P["s3-crud"] = dict(answer=s3, start=s3_start, tests=s3_tests)

# ------------------------------- s4-db(第4部「DBにつなぐ」:ServiceImpl を差し替える) -------------------------------
def entity_user(name_ann):
    return '''package com.example.demo.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
''' + ("import jakarta.validation.constraints.NotBlank;\n" if name_ann else "") + '''
// ユーザー1人分のデータ(Model)。@Entity を付けたので、USERS テーブルの1行と対応する
// (USER は多くの DB で予約語なので、テーブル名は USERS にしている)
@Entity
@Table(name = "USERS")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ID")
    private Integer id;

''' + name_ann + '''    @Column(name = "NAME")
    private String name;

    @Column(name = "EMAIL")
    private String email;

    @Column(name = "AGE")
    private Integer age;

''' + USER_CONSTRUCTORS + USER_ACCESSORS


S4_DAO = '''package com.example.demo.dao;

import com.example.demo.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

// DB を操作する DAO。JpaRepository を継承するだけで findAll・findById・save・deleteById などが使える
public interface UserDao extends JpaRepository<User, Integer> {
}
'''

DB_IMPL = '''package com.example.demo.service;

import com.example.demo.dao.UserDao;
import com.example.demo.model.User;
import java.util.List;
import org.springframework.stereotype.Service;

// UserService の中身(DB 版)。ArrayList の代わりに UserDao を使う。Controller は変えなくてよい
@Service
public class UserServiceImpl implements UserService {
    private final UserDao userDao;

    public UserServiceImpl(UserDao userDao) {
        this.userDao = userDao;
    }

    @Override
    public List<User> selectAll() {
        return userDao.findAll();
    }

    @Override
    public User selectOne(int id) {
        // findById は Optional(中身があるかもしれない箱)を返す。見つからなければ null にする
        return userDao.findById(id).orElse(null);
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
'''

s4 = {
    **s3,
    **DB_PROPS,
    R + "data.sql": USER_DATA_SQL,
    J + "model/User.java": entity_user(""),
    J + "dao/UserDao.java": S4_DAO,
    J + "service/UserServiceImpl.java": DB_IMPL + "}\n",
}
s4_start = {
    J + "model/User.java": '''package com.example.demo.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

// TODO 1: USERS テーブルの1行と対応する Entity にする(@Entity・@Table(name = "USERS"))
public class User {
    // TODO 2: 主キーにする(@Id・@GeneratedValue(strategy = GenerationType.IDENTITY)・@Column(name = "ID"))
    private Integer id;

    // TODO 3: 列名を指定する(@Column)。NAME・EMAIL・AGE
    private String name;

    private String email;

    private Integer age;

''' + USER_CONSTRUCTORS + USER_ACCESSORS,
    J + "dao/UserDao.java": '''package com.example.demo.dao;

import com.example.demo.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

// TODO 4: JpaRepository<User, Integer> を継承する
public interface UserDao {
}
''',
    J + "service/UserServiceImpl.java": '''package com.example.demo.service;

import com.example.demo.dao.UserDao;
import com.example.demo.model.User;
import java.util.List;
import org.springframework.stereotype.Service;

// UserService の中身を DB 版に作り直す。ArrayList は使わない。Controller は変えなくてよい
@Service
public class UserServiceImpl implements UserService {
    // TODO 5: UserDao をフィールドで持ち、コンストラクタで受け取る

    // TODO 6: findAll で全件を返す
    @Override
    public List<User> selectAll() {
        return List.of();
    }

    // TODO 7: findById で探し、見つからなければ null(Optional の orElse を使う)
    @Override
    public User selectOne(int id) {
        return null;
    }

    // TODO 8: id を null にしてから save する(id は DB に振らせる)
    @Override
    public User insert(User user) {
        return null;
    }

    // TODO 9: existsById でいなければ null。いれば id を入れてから save(UPDATE になる)
    @Override
    public User update(int id, User user) {
        return null;
    }

    // TODO 10: existsById でいなければ false。いれば deleteById して true
    @Override
    public boolean delete(int id) {
        return false;
    }
}
''',
}
s4_tests = {
    T + "S4DbTest.java": test_class(
        "S4DbTest",
        "s4:DB 版でも CRUD の5つの操作が同じように動く(テストが終わると DB の変更は取り消される)",
        TX,
        READ_TESTS + WRITE_TESTS,
        TX_IMPORT,
    )
}
P["s4-db"] = dict(answer=s4, start=s4_start, tests=s4_tests)

# ------------------------------- s5-errors(第5部「エラーとレスポンス」「DBをもっと」:入力チェック・検索) -------------------------------
S5_DAO = '''package com.example.demo.dao;

import com.example.demo.model.User;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

// DB を操作する DAO。JpaRepository を継承するだけで findAll・findById・save・deleteById などが使える
public interface UserDao extends JpaRepository<User, Integer> {
    // 名前の一部で検索する(メソッド名から WHERE NAME LIKE '%…%' の SQL が作られる)
    List<User> findByNameContaining(String keyword);
}
'''

S5_SERVICE = S3_SERVICE.replace('''    // 登録(id を振って''', '''    // 名前の一部で検索
    List<User> search(String keyword);

    // 登録(id を振って''')

S5_IMPL_SEARCH = '''
    @Override
    public List<User> search(String keyword) {
        return userDao.findByNameContaining(keyword);
    }
'''

CONTROLLER_SEARCH = '''
    // 名前で検索:GET /api/users/search?keyword=佐藤 → 200
    @GetMapping("/search")
    public List<User> search(@RequestParam String keyword) {
        return userService.search(keyword);
    }
'''

ERROR_RESPONSE = '''package com.example.demo.controller;

// エラーのときに返す JSON:{"message": "…"}
public record ErrorResponse(String message) {
}
'''

API_HANDLER = '''package com.example.demo.controller;

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

s5 = {
    **s4,
    J + "model/User.java": entity_user('    @NotBlank(message = "名前は必須です")\n'),
    J + "dao/UserDao.java": S5_DAO,
    J + "service/UserService.java": S5_SERVICE,
    J + "service/UserServiceImpl.java": DB_IMPL + S5_IMPL_SEARCH + "}\n",
    J + "controller/UserController.java": CONTROLLER_IMPORTS.format(valid="import jakarta.validation.Valid;\n")
    + CONTROLLER_HEAD
    + CONTROLLER_READ
    + CONTROLLER_SEARCH
    + controller_write(True)
    + "}\n",
    J + "controller/ErrorResponse.java": ERROR_RESPONSE,
    J + "controller/ApiExceptionHandler.java": API_HANDLER,
}
s5_start = {
    J + "model/User.java": entity_user(
        '    // TODO 1: 空なら「名前は必須です」で弾く(@NotBlank(message = "…"))\n'
    ),
    J + "dao/UserDao.java": S4_DAO.replace(
        "public interface UserDao extends JpaRepository<User, Integer> {\n",
        "// TODO 2: 名前の一部で検索するメソッド findByNameContaining(String keyword) を宣言する(List<User> を返す)\n"
        "public interface UserDao extends JpaRepository<User, Integer> {\n",
    ),
    J + "service/UserServiceImpl.java": DB_IMPL
    + '''
    // TODO 3: UserDao の findByNameContaining を使う
    @Override
    public List<User> search(String keyword) {
        return List.of();
    }
}
''',
    J + "controller/UserController.java": CONTROLLER_IMPORTS.format(valid="import jakarta.validation.Valid;\n")
    + CONTROLLER_HEAD
    + CONTROLLER_READ
    + '''
    // TODO 4: GET /api/users/search?keyword=… で、名前に keyword を含む人を返す(@GetMapping・@RequestParam)
    public List<User> search(String keyword) {
        return List.of();
    }
'''
    + controller_write(False).replace(
        "    // 登録:POST /api/users → 201\n",
        "    // TODO 5: 登録と更新の User に @Valid を付けて、User の @NotBlank をチェックさせる\n    // 登録:POST /api/users → 201\n",
    )
    + "}\n",
    J + "controller/ApiExceptionHandler.java": '''package com.example.demo.controller;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

// TODO 6: どの Controller の例外もまとめて受け止めるクラスにする(@RestControllerAdvice)
public class ApiExceptionHandler {
    // TODO 7: MethodArgumentNotValidException を受け止め(@ExceptionHandler)、400 Bad Request(@ResponseStatus)と ErrorResponse を返す
    //         メッセージは e.getBindingResult().getFieldErrors().get(0).getDefaultMessage() で取れる
    public ErrorResponse badRequest(MethodArgumentNotValidException e) {
        return null;
    }
}
''',
}
s5_tests = {
    T + "S5ErrorsTest.java": test_class(
        "S5ErrorsTest",
        "s5:入力チェック(400)とエラーの JSON、名前での検索",
        TX,
        READ_TESTS
        + '''
    @Test
    @DisplayName("GET /api/users/search?keyword=:名前で検索(200)")
    void search() throws Exception {
        mockMvc.perform(get("/api/users/search").param("keyword", "鈴木"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.length()").value(1))
            .andExpect(jsonPath("$[0].email").value("ichiro@example.com"));
    }

    @Test
    @DisplayName("POST /api/users:名前が空なら 400 とエラーメッセージ(登録されない)")
    void createInvalid() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\\"name\\": \\"\\", \\"email\\": \\"x@example.com\\", \\"age\\": 30}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("名前は必須です"));
        mockMvc.perform(get("/api/users")).andExpect(jsonPath("$.length()").value(3));
    }

    @Test
    @DisplayName("PUT /api/users/{id}:名前が空なら 400")
    void updateInvalid() throws Exception {
        mockMvc.perform(put("/api/users/1")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\\"name\\": \\" \\", \\"email\\": \\"x@example.com\\", \\"age\\": 30}"))
            .andExpect(status().isBadRequest())
            .andExpect(jsonPath("$.message").value("名前は必須です"));
    }
''',
        TX_IMPORT,
    )
}
P["s5-errors"] = dict(answer=s5, start=s5_start, tests=s5_tests)

# ------------------------------- s6-view(第5部「画面」・研修 Day8:一覧画面と登録フォーム) -------------------------------
USER_FORM = '''package com.example.demo.form;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

// 登録フォームの入力値を入れておくクラス。フィールド名はフォームの入力欄の name 属性と同じにする
public class UserForm {
    @NotBlank(message = "名前を入力してください")
    private String name;

    @Email(message = "メールアドレスの形式が正しくありません")
    private String email;

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

PAGE_IMPORTS = '''package com.example.demo.controller;

import com.example.demo.form.UserForm;
import com.example.demo.model.User;
import com.example.demo.service.UserService;
import jakarta.validation.Valid;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
'''

PAGE_CONTROLLER = PAGE_IMPORTS + '''
// 画面(HTML)を返す Controller。処理は REST の UserController と同じ UserService に頼む
@Controller
@RequestMapping("/users")
public class UserPageController {
    private final UserService userService;

    public UserPageController(UserService userService) {
        this.userService = userService;
    }

    // 一覧画面:GET /users → users.html
    @GetMapping
    public String list(Model model) {
        model.addAttribute("users", userService.selectAll());
        return "users";
    }

    // 登録画面:GET /users/new → 空の UserForm を Model に入れて user-form.html
    @GetMapping("/new")
    public String form(Model model) {
        model.addAttribute("userForm", new UserForm());
        return "user-form";
    }

    // 登録:POST /users → 誤りがあれば user-form.html に戻し、なければ登録して result.html
    @PostMapping
    public String create(@Valid @ModelAttribute UserForm userForm, BindingResult result, Model model) {
        if (result.hasErrors()) {
            return "user-form";
        }
        User saved = userService.insert(new User(userForm.getName(), userForm.getEmail(), userForm.getAge()));
        model.addAttribute("message", saved.getName() + "さん(" + saved.getAge() + "歳)を登録しました");
        return "result";
    }
}
'''

USERS_HTML = '''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー一覧</title>
</head>
<body>
<h1>ユーザー一覧</h1>
<table>
    <tr><th>ID</th><th>名前</th><th>メールアドレス</th><th>年齢</th></tr>
    <tr th:each="user : ${users}">
        <td th:text="${user.id}">1</td>
        <td th:text="${user.name}">名前</td>
        <td th:text="${user.email}">メール</td>
        <td th:text="${user.age}">20</td>
    </tr>
</table>
<p><a th:href="@{/users/new}">新しく登録する</a></p>
</body>
</html>
'''

USER_FORM_HTML = '''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー登録</title>
</head>
<body>
<h1>ユーザー登録</h1>
<form th:action="@{/users}" th:object="${userForm}" method="post">
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

RESULT_HTML = '''<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org" lang="ja">
<head>
    <meta charset="UTF-8">
    <title>登録完了</title>
</head>
<body>
<h1>登録完了</h1>
<p th:text="${message}">ここに結果が入る</p>
<p><a th:href="@{/users}">一覧に戻る</a></p>
</body>
</html>
'''

s6 = {
    **s5,
    J + "form/UserForm.java": USER_FORM,
    J + "controller/UserPageController.java": PAGE_CONTROLLER,
    R + "templates/users.html": USERS_HTML,
    R + "templates/user-form.html": USER_FORM_HTML,
    R + "templates/result.html": RESULT_HTML,
}
s6_start = {
    J + "form/UserForm.java": '''package com.example.demo.form;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

// 登録フォームの入力値を入れておくクラス。フィールド名はフォームの入力欄の name 属性と同じにする
public class UserForm {
    // TODO 1: 空なら「名前を入力してください」(@NotBlank)
    private String name;

    // TODO 2: メールアドレスの形でなければ「メールアドレスの形式が正しくありません」(@Email)
    private String email;

    // TODO 3: 空なら「年齢を入力してください」(@NotNull)、0未満なら「年齢は0以上にしてください」(@Min)、
    //         150より大きければ「年齢は150以下にしてください」(@Max)
    private Integer age;
''' + USER_FORM.split("    private Integer age;\n", 1)[1],
    J + "controller/UserPageController.java": PAGE_IMPORTS + '''
// 画面(HTML)を返す Controller。処理は REST の UserController と同じ UserService に頼む
// TODO 4: 画面を返す Controller にし(@Controller)、URL の頭を /users にする(@RequestMapping)
public class UserPageController {
    // TODO 5: UserService をフィールドで持ち、コンストラクタで受け取る

    // TODO 6: GET /users で、Model に "users"(全件)を入れて users.html を表示する
    public String list(Model model) {
        return "users";
    }

    // TODO 7: GET /users/new で、空の UserForm を "userForm" という名前で Model に入れて user-form.html を表示する
    public String form(Model model) {
        return "user-form";
    }

    // TODO 8: POST /users で UserForm を受け取って入力チェックし(@Valid @ModelAttribute)、誤りがあれば user-form.html に戻す。
    //         なければ User を作って登録し、Model に "message"(「田中 健さん(21歳)を登録しました」の形)を入れ、result.html を表示する
    public String create(UserForm userForm, BindingResult result, Model model) {
        return "user-form";
    }
}
''',
}
s6_tests = {
    T + "S6ViewTest.java": test_class(
        "S6ViewTest",
        "s6:一覧画面と登録フォーム(フォーム → Controller → Form → Model → HTML)",
        TX,
        '''
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
            .andExpect(content().string(containsString("name=\\"name\\"")))
            .andExpect(content().string(containsString("name=\\"email\\"")))
            .andExpect(content().string(containsString("name=\\"age\\"")));
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
''',
        TX_IMPORT,
    )
}
P["s6-view"] = dict(answer=s6, start=s6_start, tests=s6_tests)

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


for old in ["w1-spring", "w2-thymeleaf", "w3-rest", "w4-database", "w1-controller", "w2-jpa", "w4-form"]:
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
