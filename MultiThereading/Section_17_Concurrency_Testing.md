# Section 17 - Concurrency Testing

## 17.1 Testing Fundamentals

Concurrency testing is the process of verifying that multithreaded applications work correctly under various conditions. It's more complex than sequential testing due to the non-deterministic nature of concurrent execution.

### Key Concepts:

**1. Non-Deterministic Behavior:**
- Thread execution order varies
- Timing-dependent bugs
- Race conditions

**2. Test Categories:**
- Unit tests
- Integration tests
- Stress tests
- Performance tests

**3. Testing Challenges:**
- Reproducibility
- Coverage
- Debugging

### Java Example - Testing Fundamentals:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.*;

public class ConcurrencyTestingExample {
    private Counter counter;
    
    @BeforeEach
    void setUp() {
        counter = new Counter();
    }
    
    @Test
    void testConcurrentIncrement() throws InterruptedException {
        int threadCount = 10;
        int incrementsPerThread = 1000;
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        assertEquals(threadCount * incrementsPerThread, counter.getValue());
    }
    
    static class Counter {
        private int value = 0;
        
        public synchronized void increment() {
            value++;
        }
        
        public int getValue() {
            return value;
        }
    }
}
```

## 17.2 Unit Testing

Unit testing for concurrent code focuses on testing individual components in isolation. It requires special techniques to handle the non-deterministic nature of concurrency.

### Key Techniques:

**1. Deterministic Testing:**
- Control thread execution
- Use barriers and latches
- Synchronize test execution

**2. Mock Objects:**
- Mock concurrent dependencies
- Control timing
- Isolate components

**3. Test Data:**
- Use predictable data
- Avoid random values
- Ensure reproducibility

### Java Example - Unit Testing:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

public class UnitTestingExample {
    private ThreadSafeQueue<Integer> queue;
    
    @BeforeEach
    void setUp() {
        queue = new ThreadSafeQueue<>();
    }
    
    @Test
    void testConcurrentEnqueue() throws InterruptedException {
        int threadCount = 5;
        int itemsPerThread = 100;
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(threadCount);
        AtomicInteger totalItems = new AtomicInteger(0);
        
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                try {
                    startLatch.await();
                    for (int j = 0; j < itemsPerThread; j++) {
                        queue.enqueue(j);
                        totalItems.incrementAndGet();
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    endLatch.countDown();
                }
            });
            threads[i].start();
        }
        
        startLatch.countDown();
        endLatch.await();
        
        assertEquals(threadCount * itemsPerThread, totalItems.get());
        assertEquals(threadCount * itemsPerThread, queue.size());
    }
    
    static class ThreadSafeQueue<T> {
        private final java.util.concurrent.BlockingQueue<T> queue = 
            new java.util.concurrent.LinkedBlockingQueue<>();
        
        public void enqueue(T item) {
            queue.offer(item);
        }
        
        public T dequeue() throws InterruptedException {
            return queue.take();
        }
        
        public int size() {
            return queue.size();
        }
    }
}
```

## 17.3 Integration Testing

Integration testing verifies that multiple concurrent components work together correctly. It tests the interactions between different parts of the system.

### Key Aspects:

**1. Component Interactions:**
- Test communication between components
- Verify data flow
- Check synchronization

**2. System Behavior:**
- Test overall system behavior
- Verify performance characteristics
- Check resource usage

**3. Error Handling:**
- Test error propagation
- Verify recovery mechanisms
- Check failure scenarios

### Java Example - Integration Testing:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;

public class IntegrationTestingExample {
    private ProducerConsumerSystem system;
    private ExecutorService executor;
    
    @BeforeEach
    void setUp() {
        system = new ProducerConsumerSystem();
        executor = Executors.newFixedThreadPool(4);
    }
    
