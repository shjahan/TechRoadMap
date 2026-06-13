# Spring Security — Authentication، Authorization، OAuth2، Keycloak

> امنیت در هر مصاحبه‌ی backend پرسیده می‌شود. درک filter chain و JWT validation تمایز Senior است.

---

## 📖 مفاهیم

### SecurityFilterChain (Spring Security 6+)

**توضیح:**

Spring Security روی زنجیره‌ای از servlet filterها بنا شده. هر request از این زنجیره عبور می‌کند و هر filter یک مسئولیت دارد: استخراج credential، authentication، authorization، CSRF، CORS، و … . از Spring Security 6، پیکربندی با bean از نوع `SecurityFilterChain` و lambda DSL انجام می‌شود (روش قدیمی `WebSecurityConfigurerAdapter` حذف شده).

ترتیب filterها مهم است: مثلاً `UsernamePasswordAuthenticationFilter`, `BearerTokenAuthenticationFilter`, `AuthorizationFilter`. درک این زنجیره برای دیباگ «چرا 401/403 می‌گیرم» ضروری است.

**چرا مهم است:**

پیکربندی اشتباه امنیت = آسیب‌پذیری جدی. درک معماری filter برای customize کردن (مثل افزودن JWT filter سفارشی) لازم است.

**مثال کد:**

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity // برای @PreAuthorize
public class SecurityConfig {

    @Bean
    SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable()) // برای API stateless با JWT
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth -> oauth.jwt(Customizer.withDefaults()))
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .build();
    }
}
```

**نکات کلیدی:**

- از Spring Security 6 از lambda DSL و `SecurityFilterChain` استفاده کنید.
- برای API با JWT، session را STATELESS و CSRF را disable کنید.
- ترتیب requestMatcherها از خاص به عام.

---

### Authentication Components

**توضیح:**

- `UserDetailsService` کاربر را بر اساس username بارگذاری می‌کند و `UserDetails` (username، password hash، authorities) برمی‌گرداند.
- `AuthenticationManager` فرایند authentication را هماهنگ می‌کند؛ به `AuthenticationProvider`ها واگذار می‌کند.
- `PasswordEncoder` رمز را hash می‌کند — همیشه از الگوریتم مدرن (BCrypt یا Argon2) استفاده کنید، هرگز plaintext یا MD5/SHA ساده.

**مثال کد:**

```java
@Bean
PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12); // strength=12، تطبیق با سخت‌افزار
}

@Service
class DbUserDetailsService implements UserDetailsService {
    private final UserRepository repo;
    DbUserDetailsService(UserRepository repo) { this.repo = repo; }

    @Override
    public UserDetails loadUserByUsername(String username) {
        User u = repo.findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException(username));
        return org.springframework.security.core.userdetails.User
            .withUsername(u.getUsername())
            .password(u.getPasswordHash())
            .roles(u.getRoles().toArray(String[]::new))
            .build();
    }
}
```

**نکات کلیدی:**

- BCrypt/Argon2 با salt خودکار؛ هرگز رمز را plaintext ذخیره نکنید.
- BCrypt strength را با قدرت سخت‌افزار تنظیم کنید (پیش‌فرض 10).

---

### Authorization & Method Security

**توضیح:**

دو سطح: URL-based (در `authorizeHttpRequests`) و method-based (`@PreAuthorize`, `@PostAuthorize`, `@Secured`). `@PreAuthorize` قبل از اجرای متد با SpEL چک می‌کند؛ `@PostAuthorize` بعد از اجرا روی نتیجه. method security قدرت بیشتری (دسترسی به آرگومان‌ها و نتیجه) می‌دهد.

**مثال کد:**

```java
@Service
class DocumentService {
    @PreAuthorize("hasRole('ADMIN') or #ownerId == authentication.name")
    public Document getDocument(String ownerId, Long docId) { /* ... */ return null; }

