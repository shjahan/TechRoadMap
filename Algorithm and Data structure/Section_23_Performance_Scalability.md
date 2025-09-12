# Section 23 – Performance & Scalability

## 23.1 Complexity Analysis & Big O Notation

Complexity analysis is the foundation of understanding algorithm performance and scalability.

### Time Complexity Analysis

```java
public class ComplexityAnalysis {
    // O(1) - Constant Time
    public int getFirstElement(int[] arr) {
        return arr[0]; // Always takes the same time
    }
    
    // O(log n) - Logarithmic Time
    public int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }
    
    // O(n) - Linear Time
    public int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }
    
    // O(n log n) - Linearithmic Time
    public void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        mergeSort(left);
        mergeSort(right);
        merge(arr, left, right);
    }
    
    // O(n²) - Quadratic Time
    public void bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                }
            }
        }
    }
    
    // O(2^n) - Exponential Time
    public int fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    
    // O(n!) - Factorial Time
    public void permute(int[] arr, int start) {
        if (start == arr.length - 1) {
            System.out.println(Arrays.toString(arr));
            return;
        }
        for (int i = start; i < arr.length; i++) {
            swap(arr, start, i);
            permute(arr, start + 1);
            swap(arr, start, i); // backtrack
        }
    }
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    private void merge(int[] arr, int[] left, int[] right) {
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                arr[k++] = left[i++];
            } else {
                arr[k++] = right[j++];
            }
        }
        while (i < left.length) arr[k++] = left[i++];
        while (j < right.length) arr[k++] = right[j++];
    }
}
```

### Space Complexity Analysis

```java
public class SpaceComplexityAnalysis {
    // O(1) - Constant Space
    public int sum(int[] arr) {
        int total = 0; // Only one variable
        for (int num : arr) {
            total += num;
        }
        return total;
    }
    
    // O(n) - Linear Space
    public int[] reverse(int[] arr) {
        int[] result = new int[arr.length]; // New array of same size
        for (int i = 0; i < arr.length; i++) {
            result[i] = arr[arr.length - 1 - i];
        }
        return result;
    }
    
    // O(log n) - Logarithmic Space (recursion stack)
    public int binarySearchRecursive(int[] arr, int target, int left, int right) {
        if (left > right) return -1;
        int mid = left + (right - left) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) return binarySearchRecursive(arr, target, mid + 1, right);
        return binarySearchRecursive(arr, target, left, mid - 1);
    }
    
    // O(n²) - Quadratic Space
    public int[][] matrixMultiplication(int[][] a, int[][] b) {
        int n = a.length;
        int[][] result = new int[n][n]; // n² space
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return result;
    }
}
```

## 23.2 Space-Time Tradeoffs

Understanding the relationship between time and space complexity is crucial for algorithm optimization.

### Memoization vs Tabulation

```java
public class SpaceTimeTradeoffs {
    // Time: O(2^n), Space: O(n) - Naive approach
    public int fibonacciNaive(int n) {
        if (n <= 1) return n;
        return fibonacciNaive(n - 1) + fibonacciNaive(n - 2);
    }
    
    // Time: O(n), Space: O(n) - Memoization (top-down)
    public int fibonacciMemo(int n) {
        int[] memo = new int[n + 1];
        Arrays.fill(memo, -1);
        return fibonacciMemoHelper(n, memo);
    }
    
    private int fibonacciMemoHelper(int n, int[] memo) {
        if (n <= 1) return n;
        if (memo[n] != -1) return memo[n];
        memo[n] = fibonacciMemoHelper(n - 1, memo) + fibonacciMemoHelper(n - 2, memo);
        return memo[n];
    }
    
    // Time: O(n), Space: O(n) - Tabulation (bottom-up)
    public int fibonacciTab(int n) {
        if (n <= 1) return n;
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n];
    }
    
    // Time: O(n), Space: O(1) - Space-optimized
    public int fibonacciOptimized(int n) {
        if (n <= 1) return n;
        int prev2 = 0, prev1 = 1;
        for (int i = 2; i <= n; i++) {
            int current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }
}
```

### Hash Table vs Array Tradeoffs

