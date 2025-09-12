# Section 1 – Parallel Computing Fundamentals

## 1.1 What is Parallel Computing

Parallel computing is a computational approach that breaks down complex problems into smaller, independent tasks that can be executed simultaneously on multiple processors or cores. Think of it like having multiple chefs working on different parts of a meal simultaneously, rather than one chef doing everything sequentially.

### Key Concepts:
- **Simultaneous Execution**: Multiple tasks run at the same time
- **Problem Decomposition**: Breaking complex problems into smaller parts
- **Resource Utilization**: Making better use of available computing resources
- **Performance Enhancement**: Achieving faster results through parallelization

### Real-World Analogy:
Imagine a restaurant kitchen where instead of one chef preparing a 5-course meal sequentially, you have multiple chefs working simultaneously - one preparing appetizers, another working on the main course, and a third handling desserts. This parallel approach significantly reduces the total cooking time.

### Example in Java:
```java
public class ParallelExample {
    public static void main(String[] args) {
        // Sequential approach
        long startTime = System.currentTimeMillis();
        
        // Task 1: Calculate sum of numbers
        int sum = calculateSum(1000000);
        
        // Task 2: Find maximum number
        int max = findMax(1000000);
        
        // Task 3: Sort array
        int[] sorted = sortArray(1000000);
        
        long endTime = System.currentTimeMillis();
        System.out.println("Sequential time: " + (endTime - startTime) + "ms");
        
        // Parallel approach using CompletableFuture
        startTime = System.currentTimeMillis();
        
        CompletableFuture<Integer> sumFuture = CompletableFuture.supplyAsync(() -> calculateSum(1000000));
        CompletableFuture<Integer> maxFuture = CompletableFuture.supplyAsync(() -> findMax(1000000));
        CompletableFuture<int[]> sortFuture = CompletableFuture.supplyAsync(() -> sortArray(1000000));
        
        // Wait for all tasks to complete
        CompletableFuture.allOf(sumFuture, maxFuture, sortFuture).join();
        
        endTime = System.currentTimeMillis();
        System.out.println("Parallel time: " + (endTime - startTime) + "ms");
    }
    
    private static int calculateSum(int n) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += i;
        }
        return sum;
    }
    
    private static int findMax(int n) {
        int max = 0;
        for (int i = 0; i < n; i++) {
            max = Math.max(max, i);
        }
        return max;
    }
    
    private static int[] sortArray(int n) {
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = n - i;
        }
        Arrays.sort(arr);
        return arr;
    }
}
```

## 1.2 Parallel vs Sequential Computing

Sequential computing processes tasks one after another, while parallel computing processes multiple tasks simultaneously. The key difference lies in how computational resources are utilized.

### Sequential Computing Characteristics:
- **Single-threaded execution**: One task at a time
- **Predictable execution order**: Tasks follow a specific sequence
- **Simple debugging**: Easier to trace execution flow
- **Limited resource utilization**: Only uses one processor/core

### Parallel Computing Characteristics:
- **Multi-threaded execution**: Multiple tasks simultaneously
- **Unpredictable execution order**: Tasks may complete in different orders
- **Complex debugging**: Harder to trace due to concurrency
- **Optimal resource utilization**: Uses multiple processors/cores

### Real-World Analogy:
**Sequential**: Like a single-lane highway where cars must follow one behind another
**Parallel**: Like a multi-lane highway where multiple cars can travel side by side

### Performance Comparison Example:
```java
public class SequentialVsParallel {
    private static final int ARRAY_SIZE = 10000000;
    
    public static void main(String[] args) {
        int[] numbers = generateRandomArray(ARRAY_SIZE);
        
        // Sequential processing
        long startTime = System.currentTimeMillis();
        int sequentialSum = calculateSumSequential(numbers);
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        // Parallel processing
        startTime = System.currentTimeMillis();
        int parallelSum = calculateSumParallel(numbers);
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Sequential sum: " + sequentialSum + ", Time: " + sequentialTime + "ms");
        System.out.println("Parallel sum: " + parallelSum + ", Time: " + parallelTime + "ms");
        System.out.println("Speedup: " + (double)sequentialTime / parallelTime);
    }
    
    private static int calculateSumSequential(int[] numbers) {
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        return sum;
    }
    
    private static int calculateSumParallel(int[] numbers) {
        return Arrays.stream(numbers)
                .parallel()
                .sum();
    }
    
    private static int[] generateRandomArray(int size) {
        Random random = new Random();
        return random.ints(size, 1, 100).toArray();
    }
}
```

