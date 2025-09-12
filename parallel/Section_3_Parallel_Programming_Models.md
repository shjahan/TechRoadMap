# Section 3 – Parallel Programming Models

## 3.1 Shared Memory Programming

Shared memory programming is a parallel programming model where multiple threads or processes share the same memory space, allowing them to access and modify shared data directly.

### Key Concepts:
- **Single Address Space**: All threads see the same memory locations
- **Direct Memory Access**: Threads can read/write any memory location
- **Synchronization Required**: Need mechanisms to prevent race conditions
- **Fast Communication**: Direct memory access provides low-latency communication

### Real-World Analogy:
Shared memory programming is like having multiple chefs working in the same kitchen where they can all access the same ingredients and tools. They need to coordinate to avoid conflicts, but communication is immediate since they're all in the same space.

### Example: Shared Memory with Synchronization
```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class SharedMemoryExample {
    private static int sharedCounter = 0;
    private static final Object lock = new Object();
    private static final ReentrantLock reentrantLock = new ReentrantLock();
    private static AtomicInteger atomicCounter = new AtomicInteger(0);
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Shared Memory Programming Demo ===");
        
        // Demonstrate different synchronization mechanisms
        demonstrateSynchronizedBlock();
        demonstrateReentrantLock();
        demonstrateAtomicVariables();
    }
    
    private static void demonstrateSynchronizedBlock() throws InterruptedException {
        System.out.println("\n=== Synchronized Block ===");
        sharedCounter = 0;
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        sharedCounter++;
                    }
                }
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Synchronized counter: " + sharedCounter);
    }
    
    private static void demonstrateReentrantLock() throws InterruptedException {
        System.out.println("\n=== Reentrant Lock ===");
        sharedCounter = 0;
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    reentrantLock.lock();
                    try {
                        sharedCounter++;
                    } finally {
                        reentrantLock.unlock();
                    }
                }
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Reentrant lock counter: " + sharedCounter);
    }
    
    private static void demonstrateAtomicVariables() throws InterruptedException {
        System.out.println("\n=== Atomic Variables ===");
        atomicCounter.set(0);
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    atomicCounter.incrementAndGet();
                }
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Atomic counter: " + atomicCounter.get());
    }
}
```

## 3.2 Distributed Memory Programming

Distributed memory programming involves multiple processes with separate memory spaces that communicate through message passing.

### Key Concepts:
- **Separate Address Spaces**: Each process has its own private memory
- **Message Passing**: Communication through explicit send/receive operations
- **No Shared Memory**: Cannot directly access other processes' memory
- **Scalable**: Can scale to thousands of processes

### Real-World Analogy:
Distributed memory programming is like having multiple offices in different buildings where people communicate through phone calls, emails, or messengers. Each office has its own files and resources, and information must be explicitly shared.

### Example: Message Passing Simulation
```java
import java.util.concurrent.*;
import java.util.*;

public class DistributedMemoryExample {
    private static final int NUM_PROCESSES = 4;
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Distributed Memory Programming Demo ===");
        
        // Create message queues for each process
        Map<Integer, BlockingQueue<String>> messageQueues = new HashMap<>();
        for (int i = 0; i < NUM_PROCESSES; i++) {
            messageQueues.put(i, new LinkedBlockingQueue<>());
        }
        
        // Create processes
        List<Thread> processes = new ArrayList<>();
        for (int i = 0; i < NUM_PROCESSES; i++) {
            final int processId = i;
            processes.add(new Thread(() -> {
                try {
                    // Each process has its own local data
                    int localData = processId * 100;
                    System.out.println("Process " + processId + " has local data: " + localData);
                    
                    // Send data to next process
                    int nextProcess = (processId + 1) % NUM_PROCESSES;
                    String message = "Data from process " + processId + ": " + localData;
                    messageQueues.get(nextProcess).offer(message);
                    
                    // Receive message from previous process
                    String receivedMessage = messageQueues.get(processId).take();
                    System.out.println("Process " + processId + " received: " + receivedMessage);
                    
                    // Process the data
                    int processedData = localData + processId * 10;
                    System.out.println("Process " + processId + " processed data: " + processedData);
                    
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }));
        }
        
        // Start all processes
        for (Thread process : processes) {
            process.start();
        }
        
        // Wait for completion
        for (Thread process : processes) {
            process.join();
        }
    }
}
```