```java
public class HashTableVsArray {
    // Array: O(1) access, O(n) search, O(n) space
    public class ArrayBasedSet {
        private int[] elements;
        private int size;
        
        public ArrayBasedSet(int capacity) {
            this.elements = new int[capacity];
            this.size = 0;
        }
        
        public void add(int element) {
            if (!contains(element)) {
                elements[size++] = element;
            }
        }
        
        public boolean contains(int element) {
            for (int i = 0; i < size; i++) {
                if (elements[i] == element) return true;
            }
            return false;
        }
        
        public int get(int index) {
            return elements[index];
        }
    }
    
    // Hash Table: O(1) access, O(1) search, O(n) space
    public class HashSet {
        private boolean[] present;
        private int[] elements;
        private int size;
        
        public HashSet(int capacity) {
            this.present = new boolean[capacity];
            this.elements = new int[capacity];
            this.size = 0;
        }
        
        public void add(int element) {
            int index = hash(element);
            if (!present[index]) {
                elements[index] = element;
                present[index] = true;
                size++;
            }
        }
        
        public boolean contains(int element) {
            int index = hash(element);
            return present[index] && elements[index] == element;
        }
        
        private int hash(int element) {
            return element % present.length;
        }
    }
}
```

## 23.3 Amortized Analysis

Amortized analysis provides a more accurate picture of algorithm performance over a sequence of operations.

### Dynamic Array Amortized Analysis

```java
public class DynamicArray {
    private int[] array;
    private int size;
    private int capacity;
    
    public DynamicArray() {
        this.capacity = 1;
        this.array = new int[capacity];
        this.size = 0;
    }
    
    public void add(int element) {
        if (size == capacity) {
            resize();
        }
        array[size++] = element;
    }
    
    private void resize() {
        capacity *= 2;
        int[] newArray = new int[capacity];
        System.arraycopy(array, 0, newArray, 0, size);
        array = newArray;
    }
    
    public int get(int index) {
        if (index >= size) throw new IndexOutOfBoundsException();
        return array[index];
    }
    
    public int size() {
        return size;
    }
    
    // Amortized O(1) for add operation
    // Worst case O(n) when resize happens
    // But resize happens infrequently (every 2^n elements)
    // Total cost for n operations: O(n)
    // Amortized cost per operation: O(n)/n = O(1)
}
```

### Union-Find Amortized Analysis

```java
public class UnionFind {
    private int[] parent;
    private int[] rank;
    
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            rank[i] = 0;
        }
    }
    
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path compression
        }
        return parent[x];
    }
    
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        
        if (rootX == rootY) return;
        
        // Union by rank
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
    }
    
    // Amortized O(α(n)) where α is the inverse Ackermann function
    // For practical purposes, α(n) < 5 for any reasonable n
    // So effectively O(1) amortized
}
```

## 23.4 Competitive Analysis

Competitive analysis compares online algorithms against optimal offline algorithms.

### Online vs Offline Algorithms

```java
public class CompetitiveAnalysis {
    // Online Algorithm - makes decisions without seeing future
    public class OnlinePaging {
        private int cacheSize;
        private List<Integer> cache;
        private int pageFaults;
        
        public OnlinePaging(int cacheSize) {
            this.cacheSize = cacheSize;
            this.cache = new ArrayList<>();
            this.pageFaults = 0;
        }
        
        public void accessPage(int page) {
            if (!cache.contains(page)) {
                pageFaults++;
                if (cache.size() >= cacheSize) {
                    // Remove least recently used page
                    cache.remove(0);
                }
                cache.add(page);
            } else {
                // Move to end (most recently used)
                cache.remove(Integer.valueOf(page));
                cache.add(page);
            }
        }
        
        public int getPageFaults() {
            return pageFaults;
        }
    }
    
    // Offline Algorithm - sees entire sequence in advance
    public class OfflinePaging {
        private int cacheSize;
        private List<Integer> cache;
        private int pageFaults;
        
        public OfflinePaging(int cacheSize) {
            this.cacheSize = cacheSize;
            this.cache = new ArrayList<>();
            this.pageFaults = 0;
        }
        
        public void processSequence(List<Integer> sequence) {
            for (int i = 0; i < sequence.size(); i++) {
                int page = sequence.get(i);
                if (!cache.contains(page)) {
                    pageFaults++;
                    if (cache.size() >= cacheSize) {
                        // Remove page that will be used farthest in future
                        int farthestIndex = -1;
                        int farthestPage = -1;
                        for (int cachedPage : cache) {
                            int nextUse = findNextUse(sequence, cachedPage, i + 1);
                            if (nextUse > farthestIndex) {
                                farthestIndex = nextUse;
                                farthestPage = cachedPage;
                            }
                        }
                        cache.remove(Integer.valueOf(farthestPage));
                    }
                    cache.add(page);
                }
            }
        }
        
        private int findNextUse(List<Integer> sequence, int page, int startIndex) {
            for (int i = startIndex; i < sequence.size(); i++) {
                if (sequence.get(i) == page) return i;
            }
            return Integer.MAX_VALUE;
        }
        
        public int getPageFaults() {
            return pageFaults;
        }
    }
}
```