    @PostAuthorize("returnObject.owner == authentication.name")
    public Document loadDocument(Long id) { /* ... */ return null; }
}
```

**نکات کلیدی:**

- `@EnableMethodSecurity` را فعال کنید.
- method security با AOP کار می‌کند → self-invocation همان محدودیت.
- ترکیب URL-based و method-based برای defense in depth.

---

### CSRF — کِی لازم، کِی نه

**توضیح:**

CSRF حمله‌ای است که در آن سایت مخرب از session cookie کاربر برای ارسال request جعلی سوءاستفاده می‌کند. محافظت با CSRF token. اما CSRF فقط وقتی relevant است که از **cookie-based session** استفاده می‌کنید. برای API stateless با JWT در header `Authorization`، مرورگر آن را خودکار نمی‌فرستد پس CSRF موضوعیت ندارد و معمولاً disable می‌شود.

**نکات کلیدی:**

- API stateless + JWT header → CSRF disable منطقی است.
- اپ سنتی با session cookie → CSRF باید فعال بماند.

---

### OAuth 2.0 & OIDC

**توضیح:**

OAuth 2.0 چارچوب **authorization** (نه authentication) است. نقش‌ها: Resource Owner (کاربر)، Client (اپ)، Authorization Server (صادرکننده‌ی token)، Resource Server (API محافظت‌شده). **Grant types:** Authorization Code + PKCE (برای web/mobile)، Client Credentials (سرویس‌به‌سرویس)، Device Code (IoT/CLI). (Implicit و Password deprecated شده‌اند.)

**OIDC** لایه‌ی authentication روی OAuth است و **ID Token** (JWT با اطلاعات کاربر) اضافه می‌کند. Spring با `oauth2ResourceServer().jwt()` به‌عنوان Resource Server، token را اعتبارسنجی می‌کند (signature، expiry، issuer، audience).

**چرا مهم است:**

استاندارد صنعتی برای auth در میکروسرویس‌ها. درک تفاوت authentication/authorization و grant types ضروری است.

**مثال کد:**

```java
// تبدیل claims به authorities
@Bean
JwtAuthenticationConverter jwtAuthConverter() {
    JwtGrantedAuthoritiesConverter granted = new JwtGrantedAuthoritiesConverter();
    granted.setAuthoritiesClaimName("roles"); // claim حاوی roleها
    granted.setAuthorityPrefix("ROLE_");
    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(granted);
    return converter;
}
```

**نکات کلیدی:**

- OAuth = authorization، OIDC = authentication.
- Authorization Code + PKCE برای کلاینت‌های عمومی (SPA/mobile).
- token را همیشه validate کنید: signature + expiry + issuer + audience.

---

### JWT & Keycloak

**توضیح:**

**JWT** سه بخش دارد: Header.Payload.Signature. امضا با HS256 (symmetric، یک کلید مشترک) یا RS256/ES256 (asymmetric، کلید خصوصی برای امضا، عمومی برای validation — ترجیح در میکروسرویس چون Resource Server فقط کلید عمومی نیاز دارد). مشکل اصلی JWT: **revocation سخت است** چون stateless و تا expiry معتبر. راه‌حل: expiry کوتاه + refresh token، یا blacklist در Redis.

**Keycloak** یک Identity Provider متن‌باز است: Realm (tenant)، Client (public/confidential/bearer-only)، Realm Roles vs Client Roles، User Federation (LDAP/AD)، Identity Provider (Google/GitHub). adapter قدیمی deprecated شده؛ روش مدرن استفاده از Keycloak به‌عنوان OAuth2/OIDC provider و Spring به‌عنوان Resource Server است.

**مثال کد:**

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          # validation محلی JWT با کلید عمومی از JWKS
          issuer-uri: https://keycloak.example.com/realms/myrealm
```

**نکات کلیدی:**

- RS256 در میکروسرویس بهتر از HS256 (کلید خصوصی فاش نمی‌شود).
- JWT را نمی‌توان به‌راحتی revoke کرد → expiry کوتاه + refresh token.
- local validation (JWKS) سریع‌تر از introspection (هر بار فراخوانی auth server) است اما introspection امکان revocation فوری می‌دهد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت authentication و authorization چیست؟

**سطح:** Junior / Mid
**تکرار:** خیلی زیاد

**جواب کامل:**

Authentication یعنی «تو کی هستی؟» — تأیید هویت (با رمز، token، biometrics). Authorization یعنی «اجازه‌ی چه کاری داری؟» — کنترل دسترسی به منابع بر اساس نقش/مجوز. اول authentication، سپس authorization. OAuth 2.0 چارچوب authorization است؛ OIDC لایه‌ی authentication روی آن. در Spring، authentication منجر به یک `Authentication` در `SecurityContext` می‌شود و authorization با authorities/roles روی آن چک می‌شود.

**نکته مصاحبه:**

تمایز Senior: دانستن اینکه OAuth خودش authentication نیست (OIDC است). Follow-up: «چرا OAuth برای authentication ناکافی است؟»

---

### سوال ۲: JWT چطور validate می‌شود و revocation چرا سخت است؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

validation شامل: (۱) بررسی signature با کلید (symmetric یا کلید عمومی از JWKS endpoint)، (۲) بررسی expiry (`exp`)، (۳) بررسی issuer (`iss`) و audience (`aud`)، (۴) گاهی `nbf` (not before). اگر همه درست بود، token معتبر است — بدون فراخوانی auth server (stateless validation).

همین stateless بودن، revocation را سخت می‌کند: سرور state نگه نمی‌دارد، پس یک token دزدیده‌شده تا expiry معتبر می‌ماند. راه‌حل‌ها: expiry کوتاه (مثلاً ۵-۱۵ دقیقه) + refresh token بلندمدت؛ blacklist token در Redis (که stateless بودن را تا حدی نقض می‌کند)؛ یا token introspection (هر بار از auth server بپرس) که امکان revocation فوری می‌دهد اما کندتر است.

**نکته مصاحبه:**

تمایز Senior: trade-off بین local validation (سریع، بدون revocation) و introspection (کند، با revocation). Follow-up: «refresh token را کجا ذخیره می‌کنی؟» (httpOnly cookie، نه localStorage).

---

### سوال ۳: Authorization Code + PKCE چیست و چرا برای SPA؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