## 1.3 Parallel vs Concurrent Computing

While often used interchangeably, parallel and concurrent computing are distinct concepts:

### Concurrent Computing:
- **Logical parallelism**: Multiple tasks appear to run simultaneously
- **Time-slicing**: CPU switches between tasks rapidly
- **Single processor**: Tasks share CPU time
- **Cooperative multitasking**: Tasks yield control voluntarily

### Parallel Computing:
- **Physical parallelism**: Tasks actually run simultaneously
- **True simultaneity**: Multiple processors/cores work independently
- **Multiple processors**: Each task has dedicated resources
- **Hardware-based**: Achieved through multiple cores/processors

### Real-World Analogy:
**Concurrent**: Like a juggler keeping multiple balls in the air by rapidly switching attention between them
**Parallel**: Like multiple jugglers each keeping their own set of balls in the air simultaneously

### Example Illustrating the Difference:
```java
public class ConcurrentVsParallel {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Execution (Time-slicing) ===");
        
        // Concurrent execution on single thread
        Thread concurrentThread = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Concurrent Task A: " + i);
                try { Thread.sleep(100); } catch (InterruptedException e) {}
            }
        });
        
        Thread concurrentThread2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Concurrent Task B: " + i);
                try { Thread.sleep(100); } catch (InterruptedException e) {}
            }
        });
        
        concurrentThread.start();
        concurrentThread2.start();
        concurrentThread.join();
        concurrentThread2.join();
        
        System.out.println("\n=== Parallel Execution (Multiple cores) ===");
        
        // Parallel execution using thread pool
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        Future<?> future1 = executor.submit(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Parallel Task A: " + i);
                try { Thread.sleep(100); } catch (InterruptedException e) {}
            }
        });
        
        Future<?> future2 = executor.submit(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Parallel Task B: " + i);
                try { Thread.sleep(100); } catch (InterruptedException e) {}
            }
        });
        
        future1.get();
        future2.get();
        executor.shutdown();
    }
}
```

## 1.4 Parallel Computing History and Evolution

Parallel computing has evolved significantly over the decades, driven by the need for faster computation and more efficient resource utilization.

### Historical Timeline:

#### 1950s-1960s: Early Beginnings
- **ILLIAC IV**: First parallel supercomputer (1966)
- **CDC 6600**: Early vector processing
- **Conceptual foundations**: Flynn's taxonomy established

#### 1970s-1980s: Commercial Parallel Systems
- **Cray-1**: First successful vector supercomputer (1976)
- **Connection Machine**: Massively parallel architecture
- **Transputer**: Dedicated parallel processing chips

#### 1990s-2000s: Distributed Computing Era
- **Beowulf clusters**: Commodity hardware clusters
- **MPI standardization**: Message passing interface
- **Grid computing**: Internet-based parallel computing

#### 2000s-Present: Multicore Revolution
- **Moore's Law plateau**: Clock speed limitations
- **Multicore processors**: Intel Core 2 Duo (2006)
- **GPU computing**: CUDA and OpenCL
- **Cloud computing**: Distributed parallel services

### Real-World Impact:
The evolution from single-core to multicore processors mirrors how cities evolved from single-lane roads to multi-lane highways and eventually to complex transportation networks.

