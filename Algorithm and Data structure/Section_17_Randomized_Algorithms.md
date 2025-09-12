# Section 17 – Randomized Algorithms

## 17.1 Randomized Algorithm Design

Randomized algorithms use randomness as a fundamental part of their logic. They often provide simpler, faster, or more elegant solutions to problems that are difficult to solve deterministically.

### Key Concepts

**Randomness:** The use of random choices in algorithm design
**Probabilistic Analysis:** Analyzing algorithms based on probability distributions
**Las Vegas Algorithms:** Always produce correct results, but running time is random
**Monte Carlo Algorithms:** May produce incorrect results, but running time is deterministic

**Real-world Analogy:**
Think of randomized algorithms like using a random number generator to make decisions. It's like flipping a coin to decide which path to take in a maze - sometimes you'll find the exit quickly, sometimes it takes longer, but on average it's often faster than trying every path systematically.

### Basic Randomized Algorithm Template

```java
import java.util.Random;

public class RandomizedAlgorithm {
    private Random random;
    
    public RandomizedAlgorithm() {
        this.random = new Random();
    }
    
    public RandomizedAlgorithm(long seed) {
        this.random = new Random(seed);
    }
    
    // Generate random integer in range [min, max]
    public int randomInt(int min, int max) {
        return min + random.nextInt(max - min + 1);
    }
    
    // Generate random double in range [0, 1)
    public double randomDouble() {
        return random.nextDouble();
    }
    
    // Shuffle array using Fisher-Yates algorithm
    public void shuffle(int[] arr) {
        for (int i = arr.length - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            swap(arr, i, j);
        }
    }
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    // Generate random permutation
    public int[] randomPermutation(int n) {
        int[] perm = new int[n];
        for (int i = 0; i < n; i++) {
            perm[i] = i;
        }
        shuffle(perm);
        return perm;
    }
}
```

## 17.2 Monte Carlo Methods

Monte Carlo methods use random sampling to approximate solutions to problems.

### Estimating π using Monte Carlo

```java
public class MonteCarloPi {
    public static double estimatePi(int numSamples) {
        Random random = new Random();
        int pointsInCircle = 0;
        
        for (int i = 0; i < numSamples; i++) {
            double x = random.nextDouble() * 2 - 1; // [-1, 1]
            double y = random.nextDouble() * 2 - 1; // [-1, 1]
            
            if (x * x + y * y <= 1) {
                pointsInCircle++;
            }
        }
        
        return 4.0 * pointsInCircle / numSamples;
    }
    
    // Estimate area under curve y = f(x) using Monte Carlo
    public static double estimateIntegral(java.util.function.Function<Double, Double> f, 
                                        double a, double b, double maxY, int numSamples) {
        Random random = new Random();
        int pointsUnderCurve = 0;
        
        for (int i = 0; i < numSamples; i++) {
            double x = a + random.nextDouble() * (b - a);
            double y = random.nextDouble() * maxY;
            
            if (y <= f.apply(x)) {
                pointsUnderCurve++;
            }
        }
        
        return (b - a) * maxY * pointsUnderCurve / numSamples;
    }
}
```

### Monte Carlo Integration

```java
public class MonteCarloIntegration {
    public static double integrate(java.util.function.Function<Double, Double> f, 
                                 double a, double b, int numSamples) {
        Random random = new Random();
        double sum = 0;
        
        for (int i = 0; i < numSamples; i++) {
            double x = a + random.nextDouble() * (b - a);
            sum += f.apply(x);
        }
        
        return (b - a) * sum / numSamples;
    }
    
    // Multi-dimensional integration
    public static double integrate2D(java.util.function.BiFunction<Double, Double, Double> f,
                                   double xMin, double xMax, double yMin, double yMax, 
                                   int numSamples) {
        Random random = new Random();
        double sum = 0;
        
        for (int i = 0; i < numSamples; i++) {
            double x = xMin + random.nextDouble() * (xMax - xMin);
            double y = yMin + random.nextDouble() * (yMax - yMin);
            sum += f.apply(x, y);
        }
        
        return (xMax - xMin) * (yMax - yMin) * sum / numSamples;
    }
}
```

