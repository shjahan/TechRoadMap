# MQTT — پروتکل سبک برای IoT

> MQTT برای IoT و دستگاه‌های با منابع محدود طراحی شده. QoS levels مفهوم کلیدی است.

---

## 📖 مفاهیم

### مفاهیم پایه

**توضیح:**

MQTT (Message Queuing Telemetry Transport) یک پروتکل publish/subscribe سبک روی TCP است که برای شبکه‌های کم‌پهنا، دستگاه‌های با منابع محدود (IoT)، و اتصال‌های ناپایدار طراحی شده. معماری: دستگاه‌ها به یک **Broker** (Mosquitto، EMQX، HiveMQ) متصل می‌شوند، به **topic**ها publish/subscribe می‌کنند. topic سلسله‌مراتبی است (`home/bedroom/temperature`).

سربار کم (header کوچک)، مناسب باتری و پهنای باند محدود — برخلاف HTTP که سنگین است.

**چرا مهم است:**

استاندارد IoT. درک QoS برای تضمین تحویل در شبکه‌ی ناپایدار حیاتی است.

**نکات کلیدی:**

- سبک و کم‌سربار، مناسب IoT و mobile.
- topic سلسله‌مراتبی با wildcard (`+` یک سطح، `#` چند سطح).

---

### QoS Levels

**توضیح:**

سه سطح کیفیت تحویل:

- **QoS 0 (at-most-once):** fire-and-forget، بدون تأیید. ممکن گم شود. سریع‌ترین، برای داده‌ی مکرر کم‌اهمیت (مثل sensor reading لحظه‌ای).
- **QoS 1 (at-least-once):** با ack؛ تضمین رسیدن اما ممکن duplicate. برای داده‌ای که نباید گم شود اما duplicate قابل‌تحمل است.
- **QoS 2 (exactly-once):** با handshake چهارمرحله‌ای؛ بدون loss و بدون duplicate. کندترین و پرسربارترین، برای داده‌ی بحرانی.

QoS بالاتر = تضمین بیشتر اما overhead و latency بیشتر.

**نکات کلیدی:**

- QoS را بر اساس اهمیت داده انتخاب کنید (QoS 2 گران است).
- QoS بین publisher-broker و broker-subscriber می‌تواند متفاوت باشد.

---

### Retain & Last Will

**توضیح:**

- **Retained Messages:** broker آخرین پیام retain‌شده‌ی یک topic را نگه می‌دارد و به subscriberهای جدید فوراً می‌دهد (برای state فعلی، مثل آخرین دمای سنسور).
- **Last Will and Testament (LWT):** پیامی که دستگاه هنگام اتصال تعریف می‌کند و broker در صورت قطع غیرمنتظره‌ی دستگاه آن را منتشر می‌کند — برای تشخیص offline شدن.

**نکات کلیدی:**

- retained message برای دادن state فعلی به subscriber جدید.
- LWT برای تشخیص قطع ناگهانی دستگاه.

---

## 🎯 سوالات مصاحبه

### سوال ۱: QoS levels در MQTT را توضیح بده.

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

سه سطح متناظر با delivery guarantees: QoS 0 (at-most-once) پیام را یک‌بار می‌فرستد بدون تأیید؛ ممکن گم شود اما سریع و کم‌سربار — برای داده‌ی پرتکرار و کم‌اهمیت. QoS 1 (at-least-once) با PUBACK تضمین می‌کند پیام رسیده، اما اگر ack گم شود ممکن دوباره فرستاده شود (duplicate) — نیاز به idempotency در گیرنده. QoS 2 (exactly-once) با handshake چهارمرحله‌ای (PUBLISH/PUBREC/PUBREL/PUBCOMP) تضمین می‌کند دقیقاً یک‌بار تحویل شود — برای داده‌ی بحرانی، اما کندترین و پرسربارترین. انتخاب trade-off بین تضمین و overhead است؛ در IoT با باتری/پهنای باند محدود، QoS بالا گران است.

**نکته مصاحبه:**

Senior QoS را به at-most/at-least/exactly-once map می‌کند و trade-off overhead را می‌فهمد.

---

### سوال ۲: چرا MQTT به‌جای HTTP برای IoT؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

MQTT برای محدودیت‌های IoT بهینه شده: (۱) سربار بسیار کم (header کوچک، باینری) در برابر HTTP پرحجم با header متنی — مهم برای پهنای باند و باتری محدود. (۲) مدل pub/sub با اتصال persistent، پس دستگاه نیازی به polling مکرر ندارد (push). (۳) QoS برای تحویل قابل‌اطمینان روی شبکه‌ی ناپایدار. (۴) LWT برای تشخیص قطع. (۵) مقیاس‌پذیری به میلیون‌ها دستگاه با broker. HTTP برای request/response مناسب است اما برای telemetry مداوم و push از میلیون‌ها دستگاه با منابع محدود ناکارآمد است.

**نکته مصاحبه:**

Senior به سربار، pub/sub persistent، و LWT اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: QoS 2 برای همه‌چیز

```text
❌ QoS 2 برای داده‌ی پرتکرار → overhead زیاد روی دستگاه محدود
✅ QoS 0/1 برای داده‌ی مکرر، QoS 2 فقط برای بحرانی
```

**توضیح:** QoS 2 handshake چهارمرحله‌ای دارد؛ برای IoT گران است.

---

### اشتباه ۲: عدم استفاده از LWT برای تشخیص offline

```text
❌ ندانستن اینکه دستگاه قطع شده
✅ LWT برای انتشار خودکار وضعیت offline
```

**توضیح:** بدون LWT، قطع ناگهانی دستگاه تشخیص داده نمی‌شود.

---

## 🔗 ارتباط با سایر مفاهیم

- MQTT QoS با **Kafka/RabbitMQ delivery guarantees (8.1, 8.2)** قابل‌مقایسه.
- pub/sub با **Event-Driven Architecture (6.1)**.
- Spring Integration MQTT با **Enterprise Integration (13.2)**.
