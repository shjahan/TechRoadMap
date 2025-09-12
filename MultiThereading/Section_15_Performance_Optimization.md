# Section 15 - Performance Optimization

## 15.1 Performance Fundamentals

Performance optimization in multithreaded applications involves understanding the bottlenecks and optimizing the critical paths. The goal is to maximize throughput while minimizing latency and resource usage.

### Key Performance Metrics:

**1. Throughput:**
- Operations per second
- Data processed per unit time
- System capacity

**2. Latency:**
- Time to complete an operation
- Response time
- User experience

**3. Resource Utilization:**
- CPU usage
- Memory consumption
- I/O efficiency

### Java Example - Performance Fundamentals:

```java
import java.util.concurrent.atomic.AtomicLong;

public class PerformanceFundamentals {
    private final AtomicLong operationCount = new AtomicLong(0);
    private final AtomicLong totalTime = new AtomicLong(0);
    
    public void demonstratePerformanceFundamentals() throws InterruptedException {
        long startTime = System.currentTimeMillis();
        
        // Measure throughput
        measureThroughput();
        
        // Measure latency
        measureLatency();
        
        // Measure resource utilization
        measureResourceUtilization();
        
        long endTime = System.currentTimeMillis();
        long totalDuration = endTime - startTime;
        
        System.out.println("Total operations: " + operationCount.get());
        System.out.println("Total time: " + totalDuration + "ms");
        System.out.println("Throughput: " + (operationCount.get() * 1000.0 / totalDuration) + " ops/sec");
    }
    
    private void measureThroughput() throws InterruptedException {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    operationCount.incrementAndGet();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    private void measureLatency() throws InterruptedException {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                long startTime = System.currentTimeMillis();
                
                // Simulate work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                
                long endTime = System.currentTimeMillis();
                totalTime.addAndGet(endTime - startTime);
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    private void measureResourceUtilization() throws InterruptedException {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                // Simulate CPU-intensive work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        PerformanceFundamentals example = new PerformanceFundamentals();
        example.demonstratePerformanceFundamentals();
    }
}
```

### Real-World Analogy:
Think of performance optimization like optimizing a factory:
- **Throughput**: Like how many products the factory can produce per hour
- **Latency**: Like how long it takes to produce one product
- **Resource Utilization**: Like how efficiently the factory uses its machines and workers

## 15.2 Thread Overhead

Thread overhead refers to the cost of creating, managing, and switching between threads. Understanding this overhead is crucial for optimizing multithreaded applications.

### Key Overhead Sources:

**1. Thread Creation:**
- Memory allocation
- Stack space
- Initialization cost

**2. Context Switching:**
- Saving and restoring state
- CPU time
- Cache misses

**3. Synchronization:**
- Lock acquisition
- Memory barriers
- Contention

### Java Example - Thread Overhead:

```java
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;

public class ThreadOverheadExample {
    public void demonstrateThreadOverhead() throws InterruptedException {
        // Measure thread creation overhead
        measureThreadCreationOverhead();
        
        // Measure context switching overhead
        measureContextSwitchingOverhead();
        
        // Measure synchronization overhead
        measureSynchronizationOverhead();
    }
    
    private void measureThreadCreationOverhead() throws InterruptedException {
        System.out.println("=== Thread Creation Overhead ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[1000];
        for (int i = 0; i < 1000; i++) {
            threads[i] = new Thread(() -> {
                // Minimal work
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Created 1000 threads in " + (endTime - startTime) + "ms");
    }
    
    private void measureContextSwitchingOverhead() throws InterruptedException {
        System.out.println("\n=== Context Switching Overhead ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    // Simulate work
                    Math.sqrt(j);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Context switching test completed in " + (endTime - startTime) + "ms");
    }
    
    private void measureSynchronizationOverhead() throws InterruptedException {
        System.out.println("\n=== Synchronization Overhead ===");
        
        Object lock = new Object();
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        // Minimal work
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Synchronization test completed in " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadOverheadExample example = new ThreadOverheadExample();
        example.demonstrateThreadOverhead();
    }
}
```

## 15.3 Context Switching Costs

Context switching is the process of saving the state of one thread and restoring the state of another. This has significant performance implications.

### Key Costs:

**1. CPU Time:**
- Saving and restoring registers
- Updating memory management
- Cache invalidation

