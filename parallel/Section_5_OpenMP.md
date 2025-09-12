# Section 5 – OpenMP

## 5.1 OpenMP Fundamentals

OpenMP (Open Multi-Processing) is an API that supports shared memory multiprocessing programming in C, C++, and Fortran.

### Key Concepts:
- **Directive-based**: Uses compiler directives to parallelize code
- **Shared Memory**: All threads share the same memory space
- **Fork-Join Model**: Master thread creates worker threads
- **Portable**: Works across different platforms and compilers

### Real-World Analogy:
OpenMP is like having a conductor in an orchestra who can signal different sections to play simultaneously. The conductor (master thread) coordinates all the musicians (worker threads) who share the same stage (memory space).

### Example: OpenMP Concepts in Java
```java
import java.util.concurrent.*;

public class OpenMPFundamentals {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== OpenMP Fundamentals Demo ===");
        
        // Simulate OpenMP parallel region
        demonstrateParallelRegion();
        
        // Simulate OpenMP work sharing
        demonstrateWorkSharing();
    }
    
    private static void demonstrateParallelRegion() throws InterruptedException {
        System.out.println("\n=== Parallel Region (simulating #pragma omp parallel) ===");
        
        int numThreads = Runtime.getRuntime().availableProcessors();
        System.out.println("Number of threads: " + numThreads);
        
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        
        // Simulate parallel region
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                System.out.println("Thread " + threadId + " executing parallel region");
                latch.countDown();
            });
        }
        
        latch.await();
        executor.shutdown();
    }
    
    private static void demonstrateWorkSharing() throws InterruptedException {
        System.out.println("\n=== Work Sharing (simulating #pragma omp for) ===");
        
        int[] array = new int[1000000];
        Arrays.fill(array, 1);
        
        // Sequential sum
        long startTime = System.currentTimeMillis();
        int sequentialSum = 0;
        for (int value : array) {
            sequentialSum += value;
        }
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        // Parallel sum (simulating OpenMP parallel for)
        startTime = System.currentTimeMillis();
        int parallelSum = Arrays.stream(array)
                .parallel()
                .sum();
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Sequential sum: " + sequentialSum + " in " + sequentialTime + "ms");
        System.out.println("Parallel sum: " + parallelSum + " in " + parallelTime + "ms");
        System.out.println("Speedup: " + (double)sequentialTime / parallelTime);
    }
}
```

## 5.2 OpenMP Directives

OpenMP directives are compiler hints that tell the compiler how to parallelize code sections.

### Key Concepts:
- **Compiler Directives**: Special comments that start with #pragma omp
- **Parallel Directive**: Creates a parallel region
- **For Directive**: Parallelizes loops
- **Sections Directive**: Divides work into sections

### Real-World Analogy:
OpenMP directives are like traffic signs that tell drivers how to navigate. Each directive (sign) provides specific instructions about how the code should be executed in parallel.

### Example: OpenMP Directives Concepts
```java
import java.util.concurrent.*;

public class OpenMPDirectives {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== OpenMP Directives Demo ===");
        
        // Simulate #pragma omp parallel
        demonstrateParallelDirective();
        
        // Simulate #pragma omp for
        demonstrateForDirective();
        
        // Simulate #pragma omp sections
        demonstrateSectionsDirective();
    }
    
    private static void demonstrateParallelDirective() throws InterruptedException {
        System.out.println("\n=== Parallel Directive ===");
        
        // Simulate #pragma omp parallel
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                System.out.println("Thread " + threadId + " in parallel region");
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.SECONDS);
    }
    
    private static void demonstrateForDirective() throws InterruptedException {
        System.out.println("\n=== For Directive ===");
        
        int[] array = new int[1000];
        Arrays.fill(array, 2);
        
        // Simulate #pragma omp for
        int sum = Arrays.stream(array)
                .parallel()
                .sum();
        
        System.out.println("Parallel for sum: " + sum);
    }
    
    private static void demonstrateSectionsDirective() throws InterruptedException {
        System.out.println("\n=== Sections Directive ===");
        
        // Simulate #pragma omp sections
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        CompletableFuture<String> section1 = CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(1000); } catch (InterruptedException e) {}
            return "Section 1 completed";
        }, executor);
        
        CompletableFuture<String> section2 = CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(1500); } catch (InterruptedException e) {}
            return "Section 2 completed";
        }, executor);
        
        CompletableFuture<String> section3 = CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(800); } catch (InterruptedException e) {}
            return "Section 3 completed";
        }, executor);
        
        try {
            System.out.println(section1.get());
            System.out.println(section2.get());
            System.out.println(section3.get());
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        
        executor.shutdown();
    }
}
```

