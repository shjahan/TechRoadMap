# Section 20 – Algorithm Optimization & Analysis

## 20.1 Algorithm Profiling & Benchmarking

Algorithm profiling and benchmarking are essential for understanding performance characteristics and identifying optimization opportunities.

### Basic Profiling Framework

```java
import java.util.concurrent.TimeUnit;
import java.util.function.Supplier;

public class AlgorithmProfiler {
    private static class ProfilingResult {
        long executionTime;
        long memoryUsed;
        int iterations;
        String algorithmName;
        
        public ProfilingResult(String algorithmName, long executionTime, long memoryUsed, int iterations) {
            this.algorithmName = algorithmName;
            this.executionTime = executionTime;
            this.memoryUsed = memoryUsed;
            this.iterations = iterations;
        }
        
        public double getAverageTime() {
            return (double) executionTime / iterations;
        }
        
        public String toString() {
            return String.format("%s: %dms total, %.2fms avg, %d bytes, %d iterations",
                    algorithmName, executionTime, getAverageTime(), memoryUsed, iterations);
        }
    }
    
    public static ProfilingResult profile(String algorithmName, Supplier<Void> algorithm, int iterations) {
        // Warm up
        for (int i = 0; i < 10; i++) {
            algorithm.get();
        }
        
        // Force garbage collection
        System.gc();
        
        long startMemory = getUsedMemory();
        long startTime = System.nanoTime();
        
        for (int i = 0; i < iterations; i++) {
            algorithm.get();
        }
        
        long endTime = System.nanoTime();
        long endMemory = getUsedMemory();
        
        long executionTime = TimeUnit.NANOSECONDS.toMillis(endTime - startTime);
        long memoryUsed = endMemory - startMemory;
        
        return new ProfilingResult(algorithmName, executionTime, memoryUsed, iterations);
    }
    
    private static long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
    
    // Compare multiple algorithms
    public static void compareAlgorithms(AlgorithmTest[] tests, int iterations) {
        System.out.println("Algorithm Comparison (iterations: " + iterations + ")");
        System.out.println("=" .repeat(50));
        
        for (AlgorithmTest test : tests) {
            ProfilingResult result = profile(test.name, test.algorithm, iterations);
            System.out.println(result);
        }
    }
    
    public static class AlgorithmTest {
        String name;
        Supplier<Void> algorithm;
        
        public AlgorithmTest(String name, Supplier<Void> algorithm) {
            this.name = name;
            this.algorithm = algorithm;
        }
    }
}
```

### Microbenchmarking with JMH

```java
import org.openjdk.jmh.annotations.*;
import org.openjdk.jmh.runner.Runner;
import org.openjdk.jmh.runner.RunnerException;
import org.openjdk.jmh.runner.options.Options;
import org.openjdk.jmh.runner.options.OptionsBuilder;

@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
public class AlgorithmBenchmark {
    
    private int[] testData;
    private int target;
    
    @Setup
    public void setup() {
        testData = generateTestData(10000);
        target = testData[5000];
    }
    
    @Benchmark
    public int linearSearch() {
        for (int i = 0; i < testData.length; i++) {
            if (testData[i] == target) {
                return i;
            }
        }
        return -1;
    }
    
    @Benchmark
    public int binarySearch() {
        int left = 0, right = testData.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (testData[mid] == target) {
                return mid;
            } else if (testData[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
    
    private int[] generateTestData(int size) {
        int[] data = new int[size];
        for (int i = 0; i < size; i++) {
            data[i] = i;
        }
        return data;
    }
    
    public static void main(String[] args) throws RunnerException {
        Options opt = new OptionsBuilder()
                .include(AlgorithmBenchmark.class.getSimpleName())
                .forks(1)
                .warmupIterations(5)
                .measurementIterations(10)
                .build();
        
        new Runner(opt).run();
    }
}
```

## 20.2 Cache-Efficient Algorithms

Cache efficiency is crucial for performance in modern computer systems.

### Cache-Aware Matrix Multiplication

