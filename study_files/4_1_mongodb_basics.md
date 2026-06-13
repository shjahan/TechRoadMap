# MongoDB — مبانی، مدل داده، CRUD

> MongoDB محبوب‌ترین document database است. تصمیم embed در برابر reference مهم‌ترین مهارت طراحی است.

---

## 📖 مفاهیم

### مدل داده — Document-oriented

**توضیح:**

MongoDB داده را به‌صورت **document** (در فرمت BSON — Binary JSON) ذخیره می‌کند. Collection معادل table و Document معادل row است، اما documentها schema-less و می‌توانند ساختار متفاوت داشته باشند. هر document یک `_id` یکتا دارد (پیش‌فرض `ObjectId` که شامل timestamp + machine + counter است، یا می‌تواند custom باشد).

تصمیم اصلی طراحی: **Embedded documents در برابر References**. embedding داده‌ی مرتبط را درون یک document می‌گذارد (یک read، اما document بزرگ‌تر و محدودیت 16MB)؛ referencing شناسه‌ی document دیگر را نگه می‌دارد (مثل foreign key، اما نیاز به چند query یا `$lookup`).

**چرا مهم است:**

مدل‌سازی درست مهم‌ترین تصمیم در MongoDB است و مستقیماً performance را تعیین می‌کند. برخلاف relational، denormalization اینجا رایج و مطلوب است.

**مثال کد:**

```javascript
// Embedded: آدرس داخل user (یک read، اتمیک)
{
  _id: ObjectId("..."),
  name: "Ali",
  addresses: [
    { type: "home", city: "Tehran" },
    { type: "work", city: "Karaj" }
  ]
}

// Reference: order به user اشاره می‌کند (برای داده‌ی بزرگ/مشترک)
{ _id: ObjectId("..."), userId: ObjectId("..."), amount: 5000 }
```

**نکات کلیدی:**

- embed برای داده‌ای که با هم خوانده می‌شود و رابطه‌ی «contains» دارد (one-to-few).
- reference برای داده‌ی بزرگ، مشترک، یا many رابطه.
- محدودیت 16MB برای هر document.

---

### Schema Design Patterns

**توضیح:**

الگوهای طراحی schema در MongoDB:

- **Bucket:** گروه‌بندی داده‌ی time-series در یک document (مثلاً همه‌ی خواندن‌های یک ساعت سنسور) — کاهش تعداد document.
- **Outlier:** مدیریت موارد استثنایی (مثل کاربری با میلیون‌ها follower) جدا از حالت عادی.
- **Computed:** ذخیره‌ی نتیجه‌ی محاسبه (مثل مجموع) به‌جای محاسبه‌ی هر بار.
- **Subset:** نگه‌داری زیرمجموعه‌ی پرکاربرد (مثل ۱۰ نظر اخیر) در document اصلی، بقیه جدا.
- **Extended Reference:** کپی چند فیلد پرکاربرد از document مرتبط برای جلوگیری از join.

**نکات کلیدی:**

- denormalization عمدی برای read performance رایج است.
- trade-off بین read سریع و هزینه‌ی به‌روزرسانی داده‌ی تکراری.

---

### CRUD Operations

**توضیح:**

عملیات اصلی: `insertOne`/`insertMany`, `find`, `updateOne`/`updateMany`, `deleteOne`/`deleteMany`. query با document فیلتر و operatorها. update با operatorهای `$set`, `$inc`, `$push` و … .

**مثال کد:**

```javascript
db.users.insertOne({ name: "Ali", age: 30, status: "active" });

db.users.find({ age: { $gt: 25 } })   // فیلتر
        .sort({ name: 1 })             // مرتب‌سازی (1 صعودی)
        .limit(10);

db.users.updateOne(
  { _id: id },
  { $set: { age: 31 }, $inc: { loginCount: 1 } }
);

db.users.deleteMany({ status: "inactive" });
```

**نکات کلیدی:**

- `find` با projection (`{name: 1}`) فقط فیلدهای لازم را برمی‌گرداند.
- update operatorها atomic روی یک document هستند.

---

### Query Operators

**توضیح:**

- Comparison: `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`, `$in`, `$nin`.
- Logical: `$and`, `$or`, `$not`, `$nor`.
- Element: `$exists`, `$type`.
- Array: `$all` (شامل همه)، `$elemMatch` (یک عنصر همه‌ی شرط‌ها را برآورده کند)، `$size`.
- Update: `$set`, `$unset`, `$inc`, `$push`, `$pull`, `$addToSet`.

**مثال کد:**

```javascript
// $elemMatch: یک سفارش که هم بزرگ‌تر از 100 و هم paid است
db.users.find({
  orders: { $elemMatch: { amount: { $gt: 100 }, status: "paid" } }
});

// $addToSet: افزودن بدون تکرار
db.users.updateOne({ _id: id }, { $addToSet: { tags: "vip" } });
```

**نکات کلیدی:**

- `$elemMatch` برای شرط ترکیبی روی یک عنصر آرایه (نه ترکیب چند عنصر).
- `$addToSet` تکراری اضافه نمی‌کند؛ `$push` می‌کند.

