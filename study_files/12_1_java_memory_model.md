# Java Memory Model (JMM) — Visibility، Ordering، False Sharing

> JMM پایه‌ی هر استدلال درست درباره‌ی concurrency است. سوالات سطح Lead اینجا متمرکزند.

---

## 📖 مفاهیم

### Visibility & Ordering — happens-before

**توضیح:**

JMM تعریف می‌کند که تغییرات یک thread کِی برای threadهای دیگر **دیده** می‌شوند و با چه **ترتیبی**. بدون قانون، هر thread می‌تواند کپی محلی (cache CPU، register) داشته باشد و تغییرات دیگران را نبیند. رابطه‌ی محوری **happens-before** است: اگر A happens-before B، آن‌گاه اثرات A برای B تضمیناً دیده می‌شوند.

منابع happens-before:
- آزادسازی `synchronized` (unlock) → گرفتن بعدی (lock).
- نوشتن `volatile` → خواندن بعدی همان متغیر.
- `Thread.start()` → اولین عمل thread.
- `Thread.join()` → بازگشت join (آخرین عمل thread دیده می‌شود).
- عملیات روی `Atomic` و `Lock`.

**چرا مهم است:**

باگ‌های visibility (مثل thread که flag تغییریافته را نمی‌بیند و حلقه‌ی بی‌نهایت می‌زند) متناوب و سخت‌یاب‌اند. JMM ابزار استدلال درست است.

**مثال کد:**

```java
class Worker {
    private volatile boolean running = true; // volatile → visibility تضمین

    void stop() { running = false; }          // نوشتن
    void run() {
        while (running) { /* کار */ }          // خواندن → توقف دیده می‌شود
        // بدون volatile ممکن است این حلقه هرگز تمام نشود!
    }
}
```

**نکات کلیدی:**

- happens-before پایه‌ی هر تضمین visibility است.
- بدون synchronization مناسب، تغییرات ممکن دیده نشوند (نه فقط با تأخیر، بلکه هرگز).
- reordering توسط CPU/compiler مجاز است مگر happens-before آن را محدود کند.

---

### volatile — visibility نه atomicity

**توضیح:**

`volatile` تضمین می‌کند هر خواندن آخرین مقدار نوشته‌شده را می‌بیند و از reordering مضر جلوگیری می‌کند. اما عملیات مرکب (read-modify-write مثل `i++`) را atomic نمی‌کند. مناسب: flag boolean، single-writer، double-checked locking (روی reference). نامناسب: counter (`i++`)، invariant چندمتغیره.

**مثال کد:**

```java
// ✅ مناسب: flag
private volatile boolean shutdownRequested;

// ❌ نامناسب: counter — race condition
private volatile int count; // count++ atomic نیست → از AtomicInteger استفاده کنید
```

**نکات کلیدی:**

- volatile = visibility + ordering، نه mutual exclusion.
- برای read-modify-write از Atomic یا lock.

---

### False Sharing

**توضیح:**

cache line معمولاً ۶۴ بایت است. اگر دو thread روی **متغیرهای مختلف** اما در **یک cache line** کار کنند، هر نوشتن یکی، cache line را در core دیگر invalidate می‌کند — رقابت کاذب (false sharing) که performance را به‌شدت کاهش می‌دهد، حتی بدون اشتراک منطقی. راه‌حل: padding یا `@Contended` (Java 8+، نیاز به `-XX:-RestrictContended`).

**مثال کد:**

```java
@jdk.internal.vm.annotation.Contended // padding خودکار → cache line جدا
static class Counter {
    volatile long value;
}
```

**نکات کلیدی:**

- false sharing یک مشکل performance پنهان در concurrency با throughput بالاست.
- `@Contended` متغیر را در cache line جدا قرار می‌دهد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: happens-before چیست و چرا مهم است؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

