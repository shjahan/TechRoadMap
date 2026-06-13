# Architectural Patterns — Microservices، DDD، Event-Driven، CQRS، SAGA

> معماری در سطح Lead متمایزکننده است. این مفاهیم در هر مصاحبه‌ی ارشد عمیق پرسیده می‌شوند.

---

## 📖 مفاهیم

### Monolith vs Microservices

**توضیح:**

**Monolith** کل برنامه در یک deployable unit است: ساده برای شروع، توسعه و دیباگ، تراکنش‌های ساده، اما با رشد، scale و deploy مستقل سخت می‌شود و coupling زیاد. **Microservices** سرویس‌های مستقل کوچک: deploy و scale جداگانه، تیم‌های مستقل، fault isolation، اما پیچیدگی عملیاتی بالا (شبکه، distributed transaction، observability، consistency).

نکته‌ی مهم Lead: microservices پیش‌فرض نیست. اکثر پروژه‌ها باید با **monolith خوب‌ساختاریافته (modular monolith)** شروع کنند و فقط هنگام نیاز واقعی (scale، تیم بزرگ) به microservices مهاجرت کنند — معمولاً با **Strangler Fig Pattern** (جایگزینی تدریجی بخش‌ها).

**چرا مهم است:**

تصمیم اشتباه (microservices زودهنگام) هزینه‌ی عظیم پیچیدگی بدون مزیت می‌آورد. این یک تله‌ی رایج است.

**نکات کلیدی:**

- با modular monolith شروع کنید؛ microservices هزینه‌ی عملیاتی سنگین دارد.
- Strangler Fig برای مهاجرت تدریجی بدون big-bang rewrite.
- مرز سرویس‌ها را با bounded context (DDD) تعیین کنید نه دلخواه.

---

### Microservice Patterns

**توضیح:**

- **Decomposition:** تجزیه بر اساس business capability یا subdomain (DDD).
- **Database per Service:** هر سرویس DB خودش — برای استقلال و loose coupling. اما توزیع داده و consistency را سخت می‌کند (نیاز SAGA، Outbox).
- **API Gateway:** نقطه‌ی ورود واحد.
- **Service Mesh** (Istio/Linkerd): مدیریت ارتباط سرویس‌به‌سرویس (mTLS، traffic، observability) در لایه‌ی زیرساخت.
- **Sidecar:** قابلیت جانبی (مثل proxy) کنار سرویس.
- **BFF (Backend for Frontend):** API مخصوص هر نوع client.

**نکات کلیدی:**

- Database per Service استقلال می‌دهد اما distributed transaction را اجتناب‌ناپذیر می‌کند.
- Service Mesh cross-cutting شبکه را از کد به infra منتقل می‌کند.

---

### Domain-Driven Design (DDD)

**توضیح:**

DDD روشی برای مدل‌سازی نرم‌افزار حول دامنه‌ی کسب‌وکار است. مفاهیم کلیدی:

- **Ubiquitous Language:** زبان مشترک تیم و کد.
- **Bounded Context:** مرز یک مدل منسجم — اساس تعیین مرز microservice.
- **Aggregate:** خوشه‌ای از موجودیت‌ها که به‌عنوان یک واحد consistency تغییر می‌کنند؛ یک Aggregate Root نقطه‌ی ورود است.
- **Entity** (هویت‌دار، تغییرپذیر) در برابر **Value Object** (بدون هویت، immutable — مثل record).
- **Domain Event:** اتفاق مهم دامنه.
- **Repository:** انتزاع persistence برای aggregate.
- **Anti-Corruption Layer:** ترجمه بین bounded contextها برای جلوگیری از نشت مدل.

**چرا مهم است:**

DDD مرز درست microservice و مدل تمیز را می‌دهد. bounded context مهم‌ترین مفهوم برای تجزیه‌ی سیستم است.

**نکات کلیدی:**

- مرز microservice = bounded context، نه تجزیه‌ی فنی دلخواه.
- Aggregate مرز consistency تراکنشی است (یک aggregate در یک تراکنش).
- Value Object را با record مدل کنید.

---

### Event-Driven Architecture

**توضیح:**

سرویس‌ها از طریق رویداد (نه فراخوانی مستقیم) ارتباط می‌گیرند — loose coupling. سه سبک: **Event Notification** (فقط اطلاع، گیرنده باید جزئیات را بپرسد)، **Event-Carried State Transfer** (رویداد حاوی داده‌ی لازم، بدون callback)، **Event Sourcing** (state = دنباله‌ی رویدادها). دو مدل هماهنگی: **Choreography** (هر سرویس به رویداد واکنش می‌دهد، غیرمتمرکز) و **Orchestration** (یک هماهنگ‌کننده‌ی مرکزی).

الگوهای reliability: **Outbox Pattern** (نوشتن رویداد در همان تراکنش DB در یک جدول outbox، سپس انتشار — برای تضمین انتشار)، **Inbox Pattern** (idempotent consumer — جلوگیری از پردازش تکراری).

