# Section 20 - Multithreading Patterns

## 20.1 Common Multithreading Patterns

Multithreading patterns are proven solutions to common concurrency problems. They provide reusable templates for designing thread-safe and efficient concurrent systems.

### Key Patterns:

**1. Creational Patterns:**
- Thread factories
- Object pools
- Singleton with thread safety

**2. Structural Patterns:**
- Adapter for thread APIs
- Decorator for thread behavior
- Facade for complex threading

**3. Behavioral Patterns:**
- Observer for thread events
- Command for thread tasks
- State for thread lifecycle

### Java Example - Common Patterns:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class CommonMultithreadingPatterns {
    private final AtomicInteger patternCounter = new AtomicInteger(0);
    private final ExecutorService executor = Executors.newFixedThreadPool(5);
    
    public void demonstrateCommonPatterns() throws InterruptedException {
        // Pattern 1: Thread Factory
        demonstrateThreadFactory();
        
        // Pattern 2: Object Pool
        demonstrateObjectPool();
        
        // Pattern 3: Observer Pattern
        demonstrateObserverPattern();
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateThreadFactory() throws InterruptedException {
        System.out.println("=== Thread Factory Pattern ===");
        
        ThreadFactory customFactory = new ThreadFactory() {
            private final AtomicInteger threadNumber = new AtomicInteger(1);
            
            @Override
            public Thread newThread(Runnable r) {
                Thread t = new Thread(r, "CustomThread-" + threadNumber.getAndIncrement());
                t.setDaemon(false);
                return t;
            }
        };
        
        ExecutorService customExecutor = Executors.newFixedThreadPool(3, customFactory);
        
        for (int i = 0; i < 3; i++) {
            customExecutor.submit(() -> {
                System.out.println("Running on: " + Thread.currentThread().getName());
            });
        }
        
        customExecutor.shutdown();
        customExecutor.awaitTermination(2, TimeUnit.SECONDS);
    }
    
    private void demonstrateObjectPool() throws InterruptedException {
        System.out.println("\n=== Object Pool Pattern ===");
        
        BlockingQueue<String> objectPool = new LinkedBlockingQueue<>();
        
        // Pre-populate pool
        for (int i = 0; i < 5; i++) {
            objectPool.offer("Object-" + i);
        }
        
        // Use objects from pool
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                try {
                    String obj = objectPool.take();
                    System.out.println("Using object: " + obj);
                    Thread.sleep(1000);
                    objectPool.offer(obj); // Return to pool
                    System.out.println("Returned object: " + obj);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        Thread.sleep(5000);
    }
    
    private void demonstrateObserverPattern() throws InterruptedException {
        System.out.println("\n=== Observer Pattern ===");
        
        ThreadEventNotifier notifier = new ThreadEventNotifier();
        
        // Add observers
        notifier.addObserver(event -> System.out.println("Observer 1: " + event));
        notifier.addObserver(event -> System.out.println("Observer 2: " + event));
        
        // Simulate events
        for (int i = 0; i < 3; i++) {
            final int eventId = i;
            executor.submit(() -> {
                notifier.notifyObservers("Thread event " + eventId);
            });
        }
        
        Thread.sleep(2000);
    }
    
    private static class ThreadEventNotifier {
        private final List<Observer> observers = new ArrayList<>();
        
        public synchronized void addObserver(Observer observer) {
            observers.add(observer);
        }
        
        public synchronized void notifyObservers(String event) {
            observers.forEach(observer -> observer.update(event));
        }
    }
    
    private interface Observer {
        void update(String event);
    }
    
    public static void main(String[] args) throws InterruptedException {
        CommonMultithreadingPatterns example = new CommonMultithreadingPatterns();
        example.demonstrateCommonPatterns();
    }
}
```

### Real-World Analogy:
Think of multithreading patterns like construction blueprints:
- **Thread Factory**: Like a construction company that creates workers with specific skills
- **Object Pool**: Like a tool shed where workers can borrow and return tools
- **Observer Pattern**: Like a supervisor who watches workers and reports on their progress

## 20.2 Producer-Consumer Pattern

The Producer-Consumer pattern decouples data production from consumption using a shared buffer, allowing producers and consumers to work at different rates.

### Key Components:

**1. Producers:**
- Generate data
- Add to shared buffer
- Handle buffer overflow

**2. Consumers:**
- Process data
- Remove from buffer
- Handle buffer underflow

**3. Shared Buffer:**
- Thread-safe queue
- Bounded or unbounded
- Blocking or non-blocking

### Java Example - Producer-Consumer Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ProducerConsumerPatternExample {
    private final BlockingQueue<String> buffer = new LinkedBlockingQueue<>(10);
    private final AtomicInteger producedCount = new AtomicInteger(0);
    private final AtomicInteger consumedCount = new AtomicInteger(0);
    private final ExecutorService executor = Executors.newFixedThreadPool(6);
    
    public void demonstrateProducerConsumer() throws InterruptedException {
        // Create producers
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 10; j++) {
                        String item = "Item-" + producerId + "-" + j;
                        buffer.put(item);
                        producedCount.incrementAndGet();
                        System.out.println("Producer " + producerId + " produced: " + item);
                        Thread.sleep(100);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Create consumers
        for (int i = 0; i < 2; i++) {
            final int consumerId = i;
            executor.submit(() -> {
                try {
                    for (int j = 0; j < 15; j++) {
                        String item = buffer.take();
                        consumedCount.incrementAndGet();
                        System.out.println("Consumer " + consumerId + " consumed: " + item);
                        Thread.sleep(150);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        Thread.sleep(10000);
        executor.shutdown();
        
        System.out.println("Produced: " + producedCount.get());
        System.out.println("Consumed: " + consumedCount.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ProducerConsumerPatternExample example = new ProducerConsumerPatternExample();
        example.demonstrateProducerConsumer();
    }
}
```

## 20.3 Reader-Writer Pattern

The Reader-Writer pattern allows multiple readers to access shared data simultaneously while ensuring exclusive access for writers.

### Key Concepts:

**1. Readers:**
- Can read concurrently
- Don't modify data
- Shared access

**2. Writers:**
- Exclusive access
- Modify data
- Block readers

**3. Synchronization:**
- Read-write locks
- Priority handling
- Fairness policies

### Java Example - Reader-Writer Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReaderWriterPatternExample {
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    private final AtomicInteger data = new AtomicInteger(0);
    private final AtomicInteger readCount = new AtomicInteger(0);
    private final AtomicInteger writeCount = new AtomicInteger(0);
    private final ExecutorService executor = Executors.newFixedThreadPool(8);
    
    public void demonstrateReaderWriter() throws InterruptedException {
        // Create readers
        for (int i = 0; i < 5; i++) {
            final int readerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 10; j++) {
                    readData(readerId);
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        
        // Create writers
        for (int i = 0; i < 3; i++) {
            final int writerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 5; j++) {
                    writeData(writerId, j);
                    try {
                        Thread.sleep(200);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
        
        Thread.sleep(8000);
        executor.shutdown();
        
        System.out.println("Total reads: " + readCount.get());
        System.out.println("Total writes: " + writeCount.get());
    }
    
    private void readData(int readerId) {
        lock.readLock().lock();
        try {
            int value = data.get();
            readCount.incrementAndGet();
            System.out.println("Reader " + readerId + " read: " + value);
        } finally {
            lock.readLock().unlock();
        }
    }
    
    private void writeData(int writerId, int value) {
        lock.writeLock().lock();
        try {
            data.set(value);
            writeCount.incrementAndGet();
            System.out.println("Writer " + writerId + " wrote: " + value);
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ReaderWriterPatternExample example = new ReaderWriterPatternExample();
        example.demonstrateReaderWriter();
    }
}
```

## 20.4 Master-Worker Pattern

The Master-Worker pattern divides work among multiple worker threads, with a master thread coordinating the overall process.

### Key Components:

**1. Master:**
- Divides work into tasks
- Distributes tasks to workers
- Collects results

**2. Workers:**
- Process assigned tasks
- Return results to master
- Independent execution

**3. Task Queue:**
- Shared work distribution
- Load balancing
- Result collection

### Java Example - Master-Worker Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.List;
import java.util.ArrayList;

public class MasterWorkerPatternExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(5);
    private final AtomicInteger completedTasks = new AtomicInteger(0);
    
    public void demonstrateMasterWorker() throws InterruptedException {
        // Master creates tasks
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < 20; i++) {
            final int taskId = i;
            Future<Integer> future = executor.submit(() -> {
                return processTask(taskId);
            });
            futures.add(future);
        }
        
        // Master collects results
        int totalResult = 0;
        for (Future<Integer> future : futures) {
            try {
                totalResult += future.get();
            } catch (ExecutionException e) {
                System.err.println("Task failed: " + e.getCause());
            }
        }
        
        System.out.println("Total result: " + totalResult);
        System.out.println("Completed tasks: " + completedTasks.get());
        
        executor.shutdown();
    }
    
    private int processTask(int taskId) {
        try {
            // Simulate work
            Thread.sleep(100 + (int)(Math.random() * 500));
            int result = taskId * 2;
            completedTasks.incrementAndGet();
            System.out.println("Worker completed task " + taskId + " with result " + result);
            return result;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return 0;
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        MasterWorkerPatternExample example = new MasterWorkerPatternExample();
        example.demonstrateMasterWorker();
    }
}
```

## 20.5 Pipeline Pattern

The Pipeline pattern processes data through a series of stages, where each stage performs a specific transformation on the data.

### Key Concepts:

**1. Stages:**
- Sequential processing steps
- Independent transformation
- Buffered communication

**2. Data Flow:**
- Unidirectional flow
- Stage-to-stage communication
- Backpressure handling

**3. Parallelism:**
- Multiple instances per stage
- Load balancing
- Throughput optimization

### Java Example - Pipeline Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class PipelinePatternExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(6);
    private final AtomicInteger processedItems = new AtomicInteger(0);
    
    public void demonstratePipeline() throws InterruptedException {
        // Create pipeline stages
        BlockingQueue<String> stage1Queue = new LinkedBlockingQueue<>();
        BlockingQueue<String> stage2Queue = new LinkedBlockingQueue<>();
        BlockingQueue<String> stage3Queue = new LinkedBlockingQueue<>();
        
        // Stage 1: Input processing
        executor.submit(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    String item = "Input-" + i;
                    stage1Queue.put(item);
                    System.out.println("Stage 1: " + item);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Stage 2: Processing
        executor.submit(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    String item = stage1Queue.take();
                    String processed = item + "-Processed";
                    stage2Queue.put(processed);
                    System.out.println("Stage 2: " + processed);
                    Thread.sleep(150);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Stage 3: Output
        executor.submit(() -> {
            try {
                for (int i = 0; i < 10; i++) {
                    String item = stage2Queue.take();
                    String output = item + "-Output";
                    stage3Queue.put(output);
                    processedItems.incrementAndGet();
                    System.out.println("Stage 3: " + output);
                    Thread.sleep(100);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread.sleep(5000);
        executor.shutdown();
        
        System.out.println("Processed items: " + processedItems.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        PipelinePatternExample example = new PipelinePatternExample();
        example.demonstratePipeline();
    }
}
```

## 20.6 Scatter-Gather Pattern

The Scatter-Gather pattern distributes work to multiple workers and then collects and combines their results.

### Key Concepts:

**1. Scatter Phase:**
- Distribute work to workers
- Parallel execution
- Independent processing

**2. Gather Phase:**
- Collect results from workers
- Combine results
- Handle failures

**3. Coordination:**
- Synchronization points
- Result aggregation
- Error handling

### Java Example - Scatter-Gather Pattern:

```java
import java.util.concurrent.*;
import java.util.List;
import java.util.ArrayList;
import java.util.concurrent.atomic.AtomicInteger;

public class ScatterGatherPatternExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(5);
    private final AtomicInteger completedWorkers = new AtomicInteger(0);
    
    public void demonstrateScatterGather() throws InterruptedException {
        // Scatter: Distribute work
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < 8; i++) {
            final int workerId = i;
            Future<Integer> future = executor.submit(() -> {
                return processWork(workerId);
            });
            futures.add(future);
        }
        
        // Gather: Collect results
        int totalResult = 0;
        int successCount = 0;
        
        for (Future<Integer> future : futures) {
            try {
                int result = future.get(2, TimeUnit.SECONDS);
                totalResult += result;
                successCount++;
                System.out.println("Gathered result: " + result);
            } catch (TimeoutException e) {
                System.out.println("Worker timed out");
            } catch (ExecutionException e) {
                System.out.println("Worker failed: " + e.getCause());
            }
        }
        
        System.out.println("Total result: " + totalResult);
        System.out.println("Successful workers: " + successCount);
        
        executor.shutdown();
    }
    
    private int processWork(int workerId) {
        try {
            // Simulate work
            Thread.sleep(500 + (int)(Math.random() * 1000));
            int result = workerId * 10;
            completedWorkers.incrementAndGet();
            System.out.println("Worker " + workerId + " completed with result " + result);
            return result;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return 0;
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ScatterGatherPatternExample example = new ScatterGatherPatternExample();
        example.demonstrateScatterGather();
    }
}
```

## 20.7 Map-Reduce Pattern

The Map-Reduce pattern processes large datasets by mapping data to key-value pairs and then reducing them to produce final results.

### Key Concepts:

**1. Map Phase:**
- Transform input data
- Generate key-value pairs
- Parallel processing

**2. Shuffle Phase:**
- Group by keys
- Sort and partition
- Network communication

**3. Reduce Phase:**
- Aggregate values by key
- Produce final results
- Parallel reduction

### Java Example - Map-Reduce Pattern:

```java
import java.util.concurrent.*;
import java.util.*;
import java.util.stream.Collectors;

public class MapReducePatternExample {
    private final ExecutorService executor = Executors.newFixedThreadPool(4);
    
    public void demonstrateMapReduce() throws InterruptedException {
        // Input data
        List<String> words = Arrays.asList(
            "hello", "world", "java", "concurrency", "hello", "java", "world", "multithreading"
        );
        
        // Map phase
        List<Future<Map<String, Integer>>> mapFutures = new ArrayList<>();
        
        for (int i = 0; i < 2; i++) {
            final int start = i * 4;
            final int end = Math.min(start + 4, words.size());
            final List<String> partition = words.subList(start, end);
            
            Future<Map<String, Integer>> future = executor.submit(() -> {
                return mapPhase(partition);
            });
            mapFutures.add(future);
        }
        
        // Collect map results
        Map<String, Integer> allResults = new HashMap<>();
        for (Future<Map<String, Integer>> future : mapFutures) {
            try {
                Map<String, Integer> result = future.get();
                for (Map.Entry<String, Integer> entry : result.entrySet()) {
                    allResults.merge(entry.getKey(), entry.getValue(), Integer::sum);
                }
            } catch (ExecutionException e) {
                System.err.println("Map phase failed: " + e.getCause());
            }
        }
        
        // Reduce phase
        Map<String, Integer> finalResult = reducePhase(allResults);
        
        System.out.println("Final word count: " + finalResult);
        
        executor.shutdown();
    }
    
    private Map<String, Integer> mapPhase(List<String> words) {
        Map<String, Integer> result = new HashMap<>();
        for (String word : words) {
            result.merge(word, 1, Integer::sum);
        }
        System.out.println("Map result: " + result);
        return result;
    }
    
    private Map<String, Integer> reducePhase(Map<String, Integer> mapResults) {
        return mapResults.entrySet().stream()
            .collect(Collectors.toMap(
                Map.Entry::getKey,
                Map.Entry::getValue
            ));
    }
    
    public static void main(String[] args) throws InterruptedException {
        MapReducePatternExample example = new MapReducePatternExample();
        example.demonstrateMapReduce();
    }
}
```

## 20.8 Fork-Join Pattern

The Fork-Join pattern recursively divides work into smaller tasks, processes them in parallel, and then combines the results.

### Key Concepts:

**1. Fork:**
- Divide work into subtasks
- Recursive decomposition
- Parallel execution

**2. Join:**
- Combine subtask results
- Wait for completion
- Result aggregation

**3. Work Stealing:**
- Dynamic load balancing
- Idle threads steal work
- Efficient resource utilization

### Java Example - Fork-Join Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ForkJoinPatternExample {
    private final ForkJoinPool forkJoinPool = new ForkJoinPool();
    private final AtomicInteger taskCount = new AtomicInteger(0);
    
    public void demonstrateForkJoin() throws InterruptedException {
        // Create recursive task
        RecursiveTask<Integer> task = new SumTask(1, 100);
        
        // Execute task
        int result = forkJoinPool.invoke(task);
        
        System.out.println("Sum from 1 to 100: " + result);
        System.out.println("Tasks created: " + taskCount.get());
        
        forkJoinPool.shutdown();
    }
    
    private class SumTask extends RecursiveTask<Integer> {
        private final int start;
        private final int end;
        private final int threshold = 10;
        
        public SumTask(int start, int end) {
            this.start = start;
            this.end = end;
        }
        
        @Override
        protected Integer compute() {
            taskCount.incrementAndGet();
            
            if (end - start <= threshold) {
                // Base case: compute directly
                int sum = 0;
                for (int i = start; i <= end; i++) {
                    sum += i;
                }
                System.out.println("Computing sum from " + start + " to " + end + " = " + sum);
                return sum;
            } else {
                // Recursive case: fork and join
                int mid = (start + end) / 2;
                SumTask leftTask = new SumTask(start, mid);
                SumTask rightTask = new SumTask(mid + 1, end);
                
                leftTask.fork();
                int rightResult = rightTask.compute();
                int leftResult = leftTask.join();
                
                return leftResult + rightResult;
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ForkJoinPatternExample example = new ForkJoinPatternExample();
        example.demonstrateForkJoin();
    }
}
```

## 20.9 Work-Stealing Pattern

The Work-Stealing pattern allows idle threads to steal work from busy threads, improving load balancing and resource utilization.

### Key Concepts:

**1. Work Queues:**
- Each thread has its own queue
- LIFO for local work
- FIFO for stolen work

**2. Stealing:**
- Idle threads steal from others
- Random or targeted selection
- Minimal contention

**3. Load Balancing:**
- Automatic distribution
- Dynamic adjustment
- High utilization

### Java Example - Work-Stealing Pattern:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class WorkStealingPatternExample {
    private final ExecutorService executor = Executors.newWorkStealingPool();
    private final AtomicInteger completedTasks = new AtomicInteger(0);
    
    public void demonstrateWorkStealing() throws InterruptedException {
        // Create tasks with varying durations
        List<Future<String>> futures = new ArrayList<>();
        
        for (int i = 0; i < 20; i++) {
            final int taskId = i;
            Future<String> future = executor.submit(() -> {
                return processTask(taskId);
            });
            futures.add(future);
        }
        
        // Collect results
        for (Future<String> future : futures) {
            try {
                String result = future.get();
                System.out.println("Completed: " + result);
            } catch (ExecutionException e) {
                System.err.println("Task failed: " + e.getCause());
            }
        }
        
        System.out.println("Total completed: " + completedTasks.get());
        executor.shutdown();
    }
    
    private String processTask(int taskId) {
        try {
            // Simulate varying work duration
            int duration = 100 + (taskId % 5) * 200;
            Thread.sleep(duration);
            
            completedTasks.incrementAndGet();
            return "Task " + taskId + " completed by " + Thread.currentThread().getName();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return "Task " + taskId + " interrupted";
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        WorkStealingPatternExample example = new WorkStealingPatternExample();
        example.demonstrateWorkStealing();
    }
}
```

## 20.10 Pattern Selection Guidelines

Choosing the right multithreading pattern depends on the specific requirements and constraints of your application.

### Selection Criteria:

**1. Problem Type:**
- Data processing: Map-Reduce, Pipeline
- Task distribution: Master-Worker, Scatter-Gather
- Resource sharing: Reader-Writer, Producer-Consumer

**2. Performance Requirements:**
- Throughput: Work-Stealing, Fork-Join
- Latency: Pipeline, Producer-Consumer
- Scalability: Map-Reduce, Scatter-Gather

**3. Complexity:**
- Simple: Producer-Consumer, Reader-Writer
- Medium: Master-Worker, Pipeline
- Complex: Map-Reduce, Fork-Join

### Java Example - Pattern Selection:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class PatternSelectionExample {
    private final AtomicInteger patternUsage = new AtomicInteger(0);
    
    public void demonstratePatternSelection() throws InterruptedException {
        // Scenario 1: High throughput data processing
        System.out.println("=== High Throughput Scenario ===");
        useWorkStealingPattern();
        
        // Scenario 2: Simple producer-consumer
        System.out.println("\n=== Simple Producer-Consumer Scenario ===");
        useProducerConsumerPattern();
        
        // Scenario 3: Complex data transformation
        System.out.println("\n=== Complex Data Transformation Scenario ===");
        usePipelinePattern();
    }
    
    private void useWorkStealingPattern() throws InterruptedException {
        ExecutorService executor = Executors.newWorkStealingPool();
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Work-stealing task " + taskId + " on " + Thread.currentThread().getName());
                patternUsage.incrementAndGet();
            });
        }
        
        Thread.sleep(2000);
        executor.shutdown();
    }
    
    private void useProducerConsumerPattern() throws InterruptedException {
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Producer
        executor.submit(() -> {
            for (int i = 0; i < 5; i++) {
                try {
                    queue.put("Item " + i);
                    System.out.println("Produced: Item " + i);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Consumer
        executor.submit(() -> {
            for (int i = 0; i < 5; i++) {
                try {
                    String item = queue.take();
                    System.out.println("Consumed: " + item);
                    patternUsage.incrementAndGet();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        Thread.sleep(2000);
        executor.shutdown();
    }
    
    private void usePipelinePattern() throws InterruptedException {
        BlockingQueue<String> stage1 = new LinkedBlockingQueue<>();
        BlockingQueue<String> stage2 = new LinkedBlockingQueue<>();
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Stage 1
        executor.submit(() -> {
            for (int i = 0; i < 3; i++) {
                try {
                    stage1.put("Input " + i);
                    System.out.println("Stage 1: Input " + i);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Stage 2
        executor.submit(() -> {
            for (int i = 0; i < 3; i++) {
                try {
                    String item = stage1.take();
                    String processed = item + " processed";
                    stage2.put(processed);
                    System.out.println("Stage 2: " + processed);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Stage 3
        executor.submit(() -> {
            for (int i = 0; i < 3; i++) {
                try {
                    String item = stage2.take();
                    System.out.println("Stage 3: " + item + " completed");
                    patternUsage.incrementAndGet();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        Thread.sleep(2000);
        executor.shutdown();
    }
    
    public static void main(String[] args) throws InterruptedException {
        PatternSelectionExample example = new PatternSelectionExample();
        example.demonstratePatternSelection();
    }
}
```

### Real-World Analogy:
Think of multithreading patterns like different organizational structures:
- **Producer-Consumer**: Like a restaurant kitchen where chefs prepare food and waiters serve it
- **Reader-Writer**: Like a library where multiple people can read books but only one can check out a book at a time
- **Master-Worker**: Like a construction site where a foreman assigns tasks to workers
- **Pipeline**: Like an assembly line where each station performs a specific task
- **Map-Reduce**: Like a census where data is collected from different regions and then aggregated
- **Fork-Join**: Like dividing a large project into smaller tasks and then combining the results
- **Work-Stealing**: Like a flexible team where idle members help others with their work

The key is to choose the pattern that best fits your specific use case and requirements!