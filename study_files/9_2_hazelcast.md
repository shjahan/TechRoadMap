# Hazelcast — In-Memory Data Grid

> Hazelcast یک distributed in-memory data grid است که برای محاسبات توزیع‌شده و clustering استفاده می‌شود.

---

## 📖 مفاهیم

### مفاهیم پایه

**توضیح:**

Hazelcast یک in-memory data grid (IMDG) توزیع‌شده است: داده را در حافظه‌ی چند نود partition و replicate می‌کند. برخلاف Redis که عمدتاً یک سرور (یا cluster) جداگانه است، Hazelcast می‌تواند **embedded** (در همان JVM اپ) یا **client-server** اجرا شود. ساختارهای داده‌ی توزیع‌شده: `IMap` (map توزیع‌شده)، `IQueue`, `ITopic` (pub/sub)، و موارد دیگر که interface استاندارد Java Collections را پیاده می‌کنند اما توزیع‌شده‌اند.

**Near Cache** یک کپی محلی از داده‌ی پرکاربرد در هر نود برای دسترسی سریع‌تر. **Entry Processors** محاسبه را سمت سرور (روی نودی که داده آن‌جاست) انجام می‌دهند تا از انتقال داده جلوگیری شود.

**چرا مهم است:**

برای distributed computation، session clustering، distributed locking، و cache توزیع‌شده با data locality. مزیت embedded mode: بدون hop شبکه‌ی جداگانه.

**مثال کد:**

```java
HazelcastInstance hz = Hazelcast.newHazelcastInstance();
IMap<String, User> users = hz.getMap("users"); // map توزیع‌شده
users.put("123", user); // روی نودها partition می‌شود

// distributed lock
hz.getCPSubsystem().getLock("order-lock").lock();

// Entry Processor: محاسبه سمت سرور (بدون انتقال داده)
users.executeOnKey("123", entry -> {
    User u = entry.getValue();
    u.incrementLoginCount();
    entry.setValue(u);
    return null;
});
```

**نکات کلیدی:**

- embedded mode بدون hop شبکه‌ی جدا (داده در همان JVM cluster).
- Entry Processor محاسبه را به داده می‌برد نه برعکس (data locality).
- Near Cache برای read پرتکرار.

---

## 🎯 سوالات مصاحبه

### سوال ۱: Hazelcast در برابر Redis — کِی کدام؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

Redis یک in-memory store جداگانه (معمولاً client-server) با data structureهای غنی، single-threaded، و اکوسیستم بالغ است؛ زبان‌مستقل و برای cache، session، pub/sub، و rate limiting عالی. Hazelcast یک data grid مبتنی بر JVM است که می‌تواند **embedded** اجرا شود (داده در همان JVM اپ partition می‌شود — بدون hop شبکه‌ی جدا) و امکانات distributed computing (Entry Processor، distributed executor) و یکپارچگی عمیق با Java (collections توزیع‌شده) دارد. انتخاب: برای اکوسیستم چندزبانه، سادگی، و cache عمومی → Redis؛ برای اپ Java که نیاز به distributed computation، data locality، یا embedded grid دارد → Hazelcast. Redis رایج‌تر و عملیاتی‌تر است.

**نکته مصاحبه:**

Lead به embedded mode و distributed computing به‌عنوان تمایز Hazelcast اشاره می‌کند.

---

### سوال ۲: Entry Processor چه مزیتی دارد؟

**سطح:** Senior
**تکرار:** کم

**جواب کامل:**

Entry Processor محاسبه را روی نودی که داده آن‌جا ذخیره شده اجرا می‌کند، به‌جای اینکه داده را به client بیاورد، تغییر دهد، و برگرداند. مزایا: (۱) **data locality** — بدون انتقال داده روی شبکه. (۲) **atomicity** — عملیات روی یک entry به‌صورت atomic و با lock داخلی انجام می‌شود (بدون race condition read-modify-write). (۳) کارایی بهتر برای bulk update. این الگوی «بردن محاسبه به داده» (مشابه فلسفه‌ی map-reduce) است که در داده‌ی توزیع‌شده‌ی بزرگ مهم است.

**نکته مصاحبه:**

Senior به «بردن محاسبه به داده» و atomicity اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: read-modify-write روی IMap بدون Entry Processor

```java
// ❌ race condition + انتقال داده
User u = map.get(key); u.increment(); map.put(key, u);
```

```java
// ✅ Entry Processor (atomic، سمت سرور)
map.executeOnKey(key, entry -> { /* modify */ });
```

**توضیح:** get/put جداگانه race condition دارد و داده را جابه‌جا می‌کند.

---

### اشتباه ۲: نادیده گرفتن serialization

```text
❌ object‌های بزرگ بدون serialization بهینه → overhead شبکه
✅ استفاده از serialization کارآمد (IdentifiedDataSerializable)
```

**توضیح:** در grid توزیع‌شده، serialization روی performance اثر زیاد دارد.

---

## 🔗 ارتباط با سایر مفاهیم

- Hazelcast در برابر **Redis (9.1)** برای caching/lock.
- distributed lock با **concurrency** و **System Design**.
- session clustering با **horizontal scaling (6.2)**.
- distributed computing با **map-reduce** و داده‌ی بزرگ.
