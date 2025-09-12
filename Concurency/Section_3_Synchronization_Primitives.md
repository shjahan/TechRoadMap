# Section 3 – Synchronization Primitives

## 3.1 Mutexes and Locks

Mutexes (mutual exclusion) and locks are synchronization primitives that ensure only one thread can access a shared resource at a time.

### Key Concepts
- **Mutual Exclusion**: Only one thread can hold the lock at a time
- **Critical Section Protection**: Protect shared resources from concurrent access
- **Blocking**: Threads wait until the lock is available
- **Deadlock Prevention**: Must be used carefully to avoid deadlocks

### Real-World Analogy
Think of a bathroom with a lock. Only one person can use it at a time, and others must wait outside until the current user unlocks the door.

### Java Example
```java
public class MutexExample {
    private static final Object mutex = new Object();
    private static int sharedResource = 0;
    
    public static void increment() {
        synchronized (mutex) {
            sharedResource++;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " incremented to " + sharedResource);
        }
    }
    
    public static void main(String[] args) {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    increment();
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
        
        System.out.println("Final value: " + sharedResource);
    }
}
```

## 3.2 Semaphores

Semaphores are counters that control access to a resource pool, allowing a limited number of threads to access the resource simultaneously.

### Key Concepts
- **Counter**: Tracks available resources
- **Acquire/Release**: Threads acquire and release permits
- **Blocking**: Threads block when no permits are available
- **Resource Pool**: Manages access to limited resources

### Real-World Analogy
Think of a parking lot with a limited number of spaces. A semaphore tracks available spaces, and cars must wait when the lot is full.

### Java Example
```java
public class SemaphoreExample {
    private static final Semaphore semaphore = new Semaphore(3); // 3 permits
    private static int resourceCount = 0;
    
    public static void useResource() throws InterruptedException {
        semaphore.acquire(); // Acquire permit
        try {
            resourceCount++;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " using resource, count: " + resourceCount);
            Thread.sleep(1000); // Simulate work
        } finally {
            resourceCount--;
            semaphore.release(); // Release permit
        }
    }
    
    public static void main(String[] args) {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                try {
                    useResource();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
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
    }
}
```

## 3.3 Condition Variables

Condition variables allow threads to wait for specific conditions to be met before proceeding.

### Key Concepts
- **Wait/Notify**: Threads wait for conditions and get notified when conditions change
- **Predicate**: Specific condition that must be met
- **Synchronization**: Must be used with a lock
- **Spurious Wakeups**: Threads may wake up without being notified

### Real-World Analogy
Think of a restaurant where customers wait for a table. They wait until the host notifies them that a table is available.

### Java Example
```java
public class ConditionVariableExample {
    private static final Object lock = new Object();
    private static boolean condition = false;
    
    public static void waitForCondition() throws InterruptedException {
        synchronized (lock) {
            while (!condition) {
                System.out.println("Thread " + Thread.currentThread().getName() + " waiting");
                lock.wait();
            }
            System.out.println("Thread " + Thread.currentThread().getName() + " proceeding");
        }
    }
    
    public static void setCondition() {
        synchronized (lock) {
            condition = true;
            lock.notifyAll();
            System.out.println("Condition set, notifying all threads");
        }
    }
    
    public static void main(String[] args) {
        Thread waiter = new Thread(() -> {
            try {
                waitForCondition();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        waiter.start();
        
        try {
            Thread.sleep(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        setCondition();
        
        try {
            waiter.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 3.4 Barriers and Countdown Latches

Barriers and countdown latches synchronize multiple threads at specific points in their execution.

### Key Concepts
- **Synchronization Point**: All threads must reach the barrier before any can proceed
- **Countdown**: Tracks how many threads have reached the barrier
- **Blocking**: Threads block until the countdown reaches zero
- **One-time Use**: Most barriers can only be used once

### Real-World Analogy
Think of a group of friends meeting at a restaurant. Everyone must arrive before they can be seated together.

### Java Example
```java
public class BarrierExample {
    private static final CountDownLatch latch = new CountDownLatch(3);
    