**2. Memory Access:**
- Loading new thread state
- Cache misses
- Memory bandwidth

**3. Cache Effects:**
- Cache pollution
- Reduced cache efficiency
- Performance degradation

### Java Example - Context Switching Costs:

```java
public class ContextSwitchingCostsExample {
    public void demonstrateContextSwitchingCosts() throws InterruptedException {
        // Test with different numbers of threads
        testContextSwitchingCosts(1);
        testContextSwitchingCosts(2);
        testContextSwitchingCosts(4);
        testContextSwitchingCosts(8);
        testContextSwitchingCosts(16);
    }
    
    private void testContextSwitchingCosts(int threadCount) throws InterruptedException {
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                // CPU-intensive work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Thread count: " + threadCount + 
                         ", Time: " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ContextSwitchingCostsExample example = new ContextSwitchingCostsExample();
        example.demonstrateContextSwitchingCosts();
    }
}
```

## 15.4 Lock Contention

Lock contention occurs when multiple threads compete for the same lock, causing performance degradation. Understanding and minimizing contention is crucial for performance.

### Key Contention Sources:

**1. Hot Locks:**
- Frequently accessed locks
- High contention
- Performance bottleneck

**2. Lock Granularity:**
- Too coarse-grained locks
- Unnecessary blocking
- Reduced parallelism

**3. Lock Duration:**
- Long critical sections
- Increased contention
- Reduced throughput

### Java Example - Lock Contention:

```java
import java.util.concurrent.locks.ReentrantLock;

public class LockContentionExample {
    private final ReentrantLock lock = new ReentrantLock();
    private int counter = 0;
    
    public void demonstrateLockContention() throws InterruptedException {
        // Test with different contention levels
        testLockContention(1);
        testLockContention(2);
        testLockContention(4);
        testLockContention(8);
    }
    
    private void testLockContention(int threadCount) throws InterruptedException {
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10000; j++) {
                    lock.lock();
                    try {
                        counter++;
                    } finally {
                        lock.unlock();
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Thread count: " + threadCount + 
                         ", Time: " + (endTime - startTime) + "ms" +
                         ", Counter: " + counter);
    }
    
    public static void main(String[] args) throws InterruptedException {
        LockContentionExample example = new LockContentionExample();
        example.demonstrateLockContention();
    }
}
```

## 15.5 False Sharing

False sharing occurs when multiple threads access different variables that happen to be stored in the same cache line. This can cause significant performance degradation.

### Key Concepts:

**1. Cache Lines:**
- Memory is organized in cache lines
- Typically 64 bytes
- Shared between cores

**2. False Sharing:**
- Different variables in same cache line
- Unnecessary invalidations
- Performance degradation

**3. Prevention:**
- Padding variables
- Cache line alignment
- Separate variables

### Java Example - False Sharing:

```java
public class FalseSharingExample {
    private volatile int counter1 = 0;
    private volatile int counter2 = 0;
    
    // Padded variables to avoid false sharing
    private volatile int paddedCounter1 = 0;
    private volatile long padding1; // Padding
    private volatile int paddedCounter2 = 0;
    private volatile long padding2; // Padding
    
    public void demonstrateFalseSharing() throws InterruptedException {
        // Test with false sharing
        testFalseSharing();
        
        // Test with padding
        testWithPadding();
    }
    
    private void testFalseSharing() throws InterruptedException {
        System.out.println("=== False Sharing Test ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                counter1++;
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                counter2++;
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        long endTime = System.currentTimeMillis();
        System.out.println("False sharing time: " + (endTime - startTime) + "ms");
    }
    
    private void testWithPadding() throws InterruptedException {
        System.out.println("\n=== Padding Test ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                paddedCounter1++;
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                paddedCounter2++;
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        long endTime = System.currentTimeMillis();
        System.out.println("Padding time: " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        FalseSharingExample example = new FalseSharingExample();
        example.demonstrateFalseSharing();
    }
}
```

## 15.6 Cache Efficiency

Cache efficiency is crucial for performance in multithreaded applications. Understanding cache behavior helps optimize memory access patterns.

### Key Concepts:

**1. Cache Hierarchy:**
- L1, L2, L3 caches
- Different sizes and speeds
- Cache coherence