### Modern Parallel Computing Landscape:
```java
public class ParallelComputingEvolution {
    public static void main(String[] args) {
        System.out.println("Available CPU cores: " + Runtime.getRuntime().availableProcessors());
        
        // Demonstrate different parallel computing approaches
        
        // 1. Traditional threading (1990s approach)
        demonstrateTraditionalThreading();
        
        // 2. Thread pools (2000s approach)
        demonstrateThreadPools();
        
        // 3. Fork-Join framework (2010s approach)
        demonstrateForkJoin();
        
        // 4. Streams parallel processing (Modern approach)
        demonstrateParallelStreams();
    }
    
    private static void demonstrateTraditionalThreading() {
        System.out.println("\n=== Traditional Threading ===");
        Thread thread = new Thread(() -> System.out.println("Traditional thread execution"));
        thread.start();
        try { thread.join(); } catch (InterruptedException e) {}
    }
    
    private static void demonstrateThreadPools() {
        System.out.println("\n=== Thread Pools ===");
        ExecutorService executor = Executors.newFixedThreadPool(4);
        executor.submit(() -> System.out.println("Thread pool execution"));
        executor.shutdown();
    }
    
    private static void demonstrateForkJoin() {
        System.out.println("\n=== Fork-Join Framework ===");
        ForkJoinPool pool = new ForkJoinPool();
        pool.submit(() -> System.out.println("Fork-join execution"));
        pool.shutdown();
    }
    
    private static void demonstrateParallelStreams() {
        System.out.println("\n=== Parallel Streams ===");
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        int sum = numbers.parallelStream()
                        .mapToInt(Integer::intValue)
                        .sum();
        System.out.println("Parallel stream sum: " + sum);
    }
}
```

## 1.5 Parallel Computing Benefits and Challenges

Parallel computing offers significant advantages but also presents unique challenges that must be carefully managed.

### Benefits:

#### 1. Performance Improvement
- **Speedup**: Faster execution through simultaneous processing
- **Throughput**: Higher task completion rates
- **Scalability**: Ability to handle larger problems

#### 2. Resource Utilization
- **Efficiency**: Better use of available hardware
- **Cost-effectiveness**: More work per unit of hardware
- **Energy efficiency**: Parallel tasks can be more energy-efficient

#### 3. Problem-solving Capability
- **Larger problems**: Handle problems that exceed single-core capacity
- **Real-time processing**: Meet timing requirements for time-critical applications
- **Complex simulations**: Run sophisticated models and simulations

### Challenges:

#### 1. Complexity
- **Programming difficulty**: More complex than sequential programming
- **Debugging challenges**: Harder to identify and fix issues
- **Testing complexity**: More difficult to ensure correctness

#### 2. Synchronization Issues
- **Race conditions**: Unpredictable behavior from concurrent access
- **Deadlocks**: Situations where processes wait indefinitely
- **Load balancing**: Uneven distribution of work

#### 3. Overhead
- **Communication costs**: Inter-process communication overhead
- **Memory consistency**: Ensuring data consistency across processors
- **Amdahl's Law limitations**: Sequential portions limit speedup

### Real-World Analogy:
Parallel computing is like organizing a large event. The benefits include faster completion and better resource utilization, but challenges include coordinating multiple teams, managing dependencies, and ensuring everything works together harmoniously.

