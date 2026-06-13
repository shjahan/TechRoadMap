# Apache Kafka — مفاهیم، Producer/Consumer، Delivery، Streams

> Kafka ستون فقرات سیستم‌های event-driven مدرن است. delivery guarantees و rebalancing سوالات کلیدی Senior هستند.

---

## 📖 مفاهیم

### مفاهیم پایه

**توضیح:**

Kafka یک distributed event streaming platform است (نه فقط message queue). مفاهیم:

- **Topic:** دسته‌بندی منطقی پیام‌ها.
- **Partition:** واحد parallelism؛ هر topic به چند partition تقسیم می‌شود. ترتیب فقط **درون یک partition** تضمین است.
- **Offset:** موقعیت هر پیام در partition.
- **Producer/Consumer:** فرستنده/گیرنده.
- **Consumer Group:** گروهی از consumerها که بار را بین خود تقسیم می‌کنند؛ هر partition به یک consumer در گروه اختصاص می‌یابد.
- **Broker:** سرور Kafka.
- **KRaft** (از Kafka 3.3+) جایگزین ZooKeeper برای metadata شده.

تفاوت کلیدی با queue سنتی: Kafka پیام را پس از مصرف حذف نمی‌کند (log retention)؛ چند consumer group می‌توانند مستقل بخوانند و replay ممکن است.

**چرا مهم است:**

partition و consumer group پایه‌ی scalability و ordering هستند. درک اینکه ترتیب فقط per-partition است برای طراحی درست حیاتی است.

**نکات کلیدی:**

- ترتیب فقط درون یک partition تضمین می‌شود.
- تعداد consumer در یک گروه نباید از تعداد partition بیشتر باشد (مازاد idle می‌ماند).
- Kafka پیام را نگه می‌دارد (retention)، برخلاف queue سنتی.

---

### Producer

**توضیح:**

تنظیمات کلیدی producer:

- **`acks`:** `0` (fire-and-forget، سریع اما احتمال loss)، `1` (تأیید leader)، `all`/`-1` (تأیید همه‌ی in-sync replicas — durable).
- **`retries`** و `retry.backoff.ms`.
- **`linger.ms`** و `batch.size`: batching برای throughput.
- **Idempotent Producer** (`enable.idempotence=true`): جلوگیری از duplicate هنگام retry — exactly-once در سطح producer.
- **Partitioner:** کلید پیام → partition (با hash). پیام‌های با کلید یکسان به یک partition (حفظ ترتیب آن کلید).

**مثال کد:**

```java
Properties props = new Properties();
props.put(ProducerConfig.ACKS_CONFIG, "all");           // durable
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true); // بدون duplicate
props.put(ProducerConfig.LINGER_MS_CONFIG, 10);          // batching
// کلید = userId → همه‌ی رویدادهای یک کاربر در یک partition (ترتیب)
producer.send(new ProducerRecord<>("orders", order.userId(), event));
```

**نکات کلیدی:**

- `acks=all` + idempotence برای durability و بدون duplicate.
- کلید پیام ترتیب per-key را تضمین می‌کند.
- batching (`linger.ms`) throughput را بالا می‌برد.

---

### Consumer

**توضیح:**

- **`auto.offset.reset`:** `earliest` (از ابتدا) یا `latest` (فقط جدید) وقتی offset ذخیره‌شده نیست.
- **`enable.auto.commit`:** اگر true، offset خودکار commit می‌شود — خطر: ممکن پیامی commit شود قبل از پردازش کامل (loss در crash) یا برعکس. برای کنترل، manual commit.
- **commit:** `commitSync` (بلاک‌کننده، مطمئن) در برابر `commitAsync` (سریع، بدون تضمین).
- **Rebalancing:** وقتی consumer اضافه/حذف می‌شود، partitionها بازتوزیع می‌شوند. **Cooperative Rebalancing** (Kafka 2.4+) به‌جای stop-the-world کامل، تدریجی است.

**مثال کد:**

```java
// manual commit بعد از پردازش موفق
props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
while (true) {
    ConsumerRecords<String, Event> records = consumer.poll(Duration.ofMillis(100));
    for (var record : records) {
        process(record.value()); // پردازش
    }
    consumer.commitSync(); // commit بعد از پردازش → at-least-once
}
```

**نکات کلیدی:**

- manual commit بعد از پردازش = at-least-once (احتمال duplicate).
- auto-commit خطر loss یا duplicate دارد.
- consumer باید برای at-least-once، idempotent باشد.

---

### Delivery Guarantees

**توضیح:**