## 3.3 Message Passing Programming

Message passing programming is a communication paradigm where processes exchange data through explicit send and receive operations.

### Key Concepts:
- **Explicit Communication**: Must explicitly send and receive messages
- **Synchronous vs Asynchronous**: Blocking vs non-blocking operations
- **Point-to-Point**: Direct communication between two processes
- **Collective Operations**: Communication involving multiple processes

### Real-World Analogy:
Message passing is like a postal system where you must explicitly write a letter, address it, and send it through the mail. The recipient must check their mailbox and read the message.

### Example: Message Passing Patterns
```java
import java.util.concurrent.*;
import java.util.*;

public class MessagePassingExample {
    private static final int NUM_WORKERS = 3;
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Message Passing Programming Demo ===");
        
        // Create communication channels
        Map<Integer, BlockingQueue<String>> inputChannels = new HashMap<>();
        Map<Integer, BlockingQueue<String>> outputChannels = new HashMap<>();
        
        for (int i = 0; i < NUM_WORKERS; i++) {
            inputChannels.put(i, new LinkedBlockingQueue<>());
            outputChannels.put(i, new LinkedBlockingQueue<>());
        }
        
        // Create workers
        List<Thread> workers = new ArrayList<>();
        for (int i = 0; i < NUM_WORKERS; i++) {
            final int workerId = i;
            workers.add(new Thread(() -> {
                try {
                    // Receive message
                    String message = inputChannels.get(workerId).take();
                    System.out.println("Worker " + workerId + " received: " + message);
                    
                    // Process message
                    String processedMessage = "Processed by worker " + workerId + ": " + message;
                    Thread.sleep(1000); // Simulate processing time
                    
                    // Send result
                    int nextWorker = (workerId + 1) % NUM_WORKERS;
                    outputChannels.get(nextWorker).offer(processedMessage);
                    System.out.println("Worker " + workerId + " sent result to worker " + nextWorker);
                    
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }));
        }
        
        // Start workers
        for (Thread worker : workers) {
            worker.start();
        }
        
        // Send initial message
        inputChannels.get(0).offer("Hello from main process");
        
        // Wait for completion
        for (Thread worker : workers) {
            worker.join();
        }
    }
}
```

## 3.4 Data Parallel Programming

Data parallel programming divides data into chunks and processes each chunk in parallel using the same operation.

### Key Concepts:
- **Same Operation**: All processors perform the same operation
- **Different Data**: Each processor works on different data chunks
- **SIMD-like**: Single Instruction, Multiple Data approach
- **Scalable**: Performance scales with data size and processor count

### Real-World Analogy:
Data parallel programming is like having multiple workers in a factory assembly line, each working on different products but performing the same assembly steps.

### Example: Data Parallel Processing
```java
import java.util.concurrent.*;
import java.util.*;
import java.util.stream.IntStream;

public class DataParallelExample {
    private static final int ARRAY_SIZE = 1000000;
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Data Parallel Programming Demo ===");
        
        int[] data = generateData(ARRAY_SIZE);
        
        // Sequential processing
        long startTime = System.currentTimeMillis();
        int sequentialSum = calculateSumSequential(data);
        long sequentialTime = System.currentTimeMillis() - startTime;
        
        // Data parallel processing
        startTime = System.currentTimeMillis();
        int parallelSum = calculateSumParallel(data);
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Sequential sum: " + sequentialSum + " in " + sequentialTime + "ms");
        System.out.println("Parallel sum: " + parallelSum + " in " + parallelTime + "ms");
        System.out.println("Speedup: " + (double)sequentialTime / parallelTime);
        
        // Demonstrate different data parallel operations
        demonstrateVectorOperations(data);
    }
    
    private static int[] generateData(int size) {
        return IntStream.range(0, size).toArray();
    }
    
    private static int calculateSumSequential(int[] data) {
        int sum = 0;
        for (int value : data) {
            sum += value;
        }
        return sum;
    }
    
    private static int calculateSumParallel(int[] data) {
        return Arrays.stream(data)
                .parallel()
                .sum();
    }
    
    private static void demonstrateVectorOperations(int[] data) {
        System.out.println("\n=== Vector Operations (Data Parallel) ===");
        
        // Vector addition
        int[] vector1 = Arrays.copyOf(data, 1000);
        int[] vector2 = Arrays.copyOf(data, 1000);
        
        long startTime = System.currentTimeMillis();
        int[] result = vectorAdd(vector1, vector2);
        long parallelTime = System.currentTimeMillis() - startTime;
        
        System.out.println("Vector addition completed in " + parallelTime + "ms");
        System.out.println("First 10 results: " + Arrays.toString(Arrays.copyOf(result, 10)));
    }
    
    private static int[] vectorAdd(int[] a, int[] b) {
        return IntStream.range(0, a.length)
                .parallel()
                .map(i -> a[i] + b[i])
                .toArray();
    }
}
```

