# Section 13 – Performance and Scalability

## 13.1 Amdahl's Law

Amdahl's Law predicts the theoretical speedup of a program when using multiple processors, based on the proportion of the program that can be parallelized.

### Key Concepts
- **Serial Portion**: Part of the program that cannot be parallelized
- **Parallel Portion**: Part of the program that can be parallelized
- **Speedup**: Performance improvement with multiple processors
- **Limitations**: Theoretical maximum speedup

### Real-World Analogy
Think of a restaurant where 80% of the work can be done by multiple chefs in parallel, but 20% must be done by a single manager. Adding more chefs helps, but the manager's work will always be a bottleneck.

### Java Example
```java
public class AmdahlsLawExample {
    // Calculate speedup using Amdahl's Law
    public static double calculateSpeedup(double parallelFraction, int processors) {
        if (parallelFraction < 0 || parallelFraction > 1) {
            throw new IllegalArgumentException("Parallel fraction must be between 0 and 1");
        }
        if (processors < 1) {
            throw new IllegalArgumentException("Number of processors must be at least 1");
        }
        
        double serialFraction = 1 - parallelFraction;
        return 1 / (serialFraction + parallelFraction / processors);
    }
    
    // Demonstrate Amdahl's Law
    public static void demonstrateAmdahlsLaw() {
        double[] parallelFractions = {0.5, 0.8, 0.9, 0.95, 0.99};
        int[] processors = {1, 2, 4, 8, 16, 32, 64};
        
        System.out.println("Amdahl's Law Speedup Calculations:");
        System.out.println("Processors\t50%\t80%\t90%\t95%\t99%");
        
        for (int p : processors) {
            System.out.print(p + "\t\t");
            for (double pf : parallelFractions) {
                double speedup = calculateSpeedup(pf, p);
                System.out.printf("%.2f\t", speedup);
            }
            System.out.println();
        }
    }
    
    // Practical example: Parallel matrix multiplication
    public static class ParallelMatrixMultiplier {
        private final int[][] matrixA;
        private final int[][] matrixB;
        private final int[][] result;
        private final int size;
        
        public ParallelMatrixMultiplier(int size) {
            this.size = size;
            this.matrixA = new int[size][size];
            this.matrixB = new int[size][size];
            this.result = new int[size][size];
            
            // Initialize matrices with random values
            Random random = new Random();
            for (int i = 0; i < size; i++) {
                for (int j = 0; j < size; j++) {
                    matrixA[i][j] = random.nextInt(100);
                    matrixB[i][j] = random.nextInt(100);
                }
            }
        }
        
        public void multiplySequential() {
            for (int i = 0; i < size; i++) {
                for (int j = 0; j < size; j++) {
                    result[i][j] = 0;
                    for (int k = 0; k < size; k++) {
                        result[i][j] += matrixA[i][k] * matrixB[k][j];
                    }
                }
            }
        }
        
        public void multiplyParallel(int threadCount) throws InterruptedException {
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);
            CountDownLatch latch = new CountDownLatch(threadCount);
            
            int rowsPerThread = size / threadCount;
            
            for (int t = 0; t < threadCount; t++) {
                final int startRow = t * rowsPerThread;
                final int endRow = (t == threadCount - 1) ? size : (t + 1) * rowsPerThread;
                
                executor.submit(() -> {
                    try {
                        for (int i = startRow; i < endRow; i++) {
                            for (int j = 0; j < size; j++) {
                                result[i][j] = 0;
                                for (int k = 0; k < size; k++) {
                                    result[i][j] += matrixA[i][k] * matrixB[k][j];
                                }
                            }
                        }
                    } finally {
                        latch.countDown();
                    }
                });
            }
            
            latch.await();
            executor.shutdown();
        }
        
        public void measurePerformance() throws InterruptedException {
            int[] threadCounts = {1, 2, 4, 8, 16};
            
            System.out.println("\nMatrix Multiplication Performance (1000x1000):");
            System.out.println("Threads\tTime (ms)\tSpeedup");
            
            long sequentialTime = 0;
            
            for (int threads : threadCounts) {
                long startTime = System.currentTimeMillis();
                
                if (threads == 1) {
                    multiplySequential();
                } else {
                    multiplyParallel(threads);
                }
                
                long endTime = System.currentTimeMillis();
                long executionTime = endTime - startTime;
                
                if (threads == 1) {
                    sequentialTime = executionTime;
                }
                
                double speedup = (double) sequentialTime / executionTime;
                System.out.println(threads + "\t" + executionTime + "\t\t" + String.format("%.2f", speedup));
            }
        }
    }
}
```