**2. Locality:**
- Temporal locality
- Spatial locality
- Better cache utilization

**3. Cache Misses:**
- Compulsory misses
- Capacity misses
- Conflict misses

### Java Example - Cache Efficiency:

```java
public class CacheEfficiencyExample {
    private static final int ARRAY_SIZE = 1000000;
    private int[] array = new int[ARRAY_SIZE];
    
    public void demonstrateCacheEfficiency() throws InterruptedException {
        // Initialize array
        for (int i = 0; i < ARRAY_SIZE; i++) {
            array[i] = i;
        }
        
        // Test sequential access
        testSequentialAccess();
        
        // Test random access
        testRandomAccess();
        
        // Test cache-friendly access
        testCacheFriendlyAccess();
    }
    
    private void testSequentialAccess() throws InterruptedException {
        System.out.println("=== Sequential Access ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                int start = threadId * (ARRAY_SIZE / 4);
                int end = start + (ARRAY_SIZE / 4);
                
                long sum = 0;
                for (int j = start; j < end; j++) {
                    sum += array[j];
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Sequential access time: " + (endTime - startTime) + "ms");
    }
    
    private void testRandomAccess() throws InterruptedException {
        System.out.println("\n=== Random Access ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                long sum = 0;
                for (int j = 0; j < ARRAY_SIZE / 4; j++) {
                    int index = (int) (Math.random() * ARRAY_SIZE);
                    sum += array[index];
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Random access time: " + (endTime - startTime) + "ms");
    }
    
    private void testCacheFriendlyAccess() throws InterruptedException {
        System.out.println("\n=== Cache-Friendly Access ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                int start = threadId * (ARRAY_SIZE / 4);
                int end = start + (ARRAY_SIZE / 4);
                
                // Process in chunks for better cache utilization
                int chunkSize = 64; // Cache line size
                for (int j = start; j < end; j += chunkSize) {
                    int chunkEnd = Math.min(j + chunkSize, end);
                    for (int k = j; k < chunkEnd; k++) {
                        array[k] = array[k] * 2;
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Cache-friendly access time: " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        CacheEfficiencyExample example = new CacheEfficiencyExample();
        example.demonstrateCacheEfficiency();
    }
}
```

## 15.7 NUMA Awareness

NUMA (Non-Uniform Memory Access) awareness is important for performance in multi-socket systems. Understanding NUMA topology helps optimize memory access patterns.

### Key Concepts:

**1. NUMA Nodes:**
- Each socket has its own memory
- Local vs remote memory access
- Different access latencies

**2. Memory Affinity:**
- Keep data and threads on same node
- Reduce remote memory access
- Better performance

**3. Load Balancing:**
- Balance load across NUMA nodes
- Prevent node overload
- Better scalability

### Java Example - NUMA Awareness:

```java
public class NUMAwarenessExample {
    public void demonstrateNUMAwareness() throws InterruptedException {
        // Get system information
        int processors = Runtime.getRuntime().availableProcessors();
        System.out.println("Number of processors: " + processors);
        
        // Test NUMA-aware allocation
        testNUMAwareAllocation();
        
        // Test NUMA-aware threading
        testNUMAwareThreading();
    }
    
    private void testNUMAwareAllocation() throws InterruptedException {
        System.out.println("=== NUMA-Aware Allocation ===");
        
        long startTime = System.currentTimeMillis();
        
        // Allocate memory in chunks
        int chunkSize = 1024 * 1024; // 1MB chunks
        int numChunks = 100;
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                // Allocate memory for this thread
                int[] localArray = new int[chunkSize];
                
                // Initialize array
                for (int j = 0; j < chunkSize; j++) {
                    localArray[j] = j;
                }
                
                // Process array
                long sum = 0;
                for (int j = 0; j < chunkSize; j++) {
                    sum += localArray[j];
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("NUMA-aware allocation time: " + (endTime - startTime) + "ms");
    }
    
    private void testNUMAwareThreading() throws InterruptedException {
        System.out.println("\n=== NUMA-Aware Threading ===");
        
        long startTime = System.currentTimeMillis();
        
        // Create threads for each processor
        Thread[] threads = new Thread[Runtime.getRuntime().availableProcessors()];
        for (int i = 0; i < threads.length; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                // Allocate local memory
                int[] localArray = new int[1000000];
                
                // Initialize and process
                for (int j = 0; j < localArray.length; j++) {
                    localArray[j] = j;
                }
                
                long sum = 0;
                for (int j = 0; j < localArray.length; j++) {
                    sum += localArray[j];
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("NUMA-aware threading time: " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        NUMAwarenessExample example = new NUMAwarenessExample();
        example.demonstrateNUMAwareness();
    }
}
```