## 17.3 Las Vegas Algorithms

Las Vegas algorithms always produce correct results, but their running time is random.

### Randomized Quick Sort

```java
public class RandomizedQuickSort {
    private Random random;
    
    public RandomizedQuickSort() {
        this.random = new Random();
    }
    
    public void quickSort(int[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Randomly choose pivot
            int randomIndex = low + random.nextInt(high - low + 1);
            swap(arr, randomIndex, high);
            
            int pivotIndex = partition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
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
    
    // Expected Time Complexity: O(n log n)
    // Worst Case Time Complexity: O(n²)
    // Space Complexity: O(log n)
}
```

### Randomized Selection (Quick Select)

```java
public class RandomizedSelection {
    private Random random;
    
    public RandomizedSelection() {
        this.random = new Random();
    }
    
    // Find k-th smallest element
    public int quickSelect(int[] arr, int k) {
        return quickSelect(arr, 0, arr.length - 1, k - 1);
    }
    
    private int quickSelect(int[] arr, int low, int high, int k) {
        if (low == high) {
            return arr[low];
        }
        
        // Randomly choose pivot
        int randomIndex = low + random.nextInt(high - low + 1);
        swap(arr, randomIndex, high);
        
        int pivotIndex = partition(arr, low, high);
        
        if (k == pivotIndex) {
            return arr[k];
        } else if (k < pivotIndex) {
            return quickSelect(arr, low, pivotIndex - 1, k);
        } else {
            return quickSelect(arr, pivotIndex + 1, high, k);
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
    
    // Expected Time Complexity: O(n)
    // Worst Case Time Complexity: O(n²)
    // Space Complexity: O(1)
}
```

## 17.4 Randomized Quick Sort

A detailed implementation of randomized quicksort with analysis.

```java
public class RandomizedQuickSortDetailed {
    private Random random;
    private int comparisons;
    
    public RandomizedQuickSortDetailed() {
        this.random = new Random();
        this.comparisons = 0;
    }
    
    public void quickSort(int[] arr) {
        comparisons = 0;
        quickSort(arr, 0, arr.length - 1);
    }
    
    private void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            // Random pivot selection
            int pivotIndex = randomPartition(arr, low, high);
            quickSort(arr, low, pivotIndex - 1);
            quickSort(arr, pivotIndex + 1, high);
        }
    }
    
    private int randomPartition(int[] arr, int low, int high) {
        int randomIndex = low + random.nextInt(high - low + 1);
        swap(arr, randomIndex, high);
        return partition(arr, low, high);
    }
    
    private int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            comparisons++;
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
    
    public int getComparisons() {
        return comparisons;
    }
    
    // Analyze performance over multiple runs
    public void analyzePerformance(int[] arr, int numRuns) {
        int totalComparisons = 0;
        int minComparisons = Integer.MAX_VALUE;
        int maxComparisons = 0;
        
        for (int i = 0; i < numRuns; i++) {
            int[] copy = arr.clone();
            quickSort(copy);
            
            int comp = getComparisons();
            totalComparisons += comp;
            minComparisons = Math.min(minComparisons, comp);
            maxComparisons = Math.max(maxComparisons, comp);
        }
        
        double avgComparisons = (double) totalComparisons / numRuns;
        System.out.println("Average comparisons: " + avgComparisons);
        System.out.println("Min comparisons: " + minComparisons);
        System.out.println("Max comparisons: " + maxComparisons);
    }
}
```

## 17.5 Randomized Selection

Finding the k-th smallest element using randomization.

```java
public class RandomizedSelectionDetailed {
    private Random random;
    private int comparisons;
    
    public RandomizedSelectionDetailed() {
        this.random = new Random();
        this.comparisons = 0;
    }
    
    public int findKthSmallest(int[] arr, int k) {
        if (k < 1 || k > arr.length) {
            throw new IllegalArgumentException("k must be between 1 and array length");
        }
        
        comparisons = 0;
        return quickSelect(arr, 0, arr.length - 1, k - 1);
    }
    
    private int quickSelect(int[] arr, int low, int high, int k) {
        if (low == high) {
            return arr[low];
        }
        
        int pivotIndex = randomPartition(arr, low, high);
        
        if (k == pivotIndex) {
            return arr[k];
        } else if (k < pivotIndex) {
            return quickSelect(arr, low, pivotIndex - 1, k);
        } else {
            return quickSelect(arr, pivotIndex + 1, high, k);
        }
    }
    
    private int randomPartition(int[] arr, int low, int high) {
        int randomIndex = low + random.nextInt(high - low + 1);
        swap(arr, randomIndex, high);
        return partition(arr, low, high);
    }
    
    private int partition(int[] arr, int low, int high) {
        int pivot = arr[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            comparisons++;
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
    
    public int getComparisons() {
        return comparisons;
    }
}
```

