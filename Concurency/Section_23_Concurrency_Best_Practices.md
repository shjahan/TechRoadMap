# Section 23 – Concurrency Best Practices

## 23.1 Design Principles

Design principles for concurrent systems help create maintainable, scalable, and reliable applications.

### Key Concepts
- **Single Responsibility**: Each component should have one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived classes must be substitutable for base classes
- **Interface Segregation**: Clients should not depend on interfaces they don't use
- **Dependency Inversion**: Depend on abstractions, not concretions

### Real-World Analogy
Think of designing a restaurant kitchen. Each station (grill, salad, dessert) has a specific responsibility, can be extended with new equipment without changing existing setup, and follows standard protocols that any chef can understand and use.

### Java Example
```java
// Design principles in concurrent systems
public class ConcurrentDesignPrinciples {
    
    // Single Responsibility: Each class has one job
    public static class TaskProcessor {
        public void processTask(Task task) {
            // Only responsible for processing tasks
            System.out.println("Processing task: " + task.getId());
        }
    }
    
    public static class TaskScheduler {
        public void scheduleTask(Task task, long delay) {
            // Only responsible for scheduling tasks
            System.out.println("Scheduling task: " + task.getId() + " with delay: " + delay);
        }
    }
    
    // Open/Closed: Open for extension, closed for modification
    public abstract static class TaskHandler {
        public abstract void handle(Task task);
    }
    
    public static class EmailTaskHandler extends TaskHandler {
        @Override
        public void handle(Task task) {
            System.out.println("Handling email task: " + task.getId());
        }
    }
    
    public static class SmsTaskHandler extends TaskHandler {
        @Override
        public void handle(Task task) {
            System.out.println("Handling SMS task: " + task.getId());
        }
    }
    
    // Interface Segregation: Small, focused interfaces
    public interface TaskExecutor {
        void execute(Task task);
    }
    
    public interface TaskScheduler {
        void schedule(Task task, long delay);
    }
    
    // Dependency Inversion: Depend on abstractions
    public static class TaskManager {
        private final TaskExecutor executor;
        private final TaskScheduler scheduler;
        
        public TaskManager(TaskExecutor executor, TaskScheduler scheduler) {
            this.executor = executor;
            this.scheduler = scheduler;
        }
        
        public void processTask(Task task) {
            executor.execute(task);
        }
        
        public void scheduleTask(Task task, long delay) {
            scheduler.schedule(task, delay);
        }
    }
}
```

## 23.2 Code Review Guidelines

Code review guidelines help ensure that concurrent code is correct, maintainable, and follows best practices.

### Key Concepts
- **Thread Safety**: Ensuring code is safe for concurrent access
- **Performance**: Checking for performance issues
- **Readability**: Ensuring code is easy to understand
- **Testing**: Verifying that code is properly tested

### Real-World Analogy
Think of a building inspection. The inspector checks for structural integrity (thread safety), energy efficiency (performance), accessibility (readability), and compliance with codes (testing). Code review works similarly by checking all aspects of code quality.

### Java Example
```java
// Code review guidelines
public class CodeReviewGuidelines {
    
    // GOOD: Thread-safe implementation
    public static class ThreadSafeCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        public void increment() {
            count.incrementAndGet();
        }
        
        public int getCount() {
            return count.get();
        }
    }
    
    // BAD: Not thread-safe
    public static class UnsafeCounter {
        private int count = 0;
        
        public void increment() {
            count++; // Race condition!
        }
        
        public int getCount() {
            return count;
        }
    }
    
    // GOOD: Proper resource management
    public static class ResourceManager {
        private final ExecutorService executor = Executors.newFixedThreadPool(10);
        
        public void processTask(Task task) {
            executor.submit(() -> {
                try {
                    // Process task
                    System.out.println("Processing: " + task.getId());
                } catch (Exception e) {
                    System.err.println("Error processing task: " + e.getMessage());
                }
            });
        }
        
        public void shutdown() {
            executor.shutdown();
            try {
                if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                    executor.shutdownNow();
                }
            } catch (InterruptedException e) {
                executor.shutdownNow();
                Thread.currentThread().interrupt();
            }
        }
    }
    
    // GOOD: Clear and readable code
    public static class ClearConcurrentCode {
        private final Object lock = new Object();
        private final Map<String, String> data = new HashMap<>();
        
        public void updateData(String key, String value) {
            synchronized (lock) {
                data.put(key, value);
            }
        }
        
        public String getData(String key) {
            synchronized (lock) {
                return data.get(key);
            }
        }
    }
}
```

