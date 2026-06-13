# MongoDB — Transactions، Replica Set، Sharding

> مفاهیم توزیع‌شده‌ی MongoDB. shard key مهم‌ترین تصمیم scale است و write concern روی consistency اثر می‌گذارد.

---

## 📖 مفاهیم

### Transactions

**توضیح:**

از MongoDB 4.0، multi-document ACID transactions پشتیبانی می‌شود (قبلاً فقط atomicity تک‌document بود). با session شروع می‌شوند. اما هزینه‌ی performance دارند و فلسفه‌ی MongoDB این است که با طراحی درست (embedding داده‌ی مرتبط در یک document) اغلب نیازی به transaction چنددocument نباشد.

**مثال کد:**

```javascript
const session = db.getMongo().startSession();
session.startTransaction();
try {
  db.accounts.updateOne({ _id: "A" }, { $inc: { balance: -100 } }, { session });
  db.accounts.updateOne({ _id: "B" }, { $inc: { balance: 100 } }, { session });
  session.commitTransaction();
} catch (e) {
  session.abortTransaction();
}
```

**نکات کلیدی:**

- transaction چندdocument گران است؛ اول طراحی document را بازبینی کنید.
- atomicity تک‌document همیشه تضمین است (بدون transaction).

---

### Replica Set

**توضیح:**

Replica Set مجموعه‌ای از نودها برای HA و redundancy:

- **Primary:** تنها نودی که write می‌پذیرد.
- **Secondary:** کپی داده از primary (از طریق oplog)، می‌تواند read بدهد.
- **Arbiter:** فقط در election رأی می‌دهد (داده ندارد).

**Read Preference:** `primary` (پیش‌فرض، consistent)، `primaryPreferred`، `secondary` (read scaling اما ممکن stale)، `nearest`. **Write Concern:** `w:1` (فقط primary تأیید)، `w:majority` (اکثریت نودها — امن‌تر)، `j:true` (نوشته‌شدن روی journal). **Oplog** لاگ عملیات است که secondaryها replay می‌کنند. هنگام down شدن primary، election رخ می‌دهد و یک secondary primary می‌شود.

**چرا مهم است:**

write concern مستقیماً trade-off بین durability و latency را تعیین می‌کند. read از secondary می‌تواند stale باشد (eventual consistency).

**مثال کد:**

```javascript
// write امن: اکثریت + journal
db.orders.insertOne(doc, { writeConcern: { w: "majority", j: true } });

// read از secondary برای scaling (با آگاهی از staleness)
db.orders.find().readPref("secondaryPreferred");
```

**نکات کلیدی:**

- `w:majority` durability بهتر اما latency بیشتر.
- read از secondary = احتمال داده‌ی stale (eventual consistency).
- arbiter برای رأی‌گیری در تعداد فرد نودها بدون هزینه‌ی storage.

---

### Sharding

**توضیح:**

Sharding توزیع افقی داده روی چند نود برای scale فراتر از یک ماشین. **Shard Key** مهم‌ترین تصمیم است: تعیین می‌کند داده چطور توزیع شود. انواع: Range sharding (بازه‌ها — برای range query خوب اما خطر hotspot با کلید ترتیبی) و Hash sharding (توزیع یکنواخت اما range query بد). `mongos` یک query router است که request را به shard درست هدایت می‌کند. chunkها بین shardها برای balance مهاجرت می‌کنند.

**hotspot** خطر اصلی: اگر shard key ترتیبی (مثل timestamp یا ObjectId) باشد، همه‌ی writeها به یک shard می‌روند. shard key خوب: cardinality بالا، توزیع یکنواخت write، و هم‌راستا با query patterns.

**چرا مهم است:**

shard key اشتباه را نمی‌توان به‌راحتی عوض کرد و کل scale را خراب می‌کند. این یکی از سخت‌ترین تصمیمات MongoDB است.

**نکات کلیدی:**

- shard key باید cardinality بالا و توزیع یکنواخت write داشته باشد.
- کلید ترتیبی (timestamp/ObjectId) → hotspot.
- shard key را با دقت انتخاب کنید؛ تغییرش بسیار سخت است.

---

## 🎯 سوالات مصاحبه

### سوال ۱: shard key را چطور انتخاب می‌کنی؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

