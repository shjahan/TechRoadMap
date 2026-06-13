# CI/CD — GitLab CI، GitHub Actions، Pipeline Best Practices

> اتوماسیون build/test/deploy. درک pipeline و امنیت در آن برای Senior لازم است.

---

## 📖 مفاهیم

### مفاهیم CI/CD

**توضیح:**

**CI (Continuous Integration):** ادغام مکرر کد با build و test خودکار تا مشکلات زود پیدا شوند. **CD (Continuous Delivery/Deployment):** آماده‌سازی/استقرار خودکار. pipeline مجموعه‌ای از stageها (test، build، deploy) است. ابزارها: GitLab CI (`.gitlab-ci.yml`)، GitHub Actions (`.github/workflows/`)، Jenkins.

**چرا مهم است:**

CI/CD کیفیت و سرعت تحویل را بالا می‌برد. درک pipeline و امنیت آن (supply chain) برای Senior لازم است.

**مثال کد:**

```yaml
# GitLab CI
stages: [test, build, deploy]
test:
  stage: test
  script: [mvn test]
build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
    - docker push myapp:$CI_COMMIT_SHA
deploy:
  stage: deploy
  environment: production
  script:
    - kubectl set image deployment/myapp app=myapp:$CI_COMMIT_SHA
  only: [main]
```

**نکات کلیدی:**

- از commit SHA (نه `latest`) برای tag image استفاده کنید (traceability).
- اسرار را در CI variables (نه در کد) نگه دارید.

---

### GitHub Actions

**توضیح:**

workflow با event (`push`, `pull_request`, `schedule`, `workflow_dispatch`) trigger می‌شود. Jobها (موازی)، Steps، و Actions (قابل‌استفاده‌ی مجدد). Secrets و Variables، و **matrix strategy** برای تست موازی روی چند نسخه/پلتفرم.

**مثال کد:**

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix: { java: [17, 21] }   # تست روی چند نسخه
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '${{ matrix.java }}', distribution: temurin, cache: maven }
      - run: mvn verify
```

**نکات کلیدی:**

- matrix برای تست روی چند نسخه/OS موازی.
- cache dependency (`~/.m2`) برای سرعت.

---

### Pipeline Best Practices

**توضیح:**

- **Fail fast:** test سریع اول؛ اگر شکست خورد، ادامه نده.
- **Cache dependencies** (`~/.m2`, `node_modules`) و Docker layer.
- **Parallel jobs** برای سرعت.
- **Environment-specific deployment** (dev/staging/prod).
- **Rollback strategy.**
- **Security scanning:** SAST، DAST، dependency check، container scan.

**نکات کلیدی:**

- fail fast و cache برای feedback سریع.
- security scanning را در pipeline بگنجانید (shift-left).

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا از commit SHA به‌جای `latest` برای image tag؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

tag `latest` متغیر و مبهم است: نمی‌دانید دقیقاً کدام کد در آن است، rollback سخت می‌شود، و دو محیط ممکن `latest` متفاوت داشته باشند (race در push). با tag کردن image با commit SHA (یا semantic version)، هر deploy دقیقاً به یک کد قابل‌ردیابی است؛ rollback یعنی deploy کردن SHA قبلی؛ و reproducibility تضمین می‌شود. همچنین K8s با `latest` ممکن image را re-pull نکند (cache) و نسخه‌ی قدیمی اجرا شود. best practice: SHA یا version صریح + `imagePullPolicy: IfNotPresent`.

**نکته مصاحبه:**

Senior به traceability، rollback، و مشکل cache در K8s اشاره می‌کند.

---

### سوال ۲: چطور اسرار را در CI/CD امن نگه می‌داری؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

اسرار را در secret store ابزار CI (GitLab CI/CD variables masked/protected، GitHub Secrets) نگه دارید، نه در کد یا فایل yaml. اصول: masked (در لاگ نمایش داده نشود)، protected (فقط روی branch محافظت‌شده)، و حداقل دسترسی. برای production، بهتر است CI فقط به یک secret manager (Vault) با short-lived token دسترسی داشته باشد نه نگه‌داری اسرار طولانی‌مدت. خطرات: لو رفتن secret در لاگ (با echo)، در pull request از fork (دسترسی محدود کنید)، و در artifactها. ابزار scanning برای جلوگیری از commit تصادفی secret.

**نکته مصاحبه:**

Lead به masked/protected، Vault، و خطر PR از fork اشاره می‌کند.

---

### سوال ۳: انواع security scanning در pipeline؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

- **SAST** (Static Application Security Testing): تحلیل source code برای آسیب‌پذیری (SonarQube، Checkmarx) — بدون اجرا.
- **DAST** (Dynamic): تست برنامه‌ی در حال اجرا (OWASP ZAP).
- **Dependency/SCA**: بررسی کتابخانه‌های third-party برای CVE شناخته‌شده (OWASP Dependency-Check، Snyk، Dependabot).
- **Container scanning**: بررسی image برای vulnerability (Trivy، Grype).
- **SBOM** (Software Bill of Materials): فهرست اجزا (CycloneDX، SPDX) برای traceability.

فلسفه‌ی «shift-left»: امنیت را زود (در pipeline) چک کنید نه بعد از deploy. می‌توان pipeline را در صورت یافتن آسیب‌پذیری HIGH/CRITICAL fail کرد.

**نکته مصاحبه:**

Senior انواع را تفکیک و shift-left را می‌فهمد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: استفاده از `latest` tag

```yaml
# ❌
docker build -t myapp:latest .
```

```yaml
# ✅
docker build -t myapp:$CI_COMMIT_SHA .
```

**توضیح:** `latest` traceability و rollback را خراب می‌کند.

---

### اشتباه ۲: secret در لاگ

```yaml
# ❌
script: echo "deploying with $API_KEY"  # در لاگ فاش می‌شود
```

```yaml
# ✅ masked variable، بدون echo
```

**توضیح:** echo کردن secret آن را در لاگ pipeline فاش می‌کند.

---

### اشتباه ۳: بدون cache dependency

```yaml
# ❌ هر build همه‌چیز را دوباره دانلود
```

```yaml
# ✅
cache: { paths: [.m2/repository] }
```

**توضیح:** cache نکردن feedback را کند می‌کند.

---

## 🔗 ارتباط با سایر مفاهیم

- CI/CD با **Docker (10.1)** و **Kubernetes (10.2)** deploy.
- security scanning با **DevSecOps (16.5)**.
- GitOps با **ArgoCD (16.3)** به‌عنوان مدل deploy جایگزین.
- testing در pipeline با **Testing (12.5)**.
