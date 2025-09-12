# Section 12 – Concurrency Testing

## 12.1 Unit Testing Concurrent Code

Unit testing concurrent code requires special techniques to handle asynchronous operations, timing issues, and race conditions.

### Key Concepts
- **Test Isolation**: Each test should be independent
- **Timing Control**: Managing test execution timing
- **Race Condition Testing**: Verifying thread safety
- **Mocking**: Creating test doubles for concurrent components

### Real-World Analogy
Think of testing a complex machine with multiple moving parts. You need to test each part individually while ensuring they work together correctly.

### Java Example
```java
public class ConcurrencyUnitTestingExample {
    // Thread-safe counter for testing
    public static class ThreadSafeCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        public void increment() {
            count.incrementAndGet();
        }
        
        public int getCount() {
            return count.get();
        }
        
        public void reset() {
            count.set(0);
        }
    }
    
    // Test class for concurrent counter
    public static class CounterTest {
        private ThreadSafeCounter counter;
        
        @BeforeEach
        public void setUp() {
            counter = new ThreadSafeCounter();
        }
        
        @Test
        public void testSingleThreadIncrement() {
            counter.increment();
            assertEquals(1, counter.getCount());
        }
        
        @Test
        public void testConcurrentIncrement() throws InterruptedException {
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
            
            // Start all threads
            for (Thread thread : threads) {
                thread.start();
            }
            
            // Wait for all threads to complete
            for (Thread thread : threads) {
                thread.join();
            }
            
            assertEquals(threadCount * incrementsPerThread, counter.getCount());
        }
        
        @Test
        public void testCounterReset() {
            counter.increment();
            counter.increment();
            assertEquals(2, counter.getCount());
            
            counter.reset();
            assertEquals(0, counter.getCount());
        }
    }
    
    // Test for race conditions
    public static class RaceConditionTest {
        @Test
        public void testRaceCondition() throws InterruptedException {
            int iterations = 1000;
            int threadCount = 10;
            AtomicInteger successCount = new AtomicInteger(0);
            
            for (int i = 0; i < iterations; i++) {
                ThreadSafeCounter counter = new ThreadSafeCounter();
                Thread[] threads = new Thread[threadCount];
                
                for (int j = 0; j < threadCount; j++) {
                    threads[j] = new Thread(() -> {
                        counter.increment();
                    });
                }
                
                // Start all threads
                for (Thread thread : threads) {
                    thread.start();
                }
                
                // Wait for all threads
                for (Thread thread : threads) {
                    thread.join();
                }
                
                if (counter.getCount() == threadCount) {
                    successCount.incrementAndGet();
                }
            }
            
            // All iterations should succeed
            assertEquals(iterations, successCount.get());
        }
    }
}
```

## 12.2 Integration Testing

Integration testing verifies that concurrent components work together correctly in a realistic environment.

### Key Concepts
- **Component Interaction**: Testing how components work together
- **Realistic Scenarios**: Testing with real-world usage patterns
- **End-to-End Testing**: Testing complete workflows
- **Performance Verification**: Ensuring acceptable performance

### Real-World Analogy
Think of testing a restaurant where you need to verify that the kitchen, waitstaff, and cashier all work together smoothly during busy periods.

