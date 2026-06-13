# Spring Cloud — Service Discovery، Gateway، Resilience، Tracing

> ابزارهای ساخت میکروسرویس در Spring. سوالات سطح Lead روی resilience و distributed concerns تمرکز دارند.

---

## 📖 مفاهیم

### Service Discovery

**توضیح:**

در محیط پویا (کانتینر، autoscaling)، آدرس سرویس‌ها ثابت نیست. Service Discovery یک registry است که سرویس‌ها خود را در آن ثبت می‌کنند و دیگران آن‌ها را پیدا می‌کنند. **Eureka** (Netflix OSS) و **Consul** (HashiCorp) نمونه‌اند. دو مدل load balancing: client-side (کلاینت لیست instanceها را می‌گیرد و خودش انتخاب می‌کند — با `@LoadBalanced`) و server-side (یک load balancer مرکزی).

نکته‌ی مدرن: در Kubernetes، خود K8s service discovery و load balancing (با Service و DNS) را فراهم می‌کند، پس Eureka اغلب غیرضروری می‌شود.

**مثال کد:**

```java
@Bean
@LoadBalanced // client-side load balancing روی نام سرویس
RestClient.Builder restClientBuilder() {
    return RestClient.builder();
}

// استفاده: به‌جای host:port از نام سرویس
restClient.get().uri("http://order-service/api/orders/{id}", id).retrieve();
```

**نکات کلیدی:**

- در K8s معمولاً به Eureka نیازی نیست (K8s Service + DNS کافی است).
- client-side LB انعطاف بیشتر؛ server-side سادگی.

---

### API Gateway

**توضیح:**

نقطه‌ی ورود واحد به میکروسرویس‌ها. **Spring Cloud Gateway** (مبتنی بر WebFlux، non-blocking) مسئولیت‌ها را متمرکز می‌کند: routing، authentication، rate limiting، circuit breaker، CORS، logging. مفاهیم: Route (مقصد)، Predicate (شرط تطبیق request)، Filter (تغییر request/response).

**چرا مهم است:**

از تکرار cross-cutting concerns در هر سرویس جلوگیری می‌کند و یک نقطه‌ی کنترل امنیت/ترافیک می‌دهد.

**مثال کد:**

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: order-service
          uri: lb://order-service        # load-balanced
          predicates:
            - Path=/api/orders/**
          filters:
            - StripPrefix=1
            - name: CircuitBreaker
              args:
                name: orderCB
                fallbackUri: forward:/fallback/orders
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100
                redis-rate-limiter.burstCapacity: 200
```

**نکات کلیدی:**

- Gateway را برای auth/rate-limit/circuit-breaker متمرکز کنید.
- چون WebFlux است، filterهای blocking ننویسید.

---

### Resilience (Resilience4j)

**توضیح:**

در سیستم توزیع‌شده، شکست بخشی اجتناب‌ناپذیر است. Resilience4j الگوهای مقاومت می‌دهد:

- **CircuitBreaker:** اگر نرخ خطا از حد گذشت، مدار «باز» می‌شود و فراخوانی‌ها فوراً fail می‌شوند (به‌جای انتظار timeout) تا سرویس خراب فرصت بهبود بیابد. حالت‌ها: CLOSED → OPEN → HALF_OPEN.
- **Retry:** تلاش مجدد با backoff برای خطاهای گذرا.
- **RateLimiter:** محدود کردن نرخ فراخوانی.
- **Bulkhead:** ایزوله کردن منابع تا شکست یک بخش بقیه را غرق نکند.
- **TimeLimiter:** محدودیت زمان.

ترتیب ترکیب مهم است: معمولاً `Retry(CircuitBreaker(RateLimiter(TimeLimiter(call))))`.

**چرا مهم است:**

بدون این الگوها، یک سرویس کند می‌تواند cascade failure ایجاد کند و کل سیستم را down کند.

**مثال کد:**

```java
@Service
class PaymentClient {
    @CircuitBreaker(name = "payment", fallbackMethod = "fallback")
    @Retry(name = "payment")
    @TimeLimiter(name = "payment")
    public CompletableFuture<PaymentResult> charge(PaymentRequest req) {
        return CompletableFuture.supplyAsync(() -> externalGateway.charge(req));
    }

    public CompletableFuture<PaymentResult> fallback(PaymentRequest req, Throwable t) {
        return CompletableFuture.completedFuture(PaymentResult.pending()); // degradation مطلوب
    }
}
```

**نکات کلیدی:**

- CircuitBreaker از cascade failure جلوگیری می‌کند.
- Retry فقط برای خطاهای گذرا و عملیات idempotent.
- fallback باید graceful degradation بدهد نه خطای دیگر.

---

### Config & Tracing

**توضیح:**

**Spring Cloud Config** پیکربندی متمرکز از یک repo (مثلاً Git) برای همه‌ی سرویس‌ها. **Distributed Tracing**: در میکروسرویس یک request از چند سرویس عبور می‌کند؛ برای دیباگ باید آن را end-to-end دنبال کرد. **Micrometer Tracing** (جایگزین Sleuth در Boot 3+) به هر request یک `TraceId` و به هر مرحله `SpanId` می‌دهد که در لاگ‌ها و بین سرویس‌ها propagate می‌شود (استاندارد W3C `traceparent`). backendهایی مثل **Zipkin**/**Jaeger** این span‌ها را جمع و visualize می‌کنند.

