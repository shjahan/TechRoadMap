# JVM Internals عمیق — GC، JIT، JFR، Class Loading

> سوالات سطح Lead روی GC tuning، JIT و profiling تمرکز دارند. این بخش performance را تعیین می‌کند.

---

## 📖 مفاهیم

### Garbage Collection — G1، ZGC، Shenandoah

**توضیح:**

**G1GC** (پیش‌فرض از Java 9): region-based؛ heap به regionها تقسیم می‌شود. نسل جوان (Eden + Survivor) و پیر. **Minor GC** (نسل جوان، سریع)، **Mixed GC** (جوان + بخشی از پیر)، **Full GC** (همه، کند — باید avoid شود). هدف pause قابل‌تنظیم (`-XX:MaxGCPauseMillis`).

**ZGC** (production از Java 15): concurrent، pause زیر ۱ میلی‌ثانیه حتی برای heap بزرگ (terabyte). برای latency-sensitive. **Shenandoah** (RedHat): مشابه ZGC.

**چرا مهم است:**

انتخاب و tuning GC مستقیماً latency و throughput را تعیین می‌کند. Full GC مکرر علامت مشکل است.

**مثال کد:**

```bash
# G1 با هدف pause
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xms2g -Xmx2g app.jar

# ZGC برای latency پایین
java -XX:+UseZGC -Xms4g -Xmx4g app.jar

# GC logging
java -Xlog:gc*:file=gc.log:time,uptime app.jar
```

**نکات کلیدی:**

- `-Xms` = `-Xmx` تا از resize حین اجرا جلوگیری شود.
- G1 متعادل (پیش‌فرض)؛ ZGC برای latency بحرانی.
- Full GC مکرر = مشکل (نشت یا heap کوچک).

---

### JIT Compilation

**توضیح:**

کد ابتدا interpret می‌شود؛ کد «داغ» (hot، پرتکرار) توسط JIT کامپایل می‌شود. **Tiered Compilation** (پیش‌فرض): C1 (سریع کامپایل، بهینه‌سازی کم) → C2 (کند کامپایل، بهینه‌سازی زیاد). بهینه‌سازی‌های کلیدی: **inlining** (مهم‌ترین — حذف overhead فراخوانی)، **escape analysis** (اگر شیء از متد فرار نکند، روی stack تخصیص یا scalar replacement). GraalVM JIT جایگزین C2 با بهینه‌سازی بهتر در برخی workloadها.

**نکات کلیدی:**

- warmup: کد ابتدا کند است تا JIT کامپایل کند (مهم در benchmark — از JMH استفاده کنید).
- escape analysis می‌تواند تخصیص heap را حذف کند.

---

### JFR (Java Flight Recorder)

**توضیح:**

ابزار profiling کم‌سربار داخلی JVM: CPU، memory allocation، GC، thread/lock، I/O. با کمترین overhead (می‌توان در production فعال کرد). JDK Mission Control (JMC) برای تحلیل GUI.

**مثال کد:**

```bash
# شروع recording
java -XX:StartFlightRecording=duration=60s,filename=rec.jfr app.jar
# یا روی process در حال اجرا
jcmd <pid> JFR.start duration=60s filename=rec.jfr
```

**نکات کلیدی:**

- JFR کم‌سربار، مناسب production profiling.
- برای یافتن allocation hotspot و lock contention.

---

### Class Loading & Memory Leak

**توضیح:**

سه classloader (Bootstrap، Platform، Application) با **parent delegation**. memory leak در Java: نگه‌داری ناخواسته‌ی ارجاع (static collection رشدیابنده، listener حذف‌نشده، ThreadLocal در pool، classloader leak در hot redeploy). تشخیص: heap dump + تحلیل با Eclipse MAT (dominator tree).

**نکات کلیدی:**

- memory leak = ارجاع نگه‌داشته‌شده، نه bug GC.
- heap dump + MAT برای یافتن منبع leak.

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت G1 و ZGC و کِی کدام؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

G1 یک GC متعادل region-based است که throughput خوب با pause قابل‌تنظیم (هدف چند ده تا چند صد میلی‌ثانیه) می‌دهد؛ برای اکثر برنامه‌ها مناسب و پیش‌فرض است. ZGC یک concurrent collector است که تقریباً همه‌ی کار را همزمان با اپ انجام می‌دهد و pause زیر ۱ میلی‌ثانیه حتی برای heap چند ترابایتی تضمین می‌کند؛ برای latency-sensitive (trading، real-time، API با SLA سخت p99). trade-off: ZGC ممکن throughput کمی کمتر و مصرف CPU/memory بیشتر داشته باشد. انتخاب: اگر latency و pause بحرانی است (به‌خصوص با heap بزرگ) → ZGC؛ برای throughput عمومی و سادگی → G1. همیشه با اندازه‌گیری (GC log، JFR) تصمیم بگیرید نه فرض.

