# Spring Core — IoC, DI, AOP, Events

> قلب کل اکوسیستم Spring. هر سوال Spring در نهایت به فهم IoC container و چرخه‌ی حیات bean برمی‌گردد.

---

## 📖 مفاهیم

### IoC & Dependency Injection

**توضیح:**

**Inversion of Control** یعنی به‌جای اینکه کلاس خودش وابستگی‌هایش را بسازد (`new`)، کنترل ساخت و اتصال به یک container سپرده می‌شود. **Dependency Injection** سازوکار عملی IoC است: container وابستگی‌ها را از بیرون تزریق می‌کند. این مستقیماً اصل **Dependency Inversion** (D در SOLID) را پیاده می‌کند: کلاس به انتزاع وابسته می‌شود نه به پیاده‌سازی concrete.

سه نوع تزریق: constructor (توصیه‌شده)، setter، و field (با `@Autowired` روی فیلد — ضدالگو). constructor injection برتر است چون: وابستگی‌ها را `final` و اجباری می‌کند، شیء را در حالت کاملاً ساخته‌شده تحویل می‌دهد، تست بدون Spring را ممکن می‌کند، و وابستگی‌های چرخه‌ای را در زمان راه‌اندازی فاش می‌کند.

`ApplicationContext` نسخه‌ی پیشرفته‌ی `BeanFactory` است: علاوه بر DI، پشتیبانی از event، i18n، AOP، و auto-detection از BeanPostProcessorها. در عمل همیشه ApplicationContext استفاده می‌شود.

**چرا مهم است:**

DI تست‌پذیری، انعطاف و کاهش coupling را فراهم می‌کند. کل Spring Boot روی این بنا شده. درک عمیق آن برای دیباگ مشکلات bean (circular dependency، NoUniqueBeanDefinitionException) لازم است.

**مثال کد:**

```java
@Service
public class OrderService {
    private final PaymentGateway gateway;
    private final OrderRepository repository;

    // constructor injection — از Spring 4.3 @Autowired روی تک‌سازنده لازم نیست
    public OrderService(PaymentGateway gateway, OrderRepository repository) {
        this.gateway = gateway;       // final → immutable و اجباری
        this.repository = repository;
    }

    public void place(Order order) {
        gateway.charge(order.total());
        repository.save(order);
    }
}
```

**نکات کلیدی:**

- constructor injection را ترجیح دهید؛ field injection تست را سخت و وابستگی‌ها را پنهان می‌کند.
- ApplicationContext همیشه به‌جای BeanFactory.
- وابستگی‌های `final` باعث می‌شوند کامپایلر اجبار اولیه‌سازی را تضمین کند.

---

### Bean Lifecycle

**توضیح:**

چرخه‌ی حیات یک bean: (۱) instantiation (ساخت با سازنده)، (۲) populate properties (تزریق وابستگی‌ها)، (۳) `Aware` callbackها، (۴) `BeanPostProcessor.postProcessBeforeInitialization`، (۵) متد init (`@PostConstruct` یا `afterPropertiesSet` یا `initMethod`)، (۶) `BeanPostProcessor.postProcessAfterInitialization` (اینجا proxyها مثل AOP ساخته می‌شوند)، (۷) bean آماده‌ی استفاده، (۸) هنگام shutdown: `@PreDestroy` / `destroyMethod`.

**BeanPostProcessor** نقطه‌ی توسعه‌ی کلیدی است: AOP، `@Async`، `@Transactional` همگی با wrap کردن bean در proxy در این مرحله کار می‌کنند.

**چرا مهم است:**

درک اینکه proxy کِی ساخته می‌شود، علت مشکل self-invocation در `@Transactional`/`@Async` را توضیح می‌دهد. همچنین برای منابعی که باید در init باز و در destroy بسته شوند لازم است.

**مثال کد:**

```java
@Component
public class ConnectionManager {
    private Connection connection;

    @PostConstruct
    void init() { connection = openConnection(); } // پس از تزریق

    @PreDestroy
    void cleanup() { connection.close(); } // هنگام shutdown
}
```

