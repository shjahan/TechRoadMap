# Spring Data — JPA، Transactions، N+1، Locking

> Spring Data JPA پرتکرارترین موضوع مصاحبه‌ی backend است. N+1 و transaction propagation سوالات کلاسیک Senior هستند.

---

## 📖 مفاهیم

### Repository Abstraction

**توضیح:**

Spring Data سلسله‌مراتب repository می‌دهد: `Repository` (مارکر) → `CrudRepository` (CRUD پایه) → `PagingAndSortingRepository` → `JpaRepository` (متدهای JPA-specific مثل `flush`, `saveAll`, batch). شما فقط interface تعریف می‌کنید و Spring پیاده‌سازی را در runtime می‌سازد.

**Query derivation:** Spring از نام متد query می‌سازد: `findByNameAndAgeGreaterThan(String name, int age)`. برای queryهای پیچیده‌تر `@Query` با JPQL یا native SQL. `@Modifying` برای update/delete (نیاز به `@Transactional`).

**چرا مهم است:**

کاهش boilerplate دسترسی داده. اما استفاده‌ی ناآگاهانه (مثل بارگذاری همه با `findAll` یا N+1) منشأ مشکلات performance است.

**مثال کد:**

```java
public interface UserRepository extends JpaRepository<User, Long> {
    // query derivation
    List<User> findByStatusAndCreatedAtAfter(Status status, Instant after);

    // JPQL سفارشی
    @Query("SELECT u FROM User u WHERE u.email = :email")
    Optional<User> findByEmail(@Param("email") String email);

    // native + modifying
    @Modifying
    @Query(value = "UPDATE users SET status = 'INACTIVE' WHERE last_login < :date",
           nativeQuery = true)
    int deactivateInactiveUsers(@Param("date") Instant date);
}
```

**نکات کلیدی:**

- query derivation برای ساده؛ `@Query` برای پیچیده.
- `@Modifying` به `@Transactional` و گاهی `clearAutomatically` نیاز دارد.
- از برگرداندن کل جدول بپرهیزید؛ از `Pageable` استفاده کنید.

---

### N+1 Problem

**توضیح:**

شایع‌ترین مشکل performance در JPA. وقتی یک collection یا association را `LAZY` بارگذاری می‌کنید و سپس روی نتایج پیمایش می‌کنید، Hibernate برای هر رکورد یک query جداگانه می‌زند: ۱ query برای لیست اصلی + N query برای associationها = N+1.

راه‌حل‌ها: (۱) `JOIN FETCH` در JPQL، (۲) `@EntityGraph` برای تعریف declarative آنچه باید eager بارگذاری شود، (۳) batch fetching (`@BatchSize` یا `hibernate.default_batch_fetch_size`)، (۴) DTO projection که فقط فیلدهای لازم را با یک query می‌گیرد.

**چرا مهم است:**

N+1 در dev با داده‌ی کم نامرئی است اما در production با هزاران رکورد فاجعه می‌شود. تشخیص آن (لاگ SQL یا ابزار) و حل آن مهارت کلیدی Senior است.

**مثال کد:**

```java
// ❌ N+1: برای هر order یک query برای items
List<Order> orders = orderRepository.findAll();
orders.forEach(o -> o.getItems().size()); // N query اضافه

// ✅ راه‌حل ۱: JOIN FETCH
@Query("SELECT DISTINCT o FROM Order o LEFT JOIN FETCH o.items")
List<Order> findAllWithItems();

// ✅ راه‌حل ۲: EntityGraph
@EntityGraph(attributePaths = {"items", "customer"})
List<Order> findByStatus(Status status);
```

**نکات کلیدی:**

- پیش‌فرض `@ManyToOne` EAGER و `@OneToMany` LAZY است؛ معمولاً همه را LAZY کنید و انتخابی fetch کنید.
- `JOIN FETCH` با pagination مشکل دارد (در حافظه صفحه‌بندی می‌کند)؛ برای آن از `@BatchSize` یا دو query استفاده کنید.
- SQL تولیدی را در dev لاگ کنید (`spring.jpa.show-sql` یا بهتر، p6spy).

---

### Pagination & Projections

**توضیح:**

`Pageable` و `Page<T>` صفحه‌بندی + شمارش کل را می‌دهند؛ `Slice<T>` فقط می‌داند صفحه‌ی بعدی هست یا نه (بدون count گران). **Projections** اجازه می‌دهند فقط زیرمجموعه‌ای از فیلدها بارگذاری شوند: interface-based (closed/open) یا class-based (DTO با constructor expression).

