# gRPC — Protocol Buffers، Streaming، vs REST

> gRPC برای ارتباط پرکارایی بین‌سرویسی. درک مزایا بر REST و انواع streaming مهم است.

---

## 📖 مفاهیم

### مفاهیم gRPC

**توضیح:**

gRPC یک RPC framework پرکارایی است که از **Protocol Buffers** (باینری، schema‌محور) روی **HTTP/2** استفاده می‌کند. سرویس و پیام‌ها در `.proto` تعریف می‌شوند و code generation برای client/server تولید می‌کند. strongly-typed با contract صریح.

**مثال کد:**

```protobuf
syntax = "proto3";
service UserService {
    rpc GetUser (GetUserRequest) returns (User);            // unary
    rpc ListUsers (ListUsersRequest) returns (stream User); // server streaming
    rpc CreateUsers (stream CreateUserRequest) returns (Summary); // client streaming
    rpc Chat (stream ChatMessage) returns (stream ChatMessage);   // bidirectional
}
message User { int64 id = 1; string name = 2; }
```

**نکات کلیدی:**

- field number در proto برای schema evolution حیاتی است (reuse نکنید).
- code generation client/server را از contract می‌سازد.

---

### 4 نوع RPC

**توضیح:**

- **Unary:** request/response معمولی.
- **Server Streaming:** یک request، stream از responseها (مثل دانلود لیست بزرگ).
- **Client Streaming:** stream از requestها، یک response (مثل upload).
- **Bidirectional Streaming:** هر دو طرف stream (مثل chat real-time).

streaming مزیت بزرگ gRPC بر REST سنتی است (روی HTTP/2 multiplexing).

**نکات کلیدی:**

- streaming روی HTTP/2 بدون connection جدید.
- bidirectional برای real-time (chat، live updates).

---

### مزایا vs REST & Spring Boot gRPC

**توضیح:**

مزایا بر REST/JSON: باینری (سریع‌تر، فشرده‌تر)، strongly-typed (contract enforce)، HTTP/2 (multiplexing، header compression، streaming)، code generation. عیب: غیرخوانا برای debug، نیاز به tooling، پشتیبانی مرورگر محدود (نیاز gRPC-Web)، و کمتر مناسب API عمومی. در Spring با `grpc-spring-boot-starter` و `@GrpcService`/`@GrpcClient`.

**نکات کلیدی:**

- gRPC برای ارتباط داخلی microservice پرترافیک؛ REST برای API عمومی.
- مرورگر مستقیم gRPC را پشتیبانی نمی‌کند (gRPC-Web لازم).

---

## 🎯 سوالات مصاحبه

### سوال ۱: gRPC در برابر REST — کِی کدام؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

gRPC برای ارتباط **داخلی بین‌سرویسی** پرترافیک ایده‌آل است: باینری (Protocol Buffers) سریع‌تر و فشرده‌تر از JSON، strongly-typed با contract صریح که breaking change را زود می‌گیرد، HTTP/2 با multiplexing و streaming دوطرفه، و code generation. REST برای **API عمومی** بهتر است: خوانا، universal (هر client با HTTP)، cache‌پذیر، debug آسان (curl)، و پشتیبانی مرورگر مستقیم. trade-off: gRPC tooling و یادگیری بیشتر می‌خواهد، در مرورگر نیاز gRPC-Web دارد، و برای debug غیرخواناست. توصیه: microservice داخلی با latency/throughput مهم → gRPC؛ API روبه‌بیرون/عمومی → REST. بسیاری سیستم‌ها هر دو دارند (gRPC داخلی، REST/GraphQL در gateway).

**نکته مصاحبه:**

Lead «gRPC داخلی، REST عمومی» را با دلیل می‌گوید.

---

### سوال ۲: چهار نوع RPC در gRPC را توضیح بده.

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

(۱) **Unary** — یک request، یک response؛ مثل REST معمولی، برای CRUD. (۲) **Server Streaming** — یک request، stream از responseها؛ برای ارسال داده‌ی بزرگ به‌تدریج یا live feed (مثل قیمت سهام). (۳) **Client Streaming** — stream از requestها، یک response؛ برای upload یا ارسال batch (مثل آپلود فایل تکه‌تکه یا متریک). (۴) **Bidirectional Streaming** — هر دو طرف همزمان stream می‌کنند؛ برای real-time دوطرفه (chat، بازی، collaboration). همه روی یک اتصال HTTP/2 با multiplexing کار می‌کنند که مزیت بزرگ بر REST است که برای streaming به workaround (SSE، WebSocket) نیاز دارد.

**نکته مصاحبه:**

Senior هر چهار را با مثال کاربرد می‌دهد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: gRPC برای API عمومی مرورگری

```text
❌ gRPC مستقیم از مرورگر (پشتیبانی نمی‌شود)
✅ REST/GraphQL برای عمومی، یا gRPC-Web با proxy
```

**توضیح:** مرورگر gRPC خام را پشتیبانی نمی‌کند.

---

### اشتباه ۲: reuse کردن field number در proto

```protobuf
// ❌ حذف فیلد و استفاده‌ی مجدد از number → ناسازگاری
```

```protobuf
// ✅ reserved field number
reserved 3;
```

**توضیح:** field number قدیمی با داده‌ی قدیمی تداخل می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- gRPC با **Protocol Buffers (12.4)** و **microservices (6.1)**.
- streaming با **WebSocket/SSE (6.2)** (مقایسه).
- contract با **schema evolution (12.4)** و **contract testing (13.5)**.
- REST مقایسه با **API design (19.1)**.
