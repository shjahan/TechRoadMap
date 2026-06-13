# Idempotency

> idempotency برای سیستم‌های قابل‌اعتماد (پرداخت، retry) حیاتی است. درک پیاده‌سازی با idempotency key لازم است.

---

## 📖 مفاهیم

### مفهوم & پیاده‌سازی

**توضیح:**

idempotent یعنی درخواست تکراری همان نتیجه را بدهد بدون side-effect اضافه. در HTTP، GET، PUT، DELETE طبیعتاً idempotent‌اند اما POST نه (دوبار POST = دو منبع). برای امن کردن POST (مثل پرداخت) از **Idempotency Key** استفاده می‌شود: client یک key یکتا با request می‌فرستد؛ سرور قبل از پردازش، key را در store (Redis/DB) چک می‌کند — اگر قبلاً پردازش شده، نتیجه‌ی ذخیره‌شده را برمی‌گرداند بدون پردازش مجدد.

**چرا مهم است:**

در شبکه‌ی واقعی، retry (به‌خاطر timeout) و duplicate delivery (Kafka at-least-once) اجتناب‌ناپذیر است. بدون idempotency، retry یک پرداخت = دوبار شارژ.

**مثال کد:**

```java
@PostMapping("/payments")
public ResponseEntity<Payment> pay(
    @RequestHeader("Idempotency-Key") String key,
    @RequestBody PaymentRequest request) {

    String cached = redis.get("idem:" + key);
    if (cached != null) return ResponseEntity.ok(parse(cached)); // نتیجه‌ی قبلی

    Payment payment = paymentService.process(request);
    redis.setex("idem:" + key, 86400, serialize(payment)); // ذخیره با TTL
    return ResponseEntity.ok(payment);
}
```

**نکات کلیدی:**

- idempotency key برای POSTهای حساس.
- نتیجه را cache کنید تا retry همان پاسخ را بگیرد.
- unique constraint در DB به‌عنوان آخرین خط دفاع.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چطور یک endpoint پرداخت را idempotent می‌کنی؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

client با هر درخواست پرداخت یک **Idempotency Key** یکتا (UUID) می‌فرستد (که در صورت retry همان key را reuse می‌کند). سرور: (۱) قبل از پردازش، key را در یک store (Redis یا DB) چک می‌کند. (۲) اگر key وجود دارد و پردازش کامل شده، نتیجه‌ی ذخیره‌شده را برمی‌گرداند بدون پردازش مجدد. (۳) اگر key جدید است، آن را با حالت «in-progress» ثبت می‌کند (برای جلوگیری از پردازش همزمان دو request با همان key — race)، پردازش می‌کند، نتیجه را ذخیره می‌کند، و برمی‌گرداند. نکات: TTL مناسب برای key، مدیریت race با lock یا unique constraint، و idempotency در سطح DB (unique constraint روی transaction id) به‌عنوان دفاع نهایی. این «exactly-once effect» را با at-least-once delivery می‌دهد.

**نکته مصاحبه:**

Lead به race condition (دو request همزمان با یک key) و دفاع DB اشاره می‌کند.

---

### سوال ۲: چرا exactly-once با at-least-once + idempotency معادل است؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

exactly-once delivery واقعی در سیستم توزیع‌شده عملاً غیرممکن است (به‌خاطر امکان crash بین پردازش و ack). به‌جای آن، سیستم‌ها at-least-once delivery می‌دهند (پیام حداقل یک‌بار، شاید بیشتر) و idempotency در سمت گیرنده را اضافه می‌کنند: پردازش تکراری همان پیام، side-effect اضافه ندارد. ترکیب این دو، اثر exactly-once می‌دهد: پیام حتماً پردازش می‌شود (at-least-once) و حتی اگر چندبار برسد، فقط یک‌بار اثر می‌گذارد (idempotency). این الگوی استاندارد در Kafka، payment، و event-driven است. کلید: idempotency با dedup key، unique constraint، یا upsert.

**نکته مصاحبه:**

Lead فرمول «at-least-once + idempotency = exactly-once effect» را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: POST بدون idempotency در retry

```text
❌ retry پرداخت → دوبار شارژ
✅ idempotency key
```

**توضیح:** POST طبیعتاً idempotent نیست.

---

### اشتباه ۲: نادیده گرفتن race بین requestهای همزمان

```text
❌ دو request همزمان با یک key → هر دو پردازش (هنوز نتیجه ذخیره نشده)
✅ ثبت in-progress با lock/unique constraint
```

**توضیح:** بدون lock، race بین چک و ذخیره رخ می‌دهد.

---

## 🔗 ارتباط با سایر مفاهیم

- idempotency با **Kafka delivery (8.1)** و **retry (2.6)**.
- با **Redis (9.1)** برای key store و **distributed lock**.
- با **Payment System (System Design 6.2)** و **SAGA (6.1)**.
