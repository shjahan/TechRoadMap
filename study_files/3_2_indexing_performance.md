# Indexing & Performance — Index Types، Query Optimization، Connection Pooling

> ایندکس‌گذاری مهارت کلیدی هر backend Senior است. «چرا query کند است» سوال همیشگی مصاحبه‌هاست.

---

## 📖 مفاهیم

### Index Types

**توضیح:**

ایندکس ساختار داده‌ای است که جستجو را سریع می‌کند (به‌جای full table scan). انواع:

- **B-Tree** (پیش‌فرض): برای equality و range (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`). متعادل، O(log n).
- **Hash:** فقط equality، سریع‌تر برای `=` اما بدون range.
- **GiST/GIN** (PostgreSQL): GIN برای full-text، arrays، jsonb؛ GiST برای geometric/range.
- **Partial Index:** فقط روی زیرمجموعه‌ای از ردیف‌ها (`WHERE status = 'ACTIVE'`) — کوچک‌تر و سریع‌تر.
- **Composite Index:** روی چند ستون؛ **ترتیب ستون‌ها حیاتی است**.
- **Covering Index:** با `INCLUDE` ستون‌های اضافه را در index می‌گذارد تا نیاز به heap fetch نباشد (index-only scan).

**چرا مهم است:**

index درست تفاوت بین query میلی‌ثانیه‌ای و چندثانیه‌ای است. اما over-indexing نوشتن را کند می‌کند (هر index باید با هر insert/update به‌روز شود).

**مثال کد:**

```sql
-- composite: ترتیب مهم است
-- این برای WHERE status=? AND created_at>? و WHERE status=? کار می‌کند
-- اما برای WHERE created_at>? تنها کار نمی‌کند (prefix rule)
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);

-- partial: فقط active records
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- covering: index-only scan بدون heap fetch
CREATE INDEX idx_orders_covering ON orders(user_id) INCLUDE (amount, status);
```

**نکات کلیدی:**

- در composite index، ستون با بالاترین selectivity و آن‌که در equality استفاده می‌شود اول بیاید (leftmost prefix rule).
- partial index برای ستون‌هایی که اغلب با یک شرط ثابت query می‌شوند.
- هر index سرعت write را کاهش می‌دهد؛ index بی‌استفاده را حذف کنید.

---

### Leftmost Prefix Rule

**توضیح:**

یک composite index روی `(a, b, c)` فقط برای queryهایی که از prefix چپ استفاده می‌کنند کارآمد است: `WHERE a=?`, `WHERE a=? AND b=?`, `WHERE a=? AND b=? AND c=?`. برای `WHERE b=?` تنها (بدون a) معمولاً استفاده نمی‌شود. به همین دلیل ترتیب ستون‌ها در طراحی index بسیار مهم است.

**مثال کد:**

```sql
CREATE INDEX idx ON orders(user_id, status, created_at);
-- ✅ از index استفاده می‌کند:
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 1 AND status = 'PAID';
-- ❌ از index کامل استفاده نمی‌کند:
SELECT * FROM orders WHERE status = 'PAID'; -- user_id جا افتاده
```

**نکات کلیدی:**

- ستونی که در range است را آخر بگذارید (range بعد از آن، prefix را می‌شکند).
- equality columns قبل از range column.

---

### Query Optimization با EXPLAIN

**توضیح:**

`EXPLAIN` نقشه‌ی اجرای query (query plan) را نشان می‌دهد؛ `EXPLAIN ANALYZE` آن را واقعاً اجرا و زمان/ردیف واقعی را گزارش می‌کند. انواع scan: **Seq Scan** (کل جدول، بد برای جدول بزرگ)، **Index Scan** (از index سپس heap fetch)، **Index Only Scan** (فقط index، بهترین)، **Bitmap Scan** (ترکیب چند index). انواع join: Nested Loop (small)، Hash Join (large)، Merge Join (sorted).

planner بر اساس **statistics** (که با `ANALYZE` به‌روز می‌شود) تصمیم می‌گیرد؛ آمار قدیمی = plan بد.

**مثال کد:**

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT u.name, COUNT(o.id)
FROM users u LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.name;
-- به دنبال: Seq Scan روی جدول بزرگ (نیاز index)، rows تخمینی در برابر واقعی
```

**نکات کلیدی:**

