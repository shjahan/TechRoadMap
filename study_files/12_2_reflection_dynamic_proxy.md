# Reflection & Dynamic Proxy & Annotation Processing

> پایه‌ی فریم‌ورک‌ها (Spring، Hibernate، Mockito). درک proxy برای فهم AOP و `@Transactional` لازم است.

---

## 📖 مفاهیم

### Reflection API

**توضیح:**

Reflection اجازه می‌دهد در runtime ساختار کلاس‌ها را بررسی و دستکاری کنید: خواندن field/method/annotation، فراخوانی متد، ساخت instance، حتی دسترسی به اعضای private (با `setAccessible(true)`). پایه‌ی DI containerها، serialization، و ORM. هزینه: reflection کند است (نسبت به فراخوانی مستقیم) و type safety زمان کامپایل را دور می‌زند — پس باید cache شود و با احتیاط استفاده شود.

**مثال کد:**

```java
Class<?> clazz = Class.forName("com.example.MyService");
Method method = clazz.getDeclaredMethod("process", String.class);
method.setAccessible(true);
Object result = method.invoke(instance, "arg");

Field field = clazz.getDeclaredField("secret");
field.setAccessible(true);
field.set(instance, "value");
```

**نکات کلیدی:**

- reflection کند است؛ نتیجه‌ی lookup (Method/Field) را cache کنید.
- `setAccessible(true)` encapsulation را می‌شکند؛ با ماژول‌ها (Java 9+) نیاز به `opens`.
- کاربرد: framework، نه کد کسب‌وکار عادی.

---

### Dynamic Proxy

**توضیح:**

ساخت پیاده‌سازی یک interface در runtime. **JDK Dynamic Proxy** فقط برای interface کار می‌کند (`Proxy.newProxyInstance` با `InvocationHandler`). **CGLIB** با subclassing برای کلاس بدون interface (نیاز کلاس/متد غیرfinal). **ByteBuddy** مدرن‌تر (Mockito از آن استفاده می‌کند). پایه‌ی AOP در Spring.

**مثال کد:**

```java
// JDK Dynamic Proxy — logging قبل/بعد از هر متد
MyService proxy = (MyService) Proxy.newProxyInstance(
    MyService.class.getClassLoader(),
    new Class[]{MyService.class},
    (proxyObj, method, args) -> {
        System.out.println("Before: " + method.getName());
        Object result = method.invoke(target, args);
        System.out.println("After: " + method.getName());
        return result;
    });
```

**نکات کلیدی:**

- JDK proxy برای interface، CGLIB برای class.
- self-invocation از proxy عبور نمی‌کند (ریشه‌ی مشکل `@Transactional`).
- متد/کلاس final توسط CGLIB قابل proxy نیست.

---

### Annotation Processing

**توضیح:**

`@Retention` تعیین می‌کند annotation تا کِی باقی بماند: `SOURCE` (فقط در کد، مثل `@Override`)، `CLASS` (در bytecode)، `RUNTIME` (در runtime با reflection قابل‌دسترس — برای framework). `@Target` محل مجاز. annotation + reflection (در runtime) یا annotation processor (در compile time، مثل Lombok، MapStruct) ابزار قدرتمندی است.

**نکات کلیدی:**

- `RUNTIME` برای annotationهایی که framework در runtime می‌خواند.
- annotation processor (compile-time) کد تولید می‌کند بدون سربار runtime.

---

## 🎯 سوالات مصاحبه

### سوال ۱: JDK Dynamic Proxy در برابر CGLIB؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

