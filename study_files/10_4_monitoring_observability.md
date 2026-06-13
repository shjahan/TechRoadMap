# Monitoring & Observability — Metrics، Logs، Tracing

> سه ستون observability پایه‌ی عملیات production است. SLO و correlation در سطح Lead پرسیده می‌شوند.

---

## 📖 مفاهیم

### Three Pillars of Observability

**توضیح:**

سه ستون: **Metrics** (اعداد عددی در طول زمان — latency، error rate، throughput)، **Logs** (رویدادهای گسسته با جزئیات)، **Traces** (مسیر یک request در سیستم توزیع‌شده). تفاوت monitoring و observability: monitoring «آیا سیستم سالم است؟» (known-unknowns)، observability «چرا این رفتار خاص رخ داد؟» (unknown-unknowns).

**نکات کلیدی:**

- metrics برای alerting و trend، logs برای جزئیات، traces برای latency توزیع‌شده.
- correlation بین این سه (با trace id) قدرت واقعی observability است.

---

### Metrics (Prometheus + Grafana)

**توضیح:**

**Prometheus** pull-based است: endpoint `/actuator/prometheus` را scrape می‌کند. metric types: Counter (فقط افزایشی — تعداد request)، Gauge (بالا/پایین — استفاده‌ی حافظه)، Histogram (توزیع — برای percentile latency)، Summary. **PromQL** زبان query (مثل `rate(...)`, `histogram_quantile(...)`). **Grafana** برای dashboard و alert. **Micrometer** facade در Spring Boot است که به Prometheus/Datadog/… متصل می‌شود.

مهم‌ترین metricها: latency (p50/p95/p99 — نه فقط میانگین چون میانگین tail latency را پنهان می‌کند)، error rate، throughput، saturation (USE method: Utilization, Saturation, Errors).

**مثال کد:**

```promql
# error rate
rate(http_server_requests_seconds_count{status=~"5.."}[5m])
  / rate(http_server_requests_seconds_count[5m])

# p99 latency
histogram_quantile(0.99, rate(http_server_requests_seconds_bucket[5m]))
```

**نکات کلیدی:**

- percentile (p99) به‌جای میانگین برای latency.
- Histogram برای محاسبه‌ی percentile سمت سرور.
- Micrometer facade مستقل از backend.

---

### Logs (ELK Stack)

**توضیح:**

**Elasticsearch** (ذخیره/جستجو)، **Logstash** (ingestion/transform)، **Kibana** (visualization). **Filebeat/Fluent Bit** برای ارسال log. **Structured logging** (JSON) به‌جای متن خام برای parse و query آسان. **Correlation ID / Trace ID** در هر log برای دنبال کردن یک request در همه‌ی سرویس‌ها.

**نکات کلیدی:**

- structured logging (JSON) برای query؛ نه متن آزاد.
- trace id در همه‌ی logها برای correlation.
- سطح log مناسب (production: INFO؛ DEBUG فقط موقت).

---

### Tracing (Distributed)

**توضیح:**

**OpenTelemetry (OTel)** استاندارد واحد برای metrics/logs/traces. **Jaeger/Zipkin** backend tracing. **Micrometer Tracing** (Spring Boot 3+) خودکار TraceId/SpanId می‌دهد. **Sampling**: نه همه‌ی requestها trace می‌شوند (overhead). در production معمولاً ۱-۱۰٪.

**نکات کلیدی:**

- OpenTelemetry استاندارد vendor-neutral.
- sampling برای کنترل overhead.

---

## 🎯 سوالات مصاحبه

### سوال ۱: سه ستون observability را توضیح بده و کِی کدام؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

**Metrics** اعداد تجمعی در طول زمان‌اند (latency، error rate، CPU)؛ ارزان، برای alerting و dashboard و دیدن trend، اما جزئیات یک رویداد خاص را نمی‌دهند. **Logs** رویدادهای گسسته با جزئیات کامل‌اند؛ برای فهمیدن «دقیقاً چه شد» در یک مورد خاص، اما حجیم و گران برای جستجو در مقیاس. **Traces** مسیر یک request را در سرویس‌های مختلف نشان می‌دهند با زمان هر مرحله؛ برای یافتن گلوگاه latency در سیستم توزیع‌شده. جریان کار معمول: metric یک ناهنجاری را نشان می‌دهد (alert) → trace نشان می‌دهد کدام سرویس کند است → log جزئیات خطا را می‌دهد. correlation با trace id بین این سه کلید است.

**نکته مصاحبه:**

