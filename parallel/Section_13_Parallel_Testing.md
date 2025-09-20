# Section 13 – Parallel Testing

## 13.1 Parallel Testing Challenges

Parallel testing presents unique challenges due to the non-deterministic nature and complexity of concurrent systems.

### Key Concepts:
- **Non-determinism**: Different execution paths on each test run
- **Race conditions**: Timing-dependent test failures
- **Test isolation**: Ensuring tests don't interfere with each other
- **Reproducibility**: Making tests consistently repeatable

### Real-World Analogy:
Parallel testing is like testing a busy restaurant during peak hours - you need to ensure the kitchen can handle multiple orders simultaneously, servers don't interfere with each other, and the system works under various load conditions.

### Example: Testing Challenges
```java
public class ParallelTestingChallenges {
    private static int sharedCounter = 0;
    
    public static void main(String[] args) {
        System.out.println("=== Parallel Testing Challenges Demo ===");
        
        // Challenge 1: Non-deterministic behavior
        demonstrateNonDeterminism();
        
        // Challenge 2: Race conditions in tests
        demonstrateRaceConditionTesting();
    }
    
    private static void demonstrateNonDeterminism() {
        System.out.println("\n=== Challenge 1: Non-deterministic Behavior ===");
        
        for (int run = 0; run < 3; run++) {
            sharedCounter = 0;
            Thread[] threads = new Thread[5];
            
            for (int i = 0; i < 5; i++) {
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < 100; j++) {
                        sharedCounter++; // Race condition
                    }
                });
                threads[i].start();
            }
            
            for (Thread thread : threads) {
                try {
                    thread.join();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            
            System.out.println("Run " + (run + 1) + ": Counter = " + sharedCounter + 
                             " (Expected: 500)");
        }
    }
    
    private static void demonstrateRaceConditionTesting() {
        System.out.println("\n=== Challenge 2: Race Condition Testing ===");
        
        // Test that may pass or fail depending on timing
        boolean testPassed = testConcurrentIncrement();
        System.out.println("Test result: " + (testPassed ? "PASS" : "FAIL"));
        System.out.println("This test may give different results on different runs");
    }
    
    private static boolean testConcurrentIncrement() {
        final AtomicInteger counter = new AtomicInteger(0);
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    counter.incrementAndGet();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
        
        return counter.get() == 1000;
    }
}
```

## 13.2 Unit Testing

Unit testing in parallel systems focuses on testing individual components in isolation.

### Key Concepts:
- **Test isolation**: Each test runs independently
- **Mocking**: Simulating dependencies and external systems
- **Deterministic testing**: Making tests predictable
- **Thread-safe assertions**: Ensuring test assertions are thread-safe

### Real-World Analogy:
Unit testing parallel code is like testing individual kitchen appliances before putting them together - you want to make sure each component works correctly on its own before testing the entire system.

### Example: Unit Testing Parallel Components
```java
public class ParallelUnitTesting {
    
    public static void main(String[] args) {
        System.out.println("=== Parallel Unit Testing Demo ===");
        
        // Test individual parallel components
        testParallelSum();
        testThreadSafeCounter();
        testProducerConsumer();
    }
    
    // Unit test for parallel sum calculation
    private static void testParallelSum() {
        System.out.println("\n=== Unit Test: Parallel Sum ===");
        
        ParallelSumCalculator calculator = new ParallelSumCalculator();
        int[] data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        
        int result = calculator.calculateSum(data);
        int expected = 55;
        
        assert result == expected : "Expected " + expected + " but got " + result;
        System.out.println("Test passed: Sum = " + result);
    }
    
    // Unit test for thread-safe counter
    private static void testThreadSafeCounter() {
        System.out.println("\n=== Unit Test: Thread-Safe Counter ===");
        
        ThreadSafeCounter counter = new ThreadSafeCounter();
        
        // Test increment
        counter.increment();
        assert counter.getValue() == 1 : "Expected 1 but got " + counter.getValue();
        
        // Test multiple increments
        for (int i = 0; i < 99; i++) {
            counter.increment();
        }
        assert counter.getValue() == 100 : "Expected 100 but got " + counter.getValue();
        
        // Test reset
        counter.reset();
        assert counter.getValue() == 0 : "Expected 0 but got " + counter.getValue();
        
        System.out.println("Test passed: Thread-safe counter works correctly");
    }
    
    // Unit test for producer-consumer
    private static void testProducerConsumer() {
        System.out.println("\n=== Unit Test: Producer-Consumer ===");
        
        BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(5);
        ProducerConsumerTest test = new ProducerConsumerTest(queue);
        
        boolean result = test.testProducerConsumer();
        assert result : "Producer-consumer test failed";
        
        System.out.println("Test passed: Producer-consumer works correctly");
    }
    
    // Helper classes for testing
    static class ParallelSumCalculator {
        public int calculateSum(int[] data) {
            return Arrays.stream(data).parallel().sum();
        }
    }
    
    static class ThreadSafeCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        public void increment() {
            count.incrementAndGet();
        }
        
        public int getValue() {
            return count.get();
        }
        
        public void reset() {
            count.set(0);
        }
    }
    
    static class ProducerConsumerTest {
        private final BlockingQueue<Integer> queue;
        
        public ProducerConsumerTest(BlockingQueue<Integer> queue) {
            this.queue = queue;
        }
        
        public boolean testProducerConsumer() {
            try {
                // Test producer
                for (int i = 0; i < 5; i++) {
                    queue.offer(i);
                }
                
                // Test consumer
                int sum = 0;
                for (int i = 0; i < 5; i++) {
                    sum += queue.take();
                }
                
                return sum == 10; // 0+1+2+3+4 = 10
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return false;
            }
        }
    }
}
```

## 13.3 Integration Testing

Integration testing verifies that parallel components work correctly together.

### Key Concepts:
- **Component interaction**: Testing how components communicate
- **End-to-end testing**: Testing complete workflows
- **System integration**: Testing with external systems
- **Data flow testing**: Verifying data passes correctly between components