## 15.8 Performance Profiling

Performance profiling helps identify bottlenecks and optimize multithreaded applications. Understanding profiling tools and techniques is crucial for performance optimization.

### Key Profiling Techniques:

**1. CPU Profiling:**
- Identify CPU hotspots
- Find performance bottlenecks
- Optimize critical paths

**2. Memory Profiling:**
- Identify memory leaks
- Optimize memory usage
- Reduce garbage collection

**3. Thread Profiling:**
- Analyze thread behavior
- Identify contention
- Optimize synchronization

### Java Example - Performance Profiling:

```java
import java.util.concurrent.atomic.AtomicLong;

public class PerformanceProfilingExample {
    private final AtomicLong operationCount = new AtomicLong(0);
    private final AtomicLong totalTime = new AtomicLong(0);
    
    public void demonstratePerformanceProfiling() throws InterruptedException {
        // Profile CPU usage
        profileCPUUsage();
        
        // Profile memory usage
        profileMemoryUsage();
        
        // Profile thread behavior
        profileThreadBehavior();
    }
    
    private void profileCPUUsage() throws InterruptedException {
        System.out.println("=== CPU Profiling ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                long threadStartTime = System.currentTimeMillis();
                
                // CPU-intensive work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                
                long threadEndTime = System.currentTimeMillis();
                totalTime.addAndGet(threadEndTime - threadStartTime);
                operationCount.incrementAndGet();
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("CPU profiling completed in " + (endTime - startTime) + "ms");
        System.out.println("Operations: " + operationCount.get());
        System.out.println("Total time: " + totalTime.get() + "ms");
    }
    
    private void profileMemoryUsage() throws InterruptedException {
        System.out.println("\n=== Memory Profiling ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                // Allocate memory
                int[] array = new int[1000000];
                
                // Process array
                for (int j = 0; j < array.length; j++) {
                    array[j] = j;
                }
                
                // Simulate work
                long sum = 0;
                for (int j = 0; j < array.length; j++) {
                    sum += array[j];
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Memory profiling completed in " + (endTime - startTime) + "ms");
    }
    
    private void profileThreadBehavior() throws InterruptedException {
        System.out.println("\n=== Thread Profiling ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + threadId + " started");
                
                // Simulate work
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Thread " + threadId + " completed");
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Thread profiling completed in " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        PerformanceProfilingExample example = new PerformanceProfilingExample();
        example.demonstratePerformanceProfiling();
    }
}
```

## 15.9 Performance Testing

Performance testing is essential for validating optimizations and ensuring consistent performance under various conditions.

### Key Testing Strategies:

**1. Load Testing:**
- Test under normal load
- Identify performance limits
- Validate optimizations

**2. Stress Testing:**
- Test under high load
- Find breaking points
- Validate stability

**3. Benchmarking:**
- Compare different implementations
- Measure performance improvements
- Validate optimizations

### Java Example - Performance Testing:

```java
import java.util.concurrent.atomic.AtomicLong;

public class PerformanceTestingExample {
    private final AtomicLong operationCount = new AtomicLong(0);
    
    public void demonstratePerformanceTesting() throws InterruptedException {
        // Load testing
        performLoadTest();
        
        // Stress testing
        performStressTest();
        
        // Benchmarking
        performBenchmarking();
    }
    
    private void performLoadTest() throws InterruptedException {
        System.out.println("=== Load Testing ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    operationCount.incrementAndGet();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Load test completed in " + (endTime - startTime) + "ms");
        System.out.println("Operations: " + operationCount.get());
    }
    
    private void performStressTest() throws InterruptedException {
        System.out.println("\n=== Stress Testing ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[20];
        for (int i = 0; i < 20; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10000; j++) {
                    operationCount.incrementAndGet();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Stress test completed in " + (endTime - startTime) + "ms");
        System.out.println("Operations: " + operationCount.get());
    }
    
    private void performBenchmarking() throws InterruptedException {
        System.out.println("\n=== Benchmarking ===");
        
        // Test different implementations
        long time1 = benchmarkImplementation1();
        long time2 = benchmarkImplementation2();
        
        System.out.println("Implementation 1 time: " + time1 + "ms");
        System.out.println("Implementation 2 time: " + time2 + "ms");
        System.out.println("Performance improvement: " + 
                         ((double)(time1 - time2) / time1 * 100) + "%");
    }
    
    private long benchmarkImplementation1() throws InterruptedException {
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000000; j++) {
                    // Implementation 1
                    Math.sqrt(j);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        return System.currentTimeMillis() - startTime;
    }
    
    private long benchmarkImplementation2() throws InterruptedException {
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000000; j++) {
                    // Implementation 2
                    Math.pow(j, 0.5);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        return System.currentTimeMillis() - startTime;
    }
    
    public static void main(String[] args) throws InterruptedException {
        PerformanceTestingExample example = new PerformanceTestingExample();
        example.demonstratePerformanceTesting();
    }
}
```

## 15.10 Performance Best Practices

Following best practices ensures optimal performance in multithreaded applications.

### Best Practices:

**1. Minimize Lock Contention:**
- Use fine-grained locks
- Reduce lock duration
- Avoid hot locks

**2. Optimize Memory Access:**
- Improve cache locality
- Avoid false sharing
- Use appropriate data structures

**3. Monitor Performance:**
- Use profiling tools
- Monitor key metrics
- Continuously optimize

### Java Example - Performance Best Practices:

```java
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

public class PerformanceBestPracticesExample {
    private final AtomicLong counter = new AtomicLong(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateBestPractices() throws InterruptedException {
        // Practice 1: Minimize lock contention
        demonstrateMinimizeLockContention();
        
        // Practice 2: Optimize memory access
        demonstrateOptimizeMemoryAccess();
        
        // Practice 3: Monitor performance
        demonstrateMonitorPerformance();
    }
    
    private void demonstrateMinimizeLockContention() throws InterruptedException {
        System.out.println("=== Minimize Lock Contention ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10000; j++) {
                    // Use atomic operations instead of locks
                    counter.incrementAndGet();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Minimized lock contention time: " + (endTime - startTime) + "ms");
    }
    
    private void demonstrateOptimizeMemoryAccess() throws InterruptedException {
        System.out.println("\n=== Optimize Memory Access ===");
        
        long startTime = System.currentTimeMillis();
        
        // Use cache-friendly data structures
        int[] array = new int[1000000];
        for (int i = 0; i < array.length; i++) {
            array[i] = i;
        }
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                int start = threadId * (array.length / 4);
                int end = start + (array.length / 4);
                
                // Sequential access for better cache utilization
                long sum = 0;
                for (int j = start; j < end; j++) {
                    sum += array[j];
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Optimized memory access time: " + (endTime - startTime) + "ms");
    }
    
    private void demonstrateMonitorPerformance() throws InterruptedException {
        System.out.println("\n=== Monitor Performance ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < 4; i++) {
            threads[i] = new Thread(() -> {
                long threadStartTime = System.currentTimeMillis();
                
                // Simulate work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                
                long threadEndTime = System.currentTimeMillis();
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " completed in " + (threadEndTime - threadStartTime) + "ms");
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Performance monitoring completed in " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        PerformanceBestPracticesExample example = new PerformanceBestPracticesExample();
        example.demonstrateBestPractices();
    }
}
```

### Real-World Analogy:
Think of performance optimization like optimizing a busy restaurant:
- **Thread Overhead**: Like the cost of hiring and training new staff
- **Context Switching**: Like switching between different cooking stations
- **Lock Contention**: Like multiple chefs trying to use the same stove
- **False Sharing**: Like two chefs working on different dishes but sharing the same workspace
- **Cache Efficiency**: Like organizing ingredients so they're easy to reach
- **NUMA Awareness**: Like keeping ingredients close to where they'll be used
- **Performance Profiling**: Like analyzing which parts of the kitchen are bottlenecks
- **Performance Testing**: Like stress-testing the kitchen during peak hours

The key is to identify bottlenecks and optimize the critical paths for maximum efficiency!