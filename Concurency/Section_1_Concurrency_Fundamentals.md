# Section 1 – Concurrency Fundamentals

## 1.1 What is Concurrency

Concurrency is the ability of a system to handle multiple tasks or processes simultaneously, where these tasks can be executed in overlapping time periods. It's about managing multiple activities at the same time, even if they don't all run at exactly the same instant.

### Key Concepts
- **Simultaneous Execution**: Multiple tasks can be in progress at the same time
- **Resource Sharing**: Tasks may share system resources like CPU, memory, or I/O
- **Independence**: Tasks can run independently but may need coordination
- **Efficiency**: Better utilization of system resources

### Real-World Analogy
Think of a restaurant kitchen where multiple chefs work simultaneously. One chef might be chopping vegetables while another is grilling meat, and a third is plating dishes. They're all working at the same time, sharing the kitchen space and equipment, but each has their own tasks to complete.

### Java Example
```java
public class ConcurrencyExample {
    public static void main(String[] args) {
        // Create multiple threads that run concurrently
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Thread 1: Task " + i);
                try {
                    Thread.sleep(1000); // Simulate work
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Thread 2: Task " + i);
                try {
                    Thread.sleep(1000); // Simulate work
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Start both threads - they run concurrently
        thread1.start();
        thread2.start();
        
        // Wait for both threads to complete
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("All tasks completed!");
    }
}
```

## 1.2 Concurrency vs Parallelism

While often used interchangeably, concurrency and parallelism are distinct concepts that are both important in modern computing.

### Concurrency
- **Definition**: The ability to handle multiple tasks by interleaving their execution
- **Timing**: Tasks may not run at exactly the same time
- **Resource**: Can be achieved on a single processor through time-slicing
- **Focus**: Managing multiple tasks and their coordination

### Parallelism
- **Definition**: The ability to execute multiple tasks simultaneously at the same instant
- **Timing**: Tasks run at exactly the same time
- **Resource**: Requires multiple processors or cores
- **Focus**: Actual simultaneous execution for performance

### Real-World Analogy
**Concurrency**: A single chef who rapidly switches between tasks - chopping vegetables for 30 seconds, then checking the oven for 10 seconds, then returning to chopping. The tasks are interleaved.

**Parallelism**: Multiple chefs working simultaneously - one chopping vegetables while another tends the oven, both working at the exact same time.

### Java Example
```java
public class ConcurrencyVsParallelismExample {
    // Concurrent execution (can run on single core)
    public static void demonstrateConcurrency() {
        System.out.println("=== Concurrency Example ===");
        
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 3; i++) {
                System.out.println("Concurrent Task 1: " + i);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 3; i++) {
                System.out.println("Concurrent Task 2: " + i);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        thread1.start();
        thread2.start();
        
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Parallel execution (requires multiple cores)
    public static void demonstrateParallelism() {
        System.out.println("\n=== Parallelism Example ===");
        
        // Use parallel streams for true parallelism
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        
        numbers.parallelStream().forEach(num -> {
            System.out.println("Parallel processing: " + num + " on thread: " + 
                             Thread.currentThread().getName());
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
    }
    
    public static void main(String[] args) {
        demonstrateConcurrency();
        demonstrateParallelism();
    }
}
```

## 1.3 Threads vs Processes

Understanding the difference between threads and processes is fundamental to concurrent programming.

### Processes
- **Definition**: Independent execution units with their own memory space
- **Memory**: Each process has its own virtual memory space
- **Communication**: Inter-Process Communication (IPC) required
- **Overhead**: Higher overhead for creation and context switching
- **Isolation**: Complete isolation - one process crash doesn't affect others

### Threads
- **Definition**: Lightweight execution units within a process
- **Memory**: Share the same memory space within the process
- **Communication**: Direct access to shared memory
- **Overhead**: Lower overhead for creation and context switching
- **Isolation**: Less isolation - one thread crash can affect the entire process

### Real-World Analogy
**Processes**: Think of different companies in a building. Each company has its own office space, phone system, and resources. They're completely separate entities.

**Threads**: Think of different departments within the same company. They share the same building, phone system, and some resources, but each department has its own tasks and responsibilities.

