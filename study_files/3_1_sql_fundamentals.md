# مبانی SQL — DDL، DML، Joins، Aggregation، Window Functions

> SQL در هر مصاحبه‌ی backend پرسیده می‌شود. تسلط بر join، aggregation و window functions ضروری است.

---

## 📖 مفاهیم

### DDL — تعریف ساختار

**توضیح:**

DDL (Data Definition Language) ساختار داده را تعریف می‌کند: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`. انتخاب درست data type و constraint اساس یکپارچگی داده است. constraintها (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`) قوانین کسب‌وکار را در سطح DB enforce می‌کنند — حتی اگر اپ باگ داشته باشد، DB از داده‌ی نامعتبر جلوگیری می‌کند.

تفاوت `DROP` و `TRUNCATE` و `DELETE`: `DELETE` ردیف‌ها را با WHERE حذف می‌کند (loggable، قابل rollback، trigger fire می‌شود)؛ `TRUNCATE` کل جدول را سریع خالی می‌کند (بدون WHERE، معمولاً غیرقابل rollback در برخی DBها، بدون trigger)؛ `DROP` کل جدول را حذف می‌کند.

**چرا مهم است:**

طراحی schema با constraintهای درست از data corruption جلوگیری می‌کند. انتخاب type اشتباه (مثل VARCHAR برای پول) منشأ باگ است.

**مثال کد:**

```sql
CREATE TABLE orders (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id),
    amount      DECIMAL(12, 2) NOT NULL CHECK (amount >= 0), -- نه FLOAT برای پول
    status      VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_user_status UNIQUE (user_id, status)
);
```

**نکات کلیدی:**

- برای پول `DECIMAL`/`NUMERIC` استفاده کنید نه `FLOAT` (خطای گرد کردن).
- constraintها را در DB بگذارید، نه فقط در اپ.
- `TIMESTAMPTZ` برای زمان با منطقه؛ همیشه UTC ذخیره کنید.

---

### DML — دستکاری داده

**توضیح:**

DML داده را می‌خواند/تغییر می‌دهد: `SELECT`, `INSERT`, `UPDATE`, `DELETE`. بندهای کلیدی: `WHERE` (فیلتر ردیف)، `ORDER BY` (مرتب‌سازی)، `GROUP BY` (گروه‌بندی)، `HAVING` (فیلتر گروه‌ها)، `LIMIT`/`OFFSET` (صفحه‌بندی).

**Subquery** دو نوع: non-correlated (مستقل، یک‌بار اجرا) و correlated (به ردیف بیرونی وابسته، برای هر ردیف اجرا — می‌تواند کند باشد).

نکته‌ی performance: `OFFSET` بزرگ برای صفحه‌بندی عمیق کند است (DB باید همه‌ی ردیف‌های قبلی را اسکن کند)؛ keyset pagination (`WHERE id > last_id`) بهتر است.

**مثال کد:**

```sql
-- صفحه‌بندی keyset (بهتر از OFFSET بزرگ)
SELECT id, name FROM users
WHERE id > 1000          -- last_seen_id
ORDER BY id
LIMIT 20;

-- correlated subquery: آخرین سفارش هر کاربر
SELECT u.name,
       (SELECT MAX(o.created_at) FROM orders o WHERE o.user_id = u.id) AS last_order
FROM users u;
```

**نکات کلیدی:**

- `OFFSET` بزرگ کند است؛ keyset pagination برای صفحه‌بندی عمیق.
- correlated subquery می‌تواند به join تبدیل شود برای performance بهتر.
- `WHERE` قبل از group، `HAVING` بعد از group فیلتر می‌کند.

---

### Joins

**توضیح:**