## 5.3 Parallel Regions

Parallel regions are sections of code that are executed by multiple threads simultaneously.

### Key Concepts:
- **Fork-Join**: Master thread forks into multiple threads, then joins
- **Thread Creation**: Threads are created at the start of parallel region
- **Thread Destruction**: Threads are destroyed at the end of parallel region
- **Shared Variables**: Variables are shared among all threads by default

### Real-World Analogy:
Parallel regions are like having multiple workers start working on the same project simultaneously. They all begin at the same time, work independently, and finish together.

### Example: Parallel Regions
```java
import java.util.concurrent.*;

public class ParallelRegions {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Parallel Regions Demo ===");
        
        // Demonstrate parallel region execution
        demonstrateParallelRegionExecution();
        
        // Demonstrate thread-local variables
        demonstrateThreadLocalVariables();
    }
    
    private static void demonstrateParallelRegionExecution() throws InterruptedException {
        System.out.println("\n=== Parallel Region Execution ===");
        
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch startLatch = new CountDownLatch(1);
        CountDownLatch endLatch = new CountDownLatch(numThreads);
        
        // Simulate parallel region
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                try {
                    startLatch.await(); // Wait for all threads to be ready
                    System.out.println("Thread " + threadId + " executing parallel region");
                    Thread.sleep(1000);
                    System.out.println("Thread " + threadId + " completed parallel region");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    endLatch.countDown();
                }
            });
        }
        
        // Start all threads simultaneously
        startLatch.countDown();
        
        // Wait for all threads to complete
        endLatch.await();
        executor.shutdown();
    }
    
    private static void demonstrateThreadLocalVariables() throws InterruptedException {
        System.out.println("\n=== Thread-Local Variables ===");
        
        // Simulate thread-local variables in OpenMP
        ThreadLocal<Integer> threadLocalVar = new ThreadLocal<Integer>() {
            @Override
            protected Integer initialValue() {
                return (int) (Math.random() * 100);
            }
        };
        
        int numThreads = 3;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                int localValue = threadLocalVar.get();
                System.out.println("Thread " + Thread.currentThread().getId() + 
                                 " has local value: " + localValue);
                
                // Modify local value
                localValue *= 2;
                threadLocalVar.set(localValue);
                System.out.println("Thread " + Thread.currentThread().getId() + 
                                 " modified local value to: " + localValue);
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.SECONDS);
    }
}
```

## 5.4 Work Sharing Constructs

Work sharing constructs distribute work among threads in a parallel region.

### Key Concepts:
- **For Construct**: Distributes loop iterations among threads
- **Sections Construct**: Assigns different code sections to different threads
- **Single Construct**: Executes code block with only one thread
- **Master Construct**: Executes code block with master thread only

### Real-World Analogy:
Work sharing constructs are like a project manager assigning different tasks to team members. The for construct is like dividing a list of tasks equally, while sections construct is like assigning different types of work to specialists.