## 13.2 Gustafson's Law

Gustafson's Law provides an alternative view to Amdahl's Law, focusing on the scalability of problems rather than fixed problem sizes.

### Key Concepts
- **Scalable Problems**: Problems that grow with available resources
- **Fixed Time**: Constant execution time regardless of problem size
- **Linear Speedup**: Performance scales linearly with processors
- **Real-World Applications**: More applicable to practical scenarios

### Real-World Analogy
Think of a data processing company that can handle more data as they hire more employees, rather than trying to process the same amount of data faster.

### Java Example
```java
public class GustafsonsLawExample {
    // Calculate speedup using Gustafson's Law
    public static double calculateGustafsonSpeedup(double parallelFraction, int processors) {
        if (parallelFraction < 0 || parallelFraction > 1) {
            throw new IllegalArgumentException("Parallel fraction must be between 0 and 1");
        }
        if (processors < 1) {
            throw new IllegalArgumentException("Number of processors must be at least 1");
        }
        
        return processors - (processors - 1) * (1 - parallelFraction);
    }
    
    // Demonstrate Gustafson's Law
    public static void demonstrateGustafsonsLaw() {
        double[] parallelFractions = {0.5, 0.8, 0.9, 0.95, 0.99};
        int[] processors = {1, 2, 4, 8, 16, 32, 64};
        
        System.out.println("Gustafson's Law Speedup Calculations:");
        System.out.println("Processors\t50%\t80%\t90%\t95%\t99%");
        
        for (int p : processors) {
            System.out.print(p + "\t\t");
            for (double pf : parallelFractions) {
                double speedup = calculateGustafsonSpeedup(pf, p);
                System.out.printf("%.2f\t", speedup);
            }
            System.out.println();
        }
    }
    
    // Scalable problem example: Image processing
    public static class ScalableImageProcessor {
        private final int baseWidth;
        private final int baseHeight;
        private final int[][] image;
        
        public ScalableImageProcessor(int baseWidth, int baseHeight) {
            this.baseWidth = baseWidth;
            this.baseHeight = baseHeight;
            this.image = new int[baseHeight][baseWidth];
            
            // Initialize with random pixel values
            Random random = new Random();
            for (int i = 0; i < baseHeight; i++) {
                for (int j = 0; j < baseWidth; j++) {
                    image[i][j] = random.nextInt(256);
                }
            }
        }
        
        public void processImageSequential(int scaleFactor) {
            int width = baseWidth * scaleFactor;
            int height = baseHeight * scaleFactor;
            
            for (int i = 0; i < height; i++) {
                for (int j = 0; j < width; j++) {
                    // Simulate image processing
                    int pixel = image[i % baseHeight][j % baseWidth];
                    pixel = (pixel + 50) % 256; // Simple transformation
                }
            }
        }
        
        public void processImageParallel(int scaleFactor, int threadCount) throws InterruptedException {
            int width = baseWidth * scaleFactor;
            int height = baseHeight * scaleFactor;
            
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);
            CountDownLatch latch = new CountDownLatch(threadCount);
            
            int rowsPerThread = height / threadCount;
            
            for (int t = 0; t < threadCount; t++) {
                final int startRow = t * rowsPerThread;
                final int endRow = (t == threadCount - 1) ? height : (t + 1) * rowsPerThread;
                
                executor.submit(() -> {
                    try {
                        for (int i = startRow; i < endRow; i++) {
                            for (int j = 0; j < width; j++) {
                                // Simulate image processing
                                int pixel = image[i % baseHeight][j % baseWidth];
                                pixel = (pixel + 50) % 256; // Simple transformation
                            }
                        }
                    } finally {
                        latch.countDown();
                    }
                });
            }
            
            latch.await();
            executor.shutdown();
        }
        
        public void measureScalability() throws InterruptedException {
            int[] threadCounts = {1, 2, 4, 8, 16};
            int[] scaleFactors = {1, 2, 4, 8, 16};
            
            System.out.println("\nScalable Image Processing Performance:");
            System.out.println("Scale\tThreads\tTime (ms)\tSpeedup");
            
            for (int scale : scaleFactors) {
                long sequentialTime = 0;
                
                for (int threads : threadCounts) {
                    long startTime = System.currentTimeMillis();
                    
                    if (threads == 1) {
                        processImageSequential(scale);
                    } else {
                        processImageParallel(scale, threads);
                    }
                    
                    long endTime = System.currentTimeMillis();
                    long executionTime = endTime - startTime;
                    
                    if (threads == 1) {
                        sequentialTime = executionTime;
                    }
                    
                    double speedup = (double) sequentialTime / executionTime;
                    System.out.println(scale + "\t" + threads + "\t" + executionTime + "\t\t" + String.format("%.2f", speedup));
                }
            }
        }
    }
}
```

