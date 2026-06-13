# Spring Authorization Server

> برای ساخت OAuth2/OIDC Authorization Server اختصاصی با Spring.

---

## 📖 مفاهیم

### مفاهیم اصلی

**توضیح:**

Spring Authorization Server امکان ساخت یک OAuth2/OIDC provider اختصاصی را می‌دهد (جایگزین Keycloak وقتی نیاز به کنترل کامل دارید). مفاهیم: **RegisteredClient** (تعریف client با grant types، redirect URI، scopes)، **JWKS endpoint** (کلیدهای عمومی برای validation)، **OAuth2TokenCustomizer** (افزودن claim سفارشی به token).

**چرا مهم است:**

وقتی Keycloak یا provider خارجی مناسب نیست و نیاز به auth server embedded و سفارشی دارید.

**مثال کد:**

```java
@Bean
public RegisteredClientRepository registeredClientRepository(PasswordEncoder encoder) {
    RegisteredClient client = RegisteredClient.withId(UUID.randomUUID().toString())
        .clientId("my-client")
        .clientSecret(encoder.encode("secret"))
        .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
        .authorizationGrantType(AuthorizationGrantType.REFRESH_TOKEN)
        .redirectUri("http://localhost:8080/login/oauth2/code/my-client")
        .scope(OidcScopes.OPENID)
        .scope("read")
        .build();
    return new InMemoryRegisteredClientRepository(client);
}

// افزودن claim سفارشی
@Bean
public OAuth2TokenCustomizer<JwtEncodingContext> tokenCustomizer() {
    return context -> context.getClaims().claim("tenant", "acme");
}
```

**نکات کلیدی:**

- Authorization Code + PKCE برای user-facing؛ Client Credentials برای M2M.
- JWKS endpoint کلید عمومی برای Resource Serverها فراهم می‌کند.
- token customizer برای claim دامنه‌ای (مثل tenant، roles).

---

## 🎯 سوالات مصاحبه

### سوال ۱: کِی auth server اختصاصی به‌جای Keycloak؟

**سطح:** Lead
**تکرار:** کم

**جواب کامل:**

Keycloak یک محصول کامل و آماده است که اکثر نیازها را پوشش می‌دهد (UI مدیریت، federation، social login) — برای اکثر موارد انتخاب درست. Spring Authorization Server وقتی منطقی است که: نیاز به کنترل کامل و سفارشی‌سازی عمیق token/flow دارید، می‌خواهید auth را در همان اکوسیستم Spring و codebase نگه دارید (بدون سرویس جداگانه)، یا الزامات خاص (مثل integration عمیق با domain) دارید. trade-off: با auth server اختصاصی، خودتان مسئول امنیت، نگهداری، UI، و feature‌ها (federation، MFA) می‌شوید — که Keycloak آماده می‌دهد. توصیه: مگر دلیل قوی، Keycloak یا provider مدیریت‌شده را ترجیح دهید چون auth حساس و پرریسک است.

**نکته مصاحبه:**

Lead به مسئولیت امنیتی ساخت auth اختصاصی و ترجیح راه‌حل آماده اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: ذخیره‌ی client در حافظه برای production

```java
// ❌ InMemory → با restart از بین می‌رود
new InMemoryRegisteredClientRepository(client);
```

```java
// ✅ JDBC-backed برای production
JdbcRegisteredClientRepository
```

**توضیح:** in-memory فقط برای dev/test مناسب است.

---

### اشتباه ۲: client secret بدون encode

```java
// ❌ plaintext secret
.clientSecret("secret")
```

```java
// ✅
.clientSecret(encoder.encode("secret"))
```

**توضیح:** secret باید hash شده ذخیره شود.

---

## 🔗 ارتباط با سایر مفاهیم

- با **OAuth/OIDC/JWT (7.2)** و **Spring Security (2.5)**.
- token customizer با **multi-tenancy** و **Keycloak (مقایسه)**.
- JWKS با **Resource Server** validation.
