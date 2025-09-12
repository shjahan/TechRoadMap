# Section 9 – Parallel Algorithms

## 9.1 Parallel Algorithm Design

Parallel algorithm design involves creating algorithms that can efficiently utilize multiple processors to solve computational problems.

### Key Concepts:
- **Decomposition**: Breaking problems into independent subproblems
- **Communication**: Minimizing data exchange between processors
- **Load Balancing**: Distributing work evenly across processors
- **Synchronization**: Coordinating processor execution

### Real-World Analogy:
Parallel algorithm design is like organizing a large construction project where you divide the work among different teams, minimize coordination overhead, ensure each team has equal work, and synchronize their progress.

### Example: Parallel Algorithm Design
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelAlgorithmDesignExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Algorithm Design Demo ===");
        
        // Demonstrate problem decomposition
        demonstrateProblemDecomposition();
        
        // Demonstrate load balancing
        demonstrateLoadBalancing();
    }
    
    private static void demonstrateProblemDecomposition() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Problem Decomposition ===");
        
        int[] data = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        int numProcessors = 4;
        
        System.out.println("Original data: " + Arrays.toString(data));
        System.out.println("Number of processors: " + numProcessors);
        
        // Decompose problem into chunks
        int chunkSize = data.length / numProcessors;
        ExecutorService executor = Executors.newFixedThreadPool(numProcessors);
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < numProcessors; i++) {
            final int start = i * chunkSize;
            final int end = (i == numProcessors - 1) ? data.length : (i + 1) * chunkSize;
            
            futures.add(executor.submit(() -> {
                int sum = 0;
                for (int j = start; j < end; j++) {
                    sum += data[j];
                }
                System.out.println("Processor " + (start / chunkSize) + " processed elements " + start + "-" + (end-1) + ", sum = " + sum);
                return sum;
            }));
        }
        
        // Collect results
        int totalSum = 0;
        for (Future<Integer> future : futures) {
            totalSum += future.get();
        }
        
        System.out.println("Total sum: " + totalSum);
        executor.shutdown();
    }
    
    private static void demonstrateLoadBalancing() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Load Balancing ===");
        
        int[] workloads = {100, 200, 150, 300, 250, 100, 200, 150};
        int numProcessors = 4;
        
        System.out.println("Workloads: " + Arrays.toString(workloads));
        
        // Simple round-robin assignment
        int[] processorLoads = new int[numProcessors];
        for (int i = 0; i < workloads.length; i++) {
            int processor = i % numProcessors;
            processorLoads[processor] += workloads[i];
        }
        
        System.out.println("Load distribution:");
        for (int i = 0; i < numProcessors; i++) {
            System.out.println("Processor " + i + ": " + processorLoads[i]);
        }
    }
}
```

## 9.2 Divide and Conquer

Divide and conquer is a fundamental algorithmic paradigm that recursively breaks down problems into smaller subproblems.

### Key Concepts:
- **Divide**: Split problem into smaller subproblems
- **Conquer**: Solve subproblems recursively
- **Combine**: Merge solutions of subproblems
- **Base Case**: Simple case that can be solved directly

### Real-World Analogy:
Divide and conquer is like organizing a large event by dividing it into smaller tasks, assigning each task to different teams, and then combining the results into a complete event.

### Example: Divide and Conquer
```java
import java.util.*;
import java.util.concurrent.*;