## 13.3 Thread Overhead

Thread overhead refers to the cost of creating, managing, and switching between threads, which can impact performance.

### Key Concepts
- **Creation Cost**: Time and memory to create threads
- **Context Switching**: Cost of switching between threads
- **Memory Usage**: Memory required per thread
- **Scheduling Overhead**: Cost of thread scheduling

### Real-World Analogy
Think of hiring employees for a project. Each employee has a cost (salary, benefits, training), and switching between employees takes time and effort.

### Java Example
```java
public class ThreadOverheadExample {
    // Measure thread creation overhead
    public static class ThreadCreationOverhead {
        public long measureThreadCreation(int threadCount) {
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    // Do nothing
                });
            }
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public void demonstrateThreadCreationOverhead() {
            int[] threadCounts = {1, 10, 100, 1000, 10000};
            
            System.out.println("Thread Creation Overhead:");
            System.out.println("Threads\tTime (ns)\tTime per Thread (ns)");
            
            for (int count : threadCounts) {
                long totalTime = measureThreadCreation(count);
                long timePerThread = totalTime / count;
                System.out.println(count + "\t" + totalTime + "\t" + timePerThread);
            }
        }
    }
    
    // Measure context switching overhead
    public static class ContextSwitchingOverhead {
        private final AtomicInteger counter = new AtomicInteger(0);
        private final int iterations;
        
        public ContextSwitchingOverhead(int iterations) {
            this.iterations = iterations;
        }
        
        public long measureContextSwitching(int threadCount) throws InterruptedException {
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        for (int j = 0; j < iterations; j++) {
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
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public void demonstrateContextSwitchingOverhead() throws InterruptedException {
            int[] threadCounts = {1, 2, 4, 8, 16, 32};
            int iterations = 100000;
            
            System.out.println("\nContext Switching Overhead:");
            System.out.println("Threads\tTime (ns)\tTime per Operation (ns)");
            
            for (int count : threadCounts) {
                long totalTime = measureContextSwitching(count);
                long timePerOperation = totalTime / (count * iterations);
                System.out.println(count + "\t" + totalTime + "\t" + timePerOperation);
            }
        }
    }
    
    // Measure memory usage per thread
    public static class ThreadMemoryUsage {
        public void measureThreadMemoryUsage() {
            Runtime runtime = Runtime.getRuntime();
            
            // Measure memory before creating threads
            System.gc();
            long memoryBefore = runtime.totalMemory() - runtime.freeMemory();
            
            // Create many threads
            int threadCount = 1000;
            Thread[] threads = new Thread[threadCount];
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
                threads[i].start();
            }
            
            // Wait a bit for threads to start
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            // Measure memory after creating threads
            System.gc();
            long memoryAfter = runtime.totalMemory() - runtime.freeMemory();
            
            long memoryUsed = memoryAfter - memoryBefore;
            long memoryPerThread = memoryUsed / threadCount;
            
            System.out.println("\nThread Memory Usage:");
            System.out.println("Total memory used: " + memoryUsed / 1024 + " KB");
            System.out.println("Memory per thread: " + memoryPerThread / 1024 + " KB");
            
            // Clean up
            for (Thread thread : threads) {
                thread.interrupt();
            }
        }
    }
}
```

