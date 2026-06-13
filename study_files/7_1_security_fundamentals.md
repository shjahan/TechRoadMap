# مبانی امنیت — OWASP Top 10، Injection، XSS، CSRF، Secrets

> امنیت مسئولیت هر مهندس است. OWASP Top 10 و defense in depth در مصاحبه‌های Senior پرسیده می‌شوند.

---

## 📖 مفاهیم

### OWASP Top 10

**توضیح:**

فهرست رایج‌ترین آسیب‌پذیری‌های وب: Injection (SQL، command)، Broken Authentication، XSS، Broken Access Control (IDOR)، Security Misconfiguration، SSRF، Cryptographic Failures، Vulnerable Components، Insufficient Logging. هر کدام یک کلاس از حملات است که مهندس باید بشناسد و دفاع کند.

**چرا مهم است:**

این‌ها پرتکرارترین علل نفوذ واقعی‌اند. آگاهی از آن‌ها اولین خط دفاع است.

**نکات کلیدی:**

- defense in depth: چند لایه دفاع، نه یک نقطه.
- never trust user input — همیشه validate و sanitize.

---

### SQL Injection

**توضیح:**

حمله‌ای که در آن مهاجم ورودی مخرب را به query تزریق می‌کند تا منطق SQL را تغییر دهد (مثلاً `' OR '1'='1`). علت ریشه‌ای: ساختن query با الحاق رشته‌ی ورودی کاربر. راه‌حل قطعی: **PreparedStatement / parameterized query** که داده را از کد SQL جدا می‌کند؛ ورودی هرگز به‌عنوان کد تفسیر نمی‌شود. در JPA از parameter binding (`:param`) استفاده کنید، هرگز concatenation.

**مثال کد:**

```java
// ❌ آسیب‌پذیر به SQL injection
String sql = "SELECT * FROM users WHERE email = '" + email + "'";

// ✅ PreparedStatement (parameterized)
PreparedStatement ps = conn.prepareStatement(
    "SELECT * FROM users WHERE email = ?");
ps.setString(1, email); // داده جدا از کد

// ✅ در JPA
@Query("SELECT u FROM User u WHERE u.email = :email")
Optional<User> findByEmail(@Param("email") String email);
```

**نکات کلیدی:**

- همیشه parameterized query؛ هرگز string concatenation با ورودی.
- ORM/JPA به‌صورت پیش‌فرض امن است مگر native query با concatenation بنویسید.

---

### XSS (Cross-Site Scripting)

**توضیح:**

تزریق اسکریپت مخرب در صفحه که در مرورگر قربانی اجرا می‌شود (مثلاً سرقت cookie). انواع: Stored، Reflected، DOM-based. دفاع: **output encoding** (escape کردن داده هنگام نمایش بر اساس context — HTML، JS، URL)، **Content Security Policy (CSP)** header (محدود کردن منابع اسکریپت)، و sanitize کردن HTML ورودی. fram‌ورک‌های مدرن (React) به‌صورت پیش‌فرض escape می‌کنند.

**نکات کلیدی:**

- output encoding بر اساس context (نه فقط ورودی).
- CSP header به‌عنوان لایه‌ی دوم دفاع.
- `innerHTML` و `dangerouslySetInnerHTML` خطرناک‌اند.

---

### CSRF & CORS

**توضیح:**

**CSRF:** سوءاستفاده از session cookie کاربر برای ارسال request جعلی. دفاع: CSRF token، SameSite cookie. فقط برای cookie-based auth relevant است (نه JWT در header). **CORS:** مکانیزم مرورگر برای کنترل اینکه کدام origin می‌تواند به API دسترسی داشته باشد. باید با دقت تنظیم شود؛ `Access-Control-Allow-Origin: *` با credentials خطرناک است.

**مثال کد:**

```java
// CORS امن در Spring Security
@Bean
CorsConfigurationSource corsConfig() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://app.example.com")); // نه *
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    config.setAllowCredentials(true);
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", config);
    return source;
}
```

**نکات کلیدی:**

- CSRF فقط برای cookie-based session؛ JWT header نیازی ندارد.
- CORS `*` + credentials = آسیب‌پذیری.

---

### Security Headers & Secrets Management

**توضیح:**

**Security Headers:** HSTS (اجبار HTTPS)، X-Frame-Options (جلوگیری clickjacking)، X-Content-Type-Options (nosniff)، CSP. **Secrets Management:** هرگز رمز/کلید/token را در کد یا repo hardcode نکنید؛ از environment variable، Vault، یا cloud secret manager استفاده کنید. اسرار در Git یکی از رایج‌ترین نشت‌هاست (حتی اگر بعداً حذف شوند، در history می‌مانند).

**نکات کلیدی:**

- اسرار را در environment/Vault نگه دارید، نه در کد.
- security headers لایه‌ی دفاعی ارزان و مؤثر.

---

## 🎯 سوالات مصاحبه

### سوال ۱: SQL Injection را چطور کاملاً جلوگیری می‌کنی؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

راه قطعی **parameterized query / PreparedStatement** است که داده‌ی ورودی را از ساختار SQL جدا می‌کند؛ دیتابیس ورودی را همیشه به‌عنوان مقدار (نه کد) تفسیر می‌کند، حتی اگر شامل `'` یا `OR 1=1` باشد. ORMها (JPA/Hibernate) به‌صورت پیش‌فرض از binding استفاده می‌کنند پس امن‌اند — مگر اینکه native query با string concatenation بنویسید یا از `@Query` با concatenation استفاده کنید. لایه‌های اضافی: validation ورودی (whitelist)، least privilege برای DB user، و اجتناب از dynamic SQL. اما خط دفاع اصلی parameterization است؛ escape دستی خطاپذیر است و کافی نیست.

