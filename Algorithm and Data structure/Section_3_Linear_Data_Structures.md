# Section 3 – Linear Data Structures

## 3.1 Vectors & Dynamic Arrays

Vectors are dynamic arrays that can grow and shrink automatically, providing efficient random access and dynamic sizing.

### Vector Implementation

```java
public class Vector<T> {
    private T[] array;
    private int size;
    private int capacity;
    private static final int DEFAULT_CAPACITY = 10;
    private static final double GROWTH_FACTOR = 1.5;
    
    @SuppressWarnings("unchecked")
    public Vector() {
        this.capacity = DEFAULT_CAPACITY;
        this.size = 0;
        this.array = (T[]) new Object[capacity];
    }
    
    public void add(T element) {
        if (size >= capacity) {
            resize();
        }
        array[size++] = element;
    }
    
    public void add(int index, T element) {
        if (index < 0 || index > size) {
            throw new IndexOutOfBoundsException();
        }
        
        if (size >= capacity) {
            resize();
        }
        
        // Shift elements to the right
        for (int i = size; i > index; i--) {
            array[i] = array[i - 1];
        }
        
        array[index] = element;
        size++;
    }
    
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        return array[index];
    }
    
    public T set(int index, T element) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        T oldElement = array[index];
        array[index] = element;
        return oldElement;
    }
    
    public T remove(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        T removed = array[index];
        
        // Shift elements to the left
        for (int i = index; i < size - 1; i++) {
            array[i] = array[i + 1];
        }
        
        size--;
        return removed;
    }
    
    @SuppressWarnings("unchecked")
    private void resize() {
        capacity = (int) (capacity * GROWTH_FACTOR);
        T[] newArray = (T[]) new Object[capacity];
        System.arraycopy(array, 0, newArray, 0, size);
        array = newArray;
    }
    
    public int size() { return size; }
    public boolean isEmpty() { return size == 0; }
    public int capacity() { return capacity; }
}
```

**Real-world Analogy:** Like a parking garage that can expand by adding more floors when it gets full.

## 3.2 Deques (Double-ended Queues)

Deques allow insertion and deletion at both ends, combining the benefits of stacks and queues.

### Deque Implementation

```java
public class Deque<T> {
    private T[] array;
    private int front;
    private int rear;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public Deque(int capacity) {
        this.capacity = capacity;
        this.array = (T[]) new Object[capacity];
        this.front = 0;
        this.rear = 0;
        this.size = 0;
    }
    
    public void addFirst(T element) {
        if (isFull()) {
            throw new IllegalStateException("Deque is full");
        }
        
        front = (front - 1 + capacity) % capacity;
        array[front] = element;
        size++;
    }
    
    public void addLast(T element) {
        if (isFull()) {
            throw new IllegalStateException("Deque is full");
        }
        
        array[rear] = element;
        rear = (rear + 1) % capacity;
        size++;
    }
    
    public T removeFirst() {
        if (isEmpty()) {
            throw new NoSuchElementException("Deque is empty");
        }
        
        T element = array[front];
        front = (front + 1) % capacity;
        size--;
        return element;
    }
    
    public T removeLast() {
        if (isEmpty()) {
            throw new NoSuchElementException("Deque is empty");
        }
        
        rear = (rear - 1 + capacity) % capacity;
        T element = array[rear];
        size--;
        return element;
    }
    
    public T peekFirst() {
        if (isEmpty()) return null;
        return array[front];
    }
    
    public T peekLast() {
        if (isEmpty()) return null;
        return array[(rear - 1 + capacity) % capacity];
    }
    
    public boolean isEmpty() { return size == 0; }
    public boolean isFull() { return size == capacity; }
    public int size() { return size; }
}
```

**Applications:**
- Sliding window problems
- Palindrome checking
- Undo/Redo operations

## 3.3 Priority Queues

Priority queues maintain elements in order of priority, with the highest priority element always at the front.

### Binary Heap Implementation