### Example: Work Sharing Constructs
```java
import java.util.concurrent.*;

public class WorkSharingConstructs {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Work Sharing Constructs Demo ===");
        
        // Demonstrate for construct
        demonstrateForConstruct();
        
        // Demonstrate sections construct
        demonstrateSectionsConstruct();
        
        // Demonstrate single construct
        demonstrateSingleConstruct();
    }
    
    private static void demonstrateForConstruct() throws InterruptedException {
        System.out.println("\n=== For Construct ===");
        
        int[] array = new int[1000000];
        Arrays.fill(array, 1);
        
        // Simulate #pragma omp for
        long startTime = System.currentTimeMillis();
        int sum = Arrays.stream(array)
                .parallel()
                .sum();
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Parallel for sum: " + sum + " in " + parallelTime + "ms");
    }
    
    private static void demonstrateSectionsConstruct() throws InterruptedException {
        System.out.println("\n=== Sections Construct ===");
        
        // Simulate #pragma omp sections
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        CompletableFuture<String> section1 = CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(1000); } catch (InterruptedException e) {}
            return "Section 1: Data processing completed";
        }, executor);
        
        CompletableFuture<String> section2 = CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(1500); } catch (InterruptedException e) {}
            return "Section 2: File I/O completed";
        }, executor);
        
        CompletableFuture<String> section3 = CompletableFuture.supplyAsync(() -> {
            try { Thread.sleep(800); } catch (InterruptedException e) {}
            return "Section 3: Network operation completed";
        }, executor);
        
        try {
            System.out.println(section1.get());
            System.out.println(section2.get());
            System.out.println(section3.get());
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        
        executor.shutdown();
    }
    
    private static void demonstrateSingleConstruct() throws InterruptedException {
        System.out.println("\n=== Single Construct ===");
        
        // Simulate #pragma omp single
        AtomicBoolean singleExecuted = new AtomicBoolean(false);
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                // Only one thread should execute this block
                if (singleExecuted.compareAndSet(false, true)) {
                    System.out.println("Single construct executed by thread: " + 
                                     Thread.currentThread().getId());
                } else {
                    System.out.println("Thread " + Thread.currentThread().getId() + 
                                     " skipped single construct");
                }
                latch.countDown();
            });
        }
        
        latch.await();
        executor.shutdown();
    }
}
```

## 5.5 Synchronization Constructs

Synchronization constructs coordinate thread execution and ensure proper ordering of operations.

### Key Concepts:
- **Barrier**: Synchronization point where all threads must wait
- **Critical Section**: Code section that only one thread can execute at a time
- **Atomic Operations**: Operations that complete without interruption
- **Ordered Construct**: Ensures ordered execution of code sections

### Real-World Analogy:
Synchronization constructs are like traffic lights and road signs that coordinate traffic flow. Barriers are like stop signs where all cars must wait, critical sections are like one-lane bridges where only one car can pass at a time.

### Example: Synchronization Constructs
```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class SynchronizationConstructs {
    private static int sharedCounter = 0;
    private static final Object lock = new Object();
    private static AtomicInteger atomicCounter = new AtomicInteger(0);
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Synchronization Constructs Demo ===");
        
        // Demonstrate barrier
        demonstrateBarrier();
        
        // Demonstrate critical section
        demonstrateCriticalSection();
        
        // Demonstrate atomic operations
        demonstrateAtomicOperations();
    }
    
    private static void demonstrateBarrier() throws InterruptedException {
        System.out.println("\n=== Barrier ===");
        
        int numThreads = 4;
        CyclicBarrier barrier = new CyclicBarrier(numThreads, () -> {
            System.out.println("All threads reached the barrier!");
        });
        
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                try {
                    System.out.println("Thread " + threadId + " working...");
                    Thread.sleep(1000 + threadId * 500);
                    System.out.println("Thread " + threadId + " reached barrier");
                    barrier.await();
                    System.out.println("Thread " + threadId + " continuing after barrier");
                } catch (InterruptedException | BrokenBarrierException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private static void demonstrateCriticalSection() throws InterruptedException {
        System.out.println("\n=== Critical Section ===");
        
        sharedCounter = 0;
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        // Critical section - only one thread at a time
                        sharedCounter++;
                    }
                }
                latch.countDown();
            });
        }
        
        latch.await();
        System.out.println("Critical section counter: " + sharedCounter);
        executor.shutdown();
    }
    
    private static void demonstrateAtomicOperations() throws InterruptedException {
        System.out.println("\n=== Atomic Operations ===");
        
        atomicCounter.set(0);
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    atomicCounter.incrementAndGet(); // Atomic operation
                }
                latch.countDown();
            });
        }
        
        latch.await();
        System.out.println("Atomic counter: " + atomicCounter.get());
        executor.shutdown();
    }
}
```