```java
public class CacheEfficientMatrixMultiplication {
    private static final int BLOCK_SIZE = 64; // Cache line size
    
    public static int[][] multiply(int[][] A, int[][] B) {
        int n = A.length;
        int[][] C = new int[n][n];
        
        // Blocked matrix multiplication for cache efficiency
        for (int ii = 0; ii < n; ii += BLOCK_SIZE) {
            for (int jj = 0; jj < n; jj += BLOCK_SIZE) {
                for (int kk = 0; kk < n; kk += BLOCK_SIZE) {
                    // Multiply blocks
                    for (int i = ii; i < Math.min(ii + BLOCK_SIZE, n); i++) {
                        for (int j = jj; j < Math.min(jj + BLOCK_SIZE, n); j++) {
                            for (int k = kk; k < Math.min(kk + BLOCK_SIZE, n); k++) {
                                C[i][j] += A[i][k] * B[k][j];
                            }
                        }
                    }
                }
            }
        }
        
        return C;
    }
    
    // Transpose matrix for better cache locality
    public static int[][] multiplyWithTranspose(int[][] A, int[][] B) {
        int n = A.length;
        int[][] Bt = transpose(B);
        int[][] C = new int[n][n];
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    C[i][j] += A[i][k] * Bt[j][k];
                }
            }
        }
        
        return C;
    }
    
    private static int[][] transpose(int[][] matrix) {
        int n = matrix.length;
        int[][] transposed = new int[n][n];
        
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                transposed[i][j] = matrix[j][i];
            }
        }
        
        return transposed;
    }
}
```

### Cache-Oblivious Algorithms

```java
public class CacheObliviousAlgorithms {
    
    // Cache-oblivious matrix multiplication
    public static int[][] multiplyCacheOblivious(int[][] A, int[][] B) {
        int n = A.length;
        int[][] C = new int[n][n];
        multiplyRecursive(A, B, C, 0, 0, 0, 0, 0, 0, n);
        return C;
    }
    
    private static void multiplyRecursive(int[][] A, int[][] B, int[][] C,
                                        int aRow, int aCol, int bRow, int bCol,
                                        int cRow, int cCol, int size) {
        if (size <= 64) { // Base case
            for (int i = 0; i < size; i++) {
                for (int j = 0; j < size; j++) {
                    for (int k = 0; k < size; k++) {
                        C[cRow + i][cCol + j] += A[aRow + i][aCol + k] * B[bRow + k][bCol + j];
                    }
                }
            }
        } else {
            int half = size / 2;
            
            // Recursively multiply submatrices
            multiplyRecursive(A, B, C, aRow, aCol, bRow, bCol, cRow, cCol, half);
            multiplyRecursive(A, B, C, aRow, aCol + half, bRow + half, bCol, cRow, cCol, half);
            
            multiplyRecursive(A, B, C, aRow, aCol, bRow, bCol + half, cRow, cCol + half, half);
            multiplyRecursive(A, B, C, aRow, aCol + half, bRow + half, bCol + half, cRow, cCol + half, half);
            
            multiplyRecursive(A, B, C, aRow + half, aCol, bRow, bCol, cRow + half, cCol, half);
            multiplyRecursive(A, B, C, aRow + half, aCol + half, bRow + half, bCol, cRow + half, cCol, half);
            
            multiplyRecursive(A, B, C, aRow + half, aCol, bRow, bCol + half, cRow + half, cCol + half, half);
            multiplyRecursive(A, B, C, aRow + half, aCol + half, bRow + half, bCol + half, cRow + half, cCol + half, half);
        }
    }
    
    // Cache-oblivious merge sort
    public static void mergeSortCacheOblivious(int[] arr) {
        mergeSortRecursive(arr, 0, arr.length - 1);
    }
    
    private static void mergeSortRecursive(int[] arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSortRecursive(arr, left, mid);
            mergeSortRecursive(arr, mid + 1, right);
            merge(arr, left, mid, right);
        }
    }
    
    private static void merge(int[] arr, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        
        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
            }
        }
        
        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];
        
        System.arraycopy(temp, 0, arr, left, temp.length);
    }
}
```

## 20.3 Memory-Efficient Data Structures

### Memory-Efficient Hash Table

