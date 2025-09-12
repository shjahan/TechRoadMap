# Section 21 - Multithreading Anti-Patterns

## 21.1 Common Anti-Patterns

Anti-patterns are common mistakes in multithreading that lead to poor performance, bugs, or maintenance issues. Understanding these anti-patterns helps avoid them in your code.

### Key Anti-Patterns:

**1. Thread Overuse:**
- Creating too many threads
- Ignoring thread pool benefits
- Resource exhaustion

**2. Lock Overuse:**
- Excessive synchronization
- Coarse-grained locking
- Performance degradation

**3. Deadlock Prone Code:**
- Circular dependencies
- Nested locking
- Resource ordering issues

### Java Example - Common Anti-Patterns:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class CommonAntiPatternsExample {
    private final AtomicInteger antiPatternCount = new AtomicInteger(0);
    
    public void demonstrateCommonAntiPatterns() throws InterruptedException {
        // Anti-pattern 1: Thread overuse
        demonstrateThreadOveruse();
        
        // Anti-pattern 2: Lock overuse
        demonstrateLockOveruse();
        
        // Anti-pattern 3: Deadlock prone code
        demonstrateDeadlockProneCode();
    }
    
    private void demonstrateThreadOveruse() throws InterruptedException {
        System.out.println("=== Thread Overuse Anti-Pattern ===");
        
        // BAD: Creating too many threads
        List<Thread> threads = new ArrayList<>();
        for (int i = 0; i < 1000; i++) {
            Thread thread = new Thread(() -> {
                System.out.println("Thread " + Thread.currentThread().getName() + " running");
                antiPatternCount.incrementAndGet();
            });
            threads.add(thread);
            thread.start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Thread overuse completed");
    }
    
    private void demonstrateLockOveruse() throws InterruptedException {
        System.out.println("\n=== Lock Overuse Anti-Pattern ===");
        
        Object lock = new Object();
        AtomicInteger counter = new AtomicInteger(0);
        
        // BAD: Excessive synchronization
        for (int i = 0; i < 10; i++) {
            Thread thread = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        // Unnecessary synchronization for simple operation
                        counter.incrementAndGet();
                    }
                }
            });
            thread.start();
        }
        
        Thread.sleep(2000);
        System.out.println("Lock overuse completed: " + counter.get());
    }
    
    private void demonstrateDeadlockProneCode() throws InterruptedException {
        System.out.println("\n=== Deadlock Prone Code Anti-Pattern ===");
        
        Object lock1 = new Object();
        Object lock2 = new Object();
        
        // BAD: Potential deadlock
        Thread thread1 = new Thread(() -> {
            synchronized (lock1) {
                System.out.println("Thread 1 acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock2) {
                    System.out.println("Thread 1 acquired lock2");
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            synchronized (lock2) {
                System.out.println("Thread 2 acquired lock2");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock1) {
                    System.out.println("Thread 2 acquired lock1");
                }
            }
        });
        
        thread1.start();
        thread2.start();
        
        thread1.join(2000);
        thread2.join(2000);
        
        System.out.println("Deadlock prone code completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        CommonAntiPatternsExample example = new CommonAntiPatternsExample();
        example.demonstrateCommonAntiPatterns();
    }
}
```

### Real-World Analogy:
Think of anti-patterns like common mistakes in daily life:
- **Thread Overuse**: Like hiring too many employees for a simple task
- **Lock Overuse**: Like putting locks on every door in your house, even the ones you don't need
- **Deadlock Prone Code**: Like two people trying to pass through a narrow doorway at the same time

## 21.2 Thread Overuse

Thread overuse occurs when too many threads are created, leading to resource exhaustion and poor performance.

### Problems:

**1. Resource Exhaustion:**
- Memory overhead
- Context switching costs
- System limits

**2. Performance Degradation:**
- Increased latency
- Reduced throughput
- CPU thrashing

**3. Maintenance Issues:**
- Difficult debugging
- Complex error handling
- Hard to monitor

### Java Example - Thread Overuse:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadOveruseExample {
    private final AtomicInteger threadCount = new AtomicInteger(0);
    
    public void demonstrateThreadOveruse() throws InterruptedException {
        // BAD: Creating too many threads
        System.out.println("=== Thread Overuse Anti-Pattern ===");
        
        List<Thread> threads = new ArrayList<>();
        
        for (int i = 0; i < 100; i++) {
            final int taskId = i;
            Thread thread = new Thread(() -> {
                threadCount.incrementAndGet();
                System.out.println("Task " + taskId + " running on " + Thread.currentThread().getName());
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            threads.add(thread);
            thread.start();
        }
        
        // Wait for completion
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Total threads created: " + threadCount.get());
        
        // GOOD: Using thread pool
        System.out.println("\n=== Correct Approach with Thread Pool ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(10);
        AtomicInteger poolTaskCount = new AtomicInteger(0);
        
        for (int i = 0; i < 100; i++) {
            final int taskId = i;
            executor.submit(() -> {
                poolTaskCount.incrementAndGet();
                System.out.println("Pool task " + taskId + " running on " + Thread.currentThread().getName());
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Pool tasks completed: " + poolTaskCount.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadOveruseExample example = new ThreadOveruseExample();
        example.demonstrateThreadOveruse();
    }
}
```

## 21.3 Lock Overuse

Lock overuse occurs when synchronization is used excessively, leading to performance degradation and reduced parallelism.

### Problems:

**1. Performance Issues:**
- Reduced parallelism
- Increased contention
- Lower throughput

**2. Scalability Problems:**
- Poor scaling with more threads
- Bottlenecks
- Resource waste

**3. Maintenance Issues:**
- Complex code
- Hard to debug
- Error-prone

### Java Example - Lock Overuse:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class LockOveruseExample {
    private final AtomicInteger counter = new AtomicInteger(0);
    private final Object lock = new Object();
    
    public void demonstrateLockOveruse() throws InterruptedException {
        // BAD: Excessive synchronization
        System.out.println("=== Lock Overuse Anti-Pattern ===");
        
        long startTime = System.currentTimeMillis();
        
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        for (int i = 0; i < 1000; i++) {
            executor.submit(() -> {
                // BAD: Synchronizing simple operations
                synchronized (lock) {
                    counter.incrementAndGet();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        long endTime = System.currentTimeMillis();
        System.out.println("Lock overuse time: " + (endTime - startTime) + "ms");
        System.out.println("Counter: " + counter.get());
        
        // GOOD: Using atomic operations
        System.out.println("\n=== Correct Approach with Atomic Operations ===");
        
        AtomicInteger atomicCounter = new AtomicInteger(0);
        startTime = System.currentTimeMillis();
        
        ExecutorService executor2 = Executors.newFixedThreadPool(10);
        
        for (int i = 0; i < 1000; i++) {
            executor2.submit(() -> {
                // GOOD: Using atomic operations
                atomicCounter.incrementAndGet();
            });
        }
        
        executor2.shutdown();
        executor2.awaitTermination(10, TimeUnit.SECONDS);
        
        endTime = System.currentTimeMillis();
        System.out.println("Atomic operations time: " + (endTime - startTime) + "ms");
        System.out.println("Atomic counter: " + atomicCounter.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        LockOveruseExample example = new LockOveruseExample();
        example.demonstrateLockOveruse();
    }
}
```

## 21.4 Deadlock Prone Code

Deadlock prone code has a high risk of deadlock due to improper lock ordering or circular dependencies.

### Common Causes:

**1. Circular Dependencies:**
- Thread A waits for Thread B
- Thread B waits for Thread A
- Neither can proceed

**2. Nested Locking:**
- Acquiring multiple locks
- Different lock ordering
- Resource contention

**3. Resource Ordering:**
- Inconsistent lock ordering
- Dynamic resource allocation
- Complex dependencies

### Java Example - Deadlock Prone Code:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class DeadlockProneCodeExample {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    private final AtomicInteger deadlockCount = new AtomicInteger(0);
    
    public void demonstrateDeadlockProneCode() throws InterruptedException {
        // BAD: Potential deadlock
        System.out.println("=== Deadlock Prone Code Anti-Pattern ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        // Thread 1: Acquires lock1 then lock2
        executor.submit(() -> {
            synchronized (lock1) {
                System.out.println("Thread 1 acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock2) {
                    System.out.println("Thread 1 acquired lock2");
                    deadlockCount.incrementAndGet();
                }
            }
        });
        
        // Thread 2: Acquires lock2 then lock1 (DEADLOCK RISK)
        executor.submit(() -> {
            synchronized (lock2) {
                System.out.println("Thread 2 acquired lock2");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock1) {
                    System.out.println("Thread 2 acquired lock1");
                    deadlockCount.incrementAndGet();
                }
            }
        });
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Deadlock prone code completed: " + deadlockCount.get());
        
        // GOOD: Consistent lock ordering
        System.out.println("\n=== Correct Approach with Consistent Lock Ordering ===");
        
        ExecutorService executor2 = Executors.newFixedThreadPool(2);
        AtomicInteger correctCount = new AtomicInteger(0);
        
        // Thread 1: Acquires lock1 then lock2
        executor2.submit(() -> {
            synchronized (lock1) {
                System.out.println("Thread 1 acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock2) {
                    System.out.println("Thread 1 acquired lock2");
                    correctCount.incrementAndGet();
                }
            }
        });
        
        // Thread 2: Acquires lock1 then lock2 (SAME ORDER)
        executor2.submit(() -> {
            synchronized (lock1) {
                System.out.println("Thread 2 acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                synchronized (lock2) {
                    System.out.println("Thread 2 acquired lock2");
                    correctCount.incrementAndGet();
                }
            }
        });
        
        executor2.shutdown();
        executor2.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Correct approach completed: " + correctCount.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        DeadlockProneCodeExample example = new DeadlockProneCodeExample();
        example.demonstrateDeadlockProneCode();
    }
}
```

## 21.5 Race Condition Prone Code

Race condition prone code has unprotected shared state that can lead to data corruption and unpredictable behavior.

### Common Causes:

**1. Unprotected Shared State:**
- Non-atomic operations
- Missing synchronization
- Volatile misuse

**2. Check-Then-Act:**
- Non-atomic check and modify
- Time-of-check to time-of-use
- Lost updates

**3. Read-Modify-Write:**
- Non-atomic compound operations
- Interleaved execution
- Data corruption

### Java Example - Race Condition Prone Code:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class RaceConditionProneCodeExample {
    private int counter = 0;
    private final AtomicInteger atomicCounter = new AtomicInteger(0);
    
    public void demonstrateRaceConditionProneCode() throws InterruptedException {
        // BAD: Race condition prone code
        System.out.println("=== Race Condition Prone Code Anti-Pattern ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        for (int i = 0; i < 1000; i++) {
            executor.submit(() -> {
                // BAD: Non-atomic operation
                counter++;
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Race condition prone counter: " + counter);
        
        // GOOD: Using atomic operations
        System.out.println("\n=== Correct Approach with Atomic Operations ===");
        
        ExecutorService executor2 = Executors.newFixedThreadPool(10);
        
        for (int i = 0; i < 1000; i++) {
            executor2.submit(() -> {
                // GOOD: Atomic operation
                atomicCounter.incrementAndGet();
            });
        }
        
        executor2.shutdown();
        executor2.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Atomic counter: " + atomicCounter.get());
    }
    
    public static void main(String[] args) throws InterruptedException {
        RaceConditionProneCodeExample example = new RaceConditionProneCodeExample();
        example.demonstrateRaceConditionProneCode();
    }
}
```

## 21.6 Thread Leaks

Thread leaks occur when threads are not properly cleaned up, leading to resource exhaustion and system instability.

### Common Causes:

**1. Unclosed Executors:**
- Forgetting to shutdown
- Exception handling issues
- Resource management

**2. Daemon Thread Issues:**
- Non-daemon threads preventing shutdown
- Resource cleanup problems
- Application hang

**3. Thread Pool Mismanagement:**
- Incorrect pool sizing
- Task submission issues
- Lifecycle management

### Java Example - Thread Leaks:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadLeaksExample {
    private final AtomicInteger leakCount = new AtomicInteger(0);
    
    public void demonstrateThreadLeaks() throws InterruptedException {
        // BAD: Thread leak
        System.out.println("=== Thread Leak Anti-Pattern ===");
        
        // BAD: Not shutting down executor
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                leakCount.incrementAndGet();
                System.out.println("Leaky task running on " + Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // BAD: Forgetting to shutdown
        // executor.shutdown(); // This is missing!
        
        System.out.println("Thread leak created (executor not shutdown)");
        
        // GOOD: Proper resource management
        System.out.println("\n=== Correct Approach with Proper Cleanup ===");
        
        try (ExecutorService executor2 = Executors.newFixedThreadPool(5)) {
            for (int i = 0; i < 10; i++) {
                executor2.submit(() -> {
                    System.out.println("Proper task running on " + Thread.currentThread().getName());
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }
            
            executor2.shutdown();
            executor2.awaitTermination(5, TimeUnit.SECONDS);
        }
        
        System.out.println("Proper cleanup completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadLeaksExample example = new ThreadLeaksExample();
        example.demonstrateThreadLeaks();
    }
}
```

## 21.7 Resource Leaks

Resource leaks occur when system resources are not properly released, leading to resource exhaustion and performance degradation.

### Common Causes:

**1. File Handle Leaks:**
- Unclosed file streams
- Exception handling issues
- Resource management

**2. Database Connection Leaks:**
- Unclosed connections
- Pool exhaustion
- Transaction issues

**3. Memory Leaks:**
- Unreleased objects
- Event listener leaks
- Cache issues

### Java Example - Resource Leaks:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ResourceLeaksExample {
    private final AtomicInteger resourceCount = new AtomicInteger(0);
    
    public void demonstrateResourceLeaks() throws InterruptedException {
        // BAD: Resource leak
        System.out.println("=== Resource Leak Anti-Pattern ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        for (int i = 0; i < 10; i++) {
            executor.submit(() -> {
                // BAD: Not using try-with-resources
                try {
                    // Simulate resource usage
                    Thread.sleep(1000);
                    resourceCount.incrementAndGet();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Resource leak demonstration completed");
        
        // GOOD: Proper resource management
        System.out.println("\n=== Correct Approach with Proper Resource Management ===");
        
        try (ExecutorService executor2 = Executors.newFixedThreadPool(5)) {
            for (int i = 0; i < 10; i++) {
                executor2.submit(() -> {
                    // GOOD: Using try-with-resources
                    try {
                        // Simulate resource usage
                        Thread.sleep(1000);
                        System.out.println("Resource properly managed");
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            }
            
            executor2.shutdown();
            executor2.awaitTermination(5, TimeUnit.SECONDS);
        }
        
        System.out.println("Proper resource management completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ResourceLeaksExample example = new ResourceLeaksExample();
        example.demonstrateResourceLeaks();
    }
}
```

## 21.8 Performance Anti-Patterns

Performance anti-patterns lead to poor performance in multithreaded applications.

### Common Issues:

**1. False Sharing:**
- Cache line contention
- Performance degradation
- Memory layout issues

**2. Lock Contention:**
- Excessive synchronization
- Bottlenecks
- Poor scalability

**3. Context Switching:**
- Too many threads
- Frequent switching
- CPU overhead

### Java Example - Performance Anti-Patterns:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class PerformanceAntiPatternsExample {
    private final AtomicInteger performanceCount = new AtomicInteger(0);
    
    public void demonstratePerformanceAntiPatterns() throws InterruptedException {
        // BAD: False sharing
        System.out.println("=== False Sharing Anti-Pattern ===");
        
        long startTime = System.currentTimeMillis();
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // BAD: Variables that might be in the same cache line
        AtomicInteger counter1 = new AtomicInteger(0);
        AtomicInteger counter2 = new AtomicInteger(0);
        
        for (int i = 0; i < 2; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000000; j++) {
                    counter1.incrementAndGet();
                }
            });
        }
        
        for (int i = 0; i < 2; i++) {
            executor.submit(() -> {
                for (int j = 0; j < 1000000; j++) {
                    counter2.incrementAndGet();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        long endTime = System.currentTimeMillis();
        System.out.println("False sharing time: " + (endTime - startTime) + "ms");
        
        // GOOD: Avoiding false sharing
        System.out.println("\n=== Correct Approach Avoiding False Sharing ===");
        
        startTime = System.currentTimeMillis();
        
        ExecutorService executor2 = Executors.newFixedThreadPool(4);
        
        // GOOD: Separate objects to avoid false sharing
        AtomicInteger counter3 = new AtomicInteger(0);
        AtomicInteger counter4 = new AtomicInteger(0);
        
        for (int i = 0; i < 2; i++) {
            executor2.submit(() -> {
                for (int j = 0; j < 1000000; j++) {
                    counter3.incrementAndGet();
                }
            });
        }
        
        for (int i = 0; i < 2; i++) {
            executor2.submit(() -> {
                for (int j = 0; j < 1000000; j++) {
                    counter4.incrementAndGet();
                }
            });
        }
        
        executor2.shutdown();
        executor2.awaitTermination(10, TimeUnit.SECONDS);
        
        endTime = System.currentTimeMillis();
        System.out.println("No false sharing time: " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        PerformanceAntiPatternsExample example = new PerformanceAntiPatternsExample();
        example.demonstratePerformanceAntiPatterns();
    }
}
```

## 21.9 Security Anti-Patterns

Security anti-patterns in multithreading can lead to security vulnerabilities and data breaches.

### Common Issues:

**1. Information Leakage:**
- Shared sensitive data
- Inadequate isolation
- Memory exposure

**2. Race Conditions:**
- Security checks bypassed
- Privilege escalation
- Data corruption

**3. Resource Exhaustion:**
- Denial of service
- Resource starvation
- System instability

### Java Example - Security Anti-Patterns:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class SecurityAntiPatternsExample {
    private final AtomicInteger securityCount = new AtomicInteger(0);
    
    public void demonstrateSecurityAntiPatterns() throws InterruptedException {
        // BAD: Information leakage
        System.out.println("=== Information Leakage Anti-Pattern ===");
        
        // BAD: Sharing sensitive data without protection
        String sensitiveData = "Secret Information";
        
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        for (int i = 0; i < 5; i++) {
            executor.submit(() -> {
                // BAD: Accessing sensitive data without proper controls
                System.out.println("Thread accessing sensitive data: " + sensitiveData);
                securityCount.incrementAndGet();
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Information leakage demonstration completed");
        
        // GOOD: Proper data protection
        System.out.println("\n=== Correct Approach with Data Protection ===");
        
        ExecutorService executor2 = Executors.newFixedThreadPool(5);
        
        for (int i = 0; i < 5; i++) {
            executor2.submit(() -> {
                // GOOD: Proper access control and data protection
                String protectedData = "Protected Information";
                System.out.println("Thread accessing protected data: " + protectedData);
            });
        }
        
        executor2.shutdown();
        executor2.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Data protection demonstration completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        SecurityAntiPatternsExample example = new SecurityAntiPatternsExample();
        example.demonstrateSecurityAntiPatterns();
    }
}
```

## 21.10 Anti-Pattern Prevention

Preventing anti-patterns requires understanding common mistakes and implementing proper practices.

### Prevention Strategies:

**1. Code Reviews:**
- Peer review process
- Anti-pattern checklists
- Knowledge sharing

**2. Static Analysis:**
- Automated tools
- Code quality checks
- Continuous monitoring

**3. Testing:**
- Unit testing
- Integration testing
- Stress testing

### Java Example - Anti-Pattern Prevention:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class AntiPatternPreventionExample {
    private final AtomicInteger preventionCount = new AtomicInteger(0);
    
    public void demonstrateAntiPatternPrevention() throws InterruptedException {
        // Prevention 1: Use thread pools
        System.out.println("=== Prevention: Use Thread Pools ===");
        
        try (ExecutorService executor = Executors.newFixedThreadPool(5)) {
            for (int i = 0; i < 10; i++) {
                executor.submit(() -> {
                    System.out.println("Task running on " + Thread.currentThread().getName());
                    preventionCount.incrementAndGet();
                });
            }
            
            executor.shutdown();
            executor.awaitTermination(5, TimeUnit.SECONDS);
        }
        
        // Prevention 2: Use atomic operations
        System.out.println("\n=== Prevention: Use Atomic Operations ===");
        
        AtomicInteger atomicCounter = new AtomicInteger(0);
        
        try (ExecutorService executor2 = Executors.newFixedThreadPool(5)) {
            for (int i = 0; i < 1000; i++) {
                executor2.submit(() -> {
                    atomicCounter.incrementAndGet();
                });
            }
            
            executor2.shutdown();
            executor2.awaitTermination(5, TimeUnit.SECONDS);
        }
        
        System.out.println("Atomic counter: " + atomicCounter.get());
        
        // Prevention 3: Proper resource management
        System.out.println("\n=== Prevention: Proper Resource Management ===");
        
        try (ExecutorService executor3 = Executors.newFixedThreadPool(5)) {
            for (int i = 0; i < 10; i++) {
                executor3.submit(() -> {
                    System.out.println("Resource properly managed");
                });
            }
            
            executor3.shutdown();
            executor3.awaitTermination(5, TimeUnit.SECONDS);
        }
        
        System.out.println("Anti-pattern prevention demonstration completed");
    }
    
    public static void main(String[] args) throws InterruptedException {
        AntiPatternPreventionExample example = new AntiPatternPreventionExample();
        example.demonstrateAntiPatternPrevention();
    }
}
```

### Real-World Analogy:
Think of anti-patterns like common mistakes in daily life:
- **Thread Overuse**: Like hiring too many people for a simple task
- **Lock Overuse**: Like putting locks on everything, even things that don't need protection
- **Deadlock Prone Code**: Like two people trying to pass through a narrow doorway at the same time
- **Race Condition Prone Code**: Like multiple people trying to write on the same whiteboard without coordination
- **Thread Leaks**: Like leaving lights on when you leave a room
- **Resource Leaks**: Like not turning off the tap after washing your hands
- **Performance Anti-Patterns**: Like taking the long way to work every day
- **Security Anti-Patterns**: Like leaving your house keys under the doormat

The key is to recognize these patterns and implement proper solutions to avoid them!