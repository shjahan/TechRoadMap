# Kubernetes — Pod، Deployment، Service، Scaling، Health Checks

> Kubernetes استاندارد orchestration است. probes، scaling و resource management موضوعات کلیدی Senior/Lead هستند.

---

## 📖 مفاهیم

### مفاهیم پایه

**توضیح:**

- **Pod:** کوچک‌ترین واحد deploy؛ یک یا چند container که شبکه و storage را share می‌کنند.
- **Deployment:** مدیریت desired state و rolling update برای appهای stateless.
- **Service:** آدرس پایدار برای دسترسی به podها (که IP متغیر دارند): ClusterIP (داخلی)، NodePort، LoadBalancer (خارجی)، ExternalName.
- **Ingress:** routing L7 و SSL termination.
- **ConfigMap** (config غیرحساس)، **Secret** (حساس، base64).
- **Namespace** (ایزولاسیون منطقی).
- **Control Plane:** API Server، etcd (state)، Scheduler، Controller Manager.

**چرا مهم است:**

K8s declarative است: شما state مطلوب را اعلام می‌کنید و K8s آن را حفظ می‌کند (self-healing، scaling). Service مشکل آدرس پویای pod را حل می‌کند.

**نکات کلیدی:**

- Deployment برای stateless، StatefulSet برای stateful.
- Service آدرس پایدار روی podهای متغیر می‌دهد.
- declarative: desired state، K8s reconcile می‌کند.

---

### Workloads

**توضیح:**

- **Deployment:** stateless apps با rolling update.
- **StatefulSet:** stateful apps (DB، Kafka) — هویت پایدار، storage پایدار، ترتیب راه‌اندازی.
- **DaemonSet:** یک pod روی هر node (logging/monitoring agent).
- **Job/CronJob:** کار یک‌باره/زمان‌بندی‌شده.
- **ReplicaSet:** توسط Deployment مدیریت می‌شود (تعداد replica).

**نکات کلیدی:**

- DB را با StatefulSet (نه Deployment) اجرا کنید (هویت و storage پایدار).
- CronJob برای کارهای دوره‌ای.

---

### Health Checks (Probes)

**توضیح:**

سه probe:

- **Liveness:** آیا container زنده است؟ اگر fail شود، K8s container را **restart** می‌کند.
- **Readiness:** آیا آماده‌ی دریافت ترافیک است؟ اگر fail شود، K8s از Service خارجش می‌کند (ترافیک نمی‌فرستد) اما restart نمی‌کند.
- **Startup:** برای appهای با startup کند؛ تا کامل شدن، liveness/readiness معلق می‌مانند.

نکته‌ی حیاتی: **liveness نباید به وابستگی خارجی (DB) وابسته باشد**؛ وگرنه قطع موقت DB باعث restart مکرر کل podها می‌شود. readiness می‌تواند وابستگی را چک کند.

**مثال کد:**

```yaml
livenessProbe:
  httpGet: { path: /actuator/health/liveness, port: 8080 }
  initialDelaySeconds: 30
  periodSeconds: 10
readinessProbe:
  httpGet: { path: /actuator/health/readiness, port: 8080 }
  periodSeconds: 5
```

**نکات کلیدی:**

- liveness = restart، readiness = حذف از ترافیک.
- liveness را به DB وابسته نکنید.
- startup probe برای JVM با startup طولانی.

---

### Scaling

**توضیح:**

- **HPA (Horizontal Pod Autoscaler):** تعداد pod را بر اساس CPU/Memory/custom metric تنظیم می‌کند.
- **VPA (Vertical):** منابع هر pod را تنظیم می‌کند.
- **KEDA:** event-driven autoscaling (مثلاً بر اساس Kafka lag، طول queue) — حتی scale to zero.

**نکات کلیدی:**

- HPA به metrics server و resource request نیاز دارد.
- KEDA برای scale بر اساس event (lag صف) بهتر از CPU است.

---

### Resource Management

**توضیح:**

`requests` (حداقل تضمین‌شده، برای scheduling) و `limits` (سقف). **QoS Classes:** Guaranteed (request = limit)، Burstable (request < limit)، BestEffort (بدون تعریف). pod با memory limit که از آن بگذرد **OOMKilled** می‌شود. **LimitRange** و **ResourceQuota** برای کنترل در سطح namespace.

نکته‌ی Java: JVM باید container memory limit را respect کند (`-XX:MaxRAMPercentage` یا نسخه‌های جدید خودکار). بدون آن، JVM ممکن heap بزرگ‌تر از limit بگیرد و OOMKilled شود.

**مثال کد:**

```yaml
resources:
  requests: { memory: "256Mi", cpu: "250m" }
  limits: { memory: "512Mi", cpu: "500m" }
```

**نکات کلیدی:**

- بدون request، scheduling و HPA درست کار نمی‌کند.
- memory limit بیش از حد پایین → OOMKilled.
- JVM باید container-aware باشد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: تفاوت liveness و readiness probe چیست؟

**سطح:** Senior / Lead
**تکرار:** خیلی زیاد

**جواب کامل:**

**liveness** می‌پرسد «آیا این container باید restart شود؟» — اگر fail شود، K8s container را kill و restart می‌کند. برای تشخیص deadlock یا حالت غیرقابل‌بازیابی. **readiness** می‌پرسد «آیا این pod آماده‌ی ترافیک است؟» — اگر fail شود، K8s pod را از endpointهای Service حذف می‌کند (ترافیک نمی‌فرستد) اما restart نمی‌کند؛ وقتی دوباره ready شود، برمی‌گردد. برای زمان warmup یا وقتی موقتاً busy/وابستگی در دسترس نیست.