## 23.3 Documentation Standards

Documentation standards ensure that concurrent code is well-documented and easy to understand.

### Key Concepts
- **API Documentation**: Documenting public interfaces
- **Thread Safety**: Documenting thread safety guarantees
- **Performance**: Documenting performance characteristics
- **Examples**: Providing usage examples

### Real-World Analogy
Think of a user manual for a complex machine. It explains how to use each feature, what safety precautions to take, how fast it can operate, and provides step-by-step examples. Documentation works similarly by explaining how to use code safely and effectively.

### Java Example
```java
// Documentation standards
public class DocumentationStandards {
    
    /**
     * Thread-safe counter that supports atomic increment operations.
     * 
     * <p>This class is thread-safe and can be safely used by multiple threads
     * without external synchronization. All operations are atomic and provide
     * memory visibility guarantees.
     * 
     * <p>Performance characteristics:
     * <ul>
     *   <li>increment(): O(1) time complexity
     *   <li>getCount(): O(1) time complexity
     *   <li>Memory usage: O(1) space complexity
     * </ul>
     * 
     * <p>Example usage:
     * <pre>{@code
     * ThreadSafeCounter counter = new ThreadSafeCounter();
     * counter.increment();
     * int count = counter.getCount();
     * }</pre>
     * 
     * @author John Doe
     * @version 1.0
     * @since 1.0
     */
    public static class ThreadSafeCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        /**
         * Atomically increments the counter by 1.
         * 
         * <p>This method is thread-safe and can be called concurrently
         * by multiple threads without external synchronization.
         * 
         * @return the previous value of the counter
         */
        public int increment() {
            return count.incrementAndGet();
        }
        
        /**
         * Gets the current value of the counter.
         * 
         * <p>This method is thread-safe and provides memory visibility
         * guarantees. The returned value reflects the most recent
         * increment operation.
         * 
         * @return the current value of the counter
         */
        public int getCount() {
            return count.get();
        }
    }
    
    /**
     * Thread-safe cache with configurable capacity and eviction policy.
     * 
     * <p>This cache is thread-safe and can be safely used by multiple threads.
     * It uses a read-write lock to allow concurrent reads while ensuring
     * exclusive access for writes.
     * 
     * <p>Thread safety guarantees:
     * <ul>
     *   <li>Multiple threads can read concurrently
     *   <li>Only one thread can write at a time
     *   <li>Reads are blocked during writes
     *   <li>Writes are blocked during reads
     * </ul>
     * 
     * <p>Performance characteristics:
     * <ul>
     *   <li>get(): O(1) average time complexity
     *   <li>put(): O(1) average time complexity
     *   <li>Memory usage: O(capacity) space complexity
     * </ul>
     * 
     * @param <K> the type of keys
     * @param <V> the type of values
     */
    public static class ThreadSafeCache<K, V> {
        private final Map<K, V> cache = new HashMap<>();
        private final ReadWriteLock lock = new ReentrantReadWriteLock();
        private final int capacity;
        
        /**
         * Creates a new thread-safe cache with the specified capacity.
         * 
         * @param capacity the maximum number of elements the cache can hold
         * @throws IllegalArgumentException if capacity is negative
         */
        public ThreadSafeCache(int capacity) {
            if (capacity < 0) {
                throw new IllegalArgumentException("Capacity cannot be negative");
            }
            this.capacity = capacity;
        }
        
        /**
         * Gets the value associated with the specified key.
         * 
         * <p>This method is thread-safe and allows concurrent reads.
         * 
         * @param key the key whose associated value is to be returned
         * @return the value associated with the key, or null if not found
         */
        public V get(K key) {
            lock.readLock().lock();
            try {
                return cache.get(key);
            } finally {
                lock.readLock().unlock();
            }
        }
        
        /**
         * Associates the specified value with the specified key.
         * 
         * <p>This method is thread-safe and provides exclusive access
         * for writes. If the cache is at capacity, the least recently
         * used entry will be evicted.
         * 
         * @param key the key with which the specified value is to be associated
         * @param value the value to be associated with the specified key
         * @return the previous value associated with the key, or null if none
         */
        public V put(K key, V value) {
            lock.writeLock().lock();
            try {
                if (cache.size() >= capacity) {
                    // Evict least recently used entry
                    evictLRU();
                }
                return cache.put(key, value);
            } finally {
                lock.writeLock().unlock();
            }
        }
        
        private void evictLRU() {
            // Simplified LRU eviction
            if (!cache.isEmpty()) {
                K firstKey = cache.keySet().iterator().next();
                cache.remove(firstKey);
            }
        }
    }
}
```