### Real-World Analogy:
Integration testing is like testing how all the kitchen stations work together during service - ensuring orders flow smoothly from taking orders to cooking to serving customers.

### Example: Integration Testing
```java
public class ParallelIntegrationTesting {
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Integration Testing Demo ===");
        
        // Test integration between producer and consumer
        testProducerConsumerIntegration();
        
        // Test pipeline integration
        testPipelineIntegration();
        
        // Test distributed system integration
        testDistributedSystemIntegration();
    }
    
    private static void testProducerConsumerIntegration() throws InterruptedException {
        System.out.println("\n=== Integration Test: Producer-Consumer ===");
        
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();
        final AtomicInteger producedCount = new AtomicInteger(0);
        final AtomicInteger consumedCount = new AtomicInteger(0);
        
        // Producer thread
        Thread producer = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    queue.put("Item-" + i);
                    producedCount.incrementAndGet();
                    Thread.sleep(50);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Consumer thread
        Thread consumer = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    String item = queue.take();
                    consumedCount.incrementAndGet();
                    System.out.println("Consumed: " + item);
                    Thread.sleep(30);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        producer.start();
        consumer.start();
        
        producer.join();
        consumer.join();
        
        // Verify integration
        assert producedCount.get() == 10 : "Expected 10 produced items";
        assert consumedCount.get() == 10 : "Expected 10 consumed items";
        assert queue.isEmpty() : "Queue should be empty";
        
        System.out.println("Integration test passed: Producer-Consumer worked correctly");
    }
    
    private static void testPipelineIntegration() throws InterruptedException {
        System.out.println("\n=== Integration Test: Pipeline ===");
        
        BlockingQueue<Integer> stage1To2 = new LinkedBlockingQueue<>();
        BlockingQueue<Integer> stage2To3 = new LinkedBlockingQueue<>();
        final List<Integer> finalResults = Collections.synchronizedList(new ArrayList<>());
        
        // Stage 1: Generator
        Thread stage1 = new Thread(() -> {
            for (int i = 1; i <= 5; i++) {
                try {
                    stage1To2.put(i);
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Stage 2: Processor
        Thread stage2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                try {
                    int value = stage1To2.take();
                    int processed = value * value; // Square the value
                    stage2To3.put(processed);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Stage 3: Collector
        Thread stage3 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                try {
                    int value = stage2To3.take();
                    finalResults.add(value);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        stage1.start();
        stage2.start();
        stage3.start();
        
        stage1.join();
        stage2.join();
        stage3.join();
        
        // Verify pipeline integration
        List<Integer> expected = Arrays.asList(1, 4, 9, 16, 25);
        Collections.sort(finalResults);
        
        assert finalResults.equals(expected) : "Pipeline results don't match expected";
        System.out.println("Integration test passed: Pipeline worked correctly");
        System.out.println("Results: " + finalResults);
    }
    
    private static void testDistributedSystemIntegration() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Integration Test: Distributed System ===");
        
        // Simulate distributed nodes
        ExecutorService nodePool = Executors.newFixedThreadPool(3);
        final Map<String, String> distributedStorage = new ConcurrentHashMap<>();
        
        // Node 1: Data producer
        Future<String> node1 = nodePool.submit(() -> {
            distributedStorage.put("node1-data", "value1");
            return "Node1 completed";
        });
        
        // Node 2: Data processor
        Future<String> node2 = nodePool.submit(() -> {
            // Wait for node1 data
            while (!distributedStorage.containsKey("node1-data")) {
                Thread.sleep(50);
            }
            String data = distributedStorage.get("node1-data");
            distributedStorage.put("node2-processed", data.toUpperCase());
            return "Node2 completed";
        });
        
        // Node 3: Data consumer
        Future<String> node3 = nodePool.submit(() -> {
            // Wait for node2 processed data
            while (!distributedStorage.containsKey("node2-processed")) {
                Thread.sleep(50);
            }
            String processedData = distributedStorage.get("node2-processed");
            distributedStorage.put("final-result", processedData + "-FINAL");
            return "Node3 completed";
        });
        
        // Wait for all nodes
        String result1 = node1.get();
        String result2 = node2.get();
        String result3 = node3.get();
        
        nodePool.shutdown();
        
        // Verify distributed integration
        assert distributedStorage.containsKey("final-result") : "Final result not found";
        assert "VALUE1-FINAL".equals(distributedStorage.get("final-result")) : "Final result incorrect";
        
        System.out.println("Integration test passed: Distributed system worked correctly");
        System.out.println("Final result: " + distributedStorage.get("final-result"));
    }
}
```

## 13.4 Performance Testing

Performance testing evaluates how parallel systems perform under various load conditions.

### Key Concepts:
- **Load testing**: Testing under expected load
- **Throughput testing**: Measuring processing capacity
- **Latency testing**: Measuring response times
- **Scalability testing**: Testing performance with increasing resources

### Real-World Analogy:
Performance testing is like testing how fast a restaurant can serve customers during different busy periods - measuring how many orders can be processed per hour and how long customers wait.

