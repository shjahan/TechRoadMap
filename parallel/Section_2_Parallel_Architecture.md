# Section 2 – Parallel Architecture

## 2.1 Flynn's Taxonomy

Flynn's Taxonomy is a classification system for computer architectures based on the number of instruction streams and data streams that can be processed simultaneously.

### Classification Categories:

#### 1. SISD (Single Instruction, Single Data)
- **One instruction stream**: Sequential execution
- **One data stream**: Single data path
- **Examples**: Traditional single-core processors, early computers

#### 2. SIMD (Single Instruction, Multiple Data)
- **One instruction stream**: Same operation on multiple data elements
- **Multiple data streams**: Parallel data processing
- **Examples**: Vector processors, GPU cores, SIMD instructions (SSE, AVX)

#### 3. MISD (Multiple Instruction, Single Data)
- **Multiple instruction streams**: Different operations
- **One data stream**: Single data path
- **Examples**: Rare in practice, some fault-tolerant systems

#### 4. MIMD (Multiple Instruction, Multiple Data)
- **Multiple instruction streams**: Independent operations
- **Multiple data streams**: Independent data paths
- **Examples**: Multicore processors, distributed systems, clusters

### Real-World Analogy:
- **SISD**: Like one chef preparing one dish at a time
- **SIMD**: Like one chef using a large griddle to cook multiple identical items simultaneously
- **MISD**: Like multiple chefs working on the same dish with different techniques
- **MIMD**: Like multiple chefs each preparing different dishes independently

### Example: SIMD vs MIMD in Java
```java
public class FlynnTaxonomyDemo {
    public static void main(String[] args) {
        int[] data1 = {1, 2, 3, 4, 5};
        int[] data2 = {6, 7, 8, 9, 10};
        
        System.out.println("=== SIMD-like Operation ===");
        // SIMD: Same operation on multiple data elements
        int[] simdResult = addArrays(data1, data2);
        System.out.println("SIMD result: " + Arrays.toString(simdResult));
        
        System.out.println("\n=== MIMD-like Operation ===");
        // MIMD: Different operations on different data
        int[] mimdResult = processArraysMIMD(data1, data2);
        System.out.println("MIMD result: " + Arrays.toString(mimdResult));
    }
    
    private static int[] addArrays(int[] a, int[] b) {
        int[] result = new int[a.length];
        // SIMD: Same operation (addition) on all elements
        for (int i = 0; i < a.length; i++) {
            result[i] = a[i] + b[i];
        }
        return result;
    }
    
    private static int[] processArraysMIMD(int[] a, int[] b) {
        int[] result = new int[a.length];
        // MIMD: Different operations on different elements
        for (int i = 0; i < a.length; i++) {
            if (i % 2 == 0) {
                result[i] = a[i] * b[i]; // Multiplication
            } else {
                result[i] = a[i] - b[i]; // Subtraction
            }
        }
        return result;
    }
}
```

## 2.2 SISD (Single Instruction, Single Data)

SISD represents the traditional sequential computing model where one instruction operates on one data element at a time.

### Characteristics:
- **Sequential execution**: Instructions executed one after another
- **Single processor**: One CPU core
- **Simple control flow**: Linear program execution
- **Predictable behavior**: Deterministic execution order

### Advantages:
- **Simplicity**: Easy to understand and debug
- **Predictability**: Deterministic execution
- **Low complexity**: Simple hardware requirements
- **Reliability**: Fewer failure points

### Disadvantages:
- **Performance limitation**: Cannot utilize multiple cores
- **Scalability issues**: Cannot handle large workloads efficiently
- **Resource underutilization**: Single core usage

### Real-World Analogy:
SISD is like having one person working in a factory assembly line, handling each item sequentially. While simple and reliable, it's not efficient for large-scale production.