### Example Demonstrating Benefits and Challenges:
```java
public class ParallelBenefitsAndChallenges {
    private static final int TASK_COUNT = 1000000;
    private static volatile int sharedCounter = 0;
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Demonstrating Parallel Benefits ===");
        demonstrateBenefits();
        
        System.out.println("\n=== Demonstrating Parallel Challenges ===");
        demonstrateChallenges();
    }
    
    private static void demonstrateBenefits() {
        // Benefit: Performance improvement
        List<Integer> numbers = generateNumbers(TASK_COUNT);
        
        long startTime = System.currentTimeMillis();
        int sequentialSum = numbers.stream().mapToInt(Integer::intValue).sum();
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        startTime = System.currentTimeMillis();
        int parallelSum = numbers.parallelStream().mapToInt(Integer::intValue).sum();
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Sequential sum: " + sequentialSum + " in " + sequentialTime + "ms");
        System.out.println("Parallel sum: " + parallelSum + " in " + parallelTime + "ms");
        System.out.println("Speedup: " + (double)sequentialTime / parallelTime);
    }
    
    private static void demonstrateChallenges() throws InterruptedException {
        // Challenge: Race conditions
        System.out.println("Demonstrating race condition challenge:");
        
        ExecutorService executor = Executors.newFixedThreadPool(10);
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < 10; i++) {
            futures.add(executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    sharedCounter++; // Race condition!
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        System.out.println("Expected counter value: 10000");
        System.out.println("Actual counter value: " + sharedCounter);
        System.out.println("Race condition caused incorrect result!");
        
        executor.shutdown();
        
        // Solution: Using synchronized access
        demonstrateSolution();
    }
    
    private static void demonstrateSolution() throws InterruptedException {
        System.out.println("\nDemonstrating synchronized solution:");
        
        AtomicInteger atomicCounter = new AtomicInteger(0);
        ExecutorService executor = Executors.newFixedThreadPool(10);
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < 10; i++) {
            futures.add(executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    atomicCounter.incrementAndGet(); // Thread-safe!
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        System.out.println("Atomic counter value: " + atomicCounter.get());
        
        executor.shutdown();
    }
    
    private static List<Integer> generateNumbers(int count) {
        return IntStream.rangeClosed(1, count)
                       .boxed()
                       .collect(Collectors.toList());
    }
}
```

## 1.6 Parallel Computing Use Cases

Parallel computing finds applications across numerous domains, each with specific requirements and characteristics.

### Scientific Computing
- **Climate modeling**: Simulating weather patterns and climate change
- **Molecular dynamics**: Studying molecular interactions
- **Astrophysics**: Modeling galaxy formation and stellar evolution
- **Quantum mechanics**: Solving Schrödinger equations

### Engineering Applications
- **Finite element analysis**: Structural analysis and design
- **Computational fluid dynamics**: Fluid flow simulations
- **Signal processing**: Audio, video, and communication signal processing
- **Computer-aided design**: 3D modeling and rendering

### Business and Finance
- **Risk analysis**: Monte Carlo simulations for financial risk
- **Algorithmic trading**: High-frequency trading systems
- **Data mining**: Large-scale data analysis and pattern recognition
- **Fraud detection**: Real-time transaction monitoring

### Real-World Analogy:
Parallel computing use cases are like different types of assembly lines. Scientific computing is like a research lab with multiple experiments running simultaneously, while business applications are like a factory with different production lines working in parallel.

### Example: Parallel Image Processing
```java
public class ParallelImageProcessing {
    public static void main(String[] args) {
        int width = 1920;
        int height = 1080;
        int[][] image = generateTestImage(width, height);
        
        System.out.println("Processing " + width + "x" + height + " image...");
        
        // Sequential processing
        long startTime = System.currentTimeMillis();
        int[][] sequentialResult = processImageSequential(image);
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        // Parallel processing
        startTime = System.currentTimeMillis();
        int[][] parallelResult = processImageParallel(image);
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Sequential processing time: " + sequentialTime + "ms");
        System.out.println("Parallel processing time: " + parallelTime + "ms");
        System.out.println("Speedup: " + (double)sequentialTime / parallelTime);
    }
    
    private static int[][] generateTestImage(int width, int height) {
        int[][] image = new int[height][width];
        Random random = new Random();
        
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                image[y][x] = random.nextInt(256);
            }
        }
        
        return image;
    }
    
    private static int[][] processImageSequential(int[][] image) {
        int height = image.length;
        int width = image[0].length;
        int[][] result = new int[height][width];
        
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                // Simulate image processing (e.g., edge detection)
                result[y][x] = applyFilter(image, x, y);
            }
        }
        
        return result;
    }
    
    private static int[][] processImageParallel(int[][] image) {
        int height = image.length;
        int width = image[0].length;
        int[][] result = new int[height][width];
        
        // Divide image into horizontal strips for parallel processing
        int numThreads = Runtime.getRuntime().availableProcessors();
        int stripHeight = height / numThreads;
        
        ExecutorService executor = ExecutorService.newFixedThreadPool(numThreads);
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < numThreads; i++) {
            final int startY = i * stripHeight;
            final int endY = (i == numThreads - 1) ? height : (i + 1) * stripHeight;
            
            futures.add(executor.submit(() -> {
                for (int y = startY; y < endY; y++) {
                    for (int x = 0; x < width; x++) {
                        result[y][x] = applyFilter(image, x, y);
                    }
                }
            }));
        }
        
        // Wait for all threads to complete
        for (Future<?> future : futures) {
            try {
                future.get();
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }
        
        executor.shutdown();
        return result;
    }
    
    private static int applyFilter(int[][] image, int x, int y) {
        // Simulate a simple filter operation
        int height = image.length;
        int width = image[0].length;
        
        int sum = 0;
        int count = 0;
        
        // 3x3 neighborhood
        for (int dy = -1; dy <= 1; dy++) {
            for (int dx = -1; dx <= 1; dx++) {
                int nx = x + dx;
                int ny = y + dy;
                
                if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
                    sum += image[ny][nx];
                    count++;
                }
            }
        }
        
        return sum / count;
    }
}
```