**نکات کلیدی:**

- `@PostConstruct` پس از تزریق همه‌ی وابستگی‌ها اجرا می‌شود.
- proxyها در `postProcessAfterInitialization` ساخته می‌شوند → ریشه‌ی مشکل self-invocation.
- `@PreDestroy` برای prototype scope صدا زده نمی‌شود.

---

### Bean Scopes

**توضیح:**

- `singleton` (پیش‌فرض): یک نمونه برای کل container. باید stateless باشد.
- `prototype`: هر بار درخواست، نمونه‌ی جدید. Spring چرخه‌ی حیات کامل (destroy) را مدیریت نمی‌کند.
- `request`, `session`: مخصوص web، یک نمونه به ازای request/session.

نکته‌ی کلاسیک: تزریق یک prototype در یک singleton فقط **یک‌بار** نمونه می‌سازد (هنگام ساخت singleton). برای دریافت نمونه‌ی جدید در هر فراخوانی باید از `ObjectProvider`، `@Lookup`، یا proxy scope استفاده کرد.

**مثال کد:**

```java
@Service
public class ReportService {
    private final ObjectProvider<ReportBuilder> builderProvider; // prototype

    public ReportService(ObjectProvider<ReportBuilder> p) { this.builderProvider = p; }

    public Report build() {
        ReportBuilder builder = builderProvider.getObject(); // نمونه‌ی تازه هر بار
        return builder.build();
    }
}
```

**نکات کلیدی:**

- singleton باید stateless و thread-safe باشد.
- تزریق ساده‌ی prototype در singleton مشکل «scoped bean» دارد.
- Spring مرگ prototype را مدیریت نمی‌کند؛ منابع را خودتان آزاد کنید.

---

### Stereotype Annotations & Qualifiers

**توضیح:**

`@Component` پایه است؛ `@Service`, `@Repository`, `@Controller` تخصصی‌سازی معنایی‌اند. `@Repository` علاوه بر معنا، **exception translation** (تبدیل استثناهای JDBC/JPA به `DataAccessException` یکنواخت) را فعال می‌کند.

وقتی چند پیاده‌سازی از یک interface وجود دارد: `@Primary` پیش‌فرض را مشخص می‌کند؛ `@Qualifier("name")` انتخاب صریح؛ بدون این‌ها `NoUniqueBeanDefinitionException`.

**مثال کد:**

```java
public interface NotificationSender { void send(String msg); }

@Service @Qualifier("email")
class EmailSender implements NotificationSender { public void send(String m) {} }

@Service @Primary
class SmsSender implements NotificationSender { public void send(String m) {} }

@Service
class AlertService {
    private final NotificationSender sender;
    AlertService(@Qualifier("email") NotificationSender sender) { // انتخاب صریح
        this.sender = sender;
    }
}
```

**نکات کلیدی:**

- `@Repository` exception translation می‌دهد.
- برای ابهام چندbean از `@Qualifier`/`@Primary` استفاده کنید.

---

### Configuration & Profiles

**توضیح:**

`@Configuration` + `@Bean` برای تعریف bean به‌صورت برنامه‌نویسی (به‌خصوص برای کلاس‌های third-party که نمی‌توانید annotate کنید). `@Value` برای تزریق مقدار از properties. `@Profile` برای فعال‌سازی bean در محیط‌های مختلف (dev/prod). `Environment` انتزاع دسترسی به properties و profileهای فعال.

نکته: متدهای `@Bean` در یک `@Configuration` به‌صورت پیش‌فرض با CGLIB proxy می‌شوند تا فراخوانی bean دیگری همان singleton را برگرداند (نه نمونه‌ی جدید).

**مثال کد:**

```java
@Configuration
public class AppConfig {
    @Bean
    public RestClient restClient(@Value("${api.base-url}") String baseUrl) {
        return RestClient.builder().baseUrl(baseUrl).build();
    }

    @Bean
    @Profile("prod")
    public Cache prodCache() { return new RedisCache(); }

    @Bean
    @Profile("dev")
    public Cache devCache() { return new InMemoryCache(); }
}
```