### Example: SISD Processing
```java
public class SISDExample {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        
        System.out.println("=== SISD Processing ===");
        System.out.println("Original array: " + Arrays.toString(numbers));
        
        // Sequential processing - one instruction at a time
        long startTime = System.currentTimeMillis();
        
        int sum = 0;
        int max = Integer.MIN_VALUE;
        int min = Integer.MAX_VALUE;
        
        // Process each element sequentially
        for (int num : numbers) {
            sum += num;           // Single instruction on single data
            max = Math.max(max, num);  // Single instruction on single data
            min = Math.min(min, num);  // Single instruction on single data
        }
        
        long endTime = System.currentTimeMillis();
        
        System.out.println("Sum: " + sum);
        System.out.println("Max: " + max);
        System.out.println("Min: " + min);
        System.out.println("Processing time: " + (endTime - startTime) + "ms");
        System.out.println("CPU cores used: 1 (SISD)");
    }
}
```

## 2.3 SIMD (Single Instruction, Multiple Data)

SIMD allows the same instruction to operate on multiple data elements simultaneously, providing vectorized processing capabilities.

### Characteristics:
- **Vector processing**: Same operation on multiple data elements
- **Data parallelism**: Multiple data streams processed in parallel
- **Instruction efficiency**: One instruction handles multiple operations
- **Memory bandwidth**: Efficient memory access patterns

### Applications:
- **Scientific computing**: Matrix operations, signal processing
- **Graphics processing**: Image manipulation, rendering
- **Machine learning**: Neural network computations
- **Cryptography**: Encryption/decryption operations

### Real-World Analogy:
SIMD is like using a large cookie cutter that can cut multiple cookies from dough simultaneously, rather than cutting them one by one.

### Example: SIMD-like Operations
```java
public class SIMDExample {
    public static void main(String[] args) {
        int[] vector1 = {1, 2, 3, 4, 5, 6, 7, 8};
        int[] vector2 = {2, 3, 4, 5, 6, 7, 8, 9};
        
        System.out.println("=== SIMD-like Vector Operations ===");
        System.out.println("Vector 1: " + Arrays.toString(vector1));
        System.out.println("Vector 2: " + Arrays.toString(vector2));
        
        // SIMD: Same instruction (addition) on multiple data elements
        int[] result = vectorAdd(vector1, vector2);
        System.out.println("Addition result: " + Arrays.toString(result));
        
        // SIMD: Same instruction (multiplication) on multiple data elements
        int[] multiplyResult = vectorMultiply(vector1, vector2);
        System.out.println("Multiplication result: " + Arrays.toString(multiplyResult));
        
        // SIMD: Same instruction (comparison) on multiple data elements
        boolean[] comparisonResult = vectorCompare(vector1, vector2);
        System.out.println("Comparison result: " + Arrays.toString(comparisonResult));
    }
    
    private static int[] vectorAdd(int[] a, int[] b) {
        int[] result = new int[a.length];
        // Same instruction (addition) applied to all elements
        for (int i = 0; i < a.length; i++) {
            result[i] = a[i] + b[i];
        }
        return result;
    }
    
    private static int[] vectorMultiply(int[] a, int[] b) {
        int[] result = new int[a.length];
        // Same instruction (multiplication) applied to all elements
        for (int i = 0; i < a.length; i++) {
            result[i] = a[i] * b[i];
        }
        return result;
    }
    
    private static boolean[] vectorCompare(int[] a, int[] b) {
        boolean[] result = new boolean[a.length];
        // Same instruction (comparison) applied to all elements
        for (int i = 0; i < a.length; i++) {
            result[i] = a[i] > b[i];
        }
        return result;
    }
}
```

## 2.4 MISD (Multiple Instruction, Single Data)

MISD is a rare architecture where multiple instruction streams operate on a single data stream, primarily used in fault-tolerant and redundant systems.

### Characteristics:
- **Multiple instruction streams**: Different operations on same data
- **Single data stream**: One data path
- **Redundancy**: Multiple processors for fault tolerance
- **Voting mechanisms**: Results compared for correctness

