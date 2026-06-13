# Event Storming

> روش کشف domain با تیم — پل بین business و طراحی نرم‌افزار (DDD).

---

## 📖 مفاهیم

### روش Event Storming

**توضیح:**

Event Storming یک workshop تعاملی برای کشف و مدل‌سازی domain با مشارکت همه‌ی ذی‌نفعان (developer، domain expert، PM) است. با sticky note رنگی روی دیوار:

1. **Domain Events** (نارنجی) — چه اتفاقاتی در domain می‌افتد؟ (به‌صورت past tense: «OrderPlaced»).
2. **Commands** (آبی) — چه چیزی باعث event می‌شود؟ («PlaceOrder»).
3. **Aggregates** (زرد) — چه چیزی command را handle می‌کند و consistency را حفظ می‌کند؟
4. **Bounded Contexts** — مرزها کجا هستند؟
5. **Read Models** (سبز) — چه View هایی نیاز است؟
6. **External Systems** (صورتی) — ورودی/خروجی خارجی.

**چرا مهم است:**

پل بین زبان business و طراحی نرم‌افزار. به کشف bounded context (مرز microservice) و ubiquitous language کمک می‌کند. ارزان و سریع برای رسیدن به فهم مشترک.

**نکات کلیدی:**

- event را past tense بنویسید (اتفاق افتاده).
- خروجی اصلی: کشف bounded context و ubiquitous language.
- مشارکت domain expert حیاتی است (نه فقط developer).

---

## 🎯 سوالات مصاحبه

### سوال ۱: Event Storming چطور به طراحی microservice کمک می‌کند؟

**سطح:** Lead
**تکرار:** کم

**جواب کامل:**

Event Storming با کشف **domain events** و **commands** به‌صورت مشترک با domain expert، به طور طبیعی **bounded contextها** را آشکار می‌کند — جایی که مجموعه‌ای از eventها و aggregateها به هم مرتبط‌اند و یک زبان منسجم دارند. این bounded contextها کاندیدای مرز microservice هستند (نه تجزیه‌ی فنی دلخواه که منجر به distributed monolith می‌شود). همچنین **ubiquitous language** (زبان مشترک تیم و کد) را می‌سازد و وابستگی‌ها/جریان رویدادها بین contextها را نمایان می‌کند که برای طراحی event-driven و API بین سرویس‌ها لازم است. مزیت: فهم مشترک business و technical قبل از کد زدن، که از طراحی اشتباه پرهزینه جلوگیری می‌کند.

**نکته مصاحبه:**

Lead به کشف bounded context و جلوگیری از distributed monolith اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: Event Storming فقط با developerها

```text
❌ بدون domain expert → کشف domain ناقص
✅ مشارکت همه‌ی ذی‌نفعان
```

**توضیح:** ارزش اصلی از دانش domain expert می‌آید.

---

### اشتباه ۲: event به‌صورت command (present tense)

```text
❌ "Place Order" (command)
✅ "Order Placed" (event، past tense)
```

**توضیح:** event اتفاق افتاده را توصیف می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- Event Storming با **DDD/bounded context (6.1)**.
- domain events با **Event-Driven Architecture (6.1)** و **Kafka (8.1)**.
- aggregate با **DDD و transactions**.