## 5.6 Data Sharing Clauses

Data sharing clauses control how variables are shared among threads in OpenMP.

### Key Concepts:
- **Shared**: Variable is shared among all threads
- **Private**: Each thread has its own copy of the variable
- **Firstprivate**: Private variable initialized with master thread's value
- **Lastprivate**: Private variable with value from last iteration

### Real-World Analogy:
Data sharing clauses are like office supplies. Shared supplies are used by everyone, private supplies belong to individual workers, firstprivate supplies are given to new workers with initial values, and lastprivate supplies keep the final value when work is done.

### Example: Data Sharing Clauses
```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class DataSharingClauses {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Data Sharing Clauses Demo ===");
        
        // Demonstrate shared variables
        demonstrateSharedVariables();
        
        // Demonstrate private variables
        demonstratePrivateVariables();
        
        // Demonstrate firstprivate variables
        demonstrateFirstprivateVariables();
    }
    
    private static void demonstrateSharedVariables() throws InterruptedException {
        System.out.println("\n=== Shared Variables ===");
        
        // Simulate shared variable
        AtomicInteger sharedVar = new AtomicInteger(0);
        int numThreads = 3;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                int value = sharedVar.incrementAndGet();
                System.out.println("Thread " + threadId + " incremented shared variable to: " + value);
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.SECONDS);
        System.out.println("Final shared variable value: " + sharedVar.get());
    }
    
    private static void demonstratePrivateVariables() throws InterruptedException {
        System.out.println("\n=== Private Variables ===");
        
        // Simulate private variables using ThreadLocal
        ThreadLocal<Integer> privateVar = new ThreadLocal<Integer>() {
            @Override
            protected Integer initialValue() {
                return 0;
            }
        };
        
        int numThreads = 3;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                int value = privateVar.get();
                value += threadId * 10;
                privateVar.set(value);
                System.out.println("Thread " + threadId + " private variable: " + value);
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.SECONDS);
    }
    
    private static void demonstrateFirstprivateVariables() throws InterruptedException {
        System.out.println("\n=== Firstprivate Variables ===");
        
        // Simulate firstprivate variable
        int masterValue = 100;
        int numThreads = 3;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            final int firstprivateValue = masterValue; // Each thread gets copy of master value
            executor.submit(() -> {
                int localValue = firstprivateValue + threadId;
                System.out.println("Thread " + threadId + " firstprivate variable: " + localValue);
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.SECONDS);
    }
}
```

## 5.7 OpenMP Scheduling

OpenMP scheduling controls how loop iterations are distributed among threads.

### Key Concepts:
- **Static Scheduling**: Iterations divided into equal chunks
- **Dynamic Scheduling**: Iterations assigned as threads become available
- **Guided Scheduling**: Chunk size decreases as work progresses
- **Runtime Scheduling**: Scheduling determined at runtime

### Real-World Analogy:
OpenMP scheduling is like different ways of distributing work among team members. Static scheduling is like giving everyone the same number of tasks upfront, dynamic scheduling is like giving tasks as people finish their current work.

