# Section 3 - Synchronization Primitives

## 3.1 Synchronization Fundamentals

Synchronization is the mechanism that ensures only one thread can access a shared resource at a time, preventing race conditions and data corruption in multithreaded applications.

### Why Synchronization is Needed:

#### Race Condition Example:
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
        
        // Expected: 10000, Actual: varies due to race condition
        System.out.println("Counter value: " + counter);
    }
}
```

#### Synchronized Solution:
```java
public class SynchronizedExample {
    private static int counter = 0;
    private static final Object lock = new Object();
    
    public static void main(String[] args) throws InterruptedException {
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        counter++; // Thread-safe
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        // Always prints 10000
        System.out.println("Counter value: " + counter);
    }
}
```

### Synchronization Concepts:

#### 1. **Critical Section**
- Code that accesses shared resources
- Must be executed atomically
- Only one thread at a time

#### 2. **Mutual Exclusion**
- Ensures only one thread in critical section
- Prevents concurrent access
- Maintains data integrity

#### 3. **Atomicity**
- Operations complete entirely or not at all
- No partial execution visible
- All-or-nothing behavior

### Real-World Analogy:
Think of synchronization like a bathroom with a lock:
- **Critical Section**: The bathroom itself
- **Lock**: The door lock mechanism
- **Threads**: People wanting to use the bathroom
- **Mutual Exclusion**: Only one person can use the bathroom at a time
- **Atomicity**: Either you're completely in or completely out

## 3.2 Mutexes and Locks

Mutexes (Mutual Exclusion) and locks are fundamental synchronization primitives that ensure only one thread can access a shared resource at a time.

### Java Synchronized Keyword:

#### Synchronized Methods:
```java
public class SynchronizedMethodExample {
    private int count = 0;
    
    // Synchronized method
    public synchronized void increment() {
        count++;
    }
    
    public synchronized int getCount() {
        return count;
    }
    
    public static void main(String[] args) throws InterruptedException {
        SynchronizedMethodExample example = new SynchronizedMethodExample();
        
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
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
        
        System.out.println("Final count: " + example.getCount()); // Always 5000
    }
}
```

#### Synchronized Blocks:
```java
public class SynchronizedBlockExample {
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
    
    public static void main(String[] args) throws InterruptedException {
        SynchronizedBlockExample example = new SynchronizedBlockExample();
        
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
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
        
        System.out.println("Final count: " + example.getCount()); // Always 5000
    }
}
```

### ReentrantLock:

#### Basic ReentrantLock:
```java
import java.util.concurrent.locks.ReentrantLock;

public class ReentrantLockExample {
    private int count = 0;
    private final ReentrantLock lock = new ReentrantLock();
    
    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }
    
    public int getCount() {
        lock.lock();
        try {
            return count;
        } finally {
            lock.unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ReentrantLockExample example = new ReentrantLockExample();
        
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
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
        
        System.out.println("Final count: " + example.getCount()); // Always 5000
    }
}
```

#### TryLock with Timeout:
```java
import java.util.concurrent.locks.ReentrantLock;
import java.util.concurrent.TimeUnit;

public class TryLockExample {
    private final ReentrantLock lock = new ReentrantLock();
    
