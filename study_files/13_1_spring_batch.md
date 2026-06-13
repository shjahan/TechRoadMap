# Spring Batch — Job، Step، Chunk Processing، Scaling

> Spring Batch برای پردازش حجیم داده (ETL، گزارش، migration) استاندارد است. chunk processing و restart مفاهیم کلیدی‌اند.

---

## 📖 مفاهیم

### مفاهیم اصلی

**توضیح:**

Spring Batch چارچوب پردازش batch است. سلسله‌مراتب: **Job** (کل عملیات) → **Step** (مرحله) → **ItemReader** (خواندن)/**ItemProcessor** (پردازش)/**ItemWriter** (نوشتن). مدل **chunk-oriented**: Read N آیتم → Process N → Write N (در یک transaction) — به‌جای پردازش یک‌به‌یک یا همه‌باهم. این تعادل memory و performance می‌دهد و امکان commit دوره‌ای را فراهم می‌کند.

**چرا مهم است:**

برای پردازش میلیون‌ها رکورد بدون OOM، با امکان restart و monitoring. در سیستم‌های enterprise (بانک، گزارش) رایج است.

**مثال کد:**

```java
@Bean
public Step importStep(JobRepository jobRepository,
                       PlatformTransactionManager txManager,
                       ItemReader<User> reader, ItemWriter<User> writer) {
    return new StepBuilder("importStep", jobRepository)
        .<User, User>chunk(100, txManager)   // 100 آیتم در هر transaction
        .reader(reader)
        .processor(userProcessor())
        .writer(writer)
        .faultTolerant()
        .skipLimit(10).skip(ValidationException.class) // تحمل خطا
        .build();
}
```

**نکات کلیدی:**

- chunk size تعادل memory/performance؛ هر chunk یک transaction.
- fault tolerance با skip/retry برای رکوردهای مشکل‌دار.

---

### Readers، Scaling، Restart

**توضیح:**

**Readers:** `FlatFileItemReader` (CSV)، `JdbcPagingItemReader` (DB با صفحه‌بندی، نه cursor برای داده‌ی بزرگ)، `JpaPagingItemReader`, `KafkaItemReader`. **Scaling:** Multi-threaded Step، Parallel Steps، **Partitioning** (تقسیم داده، workerهای موازی)، Remote Chunking. **Restart:** `JobRepository` متادیتا (JobExecution، StepExecution) را در DB ذخیره می‌کند، پس job بعد از crash از جایی که متوقف شد ادامه می‌یابد. `@StepScope`/`@JobScope` برای late binding پارامترها.

**نکات کلیدی:**

- `JdbcPagingItemReader` برای داده‌ی بزرگ (cursor reader کل result را نگه می‌دارد).
- restart از JobRepository — برای job طولانی حیاتی.
- partitioning برای موازی‌سازی روی حجم بالا.

---

## 🎯 سوالات مصاحبه

### سوال ۱: chunk-oriented processing چه مزیتی دارد؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

به‌جای خواندن کل داده در حافظه (OOM برای میلیون‌ها رکورد) یا پردازش یک‌به‌یک با یک transaction به ازای هر رکورد (کند، overhead زیاد)، chunk processing N رکورد را می‌خواند، پردازش می‌کند، و در یک transaction می‌نویسد. مزایا: (۱) **memory کنترل‌شده** — فقط N رکورد در حافظه. (۲) **performance** — commit دوره‌ای به‌جای هر رکورد. (۳) **fault tolerance** — اگر chunk fail شود، فقط همان chunk rollback می‌شود و با skip/retry قابل‌مدیریت است. (۴) **restart** — می‌داند تا کدام chunk پیش رفته. انتخاب chunk size یک trade-off است: بزرگ‌تر = throughput بهتر اما memory و rollback بیشتر هنگام خطا.

**نکته مصاحبه:**

Senior trade-off chunk size را می‌فهمد.

---

### سوال ۲: چطور یک Spring Batch job را restart-able می‌کنی؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Spring Batch به‌صورت داخلی restart را پشتیبانی می‌کند: `JobRepository` وضعیت اجرا (JobExecution، StepExecution، تعداد رکورد پردازش‌شده، آخرین offset) را در DB ذخیره می‌کند. اگر job با همان JobParameters دوباره اجرا شود (و قبلاً FAILED بوده)، از آخرین chunk موفق ادامه می‌یابد نه از ابتدا. شرایط: reader باید stateful و قابل‌restart باشد (مثل `JdbcPagingItemReader` که offset را ذخیره می‌کند)، JobParameters باید یکتا و یکسان باشد، و step نباید `allowStartIfComplete` باشد مگر بخواهید همیشه از نو. برای job غیرrestartable می‌توان آن را غیرفعال کرد. این برای job طولانی روی میلیون‌ها رکورد حیاتی است (نخواهید از صفر شروع کنید).

**نکته مصاحبه:**

Senior به نقش JobRepository و reader stateful اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: cursor reader برای داده‌ی بزرگ

```java
// ❌ کل result set / اتصال طولانی
JdbcCursorItemReader
```

```java
// ✅ paging reader
JdbcPagingItemReader
```

**توضیح:** paging reader برای داده‌ی بزرگ مقیاس‌پذیرتر است.

---

### اشتباه ۲: chunk size خیلی بزرگ

```java
// ❌ OOM و rollback بزرگ هنگام خطا
.chunk(1_000_000, txManager)
```

```java
// ✅ معقول
.chunk(100, txManager)
```

**توضیح:** chunk بزرگ memory و هزینه‌ی rollback را بالا می‌برد.

---

## 🔗 ارتباط با سایر مفاهیم

- Spring Batch با **transactions (2.4)** و **JPA**.
- partitioning با **concurrency** و **scaling**.
- KafkaItemReader با **Kafka (8.1)**.
- restart با **idempotency (19.2)**.
