# Data Structures — Array، LinkedList، Stack/Queue، HashTable، Tree، Graph

> ساختار داده پایه‌ی هر سوال الگوریتمی و طراحی است. درک internals (مثل HashMap) تمایز Senior است.

---

## 📖 مفاهیم

### Array & String

**توضیح:**

آرایه‌ی static اندازه‌ی ثابت دارد؛ dynamic array (مثل `ArrayList`) با پر شدن resize می‌شود (در Java ضریب ۱.۵). دسترسی با index برابر O(1) به‌خاطر contiguous memory و cache locality عالی. الگوهای کلیدی روی آرایه/رشته: **two pointers** (دو اشاره‌گر برای مسائل مرتب‌شده/جفت)، **sliding window** (پنجره‌ی متغیر برای زیرآرایه/زیررشته)، **prefix sum** (مجموع پیشوندی برای range query سریع).

برای رشته الگوریتم‌های جستجوی الگو: KMP و Rabin-Karp (با hashing).

**چرا مهم است:**

اکثر سوالات coding روی این الگوها هستند. cache locality آرایه باعث می‌شود در عمل سریع‌تر از ساختارهای pointer-based باشد.

**مثال کد:**

```java
// sliding window: بزرگ‌ترین مجموع زیرآرایه‌ی k عنصری
static int maxSum(int[] arr, int k) {
    int windowSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    int max = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k]; // اضافه‌ی جدید، حذف قدیم
        max = Math.max(max, windowSum);
    }
    return max;
}
```

**نکات کلیدی:**

- sliding window O(n) به‌جای O(n*k) brute force.
- prefix sum برای range sum مکرر؛ پیش‌محاسبه O(n)، query O(1).

---

### Linked List

**توضیح:**

