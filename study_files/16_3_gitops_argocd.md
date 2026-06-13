# GitOps با ArgoCD

> GitOps: Git به‌عنوان منبع حقیقت برای وضعیت cluster. ArgoCD آن را sync می‌کند.

---

## 📖 مفاهیم

### مفاهیم GitOps

**توضیح:**

GitOps یعنی وضعیت مطلوب cluster در Git تعریف می‌شود و یک ابزار (ArgoCD/Flux) به‌طور مداوم cluster را با Git sync می‌کند. مزایا: Git به‌عنوان single source of truth، audit کامل (تاریخچه‌ی Git)، rollback آسان (revert commit)، و **declarative** (به‌جای دستورات دستی `kubectl`). **ArgoCD** تفاوت بین Git و cluster را تشخیص و sync می‌کند.

**مثال کد:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
spec:
  source:
    repoURL: https://github.com/myorg/myapp
    targetRevision: main
    path: k8s/overlays/prod
  destination: { server: https://kubernetes.default.svc, namespace: production }
  syncPolicy:
    automated:
      prune: true       # حذف منابع حذف‌شده از Git
      selfHeal: true    # revert تغییر دستی cluster
```

**نکات کلیدی:**

- Git منبع حقیقت؛ تغییر دستی cluster خودکار revert می‌شود (selfHeal).
- rollback = revert commit در Git.
- audit کامل از طریق Git history.

---

### Sync Strategies & Progressive Delivery

**توضیح:**

**Manual** (نیاز approve) در برابر **Automated** (هر تغییر Git → deploy). **Progressive Delivery** با Argo Rollouts: **Canary** (10% → 25% → 50% → 100% تدریجی با metric analysis)، **Blue/Green** (دو environment، switch فوری). برای deploy کم‌ریسک.

**نکات کلیدی:**

- Canary برای کاهش ریسک (تدریجی + rollback خودکار اگر metric بد).
- Blue/Green برای switch فوری و rollback آنی.

---

## 🎯 سوالات مصاحبه

### سوال ۱: GitOps چه مزایایی بر deploy سنتی دارد؟

**سطح:** Senior / Lead
**تکرار:** متوسط

**جواب کامل:**

deploy سنتی (push-based با `kubectl apply` از CI) مشکلاتی دارد: CI به cluster credential نیاز دارد (سطح حمله)، تغییرات دستی track نمی‌شوند (drift)، و rollback دستی است. GitOps (pull-based) این‌ها را حل می‌کند: (۱) **Git منبع حقیقت** — وضعیت cluster همیشه با Git مطابق است؛ تغییر دستی با selfHeal خودکار revert می‌شود. (۲) **audit کامل** — هر تغییر یک commit با author و زمان است. (۳) **rollback آسان** — فقط revert commit. (۴) **امنیت** — ArgoCD داخل cluster pull می‌کند، پس CI به cluster credential نیاز ندارد. (۵) **declarative و reproducible**. trade-off: نیاز به ابزار اضافه (ArgoCD) و یادگیری، و برای secret نیاز به External Secrets/Sealed Secrets (نباید plaintext در Git).

**نکته مصاحبه:**

Lead به pull-based، selfHeal، و امنیت credential اشاره می‌کند.

---

### سوال ۲: Canary در برابر Blue/Green deployment؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

**Blue/Green** دو محیط کامل (blue=فعلی، green=جدید) دارد؛ بعد از تست green، ترافیک یکجا switch می‌شود؛ rollback فوری (برگشت به blue). مزیت: switch و rollback آنی، تست کامل قبل از switch. عیب: نیاز به دو برابر منابع، و همه‌ی کاربران یکجا به نسخه‌ی جدید می‌روند (اگر مشکل پنهان باشد، همه تأثیر می‌بینند). **Canary** نسخه‌ی جدید را تدریجی به درصد کمی از ترافیک می‌دهد (۵٪ → ۲۵٪ → ...) با تحلیل metric؛ اگر مشکل دیده شود، خودکار rollback. مزیت: blast radius کوچک (فقط درصد کمی تأثیر می‌بینند)، تشخیص زود مشکل با ترافیک واقعی. عیب: کندتر، نیاز به metric/automation و مدیریت دو نسخه‌ی همزمان. انتخاب: Canary برای ریسک‌گریزی و تغییرات بزرگ؛ Blue/Green برای switch سریع و تست کامل.

**نکته مصاحبه:**

Lead به blast radius و trade-off منابع اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: secret plaintext در Git

```text
❌ Secret در Git → نشت
✅ Sealed Secrets / External Secrets Operator
```

**توضیح:** Git همه‌چیز را history می‌کند؛ secret خام نشت دائمی است.

---

### اشتباه ۲: تغییر دستی cluster با GitOps فعال

```text
❌ kubectl edit دستی → selfHeal آن را revert می‌کند (سردرگمی)
✅ همه‌ی تغییرات از طریق Git
```

**توضیح:** با GitOps، تغییر باید در Git باشد نه دستی.

---

## 🔗 ارتباط با سایر مفاهیم

- GitOps با **Kubernetes (10.2)** و **CI/CD (10.3)**.
- secret با **External Secrets/Sealed Secrets (16.5)**.
- Helm/Kustomize (16.1) به‌عنوان منبع manifest در Git.
- progressive delivery با **resilience (15.2)**.