## 3.5 Task Parallel Programming

Task parallel programming divides work into independent tasks that can be executed concurrently.

### Key Concepts:
- **Independent Tasks**: Tasks can run independently without dependencies
- **Different Operations**: Each task may perform different operations
- **Dynamic Scheduling**: Tasks can be scheduled dynamically
- **Load Balancing**: Work can be distributed evenly across processors

### Real-World Analogy:
Task parallel programming is like having a project manager assign different tasks to different team members. Each person works on their assigned task independently, and the manager coordinates the overall progress.

### Example: Task Parallel Processing
```java
import java.util.concurrent.*;
import java.util.*;

public class TaskParallelExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Task Parallel Programming Demo ===");
        
        // Create different types of tasks
        List<Callable<String>> tasks = Arrays.asList(
            () -> {
                Thread.sleep(2000);
                return "Task 1: Database query completed";
            },
            () -> {
                Thread.sleep(1500);
                return "Task 2: File processing completed";
            },
            () -> {
                Thread.sleep(1000);
                return "Task 3: Network request completed";
            },
            () -> {
                Thread.sleep(3000);
                return "Task 4: Complex calculation completed";
            }
        );
        
        // Execute tasks in parallel
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        long startTime = System.currentTimeMillis();
        List<Future<String>> futures = executor.invokeAll(tasks);
        long parallelTime = System.currentTimeMillis() - startTime;
        
        // Collect results
        List<String> results = new ArrayList<>();
        for (Future<String> future : futures) {
            results.add(future.get());
        }
        
        System.out.println("All tasks completed in " + parallelTime + "ms");
        for (String result : results) {
            System.out.println(result);
        }
        
        executor.shutdown();
        
        // Demonstrate task dependencies
        demonstrateTaskDependencies();
    }
    
    private static void demonstrateTaskDependencies() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Task Dependencies ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Task 1: Prepare data
        CompletableFuture<String> task1 = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
                return "Data prepared";
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return "Interrupted";
            }
        }, executor);
        
        // Task 2: Process data (depends on Task 1)
        CompletableFuture<String> task2 = task1.thenApplyAsync(data -> {
            try {
                Thread.sleep(1500);
                return "Data processed: " + data;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return "Interrupted";
            }
        }, executor);
        
        // Task 3: Save results (depends on Task 2)
        CompletableFuture<String> task3 = task2.thenApplyAsync(processedData -> {
            try {
                Thread.sleep(500);
                return "Results saved: " + processedData;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return "Interrupted";
            }
        }, executor);
        
        // Wait for final result
        String finalResult = task3.get();
        System.out.println("Final result: " + finalResult);
        
        executor.shutdown();
    }
}
```

## 3.6 Pipeline Programming

Pipeline programming divides work into stages where data flows through a series of processing stages.

### Key Concepts:
- **Sequential Stages**: Data flows through stages in sequence
- **Parallel Execution**: Different stages can process different data simultaneously
- **Streaming**: Continuous flow of data through the pipeline
- **Throughput**: High throughput due to parallel stage execution

### Real-World Analogy:
Pipeline programming is like an assembly line in a car factory where different stations perform different operations (welding, painting, assembly) on different cars simultaneously.