    @Test
    void testProducerConsumerIntegration() throws Exception {
        int producerCount = 2;
        int consumerCount = 2;
        int itemsPerProducer = 100;
        
        // Start producers
        Future<?>[] producerFutures = new Future[producerCount];
        for (int i = 0; i < producerCount; i++) {
            producerFutures[i] = executor.submit(() -> {
                for (int j = 0; j < itemsPerProducer; j++) {
                    system.produce("Item-" + j);
                }
            });
        }
        
        // Start consumers
        Future<?>[] consumerFutures = new Future[consumerCount];
        for (int i = 0; i < consumerCount; i++) {
            consumerFutures[i] = executor.submit(() -> {
                for (int j = 0; j < itemsPerProducer; j++) {
                    system.consume();
                }
            });
        }
        
        // Wait for completion
        for (Future<?> future : producerFutures) {
            future.get(5, TimeUnit.SECONDS);
        }
        for (Future<?> future : consumerFutures) {
            future.get(5, TimeUnit.SECONDS);
        }
        
        assertEquals(0, system.getQueueSize());
    }
    
    static class ProducerConsumerSystem {
        private final java.util.concurrent.BlockingQueue<String> queue = 
            new java.util.concurrent.LinkedBlockingQueue<>();
        
        public void produce(String item) {
            queue.offer(item);
        }
        
        public String consume() throws InterruptedException {
            return queue.take();
        }
        
        public int getQueueSize() {
            return queue.size();
        }
    }
}
```

## 17.4 Stress Testing

Stress testing subjects the system to high load and extreme conditions to identify breaking points and ensure stability under pressure.

### Key Techniques:

**1. High Load:**
- Many concurrent threads
- High data volume
- Extended duration

**2. Resource Exhaustion:**
- Memory pressure
- CPU saturation
- I/O bottlenecks

**3. Failure Scenarios:**
- Network failures
- Resource unavailability
- System crashes

### Java Example - Stress Testing:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;

public class StressTestingExample {
    private ExecutorService executor;
    private AtomicLong operationCount;
    private AtomicLong errorCount;
    
    @BeforeEach
    void setUp() {
        executor = Executors.newFixedThreadPool(100);
        operationCount = new AtomicLong(0);
        errorCount = new AtomicLong(0);
    }
    
    @AfterEach
    void tearDown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
    }
    
    @Test
    void testHighLoadStress() throws InterruptedException {
        int threadCount = 100;
        int operationsPerThread = 1000;
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    try {
                        performOperation();
                        operationCount.incrementAndGet();
                    } catch (Exception e) {
                        errorCount.incrementAndGet();
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
        
        System.out.println("Operations completed: " + operationCount.get());
        System.out.println("Errors: " + errorCount.get());
        System.out.println("Error rate: " + 
            (double) errorCount.get() / operationCount.get() * 100 + "%");
        
        assertTrue(errorCount.get() < operationCount.get() * 0.01); // Less than 1% error rate
    }
    
    private void performOperation() throws InterruptedException {
        // Simulate some work
        Thread.sleep(1);
        
        // Simulate occasional failures
        if (Math.random() < 0.001) {
            throw new RuntimeException("Simulated failure");
        }
    }
}
```

## 17.5 Performance Testing

Performance testing measures the system's performance characteristics under various load conditions. It helps identify bottlenecks and optimize performance.

### Key Metrics:

**1. Throughput:**
- Operations per second
- Data processed per unit time
- System capacity

**2. Latency:**
- Response time
- Processing time
- User experience

**3. Resource Usage:**
- CPU utilization
- Memory consumption
- I/O efficiency

### Java Example - Performance Testing:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicLong;

public class PerformanceTestingExample {
    private ExecutorService executor;
    private AtomicLong totalOperations;
    private AtomicLong totalTime;
    
    @BeforeEach
    void setUp() {
        executor = Executors.newFixedThreadPool(10);
        totalOperations = new AtomicLong(0);
        totalTime = new AtomicLong(0);
    }
    
