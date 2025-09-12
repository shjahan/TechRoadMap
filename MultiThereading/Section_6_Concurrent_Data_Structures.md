# Section 6 - Concurrent Data Structures

## 6.1 Concurrent Collections

Concurrent collections are thread-safe data structures designed to be accessed by multiple threads simultaneously without external synchronization. They provide better performance than synchronized wrappers by using lock-free algorithms and fine-grained locking.

### Key Concepts:

**1. Thread Safety:**
- Multiple threads can access the collection concurrently
- No external synchronization required
- Internal mechanisms ensure data consistency

**2. Performance Benefits:**
- Better concurrency than synchronized collections
- Reduced lock contention
- Optimized for multi-threaded access

**3. Consistency Guarantees:**
- Weak consistency for better performance
- Iterators may not reflect all changes
- Size operations may be approximate

### Java Example - ConcurrentHashMap:

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ConcurrentCollectionsExample {
    private final ConcurrentHashMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();
    
    public void demonstrateConcurrentAccess() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        // Multiple threads writing concurrently
        for (int i = 0; i < 100; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    String key = "thread-" + threadId + "-key-" + j;
                    concurrentMap.put(key, threadId * 100 + j);
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Map size: " + concurrentMap.size());
        System.out.println("Sample values: " + concurrentMap.entrySet().stream()
            .limit(5)
            .toList());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentCollectionsExample example = new ConcurrentCollectionsExample();
        example.demonstrateConcurrentAccess();
    }
}
```

### Real-World Analogy:
Think of concurrent collections like a well-organized library with multiple librarians:
- **Traditional Collections**: Like a library with one librarian who must handle all requests sequentially
- **Concurrent Collections**: Like a library with multiple librarians who can help different people simultaneously, each managing their own section

## 6.2 Lock-Free Data Structures

Lock-free data structures use atomic operations and compare-and-swap (CAS) instructions to achieve thread safety without traditional locking mechanisms. They provide better performance and avoid deadlock issues.

### Key Concepts:

**1. Atomic Operations:**
- Operations that complete in a single step
- No partial execution visible to other threads
- Hardware-level guarantees

**2. Compare-and-Swap (CAS):**
- Atomic operation that compares and updates a value
- Returns true if successful, false if value changed
- Foundation of lock-free programming

**3. ABA Problem:**
- Value changes from A to B and back to A
- CAS might succeed when it shouldn't
- Requires version numbers or hazard pointers

### Java Example - Lock-Free Stack:

```java
import java.util.concurrent.atomic.AtomicReference;

public class LockFreeStack<T> {
    private final AtomicReference<Node<T>> head = new AtomicReference<>();
    
    private static class Node<T> {
        final T data;
        final Node<T> next;
        
        Node(T data, Node<T> next) {
            this.data = data;
            this.next = next;
        }
    }
    
    public void push(T item) {
        Node<T> newHead = new Node<>(item, null);
        Node<T> currentHead;
        
        do {
            currentHead = head.get();
            newHead.next = currentHead;
        } while (!head.compareAndSet(currentHead, newHead));
    }
    
    public T pop() {
        Node<T> currentHead;
        Node<T> newHead;
        
        do {
            currentHead = head.get();
            if (currentHead == null) {
                return null;
            }
            newHead = currentHead.next;
        } while (!head.compareAndSet(currentHead, newHead));
        
        return currentHead.data;
    }
    
    public boolean isEmpty() {
        return head.get() == null;
    }
    