happens-before یک رابطه‌ی ترتیبی است که JMM تعریف می‌کند: اگر عمل A با B در رابطه‌ی happens-before باشد، تمام اثرات حافظه‌ی A (نوشتن‌ها) برای B تضماً قابل‌مشاهده‌اند و A قبل از B دیده می‌شود. این مهم است چون بدون آن، compiler و CPU آزادند عملیات را reorder و در cache محلی نگه دارند، پس یک thread ممکن تغییرات thread دیگر را اصلاً نبیند یا با ترتیب اشتباه ببیند. منابع happens-before (synchronized، volatile، Thread.start/join، Atomic) ابزارهایی هستند که با آن‌ها visibility و ordering را تضمین می‌کنیم. هر استدلال درست درباره‌ی thread-safety باید بر اساس یک زنجیره‌ی happens-before باشد، نه شهود.

**نکته مصاحبه:**

تمایز Lead: استدلال بر اساس happens-before نه شهود. Follow-up: «بدون volatile چرا حلقه‌ی `while(flag)` ممکن تمام نشود؟» (JIT می‌تواند flag را در register نگه دارد).

---

### سوال ۲: double-checked locking چرا به volatile نیاز دارد؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

در DCL، شیء با `instance = new Singleton()` ساخته می‌شود که در bytecode سه مرحله است: تخصیص حافظه، فراخوانی سازنده، و انتساب reference. بدون `volatile`، compiler/CPU می‌تواند این‌ها را reorder کند طوری که reference **قبل از** اتمام سازنده منتشر شود. آن‌گاه thread دیگری که `instance != null` را می‌بیند، ممکن یک شیء **نیمه‌ساخته** (با فیلدهای مقداردهی‌نشده) بگیرد. `volatile` این reordering را ممنوع و happens-before بین نوشتن و خواندن reference را تضمین می‌کند، پس هر thread که reference غیرnull می‌بیند، شیء کاملاً ساخته‌شده را می‌بیند.

**نکته مصاحبه:**

Lead reordering در ساخت شیء و شیء نیمه‌ساخته را توضیح می‌دهد.

---

### سوال ۳: false sharing چیست؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

CPU حافظه را در واحدهای cache line (معمولاً ۶۴ بایت) cache می‌کند. اگر دو thread روی دو متغیر مستقل که اتفاقاً در یک cache line قرار گرفته‌اند بنویسند، هر نوشتن باعث invalidate شدن کل cache line در core دیگر می‌شود (cache coherence protocol)، پس آن core باید دوباره از حافظه بخواند — حتی اینکه منطقاً هیچ داده‌ی مشترکی ندارند. این «false sharing» throughput را در سیستم‌های concurrency بالا به‌شدت کاهش می‌دهد. راه‌حل: padding متغیرها تا در cache lineهای جدا باشند، یا `@Contended`. این یک مشکل performance ظریف است که در ساختارهای داده‌ی high-performance (مثل LongAdder که عمداً counterها را جدا می‌کند) مطرح است.

**نکته مصاحبه:**

Lead به LongAdder به‌عنوان مثال طراحی برای جلوگیری از false sharing اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: flag بدون volatile

```java
// ❌ ممکن حلقه هرگز تمام نشود
private boolean running = true;
```

```java
// ✅
private volatile boolean running = true;
```

**توضیح:** بدون volatile، تغییر flag ممکن برای thread دیگر دیده نشود.

---

### اشتباه ۲: volatile برای counter

```java
// ❌ count++ atomic نیست
private volatile int count;
```

```java
// ✅
private final AtomicInteger count = new AtomicInteger();
```

**توضیح:** volatile visibility می‌دهد نه atomicity برای read-modify-write.

---

### اشتباه ۳: DCL بدون volatile

```java
// ❌ شیء نیمه‌ساخته دیده می‌شود
private static Config instance;
```

```java
// ✅
private static volatile Config instance;
```

**توضیح:** reordering ساخت شیء بدون volatile مشکل‌ساز است.

---

## 🔗 ارتباط با سایر مفاهیم

- JMM با **Concurrency (1.6)** و **volatile/synchronized**.
- happens-before با **ConcurrentHashMap** و **Atomic classes**.
- false sharing با **performance tuning (20)** و **LongAdder**.
- DCL با **Singleton (Design Patterns 5.3)**.