## 23.4 Error Handling

Error handling in concurrent systems must be robust and prevent errors from propagating across thread boundaries.

### Key Concepts
- **Exception Propagation**: How exceptions are handled across threads
- **Error Recovery**: Recovering from errors without affecting other threads
- **Logging**: Proper logging of errors for debugging
- **Graceful Degradation**: Continuing operation despite errors

### Real-World Analogy
Think of a power grid where one transformer fails. The system should isolate the failure, reroute power through other transformers, and alert maintenance crews, all while keeping the rest of the grid running normally.

### Java Example
```java
// Error handling in concurrent systems
public class ConcurrentErrorHandling {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    private final Logger logger = LoggerFactory.getLogger(ConcurrentErrorHandling.class);
    
    // Proper error handling with recovery
    public void processTaskWithErrorHandling(Task task) {
        executor.submit(() -> {
            try {
                processTask(task);
            } catch (Exception e) {
                logger.error("Error processing task: " + task.getId(), e);
                handleTaskError(task, e);
            }
        });
    }
    
    private void processTask(Task task) throws Exception {
        // Simulate task processing
        if (Math.random() < 0.1) { // 10% chance of failure
            throw new RuntimeException("Task processing failed");
        }
        
        System.out.println("Task processed: " + task.getId());
    }
    
    private void handleTaskError(Task task, Exception e) {
        // Retry logic
        if (task.getRetryCount() < 3) {
            task.incrementRetryCount();
            logger.info("Retrying task: " + task.getId() + " (attempt " + task.getRetryCount() + ")");
            
            // Schedule retry with exponential backoff
            long delay = (long) Math.pow(2, task.getRetryCount()) * 1000; // 1s, 2s, 4s
            executor.schedule(() -> processTaskWithErrorHandling(task), delay, TimeUnit.MILLISECONDS);
        } else {
            logger.error("Task failed after maximum retries: " + task.getId());
            // Move to dead letter queue or notify administrators
            moveToDeadLetterQueue(task);
        }
    }
    
    private void moveToDeadLetterQueue(Task task) {
        // Implementation for moving failed tasks to dead letter queue
        System.out.println("Moving task to dead letter queue: " + task.getId());
    }
    
    // Circuit breaker pattern for error handling
    public static class CircuitBreaker {
        private final int failureThreshold;
        private final long timeoutMs;
        private final AtomicInteger failureCount = new AtomicInteger(0);
        private final AtomicLong lastFailureTime = new AtomicLong(0);
        private volatile State state = State.CLOSED;
        
        public enum State {
            CLOSED, OPEN, HALF_OPEN
        }
        
        public CircuitBreaker(int failureThreshold, long timeoutMs) {
            this.failureThreshold = failureThreshold;
            this.timeoutMs = timeoutMs;
        }
        
        public <T> T execute(Supplier<T> operation, Supplier<T> fallback) {
            if (state == State.OPEN) {
                if (System.currentTimeMillis() - lastFailureTime.get() > timeoutMs) {
                    state = State.HALF_OPEN;
                } else {
                    return fallback.get();
                }
            }
            
            try {
                T result = operation.get();
                onSuccess();
                return result;
            } catch (Exception e) {
                onFailure();
                return fallback.get();
            }
        }
        
        private void onSuccess() {
            failureCount.set(0);
            state = State.CLOSED;
        }
        
        private void onFailure() {
            lastFailureTime.set(System.currentTimeMillis());
            if (failureCount.incrementAndGet() >= failureThreshold) {
                state = State.OPEN;
            }
        }
    }
}
```

## 23.5 Resource Management

Resource management ensures that resources are properly allocated, used, and released in concurrent systems.

### Key Concepts
- **Resource Allocation**: Proper allocation of resources
- **Resource Cleanup**: Ensuring resources are released
- **Resource Pooling**: Reusing resources efficiently
- **Resource Limits**: Preventing resource exhaustion

### Real-World Analogy
Think of managing a fleet of company cars. You need to allocate cars to employees, ensure they're returned when not needed, maintain a pool of available cars, and prevent the fleet from growing too large for your budget.