## 23.5 Worst-Case vs Average-Case Analysis

Understanding different performance scenarios helps in algorithm selection.

### QuickSort Analysis

```java
public class QuickSortAnalysis {
    // Worst case: O(n²) - when pivot is always smallest or largest
    public void quickSortWorstCase(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }
    
    // Average case: O(n log n) - with random pivot selection
    public void quickSortAverageCase(int[] arr) {
        randomizedQuickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private void randomizedQuickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Random pivot selection
            int randomIndex = low + (int) (Math.random() * (high - low + 1));
            swap(arr, randomIndex, high);
            
            int pivotIndex = partition(arr, low, high);
            randomizedQuickSort(arr, low, pivotIndex - 1);
            randomizedQuickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        swap(arr, i + 1, high);
        return i + 1;
    }
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

### Hash Table Analysis

```java
public class HashTableAnalysis {
    private static final int INITIAL_CAPACITY = 16;
    private static final double LOAD_FACTOR = 0.75;
    
    private Entry[] table;
    private int size;
    private int capacity;
    
    public HashTableAnalysis() {
        this.capacity = INITIAL_CAPACITY;
        this.table = new Entry[capacity];
        this.size = 0;
    }
    
    public void put(String key, Integer value) {
        if (size >= capacity * LOAD_FACTOR) {
            resize();
        }
        
        int index = hash(key);
        Entry entry = new Entry(key, value);
        
        if (table[index] == null) {
            table[index] = entry;
        } else {
            // Handle collision with chaining
            Entry current = table[index];
            while (current.next != null) {
                if (current.key.equals(key)) {
                    current.value = value;
                    return;
                }
                current = current.next;
            }
            if (current.key.equals(key)) {
                current.value = value;
                return;
            }
            current.next = entry;
        }
        size++;
    }
    
    public Integer get(String key) {
        int index = hash(key);
        Entry current = table[index];
        
        while (current != null) {
            if (current.key.equals(key)) {
                return current.value;
            }
            current = current.next;
        }
        return null;
    }
    
    private int hash(String key) {
        return Math.abs(key.hashCode()) % capacity;
    }
    
    private void resize() {
        Entry[] oldTable = table;
        capacity *= 2;
        table = new Entry[capacity];
        size = 0;
        
        for (Entry entry : oldTable) {
            while (entry != null) {
                put(entry.key, entry.value);
                entry = entry.next;
            }
        }
    }
    
    private static class Entry {
        String key;
        Integer value;
        Entry next;
        
        Entry(String key, Integer value) {
            this.key = key;
            this.value = value;
        }
    }
    
    // Analysis:
    // Best case: O(1) - no collisions
    // Average case: O(1) - with good hash function and load factor
    // Worst case: O(n) - all keys hash to same index
}
```

## 23.6 Profiling & Performance Measurement

### Algorithm Profiler

```java
public class AlgorithmProfiler {
    public static class ProfilingResult {
        private String algorithmName;
        private long executionTime;
        private long memoryUsed;
        private int operationsCount;
        
        public ProfilingResult(String algorithmName, long executionTime, 
                              long memoryUsed, int operationsCount) {
            this.algorithmName = algorithmName;
            this.executionTime = executionTime;
            this.memoryUsed = memoryUsed;
            this.operationsCount = operationsCount;
        }
        
        // Getters
        public String getAlgorithmName() { return algorithmName; }
        public long getExecutionTime() { return executionTime; }
        public long getMemoryUsed() { return memoryUsed; }
        public int getOperationsCount() { return operationsCount; }
    }
    
    public static ProfilingResult profile(Runnable algorithm, String name) {
        // Measure memory before
        long memoryBefore = getUsedMemory();
        
        // Measure time
        long startTime = System.nanoTime();
        algorithm.run();
        long endTime = System.nanoTime();
        
        // Measure memory after
        long memoryAfter = getUsedMemory();
        
        return new ProfilingResult(name, endTime - startTime, 
                                  memoryAfter - memoryBefore, 0);
    }
    
