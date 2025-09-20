# Section 11 – Parallel Performance Analysis

## 11.1 Performance Metrics

Performance metrics are quantitative measures used to evaluate the effectiveness and efficiency of parallel systems.

### Key Concepts:
- **Execution Time**: Total time to complete a task
- **Throughput**: Rate of task completion per unit time
- **Latency**: Time delay between input and output
- **Resource Utilization**: Percentage of available resources used

### Real-World Analogy:
Performance metrics are like the dashboard in a car that shows speed (throughput), fuel efficiency (resource utilization), and trip time (execution time) to help you understand how well your vehicle is performing.

### Example: Performance Metrics in Java
```java
import java.util.concurrent.*;
import java.util.*;

public class PerformanceMetricsExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Performance Metrics Demo ===");
        
        int[] data = generateData(1000000);
        
        // Measure execution time
        long startTime = System.nanoTime();
        int result = calculateSum(data);
        long endTime = System.nanoTime();
        long executionTime = endTime - startTime;
        
        // Calculate throughput (operations per second)
        double throughput = (double) data.length / (executionTime / 1_000_000_000.0);
        
        // Measure resource utilization
        int availableProcessors = Runtime.getRuntime().availableProcessors();
        double cpuUtilization = (double) availableProcessors / availableProcessors * 100;
        
        System.out.println("Execution time: " + executionTime + " ns");
        System.out.println("Throughput: " + throughput + " operations/sec");
        System.out.println("CPU utilization: " + cpuUtilization + "%");
        System.out.println("Result: " + result);
    }
    
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
    
    private static int calculateSum(int[] data) {
        return Arrays.stream(data).sum();
    }
}
```

## 11.2 Speedup and Efficiency

Speedup measures how much faster a parallel implementation is compared to its sequential counterpart, while efficiency measures how well resources are utilized.

### Key Concepts:
- **Speedup**: S(p) = T(1) / T(p) where T(1) is sequential time and T(p) is parallel time
- **Efficiency**: E(p) = S(p) / p where p is the number of processors
- **Linear Speedup**: Speedup equals number of processors
- **Superlinear Speedup**: Speedup exceeds number of processors

### Real-World Analogy:
Speedup is like comparing how much faster a team of 4 workers can complete a task compared to 1 worker. Efficiency measures how well each worker is contributing to the overall task.

### Example: Speedup and Efficiency Calculation
```java
import java.util.concurrent.*;
import java.util.*;

public class SpeedupEfficiencyExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Speedup and Efficiency Demo ===");
        
        int[] data = generateData(1000000);
        
        // Sequential execution
        long sequentialTime = measureSequentialExecution(data);
        
        // Parallel execution with different processor counts
        for (int processors = 2; processors <= 8; processors *= 2) {
            long parallelTime = measureParallelExecution(data, processors);
            
            double speedup = (double) sequentialTime / parallelTime;
            double efficiency = speedup / processors * 100;
            
            System.out.println("Processors: " + processors);
            System.out.println("Sequential time: " + sequentialTime + " ms");
            System.out.println("Parallel time: " + parallelTime + " ms");
            System.out.println("Speedup: " + speedup);
            System.out.println("Efficiency: " + efficiency + "%");
            System.out.println();
        }
    }
    
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
    
    private static long measureSequentialExecution(int[] data) {
        long startTime = System.currentTimeMillis();
        Arrays.stream(data).sum();
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureParallelExecution(int[] data, int processors) throws InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newFixedThreadPool(processors);
        
        long startTime = System.currentTimeMillis();
        int chunkSize = data.length / processors;
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < processors; i++) {
            final int start = i * chunkSize;
            final int end = (i == processors - 1) ? data.length : (i + 1) * chunkSize;
            
            futures.add(executor.submit(() -> {
                int sum = 0;
                for (int j = start; j < end; j++) {
                    sum += data[j];
                }
                return sum;
            }));
        }
        
        int totalSum = 0;
        for (Future<Integer> future : futures) {
            totalSum += future.get();
        }
        
        executor.shutdown();
        return System.currentTimeMillis() - startTime;
    }
}
```

