# OAuth 2.0، OIDC، JWT، Keycloak

> استاندارد auth در سیستم‌های مدرن. درک عمیق grant types و JWT در مصاحبه‌های Senior/Lead ضروری است.

---

## 📖 مفاهیم

### OAuth 2.0 — Roles & Grant Types

**توضیح:**

OAuth 2.0 چارچوب **authorization** (واگذاری دسترسی) است، نه authentication. چهار نقش: **Resource Owner** (کاربر)، **Client** (اپ متقاضی)، **Authorization Server** (صادرکننده‌ی token)، **Resource Server** (API محافظت‌شده).

**Grant Types:**
- **Authorization Code + PKCE:** برای web/mobile/SPA. امن‌ترین برای کلاینت‌های کاربرمحور.
- **Client Credentials:** سرویس‌به‌سرویس (بدون کاربر).
- **Device Code:** برای IoT/CLI (دستگاه بدون مرورگر).
- Deprecated: Implicit (token در URL)، Resource Owner Password (رمز را به اپ می‌دهد).

**Tokens:** Access Token (کوتاه‌عمر، برای دسترسی)، Refresh Token (بلندعمر، برای گرفتن access token جدید).

**چرا مهم است:**

استاندارد صنعتی. انتخاب grant type اشتباه = آسیب‌پذیری. درک token lifecycle برای امنیت لازم است.

**نکات کلیدی:**

- OAuth = authorization؛ برای authentication از OIDC استفاده کنید.
- Authorization Code + PKCE برای کلاینت عمومی؛ Client Credentials برای M2M.
- token storage: refresh در httpOnly cookie، access در memory.

---

### OpenID Connect (OIDC)

**توضیح:**

OIDC یک لایه‌ی **authentication** روی OAuth 2.0 است. علاوه بر access token، یک **ID Token** (JWT حاوی اطلاعات هویت کاربر مثل `sub`, `email`, `name`) صادر می‌کند. **UserInfo Endpoint** اطلاعات بیشتر کاربر را می‌دهد. **Discovery Document** (`/.well-known/openid-configuration`) endpointها و کلیدها را اعلام می‌کند. claims مثل `sub` (شناسه‌ی یکتای کاربر)، `iss`, `aud`, `exp`.

**نکات کلیدی:**

- ID Token برای authentication، Access Token برای authorization.
- `sub` شناسه‌ی پایدار کاربر است (از email استفاده نکنید چون تغییرپذیر).

---

### JWT — ساختار و validation

**توضیح:**

JWT سه بخش base64-encoded جداشده با نقطه: **Header** (الگوریتم)، **Payload** (claims)، **Signature** (امضا). امضا با:
- **HS256** (symmetric): یک کلید مشترک برای امضا و validation. ساده اما کلید باید بین auth server و همه‌ی Resource Serverها مشترک باشد (ریسک).
- **RS256/ES256** (asymmetric): کلید خصوصی برای امضا (فقط auth server)، کلید عمومی برای validation (Resource Serverها). ترجیح در microservices.

validation: signature، `exp` (expiry)، `iss` (issuer)، `aud` (audience). مشکل اصلی JWT: **revocation سخت** چون stateless. راه‌حل: expiry کوتاه + refresh token، یا blacklist.

**مثال کد:**

```yaml
# Spring Boot Resource Server — validation محلی با JWKS
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://keycloak.example.com/realms/myrealm
          # کلید عمومی از JWKS endpoint خودکار گرفته می‌شود
```

**نکات کلیدی:**

- payload فقط base64 است نه رمزنگاری‌شده → داده‌ی حساس در JWT نگذارید.
- RS256 در microservices؛ کلید خصوصی فقط در auth server.
- revocation سخت است؛ expiry کوتاه.

---

### Keycloak

**توضیح:**

Identity and Access Management متن‌باز. مفاهیم: **Realm** (tenant جداگانه با کاربران و تنظیمات خودش)، **Client** (اپ؛ انواع public/confidential/bearer-only)، **Realm Roles** (سراسری) در برابر **Client Roles** (مخصوص یک client)، **Groups**، **User Federation** (اتصال به LDAP/AD)، **Identity Provider** (federation با Google/GitHub). **Admin REST API** برای مدیریت برنامه‌نویسی‌شده. روش مدرن یکپارچگی با Spring: Keycloak به‌عنوان OAuth2/OIDC provider و Spring به‌عنوان Resource Server (adapter قدیمی deprecated شده).

**نکات کلیدی:**

- Realm برای multi-tenancy؛ هر tenant realm جدا.
- confidential client (با secret) برای backend؛ public (با PKCE) برای SPA.
- از OAuth2 Resource Server استفاده کنید نه keycloak adapter قدیمی.

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت OAuth و OIDC چیست؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

OAuth 2.0 یک چارچوب **authorization** است: به یک اپ اجازه می‌دهد بدون دانستن رمز کاربر، به منابع او دسترسی محدود داشته باشد (access token). اما OAuth خودش هویت کاربر را به اپ نمی‌گوید — به همین دلیل استفاده از OAuth خام برای login ناامن است. OIDC یک لایه‌ی نازک روی OAuth است که **authentication** اضافه می‌کند: یک **ID Token** (JWT استاندارد با claims هویتی) و UserInfo endpoint می‌دهد، پس اپ می‌داند کاربر کیست. خلاصه: OAuth برای «اجازه‌ی دسترسی»، OIDC برای «این کاربر کیست». «Login with Google» در واقع OIDC است.

**نکته مصاحبه:**

تمایز Senior: چرا OAuth خام برای authentication ناکافی است. Follow-up: «access token در برابر ID token چه تفاوتی دارد؟»

---