    public void doWork() {
        try {
            if (lock.tryLock(1, TimeUnit.SECONDS)) {
                try {
                    System.out.println("Thread " + Thread.currentThread().getName() + 
                                     " acquired lock");
                    Thread.sleep(2000); // Simulate work
                } finally {
                    lock.unlock();
                }
            } else {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " could not acquire lock");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        TryLockExample example = new TryLockExample();
        
        Thread thread1 = new Thread(example::doWork);
        Thread thread2 = new Thread(example::doWork);
        
        thread1.start();
        thread2.start();
        
        thread1.join();
        thread2.join();
    }
}
```

### ReadWriteLock:

#### ReadWriteLock Example:
```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReadWriteLockExample {
    private int value = 0;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    
    public void write(int newValue) {
        lock.writeLock().lock();
        try {
            value = newValue;
            System.out.println("Written: " + newValue);
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    public int read() {
        lock.readLock().lock();
        try {
            System.out.println("Read: " + value);
            return value;
        } finally {
            lock.readLock().unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ReadWriteLockExample example = new ReadWriteLockExample();
        
        // Multiple readers
        Thread[] readers = new Thread[5];
        for (int i = 0; i < 5; i++) {
            readers[i] = new Thread(() -> {
                for (int j = 0; j < 3; j++) {
                    example.read();
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
            readers[i].start();
        }
        
        // One writer
        Thread writer = new Thread(() -> {
            for (int i = 0; i < 3; i++) {
                example.write(i);
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        writer.start();
        
        for (Thread reader : readers) {
            reader.join();
        }
        writer.join();
    }
}
```

## 3.3 Semaphores

Semaphores are synchronization primitives that control access to a resource by maintaining a count of available permits. They can be used to limit the number of threads accessing a resource simultaneously.

### Basic Semaphore:

#### Counting Semaphore:
```java
import java.util.concurrent.Semaphore;

public class SemaphoreExample {
    private final Semaphore semaphore;
    
    public SemaphoreExample(int permits) {
        this.semaphore = new Semaphore(permits);
    }
    
    public void doWork() {
        try {
            semaphore.acquire();
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " acquired permit");
            Thread.sleep(2000); // Simulate work
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            semaphore.release();
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " released permit");
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        // Allow only 2 threads at a time
        SemaphoreExample example = new SemaphoreExample(2);
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(example::doWork);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### Binary Semaphore (Mutex):
```java
import java.util.concurrent.Semaphore;

public class BinarySemaphoreExample {
    private final Semaphore mutex = new Semaphore(1);
    private int sharedResource = 0;
    
    public void increment() {
        try {
            mutex.acquire();
            sharedResource++;
            System.out.println("Incremented to: " + sharedResource);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            mutex.release();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        BinarySemaphoreExample example = new BinarySemaphoreExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
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
        
        System.out.println("Final value: " + example.sharedResource);
    }
}
```

### Semaphore with TryAcquire:

#### Non-blocking Semaphore:
```java
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;

public class TryAcquireSemaphoreExample {
    private final Semaphore semaphore = new Semaphore(2);
    
    public void doWork() {
        try {
            if (semaphore.tryAcquire(1, TimeUnit.SECONDS)) {
                try {
                    System.out.println("Thread " + Thread.currentThread().getName() + 
                                     " acquired permit");
                    Thread.sleep(3000); // Simulate work
                } finally {
                    semaphore.release();
                    System.out.println("Thread " + Thread.currentThread().getName() + 
                                     " released permit");
                }
            } else {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " could not acquire permit");
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        TryAcquireSemaphoreExample example = new TryAcquireSemaphoreExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(example::doWork);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

### Real-World Analogy:
Think of semaphores like parking spaces:
- **Permits**: Number of available parking spaces
- **acquire()**: Taking a parking space
- **release()**: Leaving a parking space
- **tryAcquire()**: Checking if a space is available without waiting
- **Binary Semaphore**: A single parking space (like a driveway)

## 3.4 Condition Variables

Condition variables allow threads to wait for specific conditions to be met before proceeding. They work in conjunction with locks to provide more sophisticated synchronization.

### Java Condition Interface:

#### Basic Condition Usage:
```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ConditionExample {
    private final Lock lock = new ReentrantLock();
    private final Condition condition = lock.newCondition();
    private boolean ready = false;
    
    public void waitForReady() {
        lock.lock();
        try {
            while (!ready) {
                System.out.println("Thread " + Thread.currentThread().getName() + 
                                 " waiting for condition");
                condition.await();
            }
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " condition met, proceeding");
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            lock.unlock();
        }
    }
    
    public void setReady() {
        lock.lock();
        try {
            ready = true;
            System.out.println("Condition set to ready");
            condition.signalAll();
        } finally {
            lock.unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ConditionExample example = new ConditionExample();
        
        // Create waiting threads
        Thread[] waiters = new Thread[3];
        for (int i = 0; i < 3; i++) {
            waiters[i] = new Thread(example::waitForReady);
            waiters[i].start();
        }
        
        // Wait a bit, then signal
        Thread.sleep(2000);
        example.setReady();
        
        for (Thread waiter : waiters) {
            waiter.join();
        }
    }
}
```

#### Producer-Consumer with Condition:
```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;
import java.util.Queue;
import java.util.LinkedList;

public class ProducerConsumerCondition {
    private final Queue<Integer> queue = new LinkedList<>();
    private final int capacity = 5;
    private final Lock lock = new ReentrantLock();
    private final Condition notFull = lock.newCondition();
    private final Condition notEmpty = lock.newCondition();
    
    public void produce(int item) {
        lock.lock();
        try {
            while (queue.size() == capacity) {
                System.out.println("Queue full, producer waiting");
                notFull.await();
            }
            
            queue.offer(item);
            System.out.println("Produced: " + item);
            notEmpty.signal();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            lock.unlock();
        }
    }
    
    public int consume() {
        lock.lock();
        try {
            while (queue.isEmpty()) {
                System.out.println("Queue empty, consumer waiting");
                notEmpty.await();
            }
            
            int item = queue.poll();
            System.out.println("Consumed: " + item);
            notFull.signal();
            return item;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return -1;
        } finally {
            lock.unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ProducerConsumerCondition pc = new ProducerConsumerCondition();
        
        // Producer thread
        Thread producer = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                pc.produce(i);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Consumer thread
        Thread consumer = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                pc.consume();
                try {
                    Thread.sleep(150);
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

## 3.5 Barriers and Countdown Latches

Barriers and countdown latches are synchronization primitives that allow threads to wait for a group of threads to reach a common point before proceeding.

### CountDownLatch:

#### Basic CountDownLatch:
```java
import java.util.concurrent.CountDownLatch;

public class CountDownLatchExample {
    public static void main(String[] args) throws InterruptedException {
        int numberOfWorkers = 5;
        CountDownLatch latch = new CountDownLatch(numberOfWorkers);
        
        // Create worker threads
        for (int i = 0; i < numberOfWorkers; i++) {
            final int workerId = i;
            new Thread(() -> {
                try {
                    System.out.println("Worker " + workerId + " starting work");
                    Thread.sleep(2000 + workerId * 500); // Simulate work
                    System.out.println("Worker " + workerId + " finished work");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    latch.countDown();
                }
            }).start();
        }
        
        // Main thread waits for all workers
        System.out.println("Main thread waiting for all workers to complete");
        latch.await();
        System.out.println("All workers completed, main thread proceeding");
    }
}
```

#### CountDownLatch with Timeout:
```java
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

public class CountDownLatchTimeoutExample {
    public static void main(String[] args) throws InterruptedException {
        CountDownLatch latch = new CountDownLatch(3);
        
        // Create threads
        for (int i = 0; i < 3; i++) {
            final int threadId = i;
            new Thread(() -> {
                try {
                    Thread.sleep(1000 + threadId * 1000);
                    System.out.println("Thread " + threadId + " completed");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    latch.countDown();
                }
            }).start();
        }
        
        // Wait with timeout
        boolean completed = latch.await(5, TimeUnit.SECONDS);
        if (completed) {
            System.out.println("All threads completed within timeout");
        } else {
            System.out.println("Timeout occurred, some threads may not have completed");
        }
    }
}
```

### CyclicBarrier:

#### Basic CyclicBarrier:
```java
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierExample {
    public static void main(String[] args) throws InterruptedException {
        int numberOfThreads = 3;
        CyclicBarrier barrier = new CyclicBarrier(numberOfThreads, () -> {
            System.out.println("All threads reached the barrier, proceeding together");
        });
        
        // Create threads
        for (int i = 0; i < numberOfThreads; i++) {
            final int threadId = i;
            new Thread(() -> {
                try {
                    System.out.println("Thread " + threadId + " working");
                    Thread.sleep(1000 + threadId * 500);
                    System.out.println("Thread " + threadId + " reached barrier");
                    barrier.await();
                    System.out.println("Thread " + threadId + " continuing after barrier");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
}
```

#### CyclicBarrier with Multiple Rounds:
```java
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierRoundsExample {
    public static void main(String[] args) throws InterruptedException {
        int numberOfThreads = 3;
        CyclicBarrier barrier = new CyclicBarrier(numberOfThreads);
        
        // Create threads
        for (int i = 0; i < numberOfThreads; i++) {
            final int threadId = i;
            new Thread(() -> {
                try {
                    for (int round = 0; round < 3; round++) {
                        System.out.println("Thread " + threadId + " round " + round);
                        Thread.sleep(1000);
                        System.out.println("Thread " + threadId + " waiting at barrier");
                        barrier.await();
                        System.out.println("Thread " + threadId + " passed barrier");
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
}
```

### Real-World Analogy:
Think of barriers and latches like different types of group activities:
- **CountDownLatch**: Like waiting for all team members to arrive before starting a meeting
- **CyclicBarrier**: Like a relay race where all runners must reach the exchange zone before the next leg begins
- **Semaphore**: Like a parking lot with limited spaces

## 3.6 Read-Write Locks

Read-write locks allow multiple readers or a single writer to access a resource, providing better performance when reads are more frequent than writes.

### ReentrantReadWriteLock:

#### Basic Read-Write Lock:
```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReadWriteLockExample {
    private int value = 0;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    
    public void write(int newValue) {
        lock.writeLock().lock();
        try {
            System.out.println("Writer " + Thread.currentThread().getName() + 
                             " writing: " + newValue);
            value = newValue;
            Thread.sleep(1000); // Simulate write work
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    public int read() {
        lock.readLock().lock();
        try {
            System.out.println("Reader " + Thread.currentThread().getName() + 
                             " reading: " + value);
            Thread.sleep(500); // Simulate read work
            return value;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return -1;
        } finally {
            lock.readLock().unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ReadWriteLockExample example = new ReadWriteLockExample();
        
        // Create multiple readers
        Thread[] readers = new Thread[5];
        for (int i = 0; i < 5; i++) {
            readers[i] = new Thread(() -> {
                for (int j = 0; j < 3; j++) {
                    example.read();
                }
            });
            readers[i].start();
        }
        
        // Create writers
        Thread[] writers = new Thread[2];
        for (int i = 0; i < 2; i++) {
            final int writerId = i;
            writers[i] = new Thread(() -> {
                for (int j = 0; j < 2; j++) {
                    example.write(writerId * 10 + j);
                }
            });
            writers[i].start();
        }
        
        // Wait for all threads
        for (Thread reader : readers) {
            reader.join();
        }
        for (Thread writer : writers) {
            writer.join();
        }
    }
}
```

#### Read-Write Lock with TryLock:
```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import java.util.concurrent.TimeUnit;

public class ReadWriteLockTryLockExample {
    private int value = 0;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    
    public boolean tryWrite(int newValue) {
        try {
            if (lock.writeLock().tryLock(1, TimeUnit.SECONDS)) {
                try {
                    value = newValue;
                    System.out.println("Writer " + Thread.currentThread().getName() + 
                                     " wrote: " + newValue);
                    return true;
                } finally {
                    lock.writeLock().unlock();
                }
            } else {
                System.out.println("Writer " + Thread.currentThread().getName() + 
                                 " could not acquire write lock");
                return false;
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
    
    public boolean tryRead() {
        try {
            if (lock.readLock().tryLock(1, TimeUnit.SECONDS)) {
                try {
                    System.out.println("Reader " + Thread.currentThread().getName() + 
                                     " read: " + value);
                    return true;
                } finally {
                    lock.readLock().unlock();
                }
            } else {
                System.out.println("Reader " + Thread.currentThread().getName() + 
                                 " could not acquire read lock");
                return false;
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ReadWriteLockTryLockExample example = new ReadWriteLockTryLockExample();
        
        // Create mixed readers and writers
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            final int threadId = i;
            if (i % 3 == 0) {
                // Writer
                threads[i] = new Thread(() -> example.tryWrite(threadId));
            } else {
                // Reader
                threads[i] = new Thread(example::tryRead);
            }
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 3.7 Spinlocks

Spinlocks are synchronization primitives where a thread continuously checks for a condition in a loop instead of blocking. They are useful for short critical sections.

### Java Spinlock Implementation:

#### Basic Spinlock:
```java
import java.util.concurrent.atomic.AtomicBoolean;

public class SpinlockExample {
    private final AtomicBoolean locked = new AtomicBoolean(false);
    
    public void lock() {
        while (!locked.compareAndSet(false, true)) {
            // Spin until lock is acquired
            Thread.yield(); // Hint to scheduler
        }
    }
    
    public void unlock() {
        locked.set(false);
    }
    
    public void doWork() {
        lock();
        try {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " acquired spinlock");
            Thread.sleep(100); // Simulate work
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            unlock();
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " released spinlock");
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        SpinlockExample spinlock = new SpinlockExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(spinlock::doWork);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

#### Spinlock with Backoff:
```java
import java.util.concurrent.atomic.AtomicBoolean;

public class BackoffSpinlockExample {
    private final AtomicBoolean locked = new AtomicBoolean(false);
    
    public void lock() {
        int backoff = 1;
        while (!locked.compareAndSet(false, true)) {
            // Exponential backoff
            for (int i = 0; i < backoff; i++) {
                Thread.yield();
            }
            backoff = Math.min(backoff * 2, 1000);
        }
    }
    
    public void unlock() {
        locked.set(false);
    }
    
    public void doWork() {
        lock();
        try {
            System.out.println("Thread " + Thread.currentThread().getName() + 
                             " acquired backoff spinlock");
            Thread.sleep(50); // Simulate work
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            unlock();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        BackoffSpinlockExample spinlock = new BackoffSpinlockExample();
        
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(spinlock::doWork);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

## 3.8 Atomic Operations

Atomic operations are operations that complete in a single step without interference from other threads. They are the building blocks of lock-free programming.

### Atomic Variables:

#### AtomicInteger:
```java
import java.util.concurrent.atomic.AtomicInteger;

public class AtomicIntegerExample {
    private final AtomicInteger counter = new AtomicInteger(0);
    
    public void increment() {
        counter.incrementAndGet();
    }
    
    public void add(int value) {
        counter.addAndGet(value);
    }
    
    public int get() {
        return counter.get();
    }
    
    public boolean compareAndSet(int expected, int update) {
        return counter.compareAndSet(expected, update);
    }
    
    public static void main(String[] args) throws InterruptedException {
        AtomicIntegerExample example = new AtomicIntegerExample();
        
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
        
        System.out.println("Final counter value: " + example.get()); // Always 10000
    }
}
```

#### AtomicReference:
```java
import java.util.concurrent.atomic.AtomicReference;

public class AtomicReferenceExample {
    private final AtomicReference<String> value = new AtomicReference<>("initial");
    
    public void updateValue(String newValue) {
        String current;
        do {
            current = value.get();
        } while (!value.compareAndSet(current, newValue));
    }
    
    public String getValue() {
        return value.get();
    }
    
    public static void main(String[] args) throws InterruptedException {
        AtomicReferenceExample example = new AtomicReferenceExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    example.updateValue("Thread-" + threadId + "-Value-" + j);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Final value: " + example.getValue());
    }
}
```

#### AtomicArray:
```java
import java.util.concurrent.atomic.AtomicIntegerArray;

public class AtomicArrayExample {
    private final AtomicIntegerArray array = new AtomicIntegerArray(10);
    
    public void increment(int index) {
        array.incrementAndGet(index);
    }
    
    public int get(int index) {
        return array.get(index);
    }
    
    public void set(int index, int value) {
        array.set(index, value);
    }
    
    public static void main(String[] args) throws InterruptedException {
        AtomicArrayExample example = new AtomicArrayExample();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    example.increment(threadId % 10);
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        for (int i = 0; i < 10; i++) {
            System.out.println("Array[" + i + "] = " + example.get(i));
        }
    }
}
```

## 3.9 Memory Barriers

Memory barriers ensure that memory operations are performed in the correct order and are visible to other threads. They are crucial for maintaining consistency in multithreaded programs.

### Java Memory Model:

#### Volatile Keyword:
```java
public class VolatileExample {
    private volatile boolean flag = false;
    private int value = 0;
    
    public void writer() {
        value = 42;
        flag = true; // Volatile write - creates memory barrier
    }
    
    public void reader() {
        if (flag) { // Volatile read - creates memory barrier
            System.out.println("Value: " + value); // Will always see 42
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        VolatileExample example = new VolatileExample();
        
        Thread writer = new Thread(example::writer);
        Thread reader = new Thread(example::reader);
        
        reader.start();
        writer.start();
        
        writer.join();
        reader.join();
    }
}
```

#### Happens-Before Relationship:
```java
public class HappensBeforeExample {
    private int x = 0;
    private int y = 0;
    private volatile boolean ready = false;
    
    public void writer() {
        x = 1;
        y = 2;
        ready = true; // Volatile write
    }
    
    public void reader() {
        if (ready) { // Volatile read
            // Due to happens-before, these will see the correct values
            System.out.println("x = " + x + ", y = " + y);
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        HappensBeforeExample example = new HappensBeforeExample();
        
        Thread writer = new Thread(example::writer);
        Thread reader = new Thread(example::reader);
        
        reader.start();
        writer.start();
        
        writer.join();
        reader.join();
    }
}
```

## 3.10 Synchronization Best Practices

Following best practices ensures efficient, maintainable, and correct synchronization in multithreaded applications.

### Best Practices:

#### 1. **Minimize Lock Scope**
```java
public class LockScopeExample {
    private final Object lock = new Object();
    private int value = 0;
    
    // Bad: Large lock scope
    public void badMethod() {
        synchronized (lock) {
            // Expensive computation
            int result = 0;
            for (int i = 0; i < 1000000; i++) {
                result += i;
            }
            value = result; // Only this line needs synchronization
        }
    }
    
    // Good: Minimal lock scope
    public void goodMethod() {
        int result = 0;
        for (int i = 0; i < 1000000; i++) {
            result += i;
        }
        
        synchronized (lock) {
            value = result; // Only synchronize what's necessary
        }
    }
}
```

#### 2. **Use Appropriate Lock Types**
```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class AppropriateLockExample {
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    private int value = 0;
    
    // Use read lock for read operations
    public int getValue() {
        lock.readLock().lock();
        try {
            return value;
        } finally {
            lock.readLock().unlock();
        }
    }
    
    // Use write lock for write operations
    public void setValue(int newValue) {
        lock.writeLock().lock();
        try {
            value = newValue;
        } finally {
            lock.writeLock().unlock();
        }
    }
}
```

#### 3. **Avoid Nested Locks**
```java
public class NestedLockExample {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    // Bad: Nested locks can cause deadlock
    public void badMethod() {
        synchronized (lock1) {
            synchronized (lock2) {
                // Work
            }
        }
    }
    
    // Good: Always acquire locks in the same order
    public void goodMethod() {
        synchronized (lock1) {
            synchronized (lock2) {
                // Work
            }
        }
    }
}
```

#### 4. **Use Try-Finally for Lock Cleanup**
```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class LockCleanupExample {
    private final Lock lock = new ReentrantLock();
    
    public void methodWithLock() {
        lock.lock();
        try {
            // Critical section
            System.out.println("In critical section");
        } finally {
            lock.unlock(); // Always unlock in finally
        }
    }
}
```

### Real-World Analogy:
Think of synchronization primitives like different types of traffic control:
- **Mutexes/Locks**: Like traffic lights at intersections
- **Semaphores**: Like parking meters limiting spaces
- **Condition Variables**: Like waiting for a specific traffic condition
- **Barriers**: Like waiting for all cars to arrive before starting a race
- **Atomic Operations**: Like automatic doors that open/close instantly
- **Memory Barriers**: Like road signs ensuring proper traffic flow

Each primitive serves a specific purpose in managing the flow of threads, just like different traffic control mechanisms manage the flow of vehicles.