# Spring Integration — Enterprise Integration Patterns

> Spring Integration پیاده‌سازی EIP را برای ادغام سیستم‌ها فراهم می‌کند.

---

## 📖 مفاهیم

### Enterprise Integration Patterns

**توضیح:**

Spring Integration الگوهای ادغام سازمانی (EIP کتاب Hohpe/Woolf) را پیاده می‌کند: ارتباط بین سیستم‌ها از طریق پیام. مفهوم محوری **Message** (payload + headers) که از طریق **MessageChannel** بین components جریان می‌یابد. componentها: **ServiceActivator** (پردازش)، **Transformer** (تبدیل)، **Filter** (فیلتر)، **Router** (مسیریابی شرطی)، **Splitter/Aggregator** (تقسیم/تجمیع)، **Gateway** (interface POJO برای send/receive).

**MessageChannel** انواع: DirectChannel (sync، همان thread)، QueueChannel (async با buffer)، PublishSubscribeChannel (broadcast). **Adapters** برای اتصال به File، FTP/SFTP، HTTP، JDBC، Kafka، RabbitMQ، Mail.

**چرا مهم است:**

برای pipeline یکپارچه‌سازی پیچیده (مثل ETL، اتصال سیستم‌های legacy) با الگوهای استاندارد. مکمل Apache Camel.

**مثال کد:**

```java
@Bean
public IntegrationFlow orderFlow() {
    return IntegrationFlow
        .from(Kafka.messageDrivenChannelAdapter(consumerFactory(), "orders"))
        .filter(Order.class, o -> o.amount() > 100)   // فیلتر
        .transform(orderTransformer())                  // تبدیل
        .route(Order.class, o -> o.type())              // مسیریابی
        .handle(Jpa.outboundAdapter(entityManagerFactory))
        .get();
}
```

**نکات کلیدی:**

- DirectChannel sync، QueueChannel async — انتخاب بر اساس نیاز.
- Gateway یک interface POJO تمیز روی messaging می‌دهد.
- برای ادغام پیچیده مفید؛ برای ساده over-engineering.

---

## 🎯 سوالات مصاحبه

### سوال ۱: Spring Integration کِی استفاده می‌شود؟

**سطح:** Senior / Lead
**تکرار:** کم

**جواب کامل:**

Spring Integration برای پیاده‌سازی Enterprise Integration Patterns است: وقتی نیاز به یکپارچه‌سازی چند سیستم با pipeline پیچیده‌ی پیام‌محور دارید (تبدیل، routing شرطی، split/aggregate، اتصال به پروتکل‌های مختلف مثل SFTP/JDBC/Kafka). مناسب برای ETL، اتصال سیستم‌های legacy، و message-driven architecture داخل یک اپ. اما برای موارد ساده over-engineering است؛ یک `@KafkaListener` ساده یا کد مستقیم بهتر است. رقیب آن Apache Camel است که DSL غنی‌تر و connectorهای بیشتری دارد. در عمل، برای flow پیچیده‌ی integration در اکوسیستم Spring مفید است.

**نکته مصاحبه:**

Senior می‌داند برای موارد ساده over-engineering است و Camel را به‌عنوان جایگزین می‌شناسد.

---

### سوال ۲: تفاوت DirectChannel و QueueChannel؟

**سطح:** Senior
**تکرار:** کم

**جواب کامل:**

DirectChannel پیام را به‌صورت **synchronous** و در **همان thread** فرستنده به handler تحویل می‌دهد — مثل فراخوانی متد مستقیم، با transaction propagation حفظ‌شده، اما بدون buffering یا decoupling زمانی. QueueChannel پیام را در یک **buffer** می‌گذارد و یک thread جدا (با Poller) آن را مصرف می‌کند — **asynchronous**، با decoupling فرستنده و گیرنده و امکان throttling، اما transaction قطع می‌شود و نیاز به poller config دارد. انتخاب: DirectChannel برای flow ساده و sync با حفظ transaction؛ QueueChannel برای decoupling و پردازش async.

**نکته مصاحبه:**

Senior به حفظ/قطع transaction و sync/async اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: Spring Integration برای موارد ساده

```text
❌ پیچیدگی EIP برای یک consumer ساده
✅ @KafkaListener یا کد مستقیم
```

**توضیح:** برای flow ساده over-engineering است.

---

### اشتباه ۲: فرض async برای DirectChannel

```text
❌ انتظار decoupling از DirectChannel (sync است)
✅ QueueChannel برای async
```

**توضیح:** DirectChannel در همان thread sync اجرا می‌شود.

---

## 🔗 ارتباط با سایر مفاهیم

- EIP با **Architecture (6.1)** و **messaging (8)**.
- adapters با **Kafka/RabbitMQ (8)** و **File/FTP**.
- جایگزین: Apache Camel.