---

## 🎯 سوالات مصاحبه

### سوال ۱: Embedding در برابر Referencing — کِی کدام؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

embedding وقتی مناسب است که: داده‌ی مرتبط همیشه با هم خوانده می‌شود، رابطه «contains/one-to-few» است، و داده‌ی فرزند مستقل query نمی‌شود. مزیت: یک read، atomicity روی یک document. عیب: محدودیت 16MB، document بزرگ، و به‌روزرسانی داده‌ی تکراری سخت.

referencing وقتی مناسب است که: داده‌ی فرزند بزرگ یا نامحدود رشد می‌کند (one-to-many/many)، بین چند parent مشترک است، یا مستقل query می‌شود. مزیت: نرمال، بدون محدودیت اندازه. عیب: نیاز به چند query یا `$lookup` (که گران است).

قاعده‌ی عملی: «داده‌ای که با هم دسترسی می‌شود، با هم ذخیره شود». اغلب ترکیبی (مثل Extended Reference) استفاده می‌شود.

**نکته مصاحبه:**

تمایز Senior: تفکیک one-to-few/one-to-many/one-to-squillions و آگاهی از هزینه‌ی `$lookup`. Follow-up: «اگر آرایه‌ی embedded نامحدود رشد کند چه می‌شود؟» (document به 16MB می‌رسد → باید reference شود).

---

### سوال ۲: MongoDB کِی به‌جای relational؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

MongoDB وقتی مناسب است که: schema پویا/متغیر است، داده طبیعتاً سلسله‌مراتبی/document است (مثل catalog محصول با attribute متغیر)، نیاز به scale افقی آسان (sharding) دارید، و الگوی دسترسی read-heavy با داده‌ی denormalized است. نامناسب وقتی: تراکنش‌های پیچیده‌ی چندموجودیتی، روابط زیاد many-to-many با join مکرر، یا نیاز به consistency قوی و constraint سخت دارید — آن‌جا relational بهتر است. نکته‌ی مهم: «NoSQL یعنی schema-less» سوءتفاهم است؛ schema همچنان وجود دارد، فقط در کد/application enforce می‌شود نه در DB، که می‌تواند خطرناک باشد.

**نکته مصاحبه:**

Lead فریب «MongoDB همیشه scalable‌تر است» را نمی‌خورد و trade-off را می‌فهمد.

---

### سوال ۳: ObjectId چیست و چه اطلاعاتی دارد؟

**سطح:** Mid / Senior
**تکرار:** متوسط

**جواب کامل:**

`ObjectId` یک شناسه‌ی ۱۲ بایتی است: ۴ بایت timestamp (ثانیه از epoch)، ۵ بایت random (machine/process)، و ۳ بایت counter افزایشی. این طراحی تضمین می‌کند بدون هماهنگی مرکزی، شناسه‌های یکتا و تقریباً مرتب بر اساس زمان تولید شوند. مزیت: می‌توان زمان ساخت را از `_id` استخراج کرد و مرتب‌سازی بر `_id` تقریباً مرتب‌سازی زمانی است. در sharding، چون ObjectId تقریباً ترتیبی است، می‌تواند hotspot ایجاد کند (همه‌ی insertها به یک shard).

**نکته مصاحبه:**

Senior به مشکل hotspot در sharding با shard key ترتیبی اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: embedding آرایه‌ی بی‌نهایت رشد

```javascript
// ❌ comments بی‌نهایت رشد می‌کند → 16MB limit
{ _id: 1, post: "...", comments: [ /* میلیون‌ها */ ] }
```

```javascript
// ✅ subset pattern: نظرات اخیر embed، بقیه جدا
{ _id: 1, post: "...", recentComments: [/* ۱۰ تای اخیر */] }
// collection جدا برای comments با postId reference
```

**توضیح:** آرایه‌ی embedded نباید نامحدود رشد کند.

---

### اشتباه ۲: فرض «schema-less یعنی بدون طراحی»

```text
❌ ریختن داده بدون فکر به الگوی دسترسی
✅ طراحی schema بر اساس query patterns (پرتکرارترین queryها)
```

**توضیح:** در MongoDB schema را بر اساس query طراحی می‌کنید (برخلاف relational که بر اساس نرمال‌سازی).

---

### اشتباه ۳: استفاده از `$lookup` به‌جای embedding مناسب

```javascript
// ❌ join گران در هر query
db.orders.aggregate([{ $lookup: { from: "users", ... } }]);
```

```javascript
// ✅ Extended Reference: کپی userName در order
{ _id: 1, userId: 2, userName: "Ali", amount: 5000 }
```

**توضیح:** `$lookup` گران است؛ برای فیلدهای پرکاربرد denormalize کنید.

---

## 🔗 ارتباط با سایر مفاهیم

- مدل document با **PostgreSQL JSONB** (مقایسه) و **API design**.
- schema patterns با **System Design** (access patterns، scale).
- referencing/embedding با **Aggregation `$lookup` (4.2)** و **Spring Data MongoDB (4.5)**.
- ObjectId با **Sharding (4.4)** و shard key design.