### Example: Performance Testing
```java
public class ParallelPerformanceTesting {
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Performance Testing Demo ===");
        
        // Test throughput
        testThroughput();
        
        // Test latency
        testLatency();
        
        // Test scalability
        testScalability();
    }
    
    private static void testThroughput() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Performance Test: Throughput ===");
        
        int[] dataSizes = {10000, 50000, 100000};
        
        for (int dataSize : dataSizes) {
            int[] data = generateData(dataSize);
            
            long startTime = System.currentTimeMillis();
            
            // Process data in parallel
            int result = Arrays.stream(data).parallel().sum();
            
            long endTime = System.currentTimeMillis();
            long duration = endTime - startTime;
            
            double throughput = (double) dataSize / duration * 1000; // items per second
            
            System.out.println("Data size: " + dataSize + 
                             ", Duration: " + duration + "ms" +
                             ", Throughput: " + throughput + " items/sec");
        }
    }
    
    private static void testLatency() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Performance Test: Latency ===");
        
        BlockingQueue<String> requestQueue = new LinkedBlockingQueue<>();
        BlockingQueue<String> responseQueue = new LinkedBlockingQueue<>();
        
        // Start request processor
        Thread processor = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    String request = requestQueue.take();
                    // Simulate processing
                    Thread.sleep(10);
                    responseQueue.put("Processed: " + request);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        processor.start();
        
        // Measure latency for multiple requests
        List<Long> latencies = new ArrayList<>();
        
        for (int i = 0; i < 10; i++) {
            long startTime = System.nanoTime();
            
            requestQueue.put("Request-" + i);
            responseQueue.take();
            
            long endTime = System.nanoTime();
            long latency = (endTime - startTime) / 1_000_000; // Convert to milliseconds
            latencies.add(latency);
        }
        
        processor.interrupt();
        
        // Calculate statistics
        double avgLatency = latencies.stream().mapToLong(Long::longValue).average().orElse(0);
        long maxLatency = latencies.stream().mapToLong(Long::longValue).max().orElse(0);
        long minLatency = latencies.stream().mapToLong(Long::longValue).min().orElse(0);
        
        System.out.println("Average latency: " + avgLatency + "ms");
        System.out.println("Max latency: " + maxLatency + "ms");
        System.out.println("Min latency: " + minLatency + "ms");
    }
    
    private static void testScalability() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Performance Test: Scalability ===");
        
        int[] threadCounts = {1, 2, 4, 8};
        int workSize = 100000;
        
        for (int threadCount : threadCounts) {
            long startTime = System.currentTimeMillis();
            
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);
            List<Future<Integer>> futures = new ArrayList<>();
            
            int chunkSize = workSize / threadCount;
            
            for (int i = 0; i < threadCount; i++) {
                final int start = i * chunkSize;
                final int end = (i == threadCount - 1) ? workSize : (i + 1) * chunkSize;
                
                futures.add(executor.submit(() -> {
                    int sum = 0;
                    for (int j = start; j < end; j++) {
                        sum += j * j; // Simulate computation
                    }
                    return sum;
                }));
            }
            
            // Wait for completion
            for (Future<Integer> future : futures) {
                future.get();
            }
            
            executor.shutdown();
            
            long endTime = System.currentTimeMillis();
            long duration = endTime - startTime;
            
            System.out.println("Threads: " + threadCount + 
                             ", Duration: " + duration + "ms");
        }
    }
    
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
}
```

## 13.5 Stress Testing

Stress testing evaluates system behavior under extreme conditions and heavy loads.

### Key Concepts:
- **Breaking point**: Finding system limits
- **Resource exhaustion**: Testing with limited resources
- **Recovery testing**: How system recovers from stress
- **Failure modes**: Understanding how system fails

### Example: Stress Testing
```java
public class ParallelStressTesting {
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Parallel Stress Testing Demo ===");
        
        // Test memory stress
        testMemoryStress();
        
        // Test thread stress
        testThreadStress();
        
        // Test CPU stress
        testCpuStress();
    }
    
    private static void testMemoryStress() {
        System.out.println("\n=== Stress Test: Memory ===");
        
        Runtime runtime = Runtime.getRuntime();
        List<byte[]> memoryHog = new ArrayList<>();
        
        try {
            long initialMemory = runtime.totalMemory() - runtime.freeMemory();
            System.out.println("Initial memory usage: " + initialMemory / (1024 * 1024) + " MB");
            
            // Allocate memory until we approach the limit
            while (true) {
                byte[] chunk = new byte[1024 * 1024]; // 1MB chunks
                memoryHog.add(chunk);
                
                long currentMemory = runtime.totalMemory() - runtime.freeMemory();
                long maxMemory = runtime.maxMemory();
                
                if (currentMemory > maxMemory * 0.9) { // 90% of max memory
                    System.out.println("Approaching memory limit: " + 
                                     currentMemory / (1024 * 1024) + " MB");
                    break;
                }
                
                if (memoryHog.size() % 100 == 0) {
                    System.out.println("Allocated: " + memoryHog.size() + " MB");
                }
            }
            
        } catch (OutOfMemoryError e) {
            System.out.println("Memory stress test: OutOfMemoryError occurred at " + 
                             memoryHog.size() + " MB");
        } finally {
            // Clean up
            memoryHog.clear();
            System.gc();
            System.out.println("Memory cleaned up");
        }
    }
    
    private static void testThreadStress() throws InterruptedException {
        System.out.println("\n=== Stress Test: Threads ===");
        
        List<Thread> threads = new ArrayList<>();
        final AtomicInteger activeThreads = new AtomicInteger(0);
        
        try {
            // Create many threads to find the limit
            for (int i = 0; i < 10000; i++) {
                Thread thread = new Thread(() -> {
                    activeThreads.incrementAndGet();
                    try {
                        Thread.sleep(5000); // Keep thread alive
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    activeThreads.decrementAndGet();
                });
                
                thread.start();
                threads.add(thread);
                
                if (i % 100 == 0) {
                    System.out.println("Created " + (i + 1) + " threads, Active: " + 
                                     activeThreads.get());
                }
                
                // Check if we've hit a limit
                if (activeThreads.get() > 1000) {
                    System.out.println("Thread stress test: Created " + threads.size() + 
                                     " threads successfully");
                    break;
                }
            }
            
        } catch (OutOfMemoryError e) {
            System.out.println("Thread stress test: OutOfMemoryError at " + threads.size() + 
                             " threads");
        } finally {
            // Clean up threads
            for (Thread thread : threads) {
                thread.interrupt();
            }
        }
    }
    
    private static void testCpuStress() throws InterruptedException {
        System.out.println("\n=== Stress Test: CPU ===");
        
        int numCores = Runtime.getRuntime().availableProcessors();
        System.out.println("Available CPU cores: " + numCores);
        
        // Create CPU-intensive tasks
        Thread[] cpuStressThreads = new Thread[numCores * 2]; // Oversubscribe
        final AtomicBoolean running = new AtomicBoolean(true);
        
        for (int i = 0; i < cpuStressThreads.length; i++) {
            final int threadId = i;
            cpuStressThreads[i] = new Thread(() -> {
                long operations = 0;
                while (running.get()) {
                    // CPU-intensive calculation
                    Math.sqrt(Math.random() * 1000000);
                    operations++;
                    
                    if (operations % 1000000 == 0) {
                        System.out.println("Thread " + threadId + ": " + 
                                         operations + " operations");
                    }
                }
            });
            cpuStressThreads[i].start();
        }
        
        // Let it run for a while
        Thread.sleep(5000);
        
        // Stop the stress test
        running.set(false);
        
        for (Thread thread : cpuStressThreads) {
            thread.join();
        }
        
        System.out.println("CPU stress test completed");
    }
}
```