public class DivideAndConquerExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Divide and Conquer Demo ===");
        
        // Demonstrate parallel merge sort
        demonstrateParallelMergeSort();
    }
    
    private static void demonstrateParallelMergeSort() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel Merge Sort ===");
        
        int[] data = {64, 34, 25, 12, 22, 11, 90, 5, 77, 30};
        System.out.println("Original array: " + Arrays.toString(data));
        
        int[] sorted = parallelMergeSort(data, 0, data.length - 1);
        System.out.println("Sorted array: " + Arrays.toString(sorted));
    }
    
    private static int[] parallelMergeSort(int[] arr, int left, int right) throws InterruptedException, ExecutionException {
        if (left < right) {
            int mid = (left + right) / 2;
            
            // Divide: Sort left and right halves in parallel
            ExecutorService executor = Executors.newFixedThreadPool(2);
            
            Future<int[]> leftFuture = executor.submit(() -> {
                return parallelMergeSort(arr, left, mid);
            });
            
            Future<int[]> rightFuture = executor.submit(() -> {
                return parallelMergeSort(arr, mid + 1, right);
            });
            
            int[] leftSorted = leftFuture.get();
            int[] rightSorted = rightFuture.get();
            
            executor.shutdown();
            
            // Combine: Merge the sorted halves
            return merge(leftSorted, rightSorted);
        } else {
            return new int[]{arr[left]};
        }
    }
    
    private static int[] merge(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;
        
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }
        
        while (i < left.length) {
            result[k++] = left[i++];
        }
        
        while (j < right.length) {
            result[k++] = right[j++];
        }
        
        return result;
    }
}
```

## 9.3 Parallel Sorting

Parallel sorting algorithms distribute the sorting task across multiple processors to achieve better performance.

### Key Concepts:
- **Data Distribution**: Dividing data among processors
- **Local Sorting**: Each processor sorts its portion
- **Data Redistribution**: Reorganizing data for final merge
- **Global Merge**: Combining locally sorted data

### Real-World Analogy:
Parallel sorting is like having multiple librarians sort different sections of a library simultaneously, then combining their work into a single organized collection.

### Example: Parallel Sorting
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelSortingExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Sorting Demo ===");
        
        // Demonstrate parallel quicksort
        demonstrateParallelQuicksort();
    }
    
    private static void demonstrateParallelQuicksort() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel Quicksort ===");
        
        int[] data = {64, 34, 25, 12, 22, 11, 90, 5, 77, 30, 15, 8, 45, 67, 23};
        System.out.println("Original array: " + Arrays.toString(data));
        
        int[] sorted = parallelQuicksort(data);
        System.out.println("Sorted array: " + Arrays.toString(sorted));
    }
    
    private static int[] parallelQuicksort(int[] arr) throws InterruptedException, ExecutionException {
        if (arr.length <= 1) {
            return arr;
        }
        
        // Choose pivot
        int pivot = arr[arr.length / 2];
        
        // Partition array
        List<Integer> left = new ArrayList<>();
        List<Integer> right = new ArrayList<>();
        
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] < pivot) {
                left.add(arr[i]);
            } else if (arr[i] > pivot) {
                right.add(arr[i]);
            }
        }
        
        // Sort left and right partitions in parallel
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        Future<int[]> leftFuture = executor.submit(() -> {
            return parallelQuicksort(left.stream().mapToInt(i -> i).toArray());
        });
        
        Future<int[]> rightFuture = executor.submit(() -> {
            return parallelQuicksort(right.stream().mapToInt(i -> i).toArray());
        });
        
        int[] leftSorted = leftFuture.get();
        int[] rightSorted = rightFuture.get();
        
        executor.shutdown();
        
        // Combine results
        int[] result = new int[leftSorted.length + rightSorted.length + 1];
        System.arraycopy(leftSorted, 0, result, 0, leftSorted.length);
        result[leftSorted.length] = pivot;
        System.arraycopy(rightSorted, 0, result, leftSorted.length + 1, rightSorted.length);
        
        return result;
    }
}
```

## 9.4 Parallel Searching

Parallel searching algorithms distribute the search task across multiple processors to find elements more efficiently.

### Key Concepts:
- **Data Partitioning**: Dividing search space among processors
- **Parallel Search**: Each processor searches its partition
- **Result Aggregation**: Combining search results
- **Load Balancing**: Ensuring equal work distribution

### Real-World Analogy:
Parallel searching is like having multiple detectives search different areas of a city simultaneously to find a missing person, then combining their findings.

