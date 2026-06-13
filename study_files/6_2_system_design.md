# System Design — Scalability، CAP، Caching، Rate Limiting، Case Studies

> طراحی سیستم در مصاحبه‌ی Lead متمایزکننده است. CAP، caching strategy و rate limiting موضوعات کلیدی هستند.

---

## 📖 مفاهیم

### اصول پایه — Scalability، Availability

**توضیح:**

- **Scalability:** Vertical (ماشین قوی‌تر — ساده اما سقف دارد) در برابر Horizontal (ماشین‌های بیشتر — مقیاس‌پذیر اما نیاز stateless و توزیع). معماری مدرن horizontal را ترجیح می‌دهد.
- **Availability:** درصد uptime. 99.9% ≈ ۸.۷ ساعت downtime در سال، 99.99% ≈ ۵۲ دقیقه. هر «۹» اضافه هزینه‌ی غیرخطی دارد.
- ساختن سیستم stateless برای horizontal scaling کلیدی است (state در DB/cache/session store خارجی).

**نکات کلیدی:**

- horizontal scaling به stateless بودن نیاز دارد.
- هدف availability را واقع‌بینانه انتخاب کنید؛ هر ۹ گران است.

---

### CAP Theorem & Consistency Models

**توضیح:**

در سیستم توزیع‌شده، هنگام **Partition** (قطع شبکه بین نودها) باید بین **Consistency** (همه آخرین داده را می‌بینند) و **Availability** (سیستم پاسخ می‌دهد) یکی را انتخاب کنید — نمی‌توان هر دو را در زمان partition داشت. (P اجباری است چون partition در شبکه‌ی واقعی اجتناب‌ناپذیر است.) سیستم‌های **CP** (مثل برخی پیکربندی‌های etcd، MongoDB با majority) consistency را حفظ و در partition پاسخ نمی‌دهند؛ **AP** (مثل Cassandra، DynamoDB) همیشه پاسخ می‌دهند اما ممکن داده‌ی stale.

**Consistency models:** Strong (همیشه آخرین)، Eventual (در نهایت همگرا)، Causal (ترتیب علّی حفظ). **BASE** (Basically Available, Soft state, Eventual consistency) در برابر **ACID**.

**چرا مهم است:**

انتخاب CP/AP تصمیم معماری بنیادی است. درک eventual consistency برای طراحی صحیح (مثل read-your-writes) لازم است.

**نکات کلیدی:**

- در شرایط عادی (بدون partition) می‌توان هم C و هم A داشت؛ CAP فقط هنگام partition trade-off است.
- اکثر سیستم‌ها در عمل ترکیبی و قابل‌تنظیم‌اند (مثل write concern در MongoDB).

---

### Load Balancing

**توضیح:**

توزیع ترافیک بین چند instance. الگوریتم‌ها: Round Robin، Weighted، IP Hash (sticky)، Least Connections. **L4** (transport، بر اساس IP/port — سریع) در برابر **L7** (application، بر اساس محتوای HTTP مثل path/header — انعطاف‌پذیر). Health check برای حذف instance خراب.

**نکات کلیدی:**

- L7 امکان routing هوشمند (path-based، canary) می‌دهد.
- sticky session مقیاس‌پذیری را محدود می‌کند؛ session را خارجی کنید.

---

### Caching Strategy

**توضیح:**

استراتژی‌ها:

- **Cache-Aside (Lazy Loading):** اپ ابتدا cache را چک می‌کند؛ miss → از DB می‌خواند و در cache می‌گذارد. رایج‌ترین. عیب: اولین request کند، و احتمال stale.
- **Write-Through:** هر write همزمان cache و DB را به‌روز می‌کند. consistency بهتر، write کندتر.
- **Write-Behind:** write در cache، سپس async به DB. سریع اما خطر data loss.
- **Refresh-Ahead:** پیش‌بینی و refresh قبل از expiry.

**Cache Invalidation** یکی از سخت‌ترین مسائل است. **Cache Stampede** (وقتی یک کلید پرطرفدار expire می‌شود و هزاران request همزمان به DB می‌روند) با probabilistic early expiration یا lock حل می‌شود.

**نکات کلیدی:**

- Cache-Aside پیش‌فرض رایج؛ مراقب stale و stampede.
- invalidation سخت است؛ TTL + event-based invalidation.

---

### Rate Limiting

**توضیح:**

محدود کردن نرخ request برای جلوگیری از سوءاستفاده و overload. الگوریتم‌ها:

- **Token Bucket:** سطل با نرخ ثابت پر می‌شود؛ هر request یک token مصرف می‌کند. burst را مجاز می‌کند.
- **Leaky Bucket:** پردازش با نرخ ثابت؛ smoothing.
- **Fixed Window:** شمارش در پنجره‌ی ثابت زمانی؛ ساده اما مشکل لبه (burst در مرز).
- **Sliding Window:** دقیق‌تر، با پنجره‌ی لغزان.

پیاده‌سازی توزیع‌شده معمولاً با Redis (atomic counter یا sorted set).

**مثال کد:**

```java
// rate limit با Redis (Token bucket ساده)
// از Redisson یا Bucket4j استفاده کنید
Bucket bucket = Bucket.builder()
    .addLimit(Bandwidth.classic(100, Refill.greedy(100, Duration.ofMinutes(1))))
    .build();
if (bucket.tryConsume(1)) { /* پردازش */ } else { /* 429 Too Many Requests */ }
```

**نکات کلیدی:**

- Token Bucket برای اجازه‌ی burst؛ Sliding Window برای دقت.
- در سیستم توزیع‌شده، counter باید مشترک (Redis) باشد.

---

### Case Studies

**توضیح:**

سوالات کلاسیک system design interview: URL Shortener (hashing، DB، cache، redirect)، Notification System (queue، fan-out، چند channel)، Chat System (WebSocket، delivery، presence)، Payment System (idempotency، exactly-once، consistency)، Search Autocomplete (Trie، ranking)، News Feed (fan-out on write/read)، Ride-Sharing (geospatial، matching).

روش پاسخ: requirements (functional + non-functional) → estimation (QPS، storage) → API design → data model → high-level design → deep dive روی bottleneck → trade-offs.

**نکات کلیدی:**

- همیشه با clarifying requirements و estimation شروع کنید.
- trade-off را صریح بیان کنید؛ پاسخ «درست» واحد وجود ندارد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: CAP theorem را توضیح بده و یک تصمیم واقعی بر اساس آن.

**سطح:** Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

CAP می‌گوید در حضور **partition شبکه** نمی‌توان همزمان Consistency و Availability کامل داشت. چون partition در شبکه‌ی توزیع‌شده اجتناب‌ناپذیر است، عملاً بین CP و AP انتخاب می‌کنید. سوءفهم رایج: «همیشه باید یکی از سه را قربانی کرد» — درست‌تر این است که فقط **هنگام partition** trade-off وجود دارد؛ در شرایط عادی هم C و هم A ممکن است.

تصمیم واقعی: برای یک سیستم بانکی/پرداخت، consistency بحرانی است — CP را انتخاب می‌کنید (بهتر است سیستم در partition پاسخ ندهد تا اینکه موجودی اشتباه نشان دهد). برای یک feed شبکه‌ی اجتماعی یا shopping cart، availability مهم‌تر است — AP، چون نمایش داده‌ی کمی stale بهتر از در دسترس نبودن است. در عمل سیستم‌ها قابل‌تنظیم‌اند (مثل tunable consistency در Cassandra یا write concern در MongoDB).

**نکته مصاحبه:**

Lead سوءفهم «همیشه trade-off» را تصحیح و تصمیم را به دامنه‌ی کسب‌وکار گره می‌زند. Follow-up: «PACELC چیست؟» (توسعه‌ی CAP که latency در حالت عادی را هم لحاظ می‌کند).

---

### سوال ۲: cache stampede چیست و چطور حل می‌شود؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

cache stampede (thundering herd) وقتی رخ می‌دهد که یک کلید پرطرفدار expire شود و همزمان هزاران request به آن miss بخورند و همگی به DB هجوم ببرند — DB غرق می‌شود. راه‌حل‌ها: (۱) **lock/mutex**: فقط یک request اجازه‌ی محاسبه‌ی مجدد دارد، بقیه منتظر یا مقدار قدیمی می‌گیرند. (۲) **probabilistic early expiration**: قبل از expiry واقعی، با احتمالی فزاینده یکی refresh می‌کند تا همه همزمان expire نشوند. (۳) **stale-while-revalidate**: مقدار قدیمی را برگردان و در پس‌زمینه refresh کن. (۴) cache warming برای کلیدهای حیاتی. ترکیب lock + TTL با jitter رایج است.

**نکته مصاحبه:**

تمایز Lead: چند راه‌حل و درک ریشه. Follow-up: «چطور با Redis یک distributed lock برای این می‌سازی؟» (`SET NX PX`).