### Example: Pipeline Processing
```java
import java.util.concurrent.*;
import java.util.*;

public class PipelineExample {
    private static final int NUM_STAGES = 4;
    private static final int NUM_ITEMS = 10;
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Pipeline Programming Demo ===");
        
        // Create pipeline stages
        BlockingQueue<String>[] stages = new BlockingQueue[NUM_STAGES + 1];
        for (int i = 0; i <= NUM_STAGES; i++) {
            stages[i] = new LinkedBlockingQueue<>();
        }
        
        // Create stage processors
        List<Thread> stageThreads = new ArrayList<>();
        for (int i = 0; i < NUM_STAGES; i++) {
            final int stageId = i;
            stageThreads.add(new Thread(() -> {
                try {
                    while (true) {
                        String item = stages[stageId].take();
                        
                        // Process item in this stage
                        String processedItem = processStage(item, stageId);
                        
                        // Pass to next stage
                        stages[stageId + 1].put(processedItem);
                        
                        if (item.equals("END")) {
                            break;
                        }
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }));
        }
        
        // Start all stages
        for (Thread stageThread : stageThreads) {
            stageThread.start();
        }
        
        // Feed data into pipeline
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < NUM_ITEMS; i++) {
                    String item = "Item-" + i;
                    stages[0].put(item);
                    System.out.println("Produced: " + item);
                    Thread.sleep(100);
                }
                stages[0].put("END");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Collect results
        Thread collector = new Thread(() -> {
            try {
                while (true) {
                    String result = stages[NUM_STAGES].take();
                    if (result.equals("END")) {
                        break;
                    }
                    System.out.println("Final result: " + result);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        collector.start();
        
        producer.join();
        collector.join();
        
        // Wait for all stages to complete
        for (Thread stageThread : stageThreads) {
            stageThread.join();
        }
    }
    
    private static String processStage(String item, int stageId) {
        try {
            Thread.sleep(200); // Simulate processing time
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        return item + "-Stage" + stageId;
    }
}
```

## 3.7 Map-Reduce Programming

Map-Reduce is a programming model for processing large datasets by dividing work into map and reduce phases.

### Key Concepts:
- **Map Phase**: Transform input data into key-value pairs
- **Reduce Phase**: Aggregate values with the same key
- **Shuffle Phase**: Group values by key between map and reduce
- **Scalability**: Can process petabytes of data across thousands of machines

### Real-World Analogy:
Map-Reduce is like organizing a library. The map phase is like sorting books by category, and the reduce phase is like counting how many books are in each category.

### Example: Map-Reduce Implementation
```java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class MapReduceExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Map-Reduce Programming Demo ===");
        
        // Sample data: words from documents
        List<String> documents = Arrays.asList(
            "the quick brown fox",
            "the lazy dog",
            "quick brown fox jumps",
            "lazy dog sleeps"
        );
        
        // Map phase: extract words and create key-value pairs
        List<Map.Entry<String, Integer>> mapResults = mapPhase(documents);
        System.out.println("Map phase results: " + mapResults);
        
        // Shuffle phase: group by key
        Map<String, List<Integer>> shuffledData = shufflePhase(mapResults);
        System.out.println("Shuffled data: " + shuffledData);
        
        // Reduce phase: aggregate values
        Map<String, Integer> finalResults = reducePhase(shuffledData);
        System.out.println("Final word count: " + finalResults);
        
        // Demonstrate parallel map-reduce
        demonstrateParallelMapReduce(documents);
    }
    
    private static List<Map.Entry<String, Integer>> mapPhase(List<String> documents) {
        List<Map.Entry<String, Integer>> results = new ArrayList<>();
        
        for (String document : documents) {
            String[] words = document.split(" ");
            for (String word : words) {
                results.add(new AbstractMap.SimpleEntry<>(word, 1));
            }
        }
        
        return results;
    }
    
    private static Map<String, List<Integer>> shufflePhase(List<Map.Entry<String, Integer>> mapResults) {
        Map<String, List<Integer>> grouped = new HashMap<>();
        
        for (Map.Entry<String, Integer> entry : mapResults) {
            grouped.computeIfAbsent(entry.getKey(), k -> new ArrayList<>()).add(entry.getValue());
        }
        
        return grouped;
    }
    
    private static Map<String, Integer> reducePhase(Map<String, List<Integer>> shuffledData) {
        Map<String, Integer> results = new HashMap<>();
        
        for (Map.Entry<String, List<Integer>> entry : shuffledData.entrySet()) {
            int sum = entry.getValue().stream().mapToInt(Integer::intValue).sum();
            results.put(entry.getKey(), sum);
        }
        
        return results;
    }
    
    private static void demonstrateParallelMapReduce(List<String> documents) throws InterruptedException, ExecutionException {
        System.out.println("\n=== Parallel Map-Reduce ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Parallel map phase
        List<Future<List<Map.Entry<String, Integer>>>> mapFutures = new ArrayList<>();
        for (String document : documents) {
            mapFutures.add(executor.submit(() -> {
                List<Map.Entry<String, Integer>> results = new ArrayList<>();
                String[] words = document.split(" ");
                for (String word : words) {
                    results.add(new AbstractMap.SimpleEntry<>(word, 1));
                }
                return results;
            }));
        }
        
        // Collect map results
        List<Map.Entry<String, Integer>> allMapResults = new ArrayList<>();
        for (Future<List<Map.Entry<String, Integer>>> future : mapFutures) {
            allMapResults.addAll(future.get());
        }
        
        // Parallel reduce phase
        Map<String, List<Integer>> shuffledData = shufflePhase(allMapResults);
        List<Future<Map.Entry<String, Integer>>> reduceFutures = new ArrayList<>();
        
        for (Map.Entry<String, List<Integer>> entry : shuffledData.entrySet()) {
            reduceFutures.add(executor.submit(() -> {
                int sum = entry.getValue().stream().mapToInt(Integer::intValue).sum();
                return new AbstractMap.SimpleEntry<>(entry.getKey(), sum);
            }));
        }
        
        // Collect reduce results
        Map<String, Integer> finalResults = new HashMap<>();
        for (Future<Map.Entry<String, Integer>> future : reduceFutures) {
            Map.Entry<String, Integer> result = future.get();
            finalResults.put(result.getKey(), result.getValue());
        }
        
        System.out.println("Parallel map-reduce results: " + finalResults);
        executor.shutdown();
    }
}
```

