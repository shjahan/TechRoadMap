# State Management عمیق — Zustand، TanStack Query

> مدیریت state در React: client state با Zustand، server state با TanStack Query.

---

## 📖 مفاهیم

### Zustand (Client State)

**توضیح:**

Zustand یک کتابخانه‌ی state management ساده و مدرن است (جایگزین سبک Redux). با `create` یک store می‌سازید؛ component با hook subscribe می‌کند و فقط با تغییر بخش مورد استفاده re-render می‌شود (selective subscription). بدون boilerplate Redux (action، reducer، dispatch).

**مثال کد:**

```typescript
interface UserStore {
  users: User[];
  loading: boolean;
  fetchUsers: () => Promise<void>;
  addUser: (user: User) => void;
}

const useUserStore = create<UserStore>((set, get) => ({
  users: [],
  loading: false,
  fetchUsers: async () => {
    set({ loading: true });
    const users = await api.getUsers();
    set({ users, loading: false });
  },
  addUser: (user) => set(state => ({ users: [...state.users, user] })),
}));

// در component: فقط با تغییر users re-render
const users = useUserStore(state => state.users);
```

**نکات کلیدی:**

- selective subscription (selector) از re-render بی‌مورد جلوگیری می‌کند.
- Zustand برای client/UI state ساده‌تر از Redux.

---

### TanStack Query (Server State)

**توضیح:**

TanStack Query (React Query) برای **server state** است: caching، background refetch، stale-while-revalidate، deduplication، retry، و optimistic update — همه خودکار. به‌جای مدیریت دستی loading/error/cache در useEffect یا Redux.

**مثال کد:**

```typescript
const { data, isLoading, error } = useQuery({
  queryKey: ['users', userId],
  queryFn: () => api.getUser(userId),
  staleTime: 5 * 60 * 1000,        // 5 دقیقه fresh
});

const mutation = useMutation({
  mutationFn: api.createUser,
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
});
```

**نکات کلیدی:**

- `queryKey` کلید cache و invalidation است.
- `staleTime` کنترل می‌کند کِی refetch شود.
- mutation + invalidateQueries برای sync بعد از تغییر.

---

## 🎯 سوالات مصاحبه

### سوال ۱: چرا server state را با TanStack Query نه Redux؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

server state ویژگی‌های خاصی دارد که با client state فرق می‌کند: async است، می‌تواند stale شود، توسط چند کاربر تغییر کند، و نیاز به caching/refetch/sync دارد. مدیریت آن با Redux یعنی نوشتن دستی action برای loading/success/error، caching دستی، invalidation دستی، و refetch — کد زیاد و خطاپذیر. TanStack Query مخصوص server state است و همه‌ی این‌ها را خودکار می‌دهد: caching هوشمند با queryKey، background refetch، stale-while-revalidate (نمایش cache قدیمی + refresh)، deduplication (چند component با یک query → یک fetch)، retry، و optimistic update. نتیجه: کد بسیار کمتر و رفتار بهتر. Redux/Zustand برای **client state** (UI: مودال، فرم، تب) می‌ماند.

**نکته مصاحبه:**

Senior جداسازی server/client state و ابزار درست هر کدام را می‌داند.

---

### سوال ۲: optimistic update چیست؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

optimistic update یعنی UI را **فوراً** (قبل از تأیید سرور) به‌روز کنید، با این فرض که عملیات موفق خواهد بود — برای تجربه‌ی سریع و responsive (مثل like کردن که فوراً نمایش داده می‌شود). اگر سرور موفق شد، تغییر می‌ماند؛ اگر fail شد، **rollback** به حالت قبلی + نمایش خطا. در TanStack Query با `onMutate` (اعمال خوش‌بینانه + ذخیره‌ی snapshot)، `onError` (rollback)، و `onSettled` (refetch برای sync). مزیت: UX بهتر (بدون انتظار). ریسک: باید rollback را درست مدیریت کنید وگرنه UI ناسازگار با سرور می‌ماند. مناسب برای عملیات با احتمال موفقیت بالا و کم‌ریسک.

**نکته مصاحبه:**

Senior به rollback در onError اشاره می‌کند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: server state در Redux

```text
❌ مدیریت دستی fetch/cache/loading در Redux
✅ TanStack Query
```

**توضیح:** server state ابزار مخصوص می‌خواهد.

---

### اشتباه ۲: subscribe به کل store بدون selector

```typescript
// ❌ هر تغییر store → re-render
const store = useUserStore();
```

```typescript
// ✅ selector
const users = useUserStore(s => s.users);
```

**توضیح:** بدون selector، component با هر تغییر store re-render می‌شود.

---

## 🔗 ارتباط با سایر مفاهیم

- state management با **React (11.1)** و **TypeScript (18.1)**.
- server state با **API design (19.1)** و caching.
- optimistic با **useOptimistic (React 19)**.