    public static void main(String[] args) throws InterruptedException {
        LockFreeStack<Integer> stack = new LockFreeStack<>();
        
        // Test concurrent push operations
        Thread[] pushers = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            pushers[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    stack.push(threadId * 100 + j);
                }
            });
            pushers[i].start();
        }
        
        // Test concurrent pop operations
        Thread[] poppers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            poppers[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    Integer value = stack.pop();
                    if (value != null) {
                        System.out.println("Popped: " + value);
                    }
                }
            });
            poppers[i].start();
        }
        
        for (Thread pusher : pushers) pusher.join();
        for (Thread popper : poppers) popper.join();
        
        System.out.println("Stack empty: " + stack.isEmpty());
    }
}
```

### Real-World Analogy:
Think of lock-free data structures like a busy restaurant kitchen:
- **Traditional Locks**: Like having one chef who must finish completely before another can start
- **Lock-Free**: Like multiple chefs working simultaneously, each taking ingredients as they become available without waiting for others to finish

## 6.3 Concurrent Hash Maps

Concurrent hash maps provide thread-safe hash table implementations with better concurrency than synchronized hash maps. They use techniques like segment locking or lock-free algorithms.

### Key Concepts:

**1. Segment Locking:**
- Divides the hash table into segments
- Each segment has its own lock
- Reduces lock contention

**2. Lock-Free Operations:**
- Read operations don't require locking
- Write operations use CAS
- Better performance for read-heavy workloads

**3. Consistency Levels:**
- Weak consistency for better performance
- Iterators may not reflect all changes
- Size operations may be approximate

### Java Example - ConcurrentHashMap Operations:

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ConcurrentHashMapExample {
    private final ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
    
    public void demonstrateOperations() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        // Concurrent put operations
        for (int i = 0; i < 100; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    String key = "key-" + threadId + "-" + j;
                    map.put(key, threadId * 100 + j);
                }
            });
        }
        
        // Concurrent compute operations
        for (int i = 0; i < 50; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 50; j++) {
                    String key = "key-" + threadId + "-" + j;
                    map.compute(key, (k, v) -> v == null ? 1 : v + 1);
                }
            });
        }
        
        // Concurrent get operations
        for (int i = 0; i < 30; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 30; j++) {
                    String key = "key-" + threadId + "-" + j;
                    Integer value = map.get(key);
                    if (value != null) {
                        System.out.println("Retrieved: " + key + " = " + value);
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Final map size: " + map.size());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentHashMapExample example = new ConcurrentHashMapExample();
        example.demonstrateOperations();
    }
}
```

## 6.4 Concurrent Queues

Concurrent queues provide thread-safe queue implementations that allow multiple threads to add and remove elements concurrently. They are essential for producer-consumer patterns.

### Key Concepts:

**1. Blocking vs Non-Blocking:**
- Blocking queues: Threads wait when queue is empty/full
- Non-blocking queues: Operations return immediately
- Choose based on application requirements

**2. Bounded vs Unbounded:**
- Bounded queues: Fixed capacity, prevent memory issues
- Unbounded queues: No capacity limit, risk of memory overflow

**3. Fairness:**
- Fair queues: First-come-first-served ordering
- Unfair queues: Better performance, no ordering guarantee

### Java Example - BlockingQueue:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ConcurrentQueueExample {
    private final BlockingQueue<String> queue = new LinkedBlockingQueue<>(10);
    
    public void demonstrateProducerConsumer() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        // Producer threads
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 20; j++) {
                        String item = "Producer-" + producerId + "-Item-" + j;
                        queue.put(item);
                        System.out.println("Produced: " + item);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Consumer threads
        for (int i = 0; i < 2; i++) {
            final int consumerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 30; j++) {
                        String item = queue.take();
                        System.out.println("Consumer-" + consumerId + " consumed: " + item);
                        Thread.sleep(150);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentQueueExample example = new ConcurrentQueueExample();
        example.demonstrateProducerConsumer();
    }
}
```

## 6.5 Concurrent Stacks

Concurrent stacks provide thread-safe stack implementations using lock-free algorithms. They are useful for implementing work-stealing algorithms and recursive parallel algorithms.

### Key Concepts:

**1. Lock-Free Implementation:**
- Uses atomic operations for push/pop
- No blocking or waiting
- Better performance than synchronized stacks

**2. ABA Problem Handling:**
- Uses version numbers or hazard pointers
- Ensures correct behavior with concurrent modifications

**3. Memory Management:**
- Proper handling of node allocation/deallocation
- Avoiding memory leaks in concurrent environment

### Java Example - Concurrent Stack:

```java
import java.util.concurrent.atomic.AtomicReference;

public class ConcurrentStack<T> {
    private final AtomicReference<Node<T>> top = new AtomicReference<>();
    