### Applications:
- **Fault-tolerant systems**: Critical applications requiring high reliability
- **Safety-critical systems**: Aerospace, medical, nuclear systems
- **Redundant processing**: Backup computation for verification
- **Security systems**: Multiple verification paths

### Real-World Analogy:
MISD is like having multiple accountants independently verify the same financial calculation to ensure accuracy and catch errors.

### Example: MISD-like Fault Tolerance
```java
public class MISDExample {
    public static void main(String[] args) {
        int data = 42;
        
        System.out.println("=== MISD-like Fault Tolerant Processing ===");
        System.out.println("Input data: " + data);
        
        // Multiple instruction streams processing same data
        int result1 = processor1(data);
        int result2 = processor2(data);
        int result3 = processor3(data);
        
        System.out.println("Processor 1 result: " + result1);
        System.out.println("Processor 2 result: " + result2);
        System.out.println("Processor 3 result: " + result3);
        
        // Voting mechanism to determine correct result
        int finalResult = voteOnResults(result1, result2, result3);
        System.out.println("Final result (by voting): " + finalResult);
    }
    
    private static int processor1(int data) {
        // Different instruction stream: square and add 10
        return data * data + 10;
    }
    
    private static int processor2(int data) {
        // Different instruction stream: multiply by 2 and add 6
        return data * 2 + 6;
    }
    
    private static int processor3(int data) {
        // Different instruction stream: cube and subtract 2
        return data * data * data - 2;
    }
    
    private static int voteOnResults(int r1, int r2, int r3) {
        // Simple voting: return the most common result
        if (r1 == r2 || r1 == r3) return r1;
        if (r2 == r3) return r2;
        return r1; // Default to first result if no majority
    }
}
```

## 2.5 MIMD (Multiple Instruction, Multiple Data)

MIMD is the most flexible parallel architecture where multiple processors can execute different instructions on different data simultaneously.

### Characteristics:
- **Multiple instruction streams**: Independent operations
- **Multiple data streams**: Independent data paths
- **True parallelism**: Independent processor execution
- **Scalability**: Can scale to large numbers of processors

### Types:
- **Shared Memory MIMD**: Processors share common memory
- **Distributed Memory MIMD**: Each processor has private memory
- **Hybrid MIMD**: Combination of shared and distributed memory

### Applications:
- **General-purpose parallel computing**: Most parallel applications
- **Distributed systems**: Web services, databases
- **High-performance computing**: Supercomputers, clusters
- **Multicore systems**: Modern processors

### Real-World Analogy:
MIMD is like a restaurant kitchen where multiple chefs work independently, each preparing different dishes using different ingredients and techniques.

### Example: MIMD Processing
```java
public class MIMDExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== MIMD Processing ===");
        
        // Different data sets for different processors
        int[] dataSet1 = {1, 2, 3, 4, 5};
        int[] dataSet2 = {10, 20, 30, 40, 50};
        int[] dataSet3 = {100, 200, 300, 400, 500};
        
        // Results from different processors
        int[] results = new int[3];
        
        // Create threads (simulating different processors)
        Thread processor1 = new Thread(() -> {
            // Different instruction: find sum
            results[0] = Arrays.stream(dataSet1).sum();
            System.out.println("Processor 1 (sum): " + results[0]);
        });
        
        Thread processor2 = new Thread(() -> {
            // Different instruction: find product
            results[1] = Arrays.stream(dataSet2).reduce(1, (a, b) -> a * b);
            System.out.println("Processor 2 (product): " + results[1]);
        });
        
        Thread processor3 = new Thread(() -> {
            // Different instruction: find average
            results[2] = (int) Arrays.stream(dataSet3).average().orElse(0);
            System.out.println("Processor 3 (average): " + results[2]);
        });
        
        // Start all processors (MIMD execution)
        processor1.start();
        processor2.start();
        processor3.start();
        
        // Wait for completion
        processor1.join();
        processor2.join();
        processor3.join();
        
        System.out.println("All MIMD processors completed");
        System.out.println("Results: " + Arrays.toString(results));
    }
}
```