**مثال کد:**

```yaml
management:
  tracing:
    sampling:
      probability: 0.1   # 10% در production
  zipkin:
    tracing:
      endpoint: http://zipkin:9411/api/v2/spans
# TraceId و SpanId خودکار در لاگ‌ها (با logback pattern)
```

**نکات کلیدی:**

- TraceId را در لاگ‌ها بگذارید تا correlation ممکن شود.
- sampling را در production پایین نگه دارید (overhead).
- context (traceId) باید بین سرویس‌ها propagate شود (HTTP headers، Kafka headers).

---

## 🎯 سوالات مصاحبه

### سوال ۱: Circuit Breaker چطور کار می‌کند و چه حالت‌هایی دارد؟

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

سه حالت دارد: **CLOSED** (عادی، فراخوانی‌ها عبور می‌کنند و نرخ خطا رصد می‌شود)، **OPEN** (وقتی نرخ خطا از آستانه گذشت، همه‌ی فراخوانی‌ها فوراً fail می‌شوند بدون تماس با سرویس خراب، برای مدت `waitDuration`)، **HALF_OPEN** (پس از انتظار، تعداد محدودی فراخوانی آزمایشی اجازه می‌یابد؛ اگر موفق بودند → CLOSED، اگر شکست خوردند → OPEN).

هدف: جلوگیری از cascade failure. وقتی سرویس downstream کند یا خراب است، بدون circuit breaker هر فراخوانی تا timeout منتظر می‌ماند، threadها انباشته می‌شوند و سرویس فراخوان هم down می‌شود. circuit breaker با fail-fast از این جلوگیری می‌کند و به سرویس خراب فرصت بهبود می‌دهد.

**نکته مصاحبه:**

تمایز Lead: توضیح cascade failure و رابطه با thread/resource exhaustion. Follow-up: «تفاوت sliding window count-based و time-based؟»

---

### سوال ۲: Retry را کِی باید و کِی نباید استفاده کرد؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

Retry فقط برای خطاهای **گذرا** (transient) مثل timeout شبکه‌ی موقت، 503 موقت، یا deadlock DB مناسب است — جایی که تلاش مجدد احتمال موفقیت دارد. نباید برای خطاهای **دائمی** (400، 401، 404، validation) استفاده شود چون فقط بار بی‌فایده اضافه می‌کند. نکته‌ی حیاتی: عملیات باید **idempotent** باشد؛ retry یک POST غیرidempotent می‌تواند دوبار پرداخت ثبت کند. همیشه با **exponential backoff + jitter** استفاده کنید تا retry storm (همه‌ی کلاینت‌ها هم‌زمان retry می‌کنند و سرویس را دوباره down می‌کنند) رخ ندهد.

**نکته مصاحبه:**

تمایز Senior: idempotency، backoff+jitter، و تفکیک خطای گذرا/دائمی. Follow-up: «retry storm چیست و jitter چطور حلش می‌کند؟»

---

### سوال ۳: Bulkhead pattern چیست؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

الهام از دیواره‌های ضدآب کشتی: اگر یک بخش سوراخ شود، فقط همان بخش پر می‌شود نه کل کشتی. در نرم‌افزار، منابع (thread pool یا semaphore) را بین فراخوانی‌های مختلف ایزوله می‌کند. مثلاً اگر سرویس A و B هر دو از یک thread pool مشترک استفاده کنند و A کند شود، threadها را اشغال می‌کند و B هم گرسنه می‌ماند. با Bulkhead، A و B pool جدا دارند، پس کندی A روی B اثر نمی‌گذارد. دو نوع: thread pool bulkhead (ایزولاسیون کامل با pool جدا) و semaphore bulkhead (محدود کردن تعداد فراخوانی هم‌زمان).

