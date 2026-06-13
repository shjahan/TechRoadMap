# Java 12–17 (LTS) — Records, Sealed, Pattern Matching

> Java 17 baseline جدید است: Spring Boot 3/4 حداقل به آن نیاز دارند. Records و Sealed Classes زبان را به‌سمت data-oriented programming بردند.

---

## 📖 مفاهیم

### Switch Expressions (Java 12–14)

**توضیح:**

`switch` کلاسیک یک statement بود با `break` فراموش‌شدنی و fall-through خطرناک. Switch Expression آن را به یک عبارت (expression) که مقدار برمی‌گرداند تبدیل می‌کند. با سینتکس arrow (`->`) دیگر fall-through و break وجود ندارد، و برای منطق چندخطی از `yield` استفاده می‌شود. همچنین کامپایلر **exhaustiveness** را برای enum چک می‌کند.

**چرا مهم است:**

کد امن‌تر (بدون باگ fall-through)، خواناتر، و قابل‌اطمینان‌تر (پوشش کامل حالت‌ها). به‌خصوص با sealed types قدرتمند می‌شود.

**مثال کد:**

```java
enum Day { MON, TUE, SAT, SUN }

static String type(Day day) {
    return switch (day) {
        case SAT, SUN -> "تعطیل";
        case MON, TUE -> "کاری";
        // اگر یک حالت enum جا بیفتد و default نباشد → خطای کامپایل
        default -> "نامشخص";
    };
}

static int score(String grade) {
    return switch (grade) {
        case "A" -> 4;
        case "B" -> 3;
        default -> {
            int base = 0;
            yield base; // منطق چندخطی با yield
        }
    };
}
```

**نکات کلیدی:**

- arrow syntax بدون fall-through و break است.
- برای enum بدون default، کامپایلر پوشش کامل را اجبار می‌کند.
- از `yield` برای بلوک چندخطی استفاده کنید.

---

### Records (Java 14 preview → 16/17 final)

**توضیح:**

`record` یک حامل داده‌ی immutable مختصر است. کامپایلر به‌طور خودکار سازنده‌ی canonical، getterها (به نام فیلد، بدون `get`)، `equals`, `hashCode`, و `toString` را تولید می‌کند. recordها به‌طور ضمنی `final` و فیلدهایشان `private final` هستند.

می‌توان **compact constructor** برای validation نوشت، متدهای اضافه تعریف کرد، و static factory ساخت. اما record نمی‌تواند state تغییرپذیر یا فیلد اضافی غیر از componentها داشته باشد.

**چرا مهم است:**

DTO، value object، event، و کلاس‌های داده‌ای را با کمترین boilerplate و درست (immutable + equals/hashCode صحیح) می‌سازد. در DDD برای Value Object ایده‌آل است.

**مثال کد:**

```java
public record Money(long amountCents, String currency) {
    // compact constructor برای validation
    public Money {
        if (amountCents < 0) throw new IllegalArgumentException("منفی نامجاز");
        Objects.requireNonNull(currency);
    }
    // متد اضافه
    public Money plus(Money other) {
        if (!currency.equals(other.currency))
            throw new IllegalArgumentException("واحد متفاوت");
        return new Money(amountCents + other.amountCents, currency);
    }
    // static factory
    public static Money usd(long cents) { return new Money(cents, "USD"); }
}

// استفاده
Money price = Money.usd(1000);
System.out.println(price.amountCents()); // getter بدون get
System.out.println(price); // toString خودکار: Money[amountCents=1000, currency=USD]
```

**نکات کلیدی:**

- record به‌طور ضمنی final و immutable است.
- از compact constructor برای validation و normalization استفاده کنید.
- برای موجودیت‌های JPA که mutable و proxy-محورند مناسب نیست (DTO بله، Entity معمولاً نه).

---

### Pattern Matching for instanceof (Java 16)

**توضیح:**

پیش از این، الگوی `instanceof` + cast دستی پرتکرار بود. حالا `if (obj instanceof String s)` هم چک می‌کند و هم متغیر `s` را با نوع درست در scope می‌آورد (binding variable). این متغیر فقط در شاخه‌ای که شرط برقرار است در دسترس است (flow scoping).

**مثال کد:**

```java
// قبل
if (obj instanceof String) {
    String s = (String) obj; // cast تکراری
    return s.length();
}

// بعد
if (obj instanceof String s && !s.isBlank()) {
    return s.length(); // s در دسترس و type-safe
}
```

**نکات کلیدی:**

- متغیر binding فقط در scope معتبر در دسترس است.
- با `&&` می‌توان شرط ترکیبی روی متغیر binding گذاشت.

---

### Text Blocks (Java 15)