- `INNER JOIN`: فقط ردیف‌های منطبق در هر دو جدول.
- `LEFT JOIN`: همه‌ی ردیف‌های چپ + منطبق راست (راست NULL اگر نباشد).
- `RIGHT JOIN`: برعکس.
- `FULL OUTER JOIN`: همه‌ی هر دو طرف.
- `CROSS JOIN`: حاصل‌ضرب دکارتی.
- `SELF JOIN`: جدول با خودش (مثل سلسله‌مراتب کارمند-مدیر).

انتخاب join در برابر subquery: join معمولاً برای ترکیب داده‌ها بهینه‌تر است و planner بهتر آن را بهینه می‌کند؛ subquery برای existence check (`EXISTS`) یا محاسبات scalar.

**مثال کد:**

```sql
-- LEFT JOIN: همه‌ی کاربران حتی بدون سفارش
SELECT u.name, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.id, u.name;

-- SELF JOIN: کارمند و مدیرش
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

**نکات کلیدی:**

- `LEFT JOIN` + فیلتر روی جدول راست در WHERE، آن را به INNER تبدیل می‌کند (اشتباه رایج).
- `EXISTS` معمولاً سریع‌تر از `IN` با subquery برای existence check.

---

### Aggregation & GROUP BY

**توضیح:**

توابع تجمعی: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. `GROUP BY` ردیف‌ها را گروه می‌کند و تابع تجمعی روی هر گروه اعمال می‌شود. `HAVING` گروه‌ها را فیلتر می‌کند (برخلاف `WHERE` که ردیف‌ها را قبل از گروه‌بندی). 

نکته: `COUNT(*)` همه‌ی ردیف‌ها، `COUNT(column)` فقط non-NULL، `COUNT(DISTINCT column)` مقادیر یکتا.

**مثال کد:**

```sql
-- مشتریانی با بیش از ۵ سفارش پرداخت‌شده
SELECT user_id, COUNT(*) AS paid_orders, SUM(amount) AS total
FROM orders
WHERE status = 'PAID'        -- فیلتر ردیف قبل از گروه
GROUP BY user_id
HAVING COUNT(*) > 5          -- فیلتر گروه بعد از تجمیع
ORDER BY total DESC;
```

**نکات کلیدی:**

- `WHERE` قبل از group، `HAVING` بعد.
- `COUNT(col)` مقادیر NULL را نمی‌شمارد.

---

### Window Functions

**توضیح:**

برخلاف `GROUP BY` که ردیف‌ها را جمع می‌کند، window function محاسبه را روی یک «پنجره» از ردیف‌ها انجام می‌دهد اما **تک‌تک ردیف‌ها را حفظ می‌کند**. با `OVER (PARTITION BY ... ORDER BY ...)`. توابع: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LAG()`, `LEAD()`, و توابع تجمعی به‌صورت running.

**چرا مهم است:**

برای محاسبات تحلیلی (running total، ranking، مقایسه با ردیف قبل) که بدون window function نیاز به subqueryهای پیچیده و کند دارند.

**مثال کد:**

```sql
SELECT
    user_id,
    order_date,
    amount,
    -- running total به ازای هر کاربر
    SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS running_total,
    -- مبلغ سفارش قبلی
    LAG(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS prev_amount,
    -- رتبه‌ی سفارش در هر ماه
    RANK() OVER (PARTITION BY DATE_TRUNC('month', order_date)
                 ORDER BY amount DESC) AS monthly_rank
FROM orders;
```

**نکات کلیدی:**

- window function ردیف‌ها را حفظ می‌کند (برخلاف GROUP BY).
- `RANK` با مقادیر مساوی فاصله می‌اندازد (1,1,3)؛ `DENSE_RANK` نه (1,1,2)؛ `ROW_NUMBER` همیشه یکتا.

---

### Advanced SQL — CTE، Views

**توضیح:**

**CTE (Common Table Expression)** با `WITH` یک query موقت نام‌دار می‌سازد که خوانایی را بالا می‌برد و امکان **recursive CTE** (برای داده‌ی سلسله‌مراتبی مثل درخت) را می‌دهد. **View** یک query ذخیره‌شده است (هر بار اجرا)؛ **Materialized View** نتیجه را فیزیکی ذخیره می‌کند (سریع‌تر برای خواندن، اما باید refresh شود).