### Java Example
```java
public class ConcurrencyIntegrationTestingExample {
    // Message queue for integration testing
    public static class MessageQueue {
        private final BlockingQueue<String> queue = new LinkedBlockingQueue<>();
        private final AtomicInteger processedCount = new AtomicInteger(0);
        
        public void put(String message) throws InterruptedException {
            queue.put(message);
        }
        
        public String take() throws InterruptedException {
            String message = queue.take();
            processedCount.incrementAndGet();
            return message;
        }
        
        public int getProcessedCount() {
            return processedCount.get();
        }
        
        public int getQueueSize() {
            return queue.size();
        }
    }
    
    // Producer for integration testing
    public static class Producer {
        private final MessageQueue queue;
        private final String name;
        private volatile boolean running = true;
        
        public Producer(MessageQueue queue, String name) {
            this.queue = queue;
            this.name = name;
        }
        
        public void start() {
            new Thread(() -> {
                int messageCount = 0;
                while (running) {
                    try {
                        String message = name + "-Message-" + messageCount++;
                        queue.put(message);
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }).start();
        }
        
        public void stop() {
            running = false;
        }
    }
    
    // Consumer for integration testing
    public static class Consumer {
        private final MessageQueue queue;
        private final String name;
        private volatile boolean running = true;
        
        public Consumer(MessageQueue queue, String name) {
            this.queue = queue;
            this.name = name;
        }
        
        public void start() {
            new Thread(() -> {
                while (running) {
                    try {
                        String message = queue.take();
                        System.out.println(name + " processed: " + message);
                        Thread.sleep(150);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }).start();
        }
        
        public void stop() {
            running = false;
        }
    }
    
    // Integration test
    public static class IntegrationTest {
        @Test
        public void testProducerConsumerIntegration() throws InterruptedException {
            MessageQueue queue = new MessageQueue();
            Producer producer1 = new Producer(queue, "Producer1");
            Producer producer2 = new Producer(queue, "Producer2");
            Consumer consumer1 = new Consumer(queue, "Consumer1");
            Consumer consumer2 = new Consumer(queue, "Consumer2");
            
            // Start all components
            producer1.start();
            producer2.start();
            consumer1.start();
            consumer2.start();
            
            // Let them run for a while
            Thread.sleep(5000);
            
            // Stop all components
            producer1.stop();
            producer2.stop();
            consumer1.stop();
            consumer2.stop();
            
            // Verify results
            assertTrue(queue.getProcessedCount() > 0);
            System.out.println("Total messages processed: " + queue.getProcessedCount());
        }
        
        @Test
        public void testConcurrentAccess() throws InterruptedException {
            MessageQueue queue = new MessageQueue();
            int threadCount = 10;
            Thread[] threads = new Thread[threadCount];
            
            for (int i = 0; i < threadCount; i++) {
                final int threadId = i;
                threads[i] = new Thread(() -> {
                    try {
                        for (int j = 0; j < 100; j++) {
                            queue.put("Thread" + threadId + "-Message" + j);
                            Thread.sleep(10);
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }
            
            // Start all threads
            for (Thread thread : threads) {
                thread.start();
            }
            
            // Wait for all threads
            for (Thread thread : threads) {
                thread.join();
            }
            
            // Verify all messages were processed
            assertEquals(threadCount * 100, queue.getProcessedCount());
        }
    }
}
```

## 12.3 Stress Testing

Stress testing subjects concurrent systems to high loads to identify performance bottlenecks and failure points.

### Key Concepts
- **High Load**: Testing with maximum expected load
- **Performance Metrics**: Measuring response times and throughput
- **Resource Usage**: Monitoring CPU, memory, and I/O usage
- **Failure Detection**: Identifying system limits

### Real-World Analogy
Think of stress testing a bridge by driving many heavy trucks across it simultaneously to see how much weight it can handle before failing.