**توضیح:**

رشته‌ی چندخطی با `"""` که escape و الحاق دستی را حذف می‌کند. برای JSON، SQL، HTML عالی است. indentation با «incidental whitespace stripping» مدیریت می‌شود.

**مثال کد:**

```java
String json = """
    {
      "name": "Ali",
      "active": true
    }
    """;

String sql = """
    SELECT id, name FROM users
    WHERE status = 'ACTIVE'
    ORDER BY created_at DESC
    """;
```

**نکات کلیدی:**

- indentation نسبت به کمترین خط محاسبه می‌شود.
- `\` در انتهای خط از newline جلوگیری می‌کند؛ `\s` فضای محافظت‌شده.

---

### Sealed Classes (Java 17)

**توضیح:**

`sealed` کنترل می‌کند چه کلاس‌هایی می‌توانند یک کلاس/interface را extend یا implement کنند، با `permits`. هر زیرنوع باید یکی از این‌ها باشد: `final` (بسته)، `sealed` (محدودیت ادامه)، یا `non-sealed` (باز کردن مجدد). این یک سلسله‌مراتب بسته و شناخته‌شده می‌سازد.

**چرا مهم است:**

با switch pattern matching ترکیب می‌شود و **exhaustiveness check** کامل می‌دهد: کامپایلر مطمئن می‌شود همه‌ی زیرنوع‌ها پوشش داده شده‌اند. این الگوی «algebraic data types» و data-oriented programming را در Java ممکن می‌کند.

**مثال کد:**

```java
public sealed interface Shape permits Circle, Rectangle, Triangle {}

public record Circle(double radius) implements Shape {}
public record Rectangle(double w, double h) implements Shape {}
public record Triangle(double base, double height) implements Shape {}

