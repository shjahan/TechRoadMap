# Section 18 - Concurrency Debugging

## 18.1 Debugging Fundamentals

Debugging concurrent programs is significantly more challenging than debugging sequential programs due to the non-deterministic nature of concurrent execution. Understanding the fundamentals is crucial for effective debugging.

### Key Challenges:

**1. Non-Deterministic Behavior:**
- Thread execution order varies
- Timing-dependent bugs
- Race conditions

**2. Reproducibility:**
- Bugs may not occur consistently
- Different behavior on different systems
- Timing-sensitive issues

**3. Complexity:**
- Multiple execution paths
- Complex interactions
- State dependencies

### Java Example - Debugging Fundamentals:

```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class DebuggingFundamentalsExample {
    private int counter = 0;
    private final AtomicInteger atomicCounter = new AtomicInteger(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateDebuggingChallenges() throws InterruptedException {
        System.out.println("=== Debugging Challenges ===");
        
        // Challenge 1: Race conditions
        testRaceCondition();
        
        // Challenge 2: Deadlocks
        testDeadlock();
        
        // Challenge 3: Livelocks
        testLivelock();
    }
    
    private void testRaceCondition() throws InterruptedException {
        System.out.println("\n--- Race Condition Test ---");
        counter = 0;
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter++; // Race condition!
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Expected: 5000, Actual: " + counter);
        System.out.println("Race condition detected: " + (counter != 5000));
    }
    
    private void testDeadlock() throws InterruptedException {
        System.out.println("\n--- Deadlock Test ---");
        
        Object lock1 = new Object();
        Object lock2 = new Object();
        
        Thread thread1 = new Thread(() -> {
            synchronized (lock1) {
                System.out.println("Thread 1 acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock2) {
                    System.out.println("Thread 1 acquired lock2");
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            synchronized (lock2) {
                System.out.println("Thread 2 acquired lock2");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock1) {
                    System.out.println("Thread 2 acquired lock1");
                }
            }
        });
        
        thread1.start();
        thread2.start();
        
        // Wait with timeout to detect deadlock
        thread1.join(5000);
        thread2.join(5000);
        
        System.out.println("Deadlock test completed");
    }
    
    private void testLivelock() throws InterruptedException {
        System.out.println("\n--- Livelock Test ---");
        
        AtomicInteger attempts = new AtomicInteger(0);
        Object lock1 = new Object();
        Object lock2 = new Object();
        
        Thread thread1 = new Thread(() -> {
            while (attempts.get() < 10) {
                synchronized (lock1) {
                    System.out.println("Thread 1 trying lock2");
                    if (Thread.holdsLock(lock2)) {
                        System.out.println("Thread 1 livelock detected");
                        break;
                    }
                    attempts.incrementAndGet();
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            while (attempts.get() < 10) {
                synchronized (lock2) {
                    System.out.println("Thread 2 trying lock1");
                    if (Thread.holdsLock(lock1)) {
                        System.out.println("Thread 2 livelock detected");
                        break;
                    }
                    attempts.incrementAndGet();
                }
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        System.out.println("Livelock test completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        DebuggingFundamentalsExample example = new DebuggingFundamentalsExample();
        example.demonstrateDebuggingChallenges();
    }
}
```

## 18.2 Thread Dumps

Thread dumps are snapshots of all threads in a Java application at a specific point in time. They are essential for debugging concurrency issues, especially deadlocks and performance problems.

### Key Information:

**1. Thread States:**
- RUNNABLE: Thread is executing
- BLOCKED: Thread is waiting for a lock
- WAITING: Thread is waiting indefinitely
- TIMED_WAITING: Thread is waiting with timeout
- TERMINATED: Thread has finished

**2. Stack Traces:**
- Method call stack
- Line numbers
- Class and method names

**3. Lock Information:**
- Locked monitors
- Waiting for locks
- Lock ownership

### Java Example - Thread Dumps:

```java
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.CountDownLatch;

public class ThreadDumpExample {
    private final ReentrantLock lock1 = new ReentrantLock();
    private final ReentrantLock lock2 = new ReentrantLock();
    private final CountDownLatch latch = new CountDownLatch(2);
    
    public void demonstrateThreadDumps() throws InterruptedException {
        System.out.println("=== Thread Dump Example ===");
        
        // Create threads that will cause deadlock
        Thread thread1 = new Thread(() -> {
            lock1.lock();
            try {
                System.out.println("Thread 1 acquired lock1");
                Thread.sleep(1000);
                lock2.lock();
                try {
                    System.out.println("Thread 1 acquired lock2");
                } finally {
                    lock2.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock1.unlock();
            }
            latch.countDown();
        });
        
        Thread thread2 = new Thread(() -> {
            lock2.lock();
            try {
                System.out.println("Thread 2 acquired lock2");
                Thread.sleep(1000);
                lock1.lock();
                try {
                    System.out.println("Thread 2 acquired lock1");
                } finally {
                    lock1.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock2.unlock();
            }
            latch.countDown();
        });
        
        thread1.start();
        thread2.start();
        
        // Wait a bit for deadlock to occur
        Thread.sleep(2000);
        
        // Generate thread dump
        generateThreadDump();
        
        // Wait for threads to complete
        latch.await();
    }
    
    private void generateThreadDump() {
        System.out.println("\n=== Thread Dump ===");
        
        Thread.getAllStackTraces().forEach((thread, stackTrace) -> {
            System.out.println("\nThread: " + thread.getName());
            System.out.println("State: " + thread.getState());
            System.out.println("Priority: " + thread.getPriority());
            System.out.println("Daemon: " + thread.isDaemon());
            
            if (stackTrace.length > 0) {
                System.out.println("Stack Trace:");
                for (StackTraceElement element : stackTrace) {
                    System.out.println("  " + element.toString());
                }
            }
        });
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadDumpExample example = new ThreadDumpExample();
        example.demonstrateThreadDumps();
    }
}
```

## 18.3 Logging and Tracing

Logging and tracing are essential for debugging concurrent applications. They help track execution flow, identify timing issues, and understand thread interactions.

### Key Techniques:

**1. Thread Identification:**
- Log thread names and IDs
- Track thread creation and termination
- Monitor thread state changes

**2. Timing Information:**
- Log timestamps
- Measure execution time
- Track delays and timeouts

**3. State Tracking:**
- Log variable values
- Track state changes
- Monitor lock acquisition

### Java Example - Logging and Tracing:

```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;
import java.util.logging.Logger;
import java.util.logging.Level;

public class LoggingTracingExample {
    private static final Logger logger = Logger.getLogger(LoggingTracingExample.class.getName());
    private final AtomicInteger counter = new AtomicInteger(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateLoggingTracing() throws InterruptedException {
        logger.info("Starting logging and tracing demonstration");
        
        // Test with logging
        testWithLogging();
        
        // Test with tracing
        testWithTracing();
    }
    
    private void testWithLogging() throws InterruptedException {
        logger.info("=== Logging Test ===");
        
        Thread[] threads = new Thread[3];
        for (int i = 0; i < 3; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                logger.info("Thread " + threadId + " started");
                
                for (int j = 0; j < 5; j++) {
                    logger.fine("Thread " + threadId + " iteration " + j);
                    
                    lock.lock();
                    try {
                        int currentValue = counter.get();
                        logger.info("Thread " + threadId + " read counter: " + currentValue);
                        
                        Thread.sleep(100); // Simulate work
                        
                        counter.incrementAndGet();
                        logger.info("Thread " + threadId + " incremented counter to: " + counter.get());
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        logger.warning("Thread " + threadId + " interrupted");
                    } finally {
                        lock.unlock();
                        logger.fine("Thread " + threadId + " released lock");
                    }
                }
                
                logger.info("Thread " + threadId + " completed");
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        logger.info("Final counter value: " + counter.get());
    }
    
    private void testWithTracing() throws InterruptedException {
        logger.info("=== Tracing Test ===");
        
        Thread[] threads = new Thread[3];
        for (int i = 0; i < 3; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                long startTime = System.currentTimeMillis();
                logger.info("Thread " + threadId + " started at " + startTime);
                
                for (int j = 0; j < 5; j++) {
                    long iterationStart = System.currentTimeMillis();
                    logger.fine("Thread " + threadId + " iteration " + j + " started at " + iterationStart);
                    
                    // Simulate work
                    try {
                        Thread.sleep(50);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        logger.warning("Thread " + threadId + " interrupted during iteration " + j);
                        break;
                    }
                    
                    long iterationEnd = System.currentTimeMillis();
                    logger.fine("Thread " + threadId + " iteration " + j + " completed in " + 
                              (iterationEnd - iterationStart) + "ms");
                }
                
                long endTime = System.currentTimeMillis();
                logger.info("Thread " + threadId + " completed in " + (endTime - startTime) + "ms");
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        logger.info("Tracing test completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Set logging level
        Logger.getLogger(LoggingTracingExample.class.getName()).setLevel(Level.ALL);
        
        LoggingTracingExample example = new LoggingTracingExample();
        example.demonstrateLoggingTracing();
    }
}
```