## 17.6 Hashing & Hash Functions

Randomized hashing for efficient data structures.

### Universal Hashing

```java
public class UniversalHashing {
    private int m; // Table size
    private int a, b; // Hash function parameters
    private Random random;
    
    public UniversalHashing(int tableSize) {
        this.m = tableSize;
        this.random = new Random();
        generateHashFunction();
    }
    
    private void generateHashFunction() {
        // Choose a and b randomly
        a = random.nextInt(m - 1) + 1; // a ∈ [1, m-1]
        b = random.nextInt(m);         // b ∈ [0, m-1]
    }
    
    public int hash(int key) {
        return ((a * key + b) % Integer.MAX_VALUE) % m;
    }
    
    public void rehash() {
        generateHashFunction();
    }
    
    // String hashing
    public int hashString(String str) {
        int hash = 0;
        for (int i = 0; i < str.length(); i++) {
            hash = (a * hash + str.charAt(i)) % m;
        }
        return hash;
    }
}
```

### Cuckoo Hashing

```java
public class CuckooHashing {
    private int[] table1, table2;
    private int size;
    private int capacity;
    private UniversalHashing hash1, hash2;
    private Random random;
    
    public CuckooHashing(int capacity) {
        this.capacity = capacity;
        this.table1 = new int[capacity];
        this.table2 = new int[capacity];
        this.size = 0;
        this.hash1 = new UniversalHashing(capacity);
        this.hash2 = new UniversalHashing(capacity);
        this.random = new Random();
        
        Arrays.fill(table1, -1);
        Arrays.fill(table2, -1);
    }
    
    public boolean insert(int key) {
        if (contains(key)) return true;
        if (size >= capacity) return false;
        
        int maxDisplacements = 2 * capacity;
        int current = key;
        boolean useTable1 = true;
        
        for (int i = 0; i < maxDisplacements; i++) {
            int hash = useTable1 ? hash1.hash(current) : hash2.hash(current);
            int[] table = useTable1 ? table1 : table2;
            
            if (table[hash] == -1) {
                table[hash] = current;
                size++;
                return true;
            }
            
            // Displace existing element
            int displaced = table[hash];
            table[hash] = current;
            current = displaced;
            useTable1 = !useTable1;
        }
        
        // Rehash if too many displacements
        rehash();
        return insert(current);
    }
    
    public boolean contains(int key) {
        int hash1 = this.hash1.hash(key);
        int hash2 = this.hash2.hash(key);
        
        return table1[hash1] == key || table2[hash2] == key;
    }
    
    public boolean delete(int key) {
        int hash1 = this.hash1.hash(key);
        int hash2 = this.hash2.hash(key);
        
        if (table1[hash1] == key) {
            table1[hash1] = -1;
            size--;
            return true;
        }
        
        if (table2[hash2] == key) {
            table2[hash2] = -1;
            size--;
            return true;
        }
        
        return false;
    }
    
    private void rehash() {
        int[] oldTable1 = table1.clone();
        int[] oldTable2 = table2.clone();
        
        hash1 = new UniversalHashing(capacity);
        hash2 = new UniversalHashing(capacity);
        Arrays.fill(table1, -1);
        Arrays.fill(table2, -1);
        size = 0;
        
        for (int key : oldTable1) {
            if (key != -1) insert(key);
        }
        
        for (int key : oldTable2) {
            if (key != -1) insert(key);
        }
    }
}
```

## 17.7 Probabilistic Analysis

Analyzing randomized algorithms using probability theory.

