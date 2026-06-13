# Java 8 — نقطه عطف (Functional Programming, Streams, Optional)

> Java 8 مهم‌ترین نسخه‌ی تاریخ Java است. هر مصاحبه‌ی Senior حتماً Lambda، Stream و Optional را عمیق می‌پرسد.

---

## 📖 مفاهیم

### Lambda Expressions

**توضیح:**

Lambda یک تابع بی‌نام است که می‌توان آن را مثل داده پاس داد. پیش از Java 8، برای پاس دادن رفتار مجبور به ساخت anonymous class بودیم. Lambda این boilerplate را حذف می‌کند. از نظر فنی، lambda یک نمونه از یک **functional interface** (interface با دقیقاً یک متد abstract) می‌سازد.

نکته‌ی مهم Senior: lambda با anonymous class فرق دارد. lambda `this` را به کلاس میزبان bind می‌کند (نه به خودش)، شیء جدید برای هر فراخوانی نمی‌سازد (می‌تواند cache شود)، و در bytecode با `invokedynamic` پیاده می‌شود نه با کلاس مجزا.

**چرا مهم است:**

کل Stream API، callbackها، event handlerها و توابع functional روی lambda بنا شده‌اند. کد خواناتر و قابل‌ترکیب‌تر می‌شود.

**مثال کد:**

```java
// قبل: anonymous class پرحرف
Runnable r1 = new Runnable() {
    @Override public void run() { System.out.println("run"); }
};
// بعد: lambda
Runnable r2 = () -> System.out.println("run");

// lambda به‌عنوان رفتار قابل پاس
List<String> names = new ArrayList<>(List.of("Sara", "Ali", "Reza"));
names.sort((a, b) -> a.length() - b.length()); // مرتب‌سازی بر اساس طول
```

**نکات کلیدی:**

- lambda فقط برای functional interface (تک‌متده) کار می‌کند.
- `this` در lambda به کلاس بیرونی اشاره می‌کند نه به خود lambda.
- متغیرهای محلی استفاده‌شده در lambda باید effectively final باشند.

---

### Functional Interfaces

**توضیح:**

interface با یک متد abstract که با `@FunctionalInterface` علامت می‌خورد. پکیج `java.util.function` چندین مورد آماده دارد:

- `Function<T,R>` — یک ورودی، یک خروجی (`apply`)
- `Predicate<T>` — ورودی، خروجی boolean (`test`)
- `Consumer<T>` — ورودی، بدون خروجی (`accept`)
- `Supplier<T>` — بدون ورودی، یک خروجی (`get`)
- `BiFunction<T,U,R>` — دو ورودی، یک خروجی

این interfaceها قابل ترکیب‌اند (`andThen`, `compose`, `and`, `or`, `negate`).

**چرا مهم است:**

این‌ها زبان مشترک API‌های functional هستند. Stream، Optional و CompletableFuture همه از این interfaceها استفاده می‌کنند.

**مثال کد:**

```java
Function<Integer, Integer> doubler = x -> x * 2;
Function<Integer, Integer> increment = x -> x + 1;
// ترکیب: اول double بعد increment
System.out.println(doubler.andThen(increment).apply(5)); // 11
// ترکیب معکوس: اول increment بعد double
System.out.println(doubler.compose(increment).apply(5)); // 12

Predicate<String> notBlank = s -> !s.isBlank();
Predicate<String> shortStr = s -> s.length() < 5;
System.out.println(notBlank.and(shortStr).test("hi")); // true
```

**نکات کلیدی:**

- برای primitive از نسخه‌های تخصصی استفاده کنید (`IntFunction`, `ToIntFunction`) تا از boxing فرار کنید.
- `Function.identity()` گاهی در Collectors لازم می‌شود.
- ترکیب‌پذیری (`andThen`/`compose`) کد را تمیز نگه می‌دارد.

---

### Method References

**توضیح:**

میان‌بری برای lambda‌ای که فقط یک متد موجود را صدا می‌زند. چهار نوع:

1. `Class::staticMethod` — `Integer::parseInt`
2. `instance::method` — `System.out::println`
3. `Class::instanceMethod` — `String::toUpperCase` (اولین آرگومان receiver می‌شود)
4. `Class::new` — constructor reference

**چرا مهم است:**

خوانایی را بالا می‌برد و قصد کد را شفاف می‌کند. در Stream pipelineها بسیار رایج است.

**مثال کد:**

```java
List<String> names = List.of("sara", "ali");
names.stream()
     .map(String::toUpperCase)   // Class::instanceMethod
     .forEach(System.out::println); // instance::method

// constructor reference
Supplier<ArrayList<String>> listFactory = ArrayList::new;
```

**نکات کلیدی:**

- وقتی lambda فقط یک متد را صدا می‌زند، method reference تمیزتر است.
- مراقب ابهام بین `Class::instanceMethod` و `Class::staticMethod` باشید.

---

### Stream API

**توضیح:**

Stream یک خط لوله‌ی پردازش داده است که به سبک declarative نوشته می‌شود. سه بخش دارد: منبع (collection، array، …)، عملیات میانی (intermediate) که lazy هستند و یک Stream جدید برمی‌گردانند، و عملیات نهایی (terminal) که نتیجه تولید می‌کند و pipeline را اجرا می‌کند.

**Lazy evaluation** هسته‌ی Stream است: تا وقتی terminal operation صدا زده نشود، هیچ عملیات میانی اجرا نمی‌شود. این امکان short-circuit (مثل `findFirst`, `limit`) و بهینه‌سازی را می‌دهد.

عملیات میانی: `filter`, `map`, `flatMap`, `sorted`, `distinct`, `limit`, `peek`.
عملیات نهایی: `collect`, `forEach`, `reduce`, `count`, `findFirst`, `anyMatch`.

`parallelStream()` کار را روی `ForkJoinPool.commonPool()` پخش می‌کند — فقط برای حجم بالا و عملیات بدون side-effect و stateless مفید است.

**چرا مهم است:**

Stream کد پردازش داده را خواناتر و کوتاه‌تر می‌کند. اما استفاده‌ی نادرست (مثلاً parallel بی‌جا یا side-effect داخل stream) منشأ باگ است.

**مثال کد:**

```java
record Order(String customer, String status, long amountCents) {}

List<Order> orders = List.of(
    new Order("Ali", "PAID", 5000),
    new Order("Sara", "PAID", 12000),
    new Order("Ali", "PENDING", 3000));

// مجموع مبلغ سفارش‌های پرداخت‌شده به ازای هر مشتری
Map<String, Long> totals = orders.stream()
    .filter(o -> o.status().equals("PAID")) // میانی - lazy
    .collect(Collectors.groupingBy(
        Order::customer,
        Collectors.summingLong(Order::amountCents))); // نهایی
System.out.println(totals); // {Ali=5000, Sara=12000}

// flatMap: تخت کردن ساختار تو در تو
List<List<Integer>> nested = List.of(List.of(1, 2), List.of(3, 4));
List<Integer> flat = nested.stream()
    .flatMap(List::stream)
    .toList(); // [1, 2, 3, 4]
```

**نکات کلیدی:**

- عملیات میانی lazy است؛ بدون terminal هیچ اتفاقی نمی‌افتد.
- داخل stream از side-effect پرهیز کنید (به‌جز `forEach` در انتها).
- `parallelStream` فقط برای حجم بالا و عملیات stateless؛ وگرنه کندتر و خطرناک است.

---

### map vs flatMap

**توضیح:**

`map` هر عنصر را به یک عنصر تبدیل می‌کند (یک‌به‌یک). `flatMap` هر عنصر را به یک Stream تبدیل می‌کند و سپس همه را در یک Stream واحد ادغام (flatten) می‌کند (یک‌به‌چند). `flatMap` برای کار با ساختارهای تو در تو یا `Optional`/`Stream` تو در تو ضروری است.

