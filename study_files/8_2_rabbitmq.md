# RabbitMQ — Exchanges، Patterns، Reliability

> RabbitMQ یک message broker با routing قدرتمند است. درک exchange types و reliability مهم است.

---

## 📖 مفاهیم

### مفاهیم پایه — Exchange Types

**توضیح:**

در RabbitMQ، producer به **exchange** پیام می‌فرستد (نه مستقیم به queue)؛ exchange بر اساس قوانین routing، پیام را به یک یا چند **queue** هدایت می‌کند. انواع exchange:

- **Direct:** بر اساس تطابق دقیق routing key.
- **Topic:** بر اساس الگوی routing key با wildcard (`*` یک کلمه، `#` چند کلمه).
- **Fanout:** به همه‌ی queueهای bound (broadcast، بدون توجه به key).
- **Headers:** بر اساس header به‌جای routing key.

**Binding** queue را به exchange با routing key وصل می‌کند. **Virtual Host** برای isolation منطقی.

**چرا مهم است:**

routing انعطاف‌پذیر RabbitMQ مزیت اصلی آن بر Kafka است. انتخاب exchange type درست الگوی پیام‌رسانی را تعیین می‌کند.

**نکات کلیدی:**

- producer به exchange می‌فرستد نه queue.
- Topic exchange برای routing انعطاف‌پذیر با wildcard.
- Fanout برای pub/sub broadcast.

---

### Messaging Patterns

**توضیح:**

- **Work Queue:** توزیع task بین چند worker (load balancing) — هر پیام به یک worker.
- **Publish/Subscribe:** Fanout exchange، هر subscriber کپی می‌گیرد.
- **Routing:** Direct exchange با routing key.
- **Topics:** Topic exchange با wildcard (مثلاً `logs.error.*`).
- **RPC:** request/reply با correlation id و reply queue.

**مثال کد:**

```java
// Spring AMQP: مصرف
@RabbitListener(queues = "orders.processing")
public void handleOrder(OrderMessage message) {
    process(message);
}

// ارسال با routing key
rabbitTemplate.convertAndSend("orders.exchange", "order.created", message);
```

**نکات کلیدی:**

- Work Queue برای توزیع بار بین workerها.
- Topic exchange برای سناریوهای routing پیچیده.

---

### Reliability

**توضیح:**

- **Publisher Confirms:** broker دریافت پیام را ack می‌کند (تضمین رسیدن به broker).
- **Consumer Acknowledgements:** `basicAck` (پردازش موفق)، `basicNack`/`basicReject` (شکست؛ با requeue یا به DLX). manual ack برای کنترل.
- **Dead Letter Exchange (DLX):** پیام‌هایی که reject شده، expire شده، یا queue پر است به DLX می‌روند — برای بررسی و retry.
- **Quorum Queues** (توصیه‌شده، مبتنی بر Raft) در برابر Classic Queues — durability و consistency بهتر.
- **Persistence:** durable exchange + durable queue + persistent message برای بقا پس از restart.

**نکات کلیدی:**

- برای durability هر سه: durable exchange + queue + persistent message.
- DLX برای پیام‌های مشکل‌دار؛ از requeue بی‌نهایت بپرهیزید.
- Quorum Queues به‌جای Classic برای production.

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت exchange types را توضیح بده.

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

**Direct** پیام را به queueای می‌فرستد که routing key آن دقیقاً با routing key پیام مطابقت دارد — برای routing نقطه‌به‌نقطه‌ی ساده. **Topic** از الگو با wildcard استفاده می‌کند (`*` = یک کلمه، `#` = صفر یا چند کلمه)، مثلاً `order.*.created` — برای routing انعطاف‌پذیر بر اساس دسته‌بندی. **Fanout** routing key را نادیده می‌گیرد و به همه‌ی queueهای bound کپی می‌فرستد — برای broadcast/pub-sub. **Headers** بر اساس header پیام به‌جای routing key تصمیم می‌گیرد — کمتر رایج. انتخاب بر اساس الگوی routing: ساده → Direct، دسته‌بندی‌شده → Topic، broadcast → Fanout.

**نکته مصاحبه:**

Senior wildcardهای topic (`*` و `#`) را دقیق می‌داند.

---

### سوال ۲: Dead Letter Exchange چیست و کِی استفاده می‌شود؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

DLX یک exchange است که پیام‌های «مشکل‌دار» به آن هدایت می‌شوند: پیام‌هایی که consumer reject کرده (با `requeue=false`)، TTL آن‌ها منقضی شده، یا queue پر شده. این از گم شدن پیام جلوگیری می‌کند و امکان بررسی، alerting، یا retry با تأخیر را می‌دهد. الگوی رایج: retry با backoff از طریق DLX + TTL (پیام به DLX می‌رود، بعد از TTL به queue اصلی برمی‌گردد). نکته‌ی مهم: از requeue فوری و بی‌نهایت بپرهیزید چون یک پیام «سمی» (poison message) که همیشه fail می‌شود، در حلقه‌ی بی‌نهایت می‌افتد و منابع را هدر می‌دهد — به‌جای آن پس از چند تلاش به DLX دائمی بفرستید.

**نکته مصاحبه:**

Senior به poison message و retry با backoff اشاره می‌کند.

---

### سوال ۳: publisher confirm و consumer ack چه تفاوتی دارند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

publisher confirm تضمین می‌کند پیام به **broker** رسیده و persist شده — producer مطمئن می‌شود پیام گم نشده در مسیر تا broker. consumer acknowledgement تضمین می‌کند پیام **پردازش شده** — تا وقتی consumer ack نکند، broker پیام را نگه می‌دارد و در صورت crash consumer، به consumer دیگری می‌دهد. این دو نقطه‌ی متفاوت در مسیر پیام‌اند: confirm سمت producer→broker، ack سمت broker→consumer. برای reliability کامل (no loss)، هر دو + persistence لازم است. اگر auto-ack باشد، پیام به‌محض تحویل (نه پردازش) حذف می‌شود → خطر loss.

**نکته مصاحبه:**

Senior دو نقطه‌ی متفاوت مسیر را تفکیک می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: auto-ack با پردازش حساس

```java
// ❌ پیام قبل از پردازش حذف می‌شود → loss در crash
// autoAck = true
```

```java
// ✅ manual ack بعد از پردازش موفق
```

**توضیح:** auto-ack پیام را قبل از اتمام پردازش از queue حذف می‌کند.

---

### اشتباه ۲: requeue بی‌نهایت پیام سمی

```text
❌ پیام fail → requeue → دوباره fail → حلقه‌ی بی‌نهایت
✅ بعد از N تلاش به DLX بفرستید
```

**توضیح:** poison message منابع را بی‌نهایت هدر می‌دهد.

---

### اشتباه ۳: queue غیرdurable برای پیام مهم

```text
❌ پیام پس از restart broker گم می‌شود
✅ durable exchange + durable queue + persistent message
```

**توضیح:** بدون durability، پیام در حافظه است و با restart از بین می‌رود.

---

## 🔗 ارتباط با سایر مفاهیم

- RabbitMQ در برابر **Kafka (8.1)** (smart broker در برابر log).
- DLX با **retry/resilience (2.6)** و **error handling**.
- patterns با **Enterprise Integration Patterns (6.1، 13.2)**.
- Spring AMQP با **Spring Boot** و **event-driven**.