- **At-most-once:** ممکن پیام گم شود (commit قبل از پردازش). بدون duplicate.
- **At-least-once:** پیام گم نمی‌شود اما ممکن duplicate باشد (commit بعد از پردازش، crash بین پردازش و commit). نیاز به idempotent consumer.
- **Exactly-once:** با Kafka Transactions (atomic write + offset commit) و idempotent producer. پیچیده‌تر و کندتر.

در عمل **at-least-once + idempotent consumer** رایج‌ترین و عملی‌ترین انتخاب است.

**نکات کلیدی:**

- exactly-once واقعی گران است؛ at-least-once + idempotency معمول است.
- consumer idempotency با dedup key یا upsert.

---

### Spring Kafka & Kafka Streams

**توضیح:**

**Spring Kafka:** `@KafkaListener` برای مصرف، `KafkaTemplate` برای ارسال، `DefaultErrorHandler` + Dead Letter Topic برای خطا، retry با backoff. **Kafka Streams:** پردازش stream با `KStream` (رویدادها)، `KTable` (state/changelog)، عملیات stateless (`filter`, `map`) و stateful (`groupBy`, `aggregate`, join, windowing) با State Store محلی (RocksDB). **Kafka Connect** + **Debezium** برای CDC.

**مثال کد:**

```java
@KafkaListener(topics = "orders", groupId = "order-processor")
public void handle(OrderEvent event) {
    // idempotent: اگر قبلاً پردازش شده skip
    if (processedRepository.existsById(event.eventId())) return;
    process(event);
    processedRepository.save(new Processed(event.eventId()));
}
```

**نکات کلیدی:**

- Dead Letter Topic برای پیام‌هایی که مکرر fail می‌شوند.
- Kafka Streams برای پردازش stateful؛ Debezium برای CDC.

---

## 🎯 سوالات مصاحبه

### سوال ۱: delivery guarantees را توضیح بده و کدام را در عمل استفاده می‌کنی؟

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

سه سطح: **at-most-once** (offset قبل از پردازش commit می‌شود؛ اگر crash شود پیام گم می‌شود اما هرگز duplicate نیست — برای داده‌ی کم‌اهمیت مثل متریک). **at-least-once** (offset بعد از پردازش commit می‌شود؛ اگر بین پردازش و commit crash شود، پیام دوباره پردازش می‌شود — بدون loss اما با احتمال duplicate). **exactly-once** (با Kafka Transactions: write به topic و commit offset اتمیک می‌شوند، به‌علاوه idempotent producer).

در عمل، **at-least-once + idempotent consumer** رایج‌ترین است چون exactly-once پیچیده، کندتر، و محدود به مرز Kafka است (وقتی side-effect خارجی مثل فراخوانی API دارید، exactly-once Kafka کمکی نمی‌کند). idempotency را با dedup key یا upsert پیاده می‌کنید.

**نکته مصاحبه:**

تمایز Lead: اینکه exactly-once فقط درون Kafka است و برای side-effect خارجی idempotency لازم است. Follow-up: «چطور consumer را idempotent می‌کنی؟»

---

### سوال ۲: ترتیب پیام در Kafka چطور تضمین می‌شود؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

Kafka ترتیب را فقط **درون یک partition** تضمین می‌کند، نه در کل topic. برای اینکه پیام‌های مرتبط به ترتیب پردازش شوند، باید همه به یک partition بروند — که با تعیین **کلید یکسان** (مثلاً userId یا orderId) محقق می‌شود، چون partitioner پیام‌های با کلید یکسان را به یک partition می‌فرستد. trade-off: اگر همه‌ی پیام‌ها یک کلید داشته باشند، همه به یک partition می‌روند و parallelism از بین می‌رود. پس کلید را طوری انتخاب کنید که هم ترتیب لازم را حفظ کند و هم توزیع خوبی بدهد (مثلاً ترتیب per-customer کافی است، نه global). همچنین برای حفظ ترتیب با retry، `max.in.flight.requests` باید محدود شود (یا idempotence فعال باشد).

**نکته مصاحبه:**

Senior به trade-off کلید/parallelism و `max.in.flight` با retry اشاره می‌کند.

---

### سوال ۳: consumer group و rebalancing چیست؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