**نکات کلیدی:**

- `@Bean` برای third-party؛ stereotype برای کد خودتان.
- `@Configuration` با proxy تضمین می‌کند فراخوانی bean همان singleton را برگرداند (full mode).
- profile برای جداسازی config محیط‌ها.

---

### AOP (Aspect-Oriented Programming)

**توضیح:**

AOP منطق عرضی (cross-cutting) مثل logging، transaction، security، auditing را از منطق کسب‌وکار جدا می‌کند. مفاهیم: **Aspect** (ماژول cross-cutting)، **Advice** (`@Before`, `@After`, `@Around`, `@AfterReturning`, `@AfterThrowing`)، **Pointcut** (بیان اینکه کجا اعمال شود)، **JoinPoint** (نقطه‌ی اجرا).

Spring AOP مبتنی بر **proxy** است: یا JDK Dynamic Proxy (اگر bean interface دارد) یا CGLIB (subclassing، اگر ندارد). به همین دلیل دو محدودیت دارد: فقط روی فراخوانی‌های public از بیرون کار می‌کند، و **self-invocation** (فراخوانی متد دیگری از همان کلاس) از proxy عبور نمی‌کند پس advice اعمال نمی‌شود.

**چرا مهم است:**

`@Transactional`, `@Cacheable`, `@Async`, Spring Security همه روی AOP بنا شده‌اند. درک محدودیت proxy برای دیباگ «چرا transaction من کار نمی‌کند» حیاتی است.

**مثال کد:**

```java
@Aspect
@Component
public class TimingAspect {
    @Around("@annotation(Timed)") // روی متدهای دارای @Timed
    public Object measure(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed(); // اجرای متد اصلی
        } finally {
            long ms = (System.nanoTime() - start) / 1_000_000;
            System.out.println(pjp.getSignature() + " took " + ms + "ms");
        }
    }
}
```

**نکات کلیدی:**

- Spring AOP فقط proxy-based است؛ self-invocation اعمال نمی‌شود.
- JDK proxy برای interface، CGLIB برای class.
- pointcut expressionها: `execution(...)`, `within(...)`, `@annotation(...)`.

---

### Events

**توضیح:**

مکانیزم publish/subscribe درون‌برنامه‌ای. `ApplicationEventPublisher.publishEvent()` رویداد منتشر می‌کند و `@EventListener` آن را می‌گیرد. پیش‌فرض synchronous است (در همان thread و transaction)؛ با `@Async` می‌توان async کرد.

`@TransactionalEventListener` رویداد را به فاز transaction گره می‌زند (مثلاً فقط `AFTER_COMMIT`) — برای جلوگیری از انتشار رویداد وقتی transaction rollback می‌شود.

**مثال کد:**

```java
public record OrderPlacedEvent(Long orderId) {}

@Service
class OrderService {
    private final ApplicationEventPublisher publisher;
    OrderService(ApplicationEventPublisher publisher) { this.publisher = publisher; }

    @Transactional
    public void place(Order order) {
        // ذخیره...
        publisher.publishEvent(new OrderPlacedEvent(order.getId()));
    }
}

@Component
class EmailNotifier {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    void onOrderPlaced(OrderPlacedEvent event) {
        // فقط پس از commit موفق ایمیل بفرست
    }
}
```

**نکات کلیدی:**

- listener پیش‌فرض synchronous است؛ با `@Async` غیرهمزمان کنید.
- `@TransactionalEventListener(AFTER_COMMIT)` از side-effect روی rollback جلوگیری می‌کند.
- decoupling خوب، اما برای ارتباط بین سرویس‌ها از message broker استفاده کنید نه event داخلی.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا constructor injection بر field injection ترجیح دارد؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

