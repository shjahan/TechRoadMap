# Testing در Java — JUnit 5، Mockito، Spring Test، Testcontainers

> تست مهارت پایه‌ی Senior است. Test Pyramid و Testcontainers موضوعات کلیدی مصاحبه‌اند.

---

## 📖 مفاهیم

### JUnit 5

**توضیح:**

فریم‌ورک تست استاندارد. `@Test`, lifecycle (`@BeforeEach`, `@AfterEach`, `@BeforeAll`)، parameterized tests (`@ParameterizedTest` با `@ValueSource`, `@CsvSource`, `@MethodSource`)، `@ExtendWith` برای extension (مثل Mockito). الگوی **Arrange-Act-Assert** (AAA) برای ساختار خوانا.

**مثال کد:**

```java
@Test
void shouldCalculateTotal() {
    // Arrange
    var cart = new Cart();
    cart.add(new Item("book", 1000), 2);
    // Act
    long total = cart.total();
    // Assert
    assertThat(total).isEqualTo(2000);
}

@ParameterizedTest
@CsvSource({"2, 3, 5", "10, 20, 30"})
void shouldAdd(int a, int b, int expected) {
    assertThat(calculator.add(a, b)).isEqualTo(expected);
}
```

**نکات کلیدی:**

- AAA برای ساختار خوانا.
- parameterized برای چند ورودی بدون تکرار.
- نام تست باید رفتار را توصیف کند (`shouldXWhenY`).

---

### Mockito

**توضیح:**

mock کردن وابستگی‌ها برای isolation در unit test. `@Mock` (ساخت mock)، `@InjectMocks` (تزریق mockها)، `when(...).thenReturn(...)` (stub)، `verify(...)` (بررسی فراخوانی)، `ArgumentCaptor` (گرفتن آرگومان). تفاوت stub (تعیین رفتار) و verify (بررسی تعامل).