### Java Example
```java
public class ThreadsVsProcessesExample {
    // Thread example - shared memory
    private static int sharedCounter = 0;
    private static final Object lock = new Object();
    
    public static void demonstrateThreads() {
        System.out.println("=== Threads Example ===");
        
        // Create multiple threads within the same process
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                synchronized (lock) {
                    sharedCounter++;
                    System.out.println("Thread 1: Counter = " + sharedCounter);
                }
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        Thread thread2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                synchronized (lock) {
                    sharedCounter++;
                    System.out.println("Thread 2: Counter = " + sharedCounter);
                }
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        thread1.start();
        thread2.start();
        
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("Final shared counter value: " + sharedCounter);
    }
    
    // Process simulation (using separate JVM instances)
    public static void demonstrateProcesses() {
        System.out.println("\n=== Process Example ===");
        System.out.println("Process ID: " + ProcessHandle.current().pid());
        System.out.println("Each process has its own memory space");
        System.out.println("Communication between processes requires IPC mechanisms");
    }
    
    public static void main(String[] args) {
        demonstrateThreads();
        demonstrateProcesses();
    }
}
```

## 1.4 Shared Memory vs Message Passing

These are two fundamental approaches to communication between concurrent entities.

### Shared Memory
- **Definition**: Multiple threads/processes access the same memory locations
- **Communication**: Direct read/write to shared variables
- **Synchronization**: Requires explicit synchronization mechanisms (locks, semaphores)
- **Performance**: Generally faster due to direct memory access
- **Complexity**: More complex due to synchronization requirements

### Message Passing
- **Definition**: Entities communicate by sending and receiving messages
- **Communication**: Indirect through message queues, channels, or mailboxes
- **Synchronization**: Built into the message passing mechanism
- **Performance**: Slightly slower due to message overhead
- **Complexity**: Simpler programming model, easier to reason about

### Real-World Analogy
**Shared Memory**: Like a shared whiteboard in a meeting room where multiple people can write and read simultaneously. Everyone needs to coordinate to avoid conflicts.

**Message Passing**: Like passing notes in a classroom. Each person writes a message and passes it to another person, who reads it and can respond with their own message.

### Java Example
```java
public class SharedMemoryVsMessagePassingExample {
    // Shared Memory approach
    public static class SharedMemoryCounter {
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
    
    // Message Passing approach
    public static class MessagePassingCounter {
        private final BlockingQueue<String> messageQueue = new LinkedBlockingQueue<>();
        private final AtomicInteger count = new AtomicInteger(0);
        private volatile boolean running = true;
        
        public void start() {
            new Thread(() -> {
                while (running) {
                    try {
                        String message = messageQueue.take();
                        if ("increment".equals(message)) {
                            count.incrementAndGet();
                        } else if ("get".equals(message)) {
                            System.out.println("Current count: " + count.get());
                        } else if ("stop".equals(message)) {
                            running = false;
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }).start();
        }
        
        public void increment() {
            messageQueue.offer("increment");
        }
        
        public void getCount() {
            messageQueue.offer("get");
        }
        
        public void stop() {
            messageQueue.offer("stop");
        }
    }
    
    public static void demonstrateSharedMemory() {
        System.out.println("=== Shared Memory Example ===");
        SharedMemoryCounter counter = new SharedMemoryCounter();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    counter.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Final count: " + counter.getCount());
    }
    
    public static void demonstrateMessagePassing() {
        System.out.println("\n=== Message Passing Example ===");
        MessagePassingCounter counter = new MessagePassingCounter();
        counter.start();
        
        // Send increment messages
        for (int i = 0; i < 50; i++) {
            counter.increment();
        }
        
        counter.getCount();
        counter.stop();
        
        try {
            Thread.sleep(1000); // Allow time for processing
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) {
        demonstrateSharedMemory();
        demonstrateMessagePassing();
    }
}
```

## 1.5 Race Conditions and Data Races

These are critical concepts in concurrent programming that can lead to unpredictable behavior and bugs.

### Race Conditions
- **Definition**: The behavior of a system depends on the relative timing of events
- **Cause**: Multiple threads accessing shared resources without proper synchronization
- **Result**: Unpredictable and often incorrect behavior
- **Detection**: Difficult to reproduce and debug

### Data Races
- **Definition**: A specific type of race condition where multiple threads access the same memory location without synchronization
- **Requirements**: At least one access is a write operation
- **Result**: Undefined behavior, memory corruption, or incorrect values
- **Prevention**: Use synchronization mechanisms or atomic operations

### Real-World Analogy
**Race Condition**: Imagine two people trying to book the last hotel room simultaneously. The outcome depends on who gets there first, and both might think they got the room.

**Data Race**: Like two people trying to write on the same piece of paper at the same time. The result is a mess, and you can't tell what either person intended to write.