### Probabilistic Analysis of Quick Sort

```java
public class ProbabilisticAnalysis {
    // Expected number of comparisons in randomized quicksort
    public static double expectedQuickSortComparisons(int n) {
        if (n <= 1) return 0;
        
        double sum = 0;
        for (int i = 1; i <= n; i++) {
            sum += 1.0 / i;
        }
        
        return 2 * n * sum - 2 * n;
    }
    
    // Probability that randomized quicksort takes more than cn log n comparisons
    public static double probabilitySlowQuickSort(int n, double c) {
        // This is a simplified approximation
        double expected = expectedQuickSortComparisons(n);
        double variance = n * n; // Simplified variance calculation
        
        // Using Chebyshev's inequality
        double deviation = c * n * Math.log(n) - expected;
        return Math.min(1.0, variance / (deviation * deviation));
    }
    
    // Birthday paradox - probability of collision in hash table
    public static double birthdayParadox(int n, int m) {
        double probability = 1.0;
        
        for (int i = 1; i < n; i++) {
            probability *= (double) (m - i) / m;
        }
        
        return 1.0 - probability;
    }
    
    // Expected number of probes in linear probing
    public static double expectedLinearProbingProbes(double loadFactor) {
        if (loadFactor >= 1.0) return Double.POSITIVE_INFINITY;
        
        return 0.5 * (1 + 1 / (1 - loadFactor));
    }
}
```

### Randomized Algorithm Analysis

```java
public class RandomizedAlgorithmAnalysis {
    // Analyze performance of randomized algorithm over multiple runs
    public static class PerformanceStats {
        double mean;
        double variance;
        double min;
        double max;
        double median;
        
        public PerformanceStats(double[] results) {
            Arrays.sort(results);
            this.min = results[0];
            this.max = results[results.length - 1];
            this.median = results[results.length / 2];
            
            double sum = 0;
            for (double result : results) {
                sum += result;
            }
            this.mean = sum / results.length;
            
            double sumSquaredDiff = 0;
            for (double result : results) {
                sumSquaredDiff += (result - mean) * (result - mean);
            }
            this.variance = sumSquaredDiff / results.length;
        }
        
        public double getStandardDeviation() {
            return Math.sqrt(variance);
        }
        
        public double getCoefficientOfVariation() {
            return getStandardDeviation() / mean;
        }
    }
    
    // Monte Carlo estimation of algorithm performance
    public static double monteCarloEstimate(java.util.function.Supplier<Double> algorithm, 
                                          int numRuns) {
        double sum = 0;
        
        for (int i = 0; i < numRuns; i++) {
            sum += algorithm.get();
        }
        
        return sum / numRuns;
    }
    
    // Confidence interval for performance estimation
    public static double[] confidenceInterval(double[] results, double confidence) {
        Arrays.sort(results);
        int n = results.length;
        double alpha = 1 - confidence;
        int lowerIndex = (int) Math.floor(alpha / 2 * n);
        int upperIndex = (int) Math.ceil((1 - alpha / 2) * n);
        
        return new double[]{results[lowerIndex], results[upperIndex]};
    }
}
```

## 17.8 Randomized Data Structures

### Skip List (Detailed Implementation)

