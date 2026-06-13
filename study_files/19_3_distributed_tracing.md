# Distributed Tracing عملی

> دنبال کردن یک request در سرویس‌های متعدد. پایه‌ی debugging و performance در میکروسرویس.

---

## 📖 مفاهیم

### Propagation & Manual Span

**توضیح:**

در میکروسرویس، یک request از چند سرویس عبور می‌کند. distributed tracing با **TraceId** (یکتا برای کل request) و **SpanId** (هر مرحله) آن را دنبال می‌کند. context بین سرویس‌ها از طریق header استاندارد W3C (`traceparent`, `tracestate`) propagate می‌شود. در Spring Boot 3+ با Micrometer Tracing خودکار است. می‌توان span سفارشی هم ساخت.

**مثال کد:**

```java
// span دستی با Micrometer Observation
Observation.createNotStarted("order.processing", observationRegistry)
    .contextualName("Processing order")
    .lowCardinalityKeyValue("orderId", orderId.toString())
    .observe(() -> processOrder(orderId));
```

**نکات کلیدی:**

- context (traceId) باید در همه‌ی hopها propagate شود (HTTP، Kafka headers، async).
- low cardinality برای tag (نه value با کاردینالیتی بالا مثل userId در همه).
- در async/thread جدید، context را صریح propagate کنید (مشکل رایج).

---

## 🎯 سوالات مصاحبه

### سوال ۱: trace context در async/thread جدید چطور propagate می‌شود؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

trace context معمولاً در ThreadLocal (یا MDC) نگه داشته می‌شود، پس وقتی کار به thread دیگری منتقل می‌شود (`@Async`, CompletableFuture, executor)، context **به‌صورت خودکار منتقل نمی‌شود** و span گم می‌شود (trace شکسته). راه‌حل: (۱) wrap کردن executor با `ContextPropagatingTaskDecorator` یا معادل که context را به thread جدید کپی می‌کند. (۲) Micrometer Context Propagation که این را برای reactive و async مدیریت می‌کند. (۳) در Java 21، **ScopedValues** جایگزین بهتری از ThreadLocal برای propagation با virtual threads است. این یکی از مشکلات رایج tracing است: trace در مرز async می‌شکند مگر صریحاً propagate شود.

**نکته مصاحبه:**

Lead به شکستن context در async و ScopedValues اشاره می‌کند.

---

### سوال ۲: چرا sampling در tracing لازم است؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

trace کردن هر request overhead دارد: حافظه برای نگه‌داری span، شبکه برای ارسال به backend (Jaeger)، و storage برای نگه‌داری. در سیستم پرترافیک (میلیون‌ها request)، trace همه غیرعملی و گران است. **sampling** فقط درصدی (مثلاً ۱-۱۰٪) را trace می‌کند. انواع: head-based (در ابتدا تصمیم، ساده) و tail-based (بعد از کامل شدن، می‌تواند فقط traceهای کند/خطادار را نگه دارد — هوشمندتر اما پیچیده‌تر). trade-off: sampling کم overhead و هزینه را کم می‌کند اما ممکن trace یک مشکل خاص را از دست بدهید. برای debug یک مشکل، می‌توان sampling را موقتاً بالا برد یا از tail-based برای نگه‌داری traceهای مشکل‌دار استفاده کرد.

**نکته مصاحبه:**

Senior به head/tail-based sampling اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: شکستن trace در async

```text
❌ @Async بدون propagation → trace گم می‌شود
✅ context propagation decorator
```

**توضیح:** context در ThreadLocal به thread جدید منتقل نمی‌شود.

---

### اشتباه ۲: tag با کاردینالیتی بالا

```text
❌ tag کردن span با userId/requestId (کاردینالیتی بالا) → انفجار metric
✅ low cardinality tags؛ شناسه‌ها در span attribute نه metric label
```

**توضیح:** high cardinality در metric label فاجعه‌ی storage است.

---

## 🔗 ارتباط با سایر مفاهیم

- tracing با **Spring Cloud/Micrometer (2.6)** و **observability (10.4, 16.4)**.
- propagation با **ScopedValues (1.6)** و **async/virtual threads**.
- با **OpenTelemetry (16.4)**.