## 11.3 Scalability Analysis

Scalability analysis examines how system performance changes as the number of processors or problem size increases.

### Key Concepts:
- **Strong Scalability**: Performance improvement with increasing processors for fixed problem size
- **Weak Scalability**: Performance maintenance with increasing processors and problem size
- **Scalability Limit**: Point where adding processors doesn't improve performance
- **Amdahl's Law**: Theoretical limit on speedup due to sequential portions

### Real-World Analogy:
Scalability is like analyzing how well a restaurant can handle more customers. Strong scalability is like serving more customers with the same menu, while weak scalability is like expanding the menu to serve more customers.

### Example: Scalability Analysis
```java
import java.util.concurrent.*;
import java.util.*;

public class ScalabilityAnalysisExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Scalability Analysis Demo ===");
        
        // Strong scalability analysis
        demonstrateStrongScalability();
        
        // Weak scalability analysis
        demonstrateWeakScalability();
    }
    
    private static void demonstrateStrongScalability() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Strong Scalability ===");
        int fixedProblemSize = 1000000;
        int[] data = generateData(fixedProblemSize);
        
        long sequentialTime = measureSequentialExecution(data);
        
        for (int processors = 1; processors <= 8; processors++) {
            long parallelTime = measureParallelExecution(data, processors);
            double speedup = (double) sequentialTime / parallelTime;
            
            System.out.println("Processors: " + processors + 
                             ", Problem size: " + fixedProblemSize + 
                             ", Speedup: " + speedup);
        }
    }
    
    private static void demonstrateWeakScalability() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Weak Scalability ===");
        
        for (int processors = 1; processors <= 8; processors++) {
            int problemSize = 100000 * processors; // Scale problem with processors
            int[] data = generateData(problemSize);
            
            long executionTime = measureParallelExecution(data, processors);
            
            System.out.println("Processors: " + processors + 
                             ", Problem size: " + problemSize + 
                             ", Execution time: " + executionTime + " ms");
        }
    }
    
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
    
    private static long measureSequentialExecution(int[] data) {
        long startTime = System.currentTimeMillis();
        Arrays.stream(data).sum();
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureParallelExecution(int[] data, int processors) throws InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newFixedThreadPool(processors);
        
        long startTime = System.currentTimeMillis();
        int chunkSize = data.length / processors;
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < processors; i++) {
            final int start = i * chunkSize;
            final int end = (i == processors - 1) ? data.length : (i + 1) * chunkSize;
            
            futures.add(executor.submit(() -> {
                int sum = 0;
                for (int j = start; j < end; j++) {
                    sum += data[j];
                }
                return sum;
            }));
        }
        
        int totalSum = 0;
        for (Future<Integer> future : futures) {
            totalSum += future.get();
        }
        
        executor.shutdown();
        return System.currentTimeMillis() - startTime;
    }
}
```

## 11.4 Amdahl's Law

Amdahl's Law provides a theoretical upper bound on the speedup achievable through parallelization, considering the sequential portion of a program.

### Key Concepts:
- **Sequential Fraction**: Part of program that cannot be parallelized
- **Parallel Fraction**: Part of program that can be parallelized
- **Speedup Limit**: S(p) ≤ 1 / (f + (1-f)/p) where f is sequential fraction
- **Bottleneck Effect**: Sequential portion limits overall speedup

### Real-World Analogy:
Amdahl's Law is like a highway with a single-lane bridge. No matter how many lanes you add to the highway, the bottleneck at the bridge limits the overall traffic flow.

