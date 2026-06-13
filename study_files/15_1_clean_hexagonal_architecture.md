# Clean Architecture / Hexagonal (Ports & Adapters)

> معماری لایه‌ای که domain را از framework جدا می‌کند. سوال محبوب مصاحبه‌های Lead.

---

## 📖 مفاهیم

### Clean Architecture

**توضیح:**

Clean Architecture (Uncle Bob) لایه‌های متحدالمرکز با **Dependency Rule** دارد: وابستگی همیشه به سمت **داخل** است. از بیرون به داخل: Frameworks & Drivers (DB، Web، UI) → Interface Adapters (Controllers، Gateways) → Use Cases (application logic) → Entities (business rules). **Entities** هیچ وابستگی خارجی ندارند؛ **Use Cases** فقط به Entities وابسته‌اند؛ framework بیرونی‌ترین و قابل‌تعویض‌ترین لایه است.

هدف: business logic مستقل از framework، DB، و UI — قابل‌تست، قابل‌نگهداری، و مقاوم در برابر تغییر تکنولوژی.

**چرا مهم است:**

framework (Spring، JPA) جزئیات است نه هسته. با این معماری می‌توان DB یا framework را عوض کرد بدون تغییر business logic.

**نکات کلیدی:**

- Dependency Rule: وابستگی فقط به سمت داخل.
- Entities و Use Cases نباید به framework وابسته باشند.
- framework در بیرونی‌ترین لایه (قابل‌تعویض).

---

### Hexagonal Architecture (Ports & Adapters)

**توضیح:**

نسخه‌ای از همان ایده: domain در مرکز، با **Ports** (interfaceها در domain) و **Adapters** (پیاده‌سازی‌ها در بیرون). **Driving (primary) Adapters** ورودی‌ها (REST، CLI، Test) که از طریق Driving Port با domain حرف می‌زنند. **Driven (secondary) Adapters** خروجی‌ها (DB، Message Broker، External API) که Driven Port را پیاده می‌کنند. domain هیچ‌چیز از بیرون نمی‌داند — فقط interface (port) را می‌شناسد.

این مستقیماً Dependency Inversion را پیاده می‌کند: domain port (interface) را تعریف می‌کند و adapter بیرونی آن را implement می‌کند، پس domain به جزئیات DB وابسته نیست.

**مثال کد:**

```java
// domain/port/out — port (interface در domain)
public interface OrderRepository { void save(Order order); }

// domain/usecase — use case فقط به port وابسته است
public class PlaceOrderUseCase {
    private final OrderRepository repository; // port، نه JPA
    public PlaceOrderUseCase(OrderRepository repository) { this.repository = repository; }
    public void execute(Order order) { order.validate(); repository.save(order); }
}

// adapter/out/persistence — adapter (پیاده‌سازی با JPA)
@Component
class JpaOrderRepository implements OrderRepository {
    public void save(Order order) { /* JPA */ }
}
```

**نکات کلیدی:**

- port در domain، adapter در بیرون (DIP).
- domain به Spring/JPA وابسته نیست → قابل‌تست خالص.
- structure پیشنهادی: domain/port/in, domain/port/out, application/usecase, adapter/in, adapter/out.

---

## 🎯 سوالات مصاحبه

### سوال ۱: Hexagonal Architecture چه مزیتی دارد و trade-off؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

مزیت اصلی: **جدا کردن business logic از جزئیات فنی** (framework، DB، UI). domain فقط به portها (interface) وابسته است نه به Spring/JPA، پس: (۱) قابل‌تست خالص (بدون بالا آوردن Spring یا DB، فقط mock کردن port). (۲) قابل‌تعویض بودن adapter (تغییر از JPA به MongoDB بدون لمس domain). (۳) تمرکز روی domain و مقاومت در برابر framework lock-in. trade-off: **boilerplate بیشتر** (interfaceها و mapping بین domain model و persistence model)، پیچیدگی اولیه، و برای CRUD ساده over-engineering. توصیه: برای domain پیچیده و core business با عمر طولانی ارزش دارد؛ برای CRUD ساده، لایه‌بندی سبک‌تر کافی است. کلید: کورکورانه اعمال نکنید.

**نکته مصاحبه:**

Lead به boilerplate و over-engineering برای CRUD ساده اشاره می‌کند.

---

### سوال ۲: Dependency Rule چیست و چطور با DIP مرتبط است؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

Dependency Rule می‌گوید وابستگی‌های کد همیشه باید به سمت **داخل** (به‌سمت business logic) اشاره کنند، نه بیرون. یعنی Entity به Use Case وابسته نیست، Use Case به Controller/DB وابسته نیست. اما چطور Use Case داده را persist می‌کند بدون وابستگی به DB؟ با **Dependency Inversion**: Use Case یک **port (interface)** تعریف می‌کند (مثل `OrderRepository`) و adapter لایه‌ی بیرونی آن را implement می‌کند. در runtime (با DI)، پیاده‌سازی concrete تزریق می‌شود. پس جهت وابستگی source-code از بیرون به داخل است (adapter به port در domain وابسته است) در حالی که جریان کنترل از بیرون به داخل می‌رود. این دقیقاً DIP است که Spring DI پیاده می‌کند.

**نکته مصاحبه:**

Lead تفاوت جهت وابستگی source-code با جریان کنترل را می‌فهمد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: نشت JPA entity به domain/use case

```java
// ❌ use case مستقیماً JPA entity و repository استفاده می‌کند
class UseCase { JpaUserRepository repo; }
```

```java
// ✅ port + domain model، mapping در adapter
class UseCase { UserRepository repo; } // interface
```

**توضیح:** نشت framework به domain کل مزیت را خنثی می‌کند.

---

### اشتباه ۲: Hexagonal برای CRUD ساده

```text
❌ لایه‌های زیاد و mapping برای یک CRUD ساده → boilerplate بی‌فایده
✅ معماری سبک‌تر برای دامنه‌ی ساده
```

**توضیح:** پیچیدگی باید با ارزش دامنه متناسب باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- Clean/Hexagonal با **SOLID/DIP (1.1)** و **Spring DI (2.1)**.
- ports با **DDD repository (6.1)**.
- domain model با **records/Value Object (1.4)**.
- مقاومت در برابر framework با **testing (12.5)**.