### Example: OpenMP Scheduling
```java
import java.util.concurrent.*;

public class OpenMPScheduling {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== OpenMP Scheduling Demo ===");
        
        // Demonstrate static scheduling
        demonstrateStaticScheduling();
        
        // Demonstrate dynamic scheduling
        demonstrateDynamicScheduling();
        
        // Demonstrate guided scheduling
        demonstrateGuidedScheduling();
    }
    
    private static void demonstrateStaticScheduling() throws InterruptedException {
        System.out.println("\n=== Static Scheduling ===");
        
        int[] array = new int[1000];
        Arrays.fill(array, 1);
        
        // Simulate static scheduling - equal chunks
        int numThreads = 4;
        int chunkSize = array.length / numThreads;
        
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        AtomicInteger totalSum = new AtomicInteger(0);
        
        for (int i = 0; i < numThreads; i++) {
            final int start = i * chunkSize;
            final int end = (i == numThreads - 1) ? array.length : (i + 1) * chunkSize;
            final int threadId = i;
            
            executor.submit(() -> {
                int localSum = 0;
                for (int j = start; j < end; j++) {
                    localSum += array[j];
                }
                totalSum.addAndGet(localSum);
                System.out.println("Thread " + threadId + " processed indices " + 
                                 start + "-" + (end-1) + ", sum: " + localSum);
                latch.countDown();
            });
        }
        
        latch.await();
        System.out.println("Static scheduling total sum: " + totalSum.get());
        executor.shutdown();
    }
    
    private static void demonstrateDynamicScheduling() throws InterruptedException {
        System.out.println("\n=== Dynamic Scheduling ===");
        
        // Simulate dynamic scheduling with work queue
        BlockingQueue<Integer> workQueue = new LinkedBlockingQueue<>();
        for (int i = 0; i < 100; i++) {
            workQueue.offer(i);
        }
        
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        AtomicInteger totalWork = new AtomicInteger(0);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                int localWork = 0;
                Integer task;
                while ((task = workQueue.poll()) != null) {
                    // Simulate variable work time
                    try { Thread.sleep(task % 10); } catch (InterruptedException e) {}
                    localWork++;
                    System.out.println("Thread " + threadId + " completed task " + task);
                }
                totalWork.addAndGet(localWork);
                latch.countDown();
            });
        }
        
        latch.await();
        System.out.println("Dynamic scheduling total work: " + totalWork.get());
        executor.shutdown();
    }
    
    private static void demonstrateGuidedScheduling() throws InterruptedException {
        System.out.println("\n=== Guided Scheduling ===");
        
        // Simulate guided scheduling with decreasing chunk sizes
        int totalWork = 1000;
        int numThreads = 4;
        AtomicInteger remainingWork = new AtomicInteger(totalWork);
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        CountDownLatch latch = new CountDownLatch(numThreads);
        AtomicInteger completedWork = new AtomicInteger(0);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                int localWork = 0;
                while (true) {
                    int chunkSize = Math.max(1, remainingWork.get() / numThreads);
                    int work = remainingWork.addAndGet(-chunkSize);
                    
                    if (work <= 0) break;
                    
                    // Simulate work
                    try { Thread.sleep(chunkSize / 10); } catch (InterruptedException e) {}
                    localWork += chunkSize;
                    System.out.println("Thread " + threadId + " completed chunk of size " + chunkSize);
                }
                completedWork.addAndGet(localWork);
                latch.countDown();
            });
        }
        
        latch.await();
        System.out.println("Guided scheduling completed work: " + completedWork.get());
        executor.shutdown();
    }
}
```

## 5.8 OpenMP Performance

OpenMP performance optimization involves understanding and mitigating overhead and contention.

### Key Concepts:
- **Thread Creation Overhead**: Cost of creating and destroying threads
- **Load Balancing**: Ensuring work is distributed evenly
- **Memory Access Patterns**: Optimizing memory usage for parallel execution
- **Cache Effects**: Understanding how threads affect CPU cache performance