**نکته مصاحبه:**

تمایز Senior: اشاره به اینکه escape دستی کافی نیست و parameterization راه اصلی است. Follow-up: «ORDER BY پویا با parameter ممکن نیست؛ چطور امن می‌کنی؟» (whitelist نام ستون‌ها).

---

### سوال ۲: تفاوت XSS و CSRF چیست؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

XSS تزریق و اجرای **کد مخرب در مرورگر قربانی** است؛ مهاجم اسکریپت را وارد صفحه می‌کند و در context کاربر اجرا می‌شود (سرقت token، تغییر صفحه). دفاع: output encoding و CSP. CSRF کاربر را وادار به ارسال **request ناخواسته** به سایتی که در آن authenticated است می‌کند، با سوءاستفاده از ارسال خودکار cookie توسط مرورگر؛ مهاجم کد اجرا نمی‌کند بلکه از session موجود سوءاستفاده می‌کند. دفاع: CSRF token و SameSite cookie. تفاوت کلیدی: XSS مشکل اعتماد به محتوا (اجرای کد)، CSRF مشکل اعتماد به منشأ request (هویت). نکته‌ی مهم: XSS می‌تواند هر دفاع CSRF را دور بزند، پس XSS جدی‌تر است.

**نکته مصاحبه:**

تمایز Senior: «XSS می‌تواند CSRF protection را دور بزند». 

---

### سوال ۳: IDOR چیست و چطور جلوگیری می‌شود؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

IDOR (Insecure Direct Object Reference) یک نوع Broken Access Control است: کاربر با تغییر یک شناسه در request به منبع دیگران دسترسی می‌یابد. مثلاً `/api/orders/123` که کاربر `123` را به `124` تغییر می‌دهد و سفارش کاربر دیگری را می‌بیند، چون سرور فقط authentication را چک کرده نه authorization (مالکیت). راه‌حل: همیشه در سطح سرور بررسی کنید که کاربر جاری مجاز به دسترسی به آن منبع خاص است (مثلاً `order.userId == currentUser.id`)، نه فقط اینکه login کرده. هرگز به obscurity شناسه تکیه نکنید (UUID به‌جای incremental کمک می‌کند اما کافی نیست).

**کد توضیحی:**

```java
@PreAuthorize("@orderService.isOwner(#id, authentication.name)")
@GetMapping("/orders/{id}")
public Order get(@PathVariable Long id) { /* ... */ }
```

**نکته مصاحبه:**

Senior به «authentication ≠ authorization» و بررسی مالکیت اشاره می‌کند.

---

### سوال ۴: اسرار را در production چطور مدیریت می‌کنی؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

هرگز در کد یا repo (حتی فایل config commit‌شده) hardcode نکنید — اسرار در Git history برای همیشه می‌مانند حتی اگر حذف شوند. روش‌ها به ترتیب بلوغ: environment variables (پایه، برای 12-factor)، secret manager (HashiCorp Vault، AWS Secrets Manager، Azure Key Vault) که rotation، audit و access control می‌دهد، و در K8s، External Secrets Operator یا Sealed Secrets. اصول: least privilege، rotation منظم، audit دسترسی، و رمزنگاری at-rest. اگر secret لو رفت، فوراً rotate کنید. ابزارهای scanning (git-secrets، trufflehog) برای جلوگیری از commit تصادفی.

**نکته مصاحبه:**

Lead به rotation، Vault، و خطر Git history اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: string concatenation در query

```java
// ❌ SQL injection
"SELECT * FROM users WHERE name = '" + name + "'"
```

```java
// ✅ parameterized
"SELECT * FROM users WHERE name = ?" // + setString
```

**توضیح:** الحاق ورودی به query کلاسیک‌ترین آسیب‌پذیری است.

---

### اشتباه ۲: CORS با `*` و credentials

```java
// ❌
config.setAllowedOrigins(List.of("*"));
config.setAllowCredentials(true); // ترکیب خطرناک
```

```java
// ✅ origin مشخص
config.setAllowedOrigins(List.of("https://app.example.com"));
```

**توضیح:** `*` با credentials اجازه‌ی دسترسی هر سایت با cookie کاربر می‌دهد.

---

### اشتباه ۳: hardcode کردن secret

```java
// ❌
String apiKey = "sk-live-abc123";
```

```java
// ✅
String apiKey = System.getenv("API_KEY");
```

**توضیح:** secret در کد = نشت دائمی در repo.

---

### اشتباه ۴: تکیه بر authentication بدون authorization

```java
// ❌ فقط چک login، نه مالکیت → IDOR
@GetMapping("/orders/{id}")
Order get(@PathVariable Long id) { return repo.findById(id).get(); }
```

```java
// ✅ بررسی مالکیت
```

**توضیح:** login بودن کافی نیست؛ دسترسی به منبع خاص باید چک شود.

---

## 🔗 ارتباط با سایر مفاهیم

- این مفاهیم با **Spring Security (2.5)** و **OAuth/JWT (7.2)** عمیق مرتبط است.
- secrets management با **Vault (16.5)** و **K8s Secrets (10.2)**.
- SQL injection با **PreparedStatement** و **Spring Data**.
- security scanning با **DevSecOps (16.5)** و **CI/CD**.