### Example: Amdahl's Law Demonstration
```java
public class AmdahlsLawExample {
    public static void main(String[] args) {
        System.out.println("=== Amdahl's Law Demo ===");
        
        // Different sequential fractions
        double[] sequentialFractions = {0.1, 0.2, 0.3, 0.5};
        
        for (double f : sequentialFractions) {
            System.out.println("\nSequential fraction: " + f);
            System.out.println("Processors\tTheoretical Speedup");
            
            for (int p = 1; p <= 16; p *= 2) {
                double speedup = calculateAmdahlsSpeedup(f, p);
                System.out.println(p + "\t\t" + speedup);
            }
        }
    }
    
    private static double calculateAmdahlsSpeedup(double sequentialFraction, int processors) {
        // Amdahl's Law: S(p) = 1 / (f + (1-f)/p)
        return 1.0 / (sequentialFraction + (1.0 - sequentialFraction) / processors);
    }
}
```

## 11.5 Gustafson's Law

Gustafson's Law provides an alternative view to Amdahl's Law, focusing on how problem size can scale with the number of processors.

### Key Concepts:
- **Scaled Speedup**: S(p) = p - α(p-1) where α is sequential fraction
- **Problem Scaling**: Assumes problem size increases with processors
- **Real-world Applicability**: More realistic for many parallel applications
- **Linear Speedup**: Achievable when problem scales with processors

### Real-World Analogy:
Gustafson's Law is like a construction project where adding more workers allows you to build a larger building in the same time, rather than building the same building faster.

### Example: Gustafson's Law vs Amdahl's Law
```java
public class GustafsonsLawExample {
    public static void main(String[] args) {
        System.out.println("=== Gustafson's Law vs Amdahl's Law ===");
        
        double sequentialFraction = 0.1; // 10% sequential
        
        System.out.println("Sequential fraction: " + sequentialFraction);
        System.out.println("Processors\tAmdahl's Law\tGustafson's Law");
        
        for (int p = 1; p <= 16; p *= 2) {
            double amdahlsSpeedup = calculateAmdahlsSpeedup(sequentialFraction, p);
            double gustafsonsSpeedup = calculateGustafsonsSpeedup(sequentialFraction, p);
            
            System.out.println(p + "\t\t" + amdahlsSpeedup + "\t\t" + gustafsonsSpeedup);
        }
    }
    
    private static double calculateAmdahlsSpeedup(double sequentialFraction, int processors) {
        return 1.0 / (sequentialFraction + (1.0 - sequentialFraction) / processors);
    }
    
    private static double calculateGustafsonsSpeedup(double sequentialFraction, int processors) {
        // Gustafson's Law: S(p) = p - α(p-1)
        return processors - sequentialFraction * (processors - 1);
    }
}
```

## 11.6 Performance Profiling

Performance profiling involves measuring and analyzing the performance characteristics of parallel programs to identify bottlenecks and optimization opportunities.

### Key Concepts:
- **Hotspots**: Code sections consuming most execution time
- **Call Graphs**: Function call relationships and timing
- **Memory Profiling**: Memory allocation and usage patterns
- **CPU Profiling**: CPU usage and instruction-level analysis

### Real-World Analogy:
Performance profiling is like a health checkup that identifies which parts of your body are working hardest and where you might need to focus your attention for better overall health.

