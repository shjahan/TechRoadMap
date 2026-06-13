# Spring Boot — Auto-Configuration, Actuator, Boot 4

> Spring Boot سرعت توسعه را با «convention over configuration» متحول کرد. درک auto-configuration تفاوت Senior را نشان می‌دهد.

---

## 📖 مفاهیم

### Auto-Configuration

**توضیح:**

Auto-configuration هسته‌ی جادوی Spring Boot است: بر اساس آنچه در classpath وجود دارد و propertyها، bEanهای مناسب را خودکار می‌سازد. `@SpringBootApplication` ترکیب سه annotation است: `@Configuration` (این کلاس منبع تعریف bean است)، `@EnableAutoConfiguration` (فعال‌سازی auto-config)، و `@ComponentScan` (اسکن پکیج جاری و زیرپکیج‌ها).

مکانیزم: Spring Boot فایل `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (در نسخه‌های قدیمی `spring.factories`) را می‌خواند که لیستی از کلاس‌های auto-configuration است. هر کدام با annotationهای `@Conditional` کنترل می‌شوند: `@ConditionalOnClass` (اگر کلاسی در classpath باشد)، `@ConditionalOnMissingBean` (اگر کاربر bean خودش را تعریف نکرده باشد)، `@ConditionalOnProperty`. این یعنی شما می‌توانید هر چیزی را با تعریف bean خودتان override کنید.

**چرا مهم است:**

درک این مکانیزم برای دیباگ «چرا این bean ساخته شد/نشد» و سفارشی‌سازی رفتار پیش‌فرض حیاتی است. با `--debug` گزارش auto-config (شرط‌های match/not-match) را می‌بینید.

**مثال کد:**

```java
// یک auto-configuration ساده
@AutoConfiguration
@ConditionalOnClass(DataSource.class)         // فقط اگر DataSource در classpath
public class MyDataSourceAutoConfig {
    @Bean
    @ConditionalOnMissingBean                  // فقط اگر کاربر خودش تعریف نکرده
    public DataSource dataSource() {
        return new HikariDataSource();
    }
}
```

**نکات کلیدی:**

- `@ConditionalOnMissingBean` به شما اجازه می‌دهد پیش‌فرض را با تعریف bean خودتان override کنید.
- `--debug` گزارش کامل شرط‌ها را چاپ می‌کند.
- ترتیب اهمیت دارد: تعریف کاربر بر auto-config اولویت دارد.

---

### Configuration Management

**توضیح:**

`application.properties` یا `application.yml` برای تنظیمات. `@ConfigurationProperties` راه type-safe و گروه‌بندی‌شده برای bind کردن propertyها به یک شیء است (به‌جای `@Value` پراکنده). Profileها (`application-dev.yml`, `application-prod.yml`) با `spring.profiles.active` فعال می‌شوند.

ترتیب اولویت config (از بالا به پایین): command-line args، environment variables، profile-specific، application properties، defaults. این externalized configuration یکی از اصول 12-factor است.

**مثال کد:**

```java
@ConfigurationProperties(prefix = "app.payment")
@Validated
public record PaymentProperties(
    @NotBlank String apiKey,
    @Positive int timeoutSeconds,
    String currency) {}

// application.yml:
// app:
//   payment:
//     api-key: ${PAYMENT_API_KEY}   # از environment
//     timeout-seconds: 30
//     currency: USD
```

**نکات کلیدی:**

- `@ConfigurationProperties` بر `@Value` ارجح است (type-safe، گروه‌بندی، validation).
- اسرار را از environment variable بگیرید نه hardcode (12-factor).
- relaxed binding: `api-key`, `apiKey`, `API_KEY` همه map می‌شوند.

---

### Actuator

**توضیح:**

Actuator endpointهای آماده برای مانیتورینگ و مدیریت production می‌دهد: `/actuator/health` (سلامت)، `/actuator/metrics`، `/actuator/info`، `/actuator/env`، `/actuator/beans`، `/actuator/mappings`، `/actuator/prometheus` (با micrometer-registry-prometheus). می‌توان custom health indicator و custom metric ساخت.

نکته‌ی امنیتی: endpointها حاوی اطلاعات حساس‌اند؛ در production فقط `health`/`info` را expose کنید و بقیه را پشت auth بگذارید.

**مثال کد:**

```java
@Component
public class PaymentGatewayHealthIndicator implements HealthIndicator {
    private final PaymentGateway gateway;
    public PaymentGatewayHealthIndicator(PaymentGateway g) { this.gateway = g; }