### Real-World Analogy:
OpenMP performance is like managing a team's efficiency. You need to consider the overhead of coordination, ensure everyone has enough work, and organize tasks to minimize conflicts and maximize productivity.

### Example: OpenMP Performance Analysis
```java
import java.util.concurrent.*;

public class OpenMPPerformance {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== OpenMP Performance Demo ===");
        
        // Analyze thread overhead
        analyzeThreadOverhead();
        
        // Analyze load balancing
        analyzeLoadBalancing();
        
        // Analyze memory access patterns
        analyzeMemoryAccessPatterns();
    }
    
    private static void analyzeThreadOverhead() throws InterruptedException {
        System.out.println("\n=== Thread Overhead Analysis ===");
        
        int[] array = new int[1000000];
        Arrays.fill(array, 1);
        
        // Sequential execution
        long startTime = System.currentTimeMillis();
        int sequentialSum = 0;
        for (int value : array) {
            sequentialSum += value;
        }
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        // Parallel execution with different thread counts
        int[] threadCounts = {1, 2, 4, 8, 16};
        for (int threadCount : threadCounts) {
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);
            
            startTime = System.currentTimeMillis();
            int parallelSum = Arrays.stream(array)
                    .parallel()
                    .sum();
            long parallelTime = System.currentTimeMillis() - startTime;
            
            double speedup = (double)sequentialTime / parallelTime;
            System.out.println(threadCount + " threads: " + parallelTime + "ms, Speedup: " + speedup);
            
            executor.shutdown();
        }
    }
    
    private static void analyzeLoadBalancing() throws InterruptedException {
        System.out.println("\n=== Load Balancing Analysis ===");
        
        // Create work with varying complexity
        List<Integer> workItems = new ArrayList<>();
        for (int i = 0; i < 100; i++) {
            workItems.add(i * i); // Variable work complexity
        }
        
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        // Static load balancing
        long startTime = System.currentTimeMillis();
        CountDownLatch latch = new CountDownLatch(numThreads);
        int chunkSize = workItems.size() / numThreads;
        
        for (int i = 0; i < numThreads; i++) {
            final int start = i * chunkSize;
            final int end = (i == numThreads - 1) ? workItems.size() : (i + 1) * chunkSize;
            final int threadId = i;
            
            executor.submit(() -> {
                long workTime = 0;
                for (int j = start; j < end; j++) {
                    long itemStart = System.currentTimeMillis();
                    // Simulate work based on item complexity
                    try { Thread.sleep(workItems.get(j) % 10); } catch (InterruptedException e) {}
                    workTime += System.currentTimeMillis() - itemStart;
                }
                System.out.println("Thread " + threadId + " work time: " + workTime + "ms");
                latch.countDown();
            });
        }
        
        latch.await();
        long staticTime = System.currentTimeMillis() - startTime;
        System.out.println("Static load balancing time: " + staticTime + "ms");
        
        executor.shutdown();
    }
    
    private static void analyzeMemoryAccessPatterns() throws InterruptedException {
        System.out.println("\n=== Memory Access Pattern Analysis ===");
        
        int arraySize = 10000000;
        int[] array = new int[arraySize];
        
        // Initialize array
        for (int i = 0; i < arraySize; i++) {
            array[i] = i;
        }
        
        // Sequential access pattern
        long startTime = System.currentTimeMillis();
        int sequentialSum = 0;
        for (int i = 0; i < arraySize; i++) {
            sequentialSum += array[i];
        }
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        // Parallel access pattern
        startTime = System.currentTimeMillis();
        int parallelSum = Arrays.stream(array)
                .parallel()
                .sum();
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Sequential access time: " + sequentialTime + "ms");
        System.out.println("Parallel access time: " + parallelTime + "ms");
        System.out.println("Memory access speedup: " + (double)sequentialTime / parallelTime);
    }
}
```

## 5.9 OpenMP Best Practices

OpenMP best practices help optimize performance and avoid common pitfalls.