**چرا مهم است:**

برای decoupling و scalability در سیستم توزیع‌شده. Outbox مشکل dual-write (نوشتن همزمان در DB و broker) را حل می‌کند.

**نکات کلیدی:**

- Outbox برای تضمین اتمیک بودن «تغییر DB + انتشار رویداد».
- Inbox/idempotent consumer برای at-least-once delivery.
- choreography برای decoupling، orchestration برای کنترل/visibility.

---

### CQRS & Event Sourcing

**توضیح:**

**CQRS** (Command Query Responsibility Segregation): جداسازی مدل نوشتن (Command) از مدل خواندن (Query). امکان بهینه‌سازی جداگانه‌ی هر کدام و scale مستقل read. معمولاً با eventual consistency بین write و read model. **Event Sourcing**: به‌جای ذخیره‌ی state فعلی، دنباله‌ی رویدادها را ذخیره می‌کنید؛ state با replay رویدادها بازسازی می‌شود. مزیت: audit کامل، امکان بازسازی هر نقطه‌ی زمانی؛ هزینه: پیچیدگی، نیاز snapshot برای performance.

**نکات کلیدی:**

- CQRS و Event Sourcing مستقل‌اند؛ اجباری با هم نیستند.
- این‌ها پیچیدگی زیاد می‌آورند؛ فقط وقتی مزیت واقعی هست استفاده کنید.
- eventual consistency بین مدل‌ها را باید در UX در نظر گرفت.

---

### SAGA Pattern

**توضیح:**

برای تراکنش‌های توزیع‌شده (چند سرویس، هر کدام DB خودش) که 2PC در آن‌ها عملی نیست. SAGA دنباله‌ای از تراکنش‌های محلی است؛ اگر یکی شکست بخورد، **compensating transactions** تغییرات قبلی را خنثی می‌کنند. دو نوع: **Choreography-based** (هر سرویس رویداد منتشر و به رویداد دیگران واکنش می‌دهد — غیرمتمرکز، اما دنبال کردن flow سخت) و **Orchestration-based** (یک orchestrator مرکزی مراحل را هدایت می‌کند — visibility بهتر، اما single point).

**مقایسه با 2PC:** 2PC قفل توزیع‌شده و coordinator دارد که scale و availability را کاهش می‌دهد؛ SAGA بدون قفل، eventual consistency، اما باید compensation را دستی طراحی کنید.

**چرا مهم است:**

در microservices با Database per Service، SAGA راه استاندارد consistency است.

**نکات کلیدی:**

- SAGA به‌جای 2PC در microservices.
- compensating transaction باید idempotent و قابل‌اعتماد باشد.
- orchestration برای flow پیچیده visibility بهتری می‌دهد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: کِی monolith و کِی microservices؟

**سطح:** Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

monolith برای شروع تقریباً همیشه درست است: ساده‌تر، deploy سریع، تراکنش‌های راحت، و در ابتدا که domain هنوز روشن نیست انعطاف بیشتری برای refactor مرز می‌دهد. microservices وقتی توجیه می‌شود که: تیم بزرگ شده و نیاز به deploy مستقل دارد، بخش‌های مختلف نیاز scale متفاوت دارند، یا fault isolation بحرانی است. هزینه‌ی microservices واقعی است: شبکه، distributed transaction (SAGA)، observability توزیع‌شده، consistency، و پیچیدگی عملیاتی. ضدالگوی رایج «microservices زودهنگام» است که پیچیدگی توزیع‌شده را قبل از نیاز می‌آورد. توصیه: modular monolith با مرزهای تمیز (bounded context)، سپس مهاجرت تدریجی با Strangler Fig در صورت نیاز.

**نکته مصاحبه:**

تمایز Lead: microservices را پیش‌فرض نمی‌داند، modular monolith و Strangler Fig را می‌شناسد. Follow-up: «مرز microservice را چطور تعیین می‌کنی؟» (bounded context).

---

### سوال ۲: SAGA در برابر 2PC — چرا و چه trade-off؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

2PC (Two-Phase Commit) consistency قوی می‌دهد اما coordinator و قفل توزیع‌شده دارد که availability و scale را کاهش می‌دهد (اگر coordinator یا یک participant down شود، همه بلاک می‌شوند) و اکثر دیتابیس‌های مدرن/message brokerها آن را خوب پشتیبانی نمی‌کنند. SAGA دنباله‌ای از تراکنش‌های محلی است با compensation برای rollback منطقی؛ بدون قفل توزیع‌شده، availability و scale بهتر، اما فقط **eventual consistency** می‌دهد و باید compensationها را دستی طراحی کنید (که می‌تواند پیچیده باشد — مثلاً چطور یک ایمیل ارسال‌شده را compensate کنی؟). در microservices با Database per Service، SAGA انتخاب عملی است.

**نکته مصاحبه:**