    private static class Node<T> {
        final T data;
        final Node<T> next;
        
        Node(T data, Node<T> next) {
            this.data = data;
            this.next = next;
        }
    }
    
    public void push(T item) {
        Node<T> newTop = new Node<>(item, null);
        Node<T> currentTop;
        
        do {
            currentTop = top.get();
            newTop.next = currentTop;
        } while (!top.compareAndSet(currentTop, newTop));
    }
    
    public T pop() {
        Node<T> currentTop;
        Node<T> newTop;
        
        do {
            currentTop = top.get();
            if (currentTop == null) {
                return null;
            }
            newTop = currentTop.next;
        } while (!top.compareAndSet(currentTop, newTop));
        
        return currentTop.data;
    }
    
    public boolean isEmpty() {
        return top.get() == null;
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentStack<Integer> stack = new ConcurrentStack<>();
        
        // Test concurrent operations
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 50; j++) {
                    if (j % 2 == 0) {
                        stack.push(threadId * 100 + j);
                    } else {
                        Integer value = stack.pop();
                        if (value != null) {
                            System.out.println("Thread " + threadId + " popped: " + value);
                        }
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Stack empty: " + stack.isEmpty());
    }
}
```

## 6.6 Concurrent Lists

Concurrent lists provide thread-safe list implementations. They are more complex than other concurrent collections due to the sequential nature of list operations.

### Key Concepts:

**1. Copy-on-Write:**
- Creates new copy for modifications
- Readers see consistent snapshot
- Good for read-heavy workloads

**2. Lock-Free Lists:**
- Use atomic operations for modifications
- Complex implementation due to list structure
- Better performance for write-heavy workloads

**3. Skip Lists:**
- Hierarchical structure for better performance
- Lock-free implementation possible
- Good for sorted concurrent lists

### Java Example - CopyOnWriteArrayList:

```java
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ConcurrentListExample {
    private final CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
    
    public void demonstrateOperations() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        // Concurrent add operations
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 20; j++) {
                    String item = "Thread-" + threadId + "-Item-" + j;
                    list.add(item);
                }
            });
        }
        
        // Concurrent read operations
        for (int i = 0; i < 3; i++) {
            final int readerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 10; j++) {
                    System.out.println("Reader " + readerId + " sees " + list.size() + " items");
                    for (String item : list) {
                        if (item.contains("Thread-0")) {
                            System.out.println("Reader " + readerId + " found: " + item);
                        }
                    }
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Final list size: " + list.size());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentListExample example = new ConcurrentListExample();
        example.demonstrateOperations();
    }
}
```

## 6.7 Copy-on-Write Structures

Copy-on-write (COW) structures create a new copy of the data structure whenever a modification is made. This ensures that readers always see a consistent snapshot.

### Key Concepts:

**1. Immutable Snapshots:**
- Readers see consistent view
- No locking required for reads
- Good for read-heavy workloads

**2. Memory Overhead:**
- Each modification creates new copy
- Can be expensive for large structures
- Garbage collection pressure

**3. Consistency Guarantees:**
- Readers see complete snapshots
- Writers don't block readers
- Eventual consistency for modifications

### Java Example - Copy-on-Write Set:

```java
import java.util.concurrent.CopyOnWriteArraySet;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class CopyOnWriteExample {
    private final CopyOnWriteArraySet<String> set = new CopyOnWriteArraySet<>();
    
    public void demonstrateCOW() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(8);
        
        // Writers
        for (int i = 0; i < 3; i++) {
            final int writerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    String item = "Writer-" + writerId + "-Item-" + j;
                    set.add(item);
                    System.out.println("Added: " + item);
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        
        // Readers
        for (int i = 0; i < 5; i++) {
            final int readerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 20; j++) {
                    System.out.println("Reader " + readerId + " sees " + set.size() + " items");
                    for (String item : set) {
                        if (item.contains("Writer-0")) {
                            System.out.println("Reader " + readerId + " found: " + item);
                        }
                    }
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Final set size: " + set.size());
    }
    
    public static void main(String[] args) throws InterruptedException {
        CopyOnWriteExample example = new CopyOnWriteExample();
        example.demonstrateCOW();
    }
}
```

## 6.8 Blocking Queues

Blocking queues are thread-safe queues that block threads when trying to add to a full queue or remove from an empty queue. They are essential for producer-consumer patterns.

### Key Concepts:

**1. Blocking Operations:**
- put(): Blocks until space available
- take(): Blocks until item available
- offer(): Non-blocking, returns false if full
- poll(): Non-blocking, returns null if empty

**2. Bounded vs Unbounded:**
- Bounded: Fixed capacity, prevents memory issues
- Unbounded: No capacity limit, risk of memory overflow

**3. Fairness:**
- Fair queues: First-come-first-served
- Unfair queues: Better performance

### Java Example - ArrayBlockingQueue:

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class BlockingQueueExample {
    private final BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);
    
    public void demonstrateBlockingQueue() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(6);
        
        // Producer threads
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 10; j++) {
                        String item = "Producer-" + producerId + "-Item-" + j;
                        queue.put(item);
                        System.out.println("Produced: " + item + " (Queue size: " + queue.size() + ")");
                        Thread.sleep(200);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Consumer threads
        for (int i = 0; i < 3; i++) {
            final int consumerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 10; j++) {
                        String item = queue.take();
                        System.out.println("Consumer-" + consumerId + " consumed: " + item + 
                                         " (Queue size: " + queue.size() + ")");
                        Thread.sleep(300);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(15, TimeUnit.SECONDS);
    }
    
    public static void main(String[] args) throws InterruptedException {
        BlockingQueueExample example = new BlockingQueueExample();
        example.demonstrateBlockingQueue();
    }
}
```

## 6.9 Concurrent Sets

Concurrent sets provide thread-safe set implementations. They are useful for maintaining unique collections of items in multi-threaded environments.

### Key Concepts:

**1. Thread Safety:**
- Multiple threads can add/remove concurrently
- No external synchronization required
- Internal mechanisms ensure uniqueness

**2. Performance Characteristics:**
- Better than synchronized sets
- Lock-free or fine-grained locking
- Optimized for concurrent access

**3. Consistency:**
- Weak consistency for better performance
- Iterators may not reflect all changes
- Size operations may be approximate

### Java Example - ConcurrentSkipListSet:

```java
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ConcurrentSetExample {
    private final ConcurrentSkipListSet<String> set = new ConcurrentSkipListSet<>();
    
    public void demonstrateConcurrentSet() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        // Concurrent add operations
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    String item = "Thread-" + threadId + "-Item-" + j;
                    boolean added = set.add(item);
                    if (added) {
                        System.out.println("Added: " + item);
                    }
                }
            });
        }
        
        // Concurrent contains operations
        for (int i = 0; i < 3; i++) {
            final int searcherId = i;
            executor.submit(() -> {
                for (int j = 0; j < 50; j++) {
                    String searchItem = "Thread-0-Item-" + j;
                    boolean contains = set.contains(searchItem);
                    if (contains) {
                        System.out.println("Searcher " + searcherId + " found: " + searchItem);
                    }
                }
            });
        }
        
        // Concurrent remove operations
        for (int i = 0; i < 2; i++) {
            final int removerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 50; j++) {
                    String item = "Thread-0-Item-" + j;
                    boolean removed = set.remove(item);
                    if (removed) {
                        System.out.println("Removed: " + item);
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Final set size: " + set.size());
        System.out.println("First few items: " + set.stream().limit(5).toList());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConcurrentSetExample example = new ConcurrentSetExample();
        example.demonstrateConcurrentSet();
    }
}
```

## 6.10 Concurrent Data Structure Selection

Choosing the right concurrent data structure depends on the specific requirements of your application. Consider factors like read/write ratio, consistency requirements, and performance characteristics.

### Selection Criteria:

**1. Read vs Write Ratio:**
- Read-heavy: Copy-on-write structures
- Write-heavy: Lock-free structures
- Balanced: ConcurrentHashMap, ConcurrentSkipListSet

**2. Consistency Requirements:**
- Strong consistency: Synchronized collections
- Weak consistency: Concurrent collections
- Eventual consistency: Copy-on-write structures

**3. Performance Requirements:**
- High throughput: Lock-free structures
- Low latency: Blocking queues
- Memory efficiency: Bounded collections

### Java Example - Performance Comparison:

```java
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class DataStructureSelectionExample {
    private static final int OPERATIONS = 100000;
    private static final int THREADS = 10;
    
    public void comparePerformance() throws InterruptedException {
        // Test different data structures
        testSynchronizedMap();
        testConcurrentHashMap();
        testCopyOnWriteArrayList();
        testConcurrentLinkedQueue();
    }
    
    private void testSynchronizedMap() throws InterruptedException {
        Map<String, Integer> map = Collections.synchronizedMap(new HashMap<>());
        long time = testMapOperations(map, "SynchronizedMap");
        System.out.println("SynchronizedMap time: " + time + "ms");
    }
    
    private void testConcurrentHashMap() throws InterruptedException {
        Map<String, Integer> map = new ConcurrentHashMap<>();
        long time = testMapOperations(map, "ConcurrentHashMap");
        System.out.println("ConcurrentHashMap time: " + time + "ms");
    }
    
    private void testCopyOnWriteArrayList() throws InterruptedException {
        List<String> list = new CopyOnWriteArrayList<>();
        long time = testListOperations(list, "CopyOnWriteArrayList");
        System.out.println("CopyOnWriteArrayList time: " + time + "ms");
    }
    
    private void testConcurrentLinkedQueue() throws InterruptedException {
        Queue<String> queue = new ConcurrentLinkedQueue<>();
        long time = testQueueOperations(queue, "ConcurrentLinkedQueue");
        System.out.println("ConcurrentLinkedQueue time: " + time + "ms");
    }
    
    private long testMapOperations(Map<String, Integer> map, String name) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(THREADS);
        CountDownLatch latch = new CountDownLatch(THREADS);
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < THREADS; i++) {
            final int threadId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < OPERATIONS / THREADS; j++) {
                        String key = name + "-" + threadId + "-" + j;
                        map.put(key, j);
                        map.get(key);
                    }
                } finally {
                    latch.countDown();
                }
            });
        }
        
        latch.await();
        executor.shutdown();
        
        return System.currentTimeMillis() - startTime;
    }
    
    private long testListOperations(List<String> list, String name) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(THREADS);
        CountDownLatch latch = new CountDownLatch(THREADS);
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < THREADS; i++) {
            final int threadId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < OPERATIONS / THREADS; j++) {
                        String item = name + "-" + threadId + "-" + j;
                        list.add(item);
                        list.contains(item);
                    }
                } finally {
                    latch.countDown();
                }
            });
        }
        
        latch.await();
        executor.shutdown();
        
        return System.currentTimeMillis() - startTime;
    }
    
    private long testQueueOperations(Queue<String> queue, String name) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(THREADS);
        CountDownLatch latch = new CountDownLatch(THREADS);
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < THREADS; i++) {
            final int threadId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < OPERATIONS / THREADS; j++) {
                        String item = name + "-" + threadId + "-" + j;
                        queue.offer(item);
                        queue.poll();
                    }
                } finally {
                    latch.countDown();
                }
            });
        }
        
        latch.await();
        executor.shutdown();
        
        return System.currentTimeMillis() - startTime;
    }
    
    public static void main(String[] args) throws InterruptedException {
        DataStructureSelectionExample example = new DataStructureSelectionExample();
        example.comparePerformance();
    }
}
```

### Real-World Analogy:
Think of concurrent data structure selection like choosing the right type of restaurant for different occasions:
- **Synchronized Collections**: Like a formal restaurant with one waiter per table - slow but very organized
- **Concurrent Collections**: Like a fast-food restaurant with multiple cashiers - fast and efficient
- **Copy-on-Write**: Like a buffet where you get a fresh plate each time - consistent but can be wasteful
- **Blocking Queues**: Like a popular restaurant with a waiting list - you wait but you're guaranteed service

Choose the right "restaurant" based on your "dining needs" (performance requirements)!