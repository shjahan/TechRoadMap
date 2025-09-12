# Section 9 - Producer-Consumer Patterns

## 9.1 Producer-Consumer Fundamentals

The producer-consumer pattern is a classic design pattern where one or more threads (producers) generate data and place it in a shared buffer, while one or more threads (consumers) remove and process that data. This pattern is fundamental to many concurrent systems.

### Key Concepts:

**1. Decoupling:**
- Producers and consumers are independent
- No direct communication between them
- Buffer acts as intermediary

**2. Synchronization:**
- Thread-safe buffer access
- Proper coordination between threads
- Handle empty/full buffer conditions

**3. Scalability:**
- Multiple producers and consumers
- Load balancing
- Performance optimization

### Java Example - Basic Producer-Consumer:

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ProducerConsumerFundamentals {
    private final BlockingQueue<String> buffer = new LinkedBlockingQueue<>(10);
    private final ExecutorService executor = Executors.newFixedThreadPool(6);
    
    public void demonstrateBasicPattern() throws InterruptedException {
        // Create producers
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 10; j++) {
                        String item = "Producer-" + producerId + "-Item-" + j;
                        buffer.put(item);
                        System.out.println("Produced: " + item);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Create consumers
        for (int i = 0; i < 3; i++) {
            final int consumerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 10; j++) {
                        String item = buffer.take();
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
        ProducerConsumerFundamentals example = new ProducerConsumerFundamentals();
        example.demonstrateBasicPattern();
    }
}
```

### Real-World Analogy:
Think of the producer-consumer pattern like a restaurant:
- **Producers**: Like chefs who prepare dishes
- **Consumers**: Like waiters who serve dishes to customers
- **Buffer**: Like the kitchen pass where dishes are placed
- **Synchronization**: Like the system that ensures dishes don't pile up or run out

## 9.2 Blocking Queue Pattern

The blocking queue pattern uses thread-safe queues that block when trying to add to a full queue or remove from an empty queue. This provides automatic synchronization.

### Key Features:

**1. Automatic Blocking:**
- put() blocks when queue is full
- take() blocks when queue is empty
- No manual synchronization needed

**2. Thread Safety:**
- Built-in thread safety
- No race conditions
- Atomic operations

**3. Backpressure:**
- Natural flow control
- Prevents memory overflow
- Automatic load balancing

### Java Example - Blocking Queue Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class BlockingQueuePattern {
    private final BlockingQueue<String> queue = new ArrayBlockingQueue<>(5);
    private final AtomicInteger producedCount = new AtomicInteger(0);
    private final AtomicInteger consumedCount = new AtomicInteger(0);
    
    public void demonstrateBlockingQueue() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Producer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 20; i++) {
                    String item = "Item-" + i;
                    queue.put(item);
                    producedCount.incrementAndGet();
                    System.out.println("Produced: " + item + " (Queue size: " + queue.size() + ")");
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 20; i++) {
                    String item = queue.take();
                    consumedCount.incrementAndGet();
                    System.out.println("Consumed: " + item + " (Queue size: " + queue.size() + ")");
                    Thread.sleep(150);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Produced: " + producedCount.get() + ", Consumed: " + consumedCount.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        BlockingQueuePattern example = new BlockingQueuePattern();
        example.demonstrateBlockingQueue();
    }
}
```

## 9.3 Bounded Buffer Pattern

The bounded buffer pattern uses a fixed-size buffer to store items between producers and consumers. It prevents memory issues and provides natural backpressure.

### Key Features:

**1. Fixed Capacity:**
- Predefined buffer size
- Memory usage control
- Predictable resource usage

**2. Circular Buffer:**
- Efficient memory usage
- Wraps around when full
- Constant time operations

**3. Synchronization:**
- Proper coordination
- Handle full/empty conditions
- Thread-safe access

### Java Example - Bounded Buffer Implementation:

```java
import java.util.concurrent.locks.*;
import java.util.concurrent.atomic.AtomicInteger;

public class BoundedBufferPattern {
    private final String[] buffer;
    private final int capacity;
    private final AtomicInteger count = new AtomicInteger(0);
    private final AtomicInteger putIndex = new AtomicInteger(0);
    private final AtomicInteger takeIndex = new AtomicInteger(0);
    private final Lock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();
    
    public BoundedBufferPattern(int capacity) {
        this.capacity = capacity;
        this.buffer = new String[capacity];
    }
    
    public void put(String item) throws InterruptedException {
        lock.lock();
        try {
            while (count.get() == capacity) {
                notFull.await();
            }
            
            buffer[putIndex.get()] = item;
            putIndex.set((putIndex.get() + 1) % capacity);
            count.incrementAndGet();
            
            notEmpty.signal();
        } finally {
            lock.unlock();
        }
    }
    
    public String take() throws InterruptedException {
        lock.lock();
        try {
            while (count.get() == 0) {
                notEmpty.await();
            }
            
            String item = buffer[takeIndex.get()];
            takeIndex.set((takeIndex.get() + 1) % capacity);
            count.decrementAndGet();
            
            notFull.signal();
            return item;
        } finally {
            lock.unlock();
        }
    }
    
    public int size() {
        return count.get();
    }
    
    public static void main(String[] args) throws InterruptedException {
        BoundedBufferPattern buffer = new BoundedBufferPattern(5);
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Producer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 20; i++) {
                    String item = "Item-" + i;
                    buffer.put(item);
                    System.out.println("Produced: " + item + " (Buffer size: " + buffer.size() + ")");
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Consumer
        executor.submit(() -> {
            try {
                for (int i = 0; i < 20; i++) {
                    String item = buffer.take();
                    System.out.println("Consumed: " + item + " (Buffer size: " + buffer.size() + ")");
                    Thread.sleep(150);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
}
```

## 9.4 Work Queue Pattern

The work queue pattern uses a queue to distribute work items among multiple worker threads. It's commonly used in thread pools and task processing systems.

### Key Features:

**1. Work Distribution:**
- Tasks queued for processing
- Workers pull tasks from queue
- Load balancing

**2. Scalability:**
- Add/remove workers dynamically
- Handle varying workloads
- Performance scaling

**3. Fault Tolerance:**
- Workers can fail independently
- Tasks can be retried
- Graceful degradation

### Java Example - Work Queue Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class WorkQueuePattern {
    private final BlockingQueue<Task> workQueue = new LinkedBlockingQueue<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    private final AtomicInteger completedTasks = new AtomicInteger(0);
    
    public void demonstrateWorkQueue() throws InterruptedException {
        // Start workers
        for (int i = 0; i < 4; i++) {
            final int workerId = i;
            executor.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        Task task = workQueue.take();
                        processTask(workerId, task);
                        completedTasks.incrementAndGet();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }
        
        // Submit tasks
        for (int i = 0; i < 20; i++) {
            workQueue.put(new Task("Task-" + i, 1000 + (int)(Math.random() * 2000)));
        }
        
        // Wait for completion
        while (completedTasks.get() < 20) {
            Thread.sleep(100);
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void processTask(int workerId, Task task) {
        System.out.println("Worker " + workerId + " processing " + task.getName());
        try {
            Thread.sleep(task.getDuration());
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println("Worker " + workerId + " completed " + task.getName());
    }
    
    private static class Task {
        private final String name;
        private final long duration;
        
        public Task(String name, long duration) {
            this.name = name;
            this.duration = duration;
        }
        
        public String getName() { return name; }
        public long getDuration() { return duration; }
    }
    
    public static void main(String[] args) throws InterruptedException {
        WorkQueuePattern example = new WorkQueuePattern();
        example.demonstrateWorkQueue();
    }
}
```

## 9.5 Pipeline Pattern

The pipeline pattern processes data through a series of stages, where each stage performs a specific transformation. Data flows through the pipeline sequentially.

### Key Features:

**1. Sequential Processing:**
- Data flows through stages
- Each stage transforms data
- Ordered processing

**2. Parallel Stages:**
- Multiple instances of each stage
- Parallel processing within stage
- Load balancing

**3. Backpressure:**
- Handle varying processing speeds
- Buffer between stages
- Flow control

### Java Example - Pipeline Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class PipelinePattern {
    private final BlockingQueue<String> stage1Queue = new LinkedBlockingQueue<>();
    private final BlockingQueue<String> stage2Queue = new LinkedBlockingQueue<>();
    private final BlockingQueue<String> stage3Queue = new LinkedBlockingQueue<>();
    private final ExecutorService executor = Executors.newFixedThreadPool(6);
    
    public void demonstratePipeline() throws InterruptedException {
        // Stage 1: Input processing
        for (int i = 0; i < 2; i++) {
            final int workerId = i;
            executor.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        String item = stage1Queue.take();
                        String processed = processStage1(workerId, item);
                        stage2Queue.put(processed);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }
        
        // Stage 2: Transformation
        for (int i = 0; i < 2; i++) {
            final int workerId = i;
            executor.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        String item = stage2Queue.take();
                        String processed = processStage2(workerId, item);
                        stage3Queue.put(processed);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }
        
        // Stage 3: Output processing
        for (int i = 0; i < 2; i++) {
            final int workerId = i;
            executor.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        String item = stage3Queue.take();
                        processStage3(workerId, item);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
        }
        
        // Submit input data
        for (int i = 0; i < 10; i++) {
            stage1Queue.put("Input-" + i);
        }
        
        Thread.sleep(5000);
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private String processStage1(int workerId, String item) throws InterruptedException {
        System.out.println("Stage1-Worker" + workerId + " processing: " + item);
        Thread.sleep(500);
        return item + "-Stage1";
    }
    
    private String processStage2(int workerId, String item) throws InterruptedException {
        System.out.println("Stage2-Worker" + workerId + " processing: " + item);
        Thread.sleep(300);
        return item + "-Stage2";
    }
    
    private void processStage3(int workerId, String item) throws InterruptedException {
        System.out.println("Stage3-Worker" + workerId + " processing: " + item);
        Thread.sleep(200);
        System.out.println("Final output: " + item + "-Stage3");
    }
    
    public static void main(String[] args) throws InterruptedException {
        PipelinePattern example = new PipelinePattern();
        example.demonstratePipeline();
    }
}
```

## 9.6 Scatter-Gather Pattern

The scatter-gather pattern distributes work to multiple workers and then collects the results. It's useful for parallel processing and aggregation.

### Key Features:

**1. Scatter Phase:**
- Distribute work to workers
- Parallel processing
- Load balancing

**2. Gather Phase:**
- Collect results from workers
- Aggregate data
- Handle partial results

**3. Coordination:**
- Synchronize scatter and gather
- Handle worker failures
- Timeout handling

### Java Example - Scatter-Gather Pattern:

```java
import java.util.concurrent.*;
import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicInteger;

public class ScatterGatherPattern {
    private final ExecutorService executor = Executors.newFixedThreadPool(6);
    private final AtomicInteger completedWorkers = new AtomicInteger(0);
    
    public void demonstrateScatterGather() throws InterruptedException {
        // Scatter phase
        List<CompletableFuture<String>> futures = scatterWork();
        
        // Gather phase
        String result = gatherResults(futures);
        
        System.out.println("Final result: " + result);
    }
    
    private List<CompletableFuture<String>> scatterWork() {
        List<CompletableFuture<String>> futures = new ArrayList<>();
        
        for (int i = 0; i < 5; i++) {
            final int workerId = i;
            CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
                try {
                    Thread.sleep(1000 + (int)(Math.random() * 2000));
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                return "Result from worker " + workerId;
            }, executor);
            
            futures.add(future);
        }
        
        return futures;
    }
    
    private String gatherResults(List<CompletableFuture<String>> futures) throws InterruptedException {
        StringBuilder result = new StringBuilder();
        
        for (CompletableFuture<String> future : futures) {
            try {
                String workerResult = future.get(5, TimeUnit.SECONDS);
                result.append(workerResult).append("; ");
            } catch (TimeoutException e) {
                System.out.println("Worker timed out");
            } catch (ExecutionException e) {
                System.out.println("Worker failed: " + e.getCause().getMessage());
            }
        }
        
        return result.toString();
    }
    
    public static void main(String[] args) throws InterruptedException {
        ScatterGatherPattern example = new ScatterGatherPattern();
        example.demonstrateScatterGather();
    }
}
```

## 9.7 Map-Reduce Pattern

The map-reduce pattern processes large datasets by mapping data to key-value pairs and then reducing them to a final result. It's the foundation of many big data processing systems.

### Key Features:

**1. Map Phase:**
- Transform input data
- Generate key-value pairs
- Parallel processing

**2. Shuffle Phase:**
- Group by key
- Distribute to reducers
- Network communication

**3. Reduce Phase:**
- Aggregate values by key
- Generate final result
- Parallel processing

### Java Example - Map-Reduce Pattern:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.stream.Collectors;

public class MapReducePattern {
    private final ExecutorService executor = Executors.newFixedThreadPool(8);
    
    public void demonstrateMapReduce() throws InterruptedException {
        // Input data
        List<String> words = Arrays.asList(
            "hello world", "hello java", "world of java",
            "concurrent programming", "java multithreading"
        );
        
        // Map phase
        List<CompletableFuture<Map<String, Integer>>> mapFutures = words.stream()
            .map(word -> CompletableFuture.supplyAsync(() -> map(word), executor))
            .collect(Collectors.toList());
        
        // Wait for map phase
        CompletableFuture<Void> allMaps = CompletableFuture.allOf(
            mapFutures.toArray(new CompletableFuture[0])
        );
        allMaps.get();
        
        // Collect map results
        Map<String, Integer> wordCounts = new HashMap<>();
        for (CompletableFuture<Map<String, Integer>> future : mapFutures) {
            Map<String, Integer> result = future.get();
            for (Map.Entry<String, Integer> entry : result.entrySet()) {
                wordCounts.merge(entry.getKey(), entry.getValue(), Integer::sum);
            }
        }
        
        // Reduce phase
        Map<String, Integer> finalResult = reduce(wordCounts);
        
        System.out.println("Word counts: " + finalResult);
    }
    
    private Map<String, Integer> map(String text) {
        Map<String, Integer> wordCounts = new HashMap<>();
        String[] words = text.toLowerCase().split("\\s+");
        
        for (String word : words) {
            wordCounts.put(word, wordCounts.getOrDefault(word, 0) + 1);
        }
        
        System.out.println("Mapped: " + text + " -> " + wordCounts);
        return wordCounts;
    }
    
    private Map<String, Integer> reduce(Map<String, Integer> wordCounts) {
        // In a real implementation, this would be distributed
        System.out.println("Reducing: " + wordCounts);
        return wordCounts;
    }
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        MapReducePattern example = new MapReducePattern();
        example.demonstrateMapReduce();
    }
}
```

## 9.8 Fork-Join Pattern

The fork-join pattern recursively splits work into smaller pieces, processes them in parallel, and then combines the results. It's ideal for divide-and-conquer algorithms.

### Key Features:

**1. Recursive Decomposition:**
- Split work into smaller pieces
- Process recursively
- Base case handling

**2. Parallel Processing:**
- Process pieces in parallel
- Work-stealing algorithm
- Load balancing

**3. Result Combination:**
- Combine partial results
- Hierarchical aggregation
- Final result

### Java Example - Fork-Join Pattern:

```java
import java.util.concurrent.*;

public class ForkJoinPattern {
    private final ForkJoinPool forkJoinPool = new ForkJoinPool();
    
    public void demonstrateForkJoin() throws InterruptedException {
        // Calculate sum of numbers using fork-join
        int[] numbers = new int[1000];
        for (int i = 0; i < numbers.length; i++) {
            numbers[i] = i + 1;
        }
        
        SumTask task = new SumTask(numbers, 0, numbers.length);
        int result = forkJoinPool.invoke(task);
        
        System.out.println("Sum of numbers 1-1000: " + result);
    }
    
    private static class SumTask extends RecursiveTask<Integer> {
        private final int[] array;
        private final int start;
        private final int end;
        private static final int THRESHOLD = 100;
        
        public SumTask(int[] array, int start, int end) {
            this.array = array;
            this.start = start;
            this.end = end;
        }
        
        @Override
        protected Integer compute() {
            if (end - start <= THRESHOLD) {
                // Base case: compute sum directly
                int sum = 0;
                for (int i = start; i < end; i++) {
                    sum += array[i];
                }
                return sum;
            } else {
                // Fork: split into two subtasks
                int mid = (start + end) / 2;
                SumTask leftTask = new SumTask(array, start, mid);
                SumTask rightTask = new SumTask(array, mid, end);
                
                // Fork both tasks
                leftTask.fork();
                rightTask.fork();
                
                // Join: combine results
                return leftTask.join() + rightTask.join();
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ForkJoinPattern example = new ForkJoinPattern();
        example.demonstrateForkJoin();
    }
}
```

## 9.9 Work-Stealing Pattern

The work-stealing pattern allows idle threads to steal work from busy threads. It's used in fork-join frameworks to improve load balancing.

### Key Features:

**1. Work Stealing:**
- Idle threads steal work
- Load balancing
- Better utilization

**2. Double-Ended Queues:**
- LIFO for local work
- FIFO for stealing
- Efficient operations

**3. Load Balancing:**
- Automatic load distribution
- Adapts to workload
- Reduces contention

### Java Example - Work-Stealing Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class WorkStealingPattern {
    private final ForkJoinPool workStealingPool = new ForkJoinPool();
    private final AtomicInteger stolenWork = new AtomicInteger(0);
    
    public void demonstrateWorkStealing() throws InterruptedException {
        // Create tasks with varying workloads
        List<CompletableFuture<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> {
                return processTask(taskId);
            }, workStealingPool);
            futures.add(future);
        }
        
        // Wait for all tasks to complete
        CompletableFuture<Void> allTasks = CompletableFuture.allOf(
            futures.toArray(new CompletableFuture[0])
        );
        allTasks.get();
        
        System.out.println("Total stolen work: " + stolenWork.get());
    }
    
    private int processTask(int taskId) {
        // Simulate varying workload
        int work = 1000 + (int)(Math.random() * 2000);
        
        for (int i = 0; i < work; i++) {
            // Simulate work
            Math.sqrt(i);
        }
        
        System.out.println("Task " + taskId + " completed");
        return work;
    }
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        WorkStealingPattern example = new WorkStealingPattern();
        example.demonstrateWorkStealing();
    }
}
```

## 9.10 Producer-Consumer Best Practices

Following best practices ensures efficient, maintainable, and robust producer-consumer implementations.

### Best Practices:

**1. Proper Synchronization:**
- Use thread-safe data structures
- Handle empty/full conditions
- Avoid deadlocks

**2. Error Handling:**
- Handle exceptions gracefully
- Implement retry mechanisms
- Monitor for failures

**3. Performance:**
- Choose appropriate queue size
- Balance producers and consumers
- Monitor performance metrics

### Java Example - Best Practices:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicBoolean;

public class ProducerConsumerBestPractices {
    private final BlockingQueue<String> queue = new LinkedBlockingQueue<>(10);
    private final AtomicInteger producedCount = new AtomicInteger(0);
    private final AtomicInteger consumedCount = new AtomicInteger(0);
    private final AtomicBoolean running = new AtomicBoolean(true);
    private final ExecutorService executor = Executors.newFixedThreadPool(6);
    
    public void demonstrateBestPractices() throws InterruptedException {
        // Start producers
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            executor.submit(() -> {
                try {
                    while (running.get()) {
                        String item = "Producer-" + producerId + "-Item-" + producedCount.incrementAndGet();
                        if (queue.offer(item, 1, TimeUnit.SECONDS)) {
                            System.out.println("Produced: " + item);
                        } else {
                            System.out.println("Producer " + producerId + " timeout");
                        }
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Start consumers
        for (int i = 0; i < 3; i++) {
            final int consumerId = i;
            executor.submit(() -> {
                try {
                    while (running.get()) {
                        String item = queue.poll(1, TimeUnit.SECONDS);
                        if (item != null) {
                            consumedCount.incrementAndGet();
                            System.out.println("Consumer-" + consumerId + " consumed: " + item);
                        }
                        Thread.sleep(150);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Run for 10 seconds
        Thread.sleep(10000);
        running.set(false);
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Produced: " + producedCount.get() + ", Consumed: " + consumedCount.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ProducerConsumerBestPractices example = new ProducerConsumerBestPractices();
        example.demonstrateBestPractices();
    }
}
```

### Real-World Analogy:
Think of producer-consumer patterns like different types of manufacturing systems:
- **Blocking Queue**: Like an assembly line with a conveyor belt that stops when full
- **Bounded Buffer**: Like a warehouse with limited storage space
- **Work Queue**: Like a job board where workers pick up tasks
- **Pipeline**: Like a car assembly line with different stations
- **Scatter-Gather**: Like a restaurant kitchen where orders are split among chefs and then combined
- **Map-Reduce**: Like a data processing factory that breaks down large tasks
- **Fork-Join**: Like a construction project that divides work into smaller tasks
- **Work-Stealing**: Like a flexible team where idle workers help busy ones

Each pattern has its place depending on the specific requirements of your system!