### Example: Simple Performance Profiler
```java
import java.util.concurrent.*;
import java.util.*;

public class PerformanceProfilerExample {
    private static final Map<String, Long> methodTimes = new ConcurrentHashMap<>();
    private static final Map<String, Integer> methodCalls = new ConcurrentHashMap<>();
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Performance Profiling Demo ===");
        
        // Profile parallel matrix multiplication
        int[][] matrixA = generateMatrix(1000, 1000);
        int[][] matrixB = generateMatrix(1000, 1000);
        
        profileMethod("sequentialMultiply", () -> sequentialMultiply(matrixA, matrixB));
        profileMethod("parallelMultiply", () -> parallelMultiply(matrixA, matrixB));
        
        // Print profiling results
        printProfilingResults();
    }
    
    private static void profileMethod(String methodName, Runnable method) {
        long startTime = System.nanoTime();
        method.run();
        long endTime = System.nanoTime();
        
        long executionTime = endTime - startTime;
        methodTimes.merge(methodName, executionTime, Long::sum);
        methodCalls.merge(methodName, 1, Integer::sum);
    }
    
    private static void printProfilingResults() {
        System.out.println("\n=== Profiling Results ===");
        System.out.println("Method\t\tCalls\tTotal Time (ns)\tAvg Time (ns)");
        
        for (String method : methodTimes.keySet()) {
            long totalTime = methodTimes.get(method);
            int calls = methodCalls.get(method);
            double avgTime = (double) totalTime / calls;
            
            System.out.println(method + "\t" + calls + "\t" + totalTime + "\t" + avgTime);
        }
    }
    
    private static int[][] generateMatrix(int rows, int cols) {
        int[][] matrix = new int[rows][cols];
        Random random = new Random();
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = random.nextInt(100);
            }
        }
        
        return matrix;
    }
    
    private static int[][] sequentialMultiply(int[][] a, int[][] b) {
        int rows = a.length;
        int cols = b[0].length;
        int[][] result = new int[rows][cols];
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                for (int k = 0; k < a[0].length; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        
        return result;
    }
    
    private static int[][] parallelMultiply(int[][] a, int[][] b) throws InterruptedException, ExecutionException {
        int rows = a.length;
        int cols = b[0].length;
        int[][] result = new int[rows][cols];
        
        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < rows; i++) {
            final int row = i;
            futures.add(executor.submit(() -> {
                for (int j = 0; j < cols; j++) {
                    for (int k = 0; k < a[0].length; k++) {
                        result[row][j] += a[row][k] * b[k][j];
                    }
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        executor.shutdown();
        return result;
    }
}
```

## 11.7 Bottleneck Analysis

Bottleneck analysis identifies the limiting factors that prevent parallel systems from achieving optimal performance.

### Key Concepts:
- **Resource Bottlenecks**: CPU, memory, I/O, or network limitations
- **Synchronization Bottlenecks**: Contention for locks or barriers
- **Load Imbalance**: Uneven work distribution among processors
- **Communication Overhead**: Excessive inter-processor communication

### Real-World Analogy:
Bottleneck analysis is like identifying the slowest part of an assembly line that's preventing the entire production from going faster.

