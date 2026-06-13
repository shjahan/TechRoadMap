# TypeScript — Types، Generics، Utility Types، Advanced

> TypeScript استاندارد frontend مدرن است. type system قوی آن باگ‌ها را در زمان کامپایل می‌گیرد.

---

## 📖 مفاهیم

### مبانی Type System

**توضیح:**

TypeScript یک superset از JavaScript با static typing است. `type` و `interface` برای تعریف شکل داده. **Generics** برای کد reusable و type-safe. **Discriminated Union** (با یک فیلد `kind`) برای مدل‌سازی حالت‌های مختلف با exhaustiveness check.

**مثال کد:**

```typescript
type User = { id: number; name: string; email?: string };
interface Order extends User { amount: number }

function first<T>(arr: T[]): T | undefined { return arr[0]; }

// discriminated union — مثل sealed types در Java
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rectangle'; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle': return Math.PI * shape.radius ** 2;
    case 'rectangle': return shape.width * shape.height;
    // اگر case جا بیفتد، TS با exhaustiveness خطا می‌دهد (با never)
  }
}
```

**نکات کلیدی:**

- discriminated union معادل sealed types + pattern matching در Java.
- `?` برای optional؛ `strict` mode را فعال کنید.

---

### Utility Types & Advanced

**توضیح:**

Utility Types آماده: `Partial<T>` (همه optional)، `Required<T>`, `Pick<T,K>`, `Omit<T,K>`, `Record<K,V>`. **Advanced:** Conditional Types (`T extends U ? X : Y`)، Mapped Types (`{[K in keyof T]: ...}`)، Template Literal Types، `infer`، `as const`، `satisfies` (type check بدون widening).

**مثال کد:**

```typescript
type PartialUser = Partial<User>;        // همه فیلدها optional
type UserName = Pick<User, 'name'>;      // فقط name
type UserNoId = Omit<User, 'id'>;

// satisfies: چک نوع بدون از دست دادن literal type
const config = { port: 8080, host: 'localhost' } satisfies Record<string, unknown>;
```

**نکات کلیدی:**

- utility types از تکرار جلوگیری می‌کنند.
- `satisfies` چک می‌کند بدون widening (literal type حفظ می‌شود).

---

## 🎯 سوالات مصاحبه

### سوال ۱: type در برابر interface؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

هر دو شکل داده تعریف می‌کنند و اغلب قابل‌تعویض‌اند. تفاوت‌ها: `interface` قابل **declaration merging** است (چند تعریف با هم ادغام می‌شوند — مفید برای extend کردن typeهای کتابخانه) و برای OOP-style extends طبیعی‌تر. `type` قدرتمندتر است: می‌تواند union، intersection، tuple، mapped type، و conditional type باشد که interface نمی‌تواند. قاعده‌ی رایج: برای شکل object و public API از interface (به‌خاطر merging و خوانایی پیام خطا)، برای union/utility/پیچیده از type. در عمل تیم‌ها یک convention انتخاب می‌کنند. هر دو با `strict` mode بهترین ایمنی را می‌دهند.

**نکته مصاحبه:**

Senior به declaration merging و قدرت type برای union اشاره می‌کند.

---

### سوال ۲: discriminated union چه مزیتی دارد؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

discriminated union (یا tagged union) چند نوع را با یک فیلد مشترک «discriminant» (مثل `kind`) ترکیب می‌کند. مزیت: TypeScript می‌تواند بر اساس مقدار discriminant، **type narrowing** کند — در هر شاخه‌ی switch، type دقیق شناخته می‌شود (دسترسی به فیلدهای مخصوص آن نوع type-safe). همراه با `never`، TypeScript **exhaustiveness check** می‌دهد: اگر یک حالت را پوشش ندهید، خطای کامپایل. این دقیقاً معادل sealed types + pattern matching switch در Java است و برای مدل‌سازی state machine، نتیجه‌ی API (success/error)، و حالت‌های UI ایده‌آل است — حالت‌های نامعتبر را غیرقابل‌بیان می‌کند.

**نکته مصاحبه:**

Senior به narrowing و exhaustiveness با never اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: استفاده از `any`

```typescript
// ❌ type safety را خاموش می‌کند
function process(data: any) { return data.foo.bar; }
```

```typescript
// ✅ unknown + narrowing یا type دقیق
function process(data: unknown) { if (isValid(data)) {...} }
```

**توضیح:** `any` کل هدف TypeScript را خنثی می‌کند؛ `unknown` امن‌تر است.

---

### اشتباه ۲: غیرفعال بودن strict mode

```text
❌ strict: false → null safety و چک‌های مهم خاموش
✅ strict: true در tsconfig
```

**توضیح:** strict mode بیشترین ایمنی (strictNullChecks و …) را می‌دهد.

---

## 🔗 ارتباط با سایر مفاهیم

- TypeScript با **React/Next.js (11)** و **State Management (18.2)**.
- discriminated union با **sealed types/pattern matching (1.4, 1.5)** در Java.
- generics با **Java generics (1.1)** (مفهوم مشابه).