### Example: Parallel Searching
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelSearchingExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Searching Demo ===");
        
        // Demonstrate parallel linear search
        demonstrateParallelLinearSearch();
    }
    
    private static void demonstrateParallelLinearSearch() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel Linear Search ===");
        
        int[] data = {64, 34, 25, 12, 22, 11, 90, 5, 77, 30, 15, 8, 45, 67, 23};
        int target = 77;
        
        System.out.println("Array: " + Arrays.toString(data));
        System.out.println("Searching for: " + target);
        
        int result = parallelLinearSearch(data, target);
        if (result != -1) {
            System.out.println("Found at index: " + result);
        } else {
            System.out.println("Not found");
        }
    }
    
    private static int parallelLinearSearch(int[] arr, int target) throws InterruptedException, ExecutionException {
        int numProcessors = 4;
        int chunkSize = arr.length / numProcessors;
        
        ExecutorService executor = Executors.newFixedThreadPool(numProcessors);
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < numProcessors; i++) {
            final int start = i * chunkSize;
            final int end = (i == numProcessors - 1) ? arr.length : (i + 1) * chunkSize;
            
            futures.add(executor.submit(() -> {
                for (int j = start; j < end; j++) {
                    if (arr[j] == target) {
                        return j;
                    }
                }
                return -1;
            }));
        }
        
        // Check results
        for (Future<Integer> future : futures) {
            int result = future.get();
            if (result != -1) {
                executor.shutdown();
                return result;
            }
        }
        
        executor.shutdown();
        return -1;
    }
}
```

## 9.5 Parallel Graph Algorithms

Parallel graph algorithms process graph data structures using multiple processors to solve problems like shortest paths, connectivity, and traversal.

### Key Concepts:
- **Graph Partitioning**: Dividing graph among processors
- **Parallel Traversal**: Multiple processors explore different parts
- **Communication**: Exchanging graph data between processors
- **Synchronization**: Coordinating graph operations

### Real-World Analogy:
Parallel graph algorithms are like having multiple teams explore different neighborhoods of a city simultaneously to map out the entire city and find the best routes between locations.

### Example: Parallel Graph Algorithms
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelGraphAlgorithmsExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Graph Algorithms Demo ===");
        
        // Demonstrate parallel BFS
        demonstrateParallelBFS();
    }
    
    private static void demonstrateParallelBFS() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel BFS ===");
        
        // Create a simple graph
        Map<Integer, List<Integer>> graph = new HashMap<>();
        graph.put(0, Arrays.asList(1, 2));
        graph.put(1, Arrays.asList(0, 3, 4));
        graph.put(2, Arrays.asList(0, 5, 6));
        graph.put(3, Arrays.asList(1));
        graph.put(4, Arrays.asList(1));
        graph.put(5, Arrays.asList(2));
        graph.put(6, Arrays.asList(2));
        
        System.out.println("Graph: " + graph);
        
        int startNode = 0;
        Set<Integer> visited = parallelBFS(graph, startNode);
        
        System.out.println("BFS from node " + startNode + ": " + visited);
    }
    
    private static Set<Integer> parallelBFS(Map<Integer, List<Integer>> graph, int startNode) throws InterruptedException, ExecutionException {
        Set<Integer> visited = Collections.synchronizedSet(new HashSet<>());
        Queue<Integer> queue = new ConcurrentLinkedQueue<>();
        
        visited.add(startNode);
        queue.offer(startNode);
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        while (!queue.isEmpty()) {
            int currentLevelSize = queue.size();
            List<Future<Void>> futures = new ArrayList<>();
            
            for (int i = 0; i < currentLevelSize; i++) {
                Integer node = queue.poll();
                if (node != null) {
                    futures.add(executor.submit(() -> {
                        List<Integer> neighbors = graph.get(node);
                        if (neighbors != null) {
                            for (Integer neighbor : neighbors) {
                                if (visited.add(neighbor)) {
                                    queue.offer(neighbor);
                                }
                            }
                        }
                        return null;
                    }));
                }
            }
            
            // Wait for all processors to complete current level
            for (Future<Void> future : futures) {
                future.get();
            }
        }
        
        executor.shutdown();
        return visited;
    }
}
```