تله‌ی مهم: liveness را به وابستگی خارجی (مثل DB) وابسته نکنید — اگر DB موقتاً قطع شود، همه‌ی podها liveness fail می‌کنند و restart می‌شوند که نه‌تنها کمکی نمی‌کند بلکه طوفان restart می‌سازد. وابستگی‌ها را در readiness چک کنید (pod از ترافیک خارج می‌شود تا DB برگردد، بدون restart).

**نکته مصاحبه:**

تمایز Lead: تله‌ی وابسته کردن liveness به DB. Follow-up: «startup probe چه مشکلی را حل می‌کند؟»

---

### سوال ۲: requests در برابر limits — چه تفاوتی و چرا مهم؟

**سطح:** Senior / Lead
**تکرار:** زیاد

**جواب کامل:**

`requests` مقداری است که pod **تضمین‌شده** می‌گیرد و scheduler بر اساس آن pod را روی node جا می‌دهد. `limits` **سقف** مصرف است. برای CPU، عبور از limit منجر به throttling می‌شود (کند شدن، نه kill). برای memory، عبور از limit منجر به **OOMKilled** می‌شود. QoS: اگر request=limit → Guaranteed (کمترین احتمال evict)، request<limit → Burstable، بدون تعریف → BestEffort (اول evict می‌شود). تنظیم اشتباه: limit حافظه‌ی کم → OOMKill مکرر؛ request بیش از حد → هدر منابع و scheduling ضعیف. برای Java، JVM باید container limit را respect کند (`-XX:MaxRAMPercentage=75`) وگرنه heap از limit می‌گذرد و OOMKilled می‌شود.

**نکته مصاحبه:**

Lead به QoS، OOMKill، و JVM container-awareness اشاره می‌کند.

---

### سوال ۳: rolling update چطور کار می‌کند و چطور rollback می‌کنی؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Deployment با rolling update به‌تدریج podهای نسخه‌ی قدیم را با جدید جایگزین می‌کند (با `maxSurge` و `maxUnavailable` کنترل می‌شود) تا downtime صفر باشد. K8s قبل از routing ترافیک به pod جدید، readiness آن را چک می‌کند. اگر نسخه‌ی جدید مشکل داشته باشد و readiness fail کند، rollout متوقف می‌شود (podهای قدیم سرپا می‌مانند). rollback با `kubectl rollout undo deployment/app` به revision قبلی برمی‌گردد (K8s history نگه می‌دارد). برای deploy امن‌تر، canary یا blue/green با ابزارهایی مثل Argo Rollouts.

**نکته مصاحبه:**

Senior به نقش readiness در rolling update و `rollout undo` اشاره می‌کند.

---

### سوال ۴: HPA چطور کار می‌کند و KEDA چه چیزی اضافه می‌کند؟

**سطح:** Lead
**تکرار:** متوسط

**جواب کامل:**

HPA به‌صورت دوره‌ای metric (پیش‌فرض CPU/Memory) را با target مقایسه می‌کند و تعداد replica را تنظیم می‌کند تا metric به target نزدیک شود. نیاز به metrics server و resource request دارد. محدودیت: CPU/Memory همیشه معیار خوبی نیستند — مثلاً یک consumer که از Kafka lag دارد ممکن CPU پایین داشته باشد اما نیاز به scale up. **KEDA** این را حل می‌کند: scale بر اساس event sourceهای خارجی (Kafka lag، طول صف RabbitMQ، متریک Prometheus) و حتی **scale to zero** (وقتی کاری نیست، صفر pod). KEDA برای workloadهای event-driven مناسب‌تر است.

**نکته مصاحبه:**

Lead محدودیت CPU-based HPA و مزیت KEDA (scale on lag، scale to zero) را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: liveness وابسته به DB

```yaml
# ❌ قطع DB → restart همه‌ی podها
livenessProbe: { httpGet: { path: /health-with-db } }
```

```yaml
# ✅ DB در readiness
livenessProbe: { httpGet: { path: /actuator/health/liveness } }
```

**توضیح:** وابسته کردن liveness به DB طوفان restart می‌سازد.

---

### اشتباه ۲: بدون resource requests

```yaml
# ❌ scheduling ضعیف، HPA کار نمی‌کند
containers: [{ name: app }]
```

```yaml
# ✅
resources: { requests: { cpu: 250m, memory: 256Mi } }
```

**توضیح:** بدون request، scheduler و HPA معیار ندارند.

---

### اشتباه ۳: JVM بدون container-awareness

```text
❌ JVM heap بزرگ‌تر از memory limit → OOMKilled
✅ -XX:MaxRAMPercentage=75 (یا JDK جدید خودکار)
```

**توضیح:** JVM قدیمی container limit را نمی‌دید.

---

### اشتباه ۴: DB با Deployment به‌جای StatefulSet

```text
❌ Deployment برای DB → هویت/storage ناپایدار
✅ StatefulSet با PersistentVolume
```

**توضیح:** stateful workload به هویت و storage پایدار نیاز دارد.

---

## 🔗 ارتباط با سایر مفاهیم

- K8s probes با **Spring Boot Actuator (2.2)** (liveness/readiness groups).
- HPA/scaling با **System Design (6.2)** (horizontal scaling) و **Kafka lag (8.1)**.
- Secret management با **Vault، External Secrets (16.5)**.
- StatefulSet با **PostgreSQL/Kafka** و **replication**.
- resource management با **JVM tuning (12.6)**.