### Java Example
```java
public class RaceConditionExample {
    // Vulnerable class with race condition
    public static class UnsafeCounter {
        private int count = 0;
        
        public void increment() {
            count++; // This is not atomic!
        }
        
        public int getCount() {
            return count;
        }
    }
    
    // Safe class without race condition
    public static class SafeCounter {
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
    
    // Atomic counter (no race condition)
    public static class AtomicCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        public void increment() {
            count.incrementAndGet();
        }
        
        public int getCount() {
            return count.get();
        }
    }
    
    public static void demonstrateRaceCondition() {
        System.out.println("=== Race Condition Example ===");
        
        UnsafeCounter unsafeCounter = new UnsafeCounter();
        int threadCount = 10;
        int incrementsPerThread = 1000;
        
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    unsafeCounter.increment();
                }
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
        
        System.out.println("Expected count: " + (threadCount * incrementsPerThread));
        System.out.println("Actual count: " + unsafeCounter.getCount());
    }
    
    public static void demonstrateSafeCounter() {
        System.out.println("\n=== Safe Counter Example ===");
        
        SafeCounter safeCounter = new SafeCounter();
        int threadCount = 10;
        int incrementsPerThread = 1000;
        
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    safeCounter.increment();
                }
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
        
        System.out.println("Expected count: " + (threadCount * incrementsPerThread));
        System.out.println("Actual count: " + safeCounter.getCount());
    }
    
    public static void main(String[] args) {
        demonstrateRaceCondition();
        demonstrateSafeCounter();
    }
}
```

## 1.6 Critical Sections

A critical section is a code segment that accesses shared resources and must not be executed by more than one thread at a time.

### Key Concepts
- **Mutual Exclusion**: Only one thread can execute the critical section at a time
- **Atomicity**: The entire critical section executes as a single, indivisible operation
- **Synchronization**: Requires proper synchronization mechanisms
- **Deadlock Prevention**: Must be designed to avoid deadlocks

### Real-World Analogy
Think of a single-person bathroom. Only one person can use it at a time, and they must lock the door while inside. The bathroom is the critical section, and the lock ensures mutual exclusion.

### Java Example
```java
public class CriticalSectionExample {
    // Shared resource
    private static int sharedResource = 0;
    private static final Object lock = new Object();
    
    // Critical section - must be synchronized
    public static void criticalSection(int threadId) {
        synchronized (lock) {
            System.out.println("Thread " + threadId + " entering critical section");
            
            // Simulate some work
            int temp = sharedResource;
            try {
                Thread.sleep(100); // Simulate processing time
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            sharedResource = temp + 1;
            
            System.out.println("Thread " + threadId + " leaving critical section, sharedResource = " + sharedResource);
        }
    }
    
    // Non-critical section - can run concurrently
    public static void nonCriticalSection(int threadId) {
        System.out.println("Thread " + threadId + " in non-critical section");
        try {
            Thread.sleep(50);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) {
        int threadCount = 5;
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 3; j++) {
                    nonCriticalSection(threadId);
                    criticalSection(threadId);
                }
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
        
        System.out.println("Final sharedResource value: " + sharedResource);
    }
}
```

## 1.7 Mutual Exclusion

Mutual exclusion ensures that only one thread can access a shared resource at a time, preventing race conditions and data corruption.

### Key Concepts
- **Exclusive Access**: Only one thread can access the resource at any given time
- **Synchronization Primitives**: Locks, semaphores, mutexes
- **Deadlock Prevention**: Must avoid circular waiting
- **Performance**: Balance between safety and performance

### Real-World Analogy
Think of a single-lane bridge where only one car can cross at a time. There's a traffic light that ensures mutual exclusion - when one car is on the bridge, no other car can enter.

### Java Example
```java
public class MutualExclusionExample {
    // Shared resource
    private static int counter = 0;
    private static final Object mutex = new Object();
    
    // Method with mutual exclusion
    public static void incrementWithMutex() {
        synchronized (mutex) {
            int temp = counter;
            try {
                Thread.sleep(10); // Simulate work
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            counter = temp + 1;
        }
    }
    
    // Method without mutual exclusion (vulnerable)
    public static void incrementWithoutMutex() {
        int temp = counter;
        try {
            Thread.sleep(10); // Simulate work
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        counter = temp + 1;
    }
    
    public static void demonstrateMutualExclusion() {
        System.out.println("=== Mutual Exclusion Example ===");
        
        counter = 0;
        int threadCount = 5;
        int operationsPerThread = 100;
        
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    incrementWithMutex();
                }
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
        
        System.out.println("With mutual exclusion - Expected: " + (threadCount * operationsPerThread) + 
                          ", Actual: " + counter);
    }
    
    public static void demonstrateWithoutMutualExclusion() {
        System.out.println("\n=== Without Mutual Exclusion Example ===");
        
        counter = 0;
        int threadCount = 5;
        int operationsPerThread = 100;
        
        Thread[] threads = new Thread[threadCount];
        
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    incrementWithoutMutex();
                }
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
        
        System.out.println("Without mutual exclusion - Expected: " + (threadCount * operationsPerThread) + 
                          ", Actual: " + counter);
    }
    
    public static void main(String[] args) {
        demonstrateMutualExclusion();
        demonstrateWithoutMutualExclusion();
    }
}
```