## 9.6 Parallel Matrix Operations

Parallel matrix operations distribute matrix computations across multiple processors to achieve better performance for large matrices.

### Key Concepts:
- **Matrix Partitioning**: Dividing matrices among processors
- **Parallel Multiplication**: Each processor computes part of result
- **Data Redistribution**: Reorganizing matrix data
- **Result Aggregation**: Combining partial results

### Real-World Analogy:
Parallel matrix operations are like having multiple teams of accountants work on different sections of a large financial calculation simultaneously, then combining their results.

### Example: Parallel Matrix Operations
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelMatrixOperationsExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Matrix Operations Demo ===");
        
        // Demonstrate parallel matrix multiplication
        demonstrateParallelMatrixMultiplication();
    }
    
    private static void demonstrateParallelMatrixMultiplication() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel Matrix Multiplication ===");
        
        int[][] a = {{1, 2, 3}, {4, 5, 6}};
        int[][] b = {{7, 8}, {9, 10}, {11, 12}};
        
        System.out.println("Matrix A:");
        printMatrix(a);
        System.out.println("Matrix B:");
        printMatrix(b);
        
        int[][] c = parallelMatrixMultiply(a, b);
        System.out.println("Result C:");
        printMatrix(c);
    }
    
    private static int[][] parallelMatrixMultiply(int[][] a, int[][] b) throws InterruptedException, ExecutionException {
        int rows = a.length;
        int cols = b[0].length;
        int[][] result = new int[rows][cols];
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        List<Future<Void>> futures = new ArrayList<>();
        
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                final int row = i;
                final int col = j;
                
                futures.add(executor.submit(() -> {
                    int sum = 0;
                    for (int k = 0; k < a[0].length; k++) {
                        sum += a[row][k] * b[k][col];
                    }
                    result[row][col] = sum;
                    return null;
                }));
            }
        }
        
        // Wait for all computations to complete
        for (Future<Void> future : futures) {
            future.get();
        }
        
        executor.shutdown();
        return result;
    }
    
    private static void printMatrix(int[][] matrix) {
        for (int[] row : matrix) {
            System.out.println(Arrays.toString(row));
        }
    }
}
```

## 9.7 Parallel Numerical Methods

Parallel numerical methods solve mathematical problems using multiple processors to achieve better performance and accuracy.

### Key Concepts:
- **Iterative Methods**: Parallelizing iterative algorithms
- **Domain Decomposition**: Dividing computational domain
- **Convergence**: Ensuring parallel algorithms converge
- **Error Analysis**: Analyzing parallel algorithm accuracy

### Real-World Analogy:
Parallel numerical methods are like having multiple teams of scientists work on different parts of a complex mathematical problem simultaneously, then combining their results to get the final answer.

### Example: Parallel Numerical Methods
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelNumericalMethodsExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Numerical Methods Demo ===");
        
        // Demonstrate parallel numerical integration
        demonstrateParallelIntegration();
    }
    
    private static void demonstrateParallelIntegration() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel Numerical Integration ===");
        
        double a = 0.0;
        double b = 1.0;
        int n = 1000;
        
        System.out.println("Integrating f(x) = x^2 from " + a + " to " + b);
        System.out.println("Number of intervals: " + n);
        
        double result = parallelTrapezoidalRule(a, b, n);
        System.out.println("Result: " + result);
        System.out.println("Expected: " + (b*b*b/3 - a*a*a/3));
    }
    
    private static double parallelTrapezoidalRule(double a, double b, int n) throws InterruptedException, ExecutionException {
        double h = (b - a) / n;
        int numProcessors = 4;
        int chunkSize = n / numProcessors;
        
        ExecutorService executor = Executors.newFixedThreadPool(numProcessors);
        List<Future<Double>> futures = new ArrayList<>();
        
        for (int i = 0; i < numProcessors; i++) {
            final int start = i * chunkSize;
            final int end = (i == numProcessors - 1) ? n : (i + 1) * chunkSize;
            
            futures.add(executor.submit(() -> {
                double sum = 0.0;
                for (int j = start; j < end; j++) {
                    double x = a + j * h;
                    sum += f(x);
                }
                return sum;
            }));
        }
        
        double totalSum = 0.0;
        for (Future<Double> future : futures) {
            totalSum += future.get();
        }
        
        executor.shutdown();
        
        return h * (totalSum + (f(a) + f(b)) / 2);
    }
    
    private static double f(double x) {
        return x * x; // f(x) = x^2
    }
}
```