### Java Example
```java
public class ConcurrencyStressTestingExample {
    // Thread pool for stress testing
    public static class StressTestThreadPool {
        private final ExecutorService executor;
        private final AtomicInteger taskCount = new AtomicInteger(0);
        private final AtomicInteger completedCount = new AtomicInteger(0);
        private final AtomicInteger errorCount = new AtomicInteger(0);
        
        public StressTestThreadPool(int threadCount) {
            this.executor = Executors.newFixedThreadPool(threadCount);
        }
        
        public void submitTask(Runnable task) {
            taskCount.incrementAndGet();
            executor.submit(() -> {
                try {
                    task.run();
                    completedCount.incrementAndGet();
                } catch (Exception e) {
                    errorCount.incrementAndGet();
                    System.err.println("Task error: " + e.getMessage());
                }
            });
        }
        
        public void waitForCompletion() throws InterruptedException {
            executor.shutdown();
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        }
        
        public int getTaskCount() { return taskCount.get(); }
        public int getCompletedCount() { return completedCount.get(); }
        public int getErrorCount() { return errorCount.get(); }
    }
    
    // Resource monitor for stress testing
    public static class ResourceMonitor {
        private final AtomicLong startTime = new AtomicLong();
        private final AtomicLong endTime = new AtomicLong();
        private final AtomicLong maxMemory = new AtomicLong();
        private final AtomicLong totalTasks = new AtomicLong();
        
        public void start() {
            startTime.set(System.currentTimeMillis());
            maxMemory.set(Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory());
        }
        
        public void update() {
            long currentMemory = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
            long currentMax = maxMemory.get();
            while (currentMemory > currentMax && !maxMemory.compareAndSet(currentMax, currentMemory)) {
                currentMax = maxMemory.get();
            }
            totalTasks.incrementAndGet();
        }
        
        public void stop() {
            endTime.set(System.currentTimeMillis());
        }
        
        public long getDuration() {
            return endTime.get() - startTime.get();
        }
        
        public long getMaxMemory() {
            return maxMemory.get();
        }
        
        public long getTotalTasks() {
            return totalTasks.get();
        }
        
        public double getThroughput() {
            long duration = getDuration();
            return duration > 0 ? (double) totalTasks.get() / duration * 1000 : 0;
        }
    }
    
    // Stress test for concurrent counter
    public static class CounterStressTest {
        @Test
        public void testCounterUnderStress() throws InterruptedException {
            ThreadSafeCounter counter = new ThreadSafeCounter();
            StressTestThreadPool threadPool = new StressTestThreadPool(50);
            ResourceMonitor monitor = new ResourceMonitor();
            
            monitor.start();
            
            // Submit many tasks
            for (int i = 0; i < 10000; i++) {
                threadPool.submitTask(() -> {
                    counter.increment();
                    monitor.update();
                });
            }
            
            threadPool.waitForCompletion();
            monitor.stop();
            
            // Verify results
            assertEquals(10000, counter.getCount());
            assertEquals(10000, threadPool.getCompletedCount());
            assertEquals(0, threadPool.getErrorCount());
            
            System.out.println("Stress test completed:");
            System.out.println("Duration: " + monitor.getDuration() + "ms");
            System.out.println("Max memory: " + monitor.getMaxMemory() / 1024 / 1024 + "MB");
            System.out.println("Throughput: " + monitor.getThroughput() + " tasks/sec");
        }
    }
    
    // Stress test for message queue
    public static class MessageQueueStressTest {
        @Test
        public void testMessageQueueUnderStress() throws InterruptedException {
            MessageQueue queue = new MessageQueue();
            StressTestThreadPool threadPool = new StressTestThreadPool(100);
            ResourceMonitor monitor = new ResourceMonitor();
            
            monitor.start();
            
            // Submit many tasks
            for (int i = 0; i < 5000; i++) {
                final int taskId = i;
                threadPool.submitTask(() -> {
                    try {
                        queue.put("Message-" + taskId);
                        monitor.update();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }
            
            threadPool.waitForCompletion();
            monitor.stop();
            
            // Verify results
            assertEquals(5000, threadPool.getCompletedCount());
            assertEquals(0, threadPool.getErrorCount());
            
            System.out.println("Message queue stress test completed:");
            System.out.println("Duration: " + monitor.getDuration() + "ms");
            System.out.println("Max memory: " + monitor.getMaxMemory() / 1024 / 1024 + "MB");
            System.out.println("Throughput: " + monitor.getThroughput() + " tasks/sec");
        }
    }
}
```

## 12.4 Race Condition Detection

Race condition detection involves identifying and testing scenarios where race conditions might occur.

### Key Concepts
- **Race Condition**: When the outcome depends on the timing of events
- **Detection Methods**: Various techniques to find race conditions
- **Testing Strategies**: How to test for race conditions
- **Prevention**: How to prevent race conditions

### Real-World Analogy
Think of testing a traffic intersection where you need to verify that cars don't collide when they arrive at the same time from different directions.

