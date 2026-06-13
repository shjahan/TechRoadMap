# 12-Factor App

> متدولوژی ساخت اپ‌های cloud-native و مقیاس‌پذیر. اصول کلیدی برای deploy مدرن.

---

## 📖 مفاهیم

### دوازده اصل

**توضیح:**

متدولوژی برای ساخت اپ‌های SaaS مقیاس‌پذیر و قابل‌نگهداری:

1. **Codebase:** یک repo، چند deploy.
2. **Dependencies:** صریح declare و isolate (نه تکیه بر system-wide).
3. **Config:** در environment، نه در کد.
4. **Backing Services:** DB، cache، queue به‌عنوان attached resources (قابل‌تعویض با URL).
5. **Build/Release/Run:** مراحل جدا.
6. **Processes:** stateless، shared-nothing.
7. **Port Binding:** اپ خودش port export می‌کند (embedded server).
8. **Concurrency:** scale با process model (horizontal).
9. **Disposability:** startup سریع، graceful shutdown.
10. **Dev/Prod Parity:** محیط‌ها شبیه هم.
11. **Logs:** event stream (stdout)، نه فایل.
12. **Admin Processes:** one-off tasks جداگانه.

**چرا مهم است:**

این اصول پایه‌ی cloud-native و سازگاری با کانتینر/K8s هستند. نقض آن‌ها (مثل state محلی، config در کد) scale و deploy را می‌شکند.

**نکات کلیدی:**

- stateless (factor 6) پیش‌نیاز horizontal scaling.
- config در environment (factor 3) برای امنیت و انعطاف.
- logs به stdout (factor 11) برای جمع‌آوری متمرکز.

---

## 🎯 سوالات مصاحبه

### سوال ۱: کدام اصول 12-factor برای K8s حیاتی‌ترند؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

مهم‌ترین‌ها برای کانتینر/K8s: (۳) **Config در environment** — در K8s با ConfigMap/Secret تزریق می‌شود؛ بدون این، یک image برای همه‌ی محیط‌ها کار نمی‌کند. (۶) **Stateless processes** — پیش‌نیاز horizontal scaling و rolling update؛ state باید در DB/Redis باشد نه حافظه‌ی pod (که هر لحظه ممکن kill شود). (۹) **Disposability** — startup سریع (برای autoscaling و rolling) و graceful shutdown (هنگام SIGTERM، K8s grace period می‌دهد تا requestهای جاری تمام شوند). (۱۱) **Logs به stdout** — K8s/Fluent Bit از stdout جمع می‌کند؛ نوشتن به فایل در container ضدالگوست. (۴) **Backing services** — DB با URL قابل‌تعویض. نقض هر کدام مستقیماً با K8s تضاد دارد.

**نکته مصاحبه:**

Lead به stateless، graceful shutdown، و logs به stdout اشاره می‌کند.

---

### سوال ۲: چرا اپ باید stateless باشد و چطور state را مدیریت می‌کنی؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

stateless یعنی هیچ state ماندگاری در حافظه‌ی process نگه نمی‌داری بین requestها. دلیل: در محیط مقیاس‌پذیر، چند instance وجود دارد و load balancer هر request را به یکی می‌فرستد؛ اگر state در حافظه‌ی یک instance باشد (مثل session در حافظه)، request بعدی که به instance دیگر می‌رود آن را نمی‌بیند. همچنین instanceها هر لحظه ممکن kill/restart شوند (autoscaling، rolling update). راه‌حل: state را در backing service خارجی نگه دارید — session در Redis، داده در DB، فایل در object storage (S3). این horizontal scaling، rolling update بدون از دست رفتن state، و resilience را ممکن می‌کند. sticky session یک workaround ضعیف است که scale را محدود می‌کند.

**نکته مصاحبه:**

Senior به session در Redis و مشکل sticky session اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: state در حافظه‌ی process

```text
❌ session/cache در حافظه‌ی هر instance
✅ Redis/DB خارجی
```

**توضیح:** state محلی horizontal scaling را می‌شکند.

---

### اشتباه ۲: config در کد

```text
❌ hardcode کردن URL/credential
✅ environment variable / ConfigMap
```

**توضیح:** config باید per-environment و خارج از کد باشد.

---

### اشتباه ۳: log به فایل در container

```text
❌ نوشتن log در فایل داخل container (با kill pod گم می‌شود)
✅ log به stdout، جمع‌آوری توسط K8s/Fluent Bit
```

**توضیح:** فایل در container ephemeral است.

---

## 🔗 ارتباط با سایر مفاهیم

- 12-factor با **Kubernetes (10.2)** و **Docker (10.1)**.
- config با **Spring Boot externalized config (2.2)** و **Vault (16.5)**.
- stateless با **System Design scaling (6.2)** و **Redis session (9.1)**.
- logs با **observability (10.4)**.
