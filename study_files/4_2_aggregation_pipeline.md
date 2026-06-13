# MongoDB Aggregation Pipeline

> Aggregation Pipeline قدرتمندترین ابزار query در MongoDB است؛ معادل GROUP BY و JOIN و تحلیل پیچیده.

---

## 📖 مفاهیم

### مفهوم Pipeline

**توضیح:**

Aggregation Pipeline داده را از طریق دنباله‌ای از مراحل (stage) عبور می‌دهد؛ خروجی هر مرحله ورودی مرحله‌ی بعد است (مثل pipe در Unix یا Stream در Java). هر stage داده را filter، transform، group، یا join می‌کند. این declarative و قابل بهینه‌سازی توسط MongoDB است.

**چرا مهم است:**

برای گزارش‌گیری، تحلیل، و query پیچیده که با `find` ساده ممکن نیست. درک ترتیب stageها برای performance حیاتی است (مثلاً `$match` زودتر = داده‌ی کمتر).

**مثال کد:**

```javascript
db.orders.aggregate([
  { $match: { status: "completed" } },          // فیلتر زود (مهم برای performance)
  { $group: { _id: "$userId", total: { $sum: "$amount" }, count: { $sum: 1 } } },
  { $sort: { total: -1 } },                       // مرتب‌سازی
  { $limit: 10 },                                 // top 10
  { $lookup: {                                    // join با users
      from: "users", localField: "_id",
      foreignField: "_id", as: "user" } },
  { $project: { total: 1, count: 1, "user.name": 1 } } // انتخاب فیلد
]);
```

**نکات کلیدی:**

- `$match` و `$limit` را تا حد ممکن **زود** بگذارید تا داده‌ی کمتری پردازش شود.
- `$match` در ابتدا می‌تواند از index استفاده کند؛ بعد از `$group` نمی‌تواند.

---

### Stageهای مهم

**توضیح:**

- `$match`: فیلتر (مثل WHERE). زود بگذارید.
- `$group`: گروه‌بندی + تجمیع (مثل GROUP BY) با accumulatorها (`$sum`, `$avg`, `$max`, `$push`, `$addToSet`).
- `$project`/`$addFields`: انتخاب/افزودن/تبدیل فیلد.
- `$unwind`: باز کردن آرایه به چند document (یک document به ازای هر عنصر).
- `$lookup`: join با collection دیگر (left outer join).
- `$facet`: اجرای چند pipeline موازی روی یک ورودی (مثل آمار + لیست همزمان).
- `$bucket`/`$bucketAuto`: گروه‌بندی در بازه‌ها (histogram).
- `$graphLookup`: پیمایش recursive (سلسله‌مراتب).
- `$merge`/`$out`: نوشتن نتیجه در collection.

**مثال کد:**

```javascript
// $unwind + $group: شمارش tag در همه‌ی محصولات
db.products.aggregate([
  { $unwind: "$tags" },                       // هر tag یک document
  { $group: { _id: "$tags", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]);

// $facet: آمار و صفحه‌ی نتایج همزمان
db.products.aggregate([
  { $match: { category: "electronics" } },
  { $facet: {
      "totalCount": [{ $count: "count" }],
      "page": [{ $skip: 0 }, { $limit: 20 }]
  }}
]);
```

**نکات کلیدی:**

- `$unwind` برای پردازش آرایه‌ها؛ مراقب انفجار تعداد document باشید.
- `$facet` برای محاسبات موازی (مثل pagination با count).
- `$out`/`$merge` خروجی را persist می‌کند (مثل materialized view).

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا ترتیب stageها در pipeline مهم است؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

ترتیب مستقیماً performance را تعیین می‌کند. `$match` و `$limit` در ابتدای pipeline حجم داده‌ای را که stageهای بعدی پردازش می‌کنند کاهش می‌دهند. مهم‌تر: `$match` در ابتدا می‌تواند از **index** استفاده کند، اما بعد از `$group` یا `$project` (که document را تغییر داده‌اند) دیگر نمی‌تواند و به collection scan روی نتیجه‌ی میانی منجر می‌شود. MongoDB query optimizer برخی reorderها را خودکار انجام می‌دهد (مثل جابه‌جایی `$match` به ابتدا) اما نباید به آن تکیه کرد. قاعده: فیلتر و محدودسازی زود، تبدیل و join دیر.