### Java Example
```java
public class RaceConditionDetectionExample {
    // Vulnerable counter that can have race conditions
    public static class VulnerableCounter {
        private int count = 0;
        
        public void increment() {
            count++; // Not thread-safe
        }
        
        public int getCount() {
            return count;
        }
    }
    
    // Race condition detector
    public static class RaceConditionDetector {
        private final int iterations;
        private final int threadCount;
        
        public RaceConditionDetector(int iterations, int threadCount) {
            this.iterations = iterations;
            this.threadCount = threadCount;
        }
        
        public boolean detectRaceCondition(Supplier<Runnable> taskSupplier) {
            int successCount = 0;
            
            for (int i = 0; i < iterations; i++) {
                if (runTest(taskSupplier)) {
                    successCount++;
                }
            }
            
            // If not all iterations succeed, there might be a race condition
            return successCount < iterations;
        }
        
        private boolean runTest(Supplier<Runnable> taskSupplier) {
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await(); // Wait for all threads to be ready
                        taskSupplier.get().run();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } finally {
                        endLatch.countDown();
                    }
                });
                threads[i].start();
            }
            
            // Start all threads simultaneously
            startLatch.countDown();
            
            try {
                endLatch.await(); // Wait for all threads to complete
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
            
            return true;
        }
    }
    
    // Test for race conditions
    public static class RaceConditionTest {
        @Test
        public void testVulnerableCounterRaceCondition() {
            VulnerableCounter counter = new VulnerableCounter();
            RaceConditionDetector detector = new RaceConditionDetector(100, 10);
            
            boolean hasRaceCondition = detector.detectRaceCondition(() -> () -> counter.increment());
            
            assertTrue(hasRaceCondition, "Vulnerable counter should have race conditions");
        }
        
        @Test
        public void testThreadSafeCounterNoRaceCondition() {
            ThreadSafeCounter counter = new ThreadSafeCounter();
            RaceConditionDetector detector = new RaceConditionDetector(100, 10);
            
            boolean hasRaceCondition = detector.detectRaceCondition(() -> () -> counter.increment());
            
            assertFalse(hasRaceCondition, "Thread-safe counter should not have race conditions");
        }
    }
    
    // Advanced race condition detection
    public static class AdvancedRaceConditionDetector {
        private final int iterations;
        private final int threadCount;
        private final long timeoutMs;
        
        public AdvancedRaceConditionDetector(int iterations, int threadCount, long timeoutMs) {
            this.iterations = iterations;
            this.threadCount = threadCount;
            this.timeoutMs = timeoutMs;
        }
        
        public RaceConditionResult detectRaceCondition(Supplier<Runnable> taskSupplier) {
            int successCount = 0;
            int timeoutCount = 0;
            List<Long> executionTimes = new ArrayList<>();
            
            for (int i = 0; i < iterations; i++) {
                ExecutionResult result = runTestWithTimeout(taskSupplier);
                if (result.isSuccess()) {
                    successCount++;
                    executionTimes.add(result.getExecutionTime());
                } else if (result.isTimeout()) {
                    timeoutCount++;
                }
            }
            
            return new RaceConditionResult(successCount, timeoutCount, executionTimes);
        }
        
        private ExecutionResult runTestWithTimeout(Supplier<Runnable> taskSupplier) {
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            AtomicBoolean success = new AtomicBoolean(true);
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        taskSupplier.get().run();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        success.set(false);
                    } catch (Exception e) {
                        success.set(false);
                    } finally {
                        endLatch.countDown();
                    }
                });
                threads[i].start();
            }
            
            startLatch.countDown();
            long startTime = System.currentTimeMillis();
            
            try {
                boolean completed = endLatch.await(timeoutMs, TimeUnit.MILLISECONDS);
                long executionTime = System.currentTimeMillis() - startTime;
                
                if (completed) {
                    return new ExecutionResult(true, false, executionTime);
                } else {
                    return new ExecutionResult(false, true, executionTime);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return new ExecutionResult(false, false, System.currentTimeMillis() - startTime);
            }
        }
    }
    
    // Result classes
    public static class RaceConditionResult {
        private final int successCount;
        private final int timeoutCount;
        private final List<Long> executionTimes;
        
        public RaceConditionResult(int successCount, int timeoutCount, List<Long> executionTimes) {
            this.successCount = successCount;
            this.timeoutCount = timeoutCount;
            this.executionTimes = executionTimes;
        }
        
        public int getSuccessCount() { return successCount; }
        public int getTimeoutCount() { return timeoutCount; }
        public List<Long> getExecutionTimes() { return executionTimes; }
        
        public boolean hasRaceCondition() {
            return successCount < iterations;
        }
        
        public double getSuccessRate() {
            return (double) successCount / iterations;
        }
        
        public double getAverageExecutionTime() {
            return executionTimes.stream().mapToLong(Long::longValue).average().orElse(0.0);
        }
    }
    
    public static class ExecutionResult {
        private final boolean success;
        private final boolean timeout;
        private final long executionTime;
        
        public ExecutionResult(boolean success, boolean timeout, long executionTime) {
            this.success = success;
            this.timeout = timeout;
            this.executionTime = executionTime;
        }
        
        public boolean isSuccess() { return success; }
        public boolean isTimeout() { return timeout; }
        public long getExecutionTime() { return executionTime; }
    }
}
```