    public static void worker(String name) {
        System.out.println(name + " starting work");
        try {
            Thread.sleep(1000 + (int)(Math.random() * 1000));
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        System.out.println(name + " finished work, waiting at barrier");
        latch.countDown();
        
        try {
            latch.await();
            System.out.println(name + " passed barrier, continuing");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) {
        Thread[] workers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            final int workerId = i;
            workers[i] = new Thread(() -> worker("Worker" + workerId));
            workers[i].start();
        }
        
        for (Thread worker : workers) {
            try {
                worker.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
```

## 3.5 Read-Write Locks

Read-write locks allow multiple readers or one writer to access a resource, optimizing for read-heavy workloads.

### Key Concepts
- **Multiple Readers**: Multiple threads can read simultaneously
- **Exclusive Writer**: Only one thread can write at a time
- **Reader-Writer Conflict**: Readers and writers cannot access simultaneously
- **Performance**: Better performance for read-heavy workloads

### Real-World Analogy
Think of a library where multiple people can read books simultaneously, but only one person can write in the library's log book at a time.

### Java Example
```java
public class ReadWriteLockExample {
    private static final ReadWriteLock rwLock = new ReentrantReadWriteLock();
    private static final Lock readLock = rwLock.readLock();
    private static final Lock writeLock = rwLock.writeLock();
    private static String data = "Initial data";
    
    public static void readData() {
        readLock.lock();
        try {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " reading: " + data);
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            readLock.unlock();
        }
    }
    
    public static void writeData(String newData) {
        writeLock.lock();
        try {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " writing: " + newData);
            data = newData;
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            writeLock.unlock();
        }
    }
    
    public static void main(String[] args) {
        // Create readers
        Thread[] readers = new Thread[3];
        for (int i = 0; i < 3; i++) {
            readers[i] = new Thread(() -> readData());
            readers[i].start();
        }
        
        // Create writer
        Thread writer = new Thread(() -> writeData("Updated data"));
        writer.start();
        
        // Wait for all threads
        for (Thread reader : readers) {
            try {
                reader.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        try {
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 3.6 Spinlocks

Spinlocks are locks where waiting threads continuously check for the lock to become available instead of blocking.

### Key Concepts
- **Busy Waiting**: Threads continuously check lock status
- **CPU Intensive**: Consumes CPU cycles while waiting
- **Low Latency**: Fast response when lock becomes available
- **Use Case**: Short critical sections, high-performance scenarios

### Real-World Analogy
Think of someone continuously checking if a parking spot is available by driving around the lot instead of waiting in line.

### Java Example
```java
public class SpinlockExample {
    private static final AtomicBoolean lock = new AtomicBoolean(false);
    private static int sharedResource = 0;
    
    public static void acquireLock() {
        while (!lock.compareAndSet(false, true)) {
            // Spin until lock is acquired
            Thread.yield(); // Give other threads a chance
        }
    }
    
    public static void releaseLock() {
        lock.set(false);
    }
    
    public static void increment() {
        acquireLock();
        try {
            sharedResource++;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " incremented to " + sharedResource);
        } finally {
            releaseLock();
        }
    }
    
    public static void main(String[] args) {
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    increment();
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
        
        System.out.println("Final value: " + sharedResource);
    }
}
```

## 3.7 Atomic Operations

Atomic operations are operations that complete in a single step without interference from other threads.

### Key Concepts
- **Indivisible**: Operations cannot be interrupted
- **Thread-Safe**: No synchronization needed
- **Performance**: Generally faster than synchronized blocks
- **Limited Operations**: Only specific operations are atomic

### Real-World Analogy
Think of a vending machine transaction where you either get the item and your money is taken, or nothing happens. There's no in-between state.

### Java Example
```java
public class AtomicOperationsExample {
    private static final AtomicInteger counter = new AtomicInteger(0);
    private static final AtomicBoolean flag = new AtomicBoolean(false);
    private static final AtomicReference<String> data = new AtomicReference<>("Initial");
    
    public static void demonstrateAtomicInteger() {
        System.out.println("=== Atomic Integer Example ===");
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    int newValue = counter.incrementAndGet();
                    System.out.println("Thread " + Thread.currentThread().getName() + 
                                     " incremented to " + newValue);
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
        
        System.out.println("Final counter value: " + counter.get());
    }
    
    public static void demonstrateAtomicBoolean() {
        System.out.println("\n=== Atomic Boolean Example ===");
        
        Thread setter = new Thread(() -> {
            if (flag.compareAndSet(false, true)) {
                System.out.println("Flag set to true");
            } else {
                System.out.println("Failed to set flag");
            }
        });
        
        Thread getter = new Thread(() -> {
            System.out.println("Flag value: " + flag.get());
        });
        
        setter.start();
        getter.start();
        
        try {
            setter.join();
            getter.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void demonstrateAtomicReference() {
        System.out.println("\n=== Atomic Reference Example ===");
        
        Thread[] threads = new Thread[3];
        for (int i = 0; i < 3; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                String newValue = "Thread" + threadId + " data";
                String oldValue = data.getAndSet(newValue);
                System.out.println("Thread " + threadId + " set data to: " + newValue + 
                                 " (was: " + oldValue + ")");
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
        
        System.out.println("Final data value: " + data.get());
    }
    
    public static void main(String[] args) {
        demonstrateAtomicInteger();
        demonstrateAtomicBoolean();
        demonstrateAtomicReference();
    }
}
```

## 3.8 Memory Barriers and Fences

Memory barriers and fences ensure proper ordering of memory operations and visibility of changes across threads.

### Key Concepts
- **Ordering**: Ensures operations are executed in the correct order
- **Visibility**: Ensures changes are visible to other threads
- **Hardware Level**: Low-level synchronization primitives
- **Performance**: Can impact performance due to CPU pipeline stalls

### Real-World Analogy
Think of a traffic light that ensures cars go in the correct order. Without it, cars might try to go simultaneously, causing accidents.

### Java Example
```java
public class MemoryBarrierExample {
    private static volatile boolean flag = false;
    private static int data = 0;
    
    public static void writer() {
        data = 42; // Write data
        flag = true; // Set flag (volatile write acts as memory barrier)
    }
    
    public static void reader() {
        if (flag) { // Read flag (volatile read acts as memory barrier)
            System.out.println("Data: " + data); // Read data
        }
    }
    
    public static void demonstrateMemoryBarrier() {
        System.out.println("=== Memory Barrier Example ===");
        
        Thread writer = new Thread(() -> {
            System.out.println("Writer setting data and flag");
            writer();
        });
        
        Thread reader = new Thread(() -> {
            while (!flag) {
                // Busy wait
            }
            reader();
        });
        
        reader.start();
        writer.start();
        
        try {
            writer.join();
            reader.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) {
        demonstrateMemoryBarrier();
    }
}
```

This comprehensive explanation covers all the synchronization primitives, providing both theoretical understanding and practical Java examples to illustrate each concept. Each subsection builds upon the previous ones, creating a solid foundation for understanding synchronization mechanisms in concurrent programming.