    @AfterEach
    void tearDown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
    }
    
    @Test
    void testThroughput() throws InterruptedException {
        int threadCount = 10;
        int operationsPerThread = 1000;
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    performOperation();
                    totalOperations.incrementAndGet();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
        
        long endTime = System.currentTimeMillis();
        long totalDuration = endTime - startTime;
        
        double throughput = (double) totalOperations.get() / totalDuration * 1000;
        System.out.println("Throughput: " + throughput + " ops/sec");
        
        assertTrue(throughput > 1000); // Minimum throughput requirement
    }
    
    @Test
    void testLatency() throws InterruptedException {
        int threadCount = 10;
        int operationsPerThread = 100;
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    long startTime = System.currentTimeMillis();
                    performOperation();
                    long endTime = System.currentTimeMillis();
                    totalTime.addAndGet(endTime - startTime);
                    totalOperations.incrementAndGet();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
        
        double averageLatency = (double) totalTime.get() / totalOperations.get();
        System.out.println("Average latency: " + averageLatency + "ms");
        
        assertTrue(averageLatency < 10); // Maximum latency requirement
    }
    
    private void performOperation() {
        // Simulate some work
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 17.6 Race Condition Testing

Race condition testing specifically targets race conditions and data races. It uses techniques to increase the likelihood of detecting these hard-to-reproduce bugs.

### Key Techniques:

**1. Thread Interleaving:**
- Control thread execution order
- Force specific interleavings
- Increase race condition probability

**2. Timing Manipulation:**
- Add delays and sleeps
- Vary execution timing
- Create race windows

**3. Repetitive Testing:**
- Run tests multiple times
- Use different thread counts
- Vary system load

### Java Example - Race Condition Testing:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.RepeatedTest;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

public class RaceConditionTestingExample {
    @RepeatedTest(100)
    void testRaceCondition() throws InterruptedException {
        int threadCount = 10;
        int operationsPerThread = 1000;
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(threadCount);
        AtomicInteger counter = new AtomicInteger(0);
        
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                try {
                    startLatch.await();
                    for (int j = 0; j < operationsPerThread; j++) {
                        // Simulate race condition
                        int current = counter.get();
                        Thread.yield(); // Force context switch
                        counter.set(current + 1);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    endLatch.countDown();
                }
            });
            threads[i].start();
        }
        
        startLatch.countDown();
        endLatch.await();
        
        // This test will likely fail due to race condition
        assertEquals(threadCount * operationsPerThread, counter.get());
    }
    
    @Test
    void testRaceConditionWithSynchronization() throws InterruptedException {
        int threadCount = 10;
        int operationsPerThread = 1000;
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(threadCount);
        AtomicInteger counter = new AtomicInteger(0);
        
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                try {
                    startLatch.await();
                    for (int j = 0; j < operationsPerThread; j++) {
                        // Use atomic operation to avoid race condition
                        counter.incrementAndGet();
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    endLatch.countDown();
                }
            });
            threads[i].start();
        }
        
        startLatch.countDown();
        endLatch.await();
        
        assertEquals(threadCount * operationsPerThread, counter.get());
    }
}
```

## 17.7 Deadlock Testing

Deadlock testing focuses on detecting and preventing deadlocks. It uses techniques to increase the likelihood of deadlock occurrence and verify deadlock detection mechanisms.

### Key Techniques:

**1. Lock Ordering:**
- Test different lock orders
- Force lock acquisition patterns
- Verify deadlock prevention

**2. Timeout Testing:**
- Use timeouts for lock acquisition
- Test deadlock detection
- Verify recovery mechanisms

**3. Resource Exhaustion:**
- Test with limited resources
- Force resource contention
- Verify deadlock scenarios

### Java Example - Deadlock Testing:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.RepeatedTest;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class DeadlockTestingExample {
    @RepeatedTest(50)
    void testDeadlockScenario() throws InterruptedException {
        Lock lock1 = new ReentrantLock();
        Lock lock2 = new ReentrantLock();
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(2);
        
        Thread thread1 = new Thread(() -> {
            try {
                startLatch.await();
                lock1.lock();
                try {
                    Thread.sleep(10); // Increase deadlock probability
                    lock2.lock();
                    try {
                        // Work with both locks
                    } finally {
                        lock2.unlock();
                    }
                } finally {
                    lock1.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                endLatch.countDown();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            try {
                startLatch.await();
                lock2.lock();
                try {
                    Thread.sleep(10); // Increase deadlock probability
                    lock1.lock();
                    try {
                        // Work with both locks
                    } finally {
                        lock1.unlock();
                    }
                } finally {
                    lock2.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                endLatch.countDown();
            }
        });
        
        thread1.start();
        thread2.start();
        startLatch.countDown();
        
        // Wait with timeout to detect deadlock
        boolean completed = endLatch.await(5, TimeUnit.SECONDS);
        assertTrue(completed, "Potential deadlock detected");
    }
    
    @Test
    void testDeadlockPrevention() throws InterruptedException {
        Lock lock1 = new ReentrantLock();
        Lock lock2 = new ReentrantLock();
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(2);
        
        Thread thread1 = new Thread(() -> {
            try {
                startLatch.await();
                // Always acquire locks in the same order
                lock1.lock();
                try {
                    lock2.lock();
                    try {
                        // Work with both locks
                    } finally {
                        lock2.unlock();
                    }
                } finally {
                    lock1.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                endLatch.countDown();
            }
        });
        
        Thread thread2 = new Thread(() -> {
            try {
                startLatch.await();
                // Always acquire locks in the same order
                lock1.lock();
                try {
                    lock2.lock();
                    try {
                        // Work with both locks
                    } finally {
                        lock2.unlock();
                    }
                } finally {
                    lock1.unlock();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                endLatch.countDown();
            }
        });
        
        thread1.start();
        thread2.start();
        startLatch.countDown();
        
        boolean completed = endLatch.await(5, TimeUnit.SECONDS);
        assertTrue(completed, "Deadlock prevention working");
    }
}
```

