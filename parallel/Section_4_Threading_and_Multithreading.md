# Section 4 – Threading and Multithreading

## 4.1 Threading Fundamentals

Threading is the foundation of concurrent programming, allowing multiple execution paths within a single process.

### Key Concepts:
- **Thread**: Lightweight execution unit within a process
- **Process vs Thread**: Threads share memory, processes don't
- **Concurrency**: Multiple threads can run simultaneously
- **Context Switching**: CPU switches between threads

### Real-World Analogy:
Threading is like having multiple workers in a restaurant kitchen. Each worker (thread) can work on different tasks simultaneously, but they all share the same kitchen space (memory) and can communicate directly.

### Example: Basic Threading
```java
public class ThreadingFundamentals {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Threading Fundamentals Demo ===");
        
        // Create and start threads
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Thread 1: " + i);
                try { Thread.sleep(1000); } catch (InterruptedException e) {}
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Thread 2: " + i);
                try { Thread.sleep(1500); } catch (InterruptedException e) {}
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        System.out.println("All threads completed");
    }
}
```

## 4.2 POSIX Threads (pthreads)

POSIX Threads is a threading standard for Unix-like systems providing portable threading functionality.

### Key Concepts:
- **Portable**: Works across different Unix systems
- **Standard API**: Consistent interface across platforms
- **Thread Creation**: pthread_create() function
- **Thread Synchronization**: Mutexes, condition variables

### Real-World Analogy:
POSIX Threads is like having standardized cooking utensils that work in any kitchen following the same specifications, ensuring consistency across different restaurants.

### Example: POSIX Threads Concepts in Java
```java
public class POSIXThreadsExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== POSIX Threads Concepts Demo ===");
        
        // Simulate pthread_create
        Thread[] threads = new Thread[3];
        for (int i = 0; i < threads.length; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + threadId + " started");
                try { Thread.sleep(2000); } catch (InterruptedException e) {}
                System.out.println("Thread " + threadId + " completed");
            });
            threads[i].start(); // Simulates pthread_create
        }
        
        // Simulate pthread_join
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 4.3 Windows Threads

Windows Threads provide threading functionality specific to Windows operating systems.

### Key Concepts:
- **Windows API**: Uses Windows-specific functions
- **Thread Creation**: CreateThread() function
- **Synchronization**: Windows-specific synchronization objects
- **Thread Local Storage**: TLS for thread-specific data

### Real-World Analogy:
Windows Threads are like having specialized tools designed specifically for a particular brand of kitchen equipment, optimized for that specific environment.

### Example: Windows Threads Concepts
```java
public class WindowsThreadsExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Windows Threads Concepts Demo ===");
        
        // Simulate Windows thread creation and management
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        // Simulate CreateThread equivalent
        Future<String> result1 = executor.submit(() -> {
            Thread.currentThread().setName("Windows-Thread-1");
            return "Windows thread 1 completed";
        });
        
        Future<String> result2 = executor.submit(() -> {
            Thread.currentThread().setName("Windows-Thread-2");
            return "Windows thread 2 completed";
        });
        
        try {
            System.out.println(result1.get());
            System.out.println(result2.get());
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
        
        executor.shutdown();
    }
}
```

## 4.4 Java Threads

Java provides built-in threading support through the Thread class and related APIs.

### Key Concepts:
- **Thread Class**: Base class for creating threads
- **Runnable Interface**: Interface for thread execution
- **Thread Lifecycle**: NEW, RUNNABLE, BLOCKED, WAITING, TERMINATED
- **Thread Methods**: start(), join(), interrupt()

### Real-World Analogy:
Java Threads are like having a well-organized kitchen staff where each worker (thread) has clear responsibilities and can be managed efficiently through standardized procedures.

### Example: Java Threads
```java
public class JavaThreadsExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Java Threads Demo ===");
        
        // Method 1: Extending Thread class
        Thread thread1 = new MyThread("Thread-1");
        thread1.start();
        
        // Method 2: Implementing Runnable
        Thread thread2 = new Thread(new MyRunnable("Thread-2"));
        thread2.start();
        
        // Method 3: Lambda expression
        Thread thread3 = new Thread(() -> {
            System.out.println("Lambda thread executing");
            try { Thread.sleep(2000); } catch (InterruptedException e) {}
            System.out.println("Lambda thread completed");
        });
        thread3.start();
        
        thread1.join();
        thread2.join();
        thread3.join();
    }
}