JDK Dynamic Proxy بخشی از JDK است و یک شیء proxy می‌سازد که **interface** را پیاده می‌کند؛ پس کلاس هدف باید interface داشته باشد. CGLIB (و امروزه ByteBuddy) با **subclassing** کلاس هدف proxy می‌سازد، پس به interface نیاز ندارد اما کلاس و متدها نباید `final` باشند (چون CGLIB با override کردن کار می‌کند و final قابل override نیست). Spring قدیماً اگر bean interface داشت JDK proxy و وگرنه CGLIB می‌ساخت؛ Spring Boot به‌صورت پیش‌فرض CGLIB را ترجیح می‌دهد. پیامد عملی: متد `final` در یک bean با `@Transactional` کار نمی‌کند چون proxy نمی‌تواند آن را intercept کند.

**نکته مصاحبه:**

Senior به محدودیت final و رابطه با `@Transactional` اشاره می‌کند.

---

### سوال ۲: چرا reflection کند است و چطور بهینه می‌کنی؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

reflection کند است چون: lookup (پیدا کردن Method/Field با نام) جستجو و بررسی می‌خواهد، فراخوانی reflective چک‌های امنیتی و type دارد و JIT نمی‌تواند آن را به‌خوبی inline کند، و autoboxing برای آرگومان‌ها. بهینه‌سازی: (۱) نتیجه‌ی lookup (شیء `Method`/`Field`) را cache کنید تا فقط یک‌بار جستجو شود. (۲) `setAccessible(true)` چک‌های دسترسی را حذف می‌کند. (۳) برای فراخوانی مکرر، `MethodHandle` (سریع‌تر از reflection) یا `LambdaMetafactory` استفاده کنید. (۴) در صورت امکان، annotation processing (compile-time code generation مثل MapStruct) به‌جای reflection runtime. فریم‌ورک‌ها این بهینه‌سازی‌ها را انجام می‌دهند.

**نکته مصاحبه:**

Senior به cache کردن Method و MethodHandle اشاره می‌کند.

---

### سوال ۳: تفاوت RetentionPolicy.SOURCE/CLASS/RUNTIME؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`SOURCE`: annotation فقط در کد منبع است و توسط compiler/ابزار (مثل `@Override` که فقط چک می‌شود) استفاده و سپس دور انداخته می‌شود — در bytecode نیست. `CLASS` (پیش‌فرض): در bytecode هست اما در runtime با reflection قابل‌دسترس نیست؛ برای ابزارهای bytecode-level. `RUNTIME`: در runtime با reflection قابل‌خواندن — این چیزی است که فریم‌ورک‌هایی مثل Spring (`@Autowired`, `@Transactional`) و Hibernate (`@Entity`) نیاز دارند تا در runtime رفتار را تعیین کنند. انتخاب: اگر annotation باید در runtime توسط framework خوانده شود، `RUNTIME`؛ اگر فقط compile-time processing، `SOURCE`.

**نکته مصاحبه:**

Senior می‌داند framework annotationها باید RUNTIME باشند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: reflection بدون cache

```java
// ❌ lookup در هر فراخوانی
obj.getClass().getMethod("x").invoke(obj);
```

```java
// ✅ Method را یک‌بار cache کنید
```

**توضیح:** lookup مکرر کند است.

---

### اشتباه ۲: متد final با `@Transactional`

```java
// ❌ CGLIB نمی‌تواند override کند → transaction اعمال نمی‌شود
@Transactional public final void save() {}
```

```java
// ✅ غیرfinal
@Transactional public void save() {}
```

**توضیح:** proxy نمی‌تواند متد final را intercept کند.

---

### اشتباه ۳: annotation با retention اشتباه

```java
// ❌ framework نمی‌تواند در runtime بخواند
@Retention(RetentionPolicy.SOURCE)
public @interface MyFrameworkAnnotation {}
```

```java
// ✅
@Retention(RetentionPolicy.RUNTIME)
```

**توضیح:** annotation framework باید RUNTIME باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- proxy با **Spring AOP/`@Transactional` (2.1, 2.4)** و self-invocation.
- reflection با **Spring DI** و **Hibernate**.
- annotation با **custom annotation + AOP** و **MapStruct/Lombok**.
- MethodHandle با **performance (12.6)**.
