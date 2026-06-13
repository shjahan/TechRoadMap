# PostgreSQL — JSONB، MVCC، Replication، Performance

> PostgreSQL محبوب‌ترین RDBMS مدرن است و در هر مصاحبه پرسیده می‌شود. MVCC و JSONB موضوعات کلیدی Senior هستند.

---

## 📖 مفاهیم

### ویژگی‌های خاص — JSONB، Arrays، UUID

**توضیح:**

PostgreSQL فراتر از SQL استاندارد امکانات قدرتمندی دارد:

- **JSONB:** ذخیره‌ی JSON به‌صورت باینری با امکان index (GIN) و query کارآمد. برخلاف `JSON` (متن خام)، JSONB parse‌شده ذخیره می‌شود — query سریع‌تر، insert کمی کندتر. برای داده‌ی نیمه‌ساختاریافته یا فیلدهای پویا.
- **Arrays:** ستون آرایه‌ای (`integer[]`, `text[]`).
- **UUID:** با `gen_random_uuid()`؛ برای کلید توزیع‌شده.
- **Full-text search:** `tsvector`/`tsquery`.
- **Row-Level Security (RLS):** کنترل دسترسی در سطح ردیف.
- **Table Partitioning:** Range/List/Hash.
- **LISTEN/NOTIFY:** رویداد real-time.

**چرا مهم است:**

JSONB انعطاف NoSQL را با قدرت SQL ترکیب می‌کند و اغلب نیاز به دیتابیس جداگانه را حذف می‌کند. اما سوءاستفاده (همه‌چیز در JSONB) طراحی relational را خراب می‌کند.

**مثال کد:**

```sql
CREATE TABLE products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    metadata JSONB
);
CREATE INDEX idx_metadata ON products USING GIN (metadata); -- index روی JSONB

-- query داخل JSONB
SELECT * FROM products WHERE metadata @> '{"category": "electronics"}'; -- containment
SELECT metadata->>'name' FROM products WHERE metadata ? 'name';          -- key exists
SELECT * FROM products WHERE metadata #>> '{specs,ram}' = '16GB';        -- nested path

-- update
UPDATE products SET metadata = metadata || '{"discount": 10}'; -- merge
```

**نکات کلیدی:**

- JSONB با GIN index برای query کارآمد؛ `@>` (containment) از index استفاده می‌کند.
- JSONB برای فیلدهای پویا؛ داده‌ی structured را در ستون عادی نگه دارید.
- `->` مقدار JSON، `->>` مقدار text برمی‌گرداند.

---

### MVCC (Multi-Version Concurrency Control)

**توضیح:**

قلب concurrency در PostgreSQL. به‌جای قفل کردن برای خواندن، PostgreSQL **چند نسخه** از هر ردیف نگه می‌دارد. هر تراکنش یک snapshot می‌بیند: خواننده‌ها نسخه‌ای را می‌بینند که هنگام شروع تراکنش‌شان معتبر بوده، بدون بلاک کردن نویسنده‌ها و برعکس («readers don't block writers, writers don't block readers»).

پیامد: `UPDATE` در واقع نسخه‌ی جدید می‌سازد و قدیمی را به‌عنوان dead tuple علامت می‌زند. این dead tupleها باید با **VACUUM** (و autovacuum) پاک شوند وگرنه **bloat** (تورم جدول) رخ می‌دهد و performance افت می‌کند.

**چرا مهم است:**

درک MVCC برای فهم isolation levels، bloat، و tuning autovacuum ضروری است. bloat یکی از علل رایج کندی تدریجی است.

**مثال کد:**

```sql
-- بررسی dead tuples و bloat
SELECT relname, n_live_tup, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- قفل صریح برای جلوگیری از تداخل
SELECT * FROM accounts WHERE id = 1 FOR UPDATE; -- ردیف را قفل می‌کند
```

**نکات کلیدی:**

- UPDATE نسخه‌ی جدید می‌سازد → dead tuple → نیاز VACUUM.
- خواننده و نویسنده هم را بلاک نمی‌کنند.
- autovacuum را برای جداول پرتغییر tune کنید.

---

### Isolation Levels در PostgreSQL

**توضیح:**

PostgreSQL با MVCC این سطوح را پیاده می‌کند: `READ COMMITTED` (پیش‌فرض، هر statement snapshot تازه می‌بیند)، `REPEATABLE READ` (snapshot ثابت در کل تراکنش، از non-repeatable و phantom جلوگیری می‌کند)، `SERIALIZABLE` (با Serializable Snapshot Isolation — تشخیص تداخل و abort یکی از تراکنش‌ها). نکته‌ی PG: `READ UNCOMMITTED` عملاً مثل `READ COMMITTED` رفتار می‌کند (dirty read هرگز رخ نمی‌دهد).

**نکات کلیدی:**

- در SERIALIZABLE باید آماده‌ی `serialization_failure` و retry باشید.
- REPEATABLE READ در PG قوی‌تر از استاندارد است (phantom را هم تا حد زیادی پوشش می‌دهد).