    @Override
    public Health health() {
        return gateway.isReachable()
            ? Health.up().withDetail("latencyMs", gateway.ping()).build()
            : Health.down().withDetail("error", "unreachable").build();
    }
}
```

**نکات کلیدی:**

- در production فقط endpointهای لازم را expose کنید.
- health با `liveness`/`readiness` groups به K8s probeها وصل می‌شود.
- Micrometer facade است؛ به Prometheus/Datadog/… متصل می‌شود.

---

### Embedded Server

**توضیح:**

Spring Boot سرور را embed می‌کند (Tomcat پیش‌فرض، یا Jetty/Undertow؛ Netty برای WebFlux). یعنی jar خوداتکا که با `java -jar` اجرا می‌شود — مناسب کانتینر و 12-factor. تنظیمات thread pool، connection، و SSL از طریق properties. با Java 21، `spring.threads.virtual.enabled=true` هر request را روی virtual thread اجرا می‌کند.

**مثال کد:**

```yaml
server:
  port: 8080
  tomcat:
    threads:
      max: 200
      min-spare: 10
    connection-timeout: 5s
spring:
  threads:
    virtual:
      enabled: true   # Java 21+: thread-per-request مقیاس‌پذیر
```

**نکات کلیدی:**

- jar خوداتکا → مناسب کانتینر.
- virtual threads thread pool محدود را کمتر بحرانی می‌کند.

---

### Spring Boot 3.x → 4.0 Migration

**توضیح:**

نکات کلیدی مهاجرت: (۱) **Jakarta EE** — همه‌ی `javax.*` به `jakarta.*` تغییر کرده (مثلاً `javax.persistence` → `jakarta.persistence`). (۲) Java 17 حداقل (توصیه 21+). (۳) بهبود GraalVM Native Image برای startup سریع و حافظه‌ی کم. (۴) jarهای ماژولارشده در Boot 4. (۵) API Versioning داخلی در `@RequestMapping`. (۶) JSpecify برای null safety. (۷) Jackson 3 به‌عنوان پیش‌فرض.

**نکات کلیدی:**

- بزرگ‌ترین تغییر شکست‌دهنده: `javax` → `jakarta`.
- Native Image به reflection hints و AOT processing نیاز دارد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: `@SpringBootApplication` دقیقاً چه می‌کند؟

**سطح:** Mid / Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

این یک meta-annotation است که سه چیز را ترکیب می‌کند: `@Configuration` (کلاس را منبع تعریف bean می‌کند)، `@EnableAutoConfiguration` (مکانیزم auto-configuration را روشن می‌کند که بر اساس classpath و conditionها bean می‌سازد)، و `@ComponentScan` (پکیج کلاس اصلی و زیرپکیج‌ها را برای component اسکن می‌کند). به همین دلیل قرار دادن کلاس اصلی در پکیج ریشه مهم است وگرنه component scan بخش‌هایی را از دست می‌دهد.

**نکته مصاحبه:**

Senior به اهمیت محل کلاس اصلی برای component scan اشاره می‌کند. Follow-up: «اگر یک component خارج از پکیج اصلی باشد چه می‌کنی؟» (`@ComponentScan(basePackages=...)`).

---

### سوال ۲: auto-configuration چطور کار می‌کند و چطور آن را override می‌کنی؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

`@EnableAutoConfiguration` فایل `AutoConfiguration.imports` را از همه‌ی jarها می‌خواند که لیست کلاس‌های auto-config است. هر کلاس با `@Conditional`ها کنترل می‌شود (`@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`). به‌خاطر `@ConditionalOnMissingBean`، اگر شما bean خودتان را تعریف کنید، نسخه‌ی خودکار غیرفعال می‌شود — این مکانیزم اصلی override است. می‌توان یک auto-config خاص را با `spring.autoconfigure.exclude` یا `@SpringBootApplication(exclude=...)` حذف کرد. با `--debug` گزارش conditions evaluation را می‌بینید.

**نکته مصاحبه:**

تمایز Senior: دانستن `@ConditionalOnMissingBean` به‌عنوان مکانیزم override و `--debug` برای دیباگ. Follow-up: «چطور یک auto-config را کاملاً غیرفعال کنی؟»

---

### سوال ۳: `@ConfigurationProperties` در برابر `@Value` — کدام و چرا؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`@Value` برای یک مقدار منفرد ساده مناسب است اما برای config گروهی پراکنده، خطاپذیر و بدون type safety می‌شود. `@ConfigurationProperties` propertyها را به یک شیء type-safe bind می‌کند، از validation (`@Validated` + Bean Validation)، relaxed binding، nested objects و collections پشتیبانی می‌کند، و قابل تست و مستندسازی است. best practice مدرن: `@ConfigurationProperties` با record immutable.

**نکته مصاحبه:**

Follow-up: «relaxed binding چیست؟» (تطابق انعطاف‌پذیر `api-key`/`apiKey`/`API_KEY`).

---

### سوال ۴: health check در K8s چطور به Actuator وصل می‌شود؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

Actuator از Java 17/Boot با liveness و readiness groups پشتیبانی می‌کند: `/actuator/health/liveness` (آیا برنامه زنده است؟ اگر نه، K8s restart می‌کند) و `/actuator/health/readiness` (آیا آماده‌ی ترافیک است؟ اگر نه، K8s ترافیک نمی‌فرستد). این‌ها به `livenessProbe` و `readinessProbe` در K8s map می‌شوند. تمایز مهم: liveness نباید به وابستگی‌های خارجی (مثل DB) وابسته باشد وگرنه قطع موقت DB باعث restart بی‌مورد می‌شود؛ readiness می‌تواند وابستگی‌ها را چک کند.

**نکته مصاحبه:**

Lead به تفاوت liveness/readiness و خطر وابسته کردن liveness به DB اشاره می‌کند.

---

### سوال ۵: بزرگ‌ترین چالش مهاجرت Boot 2 به 3/4 چیست؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

تغییر namespace از `javax.*` به `jakarta.*` (Jakarta EE) که تقریباً همه‌ی importهای persistence، servlet، validation را تحت تأثیر قرار می‌دهد و کتابخانه‌های third-party باید نسخه‌ی سازگار داشته باشند. به‌علاوه ارتقای حداقل Java به 17، تغییرات در Spring Security (lambda DSL، حذف APIهای deprecated)، و در Boot 4 تغییر به Jackson 3. ابزارهایی مثل OpenRewrite برای خودکارسازی بخشی از مهاجرت کمک می‌کنند.

**نکته مصاحبه:**

Lead به استراتژی مهاجرت تدریجی و ابزار OpenRewrite اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: expose کردن همه‌ی Actuator endpointها در production

```yaml
# ❌ نشت اطلاعات حساس
management.endpoints.web.exposure.include: "*"
```

```yaml
# ✅
management.endpoints.web.exposure.include: health,info,prometheus
```

**توضیح:** `/env`، `/beans`، `/heapdump` اطلاعات حساس فاش می‌کنند.

---

### اشتباه ۲: hardcode کردن اسرار در application.yml

```yaml
# ❌
spring.datasource.password: myProdPassword123
```

```yaml
# ✅
spring.datasource.password: ${DB_PASSWORD}
```

**توضیح:** اسرار باید از environment/Vault بیایند، نه در repo.

---

### اشتباه ۳: قرار دادن کلاس اصلی در پکیج عمیق

```java
// ❌ component scan پکیج‌های هم‌سطح را نمی‌بیند
package com.example.app.boot;
@SpringBootApplication class App {}
```

```java
// ✅ کلاس اصلی در پکیج ریشه
package com.example.app;
@SpringBootApplication class App {}
```

**توضیح:** component scan از پکیج کلاس اصلی شروع می‌شود.

---

### اشتباه ۴: وابسته کردن liveness probe به DB

```java
// ❌ قطع DB → restart بی‌مورد pod
// liveness به DB health وابسته شود
```

```java
// ✅ DB را در readiness چک کنید نه liveness
```

**توضیح:** liveness باید فقط زنده بودن خود process را بسنجد.

---

## 🔗 ارتباط با سایر مفاهیم

- Auto-configuration روی **Spring Core** (conditional beans، BeanPostProcessor) بنا شده.
- Actuator با **Monitoring** (Prometheus/Grafana) و **Kubernetes** (probes) ترکیب می‌شود.
- Configuration externalization اصل **12-Factor App** است و با **Vault/Config Server** گره می‌خورد.
- Embedded server + virtual threads با تصمیم **MVC vs WebFlux** مرتبط است.
- مهاجرت Boot 4 با **Java 17+** و **Native Image (GraalVM)** ارتباط دارد.