## 13.6 Chaos Testing

Chaos testing introduces random failures to test system resilience and fault tolerance.

### Key Concepts:
- **Fault injection**: Introducing deliberate failures
- **Resilience testing**: Testing system recovery capabilities
- **Random failures**: Unpredictable failure scenarios
- **System robustness**: How well system handles unexpected issues

### Example: Chaos Testing
```java
public class ParallelChaosTesting {
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Parallel Chaos Testing Demo ===");
        
        // Test random thread failures
        testRandomThreadFailures();
        
        // Test network partition simulation
        testNetworkPartition();
        
        // Test resource contention chaos
        testResourceContentionChaos();
    }
    
    private static void testRandomThreadFailures() throws InterruptedException {
        System.out.println("\n=== Chaos Test: Random Thread Failures ===");
        
        final AtomicInteger completedTasks = new AtomicInteger(0);
        final AtomicInteger failedTasks = new AtomicInteger(0);
        final Random random = new Random();
        
        Thread[] workers = new Thread[10];
        
        for (int i = 0; i < workers.length; i++) {
            final int workerId = i;
            workers[i] = new Thread(() -> {
                try {
                    // Simulate work
                    for (int j = 0; j < 100; j++) {
                        // Random failure injection
                        if (random.nextDouble() < 0.05) { // 5% failure rate
                            throw new RuntimeException("Chaos failure in worker " + workerId);
                        }
                        
                        Thread.sleep(10);
                    }
                    completedTasks.incrementAndGet();
                    System.out.println("Worker " + workerId + " completed successfully");
                    
                } catch (Exception e) {
                    failedTasks.incrementAndGet();
                    System.out.println("Worker " + workerId + " failed: " + e.getMessage());
                }
            });
            workers[i].start();
        }
        
        // Wait for all workers
        for (Thread worker : workers) {
            worker.join();
        }
        
        System.out.println("Chaos test results:");
        System.out.println("Completed tasks: " + completedTasks.get());
        System.out.println("Failed tasks: " + failedTasks.get());
        System.out.println("System resilience: " + 
                         (double) completedTasks.get() / workers.length * 100 + "%");
    }
    
    private static void testNetworkPartition() throws InterruptedException {
        System.out.println("\n=== Chaos Test: Network Partition Simulation ===");
        
        final BlockingQueue<String> nodeAToB = new LinkedBlockingQueue<>();
        final BlockingQueue<String> nodeBToA = new LinkedBlockingQueue<>();
        final AtomicBoolean networkPartition = new AtomicBoolean(false);
        final Random random = new Random();
        
        // Node A
        Thread nodeA = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    // Send message to Node B
                    if (!networkPartition.get()) {
                        nodeAToB.put("Message from A: " + i);
                        System.out.println("Node A sent message " + i);
                    } else {
                        System.out.println("Node A: Network partition detected, message " + i + " lost");
                    }
                    
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Node B
        Thread nodeB = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    String message = nodeAToB.poll(100, TimeUnit.MILLISECONDS);
                    if (message != null) {
                        System.out.println("Node B received: " + message);
                        
                        // Send acknowledgment
                        if (!networkPartition.get()) {
                            nodeBToA.put("ACK from B");
                        }
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Chaos monkey - randomly creates network partitions
        Thread chaosMonkey = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                try {
                    Thread.sleep(1000);
                    
                    // Random network partition
                    if (random.nextDouble() < 0.3) { // 30% chance
                        networkPartition.set(true);
                        System.out.println("CHAOS: Network partition created!");
                        Thread.sleep(2000);
                        networkPartition.set(false);
                        System.out.println("CHAOS: Network partition healed");
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        nodeA.start();
        nodeB.start();
        chaosMonkey.start();
        
        nodeA.join();
        
        nodeB.interrupt();
        chaosMonkey.interrupt();
        
        System.out.println("Network partition chaos test completed");
    }
    
    private static void testResourceContentionChaos() throws InterruptedException {
        System.out.println("\n=== Chaos Test: Resource Contention ===");
        
        final Object[] resources = new Object[3];
        for (int i = 0; i < resources.length; i++) {
            resources[i] = new Object();
        }
        
        final Random random = new Random();
        final AtomicInteger successfulOperations = new AtomicInteger(0);
        final AtomicInteger failedOperations = new AtomicInteger(0);
        
        Thread[] workers = new Thread[8];
        
        for (int i = 0; i < workers.length; i++) {
            final int workerId = i;
            workers[i] = new Thread(() -> {
                for (int j = 0; j < 50; j++) {
                    try {
                        // Randomly select resources to acquire
                        int resource1 = random.nextInt(resources.length);
                        int resource2 = random.nextInt(resources.length);
                        
                        // Potential deadlock scenario
                        synchronized (resources[resource1]) {
                            Thread.sleep(10); // Hold resource for some time
                            synchronized (resources[resource2]) {
                                // Do some work
                                Thread.sleep(5);
                                successfulOperations.incrementAndGet();
                            }
                        }
                        
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        failedOperations.incrementAndGet();
                    } catch (Exception e) {
                        failedOperations.incrementAndGet();
                        System.out.println("Worker " + workerId + " failed: " + e.getMessage());
                    }
                }
            });
            workers[i].start();
        }
        
        // Wait with timeout to detect deadlocks
        boolean allCompleted = true;
        for (Thread worker : workers) {
            if (!worker.join(5000)) { // 5 second timeout
                worker.interrupt();
                allCompleted = false;
            }
        }
        
        System.out.println("Resource contention chaos test results:");
        System.out.println("Successful operations: " + successfulOperations.get());
        System.out.println("Failed operations: " + failedOperations.get());
        System.out.println("All workers completed: " + allCompleted);
        
        if (!allCompleted) {
            System.out.println("WARNING: Potential deadlock detected!");
        }
    }
}
```

