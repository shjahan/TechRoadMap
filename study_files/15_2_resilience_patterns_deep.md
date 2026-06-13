# Resilience Patterns عمیق — Circuit Breaker، Bulkhead، Retry، SAGA Orchestration

> الگوهای مقاومت در سیستم توزیع‌شده. ترتیب ترکیب و طراحی fallback در سطح Lead پرسیده می‌شود.

---

## 📖 مفاهیم

### Circuit Breaker States

**توضیح:**

سه حالت با گذار:
- **CLOSED → OPEN:** وقتی نرخ خطا از آستانه گذشت.
- **OPEN → HALF_OPEN:** بعد از `waitDuration`.
- **HALF_OPEN → CLOSED:** اگر فراخوانی‌های آزمایشی موفق.
- **HALF_OPEN → OPEN:** اگر شکست.

پیکربندی Resilience4j: `failureRateThreshold`, `slowCallRateThreshold`, `waitDurationInOpenState`, `slidingWindowSize`, `permittedNumberOfCallsInHalfOpenState`, `recordExceptions`/`ignoreExceptions`.

**مثال کد:**

```java
CircuitBreakerConfig.custom()
    .failureRateThreshold(50)                       // 50% خطا → OPEN
    .slowCallRateThreshold(80)
    .slowCallDurationThreshold(Duration.ofSeconds(2))
    .waitDurationInOpenState(Duration.ofSeconds(30))
    .permittedNumberOfCallsInHalfOpenState(5)
    .slidingWindowSize(10)
    .recordExceptions(HttpServerErrorException.class)
    .ignoreExceptions(BusinessException.class)       // خطای کسب‌وکار باز نکند
    .build();
```

**نکات کلیدی:**

- `ignoreExceptions` برای خطای کسب‌وکار (نباید circuit را باز کند).
- sliding window count-based یا time-based.

---

### Bulkhead & ترتیب ترکیب

**توضیح:**

**Bulkhead** منابع را ایزوله می‌کند: Thread Pool Bulkhead (pool جدا per dependency) یا Semaphore Bulkhead (محدود کردن concurrent calls). هدف: شکست یک سرویس بقیه را غرق نکند. **ترتیب ترکیب** annotationها مهم است؛ معمول: `Retry(CircuitBreaker(RateLimiter(TimeLimiter(call))))` — TimeLimiter داخلی‌ترین (هر تلاش timeout دارد)، Retry بیرونی‌ترین.

**مثال کد:**

```java
@CircuitBreaker(name = "payment", fallbackMethod = "fallback")
@Retry(name = "payment")
@Bulkhead(name = "payment")
@TimeLimiter(name = "payment")
public CompletableFuture<Result> charge(Request req) { /* ... */ }

public CompletableFuture<Result> fallback(Request req, Throwable t) {
    return CompletableFuture.completedFuture(Result.degraded());
}
```

**نکات کلیدی:**

- Bulkhead از starvation و cascade جلوگیری می‌کند.
- fallback باید graceful degradation بدهد نه خطای دیگر.

---

### SAGA Orchestration

**توضیح:**

برای تراکنش توزیع‌شده، یک orchestrator مرکزی مراحل را هدایت می‌کند و در صورت شکست، compensating transactions اجرا می‌کند. مزیت orchestration بر choreography: flow متمرکز و قابل‌مشاهده، اما single point و coupling به orchestrator.

**مثال کد:**

```java
// orchestrator: مراحل و compensation
class OrderSaga {
    void handle(OrderCreated e) { send(new ReserveInventory(e.orderId())); }
    void handle(InventoryReserved e) { send(new ProcessPayment(e.orderId())); }
    void handle(PaymentFailed e) { send(new ReleaseInventory(e.orderId())); } // compensate
}
```

**نکات کلیدی:**

- orchestration visibility بهتر؛ choreography decoupling بهتر.
- compensation باید idempotent و قابل‌اعتماد باشد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: ترتیب ترکیب resilience annotationها چرا مهم است؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

