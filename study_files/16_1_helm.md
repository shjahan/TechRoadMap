# Helm — Package Manager برای Kubernetes

> Helm استقرار اپ‌های K8s را با templating و versioning مدیریت می‌کند.

---

## 📖 مفاهیم

### مفاهیم اصلی

**توضیح:**

Helm «package manager» برای K8s است. **Chart** بسته‌ای از manifestهای template‌شده‌ی K8s. **Release** یک نمونه‌ی نصب‌شده از chart. **Values** پیکربندی که templateها را پر می‌کند (`values.yaml` + override per environment). به‌جای نوشتن دستی manifest برای هر محیط، یک chart با valueهای متفاوت deploy می‌کنید.

**مثال کد:**

```yaml
# values-prod.yaml
replicaCount: 3
image: { repository: myapp, tag: "1.2.0" }
resources: { limits: { cpu: 500m, memory: 512Mi } }
```

```bash
helm install myapp ./chart -f values-prod.yaml
helm upgrade myapp ./chart --set image.tag=1.2.1
helm rollback myapp 1          # برگشت به revision قبلی
helm template myapp ./chart    # render بدون install (dry-run)
```

**نکات کلیدی:**

- یک chart، چند environment با valueهای متفاوت.
- `helm rollback` به revision قبلی (Helm history نگه می‌دارد).
- `helm template`/`--dry-run` برای بررسی قبل از apply.

---

### Chart Structure

**توضیح:**

`Chart.yaml` (metadata)، `values.yaml` (پیش‌فرض)، `templates/` (manifestهای template با Go templating)، `_helpers.tpl` (snippet قابل‌استفاده‌ی مجدد)، `charts/` (dependencies). templating با `{{ .Values.x }}`.

**نکات کلیدی:**

- `_helpers.tpl` برای DRY (label، name مشترک).
- dependency chart برای زیرساخت (مثل PostgreSQL chart).

---

## 🎯 سوالات مصاحبه

### سوال ۱: Helm چه مشکلی را حل می‌کند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

بدون Helm، باید برای هر محیط (dev/staging/prod) فایل‌های manifest جداگانه نگه دارید که تکراری و خطاپذیر است (مثلاً replica، resource، image tag متفاوت). Helm با **templating** یک chart می‌سازد که با valueهای متفاوت برای هر محیط render می‌شود — DRY و قابل‌نگهداری. همچنین **release management** می‌دهد: نصب، upgrade، و **rollback** آسان به نسخه‌ی قبلی (Helm history را نگه می‌دارد)، و packaging/versioning chart برای توزیع. مزیت دیگر: dependency management (chartهای دیگر به‌عنوان dependency). جایگزین‌ها: Kustomize (overlay-based، بدون templating) که برای موارد ساده‌تر مناسب است.

**نکته مصاحبه:**

Senior به templating، rollback، و مقایسه با Kustomize اشاره می‌کند.

---

### سوال ۲: Helm در برابر Kustomize؟

**سطح:** Senior / Lead
**تکرار:** کم

**جواب کامل:**

Helm از **templating** (Go template با متغیر، شرط، حلقه) و package management (chart، release، rollback، repository) استفاده می‌کند — قدرتمند برای اپ‌های پیچیده و قابل‌توزیع، اما template می‌تواند پیچیده و سخت‌خوان شود. Kustomize از **overlay** استفاده می‌کند: یک base manifest + patchها per environment، بدون templating — ساده‌تر، declarative خالص، و بخشی از kubectl. trade-off: Helm برای packaging و توزیع اپ (به‌خصوص third-party) و logic پیچیده بهتر؛ Kustomize برای customization ساده‌ی محیط بدون پیچیدگی template. می‌توان ترکیب کرد (Helm + Kustomize post-render). انتخاب بر اساس پیچیدگی و نیاز به توزیع.

**نکته مصاحبه:**

Lead trade-off templating در برابر overlay را می‌فهمد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: hardcode کردن value در template

```text
❌ مقدار ثابت در template به‌جای .Values
✅ همه‌ی مقادیر متغیر در values.yaml
```

**توضیح:** hardcode کردن مزیت templating را از بین می‌برد.

---

### اشتباه ۲: عدم استفاده از dry-run قبل از apply

```bash
# ❌ install مستقیم بدون بررسی
helm install ...
```

```bash
# ✅
helm template / helm install --dry-run
```

**توضیح:** dry-run خطاهای render را قبل از apply نشان می‌دهد.

---

## 🔗 ارتباط با سایر مفاهیم

- Helm با **Kubernetes (10.2)** و **GitOps/ArgoCD (16.3)**.
- values per environment با **12-Factor config (15.3)**.
- جایگزین: Kustomize.
