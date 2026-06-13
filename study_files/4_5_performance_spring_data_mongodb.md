# MongoDB Performance & Spring Data MongoDB

> یکپارچگی MongoDB با Spring و ابزارهای performance/real-time (Change Streams، Atlas Search).

---

## 📖 مفاهیم

### Spring Data MongoDB

**توضیح:**

دو ابزار اصلی: `MongoRepository` (interface‌محور، مثل JpaRepository با query derivation) برای CRUD و queryهای ساده، و `MongoTemplate` برای queryهای پیچیده، update جزئی، و aggregation با کنترل کامل. `@Document` کلاس را به collection map می‌کند، `@Id` و `@Field` فیلدها را.

برای reactive، `ReactiveMongoRepository` و `ReactiveMongoTemplate` (با WebFlux). برای aggregation، `Aggregation`/`TypedAggregation` API.

**مثال کد:**

```java
@Document(collection = "products")
public record Product(@Id String id, String name,
                      @Field("cat") String category, double price) {}

public interface ProductRepository extends MongoRepository<Product, String> {
    List<Product> findByCategory(String category);
    List<Product> findByPriceBetween(double min, double max);
}

// MongoTemplate برای aggregation
Aggregation agg = Aggregation.newAggregation(
    Aggregation.match(Criteria.where("category").is("electronics")),
    Aggregation.group("category").sum("price").as("total"),
    Aggregation.sort(Sort.Direction.DESC, "total"));
AggregationResults<CategoryTotal> results =
    mongoTemplate.aggregate(agg, "products", CategoryTotal.class);
```

**نکات کلیدی:**

- `MongoRepository` برای ساده، `MongoTemplate` برای پیچیده/aggregation.
- `@Indexed` برای تعریف index در سطح کد (اما در production index را explicit مدیریت کنید).

---

### Change Streams

**توضیح:**

Change Streams امکان دریافت real-time تغییرات (insert/update/delete) را می‌دهد بدون polling. بر اساس oplog کار می‌کند (نیاز به replica set). جایگزین مدرن برای polling دوره‌ای یا trigger. کاربرد: sync با سیستم دیگر (مثل Elasticsearch)، notification real-time، cache invalidation، و CDC.

**مثال کد:**

```java
// با Spring Data reactive
Flux<ChangeStreamEvent<Product>> changes = reactiveMongoTemplate
    .changeStream(Product.class)
    .watchCollection("products")
    .filter(Criteria.where("operationType").is("update"))
    .listen();
changes.subscribe(event -> updateSearchIndex(event.getBody()));
```

**نکات کلیدی:**

- Change Streams به replica set نیاز دارد (oplog).
- resumable است (با resume token پس از قطع ادامه می‌دهد).
- جایگزین polling و راه‌حل CDC داخلی MongoDB.

---

### Atlas Search & Vector Search

**توضیح:**

**Atlas Search** full-text search مبتنی بر Lucene داخل MongoDB Atlas — بدون نیاز به Elasticsearch جداگانه. **Vector Search** (MongoDB 7/8) برای semantic search و AI/RAG با embedding. **Queryable Encryption** برای query روی داده‌ی رمزشده.

**نکات کلیدی:**

- Atlas Search می‌تواند نیاز به Elasticsearch جدا را در برخی موارد حذف کند.
- Vector Search برای کاربردهای AI/LLM.

---

## 🎯 سوالات مصاحبه

### سوال ۱: `MongoRepository` در برابر `MongoTemplate` — کِی کدام؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

`MongoRepository` برای CRUD و query‌های ساده با query derivation (`findByX`) عالی است — کم‌کد و خوانا. اما برای aggregation pipeline، update جزئی (مثلاً فقط `$inc` یک فیلد بدون load کل document)، query پویا/شرطی، و کنترل دقیق، `MongoTemplate` لازم است. در عمل اکثر پروژه‌ها هر دو را استفاده می‌کنند: repository برای ساده، template برای پیچیده. نکته‌ی performance: استفاده از `save()` در repository کل document را بازنویسی می‌کند؛ برای update یک فیلد، `MongoTemplate.updateFirst` با `$set` کارآمدتر است.

**نکته مصاحبه:**

Senior به مشکل `save()` کل document در برابر partial update اشاره می‌کند.

---

### سوال ۲: Change Streams چه مشکلی را حل می‌کند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

مشکل: برای واکنش به تغییر داده (sync با سیستم دیگر، invalidate cache، notification)، روش سنتی polling دوره‌ای بود که هم latency دارد و هم بار بی‌فایده. Change Streams یک stream real-time از تغییرات می‌دهد که اپ subscribe می‌کند و فقط هنگام تغییر واقعی رویداد می‌گیرد. مزایا: real-time، کارآمد، resumable (با resume token پس از crash ادامه می‌دهد). کاربرد کلاسیک: CDC برای sync با Elasticsearch، یا الگوی Outbox. به replica set نیاز دارد چون بر oplog بنا شده.

**نکته مصاحبه:**

Senior به resume token و کاربرد CDC اشاره می‌کند.

---

### سوال ۳: چطور N+1 معادل در MongoDB رخ می‌دهد؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

اگر از referencing استفاده کنید و برای هر document اصلی یک query جدا برای document مرتبط بزنید، معادل N+1 رخ می‌دهد (مثلاً برای ۱۰۰ order، ۱۰۰ query جدا برای user هر کدام). راه‌حل‌ها: `$lookup` در aggregation برای join یکجا، batch کردن queryها (`$in` با لیست idها)، یا بهتر، denormalization (embedding یا Extended Reference) تا اصلاً نیاز به query دوم نباشد. فلسفه‌ی MongoDB این است که با مدل‌سازی درست از این مشکل جلوگیری کنید.

**نکته مصاحبه:**

Senior به denormalization به‌عنوان راه‌حل اصلی اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: `save()` برای update یک فیلد

```java
// ❌ کل document را load و بازنویسی می‌کند
Product p = repo.findById(id).get();
p.setPrice(newPrice);
repo.save(p);
```

```java
// ✅ partial update
mongoTemplate.updateFirst(
    Query.query(Criteria.where("_id").is(id)),
    Update.update("price", newPrice), Product.class);
```

**توضیح:** `save` کل document را بازنویسی و race condition می‌سازد؛ `$set` فقط فیلد لازم.

---

### اشتباه ۲: polling به‌جای Change Streams

```java
// ❌ هر 5 ثانیه کل collection را چک می‌کند
@Scheduled(fixedRate = 5000)
void poll() { /* find changed since... */ }
```

```java
// ✅ Change Streams real-time
```

**توضیح:** polling latency و بار اضافه دارد.

---

### اشتباه ۳: استفاده از blocking MongoTemplate در WebFlux

```java
// ❌ blocking در reactive stack
mongoTemplate.findById(id, Product.class);
```

```java
// ✅
reactiveMongoTemplate.findById(id, Product.class); // Mono
```

**توضیح:** در WebFlux از reactive template استفاده کنید.

---

## 🔗 ارتباط با سایر مفاهیم

- Spring Data MongoDB با **Spring Data JPA** (الگوی repository مشترک) و **WebFlux** (reactive).
- Change Streams با **Kafka/CDC (Debezium)** و **Event-Driven Architecture**.
- Atlas Search با **Elasticsearch** (فصل 17).
- partial update با **optimistic locking** و concurrency.