```java
public class SkipList<T extends Comparable<T>> {
    private static final int MAX_LEVEL = 16;
    private static final double PROBABILITY = 0.5;
    
    private static class Node<T> {
        T value;
        Node<T>[] forward;
        int level;
        
        @SuppressWarnings("unchecked")
        public Node(T value, int level) {
            this.value = value;
            this.level = level;
            this.forward = new Node[level + 1];
        }
    }
    
    private Node<T> header;
    private int level;
    private Random random;
    
    public SkipList() {
        this.header = new Node<>(null, MAX_LEVEL);
        this.level = 0;
        this.random = new Random();
    }
    
    public boolean search(T value) {
        Node<T> current = header;
        
        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null && 
                   current.forward[i].value.compareTo(value) < 0) {
                current = current.forward[i];
            }
        }
        
        current = current.forward[0];
        return current != null && current.value.equals(value);
    }
    
    public void insert(T value) {
        Node<T>[] update = new Node[MAX_LEVEL + 1];
        Node<T> current = header;
        
        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null && 
                   current.forward[i].value.compareTo(value) < 0) {
                current = current.forward[i];
            }
            update[i] = current;
        }
        
        current = current.forward[0];
        
        if (current == null || !current.value.equals(value)) {
            int newLevel = randomLevel();
            
            if (newLevel > level) {
                for (int i = level + 1; i <= newLevel; i++) {
                    update[i] = header;
                }
                level = newLevel;
            }
            
            Node<T> newNode = new Node<>(value, newLevel);
            
            for (int i = 0; i <= newLevel; i++) {
                newNode.forward[i] = update[i].forward[i];
                update[i].forward[i] = newNode;
            }
        }
    }
    
    public void delete(T value) {
        Node<T>[] update = new Node[MAX_LEVEL + 1];
        Node<T> current = header;
        
        for (int i = level; i >= 0; i--) {
            while (current.forward[i] != null && 
                   current.forward[i].value.compareTo(value) < 0) {
                current = current.forward[i];
            }
            update[i] = current;
        }
        
        current = current.forward[0];
        
        if (current != null && current.value.equals(value)) {
            for (int i = 0; i <= level; i++) {
                if (update[i].forward[i] != current) {
                    break;
                }
                update[i].forward[i] = current.forward[i];
            }
            
            while (level > 0 && header.forward[level] == null) {
                level--;
            }
        }
    }
    
    private int randomLevel() {
        int level = 0;
        while (random.nextDouble() < PROBABILITY && level < MAX_LEVEL) {
            level++;
        }
        return level;
    }
    
    // Expected time complexity: O(log n) with high probability
    // Space complexity: O(n) expected
}
```

### Bloom Filter (Probabilistic Set)

```java
public class BloomFilter {
    private BitSet bitSet;
    private int size;
    private int hashFunctions;
    private Random random;
    
    public BloomFilter(int expectedElements, double falsePositiveRate) {
        this.size = calculateSize(expectedElements, falsePositiveRate);
        this.hashFunctions = calculateHashFunctions(expectedElements, size);
        this.bitSet = new BitSet(size);
        this.random = new Random();
    }
    
    private int calculateSize(int n, double p) {
        return (int) (-n * Math.log(p) / (Math.log(2) * Math.log(2)));
    }
    
    private int calculateHashFunctions(int n, int m) {
        return (int) (m * Math.log(2) / n);
    }
    
    public void add(String element) {
        for (int i = 0; i < hashFunctions; i++) {
            int hash = hash(element, i);
            bitSet.set(Math.abs(hash % size));
        }
    }
    
    public boolean contains(String element) {
        for (int i = 0; i < hashFunctions; i++) {
            int hash = hash(element, i);
            if (!bitSet.get(Math.abs(hash % size))) {
                return false;
            }
        }
        return true;
    }
    
    private int hash(String element, int seed) {
        random.setSeed(seed);
        return element.hashCode() ^ random.nextInt();
    }
    
    public double getFalsePositiveRate() {
        return Math.pow(1 - Math.exp(-hashFunctions * (double) bitSet.cardinality() / size), hashFunctions);
    }
}
```

**Real-world Analogies:**
- **Randomized Algorithms:** Like using a random number generator to make decisions in a game
- **Monte Carlo Methods:** Like estimating the area of a circle by throwing darts randomly
- **Las Vegas Algorithms:** Like a gambler who always wins, but the time it takes is random
- **Randomized Quick Sort:** Like shuffling a deck of cards before sorting them
- **Randomized Selection:** Like randomly picking a pivot to find the median
- **Universal Hashing:** Like having multiple different ways to assign addresses to items
- **Cuckoo Hashing:** Like birds that kick out other birds from their nests
- **Skip Lists:** Like having express lanes in a highway system for faster navigation
- **Bloom Filters:** Like a quick "maybe" filter before doing expensive database lookups
- **Probabilistic Analysis:** Like using statistics to predict how well an algorithm will perform

Randomized algorithms often provide elegant solutions to complex problems and can achieve better average-case performance than their deterministic counterparts. They are particularly useful in situations where the input distribution is unknown or when we need to break ties in a fair way.