**مثال کد:**

```sql
-- recursive CTE: کل زیرمجموعه‌های یک مدیر
WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id FROM employees WHERE id = 1
    UNION ALL
    SELECT e.id, e.name, e.manager_id
    FROM employees e
    JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates;
```

**نکات کلیدی:**

- recursive CTE برای داده‌ی درختی (سازمان، دسته‌بندی).
- materialized view برای گزارش‌های گران اما کم‌تغییر.

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت `WHERE` و `HAVING` چیست؟

**سطح:** Junior / Mid
**تکرار:** خیلی زیاد

**جواب کامل:**

`WHERE` ردیف‌ها را **قبل** از گروه‌بندی فیلتر می‌کند و نمی‌تواند از توابع تجمعی استفاده کند. `HAVING` گروه‌ها را **بعد** از `GROUP BY` و تجمیع فیلتر می‌کند و می‌تواند روی نتیجه‌ی تابع تجمعی شرط بگذارد. ترتیب منطقی اجرا: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY. به همین دلیل نمی‌توان در WHERE به alias در SELECT اشاره کرد (هنوز محاسبه نشده).

**کد توضیحی:**

```sql
SELECT dept, AVG(salary) FROM emp
WHERE active = true        -- فیلتر ردیف
GROUP BY dept
HAVING AVG(salary) > 5000; -- فیلتر گروه
```

**نکته مصاحبه:**

Senior ترتیب منطقی اجرای query را می‌داند. Follow-up: «چرا نمی‌توان در WHERE به alias اشاره کرد؟»

---

### سوال ۲: تفاوت `RANK`, `DENSE_RANK`, `ROW_NUMBER` چیست؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

هر سه رتبه می‌دهند اما رفتار با مقادیر مساوی فرق دارد. `ROW_NUMBER` همیشه شماره‌ی یکتا (حتی برای مساوی‌ها) می‌دهد: 1,2,3,4. `RANK` به مساوی‌ها رتبه‌ی یکسان می‌دهد و سپس **می‌پرد**: 1,1,3,4. `DENSE_RANK` رتبه‌ی یکسان بدون پرش: 1,1,2,3. انتخاب بستگی به نیاز دارد: برای «نفر دوم واقعی» با در نظر گرفتن مساوی‌ها `DENSE_RANK`، برای شماره‌گذاری یکتا `ROW_NUMBER`.

**نکته مصاحبه:**

Follow-up: «چطور با window function رکورد دوم گران‌ترین هر دسته را بگیری؟» (`DENSE_RANK() = 2` در subquery).

---

### سوال ۳: join در برابر subquery — کدام بهینه‌تر؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

معمولاً join بهینه‌تر است چون query planner آزادی بیشتری در انتخاب استراتژی (hash join، merge join) دارد. اما این مطلق نیست: برای existence check، `EXISTS` (که می‌تواند short-circuit کند) اغلب از join یا `IN` با subquery بهتر است؛ و `IN` با لیست بزرگ subquery کند می‌شود. correlated subquery که برای هر ردیف اجرا می‌شود معمولاً بدترین گزینه است و باید به join تبدیل شود. در نهایت باید با `EXPLAIN ANALYZE` بسنجید نه حدس.

**نکته مصاحبه:**

تمایز Senior: «اندازه‌گیری با EXPLAIN، نه حدس» و دانستن EXISTS. Follow-up: «`IN` در برابر `EXISTS` با NULL چه فرقی دارد؟» (`NOT IN` با NULL در لیست نتیجه‌ی خالی می‌دهد — تله‌ی رایج).

---