## 1.7 Parallel Computing Models

Parallel computing models define how parallel programs are structured and how they interact with the underlying hardware.

### 1. Shared Memory Model
- **Single address space**: All processors share the same memory
- **Direct memory access**: Processors can directly access any memory location
- **Synchronization required**: Need mechanisms to prevent race conditions
- **Examples**: SMP systems, multicore processors

### 2. Distributed Memory Model
- **Separate address spaces**: Each processor has its own memory
- **Message passing**: Processors communicate through messages
- **No shared memory**: Cannot directly access other processors' memory
- **Examples**: Clusters, distributed systems

### 3. Hybrid Model
- **Combination**: Mix of shared and distributed memory
- **Hierarchical structure**: Multiple levels of memory hierarchy
- **Complex programming**: Requires handling both models
- **Examples**: NUMA systems, modern supercomputers

### Real-World Analogy:
- **Shared Memory**: Like a shared office where everyone can access the same filing cabinet
- **Distributed Memory**: Like separate offices where people communicate via email
- **Hybrid**: Like an office building with shared floors but separate departments

### Example: Shared Memory Model
```java
public class SharedMemoryModel {
    private static final int NUM_THREADS = 4;
    private static final int ARRAY_SIZE = 1000000;
    
    // Shared memory (accessible by all threads)
    private static int[] sharedArray = new int[ARRAY_SIZE];
    private static int sharedSum = 0;
    private static final Object lock = new Object();
    
    public static void main(String[] args) throws InterruptedException {
        // Initialize shared array
        initializeArray();
        
        System.out.println("=== Shared Memory Model Demo ===");
        System.out.println("Array size: " + ARRAY_SIZE);
        System.out.println("Number of threads: " + NUM_THREADS);
        
        // Calculate sum using shared memory
        calculateSumSharedMemory();
        
        // Verify result
        int expectedSum = Arrays.stream(sharedArray).sum();
        System.out.println("Expected sum: " + expectedSum);
        System.out.println("Calculated sum: " + sharedSum);
    }
    
    private static void initializeArray() {
        Random random = new Random();
        for (int i = 0; i < ARRAY_SIZE; i++) {
            sharedArray[i] = random.nextInt(100);
        }
    }
    
    private static void calculateSumSharedMemory() throws InterruptedException {
        Thread[] threads = new Thread[NUM_THREADS];
        int chunkSize = ARRAY_SIZE / NUM_THREADS;
        
        // Create threads that work on shared memory
        for (int i = 0; i < NUM_THREADS; i++) {
            final int startIndex = i * chunkSize;
            final int endIndex = (i == NUM_THREADS - 1) ? ARRAY_SIZE : (i + 1) * chunkSize;
            
            threads[i] = new Thread(() -> {
                int localSum = 0;
                
                // Each thread processes its portion of the shared array
                for (int j = startIndex; j < endIndex; j++) {
                    localSum += sharedArray[j];
                }
                
                // Update shared variable with synchronization
                synchronized (lock) {
                    sharedSum += localSum;
                }
            });
            
            threads[i].start();
        }
        
        // Wait for all threads to complete
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 1.8 Parallel Computing Standards

Standards ensure interoperability, portability, and consistency across different parallel computing platforms and implementations.

### Key Standards:

#### 1. OpenMP
- **Purpose**: Shared memory parallel programming
- **Language bindings**: C, C++, Fortran
- **Features**: Threading, work sharing, synchronization
- **Platform**: Multi-platform (Linux, Windows, macOS)

#### 2. MPI (Message Passing Interface)
- **Purpose**: Distributed memory parallel programming
- **Language bindings**: C, C++, Fortran
- **Features**: Point-to-point and collective communication
- **Platform**: HPC clusters, supercomputers

#### 3. POSIX Threads (pthreads)
- **Purpose**: Threading standard for Unix-like systems
- **Features**: Thread creation, synchronization, communication
- **Platform**: Linux, Unix, macOS

#### 4. OpenCL
- **Purpose**: Heterogeneous parallel computing
- **Features**: GPU, CPU, and other accelerators
- **Platform**: Cross-platform

### Real-World Analogy:
Standards are like traffic rules that ensure all drivers can navigate roads safely regardless of their vehicle type or destination. Similarly, parallel computing standards ensure that programs can run on different hardware platforms consistently.

### Example: OpenMP Standard Usage
```java
// Note: This is a conceptual example. Java doesn't have native OpenMP support,
// but we can demonstrate similar concepts using Java's parallel capabilities.