### Java Example
```java
// Resource management in concurrent systems
public class ConcurrentResourceManagement {
    private final ExecutorService executor = Executors.newFixedThreadPool(10);
    private final Map<String, Connection> connections = new ConcurrentHashMap<>();
    private final Semaphore connectionSemaphore = new Semaphore(5); // Max 5 connections
    
    // Resource pooling
    public static class ConnectionPool {
        private final Queue<Connection> availableConnections = new ConcurrentLinkedQueue<>();
        private final Set<Connection> allConnections = ConcurrentHashMap.newKeySet();
        private final int maxSize;
        private final AtomicInteger currentSize = new AtomicInteger(0);
        
        public ConnectionPool(int maxSize) {
            this.maxSize = maxSize;
        }
        
        public Connection getConnection() throws InterruptedException {
            Connection connection = availableConnections.poll();
            if (connection == null) {
                if (currentSize.get() < maxSize) {
                    connection = createConnection();
                    allConnections.add(connection);
                } else {
                    throw new RuntimeException("Connection pool exhausted");
                }
            }
            return connection;
        }
        
        public void returnConnection(Connection connection) {
            if (allConnections.contains(connection)) {
                availableConnections.offer(connection);
            }
        }
        
        private Connection createConnection() {
            currentSize.incrementAndGet();
            return new Connection();
        }
        
        public void closeAll() {
            for (Connection connection : allConnections) {
                connection.close();
            }
            allConnections.clear();
            availableConnections.clear();
        }
    }
    
    // Resource cleanup with try-with-resources
    public void processWithResourceCleanup() {
        try (Connection connection = getConnection()) {
            // Use connection
            connection.execute("SELECT * FROM users");
        } catch (Exception e) {
            logger.error("Error processing with connection", e);
        }
        // Connection is automatically closed
    }
    
    private Connection getConnection() throws InterruptedException {
        connectionSemaphore.acquire();
        try {
            return new Connection();
        } catch (Exception e) {
            connectionSemaphore.release();
            throw e;
        }
    }
    
    // Resource monitoring
    public void monitorResources() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        
        System.out.println("Memory Usage:");
        System.out.println("Total: " + totalMemory / 1024 / 1024 + " MB");
        System.out.println("Used: " + usedMemory / 1024 / 1024 + " MB");
        System.out.println("Free: " + freeMemory / 1024 / 1024 + " MB");
        
        // Check for memory leaks
        if (usedMemory > totalMemory * 0.8) {
            System.out.println("WARNING: High memory usage detected!");
        }
    }
    
    // Graceful shutdown
    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

## 23.6 Performance Optimization

Performance optimization in concurrent systems involves identifying and eliminating bottlenecks.

### Key Concepts
- **Profiling**: Identifying performance bottlenecks
- **Caching**: Storing frequently accessed data
- **Load Balancing**: Distributing work evenly
- **Resource Optimization**: Using resources efficiently

### Real-World Analogy
Think of optimizing a factory production line. You need to identify which stations are slowest, add caching for frequently used parts, balance work across multiple lines, and ensure each machine is running at optimal efficiency.

### Java Example
```java
// Performance optimization in concurrent systems
public class ConcurrentPerformanceOptimization {
    private final Map<String, String> cache = new ConcurrentHashMap<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(
        Runtime.getRuntime().availableProcessors()
    );
    
    // Caching for performance
    public String getCachedData(String key) {
        return cache.computeIfAbsent(key, this::computeExpensiveData);
    }
    
    private String computeExpensiveData(String key) {
        // Simulate expensive computation
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "Data for " + key;
    }
    
    // Parallel processing for performance
    public List<String> processDataInParallel(List<String> data) {
        return data.parallelStream()
            .map(this::processItem)
            .collect(Collectors.toList());
    }
    
    private String processItem(String item) {
        // Simulate processing
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return "Processed: " + item;
    }
    
    // Batch processing for performance
    public void processBatch(List<Task> tasks) {
        int batchSize = 100;
        List<List<Task>> batches = partition(tasks, batchSize);
        
        for (List<Task> batch : batches) {
            executor.submit(() -> processBatch(batch));
        }
    }
    
    private void processBatch(List<Task> batch) {
        for (Task task : batch) {
            processTask(task);
        }
    }
    
    private List<List<Task>> partition(List<Task> list, int batchSize) {
        List<List<Task>> partitions = new ArrayList<>();
        for (int i = 0; i < list.size(); i += batchSize) {
            partitions.add(list.subList(i, Math.min(i + batchSize, list.size())));
        }
        return partitions;
    }
    