## 3.8 Actor Model Programming

The Actor Model is a programming paradigm where computation is performed by actors that communicate through asynchronous message passing.

### Key Concepts:
- **Actors**: Independent entities with their own state and behavior
- **Asynchronous Messages**: Non-blocking communication between actors
- **Isolated State**: Each actor has private state that cannot be accessed directly
- **Fault Tolerance**: Actors can fail independently without affecting others

### Real-World Analogy:
The Actor Model is like a theater production where each actor (performer) has their own script and role. They communicate through dialogue (messages) but don't directly access each other's props or costumes (state).

### Example: Actor Model Implementation
```java
import java.util.concurrent.*;
import java.util.*;

public class ActorModelExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Actor Model Programming Demo ===");
        
        // Create actor system
        ActorSystem system = new ActorSystem();
        
        // Create actors
        ActorRef counter = system.createActor(new CounterActor());
        ActorRef printer = system.createActor(new PrinterActor());
        
        // Send messages
        counter.send(new IncrementMessage());
        counter.send(new IncrementMessage());
        counter.send(new GetCountMessage(printer));
        
        Thread.sleep(1000);
        system.shutdown();
    }
}

// Message classes
abstract class Message {}
class IncrementMessage extends Message {}
class GetCountMessage extends Message {
    final ActorRef replyTo;
    GetCountMessage(ActorRef replyTo) { this.replyTo = replyTo; }
}
class CountMessage extends Message {
    final int count;
    CountMessage(int count) { this.count = count; }
}

// Actor base class
abstract class Actor {
    protected ActorRef self;
    
    public void setSelf(ActorRef self) {
        this.self = self;
    }
    
    public abstract void receive(Message message);
}

// Counter actor
class CounterActor extends Actor {
    private int count = 0;
    
    @Override
    public void receive(Message message) {
        if (message instanceof IncrementMessage) {
            count++;
            System.out.println("Counter incremented to: " + count);
        } else if (message instanceof GetCountMessage) {
            GetCountMessage msg = (GetCountMessage) message;
            msg.replyTo.send(new CountMessage(count));
        }
    }
}

// Printer actor
class PrinterActor extends Actor {
    @Override
    public void receive(Message message) {
        if (message instanceof CountMessage) {
            CountMessage msg = (CountMessage) message;
            System.out.println("Current count: " + msg.count);
        }
    }
}

// Actor reference
class ActorRef {
    private final Actor actor;
    private final BlockingQueue<Message> mailbox;
    private final Thread actorThread;
    
    public ActorRef(Actor actor) {
        this.actor = actor;
        this.mailbox = new LinkedBlockingQueue<>();
        this.actorThread = new Thread(this::processMessages);
        actor.setSelf(this);
        actorThread.start();
    }
    
    public void send(Message message) {
        mailbox.offer(message);
    }
    
    private void processMessages() {
        try {
            while (!Thread.currentThread().isInterrupted()) {
                Message message = mailbox.take();
                actor.receive(message);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public void stop() {
        actorThread.interrupt();
    }
}

// Actor system
class ActorSystem {
    private final List<ActorRef> actors = new ArrayList<>();
    
    public ActorRef createActor(Actor actor) {
        ActorRef actorRef = new ActorRef(actor);
        actors.add(actorRef);
        return actorRef;
    }
    
    public void shutdown() {
        for (ActorRef actor : actors) {
            actor.stop();
        }
    }
}
```