- Seq Scan روی جدول بزرگ معمولاً یعنی index کم است.
- اختلاف زیاد بین rows تخمینی و واقعی یعنی آمار قدیمی → `ANALYZE`.
- `BUFFERS` نشان می‌دهد چقدر I/O انجام شده.

---

### Connection Pooling

**توضیح:**

باز کردن connection به DB گران است (TCP handshake، auth). connection pool مجموعه‌ای از connectionهای آماده را نگه می‌دارد و reuse می‌کند. **HikariCP** پیش‌فرض و سریع‌ترین در Spring Boot است. پارامترهای کلیدی: `maximumPoolSize` (مهم‌ترین)، `connectionTimeout`, `idleTimeout`, `maxLifetime`.

نکته‌ی مهم: pool size بزرگ‌تر همیشه بهتر نیست. فرمول تقریبی: `connections = (core_count * 2) + effective_spindle_count`. pool بسیار بزرگ باعث context switching و فشار روی DB می‌شود. **PgBouncer** یک pooler خارجی برای PostgreSQL در مقیاس بالاست.

**مثال کد:**

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20      # نه خیلی بزرگ
      minimum-idle: 5
      connection-timeout: 5000   # ms، انتظار برای گرفتن connection
      idle-timeout: 600000
      max-lifetime: 1800000      # کمتر از timeout سمت DB