    private void processTask(Task task) {
        // Process individual task
        System.out.println("Processing task: " + task.getId());
    }
    
    // Performance monitoring
    public void monitorPerformance() {
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        long[] threadIds = threadBean.getAllThreadIds();
        
        for (long threadId : threadIds) {
            ThreadInfo threadInfo = threadBean.getThreadInfo(threadId);
            if (threadInfo != null) {
                long cpuTime = threadBean.getThreadCpuTime(threadId);
                System.out.println("Thread " + threadInfo.getThreadName() + 
                                 " CPU time: " + cpuTime / 1000000 + " ms");
            }
        }
    }
}
```

## 23.7 Testing Strategies

Testing strategies for concurrent systems must account for timing, race conditions, and non-deterministic behavior.

### Key Concepts
- **Unit Testing**: Testing individual components
- **Integration Testing**: Testing component interactions
- **Stress Testing**: Testing under high load
- **Race Condition Testing**: Testing for race conditions

### Real-World Analogy
Think of testing a complex machine. You need to test each part individually, test how parts work together, test the machine under heavy load, and specifically test for timing-related issues that could cause failures.

### Java Example
```java
// Testing strategies for concurrent systems
public class ConcurrentTestingStrategies {
    
    // Unit testing with mocks
    @Test
    public void testCounterIncrement() {
        ThreadSafeCounter counter = new ThreadSafeCounter();
        
        // Test single thread
        counter.increment();
        assertEquals(1, counter.getCount());
        
        // Test multiple threads
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
        
        // Wait for all threads
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        assertEquals(threadCount * incrementsPerThread, counter.getCount());
    }
    
    // Integration testing
    @Test
    public void testTaskProcessingIntegration() {
        TaskProcessor processor = new TaskProcessor();
        TaskScheduler scheduler = new TaskScheduler();
        TaskManager manager = new TaskManager(processor, scheduler);
        
        Task task = new Task("test-task");
        manager.processTask(task);
        
        // Verify task was processed
        assertTrue(task.isProcessed());
    }
    