```java
public class MemoryEfficientHashTable<K, V> {
    private static final int DEFAULT_CAPACITY = 16;
    private static final double LOAD_FACTOR = 0.75;
    
    private Entry[] table;
    private int size;
    private int capacity;
    
    public MemoryEfficientHashTable() {
        this(DEFAULT_CAPACITY);
    }
    
    public MemoryEfficientHashTable(int initialCapacity) {
        this.capacity = initialCapacity;
        this.table = new Entry[capacity];
        this.size = 0;
    }
    
    public void put(K key, V value) {
        if (size >= capacity * LOAD_FACTOR) {
            resize();
        }
        
        int index = hash(key) % capacity;
        Entry entry = table[index];
        
        if (entry == null) {
            table[index] = new Entry(key, value);
            size++;
        } else {
            // Handle collision with chaining
            while (entry.next != null) {
                if (entry.key.equals(key)) {
                    entry.value = value;
                    return;
                }
                entry = entry.next;
            }
            
            if (entry.key.equals(key)) {
                entry.value = value;
            } else {
                entry.next = new Entry(key, value);
                size++;
            }
        }
    }
    
    public V get(K key) {
        int index = hash(key) % capacity;
        Entry entry = table[index];
        
        while (entry != null) {
            if (entry.key.equals(key)) {
                return entry.value;
            }
            entry = entry.next;
        }
        
        return null;
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
    
    private int hash(K key) {
        return key.hashCode() & 0x7FFFFFFF; // Ensure positive
    }
    
    private static class Entry {
        Object key;
        Object value;
        Entry next;
        
        public Entry(Object key, Object value) {
            this.key = key;
            this.value = value;
            this.next = null;
        }
    }
}
```

### Memory-Efficient String Storage

```java
public class MemoryEfficientStringStorage {
    private char[] buffer;
    private int[] offsets;
    private int[] lengths;
    private int bufferSize;
    private int stringCount;
    
    public MemoryEfficientStringStorage(int initialCapacity) {
        this.buffer = new char[initialCapacity];
        this.offsets = new int[initialCapacity];
        this.lengths = new int[initialCapacity];
        this.bufferSize = 0;
        this.stringCount = 0;
    }
    
    public int addString(String str) {
        if (stringCount >= offsets.length) {
            resize();
        }
        
        int offset = bufferSize;
        int length = str.length();
        
        // Ensure buffer has enough space
        if (bufferSize + length > buffer.length) {
            resizeBuffer();
        }
        
        // Copy string to buffer
        str.getChars(0, length, buffer, bufferSize);
        
        offsets[stringCount] = offset;
        lengths[stringCount] = length;
        bufferSize += length;
        
        return stringCount++;
    }
    
    public String getString(int index) {
        if (index < 0 || index >= stringCount) {
            throw new IndexOutOfBoundsException("Index: " + index);
        }
        
        int offset = offsets[index];
        int length = lengths[index];
        
        return new String(buffer, offset, length);
    }
    
    private void resize() {
        int newCapacity = offsets.length * 2;
        int[] newOffsets = new int[newCapacity];
        int[] newLengths = new int[newCapacity];
        
        System.arraycopy(offsets, 0, newOffsets, 0, stringCount);
        System.arraycopy(lengths, 0, newLengths, 0, stringCount);
        
        offsets = newOffsets;
        lengths = newLengths;
    }
    
    private void resizeBuffer() {
        char[] newBuffer = new char[buffer.length * 2];
        System.arraycopy(buffer, 0, newBuffer, 0, bufferSize);
        buffer = newBuffer;
    }
    
    public int getStringCount() {
        return stringCount;
    }
    
    public int getTotalMemoryUsage() {
        return buffer.length * 2 + offsets.length * 4 + lengths.length * 4; // Rough estimate
    }
}
```

## 20.4 I/O Efficient Algorithms

### External Merge Sort

