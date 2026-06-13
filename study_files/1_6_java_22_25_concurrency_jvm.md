# Java 22–25 + Concurrency عمیق + JVM Internals

> تازه‌ترین ویژگی‌ها (Stream Gatherers، Scoped Values) به‌علاوه‌ی concurrency و JVM internals که قلب سوالات سطح Lead هستند.

---

## 📖 مفاهیم

### Stream Gatherers (Java 24 preview → 25 final)

**توضیح:**

تا قبل از این، عملیات میانی Stream محدود به مجموعه‌ی ثابتی بود (`map`, `filter`, …). برای منطق سفارشی (مثل sliding window، grouping متوالی) باید به collector یا کد دستی می‌رفتید. `Stream.gather(Gatherer)` امکان تعریف عملیات میانی **سفارشی و stateful** را می‌دهد — معادل `Collector` اما برای مرحله‌ی میانی.

**چرا مهم است:**

عملیاتی مثل windowing، running aggregation و deduplication متوالی که قبلاً ناخوشایند بودند، حالا تمیز و قابل‌ترکیب می‌شوند.

**مثال کد:**

```java
// پنجره‌های لغزان از ۳ عنصر با gatherer آماده
List<List<Integer>> windows = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowSliding(3))
    .toList(); // [[1,2,3],[2,3,4],[3,4,5]]

// پنجره‌های ثابت
List<List<Integer>> fixed = Stream.of(1, 2, 3, 4, 5)
    .gather(Gatherers.windowFixed(2))
    .toList(); // [[1,2],[3,4],[5]]
```

**نکات کلیدی:**

- Gatherer مکمل Collector است: یکی برای مرحله‌ی میانی، دیگری برای نهایی.
- gathererهای آماده: `windowFixed`, `windowSliding`, `fold`, `scan`, `mapConcurrent`.

---

### Scoped Values (جایگزین ThreadLocal)

**توضیح:**

`ThreadLocal` برای انتقال context (مثل user جاری، trace id) استفاده می‌شد اما مشکلاتی داشت: mutable، احتمال memory leak (به‌خصوص با thread pool)، و سنگین برای میلیون‌ها virtual thread. `ScopedValue` یک جایگزین immutable و محدوده‌دار است: مقدار فقط در طول یک scope مشخص معتبر است و خودکار پاک می‌شود، که با virtual threads و structured concurrency سازگارتر است.

**مثال کد:**

```java
private static final ScopedValue<String> USER_ID = ScopedValue.newInstance();

void handleRequest(String userId) {
    ScopedValue.where(USER_ID, userId).run(() -> {
        processOrder(); // USER_ID در این scope در دسترس است
    });
    // بیرون scope، USER_ID دیگر bind نیست
}

void processOrder() {
    String currentUser = USER_ID.get(); // دسترسی immutable
}
```

**نکات کلیدی:**

- immutable و scope-bound → بدون leak، مناسب virtual threads.
- مقدار خودکار در پایان scope پاک می‌شود.

---

### Flexible Constructor Bodies & Module Import (Java 25)

**توضیح:**

پیش از Java 25، `super()`/`this()` باید اولین دستور سازنده می‌بود؛ نمی‌شد قبل از آن validation انجام داد. **Flexible Constructor Bodies** اجازه می‌دهد قبل از `super()` کد (مثل validation آرگومان‌ها) بنویسید — جلوگیری از اجرای سازنده‌ی والد با داده‌ی نامعتبر. **Module Import Declarations** با `import module java.base;` تمام پکیج‌های یک ماژول را یکجا import می‌کند.

**مثال کد:**

```java
class PositiveInt {
    private final int value;
    PositiveInt(int value) {
        if (value <= 0) throw new IllegalArgumentException(); // قبل از super مجاز شد
        super();
        this.value = value;
    }
}
```

**نکات کلیدی:**