## 2.6 Shared Memory Architecture

Shared memory architecture allows multiple processors to access the same memory space, enabling direct data sharing and communication.

### Characteristics:
- **Single address space**: All processors see the same memory
- **Direct memory access**: Processors can read/write any memory location
- **Synchronization required**: Need locks, semaphores to prevent race conditions
- **Cache coherence**: Ensures data consistency across processor caches

### Advantages:
- **Simple programming model**: Easy to share data
- **Fast communication**: Direct memory access
- **Dynamic load balancing**: Easy to redistribute work
- **Global data structures**: Can use shared data structures

### Disadvantages:
- **Scalability limitations**: Memory bandwidth becomes bottleneck
- **Synchronization overhead**: Lock contention reduces performance
- **Cache coherence cost**: Maintaining consistency is expensive
- **Memory contention**: Multiple processors competing for memory

### Real-World Analogy:
Shared memory is like a shared whiteboard in a meeting room where everyone can read and write information, but they need to coordinate to avoid overwriting each other's work.

### Example: Shared Memory with Synchronization
```java
public class SharedMemoryExample {
    private static final Object lock = new Object();
    private static int sharedCounter = 0;
    private static int[] sharedArray = new int[1000];
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Shared Memory Architecture Demo ===");
        
        Thread[] threads = new Thread[4];
        
        // Create multiple threads accessing shared memory
        for (int i = 0; i < threads.length; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                // Each thread modifies shared memory
                for (int j = 0; j < 250; j++) {
                    synchronized (lock) {
                        // Critical section - accessing shared memory
                        sharedCounter++;
                        sharedArray[sharedCounter % sharedArray.length] = threadId;
                    }
                }
                System.out.println("Thread " + threadId + " completed");
            });
        }
        
        // Start all threads
        for (Thread thread : threads) {
            thread.start();
        }
        
        // Wait for completion
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Final shared counter: " + sharedCounter);
        System.out.println("Expected: " + (4 * 250));
    }
}
```

## 2.7 Distributed Memory Architecture

Distributed memory architecture uses separate memory spaces for each processor, requiring explicit message passing for communication.

### Characteristics:
- **Separate address spaces**: Each processor has private memory
- **Message passing**: Communication through explicit messages
- **No shared memory**: Cannot directly access other processors' memory
- **Scalable**: Can scale to thousands of processors

### Advantages:
- **High scalability**: No memory bandwidth limitations
- **Fault tolerance**: Failure of one processor doesn't affect others
- **Cost-effective**: Can use commodity hardware
- **Clear communication model**: Explicit message passing

### Disadvantages:
- **Complex programming**: Must manage message passing
- **Communication overhead**: Message passing has latency
- **Load balancing challenges**: Difficult to redistribute work dynamically
- **Data locality**: Must consider data placement

### Real-World Analogy:
Distributed memory is like a network of separate offices where people communicate through email or phone calls, rather than sharing a common workspace.

### Example: Distributed Memory Simulation
```java
public class DistributedMemoryExample {
    private static final int NUM_PROCESSORS = 4;
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Distributed Memory Architecture Demo ===");
        
        // Simulate separate memory spaces
        Map<Integer, Queue<String>> messageQueues = new HashMap<>();
        for (int i = 0; i < NUM_PROCESSORS; i++) {
            messageQueues.put(i, new ConcurrentLinkedQueue<>());
        }
        
        // Create processors with separate memory
        List<Thread> processors = new ArrayList<>();
        
        for (int i = 0; i < NUM_PROCESSORS; i++) {
            final int processorId = i;
            processors.add(new Thread(() -> {
                // Each processor has its own memory space
                int localData = processorId * 100;
                
                // Send message to next processor
                int nextProcessor = (processorId + 1) % NUM_PROCESSORS;
                String message = "Data from processor " + processorId + ": " + localData;
                messageQueues.get(nextProcessor).offer(message);
                
                // Process received messages
                Queue<String> myQueue = messageQueues.get(processorId);
                while (!myQueue.isEmpty()) {
                    String receivedMessage = myQueue.poll();
                    System.out.println("Processor " + processorId + " received: " + receivedMessage);
                }
                
                System.out.println("Processor " + processorId + " completed with local data: " + localData);
            }));
        }
        
        // Start all processors
        for (Thread processor : processors) {
            processor.start();
        }
        
        // Wait for completion
        for (Thread processor : processors) {
            processor.join();
        }
    }
}
```

