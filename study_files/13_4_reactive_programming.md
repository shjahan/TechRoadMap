# Reactive Programming عمیق‌تر — Reactor، Schedulers، Backpressure، R2DBC

> برنامه‌نویسی reactive با Project Reactor. درک backpressure و schedulers برای WebFlux ضروری است.

---

## 📖 مفاهیم

### Reactor — Mono، Flux، Operators

**توضیح:**

Project Reactor پیاده‌سازی Reactive Streams است. `Mono<T>` (0 یا 1) و `Flux<T>` (0 تا N). operatorها (مثل Stream اما async و با مدیریت خطا): `map`, `filter`, `flatMap`, `onErrorResume`, `retryWhen`, `timeout`, `collectList`. اصل کلیدی: **lazy** — تا قبل از `subscribe` هیچ‌چیز اجرا نمی‌شود (publisher فقط blueprint است).

**مثال کد:**

```java
Flux.range(1, 10)
    .filter(n -> n % 2 == 0)
    .flatMap(n -> Mono.fromCallable(() -> fetchFromDb(n))
                      .subscribeOn(Schedulers.boundedElastic())) // blocking ایزوله
    .onErrorResume(e -> Flux.empty())                  // مدیریت خطا
    .retryWhen(Retry.backoff(3, Duration.ofSeconds(1))) // retry
    .timeout(Duration.ofSeconds(5))
    .subscribe(System.out::println); // اینجا اجرا شروع می‌شود
```

**نکات کلیدی:**

- nothing happens until subscribe.
- `flatMap` برای async تو در تو؛ `map` برای تبدیل sync.
- خطا یک سیگنال است؛ با `onErrorResume`/`retryWhen` مدیریت کنید.

---

### Schedulers

**توضیح:**

Schedulers تعیین می‌کنند کار روی کدام thread اجرا شود:
- `Schedulers.immediate()`: thread جاری.
- `Schedulers.single()`: یک thread reusable.
- `Schedulers.boundedElastic()`: برای کار **blocking** (مثل JDBC) — pool قابل‌رشد محدود.
- `Schedulers.parallel()`: CPU-bound، به‌اندازه‌ی هسته‌ها.

`subscribeOn` کل زنجیره (از منبع) را تعیین می‌کند؛ `publishOn` از آن نقطه به بعد را عوض می‌کند.

**نکات کلیدی:**

- کار blocking را با `boundedElastic` ایزوله کنید تا event-loop بلاک نشود.
- `parallel` برای CPU-bound، نه برای I/O blocking.

---

### Hot vs Cold & Backpressure

**توضیح:**

**Cold publisher** برای هر subscriber از ابتدا تولید می‌کند (`Flux.fromIterable`). **Hot publisher** یک stream مشترک برای همه (`Sinks`، `ConnectableFlux`) — subscriber دیر، رویدادهای قبلی را از دست می‌دهد. **Backpressure:** وقتی producer سریع‌تر از consumer است، استراتژی‌ها: `onBackpressureBuffer` (buffer)، `onBackpressureDrop` (دور انداختن)، `onBackpressureLatest` (فقط آخرین)، `onBackpressureError`.

**نکات کلیدی:**

- cold برای داده‌ی per-subscriber؛ hot برای رویداد مشترک real-time.
- backpressure از overwhelm شدن consumer جلوگیری می‌کند.

---

### R2DBC

**توضیح:**

`DatabaseClient`/`R2dbcRepository` — دسترسی reactive به SQL (جایگزین JDBC blocking). فقط وقتی منطقی است که **کل stack** reactive باشد (JDBC در WebFlux event-loop را بلاک می‌کند). R2DBC هنوز کمتر بالغ از JPA است (بدون lazy loading، روابط پیچیده محدود).

**نکات کلیدی:**

- R2DBC فقط برای stack کاملاً reactive.
- با virtual threads (Java 21)، اغلب JDBC blocking + MVC ساده‌تر و کافی است.

---

## 🎯 سوالات مصاحبه

### سوال ۱: backpressure چیست و چطور مدیریت می‌شود؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