**نکته مصاحبه:**

Lead به resource isolation و جلوگیری از starvation اشاره می‌کند.

---

### سوال ۴: distributed tracing چطور یک request را در چند سرویس دنبال می‌کند؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

هنگام ورود اولین request، یک `TraceId` یکتا تولید می‌شود. هر واحد کار (فراخوانی سرویس) یک `SpanId` می‌گیرد که به span والد لینک است. این context در هر فراخوانی بین سرویس‌ها از طریق header استاندارد (W3C `traceparent`) propagate می‌شود — در HTTP header، Kafka header، و … . هر سرویس span خود را به backend (Zipkin/Jaeger) می‌فرستد. backend با TraceId همه‌ی span‌ها را به یک نمودار end-to-end کنار هم می‌گذارد که نشان می‌دهد request کجا وقت صرف کرده. Micrometer Tracing این را در Spring Boot 3+ خودکار می‌کند. sampling کنترل می‌کند چه درصدی trace شوند تا overhead کنترل شود.

**نکته مصاحبه:**

Senior به propagation context و sampling اشاره می‌کند. Follow-up: «چرا همه‌ی requestها را trace نمی‌کنیم؟» (overhead حافظه/شبکه/storage).

---

### سوال ۵: ترتیب annotationهای resilience4j چرا مهم است؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

چون هر کدام یک aspect جدا با ترتیب اجرای متفاوت‌اند و رفتار کلی به ترتیب wrap بستگی دارد. ترتیب رایج از بیرون به درون: `Retry → CircuitBreaker → RateLimiter → TimeLimiter → call`. منطق: TimeLimiter داخلی‌ترین است تا هر تلاش جداگانه timeout داشته باشد؛ CircuitBreaker باید قبل از Retry باشد یا بعد؟ در واقع Retry بیرونی‌تر است تا کل چرخه (شامل circuit breaker) دوباره تلاش شود — اما این یعنی retry می‌تواند circuit را زودتر باز کند. تنظیم دقیق بستگی به سناریو دارد و باید آگاهانه انتخاب شود، نه پیش‌فرض.

**نکته مصاحبه:**

Lead نشان می‌دهد که این یک تصمیم آگاهانه با trade-off است نه قانون ثابت.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: Retry بدون idempotency

```java
// ❌ retry یک پرداخت غیرidempotent → دوبار شارژ
@Retry(name = "payment")
public void charge(Card card, Money amount) { gateway.charge(card, amount); }
```

```java
// ✅ idempotency key
@Retry(name = "payment")
public void charge(String idempotencyKey, Card card, Money amount) {
    gateway.charge(idempotencyKey, card, amount);
}
```

**توضیح:** retry عملیات غیرidempotent داده را خراب می‌کند.

---

### اشتباه ۲: fallback که خطای دیگری می‌دهد

```java
// ❌ fallback خودش fail می‌شود
public Result fallback(Req r, Throwable t) {
    return anotherRemoteCall(r); // ممکن است این هم fail شود
}
```

```java
// ✅ degradation محلی و قطعی
public Result fallback(Req r, Throwable t) {
    return Result.cachedOrDefault();
}
```

**توضیح:** fallback باید قطعی و بدون وابستگی خارجی باشد.

---

### اشتباه ۳: sampling 100% در production

```yaml
# ❌ overhead و هزینه‌ی storage بالا
management.tracing.sampling.probability: 1.0
```

```yaml
# ✅
management.tracing.sampling.probability: 0.1
```

**توضیح:** trace همه‌ی requestها در production گران است.

---

### اشتباه ۴: استفاده از Eureka در K8s بدون نیاز

```text
❌ افزودن Eureka در حالی که K8s خودش discovery دارد → پیچیدگی اضافه
✅ استفاده از K8s Service + DNS
```

**توضیح:** K8s service discovery داخلی دارد؛ Eureka اضافی است.

---

## 🔗 ارتباط با سایر مفاهیم

- Resilience4j با **Architecture (SAGA، resilience patterns)** و **Spring Cloud Gateway** عمیق مرتبط است.
- distributed tracing با **Observability (OpenTelemetry، Jaeger)** و **Scoped Values** (انتقال context).
- API Gateway با **Security** (auth متمرکز) و **rate limiting (Redis)**.
- Service Discovery با **Kubernetes** (Service/DNS).
- Config Server با **12-Factor App** (config externalization).
