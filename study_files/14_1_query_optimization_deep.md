# Query Optimization عمیق — EXPLAIN، Plan Nodes، Index Design، Partitioning

> تحلیل عمیق query plan و طراحی index پیشرفته. مهارت کلیدی برای حل مشکلات performance واقعی.

---

## 📖 مفاهیم

### EXPLAIN و خواندن Plan Nodes

**توضیح:**

`EXPLAIN (ANALYZE, BUFFERS)` نقشه‌ی اجرا را با زمان و I/O واقعی نشان می‌دهد. plan node‌های مهم:

- **Seq Scan:** کل جدول — بد برای جدول بزرگ.
- **Index Scan:** از index، سپس heap fetch.
- **Index Only Scan:** فقط index (covering) — بهترین.
- **Bitmap Heap Scan:** ترکیب چند index برای فیلتر.
- **Nested Loop:** برای result کوچک.
- **Hash Join:** برای result بزرگ (نیاز memory).
- **Merge Join:** برای داده‌ی مرتب.

`cost=X..Y` (X: startup، Y: total تخمینی)، `actual time=...rows=...loops=...` (واقعی). اختلاف زیاد rows تخمینی و واقعی = آمار قدیمی.

**چرا مهم است:**

تشخیص علت کندی query (Seq Scan، join اشتباه، آمار قدیمی) و رفع آن مهارت کلیدی Senior است.

**مثال کد:**

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT u.name, COUNT(o.id)
FROM users u LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.name;
-- بررسی: Seq Scan روی جدول بزرگ؟ join type؟ rows تخمینی در برابر واقعی؟
```

**نکات کلیدی:**

- `BUFFERS` مقدار I/O (shared hit/read) را نشان می‌دهد.
- Nested Loop روی result بزرگ = مشکل (احتمالاً index یا آمار).
- اختلاف rows تخمینی/واقعی → `ANALYZE`.

---

### Index Design پیشرفته

**توضیح:**

- **Composite (ESR rule):** Equality، Sort، Range به همین ترتیب.
- **Partial index:** فقط زیرمجموعه (`WHERE active = true`).
- **Covering index:** با `INCLUDE` برای index-only scan.
- **Expression index:** روی `LOWER(email)` یا محاسبه.

**مثال کد:**

```sql
-- composite: status (equality) سپس created_at (range)
CREATE INDEX idx_orders ON orders(status, created_at DESC);

-- partial: فقط active
CREATE INDEX idx_active ON users(email) WHERE active = true;

-- covering: index-only
CREATE INDEX idx_cover ON orders(user_id) INCLUDE (amount, status);

-- expression
CREATE INDEX idx_lower ON users(LOWER(email));
```

**نکات کلیدی:**

- ESR rule برای ترتیب composite.
- partial index کوچک‌تر و سریع‌تر برای فیلتر ثابت.
- expression index برای function در WHERE.

---

### Common Performance Problems & Partitioning

**توضیح:**

مشکلات: **N+1** (با JOIN FETCH/EntityGraph/batch)، **Missing Index** (EXPLAIN نشان می‌دهد)، **Over-indexing** (write کند)، **Bloat** (dead tuple بعد از UPDATE/DELETE، با VACUUM)، **Lock Contention** (`pg_locks`)، **Bad Statistics** (`ANALYZE`).

**Partitioning** جدول بزرگ را به بخش‌های فیزیکی کوچک‌تر تقسیم می‌کند (Range بر اساس تاریخ، List، Hash). مزایا: partition pruning (query فقط partition مرتبط را اسکن می‌کند)، مدیریت آسان‌تر (drop partition قدیمی به‌جای DELETE)، VACUUM سریع‌تر.

**مثال کد:**

```sql
CREATE TABLE orders (id BIGINT, created_at TIMESTAMP, amount DECIMAL)
    PARTITION BY RANGE (created_at);
CREATE TABLE orders_2024 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

**نکات کلیدی:**

- partition pruning فقط partition مرتبط را اسکن می‌کند.
- drop partition برای حذف داده‌ی قدیمی بسیار سریع‌تر از DELETE.

---

## 🎯 سوالات مصاحبه

### سوال ۱: یک query کند را چطور دیباگ می‌کنی؟ (فرایند کامل)

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

