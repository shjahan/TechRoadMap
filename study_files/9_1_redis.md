# Redis — Data Types، Patterns، Persistence، HA، Spring Cache

> Redis محبوب‌ترین in-memory store است. data structureها و الگوهای caching/lock در مصاحبه‌ها پرسیده می‌شوند.

---

## 📖 مفاهیم

### Data Types

**توضیح:**

Redis یک in-memory data structure store است (نه فقط key-value ساده). انواع:

- **String:** ساده‌ترین؛ `SET`, `GET`, `INCR` (atomic counter)، `EXPIRE`/`TTL`.
- **List:** لیست پیوندی؛ `LPUSH`/`RPUSH`, `LRANGE`, `BLPOP` (blocking — برای job queue).
- **Set:** مجموعه‌ی یکتا؛ `SADD`, `SINTER` (اشتراک)، `SUNION`.
- **Sorted Set (ZSet):** عناصر با score مرتب؛ `ZADD`, `ZRANGE`, `ZRANGEBYSCORE` — برای leaderboard، rate limiting، priority queue.
- **Hash:** map فیلد→مقدار؛ `HSET`, `HGET` — برای object.
- **Stream:** append-only log مشابه Kafka سبک.
- **Pub/Sub:** messaging real-time.
- **HyperLogLog:** تخمین تعداد یکتا با حافظه‌ی کم.
- **Bitmap:** عملیات bitwise.

**چرا مهم است:**

انتخاب data type درست الگوی استفاده را تعیین می‌کند. Sorted Set ابزار قدرتمندی برای leaderboard و rate limiting است.

**مثال کد:**

```bash
# atomic counter با expiry (مثلاً rate limit شمارنده)
INCR api:user:123:count
EXPIRE api:user:123:count 60

# leaderboard با Sorted Set
ZADD leaderboard 1500 "player1"
ZREVRANGE leaderboard 0 9 WITHSCORES  # top 10
```

**نکات کلیدی:**

- Redis single-threaded است (برای دستورات data)؛ عملیات atomic بدون lock.
- Sorted Set برای leaderboard، rate limiting، delayed queue.
- همیشه برای cache TTL بگذارید.

---

### Patterns

**توضیح:**

- **Session Store:** session توزیع‌شده برای horizontal scaling.
- **Rate Limiting:** با sliding window (Sorted Set) یا counter + expire.
- **Distributed Lock:** `SET key value NX PX ttl` (atomic، با TTL برای جلوگیری از deadlock). برای دقت بالا، **Redlock** algorithm.
- **Cache-Aside / Write-Through.**
- **Leaderboard:** Sorted Set.
- **Job Queue:** List با `BLPOP`.
- **Pub/Sub:** messaging سبک.

**مثال کد:**

```java
// distributed lock با SET NX PX
String token = UUID.randomUUID().toString();
Boolean acquired = redis.opsForValue()
    .setIfAbsent("lock:order:1", token, Duration.ofSeconds(10)); // NX + PX
if (Boolean.TRUE.equals(acquired)) {
    try { /* بخش بحرانی */ }
    finally {
        // آزادسازی امن: فقط اگر token خودمان است (با Lua برای atomicity)
    }
}
```

**نکات کلیدی:**

- distributed lock باید TTL داشته باشد (وگرنه crash holder = deadlock).
- آزادسازی lock باید atomic و فقط توسط صاحب باشد (Lua script).
- Redlock برای محیط multi-node اما محل بحث است.

---

### Persistence

**توضیح:**

Redis in-memory است اما می‌تواند persist کند:

- **RDB (Snapshot):** dump دوره‌ای point-in-time. کم‌سربار، startup سریع، اما احتمال data loss بین snapshotها.
- **AOF (Append Only File):** هر write را log می‌کند. کامل‌تر (کمتر loss)، اما کندتر و فایل بزرگ‌تر.
- **Hybrid** (Redis 4+): RDB + AOF.

