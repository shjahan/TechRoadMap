# Section 4 - Race Conditions and Data Races

## 4.1 Race Condition Fundamentals

Race conditions occur when the behavior of a program depends on the relative timing of events, such as the order in which threads execute. They are one of the most common and dangerous bugs in multithreaded programming.

### What is a Race Condition?

A race condition happens when:
1. Multiple threads access shared data
2. At least one thread modifies the data
3. The timing of access affects the final result
4. No synchronization is used

### Basic Race Condition Example:

```java
public class RaceConditionExample {
    private static int counter = 0;
    
    public static void main(String[] args) throws InterruptedException {
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter++; // Race condition!
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        // Expected: 10000, Actual: varies (e.g., 8765, 9234, etc.)
        System.out.println("Final counter value: " + counter);
    }
}
```

### Why Race Conditions Occur:

#### 1. **Non-Atomic Operations**
The `counter++` operation is not atomic. It involves:
- Reading the current value
- Incrementing it
- Writing it back

#### 2. **Interleaved Execution**
Threads can be interrupted between these steps:
```
Thread 1: Read counter (0) → Increment (1) → [INTERRUPTED]
Thread 2: Read counter (0) → Increment (1) → Write (1)
Thread 1: [RESUMED] → Write (1) // Lost increment!
```