### Key Concepts:
- **Minimize Parallel Overhead**: Use parallel regions efficiently
- **Optimize Data Sharing**: Use appropriate data sharing clauses
- **Avoid False Sharing**: Prevent threads from accessing the same cache line
- **Load Balancing**: Choose appropriate scheduling strategies

### Real-World Analogy:
OpenMP best practices are like following proven cooking techniques. They help you avoid common mistakes and achieve consistent, high-quality results in your parallel programs.

### Example: OpenMP Best Practices
```java
import java.util.concurrent.*;

public class OpenMPBestPractices {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== OpenMP Best Practices Demo ===");
        
        // Practice 1: Minimize parallel overhead
        demonstrateMinimizeOverhead();
        
        // Practice 2: Optimize data sharing
        demonstrateOptimizeDataSharing();
        
        // Practice 3: Avoid false sharing
        demonstrateAvoidFalseSharing();
    }
    
    private static void demonstrateMinimizeOverhead() throws InterruptedException {
        System.out.println("\n=== Minimize Parallel Overhead ===");
        
        int[] array = new int[1000];
        Arrays.fill(array, 1);
        
        // Bad: Parallel region for small work
        long startTime = System.currentTimeMillis();
        int sum1 = Arrays.stream(array)
                .parallel()
                .sum();
        long parallelTime = System.currentTimeMillis() - startTime;
        
        // Good: Sequential for small work
        startTime = System.currentTimeMillis();
        int sum2 = 0;
        for (int value : array) {
            sum2 += value;
        }
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Small array - Parallel: " + parallelTime + "ms, Sequential: " + sequentialTime + "ms");
        System.out.println("For small work, sequential is often faster due to parallel overhead");
    }
    
    private static void demonstrateOptimizeDataSharing() throws InterruptedException {
        System.out.println("\n=== Optimize Data Sharing ===");
        
        // Good: Use thread-local variables to avoid synchronization
        ThreadLocal<Integer> threadLocalSum = new ThreadLocal<Integer>() {
            @Override
            protected Integer initialValue() {
                return 0;
            }
        };
        
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                int localSum = threadLocalSum.get();
                for (int j = 0; j < 1000; j++) {
                    localSum += threadId * j;
                }
                threadLocalSum.set(localSum);
                System.out.println("Thread " + threadId + " local sum: " + localSum);
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.SECONDS);
    }
    
    private static void demonstrateAvoidFalseSharing() throws InterruptedException {
        System.out.println("\n=== Avoid False Sharing ===");
        
        // Bad: False sharing - threads access adjacent memory locations
        int[] sharedArray = new int[4]; // Adjacent elements in same cache line
        
        // Good: Use padding to avoid false sharing
        class PaddedCounter {
            volatile long value;
            long p1, p2, p3, p4, p5, p6, p7; // Padding
        }
        
        PaddedCounter[] paddedCounters = new PaddedCounter[4];
        for (int i = 0; i < 4; i++) {
            paddedCounters[i] = new PaddedCounter();
        }
        
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int threadId = i;
            executor.submit(() -> {
                for (int j = 0; j < 1000000; j++) {
                    paddedCounters[threadId].value++;
                }
                System.out.println("Thread " + threadId + " padded counter: " + paddedCounters[threadId].value);
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(2, TimeUnit.SECONDS);
    }
}
```

## 5.10 OpenMP Advanced Features

OpenMP advanced features provide sophisticated parallel programming capabilities.

### Key Concepts:
- **Nested Parallelism**: Parallel regions within parallel regions
- **Task Construct**: Dynamic task creation and execution
- **Reduction**: Automatic reduction operations
- **Thread Affinity**: Controlling thread placement on CPU cores

### Real-World Analogy:
OpenMP advanced features are like having specialized tools and techniques in a kitchen. Nested parallelism is like having sub-teams within teams, task constructs are like having a dynamic task assignment system, and thread affinity is like assigning specific workers to specific stations.

