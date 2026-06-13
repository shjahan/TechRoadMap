# Advanced PostgreSQL — RLS، JSONB، Full-Text، Window Functions، Advisory Locks

> ویژگی‌های پیشرفته‌ی PostgreSQL که آن را از سایر RDBMSها متمایز می‌کند.

---

## 📖 مفاهیم

### Row-Level Security (RLS)

**توضیح:**

RLS کنترل دسترسی در سطح **ردیف** را در خود DB enforce می‌کند: هر کاربر فقط ردیف‌های مجاز خود را می‌بیند، حتی اگر اپ باگ داشته باشد. با `CREATE POLICY` و یک شرط (مثلاً `owner_id = current_setting('app.user_id')`). برای multi-tenancy (shared schema) و امنیت دفاع در عمق.

**مثال کد:**

```sql
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON documents
    USING (tenant_id = current_setting('app.tenant_id')::BIGINT);
-- اپ قبل از query: SET app.tenant_id = '5';
-- هر query خودکار فقط ردیف‌های tenant 5 را می‌بیند
```

**نکات کلیدی:**

- RLS امنیت را در DB enforce می‌کند (دفاع در عمق برای multi-tenancy).
- اپ باید context (tenant_id) را در session set کند.

---

### JSONB Operations & Indexing

**توضیح:**

JSONB با عملگرهای قدرتمند: `@>` (containment)، `->`/`->>` (دسترسی)، `#>>` (nested path)، `?` (key exists)، `||` (merge). index با GIN برای query کارآمد. برای فیلدهای پویا.

**مثال کد:**

```sql
CREATE INDEX idx_meta ON products USING GIN (metadata);
SELECT * FROM products WHERE metadata @> '{"category": "electronics"}'; -- از GIN
SELECT * FROM products WHERE metadata #>> '{specs,ram}' = '16GB';
UPDATE products SET metadata = metadata || '{"discount": 10}';
```

**نکات کلیدی:**

- `@>` از GIN index استفاده می‌کند (سریع).
- برای کلید خاص پرquery، expression index روی `(metadata->>'key')`.

---

### Full-Text Search & Window Functions

**توضیح:**

**Full-text:** `tsvector` (متن tokenize‌شده)، `tsquery` (query)، `@@` (match)، `ts_rank` (relevance). با ستون generated + GIN index. **Window functions** (پیشرفته): running total، LAG/LEAD، RANK، NTILE با `OVER(PARTITION BY ... ORDER BY ...)`.

**مثال کد:**

```sql
-- full-text با ستون generated
ALTER TABLE articles ADD COLUMN tsv tsvector
    GENERATED ALWAYS AS (to_tsvector('english', title || ' ' || body)) STORED;
CREATE INDEX idx_fts ON articles USING GIN (tsv);
SELECT * FROM articles WHERE tsv @@ to_tsquery('english', 'spring & java')
    ORDER BY ts_rank(tsv, to_tsquery('english', 'spring & java')) DESC;
```

**نکات کلیدی:**

- full-text داخلی PostgreSQL برای search ساده کافی است (نیاز Elasticsearch نیست).
- برای search پیچیده/مقیاس بالا، Elasticsearch بهتر.

---

### Advisory Locks

**توضیح:**

قفل‌های application-level که به ردیف خاصی گره نمی‌خورند — برای هماهنگی منطقی (مثل اطمینان از اجرای تک‌نمونه‌ای یک job). `pg_advisory_lock` (session)، `pg_advisory_xact_lock` (transaction)، `pg_try_advisory_lock` (non-blocking).

**مثال کد:**

```sql
-- اطمینان از اجرای تک‌نمونه‌ای یک scheduled job
SELECT pg_try_advisory_lock(hashtext('nightly-report'));
-- اگر true → اجرا کن؛ اگر false → نمونه‌ی دیگری در حال اجراست
```

**نکات کلیدی:**

- advisory lock برای هماهنگی توزیع‌شده‌ی سبک (scheduler، leader election ساده).
- transaction-level خودکار با commit/rollback آزاد می‌شود.

---

## 🎯 سوالات مصاحبه

### سوال ۱: RLS چیست و کجا استفاده می‌شود؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