Authorization Code flow کاربر را به auth server هدایت می‌کند، یک code کوتاه‌عمر می‌گیرد، و سپس اپ آن code را با client secret به token تبدیل می‌کند. مشکل: SPA و mobile نمی‌توانند client secret را امن نگه دارند (در کد فاش می‌شود). **PKCE** این را حل می‌کند: کلاینت یک `code_verifier` تصادفی می‌سازد، `code_challenge` (hash آن) را با درخواست اولیه می‌فرستد، و هنگام تبدیل code به token، `code_verifier` اصلی را ارائه می‌دهد. auth server تطابق را چک می‌کند. این تضمین می‌کند فقط کلاینتی که flow را شروع کرده می‌تواند token بگیرد، حتی اگر code رهگیری شود — بدون نیاز به secret.

**نکته مصاحبه:**

Senior می‌داند PKCE جایگزین secret برای کلاینت عمومی است. Follow-up: «چرا Implicit flow deprecated شد؟» (token در URL fragment فاش می‌شود).

---

### سوال ۴: token introspection در برابر local JWT validation — کدام؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

local validation: Resource Server خودش JWT را با کلید عمومی (JWKS) چک می‌کند، بدون فراخوانی شبکه — سریع و scalable، اما نمی‌تواند revocation را تشخیص دهد تا expiry. introspection: هر بار Resource Server از auth server می‌پرسد token معتبر است — کندتر و وابسته به auth server، اما revocation فوری و امکان opaque token. انتخاب: برای latency و scale بالا با تحمل ریسک revocation، local؛ برای امنیت سخت‌گیرانه با نیاز revocation فوری، introspection. ترکیب رایج: local validation + expiry کوتاه + blacklist برای موارد بحرانی.

**نکته مصاحبه:**

Lead trade-off latency/scale در برابر revocation را می‌فهمد.

---

### سوال ۵: چرا CSRF را برای API با JWT disable می‌کنیم؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

حمله‌ی CSRF متکی بر این است که مرورگر cookie را خودکار با هر request به دامنه می‌فرستد، پس سایت مخرب می‌تواند از session کاربر سوءاستفاده کند. اما وقتی authentication با JWT در header `Authorization: Bearer ...` است، مرورگر این header را خودکار نمی‌فرستد؛ JavaScript اپ باید صریحاً اضافه‌اش کند. بنابراین سایت مخرب نمی‌تواند token را به request جعلی بچسباند و CSRF موضوعیت ندارد. به همین دلیل برای API stateless با JWT، CSRF disable می‌شود. اما اگر token را در cookie ذخیره کنید، CSRF دوباره relevant می‌شود.

**نکته مصاحبه:**

Senior به شرط «token در header نه cookie» اشاره می‌کند. Follow-up: «اگر JWT را در cookie بگذاری چه؟» (CSRF برمی‌گردد، SameSite لازم می‌شود).

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: ذخیره‌ی رمز به‌صورت plaintext یا hash ضعیف

```java
// ❌
user.setPassword(rawPassword);
// یا MD5/SHA-1 بدون salt
```

```java
// ✅
user.setPasswordHash(passwordEncoder.encode(rawPassword)); // BCrypt/Argon2
```

**توضیح:** رمز باید با الگوریتم مقاوم در برابر brute-force و salt خودکار hash شود.

---

### اشتباه ۲: ذخیره‌ی JWT در localStorage

```javascript
// ❌ آسیب‌پذیر در برابر XSS
localStorage.setItem('token', jwt);
```

```javascript
// ✅ httpOnly cookie (غیرقابل دسترس JS) برای refresh token
// access token در memory
```

**توضیح:** localStorage در برابر XSS آسیب‌پذیر است؛ httpOnly cookie امن‌تر.

---

### اشتباه ۳: expiry طولانی برای access token

```yaml
# ❌ token دزدیده‌شده ساعت‌ها معتبر
access-token-validity: 86400
```

```yaml
# ✅ کوتاه + refresh token
access-token-validity: 900  # 15 دقیقه
```

**توضیح:** چون revocation سخت است، پنجره‌ی سوءاستفاده را با expiry کوتاه کم کنید.

---

### اشتباه ۴: HS256 با کلید مشترک در میکروسرویس‌ها

```yaml
# ❌ هر سرویس کلید مشترک دارد → فاش شدن یکی = همه
```

```yaml
# ✅ RS256: auth server کلید خصوصی، سرویس‌ها فقط کلید عمومی
```

**توضیح:** asymmetric (RS256) کلید امضا را از Resource Serverها جدا نگه می‌دارد.

---

## 🔗 ارتباط با سایر مفاهیم

- filter chain با **Spring MVC** و معماری servlet گره خورده.
- OAuth/OIDC/Keycloak با فصل **Security (7)** و **microservices** عمیق مرتبط است.
- JWT با **Redis** (blacklist) و **API Gateway** (validation متمرکز) ترکیب می‌شود.
- method security با **AOP/proxy** (self-invocation) از Spring Core.
- `@PreAuthorize` با **DDD** و کنترل دسترسی دامنه‌ای.