## 2.8 Hybrid Architecture

Hybrid architecture combines shared and distributed memory models, providing benefits of both approaches.

### Characteristics:
- **Hierarchical memory**: Multiple levels of memory hierarchy
- **Local shared memory**: Processors within a node share memory
- **Distributed memory**: Different nodes have separate memory
- **NUMA awareness**: Non-uniform memory access considerations

### Advantages:
- **Scalability**: Can scale beyond shared memory limitations
- **Performance**: Local shared memory provides fast access
- **Flexibility**: Can optimize for different access patterns
- **Cost-effectiveness**: Balance between performance and cost

### Disadvantages:
- **Complexity**: More complex programming model
- **NUMA effects**: Non-uniform memory access performance
- **Load balancing**: Complex load balancing across hierarchy
- **Debugging**: More difficult to debug and optimize

### Real-World Analogy:
Hybrid architecture is like a corporate structure with local offices (shared memory within offices) and remote branches (distributed memory between offices), with different communication patterns for each level.

### Example: Hybrid Architecture Simulation
```java
public class HybridArchitectureExample {
    private static final int NUM_NODES = 2;
    private static final int NUM_PROCESSORS_PER_NODE = 2;
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Hybrid Architecture Demo ===");
        
        // Simulate nodes with shared memory within each node
        Map<Integer, Object> nodeLocks = new HashMap<>();
        Map<Integer, Map<String, Object>> nodeSharedMemory = new HashMap<>();
        
        for (int nodeId = 0; nodeId < NUM_NODES; nodeId++) {
            nodeLocks.put(nodeId, new Object());
            nodeSharedMemory.put(nodeId, new HashMap<>());
        }
        
        // Message passing between nodes
        Map<Integer, Queue<String>> interNodeMessages = new HashMap<>();
        for (int i = 0; i < NUM_NODES; i++) {
            interNodeMessages.put(i, new ConcurrentLinkedQueue<>());
        }
        
        List<Thread> allProcessors = new ArrayList<>();
        
        // Create processors for each node
        for (int nodeId = 0; nodeId < NUM_NODES; nodeId++) {
            for (int procId = 0; procId < NUM_PROCESSORS_PER_NODE; procId++) {
                final int finalNodeId = nodeId;
                final int finalProcId = procId;
                final int globalProcId = nodeId * NUM_PROCESSORS_PER_NODE + procId;
                
                allProcessors.add(new Thread(() -> {
                    // Access local shared memory (fast)
                    synchronized (nodeLocks.get(finalNodeId)) {
                        Map<String, Object> localMemory = nodeSharedMemory.get(finalNodeId);
                        localMemory.put("processor_" + globalProcId, "data_" + globalProcId);
                        System.out.println("Processor " + globalProcId + " wrote to local shared memory");
                    }
                    
                    // Send message to other node (slower)
                    int targetNode = (finalNodeId + 1) % NUM_NODES;
                    String message = "Message from processor " + globalProcId + " in node " + finalNodeId;
                    interNodeMessages.get(targetNode).offer(message);
                    
                    // Check for messages from other nodes
                    Queue<String> myMessages = interNodeMessages.get(finalNodeId);
                    while (!myMessages.isEmpty()) {
                        String receivedMessage = myMessages.poll();
                        System.out.println("Processor " + globalProcId + " received: " + receivedMessage);
                    }
                }));
            }
        }
        
        // Start all processors
        for (Thread processor : allProcessors) {
            processor.start();
        }
        
        // Wait for completion
        for (Thread processor : allProcessors) {
            processor.join();
        }
    }
}
```