**مثال کد:**

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock UserRepository repository;
    @InjectMocks UserService service;

    @Test
    void shouldSaveUser() {
        when(repository.save(any())).thenReturn(new User(1L, "Ali"));
        User result = service.create("Ali");
        ArgumentCaptor<User> captor = ArgumentCaptor.forClass(User.class);
        verify(repository).save(captor.capture());
        assertThat(captor.getValue().name()).isEqualTo("Ali");
    }
}
```

**نکات کلیدی:**

- mock فقط وابستگی‌های خارجی؛ منطق خودِ کلاس تحت تست را mock نکنید.
- verify برای تعامل، assert برای نتیجه.
- از over-mocking بپرهیزید (تست شکننده می‌شود).

---

### Spring Boot Testing

**توضیح:**

**Test slices** برای بارگذاری بخشی از context (سریع‌تر): `@WebMvcTest` (فقط web layer + MockMvc)، `@DataJpaTest` (JPA + embedded/Testcontainers DB)، `@JsonTest`, `@RestClientTest`. `@SpringBootTest` کل context را بالا می‌آورد (کندتر، برای integration). `@MockBean` (یا `@MockitoBean` در نسخه‌های جدید) برای mock در context.

**مثال کد:**

```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired MockMvc mockMvc;
    @MockitoBean UserService userService;

    @Test
    void shouldReturnUser() throws Exception {
        when(userService.findById(1L)).thenReturn(new UserDto(1L, "Ali"));
        mockMvc.perform(get("/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("Ali"));
    }
}
```

**نکات کلیدی:**

- test slice سریع‌تر از `@SpringBootTest` کامل است.
- `@WebMvcTest` فقط web layer؛ service را mock کنید.

---

### Testcontainers

**توضیح:**

اجرای دیتابیس/سرویس واقعی در container برای تست — به‌جای H2 که رفتار متفاوت دارد. `@Testcontainers` + `@Container`. با `@DynamicPropertySource` آدرس container به Spring داده می‌شود. برای PostgreSQL، MongoDB، Redis، Kafka، Elasticsearch.

**مثال کد:**

```java
@SpringBootTest
@Testcontainers
class OrderRepositoryTest {
    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:17");

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

**نکات کلیدی:**

- Testcontainers DB واقعی → رفتار production-like (برخلاف H2).
- container را static کنید تا بین تست‌ها reuse شود (سرعت).

---

### Test Pyramid

**توضیح:**

نسبت توصیه‌شده: **Unit (70%)** سریع و isolated؛ **Integration (20%)** چند component؛ **E2E (10%)** کند و شکننده. هرم نه ساعت‌شنی (ضدالگو: E2E زیاد، unit کم). **Contract tests** (Pact) برای microservices API contracts.

**نکات کلیدی:**

- بیشتر unit (سریع)، کمتر E2E (کند، شکننده).
- contract testing برای جلوگیری از breaking change بین سرویس‌ها.

---

## 🎯 سوالات مصاحبه

### سوال ۱: Test Pyramid چیست و چرا E2E کم؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

Test Pyramid توزیع پیشنهادی تست‌هاست: پایه‌ی پهن از unit tests (سریع، isolated، ارزان)، لایه‌ی میانی integration tests، و نوک کوچک E2E tests. دلیل کم بودن E2E: کند هستند (کل سیستم بالا می‌آید)، **شکننده** (به محیط، شبکه، داده، timing وابسته‌اند و flaky می‌شوند)، و دیباگ سخت (وقتی fail می‌شوند، علت مبهم است). unit tests سریع feedback می‌دهند و دقیقاً مشکل را نشان می‌دهند. ضدالگوی «ice cream cone» (E2E زیاد، unit کم) منجر به test suite کند و بی‌اعتماد می‌شود. استراتژی: منطق را با unit، یکپارچگی را با integration (Testcontainers)، و فقط مسیرهای حیاتی کاربر را با E2E تست کنید.

**نکته مصاحبه:**

Senior به flakiness و ضدالگوی ice cream cone اشاره می‌کند.

---

### سوال ۲: چرا Testcontainers به‌جای H2؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

H2 یک in-memory DB است که برای تست سریع است اما رفتار آن با دیتابیس production (PostgreSQL) **متفاوت** است: dialect SQL متفاوت، عدم پشتیبانی از feature‌های خاص (JSONB، window functions پیشرفته، انواع داده)، رفتار متفاوت در constraint و transaction. نتیجه: تست با H2 سبز می‌شود اما در production می‌شکند (false confidence). Testcontainers یک نمونه‌ی **واقعی** PostgreSQL را در container اجرا می‌کند، پس تست دقیقاً علیه همان DB production اجرا می‌شود — اطمینان واقعی. هزینه: کندتر از H2 (نیاز Docker و startup container)، که با reuse container و parallel تا حدی جبران می‌شود. trade-off اطمینان در برابر سرعت، که برای persistence layer به نفع Testcontainers است.

**نکته مصاحبه:**

Senior به false confidence با H2 (dialect متفاوت) اشاره می‌کند.

---

### سوال ۳: تفاوت `@WebMvcTest` و `@SpringBootTest`؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`@WebMvcTest` یک test slice است که فقط لایه‌ی web را بالا می‌آورد (controllerها، filterها، MockMvc) و بقیه (service، repository) را بارگذاری نمی‌کند — پس باید آن‌ها را `@MockitoBean` کنید. سریع است و فقط منطق controller (routing، serialization، validation، status) را تست می‌کند. `@SpringBootTest` کل application context را بالا می‌آورد (همه‌ی beanها، DB، …) — برای integration test کامل، اما کند. انتخاب: برای تست controller به‌تنهایی `@WebMvcTest`؛ برای تست یکپارچه‌ی end-to-end داخلی `@SpringBootTest` (معمولاً با Testcontainers). استفاده‌ی `@SpringBootTest` برای همه‌چیز test suite را کند می‌کند.

**نکته مصاحبه:**

Senior test slice را برای سرعت ترجیح می‌دهد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: `@SpringBootTest` برای همه‌چیز

```java
// ❌ کند، کل context برای تست یک controller
@SpringBootTest
class UserControllerTest {}
```

```java
// ✅ test slice
@WebMvcTest(UserController.class)
```

**توضیح:** test slice سریع‌تر و متمرکزتر است.

---

### اشتباه ۲: over-mocking

```java
// ❌ mock کردن همه‌چیز → تست به پیاده‌سازی gره می‌خورد
```

```java
// ✅ فقط وابستگی‌های خارجی را mock کنید
```

**توضیح:** mock زیاد تست را شکننده و بی‌ارزش می‌کند.

---

### اشتباه ۳: تست با H2 برای کد PostgreSQL-specific

```text
❌ H2 → سبز، production → قرمز
✅ Testcontainers با PostgreSQL واقعی
```

**توضیح:** dialect متفاوت H2 false confidence می‌دهد.

---

## 🔗 ارتباط با سایر مفاهیم

- testing با **CI/CD (10.3)** (fail fast).
- Testcontainers با **Docker (10.1)** و **Spring Data (2.4)**.
- contract testing با **microservices (6.1)** و **Spring Test عمیق (13.5)**.
- mocking با **dependency injection (2.1)** (constructor injection تست را آسان می‌کند).