فرایند سیستماتیک: (۱) `EXPLAIN (ANALYZE, BUFFERS)` query را اجرا کنید. (۲) دنبال **Seq Scan** روی جدول بزرگ بگردید → نشانه‌ی index کم. (۳) اختلاف بین **rows تخمینی و واقعی** را چک کنید → آمار قدیمی، `ANALYZE` بزنید. (۴) **join type** را بررسی کنید: Nested Loop روی result بزرگ معمولاً بد است. (۵) **BUFFERS** را ببینید: read بالا یعنی داده در cache نیست. (۶) چک کنید آیا index موجود استفاده می‌شود (شاید function در WHERE یا type mismatch مانع شده). (۷) برای N+1، تعداد query را با ابزار (p6spy، pg_stat_statements) بشمارید. سپس راه‌حل: افزودن index مناسب (با ESR)، بازنویسی query، ANALYZE، یا partitioning. همیشه قبل/بعد را با EXPLAIN ANALYZE مقایسه کنید نه حدس.

**نکته مصاحبه:**

Lead فرایند سیستماتیک با ابزار مشخص دارد، نه حدس. Follow-up: «چرا index موجود استفاده نمی‌شود؟» (function در WHERE، type mismatch، آمار، selectivity پایین).

---

### سوال ۲: partition pruning چیست و چه مزیتی دارد؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

partition pruning یعنی query planner فقط partitionهای مرتبط با شرط query را اسکن می‌کند و بقیه را نادیده می‌گیرد. مثلاً اگر جدول orders بر اساس `created_at` به ماه partition شده باشد و query فقط ماه جاری را بخواهد، فقط partition آن ماه اسکن می‌شود نه کل تاریخچه. مزایا: کاهش چشمگیر داده‌ی اسکن‌شده (performance)، index هر partition کوچک‌تر و کارآمدتر، و مدیریت آسان (حذف داده‌ی قدیمی با `DROP TABLE partition` به‌جای `DELETE` گران و bloat‌ساز). شرط: شرط query باید روی partition key باشد وگرنه pruning رخ نمی‌دهد و همه‌ی partitionها اسکن می‌شوند.

**نکته مصاحبه:**

Senior به شرط «query روی partition key» و مزیت drop partition اشاره می‌کند.

---

### سوال ۳: bloat چیست و چطور با آن مقابله می‌کنی؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

به‌خاطر MVCC، هر UPDATE/DELETE نسخه‌های قدیمی (dead tuple) باقی می‌گذارد که فضا اشغال می‌کنند اما visible نیستند — این bloat است. علائم: جدول/index بزرگ‌تر از داده‌ی واقعی، query کندتر (اسکن صفحات خالی)، I/O بیشتر. مقابله: (۱) **autovacuum** را برای جداول پرتغییر tune کنید (آستانه‌ی پایین‌تر). (۲) `VACUUM` فضا را برای reuse آزاد می‌کند (اما به OS برنمی‌گرداند). (۳) `VACUUM FULL` فضا را به OS برمی‌گرداند اما جدول را قفل می‌کند (downtime) — در production از `pg_repack` (بدون قفل) استفاده کنید. (۴) رصد با `pg_stat_user_tables` (n_dead_tup). پیشگیری: کاهش UPDATE غیرضروری و batch کردن.

**نکته مصاحبه:**

Senior به pg_repack به‌جای VACUUM FULL در production اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: index بدون توجه به ESR

```sql
-- ❌ range قبل از equality
CREATE INDEX ON orders(created_at, status);
```

```sql
-- ✅ equality اول
CREATE INDEX ON orders(status, created_at);
```

**توضیح:** ESR rule: Equality، Sort، Range.

---

### اشتباه ۲: query روی غیر partition key

```sql
-- ❌ pruning رخ نمی‌دهد، همه partition اسکن
SELECT * FROM orders WHERE customer_id = 5; -- partition key: created_at
```

```sql
-- ✅ شامل partition key
SELECT * FROM orders WHERE created_at >= '2024-06-01' AND customer_id = 5;
```

**توضیح:** بدون partition key در شرط، pruning کار نمی‌کند.

---

### اشتباه ۳: VACUUM FULL در production

```sql
-- ❌ قفل جدول (downtime)
VACUUM FULL orders;
```

```text
✅ pg_repack یا autovacuum tuning
```

**توضیح:** `VACUUM FULL` exclusive lock می‌گیرد.

---

## 🔗 ارتباط با سایر مفاهیم

- query optimization با **Indexing (3.2)** و **PostgreSQL MVCC (3.3)**.
- N+1 با **Spring Data JPA (2.4)**.
- partitioning با **System Design scaling (6.2)** و **MongoDB sharding (مقایسه)**.
- bloat با **MVCC و VACUUM (3.3)**.
