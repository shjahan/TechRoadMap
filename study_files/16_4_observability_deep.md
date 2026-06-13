# Observability عمیق — OpenTelemetry، PromQL، SLO، ELK

> پیاده‌سازی عملی observability: OTel در Spring، PromQL، error budget، و structured logging.

---

## 📖 مفاهیم

### OpenTelemetry در Spring Boot

**توضیح:**

OpenTelemetry (OTel) استاندارد vendor-neutral برای metrics/logs/traces است. در Spring Boot 3+ با Micrometer Tracing خودکار trace می‌شود؛ context (traceId) بین سرویس‌ها propagate می‌شود (W3C `traceparent`). `@Observed` برای span سفارشی. sampling برای کنترل overhead.

**مثال کد:**

```yaml
management:
  tracing:
    sampling: { probability: 0.1 }   # 10% در production
  otlp:
    tracing: { endpoint: http://jaeger:4317 }
```

```java
@Observed(name = "user.find", contextualName = "findUser")
public User findUser(Long id) { /* ... */ }
```

**نکات کلیدی:**

- OTel استاندارد واحد → vendor lock-in کمتر.
- sampling در production پایین (overhead).

---

### PromQL & SLO

**توضیح:**

PromQL queryهای کلیدی: request rate، error rate، p99 latency، resource usage. **SLO/Error Budget/Burn Rate** برای alerting مبتنی بر تجربه‌ی کاربر.

**مثال کد:**

```promql
# error rate
rate(http_server_requests_seconds_count{status=~"5.."}[5m])
  / rate(http_server_requests_seconds_count[5m])

# p99 latency
histogram_quantile(0.99, rate(http_server_requests_seconds_bucket[5m]))

# burn rate (آیا error budget سریع مصرف می‌شود؟)
( rate(http_requests_total{status=~"5.."}[1h]) / rate(http_requests_total[1h]) )
  / (1 - 0.999)
```

**نکات کلیدی:**

- alert بر اساس SLO/burn rate نه CPU خام.
- p99 (نه میانگین) برای latency.

---

### ELK & Structured Logging

**توضیح:**

ELK (Elasticsearch + Logstash + Kibana). **Structured logging** (JSON) با key-value برای query آسان. trace id در هر log برای correlation. Logstash pipeline برای parse و enrich.

**مثال کد:**

```java
// با logstash-logback-encoder، JSON output
log.info("Order processed",
    kv("orderId", order.getId()),
    kv("userId", order.getUserId()),
    kv("amount", order.getAmount()));
```

**نکات کلیدی:**

- structured (JSON) به‌جای متن آزاد برای query.
- trace id در هر log برای correlation با trace.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا OpenTelemetry به‌جای ابزار خاص vendor؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

پیش از OTel، هر vendor (Datadog، New Relic) SDK و فرمت خودش را داشت؛ instrument کردن کد به یک vendor قفل می‌کرد و تغییر backend یعنی بازنویسی instrumentation. OpenTelemetry یک استاندارد واحد (API + SDK + protocol OTLP) برای metrics، logs، و traces است: کد را یک‌بار با OTel instrument می‌کنید و می‌توانید به هر backend (Jaeger، Prometheus، Datadog، …) export کنید — بدون vendor lock-in. همچنین auto-instrumentation برای فریم‌ورک‌های رایج. در Spring Boot 3+ با Micrometer/OTel یکپارچه است. مزیت استراتژیک: انعطاف در انتخاب/تغییر ابزار observability.

**نکته مصاحبه:**

Lead به vendor lock-in و OTLP اشاره می‌کند.

---

### سوال ۲: burn rate alert چیست؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

burn rate نرخ مصرف error budget است. اگر SLO «۹۹.۹٪» باشد، error budget ماهانه ۰.۱٪ است. burn rate = (نرخ خطای فعلی) / (نرخ مجاز). burn rate برابر ۱ یعنی دقیقاً با سرعتی مصرف می‌شود که budget در پایان دوره تمام شود؛ burn rate برابر ۱۰ یعنی ۱۰ برابر سریع‌تر (budget در یک‌دهم زمان تمام می‌شود). **burn rate alert** هشدار می‌دهد وقتی مصرف خیلی سریع است — مثلاً «اگر با این نرخ ادامه یابد، کل budget ماه در چند ساعت تمام می‌شود». مزیت بر alert ساده‌ی threshold: حساسیت متناسب با severity (multi-window multi-burn-rate: fast burn → page فوری، slow burn → ticket). این از alert fatigue جلوگیری و فقط مشکلات واقعی را escalate می‌کند.

**نکته مصاحبه:**

Lead به multi-window burn rate و کاهش alert fatigue اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: log غیرstructured

```java
// ❌ متن آزاد، query سخت
log.info("Order " + id + " processed for " + userId);
```

```java
// ✅ structured
log.info("Order processed", kv("orderId", id), kv("userId", userId));
```

**توضیح:** structured logging query و تحلیل را ممکن می‌کند.

---

### اشتباه ۲: alert بر منابع خام به‌جای SLO

```text
❌ alert روی CPU > 80% (شاید مشکلی نباشد)
✅ alert بر error rate/latency (تجربه‌ی کاربر) و burn rate
```

**توضیح:** alert روی symptom (تجربه‌ی کاربر) نه cause.

---

## 🔗 ارتباط با سایر مفاهیم

- observability با **Monitoring (10.4)** و **Spring Actuator (2.2)**.
- tracing با **Micrometer/Spring Cloud (2.6)** و **Scoped Values (1.6)**.
- SLO با **System Design availability (6.2)**.
