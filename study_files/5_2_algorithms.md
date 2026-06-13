# Algorithms — Sorting، Search، DP، Greedy، Complexity

> الگوریتم‌ها در مصاحبه‌های coding و تحلیل complexity در طراحی سیستم پرسیده می‌شوند.

---

## 📖 مفاهیم

### Sorting

**توضیح:**

الگوریتم‌های مرتب‌سازی با complexity و پایداری (stability) متفاوت:

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | بله |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | خیر |
| Heap | O(n log n) | O(n log n) | O(n log n) | O(1) | خیر |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | بله |
| TimSort (Java) | O(n) | O(n log n) | O(n log n) | O(n) | بله |

**stability** یعنی ترتیب نسبی عناصر مساوی حفظ شود — مهم برای مرتب‌سازی چندمرحله‌ای. Java برای object از **TimSort** (ترکیب merge + insertion، پایدار) و برای primitive از dual-pivot quicksort استفاده می‌کند.

**چرا مهم است:**

انتخاب الگوریتم و درک stability در عمل (مثل مرتب‌سازی بر چند کلید) لازم است. quicksort worst case O(n²) دارد که با pivot بد رخ می‌دهد.

**مثال کد:**

```java
List<Person> people = new ArrayList<>(/* ... */);
// مرتب‌سازی پایدار چندمرحله‌ای: اول name بعد age (stability حفظ می‌شود)
people.sort(Comparator.comparing(Person::name));
people.sort(Comparator.comparingInt(Person::age)); // ترتیب name در مساوی‌ها حفظ
// یا یک‌جا:
people.sort(Comparator.comparingInt(Person::age).thenComparing(Person::name));
```

**نکات کلیدی:**

- Java: TimSort (object، پایدار)، dual-pivot quicksort (primitive، ناپایدار).
- stability برای مرتب‌سازی روی چند کلید مهم است.
- quicksort worst case O(n²)؛ TimSort تضمین O(n log n).

---

### Search — Binary Search

**توضیح:**

binary search روی داده‌ی مرتب O(log n). نکات: مراقب overflow در محاسبه‌ی mid باشید (`low + (high - low) / 2` نه `(low + high) / 2`)، و درست مدیریت کردن مرزها. الگوی قدرتمند **binary search on answer**: وقتی فضای جواب monotonic است (مثلاً «کمترین ظرفیتی که شرط را برآورده می‌کند»)، روی جواب binary search می‌کنیم.

**مثال کد:**

```java
static int binarySearch(int[] arr, int target) {
    int low = 0, high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2; // جلوگیری از overflow
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
```

**نکات کلیدی:**

- overflow را با `low + (high-low)/2` رفع کنید.
- binary search on answer برای مسائل بهینه‌سازی monotonic.

---

### Dynamic Programming

**توضیح:**

DP مسائلی را که **overlapping subproblems** و **optimal substructure** دارند حل می‌کند، با ذخیره‌ی نتایج زیرمسائل. دو روش: **memoization** (top-down، recursion + cache) و **tabulation** (bottom-up، پر کردن جدول). مهم‌ترین مرحله **تعریف state** است (چه چیزی زیرمسئله را یکتا مشخص می‌کند). مسائل کلاسیک: Fibonacci، Knapsack، LCS، LIS، Edit Distance، Coin Change. بهینه‌سازی فضا با rolling array.

**چرا مهم است:**

DP سخت‌ترین دسته‌ی سوالات coding است. درک تشخیص الگو و تعریف state کلید است.

**مثال کد:**

```java
// Coin Change: کمترین تعداد سکه برای amount (tabulation)
static int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);     // بی‌نهایت مجازی
    dp[0] = 0;
    for (int i = 1; i <= amount; i++)
        for (int coin : coins)
            if (coin <= i) dp[i] = Math.min(dp[i], dp[i - coin] + 1);
    return dp[amount] > amount ? -1 : dp[amount];
}
```

**نکات کلیدی:**

- تشخیص DP: overlapping subproblems + optimal substructure.
- memoization آسان‌تر برای نوشتن؛ tabulation بهینه‌تر در فضا/سرعت.
- تعریف state سخت‌ترین و مهم‌ترین بخش است.

---

### Greedy & Divide and Conquer

**توضیح:**

**Greedy** در هر مرحله انتخاب محلی بهینه می‌کند به امید بهینه‌ی سراسری. فقط وقتی درست است که **greedy choice property** و **optimal substructure** برقرار باشد (مثل Activity Selection، Huffman). برخلاف DP که همه‌ی گزینه‌ها را بررسی می‌کند. **Divide and Conquer** مسئله را به زیرمسائل تقسیم، حل، و ترکیب می‌کند (Merge Sort، Quick Sort). تحلیل با Master Theorem.

**نکات کلیدی:**

- greedy همیشه بهینه نیست؛ باید اثبات شود (مثلاً coin change با سکه‌های دلخواه greedy جواب نمی‌دهد).
- DP در صورت شک به جای greedy امن‌تر است.

---

### Complexity Analysis

**توضیح:**

- **Big O** (کران بالا)، **Big Ω** (کران پایین)، **Big Θ** (کران دقیق).
- **Amortized analysis:** میانگین در دنباله‌ای از عملیات؛ مثال کلاسیک `ArrayList.add` که گاهی O(n) (resize) اما amortized O(1).
- **Space complexity:** حافظه‌ی اضافه.
- **Recurrence relations** برای الگوریتم‌های بازگشتی.