    public static void benchmark(String name, Runnable algorithm, int iterations) {
        System.out.println("Benchmarking: " + name);
        System.out.println("Iterations: " + iterations);
        
        long totalTime = 0;
        long minTime = Long.MAX_VALUE;
        long maxTime = Long.MIN_VALUE;
        
        for (int i = 0; i < iterations; i++) {
            long startTime = System.nanoTime();
            algorithm.run();
            long endTime = System.nanoTime();
            
            long executionTime = endTime - startTime;
            totalTime += executionTime;
            minTime = Math.min(minTime, executionTime);
            maxTime = Math.max(maxTime, executionTime);
        }
        
        double averageTime = (double) totalTime / iterations;
        
        System.out.println("Average time: " + averageTime + " ns");
        System.out.println("Min time: " + minTime + " ns");
        System.out.println("Max time: " + maxTime + " ns");
        System.out.println("Total time: " + totalTime + " ns");
    }
    
    private static long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
}
```

### Performance Testing Framework

```java
public class PerformanceTestingFramework {
    public static void runPerformanceTests() {
        // Test different array sizes
        int[] sizes = {1000, 10000, 100000, 1000000};
        
        for (int size : sizes) {
            System.out.println("\nTesting with array size: " + size);
            
            // Generate test data
            int[] testData = generateRandomArray(size);
            
            // Test sorting algorithms
            testSortingAlgorithm("Bubble Sort", testData.clone(), 
                               arr -> bubbleSort(arr));
            testSortingAlgorithm("Quick Sort", testData.clone(), 
                               arr -> quickSort(arr));
            testSortingAlgorithm("Merge Sort", testData.clone(), 
                               arr -> mergeSort(arr));
        }
    }
    
    private static void testSortingAlgorithm(String name, int[] data, 
                                           Consumer<int[]> algorithm) {
        long startTime = System.nanoTime();
        algorithm.accept(data);
        long endTime = System.nanoTime();
        
        long executionTime = endTime - startTime;
        System.out.println(name + ": " + executionTime + " ns");
    }
    
    private static int[] generateRandomArray(int size) {
        int[] arr = new int[size];
        Random random = new Random();
        for (int i = 0; i < size; i++) {
            arr[i] = random.nextInt(1000);
        }
        return arr;
    }
    
    private static void bubbleSort(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    swap(arr, j, j + 1);
                }
            }
        }
    }
    
    private static void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }
    
    private static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private static int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] <= pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        
        swap(arr, i + 1, high);
        return i + 1;
    }
    
    private static void mergeSort(int[] arr) {
        if (arr.length <= 1) return;
        int mid = arr.length / 2;
        int[] left = Arrays.copyOfRange(arr, 0, mid);
        int[] right = Arrays.copyOfRange(arr, mid, arr.length);
        mergeSort(left);
        mergeSort(right);
        merge(arr, left, right);
    }
    
    private static void merge(int[] arr, int[] left, int[] right) {
        int i = 0, j = 0, k = 0;
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                arr[k++] = left[i++];
            } else {
                arr[k++] = right[j++];
            }
        }
        while (i < left.length) arr[k++] = left[i++];
        while (j < right.length) arr[k++] = right[j++];
    }
    
    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
```

## 23.7 Optimization Techniques

### Algorithm Optimization

```java
public class AlgorithmOptimization {
    // Optimized Fibonacci with matrix exponentiation
    public long fibonacciOptimized(int n) {
        if (n <= 1) return n;
        
        long[][] matrix = {{1, 1}, {1, 0}};
        long[][] result = matrixPower(matrix, n - 1);
        return result[0][0];
    }
    
    private long[][] matrixPower(long[][] matrix, int n) {
        if (n == 1) return matrix;
        
        if (n % 2 == 0) {
            long[][] half = matrixPower(matrix, n / 2);
            return matrixMultiply(half, half);
        } else {
            long[][] half = matrixPower(matrix, (n - 1) / 2);
            return matrixMultiply(matrixMultiply(half, half), matrix);
        }
    }
    
    private long[][] matrixMultiply(long[][] a, long[][] b) {
        long[][] result = new long[2][2];
        result[0][0] = a[0][0] * b[0][0] + a[0][1] * b[1][0];
        result[0][1] = a[0][0] * b[0][1] + a[0][1] * b[1][1];
        result[1][0] = a[1][0] * b[0][0] + a[1][1] * b[1][0];
        result[1][1] = a[1][0] * b[0][1] + a[1][1] * b[1][1];
        return result;
    }
    