```java
import java.io.*;
import java.util.*;

public class ExternalMergeSort {
    private static final int CHUNK_SIZE = 1000000; // 1 million integers per chunk
    
    public static void sort(String inputFile, String outputFile) throws IOException {
        List<String> chunkFiles = createSortedChunks(inputFile);
        mergeChunks(chunkFiles, outputFile);
        
        // Clean up temporary files
        for (String chunkFile : chunkFiles) {
            new File(chunkFile).delete();
        }
    }
    
    private static List<String> createSortedChunks(String inputFile) throws IOException {
        List<String> chunkFiles = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new FileReader(inputFile));
        List<Integer> chunk = new ArrayList<>();
        int chunkIndex = 0;
        
        String line;
        while ((line = reader.readLine()) != null) {
            chunk.add(Integer.parseInt(line));
            
            if (chunk.size() >= CHUNK_SIZE) {
                String chunkFile = "chunk_" + chunkIndex + ".tmp";
                writeSortedChunk(chunk, chunkFile);
                chunkFiles.add(chunkFile);
                chunk.clear();
                chunkIndex++;
            }
        }
        
        // Write remaining elements
        if (!chunk.isEmpty()) {
            String chunkFile = "chunk_" + chunkIndex + ".tmp";
            writeSortedChunk(chunk, chunkFile);
            chunkFiles.add(chunkFile);
        }
        
        reader.close();
        return chunkFiles;
    }
    
    private static void writeSortedChunk(List<Integer> chunk, String filename) throws IOException {
        Collections.sort(chunk);
        BufferedWriter writer = new BufferedWriter(new FileWriter(filename));
        
        for (Integer value : chunk) {
            writer.write(value.toString());
            writer.newLine();
        }
        
        writer.close();
    }
    
    private static void mergeChunks(List<String> chunkFiles, String outputFile) throws IOException {
        PriorityQueue<ChunkReader> heap = new PriorityQueue<>();
        BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile));
        
        // Initialize heap with first element from each chunk
        for (String chunkFile : chunkFiles) {
            ChunkReader reader = new ChunkReader(chunkFile);
            if (reader.hasNext()) {
                heap.offer(reader);
            }
        }
        
        // Merge chunks
        while (!heap.isEmpty()) {
            ChunkReader reader = heap.poll();
            writer.write(reader.next().toString());
            writer.newLine();
            
            if (reader.hasNext()) {
                heap.offer(reader);
            } else {
                reader.close();
            }
        }
        
        writer.close();
    }
    
    private static class ChunkReader implements Comparable<ChunkReader> {
        private BufferedReader reader;
        private Integer current;
        private String filename;
        
        public ChunkReader(String filename) throws IOException {
            this.filename = filename;
            this.reader = new BufferedReader(new FileReader(filename));
            this.current = null;
            readNext();
        }
        
        public boolean hasNext() {
            return current != null;
        }
        
        public Integer next() {
            Integer result = current;
            readNext();
            return result;
        }
        
        private void readNext() {
            try {
                String line = reader.readLine();
                current = (line != null) ? Integer.parseInt(line) : null;
            } catch (IOException e) {
                current = null;
            }
        }
        
        public void close() throws IOException {
            reader.close();
        }
        
        @Override
        public int compareTo(ChunkReader other) {
            return Integer.compare(this.current, other.current);
        }
    }
}
```

### B-Tree for External Storage

```java
public class BTree {
    private static final int DEFAULT_ORDER = 3;
    
    private int order;
    private BTreeNode root;
    
    public BTree(int order) {
        this.order = order;
        this.root = new BTreeNode(true);
    }
    
    public void insert(int key, String value) {
        if (root.isFull()) {
            BTreeNode newRoot = new BTreeNode(false);
            newRoot.children.add(root);
            newRoot.splitChild(0, root);
            root = newRoot;
        }
        
        root.insertNonFull(key, value);
    }
    
    public String search(int key) {
        return root.search(key);
    }
    
    private class BTreeNode {
        private List<Integer> keys;
        private List<String> values;
        private List<BTreeNode> children;
        private boolean isLeaf;
        
        public BTreeNode(boolean isLeaf) {
            this.keys = new ArrayList<>();
            this.values = new ArrayList<>();
            this.children = new ArrayList<>();
            this.isLeaf = isLeaf;
        }
        
        public boolean isFull() {
            return keys.size() == 2 * order - 1;
        }
        
        public String search(int key) {
            int i = 0;
            while (i < keys.size() && key > keys.get(i)) {
                i++;
            }
            
            if (i < keys.size() && key == keys.get(i)) {
                return values.get(i);
            }
            
            if (isLeaf) {
                return null;
            }
            
            return children.get(i).search(key);
        }
        
        public void insertNonFull(int key, String value) {
            int i = keys.size() - 1;
            
            if (isLeaf) {
                // Insert into leaf node
                while (i >= 0 && key < keys.get(i)) {
                    i--;
                }
                keys.add(i + 1, key);
                values.add(i + 1, value);
            } else {
                // Find child to insert into
                while (i >= 0 && key < keys.get(i)) {
                    i--;
                }
                i++;
                
                if (children.get(i).isFull()) {
                    splitChild(i, children.get(i));
                    if (key > keys.get(i)) {
                        i++;
                    }
                }
                
                children.get(i).insertNonFull(key, value);
            }
        }
        
        public void splitChild(int index, BTreeNode child) {
            BTreeNode newChild = new BTreeNode(child.isLeaf);
            
            // Move keys and values
            for (int i = order; i < 2 * order - 1; i++) {
                newChild.keys.add(child.keys.get(i));
                newChild.values.add(child.values.get(i));
            }
            
            // Move children if not leaf
            if (!child.isLeaf) {
                for (int i = order; i < 2 * order; i++) {
                    newChild.children.add(child.children.get(i));
                }
            }
            
            // Remove moved keys and children from child
            for (int i = 2 * order - 2; i >= order - 1; i--) {
                child.keys.remove(i);
                child.values.remove(i);
            }
            
            if (!child.isLeaf) {
                for (int i = 2 * order - 1; i >= order; i--) {
                    child.children.remove(i);
                }
            }
            
            // Insert new child
            children.add(index + 1, newChild);
            keys.add(index, child.keys.get(order - 1));
            values.add(index, child.values.get(order - 1));
            
            // Remove moved key from child
            child.keys.remove(order - 1);
            child.values.remove(order - 1);
        }
    }
}
```

