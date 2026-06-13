# Terraform عمیق — Providers، State، Modules، Workspaces

> Terraform استاندارد IaC برای provisioning زیرساخت cloud است. state management مهم‌ترین جنبه است.

---

## 📖 مفاهیم

### مفاهیم اصلی

**توضیح:**

Terraform زیرساخت را declarative تعریف می‌کند (HCL). `provider` (AWS، GCP)، `resource` (منبع)، `variable`/`output`, `module` (گروه قابل‌استفاده‌ی مجدد). جریان: `init` (دانلود provider) → `plan` (پیش‌نمایش diff) → `apply` (اعمال) → `destroy`. **State** وضعیت فعلی را نگه می‌دارد و باید remote (S3) با locking (DynamoDB) باشد.

**مثال کد:**

```hcl
terraform {
  backend "s3" {
    bucket = "tf-state"
    key    = "prod/terraform.tfstate"
    dynamodb_table = "tf-lock"   # state locking
  }
}
resource "aws_db_instance" "postgres" {
  engine = "postgres"
  engine_version = "17"
  multi_az = true
}
```

**نکات کلیدی:**

- همیشه `plan` قبل از `apply`.
- module برای reuse (مثل یک module استاندارد برای microservice).
- Workspaces برای محیط‌های مختلف با همان کد.

---

### State Management عمیق

**توضیح:**

state حیاتی‌ترین جنبه است: Terraform از آن برای محاسبه‌ی diff استفاده می‌کند. **remote state** (S3/GCS) برای اشتراک تیمی، **state locking** (DynamoDB) برای جلوگیری از apply همزمان (corruption). state ممکن **secret** داشته باشد (رمزنگاری at-rest). **drift** وقتی منابع دستی خارج Terraform تغییر کنند (با `plan` تشخیص). `terraform import` برای آوردن منبع موجود به state.

**نکات کلیدی:**

- remote + locked state برای کار تیمی.
- state ممکن secret داشته باشد → رمزنگاری و دسترسی محدود.
- drift را با plan تشخیص دهید.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا remote state با locking لازم است؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

state محلی در کار تیمی مشکل‌ساز است: (۱) هر نفر state متفاوت دارد و apply‌ها تداخل می‌کنند. (۲) اگر دو نفر همزمان apply کنند، state corrupt می‌شود (race). remote state (S3/GCS) state را در یک محل مرکزی share می‌کند و **locking** (DynamoDB) تضمین می‌کند فقط یک apply در یک زمان اجرا شود (بقیه منتظر می‌مانند). بدون این، corruption state می‌تواند کل زیرساخت را در وضعیت ناشناخته بگذارد — یکی از خطرناک‌ترین سناریوها. به‌علاوه remote state می‌تواند secret داشته باشد، پس باید encrypted و با دسترسی محدود باشد.

**نکته مصاحبه:**

Lead به corruption از apply همزمان و secret در state اشاره می‌کند.

---

### سوال ۲: drift چیست و چطور مدیریت می‌شود؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

drift وقتی است که وضعیت واقعی زیرساخت با آنچه در state/کد Terraform است متفاوت شود — معمولاً به‌خاطر تغییر دستی در console یا توسط ابزار دیگر. مشکل: `apply` بعدی ممکن تغییر دستی را undo کند یا رفتار غیرمنتظره بدهد. مدیریت: (۱) `terraform plan` drift را نشان می‌دهد (تفاوت state با واقعیت). (۲) سیاست «همه‌ی تغییرات از طریق Terraform» (immutable infrastructure، عدم تغییر دستی). (۳) `terraform refresh`/import برای sync. (۴) در CI، plan منظم برای detect drift. بهترین راه پیشگیری است: دسترسی دستی به production را محدود کنید.

**نکته مصاحبه:**

Senior به سیاست «no manual change» و detect با plan اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: state محلی در تیم

```text
❌ corruption و تداخل
✅ remote state + locking
```

**توضیح:** apply همزمان روی state محلی خطرناک است.

---

### اشتباه ۲: secret در کد/state بدون رمزنگاری

```text
❌ secret در .tf یا state plaintext
✅ از Vault/secret manager + رمزنگاری state
```

**توضیح:** state ممکن secret داشته باشد.

---

## 🔗 ارتباط با سایر مفاهیم

- Terraform با **IaC (10.5)** و **12-Factor (15.3)**.
- state secret با **Vault (16.5)**.
- module با **DRY** و reuse.