## 13.7 Test Data Management

Managing test data for parallel testing scenarios requires special consideration for concurrency and isolation.

### Key Concepts:
- **Test data isolation**: Ensuring tests don't interfere with each other's data
- **Concurrent data access**: Managing shared test data safely
- **Data generation**: Creating appropriate test datasets
- **Cleanup strategies**: Properly cleaning up test data

### Example: Test Data Management
```java
public class ParallelTestDataManagement {
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Test Data Management Demo ===");
        
        // Test isolated data management
        testIsolatedDataManagement();
        
        // Test shared data management
        testSharedDataManagement();
        
        // Test data cleanup
        testDataCleanup();
    }
    
    private static void testIsolatedDataManagement() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Test: Isolated Data Management ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        List<Future<Boolean>> testResults = new ArrayList<>();
        
        // Each test gets its own isolated data
        for (int i = 0; i < 4; i++) {
            final int testId = i;
            testResults.add(executor.submit(() -> {
                // Create isolated test data for this test
                TestDataSet testData = createIsolatedTestData(testId);
                
                // Perform test operations
                boolean result = performTestOperations(testData);
                
                // Cleanup test data
                cleanupTestData(testData);
                
                System.out.println("Test " + testId + " completed with isolated data");
                return result;
            }));
        }
        
        // Verify all tests passed
        boolean allPassed = true;
        for (Future<Boolean> result : testResults) {
            if (!result.get()) {
                allPassed = false;
            }
        }
        
        executor.shutdown();
        
        System.out.println("All isolated tests passed: " + allPassed);
    }
    
    private static void testSharedDataManagement() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Test: Shared Data Management ===");
        
        // Create shared test data
        SharedTestData sharedData = new SharedTestData();
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        List<Future<Boolean>> testResults = new ArrayList<>();
        
        // Multiple tests sharing the same data
        for (int i = 0; i < 4; i++) {
            final int testId = i;
            testResults.add(executor.submit(() -> {
                // Use shared data with thread-safe operations
                boolean result = performSharedDataTest(sharedData, testId);
                
                System.out.println("Test " + testId + " completed with shared data");
                return result;
            }));
        }
        
        // Verify all tests passed
        boolean allPassed = true;
        for (Future<Boolean> result : testResults) {
            if (!result.get()) {
                allPassed = false;
            }
        }
        
        executor.shutdown();
        
        System.out.println("All shared data tests passed: " + allPassed);
        System.out.println("Final shared data state: " + sharedData.getOperationCount());
    }
    
    private static void testDataCleanup() throws InterruptedException {
        System.out.println("\n=== Test: Data Cleanup ===");
        
        List<TestDataSet> createdDataSets = new ArrayList<>();
        
        try {
            // Create multiple test datasets
            for (int i = 0; i < 5; i++) {
                TestDataSet dataSet = createIsolatedTestData(i);
                createdDataSets.add(dataSet);
                System.out.println("Created test dataset " + i);
            }
            
            System.out.println("Total datasets created: " + createdDataSets.size());
            
            // Simulate some test failures
            throw new RuntimeException("Simulated test failure");
            
        } catch (Exception e) {
            System.out.println("Exception occurred: " + e.getMessage());
        } finally {
            // Cleanup all created datasets
            System.out.println("Cleaning up test datasets...");
            for (TestDataSet dataSet : createdDataSets) {
                cleanupTestData(dataSet);
            }
            System.out.println("Cleanup completed for " + createdDataSets.size() + " datasets");
        }
    }
    
    // Helper classes and methods
    static class TestDataSet {
        private final int id;
        private final List<String> data;
        
        public TestDataSet(int id) {
            this.id = id;
            this.data = new ArrayList<>();
            
            // Generate test data
            for (int i = 0; i < 100; i++) {
                data.add("TestData-" + id + "-" + i);
            }
        }
        
        public List<String> getData() {
            return data;
        }
        
        public int getId() {
            return id;
        }
    }
    
    static class SharedTestData {
        private final AtomicInteger operationCount = new AtomicInteger(0);
        private final ConcurrentHashMap<String, String> sharedMap = new ConcurrentHashMap<>();
        
        public void performOperation(String key, String value) {
            sharedMap.put(key, value);
            operationCount.incrementAndGet();
        }
        
        public String getValue(String key) {
            return sharedMap.get(key);
        }
        
        public int getOperationCount() {
            return operationCount.get();
        }
    }
    
    private static TestDataSet createIsolatedTestData(int testId) {
        return new TestDataSet(testId);
    }
    
    private static boolean performTestOperations(TestDataSet testData) {
        // Perform operations on isolated test data
        List<String> data = testData.getData();
        
        // Verify data integrity
        if (data.size() != 100) {
            return false;
        }
        
        // Perform some operations
        for (String item : data) {
            if (!item.startsWith("TestData-" + testData.getId())) {
                return false;
            }
        }
        
        return true;
    }
    
    private static boolean performSharedDataTest(SharedTestData sharedData, int testId) {
        // Perform thread-safe operations on shared data
        for (int i = 0; i < 10; i++) {
            String key = "test-" + testId + "-" + i;
            String value = "value-" + testId + "-" + i;
            
            sharedData.performOperation(key, value);
            
            // Verify the operation
            String retrievedValue = sharedData.getValue(key);
            if (!value.equals(retrievedValue)) {
                return false;
            }
        }
        
        return true;
    }
    
    private static void cleanupTestData(TestDataSet testData) {
        // Simulate cleanup operations
        testData.getData().clear();
        System.out.println("Cleaned up test data for test " + testData.getId());
    }
}
```