## 12.5 Deadlock Detection

Deadlock detection involves identifying and testing scenarios where deadlocks might occur.

### Key Concepts
- **Deadlock**: When threads are blocked waiting for each other
- **Detection Methods**: Techniques to find deadlocks
- **Testing Strategies**: How to test for deadlocks
- **Prevention**: How to prevent deadlocks

### Real-World Analogy
Think of testing a traffic system where you need to verify that cars don't get stuck waiting for each other in a circular pattern.

### Java Example
```java
public class DeadlockDetectionExample {
    // Resource class that can cause deadlocks
    public static class Resource {
        private final String name;
        private final Object lock = new Object();
        
        public Resource(String name) {
            this.name = name;
        }
        
        public void use(Resource other) {
            synchronized (lock) {
                System.out.println(Thread.currentThread().getName() + " acquired " + name);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                synchronized (other.lock) {
                    System.out.println(Thread.currentThread().getName() + " acquired " + other.name);
                    // Simulate work
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            }
        }
    }
    
    // Deadlock detector
    public static class DeadlockDetector {
        private final int iterations;
        private final int threadCount;
        private final long timeoutMs;
        
        public DeadlockDetector(int iterations, int threadCount, long timeoutMs) {
            this.iterations = iterations;
            this.threadCount = threadCount;
            this.timeoutMs = timeoutMs;
        }
        
        public DeadlockResult detectDeadlock(Supplier<Runnable> taskSupplier) {
            int successCount = 0;
            int deadlockCount = 0;
            int timeoutCount = 0;
            
            for (int i = 0; i < iterations; i++) {
                ExecutionResult result = runTestWithTimeout(taskSupplier);
                if (result.isSuccess()) {
                    successCount++;
                } else if (result.isTimeout()) {
                    deadlockCount++;
                } else {
                    timeoutCount++;
                }
            }
            
            return new DeadlockResult(successCount, deadlockCount, timeoutCount);
        }
        
        private ExecutionResult runTestWithTimeout(Supplier<Runnable> taskSupplier) {
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            AtomicBoolean success = new AtomicBoolean(true);
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        taskSupplier.get().run();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        success.set(false);
                    } catch (Exception e) {
                        success.set(false);
                    } finally {
                        endLatch.countDown();
                    }
                });
                threads[i].start();
            }
            
            startLatch.countDown();
            
            try {
                boolean completed = endLatch.await(timeoutMs, TimeUnit.MILLISECONDS);
                if (completed) {
                    return new ExecutionResult(success.get(), false, 0);
                } else {
                    return new ExecutionResult(false, true, 0);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return new ExecutionResult(false, false, 0);
            }
        }
    }
    
    // Test for deadlocks
    public static class DeadlockTest {
        @Test
        public void testDeadlockDetection() {
            Resource resource1 = new Resource("Resource1");
            Resource resource2 = new Resource("Resource2");
            
            DeadlockDetector detector = new DeadlockDetector(10, 2, 2000);
            
            DeadlockResult result = detector.detectDeadlock(() -> () -> {
                resource1.use(resource2);
            });
            
            assertTrue(result.getDeadlockCount() > 0, "Should detect deadlocks");
            System.out.println("Deadlock test results:");
            System.out.println("Success: " + result.getSuccessCount());
            System.out.println("Deadlocks: " + result.getDeadlockCount());
            System.out.println("Timeouts: " + result.getTimeoutCount());
        }
    }
    
    // Result classes
    public static class DeadlockResult {
        private final int successCount;
        private final int deadlockCount;
        private final int timeoutCount;
        
        public DeadlockResult(int successCount, int deadlockCount, int timeoutCount) {
            this.successCount = successCount;
            this.deadlockCount = deadlockCount;
            this.timeoutCount = timeoutCount;
        }
        
        public int getSuccessCount() { return successCount; }
        public int getDeadlockCount() { return deadlockCount; }
        public int getTimeoutCount() { return timeoutCount; }
        
        public boolean hasDeadlocks() {
            return deadlockCount > 0;
        }
        
        public double getDeadlockRate() {
            return (double) deadlockCount / (successCount + deadlockCount + timeoutCount);
        }
    }
}
```