## 13.4 Context Switching Costs

Context switching costs refer to the overhead of switching between threads, including saving and restoring thread state.

### Key Concepts
- **State Saving**: Saving current thread's state
- **State Restoring**: Restoring new thread's state
- **Cache Effects**: Impact on CPU cache
- **Scheduling Overhead**: Cost of thread scheduling decisions

### Real-World Analogy
Think of switching between different tasks at work. You need to save your current work, remember where you left off, then switch to the new task and remember its context.

### Java Example
```java
public class ContextSwitchingCostsExample {
    // Measure context switching costs
    public static class ContextSwitchingCosts {
        private final AtomicInteger counter = new AtomicInteger(0);
        private final int iterations;
        
        public ContextSwitchingCosts(int iterations) {
            this.iterations = iterations;
        }
        
        public long measureContextSwitching(int threadCount) throws InterruptedException {
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        for (int j = 0; j < iterations; j++) {
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
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public void demonstrateContextSwitchingCosts() throws InterruptedException {
            int[] threadCounts = {1, 2, 4, 8, 16, 32, 64};
            int iterations = 100000;
            
            System.out.println("Context Switching Costs:");
            System.out.println("Threads\tTime (ns)\tTime per Operation (ns)\tEfficiency");
            
            long singleThreadTime = measureContextSwitching(1);
            
            for (int count : threadCounts) {
                long totalTime = measureContextSwitching(count);
                long timePerOperation = totalTime / (count * iterations);
                double efficiency = (double) singleThreadTime / totalTime;
                
                System.out.println(count + "\t" + totalTime + "\t" + timePerOperation + "\t\t" + String.format("%.2f", efficiency));
            }
        }
    }
    
    // Measure cache effects
    public static class CacheEffects {
        private final int arraySize;
        private final int[] array;
        
        public CacheEffects(int arraySize) {
            this.arraySize = arraySize;
            this.array = new int[arraySize];
            
            // Initialize array with random values
            Random random = new Random();
            for (int i = 0; i < arraySize; i++) {
                array[i] = random.nextInt(100);
            }
        }
        
        public long measureCacheEffects(int threadCount) throws InterruptedException {
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                final int threadId = i;
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        int startIndex = threadId * (arraySize / threadCount);
                        int endIndex = (threadId == threadCount - 1) ? arraySize : (threadId + 1) * (arraySize / threadCount);
                        
                        for (int j = startIndex; j < endIndex; j++) {
                            array[j] = array[j] * 2; // Simple operation
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
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public void demonstrateCacheEffects() throws InterruptedException {
            int[] threadCounts = {1, 2, 4, 8, 16};
            int arraySize = 1000000;
            
            System.out.println("\nCache Effects:");
            System.out.println("Threads\tTime (ns)\tTime per Element (ns)");
            
            for (int count : threadCounts) {
                long totalTime = measureCacheEffects(count);
                long timePerElement = totalTime / arraySize;
                System.out.println(count + "\t" + totalTime + "\t" + timePerElement);
            }
        }
    }
}
```

## 13.5 Lock Contention

Lock contention occurs when multiple threads compete for the same lock, causing performance degradation.

### Key Concepts
- **Lock Competition**: Multiple threads waiting for the same lock
- **Contention Hotspots**: Areas with high lock contention
- **Lock Granularity**: Size of critical sections
- **Lock-Free Alternatives**: Avoiding locks entirely

### Real-World Analogy
Think of a busy restaurant with only one cash register. Customers have to wait in line, and the more customers there are, the longer everyone waits.