## 20.5 Algorithm Engineering

### Algorithm Selection Framework

```java
public class AlgorithmSelectionFramework {
    
    public static class AlgorithmProfile {
        String name;
        double timeComplexity;
        double spaceComplexity;
        double constantFactor;
        boolean isStable;
        boolean isInPlace;
        
        public AlgorithmProfile(String name, double timeComplexity, double spaceComplexity, 
                              double constantFactor, boolean isStable, boolean isInPlace) {
            this.name = name;
            this.timeComplexity = timeComplexity;
            this.spaceComplexity = spaceComplexity;
            this.constantFactor = constantFactor;
            this.isStable = isStable;
            this.isInPlace = isInPlace;
        }
        
        public double estimateTime(int inputSize) {
            return constantFactor * Math.pow(inputSize, timeComplexity);
        }
        
        public double estimateSpace(int inputSize) {
            return constantFactor * Math.pow(inputSize, spaceComplexity);
        }
    }
    
    public static class ProblemConstraints {
        int inputSize;
        long timeLimit;
        long memoryLimit;
        boolean requiresStability;
        boolean requiresInPlace;
        
        public ProblemConstraints(int inputSize, long timeLimit, long memoryLimit, 
                                boolean requiresStability, boolean requiresInPlace) {
            this.inputSize = inputSize;
            this.timeLimit = timeLimit;
            this.memoryLimit = memoryLimit;
            this.requiresStability = requiresStability;
            this.requiresInPlace = requiresInPlace;
        }
    }
    
    public static String selectAlgorithm(List<AlgorithmProfile> algorithms, ProblemConstraints constraints) {
        List<AlgorithmProfile> candidates = new ArrayList<>();
        
        // Filter algorithms based on constraints
        for (AlgorithmProfile algorithm : algorithms) {
            if (constraints.requiresStability && !algorithm.isStable) continue;
            if (constraints.requiresInPlace && !algorithm.isInPlace) continue;
            
            double estimatedTime = algorithm.estimateTime(constraints.inputSize);
            double estimatedSpace = algorithm.estimateSpace(constraints.inputSize);
            
            if (estimatedTime <= constraints.timeLimit && estimatedSpace <= constraints.memoryLimit) {
                candidates.add(algorithm);
            }
        }
        
        if (candidates.isEmpty()) {
            return "No suitable algorithm found";
        }
        
        // Select algorithm with best time complexity
        candidates.sort((a, b) -> Double.compare(a.timeComplexity, b.timeComplexity));
        
        return candidates.get(0).name;
    }
    
    // Example usage
    public static void main(String[] args) {
        List<AlgorithmProfile> sortingAlgorithms = Arrays.asList(
            new AlgorithmProfile("Bubble Sort", 2.0, 1.0, 0.1, true, true),
            new AlgorithmProfile("Insertion Sort", 2.0, 1.0, 0.05, true, true),
            new AlgorithmProfile("Merge Sort", 1.0, 1.0, 1.0, true, false),
            new AlgorithmProfile("Quick Sort", 1.0, 1.0, 0.5, false, true),
            new AlgorithmProfile("Heap Sort", 1.0, 1.0, 0.8, false, true)
        );
        
        ProblemConstraints constraints = new ProblemConstraints(
            1000000, 1000, 100000000, false, false
        );
        
        String selectedAlgorithm = selectAlgorithm(sortingAlgorithms, constraints);
        System.out.println("Selected algorithm: " + selectedAlgorithm);
    }
}
```