public class ParallelStandardsDemo {
    public static void main(String[] args) {
        System.out.println("=== Demonstrating Parallel Standards Concepts ===");
        
        // Simulate OpenMP-like parallel region
        demonstrateOpenMPConcept();
        
        // Simulate MPI-like message passing
        demonstrateMPIConcept();
        
        // Demonstrate POSIX-like threading
        demonstrateThreadingStandard();
    }
    
    private static void demonstrateOpenMPConcept() {
        System.out.println("\n=== OpenMP-like Parallel Region ===");
        
        int[] data = generateData(1000000);
        
        // Simulate #pragma omp parallel for
        int sum = Arrays.stream(data)
                       .parallel()  // Similar to OpenMP parallel directive
                       .sum();
        
        System.out.println("Parallel sum: " + sum);
    }
    
    private static void demonstrateMPIConcept() {
        System.out.println("\n=== MPI-like Message Passing ===");
        
        // Simulate MPI rank and size
        int rank = 0; // Process rank
        int size = Runtime.getRuntime().availableProcessors(); // Number of processes
        
        System.out.println("Process " + rank + " of " + size + " processes");
        
        // Simulate MPI_Bcast (broadcast)
        String message = "Hello from process " + rank;
        System.out.println("Broadcasting: " + message);
        
        // Simulate MPI_Reduce (reduction)
        int localValue = rank * 100;
        System.out.println("Local value: " + localValue);
        
        // Simulate reduction operation
        int globalSum = localValue * size; // Simplified reduction
        System.out.println("Global sum: " + globalSum);
    }
    
    private static void demonstrateThreadingStandard() {
        System.out.println("\n=== POSIX-like Threading ===");
        
        // Simulate pthread_create
        Thread[] threads = new Thread[4];
        
        for (int i = 0; i < threads.length; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + threadId + " executing");
                
                // Simulate work
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                System.out.println("Thread " + threadId + " completed");
            });
        }
        
        // Start all threads (simulate pthread_create)
        for (Thread thread : threads) {
            thread.start();
        }
        
        // Wait for all threads (simulate pthread_join)
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("All threads completed");
    }
    
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
}
```

This comprehensive section covers all the fundamental concepts of parallel computing, from basic definitions to practical examples and real-world applications. Each subsection provides detailed explanations, code examples, and analogies to help understand these complex concepts from the ground up.