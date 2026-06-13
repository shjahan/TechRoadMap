# Design Patterns (Gang of Four)

> الگوهای طراحی زبان مشترک مهندسان‌اند. شناخت آن‌ها در کد Spring/JDK تمایز Senior است.

---

## 📖 مفاهیم

### Creational Patterns

**توضیح:**

- **Singleton:** یک نمونه برای کل برنامه. thread-safe با double-checked locking (نیاز `volatile`) یا بهتر، **enum** (serialization-safe و reflection-safe). در Spring، beanها به‌صورت پیش‌فرض singleton هستند (managed by container).
- **Factory Method:** delegate ساخت به subclass/متد. `@Bean` در Spring نمونه است.
- **Abstract Factory:** خانواده‌ای از factoryهای مرتبط.
- **Builder:** ساخت گام‌به‌گام شیء پیچیده/immutable. Lombok `@Builder`.
- **Prototype:** کپی از یک نمونه.

**چرا مهم است:**

این الگوها در JDK و Spring همه‌جا هستند. Builder برای شیء با پارامترهای زیاد و immutability ضروری است.

**مثال کد:**

```java
// Singleton با enum — بهترین روش
public enum ConnectionPool {
    INSTANCE;
    private final DataSource dataSource = createDataSource();
    public Connection get() { return dataSource.getConnection(); }
}

// Builder برای شیء immutable با پارامترهای زیاد
public record HttpRequest(String url, String method, Map<String,String> headers) {
    public static class Builder {
        private String url, method = "GET";
        private final Map<String,String> headers = new HashMap<>();
        public Builder url(String u) { this.url = u; return this; }
        public Builder header(String k, String v) { headers.put(k, v); return this; }
        public HttpRequest build() { return new HttpRequest(url, method, headers); }
    }
}
```

**نکات کلیدی:**

- enum بهترین Singleton است (در برابر serialization/reflection امن).
- Builder برای پارامترهای اختیاری زیاد به‌جای telescoping constructor.
- در Spring از container singleton استفاده کنید نه Singleton دستی.

---

### Structural Patterns

**توضیح:**

- **Adapter:** wrap کردن یک interface ناسازگار به interface مورد انتظار.
- **Decorator:** افزودن رفتار به شیء بدون تغییر کلاس آن، با wrap. (مثل `BufferedReader(new FileReader())`؛ Spring AOP هم decorator-like است.)
- **Proxy:** کنترل دسترسی به شیء (lazy، security، logging). dynamic proxy در Spring.
- **Facade:** interface ساده روی زیرسیستم پیچیده (Service layer).
- **Composite:** ساختار درختی که شیء و گروه را یکسان رفتار می‌کند.

**مثال کد:**

```java
// Decorator: افزودن caching بدون تغییر سرویس اصلی
interface UserService { User find(Long id); }

class CachingUserService implements UserService {
    private final UserService delegate;
    private final Map<Long,User> cache = new ConcurrentHashMap<>();
    CachingUserService(UserService d) { this.delegate = d; }
    public User find(Long id) { return cache.computeIfAbsent(id, delegate::find); }
}
```

**نکات کلیدی:**

- Decorator رفتار را به‌صورت ترکیبی (نه وراثت) می‌چسباند.
- Proxy و Decorator ساختار مشابه دارند اما قصد متفاوت (کنترل دسترسی در برابر افزودن رفتار).

---

### Behavioral Patterns

**توضیح:**

- **Strategy:** الگوریتم‌های قابل‌تعویض پشت یک interface (`Comparator`، `PaymentStrategy`). در Spring با تزریق لیست/map از پیاده‌سازی‌ها.
- **Observer:** publish/subscribe (Spring Events).
- **Template Method:** اسکلت الگوریتم در والد، جزئیات در فرزند (`JdbcTemplate`).
- **Command:** بسته‌بندی request به‌عنوان شیء.
- **Chain of Responsibility:** زنجیره‌ی handlerها (Servlet Filter chain، Spring Security).
- **Iterator:** پیمایش بدون افشای ساختار (`Iterable`).
- **State:** رفتار بر اساس state داخلی.

**مثال کد:**

```java
// Strategy با Spring: انتخاب پیاده‌سازی بر اساس نوع
interface PaymentStrategy { boolean supports(String type); void pay(Order o); }

@Service
class PaymentProcessor {
    private final List<PaymentStrategy> strategies;
    PaymentProcessor(List<PaymentStrategy> strategies) { this.strategies = strategies; }
    void process(String type, Order order) {
        strategies.stream().filter(s -> s.supports(type)).findFirst()
            .orElseThrow().pay(order);
    }
}
```

**نکات کلیدی:**

- Strategy جایگزین تمیز برای if/else بزرگ یا switch روی نوع.
- Spring لیست/map پیاده‌سازی‌های یک interface را خودکار تزریق می‌کند.
- Chain of Responsibility پایه‌ی filter chain است.

---

## 🎯 سوالات مصاحبه

### سوال ۱: بهترین راه پیاده‌سازی Singleton thread-safe چیست؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