- validation قبل از super از حالت نامعتبر جلوگیری می‌کند.
- Project Leyden روی بهبود startup time و memory با AOT تمرکز دارد.

---

### Java Memory Model — happens-before, volatile

**توضیح:**

JMM قوانین visibility و ordering بین threadها را تعریف می‌کند. رابطه‌ی کلیدی **happens-before** است: اگر عملیات A قبل از B اتفاق بیفتد (به معنای JMM)، اثرات A برای B دیده می‌شوند. منابع happens-before: آزادسازی/گرفتن یک monitor (`synchronized`)، نوشتن/خواندن `volatile`، `Thread.start()`/`join()`.

`volatile` **visibility** را تضمین می‌کند (هر thread آخرین مقدار را می‌بیند و reordering مضر جلوگیری می‌شود) اما **atomicity** عملیات مرکب را نه (مثلاً `i++` که read-modify-write است). برای آن `Atomic` classes یا lock لازم است.

**چرا مهم است:**

باگ‌های concurrency (visibility، race) اغلب متناوب و سخت‌یاب‌اند. درک JMM برای نوشتن کد thread-safe درست ضروری است.

**مثال کد:**

```java
class Flag {
    private volatile boolean running = true; // مناسب برای flag

    void stop() { running = false; }      // نوشتن volatile
    void loop() { while (running) { /* ... */ } } // خواندن volatile → توقف دیده می‌شود
}

class Counter {
    private final AtomicInteger count = new AtomicInteger();
    void inc() { count.incrementAndGet(); } // atomic، نه volatile
}
```

**نکات کلیدی:**

- volatile = visibility، نه atomicity. برای read-modify-write از Atomic استفاده کنید.
- double-checked locking باید از volatile روی instance استفاده کند.
- happens-before پایه‌ی هر استدلال درست درباره‌ی concurrency است.

---

### Executors, CompletableFuture, Locks

**توضیح:**

`ExecutorService` مدیریت thread pool را از منطق تسک جدا می‌کند. `ThreadPoolExecutor` پارامترهای core/max pool، queue و rejection policy دارد. `ForkJoinPool` برای تقسیم‌وغلبه (work-stealing).

`CompletableFuture` برای ترکیب عملیات async به‌صورت declarative: `thenApply`, `thenCompose` (flatMap)، `thenCombine`، `exceptionally`، `handle`. ابزارهای هماهنگی: `CountDownLatch` (انتظار تا N رویداد)، `CyclicBarrier` (نقطه‌ی همگام‌سازی قابل‌استفاده‌ی مجدد)، `Semaphore` (محدود کردن دسترسی همزمان).

Lockها: `ReentrantLock` (انعطاف بیشتر از synchronized، tryLock، fairness)، `ReadWriteLock` (چند reader، یک writer)، `StampedLock` (optimistic read).

**مثال کد:**

```java
ExecutorService executor = Executors.newFixedThreadPool(4);

CompletableFuture<String> result = CompletableFuture
    .supplyAsync(() -> fetchUser(id), executor)
    .thenCompose(user -> CompletableFuture.supplyAsync(() -> fetchOrders(user)))
    .thenApply(orders -> "تعداد: " + orders.size())
    .exceptionally(ex -> "خطا: " + ex.getMessage());

// محدود کردن concurrency با Semaphore
Semaphore limiter = new Semaphore(10);
void call() throws InterruptedException {
    limiter.acquire();
    try { externalApi(); } finally { limiter.release(); }
}
```

**نکات کلیدی:**

- `thenApply` برای تابع همگام، `thenCompose` برای زنجیره‌ی async (مثل flatMap).
- همیشه exception را با `exceptionally`/`handle` مدیریت کنید وگرنه خاموش گم می‌شود.
- `ReentrantLock` را در `finally` آزاد کنید.

---

### JVM Internals — GC, JIT, Class Loading

**توضیح:**