### Example: Bottleneck Analysis
```java
import java.util.concurrent.*;
import java.util.*;

public class BottleneckAnalysisExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Bottleneck Analysis Demo ===");
        
        // Analyze different types of bottlenecks
        analyzeSynchronizationBottleneck();
        analyzeLoadImbalanceBottleneck();
        analyzeCommunicationBottleneck();
    }
    
    private static void analyzeSynchronizationBottleneck() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Synchronization Bottleneck ===");
        
        int numThreads = 8;
        int iterations = 100000;
        
        // With synchronization bottleneck
        long startTime = System.nanoTime();
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<?>> futures = new ArrayList<>();
        
        final Object lock = new Object();
        final int[] counter = {0};
        
        for (int i = 0; i < numThreads; i++) {
            futures.add(executor.submit(() -> {
                for (int j = 0; j < iterations; j++) {
                    synchronized (lock) {
                        counter[0]++; // Synchronization bottleneck
                    }
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        long synchronizedTime = System.nanoTime() - startTime;
        executor.shutdown();
        
        // Without synchronization bottleneck
        startTime = System.nanoTime();
        executor = Executors.newFixedThreadPool(numThreads);
        futures.clear();
        
        final AtomicInteger atomicCounter = new AtomicInteger(0);
        
        for (int i = 0; i < numThreads; i++) {
            futures.add(executor.submit(() -> {
                for (int j = 0; j < iterations; j++) {
                    atomicCounter.incrementAndGet(); // No bottleneck
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        long atomicTime = System.nanoTime() - startTime;
        executor.shutdown();
        
        System.out.println("Synchronized time: " + synchronizedTime + " ns");
        System.out.println("Atomic time: " + atomicTime + " ns");
        System.out.println("Bottleneck impact: " + (double) synchronizedTime / atomicTime + "x slower");
    }
    
    private static void analyzeLoadImbalanceBottleneck() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Load Imbalance Bottleneck ===");
        
        int numThreads = 4;
        
        // Imbalanced workload
        int[] imbalancedWork = {100, 1000, 100, 100}; // One thread gets 10x more work
        
        long startTime = System.nanoTime();
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < numThreads; i++) {
            final int work = imbalancedWork[i];
            futures.add(executor.submit(() -> {
                for (int j = 0; j < work; j++) {
                    Thread.sleep(1); // Simulate work
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        long imbalancedTime = System.nanoTime() - startTime;
        executor.shutdown();
        
        // Balanced workload
        int[] balancedWork = {400, 400, 400, 400}; // Equal work for all threads
        
        startTime = System.nanoTime();
        executor = Executors.newFixedThreadPool(numThreads);
        futures.clear();
        
        for (int i = 0; i < numThreads; i++) {
            final int work = balancedWork[i];
            futures.add(executor.submit(() -> {
                for (int j = 0; j < work; j++) {
                    Thread.sleep(1); // Simulate work
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        long balancedTime = System.nanoTime() - startTime;
        executor.shutdown();
        
        System.out.println("Imbalanced time: " + imbalancedTime + " ns");
        System.out.println("Balanced time: " + balancedTime + " ns");
        System.out.println("Load imbalance impact: " + (double) imbalancedTime / balancedTime + "x slower");
    }
    
    private static void analyzeCommunicationBottleneck() {
        System.out.println("\n=== Communication Bottleneck ===");
        
        // Simulate communication overhead
        int messages = 1000;
        int messageSize = 1024; // bytes
        
        // High communication frequency
        long startTime = System.nanoTime();
        for (int i = 0; i < messages; i++) {
            simulateMessagePassing(messageSize);
        }
        long highFreqTime = System.nanoTime() - startTime;
        
        // Low communication frequency (batch messages)
        startTime = System.nanoTime();
        int batchSize = 10;
        for (int i = 0; i < messages; i += batchSize) {
            simulateMessagePassing(messageSize * batchSize);
        }
        long lowFreqTime = System.nanoTime() - startTime;
        
        System.out.println("High frequency communication: " + highFreqTime + " ns");
        System.out.println("Low frequency communication: " + lowFreqTime + " ns");
        System.out.println("Communication efficiency: " + (double) highFreqTime / lowFreqTime + "x improvement");
    }
    
    private static void simulateMessagePassing(int size) {
        // Simulate message passing overhead
        byte[] data = new byte[size];
        Arrays.fill(data, (byte) 1);
        
        // Simulate processing
        int sum = 0;
        for (byte b : data) {
            sum += b;
        }
    }
}
```

## 11.8 Performance Optimization

Performance optimization involves improving the efficiency and speed of parallel programs through various techniques.

### Key Concepts:
- **Algorithm Optimization**: Choosing better algorithms
- **Data Structure Optimization**: Using appropriate data structures
- **Memory Optimization**: Improving memory access patterns
- **Communication Optimization**: Reducing communication overhead

### Real-World Analogy:
Performance optimization is like tuning a race car - you adjust the engine, improve aerodynamics, and optimize the suspension to get the best possible performance.

