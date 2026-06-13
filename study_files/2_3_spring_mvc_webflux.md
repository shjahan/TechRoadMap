# Spring MVC & WebFlux — REST، Reactive، HTTP Clients

> دو مدل برنامه‌نویسی وب در Spring: servlet-based (MVC) و reactive (WebFlux). انتخاب درست تصمیم معماری است.

---

## 📖 مفاهیم

### Spring MVC (Servlet-based)

**توضیح:**

مدل کلاسیک و رایج: هر request توسط یک thread از thread pool پردازش می‌شود (thread-per-request) و کد به‌صورت blocking نوشته می‌شود. `@RestController` ترکیب `@Controller` + `@ResponseBody` است. mapping با `@GetMapping`, `@PostMapping`, و … . binding ورودی با `@PathVariable`, `@RequestParam`, `@RequestBody`, `@RequestHeader`.

`ResponseEntity<T>` کنترل کامل بر status code، header و body می‌دهد. مدیریت خطای متمرکز با `@RestControllerAdvice` + `@ExceptionHandler`. validation با `@Valid`/`@Validated` و Bean Validation. `HandlerInterceptor` برای pre/post processing (مثل logging، auth ساده).

**چرا مهم است:**

اکثر برنامه‌های Spring از MVC استفاده می‌کنند. با Java 21 virtual threads، MVC برای throughput بالا هم رقابتی شده و نیاز به WebFlux را کم کرده.

**مثال کد:**

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    private final UserService service;
    public UserController(UserService service) { this.service = service; }

    @GetMapping("/{id}")
    public ResponseEntity<UserDto> getUser(@PathVariable Long id) {
        return service.findById(id)
            .map(ResponseEntity::ok)
            .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<UserDto> create(@Valid @RequestBody CreateUserRequest req) {
        UserDto created = service.create(req);
        return ResponseEntity
            .created(URI.create("/api/v1/users/" + created.id()))
            .body(created);
    }
}
```

**نکات کلیدی:**

- `ResponseEntity` برای کنترل دقیق response؛ برای کد ساده می‌توان مستقیم DTO برگرداند.
- `@Valid` validation را trigger می‌کند؛ خطا را در `@RestControllerAdvice` بگیرید.
- با virtual threads، MVC blocking مقیاس‌پذیرتر شده.

---

### Exception Handling متمرکز

**توضیح:**

به‌جای try/catch در هر controller، `@RestControllerAdvice` یک نقطه‌ی مرکزی برای تبدیل استثناها به response استاندارد می‌دهد. Spring 6+ از `ProblemDetail` (RFC 7807) پشتیبانی می‌کند که فرمت استاندارد خطا برای APIهاست.

**مثال کد:**

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(UserNotFoundException.class)
    public ProblemDetail handleNotFound(UserNotFoundException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setType(URI.create("https://api.example.com/errors/not-found"));
        return pd;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        pd.setDetail("اعتبارسنجی ناموفق");
        pd.setProperty("violations", ex.getFieldErrors().stream()
            .map(e -> Map.of("field", e.getField(), "message", e.getDefaultMessage()))
            .toList());
        return pd;
    }
}
```

**نکات کلیدی:**

- مدیریت خطا را متمرکز کنید نه پراکنده در controllerها.
- `ProblemDetail` فرمت استاندارد و قابل‌پیش‌بینی برای مصرف‌کننده می‌دهد.

---

### Spring WebFlux (Reactive)

**توضیح:**

مدل non-blocking و event-loop مبتنی بر Project Reactor. به‌جای thread-per-request، تعداد کمی event-loop thread درخواست‌ها را با callback مدیریت می‌کنند. دو نوع publisher: `Mono<T>` (صفر یا یک عنصر) و `Flux<T>` (صفر تا N). `WebClient` کلاینت HTTP reactive و جایگزین `RestTemplate` است.

مفهوم کلیدی **backpressure**: مصرف‌کننده می‌تواند نرخ تولید را کنترل کند تا overwhelm نشود. WebFlux برای streaming، تعداد اتصال بالای I/O-bound، و وقتی کل stack reactive است مزیت دارد.

**چرا مهم است:**

برای سیستم‌های با اتصال هم‌زمان بسیار بالا و streaming. اما با ظهور virtual threads، برای اکثر CRUD، MVC ساده‌تر و کافی است.