shard key باید سه ویژگی داشته باشد: (۱) **cardinality بالا** — مقادیر متنوع کافی برای توزیع روی shardها (کلید با مقادیر کم مثل boolean بد است). (۲) **توزیع یکنواخت write** — برای جلوگیری از hotspot؛ کلید ترتیبی مثل timestamp یا ObjectId همه‌ی writeها را به یک shard می‌فرستد. (۳) **هم‌راستا با query patterns** — queryها باید بتوانند shard key را شامل کنند تا targeted باشند (به یک shard بروند) نه scatter-gather (به همه). راه‌حل رایج برای کلید ترتیبی: hashed shard key یا compound (مثل `{region, timestamp}`). نکته‌ی مهم: تغییر shard key بسیار سخت است، پس باید از ابتدا درست انتخاب شود.

**نکته مصاحبه:**

تمایز Lead: سه معیار + مشکل hotspot کلید ترتیبی + راه‌حل hashed/compound. Follow-up: «scatter-gather query چیست و چرا بد است؟»

---

### سوال ۲: write concern چیست و چه trade-off دارد؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

write concern تعیین می‌کند قبل از تأیید write، چند نود باید آن را تأیید کنند. `w:1` فقط primary را منتظر می‌ماند (سریع اما اگر primary قبل از replication down شود، آن write گم می‌شود). `w:majority` منتظر تأیید اکثریت نودها می‌ماند (durable حتی با failover، اما latency بیشتر). `j:true` تضمین می‌کند روی journal (disk) نوشته شده. trade-off کلاسیک durability در برابر latency: برای داده‌ی بحرانی (پرداخت) `w:majority, j:true`؛ برای لاگ/متریک کم‌اهمیت `w:1` کافی است. این مستقیماً به CAP و انتخاب C در برابر A مربوط است.

**نکته مصاحبه:**

Senior به رابطه با CAP و انتخاب بر اساس اهمیت داده اشاره می‌کند.

---

### سوال ۳: read از secondary چه ریسکی دارد؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

secondaryها داده را به‌صورت async از primary از طریق oplog replay می‌کنند، پس ممکن است **عقب** (replication lag) باشند. read از secondary می‌تواند داده‌ی **stale** برگرداند — مشکل «read-your-own-writes»: کاربری که چیزی نوشته بلافاصله از secondary بخواند، ممکن است تغییر خودش را نبیند. بنابراین read scaling از secondary فقط برای داده‌ای مناسب است که tolerance به staleness دارد (مثل گزارش، آمار). برای consistency قوی باید از primary خواند. این trade-off همان eventual consistency است.

**نکته مصاحبه:**

Senior به read-your-writes و eventual consistency اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: shard key ترتیبی

```javascript
// ❌ همه‌ی writeها به یک shard (hotspot)
sh.shardCollection("db.events", { createdAt: 1 });
```

```javascript
// ✅ hashed یا compound برای توزیع
sh.shardCollection("db.events", { userId: "hashed" });
```

**توضیح:** کلید ترتیبی توزیع write را نامتعادل می‌کند.

---

### اشتباه ۲: استفاده‌ی بی‌رویه از transaction

```javascript
// ❌ transaction برای کاری که می‌توانست تک‌document باشد
```

```javascript
// ✅ embed داده‌ی مرتبط → atomicity تک‌document رایگان
```

**توضیح:** transaction چندdocument گران است؛ طراحی document را بازبینی کنید.

---

### اشتباه ۳: `w:1` برای داده‌ی بحرانی

```javascript
// ❌ احتمال data loss هنگام failover
db.payments.insertOne(doc, { writeConcern: { w: 1 } });
```

```javascript
// ✅
db.payments.insertOne(doc, { writeConcern: { w: "majority", j: true } });
```

**توضیح:** برای داده‌ی مهم durability را با majority تضمین کنید.

---

## 🔗 ارتباط با سایر مفاهیم

- write concern/read preference با **CAP Theorem** و **consistency models** (System Design).
- sharding با **scalability** و **PostgreSQL partitioning** (مقایسه).
- transactions با **SAGA pattern** (وقتی transaction توزیع‌شده ممکن نیست).
- replica set با **HA** و **PostgreSQL replication**.
