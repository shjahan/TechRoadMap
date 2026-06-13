# Elasticsearch — CRUD و Search

> Query DSL قلب جستجو در ES است. درک bool query و تفاوت query/filter context مهم است.

---

## 📖 مفاهیم

### CRUD و Query DSL

**توضیح:**

index کردن document با `PUT /index/_doc/id`. جستجو با Query DSL (JSON). **bool query** ترکیب شرط‌ها: `must` (AND، روی score اثر دارد)، `should` (OR، score boost)، `must_not` (NOT)، `filter` (AND، بدون score، cacheable). تفاوت کلیدی **query context** (relevance score محاسبه می‌شود) در برابر **filter context** (فقط yes/no، سریع‌تر و cache می‌شود).

**مثال کد:**

```json
GET /products/_search
{
  "query": {
    "bool": {
      "must": [{ "match": { "name": "iphone" } }],       // relevance
      "filter": [{ "range": { "price": { "gte": 500, "lte": 2000 } } }], // بدون score، cache
      "must_not": [{ "term": { "discontinued": true } }]
    }
  },
  "aggs": {
    "by_category": { "terms": { "field": "category.keyword" } },
    "avg_price": { "avg": { "field": "price" } }
  }
}
```

**نکات کلیدی:**

- شرط‌های exact/range را در `filter` بگذارید (cacheable، سریع‌تر، بدون score).
- `must` برای full-text که relevance مهم است.
- aggregation روی keyword (نه text).

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت query context و filter context؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

در **query context** (مثل `must`, `should`)، ES علاوه بر تطابق، یک **relevance score** (`_score`) محاسبه می‌کند که چقدر document با query مرتبط است — برای full-text که می‌خواهید مرتبط‌ترین‌ها بالا باشند. در **filter context** (مثل `filter`, `must_not`)، فقط yes/no مطرح است (آیا match می‌کند) بدون محاسبه‌ی score — سریع‌تر و **cacheable** (ES نتیجه‌ی filter را cache می‌کند). best practice: شرط‌های exact/range/boolean (مثل price range، status، date) را در filter context بگذارید (سریع‌تر، cache)، و فقط full-text relevance را در query context. این performance را به‌شدت بهبود می‌دهد.

**نکته مصاحبه:**

Senior به cacheable بودن filter و قرار دادن range/exact در filter اشاره می‌کند.

---

### سوال ۲: relevance scoring چطور کار می‌کند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

ES از الگوریتم **BM25** (پیش‌فرض، بهبود TF-IDF) برای score استفاده می‌کند. عوامل اصلی: **TF** (term frequency — هرچه term بیشتر در document، مرتبط‌تر، اما با saturation)، **IDF** (inverse document frequency — term نادر در کل index ارزش بیشتری دارد)، و **field length normalization** (term در فیلد کوتاه مرتبط‌تر از فیلد بلند). می‌توان score را با `boost`، `function_score`، یا rescoring تنظیم کرد. درک scoring برای tuning نتایج جستجو (مثلاً اولویت title بر body) لازم است. برای exact/filter که relevance مهم نیست، filter context استفاده کنید تا score محاسبه نشود.

**نکته مصاحبه:**

Senior BM25 و TF/IDF را می‌شناسد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: range/exact در must به‌جای filter

```json
// ❌ score بی‌فایده محاسبه می‌شود، بدون cache
"must": [{ "range": { "price": { "gte": 100 } } }]
```

```json
// ✅
"filter": [{ "range": { "price": { "gte": 100 } } }]
```

**توضیح:** range/exact در filter سریع‌تر و cacheable است.

---

### اشتباه ۲: aggregation روی فیلد text

```json
// ❌ خطا یا fielddata گران
"terms": { "field": "category" }  // text
```

```json
// ✅
"terms": { "field": "category.keyword" }
```

**توضیح:** aggregation/sort روی keyword نه text.

---

## 🔗 ارتباط با سایر مفاهیم

- Query DSL با **Spring Data Elasticsearch (17.3)**.
- filter cache با **caching (9)**.
- aggregation با **MongoDB aggregation (4.2)** (مقایسه).