## 1.8 Deadlock and Livelock

These are two critical problems that can occur in concurrent systems when threads are waiting for each other.

### Deadlock
- **Definition**: A situation where two or more threads are blocked forever, waiting for each other
- **Conditions**: Mutual exclusion, hold and wait, no preemption, circular wait
- **Detection**: Can be detected using resource allocation graphs
- **Prevention**: Break one of the four conditions

### Livelock
- **Definition**: Threads are actively trying to resolve a conflict but end up in an infinite loop
- **Behavior**: Threads are not blocked but make no progress
- **Cause**: Overly polite algorithms or poor conflict resolution
- **Solution**: Introduce randomness or timeouts

### Real-World Analogy
**Deadlock**: Two cars approaching a narrow bridge from opposite directions. Both stop and wait for the other to go first, resulting in a permanent standstill.

**Livelock**: Two people trying to pass each other in a narrow hallway, both stepping to the same side, then both stepping to the other side, repeating indefinitely.

### Java Example
```java
public class DeadlockAndLivelockExample {
    // Deadlock example
    public static class DeadlockExample {
        private static final Object lock1 = new Object();
        private static final Object lock2 = new Object();
        
        public static void method1() {
            synchronized (lock1) {
                System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                synchronized (lock2) {
                    System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock2");
                }
            }
        }
        
        public static void method2() {
            synchronized (lock2) {
                System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock2");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                synchronized (lock1) {
                    System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock1");
                }
            }
        }
    }
    
    // Livelock example
    public static class LivelockExample {
        private static final Object lock = new Object();
        private static boolean isLocked = false;
        
        public static void politeMethod() {
            while (true) {
                synchronized (lock) {
                    if (!isLocked) {
                        isLocked = true;
                        System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock");
                        try {
                            Thread.sleep(1000);
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                        }
                        isLocked = false;
                        break;
                    } else {
                        System.out.println("Thread " + Thread.currentThread().getName() + " being polite, waiting...");
                    }
                }
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }
    
    // Deadlock prevention example
    public static class DeadlockPreventionExample {
        private static final Object lock1 = new Object();
        private static final Object lock2 = new Object();
        
        public static void method1() {
            // Always acquire locks in the same order
            synchronized (lock1) {
                System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                synchronized (lock2) {
                    System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock2");
                }
            }
        }
        
        public static void method2() {
            // Same order as method1
            synchronized (lock1) {
                System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock1");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                synchronized (lock2) {
                    System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock2");
                }
            }
        }
    }
    
    public static void demonstrateDeadlock() {
        System.out.println("=== Deadlock Example ===");
        System.out.println("Starting threads that will deadlock...");
        
        Thread thread1 = new Thread(() -> DeadlockExample.method1());
        Thread thread2 = new Thread(() -> DeadlockExample.method2());
        
        thread1.start();
        thread2.start();
        
        // Let them run for a bit, then interrupt
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        thread1.interrupt();
        thread2.interrupt();
        System.out.println("Deadlock example completed (threads interrupted)");
    }
    
    public static void demonstrateLivelock() {
        System.out.println("\n=== Livelock Example ===");
        System.out.println("Starting threads that will livelock...");
        
        Thread thread1 = new Thread(() -> LivelockExample.politeMethod());
        Thread thread2 = new Thread(() -> LivelockExample.politeMethod());
        
        thread1.start();
        thread2.start();
        
        // Let them run for a bit, then interrupt
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        thread1.interrupt();
        thread2.interrupt();
        System.out.println("Livelock example completed (threads interrupted)");
    }
    
    public static void demonstrateDeadlockPrevention() {
        System.out.println("\n=== Deadlock Prevention Example ===");
        System.out.println("Starting threads with deadlock prevention...");
        
        Thread thread1 = new Thread(() -> DeadlockPreventionExample.method1());
        Thread thread2 = new Thread(() -> DeadlockPreventionExample.method2());
        
        thread1.start();
        thread2.start();
        
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("Deadlock prevention example completed successfully");
    }
    
    public static void main(String[] args) {
        demonstrateDeadlock();
        demonstrateLivelock();
        demonstrateDeadlockPrevention();
    }
}
```

This comprehensive explanation covers all the fundamental concepts of concurrency, providing both theoretical understanding and practical Java examples to illustrate each concept. Each subsection builds upon the previous ones, creating a solid foundation for understanding concurrent programming.