### Example: Performance Optimization Techniques
```java
import java.util.concurrent.*;
import java.util.*;

public class PerformanceOptimizationExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Performance Optimization Demo ===");
        
        int[] data = generateData(10000000);
        
        // Original implementation
        long originalTime = measureOriginalImplementation(data);
        
        // Optimized implementation
        long optimizedTime = measureOptimizedImplementation(data);
        
        System.out.println("Original time: " + originalTime + " ms");
        System.out.println("Optimized time: " + optimizedTime + " ms");
        System.out.println("Speedup: " + (double) originalTime / optimizedTime);
    }
    
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
    
    private static long measureOriginalImplementation(int[] data) {
        long startTime = System.currentTimeMillis();
        
        // Inefficient: sequential processing
        int sum = 0;
        for (int value : data) {
            sum += value * value; // Square each element
        }
        
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureOptimizedImplementation(int[] data) throws InterruptedException, ExecutionException {
        long startTime = System.currentTimeMillis();
        
        // Optimized: parallel processing with optimal chunk size
        int numProcessors = Runtime.getRuntime().availableProcessors();
        ExecutorService executor = Executors.newFixedThreadPool(numProcessors);
        
        int chunkSize = Math.max(1, data.length / (numProcessors * 4)); // Optimal chunk size
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < data.length; i += chunkSize) {
            final int start = i;
            final int end = Math.min(i + chunkSize, data.length);
            
            futures.add(executor.submit(() -> {
                int localSum = 0;
                for (int j = start; j < end; j++) {
                    localSum += data[j] * data[j]; // Square each element
                }
                return localSum;
            }));
        }
        
        int sum = 0;
        for (Future<Integer> future : futures) {
            sum += future.get();
        }
        
        executor.shutdown();
        return System.currentTimeMillis() - startTime;
    }
}
```

## 11.9 Performance Tools

Performance tools help measure, analyze, and optimize parallel program performance.

### Key Concepts:
- **Profilers**: Tools that measure execution time and resource usage
- **Monitors**: Real-time performance monitoring tools
- **Analyzers**: Tools that analyze performance data
- **Optimizers**: Tools that suggest performance improvements

### Real-World Analogy:
Performance tools are like diagnostic equipment in a hospital - they help doctors identify problems and monitor patient health in real-time.

### Example: Custom Performance Monitoring Tool
```java
import java.util.concurrent.*;
import java.util.*;
import java.time.LocalDateTime;

public class PerformanceMonitoringTool {
    private static final Map<String, PerformanceMetrics> metrics = new ConcurrentHashMap<>();
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Performance Monitoring Tool Demo ===");
        
        // Monitor different operations
        monitorOperation("matrixMultiplication", () -> performMatrixMultiplication());
        monitorOperation("dataProcessing", () -> performDataProcessing());
        monitorOperation("fileIO", () -> performFileIO());
        
        // Print monitoring results
        printMonitoringResults();
    }
    
    private static void monitorOperation(String operationName, Runnable operation) {
        long startTime = System.nanoTime();
        long startMemory = getUsedMemory();
        
        operation.run();
        
        long endTime = System.nanoTime();
        long endMemory = getUsedMemory();
        
        PerformanceMetrics metric = new PerformanceMetrics(
            operationName,
            endTime - startTime,
            endMemory - startMemory,
            LocalDateTime.now()
        );
        
        metrics.put(operationName, metric);
    }
    
    private static void printMonitoringResults() {
        System.out.println("\n=== Performance Monitoring Results ===");
        System.out.println("Operation\t\tExecution Time (ns)\tMemory Usage (bytes)\tTimestamp");
        
        for (PerformanceMetrics metric : metrics.values()) {
            System.out.println(metric.operationName + "\t\t" + 
                             metric.executionTime + "\t\t" + 
                             metric.memoryUsage + "\t\t" + 
                             metric.timestamp);
        }
    }
    
    private static long getUsedMemory() {
        Runtime runtime = Runtime.getRuntime();
        return runtime.totalMemory() - runtime.freeMemory();
    }
    
    private static void performMatrixMultiplication() {
        int[][] a = generateMatrix(100, 100);
        int[][] b = generateMatrix(100, 100);
        int[][] result = new int[100][100];
        
        for (int i = 0; i < 100; i++) {
            for (int j = 0; j < 100; j++) {
                for (int k = 0; k < 100; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
    }
    
    private static void performDataProcessing() {
        List<Integer> data = new ArrayList<>();
        for (int i = 0; i < 100000; i++) {
            data.add(i);
        }
        
        data.stream()
            .map(x -> x * x)
            .filter(x -> x % 2 == 0)
            .collect(Collectors.toList());
    }
    
    private static void performFileIO() {
        // Simulate file I/O
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    private static int[][] generateMatrix(int rows, int cols) {
        int[][] matrix = new int[rows][cols];
        Random random = new Random();
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = random.nextInt(100);
            }
        }
        
        return matrix;
    }
    
    static class PerformanceMetrics {
        final String operationName;
        final long executionTime;
        final long memoryUsage;
        final LocalDateTime timestamp;
        
        PerformanceMetrics(String operationName, long executionTime, long memoryUsage, LocalDateTime timestamp) {
            this.operationName = operationName;
            this.executionTime = executionTime;
            this.memoryUsage = memoryUsage;
            this.timestamp = timestamp;
        }
    }
}
```

