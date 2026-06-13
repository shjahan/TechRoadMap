# Database Design Patterns — Soft Delete، Audit، Optimistic Locking، Multi-tenancy

> الگوهای طراحی DB که در هر سیستم enterprise تکرار می‌شوند.

---

## 📖 مفاهیم

### Soft Delete

**توضیح:**

به‌جای حذف فیزیکی، یک ستون `deleted_at` می‌گذارید و رکوردهای حذف‌شده را با فیلتر مخفی می‌کنید. مزیت: امکان بازیابی، audit، حفظ یکپارچگی ارجاعی. عیب: پیچیدگی query (همه باید فیلتر کنند)، رشد جدول، و مشکل unique constraint (رکورد حذف‌شده هنوز constraint را اشغال می‌کند).

**مثال کد:**

```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMP;
-- Hibernate: @SQLRestriction("deleted_at IS NULL") (یا @Where قدیمی)
-- unique partial برای حل مشکل unique با soft delete:
CREATE UNIQUE INDEX uq_email ON users(email) WHERE deleted_at IS NULL;
```

**نکات کلیدی:**

- partial unique index برای حل تداخل unique با soft delete.
- همه‌ی queryها باید فیلتر `deleted_at IS NULL` داشته باشند (با Hibernate filter خودکار).

---

### Audit Trail

**توضیح:**

ثبت تاریخچه‌ی تغییرات (چه کسی، چه زمانی، چه چیزی). روش‌ها: ستون‌های audit (`created_at`, `updated_at`, `created_by` با Spring Data Auditing)، جدول audit_log جداگانه (با trigger یا app)، یا temporal tables. برای compliance و debugging.

**مثال کد:**

```java
// Spring Data Auditing
@EntityListeners(AuditingEntityListener.class)
class Order {
    @CreatedDate Instant createdAt;
    @LastModifiedDate Instant updatedAt;
    @CreatedBy String createdBy;
}
// @EnableJpaAuditing در config
```

**نکات کلیدی:**

- Spring Data Auditing برای ستون‌های audit ساده.
- جدول audit_log جدا (با JSONB old/new) برای تاریخچه‌ی کامل.

---

### Optimistic Locking

**توضیح:**

ستون `version` که با هر update افزایش می‌یابد؛ update فقط اگر version مطابق باشد موفق می‌شود (در غیر این صورت conflict). برای جلوگیری از lost update در concurrency بدون قفل. در JPA با `@Version`.

**مثال کد:**

```sql
UPDATE products SET name='new', version=version+1
WHERE id=1 AND version=5; -- اگر 0 row → کسی دیگر تغییر داده (conflict)
```

```java
@Entity class Product { @Version Long version; }
// OptimisticLockException هنگام conflict → retry
```

**نکات کلیدی:**

- optimistic برای تداخل کم (read-heavy)؛ نیاز به retry هنگام conflict.
- `@Version` در JPA خودکار این را مدیریت می‌کند.

---

### Multi-tenancy Patterns

**توضیح:**

سه الگو با trade-off isolation/cost:

1. **Separate Database:** هر tenant DB جدا — بهترین isolation، گران‌ترین، مدیریت سخت.
2. **Separate Schema:** یک DB، schema جدا per tenant — تعادل.
3. **Shared Schema:** یک جدول با `tenant_id` — ارزان‌ترین، اما نیاز RLS برای isolation و خطر نشت داده.

**نکات کلیدی:**

- shared schema ارزان اما به RLS/فیلتر دقیق نیاز دارد.
- separate DB برای isolation/compliance بالا اما گران.

---

## 🎯 سوالات مصاحبه

### سوال ۱: soft delete چه مشکلاتی دارد و چطور حل می‌شوند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

