# API Design عمیق — REST Maturity، OpenAPI، Versioning، Problem Details

> طراحی API خوب پایه‌ی سیستم قابل‌نگهداری است. versioning و error standardization موضوعات کلیدی‌اند.

---

## 📖 مفاهیم

### Richardson Maturity Model & OpenAPI

**توضیح:**

**Richardson Maturity Model** سطح بلوغ REST: Level 0 (یک endpoint، همه POST)، Level 1 (resources جدا)، Level 2 (HTTP verbs و status صحیح — هدف عملی)، Level 3 (HATEOAS با links). **OpenAPI/Swagger** برای مستندسازی و قرارداد API: Contract-First (spec اول، code generation) یا Code-First (Springdoc با `@Operation`).

**نکات کلیدی:**

- اکثر APIها Level 2 هستند؛ HATEOAS (Level 3) به‌ندرت ارزش هزینه دارد.
- Contract-First برای هماهنگی تیم‌ها (frontend/backend موازی).

---

### API Versioning & Problem Details

**توضیح:**

**Versioning:** URL (`/v1/`)، Header، یا Content-Type. **Problem Details (RFC 7807):** فرمت استاندارد خطا با `type`, `title`, `status`, `detail`, `instance`. Spring 6+ از `ProblemDetail` پشتیبانی می‌کند.

**مثال کد:**

```java
@ExceptionHandler(ValidationException.class)
ProblemDetail handle(ValidationException ex) {
    ProblemDetail pd = ProblemDetail.forStatusAndDetail(
        HttpStatus.BAD_REQUEST, ex.getMessage());
    pd.setType(URI.create("https://api.example.com/errors/validation"));
    pd.setProperty("violations", ex.getViolations());
    return pd;
}
```

**نکات کلیدی:**

- Problem Details فرمت قابل‌پیش‌بینی خطا برای مصرف‌کننده.
- versioning را از ابتدا پلن کنید با سیاست deprecation.

---

## 🎯 سوالات مصاحبه

### سوال ۱: API versioning strategies و کدام بهتر؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

سه روش: **URL** (`/api/v1/users`) — ساده، قابل‌مشاهده، cache-friendly، رایج‌ترین، اما RESTful pure نیست (URL باید resource را شناسایی کند نه نسخه). **Header** (`X-API-Version`) — URL تمیز، اما کمتر شفاف و تست دستی سخت‌تر. **Content-Type** (`application/vnd.company.v1+json`) — content negotiation اصیل اما پیچیده. در عمل URL versioning عملی‌ترین است. اما مهم‌تر از مکانیزم: **سیاست backward compatibility و deprecation** — تغییرات additive (افزودن فیلد) معمولاً breaking نیستند و نیاز به نسخه‌ی جدید ندارند؛ فقط تغییرات breaking (حذف/تغییر فیلد) نسخه می‌خواهند. باید دوره‌ی deprecation و مهاجرت مصرف‌کنندگان را مدیریت کنید. Spring Framework 7 versioning داخلی دارد.

**نکته مصاحبه:**

Lead به additive vs breaking change و deprecation policy اشاره می‌کند.

---

### سوال ۲: یک API خوب چه ویژگی‌هایی دارد؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

ویژگی‌ها: (۱) **consistency** — نام‌گذاری، ساختار، و convention یکسان در همه‌ی endpointها. (۲) **HTTP semantics صحیح** — verb درست (GET idempotent/safe، POST برای ساخت)، status code معنادار (201، 404، 409، 422). (۳) **error standardization** (Problem Details). (۴) **pagination، filtering، sorting** برای collectionها. (۵) **versioning** برای تکامل. (۶) **idempotency** برای عملیات حساس (با idempotency key). (۷) **مستندسازی** (OpenAPI). (۸) **امنیت** (auth، rate limiting، validation). (۹) **predictability** — رفتار قابل‌حدس. هدف: API که توسعه‌دهنده بدون خواندن مفصل مستندات بتواند حدس بزند چطور کار می‌کند.

**نکته مصاحبه:**

Senior consistency و HTTP semantics را برجسته می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: status code اشتباه

```text
❌ همه‌چیز 200 حتی خطا
✅ 201 ساخت، 400 ورودی بد، 404 نبود، 409 conflict، 500 خطای سرور
```

**توضیح:** status code صحیح برای client و ابزارها مهم است.

---

### اشتباه ۲: breaking change بدون versioning

```text
❌ حذف فیلد در v فعلی → شکستن مصرف‌کنندگان
✅ نسخه‌ی جدید + deprecation دوره‌ای
```

**توضیح:** تغییر breaking باید با version و دوره‌ی مهاجرت باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- API design با **Spring MVC (2.3)** و **REST best practices**.
- Problem Details با **exception handling (2.3)**.
- versioning با **API Gateway (2.6)** و **microservices**.
- idempotency با **Idempotency (19.2)**.