**نکات کلیدی:**

- amortized با worst-case تک‌عملیات فرق دارد.
- در مصاحبه هم time و هم space را تحلیل کنید.

---

## 🎯 سوالات مصاحبه

### سوال ۱: stability در مرتب‌سازی چیست و چرا مهم است؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

یک الگوریتم مرتب‌سازی **پایدار** است اگر ترتیب نسبی عناصر با کلید مساوی را حفظ کند. اهمیت: در مرتب‌سازی چندمرحله‌ای. مثلاً اگر بخواهید لیست را اول بر اساس نام و سپس بر اساس سن مرتب کنید، با الگوریتم پایدار می‌توانید دو بار مرتب کنید (اول name، بعد age) و در گروه‌های هم‌سن، ترتیب name حفظ می‌شود. با الگوریتم ناپایدار این تضمین از بین می‌رود. Java برای object از TimSort (پایدار) و برای primitive از quicksort (ناپایدار، چون primitiveها قابل‌تمایز نیستند پس stability بی‌معناست) استفاده می‌کند.

**نکته مصاحبه:**

تمایز Senior: دانستن چرا Java برای primitive ناپایدار و برای object پایدار است. Follow-up: «چرا quicksort برای object استفاده نمی‌شود؟» (ناپایدار + worst case).

---

### سوال ۲: memoization در برابر tabulation؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

memoization (top-down) recursion طبیعی مسئله را می‌نویسد و نتایج را cache می‌کند؛ آسان‌تر برای فکر کردن، فقط زیرمسائل لازم را محاسبه می‌کند، اما سربار recursion و خطر StackOverflow برای عمق زیاد. tabulation (bottom-up) جدول را به ترتیب پر می‌کند؛ بدون recursion، معمولاً سریع‌تر و قابل بهینه‌سازی فضا (rolling array)، اما باید ترتیب وابستگی‌ها را دستی بفهمید و گاهی زیرمسائل غیرلازم را هم محاسبه می‌کند. انتخاب: memoization برای شروع و وضوح، tabulation برای بهینه‌سازی نهایی.

**نکته مصاحبه:**

Follow-up: «چطور فضای DP را از O(n²) به O(n) کاهش می‌دهی؟» (rolling array — فقط ردیف قبلی را نگه دار).

---

### سوال ۳: amortized complexity یعنی چه؟ مثال ArrayList.add؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

amortized یعنی میانگین هزینه‌ی هر عملیات در یک **دنباله** از عملیات، حتی اگر تک‌عملیات گاهی گران باشد. `ArrayList.add` معمولاً O(1) است (نوشتن در index بعدی)، اما گاهی وقتی آرایه پر است، resize (کپی همه به آرایه‌ی بزرگ‌تر) O(n) می‌شود. چون resize دوبرابر می‌کند، این هزینه‌ی گران به‌ندرت رخ می‌دهد و وقتی روی کل n عملیات پخش شود، هزینه‌ی amortized هر add برابر O(1) است. این با worst-case یک عملیات (O(n)) فرق دارد. تحلیل با accounting method یا aggregate method.

**نکته مصاحبه:**

Senior تفاوت amortized با worst-case تک‌عملیات را روشن می‌کند.

---

### سوال ۴: کِی greedy و کِی DP؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

greedy وقتی کار می‌کند که مسئله **greedy choice property** داشته باشد: انتخاب محلی بهینه به جواب سراسری بهینه منجر شود (مثل Activity Selection، Huffman، Dijkstra). مزیت: سریع‌تر و ساده‌تر از DP. اما خطرناک است چون همیشه درست نیست و باید اثبات شود — مثلاً Coin Change با سکه‌های دلخواه (مثل ۱، ۳، ۴ برای ۶) با greedy جواب بهینه نمی‌دهد. DP همه‌ی گزینه‌ها را بررسی می‌کند پس همیشه بهینه است اما کندتر. قاعده‌ی عملی: اگر مطمئن به اثبات greedy نیستید، DP امن‌تر است.

**نکته مصاحبه:**

Senior مثال نقض greedy (coin change) را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: overflow در binary search mid

```java
// ❌ ممکن است overflow شود
int mid = (low + high) / 2;
```

```java
// ✅
int mid = low + (high - low) / 2;
```

**توضیح:** برای آرایه‌ی بزرگ، `low + high` می‌تواند از Integer.MAX_VALUE بگذرد.

---

### اشتباه ۲: فرض greedy برای coin change

```java
// ❌ greedy: همیشه بزرگ‌ترین سکه — برای سکه‌های دلخواه غلط
```

```java
// ✅ DP coin change (بالا)
```

**توضیح:** greedy فقط برای سیستم سکه‌ی canonical جواب می‌دهد.

---

### اشتباه ۳: DP recursive بدون memoization

```java
// ❌ O(2^n) — فاجعه
int fib(int n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
```

```java
// ✅ با memo یا tabulation O(n)
```

**توضیح:** بدون cache، زیرمسائل بارها محاسبه می‌شوند.

---

## 🔗 ارتباط با سایر مفاهیم

- complexity با **performance** و **System Design** (مقیاس‌پذیری).
- sorting/TimSort با **Java Collections.sort** و **Comparator (1.1)**.
- graph algorithms با **Data Structures (5.1)** و **System Design**.
- DP با مسائل **LeetCode** برای آمادگی مصاحبه.