- **Class Loading:** سه classloader (Bootstrap، Platform/Extension، Application) با **parent delegation**: هر loader ابتدا از والد می‌خواهد load کند.
- **GC:** الگوریتم‌های اصلی: Serial، Parallel (throughput)، G1 (پیش‌فرض از Java 9، تعادل)، ZGC و Shenandoah (latency پایین، pause زیر میلی‌ثانیه).
- **JIT:** کد داغ از interpreter به C1 سپس C2 کامپایل می‌شود (Tiered Compilation). بهینه‌سازی‌های کلیدی: inlining، escape analysis.

**چرا مهم است:**

برای تشخیص memory leak، tuning pause، و کاهش startup time لازم است. سوالات Lead معمولاً اینجا متمرکزند.

**مثال کد:**

```bash
# انتخاب GC و heap
java -XX:+UseZGC -Xms2g -Xmx2g -Xlog:gc*:file=gc.log MyApp

# Flight Recorder برای profiling
java -XX:StartFlightRecording=duration=60s,filename=rec.jfr MyApp
```

**نکات کلیدی:**

- `-Xms` = `-Xmx` بگذارید تا از resize حین اجرا جلوگیری شود.
- G1 پیش‌فرض و متعادل؛ ZGC برای latency بحرانی.
- escape analysis می‌تواند اشیاء را روی stack تخصیص دهد (scalar replacement).

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت `volatile` و `synchronized` چیست؟

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

`volatile` فقط **visibility** و جلوگیری از reordering را برای یک متغیر تضمین می‌کند: هر thread همیشه آخرین مقدار نوشته‌شده را می‌بیند. اما atomicity عملیات مرکب را تضمین نمی‌کند؛ `count++` با volatile همچنان race دارد چون سه عمل (read, modify, write) است.

`synchronized` هم visibility و هم **mutual exclusion** (atomicity) را تضمین می‌کند: فقط یک thread در یک زمان وارد بلوک می‌شود و هنگام خروج، تغییرات را flush می‌کند. اما هزینه‌ی lock و احتمال contention دارد.

قاعده: volatile برای flag ساده یا یک نوشتن/چند خواندن؛ synchronized (یا Atomic/Lock) برای عملیات مرکب و invariant چندمتغیره.

**کد توضیحی:**

```java
volatile boolean ready;          // ✅ مناسب: flag
volatile int counter;            // ❌ نامناسب: counter++ atomic نیست
AtomicInteger safeCounter;       // ✅ برای counter
```

**نکته مصاحبه:**

تمایز Lead: توضیح happens-before و اینکه چرا volatile برای `i++` کافی نیست. Follow-up: «double-checked locking چرا به volatile نیاز دارد؟»

---

### سوال ۲: ConcurrentHashMap چطور thread-safe است؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

تا Java 7، `ConcurrentHashMap` از **segment locking** (تقسیم به segmentها، هر کدام lock جدا) استفاده می‌کرد تا concurrency نوشتن را بالا ببرد. از Java 8، این به **CAS (compare-and-swap)** روی هر bucket به‌علاوه‌ی synchronized روی سر bucket هنگام collision تغییر کرد. خواندن معمولاً بدون lock است (با volatile node). همچنین مثل HashMap، binهای بزرگ به درخت قرمز-سیاه تبدیل می‌شوند.

برخلاف `Collections.synchronizedMap` که کل map را با یک lock می‌پیچد، `ConcurrentHashMap` lock granular دارد و مقیاس بهتری می‌دهد. عملیات atomic مثل `compute`, `merge`, `computeIfAbsent` فراهم است.

**کد توضیحی:**

```java
ConcurrentHashMap<String, Integer> counts = new ConcurrentHashMap<>();
counts.merge("a", 1, Integer::sum); // atomic، thread-safe
```

**نکته مصاحبه:**