## 12.6 Performance Testing

Performance testing measures the performance characteristics of concurrent systems under various conditions.

### Key Concepts
- **Throughput**: Number of operations per unit time
- **Latency**: Time to complete a single operation
- **Resource Usage**: CPU, memory, and I/O usage
- **Scalability**: How performance changes with load

### Real-World Analogy
Think of testing a factory's production line to see how many products it can make per hour and how long each product takes to complete.

### Java Example
```java
public class ConcurrencyPerformanceTestingExample {
    // Performance metrics collector
    public static class PerformanceMetrics {
        private final AtomicLong totalOperations = new AtomicLong(0);
        private final AtomicLong totalTime = new AtomicLong(0);
        private final AtomicLong minTime = new AtomicLong(Long.MAX_VALUE);
        private final AtomicLong maxTime = new AtomicLong(0);
        private final AtomicLong errorCount = new AtomicLong(0);
        
        public void recordOperation(long executionTime) {
            totalOperations.incrementAndGet();
            totalTime.addAndGet(executionTime);
            
            long currentMin = minTime.get();
            while (executionTime < currentMin && !minTime.compareAndSet(currentMin, executionTime)) {
                currentMin = minTime.get();
            }
            
            long currentMax = maxTime.get();
            while (executionTime > currentMax && !maxTime.compareAndSet(currentMax, executionTime)) {
                currentMax = maxTime.get();
            }
        }
        
        public void recordError() {
            errorCount.incrementAndGet();
        }
        
        public long getTotalOperations() { return totalOperations.get(); }
        public long getTotalTime() { return totalTime.get(); }
        public long getMinTime() { return minTime.get(); }
        public long getMaxTime() { return maxTime.get(); }
        public long getErrorCount() { return errorCount.get(); }
        
        public double getAverageTime() {
            long total = totalOperations.get();
            return total > 0 ? (double) totalTime.get() / total : 0;
        }
        
        public double getThroughput() {
            long total = totalOperations.get();
            long time = totalTime.get();
            return time > 0 ? (double) total / time * 1000 : 0;
        }
    }
    
    // Performance test runner
    public static class PerformanceTestRunner {
        private final int threadCount;
        private final int operationsPerThread;
        private final long testDurationMs;
        
        public PerformanceTestRunner(int threadCount, int operationsPerThread, long testDurationMs) {
            this.threadCount = threadCount;
            this.operationsPerThread = operationsPerThread;
            this.testDurationMs = testDurationMs;
        }
        
        public PerformanceMetrics runTest(Supplier<Runnable> taskSupplier) {
            PerformanceMetrics metrics = new PerformanceMetrics();
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                executor.submit(() -> {
                    try {
                        startLatch.await();
                        
                        long startTime = System.currentTimeMillis();
                        long endTime = startTime + testDurationMs;
                        
                        while (System.currentTimeMillis() < endTime) {
                            long operationStart = System.currentTimeMillis();
                            try {
                                taskSupplier.get().run();
                                long operationEnd = System.currentTimeMillis();
                                metrics.recordOperation(operationEnd - operationStart);
                            } catch (Exception e) {
                                metrics.recordError();
                            }
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } finally {
                        endLatch.countDown();
                    }
                });
            }
            
            startLatch.countDown();
            
            try {
                endLatch.await();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            executor.shutdown();
            return metrics;
        }
    }
    
    // Performance test for counter
    public static class CounterPerformanceTest {
        @Test
        public void testCounterPerformance() {
            ThreadSafeCounter counter = new ThreadSafeCounter();
            PerformanceTestRunner runner = new PerformanceTestRunner(10, 1000, 5000);
            
            PerformanceMetrics metrics = runner.runTest(() -> () -> counter.increment());
            
            System.out.println("Counter performance test results:");
            System.out.println("Total operations: " + metrics.getTotalOperations());
            System.out.println("Total time: " + metrics.getTotalTime() + "ms");
            System.out.println("Average time: " + metrics.getAverageTime() + "ms");
            System.out.println("Min time: " + metrics.getMinTime() + "ms");
            System.out.println("Max time: " + metrics.getMaxTime() + "ms");
            System.out.println("Throughput: " + metrics.getThroughput() + " ops/sec");
            System.out.println("Errors: " + metrics.getErrorCount());
            
            assertTrue(metrics.getTotalOperations() > 0);
            assertTrue(metrics.getThroughput() > 0);
        }
    }
    
    // Performance test for message queue
    public static class MessageQueuePerformanceTest {
        @Test
        public void testMessageQueuePerformance() {
            MessageQueue queue = new MessageQueue();
            PerformanceTestRunner runner = new PerformanceTestRunner(20, 500, 5000);
            
            PerformanceMetrics metrics = runner.runTest(() -> () -> {
                try {
                    queue.put("Test message");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            System.out.println("Message queue performance test results:");
            System.out.println("Total operations: " + metrics.getTotalOperations());
            System.out.println("Total time: " + metrics.getTotalTime() + "ms");
            System.out.println("Average time: " + metrics.getAverageTime() + "ms");
            System.out.println("Min time: " + metrics.getMinTime() + "ms");
            System.out.println("Max time: " + metrics.getMaxTime() + "ms");
            System.out.println("Throughput: " + metrics.getThroughput() + " ops/sec");
            System.out.println("Errors: " + metrics.getErrorCount());
            
            assertTrue(metrics.getTotalOperations() > 0);
            assertTrue(metrics.getThroughput() > 0);
        }
    }
}
```