```

**نکات کلیدی:**

- pool size را با محاسبه تنظیم کنید، نه حدس؛ بزرگ‌تر همیشه بهتر نیست.
- `max-lifetime` را کمتر از DB/firewall idle timeout بگذارید.
- pool exhaustion (همه‌ی connectionها مشغول) منشأ رایج timeout است.

---

## 🎯 سوالات مصاحبه

### سوال ۱: ترتیب ستون‌ها در composite index چرا مهم است؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

به‌خاطر **leftmost prefix rule**. یک index روی `(a, b, c)` مثل یک دفترچه‌ی مرتب‌شده ابتدا بر اساس a، سپس b، سپس c است. می‌توان با a، یا a+b، یا a+b+c جستجو کرد، اما نمی‌توان مستقیماً با b تنها استفاده‌ی کارآمد کرد چون b فقط درون هر گروه a مرتب است. قاعده‌ی طراحی: ستون‌های equality را اول، ستون range را آخر بگذارید (چون بعد از range، ستون‌های بعدی مرتب نیستند و prefix می‌شکند). همچنین ستون پرselectivity زودتر برای فیلتر مؤثرتر.

**کد توضیحی:**

```sql
-- برای WHERE status=? AND created_at BETWEEN ? AND ?
CREATE INDEX idx ON orders(status, created_at); -- equality اول، range آخر
```

**نکته مصاحبه:**

تمایز Senior: قانون «equality قبل از range» و prefix rule. Follow-up: «آیا index روی (a,b) برای ORDER BY a,b هم استفاده می‌شود؟» (بله).

---

### سوال ۲: index-only scan چیست و چرا سریع‌تر است؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

در index scan معمولی، DB ابتدا index را پیمایش می‌کند تا pointer به ردیف‌ها را بیابد، سپس برای گرفتن ستون‌های دیگر به heap (جدول اصلی) مراجعه می‌کند (heap fetch) — این I/O اضافه است. در **index-only scan**، اگر همه‌ی ستون‌های مورد نیاز query در خود index موجود باشند (با covering index و `INCLUDE`)، نیازی به heap fetch نیست و همه‌چیز از index خوانده می‌شود — بسیار سریع‌تر. در PostgreSQL، این به visibility map هم وابسته است (ردیف باید همه‌جا visible باشد، که با VACUUM به‌روز می‌شود).

**نکته مصاحبه:**

Senior به covering index و visibility map (در PG) اشاره می‌کند. Follow-up: «چرا گاهی covering index هم heap fetch می‌کند؟» (visibility map قدیمی).

---

### سوال ۳: چه زمانی index کمک نمی‌کند (یا حتی بد است)؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

موارد: (۱) ستون با selectivity پایین (مثل boolean یا gender) — اگر ۵۰٪ ردیف‌ها match کنند، seq scan ارزان‌تر از index + heap fetch است. (۲) جدول کوچک — seq scan سریع‌تر. (۳) استفاده از function روی ستون (`WHERE LOWER(email)=...`) که index معمولی را بی‌اثر می‌کند مگر expression index بسازید. (۴) leading wildcard در LIKE (`'%abc'`). (۵) type mismatch که implicit cast ایجاد می‌کند. و هزینه: هر index، insert/update/delete را کند می‌کند و فضا می‌گیرد؛ over-indexing مضر است.

**کد توضیحی:**

```sql
-- ❌ index روی email بی‌اثر می‌شود
WHERE LOWER(email) = 'x';
-- ✅ expression index
CREATE INDEX idx_lower_email ON users(LOWER(email));
```

**نکته مصاحبه:**

Lead به trade-off read/write و selectivity اشاره می‌کند.

---

### سوال ۴: HikariCP pool size را چطور تنظیم می‌کنی؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

برخلاف تصور، pool بزرگ بهتر نیست. DB تعداد محدودی کار موازی واقعی انجام می‌دهد (محدود به CPU و disk). فرمول مرجع HikariCP: `connections ≈ (core_count * 2) + effective_spindles`. pool بسیار بزرگ منجر به context switching، contention، و فشار روی DB می‌شود و throughput را کاهش می‌دهد. باید با load test و رصد metric (active/idle/pending) تنظیم شود. همچنین `maximum-pool-size` باید با ظرفیت `max_connections` خود DB هماهنگ باشد (به‌خصوص با چند instance اپ). اگر connection کم می‌آید، اول ببینید queryها چرا connection را زیاد نگه می‌دارند (transaction طولانی، N+1) نه اینکه کورکورانه pool را بزرگ کنید.

**نکته مصاحبه:**

Lead به فرمول، رصد و هماهنگی با DB max_connections اشاره می‌کند.

---

### سوال ۵: N+1 را در سطح DB چطور تشخیص می‌دهی؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

علائم: تعداد زیادی query تقریباً یکسان با مقادیر متفاوت در `pg_stat_statements` یا لاگ query؛ یک endpoint که با افزایش داده، تعداد queryها خطی رشد می‌کند. ابزار: فعال کردن SQL logging (در Hibernate `show-sql` یا بهتر p6spy/datasource-proxy که تعداد را می‌شمارد)، `pg_stat_statements` برای دیدن query پرتکرار، و APM که تعداد DB call در هر request را نشان می‌دهد. حل با `JOIN FETCH`/`@EntityGraph`/batch fetching.

**نکته مصاحبه:**

Senior ابزارهای مشخص (`pg_stat_statements`، p6spy) را نام می‌برد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: function روی ستون indexed

```sql
-- ❌ index بی‌اثر
WHERE DATE(created_at) = '2024-01-01';
```

```sql
-- ✅ range به‌جای function
WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02';
```

**توضیح:** function روی ستون، index B-Tree را بی‌اثر می‌کند مگر expression index.

---

### اشتباه ۲: over-indexing

```sql
-- ❌ index روی هر ستون → write کند، فضای زیاد
CREATE INDEX ON t(a); CREATE INDEX ON t(b); CREATE INDEX ON t(c); ...
```

```sql
-- ✅ index بر اساس query واقعی، composite هوشمند
CREATE INDEX ON t(a, b);
```

**توضیح:** هر index هزینه‌ی write و storage دارد؛ فقط برای queryهای واقعی بسازید.

---

### اشتباه ۳: فراموشی ANALYZE بعد از bulk load

```sql
-- ❌ آمار قدیمی → plan بد
COPY orders FROM 'data.csv';
-- query کند می‌شود
```

```sql
-- ✅
COPY orders FROM 'data.csv';
ANALYZE orders;
```

**توضیح:** planner بر اساس آمار تصمیم می‌گیرد؛ بعد از تغییر بزرگ باید ANALYZE شود.

---

### اشتباه ۴: pool size خیلی بزرگ

```yaml
# ❌
maximum-pool-size: 200
```

```yaml
# ✅ متناسب با CPU و DB
maximum-pool-size: 20
```

**توضیح:** pool بزرگ contention و فشار روی DB می‌سازد.

---

## 🔗 ارتباط با سایر مفاهیم

- indexing با **SQL fundamentals** و **query optimization عمیق (فصل 14)** گره خورده.
- N+1 با **Spring Data JPA** عمیق مرتبط است.
- connection pooling با **Spring Boot config** و **performance tuning**.
- EXPLAIN با **PostgreSQL MVCC** و آمار.
- partial/covering index با **PostgreSQL** ویژگی‌های خاص.