دلایل: (۱) وابستگی‌ها را می‌توان `final` کرد → immutable و تضمین مقداردهی. (۲) شیء همیشه در حالت کامل و معتبر ساخته می‌شود (نمی‌توان شیء نیمه‌ساخته داشت). (۳) تست واحد بدون Spring container ممکن است — فقط `new Service(mockDep)`؛ با field injection باید reflection یا context بالا بیاورید. (۴) وابستگی‌های اجباری در امضای سازنده شفاف‌اند (برخلاف field injection که آن‌ها را پنهان می‌کند و کلاس را به‌سمت تعداد زیاد وابستگی سوق می‌دهد). (۵) circular dependency در زمان راه‌اندازی فاش می‌شود به‌جای رفتار مبهم.

**کد توضیحی:**

```java
// تست بدون Spring
var service = new OrderService(mock(PaymentGateway.class), mock(OrderRepository.class));
```

**نکته مصاحبه:**

تمایز Senior: اشاره به immutability، تست‌پذیری و فاش شدن circular dependency. Follow-up: «field injection چه زمانی circular dependency را پنهان می‌کند؟»

---

### سوال ۲: مشکل self-invocation در `@Transactional` چیست؟

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

`@Transactional` (و `@Async`, `@Cacheable`) از طریق AOP proxy کار می‌کند. وقتی از بیرون متد را صدا می‌زنید، فراخوانی از proxy عبور می‌کند و advice (شروع transaction) اعمال می‌شود. اما وقتی یک متد public از همان کلاس، متد transactional دیگری از **همان کلاس** را با `this.method()` صدا می‌زند، این فراخوانی مستقیم روی شیء واقعی است و از proxy عبور نمی‌کند — پس transaction شروع نمی‌شود.

راه‌حل‌ها: (۱) متد را به یک bean جداگانه منتقل کنید. (۲) خود bean را تزریق کنید (self-injection) و از طریق proxy صدا بزنید. (۳) `TransactionTemplate` برنامه‌نویسی‌شده. بهترین راه معمولاً جداسازی مسئولیت‌هاست.

**کد توضیحی:**

```java
@Service
class OrderService {
    public void process() {
        save(); // ❌ self-invocation → @Transactional اعمال نمی‌شود
    }
    @Transactional
    public void save() { /* ... */ }
}
```

**نکته مصاحبه:**

Lead به دلیل ریشه‌ای (proxy در BeanPostProcessor) و چند راه‌حل اشاره می‌کند. Follow-up: «چرا متد private هم transactional نمی‌شود؟» (proxy فقط متد public override-پذیر را intercept می‌کند).

---

### سوال ۳: تفاوت BeanFactory و ApplicationContext چیست؟

**سطح:** Mid / Senior
**تکرار:** متوسط

**جواب کامل:**

`BeanFactory` container پایه با DI و lazy initialization است. `ApplicationContext` superset آن است و امکانات enterprise اضافه می‌کند: eager initialization پیش‌فرض singletonها (خطاها زود فاش می‌شوند)، پشتیبانی از event publishing، internationalization، resource loading، یکپارچگی AOP، و تشخیص خودکار BeanPostProcessor/BeanFactoryPostProcessor. در عمل همیشه ApplicationContext استفاده می‌شود.

**نکته مصاحبه:**

Follow-up: «BeanFactoryPostProcessor با BeanPostProcessor چه فرقی دارد؟» (اولی روی تعریف bean قبل از ساخت، دومی روی نمونه‌ی ساخته‌شده).

---

### سوال ۴: bean lifecycle را شرح بده و proxyها کجا ساخته می‌شوند؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

instantiation → تزریق وابستگی → Aware callbackها → `postProcessBeforeInitialization` → init (`@PostConstruct`) → `postProcessAfterInitialization` → آماده → destroy (`@PreDestroy`). proxyهای AOP (transaction، async، cache، security) در مرحله‌ی `postProcessAfterInitialization` ساخته می‌شوند؛ یعنی bean در `@PostConstruct` هنوز proxy نشده. این توضیح می‌دهد چرا فراخوانی متد transactional در `@PostConstruct` بی‌اثر است.

**نکته مصاحبه:**

Senior می‌داند که در `@PostConstruct` هنوز proxy وجود ندارد. Follow-up: «`InitializingBean` و `@PostConstruct` چه ترتیبی دارند؟»