## 17.8 Test Automation

Test automation is crucial for concurrent testing due to the need for repetitive execution and continuous monitoring. It helps maintain test quality and reduces manual effort.

### Key Components:

**1. Test Runners:**
- JUnit, TestNG
- Parallel execution
- Test reporting

**2. CI/CD Integration:**
- Automated test execution
- Continuous monitoring
- Failure notification

**3. Test Data Management:**
- Test data generation
- Data cleanup
- Test isolation

### Java Example - Test Automation:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.parallel.Execution;
import org.junit.jupiter.api.parallel.ExecutionMode;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

@Execution(ExecutionMode.CONCURRENT)
public class TestAutomationExample {
    private ExecutorService executor;
    private TestDataManager dataManager;
    
    @BeforeEach
    void setUp() {
        executor = Executors.newFixedThreadPool(10);
        dataManager = new TestDataManager();
    }
    
    @AfterEach
    void tearDown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
        dataManager.cleanup();
    }
    
    @Test
    void testAutomatedConcurrency() throws InterruptedException {
        int threadCount = 10;
        int operationsPerThread = 100;
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    String testData = dataManager.generateTestData();
                    processData(testData);
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
        
        assertTrue(dataManager.getProcessedCount() > 0);
    }
    
    private void processData(String data) {
        // Simulate data processing
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    static class TestDataManager {
        private int processedCount = 0;
        
        public String generateTestData() {
            return "TestData-" + System.currentTimeMillis();
        }
        
        public void cleanup() {
            processedCount = 0;
        }
        
        public int getProcessedCount() {
            return processedCount;
        }
    }
}
```

## 17.9 Test Debugging

Debugging concurrent tests is challenging due to the non-deterministic nature of concurrency. Special techniques and tools are needed to identify and fix issues.

### Key Techniques:

**1. Logging:**
- Detailed execution logs
- Thread identification
- Timing information

**2. Thread Dumps:**
- Capture thread states
- Identify deadlocks
- Analyze thread behavior

**3. Debugging Tools:**
- IDE debuggers
- Profiling tools
- Monitoring tools

### Java Example - Test Debugging:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.logging.Logger;

public class TestDebuggingExample {
    private static final Logger logger = Logger.getLogger(TestDebuggingExample.class.getName());
    private ExecutorService executor;
    
    @BeforeEach
    void setUp() {
        executor = Executors.newFixedThreadPool(5);
    }
    
    @AfterEach
    void tearDown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
    }
    
    @Test
    void testWithDebugging() throws InterruptedException {
        logger.info("Starting concurrent test");
        
        int threadCount = 5;
        int operationsPerThread = 100;
        
        for (int i = 0; i < threadCount; i++) {
            final int threadId = i;
            executor.submit(() -> {
                logger.info("Thread " + threadId + " started");
                try {
                    for (int j = 0; j < operationsPerThread; j++) {
                        performOperation(threadId, j);
                    }
                    logger.info("Thread " + threadId + " completed");
                } catch (Exception e) {
                    logger.severe("Thread " + threadId + " failed: " + e.getMessage());
                    e.printStackTrace();
                }
            });
        }
        
        executor.shutdown();
        boolean completed = executor.awaitTermination(60, TimeUnit.SECONDS);
        
        if (!completed) {
            logger.warning("Test did not complete within timeout");
            // Generate thread dump
            generateThreadDump();
        }
        
        assertTrue(completed, "Test should complete within timeout");
    }
    
    private void performOperation(int threadId, int operationId) throws InterruptedException {
        logger.fine("Thread " + threadId + " performing operation " + operationId);
        
        // Simulate work
        Thread.sleep(10);
        
        // Simulate occasional failures
        if (Math.random() < 0.01) {
            throw new RuntimeException("Simulated failure in thread " + threadId);
        }
    }
    
    private void generateThreadDump() {
        logger.info("Generating thread dump...");
        Thread.getAllStackTraces().forEach((thread, stackTrace) -> {
            logger.info("Thread: " + thread.getName() + " - State: " + thread.getState());
            for (StackTraceElement element : stackTrace) {
                logger.info("  " + element.toString());
            }
        });
    }
}
```