## 13.8 Testing Tools

Various tools are available for testing parallel systems, each with specific capabilities and use cases.

### Key Concepts:
- **Unit testing frameworks**: JUnit, TestNG for Java
- **Load testing tools**: JMeter, Gatling for performance testing
- **Monitoring tools**: Profilers and system monitors
- **Specialized tools**: Tools designed for parallel system testing

### Example: Custom Testing Framework
```java
public class ParallelTestingTools {
    
    public static void main(String[] args) {
        System.out.println("=== Parallel Testing Tools Demo ===");
        
        // Custom test runner
        ParallelTestRunner testRunner = new ParallelTestRunner();
        
        // Add test cases
        testRunner.addTest("BasicFunctionality", ParallelTestingTools::testBasicFunctionality);
        testRunner.addTest("ThreadSafety", ParallelTestingTools::testThreadSafety);
        testRunner.addTest("Performance", ParallelTestingTools::testPerformance);
        testRunner.addTest("LoadTest", ParallelTestingTools::testLoad);
        
        // Run all tests
        testRunner.runAllTests();
        
        // Print results
        testRunner.printResults();
    }
    
    // Test framework implementation
    static class ParallelTestRunner {
        private final Map<String, TestCase> tests = new LinkedHashMap<>();
        private final Map<String, TestResult> results = new HashMap<>();
        
        public void addTest(String name, TestCase test) {
            tests.put(name, test);
        }
        
        public void runAllTests() {
            System.out.println("Running " + tests.size() + " tests...");
            
            for (Map.Entry<String, TestCase> entry : tests.entrySet()) {
                String testName = entry.getKey();
                TestCase test = entry.getValue();
                
                System.out.println("Running test: " + testName);
                
                long startTime = System.currentTimeMillis();
                boolean passed = false;
                String errorMessage = null;
                
                try {
                    passed = test.run();
                } catch (Exception e) {
                    errorMessage = e.getMessage();
                }
                
                long endTime = System.currentTimeMillis();
                long duration = endTime - startTime;
                
                results.put(testName, new TestResult(passed, duration, errorMessage));
            }
        }
        
        public void printResults() {
            System.out.println("\n=== Test Results ===");
            
            int passed = 0;
            int failed = 0;
            long totalTime = 0;
            
            for (Map.Entry<String, TestResult> entry : results.entrySet()) {
                String testName = entry.getKey();
                TestResult result = entry.getValue();
                
                String status = result.passed ? "PASS" : "FAIL";
                System.out.println(testName + ": " + status + " (" + result.duration + "ms)");
                
                if (result.errorMessage != null) {
                    System.out.println("  Error: " + result.errorMessage);
                }
                
                if (result.passed) {
                    passed++;
                } else {
                    failed++;
                }
                
                totalTime += result.duration;
            }
            
            System.out.println("\nSummary:");
            System.out.println("Total tests: " + (passed + failed));
            System.out.println("Passed: " + passed);
            System.out.println("Failed: " + failed);
            System.out.println("Total time: " + totalTime + "ms");
        }
    }
    
    @FunctionalInterface
    interface TestCase {
        boolean run() throws Exception;
    }
    
    static class TestResult {
        final boolean passed;
        final long duration;
        final String errorMessage;
        
        TestResult(boolean passed, long duration, String errorMessage) {
            this.passed = passed;
            this.duration = duration;
            this.errorMessage = errorMessage;
        }
    }
    
    // Test implementations
    private static boolean testBasicFunctionality() {
        int[] data = {1, 2, 3, 4, 5};
        int sum = Arrays.stream(data).sum();
        return sum == 15;
    }
    
    private static boolean testThreadSafety() throws InterruptedException {
        final AtomicInteger counter = new AtomicInteger(0);
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
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
        
        return counter.get() == 10000;
    }
    
    private static boolean testPerformance() {
        long startTime = System.currentTimeMillis();
        
        int[] data = new int[1000000];
        Arrays.fill(data, 1);
        Arrays.stream(data).parallel().sum();
        
        long duration = System.currentTimeMillis() - startTime;
        return duration < 1000; // Should complete within 1 second
    }
    
    private static boolean testLoad() throws InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newFixedThreadPool(50);
        List<Future<Boolean>> futures = new ArrayList<>();
        
        // Submit 100 concurrent tasks
        for (int i = 0; i < 100; i++) {
            futures.add(executor.submit(() -> {
                // Simulate work
                Thread.sleep(100);
                return true;
            }));
        }
        
        // Check all tasks completed successfully
        boolean allPassed = true;
        for (Future<Boolean> future : futures) {
            if (!future.get()) {
                allPassed = false;
            }
        }
        
        executor.shutdown();
        return allPassed;
    }
}
```

## 13.9 Testing Best Practices

Best practices for testing parallel systems help ensure thorough and reliable testing.

### Key Concepts:
- **Test isolation**: Keep tests independent
- **Deterministic testing**: Make tests predictable
- **Comprehensive coverage**: Test all scenarios
- **Continuous testing**: Integrate testing into development workflow

