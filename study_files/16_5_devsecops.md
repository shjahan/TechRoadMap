# DevSecOps — Container Security، K8s Security Context، Vault، Scanning

> امنیت در خط لوله و runtime. shift-left security و least privilege اصول کلیدی‌اند.

---

## 📖 مفاهیم

### Container Security

**توضیح:**

- **non-root user:** container را با کاربر غیرروت اجرا کنید (در صورت escape، دسترسی محدود).
- **read-only filesystem:** جلوگیری از نوشتن غیرمنتظره.
- **minimal base image:** distroless/Alpine → attack surface کمتر.
- **no privilege escalation.**

**مثال کد:**

```dockerfile
FROM eclipse-temurin:21-jre-alpine
RUN addgroup -S app && adduser -S app -G app
USER app
```

**نکات کلیدی:**

- non-root + read-only + minimal base = دفاع پایه.

---

### K8s Security Context

**توضیح:**

`securityContext` در pod/container: `runAsNonRoot`, `runAsUser`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, drop کردن capabilities. **Network Policy** برای محدود کردن ترافیک بین podها (firewall). **Pod Security Standards** برای enforce.

**مثال کد:**

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  containers:
  - securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities: { drop: ["ALL"] }
```

**نکات کلیدی:**

- drop همه‌ی capabilities و فقط لازم را اضافه کنید (least privilege).
- Network Policy برای محدود کردن ارتباط pod (پیش‌فرض K8s همه باز است).

---

### Secret Management (Vault) & Scanning

**توضیح:**

**Vault** (Spring Cloud Vault) برای اسرار با rotation، audit، و dynamic secrets (مثل credential کوتاه‌عمر DB). در K8s، **External Secrets Operator** (sync از Vault/cloud) یا **Sealed Secrets** (encrypted در Git). **Scanning:** SAST (SonarQube)، DAST (OWASP ZAP)، dependency check (Snyk، Dependabot)، container scan (Trivy، Grype)، SBOM (CycloneDX). فلسفه‌ی **shift-left**: امنیت زود در pipeline.

**مثال کد:**

```yaml
# GitLab CI security stage
security-scan:
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL myapp:$CI_COMMIT_SHA
    - mvn org.owasp:dependency-check-maven:check
```

**نکات کلیدی:**

- Vault dynamic secrets (کوتاه‌عمر) امن‌تر از static.
- scanning در pipeline؛ fail بر HIGH/CRITICAL.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا container را non-root و read-only اجرا می‌کنیم؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

container kernel را با host share می‌کند، پس اگر مهاجم از اپ به container دسترسی یابد و container روت باشد، احتمال container escape و دسترسی به host بالا می‌رود. اجرای **non-root** سطح دسترسی مهاجم را محدود می‌کند (least privilege). **read-only filesystem** از نوشتن malware یا تغییر باینری جلوگیری می‌کند (هر چیز قابل‌نوشتن باید volume صریح باشد). همراه با `allowPrivilegeEscalation: false` و drop کردن capabilities، attack surface به‌شدت کاهش می‌یابد. این‌ها بخشی از defense in depth هستند: حتی اگر یک لایه شکست، لایه‌های دیگر مهاجم را محدود می‌کنند. ابزارهایی مثل Pod Security Standards این‌ها را enforce می‌کنند.

**نکته مصاحبه:**

Lead به container escape و defense in depth اشاره می‌کند.

---

### سوال ۲: dynamic secrets در Vault چه مزیتی دارد؟

**سطح:** Lead
**تکرار:** کم

**جواب کامل:**

static secret (مثل یک رمز DB ثابت) ریسک دارد: اگر لو برود، تا rotation دستی معتبر است و rotation دستی نادر و فراموش‌شدنی است. **dynamic secrets** در Vault: Vault به‌صورت on-demand یک credential **کوتاه‌عمر و منحصربه‌فرد** می‌سازد (مثلاً یک DB user موقت با TTL کوتاه) و پس از انقضا خودکار آن را revoke می‌کند. مزایا: اگر credential لو برود، فقط مدت کوتاهی معتبر است؛ هر سرویس/instance credential خودش را دارد (audit دقیق)؛ بدون rotation دستی. این least privilege در زمان را پیاده می‌کند. همچنین Vault می‌تواند با authentication روش K8s (service account) به pod credential بدهد بدون نگه‌داری secret طولانی.

**نکته مصاحبه:**

Lead به credential کوتاه‌عمر و کاهش پنجره‌ی سوءاستفاده اشاره می‌کند.

---

### سوال ۳: shift-left security یعنی چه؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

shift-left یعنی انجام بررسی‌های امنیتی **زود** در چرخه‌ی توسعه (سمت چپ pipeline) به‌جای بعد از deploy. به‌جای یک audit امنیتی در پایان، در هر مرحله چک کنید: SAST روی کد در commit/PR، dependency scanning برای CVE، container scanning قبل از push، و IaC scanning. مزیت: یافتن و رفع آسیب‌پذیری زود ارزان‌تر و سریع‌تر است (هرچه دیرتر، گران‌تر). می‌توان pipeline را در صورت یافتن آسیب‌پذیری بحرانی fail کرد تا کد ناامن به production نرسد. این امنیت را از مسئولیت یک تیم جداگانه به مسئولیت همه (DevSecOps) تبدیل می‌کند.

**نکته مصاحبه:**

Senior به «هرچه زودتر، ارزان‌تر» و fail pipeline اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: container روت

```dockerfile
# ❌
USER root  # یا بدون USER
```

```dockerfile
# ✅
USER app
```

**توضیح:** روت بودن ریسک escape را بالا می‌برد.

---

### اشتباه ۲: secret در ConfigMap

```yaml
# ❌ ConfigMap برای داده‌ی حساس (plaintext)
```

```yaml
# ✅ Secret + External Secrets/Vault
```

**توضیح:** ConfigMap رمزنگاری ندارد؛ secret حساس باید در Secret/Vault باشد.

---

### اشتباه ۳: Network Policy پیش‌فرض باز

```text
❌ همه‌ی podها می‌توانند به هم وصل شوند (پیش‌فرض K8s)
✅ default deny + اجازه‌ی صریح
```

**توضیح:** بدون Network Policy، lateral movement مهاجم آسان است.

---

## 🔗 ارتباط با سایر مفاهیم

- DevSecOps با **Security (7)** و **CI/CD (10.3)**.
- Vault با **Secrets Management (7.1)** و **12-Factor config**.
- security context با **Kubernetes (10.2)**.
- scanning با **supply chain security** و **SBOM**.