backpressure مکانیزمی است که در آن consumer می‌تواند نرخ تولید producer را کنترل کند تا overwhelm نشود (memory پر نشود). در Reactive Streams، subscriber با `request(n)` اعلام می‌کند چند آیتم می‌تواند بپذیرد، و producer فقط همان مقدار می‌فرستد (pull-push hybrid). وقتی producer ذاتاً نمی‌تواند کند شود (مثل رویدادهای خارجی)، استراتژی‌ها: `onBackpressureBuffer` (در buffer نگه دار — خطر OOM اگر نامحدود)، `onBackpressureDrop` (آیتم‌های اضافه را دور بریز)، `onBackpressureLatest` (فقط جدیدترین را نگه دار)، `onBackpressureError` (خطا بده). انتخاب بستگی به اینکه از دست رفتن داده قابل‌تحمل است یا نه. این یکی از مزایای اصلی reactive بر مدل ساده‌ی async است.

**نکته مصاحبه:**

Lead به `request(n)` و trade-off استراتژی‌ها اشاره می‌کند.

---

### سوال ۲: چرا کار blocking در reactive باید با boundedElastic ایزوله شود؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

WebFlux/Reactor با تعداد کمی event-loop thread (به‌اندازه‌ی هسته‌ها) کار می‌کند. اگر یک عملیات blocking (JDBC، `Thread.sleep`، فایل blocking) روی این threadها اجرا شود، آن thread مسدود می‌شود و نمی‌تواند رویدادهای دیگر را پردازش کند — throughput سقوط می‌کند و کل مزیت reactive از بین می‌رود. `subscribeOn(Schedulers.boundedElastic())` آن کار را به یک thread pool جدا (مخصوص blocking، قابل‌رشد) منتقل می‌کند تا event-loop آزاد بماند. اما این فقط یک workaround است؛ بهتر است کل stack non-blocking باشد (R2DBC به‌جای JDBC). نکته‌ی مدرن: virtual threads این مشکل را برای مدل blocking حل کرده‌اند.

**نکته مصاحبه:**

Senior می‌داند boundedElastic فقط workaround است و stack باید reactive باشد.

---

### سوال ۳: hot در برابر cold publisher؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

cold publisher برای هر subscriber جریان را از ابتدا و مستقل تولید می‌کند — مثل `Flux.range` یا یک DB query که هر subscriber کل نتیجه را می‌گیرد. hot publisher یک جریان مشترک است که مستقل از subscriber تولید می‌کند؛ subscriberها فقط رویدادهای بعد از اتصال خود را می‌گیرند (مثل رویدادهای real-time، sensor، یا `Sinks`). تفاوت کلیدی: در cold، subscriber دیر هم همه را می‌گیرد؛ در hot، رویدادهای قبل از subscribe از دست می‌روند. برای تبدیل cold به hot از `share()`/`publish().refCount()` استفاده می‌شود (تا چند subscriber یک منبع را share کنند به‌جای اجرای مجدد).

**نکته مصاحبه:**

Senior به `share()` برای multicast اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: blocking در event-loop

```java
// ❌ JDBC در reactive chain
flux.map(id -> jdbcRepo.findById(id));
```

```java
// ✅
flux.flatMap(id -> Mono.fromCallable(() -> jdbcRepo.findById(id))
                       .subscribeOn(Schedulers.boundedElastic()));
```

**توضیح:** blocking روی event-loop throughput را نابود می‌کند.

---

### اشتباه ۲: فراموشی subscribe

```java
// ❌ هیچ‌چیز اجرا نمی‌شود
Mono.fromCallable(() -> doWork());
```

```java
// ✅ در WebFlux، framework subscribe می‌کند؛ در کد عادی خودتان
mono.subscribe();
```

**توضیح:** بدون subscriber، publisher فقط blueprint است.

---

### اشتباه ۳: onBackpressureBuffer نامحدود

```java
// ❌ OOM اگر producer بسیار سریع‌تر باشد
.onBackpressureBuffer()
```

```java
// ✅ buffer محدود + استراتژی overflow
.onBackpressureBuffer(1000, BufferOverflowStrategy.DROP_OLDEST)
```

**توضیح:** buffer نامحدود می‌تواند memory را پر کند.

---

## 🔗 ارتباط با سایر مفاهیم

- Reactor با **WebFlux (2.3)** و **Mono/Flux**.
- backpressure با **System Design (6.2)** و **Kafka**.
- virtual threads (1.5) به‌عنوان جایگزین ساده‌تر reactive.
- R2DBC با **Spring Data (2.4)**.