```java
public class PriorityQueue<T extends Comparable<T>> {
    private T[] heap;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public PriorityQueue(int capacity) {
        this.capacity = capacity;
        this.heap = (T[]) new Comparable[capacity];
        this.size = 0;
    }
    
    public void insert(T element) {
        if (size >= capacity) {
            throw new IllegalStateException("Priority queue is full");
        }
        
        heap[size] = element;
        heapifyUp(size);
        size++;
    }
    
    public T extractMax() {
        if (isEmpty()) {
            throw new NoSuchElementException("Priority queue is empty");
        }
        
        T max = heap[0];
        heap[0] = heap[size - 1];
        size--;
        heapifyDown(0);
        return max;
    }
    
    public T peek() {
        if (isEmpty()) return null;
        return heap[0];
    }
    
    private void heapifyUp(int index) {
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (heap[index].compareTo(heap[parent]) <= 0) {
                break;
            }
            swap(index, parent);
            index = parent;
        }
    }
    
    private void heapifyDown(int index) {
        while (true) {
            int left = 2 * index + 1;
            int right = 2 * index + 2;
            int largest = index;
            
            if (left < size && heap[left].compareTo(heap[largest]) > 0) {
                largest = left;
            }
            
            if (right < size && heap[right].compareTo(heap[largest]) > 0) {
                largest = right;
            }
            
            if (largest == index) break;
            
            swap(index, largest);
            index = largest;
        }
    }
    
    private void swap(int i, int j) {
        T temp = heap[i];
        heap[i] = heap[j];
        heap[j] = temp;
    }
    
    public boolean isEmpty() { return size == 0; }
    public int size() { return size; }
}
```

**Applications:**
- Task scheduling
- Dijkstra's algorithm
- Huffman coding
- A* pathfinding

## 3.4 Circular Buffers

Circular buffers provide fixed-size storage with wraparound behavior, useful for streaming data.

### Circular Buffer Implementation

```java
public class CircularBuffer<T> {
    private T[] buffer;
    private int head;
    private int tail;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public CircularBuffer(int capacity) {
        this.capacity = capacity;
        this.buffer = (T[]) new Object[capacity];
        this.head = 0;
        this.tail = 0;
        this.size = 0;
    }
    
    public void write(T data) {
        if (isFull()) {
            // Overwrite oldest data
            head = (head + 1) % capacity;
        } else {
            size++;
        }
        
        buffer[tail] = data;
        tail = (tail + 1) % capacity;
    }
    
    public T read() {
        if (isEmpty()) {
            throw new NoSuchElementException("Buffer is empty");
        }
        
        T data = buffer[head];
        head = (head + 1) % capacity;
        size--;
        return data;
    }
    
    public T peek() {
        if (isEmpty()) return null;
        return buffer[head];
    }
    
    public boolean isEmpty() { return size == 0; }
    public boolean isFull() { return size == capacity; }
    public int size() { return size; }
    public int capacity() { return capacity; }
}
```

**Applications:**
- Audio/video streaming
- Network packet buffering
- Log file rotation
- Producer-consumer patterns

## 3.5 Sparse Arrays

Sparse arrays efficiently store arrays with many zero or null values by only storing non-zero elements.

### Sparse Array Implementation

```java
public class SparseArray<T> {
    private Map<Integer, T> elements;
    private T defaultValue;
    private int size;
    
    public SparseArray(int size, T defaultValue) {
        this.size = size;
        this.defaultValue = defaultValue;
        this.elements = new HashMap<>();
    }
    
    public void set(int index, T value) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        if (value.equals(defaultValue)) {
            elements.remove(index);
        } else {
            elements.put(index, value);
        }
    }
    
    public T get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        return elements.getOrDefault(index, defaultValue);
    }
    
    public void clear() {
        elements.clear();
    }
    
    public int size() { return size; }
    public int actualSize() { return elements.size(); }
    public boolean isEmpty() { return elements.isEmpty(); }
}
```

**Applications:**
- Sparse matrices
- Sparse graphs
- Memory-efficient storage
- Scientific computing

## 3.6 Bit Arrays & Bit Manipulation

Bit arrays provide space-efficient storage for boolean values and enable efficient bit-level operations.

### Bit Array Implementation

```java
public class BitArray {
    private long[] bits;
    private int size;
    private static final int BITS_PER_LONG = 64;
    
    public BitArray(int size) {
        this.size = size;
        this.bits = new long[(size + BITS_PER_LONG - 1) / BITS_PER_LONG];
    }
    
    public void set(int index, boolean value) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        int arrayIndex = index / BITS_PER_LONG;
        int bitIndex = index % BITS_PER_LONG;
        
        if (value) {
            bits[arrayIndex] |= (1L << bitIndex);
        } else {
            bits[arrayIndex] &= ~(1L << bitIndex);
        }
    }
    
    public boolean get(int index) {
        if (index < 0 || index >= size) {
            throw new IndexOutOfBoundsException();
        }
        
        int arrayIndex = index / BITS_PER_LONG;
        int bitIndex = index % BITS_PER_LONG;
        
        return (bits[arrayIndex] & (1L << bitIndex)) != 0;
    }
    
    public void flip(int index) {
        set(index, !get(index));
    }
    
    public int countSetBits() {
        int count = 0;
        for (long word : bits) {
            count += Long.bitCount(word);
        }
        return count;
    }
    
    public int size() { return size; }
}
```