**نکته مصاحبه:**

تمایز Senior: ربط `$match` زود به استفاده از index. Follow-up: «چطور می‌فهمی pipeline از index استفاده می‌کند؟» (`explain("executionStats")`).

---

### سوال ۲: `$lookup` چیست و چه محدودیتی دارد؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

`$lookup` معادل left outer join است: برای هر document، documentهای منطبق از collection دیگر را در یک آرایه می‌آورد. محدودیت‌ها: گران است (به‌خصوص بدون index روی foreignField)، و فلسفه‌ی MongoDB embedding/denormalization را ترجیح می‌دهد تا نیاز به join کم شود. در sharded collection محدودیت‌هایی دارد. برای join مکرر و پرحجم، MongoDB انتخاب خوبی نیست؛ بهتر است داده را denormalize کنید (Extended Reference). `$lookup` برای گزارش‌گیری گاه‌به‌گاه مناسب است نه مسیر داغ.

**نکته مصاحبه:**

Senior می‌داند join در MongoDB ضدالگوی مسیر داغ است و denormalization ترجیح دارد.

---

### سوال ۳: `$unwind` چه می‌کند و چه خطری دارد؟

**سطح:** Mid / Senior
**تکرار:** متوسط

**جواب کامل:**

`$unwind` یک آرایه را باز می‌کند: هر document با آرایه‌ی N عنصری به N document تبدیل می‌شود که هر کدام یک عنصر آرایه دارند. برای group/تحلیل روی عناصر آرایه لازم است. خطر: انفجار تعداد document؛ اگر document بزرگ با آرایه‌ی بزرگ unwind شود، حجم داده‌ی میانی منفجر می‌شود و حافظه/زمان زیاد می‌برد. باید قبل از `$unwind` با `$match` فیلتر کرد و در صورت امکان از `$filter`/accumulatorها به‌جای unwind استفاده کرد.

**نکته مصاحبه:**

Follow-up: «چطور بدون unwind روی آرایه aggregate کنی؟» (operatorهای آرایه مثل `$size`, `$reduce`).

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: `$match` بعد از `$group`

```javascript
// ❌ ابتدا همه‌چیز group می‌شود، بعد فیلتر → index بی‌استفاده
db.orders.aggregate([
  { $group: { _id: "$userId", total: { $sum: "$amount" } } },
  { $match: { _id: ObjectId("...") } }
]);
```

```javascript
// ✅ فیلتر زود با index
db.orders.aggregate([
  { $match: { userId: ObjectId("...") } },
  { $group: { _id: "$userId", total: { $sum: "$amount" } } }
]);
```

**توضیح:** `$match` زود از index استفاده می‌کند و داده‌ی کمتری group می‌شود.

---

### اشتباه ۲: `$lookup` در مسیر داغ پرترافیک

```javascript
// ❌ join گران در هر request
{ $lookup: { from: "users", ... } }
```

```javascript
// ✅ denormalize فیلدهای لازم در زمان write
```

**توضیح:** join در hot path کند است؛ denormalize کنید.

---

### اشتباه ۳: فراموشی index روی foreignField در `$lookup`

```text
❌ $lookup بدون index روی foreignField → collection scan برای هر document
✅ index روی فیلد join
```

**توضیح:** بدون index، `$lookup` به‌شدت کند می‌شود.

---

## 🔗 ارتباط با سایر مفاهیم

- pipeline با **SQL GROUP BY/JOIN/Window** قابل‌مقایسه است.
- `$match` زود با **Indexing (4.3)** و performance.
- `$lookup`/denormalization با **schema design (4.1)**.
- aggregation با **Spring Data MongoDB `Aggregation` (4.5)**.