**مثال کد:**

```java
// map: تبدیل یک‌به‌یک
List<Integer> lengths = Stream.of("a", "bb", "ccc").map(String::length).toList();

// flatMap: تخت کردن لیست کلمات هر جمله
List<String> words = Stream.of("hello world", "java stream")
    .flatMap(s -> Arrays.stream(s.split(" ")))
    .toList(); // [hello, world, java, stream]
```

**نکات کلیدی:**

- اگر تبدیل شما `Stream<Stream<X>>` می‌سازد، احتمالاً به flatMap نیاز دارید.
- flatMap با Optional هم کار می‌کند (تخت کردن Optional تو در تو).

---

### Optional

**توضیح:**

`Optional<T>` یک ظرف برای نمایش «شاید مقدار، شاید هیچ» است و برای کاهش NPE طراحی شده. سازنده‌ها: `Optional.of(value)` (مقدار غیرnull)، `ofNullable(value)` (ممکن null)، `empty()`. عملیات: `map`, `flatMap`, `filter`, `orElse`, `orElseGet`, `orElseThrow`, `ifPresent`, `ifPresentOrElse`.

تفاوت کلیدی: `orElse(x)` همیشه `x` را ارزیابی می‌کند (حتی اگر مقدار موجود باشد)؛ `orElseGet(supplier)` فقط در صورت خالی بودن، supplier را اجرا می‌کند — بنابراین برای عملیات سنگین `orElseGet` بهتر است.

**چرا مهم است:**

به‌جای برگرداندن null از متد، Optional قصد را شفاف می‌کند و caller را مجبور به مدیریت حالت خالی می‌کند.

**مثال کد:**

```java
Optional<User> user = repository.findById(id);

// زنجیره‌ای و null-safe
String city = user
    .map(User::address)
    .map(Address::city)
    .orElse("نامشخص");

// ❌ این کل هدف Optional را نقض می‌کند
if (user.isPresent()) { return user.get(); }

// ✅ idiomatic
return user.orElseThrow(() -> new UserNotFoundException(id));
```

**نکات کلیدی:**

- Optional را به‌عنوان field یا پارامتر متد استفاده نکنید؛ فقط به‌عنوان return type.
- `get()` بدون چک خطرناک است؛ `orElseThrow`/`orElse` را ترجیح دهید.
- `orElseGet` برای fallback پرهزینه؛ `orElse` برای ثابت ساده.

---

### Date/Time API (java.time)

**توضیح:**

API قدیمی `Date`/`Calendar` معیوب بود: mutable، thread-unsafe، ماه‌ها از صفر، طراحی گیج‌کننده. `java.time` (الهام از Joda-Time) جایگزین immutable و thread-safe آورد:

- `LocalDate` (تاریخ بدون زمان)، `LocalTime`، `LocalDateTime` (بدون منطقه)
- `ZonedDateTime` (با منطقه‌ی زمانی)، `Instant` (نقطه روی خط زمان UTC)
- `Duration` (فاصله‌ی زمانی مبتنی بر ثانیه)، `Period` (مبتنی بر تاریخ)
- `DateTimeFormatter` برای parse/format

**چرا مهم است:**

مدیریت اشتباه منطقه‌ی زمانی منبع باگ‌های جدی در سیستم‌های توزیع‌شده است. ذخیره‌ی زمان به‌صورت `Instant`/UTC و تبدیل در لایه‌ی نمایش best practice است.

**مثال کد:**

```java
LocalDate today = LocalDate.now();
LocalDate nextWeek = today.plusWeeks(1); // immutable → شیء جدید

Instant now = Instant.now(); // UTC، برای ذخیره در DB
ZonedDateTime tehran = now.atZone(ZoneId.of("Asia/Tehran"));

Duration between = Duration.between(
    LocalTime.of(9, 0), LocalTime.of(17, 30));
System.out.println(between.toHours()); // 8

String formatted = today.format(DateTimeFormatter.ISO_DATE);
```