Row-Level Security کنترل دسترسی در سطح ردیف را در خود PostgreSQL پیاده می‌کند: با یک policy، هر query (حتی `SELECT *`) خودکار فقط ردیف‌های مجاز را برمی‌گرداند بر اساس یک شرط (مثل tenant_id یا owner). کاربرد اصلی: **multi-tenancy با shared schema** (همه‌ی tenantها در یک جدول با ستون tenant_id) که RLS تضمین می‌کند یک tenant داده‌ی دیگری را نبیند، حتی اگر کد اپ فراموش کند فیلتر کند — دفاع در عمق در برابر IDOR. اپ باید context را در session set کند (`SET app.tenant_id`). trade-off: پیچیدگی، و باید مطمئن شوید connection pool context را به‌درستی reset می‌کند (خطر نشت بین requestها در pooled connection).

**نکته مصاحبه:**

Lead به دفاع در عمق و تله‌ی context در connection pool اشاره می‌کند.

---

### سوال ۲: PostgreSQL full-text در برابر Elasticsearch؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

PostgreSQL full-text (`tsvector`/`tsquery` + GIN) برای search ساده تا متوسط کافی و راحت است: بدون زیرساخت جداگانه، در همان transaction و consistency با داده، و برای حجم متوسط خوب. Elasticsearch وقتی برتر است که: حجم داده/query بسیار بالا، نیاز به relevance scoring پیشرفته، fuzzy/typo tolerance، faceted search، aggregation پیچیده، یا زبان‌های متعدد با analyzer سفارشی. trade-off: Elasticsearch زیرساخت جداگانه، sync داده (با CDC)، و eventual consistency می‌آورد. توصیه: با PostgreSQL full-text شروع کنید؛ فقط وقتی واقعاً به قابلیت‌های ES نیاز شد مهاجرت کنید (از over-engineering بپرهیزید).

**نکته مصاحبه:**

Lead «با PG شروع کن، در صورت نیاز ES» را توصیه می‌کند.

---

### سوال ۳: advisory lock کجا مفید است؟

**سطح:** Senior
**تکرار:** کم

**جواب کامل:**

advisory lock یک قفل application-level است که به داده‌ی خاصی گره نمی‌خورد — برای هماهنگی منطقی. کاربرد کلاسیک: اطمینان از اینکه یک scheduled job فقط روی یک instance اجرا می‌شود (در محیط چند instance، همه job را trigger می‌کنند اما فقط آن‌که `pg_try_advisory_lock` را می‌گیرد اجرا می‌کند). همچنین برای leader election ساده، یا serialize کردن یک عملیات خاص بدون قفل کردن ردیف. مزیت بر distributed lock با Redis: اگر قبلاً PostgreSQL دارید، نیازی به زیرساخت اضافه نیست. transaction-level (`pg_advisory_xact_lock`) خودکار آزاد می‌شود که از deadlock ناشی از فراموشی unlock جلوگیری می‌کند.

**نکته مصاحبه:**

Senior به استفاده برای single-instance job و مقایسه با Redis lock اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: RLS context در connection pool reset نشود

```text
❌ tenant_id از request قبلی در pooled connection باقی می‌ماند → نشت داده
✅ context را در ابتدای هر transaction set/reset کنید
```

**توضیح:** pooled connection بین requestها reuse می‌شود.

---

### اشتباه ۲: full-text بدون GIN index

```sql
-- ❌ tsvector محاسبه در هر query، بدون index → کند
WHERE to_tsvector('english', body) @@ to_tsquery('java');
```

```sql
-- ✅ ستون generated + GIN
```

**توضیح:** بدون index و precompute، full-text کند است.

---

### اشتباه ۳: فراموشی unlock در session advisory lock

```sql
-- ❌ session-level lock تا disconnect می‌ماند
SELECT pg_advisory_lock(1);
```

```sql
-- ✅ transaction-level (خودکار آزاد)
SELECT pg_advisory_xact_lock(1);
```

**توضیح:** session lock بدون unlock تا قطع connection می‌ماند.

---

## 🔗 ارتباط با سایر مفاهیم

- RLS با **multi-tenancy (14.3)** و **Security/IDOR (7.1)**.
- JSONB با **MongoDB (4)** (مقایسه‌ی document).
- full-text با **Elasticsearch (17)**.
- advisory lock با **Redis distributed lock (9.1)** و **scheduler**.