class MyThread extends Thread {
    public MyThread(String name) {
        super(name);
    }
    
    @Override
    public void run() {
        System.out.println(getName() + " is running");
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        System.out.println(getName() + " completed");
    }
}

class MyRunnable implements Runnable {
    private String name;
    
    public MyRunnable(String name) {
        this.name = name;
    }
    
    @Override
    public void run() {
        System.out.println(name + " is running");
        try { Thread.sleep(2000); } catch (InterruptedException e) {}
        System.out.println(name + " completed");
    }
}
```

## 4.5 C++ Threads

C++11 introduced standard threading support through the `<thread>` header.

### Key Concepts:
- **std::thread**: Standard thread class
- **Thread Creation**: Constructor with function/lambda
- **Thread Management**: join(), detach(), get_id()
- **Thread Safety**: Mutexes, condition variables

### Real-World Analogy:
C++ Threads are like having precise, high-performance kitchen equipment that gives you fine control over every aspect of cooking, but requires more expertise to use effectively.

### Example: C++ Threads Concepts in Java
```java
public class CppThreadsExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== C++ Threads Concepts Demo ===");
        
        // Simulate std::thread creation
        Thread thread1 = new Thread(() -> {
            System.out.println("C++ style thread 1 executing");
            try { Thread.sleep(1000); } catch (InterruptedException e) {}
        });
        
        Thread thread2 = new Thread(() -> {
            System.out.println("C++ style thread 2 executing");
            try { Thread.sleep(1500); } catch (InterruptedException e) {}
        });
        
        // Simulate std::thread::join()
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
        
        System.out.println("All C++ style threads completed");
    }
}
```

## 4.6 Thread Synchronization

Thread synchronization ensures proper coordination between threads accessing shared resources.

### Key Concepts:
- **Race Conditions**: Unpredictable behavior from concurrent access
- **Critical Sections**: Code sections that must be executed atomically
- **Synchronization Mechanisms**: Locks, semaphores, barriers
- **Deadlock Prevention**: Avoiding circular waiting conditions

### Real-World Analogy:
Thread synchronization is like having a traffic control system in a busy intersection. Without proper coordination, cars (threads) would collide when trying to access the same road (shared resource).

### Example: Thread Synchronization
```java
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class ThreadSynchronizationExample {
    private static int sharedCounter = 0;
    private static final Object lock = new Object();
    private static final ReentrantLock reentrantLock = new ReentrantLock();
    private static AtomicInteger atomicCounter = new AtomicInteger(0);
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Thread Synchronization Demo ===");
        
        // Demonstrate race condition
        demonstrateRaceCondition();
        
        // Demonstrate synchronized solution
        demonstrateSynchronizedSolution();
        
        // Demonstrate lock solution
        demonstrateLockSolution();
        
        // Demonstrate atomic solution
        demonstrateAtomicSolution();
    }
    
    private static void demonstrateRaceCondition() throws InterruptedException {
        System.out.println("\n=== Race Condition ===");
        sharedCounter = 0;
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    sharedCounter++; // Race condition!
                }
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Unsafe counter: " + sharedCounter);
    }
    
    private static void demonstrateSynchronizedSolution() throws InterruptedException {
        System.out.println("\n=== Synchronized Solution ===");
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
    
    private static void demonstrateLockSolution() throws InterruptedException {
        System.out.println("\n=== Lock Solution ===");
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
        
        System.out.println("Lock counter: " + sharedCounter);
    }
    
    private static void demonstrateAtomicSolution() throws InterruptedException {
        System.out.println("\n=== Atomic Solution ===");
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

## 4.7 Thread Communication

Thread communication enables threads to exchange data and coordinate their activities.

### Key Concepts:
- **Shared Memory**: Direct memory access for communication
- **Message Passing**: Explicit message exchange
- **Producer-Consumer**: One thread produces, another consumes
- **Wait-Notify**: Threads waiting for conditions

### Real-World Analogy:
Thread communication is like having a communication system in a restaurant where the chef (producer) puts completed dishes on a pass (shared memory) and the server (consumer) takes them to customers.

### Example: Thread Communication
```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public class ThreadCommunicationExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Thread Communication Demo ===");
        
        // Producer-Consumer pattern
        BlockingQueue<String> queue = new LinkedBlockingQueue<>();
        
        // Producer thread
        Thread producer = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                String item = "Item-" + i;
                queue.offer(item);
                System.out.println("Produced: " + item);
                try { Thread.sleep(1000); } catch (InterruptedException e) {}
            }
        });
        
        // Consumer thread
        Thread consumer = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                try {
                    String item = queue.take();
                    System.out.println("Consumed: " + item);
                    Thread.sleep(1500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        producer.start();
        consumer.start();
        
        producer.join();
        consumer.join();
    }
}
```

## 4.8 Thread Safety

Thread safety ensures that shared resources can be accessed safely by multiple threads without causing data corruption.

### Key Concepts:
- **Atomic Operations**: Operations that complete without interruption
- **Immutable Objects**: Objects that cannot be modified after creation
- **Thread-Safe Collections**: Collections designed for concurrent access
- **Volatile Variables**: Variables that are always read from main memory

### Real-World Analogy:
Thread safety is like having safety protocols in a laboratory where multiple scientists work with the same equipment. Proper protocols ensure no one gets hurt and experiments aren't contaminated.

### Example: Thread Safety
```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;

public class ThreadSafetyExample {
    private static volatile boolean running = true;
    private static final ConcurrentHashMap<String, Integer> threadSafeMap = new ConcurrentHashMap<>();
    private static final CopyOnWriteArrayList<String> threadSafeList = new CopyOnWriteArrayList<>();
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Thread Safety Demo ===");
        
        // Demonstrate thread-safe collections
        demonstrateThreadSafeCollections();
        
        // Demonstrate volatile variables
        demonstrateVolatileVariables();
    }
    
    private static void demonstrateThreadSafeCollections() throws InterruptedException {
        System.out.println("\n=== Thread-Safe Collections ===");
        
        Thread[] threads = new Thread[3];
        for (int i = 0; i < threads.length; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 5; j++) {
                    String key = "Thread-" + threadId + "-Item-" + j;
                    threadSafeMap.put(key, j);
                    threadSafeList.add(key);
                }
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Thread-safe map size: " + threadSafeMap.size());
        System.out.println("Thread-safe list size: " + threadSafeList.size());
    }
    
    private static void demonstrateVolatileVariables() throws InterruptedException {
        System.out.println("\n=== Volatile Variables ===");
        
        Thread writer = new Thread(() -> {
            try {
                Thread.sleep(1000);
                running = false;
                System.out.println("Writer: Set running to false");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        Thread reader = new Thread(() -> {
            while (running) {
                System.out.println("Reader: Still running...");
                try { Thread.sleep(200); } catch (InterruptedException e) {}
            }
            System.out.println("Reader: Stopped");
        });
        
        writer.start();
        reader.start();
        
        writer.join();
        reader.join();
    }
}
```

## 4.9 Thread Performance

Thread performance optimization involves understanding and mitigating the overhead associated with threading.

### Key Concepts:
- **Thread Creation Overhead**: Cost of creating and destroying threads
- **Context Switching**: CPU time spent switching between threads
- **Memory Usage**: Each thread consumes memory for stack and metadata
- **Cache Effects**: Threads can affect CPU cache performance

### Real-World Analogy:
Thread performance is like managing a team of workers. While more workers can potentially do more work, there's overhead in coordination, and sometimes fewer well-coordinated workers are more efficient than many poorly coordinated ones.

### Example: Thread Performance Analysis
```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ThreadPerformanceExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Thread Performance Demo ===");
        
        // Analyze thread creation overhead
        analyzeThreadCreationOverhead();
        
        // Analyze optimal thread count
        analyzeOptimalThreadCount();
    }
    
    private static void analyzeThreadCreationOverhead() throws InterruptedException {
        System.out.println("\n=== Thread Creation Overhead ===");
        
        int numThreads = 1000;
        
        // Measure thread creation time
        long startTime = System.currentTimeMillis();
        Thread[] threads = new Thread[numThreads];
        
        for (int i = 0; i < numThreads; i++) {
            threads[i] = new Thread(() -> {
                // Minimal work
            });
        }
        
        long creationTime = System.currentTimeMillis() - startTime;
        System.out.println("Created " + numThreads + " threads in " + creationTime + "ms");
        
        // Start threads
        startTime = System.currentTimeMillis();
        for (Thread thread : threads) {
            thread.start();
        }
        
        // Wait for completion
        for (Thread thread : threads) {
            thread.join();
        }
        
        long totalTime = System.currentTimeMillis() - startTime;
        System.out.println("Total execution time: " + totalTime + "ms");
    }
    
    private static void analyzeOptimalThreadCount() throws InterruptedException {
        System.out.println("\n=== Optimal Thread Count Analysis ===");
        
        int[] threadCounts = {1, 2, 4, 8, 16};
        int workLoad = 1000000;
        
        for (int threadCount : threadCounts) {
            ExecutorService executor = Executors.newFixedThreadPool(threadCount);
            
            long startTime = System.currentTimeMillis();
            
            for (int i = 0; i < threadCount; i++) {
                executor.submit(() -> {
                    // CPU-intensive work
                    long sum = 0;
                    for (int j = 0; j < workLoad / threadCount; j++) {
                        sum += j;
                    }
                    return sum;
                });
            }
            
            executor.shutdown();
            while (!executor.isTerminated()) {
                Thread.sleep(1);
            }
            
            long executionTime = System.currentTimeMillis() - startTime;
            System.out.println(threadCount + " threads: " + executionTime + "ms");
        }
    }
}
```

## 4.10 Threading Best Practices

Threading best practices help avoid common pitfalls and improve performance and reliability.

### Key Concepts:
- **Avoid Thread Creation**: Use thread pools instead of creating threads frequently
- **Minimize Synchronization**: Reduce lock contention and critical sections
- **Prefer Immutable Objects**: Use immutable data structures when possible
- **Handle InterruptedException**: Always handle thread interruption properly

### Real-World Analogy:
Threading best practices are like following proven recipes and cooking techniques in a kitchen. They help avoid disasters and ensure consistent, high-quality results.

### Example: Threading Best Practices
```java
import java.util.concurrent.*;

public class ThreadingBestPracticesExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Threading Best Practices Demo ===");
        
        // Practice 1: Use thread pools
        demonstrateThreadPools();
        
        // Practice 2: Minimize synchronization
        demonstrateMinimalSynchronization();
        
        // Practice 3: Proper exception handling
        demonstrateExceptionHandling();
    }
    
    private static void demonstrateThreadPools() throws InterruptedException {
        System.out.println("\n=== Use Thread Pools ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        List<Future<String>> futures = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            futures.add(executor.submit(() -> {
                try {
                    Thread.sleep(1000);
                    return "Task " + taskId + " completed";
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return "Task " + taskId + " interrupted";
                }
            }));
        }
        
        for (Future<String> future : futures) {
            try {
                System.out.println(future.get());
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }
        
        executor.shutdown();
    }
    
    private static void demonstrateMinimalSynchronization() throws InterruptedException {
        System.out.println("\n=== Minimize Synchronization ===");
        
        // Good: Use atomic variables instead of synchronized blocks
        AtomicInteger counter = new AtomicInteger(0);
        
        Thread[] threads = new Thread[4];
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter.incrementAndGet(); // No synchronization needed
                }
            });
        }
        
        for (Thread thread : threads) {
            thread.start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter value: " + counter.get());
    }
    
    private static void demonstrateExceptionHandling() throws InterruptedException {
        System.out.println("\n=== Proper Exception Handling ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        Future<String> future = executor.submit(() -> {
            try {
                Thread.sleep(2000);
                return "Task completed successfully";
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt(); // Restore interrupt status
                return "Task was interrupted";
            }
        });
        
        // Interrupt the task after 1 second
        Thread.sleep(1000);
        future.cancel(true);
        
        try {
            String result = future.get();
            System.out.println("Result: " + result);
        } catch (CancellationException e) {
            System.out.println("Task was cancelled");
        } catch (ExecutionException e) {
            System.out.println("Task failed: " + e.getCause());
        }
        
        executor.shutdown();
    }
}
```

This comprehensive section covers all aspects of threading and multithreading, from basic concepts to advanced best practices, with practical examples and real-world analogies to help understand these complex concepts from the ground up.