**نکات کلیدی:**

- همه‌ی کلاس‌های java.time immutable هستند → thread-safe.
- برای ذخیره‌سازی از `Instant`/UTC استفاده کنید، تبدیل منطقه را به لایه‌ی presentation بسپارید.
- `Period` برای تاریخ (روز/ماه/سال)، `Duration` برای زمان (ساعت/دقیقه/ثانیه).

---

### Default & Static Methods در Interface

**توضیح:**

از Java 8، interface می‌تواند متد `default` (با بدنه) و `static` داشته باشد. انگیزه‌ی اصلی **backward compatibility** بود: افزودن `stream()` و `forEach()` به `Collection` بدون شکستن میلیون‌ها پیاده‌سازی موجود.

این قابلیت یک شکل محدود از multiple inheritance رفتار می‌آورد و در نتیجه **diamond problem** ممکن می‌شود: اگر کلاسی دو interface با متد default هم‌نام implement کند، کامپایلر خطا می‌دهد و کلاس مجبور است متد را override کرده و با `Interface.super.method()` ابهام را حل کند.

**مثال کد:**

```java
interface A { default String hi() { return "A"; } }
interface B { default String hi() { return "B"; } }

class C implements A, B {
    @Override public String hi() {
        return A.super.hi() + B.super.hi(); // رفع ابهام diamond
    }
}
```

**نکات کلیدی:**

- default method برای تکامل API بدون شکستن backward compatibility است.
- diamond problem را باید با override صریح حل کرد.
- متد static در interface به ارث نمی‌رسد و فقط با نام interface صدا زده می‌شود.

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت `orElse` و `orElseGet` چیست؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

هر دو مقدار fallback را وقتی Optional خالی است برمی‌گردانند، اما زمان ارزیابی فرق دارد. `orElse(value)` آرگومان را **همیشه** ارزیابی می‌کند — حتی اگر Optional مقدار داشته باشد و fallback استفاده نشود. `orElseGet(supplier)` تنبل است: supplier فقط هنگام خالی بودن اجرا می‌شود.

این تفاوت وقتی fallback پرهزینه است (مثلاً فراخوانی DB یا ساخت شیء سنگین) بحرانی می‌شود. استفاده از `orElse(expensiveCall())` یعنی expensiveCall همیشه اجرا می‌شود، حتی بی‌فایده — یک باگ performance خاموش.

**کد توضیحی:**

```java
// ❌ getDefaultFromDb() همیشه اجرا می‌شود حتی اگر user موجود باشد
User u1 = findUser().orElse(getDefaultFromDb());

// ✅ getDefaultFromDb() فقط در صورت خالی بودن
User u2 = findUser().orElseGet(this::getDefaultFromDb);
```

**نکته مصاحبه:**

Senior به ارزیابی eager در برابر lazy و پیامد performance اشاره می‌کند. Follow-up: «کِی `orElse` کافی است؟» (وقتی fallback یک ثابت ارزان است).

---

### سوال ۲: Stream lazy یعنی چه و چه فایده‌ای دارد؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

عملیات میانی Stream تا قبل از terminal اجرا نمی‌شوند؛ Stream فقط pipeline را تعریف می‌کند. وقتی terminal صدا زده می‌شود، عناصر یکی‌یکی از منبع کشیده شده و از کل pipeline عبور می‌کنند (نه اینکه هر مرحله روی کل داده اجرا شود). این رفتار دو مزیت می‌دهد: **short-circuit** (مثلاً با `findFirst` یا `limit` به‌محض یافتن نتیجه متوقف می‌شود) و امکان کار با Streamهای بی‌نهایت (`Stream.iterate`).

**کد توضیحی:**

```java
// peek نشان می‌دهد فقط تا یافتن اولین مورد اجرا می‌شود
Optional<Integer> first = Stream.iterate(1, n -> n + 1) // بی‌نهایت
    .peek(n -> System.out.println("check " + n))
    .filter(n -> n % 7 == 0)
    .findFirst(); // فقط تا 7 ادامه می‌یابد
```