## 11.10 Performance Best Practices

Performance best practices provide guidelines for writing efficient parallel programs.

### Key Concepts:
- **Measure First**: Always measure before optimizing
- **Profile Regularly**: Use profiling tools to identify bottlenecks
- **Optimize Hotspots**: Focus on code that consumes most time
- **Consider Trade-offs**: Balance performance with maintainability

### Real-World Analogy:
Performance best practices are like following proven recipes in cooking - they help you avoid common mistakes and achieve consistent, high-quality results.

### Example: Performance Best Practices Implementation
```java
import java.util.concurrent.*;
import java.util.*;

public class PerformanceBestPracticesExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Performance Best Practices Demo ===");
        
        // Best Practice 1: Measure before optimizing
        demonstrateMeasurementFirst();
        
        // Best Practice 2: Use appropriate data structures
        demonstrateDataStructureSelection();
        
        // Best Practice 3: Minimize synchronization
        demonstrateMinimalSynchronization();
        
        // Best Practice 4: Optimize memory access patterns
        demonstrateMemoryAccessOptimization();
    }
    
    private static void demonstrateMeasurementFirst() {
        System.out.println("\n=== Best Practice 1: Measure First ===");
        
        int[] data = generateData(1000000);
        
        // Measure different approaches
        long sequentialTime = measureSequentialSum(data);
        long parallelTime = measureParallelSum(data);
        
        System.out.println("Sequential time: " + sequentialTime + " ms");
        System.out.println("Parallel time: " + parallelTime + " ms");
        
        if (parallelTime < sequentialTime) {
            System.out.println("Parallel approach is faster by " + (sequentialTime - parallelTime) + " ms");
        } else {
            System.out.println("Sequential approach is faster - parallel overhead too high");
        }
    }
    
    private static void demonstrateDataStructureSelection() {
        System.out.println("\n=== Best Practice 2: Appropriate Data Structures ===");
        
        int size = 100000;
        
        // ArrayList vs LinkedList for random access
        List<Integer> arrayList = new ArrayList<>();
        List<Integer> linkedList = new LinkedList<>();
        
        // Fill lists
        for (int i = 0; i < size; i++) {
            arrayList.add(i);
            linkedList.add(i);
        }
        
        // Measure random access
        long arrayListTime = measureRandomAccess(arrayList, 1000);
        long linkedListTime = measureRandomAccess(linkedList, 1000);
        
        System.out.println("ArrayList random access: " + arrayListTime + " ms");
        System.out.println("LinkedList random access: " + linkedListTime + " ms");
        System.out.println("ArrayList is " + (double) linkedListTime / arrayListTime + "x faster for random access");
    }
    
    private static void demonstrateMinimalSynchronization() {
        System.out.println("\n=== Best Practice 3: Minimal Synchronization ===");
        
        int iterations = 100000;
        int numThreads = 8;
        
        // Heavy synchronization
        long heavySyncTime = measureHeavySynchronization(iterations, numThreads);
        
        // Minimal synchronization
        long minimalSyncTime = measureMinimalSynchronization(iterations, numThreads);
        
        System.out.println("Heavy synchronization time: " + heavySyncTime + " ms");
        System.out.println("Minimal synchronization time: " + minimalSyncTime + " ms");
        System.out.println("Minimal synchronization is " + (double) heavySyncTime / minimalSyncTime + "x faster");
    }
    
    private static void demonstrateMemoryAccessOptimization() {
        System.out.println("\n=== Best Practice 4: Memory Access Optimization ===");
        
        int size = 1000;
        int[][] matrix = generateMatrix(size, size);
        
        // Row-major access (cache-friendly)
        long rowMajorTime = measureRowMajorAccess(matrix);
        
        // Column-major access (cache-unfriendly)
        long columnMajorTime = measureColumnMajorAccess(matrix);
        
        System.out.println("Row-major access time: " + rowMajorTime + " ms");
        System.out.println("Column-major access time: " + columnMajorTime + " ms");
        System.out.println("Row-major access is " + (double) columnMajorTime / rowMajorTime + "x faster");
    }
    
    // Helper methods for demonstrations
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
    
    private static long measureSequentialSum(int[] data) {
        long startTime = System.currentTimeMillis();
        Arrays.stream(data).sum();
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureParallelSum(int[] data) throws InterruptedException, ExecutionException {
        long startTime = System.currentTimeMillis();
        
        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
        int chunkSize = data.length / Runtime.getRuntime().availableProcessors();
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < data.length; i += chunkSize) {
            final int start = i;
            final int end = Math.min(i + chunkSize, data.length);
            
            futures.add(executor.submit(() -> {
                int sum = 0;
                for (int j = start; j < end; j++) {
                    sum += data[j];
                }
                return sum;
            }));
        }
        
        int totalSum = 0;
        for (Future<Integer> future : futures) {
            totalSum += future.get();
        }
        
        executor.shutdown();
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureRandomAccess(List<Integer> list, int iterations) {
        Random random = new Random();
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < iterations; i++) {
            int index = random.nextInt(list.size());
            list.get(index);
        }
        
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureHeavySynchronization(int iterations, int numThreads) throws InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<?>> futures = new ArrayList<>();
        
        final Object lock = new Object();
        final int[] counter = {0};
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < numThreads; i++) {
            futures.add(executor.submit(() -> {
                for (int j = 0; j < iterations; j++) {
                    synchronized (lock) {
                        counter[0]++;
                    }
                }
            }));
        }
        
        for (Future<?> future : futures) {
            future.get();
        }
        
        executor.shutdown();
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureMinimalSynchronization(int iterations, int numThreads) throws InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newFixedThreadPool(numThreads);
        List<Future<Integer>> futures = new ArrayList<>();
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < numThreads; i++) {
            futures.add(executor.submit(() -> {
                int localCount = 0;
                for (int j = 0; j < iterations; j++) {
                    localCount++;
                }
                return localCount;
            }));
        }
        
        int totalCount = 0;
        for (Future<Integer> future : futures) {
            totalCount += future.get();
        }
        
        executor.shutdown();
        return System.currentTimeMillis() - startTime;
    }
    
    private static int[][] generateMatrix(int rows, int cols) {
        int[][] matrix = new int[rows][cols];
        Random random = new Random();
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = random.nextInt(100);
            }
        }
        
        return matrix;
    }
    
    private static long measureRowMajorAccess(int[][] matrix) {
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[0].length; j++) {
                matrix[i][j] *= 2;
            }
        }
        
        return System.currentTimeMillis() - startTime;
    }
    
    private static long measureColumnMajorAccess(int[][] matrix) {
        long startTime = System.currentTimeMillis();
        
        for (int j = 0; j < matrix[0].length; j++) {
            for (int i = 0; i < matrix.length; i++) {
                matrix[i][j] *= 2;
            }
        }
        
        return System.currentTimeMillis() - startTime;
    }
}
```

This comprehensive section covers all aspects of parallel performance analysis, from basic metrics to advanced optimization techniques, with practical examples and real-world analogies to help understand these complex concepts from the ground up.