## 12.7 Property-Based Testing

Property-based testing uses random inputs to test properties that should hold for all valid inputs.

### Key Concepts
- **Random Inputs**: Generate random test data
- **Properties**: Assertions that should hold for all inputs
- **Shrinking**: Find minimal failing cases
- **Coverage**: Test edge cases automatically

### Real-World Analogy
Think of testing a calculator by randomly generating numbers and operations, then verifying that the results always follow mathematical rules.

### Java Example
```java
public class ConcurrencyPropertyBasedTestingExample {
    // Property-based test for counter
    public static class CounterPropertyTest {
        @Test
        public void testCounterProperties() {
            for (int i = 0; i < 1000; i++) {
                ThreadSafeCounter counter = new ThreadSafeCounter();
                int threadCount = 1 + (int)(Math.random() * 10);
                int operationsPerThread = 1 + (int)(Math.random() * 100);
                
                Thread[] threads = new Thread[threadCount];
                CountDownLatch startLatch = new CountDownLatch(1);
                CountDownLatch endLatch = new CountDownLatch(threadCount);
                
                for (int j = 0; j < threadCount; j++) {
                    threads[j] = new Thread(() -> {
                        try {
                            startLatch.await();
                            for (int k = 0; k < operationsPerThread; k++) {
                                counter.increment();
                            }
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                        } finally {
                            endLatch.countDown();
                        }
                    });
                    threads[j].start();
                }
                
                startLatch.countDown();
                
                try {
                    endLatch.await();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                // Property: final count should equal total operations
                assertEquals(threadCount * operationsPerThread, counter.getCount());
            }
        }
    }
    
    // Property-based test for message queue
    public static class MessageQueuePropertyTest {
        @Test
        public void testMessageQueueProperties() {
            for (int i = 0; i < 100; i++) {
                MessageQueue queue = new MessageQueue();
                int threadCount = 1 + (int)(Math.random() * 5);
                int messagesPerThread = 1 + (int)(Math.random() * 50);
                
                Thread[] threads = new Thread[threadCount];
                CountDownLatch startLatch = new CountDownLatch(1);
                CountDownLatch endLatch = new CountDownLatch(threadCount);
                
                for (int j = 0; j < threadCount; j++) {
                    final int threadId = j;
                    threads[j] = new Thread(() -> {
                        try {
                            startLatch.await();
                            for (int k = 0; k < messagesPerThread; k++) {
                                queue.put("Thread" + threadId + "-Message" + k);
                            }
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                        } finally {
                            endLatch.countDown();
                        }
                    });
                    threads[j].start();
                }
                
                startLatch.countDown();
                
                try {
                    endLatch.await();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                // Property: all messages should be processed
                assertEquals(threadCount * messagesPerThread, queue.getProcessedCount());
            }
        }
    }
}
```

