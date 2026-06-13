# Elasticsearch — مفاهیم پایه

> Elasticsearch موتور جستجو و تحلیل توزیع‌شده مبتنی بر Lucene است.

---

## 📖 مفاهیم

### مفاهیم پایه

**توضیح:**

- **Index:** مشابه table (مجموعه‌ی documentها).
- **Document:** مشابه row، یک JSON.
- **Shard:** بخش‌های یک index (primary + replica) — برای توزیع و HA.
- **Node:** یک سرور Elasticsearch.
- **Cluster:** مجموعه‌ی nodeها.
- **Mapping:** schema (می‌تواند dynamic باشد) که type فیلدها را تعریف می‌کند.
- **Analyzer:** tokenization + normalization متن برای جستجوی full-text.

ES برای full-text search، log analytics، و aggregation طراحی شده — نه به‌عنوان source of truth اصلی (معمولاً داده از DB اصلی sync می‌شود).

**چرا مهم است:**

ES برای search پیشرفته، relevance scoring، و تحلیل log در مقیاس بالا. درک shard و analyzer برای performance و درستی نتایج لازم است.

**نکات کلیدی:**

- ES معمولاً source of truth نیست؛ از DB sync می‌شود (با CDC).
- تعداد shard بعد از ساخت index ثابت است (با دقت انتخاب کنید).
- analyzer روی نحوه‌ی index و search متن اثر می‌گذارد.

---

### Text vs Keyword & Analyzer

**توضیح:**

تفاوت کلیدی mapping: **text** (تحلیل می‌شود، tokenize، برای full-text search — `match`) در برابر **keyword** (تحلیل نمی‌شود، exact، برای فیلتر/مرتب‌سازی/aggregation — `term`). **Analyzer** متن را به token تبدیل می‌کند: tokenizer + filter (lowercase، stop words، stemming). یک فیلد می‌تواند هم text و هم keyword (`field` و `field.keyword`) باشد.

**نکات کلیدی:**

- `text` برای search، `keyword` برای exact/aggregation/sort.
- `term` query روی text نتیجه‌ی غیرمنتظره می‌دهد (به‌خاطر analysis).

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت text و keyword چیست؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

`text` فیلد تحلیل (analyze) می‌شود: به tokenها شکسته، lowercase، و گاهی stem می‌شود — برای **full-text search** با `match` که relevance می‌دهد. `keyword` تحلیل نمی‌شود و به‌صورت یک مقدار کامل ذخیره می‌شود — برای **exact match** (`term`)، مرتب‌سازی، و aggregation. تله‌ی رایج: استفاده از `term` روی فیلد `text` نتیجه نمی‌دهد چون مقدار query با token تحلیل‌شده مطابقت نمی‌کند (مثلاً `term: "New York"` روی text که به `new`, `york` شکسته شده). راه‌حل: برای فیلدی که هم search و هم exact می‌خواهید، multi-field mapping (`field` به‌عنوان text + `field.keyword`). aggregation و sort فقط روی keyword (یا fielddata) کار می‌کنند.

**نکته مصاحبه:**

Senior به تله‌ی term روی text و multi-field اشاره می‌کند.

---

### سوال ۲: ES کِی به‌جای DB یا به‌علاوه‌ی آن؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

ES معمولاً **به‌علاوه‌ی** DB اصلی استفاده می‌شود نه به‌جای آن. DB (PostgreSQL) source of truth با transaction و consistency است؛ ES برای قابلیت‌هایی که DB ضعیف است: full-text search پیشرفته با relevance، fuzzy/typo tolerance، faceted search، autocomplete، و log/metric analytics در مقیاس بالا. الگو: داده در DB نوشته می‌شود، سپس به ES sync می‌شود (با CDC/Debezium، Change Streams، یا application dual-write با Outbox). نباید ES را source of truth کرد چون durability/consistency تضمین DB را ندارد و reindex ممکن لازم شود. trade-off: پیچیدگی sync و eventual consistency بین DB و ES.

**نکته مصاحبه:**

Lead به الگوی sync (CDC) و ES نبودن source of truth اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: term روی فیلد text

```json
// ❌ نتیجه نمی‌دهد (text تحلیل شده)
{ "term": { "title": "New York" } }
```

```json
// ✅
{ "match": { "title": "New York" } }   // full-text
{ "term": { "title.keyword": "New York" } } // exact
```

**توضیح:** term با token تحلیل‌شده مطابقت نمی‌کند.

---

### اشتباه ۲: ES به‌عنوان source of truth

```text
❌ نوشتن مستقیم همه‌چیز فقط در ES
✅ DB source of truth، ES برای search (sync با CDC)
```

**توضیح:** ES تضمین durability/consistency یک DB را ندارد.

---

## 🔗 ارتباط با سایر مفاهیم

- ES با **PostgreSQL full-text (14.2)** (مقایسه) و **MongoDB Atlas Search (4.5)**.
- sync با **Kafka/CDC/Debezium (8.1)** و **Change Streams**.
- shard با **sharding (4.4)** و **System Design scaling**.