چند روش: (۱) **enum** — بهترین؛ JVM یکتایی را تضمین می‌کند، در برابر serialization و reflection امن است، و thread-safe به‌صورت ذاتی. (۲) **eager static field** — ساده و thread-safe اما همیشه ساخته می‌شود حتی اگر استفاده نشود. (۳) **double-checked locking** — lazy و thread-safe اما باید فیلد `volatile` باشد (وگرنه به‌خاطر reordering یک نمونه‌ی نیمه‌ساخته دیده می‌شود) و پیاده‌سازی ظریف است. (۴) **initialization-on-demand holder** — lazy، thread-safe، بدون synchronization (با class loading). در عمل، در برنامه‌ی Spring اصلاً Singleton دستی ننویسید؛ از bean singleton container استفاده کنید.

**کد توضیحی:**

```java
// double-checked locking — volatile ضروری است
class Config {
    private static volatile Config instance;
    static Config getInstance() {
        if (instance == null) {
            synchronized (Config.class) {
                if (instance == null) instance = new Config();
            }
        }
        return instance;
    }
}
```

**نکته مصاحبه:**

تمایز Senior: چرا `volatile` در DCL ضروری است (reordering) و چرا enum بهترین است. Follow-up: «reflection چطور Singleton را می‌شکند و enum چطور مقاوم است؟»

---

### سوال ۲: Strategy pattern کجا و چرا؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

Strategy وقتی استفاده می‌شود که چند الگوریتم/رفتار جایگزین برای یک کار دارید و می‌خواهید در runtime انتخاب کنید بدون if/else بزرگ. هر استراتژی یک interface مشترک را پیاده می‌کند. مزایا: رعایت Open/Closed (افزودن استراتژی جدید بدون تغییر کد موجود)، تست‌پذیری، و حذف switch/if پراکنده. در Spring بسیار طبیعی است: همه‌ی پیاده‌سازی‌های یک interface را به‌صورت `List` یا `Map` تزریق می‌کنید و بر اساس شرط انتخاب می‌کنید. مثال‌ها: روش‌های پرداخت، الگوریتم‌های قیمت‌گذاری، notification channels.

**نکته مصاحبه:**

Senior به ربط با Open/Closed و تزریق خودکار Spring اشاره می‌کند. Follow-up: «Strategy با State چه فرقی دارد؟»

---

### سوال ۳: کدام design pattern را در Spring/JDK دیده‌ای؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

نمونه‌های واقعی: **Proxy** (Spring AOP، dynamic proxy برای `@Transactional`)، **Template Method** (`JdbcTemplate`, `RestTemplate`)، **Factory** (`@Bean`, `BeanFactory`)، **Singleton** (Spring beans)، **Observer** (`ApplicationEvent`)، **Decorator** (`BufferedReader`, `Collections.synchronizedList`)، **Builder** (`UriComponentsBuilder`, `Stream.Builder`)، **Strategy** (`Comparator`, `PlatformTransactionManager` پیاده‌سازی‌ها)، **Adapter** (`HandlerAdapter`)، **Chain of Responsibility** (Servlet Filter، Spring Security filter chain). توانایی نام بردن این‌ها نشان می‌دهد patternها را در عمل می‌شناسید نه فقط تئوری.

**نکته مصاحبه:**

Senior مثال‌های concrete از framework می‌آورد نه تعریف کتابی.

---

### سوال ۴: تفاوت Proxy و Decorator چیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

از نظر ساختار مشابه‌اند (هر دو یک شیء را wrap می‌کنند و همان interface را پیاده می‌کنند) اما **قصد** فرق دارد. Decorator رفتار جدید **اضافه** می‌کند (مثل caching، logging، buffering) و معمولاً چند لایه stack می‌شود. Proxy دسترسی به شیء را **کنترل** می‌کند بدون افزودن رفتار اصلی جدید: lazy initialization، access control/security، remote proxy، یا lazy loading. در Spring، AOP از proxy استفاده می‌کند تا cross-cutting concerns را تزریق کند که عملاً مرز بین این دو را محو می‌کند.

**نکته مصاحبه:**

Senior تمایز «افزودن رفتار» در برابر «کنترل دسترسی» را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: double-checked locking بدون volatile

```java
// ❌ بدون volatile → نمونه‌ی نیمه‌ساخته دیده می‌شود
private static Config instance;
```

```java
// ✅
private static volatile Config instance;
```

**توضیح:** reordering می‌تواند ارجاع را قبل از کامل شدن سازنده منتشر کند.

---

### اشتباه ۲: Singleton دستی در Spring

```java
// ❌ مبارزه با container
class MyService { private static MyService instance = new MyService(); }
```

```java
// ✅ از bean singleton استفاده کنید
@Service class MyService {}
```

**توضیح:** Spring خودش lifecycle و singleton را مدیریت می‌کند.

---

### اشتباه ۳: switch/if بزرگ به‌جای Strategy

```java
// ❌
if (type.equals("card")) {...} else if (type.equals("paypal")) {...} ...
```

```java
// ✅ Strategy + تزریق (بالا)
```

**توضیح:** Strategy افزودن نوع جدید را بدون تغییر کد موجود ممکن می‌کند (Open/Closed).

---

## 🔗 ارتباط با سایر مفاهیم

- patternها با **SOLID (1.1)** و **Clean Architecture (15.1)**.
- Strategy/Factory با **Spring DI (2.1)** و تزریق لیست/map.
- Proxy/Decorator با **Spring AOP** و **`@Transactional`**.
- Chain of Responsibility با **Spring Security filter chain** و **Spring Integration**.
