# MySQL / Oracle (مقایسه‌ای)

> آشنایی با تفاوت‌های MySQL و Oracle برای محیط‌هایی که این دیتابیس‌ها استفاده می‌شوند مهم است.

---

## 📖 مفاهیم

### MySQL — Storage Engines

**توضیح:**

MySQL معماری pluggable storage engine دارد. دو اصلی:

- **InnoDB** (پیش‌فرض): transactional، ACID، row-level locking، foreign key، crash recovery، MVCC. انتخاب درست برای تقریباً همه موارد.
- **MyISAM** (قدیمی): بدون transaction، table-level locking، بدون foreign key. سریع برای read-only اما در عمل منسوخ.

MySQL 8 امکانات مدرن آورد: Window Functions، CTEs (شامل recursive)، roles، invisible indexes (برای تست حذف index بدون drop)، و بهبود JSON.

**چرا مهم است:**

انتخاب engine روی transaction و locking تأثیر مستقیم دارد. MyISAM در سیستم‌های جدید نباید استفاده شود.

**مثال کد:**

```sql
-- صریحاً InnoDB
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- invisible index (MySQL 8): تست تأثیر حذف بدون drop واقعی
ALTER TABLE orders ALTER INDEX idx_amount INVISIBLE;
```

**نکات کلیدی:**

- همیشه InnoDB برای داده‌ی transactional.
- MySQL 8 window functions و CTE اضافه کرد (قبلاً نبود).
- invisible index برای ارزیابی امن حذف index.

---

### MySQL — Replication

**توضیح:**

دو روش: **Binary Log-based** (replica لاگ باینری primary را پخش می‌کند) و **GTID-based** (Global Transaction Identifier — هر transaction شناسه‌ی یکتای جهانی دارد که failover و consistency را ساده می‌کند). slow query log برای یافتن کوئری‌های کند. `EXPLAIN` با فرمت متفاوت از PostgreSQL.

**نکات کلیدی:**

- GTID-based replication مدیریت failover را ساده‌تر می‌کند.
- slow query log را برای شناسایی کوئری مشکل‌دار فعال کنید.

---

### Oracle — ویژگی‌های خاص

**توضیح:**

Oracle دیتابیس enterprise با ویژگی‌های خاص:

- `ROWNUM` (شماره‌ی ردیف pseudo-column، قبل از ORDER BY اعمال می‌شود — تله‌ی رایج) در برابر `ROW_NUMBER()` (window function، بعد از ORDER BY).
- `SEQUENCE` با `NEXTVAL`/`CURRVAL` برای تولید شناسه.
- `CONNECT BY` برای queryهای سلسله‌مراتبی (معادل recursive CTE).
- Tablespaces، Schemas برای سازماندهی فیزیکی/منطقی.
- **AWR** (Automatic Workload Repository) و **ASH** (Active Session History) برای گزارش performance.
- **RAC** (Real Application Clusters) برای HA و scaling افقی با shared storage.

**چرا مهم است:**

در بانک‌ها و سازمان‌های بزرگ Oracle رایج است. درک تفاوت‌ها (مثل ROWNUM) از باگ جلوگیری می‌کند.

**مثال کد:**

```sql
-- ❌ تله: ROWNUM قبل از ORDER BY → ۵ ردیف تصادفی سپس مرتب
SELECT * FROM orders WHERE ROWNUM <= 5 ORDER BY amount DESC;

-- ✅ صحیح: ابتدا مرتب، سپس محدود
SELECT * FROM (SELECT * FROM orders ORDER BY amount DESC) WHERE ROWNUM <= 5;
-- یا در Oracle 12c+: FETCH FIRST
SELECT * FROM orders ORDER BY amount DESC FETCH FIRST 5 ROWS ONLY;

-- sequence
CREATE SEQUENCE order_seq START WITH 1 INCREMENT BY 1;
INSERT INTO orders (id) VALUES (order_seq.NEXTVAL);
```

**نکات کلیدی:**

- `ROWNUM` قبل از `ORDER BY` اعمال می‌شود → برای top-N از subquery یا `FETCH FIRST`.
- Oracle 12c+ از `FETCH FIRST N ROWS ONLY` (استاندارد) پشتیبانی می‌کند.

---

## 🎯 سوالات مصاحبه

### سوال ۱: InnoDB در برابر MyISAM چه تفاوتی دارد؟

**سطح:** Mid / Senior
**تکرار:** زیاد

**جواب کامل:**

InnoDB transactional است (ACID)، row-level locking دارد (concurrency بالا)، از foreign key و crash recovery پشتیبانی می‌کند و MVCC دارد. MyISAM غیرtransactional است، table-level locking دارد (هر write کل جدول را قفل می‌کند → concurrency پایین)، بدون foreign key و بدون crash recovery امن. تاریخاً MyISAM برای read-heavy سریع‌تر تلقی می‌شد، اما با بهبودهای InnoDB دیگر دلیلی برای MyISAM در سیستم جدید نیست. پیش‌فرض MySQL از 5.5 به بعد InnoDB است.