## 12.8 Chaos Engineering

Chaos engineering involves intentionally introducing failures to test system resilience.

### Key Concepts
- **Failure Injection**: Deliberately causing failures
- **Resilience Testing**: Verifying system recovery
- **Fault Tolerance**: Testing error handling
- **Recovery Testing**: Verifying system restoration

### Real-World Analogy
Think of testing a building's fire safety by intentionally starting small fires to see how well the sprinkler system and evacuation procedures work.

### Java Example
```java
public class ConcurrencyChaosEngineeringExample {
    // Chaos injector
    public static class ChaosInjector {
        private final Random random = new Random();
        private final double failureRate;
        private final long maxDelayMs;
        
        public ChaosInjector(double failureRate, long maxDelayMs) {
            this.failureRate = failureRate;
            this.maxDelayMs = maxDelayMs;
        }
        
        public void injectChaos() {
            if (random.nextDouble() < failureRate) {
                try {
                    Thread.sleep(random.nextLong(maxDelayMs));
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                if (random.nextDouble() < 0.5) {
                    throw new RuntimeException("Chaos injection: random failure");
                }
            }
        }
    }
    
    // Resilient service
    public static class ResilientService {
        private final ChaosInjector chaosInjector;
        private final AtomicInteger successCount = new AtomicInteger(0);
        private final AtomicInteger failureCount = new AtomicInteger(0);
        private final AtomicInteger retryCount = new AtomicInteger(0);
        
        public ResilientService(ChaosInjector chaosInjector) {
            this.chaosInjector = chaosInjector;
        }
        
        public void processRequest(String request) {
            int maxRetries = 3;
            int retries = 0;
            
            while (retries < maxRetries) {
                try {
                    chaosInjector.injectChaos();
                    // Simulate work
                    Thread.sleep(100);
                    successCount.incrementAndGet();
                    return;
                } catch (Exception e) {
                    retries++;
                    retryCount.incrementAndGet();
                    if (retries >= maxRetries) {
                        failureCount.incrementAndGet();
                        throw new RuntimeException("Max retries exceeded", e);
                    }
                }
            }
        }
        
        public int getSuccessCount() { return successCount.get(); }
        public int getFailureCount() { return failureCount.get(); }
        public int getRetryCount() { return retryCount.get(); }
    }
    
    // Chaos engineering test
    public static class ChaosEngineeringTest {
        @Test
        public void testResilienceUnderChaos() throws InterruptedException {
            ChaosInjector chaosInjector = new ChaosInjector(0.3, 1000); // 30% failure rate
            ResilientService service = new ResilientService(chaosInjector);
            
            int threadCount = 10;
            int requestsPerThread = 100;
            Thread[] threads = new Thread[threadCount];
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < requestsPerThread; j++) {
                        try {
                            service.processRequest("Request " + j);
                        } catch (Exception e) {
                            // Handle failures
                        }
                    }
                });
                threads[i].start();
            }
            
            for (Thread thread : threads) {
                thread.join();
            }
            
            System.out.println("Chaos engineering test results:");
            System.out.println("Success count: " + service.getSuccessCount());
            System.out.println("Failure count: " + service.getFailureCount());
            System.out.println("Retry count: " + service.getRetryCount());
            
            assertTrue(service.getSuccessCount() > 0);
            assertTrue(service.getRetryCount() > 0);
        }
    }
}
```

This comprehensive explanation covers all aspects of concurrency testing, providing both theoretical understanding and practical Java examples to illustrate each concept.