### Bit Manipulation Operations

```java
public class BitManipulation {
    // Check if number is power of 2
    public static boolean isPowerOfTwo(int n) {
        return n > 0 && (n & (n - 1)) == 0;
    }
    
    // Get the rightmost set bit
    public static int getRightmostSetBit(int n) {
        return n & -n;
    }
    
    // Count number of set bits
    public static int countSetBits(int n) {
        int count = 0;
        while (n > 0) {
            count += n & 1;
            n >>= 1;
        }
        return count;
    }
    
    // Toggle all bits
    public static int toggleAllBits(int n) {
        return ~n;
    }
    
    // Check if bit is set
    public static boolean isBitSet(int n, int position) {
        return (n & (1 << position)) != 0;
    }
    
    // Set bit at position
    public static int setBit(int n, int position) {
        return n | (1 << position);
    }
    
    // Clear bit at position
    public static int clearBit(int n, int position) {
        return n & ~(1 << position);
    }
    
    // Toggle bit at position
    public static int toggleBit(int n, int position) {
        return n ^ (1 << position);
    }
}
```

**Applications:**
- Sieve of Eratosthenes
- Subset generation
- Bitmask DP
- Memory-efficient boolean storage

## 3.7 Memory Layout & Cache Efficiency

Understanding memory layout and cache behavior is crucial for writing efficient algorithms.

### Cache-Friendly Data Structures

```java
public class CacheEfficientArray {
    private int[] data;
    private int size;
    
    public CacheEfficientArray(int capacity) {
        this.data = new int[capacity];
        this.size = 0;
    }
    
    // Cache-friendly sequential access
    public int sum() {
        int sum = 0;
        for (int i = 0; i < size; i++) {
            sum += data[i];
        }
        return sum;
    }
    
    // Cache-friendly matrix multiplication
    public static void matrixMultiply(int[][] A, int[][] B, int[][] C) {
        int n = A.length;
        
        // Block size for cache optimization
        int blockSize = 64;
        
        for (int i = 0; i < n; i += blockSize) {
            for (int j = 0; j < n; j += blockSize) {
                for (int k = 0; k < n; k += blockSize) {
                    // Process block
                    for (int ii = i; ii < Math.min(i + blockSize, n); ii++) {
                        for (int jj = j; jj < Math.min(j + blockSize, n); jj++) {
                            for (int kk = k; kk < Math.min(k + blockSize, n); kk++) {
                                C[ii][jj] += A[ii][kk] * B[kk][jj];
                            }
                        }
                    }
                }
            }
        }
    }
}
```

### Memory Pool Pattern

```java
public class MemoryPool<T> {
    private T[] pool;
    private boolean[] used;
    private int size;
    private int capacity;
    
    @SuppressWarnings("unchecked")
    public MemoryPool(int capacity, Class<T> clazz) {
        this.capacity = capacity;
        this.pool = (T[]) java.lang.reflect.Array.newInstance(clazz, capacity);
        this.used = new boolean[capacity];
        this.size = 0;
    }
    
    public T allocate() {
        for (int i = 0; i < capacity; i++) {
            if (!used[i]) {
                used[i] = true;
                size++;
                return pool[i];
            }
        }
        return null; // Pool is full
    }
    
    public void deallocate(T obj) {
        for (int i = 0; i < capacity; i++) {
            if (pool[i] == obj && used[i]) {
                used[i] = false;
                size--;
                return;
            }
        }
    }
    
    public int available() { return capacity - size; }
    public int size() { return size; }
}
```

**Cache Optimization Principles:**
1. **Spatial Locality:** Access nearby memory locations
2. **Temporal Locality:** Reuse recently accessed data
3. **Data Structure Layout:** Keep related data together
4. **Blocking:** Process data in cache-sized blocks
5. **Prefetching:** Load data before it's needed

**Real-world Analogy:** Like organizing a library where books on similar topics are placed close together for easy access, cache-friendly algorithms organize data to minimize memory access time.

Understanding linear data structures and their memory characteristics is essential for writing efficient algorithms. The choice of data structure can significantly impact performance, especially when dealing with large datasets or real-time systems.