## 2.9 NUMA (Non-Uniform Memory Access)

NUMA is a memory architecture where memory access times depend on the memory location relative to the processor.

### Characteristics:
- **Non-uniform access**: Different memory access times
- **Local memory**: Fast access to local memory
- **Remote memory**: Slower access to remote memory
- **Memory hierarchy**: Multiple levels of memory performance

### NUMA Effects:
- **Locality matters**: Data placement affects performance
- **Cache coherence**: Complex cache coherence protocols
- **Load balancing**: Must consider memory locality
- **Programming complexity**: Need NUMA-aware programming

### Real-World Analogy:
NUMA is like living in a city where accessing nearby stores is fast, but accessing stores in distant neighborhoods takes longer due to travel time.

### Example: NUMA Awareness
```java
public class NUMAExample {
    private static final int ARRAY_SIZE = 1000000;
    
    public static void main(String[] args) {
        System.out.println("=== NUMA Memory Access Demo ===");
        
        // Simulate NUMA nodes
        int[] localData = new int[ARRAY_SIZE];
        int[] remoteData = new int[ARRAY_SIZE];
        
        // Initialize data
        Arrays.fill(localData, 1);
        Arrays.fill(remoteData, 1);
        
        // Local memory access (fast)
        long startTime = System.nanoTime();
        int localSum = Arrays.stream(localData).sum();
        long localTime = System.nanoTime() - startTime;
        
        // Remote memory access (slower - simulated with delay)
        startTime = System.nanoTime();
        int remoteSum = Arrays.stream(remoteData).sum();
        long remoteTime = System.nanoTime() - startTime;
        
        System.out.println("Local memory sum: " + localSum + " in " + localTime + " ns");
        System.out.println("Remote memory sum: " + remoteSum + " in " + remoteTime + " ns");
        System.out.println("Access time ratio: " + (double)remoteTime / localTime);
        
        // Demonstrate NUMA-aware allocation
        demonstrateNUMAAwareAllocation();
    }
    
    private static void demonstrateNUMAAwareAllocation() {
        System.out.println("\n=== NUMA-Aware Allocation ===");
        
        // Simulate thread-local storage (NUMA-aware)
        ThreadLocal<int[]> threadLocalData = new ThreadLocal<int[]>() {
            @Override
            protected int[] initialValue() {
                // Allocate data local to this thread's NUMA node
                return new int[1000];
            }
        };
        
        // Use thread-local data to improve NUMA locality
        Thread[] threads = new Thread[4];
        for (int i = 0; i < threads.length; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                int[] localArray = threadLocalData.get();
                Arrays.fill(localArray, threadId);
                
                int sum = Arrays.stream(localArray).sum();
                System.out.println("Thread " + threadId + " local sum: " + sum);
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
```

## 2.10 Parallel Architecture Trends

Modern parallel architecture trends focus on increasing performance while managing complexity and power consumption.

### Current Trends:

#### 1. Many-Core Processors
- **Increasing core count**: 64+ cores in single processors
- **Heterogeneous cores**: Different types of cores for different tasks
- **Power efficiency**: Better performance per watt
- **Specialized units**: Graphics, AI, encryption accelerators

#### 2. Memory Hierarchy Evolution
- **3D memory**: Stacked memory for higher bandwidth
- **Persistent memory**: Non-volatile memory technologies
- **Memory bandwidth**: Increasing memory bandwidth
- **Cache optimization**: Larger and more efficient caches

#### 3. Interconnect Advances
- **High-speed interconnects**: Faster processor-to-processor communication
- **Optical interconnects**: Light-based communication
- **Network-on-chip**: On-chip communication networks
- **Reduced latency**: Lower communication delays