**مثال کد:**

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    private final ProductRepository repository; // ReactiveCrudRepository

    public ProductController(ProductRepository r) { this.repository = r; }

    @GetMapping("/{id}")
    public Mono<Product> getProduct(@PathVariable String id) {
        return repository.findById(id)
            .switchIfEmpty(Mono.error(new ProductNotFoundException(id)));
    }

    @GetMapping(produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<Product> streamProducts() {
        return repository.findAll().delayElements(Duration.ofSeconds(1)); // streaming
    }
}
```

**نکات کلیدی:**

- هرگز کد blocking را داخل reactive chain اجرا نکنید (event-loop را مسدود می‌کند).
- `subscribeOn(Schedulers.boundedElastic())` برای wrap کردن blocking ناگزیر.
- اشتراک (subscribe) باعث اجرا می‌شود؛ بدون subscriber هیچ اتفاقی نمی‌افتد.

---

### HTTP Interface Clients

**توضیح:**

از Spring 6/Boot 3، می‌توان کلاینت HTTP را به‌صورت declarative با interface تعریف کرد، مشابه Feign. با `@HttpExchange` و `@GetExchange`/`@PostExchange`. Spring پیاده‌سازی را تولید می‌کند.

**مثال کد:**

```java
@HttpExchange("/users")
public interface UserClient {
    @GetExchange("/{id}")
    User getUser(@PathVariable Long id);

    @PostExchange
    User create(@RequestBody CreateUserRequest req);
}