**مثال کد:**

```java
// projection با interface
public interface UserSummary {
    Long getId();
    String getName();
}
Page<UserSummary> findByStatus(Status status, Pageable pageable);

// استفاده
Page<UserSummary> page = repo.findByStatus(
    Status.ACTIVE, PageRequest.of(0, 20, Sort.by("name")));
```

**نکات کلیدی:**

- `Page` یک query شمارش اضافه می‌زند؛ اگر count لازم نیست `Slice` بهتر است.
- projection فقط ستون‌های لازم را select می‌کند → کارایی بهتر.

---

### Transactions — Propagation & Isolation

**توضیح:**

`@Transactional` مرز تراکنش را تعریف می‌کند. **Propagation** رفتار وقتی متدی داخل تراکنش دیگری صدا زده می‌شود:

- `REQUIRED` (پیش‌فرض): به تراکنش موجود می‌پیوندد یا جدید می‌سازد.
- `REQUIRES_NEW`: همیشه تراکنش جدید و مستقل (تراکنش بیرونی معلق می‌شود) — برای logging/audit که باید مستقل از rollback اصلی commit شوند.
- `NESTED`: savepoint داخل تراکنش موجود.
- `SUPPORTS`, `NOT_SUPPORTED`, `MANDATORY`, `NEVER`.

**Isolation** کنترل دیده شدن تغییرات تراکنش‌های هم‌زمان: `READ_UNCOMMITTED`, `READ_COMMITTED` (پیش‌فرض اکثر DBها)، `REPEATABLE_READ`, `SERIALIZABLE`. هر سطح بالاتر از anomalyهای بیشتر (dirty read، non-repeatable read، phantom) جلوگیری می‌کند اما concurrency را کم می‌کند.

نکته‌ی مهم: rollback پیش‌فرض فقط برای **unchecked** exception است. برای checked باید `rollbackFor` مشخص شود.

**چرا مهم است:**

مدیریت اشتباه تراکنش منجر به data inconsistency، deadlock، و باگ‌های ظریف می‌شود. propagation در سناریوهای واقعی (مثل audit log که باید حتی با rollback اصلی بماند) حیاتی است.

**مثال کد:**

```java
@Service
public class OrderService {
    @Transactional // REQUIRED پیش‌فرض
    public void placeOrder(Order order) {
        orderRepository.save(order);
        auditService.log("order placed"); // باید مستقل commit شود
        paymentService.charge(order);      // اگر اینجا خطا → rollback همه‌چیز جز audit
    }
}

@Service
class AuditService {
    @Transactional(propagation = Propagation.REQUIRES_NEW) // مستقل
    public void log(String message) {
        auditRepository.save(new AuditEntry(message));
    }
}
```

**نکات کلیدی:**

- rollback پیش‌فرض فقط unchecked؛ برای checked از `rollbackFor` استفاده کنید.
- `REQUIRES_NEW` برای audit/logging مستقل.
- self-invocation تراکنش را می‌شکند (proxy؛ بخش Spring Core).

---

### Locking — Optimistic vs Pessimistic

**توضیح:**

**Optimistic locking** فرض می‌کند تداخل نادر است: یک ستون `@Version` نگه می‌دارد و هنگام update چک می‌کند version تغییر نکرده باشد؛ اگر کرده، `OptimisticLockException`. مناسب برای read-heavy و تداخل کم. **Pessimistic locking** ردیف را در DB قفل می‌کند (`SELECT FOR UPDATE`) تا دیگران نتوانند تغییر دهند؛ مناسب برای تداخل زیاد اما هزینه‌ی concurrency.

**مثال کد:**

```java
@Entity
class Product {
    @Id Long id;
    @Version Long version; // optimistic locking خودکار
    int stock;
}

public interface ProductRepository extends JpaRepository<Product, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("SELECT p FROM Product p WHERE p.id = :id")
    Optional<Product> findByIdForUpdate(@Param("id") Long id);
}
```

**نکات کلیدی:**

- optimistic برای تداخل کم (پیش‌فرض خوب)؛ pessimistic برای rezervation/stock بحرانی.
- optimistic lock failure را با retry مدیریت کنید.

---

### Spring Data MongoDB & Redis

**توضیح:**