**نکته مصاحبه:**

Lead trade-off latency/throughput و heap size را می‌داند.

---

### سوال ۲: memory leak را چطور پیدا می‌کنی؟

**سطح:** Lead
**تکرار:** زیاد

**جواب کامل:**

memory leak در Java یعنی اشیاء reachable می‌مانند (GC نمی‌تواند آزادشان کند) در حالی که دیگر لازم نیستند. علائم: heap به‌تدریج رشد می‌کند، Full GC مکرر اما حافظه آزاد نمی‌شود، و نهایتاً `OutOfMemoryError`. فرایند تشخیص: (۱) رصد metric (heap used، GC frequency با Micrometer/JMX) برای تأیید روند صعودی. (۲) گرفتن **heap dump** (با `jmap`، JFR، یا `-XX:+HeapDumpOnOutOfMemoryError`). (۳) تحلیل با Eclipse MAT یا VisualVM: نگاه به **dominator tree** برای یافتن بزرگ‌ترین مصرف‌کننده و مسیر نگه‌داری ارجاع (چه چیزی این اشیاء را زنده نگه داشته). علل رایج: static collection رشدیابنده، cache بدون eviction، listener حذف‌نشده، ThreadLocal در thread pool بدون remove. سپس مرجع را قطع کنید.

**نکته مصاحبه:**

Lead فرایند سیستماتیک (رصد → heap dump → dominator tree) را شرح می‌دهد.

---

### سوال ۳: JIT warmup چیست و چرا در benchmark مهم است؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

کد در ابتدا interpret می‌شود (کند)؛ JIT فقط بعد از اینکه یک متد به‌اندازه‌ی کافی اجرا شد (hot) آن را کامپایل و بهینه می‌کند. این دوره‌ی **warmup** یعنی اجرای اولیه به‌مراتب کندتر از حالت پایدار است. در benchmark، اگر warmup را در نظر نگیرید، نتایج بی‌معنا می‌شوند (زمان interpret را اندازه می‌گیرید نه کد بهینه). به همین دلیل از **JMH** (Java Microbenchmark Harness) استفاده می‌شود که warmup iterationها را اجرا و سپس اندازه می‌گیرد، و از مشکلاتی مثل dead code elimination توسط JIT جلوگیری می‌کند. در production، startup کند (تا JIT warm شود) با AOT/CDS یا GraalVM Native Image بهبود می‌یابد.

**نکته مصاحبه:**

Senior به JMH و خطر benchmark بدون warmup اشاره می‌کند.

---

### سوال ۴: چرا `-Xms` و `-Xmx` را برابر می‌گذاریم؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`-Xms` (heap اولیه) و `-Xmx` (حداکثر heap). اگر متفاوت باشند، JVM heap را با رشد نیاز resize می‌کند که هزینه دارد (و gمی‌تواند pause اضافه و fragmentation بیاورد). با برابر گذاشتن، heap از ابتدا کامل تخصیص می‌یابد و resize حین اجرا حذف می‌شود — performance پایدارتر و قابل‌پیش‌بینی‌تر، به‌خصوص در کانتینر با memory limit ثابت. در محیط کانتینری، این با memory limit K8s هماهنگ می‌شود (با `-XX:MaxRAMPercentage`). همچنین از سناریوی «heap کوچک شروع شد، بعد نتوانست بزرگ شود» جلوگیری می‌کند.

**نکته مصاحبه:**

Senior به حذف resize و هماهنگی با container limit اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: benchmark بدون JMH/warmup

```java
// ❌ اندازه‌گیری زمان interpret، نه کد بهینه
long start = System.nanoTime();
for (int i = 0; i < 1000; i++) doWork();
```

```java
// ✅ JMH با warmup
```

**توضیح:** بدون warmup، نتیجه‌ی benchmark بی‌معناست.

---

### اشتباه ۲: `-Xms` خیلی کوچک

```bash
# ❌ resize مکرر
java -Xms256m -Xmx4g
```

```bash
# ✅
java -Xms4g -Xmx4g
```

**توضیح:** اختلاف باعث resize پرهزینه می‌شود.

---

### اشتباه ۳: ThreadLocal بدون remove → classloader/memory leak

```java
// ❌ در thread pool، مقدار باقی می‌ماند
threadLocal.set(bigObject);
```

```java
// ✅
try { threadLocal.set(bigObject); ... } finally { threadLocal.remove(); }
```

**توضیح:** thread در pool reuse می‌شود و مقدار نشت می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- GC/JIT با **performance & scalability (20)** و **Concurrency (1.6)**.
- JVM tuning با **Kubernetes resource limits (10.2)** و **Docker**.
- JFR با **observability/profiling (10.4)**.
- memory leak با **JMM** و **ThreadLocal/ScopedValues (1.6)**.