**نکته مصاحبه:**

Senior می‌داند که عناصر «عمودی» از pipeline عبور می‌کنند نه «افقی». Follow-up: «چرا یک Stream را نمی‌توان دوبار مصرف کرد؟» (پاسخ: Stream یک‌بارمصرف است، پس از terminal بسته می‌شود).

---

### سوال ۳: چرا نباید Optional را به‌عنوان field یا پارامتر استفاده کرد؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Optional برای نمایش «نبود مقدار به‌عنوان خروجی متد» طراحی شده، نه به‌عنوان ظرف عمومی nullability. به‌عنوان field مشکلاتی دارد: serializable نیست (شکستن JPA/Jackson قدیمی)، یک سطح indirection و تخصیص اضافه می‌آورد، و کد را پیچیده‌تر می‌کند بدون مزیت واقعی. به‌عنوان پارامتر هم بد است چون caller را مجبور به wrap کردن می‌کند و سه حالت ایجاد می‌کند (null, empty, present) که بدتر است.

best practice: field را nullable نگه دارید و در getter آن را `Optional.ofNullable(...)` برگردانید، یا از pattern دیگری استفاده کنید.

**نکته مصاحبه:**

نشان‌دهنده‌ی درک طراحی API. Follow-up: «پس برای فیلد nullable چه می‌کنی؟» (getter که Optional برمی‌گرداند یا null object pattern).

---

### سوال ۴: parallelStream کِی مفید و کِی خطرناک است؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

`parallelStream` کار را روی `ForkJoinPool.commonPool()` (به تعداد هسته‌ها) تقسیم می‌کند. فقط وقتی مفید است که: حجم داده بزرگ باشد، عملیات CPU-bound و مستقل (stateless، بدون side-effect) باشد، و ساختار داده به‌خوبی splittable باشد (آرایه، ArrayList بهتر از LinkedList).

خطرناک است وقتی: عملیات side-effect دارد (race condition)، داده کم است (سربار تقسیم غالب می‌شود)، یا داخل آن I/O بلاک‌کننده انجام می‌دهید (کل commonPool را اشغال می‌کنید و کل برنامه را کند می‌کنید). همچنین ترتیب نتایج ممکن است تغییر کند.

**کد توضیحی:**

```java
// مناسب: محاسبه‌ی CPU-bound روی حجم بالا
long count = LongStream.rangeClosed(1, 10_000_000)
    .parallel()
    .filter(PrimeUtil::isPrime)
    .count();

// خطرناک: side-effect → race condition
List<Integer> sink = new ArrayList<>();
// numbers.parallelStream().forEach(sink::add); // ❌ ArrayList thread-safe نیست
```

**نکته مصاحبه:**

Lead به اشتراک commonPool و خطر بلاک کردن I/O اشاره می‌کند. Follow-up: «چطور یک ForkJoinPool اختصاصی برای parallel stream بدهی؟»

---

### سوال ۵: تفاوت lambda و anonymous class چیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

تفاوت‌های مهم: (۱) در lambda، `this` به کلاس میزبان اشاره می‌کند؛ در anonymous class به خود شیء anonymous. (۲) lambda می‌تواند فقط functional interface را پیاده کند؛ anonymous class هر interface/کلاس را. (۳) anonymous class همیشه یک کلاس و شیء جدید می‌سازد؛ lambda با `invokedynamic` پیاده می‌شود و JVM می‌تواند آن را بهینه/cache کند. (۴) anonymous class می‌تواند state و چند متد داشته باشد؛ lambda بدون state و تک‌رفتاری است.

**نکته مصاحبه:**

اشاره به `this` و `invokedynamic` تمایز Senior است. Follow-up: «متغیر محلی در lambda چرا باید effectively final باشد؟» (پاسخ: lambda مقدار را capture می‌کند نه ارجاع متغیر؛ برای جلوگیری از ناسازگاری visibility در concurrency).