    // Optimized Prime Number Generation
    public List<Integer> generatePrimes(int limit) {
        boolean[] isPrime = new boolean[limit + 1];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        
        for (int p = 2; p * p <= limit; p++) {
            if (isPrime[p]) {
                for (int i = p * p; i <= limit; i += p) {
                    isPrime[i] = false;
                }
            }
        }
        
        List<Integer> primes = new ArrayList<>();
        for (int i = 2; i <= limit; i++) {
            if (isPrime[i]) {
                primes.add(i);
            }
        }
        return primes;
    }
    
    // Optimized String Matching with KMP
    public List<Integer> kmpSearch(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        int[] lps = computeLPS(pattern);
        int i = 0, j = 0;
        
        while (i < text.length()) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }
            if (j == pattern.length()) {
                matches.add(i - j);
                j = lps[j - 1];
            } else if (i < text.length() && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        return matches;
    }
    
    private int[] computeLPS(String pattern) {
        int[] lps = new int[pattern.length()];
        int len = 0;
        int i = 1;
        
        while (i < pattern.length()) {
            if (pattern.charAt(i) == pattern.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }
}
```

### Memory Optimization

```java
public class MemoryOptimization {
    // Bit manipulation for space efficiency
    public class BitSet {
        private long[] bits;
        private int size;
        
        public BitSet(int size) {
            this.size = size;
            this.bits = new long[(size + 63) / 64];
        }
        
        public void set(int index) {
            if (index >= size) throw new IndexOutOfBoundsException();
            bits[index / 64] |= 1L << (index % 64);
        }
        
        public boolean get(int index) {
            if (index >= size) throw new IndexOutOfBoundsException();
            return (bits[index / 64] & (1L << (index % 64))) != 0;
        }
        
        public void clear(int index) {
            if (index >= size) throw new IndexOutOfBoundsException();
            bits[index / 64] &= ~(1L << (index % 64));
        }
    }
    
    // Object pooling for memory efficiency
    public class ObjectPool<T> {
        private Queue<T> pool;
        private Supplier<T> factory;
        private int maxSize;
        
        public ObjectPool(Supplier<T> factory, int maxSize) {
            this.factory = factory;
            this.maxSize = maxSize;
            this.pool = new ConcurrentLinkedQueue<>();
        }
        
        public T acquire() {
            T obj = pool.poll();
            if (obj == null) {
                obj = factory.get();
            }
            return obj;
        }
        
        public void release(T obj) {
            if (pool.size() < maxSize) {
                pool.offer(obj);
            }
        }
    }
    
    // String interning for memory efficiency
    public class StringInterner {
        private Map<String, String> internedStrings;
        
        public StringInterner() {
            this.internedStrings = new ConcurrentHashMap<>();
        }
        
        public String intern(String str) {
            return internedStrings.computeIfAbsent(str, k -> k);
        }
        
        public int getSize() {
            return internedStrings.size();
        }
    }
}
```

## 23.8 Scalability Patterns

### Horizontal Scaling Patterns

```java
public class HorizontalScalingPatterns {
    // Consistent Hashing for distributed systems
    public class ConsistentHashRing {
        private SortedMap<Long, String> ring;
        private int numberOfReplicas;
        
        public ConsistentHashRing(int numberOfReplicas, Collection<String> nodes) {
            this.numberOfReplicas = numberOfReplicas;
            this.ring = new TreeMap<>();
            
            for (String node : nodes) {
                addNode(node);
            }
        }
        
        public void addNode(String node) {
            for (int i = 0; i < numberOfReplicas; i++) {
                String virtualNode = node + ":" + i;
                long hash = hash(virtualNode);
                ring.put(hash, node);
            }
        }
        
        public void removeNode(String node) {
            for (int i = 0; i < numberOfReplicas; i++) {
                String virtualNode = node + ":" + i;
                long hash = hash(virtualNode);
                ring.remove(hash);
            }
        }
        
        public String getNode(String key) {
            if (ring.isEmpty()) return null;
            
            long hash = hash(key);
            SortedMap<Long, String> tailMap = ring.tailMap(hash);
            
            if (tailMap.isEmpty()) {
                return ring.get(ring.firstKey());
            }
            
            return tailMap.get(tailMap.firstKey());
        }
        
        private long hash(String input) {
            return input.hashCode();
        }
    }
    
    // Sharding strategy
    public class ShardingStrategy {
        private int numberOfShards;
        private List<Shard> shards;
        
        public ShardingStrategy(int numberOfShards) {
            this.numberOfShards = numberOfShards;
            this.shards = new ArrayList<>();
            
            for (int i = 0; i < numberOfShards; i++) {
                shards.add(new Shard(i));
            }
        }
        
        public Shard getShard(String key) {
            int hash = key.hashCode();
            int shardIndex = Math.abs(hash) % numberOfShards;
            return shards.get(shardIndex);
        }
        
        public void addShard() {
            numberOfShards++;
            shards.add(new Shard(numberOfShards - 1));
        }
        
        public void removeShard(int shardIndex) {
            if (shardIndex < numberOfShards) {
                shards.remove(shardIndex);
                numberOfShards--;
            }
        }
        
        public static class Shard {
            private int id;
            private Map<String, Object> data;
            
            public Shard(int id) {
                this.id = id;
                this.data = new ConcurrentHashMap<>();
            }
            
            public void put(String key, Object value) {
                data.put(key, value);
            }
            
            public Object get(String key) {
                return data.get(key);
            }
            
            public void remove(String key) {
                data.remove(key);
            }
            
            public int getId() {
                return id;
            }
        }
    }
}
```

### Vertical Scaling Patterns

```java
public class VerticalScalingPatterns {
    // Connection pooling for database connections
    public class ConnectionPool {
        private Queue<Connection> availableConnections;
        private Set<Connection> usedConnections;
        private int maxConnections;
        private String url;
        private String username;
        private String password;
        
        public ConnectionPool(String url, String username, String password, int maxConnections) {
            this.url = url;
            this.username = username;
            this.password = password;
            this.maxConnections = maxConnections;
            this.availableConnections = new ConcurrentLinkedQueue<>();
            this.usedConnections = ConcurrentHashMap.newKeySet();
        }
        
        public Connection getConnection() throws SQLException {
            Connection connection = availableConnections.poll();
            if (connection == null) {
                if (usedConnections.size() < maxConnections) {
                    connection = DriverManager.getConnection(url, username, password);
                } else {
                    throw new SQLException("No available connections");
                }
            }
            usedConnections.add(connection);
            return connection;
        }
        
        public void releaseConnection(Connection connection) {
            if (usedConnections.remove(connection)) {
                availableConnections.offer(connection);
            }
        }
        
        public void closeAllConnections() throws SQLException {
            for (Connection connection : availableConnections) {
                connection.close();
            }
            for (Connection connection : usedConnections) {
                connection.close();
            }
            availableConnections.clear();
            usedConnections.clear();
        }
    }
    
    // Thread pool for CPU-intensive tasks
    public class ThreadPool {
        private ExecutorService executor;
        private int corePoolSize;
        private int maximumPoolSize;
        private long keepAliveTime;
        private TimeUnit unit;
        private BlockingQueue<Runnable> workQueue;
        
        public ThreadPool(int corePoolSize, int maximumPoolSize, long keepAliveTime, TimeUnit unit) {
            this.corePoolSize = corePoolSize;
            this.maximumPoolSize = maximumPoolSize;
            this.keepAliveTime = keepAliveTime;
            this.unit = unit;
            this.workQueue = new LinkedBlockingQueue<>();
            this.executor = new ThreadPoolExecutor(corePoolSize, maximumPoolSize, keepAliveTime, unit, workQueue);
        }
        
        public Future<?> submit(Runnable task) {
            return executor.submit(task);
        }
        
        public <T> Future<T> submit(Callable<T> task) {
            return executor.submit(task);
        }
        
        public void shutdown() {
            executor.shutdown();
        }
        
        public boolean awaitTermination(long timeout, TimeUnit unit) throws InterruptedException {
            return executor.awaitTermination(timeout, unit);
        }
    }
}
```

**Real-world Analogies:**
- **Complexity Analysis:** Like measuring how long it takes to find a book in a library (linear search vs catalog system)
- **Space-Time Tradeoffs:** Like choosing between a small, fast car or a large, slow truck for different tasks
- **Amortized Analysis:** Like the cost of a gym membership - expensive upfront but cheap per workout
- **Competitive Analysis:** Like comparing a taxi driver who knows the city vs one who doesn't
- **Worst-Case vs Average-Case:** Like planning for the worst traffic vs typical traffic
- **Profiling:** Like using a stopwatch to time different routes to work
- **Optimization:** Like tuning a car engine for better performance
- **Scalability Patterns:** Like designing a restaurant that can handle more customers by adding tables or opening new locations

Performance and scalability are critical aspects of algorithm design and system architecture. Understanding these concepts helps in choosing the right algorithms and designing systems that can handle growth while maintaining performance.