---

### Deadlocks & Locks

**توضیح:**

deadlock وقتی رخ می‌دهد که دو تراکنش هر کدام منتظر قفلی هستند که دیگری نگه داشته. PostgreSQL آن را تشخیص می‌دهد و یکی را abort می‌کند. پیشگیری: همیشه منابع را به ترتیب یکسان قفل کنید. `SELECT FOR UPDATE` (قفل نوشتن ردیف)، `SELECT FOR SHARE` (قفل خواندن). **Advisory Locks** قفل‌های application-level هستند که به ردیف خاصی گره نمی‌خورند (برای هماهنگی منطقی مثل اجرای یک job).

**مثال کد:**

```sql
-- advisory lock برای تضمین اجرای تک‌نمونه‌ای یک job
SELECT pg_try_advisory_lock(12345); -- non-blocking، true اگر گرفت
-- ... کار ...
SELECT pg_advisory_unlock(12345);
```

**نکات کلیدی:**

- برای پیشگیری از deadlock، ترتیب قفل‌گیری را ثابت نگه دارید.
- advisory lock برای هماهنگی توزیع‌شده‌ی سبک (مثل scheduler تک‌نمونه).

---

### Replication & HA

**توضیح:**

- **Streaming Replication:** primary تغییرات WAL را به replicaها استریم می‌کند (physical). معمولاً async (احتمال data loss کم هنگام failover) یا sync (بدون loss اما latency).
- **Logical Replication:** بر اساس تغییر منطقی (per-table)، برای migration و CDC.
- **Patroni:** ابزار automatic failover.
- backup: `pg_dump` (logical)، `pgBackRest` (physical، incremental، PITR).

**نکات کلیدی:**

- replica برای read scaling و HA؛ اما replication lag یعنی read از replica ممکن است stale باشد.
- برای failover خودکار به ابزار (Patroni) نیاز است.

---

### Performance Tools

**توضیح:**

`pg_stat_statements` (آمار query پرتکرار/کند)، `pg_stat_activity` (connectionهای فعال و قفل‌ها)، تنظیمات حافظه: `shared_buffers` (~25% RAM)، `work_mem` (برای sort/hash هر operation)، `effective_cache_size`، `max_connections`. autovacuum tuning برای جلوگیری از bloat.

**مثال کد:**

```sql
-- کندترین queryها
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;

-- connectionهای طولانی/گیرکرده
SELECT pid, state, wait_event_type, now() - query_start AS duration, query
FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC;
```

**نکات کلیدی:**

- `pg_stat_statements` اولین ابزار برای یافتن query مشکل‌دار.
- `work_mem` بزرگ × تعداد connection می‌تواند RAM را تمام کند.

---

## 🎯 سوالات مصاحبه

### سوال ۱: MVCC چطور کار می‌کند و چه پیامدی دارد؟

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

MVCC به‌جای قفل برای خواندن، چند نسخه از هر ردیف نگه می‌دارد. هر تراکنش یک snapshot سازگار می‌بیند بر اساس transaction id. این یعنی خواننده‌ها نویسنده‌ها را بلاک نمی‌کنند و برعکس — concurrency بالا. پیامد مهم: `UPDATE`/`DELETE` ردیف قدیمی را فیزیکی حذف نمی‌کند بلکه نسخه‌ی جدید می‌سازد و قدیمی را dead tuple می‌کند. این dead tupleها فضا می‌گیرند و باید با VACUUM پاک شوند؛ وگرنه table/index bloat رخ می‌دهد و کوئری‌ها به‌تدریج کند می‌شوند. autovacuum این کار را خودکار می‌کند اما برای جداول پرتغییر باید tune شود.

**نکته مصاحبه:**

تمایز Lead: ربط دادن MVCC به bloat و VACUUM و autovacuum tuning. Follow-up: «transaction id wraparound چیست؟» (خطر جدی اگر VACUUM عقب بماند).

---

### سوال ۲: کِی JSONB و کِی ستون relational؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

JSONB برای داده‌ی **نیمه‌ساختاریافته، پویا، یا اسپارس** مناسب است: فیلدهایی که schema ثابت ندارند، metadata متغیر، یا attributeهای محصول که بین دسته‌ها فرق می‌کنند. مزیت: انعطاف بدون migration، query با GIN index. اما برای داده‌ای که structured است و در query/join/constraint استفاده می‌شود، ستون relational بهتر است: type safety، constraint، index کارآمدتر، و خوانایی. ضدالگو: ریختن همه‌چیز در یک ستون JSONB و از دست دادن قدرت relational. قاعده: اگر روی فیلد join/constraint/aggregate می‌کنید، ستون عادی؛ اگر فقط ذخیره و گاهی query، JSONB.

**نکته مصاحبه:**

Senior تعادل را می‌فهمد و ضدالگوی «همه‌چیز JSONB» را می‌شناسد. Follow-up: «چطور روی یک کلید JSONB index می‌زنی؟» (GIN یا expression index روی `(metadata->>'key')`).