Senior به تغییر از segment به CAS در Java 8 و عدم پشتیبانی null (برخلاف HashMap) اشاره می‌کند. Follow-up: «چرا ConcurrentHashMap اجازه‌ی کلید/مقدار null نمی‌دهد؟»

---

### سوال ۳: تفاوت `thenApply` و `thenCompose` در CompletableFuture چیست؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

`thenApply(fn)` خروجی را با یک تابع **همگام** تبدیل می‌کند: `CompletableFuture<T>` → `CompletableFuture<R>` که `fn` برمی‌گرداند `R`. `thenCompose(fn)` برای زنجیره کردن یک عملیات **async دیگر** است: `fn` خودش `CompletableFuture<R>` برمی‌گرداند و `thenCompose` آن را flatten می‌کند تا از `CompletableFuture<CompletableFuture<R>>` جلوگیری شود. دقیقاً مثل تفاوت `map` و `flatMap` در Stream/Optional.

**کد توضیحی:**

```java
// thenApply: تبدیل ساده
cf.thenApply(user -> user.name());

// thenCompose: زنجیره‌ی async
cf.thenCompose(user -> fetchOrdersAsync(user.id())); // برمی‌گرداند CF<List<Order>>
```

**نکته مصاحبه:**

Follow-up: «اگر به اشتباه thenApply با تابع async استفاده کنی چه می‌شود؟» (نوع تو در تو `CF<CF<R>>`).

---

### سوال ۴: GC چطور کار می‌کند و چطور memory leak پیدا می‌کنی؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

GC اشیاء غیرقابل‌دسترس (unreachable از GC roots) را بازیابی می‌کند. اکثر GCهای مدرن generational‌اند: نسل جوان (Eden + Survivor) با Minor GC سریع، نسل پیر با جمع‌آوری کمتر و گران‌تر. G1 (پیش‌فرض) heap را به region تقسیم می‌کند و pause را هدف‌گذاری می‌کند؛ ZGC/Shenandoah concurrent‌اند با pause زیر میلی‌ثانیه.

memory leak در Java معمولاً یعنی نگه‌داشتن ناخواسته‌ی ارجاع (مثلاً static collection که رشد می‌کند، listener حذف‌نشده، یا ThreadLocal در pool). برای یافتن: رصد heap با metrics (Micrometer/JMX)، گرفتن heap dump (`jmap`/JFR)، و تحلیل با Eclipse MAT یا VisualVM برای یافتن «dominator» و مسیر نگه‌داری ارجاع.

**نکته مصاحبه:**

Lead فرایند سیستماتیک (رصد → heap dump → تحلیل dominator tree) را شرح می‌دهد. Follow-up: «تفاوت memory leak با high allocation rate چیست؟»

---

### سوال ۵: parent delegation در class loading چیست و چرا مهم است؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

هر classloader قبل از اینکه خودش کلاسی را load کند، ابتدا از classloader والد می‌خواهد. این تضمین می‌کند کلاس‌های هسته‌ای (مثل `java.lang.String`) همیشه توسط bootstrap loader load شوند و کسی نتواند با قرار دادن `String` جعلی در classpath امنیت را بشکند. همچنین از load دوباره‌ی کلاس‌ها و `ClassCastException` ناشی از دو نسخه‌ی یک کلاس توسط loaderهای مختلف جلوگیری می‌کند. فریم‌ورک‌هایی مثل application serverها و OSGi گاهی این مدل را برای isolation می‌شکنند.

**نکته مصاحبه:**

Follow-up: «چرا گاهی `NoClassDefFoundError` یا `ClassCastException` بین دو loader می‌گیریم؟»

---

### سوال ۶: ThreadPoolExecutor چه پارامترهایی دارد و rejection policy چیست؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