مشکلات: (۱) **همه‌ی queryها باید فیلتر کنند** — فراموشی یک فیلتر = نمایش داده‌ی حذف‌شده؛ راه‌حل Hibernate `@SQLRestriction`/filter که خودکار اعمال می‌کند. (۲) **unique constraint** — رکورد حذف‌شده هنوز email را اشغال می‌کند، پس کاربر جدید با همان email نمی‌تواند ثبت شود؛ راه‌حل partial unique index (`WHERE deleted_at IS NULL`). (۳) **رشد جدول و performance** — رکوردهای حذف‌شده انباشته می‌شوند؛ راه‌حل archiving دوره‌ای. (۴) **foreign key** و cascade پیچیده می‌شوند. (۵) گزارش‌ها باید آگاه باشند. به‌خاطر این پیچیدگی‌ها، گاهی به‌جای soft delete سراسری، فقط برای جداول خاص که نیاز بازیابی دارند استفاده می‌شود.

**نکته مصاحبه:**

Senior به partial unique index و فیلتر خودکار اشاره می‌کند.

---

### سوال ۲: multi-tenancy patterns را مقایسه کن.

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

سه الگو روی طیف isolation/cost: **Separate Database** بهترین isolation (داده‌ی tenantها فیزیکی جداست، backup/restore و compliance per-tenant آسان، blast radius محدود) اما گران‌ترین (هزینه‌ی هر DB، migration روی همه، مدیریت پیچیده) — برای enterprise/تعداد کم tenant بزرگ یا الزام compliance. **Separate Schema** تعادل: یک DB با schema per tenant — isolation منطقی خوب، مدیریت متوسط، اما migration روی همه‌ی schemaها و سقف تعداد schema. **Shared Schema** (یک جدول با tenant_id) ارزان‌ترین و مقیاس‌پذیرترین برای تعداد زیاد tenant کوچک، اما isolation ضعیف (نیاز RLS/فیلتر دقیق، خطر نشت داده با یک باگ) و noisy neighbor. انتخاب بر اساس تعداد/اندازه‌ی tenant، الزام compliance، و بودجه.

**نکته مصاحبه:**

Lead trade-off هر سه و عوامل تصمیم را می‌داند.

---

### سوال ۳: optimistic locking چطور lost update را حل می‌کند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

lost update وقتی رخ می‌دهد که دو تراکنش همزمان یک رکورد را می‌خوانند، تغییر می‌دهند، و می‌نویسند؛ نوشتن دومی، تغییر اولی را پاک می‌کند (بدون اینکه بداند). optimistic locking با یک ستون `version` این را می‌گیرد: هنگام update، شرط `WHERE version = <خوانده‌شده>` می‌گذارد و version را افزایش می‌دهد. اگر بین خواندن و نوشتن کسی دیگر version را تغییر داده باشد، update صفر ردیف تحت تأثیر قرار می‌دهد → conflict تشخیص داده می‌شود (در JPA `OptimisticLockException`). اپ می‌تواند retry کند (دوباره بخواند و اعمال کند) یا به کاربر خطا بدهد. مزیت بر pessimistic: بدون قفل، concurrency بالا، مناسب read-heavy با تداخل کم.

**نکته مصاحبه:**

Senior به نیاز retry و مناسب بودن برای تداخل کم اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: soft delete بدون partial unique

```sql
-- ❌ unique معمولی → کاربر جدید با email رکورد حذف‌شده نمی‌تواند ثبت شود
UNIQUE (email)
```

```sql
-- ✅
CREATE UNIQUE INDEX ON users(email) WHERE deleted_at IS NULL;
```

**توضیح:** رکورد soft-deleted هنوز unique را اشغال می‌کند.

---

### اشتباه ۲: shared schema بدون RLS

```text
❌ تکیه بر فیلتر app برای tenant isolation → یک باگ = نشت داده
✅ RLS در DB به‌عنوان دفاع در عمق
```

**توضیح:** isolation در shared schema نباید فقط به کد اپ تکیه کند.

---

### اشتباه ۳: optimistic locking بدون retry

```text
❌ OptimisticLockException مستقیم به کاربر → تجربه‌ی بد
✅ retry محدود قبل از خطا دادن
```

**توضیح:** conflict گذرا را با retry مدیریت کنید.

---

## 🔗 ارتباط با سایر مفاهیم

- optimistic locking با **Spring Data locking (2.4)** و **concurrency**.
- multi-tenancy با **RLS (14.2)** و **Keycloak realm (7.2)**.
- audit با **Spring Data Auditing** و **Event Sourcing (6.1)**.
- soft delete با **Hibernate filters**.