تمایز Lead: جریان کار «metric → trace → log» و correlation.

---

### سوال ۲: چرا p99 به‌جای میانگین latency؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

میانگین tail latency را پنهان می‌کند. مثلاً اگر ۹۹٪ requestها ۱۰ms و ۱٪ آن‌ها ۵ ثانیه باشند، میانگین ممکن ۶۰ms باشد که خوب به‌نظر می‌رسد، اما آن ۱٪ کاربر تجربه‌ی افتضاح دارند. p99 (صدک ۹۹) می‌گوید «بدترین تجربه‌ی ۹۹٪ کاربران چقدر است» — معیار واقعی‌تر برای SLO. در سیستم با fan-out (یک request به چند سرویس)، احتمال برخورد با tail latency بالا می‌رود (tail amplification)، پس p99/p99.9 حیاتی است. همیشه percentileها را گزارش کنید نه فقط میانگین. Histogram به محاسبه‌ی percentile سمت سرور امکان می‌دهد.

**نکته مصاحبه:**

Lead به tail amplification در fan-out اشاره می‌کند.

---

### سوال ۳: SLI/SLO/Error Budget چیست؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

**SLI** (Service Level Indicator) یک معیار قابل‌اندازه‌گیری از کیفیت سرویس است (مثل درصد requestهای موفق زیر ۲۰۰ms). **SLO** (Objective) هدف برای آن SLI (مثل «۹۹.۹٪ requestها زیر ۲۰۰ms»). **Error Budget** = ۱۰۰٪ − SLO؛ یعنی مقدار مجاز خطا (۹۹.۹٪ → ۰.۱٪ budget ≈ ۴۳ دقیقه downtime در ماه). فلسفه: تا وقتی error budget باقی است، تیم می‌تواند ریسک کند و feature deploy کند؛ وقتی budget تمام شد، تمرکز به reliability برمی‌گردد. **Burn rate alert** هشدار می‌دهد اگر budget سریع‌تر از حد مصرف شود. این چارچوب تنش بین سرعت توسعه و پایداری را عینی می‌کند.

**نکته مصاحبه:**

Lead به نقش error budget در تصمیم feature در برابر reliability اشاره می‌کند.

---

### سوال ۴: چطور alert fatigue را کاهش می‌دهی؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

alert fatigue وقتی است که alertهای زیاد/کم‌اهمیت باعث می‌شوند تیم آن‌ها را نادیده بگیرد و alert مهم گم شود. راه‌حل‌ها: (۱) alert بر اساس **symptom** (تجربه‌ی کاربر، مثل error rate یا latency) نه **cause** (مثل CPU بالا که شاید مشکلی نسازد). (۲) **SLO-based alerting** با burn rate (فقط وقتی error budget واقعاً تهدید می‌شود). (۳) تعریف severity و فقط page کردن برای موارد actionable و فوری. (۴) حذف alertهای flaky و noisy. (۵) گروه‌بندی و deduplication. هدف: هر alert باید actionable باشد و نیاز به اقدام انسانی فوری داشته باشد.

**نکته مصاحبه:**

Lead «alert on symptoms not causes» و SLO-based را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: alert بر اساس میانگین

```text
❌ alert روی avg latency → tail پنهان می‌ماند
✅ alert روی p99 و error rate
```

**توضیح:** میانگین مشکل tail را پنهان می‌کند.

---

### اشتباه ۲: log بدون correlation id

```text
❌ logهای پراکنده بدون امکان دنبال کردن یک request
✅ trace id در هر log (MDC)
```

**توضیح:** بدون correlation، دیباگ توزیع‌شده غیرممکن است.

---

### اشتباه ۳: sampling 100% trace در production

```text
❌ overhead و هزینه‌ی storage بالا
✅ sampling 1-10%
```

**توضیح:** trace همه‌ی requestها گران است.

---

### اشتباه ۴: DEBUG logging در production

```text
❌ حجم لاگ عظیم، هزینه، و نشت اطلاعات
✅ INFO در production، DEBUG موقت و هدفمند
```

**توضیح:** DEBUG دائمی حجم و هزینه را منفجر می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- metrics با **Spring Boot Actuator/Micrometer (2.2)** و **K8s HPA (10.2)**.
- tracing با **Spring Cloud / Micrometer Tracing (2.6)** و **OpenTelemetry (16.4)**.
- SLO با **System Design availability (6.2)**.
- correlation id با **distributed tracing (19.3)** و **Scoped Values (1.6)**.