    // Stress testing
    @Test
    public void testUnderStress() {
        ThreadSafeCounter counter = new ThreadSafeCounter();
        int threadCount = 100;
        int operationsPerThread = 10000;
        
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    counter.increment();
                }
            });
        }
        
        long startTime = System.currentTimeMillis();
        
        // Start all threads
        for (Thread thread : threads) {
            thread.start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        long endTime = System.currentTimeMillis();
        
        assertEquals(threadCount * operationsPerThread, counter.getCount());
        System.out.println("Stress test completed in " + (endTime - startTime) + " ms");
    }
    
    // Race condition testing
    @Test
    public void testRaceCondition() {
        VulnerableCounter counter = new VulnerableCounter();
        int iterations = 1000;
        int threadCount = 10;
        
        for (int i = 0; i < iterations; i++) {
            Thread[] threads = new Thread[threadCount];
            for (int j = 0; j < threadCount; j++) {
                threads[j] = new Thread(() -> counter.increment());
            }
            
            // Start all threads
            for (Thread thread : threads) {
                thread.start();
            }
            
            // Wait for all threads
            for (Thread thread : threads) {
                try {
                    thread.join();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            
            // Check for race condition
            if (counter.getCount() != threadCount) {
                System.out.println("Race condition detected! Expected: " + 
                                 threadCount + ", Actual: " + counter.getCount());
            }
            
            counter.reset();
        }
    }
}
```

## 23.8 Maintenance and Evolution

Maintenance and evolution of concurrent systems requires careful planning and execution to avoid introducing bugs.

### Key Concepts
- **Refactoring**: Improving code without changing functionality
- **Version Control**: Managing code changes
- **Backward Compatibility**: Maintaining compatibility with existing code
- **Documentation Updates**: Keeping documentation current

### Real-World Analogy
Think of maintaining and upgrading a complex machine. You need to make improvements without breaking existing functionality, keep track of all changes, ensure new parts work with old ones, and update the manual to reflect changes.

### Java Example
```java
// Maintenance and evolution of concurrent systems
public class ConcurrentMaintenanceAndEvolution {
    
    // Version 1: Simple implementation
    public static class TaskProcessorV1 {
        private final ExecutorService executor = Executors.newFixedThreadPool(10);
        
        public void processTask(Task task) {
            executor.submit(() -> {
                // Process task
                System.out.println("Processing task: " + task.getId());
            });
        }
    }
    
    // Version 2: Added error handling
    public static class TaskProcessorV2 {
        private final ExecutorService executor = Executors.newFixedThreadPool(10);
        private final Logger logger = LoggerFactory.getLogger(TaskProcessorV2.class);
        
        public void processTask(Task task) {
            executor.submit(() -> {
                try {
                    // Process task
                    System.out.println("Processing task: " + task.getId());
                } catch (Exception e) {
                    logger.error("Error processing task: " + task.getId(), e);
                }
            });
        }
    }
    
    // Version 3: Added monitoring and metrics
    public static class TaskProcessorV3 {
        private final ExecutorService executor = Executors.newFixedThreadPool(10);
        private final Logger logger = LoggerFactory.getLogger(TaskProcessorV3.class);
        private final AtomicLong processedCount = new AtomicLong(0);
        private final AtomicLong errorCount = new AtomicLong(0);
        
        public void processTask(Task task) {
            executor.submit(() -> {
                try {
                    // Process task
                    System.out.println("Processing task: " + task.getId());
                    processedCount.incrementAndGet();
                } catch (Exception e) {
                    logger.error("Error processing task: " + task.getId(), e);
                    errorCount.incrementAndGet();
                }
            });
        }
        
        public long getProcessedCount() {
            return processedCount.get();
        }
        
        public long getErrorCount() {
            return errorCount.get();
        }
    }
    
    // Refactoring example
    public static class RefactoredTaskProcessor {
        private final ExecutorService executor;
        private final Logger logger;
        private final Metrics metrics;
        
        public RefactoredTaskProcessor(ExecutorService executor, Logger logger, Metrics metrics) {
            this.executor = executor;
            this.logger = logger;
            this.metrics = metrics;
        }
        
        public void processTask(Task task) {
            executor.submit(() -> {
                try {
                    processTaskInternal(task);
                    metrics.incrementProcessedCount();
                } catch (Exception e) {
                    logger.error("Error processing task: " + task.getId(), e);
                    metrics.incrementErrorCount();
                }
            });
        }
        
        private void processTaskInternal(Task task) {
            // Process task
            System.out.println("Processing task: " + task.getId());
        }
    }
    
    // Backward compatibility
    public static class BackwardCompatibleTaskProcessor {
        private final TaskProcessorV3 processor;
        
        public BackwardCompatibleTaskProcessor() {
            this.processor = new TaskProcessorV3();
        }
        
        // Maintain old interface
        public void processTask(Task task) {
            processor.processTask(task);
        }
        
        // Add new functionality
        public void processTaskWithCallback(Task task, Callback callback) {
            processor.processTask(task);
            callback.onComplete(task);
        }
    }
    
    // Documentation updates
    /**
     * Task processor for handling concurrent task execution.
     * 
     * <p>This class provides thread-safe task processing with the following features:
     * <ul>
     *   <li>Configurable thread pool size
     *   <li>Error handling and logging
     *   <li>Performance metrics
     *   <li>Graceful shutdown
     * </ul>
     * 
     * <p>Example usage:
     * <pre>{@code
     * TaskProcessor processor = new TaskProcessor(10);
     * processor.processTask(new Task("task1"));
     * processor.shutdown();
     * }</pre>
     * 
     * @version 3.0
     * @since 1.0
     */
    public static class TaskProcessor {
        private final ExecutorService executor;
        private final Logger logger;
        private final Metrics metrics;
        
        public TaskProcessor(int threadCount) {
            this.executor = Executors.newFixedThreadPool(threadCount);
            this.logger = LoggerFactory.getLogger(TaskProcessor.class);
            this.metrics = new Metrics();
        }
        
        public void processTask(Task task) {
            executor.submit(() -> {
                try {
                    processTaskInternal(task);
                    metrics.incrementProcessedCount();
                } catch (Exception e) {
                    logger.error("Error processing task: " + task.getId(), e);
                    metrics.incrementErrorCount();
                }
            });
        }
        
        private void processTaskInternal(Task task) {
            // Process task
            System.out.println("Processing task: " + task.getId());
        }
        
        public void shutdown() {
            executor.shutdown();
            try {
                if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                    executor.shutdownNow();
                }
            } catch (InterruptedException e) {
                executor.shutdownNow();
                Thread.currentThread().interrupt();
            }
        }
    }
}
```

This comprehensive explanation covers all aspects of concurrency best practices, providing both theoretical understanding and practical examples to illustrate each concept.