پارامترها: `corePoolSize` (حداقل threadهای زنده)، `maximumPoolSize` (حداکثر)، `keepAliveTime` (مدت زنده‌ماندن threadهای اضافه)، `workQueue` (صف تسک‌ها)، و `RejectedExecutionHandler`. منطق: ابتدا تا core thread می‌سازد، سپس تسک‌ها را در صف می‌گذارد، اگر صف پر شد تا max thread می‌سازد، و اگر باز هم پر بود rejection policy اجرا می‌شود (`AbortPolicy` پیش‌فرض که استثنا می‌دهد، `CallerRunsPolicy`، `DiscardPolicy`، `DiscardOldestPolicy`).

نکته‌ی مهم: با صف نامحدود (مثل `Executors.newFixedThreadPool`)، max pool بی‌اثر می‌شود و ممکن است OOM رخ دهد؛ بنابراین صف کران‌دار + سیاست مناسب توصیه می‌شود.

**نکته مصاحبه:**

Lead به خطر unbounded queue در `newFixedThreadPool` و انتخاب `CallerRunsPolicy` برای backpressure اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: استفاده از volatile برای شمارنده

```java
// ❌ race condition
volatile int count;
void inc() { count++; }
```

```java
// ✅
AtomicInteger count = new AtomicInteger();
void inc() { count.incrementAndGet(); }
```

**توضیح:** `count++` سه عمل است؛ volatile atomicity نمی‌دهد.

---

### اشتباه ۲: بلعیدن استثنا در CompletableFuture

```java
// ❌ خطا خاموش گم می‌شود
CompletableFuture.supplyAsync(this::risky);
```

```java
// ✅
CompletableFuture.supplyAsync(this::risky)
    .exceptionally(ex -> { log.error("failed", ex); return fallback(); });
```

**توضیح:** بدون `exceptionally`/`handle`/`join`، استثنا بی‌سروصدا گم می‌شود.

---

### اشتباه ۳: `newFixedThreadPool` با صف نامحدود برای کار I/O بحرانی

```java
// ❌ صف نامحدود → انباشت تسک → OOM، بدون backpressure
ExecutorService pool = Executors.newFixedThreadPool(10);
```

```java
// ✅ صف کران‌دار + سیاست backpressure
ExecutorService pool = new ThreadPoolExecutor(
    10, 10, 0L, TimeUnit.MILLISECONDS,
    new ArrayBlockingQueue<>(1000),
    new ThreadPoolExecutor.CallerRunsPolicy());
```

**توضیح:** صف نامحدود حافظه را بی‌کنترل پر می‌کند؛ صف کران‌دار backpressure می‌دهد.

---

### اشتباه ۴: آزاد نکردن ReentrantLock در finally

```java
// ❌ اگر استثنا رخ دهد lock آزاد نمی‌شود → deadlock
lock.lock();
doWork();
lock.unlock();
```

```java
// ✅
lock.lock();
try { doWork(); } finally { lock.unlock(); }
```

**توضیح:** lock باید همیشه در `finally` آزاد شود.

---

### اشتباه ۵: ThreadLocal بدون remove در thread pool

```java
// ❌ نشت حافظه: thread در pool زنده می‌ماند و مقدار باقی می‌ماند
threadLocal.set(heavyContext);
```

```java
// ✅
threadLocal.set(heavyContext);
try { process(); } finally { threadLocal.remove(); }
// یا در Java 21+: ScopedValue
```

**توضیح:** thread در pool reuse می‌شود؛ بدون remove مقدار قدیمی نشت می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- Concurrency با **Virtual Threads** (فصل 1.5)، **Reactive** و **resilience patterns** گره خورده است.
- JMM پایه‌ی درست‌نویسی همه‌ی الگوهای **caching** و **distributed lock** است.
- JVM Internals (GC، JIT) با **performance tuning**، **Docker memory limits** و **monitoring** (JFR، Micrometer) ترکیب می‌شود.
- Scoped Values با **distributed tracing** (انتقال context) مرتبط است.
- Stream Gatherers مکمل **Stream API** و الگوهای پردازش داده است.
