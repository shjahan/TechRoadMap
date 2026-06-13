# Spring Boot Testing عمیق — Test Slices، WireMock، Contract Testing

> تست پیشرفته‌ی Spring Boot: test slices برای سرعت، WireMock برای mock کردن HTTP خارجی، Pact برای contract.

---

## 📖 مفاهیم

### Test Slices

**توضیح:**

به‌جای بالا آوردن کل context با `@SpringBootTest` (کند)، test sliceها فقط بخش لازم را load می‌کنند:

| Annotation | چه load می‌شود |
|-----------|---------------|
| `@WebMvcTest` | فقط web layer |
| `@DataJpaTest` | JPA + DB |
| `@DataMongoTest` | MongoDB layer |
| `@JsonTest` | Jackson |
| `@RestClientTest` | REST client |
| `@SpringBootTest` | کل context |

هر slice فقط beanهای مرتبط را register می‌کند و بقیه را باید mock کنید.

**نکات کلیدی:**

- test slice سریع‌تر و متمرکزتر.
- `@DataJpaTest` به‌صورت پیش‌فرض transaction را rollback می‌کند.

---

### WireMock

**توضیح:**

برای mock کردن سرویس HTTP خارجی در تست. به‌جای فراخوانی واقعی API third-party (که کند، شکننده، و وابسته به دسترسی است)، WireMock یک HTTP server محلی راه می‌اندازد که پاسخ‌های از پیش تعریف‌شده (stub) می‌دهد. برای تست resilience (timeout، 500) هم عالی است.

**مثال کد:**

```java
@WireMockTest
class PaymentServiceTest {
    @Test
    void shouldHandlePaymentSuccess(WireMockRuntimeInfo wm) {
        stubFor(post("/charge")
            .willReturn(ok().withBody("{\"status\":\"success\"}")));
        // فراخوانی به wm.getHttpBaseUrl() → پاسخ stub
    }

    @Test
    void shouldHandleTimeout(WireMockRuntimeInfo wm) {
        stubFor(post("/charge").willReturn(aResponse().withFixedDelay(5000)));
        // تست رفتار circuit breaker / timeout
    }
}
```

**نکات کلیدی:**

- WireMock تست را از سرویس خارجی مستقل می‌کند.
- برای تست سناریوهای خطا (timeout، 5xx) عالی.

---

### Contract Testing با Pact

**توضیح:**

در microservices، تغییر API یک سرویس می‌تواند مصرف‌کننده را بشکند. **Consumer-driven contracts** (Pact): consumer انتظاراتش را به‌صورت contract تعریف می‌کند؛ provider در تست خود verify می‌کند که contract را برآورده می‌کند. این breaking change را قبل از deploy می‌گیرد بدون نیاز به E2E کامل.

**نکات کلیدی:**

- contract testing breaking change بین سرویس‌ها را زود می‌گیرد.
- سبک‌تر از E2E، متمرکز بر قرارداد API.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا WireMock به‌جای فراخوانی واقعی API خارجی در تست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

فراخوانی واقعی API third-party در تست مشکلات دارد: کند است (latency شبکه)، **شکننده** (اگر سرویس خارجی down یا کند باشد تست fail می‌شود — flaky)، وابسته به دسترسی شبکه و credential، و نمی‌توان سناریوهای خطا را به‌سادگی تست کرد. WireMock یک HTTP server محلی با پاسخ‌های stub راه می‌اندازد، پس تست سریع، قطعی، و مستقل است. مهم‌تر: می‌توان سناریوهای سخت مثل timeout، 500، یا پاسخ نامعتبر را شبیه‌سازی کرد تا رفتار resilience (circuit breaker، retry، fallback) را تست کرد — که با API واقعی تقریباً غیرممکن است. trade-off: WireMock رفتار واقعی API را تضمین نمی‌کند (برای آن contract testing لازم است).

**نکته مصاحبه:**

Senior به تست سناریوهای خطا و محدودیت (عدم تضمین رفتار واقعی) اشاره می‌کند.

---

### سوال ۲: contract testing چه مشکلی را حل می‌کند؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

در microservices، سرویس A (consumer) به API سرویس B (provider) وابسته است. اگر B یک تغییر شکست‌دهنده (حذف فیلد، تغییر type) بدهد، A در production می‌شکند — اما unit testهای جداگانه‌ی هر سرویس این را نمی‌گیرند و E2E کامل کند و شکننده است. contract testing (Pact، consumer-driven) این فاصله را پر می‌کند: consumer انتظاراتش از API را به‌صورت یک contract مستند می‌کند؛ provider در pipeline خود verify می‌کند که هنوز آن contract را برآورده می‌کند. اگر تغییر provider contract را بشکند، build او fail می‌شود — breaking change قبل از deploy گرفته می‌شود، بدون نیاز به بالا آوردن همه‌ی سرویس‌ها با هم. این تعادل بین unit (سریع اما ناکافی) و E2E (کامل اما کند) است.

**نکته مصاحبه:**

Lead به جایگاه contract testing بین unit و E2E اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: فراخوانی واقعی API خارجی در تست

```text
❌ تست flaky و وابسته به سرویس خارجی
✅ WireMock برای mock HTTP
```

**توضیح:** API واقعی تست را شکننده می‌کند.

---

### اشتباه ۲: تکیه‌ی کامل بر E2E برای microservices

```text
❌ E2E کند و شکننده برای همه‌ی سناریوها
✅ contract testing برای API contracts + unit
```

**توضیح:** E2E گران است؛ contract testing مکمل بهتری است.

---

## 🔗 ارتباط با سایر مفاهیم

- test slices با **Testing (12.5)** و **CI/CD (10.3)**.
- WireMock با **resilience4j (2.6)** (تست circuit breaker).
- contract testing با **microservices (6.1)** و **API versioning**.
