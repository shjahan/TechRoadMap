# Serialization — Java Serialization، Jackson، Protobuf، Avro

> serialization در API، messaging و persistence همه‌جا هست. Java serialization خطرناک است؛ مدرن‌ها امن‌ترند.

---

## 📖 مفاهیم

### Java Serialization

**توضیح:**

مکانیزم داخلی با `implements Serializable`. `serialVersionUID` برای version control (اگر تغییر کند، deserialize شکست می‌خورد). `transient` فیلدهای حساس/غیرضروری را از serialization حذف می‌کند. `readObject`/`writeObject` برای custom. **مشکلات جدی:** آسیب‌پذیری امنیتی (deserialization of untrusted data → RCE، یکی از خطرناک‌ترین کلاس‌های آسیب‌پذیری)، performance ضعیف، coupling شدید به ساختار کلاس. در production معمولاً از آن اجتناب می‌شود.

**نکات کلیدی:**

- Java serialization برای داده‌ی untrusted خطرناک است (RCE).
- در سیستم‌های مدرن از JSON/Protobuf استفاده کنید.
- `transient` برای حذف فیلد حساس.

---

### Jackson (JSON)

**توضیح:**

کتابخانه‌ی استاندارد JSON در Spring Boot. `ObjectMapper` هسته است. annotationها: `@JsonProperty` (نام فیلد)، `@JsonIgnore` (حذف)، `@JsonFormat` (فرمت تاریخ)، `@JsonInclude` (حذف null). custom serializer/deserializer برای منطق خاص. Jackson 3 در Boot 4 module-based است.

**مثال کد:**

```java
public record UserDto(
    @JsonProperty("user_name") String name,
    @JsonIgnore String password,
    @JsonFormat(pattern = "yyyy-MM-dd") LocalDate birthDate) {}

// config
ObjectMapper mapper = new ObjectMapper()
    .registerModule(new JavaTimeModule())  // برای java.time
    .setSerializationInclusion(JsonInclude.Include.NON_NULL);
```

**نکات کلیدی:**

- `@JsonIgnore` برای فیلد حساس (مثل password).
- `JavaTimeModule` برای java.time (وگرنه خطا).
- `FAIL_ON_UNKNOWN_PROPERTIES` را برای backward compatibility مدیریت کنید.

---

### Protocol Buffers & Avro

**توضیح:**

**Protobuf** (Google): باینری، فشرده، با schema (`.proto`)، code generation، سریع. برای gRPC و ارتباط بین‌سرویسی پرکارایی. **Avro:** schema-based، برای Kafka رایج (با Schema Registry). هر دو **schema evolution** را پشتیبانی می‌کنند (افزودن/حذف فیلد با حفظ سازگاری backward/forward).

**نکات کلیدی:**

- Protobuf/Avro فشرده‌تر و سریع‌تر از JSON برای ارتباط داخلی.
- schema evolution امکان تغییر بدون شکستن مصرف‌کننده.
- JSON برای API عمومی (خوانا)؛ Protobuf/Avro برای داخلی (کارایی).

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا Java native serialization خطرناک است؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

مشکل اصلی **deserialization of untrusted data**: وقتی داده‌ی serialize‌شده‌ی Java را از منبع نامطمئن deserialize می‌کنید، Java می‌تواند هر کلاسی در classpath را instantiate و متدهایش (readObject) را اجرا کند. مهاجم می‌تواند یک «gadget chain» بسازد که هنگام deserialize، کد دلخواه اجرا کند (Remote Code Execution) — یکی از خطرناک‌ترین آسیب‌پذیری‌ها (مثل حملات معروف به Apache Commons Collections). مشکلات دیگر: performance ضعیف، coupling شدید (هر تغییر کلاس می‌تواند سازگاری را بشکند)، و فرمت verbose. به همین دلیل توصیه می‌شود به‌جای آن از فرمت‌های داده‌محور (JSON، Protobuf) استفاده کنید که کد اجرا نمی‌کنند.

**نکته مصاحبه:**

Lead به gadget chain و RCE اشاره می‌کند.

---

### سوال ۲: JSON در برابر Protobuf — کِی کدام؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

JSON متنی، خوانا، schema-less (انعطاف)، و universal است — برای API عمومی/REST که خوانایی و سازگاری با هر client مهم است. Protobuf باینری، فشرده (کوچک‌تر و سریع‌تر برای parse)، strongly-typed با schema و code generation است — برای ارتباط داخلی بین‌سرویسی پرترافیک (gRPC) که performance و قرارداد سخت‌گیرانه مهم است. trade-off: JSON خوانا اما حجیم‌تر و کندتر؛ Protobuf کارآمد اما نیاز به schema و ابزار، و غیرخوانا برای debug. هر دو schema evolution دارند (JSON با احتیاط، Protobuf با قواعد field number). انتخاب: API عمومی → JSON؛ microservice داخلی پرترافیک → Protobuf/gRPC.

**نکته مصاحبه:**

Senior trade-off خوانایی/کارایی و موارد استفاده را می‌داند.

---

### سوال ۳: schema evolution چیست و چرا مهم است؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

schema evolution توانایی تغییر schema داده (افزودن/حذف فیلد) بدون شکستن producerها و consumerهایی است که نسخه‌ی متفاوت دارند — حیاتی در سیستم توزیع‌شده که نمی‌توان همه را همزمان deploy کرد. **backward compatibility**: consumer جدید بتواند داده‌ی قدیمی را بخواند. **forward compatibility**: consumer قدیمی بتواند داده‌ی جدید را بخواند (فیلد ناشناخته را نادیده بگیرد). Protobuf با field number و optional بودن این را به‌خوبی پشتیبانی می‌کند (فیلد جدید را با number جدید اضافه کنید، فیلد حذف‌شده را reuse نکنید). Avro با Schema Registry سازگاری را enforce می‌کند. در Kafka، schema evolution برای deploy تدریجی ضروری است.

**نکته مصاحبه:**

Senior backward/forward compatibility و نقش Schema Registry را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: deserialize داده‌ی untrusted با Java serialization

```java
// ❌ RCE risk
ObjectInputStream in = new ObjectInputStream(untrustedSource);
Object obj = in.readObject();
```

```java
// ✅ JSON/Protobuf که کد اجرا نمی‌کند
```

**توضیح:** Java deserialization می‌تواند کد دلخواه اجرا کند.

---

### اشتباه ۲: serialize کردن password

```java
// ❌ password در JSON خروجی
public record User(String name, String password) {}
```

```java
// ✅
public record User(String name, @JsonIgnore String password) {}
```

**توضیح:** فیلد حساس باید از serialization حذف شود.

---

### اشتباه ۳: reuse کردن field number در Protobuf

```text
❌ حذف فیلد و استفاده‌ی مجدد از number آن → ناسازگاری داده‌ی قدیمی
✅ field number را reserve کنید، reuse نکنید
```

**توضیح:** field number قدیمی با داده‌ی قدیمی تداخل می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- Java serialization با **Security (7.1)** (deserialization vulnerability).
- Jackson با **Spring MVC (2.3)** و **API design**.
- Protobuf با **gRPC (15.4)**؛ Avro با **Kafka (8.1)**.
- schema evolution با **microservices deploy (6.1)**.