---

### سوال ۳: تفaوت streaming و logical replication چیست؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

streaming (physical) replication کل WAL (تغییرات سطح بایت دیسک) را به replica می‌فرستد؛ replica یک کپی بایت‌به‌بایت است، فقط read، و باید همان نسخه‌ی PG باشد — برای HA و read scaling عالی. logical replication تغییرات را در سطح منطقی (INSERT/UPDATE/DELETE روی جداول مشخص) منتشر می‌کند؛ انعطاف بیشتر (انتخاب جدول، بین نسخه‌های مختلف، subscriber قابل‌نوشتن) — برای migration، CDC، و ادغام داده. logical کندتر و پیچیده‌تر است.

**نکته مصاحبه:**

Lead به موارد استفاده (HA در برابر CDC/migration) اشاره می‌کند.

---

### سوال ۴: deadlock را چطور تشخیص و پیشگیری می‌کنی؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

تشخیص: PostgreSQL خودکار deadlock را detect و یکی را با خطای `deadlock detected` abort می‌کند؛ در لاگ ثبت می‌شود و می‌توان از `pg_locks` + `pg_stat_activity` تحلیل کرد. پیشگیری: (۱) همیشه منابع را به ترتیب ثابت قفل کنید (مثلاً همیشه به ترتیب id صعودی) — رایج‌ترین راه‌حل. (۲) تراکنش‌ها را کوتاه نگه دارید. (۳) از قفل‌های گسترده بپرهیزید. (۴) در صورت بروز، retry با backoff. (۵) سطح isolation و الگوی دسترسی را بازبینی کنید.

**نکته مصاحبه:**

Senior به «ترتیب ثابت قفل‌گیری» به‌عنوان راه‌حل اصلی اشاره می‌کند.

---

### سوال ۵: VACUUM چیست و چرا مهم است؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

به‌خاطر MVCC، UPDATE/DELETE نسخه‌های قدیمی (dead tuples) باقی می‌گذارند. VACUUM این فضا را برای استفاده‌ی مجدد آزاد می‌کند، آمار را به‌روز می‌کند (با ANALYZE)، و از transaction id wraparound جلوگیری می‌کند. بدون VACUUM کافی: bloat (جدول و index بزرگ و کند می‌شوند) و در بدترین حالت wraparound که می‌تواند DB را متوقف کند. `VACUUM` فضا را برای reuse آزاد می‌کند اما به OS برنمی‌گرداند؛ `VACUUM FULL` فضا را به OS برمی‌گرداند ولی جدول را قفل می‌کند (در production خطرناک). autovacuum خودکار اجرا می‌شود اما برای جداول پرترافیک باید آستانه‌هایش tune شود.

**نکته مصاحبه:**

Lead به wraparound و تفاوت VACUUM/VACUUM FULL اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: همه‌چیز در JSONB

```sql
-- ❌ از دست دادن قدرت relational
CREATE TABLE orders (id BIGINT, data JSONB); -- همه‌چیز در data
```

```sql
-- ✅ structured در ستون، پویا در JSONB
CREATE TABLE orders (
    id BIGINT, user_id BIGINT, amount DECIMAL, status TEXT,
    metadata JSONB -- فقط فیلدهای پویا
);
```

**توضیح:** فیلدهای مهم باید ستون باشند تا constraint/index/join ممکن شود.

---

### اشتباه ۲: نادیده گرفتن autovacuum روی جدول پرتغییر

```text
❌ جدولی با میلیون‌ها UPDATE در روز با تنظیم پیش‌فرض autovacuum → bloat
✅ کاهش آستانه‌ی autovacuum برای این جدول
```

```sql
ALTER TABLE hot_table SET (autovacuum_vacuum_scale_factor = 0.05);
```

**توضیح:** پیش‌فرض autovacuum برای جداول بسیار پرتغییر کافی نیست.

---

### اشتباه ۳: `VACUUM FULL` در production

```sql
-- ❌ جدول را قفل می‌کند (downtime)
VACUUM FULL big_table;
```

```sql
-- ✅ از pg_repack یا VACUUM معمولی + tuning استفاده کنید
```

**توضیح:** `VACUUM FULL` exclusive lock می‌گیرد و سرویس را متوقف می‌کند.

---

### اشتباه ۴: خواندن از replica بدون توجه به lag

```text
❌ نوشتن در primary و بلافاصله خواندن از replica → داده‌ی قدیمی
✅ read-your-writes را از primary بخوانید یا lag را در نظر بگیرید
```

**توضیح:** replication async است؛ replica ممکن است عقب باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- MVCC با **isolation levels** و **Spring transactions** (فصل 2.4) عمیق مرتبط است.
- JSONB با **MongoDB** (مقایسه‌ی document model) و **API design**.
- replication با **System Design** (read scaling، CAP) و **HA**.
- performance tools با **Indexing (3.2)** و **query optimization عمیق (14.1)**.
- advisory locks با **distributed lock (Redis)** و **scheduler**.
