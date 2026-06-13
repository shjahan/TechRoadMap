# Docker — Images، Dockerfile، Compose، Networking

> Docker پایه‌ی containerization مدرن است. multi-stage build و best practices برای Java مهم‌اند.

---

## 📖 مفاهیم

### مفاهیم پایه

**توضیح:**

- **Image:** قالب read-only و لایه‌ای (layers) که برنامه و وابستگی‌ها را شامل می‌شود.
- **Container:** نمونه‌ی در حال اجرای یک image (process ایزوله با namespace و cgroups).
- **Dockerfile:** دستورالعمل ساخت image.
- **Registry:** مخزن image (Docker Hub، GHCR، private).

container برخلاف VM، kernel میزبان را share می‌کند پس سبک و سریع است. هر دستور Dockerfile یک layer می‌سازد که cache می‌شود.

**نکات کلیدی:**

- container kernel را share می‌کند (سبک‌تر از VM).
- layerها cache می‌شوند → ترتیب دستورات روی build speed اثر دارد.

---

### Dockerfile Best Practices (Java)

**توضیح:**

- **Multi-stage build:** مرحله‌ی build (با JDK + Maven) جدا از مرحله‌ی runtime (فقط JRE) → image نهایی کوچک‌تر و امن‌تر (بدون ابزار build).
- **Non-root user:** اجرای container با کاربر غیرروت برای امنیت.
- **Layer caching:** dependencyها را قبل از source code کپی کنید تا با تغییر کد، cache وابستگی‌ها حفظ شود.
- **`.dockerignore`** برای حذف فایل‌های غیرضروری.
- **base image کوچک:** Alpine یا distroless.

**مثال کد:**

```dockerfile
# مرحله build
FROM eclipse-temurin:21-jdk-alpine AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline   # cache وابستگی‌ها (لایه‌ی جدا)
COPY src ./src
RUN mvn package -DskipTests

# مرحله runtime — image کوچک
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
RUN addgroup -S app && adduser -S app -G app
USER app                         # non-root
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**نکات کلیدی:**

- multi-stage → image کوچک (فقط JRE + jar).
- copy کردن pom قبل از src برای cache وابستگی.
- non-root user برای امنیت.

---

### Docker Compose & Networking

**توضیح:**

**Compose** برای تعریف و اجرای چند container با هم (`services`, `networks`, `volumes`). `depends_on` + `healthcheck` برای ترتیب راه‌اندازی. named volume برای persistence. **Networking:** Bridge (پیش‌فرض، container روی یک شبکه)، Host، None، Overlay (برای چند host در Swarm/K8s). در یک شبکه، containerها با **service name** به‌عنوان hostname همدیگر را پیدا می‌کنند (DNS داخلی).

**مثال کد:**

```yaml
services:
  app:
    build: .
    ports: ["8080:8080"]
    depends_on:
      db: { condition: service_healthy }
    environment:
      DB_URL: jdbc:postgresql://db:5432/mydb  # db = service name
  db:
    image: postgres:17
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

**نکات کلیدی:**

- service name به‌عنوان hostname (DNS داخلی).
- healthcheck + depends_on برای ترتیب درست راه‌اندازی.
- named volume برای persistence داده.

---

## 🎯 سوالات مصاحبه

### سوال ۱: multi-stage build چه مزیتی دارد؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

multi-stage build اجازه می‌دهد از چند `FROM` در یک Dockerfile استفاده کنید: یک مرحله برای build (با JDK، Maven، ابزارها) و مرحله‌ی نهایی فقط نتیجه (jar) را از مرحله‌ی build کپی می‌کند روی یک base کوچک (JRE یا distroless). مزایا: (۱) **image کوچک‌تر** — ابزارهای build (که صدها مگابایت‌اند) در image نهایی نیستند. (۲) **امنیت** — کمتر بودن چیزها = attack surface کمتر (بدون compiler، shell، ابزار). (۳) **سرعت deploy** — image کوچک سریع‌تر pull/push می‌شود. این یک best practice استاندارد برای Java است که image را از ~۷۰۰MB به ~۲۰۰MB یا کمتر می‌رساند.

