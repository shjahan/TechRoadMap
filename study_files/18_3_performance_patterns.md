# Frontend Performance Patterns — Code Splitting، Virtualization، Web Vitals

> performance frontend مستقیماً روی UX و SEO اثر دارد. Web Vitals معیار استاندارد است.

---

## 📖 مفاهیم

### Code Splitting & Virtualization

**توضیح:**

**Code Splitting** با `lazy()` + `Suspense`: به‌جای bundle بزرگ یکجا، کد را به chunkهای lazy تقسیم می‌کنید که فقط هنگام نیاز load می‌شوند → initial load سریع‌تر. **Virtualization** (`react-window`, TanStack Virtual): برای لیست‌های بزرگ، فقط آیتم‌های visible را render می‌کند (نه هزاران آیتم) → DOM سبک.

**مثال کد:**

```typescript
const Dashboard = lazy(() => import('./Dashboard')); // فقط هنگام نیاز load

<Suspense fallback={<Loading />}>
  <Dashboard />
</Suspense>

// virtualization
const rowVirtualizer = useVirtualizer({
  count: 100000,                        // 100k آیتم
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
}); // فقط visible render می‌شوند
```

**نکات کلیدی:**

- code splitting initial bundle را کوچک می‌کند.
- virtualization برای لیست هزاران آیتمی ضروری است.

---

### Web Vitals

**توضیح:**

معیارهای Google برای UX:
- **LCP** (Largest Contentful Paint) < 2.5s — سرعت نمایش محتوای اصلی.
- **INP** (Interaction to Next Paint، جایگزین FID) < 200ms — پاسخ‌دهی به تعامل.
- **CLS** (Cumulative Layout Shift) < 0.1 — ثبات layout (جابه‌جایی ناگهانی).
- **TTFB** (Time to First Byte) < 800ms.

بهبود: SSR/SSG، image optimization، code splitting، CDN، font optimization (جلوگیری از layout shift).

**نکات کلیدی:**

- Web Vitals روی SEO (رتبه‌ی Google) هم اثر دارد.
- CLS با تعیین ابعاد image/ad و font preload بهبود می‌یابد.

---

## 🎯 سوالات مصاحبه

### سوال ۱: Web Vitals را توضیح بده و چطور بهبود می‌دهی؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

سه core Web Vital: **LCP** (سرعت نمایش بزرگ‌ترین محتوا، هدف <2.5s) — بهبود با SSR/SSG، CDN، image optimization، و کاهش render-blocking resources. **INP** (پاسخ‌دهی به تعامل کاربر، <200ms) — بهبود با کاهش کار سنگین روی main thread (code splitting، web worker، debounce). **CLS** (پایداری بصری، <0.1) — بهبود با تعیین ابعاد صریح برای image/video/ad و font preload (جلوگیری از جابه‌جایی محتوا هنگام load). این‌ها روی هم UX و رتبه‌ی SEO Google را تعیین می‌کنند. اندازه‌گیری با Lighthouse، PageSpeed Insights، و RUM (Real User Monitoring) در production.

**نکته مصاحبه:**

Senior هر سه vital و راه بهبود مشخص را می‌داند.

---

### سوال ۲: چرا virtualization برای لیست بزرگ لازم است؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

اگر یک لیست با هزاران آیتم را مستقیماً render کنید، هزاران DOM node ساخته می‌شود — حافظه‌ی زیاد، render کند، و scroll lag. **virtualization** فقط آیتم‌هایی را که در viewport visible هستند (مثلاً ۲۰ تا) render می‌کند و بقیه را با spacer شبیه‌سازی می‌کند؛ هنگام scroll، آیتم‌های جدید render و قدیمی‌ها unmount می‌شوند. نتیجه: DOM سبک (ثابت، مستقل از تعداد کل آیتم)، render سریع، و scroll روان حتی برای ۱۰۰هزار آیتم. کتابخانه‌ها: react-window، TanStack Virtual. trade-off: پیچیدگی بیشتر و مشکل با ارتفاع متغیر آیتم‌ها (نیاز به estimate). برای لیست/جدول بزرگ ضروری است.

**نکته مصاحبه:**

Senior به DOM ثابت مستقل از تعداد آیتم اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: render کل لیست بزرگ

```text
❌ map روی 10k آیتم → هزاران DOM node، lag
✅ virtualization
```

**توضیح:** DOM بزرگ performance را نابود می‌کند.

---

### اشتباه ۲: image بدون ابعاد → CLS

```html
<!-- ❌ layout shift هنگام load -->
<img src="..." />
```

```html
<!-- ✅ ابعاد صریح -->
<img src="..." width="600" height="400" />
```

**توضیح:** بدون ابعاد، محتوا هنگام load image جابه‌جا می‌شود (CLS بد).

---

## 🔗 ارتباط با سایر مفاهیم

- performance با **React (11.1)** و **Next.js rendering (11.2)**.
- Web Vitals با **SSR/SSG** و **CDN/caching (6.2)**.
- code splitting با **bundle optimization**.