---

### سوال ۳: Token Bucket در برابر Sliding Window برای rate limiting؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Token Bucket یک سطل با ظرفیت ثابت دارد که با نرخ معین token اضافه می‌شود؛ هر request یک token مصرف می‌کند. مزیت: **burst** را تا ظرفیت سطل مجاز می‌کند (مناسب وقتی trafic ناهموار طبیعی است). Fixed Window ساده است اما مشکل لبه دارد: ۲ برابر limit ممکن است در مرز دو پنجره عبور کند. Sliding Window این را با در نظر گرفتن پنجره‌ی لغزان (یا log زمان requestها در sorted set) حل می‌کند — دقیق‌تر اما حافظه/محاسبه‌ی بیشتر. انتخاب: Token Bucket برای اجازه‌ی burst و سادگی، Sliding Window برای دقت سخت‌گیرانه.

**نکته مصاحبه:**

Senior مشکل لبه‌ی fixed window را می‌داند.

---

### سوال ۴: یک URL Shortener طراحی کن.

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

requirements: کوتاه کردن URL، redirect، (اختیاری) آمار و custom alias. estimation: read >> write (مثلاً ۱۰۰:۱)، پس read-optimized. تولید short code: encode یک شناسه‌ی یکتای incremental با base62 (کوتاه و یکتا) یا hash + collision handling. data model: جدول `(short_code PK, long_url, created_at)`. high-level: write به DB، read با cache (Redis) جلوی DB چون redirect پرترافیک است. scale: DB را با short_code shard کنید، CDN/cache برای redirect. trade-off: base62 incremental قابل‌حدس است (امنیت)، hash نیاز collision handling دارد. redirect با 301 (cache مرورگر) یا 302 (برای آمار).

**نکته مصاحبه:**

Lead با estimation و read/write ratio شروع می‌کند و trade-off encode را می‌فهمد. Follow-up: «301 یا 302؟» (302 اگر آمار می‌خواهی).

---

### سوال ۵: چطور exactly-once در یک Payment System تضمین می‌کنی؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

exactly-once واقعی در سیستم توزیع‌شده عملاً غیرممکن است؛ به‌جای آن **at-least-once + idempotency** پیاده می‌کنیم که اثر exactly-once می‌دهد. مکانیزم: client یک **idempotency key** یکتا با هر request پرداخت می‌فرستد. سرور قبل از پردازش، key را در یک store (Redis یا DB با unique constraint) چک می‌کند؛ اگر قبلاً پردازش شده، نتیجه‌ی ذخیره‌شده را برمی‌گرداند بدون پردازش مجدد. ترکیب با Outbox برای انتشار رویداد اتمیک، و SAGA برای هماهنگی چندسرویسی. همچنین unique constraint روی DB به‌عنوان آخرین خط دفاع.

**نکته مصاحبه:**

Lead «exactly-once = at-least-once + idempotency» را می‌داند. Follow-up: «idempotency key را کجا و چقدر نگه می‌داری؟»

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: stateful سرویس و horizontal scaling

```text
❌ نگه‌داری session در حافظه‌ی هر instance → load balancing می‌شکند
✅ session در Redis/DB، سرویس stateless
```

**توضیح:** state محلی horizontal scaling را غیرممکن می‌کند.

---

### اشتباه ۲: cache بدون TTL/invalidation

```text
❌ داده‌ی stale برای همیشه در cache
✅ TTL + invalidation رویداد-محور
```

**توضیح:** بدون invalidation، داده‌ی قدیمی سرو می‌شود.

---

### اشتباه ۳: rate limiter محلی در سیستم توزیع‌شده

```text
❌ counter در حافظه‌ی هر instance → limit واقعی = limit × تعداد instance
✅ counter مشترک در Redis
```

**توضیح:** limit باید سراسری باشد نه per-instance.

---

### اشتباه ۴: پاسخ system design بدون estimation

```text
❌ پریدن مستقیم به جزئیات بدون QPS/storage
✅ requirements → estimation → design → deep dive
```

**توضیح:** estimation مقیاس و bottleneck را مشخص می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- CAP با **MongoDB write concern (4.4)** و **PostgreSQL replication**.
- caching strategy با **Redis (9.1)** و **Spring Cache**.
- rate limiting با **Redis** و **API Gateway (2.6)**.
- idempotency با **Idempotency (19.2)** و **Kafka delivery**.
- horizontal scaling با **Kubernetes HPA (10.2)** و **stateless 12-factor**.