### Example: Testing Best Practices
```java
public class ParallelTestingBestPractices {
    
    public static void main(String[] args) {
        System.out.println("=== Parallel Testing Best Practices Demo ===");
        
        // Best Practice 1: Test isolation
        demonstrateTestIsolation();
        
        // Best Practice 2: Deterministic testing
        demonstrateDeterministicTesting();
        
        // Best Practice 3: Comprehensive coverage
        demonstrateComprehensiveCoverage();
    }
    
    private static void demonstrateTestIsolation() {
        System.out.println("\n=== Best Practice 1: Test Isolation ===");
        
        // Each test should be independent
        boolean test1 = isolatedTest1();
        boolean test2 = isolatedTest2();
        boolean test3 = isolatedTest3();
        
        System.out.println("Test 1: " + (test1 ? "PASS" : "FAIL"));
        System.out.println("Test 2: " + (test2 ? "PASS" : "FAIL"));
        System.out.println("Test 3: " + (test3 ? "PASS" : "FAIL"));
        
        System.out.println("All tests are isolated and independent");
    }
    
    private static void demonstrateDeterministicTesting() {
        System.out.println("\n=== Best Practice 2: Deterministic Testing ===");
        
        // Use fixed seeds and controlled conditions
        Random fixedRandom = new Random(12345); // Fixed seed
        
        // Test should produce same results every time
        for (int run = 0; run < 3; run++) {
            fixedRandom.setSeed(12345); // Reset seed
            
            int[] data = new int[10];
            for (int i = 0; i < data.length; i++) {
                data[i] = fixedRandom.nextInt(100);
            }
            
            int sum = Arrays.stream(data).sum();
            System.out.println("Run " + (run + 1) + " sum: " + sum);
        }
        
        System.out.println("Deterministic testing ensures consistent results");
    }
    
    private static void demonstrateComprehensiveCoverage() {
        System.out.println("\n=== Best Practice 3: Comprehensive Coverage ===");
        
        System.out.println("Testing scenarios:");
        System.out.println("1. Normal operation");
        System.out.println("2. Edge cases");
        System.out.println("3. Error conditions");
        System.out.println("4. Performance limits");
        System.out.println("5. Concurrent access");
        System.out.println("6. Resource constraints");
        
        // Example comprehensive test
        boolean normalTest = testNormalOperation();
        boolean edgeTest = testEdgeCases();
        boolean errorTest = testErrorConditions();
        boolean performanceTest = testPerformanceLimits();
        boolean concurrencyTest = testConcurrentAccess();
        boolean resourceTest = testResourceConstraints();
        
        System.out.println("\nTest Results:");
        System.out.println("Normal operation: " + (normalTest ? "PASS" : "FAIL"));
        System.out.println("Edge cases: " + (edgeTest ? "PASS" : "FAIL"));
        System.out.println("Error conditions: " + (errorTest ? "PASS" : "FAIL"));
        System.out.println("Performance limits: " + (performanceTest ? "PASS" : "FAIL"));
        System.out.println("Concurrent access: " + (concurrencyTest ? "PASS" : "FAIL"));
        System.out.println("Resource constraints: " + (resourceTest ? "PASS" : "FAIL"));
    }
    
    // Helper methods for best practices
    private static boolean isolatedTest1() {
        // Test with its own data and resources
        int[] localData = {1, 2, 3};
        return Arrays.stream(localData).sum() == 6;
    }
    
    private static boolean isolatedTest2() {
        // Independent test with different data
        List<String> localList = Arrays.asList("a", "b", "c");
        return localList.size() == 3;
    }
    
    private static boolean isolatedTest3() {
        // Another independent test
        Map<String, Integer> localMap = new HashMap<>();
        localMap.put("key", 42);
        return localMap.get("key") == 42;
    }
    
    private static boolean testNormalOperation() {
        // Test typical use case
        return true;
    }
    
    private static boolean testEdgeCases() {
        // Test boundary conditions
        return true;
    }
    
    private static boolean testErrorConditions() {
        // Test error handling
        return true;
    }
    
    private static boolean testPerformanceLimits() {
        // Test performance boundaries
        return true;
    }
    
    private static boolean testConcurrentAccess() {
        // Test thread safety
        return true;
    }
    
    private static boolean testResourceConstraints() {
        // Test with limited resources
        return true;
    }
}
```

## 13.10 Test Automation

Automating parallel tests ensures consistent execution and enables continuous integration.

### Key Concepts:
- **Automated test execution**: Running tests without manual intervention
- **Continuous integration**: Integrating tests into build pipeline
- **Test scheduling**: Running tests at appropriate times
- **Result reporting**: Automated reporting of test results