### Future Directions:
- **Quantum computing**: Revolutionary computing paradigm
- **Neuromorphic computing**: Brain-inspired architectures
- **Edge computing**: Distributed computing at the edge
- **AI acceleration**: Specialized hardware for AI workloads

### Real-World Analogy:
Parallel architecture trends are like the evolution of transportation systems - from single-lane roads to multi-lane highways, then to high-speed rail and eventually to flying cars and teleportation.

### Example: Modern Parallel Architecture Features
```java
public class ParallelArchitectureTrends {
    public static void main(String[] args) {
        System.out.println("=== Modern Parallel Architecture Features ===");
        
        // Demonstrate many-core utilization
        demonstrateManyCoreProcessing();
        
        // Demonstrate heterogeneous processing
        demonstrateHeterogeneousProcessing();
        
        // Demonstrate memory hierarchy awareness
        demonstrateMemoryHierarchy();
    }
    
    private static void demonstrateManyCoreProcessing() {
        System.out.println("\n=== Many-Core Processing ===");
        
        int numCores = Runtime.getRuntime().availableProcessors();
        System.out.println("Available cores: " + numCores);
        
        // Utilize all available cores
        ExecutorService executor = Executors.newFixedThreadPool(numCores);
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < numCores; i++) {
            final int coreId = i;
            futures.add(executor.submit(() -> {
                // Simulate work on each core
                int result = 0;
                for (int j = 0; j < 1000000; j++) {
                    result += coreId * j;
                }
                return result;
            }));
        }
        
        int totalResult = 0;
        for (Future<Integer> future : futures) {
            try {
                totalResult += future.get();
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }
        
        System.out.println("Total result from all cores: " + totalResult);
        executor.shutdown();
    }
    
    private static void demonstrateHeterogeneousProcessing() {
        System.out.println("\n=== Heterogeneous Processing ===");
        
        // Simulate different types of processors
        ExecutorService cpuExecutor = Executors.newFixedThreadPool(2);
        ExecutorService gpuExecutor = Executors.newFixedThreadPool(1);
        
        // CPU task (general purpose)
        Future<String> cpuTask = cpuExecutor.submit(() -> {
            Thread.sleep(1000);
            return "CPU task completed";
        });
        
        // GPU task (parallel computation)
        Future<String> gpuTask = gpuExecutor.submit(() -> {
            Thread.sleep(500);
            return "GPU task completed";
        });
        
        try {
            System.out.println(cpuTask.get());
            System.out.println(gpuTask.get());
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
        
        cpuExecutor.shutdown();
        gpuExecutor.shutdown();
    }
    
    private static void demonstrateMemoryHierarchy() {
        System.out.println("\n=== Memory Hierarchy Awareness ===");
        
        // Demonstrate different memory access patterns
        int[] smallArray = new int[1000];    // L1 cache
        int[] mediumArray = new int[100000]; // L2 cache
        int[] largeArray = new int[10000000]; // Main memory
        
        // Access patterns that favor different cache levels
        long startTime = System.nanoTime();
        int smallSum = Arrays.stream(smallArray).sum();
        long smallTime = System.nanoTime() - startTime;
        
        startTime = System.nanoTime();
        int mediumSum = Arrays.stream(mediumArray).sum();
        long mediumTime = System.nanoTime() - startTime;
        
        startTime = System.nanoTime();
        int largeSum = Arrays.stream(largeArray).sum();
        long largeTime = System.nanoTime() - startTime;
        
        System.out.println("Small array (L1): " + smallTime + " ns");
        System.out.println("Medium array (L2): " + mediumTime + " ns");
        System.out.println("Large array (RAM): " + largeTime + " ns");
    }
}
```

This comprehensive section covers all aspects of parallel architecture, from Flynn's taxonomy to modern trends, with practical examples and real-world analogies to help understand these complex concepts.