## 9.8 Parallel String Algorithms

Parallel string algorithms process text data using multiple processors to solve problems like pattern matching, string sorting, and text analysis.

### Key Concepts:
- **String Partitioning**: Dividing text among processors
- **Parallel Pattern Matching**: Multiple processors search for patterns
- **String Sorting**: Parallel sorting of string data
- **Text Analysis**: Parallel processing of text features

### Real-World Analogy:
Parallel string algorithms are like having multiple editors proofread different sections of a large document simultaneously, then combining their findings to produce a complete analysis.

### Example: Parallel String Algorithms
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelStringAlgorithmsExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel String Algorithms Demo ===");
        
        // Demonstrate parallel string search
        demonstrateParallelStringSearch();
    }
    
    private static void demonstrateParallelStringSearch() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel String Search ===");
        
        String text = "The quick brown fox jumps over the lazy dog";
        String pattern = "fox";
        
        System.out.println("Text: " + text);
        System.out.println("Pattern: " + pattern);
        
        List<Integer> positions = parallelStringSearch(text, pattern);
        System.out.println("Found at positions: " + positions);
    }
    
    private static List<Integer> parallelStringSearch(String text, String pattern) throws InterruptedException, ExecutionException {
        int numProcessors = 4;
        int chunkSize = text.length() / numProcessors;
        List<Integer> positions = Collections.synchronizedList(new ArrayList<>());
        
        ExecutorService executor = Executors.newFixedThreadPool(numProcessors);
        List<Future<Void>> futures = new ArrayList<>();
        
        for (int i = 0; i < numProcessors; i++) {
            final int start = i * chunkSize;
            final int end = (i == numProcessors - 1) ? text.length() : (i + 1) * chunkSize;
            
            futures.add(executor.submit(() -> {
                for (int j = start; j <= end - pattern.length(); j++) {
                    if (text.substring(j, j + pattern.length()).equals(pattern)) {
                        positions.add(j);
                    }
                }
                return null;
            }));
        }
        
        // Wait for all processors to complete
        for (Future<Void> future : futures) {
            future.get();
        }
        
        executor.shutdown();
        return positions;
    }
}
```

## 9.9 Parallel Algorithm Analysis

Parallel algorithm analysis evaluates the performance and efficiency of parallel algorithms using various metrics and theoretical models.

### Key Concepts:
- **Speedup**: Performance improvement over sequential version
- **Efficiency**: Ratio of speedup to number of processors
- **Scalability**: Performance with increasing processors
- **Amdahl's Law**: Theoretical speedup limits

### Real-World Analogy:
Parallel algorithm analysis is like evaluating the efficiency of a factory production line - measuring how much faster it is with more workers, how efficiently resources are used, and how well it scales with more equipment.

### Example: Parallel Algorithm Analysis
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelAlgorithmAnalysisExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Algorithm Analysis Demo ===");
        
        // Analyze parallel algorithm performance
        analyzeParallelPerformance();
    }
    
    private static void analyzeParallelPerformance() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel Performance Analysis ===");
        
        int[] data = new int[1000000];
        Arrays.fill(data, 1);
        
        // Sequential execution
        long startTime = System.nanoTime();
        int sequentialSum = Arrays.stream(data).sum();
        long sequentialTime = System.nanoTime() - startTime;
        
        // Parallel execution
        startTime = System.nanoTime();
        int parallelSum = Arrays.stream(data).parallel().sum();
        long parallelTime = System.nanoTime() - startTime;
        
        // Calculate metrics
        double speedup = (double) sequentialTime / parallelTime;
        int numProcessors = Runtime.getRuntime().availableProcessors();
        double efficiency = speedup / numProcessors;
        
        System.out.println("Sequential time: " + sequentialTime + " ns");
        System.out.println("Parallel time: " + parallelTime + " ns");
        System.out.println("Speedup: " + speedup);
        System.out.println("Number of processors: " + numProcessors);
        System.out.println("Efficiency: " + efficiency);
        
        // Amdahl's Law analysis
        double parallelFraction = 0.9; // 90% parallelizable
        double maxSpeedup = 1.0 / (1.0 - parallelFraction + parallelFraction / numProcessors);
        System.out.println("Theoretical max speedup (Amdahl's Law): " + maxSpeedup);
    }
}
```