### Java Example
```java
public class LockContentionExample {
    // High contention counter
    public static class HighContentionCounter {
        private int count = 0;
        private final Object lock = new Object();
        
        public void increment() {
            synchronized (lock) {
                count++;
            }
        }
        
        public int getCount() {
            synchronized (lock) {
                return count;
            }
        }
    }
    
    // Low contention counter using atomic operations
    public static class LowContentionCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        public void increment() {
            count.incrementAndGet();
        }
        
        public int getCount() {
            return count.get();
        }
    }
    
    // Measure lock contention
    public static class LockContentionMeasurement {
        public long measureContention(Supplier<Runnable> taskSupplier, int threadCount, int operationsPerThread) throws InterruptedException {
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        for (int j = 0; j < operationsPerThread; j++) {
                            taskSupplier.get().run();
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
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public void demonstrateLockContention() throws InterruptedException {
            HighContentionCounter highContentionCounter = new HighContentionCounter();
            LowContentionCounter lowContentionCounter = new LowContentionCounter();
            
            int[] threadCounts = {1, 2, 4, 8, 16, 32};
            int operationsPerThread = 100000;
            
            System.out.println("Lock Contention Comparison:");
            System.out.println("Threads\tHigh Contention (ns)\tLow Contention (ns)\tSpeedup");
            
            for (int count : threadCounts) {
                long highContentionTime = measureContention(() -> () -> highContentionCounter.increment(), count, operationsPerThread);
                long lowContentionTime = measureContention(() -> () -> lowContentionCounter.increment(), count, operationsPerThread);
                
                double speedup = (double) highContentionTime / lowContentionTime;
                System.out.println(count + "\t" + highContentionTime + "\t\t" + lowContentionTime + "\t\t" + String.format("%.2f", speedup));
            }
        }
    }
    
    // Lock-free data structure
    public static class LockFreeStack<T> {
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        
        private static class Node<T> {
            final T data;
            final AtomicReference<Node<T>> next;
            
            Node(T data) {
                this.data = data;
                this.next = new AtomicReference<>();
            }
        }
        
        public void push(T item) {
            Node<T> newNode = new Node<>(item);
            Node<T> currentHead;
            
            do {
                currentHead = head.get();
                newNode.next.set(currentHead);
            } while (!head.compareAndSet(currentHead, newNode));
        }
        
        public T pop() {
            Node<T> currentHead;
            Node<T> newHead;
            
            do {
                currentHead = head.get();
                if (currentHead == null) {
                    return null;
                }
                newHead = currentHead.next.get();
            } while (!head.compareAndSet(currentHead, newHead));
            
            return currentHead.data;
        }
    }
}
```

## 13.6 False Sharing

False sharing occurs when multiple threads access different variables that happen to be on the same cache line, causing unnecessary cache invalidations.

### Key Concepts
- **Cache Line**: Unit of data transfer between cache and memory
- **False Sharing**: Unnecessary cache invalidations
- **Cache Coherence**: Maintaining cache consistency
- **Padding**: Adding padding to separate variables

### Real-World Analogy
Think of two people working on different parts of the same page. When one person makes a change, the other person's work is also affected because they're working on the same physical page.

### Java Example
```java
public class FalseSharingExample {
    // Variables that might be on the same cache line
    private static volatile int counter1 = 0;
    private static volatile int counter2 = 0;
    
    // Padded variables to avoid false sharing
    private static volatile int paddedCounter1 = 0;
    private static volatile long padding1, padding2, padding3, padding4, padding5, padding6, padding7;
    private static volatile int paddedCounter2 = 0;
    
    // Measure false sharing impact
    public static class FalseSharingMeasurement {
        public long measureFalseSharing(int threadCount, int iterations) throws InterruptedException {
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                final int threadId = i;
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        for (int j = 0; j < iterations; j++) {
                            if (threadId % 2 == 0) {
                                counter1++;
                            } else {
                                counter2++;
                            }
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
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public long measurePaddedCounters(int threadCount, int iterations) throws InterruptedException {
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                final int threadId = i;
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        for (int j = 0; j < iterations; j++) {
                            if (threadId % 2 == 0) {
                                paddedCounter1++;
                            } else {
                                paddedCounter2++;
                            }
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
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public void demonstrateFalseSharing() throws InterruptedException {
            int[] threadCounts = {2, 4, 8, 16};
            int iterations = 1000000;
            
            System.out.println("False Sharing Impact:");
            System.out.println("Threads\tFalse Sharing (ns)\tPadded (ns)\tSpeedup");
            
            for (int count : threadCounts) {
                long falseSharingTime = measureFalseSharing(count, iterations);
                long paddedTime = measurePaddedCounters(count, iterations);
                
                double speedup = (double) falseSharingTime / paddedTime;
                System.out.println(count + "\t" + falseSharingTime + "\t\t" + paddedTime + "\t\t" + String.format("%.2f", speedup));
            }
        }
    }
    
    // Using @Contended annotation (Java 8+)
    public static class ContendedExample {
        @sun.misc.Contended
        private static volatile int contendedCounter1 = 0;
        
        @sun.misc.Contended
        private static volatile int contendedCounter2 = 0;
        
        public static void demonstrateContended() throws InterruptedException {
            int threadCount = 8;
            int iterations = 1000000;
            
            long startTime = System.nanoTime();
            
            Thread[] threads = new Thread[threadCount];
            CountDownLatch startLatch = new CountDownLatch(1);
            CountDownLatch endLatch = new CountDownLatch(threadCount);
            
            for (int i = 0; i < threadCount; i++) {
                final int threadId = i;
                threads[i] = new Thread(() -> {
                    try {
                        startLatch.await();
                        for (int j = 0; j < iterations; j++) {
                            if (threadId % 2 == 0) {
                                contendedCounter1++;
                            } else {
                                contendedCounter2++;
                            }
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
            
            long endTime = System.nanoTime();
            System.out.println("Contended counters time: " + (endTime - startTime) + " ns");
        }
    }
}
```