static double area(Shape shape) {
    return switch (shape) { // بدون default، کامپایلر پوشش کامل را چک می‌کند
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.w() * r.h();
        case Triangle t -> 0.5 * t.base() * t.height();
    };
}
```

**نکات کلیدی:**

- ترکیب sealed + record + switch = data-oriented programming قدرتمند.
- exhaustiveness check نیاز به default را حذف می‌کند و افزودن نوع جدید را به‌صورت compile-time error نشان می‌دهد.
- زیرنوع‌ها باید final/sealed/non-sealed باشند.

---

## 🎯 سوالات مصاحبه

### سوال ۱: Record چیست و کِی به‌جای کلاس معمولی استفاده می‌شود؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

record یک حامل داده‌ی immutable است که سازنده، accessorها، `equals`, `hashCode`, و `toString` را خودکار تولید می‌کند. زمانی استفاده می‌شود که هدف اصلی کلاس **نگهداری داده** است: DTO، value object، event، نتیجه‌ی query، یا کلید composite. می‌توان با compact constructor validation اضافه کرد.

کِی مناسب نیست: وقتی به state تغییرپذیر، وراثت، یا کنترل دقیق بر representation نیاز دارید. به‌خصوص برای JPA Entity معمولاً مناسب نیست چون Hibernate به سازنده‌ی بدون آرگومان، فیلدهای mutable و proxy نیاز دارد.

**کد توضیحی:**

```java
public record UserDto(Long id, String name, String email) {
    public UserDto {
        Objects.requireNonNull(email);
    }
}
```

**نکته مصاحبه:**

تمایز Senior: دانستن محدودیت‌ها (immutability، عدم وراثت، نامناسب برای Entity). Follow-up: «آیا record می‌تواند فیلد اضافی داشته باشد؟» (پاسخ: فقط static؛ instance field فقط componentها).

---

### سوال ۲: Sealed Classes چه مشکلی را حل می‌کنند؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

sealed سلسله‌مراتب وراثت را بسته و کنترل‌شده می‌کند. مهم‌ترین مزیت ترکیب با pattern matching switch است: کامپایلر می‌تواند **exhaustiveness** را تضمین کند، یعنی اگر یک زیرنوع جدید اضافه کنید و در switchها پوشش ندهید، خطای کامپایل می‌گیرید. این الگوی «modeling with the type system» را ممکن می‌کند که در آن حالت‌های نامعتبر اصلاً قابل بیان نیستند.

بدون sealed، یک hierarchy باز است و همیشه باید default بگذارید و امکان پوشش ناقص وجود دارد.

**نکته مصاحبه:**

Lead به data-oriented programming و algebraic data types اشاره می‌کند. Follow-up: «تفاوت `final`, `sealed`, `non-sealed` در زیرنوع چیست؟»

---

### سوال ۳: تفاوت switch statement و switch expression چیست؟

**سطح:** Mid / Senior
**تکرار:** زیاد

**جواب کامل:**

switch statement فقط کنترل جریان است و مقدار برنمی‌گرداند؛ با `:` و `break` کار می‌کند و در معرض باگ fall-through است. switch expression مقدار برمی‌گرداند، با arrow (`->`) بدون fall-through است، برای منطق چندخطی `yield` دارد، و برای enum/sealed پوشش کامل را اجبار می‌کند. expression خواناتر و امن‌تر است.

**نکته مصاحبه:**

Follow-up: «چرا fall-through در statement خطرناک است؟» (فراموشی break = اجرای ناخواسته‌ی caseهای بعدی).

---

### سوال ۴: pattern matching for instanceof چه boilerplate‌ای را حذف می‌کند؟

**سطح:** Mid
**تکرار:** متوسط

**جواب کامل:**

الگوی قدیمی نیاز به سه قدم داشت: چک با `instanceof`، سپس cast دستی، سپس استفاده. pattern matching هر سه را در یک عبارت ادغام می‌کند و متغیر binding با نوع صحیح و flow scoping ایجاد می‌کند. این هم کد را کوتاه می‌کند و هم خطای cast را حذف می‌کند.

**نکته مصاحبه:**

Follow-up: «flow scoping یعنی چه؟» (متغیر فقط جایی در دسترس است که کامپایلر مطمئن است شرط برقرار بوده).

---

### سوال ۵: چرا record برای JPA Entity مناسب نیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Hibernate به سازنده‌ی بدون آرگومان (no-arg) برای instantiate کردن proxy نیاز دارد؛ record فقط سازنده‌ی canonical دارد. همچنین Hibernate برای lazy loading و dirty checking به فیلدهای mutable و proxy (subclass) نیاز دارد؛ record final و immutable است. به‌علاوه `@Id` و چرخه‌ی حیات entity با immutability سازگار نیست. record برای DTO/projection در همان لایه عالی است اما Entity باید کلاس معمولی باشد.

**نکته مصاحبه:**

Senior به proxy، no-arg constructor و dirty checking اشاره می‌کند. Follow-up: «از record کجا در Spring Data استفاده می‌کنی؟» (projection و DTO).

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: تلاش برای تغییر record

```java
// ❌ record immutable است
record Point(int x, int y) {}
Point p = new Point(1, 2);
// p.x = 5; // کامپایل نمی‌شود، setter ندارد
```

```java
// ✅ شیء جدید بسازید (with-style)
Point moved = new Point(5, p.y());
```

**توضیح:** record immutable است؛ برای «تغییر» یک نمونه‌ی جدید بسازید.

---

### اشتباه ۲: استفاده از record به‌عنوان JPA Entity

```java
// ❌ Hibernate نمی‌تواند proxy/no-arg بسازد
@Entity
record User(@Id Long id, String name) {}
```

```java
// ✅ Entity کلاس معمولی، DTO به‌صورت record
@Entity
class User { @Id Long id; String name; /* ... */ }
record UserDto(Long id, String name) {}
```

**توضیح:** Entity به no-arg constructor و mutability نیاز دارد.

---

### اشتباه ۳: گذاشتن default غیرضروری در sealed switch

```java
// ❌ default مانع exhaustiveness check می‌شود
String s = switch (shape) {
    case Circle c -> "c";
    default -> "other"; // افزودن نوع جدید خطا نمی‌دهد!
};
```

```java
// ✅ بدون default → کامپایلر افزودن نوع جدید را به خطا تبدیل می‌کند
String s = switch (shape) {
    case Circle c -> "c";
    case Rectangle r -> "r";
    case Triangle t -> "t";
};
```

**توضیح:** با sealed types، default را حذف کنید تا از پوشش کامل بهره ببرید.

---

### اشتباه ۴: فراموشی validation در record

```java
// ❌ مقدار نامعتبر مجاز است
record Age(int value) {}
new Age(-5); // مشکلی نمی‌گیرد
```

```java
// ✅ compact constructor
record Age(int value) {
    Age { if (value < 0) throw new IllegalArgumentException(); }
}
```

**توضیح:** record خودکار validation ندارد؛ از compact constructor استفاده کنید.

---

## 🔗 ارتباط با سایر مفاهیم

- Records با **DDD Value Objects** و **DTO** در Spring و **JSON serialization** (Jackson) ترکیب می‌شوند.
- Sealed + record + switch پایه‌ی **Record Patterns** در Java 21 است.
- Pattern matching مکمل **Java 21 pattern matching for switch** است.
- Text blocks با **SQL/JPQL** و تست‌های **JSON** ترکیب می‌شوند.
- Java 17 پیش‌نیاز **Spring Boot 3/4** است.
