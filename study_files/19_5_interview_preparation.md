# Interview Preparation — Java، System Design، Spring، Leadership

> جمع‌بندی سوالات پرتکرار Senior/Lead و راهنمای پاسخ‌دهی.

---

## 📖 مفاهیم

### استراتژی پاسخ‌دهی

**توضیح:**

تمایز Senior/Lead از Junior در عمق و trade-off awareness است. اصول پاسخ خوب: (۱) با مفهوم اصلی شروع کنید، سپس جزئیات. (۲) trade-off را صریح بیان کنید (هیچ پاسخ «همیشه درست» وجود ندارد). (۳) با مثال عملی production پشتیبانی کنید. (۴) follow-up را پیش‌بینی کنید. (۵) برای system design، ساختار داشته باشید (requirements → estimation → design → deep dive → trade-off).

**نکات کلیدی:**

- trade-off awareness مهم‌ترین تمایز Senior است.
- مثال واقعی بهتر از تعریف کتابی.

---

### سوالات پرتکرار Java/Concurrency

**توضیح:**

- HashMap چطور کار می‌کند؟ تغییر Java 8 (LinkedList → Red-Black Tree)؟
- `volatile` در برابر `synchronized`؟
- Virtual Threads چه مشکلی حل می‌کنند؟ کجا مناسب‌اند؟
- `CompletableFuture` در برابر Reactive؟
- GC چطور کار می‌کند؟ memory leak را چطور پیدا می‌کنی؟
- `ConcurrentHashMap` چطور thread-safe است؟

**نکات کلیدی:**

- این‌ها در فایل‌های 1.1، 1.6، 12.1، 12.6 با جواب کامل پوشش داده شده‌اند.

---

### سوالات System Design، Spring، Leadership

**توضیح:**

**System Design:** Notification System، Rate Limiter، Distributed Cache، Payment System (exactly-once)، Leaderboard. **Spring:** `@Transactional` و self-invocation، bean lifecycle، `@SpringBootApplication`، CircuitBreaker، Security filter chain. **Leadership:** مدیریت technical debt، trade-off microservices، monolith در برابر microservice، حل اختلاف technical، mentoring junior.

**نکات کلیدی:**

- Leadership questions روی تصمیم‌گیری، ارتباط، و mentoring تمرکز دارند نه فقط فنی.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چطور technical debt را مدیریت می‌کنی؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

technical debt اجتناب‌ناپذیر است؛ مدیریت آن نه حذف کامل، بلکه کنترل آگاهانه است. رویکرد: (۱) **شفاف‌سازی** — debt را مستند و قابل‌مشاهده کنید (backlog، tracking)، نه پنهان. (۲) **اولویت‌بندی بر اساس تأثیر** — debt‌ای که سرعت توسعه را کند می‌کند یا ریسک تولید دارد را اول. (۳) **boy scout rule** — هر بار که کدی را لمس می‌کنید کمی بهترش کنید (refactor تدریجی به‌جای big rewrite پرریسک). (۴) **بودجه‌ی منظم** — مثلاً درصدی از هر sprint به کاهش debt. (۵) **ارتباط با business** — debt را به زبان ریسک/هزینه/سرعت برای ذی‌نفعان توضیح دهید نه اصطلاح فنی. (۶) جلوگیری از debt جدید با code review و استاندارد. کلید: تعادل بین تحویل feature و سلامت کد، با تصمیم آگاهانه نه نادیده گرفتن.

**نکته مصاحبه:**

Lead به boy scout rule، ارتباط با business، و تعادل اشاره می‌کند. Follow-up: «چطور debt را به مدیر غیرفنی توجیه می‌کنی؟»

---

### سوال ۲: چطور تصمیم می‌گیری monolith یا microservice؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

با monolith (به‌خصوص modular monolith) شروع می‌کنم مگر دلیل قوی برعکس باشد. عوامل تصمیم به microservice: (۱) **اندازه‌ی تیم** — چند تیم مستقل که نیاز به deploy جداگانه دارند. (۲) **نیاز scale متفاوت** بخش‌ها. (۳) **fault isolation** بحرانی. (۴) **بلوغ domain** — مرزها روشن شده‌اند (با DDD/Event Storming). در برابر هزینه‌ها: پیچیدگی عملیاتی (شبکه، distributed transaction، observability)، نیاز به بلوغ DevOps، و overhead. ضدالگو: microservices زودهنگام که پیچیدگی توزیع‌شده را قبل از نیاز می‌آورد. رویکرد: modular monolith با مرزهای تمیز، سپس مهاجرت تدریجی (Strangler Fig) بخش‌هایی که واقعاً نیاز دارند. تصمیم باید بر اساس داده (متریک، نقطه‌درد) باشد نه trend.