## 13.7 NUMA Awareness

NUMA (Non-Uniform Memory Access) awareness involves understanding and optimizing for systems where memory access times vary depending on the location of the memory relative to the processor.

### Key Concepts
- **NUMA Nodes**: Groups of processors with local memory
- **Memory Affinity**: Keeping data close to the processor using it
- **Load Balancing**: Distributing work across NUMA nodes
- **Performance Impact**: Significant performance differences

### Real-World Analogy
Think of a company with offices in different cities. It's faster to access files in your local office than to request files from a remote office.

### Java Example
```java
public class NUMAwarenessExample {
    // NUMA-aware thread pool
    public static class NUMAwareThreadPool {
        private final ExecutorService[] executors;
        private final int numaNodeCount;
        
        public NUMAwareThreadPool(int numaNodeCount, int threadsPerNode) {
            this.numaNodeCount = numaNodeCount;
            this.executors = new ExecutorService[numaNodeCount];
            
            for (int i = 0; i < numaNodeCount; i++) {
                executors[i] = Executors.newFixedThreadPool(threadsPerNode);
            }
        }
        
        public void submitTask(int numaNode, Runnable task) {
            if (numaNode >= 0 && numaNode < numaNodeCount) {
                executors[numaNode].submit(task);
            } else {
                // Fallback to first node
                executors[0].submit(task);
            }
        }
        
        public void shutdown() {
            for (ExecutorService executor : executors) {
                executor.shutdown();
            }
        }
    }
    
    // NUMA-aware data structure
    public static class NUMAwareDataStructure {
        private final int[] data;
        private final int numaNodeCount;
        private final int dataPerNode;
        
        public NUMAwareDataStructure(int totalSize, int numaNodeCount) {
            this.numaNodeCount = numaNodeCount;
            this.dataPerNode = totalSize / numaNodeCount;
            this.data = new int[totalSize];
            
            // Initialize data
            for (int i = 0; i < totalSize; i++) {
                data[i] = i;
            }
        }
        
        public void processData(int numaNode) {
            int startIndex = numaNode * dataPerNode;
            int endIndex = (numaNode == numaNodeCount - 1) ? data.length : (numaNode + 1) * dataPerNode;
            
            for (int i = startIndex; i < endIndex; i++) {
                data[i] = data[i] * 2; // Simple operation
            }
        }
        
        public void processDataNUMAware(int numaNode) {
            // Process data in chunks to improve cache locality
            int startIndex = numaNode * dataPerNode;
            int endIndex = (numaNode == numaNodeCount - 1) ? data.length : (numaNode + 1) * dataPerNode;
            
            int chunkSize = 64; // Cache line size
            for (int i = startIndex; i < endIndex; i += chunkSize) {
                int chunkEnd = Math.min(i + chunkSize, endIndex);
                for (int j = i; j < chunkEnd; j++) {
                    data[j] = data[j] * 2;
                }
            }
        }
    }
    
    // Measure NUMA performance
    public static class NUMAPerformanceMeasurement {
        public long measureNUMAwareness(int numaNodeCount, int dataSize, boolean numaAware) throws InterruptedException {
            NUMAwareDataStructure dataStructure = new NUMAwareDataStructure(dataSize, numaNodeCount);
            NUMAwareThreadPool threadPool = new NUMAwareThreadPool(numaNodeCount, 2);
            
            long startTime = System.nanoTime();
            
            CountDownLatch latch = new CountDownLatch(numaNodeCount);
            
            for (int i = 0; i < numaNodeCount; i++) {
                final int nodeId = i;
                threadPool.submitTask(nodeId, () -> {
                    try {
                        if (numaAware) {
                            dataStructure.processDataNUMAware(nodeId);
                        } else {
                            dataStructure.processData(nodeId);
                        }
                    } finally {
                        latch.countDown();
                    }
                });
            }
            
            latch.await();
            threadPool.shutdown();
            
            long endTime = System.nanoTime();
            return endTime - startTime;
        }
        
        public void demonstrateNUMAwareness() throws InterruptedException {
            int[] numaNodeCounts = {1, 2, 4, 8};
            int dataSize = 1000000;
            
            System.out.println("NUMA Awareness Performance:");
            System.out.println("Nodes\tNUMA Aware (ns)\tNUMA Unaware (ns)\tSpeedup");
            
            for (int count : numaNodeCounts) {
                long numaAwareTime = measureNUMAwareness(count, dataSize, true);
                long numaUnawareTime = measureNUMAwareness(count, dataSize, false);
                
                double speedup = (double) numaUnawareTime / numaAwareTime;
                System.out.println(count + "\t" + numaAwareTime + "\t\t" + numaUnawareTime + "\t\t" + String.format("%.2f", speedup));
            }
        }
    }
}
```