Lead به مشکل availability در 2PC و چالش طراحی compensation در SAGA اشاره می‌کند. Follow-up: «اگر compensation هم شکست بخورد چه؟» (retry، dead letter، مداخله‌ی دستی).

---

### سوال ۳: Outbox Pattern چه مشکلی را حل می‌کند؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

مشکل **dual write**: وقتی می‌خواهید همزمان در DB بنویسید و یک رویداد به Kafka منتشر کنید، این دو عملیات اتمیک نیستند. اگر DB commit شود اما انتشار Kafka fail شود (یا برعکس)، سیستم ناسازگار می‌شود (مثلاً سفارش ثبت شده اما رویداد منتشر نشده). Outbox این را حل می‌کند: رویداد را در یک جدول `outbox` در **همان تراکنش DB** که داده‌ی اصلی را می‌نویسید درج می‌کنید — پس اتمیک است. سپس یک فرایند جدا (polling یا CDC با Debezium) رویدادهای outbox را می‌خواند و به broker منتشر می‌کند و علامت می‌زند. این at-least-once delivery می‌دهد، پس consumer باید idempotent باشد (Inbox).

**نکته مصاحبه:**

تمایز Senior: تشخیص مشکل dual-write و ربط Outbox به CDC/Debezium. Follow-up: «چرا نمی‌توان فقط بعد از commit منتشر کرد؟» (بین commit و publish ممکن است crash شود).

---

### سوال ۴: bounded context چیست و چرا برای microservices مهم است؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

bounded context مرز یک مدل منسجم است که در آن یک اصطلاح معنای واحد دارد. مثلاً «Customer» در context فروش با «Customer» در context پشتیبانی مدل و معنای متفاوت دارد. اهمیت برای microservices: مرز سرویس باید بر اساس bounded context تعیین شود نه تجزیه‌ی فنی یا entity-by-entity. اگر مرزها اشتباه باشند، سرویس‌ها coupling زیاد پیدا می‌کنند و هر تغییر چند سرویس را درگیر می‌کند (distributed monolith — بدترین حالت). تعیین درست bounded context (با event storming) مهم‌ترین قدم در طراحی microservices است.

**نکته مصاحبه:**

Lead به distributed monolith به‌عنوان نتیجه‌ی مرز اشتباه اشاره می‌کند.

---

### سوال ۵: CQRS کِی ارزش پیچیدگی‌اش را دارد؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

CQRS وقتی توجیه می‌شود که: الگوی read و write به‌شدت متفاوت‌اند (مثلاً write ساده اما read نیاز به join/aggregation پیچیده و scale بالا دارد)، نیاز به scale مستقل read و write، یا read model‌های متعدد (denormalized views) برای queryهای مختلف. هزینه: پیچیدگی، sync بین مدل‌ها، و eventual consistency که باید در UX مدیریت شود. برای CRUD ساده، CQRS over-engineering است. اغلب نسخه‌ی سبک (جداسازی query service از command service بدون event sourcing کامل) کافی است.

**نکته مصاحبه:**

Lead over-engineering را تشخیص می‌دهد و نسخه‌ی سبک را می‌شناسد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: microservices زودهنگام

```text
❌ شروع پروژه‌ی کوچک با ۱۵ microservice → پیچیدگی بدون مزیت
✅ modular monolith، تجزیه هنگام نیاز واقعی
```

**توضیح:** پیچیدگی توزیع‌شده را قبل از نیاز نیاورید.

---

### اشتباه ۲: dual write بدون Outbox

```java
// ❌ غیراتمیک: ممکن است یکی fail شود
orderRepository.save(order);
kafkaTemplate.send("orders", event); // اگر این fail شود ناسازگاری
```

```java
// ✅ Outbox: رویداد در همان تراکنش DB
@Transactional
void place(Order o) { orderRepository.save(o); outboxRepository.save(event); }
```

**توضیح:** نوشتن همزمان در DB و broker اتمیک نیست.

---

### اشتباه ۳: shared database بین microservices

```text
❌ چند سرویس به یک DB → coupling شدید، distributed monolith
✅ Database per Service + SAGA/Outbox برای consistency
```

**توضیح:** DB مشترک استقلال سرویس‌ها را نابود می‌کند.

---

### اشتباه ۴: SAGA بدون compensation قابل‌اعتماد

```text
❌ compensation که خودش ممکن است fail شود و نادیده گرفته شود
✅ compensation idempotent + retry + dead letter + alerting
```

**توضیح:** شکست compensation باید مدیریت شود وگرنه داده ناسازگار می‌ماند.

---

## 🔗 ارتباط با سایر مفاهیم

- microservices با **Spring Cloud (2.6)** و **Kubernetes (10.2)**.
- Event-Driven/Outbox با **Kafka (8.1)** و **CDC (Debezium)**.
- SAGA با **Spring resilience (15.2)** و **transactions**.
- DDD با **Clean/Hexagonal Architecture (15.1)** و **Event Storming (19.4)**.
- CQRS با **read replicas** و **caching**.