### سوال ۴: چرا `OFFSET` بزرگ برای صفحه‌بندی کند است؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`OFFSET 100000 LIMIT 20` یعنی DB باید ۱۰۰٬۰۲۰ ردیف را پردازش/مرتب کند و سپس ۱۰۰٬۰۰۰ تای اول را دور بریزد — کار خطی که با عمق صفحه بدتر می‌شود. راه‌حل **keyset pagination** (seek method): به‌جای offset، از `WHERE id > last_seen_id ORDER BY id LIMIT 20` استفاده کنید که با index می‌تواند مستقیماً به نقطه‌ی شروع برود — O(log n) به‌جای O(n). محدودیت keyset: پرش به صفحه‌ی دلخواه سخت‌تر است و به ستون مرتب‌سازی یکتا نیاز دارد.

**نکته مصاحبه:**

Senior keyset pagination را می‌شناسد. Follow-up: «keyset با مرتب‌سازی روی ستون غیریکتا چطور؟» (ترکیب با id به‌عنوان tie-breaker).

---

### سوال ۵: recursive CTE برای چه استفاده می‌شود؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

برای پیمایش داده‌ی سلسله‌مراتبی یا گرافی: درخت سازمانی (همه‌ی زیردستان یک مدیر)، دسته‌بندی تو در تو، graph traversal، یا تولید سری اعداد. ساختار دو بخش دارد: anchor (نقطه‌ی شروع) و recursive part که به نتیجه‌ی خودش join می‌شود تا وقتی ردیف جدیدی تولید نشود. باید مراقب حلقه‌ی بی‌نهایت بود (با depth limit یا cycle detection). در Oracle معادل آن `CONNECT BY` است.

**نکته مصاحبه:**

Follow-up: «چطور از حلقه‌ی بی‌نهایت در گراف جلوگیری می‌کنی؟» (نگه‌داری مسیر بازدیدشده).

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: استفاده از FLOAT برای پول

```sql
-- ❌ خطای گرد کردن: 0.1 + 0.2 != 0.3
amount FLOAT
```

```sql
-- ✅
amount DECIMAL(12, 2)
```

**توضیح:** اعداد اعشاری باینری پول را دقیق نگه نمی‌دارند.

---

### اشتباه ۲: LEFT JOIN که به INNER تبدیل می‌شود

```sql
-- ❌ فیلتر روی جدول راست در WHERE، NULLها را حذف می‌کند
SELECT * FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.status = 'PAID'; -- کاربران بدون سفارش حذف می‌شوند
```

```sql
-- ✅ شرط را در ON بگذارید
SELECT * FROM users u
LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'PAID';
```

**توضیح:** فیلتر روی ستون جدول راست در WHERE، رفتار LEFT JOIN را می‌شکند.

---

### اشتباه ۳: `NOT IN` با مقادیر NULL

```sql
-- ❌ اگر subquery حتی یک NULL داشته باشد، نتیجه خالی می‌شود
SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM orders);
```

```sql
-- ✅
SELECT * FROM users u WHERE NOT EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id);
```

**توضیح:** `NOT IN` با NULL در لیست به‌خاطر منطق سه‌وضعیتی نتیجه‌ی غیرمنتظره می‌دهد.

---

### اشتباه ۴: OFFSET بزرگ برای صفحه‌بندی عمیق

```sql
-- ❌
SELECT * FROM events ORDER BY id LIMIT 20 OFFSET 500000;
```

```sql
-- ✅ keyset
SELECT * FROM events WHERE id > 500000 ORDER BY id LIMIT 20;
```

**توضیح:** OFFSET بزرگ همه‌ی ردیف‌های قبلی را اسکن می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- این مفاهیم با **Indexing & Performance** (فصل 3.2) عمیق گره خورده — query بدون index کند است.
- با **Spring Data JPA** (JPQL، query derivation، N+1) و **transactions** ترکیب می‌شود.
- window functions با **PostgreSQL advanced** و گزارش‌گیری.
- keyset pagination با **API design** (cursor-based pagination).