**نکته مصاحبه:**

Lead microservices را پیش‌فرض نمی‌داند و تصمیم را به عوامل عینی گره می‌زند.

---

### سوال ۳: وقتی با تیم درباره‌ی تصمیم technical اختلاف داری چه می‌کنی؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

رویکرد: (۱) **گوش دادن و فهم** دیدگاه طرف مقابل — شاید context‌ای دارند که من ندارم. (۲) **تمرکز بر داده و trade-off** نه نظر شخصی — معیارهای عینی (performance، نگهداری، ریسک، هزینه) را روی میز بگذارید. (۳) **disagree and commit** — اگر بعد از بحث تصمیم خلاف نظر من گرفته شد (به‌خصوص اگر برگشت‌پذیر است)، آن را بپذیرم و کامل حمایت کنم. (۴) برای تصمیمات پرریسک/برگشت‌ناپذیر، **prototype/spike** یا نظر سوم برای داده‌ی بیشتر. (۵) اولویت با سلامت تیم و محصول، نه برنده شدن بحث. (۶) مستند کردن تصمیم و دلیل (ADR) برای آینده. کلید: اختلاف فنی سالم است؛ مدیریت آن با احترام، داده، و تواضع تمایز یک lead خوب است.

**نکته مصاحبه:**

Lead به «disagree and commit»، تصمیم data-driven، و ADR اشاره می‌کند.

---

### سوال ۴: چطور junior را mentor می‌کنی؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

اصول: (۱) **تطبیق با سطح** — کار با چالش مناسب (نه خیلی سخت که سرخورده شود، نه خیلی ساده). (۲) **آموزش ماهیگیری نه دادن ماهی** — به‌جای دادن جواب، سوال هدایت‌کننده بپرسید تا خودش به راه‌حل برسد. (۳) **code review سازنده** — توضیح «چرا» نه فقط «چه»، با لحن محترمانه و تمرکز بر یادگیری نه انتقاد. (۴) **pair programming** برای انتقال دانش عملی. (۵) **فضای امن برای اشتباه** — اشتباه بخشی از یادگیری است؛ blameless culture. (۶) **مسیر رشد** — اهداف روشن و feedback منظم. (۷) الگو بودن (best practice، تست، مستندسازی). هدف: ساختن مهندس مستقل و بااعتمادبه‌نفس، نه وابسته. سرمایه‌گذاری روی junior به بهره‌وری کل تیم برمی‌گردد.

**نکته مصاحبه:**

Lead به «teach to fish»، blameless culture، و رشد بلندمدت اشاره می‌کند.

---

## ⚠️ اشتباهات رایج (در مصاحبه)

### اشتباه ۱: پاسخ بدون trade-off

```text
❌ "همیشه microservice/NoSQL/reactive بهتر است"
✅ "بستگی دارد به... ، trade-off این است..."
```

**توضیح:** پاسخ مطلق نشانه‌ی عدم بلوغ است.

---

### اشتباه ۲: system design بدون ساختار

```text
❌ پریدن به جزئیات بدون requirements/estimation
✅ requirements → estimation → high-level → deep dive → trade-off
```

**توضیح:** ساختار نشان‌دهنده‌ی تفکر منظم است.

---

### اشتباه ۳: نادیده گرفتن بُعد non-technical در Lead questions

```text
❌ پاسخ صرفاً فنی به سوال leadership
✅ ارتباط، تصمیم‌گیری، mentoring، business alignment
```

**توضیح:** Lead بودن فراتر از مهارت فنی است.

---

## 🔗 ارتباط با سایر مفاهیم

- این فایل جمع‌بندی همه‌ی فصل‌هاست؛ هر سوال به فایل مربوطه ارجاع دارد.
- Java questions → فایل‌های 1.x، 12.x.
- System Design → 6.x.
- Spring → 2.x.
- Leadership → تجربه‌ی عملی و این فایل.