## 20.6 Competitive Programming Techniques

### Fast I/O for Competitive Programming

```java
import java.io.*;
import java.util.*;

public class FastIO {
    private BufferedReader reader;
    private StringTokenizer tokenizer;
    private PrintWriter writer;
    
    public FastIO() {
        reader = new BufferedReader(new InputStreamReader(System.in));
        writer = new PrintWriter(System.out);
        tokenizer = null;
    }
    
    public FastIO(String inputFile, String outputFile) throws IOException {
        reader = new BufferedReader(new FileReader(inputFile));
        writer = new PrintWriter(new FileWriter(outputFile));
        tokenizer = null;
    }
    
    public String next() {
        while (tokenizer == null || !tokenizer.hasMoreTokens()) {
            try {
                tokenizer = new StringTokenizer(reader.readLine());
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        return tokenizer.nextToken();
    }
    
    public int nextInt() {
        return Integer.parseInt(next());
    }
    
    public long nextLong() {
        return Long.parseLong(next());
    }
    
    public double nextDouble() {
        return Double.parseDouble(next());
    }
    
    public String nextLine() {
        try {
            return reader.readLine();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
    
    public void print(Object obj) {
        writer.print(obj);
    }
    
    public void println(Object obj) {
        writer.println(obj);
    }
    
    public void close() {
        writer.close();
    }
}
```

### Bit Manipulation Utilities

```java
public class BitManipulation {
    
    // Check if bit is set
    public static boolean isBitSet(int num, int bit) {
        return (num & (1 << bit)) != 0;
    }
    
    // Set bit
    public static int setBit(int num, int bit) {
        return num | (1 << bit);
    }
    
    // Clear bit
    public static int clearBit(int num, int bit) {
        return num & ~(1 << bit);
    }
    
    // Toggle bit
    public static int toggleBit(int num, int bit) {
        return num ^ (1 << bit);
    }
    
    // Count set bits
    public static int countSetBits(int num) {
        int count = 0;
        while (num > 0) {
            count += num & 1;
            num >>= 1;
        }
        return count;
    }
    
    // Count set bits (Brian Kernighan's algorithm)
    public static int countSetBitsFast(int num) {
        int count = 0;
        while (num > 0) {
            num &= (num - 1);
            count++;
        }
        return count;
    }
    
    // Get lowest set bit
    public static int getLowestSetBit(int num) {
        return num & (-num);
    }
    
    // Check if number is power of 2
    public static boolean isPowerOfTwo(int num) {
        return num > 0 && (num & (num - 1)) == 0;
    }
    
    // Get next power of 2
    public static int nextPowerOfTwo(int num) {
        if (num <= 0) return 1;
        if (isPowerOfTwo(num)) return num;
        
        int power = 1;
        while (power < num) {
            power <<= 1;
        }
        return power;
    }
    
    // Generate all subsets
    public static List<List<Integer>> generateSubsets(int[] nums) {
        List<List<Integer>> subsets = new ArrayList<>();
        int n = nums.length;
        
        for (int i = 0; i < (1 << n); i++) {
            List<Integer> subset = new ArrayList<>();
            for (int j = 0; j < n; j++) {
                if ((i & (1 << j)) != 0) {
                    subset.add(nums[j]);
                }
            }
            subsets.add(subset);
        }
        
        return subsets;
    }
}
```

## 20.7 Algorithm Visualization

### Sorting Algorithm Visualizer