`MongoRepository`/`MongoTemplate` برای MongoDB با `@Document`. `RedisTemplate` و annotationهای cache (`@Cacheable`, `@CachePut`, `@CacheEvict`) برای Redis. این‌ها API یکنواخت Spring Data را به دیتابیس‌های مختلف می‌آورند.

**نکات کلیدی:**

- `@Cacheable` با AOP کار می‌کند → self-invocation همان مشکل را دارد.
- کلید cache را با دقت تعریف کنید (`key = "#id"`).

---

## 🎯 سوالات مصاحبه

### سوال ۱: N+1 problem چیست و چطور حل می‌شود؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

N+1 وقتی رخ می‌دهد که یک query اصلی N رکورد برمی‌گرداند و سپس برای دسترسی به association هر رکورد (که LAZY است) یک query جداگانه زده می‌شود — مجموعاً 1+N query به‌جای یک یا دو. این در dev با داده‌ی کم دیده نمی‌شود اما در production با حجم بالا latency را منفجر می‌کند.

راه‌حل‌ها بر اساس سناریو: `JOIN FETCH` در JPQL برای بارگذاری یکجا؛ `@EntityGraph` برای کنترل declarative؛ batch fetching (`hibernate.default_batch_fetch_size`) که N+1 را به N/batch_size+1 کاهش می‌دهد؛ و DTO projection که فقط داده‌ی لازم را با یک query می‌گیرد. برای pagination، `JOIN FETCH` روی collection خطرناک است (صفحه‌بندی در حافظه)، پس batch fetching یا دو query بهتر است.

**کد توضیحی:**

```java
@EntityGraph(attributePaths = {"items"})
List<Order> findByCustomerId(Long customerId);
```

**نکته مصاحبه:**

تمایز Senior: دانستن مشکل `JOIN FETCH` با pagination و معرفی batch fetching. Follow-up: «چطور N+1 را تشخیص می‌دهی؟» (لاگ SQL، Hibernate statistics، ابزار مثل p6spy).

---

### سوال ۲: تفاوت `REQUIRED` و `REQUIRES_NEW` چیست؟ یک سناریوی واقعی بده.

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

`REQUIRED` (پیش‌فرض) به تراکنش جاری می‌پیوندد؛ اگر متد بیرونی rollback شود، کار این متد هم rollback می‌شود (همه در یک تراکنش‌اند). `REQUIRES_NEW` تراکنش جدید و کاملاً مستقل می‌سازد و تراکنش بیرونی را معلق می‌کند؛ commit/rollback این مستقل از بیرونی است.

سناریوی کلاسیک: audit logging. می‌خواهید حتی اگر تراکنش اصلی (مثلاً پرداخت) شکست بخورد و rollback شود، رکورد audit «تلاش برای پرداخت» باقی بماند. با `REQUIRES_NEW` روی متد audit، آن لاگ مستقل commit می‌شود. خطر: `REQUIRES_NEW` یک connection دوم از pool می‌گیرد؛ استفاده‌ی بی‌رویه می‌تواند pool را تمام کند و حتی self-deadlock بسازد.

**نکته مصاحبه:**

Lead به مصرف connection و خطر pool exhaustion اشاره می‌کند. Follow-up: «اگر تراکنش بیرونی rollback شود، REQUIRES_NEW چه می‌شود؟» (commit‌شده می‌ماند).

---

### سوال ۳: isolation levels را توضیح بده و هر کدام چه anomaly‌ای را حل می‌کند.

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

- `READ_UNCOMMITTED`: می‌تواند dirty read ببیند (خواندن داده‌ی commit‌نشده). به‌ندرت استفاده می‌شود.
- `READ_COMMITTED` (پیش‌فرض اکثر DBها): فقط داده‌ی commit‌شده دیده می‌شود؛ dirty read حذف می‌شود اما non-repeatable read ممکن است (همان query دوبار، نتیجه‌ی متفاوت).
- `REPEATABLE_READ`: همان ردیف در طول تراکنش ثابت می‌ماند؛ non-repeatable read حذف می‌شود اما phantom read (ردیف‌های جدید) ممکن است (در برخی DBها مثل MySQL InnoDB با gap lock حل شده).
- `SERIALIZABLE`: کامل‌ترین؛ همه‌ی anomalyها حذف اما کمترین concurrency و احتمال بالای deadlock/serialization failure.

انتخاب سطح، trade-off بین consistency و throughput است.

**نکته مصاحبه:**