### Example: OpenMP Advanced Features
```java
import java.util.concurrent.*;

public class OpenMPAdvancedFeatures {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== OpenMP Advanced Features Demo ===");
        
        // Demonstrate nested parallelism
        demonstrateNestedParallelism();
        
        // Demonstrate task construct
        demonstrateTaskConstruct();
        
        // Demonstrate reduction
        demonstrateReduction();
    }
    
    private static void demonstrateNestedParallelism() throws InterruptedException {
        System.out.println("\n=== Nested Parallelism ===");
        
        // Simulate nested parallel regions
        int outerThreads = 2;
        int innerThreads = 2;
        
        ExecutorService outerExecutor = Executors.newFixedThreadPool(outerThreads);
        
        for (int i = 0; i < outerThreads; i++) {
            final int outerId = i;
            outerExecutor.submit(() -> {
                System.out.println("Outer thread " + outerId + " starting");
                
                // Nested parallel region
                ExecutorService innerExecutor = Executors.newFixedThreadPool(innerThreads);
                
                for (int j = 0; j < innerThreads; j++) {
                    final int innerId = j;
                    innerExecutor.submit(() -> {
                        System.out.println("Inner thread " + innerId + " in outer thread " + outerId);
                    });
                }
                
                innerExecutor.shutdown();
                try {
                    innerExecutor.awaitTermination(1, TimeUnit.SECONDS);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Outer thread " + outerId + " completed");
            });
        }
        
        outerExecutor.shutdown();
        outerExecutor.awaitTermination(2, TimeUnit.SECONDS);
    }
    
    private static void demonstrateTaskConstruct() throws InterruptedException {
        System.out.println("\n=== Task Construct ===");
        
        // Simulate dynamic task creation
        ExecutorService executor = Executors.newFixedThreadPool(4);
        BlockingQueue<Runnable> taskQueue = new LinkedBlockingQueue<>();
        
        // Task generator
        Thread taskGenerator = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                final int taskId = i;
                taskQueue.offer(() -> {
                    System.out.println("Executing task " + taskId + " on thread " + 
                                     Thread.currentThread().getId());
                    try { Thread.sleep(500); } catch (InterruptedException e) {}
                });
            }
        });
        
        // Task executor
        Thread taskExecutor = new Thread(() -> {
            while (true) {
                Runnable task = taskQueue.poll();
                if (task == null) {
                    try { Thread.sleep(100); } catch (InterruptedException e) { break; }
                    continue;
                }
                executor.submit(task);
            }
        });
        
        taskGenerator.start();
        taskExecutor.start();
        
        taskGenerator.join();
        Thread.sleep(2000); // Let tasks complete
        taskExecutor.interrupt();
        
        executor.shutdown();
    }
    
    private static void demonstrateReduction() throws InterruptedException {
        System.out.println("\n=== Reduction ===");
        
        int[] array = new int[1000000];
        Arrays.fill(array, 1);
        
        // Simulate reduction operation
        int numThreads = 4;
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        AtomicInteger globalSum = new AtomicInteger(0);
        
        int chunkSize = array.length / numThreads;
        CountDownLatch latch = new CountDownLatch(numThreads);
        
        for (int i = 0; i < numThreads; i++) {
            final int start = i * chunkSize;
            final int end = (i == numThreads - 1) ? array.length : (i + 1) * chunkSize;
            
            executor.submit(() -> {
                int localSum = 0;
                for (int j = start; j < end; j++) {
                    localSum += array[j];
                }
                globalSum.addAndGet(localSum);
                latch.countDown();
            });
        }
        
        latch.await();
        System.out.println("Reduction sum: " + globalSum.get());
        
        executor.shutdown();
    }
}
```

This comprehensive section covers all aspects of OpenMP, from basic concepts to advanced features, with practical examples and real-world analogies to help understand these complex concepts from the ground up.