**نکات کلیدی:**

- RDB برای backup سریع؛ AOF برای durability بهتر.
- Redis معمولاً به‌عنوان cache (نه source of truth) استفاده می‌شود؛ data loss قابل‌تحمل.

---

### High Availability

**توضیح:**

- **Sentinel:** automatic failover برای primary/replica (monitoring + election).
- **Redis Cluster:** sharding خودکار با ۱۶۳۸۴ hash slot؛ scale افقی.
- **Valkey:** fork متن‌باز Redis پس از تغییر license (۲۰۲۴).

**نکات کلیدی:**

- Sentinel برای HA؛ Cluster برای sharding + HA.
- replication async است → احتمال loss کوچک هنگام failover.

---

### Spring Cache

**توضیح:**

Spring abstraction روی cache با annotation: `@Cacheable` (نتیجه را cache می‌کند)، `@CachePut` (همیشه اجرا و cache را به‌روز می‌کند)، `@CacheEvict` (حذف از cache). با Redis به‌عنوان provider.

**مثال کد:**

```java
@Cacheable(value = "users", key = "#id")
public User findById(Long id) { return repository.findById(id).orElseThrow(); }

@CacheEvict(value = "users", key = "#user.id")
public void update(User user) { repository.save(user); }
```

**نکات کلیدی:**

- `@Cacheable` با AOP کار می‌کند → self-invocation اعمال نمی‌شود.
- TTL را در پیکربندی cache manager تنظیم کنید.
- کلید cache را دقیق تعریف کنید تا collision نشود.

---

## 🎯 سوالات مصاحبه

### سوال ۱: distributed lock با Redis چطور پیاده می‌کنی و چه تله‌هایی دارد؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

اصل: `SET key value NX PX ttl` — `NX` یعنی فقط اگر کلید وجود ندارد (atomic acquire)، `PX ttl` یعنی expiry خودکار. value یک token یکتا (UUID) است تا فقط صاحب بتواند آزاد کند. تله‌ها: (۱) **بدون TTL** اگر holder crash کند، lock برای همیشه می‌ماند (deadlock). (۲) **آزادسازی غیراتمیک**: اگر فقط `DEL key` بزنید بدون چک token، ممکن lock کسی دیگر را که در این فاصله گرفته آزاد کنید — باید با Lua script (چک token + del اتمیک) آزاد کنید. (۳) **TTL کوتاه‌تر از کار**: اگر کار طولانی‌تر از TTL شود، lock منقضی و دو نفر همزمان وارد می‌شوند — راه‌حل: watchdog که TTL را تمدید می‌کند (مثل Redisson). (۴) در محیط multi-master، Redlock مطرح است اما بحث‌برانگیز.

**کد توضیحی:**

```lua
-- آزادسازی atomic: فقط اگر token خودمان باشد
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else return 0 end
```

**نکته مصاحبه:**

تمایز Lead: token برای آزادسازی امن، Lua برای atomicity، watchdog برای کار طولانی. Follow-up: «Redlock چرا بحث‌برانگیز است؟»

---

### سوال ۲: cache invalidation strategy و مشکلاتش؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

«cache invalidation یکی از دو مسئله‌ی سخت علوم کامپیوتر است». استراتژی‌ها: (۱) **TTL-based**: ساده، اما داده‌ی stale تا expiry. (۲) **write-through/write-around**: هنگام نوشتن، cache را به‌روز/حذف کنید — consistency بهتر اما coupling. (۳) **event-based**: با تغییر داده، event منتشر و cache invalidate شود (با Kafka/pub-sub در سیستم توزیع‌شده). مشکلات: stale data، race condition بین update DB و cache (یک thread قدیمی را می‌نویسد بعد از جدید)، و cache stampede هنگام invalidation همزمان. راه‌حل race: حذف cache به‌جای update (lazy reload)، و TTL به‌عنوان safety net. در سیستم توزیع‌شده، invalidation همه‌ی nodeها چالش است (pub/sub).

