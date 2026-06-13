# Infrastructure as Code — Terraform، Ansible

> IaC زیرساخت را به کد تبدیل می‌کند: قابل‌بازتولید، نسخه‌دار، و قابل‌بازبینی.

---

## 📖 مفاهیم

### Terraform

**توضیح:**

Terraform زیرساخت را به‌صورت declarative تعریف می‌کند (HCL): شما state مطلوب را می‌نویسید و Terraform تفاوت با وضعیت فعلی را محاسبه و اعمال می‌کند. مفاهیم: `provider` (مثل AWS)، `resource` (یک منبع مثل DB)، `variable`, `output`, `module` (قابل‌استفاده‌ی مجدد). **State management** قلب Terraform است: فایل state وضعیت فعلی را نگه می‌دارد؛ باید **remote** (S3/GCS) با **locking** (DynamoDB) باشد تا چند نفر همزمان کار نکنند.

دستورات: `plan` (پیش‌نمایش تغییرات)، `apply` (اعمال)، `destroy`.

**چرا مهم است:**

IaC زیرساخت را reproducible، versioned، و reviewable می‌کند — اساس DevOps و dev/prod parity (12-factor).

**مثال کد:**

```hcl
terraform {
  backend "s3" {                     # remote state
    bucket = "my-tf-state"
    key    = "prod/terraform.tfstate"
    region = "eu-west-1"
  }
}
resource "aws_db_instance" "postgres" {
  engine         = "postgres"
  engine_version = "17"
  instance_class = "db.t3.medium"
  multi_az       = true
}
```

**نکات کلیدی:**

- state را remote + locked نگه دارید (وگرنه corruption با کار همزمان).
- همیشه `plan` قبل از `apply` بررسی کنید.
- secret را در state نگذارید (state ممکن حاوی secret باشد → رمزنگاری).

---

### Ansible

**توضیح:**

Ansible برای configuration management و provisioning است: با Playbook (YAML)، Roles، و Inventory. **idempotent** است: اجرای مکرر همان playbook نتیجه‌ی یکسان می‌دهد بدون تغییر اضافه (فقط آنچه لازم است را تغییر می‌دهد). برخلاف Terraform که عمدتاً برای provisioning زیرساخت است، Ansible بیشتر برای configuration روی سرورهای موجود.

**نکات کلیدی:**

- idempotency کلید Ansible است.
- Terraform برای provisioning، Ansible برای configuration (مکمل هم).

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا state management در Terraform مهم است؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

Terraform برای محاسبه‌ی تفاوت بین وضعیت مطلوب (کد) و واقعی، به یک فایل state نیاز دارد که می‌داند چه منابعی قبلاً ساخته شده. مشکلات state محلی: (۱) اگر چند نفر همزمان apply کنند، state corrupt می‌شود — راه‌حل **state locking** (DynamoDB). (۲) state محلی share نمی‌شود — راه‌حل **remote state** (S3/GCS). (۳) state ممکن حاوی **secret** (مثل رمز DB) باشد — باید رمزنگاری at-rest و دسترسی محدود داشته باشد. (۴) دستکاری دستی منابع خارج از Terraform باعث **drift** می‌شود (state با واقعیت نمی‌خواند) — با `terraform plan` تشخیص دهید. مدیریت درست state حیاتی‌ترین جنبه‌ی عملیاتی Terraform است.

**نکته مصاحبه:**

Lead به locking، secret در state، و drift اشاره می‌کند.

---

### سوال ۲: idempotency در Ansible/IaC یعنی چه؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

idempotency یعنی اجرای مکرر همان عملیات نتیجه‌ی یکسان می‌دهد و اگر وضعیت مطلوب از قبل برقرار است، تغییری اعمال نمی‌شود. در Ansible، اکثر ماژول‌ها idempotent‌اند: مثلاً «مطمئن شو این package نصب است» — اگر نصب است کاری نمی‌کند، اگر نیست نصب می‌کند. اهمیت: می‌توان playbook را بارها امن اجرا کرد بدون ترس از side-effect یا duplicate، که برای اطمینان از convergence به وضعیت مطلوب و recovery حیاتی است. این با اسکریپت imperative (مثل bash که هر بار `mkdir` می‌زند و دوم بار error می‌دهد) تفاوت اساسی دارد.

**نکته مصاحبه:**

Senior تفاوت declarative idempotent با imperative script را می‌فهمد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: state محلی بدون locking

```text
❌ کار تیمی با state محلی → corruption
✅ remote state (S3) + locking (DynamoDB)
```

**توضیح:** apply همزمان روی state محلی آن را خراب می‌کند.

---

### اشتباه ۲: تغییر دستی منابع (drift)

```text
❌ تغییر منبع در console به‌جای Terraform → drift
✅ همه‌ی تغییرات از طریق Terraform
```

**توضیح:** drift باعث می‌شود state با واقعیت ناسازگار شود.

---

### اشتباه ۳: secret در کد Terraform

```hcl
# ❌
password = "myProdPassword"
```

```hcl
# ✅ از variable/secret manager
password = var.db_password  # از Vault/env
```

**توضیح:** secret در کد یا state فاش می‌شود.

---

## 🔗 ارتباط با سایر مفاهیم

- IaC با **12-Factor App (15.3)** (dev/prod parity).
- Terraform با **Kubernetes** و **cloud provisioning**.
- secret در state با **Vault / Secrets Management (16.5)**.
- GitOps با **ArgoCD (16.3)** (IaC برای K8s manifests).