---

### سوال ۵: تفاوت JDK Dynamic Proxy و CGLIB چیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

JDK Dynamic Proxy فقط برای کلاس‌هایی که **interface** دارند کار می‌کند و یک پیاده‌سازی runtime از آن interface می‌سازد. CGLIB با **subclassing** کلاس هدف proxy می‌سازد، پس به interface نیاز ندارد اما کلاس و متدها نباید `final` باشند (چون نمی‌تواند override کند). Spring Boot به‌صورت پیش‌فرض CGLIB را ترجیح می‌دهد (حتی برای کلاس‌های دارای interface) مگر تنظیم شود. به همین دلیل متد/کلاس `final` ممکن است proxy نشود و advice اعمال نگردد.

**نکته مصاحبه:**

Follow-up: «چرا متد final در یک bean transactional کار نمی‌کند؟» (CGLIB نمی‌تواند override کند).

---

### سوال ۶: prototype bean در singleton — چرا فقط یک‌بار ساخته می‌شود؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

تزریق وابستگی فقط یک‌بار هنگام ساخت singleton انجام می‌شود. پس حتی اگر bean تزریق‌شده prototype باشد، singleton همان یک نمونه را برای همیشه نگه می‌دارد. برای دریافت نمونه‌ی تازه در هر استفاده باید container را دوباره صدا بزنید: `ObjectProvider<T>`, `@Lookup` method injection، یا scoped proxy. این یک سوءتفاهم رایج است که گمان می‌کنند prototype خودکار در هر فراخوانی نو می‌شود.

**نکته مصاحبه:**

Follow-up: «scoped proxy چطور این را حل می‌کند؟»

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: field injection

```java
// ❌
@Service
class OrderService {
    @Autowired private PaymentGateway gateway;
}
```

```java
// ✅ constructor injection
@Service
class OrderService {
    private final PaymentGateway gateway;
    OrderService(PaymentGateway gateway) { this.gateway = gateway; }
}
```

**توضیح:** field injection تست را سخت و وابستگی‌ها را پنهان می‌کند و امکان `final` نمی‌دهد.

---

### اشتباه ۲: انتظار transaction از self-invocation

```java
// ❌
public void process() { this.saveInTx(); } // proxy دور زده می‌شود
@Transactional public void saveInTx() {}
```

```java
// ✅ متد transactional در bean جدا
public void process() { txService.saveInTx(); }
```

**توضیح:** فراخوانی داخلی از proxy عبور نمی‌کند.

---

### اشتباه ۳: state تغییرپذیر در singleton

```java
// ❌ race condition بین requestها
@Service
class CounterService {
    private int count; // مشترک بین همه threadها
    void inc() { count++; }
}
```

```java
// ✅
@Service
class CounterService {
    private final AtomicInteger count = new AtomicInteger();
    void inc() { count.incrementAndGet(); }
}
```

**توضیح:** singleton بین همه‌ی threadها مشترک است؛ باید stateless/thread-safe باشد.

---

### اشتباه ۴: انتشار event بدون توجه به transaction

```java
// ❌ ایمیل حتی اگر transaction rollback شود ارسال می‌شود
@EventListener
void onOrder(OrderPlacedEvent e) { sendEmail(e); }
```

```java
// ✅
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
void onOrder(OrderPlacedEvent e) { sendEmail(e); }
```

**توضیح:** listener پیش‌فرض در همان transaction اجرا می‌شود؛ برای side-effect خارجی AFTER_COMMIT بهتر است.

---

## 🔗 ارتباط با سایر مفاهیم

- IoC/DI مستقیماً **Dependency Inversion** از SOLID را پیاده می‌کند.
- AOP پایه‌ی **`@Transactional`** (Spring Data)، **`@Cacheable`** (Caching) و **Spring Security** است.
- Events با **Event-Driven Architecture** و الگوی **Outbox** مرتبط است.
- Bean lifecycle با **Spring Boot auto-configuration** و **testing** گره می‌خورد.
- درک proxy برای دیباگ مشکلات **transaction** و **async** ضروری است.