هر annotation یک aspect با ترتیب اجرای متفاوت است و رفتار کلی به ترتیب wrap بستگی دارد. ترتیب متداول از بیرون به درون: `Retry → CircuitBreaker → RateLimiter → TimeLimiter → call`. منطق: TimeLimiter داخلی‌ترین تا هر تلاش جداگانه timeout داشته باشد (نه کل چرخه). CircuitBreaker باید شکست‌ها را ببیند تا state را به‌روز کند. Retry بیرونی‌تر تا اگر یک تلاش fail شد، کل چرخه (شامل circuit breaker check) دوباره اجرا شود. اما این تصمیم trade-off دارد: اگر Retry بیرون CircuitBreaker باشد، retryها می‌توانند circuit را سریع‌تر باز کنند؛ اگر داخل باشد، رفتار متفاوت است. نکته‌ی مهم: این یک تصمیم آگاهانه بر اساس سناریوست، نه قانون ثابت — باید بفهمید چه می‌خواهید.

**نکته مصاحبه:**

Lead نشان می‌دهد این تصمیم آگاهانه است نه پیش‌فرض کورکورانه.

---

### سوال ۲: یک fallback خوب چه ویژگی‌هایی دارد؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

fallback باید **graceful degradation** بدهد — یک پاسخ معقول وقتی سرویس اصلی در دسترس نیست. ویژگی‌ها: (۱) **قطعی و سریع** — نباید خودش به سرویس خارجی دیگری وابسته باشد که ممکن fail شود (وگرنه fallback هم می‌شکند). (۲) **معنادار برای کاربر** — مثلاً نمایش داده‌ی cached، مقدار پیش‌فرض، یا صف کردن برای پردازش بعدی، نه فقط خطا. (۳) **آگاه از context** — مثلاً برای پرداخت، «pending» برگرداند و بعداً پردازش کند، نه «failed». (۴) **بدون side-effect خطرناک**. مثال خوب: اگر سرویس توصیه down است، لیست محصولات پرفروش عمومی را نشان بده به‌جای صفحه‌ی خالی. fallback بد: فراخوانی یک API دیگر که آن هم ممکن fail شود.

**نکته مصاحبه:**

Senior به «fallback نباید به سرویس خارجی دیگری وابسته باشد» اشاره می‌کند.

---

### سوال ۳: orchestration در برابر choreography SAGA؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

در **choreography**، هر سرویس به رویدادها واکنش می‌دهد و رویداد بعدی را منتشر می‌کند — غیرمتمرکز، loose coupling، اما **دنبال کردن flow کلی سخت است** (منطق پخش شده در سرویس‌ها، debugging دشوار، و خطر چرخه‌ی رویداد). در **orchestration**، یک orchestrator مرکزی مراحل را به‌ترتیب صدا می‌زند و compensation را مدیریت می‌کند — **visibility و کنترل بهتر** (کل flow در یک جا)، اما orchestrator یک نقطه‌ی coupling و potential bottleneck است. انتخاب: برای flow ساده با چند سرویس، choreography (decoupling)؛ برای flow پیچیده با مراحل زیاد و نیاز به monitoring/کنترل، orchestration. بسیاری سیستم‌ها ترکیب می‌کنند.

**نکته مصاحبه:**

Lead trade-off visibility در برابر coupling را می‌فهمد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: circuit breaker باز شدن با خطای کسب‌وکار

```java
// ❌ خطای validation (400) circuit را باز می‌کند
.recordExceptions(Exception.class)
```

```java
// ✅
.ignoreExceptions(BusinessException.class)
```

**توضیح:** فقط خطای زیرساختی (5xx، timeout) باید circuit را باز کند.

---

### اشتباه ۲: fallback وابسته به سرویس خارجی

```java
// ❌ fallback خودش fail می‌شود
Result fallback(Req r, Throwable t) { return anotherRemoteCall(); }
```

```java
// ✅ degradation محلی
Result fallback(Req r, Throwable t) { return Result.cachedOrDefault(); }
```

**توضیح:** fallback باید مستقل و قطعی باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- resilience با **Spring Cloud (2.6)** و **microservices (6.1)**.
- SAGA با **distributed transactions** و **Outbox/Kafka (8.1)**.
- bulkhead با **thread pool** و **concurrency**.
- circuit breaker با **System Design (cascade failure) (6.2)**.
