# Next.js 16 — Rendering Strategies، App Router، Data Fetching

> Next.js محبوب‌ترین فریم‌ورک React برای production است. درک رندرینگ‌ها و App Router کلیدی است.

---

## 📖 مفاهیم

### Rendering Strategies

**توضیح:**

- **SSR (Server-Side Rendering):** HTML در هر request روی server render می‌شود — برای داده‌ی پویا و SEO.
- **SSG (Static Site Generation):** HTML در build time تولید می‌شود — سریع‌ترین، برای محتوای ثابت.
- **ISR (Incremental Static Regeneration):** SSG + revalidate دوره‌ای — تعادل سرعت و تازگی.
- **PPR (Partial Pre-Rendering):** پوسته‌ی static + بخش‌های dynamic که stream می‌شوند (جدید).

انتخاب بر اساس نیاز: محتوای ثابت → SSG، پویای کاربرمحور → SSR، نیمه‌پویا → ISR.

**نکات کلیدی:**

- SSG سریع‌ترین اما برای داده‌ی پویا نامناسب.
- ISR تعادل بین تازگی و performance.
- PPR ترکیب static shell + dynamic streaming.

---

### App Router

**توضیح:**

از Next.js 13، routing مبتنی بر فایل در پوشه‌ی `app/`: `app/users/[id]/page.tsx`. **Server Components پیش‌فرض**اند؛ برای interactivity از `'use client'` استفاده می‌کنید. فایل‌های خاص: `layout` (UI مشترک)، `loading` (Suspense خودکار)، `error` (error boundary)، `route.ts` (API endpoint).

**مثال کد:**

```tsx
// app/users/[id]/page.tsx — Server Component
async function UserPage({ params }: { params: { id: string } }) {
  const user = await fetchUser(params.id); // مستقیماً روی server (بدون API)
  return <UserProfile user={user} />;
}

// app/users/[id]/loading.tsx — Suspense خودکار
export default function Loading() { return <Spinner />; }
```

**نکات کلیدی:**

- Server Components پیش‌فرض؛ `'use client'` برای تعامل.
- `loading.tsx` و `error.tsx` خودکار Suspense/error boundary می‌دهند.

---

### Data Fetching & Caching

**توضیح:**

`fetch()` با گزینه‌های caching: `{ cache: 'force-cache' }` (static)، `{ next: { revalidate: 60 } }` (ISR)، `{ cache: 'no-store' }` (پویا، هر request). **Server Actions** (`'use server'`) برای mutation از client. **Cache Components** (Next.js 16) با `use cache` directive برای کنترل دقیق.

**نکات کلیدی:**

- caching در `fetch` رفتار رندرینگ را تعیین می‌کند.
- Server Actions جایگزین API route برای mutation ساده.

---

### Next.js 16 جدیدها

**توضیح:**

- **Build Adapters API:** deploy روی هر platform (نه فقط Vercel).
- **Turbopack:** bundler پیش‌فرض، سریع‌تر از Webpack.
- **PPR stable.**
- **`use cache`:** کنترل ریز caching.

**نکات کلیدی:**

- Turbopack build/dev سریع‌تر.
- Build Adapters استقلال از Vercel.

---

## 🎯 سوالات مصاحبه

### سوال ۱: SSR، SSG، ISR را مقایسه کن و کِی کدام؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

**SSG** HTML را در build time تولید می‌کند: سریع‌ترین (سرو از CDN)، بهترین برای محتوای ثابت (بلاگ، docs، landing)، اما برای داده‌ی پویا یا کاربرمحور نامناسب چون هنگام build داده ثابت می‌شود. **SSR** در هر request روی server render می‌کند: داده همیشه تازه، برای dashboard کاربرمحور و SEO با محتوای پویا، اما کندتر (server کار می‌کند در هر request) و بار بیشتر. **ISR** ترکیب است: مثل SSG static سرو می‌شود اما بعد از `revalidate` ثانیه، در پس‌زمینه دوباره تولید می‌شود — تعادل سرعت SSG و تازگی نسبی، برای محتوای نیمه‌پویا (لیست محصول که هر چند دقیقه تغییر می‌کند). انتخاب بر اساس تازگی لازم در برابر performance.

**نکته مصاحبه:**

Senior trade-off تازگی/performance هر کدام را می‌داند.

---

### سوال ۲: Server Components در App Router چه مزیتی دارند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

در App Router، componentها پیش‌فرض Server Component‌اند: روی server اجرا می‌شوند، می‌توانند مستقیماً async باشند و داده fetch کنند (حتی مستقیم از DB)، و **کد آن‌ها به client نمی‌رود** (bundle کوچک‌تر). برای interactivity (state، event handler، browser API) باید `'use client'` بگذارید تا Client Component شود. الگوی بهینه: محتوای data-heavy و static را Server Component نگه دارید و فقط بخش‌های تعاملی را Client Component کنید. مزیت: کاهش JS سمت client، امنیت (کد حساس روی server می‌ماند)، و دسترسی مستقیم به backend بدون لایه‌ی API اضافه.

**نکته مصاحبه:**

Senior الگوی «server by default, client when needed» را می‌داند.

---

### سوال ۳: caching در `fetch` Next.js چطور کار می‌کند؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

Next.js رفتار `fetch` را extend کرده تا رندرینگ را کنترل کند: `cache: 'force-cache'` (پیش‌فرض قدیمی) نتیجه را cache می‌کند و عملاً route را static می‌کند؛ `next: { revalidate: 60 }` ISR می‌دهد (cache با refresh هر ۶۰ ثانیه)؛ `cache: 'no-store'` هر بار تازه fetch می‌کند و route را dynamic می‌کند. این یعنی استراتژی رندرینگ از طریق caching در fetch تعیین می‌شود نه config جداگانه. در Next.js 16 با `use cache` directive کنترل ریزتر و صریح‌تر روی caching دارید. مهم: درک اینکه caching پیش‌فرض می‌تواند داده‌ی stale نشان دهد اگر آگاهانه تنظیم نشود.

**نکته مصاحبه:**

Senior ربط caching در fetch به استراتژی رندرینگ را می‌فهمد.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: `'use client'` روی همه‌چیز

```tsx
// ❌ کل درخت client → از دست رفتن مزیت RSC
'use client';
```

```tsx
// ✅ فقط برگ‌های تعاملی client
```

**توضیح:** `'use client'` را فقط جایی که interactivity لازم است بگذارید.

---

### اشتباه ۲: SSG برای داده‌ی کاربرمحور

```text
❌ SSG برای dashboard کاربر → داده‌ی همه یکسان/stale
✅ SSR یا client fetch برای داده‌ی کاربرمحور
```

**توضیح:** SSG داده را در build ثابت می‌کند.

---

### اشتباه ۳: نادیده گرفتن caching پیش‌فرض fetch

```text
❌ انتظار داده‌ی تازه اما fetch cache شده → stale
✅ cache: 'no-store' یا revalidate مناسب
```

**توضیح:** caching پیش‌فرض می‌تواند داده‌ی قدیمی نشان دهد.

---

## 🔗 ارتباط با سایر مفاهیم

- Next.js با **React 19 (11.1)** و Server Components.
- rendering با **Web Vitals/Performance (18.3)** و **caching (6.2)**.
- Server Actions با **API design (19.1)** و backend.
- App Router با **TypeScript (18.1)**.