// ثبت
@Bean
UserClient userClient(RestClient.Builder builder) {
    RestClient client = builder.baseUrl("https://api.example.com").build();
    return HttpServiceProxyFactory
        .builderFor(RestClientAdapter.create(client))
        .build()
        .createClient(UserClient.class);
}
```

**نکات کلیدی:**

- declarative client کد boilerplate را حذف می‌کند.
- با resilience4j (circuit breaker، retry) ترکیب می‌شود.

---

### REST Best Practices

**توضیح:**

- **Richardson Maturity Model:** Level 0 (یک endpoint)، Level 1 (resources)، Level 2 (HTTP verbs و status صحیح — هدف عملی)، Level 3 (HATEOAS).
- **API Versioning:** URL (`/v1/`)، header، یا content-type. هر کدام trade-off دارد.
- **Error standardization:** RFC 7807 Problem Details.
- استفاده‌ی صحیح از status codeها (200, 201, 204, 400, 404, 409, 422, 500).

**نکات کلیدی:**

- اکثر APIها Level 2 هستند؛ HATEOAS به‌ندرت ارزش هزینه‌اش را دارد.
- versioning را از ابتدا پلن کنید.

---

## 🎯 سوالات مصاحبه

### سوال ۱: WebFlux کِی به‌جای MVC؟ (به‌خصوص با virtual threads)

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

WebFlux وقتی مزیت دارد که: تعداد اتصال هم‌زمان بسیار بالا با I/O-bound کار، نیاز به streaming واقعی (SSE، WebSocket)، backpressure واقعی، یا ترکیب پیچیده‌ی جریان‌های async. هزینه‌اش: منحنی یادگیری تند، دیباگ سخت (stacktrace غیرخطی)، و آلودگی کل stack (هر چیز باید reactive باشد، یک فراخوانی blocking کل event-loop را خراب می‌کند).

با ظهور virtual threads در Java 21، MVC با کد blocking ساده می‌تواند به throughput مشابه برسد بدون پیچیدگی reactive. بنابراین برای اکثر برنامه‌های CRUD/microservice، MVC + virtual threads انتخاب پیش‌فرض منطقی است؛ WebFlux برای موارد خاص streaming و backpressure می‌ماند.

**نکته مصاحبه:**

Lead trade-off را می‌فهمد و کورکورانه reactive را تجویز نمی‌کند. Follow-up: «backpressure در virtual threads چطور مدیریت می‌شود؟»

---

### سوال ۲: تفاوت `Mono` و `Flux` چیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

هر دو publisher در Reactor هستند. `Mono<T>` صفر یا یک عنصر تولید می‌کند (مثل نتیجه‌ی یک query تک‌رکوردی یا یک عملیات async که یک مقدار برمی‌گرداند). `Flux<T>` صفر تا N عنصر (مثل stream رکوردها یا رویدادها). هر دو lazy هستند: تا قبل از `subscribe` هیچ کاری انجام نمی‌شود. عملیات مشابه Stream دارند (`map`, `filter`, `flatMap`) به‌علاوه‌ی عملگرهای async و خطا (`onErrorResume`, `retryWhen`, `timeout`).

**نکته مصاحبه:**

Follow-up: «چرا بدون subscribe هیچ اتفاقی نمی‌افتد؟» (nothing happens until you subscribe — publisher فقط blueprint است).

---

### سوال ۳: چرا نباید کد blocking در WebFlux استفاده کرد؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

WebFlux تعداد کمی event-loop thread (به‌اندازه‌ی هسته‌ها) دارد که همه‌ی requestها را مدیریت می‌کنند. اگر یک عملیات blocking (مثل JDBC یا `Thread.sleep`) روی این threadها اجرا شود، آن thread مسدود می‌شود و نمی‌تواند requestهای دیگر را سرویس دهد — throughput سقوط می‌کند و کل مزیت reactive از بین می‌رود. اگر مجبور به blocking هستید، باید آن را با `subscribeOn(Schedulers.boundedElastic())` به یک thread pool جدا منتقل کنید. به همین دلیل برای WebFlux کل stack (شامل DB با R2DBC) باید reactive باشد.

**نکته مصاحبه:**

Lead به boundedElastic و نیاز به reactive driver (R2DBC) اشاره می‌کند.

---

### سوال ۴: API versioning — چه استراتژی‌هایی و کدام بهتر؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

سه روش اصلی: (۱) **URL** (`/api/v1/users`) — ساده، قابل‌مشاهده، cache-friendly، اما RESTful pure نیست. (۲) **Header** (`X-API-Version: 1`) — URL تمیز می‌ماند اما کمتر شفاف و تست دستی سخت‌تر. (۳) **Content-Type** (`application/vnd.company.v1+json`) — content negotiation اصیل اما پیچیده. در عمل URL versioning رایج‌ترین و عملی‌ترین است. Spring Framework 7 versioning داخلی در `@RequestMapping(version=...)` اضافه کرده. مهم‌تر از روش، داشتن سیاست deprecation و backward compatibility است.

**نکته مصاحبه:**

Lead به سیاست deprecation و backward compatibility اشاره می‌کند نه فقط مکانیزم.

---

### سوال ۵: `@RequestParam` در برابر `@PathVariable` — کِی کدام؟

**سطح:** Junior / Mid
**تکرار:** متوسط

**جواب کامل:**

`@PathVariable` بخشی از مسیر است و معمولاً برای شناسایی یک resource مشخص (`/users/{id}`). `@RequestParam` query parameter است و برای فیلتر، صفحه‌بندی، یا گزینه‌های اختیاری (`/users?status=active&page=2`). قاعده‌ی RESTful: شناسه‌ی resource در path، معیارهای جستجو/فیلتر در query.

**نکته مصاحبه:**

Follow-up: «چطور یک query param اختیاری با مقدار پیش‌فرض بگیری؟» (`@RequestParam(defaultValue="0")`).

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: کد blocking در reactive chain

```java
// ❌ event-loop را مسدود می‌کند
@GetMapping("/{id}")
Mono<User> get(@PathVariable Long id) {
    User u = jdbcRepository.findById(id); // blocking!
    return Mono.just(u);
}
```

```java
// ✅
Mono<User> get(@PathVariable Long id) {
    return Mono.fromCallable(() -> jdbcRepository.findById(id))
               .subscribeOn(Schedulers.boundedElastic());
}
```

**توضیح:** blocking روی event-loop throughput را نابود می‌کند.

---

### اشتباه ۲: try/catch پراکنده به‌جای advice

```java
// ❌ تکرار در هر controller
@GetMapping("/{id}")
ResponseEntity<?> get(@PathVariable Long id) {
    try { return ResponseEntity.ok(service.find(id)); }
    catch (Exception e) { return ResponseEntity.status(500).build(); }
}
```

```java
// ✅ متمرکز
@RestControllerAdvice
class Handler { @ExceptionHandler(...) ProblemDetail handle(...) {} }
```

**توضیح:** مدیریت خطا را متمرکز کنید.

---

### اشتباه ۳: فراموشی `@Valid`

```java
// ❌ validation اجرا نمی‌شود
@PostMapping
User create(@RequestBody CreateUserRequest req) {}
```

```java
// ✅
@PostMapping
User create(@Valid @RequestBody CreateUserRequest req) {}
```

**توضیح:** بدون `@Valid` constraintها بررسی نمی‌شوند.

---

### اشتباه ۴: استفاده از 200 برای همه‌چیز

```java
// ❌ همه‌چیز 200 حتی ساخت یا خطا
return ResponseEntity.ok(result);
```

```java
// ✅ status معنادار
return ResponseEntity.created(uri).body(result); // 201 برای ساخت
```

**توضیح:** status code صحیح برای مصرف‌کننده و ابزارها مهم است.

---

## 🔗 ارتباط با سایر مفاهیم

- MVC vs WebFlux مستقیماً با **Virtual Threads** (Java 21) گره خورده.
- WebFlux با **R2DBC** (Spring Data reactive) و **Reactor** عمیق مرتبط است.
- Exception handling با **Problem Details (RFC 7807)** در بخش API Design.
- HTTP Interface clients با **resilience4j** (circuit breaker) و **microservices** ترکیب می‌شود.
- REST best practices با **API Gateway** و **versioning** در Spring Cloud.