consumer group مجموعه‌ای از consumerهاست که بار یک topic را بین خود تقسیم می‌کنند؛ هر partition به دقیقاً یک consumer در گروه اختصاص می‌یابد (پس parallelism = تعداد partition). **rebalancing** فرایند بازتوزیع partitionها وقتی consumer اضافه/حذف می‌شود یا crash می‌کند. در rebalancing سنتی (eager)، همه‌ی consumerها partitionهایشان را رها می‌کنند و دوباره تخصیص می‌یابند — یک «stop-the-world» که پردازش را موقتاً متوقف می‌کند. **Cooperative Rebalancing** (Kafka 2.4+) فقط partitionهایی را که باید جابه‌جا شوند منتقل می‌کند، پس وقفه کمتر است. rebalancing مکرر (به‌خاطر پردازش طولانی که از `max.poll.interval` می‌گذرد) مشکل رایج است.

**نکته مصاحبه:**

Senior به cooperative rebalancing و مشکل rebalancing مکرر اشاره می‌کند. Follow-up: «چرا consumer از گروه خارج می‌شود؟» (heartbeat یا max.poll.interval).

---

### سوال ۴: Kafka در برابر RabbitMQ — کِی کدام؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

Kafka یک log توزیع‌شده با throughput بسیار بالا، retention پیام (replay)، و چند consumer group مستقل است؛ برای event streaming، event sourcing، حجم بالا، و pipeline داده ایده‌آل. RabbitMQ یک message broker سنتی (smart broker) با routing پیچیده (exchange types)، per-message ack، و الگوهای کلاسیک (work queue، RPC) است؛ برای task distribution، routing پیچیده، و پیام‌های با priority. تفاوت کلیدی: Kafka پیام را نگه می‌دارد و consumer offset را مدیریت می‌کند (dumb broker, smart consumer)؛ RabbitMQ پیام را پس از ack حذف می‌کند (smart broker). برای حجم بالا و replay → Kafka؛ برای routing پیچیده و task queue → RabbitMQ.

**نکته مصاحبه:**

Lead به «smart broker در برابر smart consumer» و retention اشاره می‌کند.

---

### سوال ۵: KStream در برابر KTable چیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`KStream` یک stream از رویدادهای مستقل است؛ هر رکورد یک رویداد جدید (مثل «کاربر X کلیک کرد»). `KTable` یک changelog/snapshot از آخرین مقدار به ازای هر کلید است (مثل «آخرین وضعیت کاربر X»)؛ رکورد جدید با کلید موجود، مقدار قبلی را به‌روز می‌کند (upsert) نه اینکه رویداد جدید باشد. تشبیه: KStream مثل INSERT-only log، KTable مثل جدول با UPDATE. join بین این‌ها قدرتمند است (مثل enrich کردن stream رویداد با state از table). GlobalKTable نسخه‌ای است که کاملاً در هر instance replicate می‌شود (برای lookup table کوچک).

**نکته مصاحبه:**

Senior تشبیه stream/table (INSERT log در برابر upsert) را می‌دهد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: انتظار ترتیب global

```text
❌ فرض اینکه پیام‌ها در کل topic مرتب می‌رسند
✅ ترتیب فقط per-partition؛ از کلید برای گروه‌بندی استفاده کنید
```

**توضیح:** بدون کلید مناسب، ترتیب پیام‌های مرتبط تضمین نیست.

---

### اشتباه ۲: auto-commit با پردازش طولانی

```java
// ❌ ممکن پیام commit شود قبل از پردازش کامل → loss
props.put(ENABLE_AUTO_COMMIT_CONFIG, true);
```

```java
// ✅ manual commit بعد از پردازش
props.put(ENABLE_AUTO_COMMIT_CONFIG, false);
// ... process(); consumer.commitSync();
```

**توضیح:** auto-commit زمان‌بندی commit را از پردازش جدا می‌کند.

---

### اشتباه ۳: consumer بیشتر از partition

```text
❌ ۱۰ consumer برای topic با ۳ partition → ۷ تا idle
✅ تعداد partition >= consumer مورد نظر
```

**توضیح:** هر partition فقط یک consumer در گروه؛ مازاد بی‌کار می‌ماند.

---

### اشتباه ۴: consumer بدون idempotency در at-least-once

```text
❌ پردازش duplicate → دوبار side-effect (مثلاً دوبار ایمیل)
✅ dedup با eventId یا upsert
```

**توضیح:** at-least-once یعنی duplicate ممکن است؛ consumer باید idempotent باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- Kafka با **Event-Driven Architecture، Outbox، CDC (6.1)** عمیق مرتبط است.
- idempotency با **Idempotency (19.2)** و **delivery guarantees**.
- Kafka Streams با **CQRS** و **stream processing**.
- Spring Kafka با **Spring Boot** و **resilience (DLT، retry)**.
- Debezium با **PostgreSQL replication** و **Change Streams (MongoDB)**.