## 13.8 Profiling Concurrent Applications

Profiling concurrent applications involves measuring and analyzing the performance characteristics of multi-threaded programs.

### Key Concepts
- **CPU Profiling**: Measuring CPU usage per thread
- **Memory Profiling**: Analyzing memory usage patterns
- **Lock Profiling**: Identifying lock contention
- **Thread Profiling**: Analyzing thread behavior

### Real-World Analogy
Think of monitoring a busy restaurant to see which stations are overloaded, which staff members are idle, and where bottlenecks occur.

### Java Example
```java
public class ConcurrentProfilingExample {
    // Simple profiler for concurrent applications
    public static class ConcurrentProfiler {
        private final Map<String, Long> methodTimes = new ConcurrentHashMap<>();
        private final Map<String, AtomicInteger> methodCalls = new ConcurrentHashMap<>();
        private final Map<String, Long> lockWaitTimes = new ConcurrentHashMap<>();
        
        public void startMethod(String methodName) {
            methodTimes.put(methodName, System.nanoTime());
        }
        
        public void endMethod(String methodName) {
            Long startTime = methodTimes.get(methodName);
            if (startTime != null) {
                long duration = System.nanoTime() - startTime;
                methodTimes.put(methodName, duration);
                methodCalls.computeIfAbsent(methodName, k -> new AtomicInteger(0)).incrementAndGet();
            }
        }
        
        public void recordLockWait(String lockName, long waitTime) {
            lockWaitTimes.merge(lockName, waitTime, Long::sum);
        }
        
        public void printProfile() {
            System.out.println("Method Profile:");
            System.out.println("Method\t\tCalls\tTotal Time (ns)\tAvg Time (ns)");
            
            for (Map.Entry<String, AtomicInteger> entry : methodCalls.entrySet()) {
                String methodName = entry.getKey();
                int calls = entry.getValue().get();
                long totalTime = methodTimes.getOrDefault(methodName, 0L);
                long avgTime = calls > 0 ? totalTime / calls : 0;
                
                System.out.println(methodName + "\t\t" + calls + "\t" + totalTime + "\t" + avgTime);
            }
            
            System.out.println("\nLock Wait Times:");
            System.out.println("Lock\t\tTotal Wait Time (ns)");
            
            for (Map.Entry<String, Long> entry : lockWaitTimes.entrySet()) {
                System.out.println(entry.getKey() + "\t\t" + entry.getValue());
            }
        }
    }
    
    // Profiled service
    public static class ProfiledService {
        private final ConcurrentProfiler profiler;
        private final Object lock = new Object();
        private int counter = 0;
        
        public ProfiledService(ConcurrentProfiler profiler) {
            this.profiler = profiler;
        }
        
        public void processRequest(String request) {
            profiler.startMethod("processRequest");
            
            try {
                // Simulate some work
                Thread.sleep(10);
                
                synchronized (lock) {
                    profiler.startMethod("criticalSection");
                    try {
                        // Simulate critical section work
                        Thread.sleep(5);
                        counter++;
                    } finally {
                        profiler.endMethod("criticalSection");
                    }
                }
                
                // Simulate more work
                Thread.sleep(15);
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            } finally {
                profiler.endMethod("processRequest");
            }
        }
        
        public int getCounter() {
            return counter;
        }
    }
    
    // Thread pool profiler
    public static class ThreadPoolProfiler {
        private final ExecutorService executor;
        private final AtomicInteger activeThreads = new AtomicInteger(0);
        private final AtomicInteger completedTasks = new AtomicInteger(0);
        private final AtomicInteger failedTasks = new AtomicInteger(0);
        
        public ThreadPoolProfiler(int threadCount) {
            this.executor = Executors.newFixedThreadPool(threadCount);
        }
        
        public void submitTask(Runnable task) {
            executor.submit(() -> {
                activeThreads.incrementAndGet();
                try {
                    task.run();
                    completedTasks.incrementAndGet();
                } catch (Exception e) {
                    failedTasks.incrementAndGet();
                } finally {
                    activeThreads.decrementAndGet();
                }
            });
        }
        
        public void printProfile() {
            System.out.println("Thread Pool Profile:");
            System.out.println("Active threads: " + activeThreads.get());
            System.out.println("Completed tasks: " + completedTasks.get());
            System.out.println("Failed tasks: " + failedTasks.get());
        }
        
        public void shutdown() {
            executor.shutdown();
        }
    }
    
    // Memory profiler
    public static class MemoryProfiler {
        private final Runtime runtime;
        private long initialMemory;
        
        public MemoryProfiler() {
            this.runtime = Runtime.getRuntime();
            this.initialMemory = runtime.totalMemory() - runtime.freeMemory();
        }
        
        public void recordMemoryUsage(String phase) {
            long currentMemory = runtime.totalMemory() - runtime.freeMemory();
            long memoryUsed = currentMemory - initialMemory;
            
            System.out.println(phase + " memory usage: " + memoryUsed / 1024 / 1024 + " MB");
        }
        
        public void forceGC() {
            System.gc();
            System.gc(); // Call twice to ensure cleanup
        }
    }
    
    // Demonstrate profiling
    public static void demonstrateProfiling() throws InterruptedException {
        ConcurrentProfiler profiler = new ConcurrentProfiler();
        ProfiledService service = new ProfiledService(profiler);
        ThreadPoolProfiler threadPoolProfiler = new ThreadPoolProfiler(4);
        MemoryProfiler memoryProfiler = new MemoryProfiler();
        
        memoryProfiler.recordMemoryUsage("Initial");
        
        // Submit tasks
        for (int i = 0; i < 100; i++) {
            threadPoolProfiler.submitTask(() -> service.processRequest("Request " + i));
        }
        
        // Wait for completion
        Thread.sleep(2000);
        
        memoryProfiler.recordMemoryUsage("After processing");
        
        // Print profiles
        profiler.printProfile();
        threadPoolProfiler.printProfile();
        
        memoryProfiler.forceGC();
        memoryProfiler.recordMemoryUsage("After GC");
        
        threadPoolProfiler.shutdown();
    }
}
```

This comprehensive explanation covers all aspects of performance and scalability in concurrent programming, providing both theoretical understanding and practical Java examples to illustrate each concept.