# MongoDB Indexing

> ایندکس‌گذاری در MongoDB مشابه relational اما با ویژگی‌های خاص document (multikey، TTL). تفاوت dev و production اینجاست.

---

## 📖 مفاهیم

### انواع Index

**توضیح:**

- **Single field:** روی یک فیلد.
- **Compound:** روی چند فیلد؛ leftmost prefix rule مثل relational.
- **Multikey:** خودکار وقتی روی فیلد آرایه‌ای index می‌زنید — برای هر عنصر آرایه یک entry.
- **Text:** برای full-text search ساده.
- **Geospatial:** برای query مکانی (`2dsphere`).
- **Hashed:** برای sharding با توزیع یکنواخت.
- **TTL:** auto-delete document بعد از مدت مشخص (برای session، log، cache).
- **Sparse:** فقط documentهایی که فیلد را دارند index می‌شوند (برای فیلد اختیاری).
- **Partial:** فقط documentهایی که شرط را برآورده می‌کنند.

**چرا مهم است:**

بدون index، MongoDB collection scan می‌کند (کند). TTL index یک ابزار قدرتمند برای پاکسازی خودکار است. multikey رفتار خاصی دارد که باید درک شود.

**مثال کد:**

```javascript
// compound index
db.orders.createIndex({ userId: 1, createdAt: -1 });

// TTL: حذف خودکار session بعد از 1 ساعت
db.sessions.createIndex({ createdAt: 1 }, { expireAfterSeconds: 3600 });

// partial: فقط active users
db.users.createIndex({ email: 1 }, { partialFilterExpression: { active: true } });

// multikey خودکار روی آرایه
db.products.createIndex({ tags: 1 }); // tags یک آرایه است
```

**نکات کلیدی:**

- TTL index برای session/log/cache — خودکار پاک می‌کند.
- multikey روی آرایه خودکار است؛ نمی‌توان دو فیلد آرایه‌ای در یک compound index داشت.
- partial/sparse برای فیلدهای اختیاری → index کوچک‌تر.

---

### Covered Queries & explain

**توضیح:**

اگر همه‌ی فیلدهای مورد نیاز (در query و projection) در index باشند، MongoDB **covered query** انجام می‌دهد: بدون مراجعه به document، فقط از index — سریع. `explain("executionStats")` query plan را نشان می‌دهد: `IXSCAN` (index scan، خوب) در برابر `COLLSCAN` (collection scan، بد)، تعداد document بررسی‌شده در برابر بازگشتی، و آیا covered بوده.

**مثال کد:**

```javascript
db.users.find({ status: "active" }, { _id: 0, name: 1 })
        .explain("executionStats");
// به دنبال: stage: "IXSCAN"، totalDocsExamined کم، COLLSCAN نباشد
```

**نکات کلیدی:**

- نسبت `totalDocsExamined` به `nReturned` نزدیک به ۱ یعنی index خوب کار می‌کند.
- `COLLSCAN` روی collection بزرگ یعنی index لازم است.

---

### Background vs Foreground & Index Stats

**توضیح:**

ساخت index در نسخه‌های قدیمی foreground بود (collection را قفل می‌کرد) یا background (کندتر اما بدون قفل). در نسخه‌های جدید (4.2+) ساخت index بهینه‌تر شده. `$indexStats` نشان می‌دهد هر index چقدر استفاده شده — برای یافتن indexهای بی‌استفاده که فضا و سرعت write را هدر می‌دهند.

**نکات کلیدی:**

- index بی‌استفاده را حذف کنید (با `$indexStats` پیدا کنید).
- ساخت index روی collection بزرگ در production را با احتیاط انجام دهید.

---

## 🎯 سوالات مصاحبه

### سوال ۱: TTL index چیست و کجا استفاده می‌شود؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

TTL (Time To Live) index یک single-field index روی یک فیلد date است با `expireAfterSeconds`. یک background thread (هر ~۶۰ ثانیه) documentهایی را که از زمان تعیین‌شده گذشته‌اند خودکار حذف می‌کند. کاربردها: session expiry، log retention، cache entry، OTP/token موقت، و داده‌ی موقت. مزیت: نیازی به cron job دستی برای پاکسازی نیست. محدودیت‌ها: دقت در سطح دقیقه است نه ثانیه (به‌خاطر دوره‌ی پاکسازی)، روی compound index کار نمی‌کند، و حذف بار I/O ایجاد می‌کند.

**نکته مصاحبه:**

Senior به دقت تقریبی (نه دقیقاً لحظه‌ای) و بار I/O حذف اشاره می‌کند.

---

### سوال ۲: چرا query در dev سریع و در production کند است؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

دلیل اصلی: در dev داده کم است، پس collection scan (`COLLSCAN`) هم سریع به‌نظر می‌رسد و نبود index پنهان می‌ماند. در production با میلیون‌ها document، همان query بدون index فاجعه می‌شود. راه تشخیص: `explain("executionStats")` که `COLLSCAN` و `totalDocsExamined` بالا را نشان می‌دهد. علل دیگر: working set بزرگ‌تر از RAM (page fault به disk)، index‌ای که در RAM جا نمی‌شود، یا الگوی داده‌ی متفاوت. راه‌حل: index مناسب بر اساس query واقعی، و تست با حجم داده‌ی نزدیک به production.

**نکته مصاحبه:**

Senior روی تست با حجم واقعی و `explain` تأکید می‌کند.

---

### سوال ۳: multikey index چه محدودیتی دارد؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

multikey index خودکار وقتی یک فیلد index‌شده آرایه است ایجاد می‌شود و برای هر عنصر آرایه یک entry می‌سازد. محدودیت اصلی: در یک compound index نمی‌توان روی **دو فیلد آرایه‌ای** index زد (چون منجر به انفجار ترکیبی entryها می‌شود — حاصل‌ضرب دکارتی). همچنین multikey index بزرگ‌تر است و برخی بهینه‌سازی‌ها (مثل index-only sort) روی آن محدودند. باید آگاه بود که index روی فیلد آرایه می‌تواند سریع رشد کند.

**نکته مصاحبه:**

Senior محدودیت «دو فیلد آرایه‌ای در یک compound» را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: نبود index → COLLSCAN

```javascript
// ❌ بدون index روی email
db.users.find({ email: "a@b.com" }); // COLLSCAN روی میلیون‌ها document
```

```javascript
// ✅
db.users.createIndex({ email: 1 }, { unique: true });
```

**توضیح:** فیلدهای پرquery باید index داشته باشند.

---

### اشتباه ۲: index بیش از حد

```javascript
// ❌ index روی هر فیلد → write کند، RAM پر
```

```javascript
// ✅ index بر اساس query واقعی؛ بی‌استفاده‌ها را با $indexStats حذف کنید
```

**توضیح:** هر index هزینه‌ی write و حافظه دارد.

---

### اشتباه ۳: ترتیب اشتباه در compound index

```javascript
// ❌ برای WHERE status + sort createdAt
db.orders.createIndex({ createdAt: 1, status: 1 });
```

```javascript
// ✅ equality اول، sort/range بعد
db.orders.createIndex({ status: 1, createdAt: -1 });
```

**توضیح:** ESR rule (Equality, Sort, Range) برای ترتیب compound index.

---

## 🔗 ارتباط با سایر مفاهیم

- indexing با **relational indexing (3.2)** قابل‌مقایسه (leftmost prefix، covered).
- explain با **query optimization** و performance.
- TTL index با **Redis expiry** و **caching**.
- hashed index با **Sharding (4.4)**.