## 3.9 Functional Parallel Programming

Functional parallel programming applies functional programming principles to parallel computation, emphasizing immutability and pure functions.

### Key Concepts:
- **Immutability**: Data structures cannot be modified after creation
- **Pure Functions**: Functions without side effects
- **Higher-Order Functions**: Functions that take or return other functions
- **Lazy Evaluation**: Computation is deferred until needed

### Real-World Analogy:
Functional parallel programming is like a mathematical proof where each step is immutable and can be verified independently. Multiple mathematicians can work on different parts of the proof simultaneously.

### Example: Functional Parallel Programming
```java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class FunctionalParallelExample {
    public static void main(String[] args) {
        System.out.println("=== Functional Parallel Programming Demo ===");
        
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        // Functional approach with parallel streams
        demonstrateFunctionalParallel(numbers);
        
        // Higher-order functions
        demonstrateHigherOrderFunctions(numbers);
        
        // Immutable data structures
        demonstrateImmutability();
    }
    
    private static void demonstrateFunctionalParallel(List<Integer> numbers) {
        System.out.println("\n=== Functional Parallel Processing ===");
        
        // Pure functions for parallel processing
        List<Integer> doubled = numbers.parallelStream()
                .map(FunctionalParallelExample::doubleValue)  // Pure function
                .collect(Collectors.toList());
        
        System.out.println("Doubled values: " + doubled);
        
        // Parallel reduction with pure functions
        int sum = numbers.parallelStream()
                .mapToInt(FunctionalParallelExample::squareValue)  // Pure function
                .sum();
        
        System.out.println("Sum of squares: " + sum);
        
        // Parallel filtering
        List<Integer> evens = numbers.parallelStream()
                .filter(FunctionalParallelExample::isEven)  // Pure function
                .collect(Collectors.toList());
        
        System.out.println("Even numbers: " + evens);
    }
    
    private static void demonstrateHigherOrderFunctions(List<Integer> numbers) {
        System.out.println("\n=== Higher-Order Functions ===");
        
        // Function that returns a function
        Function<Integer, Function<Integer, Integer>> add = x -> y -> x + y;
        
        // Apply higher-order function
        Function<Integer, Integer> add5 = add.apply(5);
        
        List<Integer> result = numbers.parallelStream()
                .map(add5)
                .collect(Collectors.toList());
        
        System.out.println("Numbers + 5: " + result);
        
        // Function composition
        Function<Integer, Integer> doubleAndAdd5 = add5.compose(FunctionalParallelExample::doubleValue);
        
        List<Integer> composed = numbers.parallelStream()
                .map(doubleAndAdd5)
                .collect(Collectors.toList());
        
        System.out.println("Double and add 5: " + composed);
    }
    
    private static void demonstrateImmutability() {
        System.out.println("\n=== Immutability ===");
        
        // Immutable list
        List<String> original = Arrays.asList("a", "b", "c");
        List<String> modified = original.stream()
                .map(String::toUpperCase)
                .collect(Collectors.toList());
        
        System.out.println("Original: " + original);
        System.out.println("Modified: " + modified);
        System.out.println("Original unchanged: " + original);
        
        // Immutable map
        Map<String, Integer> map1 = Map.of("a", 1, "b", 2);
        Map<String, Integer> map2 = map1.entrySet().stream()
                .collect(Collectors.toMap(
                    Map.Entry::getKey,
                    entry -> entry.getValue() * 2
                ));
        
        System.out.println("Original map: " + map1);
        System.out.println("Modified map: " + map2);
    }
    
    // Pure functions (no side effects)
    private static int doubleValue(int x) {
        return x * 2;
    }
    
    private static int squareValue(int x) {
        return x * x;
    }
    
    private static boolean isEven(int x) {
        return x % 2 == 0;
    }
}
```

