# Java I/O — Streams، NIO، NIO.2

> درک I/O و NIO برای performance و کار با فایل/شبکه لازم است. zero-copy و non-blocking I/O مفاهیم کلیدی‌اند.

---

## 📖 مفاهیم

### I/O Streams (java.io)

**توضیح:**

API کلاسیک blocking I/O. **InputStream/OutputStream** byte-based؛ **Reader/Writer** character-based (با encoding). از **Decorator pattern** استفاده می‌کند: `BufferedReader(new FileReader(...))` — هر لایه قابلیتی اضافه می‌کند (buffering، encoding). همیشه با `try-with-resources` (که `AutoCloseable` را close می‌کند) استفاده کنید.

**مثال کد:**

```java
try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
    return reader.lines().collect(Collectors.toList());
} // close خودکار
```

**نکات کلیدی:**

- Reader/Writer برای متن (با encoding صریح)؛ Stream برای byte.
- buffering برای کاهش تعداد system call.
- همیشه try-with-resources.

---

### NIO (java.nio)

**توضیح:**

NIO برای I/O کارآمدتر و non-blocking:

- **Buffer** (`ByteBuffer`): ظرف داده با `flip()`, `clear()`, `compact()`. Direct buffer (خارج heap، برای I/O سریع) در برابر Heap buffer.
- **Channel** (`FileChannel`, `SocketChannel`): دوطرفه، با buffer کار می‌کند.
- **Selector:** multiplexing — یک thread چند channel را مدیریت می‌کند (non-blocking I/O، پایه‌ی Netty).
- **`FileChannel.transferTo()`:** zero-copy (انتقال مستقیم بین channelها بدون کپی به user space).

**چرا مهم است:**

non-blocking I/O با Selector پایه‌ی سرورهای high-concurrency (Netty، WebFlux) است. zero-copy برای انتقال فایل بزرگ بهینه است.

**نکات کلیدی:**

- Selector یک thread برای هزاران اتصال (event-driven).
- zero-copy از کپی اضافی بین kernel و user space جلوگیری می‌کند.
- direct buffer برای I/O مکرر بزرگ.

---

### NIO.2 (java.nio.file — Java 7)

**توضیح:**

API مدرن فایل: `Path`/`Paths`/`Files`. متدهای راحت: `Files.readAllLines`, `Files.walk` (پیمایش درخت با Stream)، `WatchService` (نظارت بر تغییر فایل).

**مثال کد:**

```java
// پیمایش و فیلتر فایل‌ها
try (Stream<Path> paths = Files.walk(Path.of("/dir"))) {
    paths.filter(Files::isRegularFile)
         .filter(p -> p.toString().endsWith(".java"))
         .forEach(System.out::println);
}

// نظارت بر تغییر دایرکتوری
WatchService watcher = FileSystems.getDefault().newWatchService();
path.register(watcher, ENTRY_CREATE, ENTRY_MODIFY);
```

**نکات کلیدی:**

- `Files.walk`/`lines` Stream برمی‌گردانند → با try-with-resources ببندید.
- `WatchService` برای واکنش به تغییر فایل بدون polling.

---

## 🎯 سوالات مصاحبه

### سوال ۱: blocking I/O در برابر non-blocking I/O (NIO)؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

در blocking I/O (java.io)، هر thread روی یک اتصال block می‌شود تا داده برسد — مدل thread-per-connection که برای اتصال زیاد مقیاس نمی‌گیرد (thread گران). در non-blocking I/O (NIO با Selector)، یک thread (یا چند) با Selector چند channel را همزمان مدیریت می‌کند: به‌جای block شدن، Selector اطلاع می‌دهد کدام channel آماده‌ی read/write است (event-driven). این مدل با تعداد کم thread، هزاران اتصال را مدیریت می‌کند — پایه‌ی Netty و WebFlux. trade-off: کد NIO پیچیده‌تر است. نکته‌ی مدرن: با virtual threads (Java 21)، blocking I/O ساده دوباره مقیاس‌پذیر شده و نیاز به پیچیدگی NIO/reactive را در بسیاری موارد کم کرده.

**نکته مصاحبه:**

Lead به Selector، Netty، و تأثیر virtual threads اشاره می‌کند.

---

### سوال ۲: zero-copy چیست و چه مزیتی دارد؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

در کپی معمولی فایل به socket، داده چندبار کپی می‌شود: disk → kernel buffer → user space (اپ) → kernel socket buffer → NIC. هر کپی و context switch هزینه دارد. **zero-copy** (با `FileChannel.transferTo()` که از `sendfile` سیستم‌عامل استفاده می‌کند) داده را مستقیماً از kernel buffer به socket buffer منتقل می‌کند بدون عبور از user space — کپی‌ها و context switchها کاهش می‌یابند. مزیت: throughput بالاتر و CPU کمتر برای انتقال فایل بزرگ (مثل static file serving، Kafka که از zero-copy استفاده می‌کند). به همین دلیل Kafka throughput بالایی دارد.

**نکته مصاحبه:**

Senior به استفاده‌ی Kafka از zero-copy اشاره می‌کند.

---

### سوال ۳: Selector چطور کار می‌کند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Selector یک multiplexer است: چند channel (non-blocking) را با یک Selector register می‌کنید با علاقه به رویدادهای خاص (OP_READ، OP_WRITE، OP_ACCEPT). سپس `selector.select()` صدا می‌زنید که block می‌شود تا حداقل یک channel آماده شود، و مجموعه‌ی channelهای آماده را برمی‌گرداند. یک thread در یک حلقه این رویدادها را پردازش می‌کند. زیر کاپوت از `epoll` (Linux)/`kqueue` استفاده می‌کند. این یعنی یک thread می‌تواند هزاران اتصال را مدیریت کند به‌جای یک thread per connection — پایه‌ی event-loop در Netty و سرورهای reactive.

**نکته مصاحبه:**

Senior به epoll و event-loop اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: عدم بستن Stream از Files.walk/lines

```java
// ❌ resource leak (file handle)
Files.lines(path).forEach(...);
```

```java
// ✅
try (var lines = Files.lines(path)) { lines.forEach(...); }
```

**توضیح:** `Files.walk`/`lines` منبع باز نگه می‌دارند؛ باید بسته شوند.

---

### اشتباه ۲: خواندن بدون buffering

```java
// ❌ هر read یک system call
FileReader r = new FileReader(file);
```

```java
// ✅
BufferedReader r = new BufferedReader(new FileReader(file));
```

**توضیح:** بدون buffer، I/O کند است (system call زیاد).

---

### اشتباه ۳: فراموشی encoding صریح

```java
// ❌ وابسته به default platform encoding → باگ روی سیستم متفاوت
new FileReader(file);
```

```java
// ✅
Files.newBufferedReader(path, StandardCharsets.UTF_8);
```

**توضیح:** encoding صریح از باگ‌های cross-platform جلوگیری می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- NIO/Selector با **WebFlux/Netty (2.3)** و **non-blocking**.
- virtual threads با blocking I/O ساده (**1.5**).
- zero-copy با **Kafka (8.1)** performance.
- try-with-resources با **Exceptions (1.1)**.