## 17.10 Testing Best Practices

Following best practices ensures effective and reliable concurrent testing. It helps maintain test quality and reduces debugging effort.

### Best Practices:

**1. Test Design:**
- Keep tests simple
- Use deterministic data
- Avoid timing dependencies

**2. Test Execution:**
- Run tests multiple times
- Use different thread counts
- Monitor system resources

**3. Test Maintenance:**
- Regular test updates
- Performance monitoring
- Continuous improvement

### Java Example - Testing Best Practices:

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.RepeatedTest;
import static org.junit.jupiter.api.Assertions.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

public class TestingBestPracticesExample {
    private ExecutorService executor;
    private AtomicInteger successCount;
    private AtomicInteger failureCount;
    
    @BeforeEach
    void setUp() {
        executor = Executors.newFixedThreadPool(10);
        successCount = new AtomicInteger(0);
        failureCount = new AtomicInteger(0);
    }
    
    @AfterEach
    void tearDown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
    }
    
    @RepeatedTest(10)
    void testConcurrentOperation() throws InterruptedException {
        int threadCount = 10;
        int operationsPerThread = 100;
        
        for (int i = 0; i < threadCount; i++) {
            executor.submit(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    try {
                        performOperation();
                        successCount.incrementAndGet();
                    } catch (Exception e) {
                        failureCount.incrementAndGet();
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(60, TimeUnit.SECONDS);
        
        int totalOperations = threadCount * operationsPerThread;
        int totalSuccess = successCount.get();
        int totalFailures = failureCount.get();
        
        assertEquals(totalOperations, totalSuccess + totalFailures);
        assertTrue(totalFailures < totalOperations * 0.01); // Less than 1% failure rate
    }
    
    private void performOperation() throws InterruptedException {
        // Simulate work
        Thread.sleep(1);
        
        // Simulate occasional failures
        if (Math.random() < 0.001) {
            throw new RuntimeException("Simulated failure");
        }
    }
}
```

### Real-World Analogy:
Think of concurrency testing like testing a busy intersection:

- **Unit Testing**: Like testing each traffic light individually
- **Integration Testing**: Like testing how all traffic lights work together
- **Stress Testing**: Like testing the intersection during rush hour
- **Performance Testing**: Like measuring how many cars can pass through per hour
- **Race Condition Testing**: Like testing what happens when multiple cars arrive at the same time
- **Deadlock Testing**: Like testing what happens when cars get stuck in a gridlock
- **Test Automation**: Like having automated traffic monitoring systems
- **Test Debugging**: Like having traffic cameras to see what went wrong
- **Testing Best Practices**: Like following traffic engineering standards

The key is to test under various conditions and ensure the system works correctly even when things don't go as planned!