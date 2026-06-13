# Spring Data Elasticsearch

> یکپارچگی ES با Spring برای جستجو در اپ‌های Java.

---

## 📖 مفاهیم

### مفاهیم اصلی

**توضیح:**

`@Document(indexName=...)` کلاس را به index map می‌کند. `@Field(type=...)` نوع و analyzer فیلد. `ElasticsearchRepository` برای CRUD و query derivation. برای queryهای پیچیده، `ElasticsearchOperations`/`NativeQuery`.

**مثال کد:**

```java
@Document(indexName = "products")
public class Product {
    @Id private String id;
    @Field(type = FieldType.Text, analyzer = "standard") private String name;
    @Field(type = FieldType.Keyword) private String category;
    @Field(type = FieldType.Double) private Double price;
}

public interface ProductRepository extends ElasticsearchRepository<Product, String> {
    List<Product> findByCategory(String category);
    List<Product> findByPriceBetween(Double min, Double max);
}

// query پیچیده
NativeQuery query = NativeQuery.builder()
    .withQuery(q -> q.match(m -> m.field("name").query("iphone")))
    .build();
SearchHits<Product> hits = operations.search(query, Product.class);
```

**نکات کلیدی:**

- `@Field(type=Text/Keyword)` بر اساس استفاده (search یا exact).
- repository برای ساده؛ `NativeQuery`/`ElasticsearchOperations` برای پیچیده.

---

## 🎯 سوالات مصاحبه

### سوال ۱: داده را بین DB و ES چطور sync نگه می‌داری؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

چند روش با trade-off: (۱) **dual write** (اپ همزمان در DB و ES می‌نویسد) — ساده اما غیراتمیک (اگر یکی fail شود ناسازگاری)، پس باید با Outbox همراه شود. (۲) **CDC** (Change Data Capture با Debezium که از WAL دیتابیس تغییرات را به Kafka و سپس ES می‌فرستد) — قابل‌اعتماد، decoupled، اما زیرساخت بیشتر. (۳) **Outbox pattern** (نوشتن رویداد در جدول outbox در همان transaction، سپس انتشار به ES). (۴) **scheduled reindex** برای داده‌ی کم‌تغییر. بهترین برای production: CDC یا Outbox که اتمیک بودن و قابلیت‌اعتماد می‌دهند. نکته: sync همیشه eventual consistency است (ES کمی عقب از DB)، که باید در UX در نظر گرفت.

**نکته مصاحبه:**

Lead به CDC/Outbox و eventual consistency اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: dual write بدون Outbox

```text
❌ نوشتن همزمان DB و ES غیراتمیک → ناسازگاری
✅ Outbox/CDC
```

**توضیح:** dual write می‌تواند یکی موفق و دیگری ناموفق شود.

---

### اشتباه ۲: blocking ES call در WebFlux

```java
// ❌
repository.findByCategory(c); // blocking
```

```java
// ✅ reactive operations
ReactiveElasticsearchOperations
```

**توضیح:** در reactive stack از reactive ES client استفاده کنید.

---

## 🔗 ارتباط با سایر مفاهیم

- Spring Data ES با **Spring Data (2.4)** الگوی مشترک.
- sync با **CDC/Debezium (8.1)** و **Outbox (6.1)**.
- mapping با **text/keyword (17.1)**.