**نکته مصاحبه:**

Lead به race condition update و راه‌حل «delete به‌جای update» اشاره می‌کند.

---

### سوال ۳: چرا Redis single-threaded است و چطور سریع است؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Redis دستورات data را در یک thread واحد پردازش می‌کند (هرچند I/O و برخی کارها در نسخه‌های جدید multi-thread است). دلیل سرعت با وجود single-thread: (۱) همه‌چیز in-memory است (بدون disk I/O در مسیر اصلی). (۲) single-thread یعنی بدون lock، context switch، یا race condition — هر دستور atomic است که هم سریع و هم ساده است. (۳) event loop غیرمسدودکننده (epoll). (۴) data structureهای بهینه. مزیت جانبی: عملیات مثل `INCR` ذاتاً atomic‌اند بدون نیاز به lock. محدودیت: یک دستور کند (مثل `KEYS *` روی dataset بزرگ) کل سرور را بلاک می‌کند — باید از دستورات O(n) بزرگ پرهیز کرد.

**نکته مصاحبه:**

Senior به atomicity رایگان و خطر دستورات بلاک‌کننده (`KEYS *`) اشاره می‌کند.

---

### سوال ۴: RDB در برابر AOF — کدام؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

RDB یک snapshot دوره‌ای point-in-time است: فایل فشرده، startup سریع، کم‌سربار، اما اگر بین دو snapshot crash شود، داده‌ی آن بازه گم می‌شود. AOF هر دستور write را در فایل log می‌کند: durability بهتر (بسته به fsync policy، حداکثر ۱ ثانیه loss)، اما فایل بزرگ‌تر و startup کندتر (replay). Redis 4+ از hybrid پشتیبانی می‌کند (RDB base + AOF برای تغییرات اخیر). انتخاب: اگر Redis به‌عنوان cache است و loss قابل‌تحمل، RDB کافی؛ اگر به‌عنوان source of truth یا durability مهم است، AOF (یا hybrid). اکثر کاربردهای cache با RDB راحت‌اند.

**نکته مصاحبه:**

Senior به نقش Redis (cache در برابر datastore) برای انتخاب اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: distributed lock بدون TTL

```java
// ❌ اگر holder crash کند، lock ابدی
redis.opsForValue().setIfAbsent("lock", token);
```

```java
// ✅ با TTL
redis.opsForValue().setIfAbsent("lock", token, Duration.ofSeconds(10));
```

**توضیح:** بدون TTL، crash منجر به deadlock می‌شود.

---

### اشتباه ۲: `KEYS *` در production

```bash
# ❌ کل سرور را بلاک می‌کند (O(n))
KEYS user:*
```

```bash
# ✅ SCAN با cursor (non-blocking)
SCAN 0 MATCH user:* COUNT 100
```

**توضیح:** `KEYS` single-thread را روی dataset بزرگ بلاک می‌کند.

---

### اشتباه ۳: cache بدون TTL

```java
// ❌ داده‌ی stale برای همیشه + رشد نامحدود حافظه
redis.opsForValue().set(key, value);
```

```java
// ✅
redis.opsForValue().set(key, value, Duration.ofMinutes(10));
```

**توضیح:** بدون TTL، حافظه پر می‌شود و stale می‌ماند.

---

### اشتباه ۴: update cache به‌جای delete

```text
❌ update cache هنگام write → race condition (نوشتن مقدار قدیمی روی جدید)
✅ delete cache → بار بعد از DB lazy reload
```

**توضیح:** delete از race condition جلوگیری می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- caching strategy با **System Design (6.2)** (cache-aside، stampede).
- distributed lock با **PostgreSQL advisory lock (3.3)** و **concurrency**.
- Spring Cache با **AOP/`@Cacheable` (2.1, 2.4)**.
- rate limiting با **API Gateway (2.6)** و **System Design**.
- JWT blacklist با **Security (7.2)**.