**نکته مصاحبه:**

Senior می‌داند MyISAM منسوخ است و دلیل (locking، عدم transaction) را توضیح می‌دهد.

---

### سوال ۲: تفاوت `ROWNUM` و `ROW_NUMBER()` در Oracle چیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`ROWNUM` یک pseudo-column است که **هنگام انتخاب ردیف‌ها** (قبل از ORDER BY) تخصیص می‌یابد. بنابراین `WHERE ROWNUM <= 5 ORDER BY x` ابتدا ۵ ردیف دلخواه را برمی‌دارد و بعد مرتب می‌کند — نتیجه‌ی اشتباه برای top-N. `ROW_NUMBER()` یک window function است که **بعد از** اعمال ORDER BY در `OVER(...)` شماره می‌دهد، پس top-N درست را می‌دهد. برای top-N یا باید ROWNUM را روی subquery مرتب‌شده اعمال کنید یا از `ROW_NUMBER()`/`FETCH FIRST` استفاده کنید.

**نکته مصاحبه:**

تمایز Senior: دانستن تله‌ی ترتیب اعمال ROWNUM. Follow-up: «pagination در Oracle 12c چطور؟» (`OFFSET ... FETCH NEXT`).

---

### سوال ۳: GTID در replication چه مزیتی دارد؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

در replication سنتی binlog-based، موقعیت replica با نام فایل و offset binlog مشخص می‌شد که هنگام failover (تغییر primary) محاسبه‌ی موقعیت معادل روی master جدید سخت و خطاپذیر بود. GTID به هر transaction یک شناسه‌ی یکتای جهانی می‌دهد، پس replica دقیقاً می‌داند کدام transactionها را اعمال کرده و failover به master جدید خودکار و امن می‌شود (بدون محاسبه‌ی دستی offset). همچنین تشخیص ناسازگاری و auto-positioning را ممکن می‌کند.

**نکته مصاحبه:**

Lead به ساده‌سازی failover اشاره می‌کند.

---

### سوال ۴: AWR و ASH در Oracle برای چه هستند؟

**سطح:** Senior
**تکرار:** کم

**جواب کامل:**

هر دو ابزار performance diagnostics در Oracle هستند. **AWR** (Automatic Workload Repository) به‌صورت دوره‌ای snapshot از آمار performance (top SQL، wait events، منابع) می‌گیرد و گزارش بین دو snapshot می‌دهد — برای تحلیل تاریخی و یافتن گلوگاه. **ASH** (Active Session History) نمونه‌برداری مکرر از sessionهای فعال است — برای تحلیل real-time و رویدادهای کوتاه‌مدت که بین snapshotهای AWR گم می‌شوند. ترکیب این دو برای troubleshooting performance استفاده می‌شود (معادل تقریبی `pg_stat_statements` در PostgreSQL).

**نکته مصاحبه:**

Senior معادل PostgreSQL را می‌داند و تفاوت تاریخی/real-time را توضیح می‌دهد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: ROWNUM قبل از ORDER BY

```sql
-- ❌ ۵ ردیف تصادفی
SELECT * FROM orders WHERE ROWNUM <= 5 ORDER BY amount DESC;
```

```sql
-- ✅
SELECT * FROM orders ORDER BY amount DESC FETCH FIRST 5 ROWS ONLY;
```

**توضیح:** ROWNUM قبل از مرتب‌سازی اعمال می‌شود.

---

### اشتباه ۲: استفاده از MyISAM برای داده‌ی transactional

```sql
-- ❌
CREATE TABLE payments (...) ENGINE=MyISAM; -- بدون transaction!
```

```sql
-- ✅
CREATE TABLE payments (...) ENGINE=InnoDB;
```

**توضیح:** MyISAM transaction و FK ندارد؛ برای پول فاجعه است.

---

### اشتباه ۳: فرض رفتار یکسان EXPLAIN بین MySQL و PostgreSQL

```text
❌ انتظار همان خروجی و plan node
✅ هر DB planner و فرمت EXPLAIN متفاوتی دارد
```

**توضیح:** مهارت EXPLAIN باید برای هر DB جداگانه یاد گرفته شود.

---

## 🔗 ارتباط با سایر مفاهیم

- storage engine و locking با **transactions** و **isolation (3.1, 2.4)** مرتبط است.
- replication با **System Design (HA، read scaling)** و **PostgreSQL replication** قابل‌مقایسه.
- ROWNUM/ROW_NUMBER با **window functions (3.1)**.
- AWR/ASH با **performance tools** PostgreSQL.