## 3.10 Hybrid Programming Models

Hybrid programming models combine multiple parallel programming paradigms to leverage the strengths of each approach.

### Key Concepts:
- **Multiple Paradigms**: Combine different programming models
- **Optimized Performance**: Use the best model for each part of the application
- **Complexity Management**: Handle the complexity of multiple models
- **Flexibility**: Adapt to different workload characteristics

### Real-World Analogy:
Hybrid programming models are like a modern kitchen that combines different cooking methods - gas stoves for precise temperature control, electric ovens for even heating, and microwave ovens for quick tasks.

### Example: Hybrid Programming Model
```java
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class HybridProgrammingExample {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.out.println("=== Hybrid Programming Model Demo ===");
        
        // Combine shared memory, message passing, and data parallel
        demonstrateHybridApproach();
    }
    
    private static void demonstrateHybridApproach() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Hybrid Approach ===");
        
        // Phase 1: Data parallel processing (shared memory)
        List<Integer> data = generateData(1000);
        List<Integer> processedData = processDataParallel(data);
        
        // Phase 2: Message passing for coordination
        Map<String, Object> results = coordinateWithMessagePassing(processedData);
        
        // Phase 3: Task parallel for final processing
        String finalResult = processTasksParallel(results);
        
        System.out.println("Final result: " + finalResult);
    }
    
    private static List<Integer> generateData(int size) {
        return new Random().ints(size, 1, 100)
                .boxed()
                .collect(Collectors.toList());
    }
    
    private static List<Integer> processDataParallel(List<Integer> data) {
        // Data parallel processing using shared memory
        return data.parallelStream()
                .map(x -> x * x + 2 * x + 1)
                .collect(Collectors.toList());
    }
    
    private static Map<String, Object> coordinateWithMessagePassing(List<Integer> data) throws InterruptedException, ExecutionException {
        // Message passing for coordination
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        // Worker 1: Calculate statistics
        Future<Map<String, Double>> statsFuture = executor.submit(() -> {
            double sum = data.stream().mapToInt(Integer::intValue).sum();
            double avg = sum / data.size();
            double max = data.stream().mapToInt(Integer::intValue).max().orElse(0);
            
            Map<String, Double> stats = new HashMap<>();
            stats.put("sum", sum);
            stats.put("avg", avg);
            stats.put("max", (double) max);
            return stats;
        });
        
        // Worker 2: Filter data
        Future<List<Integer>> filteredFuture = executor.submit(() -> {
            return data.stream()
                    .filter(x -> x > 1000)
                    .collect(Collectors.toList());
        });
        
        // Collect results
        Map<String, Object> results = new HashMap<>();
        results.put("statistics", statsFuture.get());
        results.put("filtered", filteredFuture.get());
        
        executor.shutdown();
        return results;
    }
    
    private static String processTasksParallel(Map<String, Object> results) throws InterruptedException, ExecutionException {
        // Task parallel processing
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Task 1: Generate report
        Future<String> reportFuture = executor.submit(() -> {
            Map<String, Double> stats = (Map<String, Double>) results.get("statistics");
            return "Report: Sum=" + stats.get("sum") + ", Avg=" + stats.get("avg");
        });
        
        // Task 2: Process filtered data
        Future<String> processFuture = executor.submit(() -> {
            List<Integer> filtered = (List<Integer>) results.get("filtered");
            return "Processed " + filtered.size() + " items";
        });
        
        // Task 3: Generate summary
        Future<String> summaryFuture = executor.submit(() -> {
            return "Summary: Data processing completed successfully";
        });
        
        // Combine results
        String report = reportFuture.get();
        String processed = processFuture.get();
        String summary = summaryFuture.get();
        
        executor.shutdown();
        
        return report + " | " + processed + " | " + summary;
    }
}
```

This comprehensive section covers all parallel programming models from basic shared memory to advanced hybrid approaches, with detailed explanations, practical examples, and real-world analogies to help understand these complex concepts from the ground up.