**نکته مصاحبه:**

Senior به کاهش attack surface و اندازه اشاره می‌کند. Follow-up: «distroless چیست؟» (image بدون OS/shell، فقط runtime — امن‌تر).

---

### سوال ۲: چطور layer caching را در Dockerfile بهینه می‌کنی؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

Docker هر دستور را یک layer می‌سازد و cache می‌کند؛ اگر یک layer تغییر کند، همه‌ی layerهای بعد از آن دوباره build می‌شوند. کلید بهینه‌سازی: چیزهایی که **کمتر تغییر می‌کنند** را زودتر بگذارید. برای Java/Maven: ابتدا `pom.xml` را کپی و `mvn dependency:go-offline` بزنید (این layer فقط با تغییر dependency invalidate می‌شود)، سپس `src` را کپی کنید. چون source code مکرر تغییر می‌کند اما dependencyها به‌ندرت، با این ترتیب هر build کد، از cache وابستگی‌ها استفاده می‌کند و فقط compile دوباره انجام می‌شود — build بسیار سریع‌تر. اگر pom و src را با هم کپی کنید، هر تغییر کد کل دانلود وابستگی را دوباره اجرا می‌کند.

**نکته مصاحبه:**

Senior ترتیب «کم‌تغییر زودتر» را توضیح می‌دهد.

---

### سوال ۳: container در برابر VM؟

**سطح:** Mid / Senior
**تکرار:** متوسط

**جواب کامل:**

VM یک kernel و OS کامل مجزا روی hypervisor دارد — ایزولاسیون قوی اما سنگین (گیگابایت، startup کند). container kernel میزبان را share می‌کند و فقط process را با namespace (ایزولاسیون دید) و cgroups (محدودیت منابع) ایزوله می‌کند — سبک (مگابایت)، startup سریع (ثانیه)، چگالی بالا. trade-off: container ایزولاسیون ضعیف‌تری از VM دارد (kernel مشترک = سطح حمله مشترک)، پس برای multi-tenancy با امنیت سخت‌گیرانه گاهی VM یا microVM (Firecracker) استفاده می‌شود. برای اکثر کاربردها container کافی و کارآمدتر است.

**نکته مصاحبه:**

Senior به kernel مشترک و trade-off ایزولاسیون اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: اجرای container به‌عنوان root

```dockerfile
# ❌ بدون USER → root
ENTRYPOINT ["java", "-jar", "app.jar"]
```

```dockerfile
# ✅
RUN adduser -S app && USER app
```

**توضیح:** container روت = خطر امنیتی (escape به host).

---

### اشتباه ۲: کپی همه‌چیز قبل از build

```dockerfile
# ❌ هر تغییر کد، دانلود مجدد وابستگی
COPY . .
RUN mvn package
```

```dockerfile
# ✅ pom اول
COPY pom.xml . && RUN mvn dependency:go-offline
COPY src ./src && RUN mvn package
```

**توضیح:** cache وابستگی با ترتیب درست حفظ می‌شود.

---

### اشتباه ۳: image بزرگ (full JDK + ابزار)

```dockerfile
# ❌ image نهایی شامل JDK و Maven
FROM maven:3-eclipse-temurin-21
```

```dockerfile
# ✅ multi-stage با JRE نهایی
```

**توضیح:** image بزرگ = pull کند و attack surface زیاد.

---

## 🔗 ارتباط با سایر مفاهیم

- Docker پایه‌ی **Kubernetes (10.2)** و **CI/CD (10.3)**.
- non-root و scanning با **DevSecOps (16.5)**.
- jlink (Java module) برای image کوچک‌تر با **Java Modules (1.3)**.
- Compose با **local development** و **Testcontainers (12.5)**.