### سوال ۲: PKCE چیست و چرا لازم است؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

PKCE (Proof Key for Code Exchange) از حمله‌ی interception authorization code محافظت می‌کند، به‌خصوص برای کلاینت‌های عمومی (SPA، mobile) که نمی‌توانند client secret را امن نگه دارند. کلاینت یک `code_verifier` تصادفی می‌سازد و `code_challenge` (hash آن) را در درخواست اولیه می‌فرستد. هنگام تبدیل authorization code به token، `code_verifier` اصلی را ارائه می‌دهد؛ auth server hash آن را با challenge قبلی مقایسه می‌کند. اگر مهاجم code را رهگیری کند، بدون `code_verifier` نمی‌تواند آن را به token تبدیل کند. این جایگزین client secret برای کلاینت عمومی است. امروزه PKCE برای همه‌ی Authorization Code flowها (حتی confidential) توصیه می‌شود.

**نکته مصاحبه:**

Senior می‌داند PKCE حالا برای همه توصیه می‌شود نه فقط public client.

---

### سوال ۳: revocation در JWT چرا سخت است و چه راه‌حل‌هایی دارد؟

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

JWT stateless است: Resource Server با validation محلی (signature + expiry) آن را می‌پذیرد بدون پرسیدن از auth server. همین یعنی هیچ نقطه‌ای نمی‌تواند یک token صادرشده را قبل از expiry «باطل» کند — اگر token دزدیده شود تا expiry معتبر است. راه‌حل‌ها: (۱) **expiry کوتاه** (۵-۱۵ دقیقه) + **refresh token** — پنجره‌ی سوءاستفاده کوچک می‌شود و refresh token قابل revoke است. (۲) **blacklist** در Redis برای tokenهای باطل‌شده (که stateless بودن را تا حدی نقض می‌کند اما revocation فوری می‌دهد). (۳) **token introspection** به‌جای local validation (هر بار از auth server بپرس) — revocation فوری اما کندتر. (۴) token versioning (یک claim نسخه که با logout افزایش می‌یابد). معمولاً ترکیب expiry کوتاه + refresh + blacklist برای موارد بحرانی.

**نکته مصاحبه:**

تمایز Lead: چند راه‌حل و trade-off هر کدام. Follow-up: «refresh token rotation چیست؟»

---

### سوال ۴: HS256 در برابر RS256 — کدام و چرا در microservices؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

HS256 symmetric است: یک کلید مشترک هم امضا و هم validation را انجام می‌دهد. مشکل در microservices: همه‌ی Resource Serverها باید این کلید مشترک را داشته باشند تا validate کنند، اما همان کلید می‌تواند token **جعل** هم بکند — پس اگر یک سرویس compromise شود، مهاجم می‌تواند token جعلی بسازد. RS256 asymmetric است: auth server با کلید **خصوصی** امضا می‌کند و Resource Serverها فقط با کلید **عمومی** (از JWKS endpoint) validate می‌کنند؛ کلید عمومی نمی‌تواند token جعل کند. پس فاش شدن یک Resource Server امنیت امضا را نمی‌شکند. به همین دلیل RS256/ES256 در microservices استاندارد است. HS256 برای monolith ساده یا وقتی فقط یک طرف امضا و validate می‌کند قابل‌قبول است.

**نکته مصاحبه:**

Senior به «کلید عمومی نمی‌تواند جعل کند» اشاره می‌کند.

---

### سوال ۵: Realm Role در برابر Client Role در Keycloak؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Realm Roles در سطح کل realm تعریف می‌شوند و در همه‌ی clientها قابل‌استفاده‌اند (مثل `admin`, `user` سراسری). Client Roles مخصوص یک client خاص‌اند و فقط در context آن معنا دارند (مثل `order-service:manager`). استفاده: Realm Role برای نقش‌های عمومی سازمانی، Client Role برای مجوزهای ریز مخصوص یک سرویس. در token، realm roles در `realm_access.roles` و client roles در `resource_access.<client>.roles` قرار می‌گیرند که باید در `JwtAuthenticationConverter` به authorities map شوند.

**نکته مصاحبه:**

Senior می‌داند roleها کجای token قرار می‌گیرند و چطور map می‌شوند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: داده‌ی حساس در JWT payload

```text
❌ گذاشتن رمز/شماره کارت در claims (payload فقط base64 است، رمزنگاری نشده)
✅ فقط شناسه و roleهای لازم
```

**توضیح:** هر کسی می‌تواند payload را decode کند.

---

### اشتباه ۲: استفاده از Implicit flow

```text
❌ Implicit flow (token در URL fragment) — deprecated و ناامن
✅ Authorization Code + PKCE
```

**توضیح:** Implicit token را در URL فاش می‌کند؛ deprecated شده.

---

### اشتباه ۳: HS256 با کلید مشترک در چند سرویس

```text
❌ کلید مشترک → هر سرویس می‌تواند token جعل کند
✅ RS256 با کلید عمومی برای validation
```

**توضیح:** symmetric در microservices ریسک جعل دارد.

---

### اشتباه ۴: استفاده از email به‌عنوان شناسه‌ی کاربر

```text
❌ تکیه بر claim email (تغییرپذیر، گاهی verify نشده)
✅ استفاده از sub (شناسه‌ی پایدار و یکتا)
```

**توضیح:** `sub` پایدار است؛ email می‌تواند تغییر کند یا جعلی باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- OAuth/OIDC/JWT با **Spring Security (2.5)** و **API Gateway (2.6)**.
- JWT revocation با **Redis (9.1)** (blacklist).
- Keycloak با **microservices (6.1)** و multi-tenancy.
- security fundamentals با **DevSecOps (16.5)**.