---

### سوال ۶: چرا default method اضافه شد و diamond problem را چطور حل می‌کند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

default method برای تکامل interfaceها بدون شکستن پیاده‌سازی‌های موجود اضافه شد — مثلاً افزودن `Collection.stream()`. اگر بدون default اضافه می‌شد، هر کلاسی که Collection را پیاده کرده بود می‌شکست.

diamond problem وقتی رخ می‌دهد که کلاسی دو interface با متد default هم‌امضا را implement کند. Java در این حالت کامپایل نمی‌شود و توسعه‌دهنده را مجبور می‌کند متد را override کرده و با سینتکس `InterfaceName.super.method()` انتخاب صریح کند. این برخلاف C++ از ابهام خاموش جلوگیری می‌کند.

**نکته مصاحبه:**

Follow-up: «اگر یک کلاس و یک interface متد هم‌نام داشته باشند کدام برنده است؟» (پاسخ: کلاس همیشه بر interface اولویت دارد — "class wins").

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: side-effect داخل Stream

```java
// ❌ تغییر state بیرونی داخل map
List<String> result = new ArrayList<>();
items.stream().map(i -> { result.add(i); return i; }).count();
```

```java
// ✅ استفاده از collect
List<String> result = items.stream().collect(Collectors.toList());
```

**توضیح:** Streamها باید بدون side-effect باشند؛ به‌خصوص در حالت parallel این race condition می‌سازد. از collector استفاده کنید.

---

### اشتباه ۲: استفاده از `get()` روی Optional بدون چک

```java
// ❌ اگر خالی باشد NoSuchElementException
User u = repository.findById(id).get();
```

```java
// ✅
User u = repository.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));
```

**توضیح:** `get()` کل هدف Optional (اجبار به مدیریت حالت خالی) را نقض می‌کند.

---

### اشتباه ۳: استفاده از `Date` به‌جای `java.time`

```java
// ❌ mutable، thread-unsafe، ماه از صفر
Date d = new Date(2024 - 1900, 0, 15);
```

```java
// ✅
LocalDate d = LocalDate.of(2024, 1, 15);
```

**توضیح:** `Date`/`Calendar` معیوب و خطاپذیرند. همیشه `java.time` استفاده کنید.

---

### اشتباه ۴: استفاده از `orElse` با fallback پرهزینه

```java
// ❌ buildExpensiveDefault همیشه اجرا می‌شود
Config c = findConfig().orElse(buildExpensiveDefault());
```

```java
// ✅
Config c = findConfig().orElseGet(this::buildExpensiveDefault);
```

**توضیح:** `orElse` آرگومان را eager ارزیابی می‌کند؛ برای fallback سنگین `orElseGet` لازم است.

---

### اشتباه ۵: استفاده‌ی مجدد از یک Stream

```java
// ❌ IllegalStateException: stream has already been operated upon
Stream<String> s = list.stream();
s.filter(x -> true).count();
s.map(String::length).count(); // خطا
```

```java
// ✅ هر بار stream جدید بسازید
list.stream().filter(x -> true).count();
list.stream().map(String::length).count();
```

**توضیح:** Stream یک‌بارمصرف است؛ پس از terminal بسته می‌شود.

---

## 🔗 ارتباط با سایر مفاهیم

- Functional interfaces پایه‌ی **CompletableFuture** و **Reactive (Reactor)** در فصل‌های بعد هستند.
- Stream API با **Collections** و **Collectors** گره خورده و در **Spring Data** و پردازش داده استفاده می‌شود.
- Optional با الگوی **null-safety** و در Spring (`Optional<T>` به‌عنوان return type ریپازیتوری) ترکیب می‌شود.
- درک lambda و effectively final پیش‌نیاز **Concurrency** و کار با thread است.
- وقتی **functional style** می‌بینید، احتمالاً generics و method reference هم درگیرند.