```java
import java.util.*;
import java.util.concurrent.TimeUnit;

public class SortingVisualizer {
    private int[] array;
    private int delay;
    
    public SortingVisualizer(int[] array, int delay) {
        this.array = array.clone();
        this.delay = delay;
    }
    
    public void visualizeBubbleSort() throws InterruptedException {
        System.out.println("Bubble Sort Visualization:");
        printArray();
        
        for (int i = 0; i < array.length - 1; i++) {
            for (int j = 0; j < array.length - i - 1; j++) {
                if (array[j] > array[j + 1]) {
                    swap(j, j + 1);
                    printArray();
                    Thread.sleep(delay);
                }
            }
        }
    }
    
    public void visualizeQuickSort() throws InterruptedException {
        System.out.println("Quick Sort Visualization:");
        printArray();
        quickSort(0, array.length - 1);
    }
    
    private void quickSort(int low, int high) throws InterruptedException {
        if (low < high) {
            int pivotIndex = partition(low, high);
            quickSort(low, pivotIndex - 1);
            quickSort(pivotIndex + 1, high);
        }
    }
    
    private int partition(int low, int high) throws InterruptedException {
        int pivot = array[high];
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (array[j] <= pivot) {
                i++;
                swap(i, j);
                printArray();
                Thread.sleep(delay);
            }
        }
        
        swap(i + 1, high);
        printArray();
        Thread.sleep(delay);
        
        return i + 1;
    }
    
    private void swap(int i, int j) {
        int temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    
    private void printArray() {
        for (int value : array) {
            System.out.print(value + " ");
        }
        System.out.println();
    }
}
```

## 20.8 Performance Tuning

### JVM Tuning for Algorithm Performance

```java
public class JVMTuning {
    
    // JVM flags for optimal performance:
    // -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+UseStringDeduplication
    // -XX:+UseCompressedOops -XX:+UseCompressedClassPointers
    // -XX:+TieredCompilation -XX:TieredStopAtLevel=4
    
    public static void optimizeForAlgorithm() {
        // Set JVM properties programmatically
        System.setProperty("java.awt.headless", "true");
        System.setProperty("file.encoding", "UTF-8");
        
        // Optimize for throughput
        System.setProperty("java.util.concurrent.ForkJoinPool.common.parallelism", 
                          String.valueOf(Runtime.getRuntime().availableProcessors()));
    }
    
    // Memory allocation optimization
    public static class OptimizedArrayList<T> {
        private T[] array;
        private int size;
        private int capacity;
        
        @SuppressWarnings("unchecked")
        public OptimizedArrayList(int initialCapacity) {
            this.capacity = initialCapacity;
            this.array = (T[]) new Object[capacity];
            this.size = 0;
        }
        
        public void add(T element) {
            if (size >= capacity) {
                resize();
            }
            array[size++] = element;
        }
        
        @SuppressWarnings("unchecked")
        private void resize() {
            capacity = capacity * 2;
            T[] newArray = (T[]) new Object[capacity];
            System.arraycopy(array, 0, newArray, 0, size);
            array = newArray;
        }
        
        public T get(int index) {
            return array[index];
        }
        
        public int size() {
            return size;
        }
    }
    
    // Cache-friendly data structure
    public static class CacheFriendlyArray {
        private int[] data;
        private int size;
        
        public CacheFriendlyArray(int capacity) {
            this.data = new int[capacity];
            this.size = 0;
        }
        
        public void add(int value) {
            data[size++] = value;
        }
        
        public int get(int index) {
            return data[index];
        }
        
        // Sequential access for better cache performance
        public int sum() {
            int sum = 0;
            for (int i = 0; i < size; i++) {
                sum += data[i];
            }
            return sum;
        }
        
        // Random access (worse cache performance)
        public int sumRandom() {
            int sum = 0;
            Random random = new Random();
            for (int i = 0; i < size; i++) {
                int index = random.nextInt(size);
                sum += data[index];
            }
            return sum;
        }
    }
}
```

**Real-world Analogies:**
- **Algorithm Profiling:** Like using a stopwatch to time how long different routes take to work
- **Cache Efficiency:** Like organizing your desk so frequently used items are within arm's reach
- **Memory Efficiency:** Like packing a suitcase efficiently to fit more items
- **I/O Efficiency:** Like reading a book by loading pages in chunks instead of one word at a time
- **Algorithm Engineering:** Like choosing the right tool for each specific job
- **Competitive Programming:** Like having a well-organized toolbox for quick problem solving
- **Algorithm Visualization:** Like watching a time-lapse video of a construction project
- **Performance Tuning:** Like fine-tuning a race car for optimal speed and efficiency

Algorithm optimization and analysis are crucial for building high-performance systems. Understanding the trade-offs between time, space, and implementation complexity helps in selecting the right algorithm for each specific use case.