## 9.10 Parallel Algorithm Best Practices

Parallel algorithm best practices help avoid common pitfalls and improve the performance and correctness of parallel algorithms.

### Key Concepts:
- **Load Balancing**: Ensuring equal work distribution
- **Minimize Communication**: Reducing data exchange overhead
- **Avoid Race Conditions**: Preventing data corruption
- **Test Thoroughly**: Ensuring correctness across different scenarios

### Real-World Analogy:
Parallel algorithm best practices are like following proven construction techniques - ensuring all workers have equal work, minimizing coordination overhead, preventing accidents, and thoroughly testing the final structure.

### Example: Parallel Algorithm Best Practices
```java
import java.util.*;
import java.util.concurrent.*;

public class ParallelAlgorithmBestPracticesExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Parallel Algorithm Best Practices Demo ===");
        
        // Demonstrate best practices
        demonstrateLoadBalancing();
        demonstrateMinimizeCommunication();
        demonstrateAvoidRaceConditions();
    }
    
    private static void demonstrateLoadBalancing() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Load Balancing ===");
        
        int[] workloads = {100, 200, 150, 300, 250, 100, 200, 150};
        int numProcessors = 4;
        
        System.out.println("Workloads: " + Arrays.toString(workloads));
        
        // Good: Balanced load distribution
        int[] balancedLoads = new int[numProcessors];
        for (int i = 0; i < workloads.length; i++) {
            int processor = i % numProcessors;
            balancedLoads[processor] += workloads[i];
        }
        
        System.out.println("Balanced load distribution:");
        for (int i = 0; i < numProcessors; i++) {
            System.out.println("Processor " + i + ": " + balancedLoads[i]);
        }
    }
    
    private static void demonstrateMinimizeCommunication() {
        System.out.println("\n=== Minimize Communication ===");
        
        System.out.println("Best practices for minimizing communication:");
        System.out.println("1. Use local data when possible");
        System.out.println("2. Batch multiple operations together");
        System.out.println("3. Use collective operations instead of point-to-point");
        System.out.println("4. Cache frequently accessed data");
    }
    
    private static void demonstrateAvoidRaceConditions() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Avoid Race Conditions ===");
        
        // Bad: Race condition
        int[] sharedCounter = {0};
        Object lock = new Object();
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        List<Future<Void>> futures = new ArrayList<>();
        
        for (int i = 0; i < 4; i++) {
            futures.add(executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        sharedCounter[0]++;
                    }
                }
                return null;
            }));
        }
        
        for (Future<Void> future : futures) {
            future.get();
        }
        
        System.out.println("Safe counter value: " + sharedCounter[0]);
        executor.shutdown();
    }
}
```

This comprehensive section covers all aspects of parallel algorithms, from basic design principles to advanced analysis techniques, with practical examples and real-world analogies to help understand these complex concepts from the ground up.