### Real-World Analogy:
Think of a race condition like two people trying to update the same bank account balance:
- **Person A**: Reads balance ($100) → Adds $50 → [Phone rings, gets distracted]
- **Person B**: Reads balance ($100) → Adds $30 → Writes $130
- **Person A**: [Returns] → Writes $150 (overwrites Person B's change)
- **Result**: Lost $30 instead of having $180

## 4.2 Data Race Detection

Data races are a specific type of race condition where two or more threads access the same memory location concurrently, at least one is a write, and there's no synchronization.

### Data Race Characteristics:

#### 1. **Concurrent Access**
- Multiple threads access the same variable
- At least one thread writes to it
- No synchronization mechanism

#### 2. **Unpredictable Results**
- Different outcomes on different runs
- Depends on thread scheduling
- Hard to reproduce consistently

### Data Race Example:

```java
public class DataRaceExample {
    private static int sharedVariable = 0;
    private static boolean flag = false;
    
    public static void main(String[] args) throws InterruptedException {
        Thread writer = new Thread(() -> {
            sharedVariable = 42;
            flag = true;
        });
        
        Thread reader = new Thread(() -> {
            if (flag) {
                // Data race: might not see the updated sharedVariable
                System.out.println("Value: " + sharedVariable);
            }
        });
        
        reader.start();
        writer.start();
        
        writer.join();
        reader.join();
    }
}
```

### Data Race Detection Tools:

#### 1. **Thread Sanitizer (TSan)**
```bash
# Compile with Thread Sanitizer
gcc -fsanitize=thread -g -O1 race_condition.c -o race_condition
./race_condition
```

#### 2. **Java Race Condition Detection**
```java
public class RaceDetectionExample {
    private volatile int counter = 0; // volatile prevents some data races
    
    public void increment() {
        counter++; // Still a race condition for increment operation
    }
    
    public int getCounter() {
        return counter; // Safe read with volatile
    }
    
    public static void main(String[] args) throws InterruptedException {
        RaceDetectionExample example = new RaceDetectionExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter());
    }
}
```

## 4.3 Critical Sections

A critical section is a code segment that accesses shared resources and must not be executed concurrently by multiple threads. Only one thread can be in a critical section at a time.

### Critical Section Properties:

#### 1. **Mutual Exclusion**
- Only one thread in critical section at a time
- Other threads must wait
- Prevents concurrent access

#### 2. **Progress**
- Threads not in critical section don't block others
- No deadlock situations
- Fair access to critical section

#### 3. **Bounded Waiting**
- Threads don't wait indefinitely
- Fair scheduling
- No starvation

### Critical Section Example:

```java
public class CriticalSectionExample {
    private int sharedResource = 0;
    private final Object lock = new Object();
    
    public void criticalSection() {
        synchronized (lock) {
            // Critical section begins
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " entering critical section");
            
            // Access shared resource
            int temp = sharedResource;
            temp++;
            Thread.sleep(100); // Simulate work
            sharedResource = temp;
            
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " leaving critical section, value: " + sharedResource);
            // Critical section ends
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        CriticalSectionExample example = new CriticalSectionExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(example::criticalSection);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Final shared resource value: " + example.sharedResource);
    }
}
```

### Critical Section with Multiple Resources:

```java
public class MultipleResourceCriticalSection {
    private int account1 = 1000;
    private int account2 = 1000;
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    public void transfer(int amount) {
        // Acquire locks in consistent order to prevent deadlock
        Object firstLock = lock1;
        Object secondLock = lock2;
        
        if (System.identityHashCode(lock1) > System.identityHashCode(lock2)) {
            firstLock = lock2;
            secondLock = lock1;
        }
        
        synchronized (firstLock) {
            synchronized (secondLock) {
                // Critical section for both accounts
                if (account1 >= amount) {
                    account1 -= amount;
                    account2 += amount;
                    System.out.println("Transferred " + amount + 
                                     " from account1 to account2");
                }
            }
        }
    }
    
    public void printBalances() {
        synchronized (lock1) {
            synchronized (lock2) {
                System.out.println("Account1: " + account1 + 
                                 ", Account2: " + account2);
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        MultipleResourceCriticalSection bank = new MultipleResourceCriticalSection();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    bank.transfer(10);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        bank.printBalances();
    }
}
```

## 4.4 Mutual Exclusion

Mutual exclusion ensures that only one thread can access a shared resource at a time. It's the fundamental principle behind synchronization mechanisms.

### Mutual Exclusion Methods:

#### 1. **Synchronized Methods**
```java
public class SynchronizedMethodExample {
    private int counter = 0;
    
    public synchronized void increment() {
        counter++;
    }
    
    public synchronized int getCounter() {
        return counter;
    }
    
    public static void main(String[] args) throws InterruptedException {
        SynchronizedMethodExample example = new SynchronizedMethodExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter()); // Always 10000
    }
}
```

#### 2. **Synchronized Blocks**
```java
public class SynchronizedBlockExample {
    private int counter = 0;
    private final Object lock = new Object();
    
    public void increment() {
        synchronized (lock) {
            counter++;
        }
    }
    
    public int getCounter() {
        synchronized (lock) {
            return counter;
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        SynchronizedBlockExample example = new SynchronizedBlockExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter()); // Always 10000
    }
}
```

#### 3. **ReentrantLock**
```java
import java.util.concurrent.locks.ReentrantLock;

public class ReentrantLockExample {
    private int counter = 0;
    private final ReentrantLock lock = new ReentrantLock();
    
    public void increment() {
        lock.lock();
        try {
            counter++;
        } finally {
            lock.unlock();
        }
    }
    
    public int getCounter() {
        lock.lock();
        try {
            return counter;
        } finally {
            lock.unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ReentrantLockExample example = new ReentrantLockExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Counter: " + example.getCounter()); // Always 10000
    }
}
```

## 4.5 Deadlock Prevention

Deadlock occurs when two or more threads are blocked forever, waiting for each other to release resources. It's one of the most serious problems in multithreaded programming.

### Deadlock Conditions (Coffman Conditions):

#### 1. **Mutual Exclusion**
- Resources cannot be shared
- Only one thread can hold a resource

#### 2. **Hold and Wait**
- Thread holds one resource while waiting for another
- Doesn't release held resources

#### 3. **No Preemption**
- Resources cannot be forcibly taken away
- Must be voluntarily released

#### 4. **Circular Wait**
- Threads form a circular chain
- Each waits for the next in the chain

### Deadlock Example:

```java
public class DeadlockExample {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    public void method1() {
        synchronized (lock1) {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " acquired lock1");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            synchronized (lock2) {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " acquired lock2");
            }
        }
    }
    
    public void method2() {
        synchronized (lock2) {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " acquired lock2");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            synchronized (lock1) {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " acquired lock1");
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        DeadlockExample example = new DeadlockExample();
        
        Thread thread1 = new Thread(example::method1);
        Thread thread2 = new Thread(example::method2);
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
}
```

### Deadlock Prevention Strategies:

#### 1. **Lock Ordering**
```java
public class LockOrderingExample {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    public void method1() {
        // Always acquire locks in the same order
        synchronized (lock1) {
            synchronized (lock2) {
                System.out.println("Method1 executing");
            }
        }
    }
    
    public void method2() {
        // Same order as method1
        synchronized (lock1) {
            synchronized (lock2) {
                System.out.println("Method2 executing");
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        LockOrderingExample example = new LockOrderingExample();
        
        Thread thread1 = new Thread(example::method1);
        Thread thread2 = new Thread(example::method2);
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
}
```

#### 2. **TryLock with Timeout**
```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.TimeUnit;

public class TryLockExample {
    private final Lock lock1 = new ReentrantLock();
    private final Lock lock2 = new ReentrantLock();
    
    public void method1() {
        if (lock1.tryLock()) {
            try {
                if (lock2.tryLock(1, TimeUnit.SECONDS)) {
                    try {
                        System.out.println("Method1 executing");
                    } finally {
                        lock2.unlock();
                    }
                } else {
                    System.out.println("Method1 could not acquire lock2");
                }
            } finally {
                lock1.unlock();
            }
        } else {
            System.out.println("Method1 could not acquire lock1");
        }
    }
    
    public void method2() {
        if (lock2.tryLock()) {
            try {
                if (lock1.tryLock(1, TimeUnit.SECONDS)) {
                    try {
                        System.out.println("Method2 executing");
                    } finally {
                        lock1.unlock();
                    }
                } else {
                    System.out.println("Method2 could not acquire lock1");
                }
            } finally {
                lock2.unlock();
            }
        } else {
            System.out.println("Method2 could not acquire lock2");
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        TryLockExample example = new TryLockExample();
        
        Thread thread1 = new Thread(example::method1);
        Thread thread2 = new Thread(example::method2);
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
}
```

## 4.6 Livelock Prevention

Livelock occurs when threads are not blocked but are unable to make progress because they keep responding to each other's actions. It's like a polite version of deadlock.

### Livelock Example:

```java
public class LivelockExample {
    private boolean flag1 = false;
    private boolean flag2 = false;
    
    public void method1() {
        while (flag2) {
            System.out.println("Thread1 waiting for flag2 to be false");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        
        flag1 = true;
        System.out.println("Thread1 set flag1 to true");
        
        // Simulate work
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        flag1 = false;
        System.out.println("Thread1 set flag1 to false");
    }
    
    public void method2() {
        while (flag1) {
            System.out.println("Thread2 waiting for flag1 to be false");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        
        flag2 = true;
        System.out.println("Thread2 set flag2 to true");
        
        // Simulate work
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        flag2 = false;
        System.out.println("Thread2 set flag2 to false");
    }
    
    public static void main(String[] args) throws InterruptedException {
        LivelockExample example = new LivelockExample();
        
        Thread thread1 = new Thread(example::method1);
        Thread thread2 = new Thread(example::method2);
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
}
```

### Livelock Prevention:

#### 1. **Random Backoff**
```java
import java.util.Random;

public class LivelockPreventionExample {
    private boolean flag1 = false;
    private boolean flag2 = false;
    private final Random random = new Random();
    
    public void method1() {
        int backoff = 100;
        while (flag2) {
            System.out.println("Thread1 waiting for flag2");
            try {
                Thread.sleep(backoff + random.nextInt(100));
                backoff = Math.min(backoff * 2, 1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        
        flag1 = true;
        System.out.println("Thread1 set flag1 to true");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        flag1 = false;
        System.out.println("Thread1 set flag1 to false");
    }
    
    public void method2() {
        int backoff = 100;
        while (flag1) {
            System.out.println("Thread2 waiting for flag1");
            try {
                Thread.sleep(backoff + random.nextInt(100));
                backoff = Math.min(backoff * 2, 1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        
        flag2 = true;
        System.out.println("Thread2 set flag2 to true");
        
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        flag2 = false;
        System.out.println("Thread2 set flag2 to false");
    }
    
    public static void main(String[] args) throws InterruptedException {
        LivelockPreventionExample example = new LivelockPreventionExample();
        
        Thread thread1 = new Thread(example::method1);
        Thread thread2 = new Thread(example::method2);
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
}
```

## 4.7 Starvation Prevention

Starvation occurs when a thread is unable to gain regular access to shared resources and is unable to make progress. It's often caused by unfair scheduling or resource allocation.

### Starvation Example:

```java
public class StarvationExample {
    private final Object lock = new Object();
    private int counter = 0;
    
    public void method() {
        synchronized (lock) {
            counter++;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " counter: " + counter);
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        StarvationExample example = new StarvationExample();
        
        // Create high-priority threads
        Thread[] highPriorityThreads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            highPriorityThreads[i] = new Thread(example::method);
            highPriorityThreads[i].setPriority(Thread.MAX_PRIORITY);
            highPriorityThreads[i].start();
        }
        
        // Create low-priority thread
        Thread lowPriorityThread = new Thread(example::method);
        lowPriorityThread.setPriority(Thread.MIN_PRIORITY);
        lowPriorityThread.start();
        
        for (Thread thread : highPriorityThreads) {
            thread.join();
        }
        lowPriorityThread.join();
    }
}
```

### Starvation Prevention:

#### 1. **Fair Locking**
```java
import java.util.concurrent.locks.ReentrantLock;

public class FairLockingExample {
    private final ReentrantLock lock = new ReentrantLock(true); // Fair lock
    private int counter = 0;
    
    public void method() {
        lock.lock();
        try {
            counter++;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " counter: " + counter);
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        } finally {
            lock.unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        FairLockingExample example = new FairLockingExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(example::method);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 2. **Semaphore with Fairness**
```java
import java.util.concurrent.Semaphore;

public class FairSemaphoreExample {
    private final Semaphore semaphore = new Semaphore(1, true); // Fair semaphore
    private int counter = 0;
    
    public void method() {
        try {
            semaphore.acquire();
            counter++;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " counter: " + counter);
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            semaphore.release();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        FairSemaphoreExample example = new FairSemaphoreExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(example::method);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 4.8 Race Condition Debugging

Debugging race conditions is challenging because they are often non-deterministic and hard to reproduce. Here are some strategies and tools to help.

### Debugging Strategies:

#### 1. **Logging and Tracing**
```java
import java.util.concurrent.atomic.AtomicLong;

public class RaceConditionDebugging {
    private int counter = 0;
    private final Object lock = new Object();
    private final AtomicLong operationCount = new AtomicLong(0);
    
    public void increment() {
        long opId = operationCount.incrementAndGet();
        System.out.println("Thread " + Thread.currentThread().getName() + 
                         " starting increment " + opId);
        
        synchronized (lock) {
            int oldValue = counter;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " read value " + oldValue + " in increment " + opId);
            
            try {
                Thread.sleep(10); // Simulate work
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            counter = oldValue + 1;
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " wrote value " + counter + " in increment " + opId);
        }
    }
    
    public int getCounter() {
        return counter;
    }
    
    public static void main(String[] args) throws InterruptedException {
        RaceConditionDebugging example = new RaceConditionDebugging();
        
        Thread[] threads = new Thread[3];
        for (int i = 0; i < 3; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 5; j++) {
                    example.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Final counter: " + example.getCounter());
    }
}
```

#### 2. **Thread Dump Analysis**
```java
public class ThreadDumpExample {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    public void method1() {
        synchronized (lock1) {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " acquired lock1");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            synchronized (lock2) {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " acquired lock2");
            }
        }
    }
    
    public void method2() {
        synchronized (lock2) {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " acquired lock2");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            synchronized (lock1) {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " acquired lock1");
            }
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadDumpExample example = new ThreadDumpExample();
        
        Thread thread1 = new Thread(example::method1);
        Thread thread2 = new Thread(example::method2);
        
        thread1.start();
        thread2.start();
        
        // Let them run for a bit, then take a thread dump
        Thread.sleep(1000);
        
        // Print thread states
        System.out.println("Thread1 state: " + thread1.getState());
        System.out.println("Thread2 state: " + thread2.getState());
        
        thread1.join();
        thread2.join();
    }
}
```

### Debugging Tools:

#### 1. **JConsole**
```bash
# Start JConsole
jconsole
```

#### 2. **VisualVM**
```bash
# Start VisualVM
jvisualvm
```

#### 3. **Thread Dump**
```bash
# Get thread dump
jstack <pid>
```

## 4.9 Race Condition Testing

Testing race conditions requires special techniques because they are non-deterministic. Here are some strategies for testing multithreaded code.

### Testing Strategies:

#### 1. **Stress Testing**
```java
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class RaceConditionStressTest {
    private int counter = 0;
    private final Object lock = new Object();
    
    public void increment() {
        synchronized (lock) {
            counter++;
        }
    }
    
    public int getCounter() {
        synchronized (lock) {
            return counter;
        }
    }
    
    public void stressTest(int numberOfThreads, int operationsPerThread) 
            throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(numberOfThreads);
        CountDownLatch latch = new CountDownLatch(numberOfThreads);
        
        for (int i = 0; i < numberOfThreads; i++) {
            executor.submit(() -> {
                try {
                    for (int j = 0; j < operationsPerThread; j++) {
                        increment();
                    }
                } finally {
                    latch.countDown();
                }
            });
        }
        
        latch.await();
        executor.shutdown();
        
        int expected = numberOfThreads * operationsPerThread;
        int actual = getCounter();
        
        System.out.println("Expected: " + expected + ", Actual: " + actual + 
                         ", Test " + (expected == actual ? "PASSED" : "FAILED"));
    }
    
    public static void main(String[] args) throws InterruptedException {
        RaceConditionStressTest test = new RaceConditionStressTest();
        
        // Test with different configurations
        test.stressTest(10, 1000);
        test.stressTest(100, 100);
        test.stressTest(1000, 10);
    }
}
```

#### 2. **Property-Based Testing**
```java
import java.util.concurrent.atomic.AtomicInteger;

public class PropertyBasedTesting {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    public void increment() {
        counter.incrementAndGet();
    }
    
    public int getCounter() {
        return counter.get();
    }
    
    public void propertyTest(int numberOfThreads, int operationsPerThread) 
            throws InterruptedException {
        Thread[] threads = new Thread[numberOfThreads];
        
        for (int i = 0; i < numberOfThreads; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < operationsPerThread; j++) {
                    increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        // Properties to verify
        int expected = numberOfThreads * operationsPerThread;
        int actual = getCounter();
        
        // Property 1: Counter should equal expected value
        assert actual == expected : "Counter mismatch: expected " + expected + 
                                  ", got " + actual;
        
        // Property 2: Counter should be non-negative
        assert actual >= 0 : "Counter should be non-negative";
        
        // Property 3: Counter should be monotonically increasing
        // (This is harder to test in a single run)
        
        System.out.println("Property test PASSED for " + numberOfThreads + 
                         " threads, " + operationsPerThread + " operations each");
    }
    
    public static void main(String[] args) throws InterruptedException {
        PropertyBasedTesting test = new PropertyBasedTesting();
        
        // Run multiple test cases
        for (int threads = 1; threads <= 10; threads++) {
            for (int ops = 100; ops <= 1000; ops += 100) {
                test.propertyTest(threads, ops);
            }
        }
    }
}
```

## 4.10 Race Condition Best Practices

Following best practices helps prevent race conditions and makes multithreaded code more robust and maintainable.

### Best Practices:

#### 1. **Use Thread-Safe Collections**
```java
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

public class ThreadSafeCollectionsExample {
    // Good: Thread-safe collections
    private final Map<String, Integer> concurrentMap = new ConcurrentHashMap<>();
    private final List<String> copyOnWriteList = new CopyOnWriteArrayList<>();
    private final List<String> synchronizedList = Collections.synchronizedList(new ArrayList<>());
    
    public void addToMap(String key, Integer value) {
        concurrentMap.put(key, value);
    }
    
    public void addToList(String item) {
        copyOnWriteList.add(item);
    }
    
    public void addToSynchronizedList(String item) {
        synchronizedList.add(item);
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadSafeCollectionsExample example = new ThreadSafeCollectionsExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    example.addToMap("key" + threadId + "-" + j, threadId * 100 + j);
                    example.addToList("item" + threadId + "-" + j);
                    example.addToSynchronizedList("sync" + threadId + "-" + j);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Map size: " + example.concurrentMap.size());
        System.out.println("List size: " + example.copyOnWriteList.size());
        System.out.println("Synchronized list size: " + example.synchronizedList.size());
    }
}
```

#### 2. **Minimize Shared State**
```java
public class MinimizeSharedStateExample {
    // Bad: Shared mutable state
    private static int globalCounter = 0;
    
    // Good: Thread-local state
    private static final ThreadLocal<Integer> threadLocalCounter = new ThreadLocal<Integer>() {
        @Override
        protected Integer initialValue() {
            return 0;
        }
    };
    
    public void incrementThreadLocal() {
        int current = threadLocalCounter.get();
        threadLocalCounter.set(current + 1);
    }
    
    public int getThreadLocalValue() {
        return threadLocalCounter.get();
    }
    
    public static void main(String[] args) throws InterruptedException {
        MinimizeSharedStateExample example = new MinimizeSharedStateExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.incrementThreadLocal();
                }
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " final value: " + example.getThreadLocalValue());
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### 3. **Use Immutable Objects**
```java
import java.util.Collections;
import java.util.List;

public class ImmutableObjectsExample {
    // Immutable class
    public static final class ImmutablePoint {
        private final int x;
        private final int y;
        
        public ImmutablePoint(int x, int y) {
            this.x = x;
            this.y = y;
        }
        
        public int getX() { return x; }
        public int getY() { return y; }
        
        public ImmutablePoint move(int dx, int dy) {
            return new ImmutablePoint(x + dx, y + dy);
        }
        
        @Override
        public String toString() {
            return "(" + x + ", " + y + ")";
        }
    }
    
    // Immutable collection
    private final List<ImmutablePoint> points;
    
    public ImmutableObjectsExample(List<ImmutablePoint> points) {
        this.points = Collections.unmodifiableList(points);
    }
    
    public List<ImmutablePoint> getPoints() {
        return points; // Safe to return - unmodifiable
    }
    
    public static void main(String[] args) {
        ImmutablePoint p1 = new ImmutablePoint(1, 2);
        ImmutablePoint p2 = new ImmutablePoint(3, 4);
        
        List<ImmutablePoint> pointList = List.of(p1, p2);
        ImmutableObjectsExample example = new ImmutableObjectsExample(pointList);
        
        // Safe to access from multiple threads
        System.out.println("Points: " + example.getPoints());
    }
}
```

### Real-World Analogy:
Think of race conditions like traffic at a busy intersection:
- **Race Condition**: Like two cars trying to go through the same space at the same time
- **Critical Section**: Like the intersection itself - only one car can be there at a time
- **Mutual Exclusion**: Like traffic lights ensuring only one direction goes at a time
- **Deadlock**: Like four cars all waiting for each other to move
- **Livelock**: Like two polite drivers both trying to let the other go first
- **Starvation**: Like one car never getting a chance to go because others keep cutting in

The key is to have proper traffic control (synchronization) to ensure smooth and safe flow of traffic (threads).