### Example: Test Automation Framework
```java
public class ParallelTestAutomation {
    
    public static void main(String[] args) {
        System.out.println("=== Parallel Test Automation Demo ===");
        
        // Create automation framework
        TestAutomationFramework framework = new TestAutomationFramework();
        
        // Configure test suites
        framework.addTestSuite("Unit Tests", createUnitTestSuite());
        framework.addTestSuite("Integration Tests", createIntegrationTestSuite());
        framework.addTestSuite("Performance Tests", createPerformanceTestSuite());
        
        // Run automated tests
        framework.runAllTestSuites();
        
        // Generate reports
        framework.generateReports();
    }
    
    static class TestAutomationFramework {
        private final Map<String, TestSuite> testSuites = new LinkedHashMap<>();
        private final Map<String, TestSuiteResult> results = new HashMap<>();
        
        public void addTestSuite(String name, TestSuite suite) {
            testSuites.put(name, suite);
        }
        
        public void runAllTestSuites() {
            System.out.println("Starting automated test execution...");
            
            for (Map.Entry<String, TestSuite> entry : testSuites.entrySet()) {
                String suiteName = entry.getKey();
                TestSuite suite = entry.getValue();
                
                System.out.println("\nRunning test suite: " + suiteName);
                TestSuiteResult result = suite.run();
                results.put(suiteName, result);
                
                System.out.println("Suite " + suiteName + " completed: " + 
                                 result.passed + "/" + result.total + " tests passed");
            }
        }
        
        public void generateReports() {
            System.out.println("\n=== Automated Test Report ===");
            
            int totalTests = 0;
            int totalPassed = 0;
            long totalTime = 0;
            
            for (Map.Entry<String, TestSuiteResult> entry : results.entrySet()) {
                String suiteName = entry.getKey();
                TestSuiteResult result = entry.getValue();
                
                System.out.println("\nTest Suite: " + suiteName);
                System.out.println("Tests: " + result.total);
                System.out.println("Passed: " + result.passed);
                System.out.println("Failed: " + (result.total - result.passed));
                System.out.println("Duration: " + result.duration + "ms");
                System.out.println("Success Rate: " + 
                                 (double) result.passed / result.total * 100 + "%");
                
                totalTests += result.total;
                totalPassed += result.passed;
                totalTime += result.duration;
            }
            
            System.out.println("\n=== Overall Summary ===");
            System.out.println("Total Test Suites: " + testSuites.size());
            System.out.println("Total Tests: " + totalTests);
            System.out.println("Total Passed: " + totalPassed);
            System.out.println("Total Failed: " + (totalTests - totalPassed));
            System.out.println("Overall Success Rate: " + 
                             (double) totalPassed / totalTests * 100 + "%");
            System.out.println("Total Execution Time: " + totalTime + "ms");
            
            // Determine if build should pass or fail
            double successRate = (double) totalPassed / totalTests;
            if (successRate >= 0.95) { // 95% threshold
                System.out.println("BUILD STATUS: PASS");
            } else {
                System.out.println("BUILD STATUS: FAIL");
            }
        }
    }
    
    static class TestSuite {
        private final List<AutomatedTest> tests = new ArrayList<>();
        
        public void addTest(String name, TestExecutor executor) {
            tests.add(new AutomatedTest(name, executor));
        }
        
        public TestSuiteResult run() {
            int passed = 0;
            long startTime = System.currentTimeMillis();
            
            for (AutomatedTest test : tests) {
                boolean result = test.run();
                if (result) {
                    passed++;
                }
            }
            
            long duration = System.currentTimeMillis() - startTime;
            return new TestSuiteResult(tests.size(), passed, duration);
        }
    }
    
    static class AutomatedTest {
        private final String name;
        private final TestExecutor executor;
        
        public AutomatedTest(String name, TestExecutor executor) {
            this.name = name;
            this.executor = executor;
        }
        
        public boolean run() {
            try {
                return executor.execute();
            } catch (Exception e) {
                System.out.println("Test " + name + " failed with exception: " + e.getMessage());
                return false;
            }
        }
    }
    
    static class TestSuiteResult {
        final int total;
        final int passed;
        final long duration;
        
        TestSuiteResult(int total, int passed, long duration) {
            this.total = total;
            this.passed = passed;
            this.duration = duration;
        }
    }
    
    @FunctionalInterface
    interface TestExecutor {
        boolean execute() throws Exception;
    }
    
    // Test suite creation methods
    private static TestSuite createUnitTestSuite() {
        TestSuite suite = new TestSuite();
        
        suite.addTest("Basic Math", () -> {
            return 2 + 2 == 4;
        });
        
        suite.addTest("Array Sum", () -> {
            int[] arr = {1, 2, 3, 4, 5};
            return Arrays.stream(arr).sum() == 15;
        });
        
        suite.addTest("String Operations", () -> {
            String str = "Hello World";
            return str.length() == 11 && str.contains("World");
        });
        
        return suite;
    }
    
    private static TestSuite createIntegrationTestSuite() {
        TestSuite suite = new TestSuite();
        
        suite.addTest("Producer Consumer", () -> {
            BlockingQueue<String> queue = new LinkedBlockingQueue<>();
            
            // Producer
            CompletableFuture<Void> producer = CompletableFuture.runAsync(() -> {
                try {
                    for (int i = 0; i < 5; i++) {
                        queue.put("Item " + i);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            
            // Consumer
            CompletableFuture<Integer> consumer = CompletableFuture.supplyAsync(() -> {
                int count = 0;
                try {
                    while (count < 5) {
                        queue.take();
                        count++;
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                return count;
            });
            
            CompletableFuture.allOf(producer, consumer).join();
            return consumer.join() == 5;
        });
        
        suite.addTest("Parallel Processing", () -> {
            List<Integer> data = Arrays.asList(1, 2, 3, 4, 5);
            int parallelSum = data.parallelStream().mapToInt(Integer::intValue).sum();
            return parallelSum == 15;
        });
        
        return suite;
    }
    
    private static TestSuite createPerformanceTestSuite() {
        TestSuite suite = new TestSuite();
        
        suite.addTest("Large Array Processing", () -> {
            int[] largeArray = new int[1000000];
            Arrays.fill(largeArray, 1);
            
            long startTime = System.currentTimeMillis();
            int sum = Arrays.stream(largeArray).parallel().sum();
            long duration = System.currentTimeMillis() - startTime;
            
            return sum == 1000000 && duration < 1000; // Should complete within 1 second
        });
        
        suite.addTest("Concurrent Access", () -> {
            final AtomicInteger counter = new AtomicInteger(0);
            final int numThreads = 10;
            final int incrementsPerThread = 1000;
            
            Thread[] threads = new Thread[numThreads];
            for (int i = 0; i < numThreads; i++) {
                threads[i] = new Thread(() -> {
                    for (int j = 0; j < incrementsPerThread; j++) {
                        counter.incrementAndGet();
                    }
                });
            }
            
            long startTime = System.currentTimeMillis();
            for (Thread thread : threads) {
                thread.start();
            }
            
            for (Thread thread : threads) {
                try {
                    thread.join();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return false;
                }
            }
            
            long duration = System.currentTimeMillis() - startTime;
            
            return counter.get() == numThreads * incrementsPerThread && duration < 2000;
        });
        
        return suite;
    }
}
```

This comprehensive section covers all aspects of parallel testing, from basic challenges to advanced automation techniques, with practical examples and real-world analogies to help understand these complex concepts from the ground up.