## 18.4 Profiling Tools

Profiling tools help identify performance bottlenecks, memory leaks, and concurrency issues in Java applications. They provide detailed insights into application behavior.

### Key Tools:

**1. JProfiler:**
- CPU profiling
- Memory profiling
- Thread profiling

**2. VisualVM:**
- Free profiling tool
- Thread monitoring
- Memory analysis

**3. JConsole:**
- Built-in monitoring
- Thread information
- Memory usage

### Java Example - Profiling Tools:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

public class ProfilingToolsExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    private final AtomicLong operationCount = new AtomicLong(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateProfilingTools() throws InterruptedException {
        System.out.println("=== Profiling Tools Example ===");
        
        // CPU-intensive work
        testCPUIntensiveWork();
        
        // Memory-intensive work
        testMemoryIntensiveWork();
        
        // Thread-intensive work
        testThreadIntensiveWork();
        
        executor.shutdown();
    }
    
    private void testCPUIntensiveWork() throws InterruptedException {
        System.out.println("\n--- CPU-Intensive Work ---");
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                operationCount.incrementAndGet();
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 10) {
            Thread.sleep(100);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("CPU-intensive work completed in " + (endTime - startTime) + "ms");
    }
    
    private void testMemoryIntensiveWork() throws InterruptedException {
        System.out.println("\n--- Memory-Intensive Work ---");
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 5; i++) {
            executor.submit(() -> {
                // Allocate large arrays
                int[] array1 = new int[1000000];
                int[] array2 = new int[1000000];
                
                // Process arrays
                for (int j = 0; j < array1.length; j++) {
                    array1[j] = j;
                    array2[j] = j * 2;
                }
                
                // Simulate work
                long sum = 0;
                for (int j = 0; j < array1.length; j++) {
                    sum += array1[j] + array2[j];
                }
                
                operationCount.incrementAndGet();
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 15) {
            Thread.sleep(100);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Memory-intensive work completed in " + (endTime - startTime) + "ms");
    }
    
    private void testThreadIntensiveWork() throws InterruptedException {
        System.out.println("\n--- Thread-Intensive Work ---");
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 20; i++) {
            executor.submit(() -> {
                lock.lock();
                try {
                    // Simulate work
                    Thread.sleep(100);
                    operationCount.incrementAndGet();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    lock.unlock();
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 35) {
            Thread.sleep(100);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Thread-intensive work completed in " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ProfilingToolsExample example = new ProfilingToolsExample();
        example.demonstrateProfilingTools();
    }
}
```

## 18.5 Deadlock Detection

Deadlock detection is crucial for identifying and resolving deadlock situations. Various techniques and tools can help detect deadlocks in Java applications.

### Key Techniques:

**1. Lock Ordering:**
- Always acquire locks in the same order
- Prevent circular wait conditions
- Use timeout mechanisms

**2. Deadlock Detection:**
- Monitor lock acquisition
- Detect circular dependencies
- Use deadlock detection tools

**3. Prevention Strategies:**
- Avoid nested locks
- Use tryLock with timeout
- Implement lock hierarchy

### Java Example - Deadlock Detection:

```java
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

public class DeadlockDetectionExample {
    private final ReentrantLock lock1 = new ReentrantLock();
    private final ReentrantLock lock2 = new ReentrantLock();
    private final AtomicBoolean deadlockDetected = new AtomicBoolean(false);
    
    public void demonstrateDeadlockDetection() throws InterruptedException {
        System.out.println("=== Deadlock Detection Example ===");
        
        // Test deadlock scenario
        testDeadlockScenario();
        
        // Test deadlock prevention
        testDeadlockPrevention();
        
        // Test deadlock detection
        testDeadlockDetection();
    }
    
    private void testDeadlockScenario() throws InterruptedException {
        System.out.println("\n--- Deadlock Scenario ---");
        
        Thread thread1 = new Thread(() -> {
            lock1.lock();
            try {
                System.out.println("Thread 1 acquired lock1");
                Thread.sleep(1000);
                
                if (lock2.tryLock(1000, TimeUnit.MILLISECONDS)) {
                    try {
                        System.out.println("Thread 1 acquired lock2");
                    } finally {
                        lock2.unlock();
                    }
                } else {
                    System.out.println("Thread 1 failed to acquire lock2 - potential deadlock");
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock1.unlock();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            lock2.lock();
            try {
                System.out.println("Thread 2 acquired lock2");
                Thread.sleep(1000);
                
                if (lock1.tryLock(1000, TimeUnit.MILLISECONDS)) {
                    try {
                        System.out.println("Thread 2 acquired lock1");
                    } finally {
                        lock1.unlock();
                    }
                } else {
                    System.out.println("Thread 2 failed to acquire lock1 - potential deadlock");
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock2.unlock();
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
    
    private void testDeadlockPrevention() throws InterruptedException {
        System.out.println("\n--- Deadlock Prevention ---");
        
        Thread thread1 = new Thread(() -> {
            // Always acquire locks in the same order
            lock1.lock();
            try {
                System.out.println("Thread 1 acquired lock1");
                Thread.sleep(1000);
                
                lock2.lock();
                try {
                    System.out.println("Thread 1 acquired lock2");
                } finally {
                    lock2.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock1.unlock();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            // Always acquire locks in the same order
            lock1.lock();
            try {
                System.out.println("Thread 2 acquired lock1");
                Thread.sleep(1000);
                
                lock2.lock();
                try {
                    System.out.println("Thread 2 acquired lock2");
                } finally {
                    lock2.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock1.unlock();
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
    
    private void testDeadlockDetection() throws InterruptedException {
        System.out.println("\n--- Deadlock Detection ---");
        
        Thread thread1 = new Thread(() -> {
            lock1.lock();
            try {
                System.out.println("Thread 1 acquired lock1");
                Thread.sleep(1000);
                
                if (lock2.tryLock(1000, TimeUnit.MILLISECONDS)) {
                    try {
                        System.out.println("Thread 1 acquired lock2");
                    } finally {
                        lock2.unlock();
                    }
                } else {
                    System.out.println("Thread 1 detected potential deadlock");
                    deadlockDetected.set(true);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock1.unlock();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            lock2.lock();
            try {
                System.out.println("Thread 2 acquired lock2");
                Thread.sleep(1000);
                
                if (lock1.tryLock(1000, TimeUnit.MILLISECONDS)) {
                    try {
                        System.out.println("Thread 2 acquired lock1");
                    } finally {
                        lock1.unlock();
                    }
                } else {
                    System.out.println("Thread 2 detected potential deadlock");
                    deadlockDetected.set(true);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                lock2.unlock();
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        System.out.println("Deadlock detected: " + deadlockDetected.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        DeadlockDetectionExample example = new DeadlockDetectionExample();
        example.demonstrateDeadlockDetection();
    }
}
```

## 18.6 Memory Leak Detection

Memory leaks in concurrent applications can be particularly problematic. They can cause performance degradation, out-of-memory errors, and system instability.

### Key Techniques:

**1. Memory Monitoring:**
- Track memory usage
- Monitor garbage collection
- Identify memory growth patterns

**2. Leak Detection:**
- Use profiling tools
- Analyze heap dumps
- Track object references

**3. Prevention:**
- Proper resource cleanup
- Avoid circular references
- Use weak references

### Java Example - Memory Leak Detection:

```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.WeakHashMap;
import java.util.Map;

public class MemoryLeakDetectionExample {
    private final Map<String, Object> memoryLeakMap = new ConcurrentHashMap<>();
    private final Map<String, Object> properMap = new WeakHashMap<>();
    private final AtomicLong objectCount = new AtomicLong(0);
    
    public void demonstrateMemoryLeakDetection() throws InterruptedException {
        System.out.println("=== Memory Leak Detection Example ===");
        
        // Test memory leak scenario
        testMemoryLeak();
        
        // Test proper memory management
        testProperMemoryManagement();
        
        // Test weak references
        testWeakReferences();
    }
    
    private void testMemoryLeak() throws InterruptedException {
        System.out.println("\n--- Memory Leak Test ---");
        
        long startMemory = getUsedMemory();
        
        // Create objects that will cause memory leak
        for (int i = 0; i < 1000; i++) {
            String key = "key" + i;
            Object value = new Object();
            memoryLeakMap.put(key, value);
            objectCount.incrementAndGet();
        }
        
        long endMemory = getUsedMemory();
        System.out.println("Memory used: " + (endMemory - startMemory) + " bytes");
        System.out.println("Objects created: " + objectCount.get());
        
        // Clear references but objects remain in map
        System.gc();
        Thread.sleep(1000);
        
        long afterGCMemory = getUsedMemory();
        System.out.println("Memory after GC: " + (afterGCMemory - startMemory) + " bytes");
        System.out.println("Memory leak detected: " + (afterGCMemory > endMemory));
    }
    
    private void testProperMemoryManagement() throws InterruptedException {
        System.out.println("\n--- Proper Memory Management Test ---");
        
        long startMemory = getUsedMemory();
        
        // Create objects with proper cleanup
        for (int i = 0; i < 1000; i++) {
            String key = "key" + i;
            Object value = new Object();
            properMap.put(key, value);
        }
        
        long endMemory = getUsedMemory();
        System.out.println("Memory used: " + (endMemory - startMemory) + " bytes");
        
        // Clear references
        properMap.clear();
        System.gc();
        Thread.sleep(1000);
        
        long afterGCMemory = getUsedMemory();
        System.out.println("Memory after GC: " + (afterGCMemory - startMemory) + " bytes");
        System.out.println("Memory properly managed: " + (afterGCMemory < endMemory));
    }
    
    private void testWeakReferences() throws InterruptedException {
        System.out.println("\n--- Weak References Test ---");
        
        long startMemory = getUsedMemory();
        
        // Create objects with weak references
        for (int i = 0; i < 1000; i++) {
            String key = "key" + i;
            Object value = new Object();
            properMap.put(key, value);
        }
        
        long endMemory = getUsedMemory();
        System.out.println("Memory used: " + (endMemory - startMemory) + " bytes");
        
        // Clear strong references
        System.gc();
        Thread.sleep(1000);
        
        long afterGCMemory = getUsedMemory();
        System.out.println("Memory after GC: " + (afterGCMemory - startMemory) + " bytes");
        System.out.println("Weak references working: " + (afterGCMemory < endMemory));
    }
    
    private long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
    
    public static void main(String[] args) throws InterruptedException {
        MemoryLeakDetectionExample example = new MemoryLeakDetectionExample();
        example.demonstrateMemoryLeakDetection();
    }
}
```

## 18.7 Performance Debugging

Performance debugging in concurrent applications involves identifying bottlenecks, optimizing critical paths, and ensuring efficient resource utilization.

### Key Techniques:

**1. Profiling:**
- CPU profiling
- Memory profiling
- Thread profiling

**2. Bottleneck Identification:**
- Identify slow operations
- Find contention points
- Analyze resource usage

**3. Optimization:**
- Optimize critical paths
- Reduce contention
- Improve resource utilization

### Java Example - Performance Debugging:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

public class PerformanceDebuggingExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    private final AtomicLong operationCount = new AtomicLong(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstratePerformanceDebugging() throws InterruptedException {
        System.out.println("=== Performance Debugging Example ===");
        
        // Test performance with different configurations
        testPerformanceWithLocking();
        testPerformanceWithoutLocking();
        testPerformanceWithAtomicOperations();
        
        executor.shutdown();
    }
    
    private void testPerformanceWithLocking() throws InterruptedException {
        System.out.println("\n--- Performance with Locking ---");
        
        long startTime = System.currentTimeMillis();
        operationCount.set(0);
        
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    lock.lock();
                    try {
                        operationCount.incrementAndGet();
                    } finally {
                        lock.unlock();
                    }
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 10000) {
            Thread.sleep(10);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Locking performance: " + (endTime - startTime) + "ms");
    }
    
    private void testPerformanceWithoutLocking() throws InterruptedException {
        System.out.println("\n--- Performance without Locking ---");
        
        long startTime = System.currentTimeMillis();
        operationCount.set(0);
        
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    operationCount.incrementAndGet();
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 20000) {
            Thread.sleep(10);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("No locking performance: " + (endTime - startTime) + "ms");
    }
    
    private void testPerformanceWithAtomicOperations() throws InterruptedException {
        System.out.println("\n--- Performance with Atomic Operations ---");
        
        long startTime = System.currentTimeMillis();
        operationCount.set(0);
        
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    operationCount.incrementAndGet();
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 30000) {
            Thread.sleep(10);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Atomic operations performance: " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        PerformanceDebuggingExample example = new PerformanceDebuggingExample();
        example.demonstratePerformanceDebugging();
    }
}
```

## 18.8 Debugging Tools

Various debugging tools are available for Java concurrent applications. These tools help identify issues, monitor performance, and analyze application behavior.

### Key Tools:

**1. IDE Debuggers:**
- IntelliJ IDEA
- Eclipse
- Visual Studio Code

**2. Profiling Tools:**
- JProfiler
- VisualVM
- JConsole

**3. Monitoring Tools:**
- JMC (Java Mission Control)
- JFR (Java Flight Recorder)
- APM tools

### Java Example - Debugging Tools:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;

public class DebuggingToolsExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(5);
    private final AtomicLong operationCount = new AtomicLong(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateDebuggingTools() throws InterruptedException {
        System.out.println("=== Debugging Tools Example ===");
        
        // Test with different scenarios
        testNormalOperation();
        testErrorScenario();
        testPerformanceScenario();
        
        executor.shutdown();
    }
    
    private void testNormalOperation() throws InterruptedException {
        System.out.println("\n--- Normal Operation ---");
        
        for (int i = 0; i < 5; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    lock.lock();
                    try {
                        operationCount.incrementAndGet();
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } finally {
                        lock.unlock();
                    }
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 500) {
            Thread.sleep(100);
        }
        
        System.out.println("Normal operation completed");
    }
    
    private void testErrorScenario() throws InterruptedException {
        System.out.println("\n--- Error Scenario ---");
        
        for (int i = 0; i < 5; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    try {
                        lock.lock();
                        operationCount.incrementAndGet();
                        
                        // Simulate occasional errors
                        if (Math.random() < 0.1) {
                            throw new RuntimeException("Simulated error");
                        }
                        
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } catch (RuntimeException e) {
                        System.err.println("Error in thread: " + e.getMessage());
                    } finally {
                        if (lock.isHeldByCurrentThread()) {
                            lock.unlock();
                        }
                    }
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 1000) {
            Thread.sleep(100);
        }
        
        System.out.println("Error scenario completed");
    }
    
    private void testPerformanceScenario() throws InterruptedException {
        System.out.println("\n--- Performance Scenario ---");
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < 5; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    lock.lock();
                    try {
                        operationCount.incrementAndGet();
                        Thread.sleep(5);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } finally {
                        lock.unlock();
                    }
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 1500) {
            Thread.sleep(100);
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Performance scenario completed in " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        DebuggingToolsExample example = new DebuggingToolsExample();
        example.demonstrateDebuggingTools();
    }
}
```

## 18.9 Debugging Best Practices

Following best practices ensures effective debugging of concurrent applications. It helps maintain code quality and reduces debugging effort.

### Best Practices:

**1. Prevention:**
- Design for testability
- Use defensive programming
- Implement proper error handling

**2. Monitoring:**
- Add comprehensive logging
- Monitor key metrics
- Use profiling tools

**3. Testing:**
- Write comprehensive tests
- Test edge cases
- Use stress testing

### Java Example - Debugging Best Practices:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;
import java.util.logging.Logger;
import java.util.logging.Level;

public class DebuggingBestPracticesExample {
    private static final Logger logger = Logger.getLogger(DebuggingBestPracticesExample.class.getName());
    private final ExecutorService executor = Executors.newFixedThreadPool(5);
    private final AtomicLong operationCount = new AtomicLong(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateBestPractices() throws InterruptedException {
        logger.info("Starting debugging best practices demonstration");
        
        // Test with best practices
        testWithBestPractices();
        
        executor.shutdown();
    }
    
    private void testWithBestPractices() throws InterruptedException {
        logger.info("=== Best Practices Test ===");
        
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            executor.submit(() -> {
                logger.info("Thread " + threadId + " started");
                
                try {
                    for (int j = 0; j < 100; j++) {
                        performOperation(threadId, j);
                    }
                    logger.info("Thread " + threadId + " completed successfully");
                } catch (Exception e) {
                    logger.log(Level.SEVERE, "Thread " + threadId + " failed", e);
                }
            });
        }
        
        // Wait for completion
        while (operationCount.get() < 500) {
            Thread.sleep(100);
        }
        
        logger.info("Best practices test completed");
    }
    
    private void performOperation(int threadId, int operationId) throws InterruptedException {
        logger.fine("Thread " + threadId + " performing operation " + operationId);
        
        lock.lock();
        try {
            operationCount.incrementAndGet();
            Thread.sleep(10);
        } finally {
            lock.unlock();
        }
        
        logger.fine("Thread " + threadId + " completed operation " + operationId);
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Set logging level
        Logger.getLogger(DebuggingBestPracticesExample.class.getName()).setLevel(Level.ALL);
        
        DebuggingBestPracticesExample example = new DebuggingBestPracticesExample();
        example.demonstrateBestPractices();
    }
}
```

## 18.10 Troubleshooting Common Issues

Common concurrency issues include deadlocks, race conditions, memory leaks, and performance problems. Understanding these issues and their solutions is crucial for effective debugging.

### Common Issues:

**1. Deadlocks:**
- Circular wait conditions
- Lock ordering problems
- Resource contention

**2. Race Conditions:**
- Unsynchronized access
- Data corruption
- Inconsistent state

**3. Memory Leaks:**
- Unreleased resources
- Circular references
- Event listener leaks

### Java Example - Troubleshooting Common Issues:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.TimeUnit;

public class TroubleshootingExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(5);
    private final AtomicLong operationCount = new AtomicLong(0);
    private final ReentrantLock lock = new ReentrantLock();
    
    public void demonstrateTroubleshooting() throws InterruptedException {
        System.out.println("=== Troubleshooting Common Issues ===");
        
        // Test deadlock prevention
        testDeadlockPrevention();
        
        // Test race condition prevention
        testRaceConditionPrevention();
        
        // Test memory leak prevention
        testMemoryLeakPrevention();
        
        executor.shutdown();
    }
    
    private void testDeadlockPrevention() throws InterruptedException {
        System.out.println("\n--- Deadlock Prevention ---");
        
        Object lock1 = new Object();
        Object lock2 = new Object();
        
        Thread thread1 = new Thread(() -> {
            synchronized (lock1) {
                System.out.println("Thread 1 acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock2) {
                    System.out.println("Thread 1 acquired lock2");
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            synchronized (lock1) {
                System.out.println("Thread 2 acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock2) {
                    System.out.println("Thread 2 acquired lock2");
                }
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
    
    private void testRaceConditionPrevention() throws InterruptedException {
        System.out.println("\n--- Race Condition Prevention ---");
        
        AtomicLong counter = new AtomicLong(0);
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter.incrementAndGet();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter value: " + counter.get());
        System.out.println("Race condition prevented: " + (counter.get() == 5000));
    }
    
    private void testMemoryLeakPrevention() throws InterruptedException {
        System.out.println("\n--- Memory Leak Prevention ---");
        
        long startMemory = getUsedMemory();
        
        // Create objects with proper cleanup
        for (int i = 0; i < 1000; i++) {
            Object obj = new Object();
            // Simulate work
            Thread.sleep(1);
        }
        
        long endMemory = getUsedMemory();
        System.out.println("Memory used: " + (endMemory - startMemory) + " bytes");
        
        // Force garbage collection
        System.gc();
        Thread.sleep(1000);
        
        long afterGCMemory = getUsedMemory();
        System.out.println("Memory after GC: " + (afterGCMemory - startMemory) + " bytes");
        System.out.println("Memory leak prevented: " + (afterGCMemory < endMemory));
    }
    
    private long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
    
    public static void main(String[] args) throws InterruptedException {
        TroubleshootingExample example = new TroubleshootingExample();
        example.demonstrateTroubleshooting();
    }
}
```

### Real-World Analogy:
Think of concurrency debugging like debugging a complex machine:

- **Thread Dumps**: Like taking a snapshot of all the machine's parts at a specific moment
- **Logging and Tracing**: Like having detailed logs of what each part of the machine is doing
- **Profiling Tools**: Like having sensors that monitor the machine's performance
- **Deadlock Detection**: Like detecting when parts of the machine get stuck waiting for each other
- **Memory Leak Detection**: Like detecting when the machine is using more resources than it should
- **Performance Debugging**: Like optimizing the machine to run more efficiently
- **Debugging Tools**: Like having specialized tools to inspect and fix the machine
- **Best Practices**: Like following maintenance procedures to keep the machine running smoothly
- **Troubleshooting**: Like having a systematic approach to fix common problems

The key is to have the right tools and techniques to identify and fix issues quickly and effectively!