Senior سه anomaly (dirty, non-repeatable, phantom) را به سطوح map می‌کند. Follow-up: «PostgreSQL با MVCC چطور این‌ها را پیاده می‌کند؟»

---

### سوال ۴: optimistic در برابر pessimistic locking — کِی کدام؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

optimistic (با `@Version`) فرض تداخل نادر دارد: قفل نمی‌گیرد، فقط هنگام commit چک می‌کند version عوض نشده باشد؛ اگر شده، استثنا و باید retry کنید. مناسب read-heavy با تداخل کم، scalable چون lock نگه نمی‌دارد. pessimistic ردیف را قفل می‌کند (`SELECT FOR UPDATE`) تا تداخل اصلاً رخ ندهد؛ مناسب وقتی تداخل زیاد است یا هزینه‌ی retry بالاست (مثل کم کردن موجودی انبار در فروش لحظه‌ای)، اما concurrency را کاهش می‌دهد و خطر deadlock دارد.

**کد توضیحی:**

```java
// optimistic با retry
@Retryable(retryFor = OptimisticLockingFailureException.class, maxAttempts = 3)
@Transactional
public void updateStock(Long id, int delta) { /* ... */ }
```

**نکته مصاحبه:**

Senior به نیاز retry برای optimistic و خطر deadlock برای pessimistic اشاره می‌کند.

---

### سوال ۵: چرا `@Transactional` گاهی rollback نمی‌کند؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

دلایل رایج: (۱) استثنا یک **checked exception** است و `@Transactional` پیش‌فرض فقط روی unchecked rollback می‌کند — باید `rollbackFor` بگذارید. (۲) استثنا داخل متد catch و swallow شده، پس به proxy نمی‌رسد. (۳) **self-invocation**: متد transactional از همان کلاس صدا زده شده و proxy دور زده شده. (۴) متد `private` یا `final` است (proxy نمی‌تواند intercept کند). (۵) تراکنش روی متدی است که در thread دیگری اجرا می‌شود (`@Async`). تشخیص با لاگ تراکنش و آگاهی از این موارد.

**نکته مصاحبه:**

Senior چندین علت را می‌داند نه فقط یکی. Follow-up: «چرا checked exception پیش‌فرض rollback نمی‌کند؟» (تصمیم تاریخی سازگار با EJB).

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: انتظار rollback برای checked exception

```java
// ❌ rollback نمی‌شود
@Transactional
public void process() throws IOException { throw new IOException(); }
```

```java
// ✅
@Transactional(rollbackFor = IOException.class)
public void process() throws IOException { throw new IOException(); }
```

**توضیح:** پیش‌فرض فقط unchecked rollback می‌شود.

---

### اشتباه ۲: N+1 با LAZY و پیمایش

```java
// ❌ N+1
orders.forEach(o -> System.out.println(o.getItems().size()));
```

```java
// ✅
@Query("SELECT DISTINCT o FROM Order o JOIN FETCH o.items")
List<Order> findAllWithItems();
```

**توضیح:** هر دسترسی LAZY یک query می‌زند.

---

### اشتباه ۳: `JOIN FETCH` با pagination

```java
// ❌ هشدار HHH000104: صفحه‌بندی در حافظه
@Query("SELECT o FROM Order o JOIN FETCH o.items")
Page<Order> findAll(Pageable p);
```

```java
// ✅ batch fetching
// application.yml: spring.jpa.properties.hibernate.default_batch_fetch_size: 50
@EntityGraph(attributePaths = "items")
Page<Order> findAll(Pageable p);
```

**توضیح:** `JOIN FETCH` روی collection با pagination، صفحه‌بندی را به حافظه می‌برد.

---

### اشتباه ۴: استفاده‌ی بیش از حد `REQUIRES_NEW`

```java
// ❌ هر فراخوانی یک connection دوم → pool exhaustion
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void everyCall() {}
```

```java
// ✅ فقط برای audit/logging واقعاً مستقل
```

**توضیح:** `REQUIRES_NEW` connection دوم می‌گیرد و pool را تمام می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- transaction propagation با **Spring Core AOP/proxy** و مشکل self-invocation گره خورده.
- N+1 با **DB indexing/query optimization** (فصل DB) مرتبط است.
- locking با **PostgreSQL MVCC** و **concurrency** ارتباط دارد.
- `@Cacheable` با **Redis/Caching** و الگوهای cache.
- DTO projection با **records** (Java 17) و **API design**.