لیست پیوندی: هر node داده + pointer به بعدی (singly) یا قبلی و بعدی (doubly) دارد. درج/حذف O(1) اگر node را داشته باشید، اما دسترسی تصادفی O(n). الگوی مهم **fast/slow pointers** (Floyd's cycle detection): برای یافتن وسط، تشخیص حلقه، و یافتن نقطه‌ی شروع حلقه.

**مثال کد:**

```java
// تشخیص حلقه با Floyd
static boolean hasCycle(ListNode head) {
    ListNode slow = head, fast = head;
    while (fast != null && fast.next != null) {
        slow = slow.next;          // یک قدم
        fast = fast.next.next;     // دو قدم
        if (slow == fast) return true; // برخورد → حلقه
    }
    return false;
}
```

**نکات کلیدی:**

- fast/slow برای وسط لیست، تشخیص حلقه، یافتن node k-ام از آخر.
- در عمل ArrayList معمولاً از LinkedList سریع‌تر است (cache locality).

---

### Stack & Queue

**توضیح:**

Stack (LIFO) و Queue (FIFO). در Java `ArrayDeque` بهترین انتخاب برای هر دو است (سریع‌تر از `Stack` legacy و `LinkedList`). الگوی **monotonic stack** برای مسائلی مثل Next Greater Element. Queue برای BFS.

**مثال کد:**

```java
// Next Greater Element با monotonic stack
static int[] nextGreater(int[] nums) {
    int[] res = new int[nums.length];
    Arrays.fill(res, -1);
    Deque<Integer> stack = new ArrayDeque<>(); // indexها
    for (int i = 0; i < nums.length; i++) {
        while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
            res[stack.pop()] = nums[i];
        }
        stack.push(i);
    }
    return res;
}
```

**نکات کلیدی:**

- `ArrayDeque` به‌جای `Stack`/`LinkedList`.
- monotonic stack الگوی پرتکرار برای مسائل «بعدی بزرگ‌تر/کوچک‌تر».

---

### Hash Table — HashMap internals

**توضیح:**

`HashMap` با hashing کلید را به یک bucket map می‌کند: دسترسی متوسط O(1). **Collision** (دو کلید در یک bucket) با chaining (لیست پیوندی) مدیریت می‌شود؛ از Java 8، اگر یک bucket بیش از ۸ عنصر شود به **درخت قرمز-سیاه** تبدیل می‌شود (O(log n) به‌جای O(n) در بدترین حالت). **load factor** (پیش‌فرض ۰.۷۵): وقتی تعداد عناصر از `capacity * loadFactor` گذشت، resize (دوبرابر) و **rehash** رخ می‌دهد.

کیفیت `hashCode` حیاتی است: توزیع بد → همه در یک bucket → O(n). به همین دلیل کلید HashMap باید immutable و `equals/hashCode` درست داشته باشد.

**چرا مهم است:**

HashMap پرکاربردترین ساختار است و internals آن سوال کلاسیک مصاحبه. درک resize و treeification برای performance لازم است.

**مثال کد:**

```java
// کلید HashMap باید immutable و equals/hashCode درست داشته باشد
record CacheKey(String tenant, Long userId) {} // record خودکار درست می‌کند

Map<CacheKey, User> cache = new HashMap<>();
cache.put(new CacheKey("t1", 5L), user);
```

**نکات کلیدی:**

- از Java 8 bucket بزرگ به درخت قرمز-سیاه تبدیل می‌شود (O(log n)).
- load factor ۰.۷۵ تعادل فضا/سرعت.
- کلید mutable در HashMap = باگ (شیء گم می‌شود).

---

### Tree

**توضیح:**

- **Binary Tree** و پیمایش‌ها: inorder، preorder، postorder (DFS)، level-order (BFS).
- **BST:** برای جستجو/درج/حذف O(h)؛ h در بدترین حالت (نامتعادل) O(n).
- **Balanced BST:** AVL، Red-Black (پایه‌ی `TreeMap`/`TreeSet` در Java) — تضمین O(log n).
- **Heap:** MinHeap/MaxHeap، پایه‌ی `PriorityQueue` — درج/حذف O(log n)، دسترسی به min/max O(1).
- **Trie:** برای prefix search (autocomplete).
- **Segment Tree / Fenwick Tree:** برای range query.

**مثال کد:**

```java
// inorder traversal (BST → مرتب)
static void inorder(TreeNode node, List<Integer> out) {
    if (node == null) return;
    inorder(node.left, out);
    out.add(node.val);     // وسط
    inorder(node.right, out);
}
```

**نکات کلیدی:**

- inorder روی BST خروجی مرتب می‌دهد.
- `TreeMap` (Red-Black) برای کلید مرتب و range query؛ `PriorityQueue` برای top-k.

---

### Graph

**توضیح:**

نمایش: Adjacency List (کم‌حجم برای گراف sparse) یا Matrix (برای dense). الگوریتم‌ها:

- **BFS:** کوتاه‌ترین مسیر در گراف بدون وزن.
- **DFS:** topological sort، connected components، cycle detection.
- **Dijkstra:** کوتاه‌ترین مسیر وزن‌دار (بدون وزن منفی).
- **Bellman-Ford:** با وزن منفی.
- **Floyd-Warshall:** کوتاه‌ترین مسیر همه‌جفت.
- **Prim/Kruskal:** Minimum Spanning Tree.
- **Union-Find:** برای connected component و cycle در گراف بدون جهت.

**مثال کد:**

```java
// BFS کوتاه‌ترین مسیر بدون وزن
static int shortestPath(Map<Integer, List<Integer>> graph, int start, int target) {
    Queue<Integer> queue = new ArrayDeque<>();
    Map<Integer, Integer> dist = new HashMap<>();
    queue.add(start); dist.put(start, 0);
    while (!queue.isEmpty()) {
        int node = queue.poll();
        if (node == target) return dist.get(node);
        for (int next : graph.getOrDefault(node, List.of())) {
            if (!dist.containsKey(next)) {
                dist.put(next, dist.get(node) + 1);
                queue.add(next);
            }
        }
    }
    return -1;
}
```

**نکات کلیدی:**

- BFS برای کوتاه‌ترین مسیر بدون وزن؛ Dijkstra برای وزن‌دار.
- Union-Find برای cycle detection و MST (Kruskal).

---

## 🎯 سوالات مصاحبه

### سوال ۱: HashMap چطور کار می‌کند و در Java 8 چه تغییری کرد؟

**سطح:** Senior
**تکرار:** خیلی زیاد

**جواب کامل:**

HashMap کلید را با `hashCode()` به یک bucket map می‌کند (با bitwise روی hash برای توزیع). دسترسی متوسط O(1). هنگام collision، چند کلید در یک bucket قرار می‌گیرند. تا Java 7 این‌ها در یک لیست پیوندی نگه داشته می‌شدند، پس در بدترین حالت (همه در یک bucket با hashCode بد) جستجو O(n) می‌شد — که یک بردار حمله‌ی DoS هم بود. از **Java 8**، وقتی یک bucket از آستانه (۸ عنصر) بیشتر شود و capacity کافی باشد، لیست به **درخت قرمز-سیاه** تبدیل می‌شود و بدترین حالت به O(log n) بهبود می‌یابد. همچنین load factor ۰.۷۵ و resize با دوبرابر کردن capacity و rehash.

**کد توضیحی:**

```java
// hashCode بد → همه در یک bucket → کند
class BadKey { public int hashCode() { return 1; } } // ❌
```

**نکته مصاحبه:**

تمایز Senior: treeification در Java 8، load factor، و امنیت (DoS). Follow-up: «چرا کلید باید immutable باشد؟»

---

### سوال ۲: ArrayList در برابر LinkedList از نظر complexity؟

**سطح:** Mid / Senior
**تکرار:** زیاد

**جواب کامل:**

ArrayList: دسترسی index O(1)، add در انتها amortized O(1)، درج/حذف وسط O(n) (shift). LinkedList: دسترسی index O(n)، درج/حذف در سر O(1)، اما برای رسیدن به وسط O(n). در نظریه LinkedList برای درج زیاد بهتر است، اما در عمل به‌خاطر cache locality و سربار pointer، ArrayList تقریباً همیشه برنده است. برای صف/پشته `ArrayDeque` بهتر از هر دو است.

**نکته مصاحبه:**

Senior می‌داند نظریه و عمل فرق دارند (cache locality). 

---

### سوال ۳: BFS در برابر DFS — کِی کدام؟

**سطح:** Senior
**تکرار:** زیاد

**جواب کامل:**

BFS سطح‌به‌سطح پیمایش می‌کند و برای **کوتاه‌ترین مسیر در گراف بدون وزن** و یافتن نزدیک‌ترین گره ایده‌آل است؛ از queue استفاده می‌کند و حافظه‌اش متناسب با عرض گراف. DFS تا عمق می‌رود و برای **topological sort، cycle detection، connected components، و مسائل backtracking** مناسب است؛ با stack یا recursion، حافظه متناسب با عمق. برای گراف بسیار عمیق، DFS recursive ممکن است StackOverflow بدهد (از iterative استفاده کنید). انتخاب بر اساس مسئله: کوتاه‌ترین مسیر بدون وزن → BFS؛ ساختار/ترتیب/چرخه → DFS.

**نکته مصاحبه:**

Follow-up: «کوتاه‌ترین مسیر در گراف وزن‌دار؟» (Dijkstra نه BFS).

---

### سوال ۴: PriorityQueue چطور کار می‌کند و کجا استفاده می‌شود؟

**سطح:** Senior
**تکرار:** متوسط

**جواب کامل:**

`PriorityQueue` در Java یک binary heap است: درج و حذف min/max برابر O(log n)، دسترسی به min/max برابر O(1). برای مسائل **top-k** (k بزرگ‌ترین/کوچک‌ترین)، merge کردن k لیست مرتب، Dijkstra، و scheduling بر اساس اولویت. برای top-k بزرگ‌ترین، یک min-heap با اندازه‌ی k نگه می‌دارید؛ هر عنصر را اضافه و اگر اندازه از k گذشت، کوچک‌ترین را حذف می‌کنید — O(n log k).

**کد توضیحی:**

```java
// k بزرگ‌ترین عنصر با min-heap اندازه k
PriorityQueue<Integer> heap = new PriorityQueue<>(); // min-heap
for (int n : nums) {
    heap.offer(n);
    if (heap.size() > k) heap.poll(); // کوچک‌ترین را دور بریز
}
return heap.peek(); // k-امین بزرگ‌ترین
```

**نکته مصاحبه:**

Senior الگوی min-heap اندازه k برای top-k را می‌داند.

---

## ⚠️ اشتباهات رایج

### اشتباه ۱: کلید mutable در HashMap

```java
// ❌ تغییر فیلد بعد از put → شیء گم می‌شود
class Key { int id; public int hashCode(){return id;} }
Key k = new Key(); map.put(k, v); k.id = 99; // map.get(k) → null
```

```java
// ✅ کلید immutable (record)
record Key(int id) {}
```

**توضیح:** تغییر کلید hashCode را عوض می‌کند و شیء در bucket اشتباه می‌ماند.

---

### اشتباه ۲: استفاده از `Stack` legacy

```java
// ❌ کند، synchronized بی‌مورد
Stack<Integer> stack = new Stack<>();
```

```java
// ✅
Deque<Integer> stack = new ArrayDeque<>();
```

**توضیح:** `Stack` کلاس قدیمی و synchronized است؛ `ArrayDeque` بهتر است.

---

### اشتباه ۳: DFS recursive روی گراف عمیق

```java
// ❌ StackOverflow روی گراف خیلی عمیق
void dfs(int node) { ...; dfs(next); }
```

```java
// ✅ iterative با stack صریح
Deque<Integer> stack = new ArrayDeque<>();
```

**توضیح:** عمق زیاد recursion → StackOverflowError.

---

## 🔗 ارتباط با سایر مفاهیم

- HashMap internals با **Collections (1.1)** و **ConcurrentHashMap (concurrency)**.
- Tree (Red-Black) با **TreeMap** و **DB index (B-Tree)**.
- Graph با **System Design** (social network، routing).
- complexity با **Algorithms (5.2)** و **performance**.
