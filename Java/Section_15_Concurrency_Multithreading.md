# Section 15 - Concurrency & Multithreading

## 15.1 Thread Fundamentals

Thread Fundamentals یکی از مهم‌ترین مفاهیم Java است که امکان اجرای همزمان چندین task را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Thread Creation:**
- Extending Thread class
- Implementing Runnable interface
- Using ExecutorService
- Using CompletableFuture

**2. Thread Lifecycle:**
- NEW
- RUNNABLE
- BLOCKED
- WAITING
- TIMED_WAITING
- TERMINATED

**3. Thread Safety:**
- Synchronization
- Volatile variables
- Atomic classes
- Immutable objects

### مثال عملی:

```java
public class ThreadFundamentalsExample {
    public static void main(String[] args) {
        System.out.println("=== Thread Fundamentals Example ===");
        
        // 1. Extending Thread class
        MyThread thread1 = new MyThread("Thread-1");
        thread1.start();
        
        // 2. Implementing Runnable interface
        Thread thread2 = new Thread(new MyRunnable("Thread-2"));
        thread2.start();
        
        // 3. Using lambda expression
        Thread thread3 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Lambda Thread: " + i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        thread3.start();
        
        // 4. Using ExecutorService
        ExecutorService executor = Executors.newFixedThreadPool(3);
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Executor Task " + taskId + " running on: " + 
                    Thread.currentThread().getName());
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        
        // 5. Thread states demonstration
        demonstrateThreadStates();
    }
    
    public static void demonstrateThreadStates() {
        System.out.println("\n=== Thread States ===");
        
        Thread thread = new Thread(() -> {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        System.out.println("Before start: " + thread.getState()); // NEW
        thread.start();
        System.out.println("After start: " + thread.getState()); // RUNNABLE
        
        try {
            Thread.sleep(1000);
            System.out.println("During sleep: " + thread.getState()); // TIMED_WAITING
            thread.join();
            System.out.println("After join: " + thread.getState()); // TERMINATED
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}

class MyThread extends Thread {
    private String threadName;
    
    public MyThread(String name) {
        this.threadName = name;
    }
    
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(threadName + ": " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}

class MyRunnable implements Runnable {
    private String threadName;
    
    public MyRunnable(String name) {
        this.threadName = name;
    }
    
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(threadName + ": " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}
```

### آنالوژی دنیای واقعی:
Threads مانند کارگران مختلف در یک کارخانه هستند که:
- **Each Thread:** مانند هر کارگر که وظیفه خاصی دارد
- **Thread Lifecycle:** مانند مراحل مختلف زندگی کارگر (استخدام، کار، استراحت، بازنشستگی)
- **Thread Safety:** مانند قوانین کارخانه که از تداخل کارگران جلوگیری می‌کند

## 15.2 Synchronization & Locks

Synchronization & Locks ابزارهای مهمی برای اطمینان از thread safety در Java هستند.

### مفاهیم کلیدی:

**1. Synchronization:**
- Synchronized methods
- Synchronized blocks
- Intrinsic locks
- Monitor concept

**2. Lock Interface:**
- ReentrantLock
- ReadWriteLock
- StampedLock
- Lock-free programming

**3. Thread Safety Patterns:**
- Double-checked locking
- Thread-local storage
- Immutable objects
- Atomic operations

### مثال عملی:

```java
import java.util.concurrent.locks.*;

public class SynchronizationLocksExample {
    private static int counter = 0;
    private static final Object lock = new Object();
    private static final ReentrantLock reentrantLock = new ReentrantLock();
    private static final ReadWriteLock readWriteLock = new ReentrantReadWriteLock();
    
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Synchronization & Locks Example ===");
        
        // 1. Synchronized methods
        demonstrateSynchronizedMethods();
        
        // 2. Synchronized blocks
        demonstrateSynchronizedBlocks();
        
        // 3. ReentrantLock
        demonstrateReentrantLock();
        
        // 4. ReadWriteLock
        demonstrateReadWriteLock();
        
        // 5. Thread safety issues
        demonstrateThreadSafetyIssues();
    }
    
    public static void demonstrateSynchronizedMethods() throws InterruptedException {
        System.out.println("\n=== Synchronized Methods ===");
        
        counter = 0;
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    incrementSynchronized();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Final counter value: " + counter);
    }
    
    public static synchronized void incrementSynchronized() {
        counter++;
    }
    
    public static void demonstrateSynchronizedBlocks() throws InterruptedException {
        System.out.println("\n=== Synchronized Blocks ===");
        
        counter = 0;
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        counter++;
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Final counter value: " + counter);
    }
    
    public static void demonstrateReentrantLock() throws InterruptedException {
        System.out.println("\n=== ReentrantLock ===");
        
        counter = 0;
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    reentrantLock.lock();
                    try {
                        counter++;
                    } finally {
                        reentrantLock.unlock();
                    }
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Final counter value: " + counter);
    }
    
    public static void demonstrateReadWriteLock() throws InterruptedException {
        System.out.println("\n=== ReadWriteLock ===");
        
        counter = 0;
        Thread[] readers = new Thread[5];
        Thread[] writers = new Thread[5];
        
        // Create reader threads
        for (int i = 0; i < 5; i++) {
            readers[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    readWriteLock.readLock().lock();
                    try {
                        int value = counter; // Read operation
                    } finally {
                        readWriteLock.readLock().unlock();
                    }
                }
            });
        }
        
        // Create writer threads
        for (int i = 0; i < 5; i++) {
            writers[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    readWriteLock.writeLock().lock();
                    try {
                        counter++; // Write operation
                    } finally {
                        readWriteLock.writeLock().unlock();
                    }
                }
            });
        }
        
        // Start all threads
        for (Thread thread : readers) {
            thread.start();
        }
        for (Thread thread : writers) {
            thread.start();
        }
        
        // Wait for completion
        for (Thread thread : readers) {
            thread.join();
        }
        for (Thread thread : writers) {
            thread.join();
        }
        
        System.out.println("Final counter value: " + counter);
    }
    
    public static void demonstrateThreadSafetyIssues() throws InterruptedException {
        System.out.println("\n=== Thread Safety Issues ===");
        
        // Unsafe counter
        UnsafeCounter unsafeCounter = new UnsafeCounter();
        Thread[] threads = new Thread[10];
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    unsafeCounter.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Unsafe counter value: " + unsafeCounter.getValue());
        
        // Safe counter
        SafeCounter safeCounter = new SafeCounter();
        
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    safeCounter.increment();
                }
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        System.out.println("Safe counter value: " + safeCounter.getValue());
    }
}

class UnsafeCounter {
    private int value = 0;
    
    public void increment() {
        value++; // Not thread-safe
    }
    
    public int getValue() {
        return value;
    }
}

class SafeCounter {
    private int value = 0;
    private final Object lock = new Object();
    
    public void increment() {
        synchronized (lock) {
            value++; // Thread-safe
        }
    }
    
    public int getValue() {
        synchronized (lock) {
            return value;
        }
    }
}
```

### آنالوژی دنیای واقعی:
Synchronization & Locks مانند داشتن یک سیستم کنترل ترافیک هوشمند است که:
- **Synchronized Methods:** مانند قوانین راهنمایی که همه باید رعایت کنند
- **Locks:** مانند چراغ‌های راهنمایی که عبور را کنترل می‌کنند
- **Thread Safety:** مانند اطمینان از اینکه هیچ تصادفی رخ ندهد

## 15.3 Executor Framework

Executor Framework مجموعه‌ای از interfaces و classes است که مدیریت threads را ساده‌تر می‌کند.

### مفاهیم کلیدی:

**1. Executor Interface:**
- Simple task execution
- Decoupling task submission from execution
- Thread pool management

**2. ExecutorService:**
- Lifecycle management
- Task submission methods
- Shutdown methods
- Future handling

**3. Thread Pools:**
- FixedThreadPool
- CachedThreadPool
- SingleThreadExecutor
- ScheduledThreadPool

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ExecutorFrameworkExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Executor Framework Example ===");
        
        // 1. Basic ExecutorService
        demonstrateBasicExecutorService();
        
        // 2. Different thread pools
        demonstrateThreadPools();
        
        // 3. Future and Callable
        demonstrateFutureAndCallable();
        
        // 4. ScheduledExecutorService
        demonstrateScheduledExecutorService();
        
        // 5. Custom ThreadPoolExecutor
        demonstrateCustomThreadPoolExecutor();
    }
    
    public static void demonstrateBasicExecutorService() throws InterruptedException {
        System.out.println("\n=== Basic ExecutorService ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " executed by " + 
                    Thread.currentThread().getName());
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    public static void demonstrateThreadPools() throws InterruptedException {
        System.out.println("\n=== Different Thread Pools ===");
        
        // Fixed thread pool
        System.out.println("Fixed Thread Pool:");
        ExecutorService fixedPool = Executors.newFixedThreadPool(2);
        submitTasks(fixedPool, "Fixed");
        fixedPool.shutdown();
        fixedPool.awaitTermination(5, TimeUnit.SECONDS);
        
        // Cached thread pool
        System.out.println("\nCached Thread Pool:");
        ExecutorService cachedPool = Executors.newCachedThreadPool();
        submitTasks(cachedPool, "Cached");
        cachedPool.shutdown();
        cachedPool.awaitTermination(5, TimeUnit.SECONDS);
        
        // Single thread executor
        System.out.println("\nSingle Thread Executor:");
        ExecutorService singlePool = Executors.newSingleThreadExecutor();
        submitTasks(singlePool, "Single");
        singlePool.shutdown();
        singlePool.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    public static void submitTasks(ExecutorService executor, String poolName) {
        for (int i = 0; i < 3; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println(poolName + " Task " + taskId + " by " + 
                    Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
    }
    
    public static void demonstrateFutureAndCallable() throws InterruptedException, ExecutionException {
        System.out.println("\n=== Future and Callable ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Submit Callable tasks
        Future<Integer> future1 = executor.submit(new MyCallable("Task 1", 2000));
        Future<Integer> future2 = executor.submit(new MyCallable("Task 2", 3000));
        Future<Integer> future3 = executor.submit(new MyCallable("Task 3", 1000));
        
        // Get results
        try {
            System.out.println("Result 1: " + future1.get());
            System.out.println("Result 2: " + future2.get());
            System.out.println("Result 3: " + future3.get());
        } catch (ExecutionException e) {
            System.err.println("Task failed: " + e.getCause());
        }
        
        executor.shutdown();
    }
    
    public static void demonstrateScheduledExecutorService() throws InterruptedException {
        System.out.println("\n=== ScheduledExecutorService ===");
        
        ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
        
        // Schedule task to run after delay
        scheduler.schedule(() -> {
            System.out.println("Delayed task executed");
        }, 2, TimeUnit.SECONDS);
        
        // Schedule task to run periodically
        scheduler.scheduleAtFixedRate(() -> {
            System.out.println("Periodic task executed at " + System.currentTimeMillis());
        }, 0, 1, TimeUnit.SECONDS);
        
        // Schedule task to run with fixed delay
        scheduler.scheduleWithFixedDelay(() -> {
            System.out.println("Fixed delay task executed");
        }, 0, 2, TimeUnit.SECONDS);
        
        // Let it run for 10 seconds
        Thread.sleep(10000);
        scheduler.shutdown();
    }
    
    public static void demonstrateCustomThreadPoolExecutor() throws InterruptedException {
        System.out.println("\n=== Custom ThreadPoolExecutor ===");
        
        ThreadPoolExecutor customExecutor = new ThreadPoolExecutor(
            2, // core pool size
            5, // maximum pool size
            60L, // keep alive time
            TimeUnit.SECONDS, // time unit
            new LinkedBlockingQueue<>(10), // work queue
            new ThreadFactory() {
                private final AtomicInteger threadNumber = new AtomicInteger(1);
                @Override
                public Thread newThread(Runnable r) {
                    Thread t = new Thread(r, "CustomThread-" + threadNumber.getAndIncrement());
                    t.setDaemon(false);
                    return t;
                }
            },
            new ThreadPoolExecutor.CallerRunsPolicy() // rejection policy
        );
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            customExecutor.submit(() -> {
                System.out.println("Custom task " + taskId + " executed by " + 
                    Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        customExecutor.shutdown();
        customExecutor.awaitTermination(10, TimeUnit.SECONDS);
    }
}

class MyCallable implements Callable<Integer> {
    private String taskName;
    private int delay;
    
    public MyCallable(String taskName, int delay) {
        this.taskName = taskName;
        this.delay = delay;
    }
    
    @Override
    public Integer call() throws Exception {
        System.out.println(taskName + " started");
        Thread.sleep(delay);
        System.out.println(taskName + " completed");
        return delay;
    }
}
```

### آنالوژی دنیای واقعی:
Executor Framework مانند داشتن یک سیستم مدیریت کارگران هوشمند است که:
- **ExecutorService:** مانند مدیر کارخانه که کارگران را مدیریت می‌کند
- **Thread Pools:** مانند گروه‌های مختلف کارگران با تخصص‌های مختلف
- **Future:** مانند سیستم پیگیری پیشرفت کارها

## 15.4 Concurrent Collections

Concurrent Collections مجموعه‌ای از thread-safe collections هستند که برای برنامه‌نویسی concurrent طراحی شده‌اند.

### مفاهیم کلیدی:

**1. Thread-Safe Collections:**
- ConcurrentHashMap
- ConcurrentLinkedQueue
- CopyOnWriteArrayList
- BlockingQueue implementations

**2. Performance Benefits:**
- Lock-free algorithms
- Better concurrency
- Reduced contention
- Optimized for multi-threading

**3. Use Cases:**
- Producer-Consumer patterns
- Caching
- Event handling
- Data processing

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ConcurrentCollectionsExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Concurrent Collections Example ===");
        
        // 1. ConcurrentHashMap
        demonstrateConcurrentHashMap();
        
        // 2. ConcurrentLinkedQueue
        demonstrateConcurrentLinkedQueue();
        
        // 3. CopyOnWriteArrayList
        demonstrateCopyOnWriteArrayList();
        
        // 4. BlockingQueue
        demonstrateBlockingQueue();
        
        // 5. Producer-Consumer pattern
        demonstrateProducerConsumer();
    }
    
    public static void demonstrateConcurrentHashMap() throws InterruptedException {
        System.out.println("\n=== ConcurrentHashMap ===");
        
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        ExecutorService executor = Executors.newFixedThreadPool(10);
        
        // Multiple threads adding to map
        for (int i = 0; i < 10; i++) {
            final int value = i;
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    map.put("key" + value + "_" + j, value * 1000 + j);
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        
        System.out.println("Map size: " + map.size());
        System.out.println("Sample values: " + map.entrySet().stream().limit(5).toList());
    }
    
    public static void demonstrateConcurrentLinkedQueue() throws InterruptedException {
        System.out.println("\n=== ConcurrentLinkedQueue ===");
        
        ConcurrentLinkedQueue<String> queue = new ConcurrentLinkedQueue<>();
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        // Producer threads
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    queue.offer("Producer" + producerId + "_Item" + j);
                }
            });
        }
        
        // Consumer threads
        for (int i = 0; i < 2; i++) {
            final int consumerId = i;
            executor.submit(() -> {
                while (!queue.isEmpty()) {
                    String item = queue.poll();
                    if (item != null) {
                        System.out.println("Consumer" + consumerId + " processed: " + item);
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    public static void demonstrateCopyOnWriteArrayList() throws InterruptedException {
        System.out.println("\n=== CopyOnWriteArrayList ===");
        
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        // Writer threads
        for (int i = 0; i < 3; i++) {
            final int writerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 100; j++) {
                    list.add("Writer" + writerId + "_Item" + j);
                }
            });
        }
        
        // Reader threads
        for (int i = 0; i < 2; i++) {
            final int readerId = i;
            executor.submit(() -> {
                for (int j = 0; j < 1000; j++) {
                    if (!list.isEmpty()) {
                        String item = list.get(0);
                        System.out.println("Reader" + readerId + " read: " + item);
                    }
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
        System.out.println("Final list size: " + list.size());
    }
    
    public static void demonstrateBlockingQueue() throws InterruptedException {
        System.out.println("\n=== BlockingQueue ===");
        
        BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Producer
        executor.submit(() -> {
            for (int i = 0; i < 20; i++) {
                try {
                    queue.put("Item" + i);
                    System.out.println("Produced: Item" + i);
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        // Consumer
        executor.submit(() -> {
            for (int i = 0; i < 20; i++) {
                try {
                    String item = queue.take();
                    System.out.println("Consumed: " + item);
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    public static void demonstrateProducerConsumer() throws InterruptedException {
        System.out.println("\n=== Producer-Consumer Pattern ===");
        
        BlockingQueue<Integer> queue = new LinkedBlockingQueue<>(5);
        AtomicInteger counter = new AtomicInteger(0);
        
        // Producer
        Thread producer = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    int value = counter.incrementAndGet();
                    queue.put(value);
                    System.out.println("Produced: " + value);
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        // Consumer
        Thread consumer = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                try {
                    Integer value = queue.take();
                    System.out.println("Consumed: " + value);
                    Thread.sleep(700);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
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

### آنالوژی دنیای واقعی:
Concurrent Collections مانند داشتن یک سیستم انبار هوشمند است که:
- **Thread-Safe:** مانند قفل‌های امنیتی که از دسترسی همزمان محافظت می‌کنند
- **Performance:** مانند سیستم‌های خودکار که کارایی بالایی دارند
- **Producer-Consumer:** مانند سیستم تامین و توزیع کالا

## 15.5 CompletableFuture & Asynchronous Programming

CompletableFuture & Asynchronous Programming راه‌های قدرتمندی برای برنامه‌نویسی asynchronous در Java فراهم می‌کند.

### مفاهیم کلیدی:

**1. CompletableFuture:**
- Asynchronous computation
- Chaining operations
- Exception handling
- Combining futures

**2. Asynchronous Patterns:**
- Callback-based programming
- Promise-based programming
- Reactive programming
- Event-driven programming

**3. Use Cases:**
- I/O operations
- Web service calls
- Database operations
- File processing

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.function.Function;
import java.util.function.Supplier;

public class CompletableFutureExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== CompletableFuture Example ===");
        
        // 1. Basic CompletableFuture
        demonstrateBasicCompletableFuture();
        
        // 2. Chaining operations
        demonstrateChainingOperations();
        
        // 3. Combining futures
        demonstrateCombiningFutures();
        
        // 4. Exception handling
        demonstrateExceptionHandling();
        
        // 5. Real-world example
        demonstrateRealWorldExample();
    }
    
    public static void demonstrateBasicCompletableFuture() throws InterruptedException {
        System.out.println("\n=== Basic CompletableFuture ===");
        
        CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Hello from CompletableFuture!";
        });
        
        future.thenAccept(result -> {
            System.out.println("Result: " + result);
        });
        
        // Wait for completion
        future.join();
    }
    
    public static void demonstrateChainingOperations() throws InterruptedException {
        System.out.println("\n=== Chaining Operations ===");
        
        CompletableFuture<String> future = CompletableFuture
            .supplyAsync(() -> "Hello")
            .thenApply(s -> s + " World")
            .thenApply(String::toUpperCase)
            .thenApply(s -> s + "!")
            .thenApply(s -> "Result: " + s);
        
        future.thenAccept(System.out::println);
        future.join();
    }
    
    public static void demonstrateCombiningFutures() throws InterruptedException {
        System.out.println("\n=== Combining Futures ===");
        
        CompletableFuture<String> future1 = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Hello";
        });
        
        CompletableFuture<String> future2 = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "World";
        });
        
        // Combine both futures
        CompletableFuture<String> combined = future1.thenCombine(future2, (s1, s2) -> s1 + " " + s2);
        
        combined.thenAccept(result -> {
            System.out.println("Combined result: " + result);
        });
        
        combined.join();
    }
    
    public static void demonstrateExceptionHandling() throws InterruptedException {
        System.out.println("\n=== Exception Handling ===");
        
        CompletableFuture<String> future = CompletableFuture
            .supplyAsync(() -> {
                if (Math.random() > 0.5) {
                    throw new RuntimeException("Random error occurred");
                }
                return "Success";
            })
            .handle((result, throwable) -> {
                if (throwable != null) {
                    return "Error handled: " + throwable.getMessage();
                }
                return result;
            });
        
        future.thenAccept(System.out::println);
        future.join();
    }
    
    public static void demonstrateRealWorldExample() throws InterruptedException {
        System.out.println("\n=== Real-World Example ===");
        
        // Simulate user service
        CompletableFuture<User> userFuture = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return new User("احمد", "ahmad@example.com");
        });
        
        // Simulate order service
        CompletableFuture<Order> orderFuture = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(1500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return new Order(1L, 100.0);
        });
        
        // Simulate payment service
        CompletableFuture<Payment> paymentFuture = CompletableFuture.supplyAsync(() -> {
            try {
                Thread.sleep(800);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return new Payment(1L, "SUCCESS");
        });
        
        // Combine all futures
        CompletableFuture<String> result = userFuture
            .thenCombine(orderFuture, (user, order) -> {
                System.out.println("User: " + user.getName() + ", Order: " + order.getAmount());
                return new UserOrder(user, order);
            })
            .thenCombine(paymentFuture, (userOrder, payment) -> {
                System.out.println("Payment: " + payment.getStatus());
                return "Order processed successfully for " + userOrder.getUser().getName();
            });
        
        result.thenAccept(System.out::println);
        result.join();
    }
}

// Supporting classes
class User {
    private String name;
    private String email;
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    public String getName() { return name; }
    public String getEmail() { return email; }
}

class Order {
    private Long id;
    private Double amount;
    
    public Order(Long id, Double amount) {
        this.id = id;
        this.amount = amount;
    }
    
    public Long getId() { return id; }
    public Double getAmount() { return amount; }
}

class Payment {
    private Long orderId;
    private String status;
    
    public Payment(Long orderId, String status) {
        this.orderId = orderId;
        this.status = status;
    }
    
    public Long getOrderId() { return orderId; }
    public String getStatus() { return status; }
}

class UserOrder {
    private User user;
    private Order order;
    
    public UserOrder(User user, Order order) {
        this.user = user;
        this.order = order;
    }
    
    public User getUser() { return user; }
    public Order getOrder() { return order; }
}
```

### آنالوژی دنیای واقعی:
CompletableFuture & Asynchronous Programming مانند داشتن یک سیستم سفارش آنلاین هوشمند است که:
- **Asynchronous:** مانند ارسال سفارش بدون انتظار برای پاسخ
- **Chaining:** مانند مراحل مختلف پردازش سفارش
- **Exception Handling:** مانند سیستم مدیریت خطاها

## 15.6 Reactive Programming with Java

Reactive Programming با Java مجموعه‌ای از libraries و patterns برای برنامه‌نویسی reactive فراهم می‌کند.

### مفاهیم کلیدی:

**1. Reactive Streams:**
- Publisher
- Subscriber
- Subscription
- Processor

**2. Reactive Libraries:**
- RxJava
- Project Reactor
- Akka Streams
- Spring WebFlux

**3. Reactive Patterns:**
- Backpressure
- Error handling
- Composition
- Transformation

### مثال عملی:

```java
import reactor.core.publisher.*;
import reactor.core.scheduler.Schedulers;
import java.time.Duration;
import java.util.concurrent.TimeUnit;

public class ReactiveProgrammingExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Reactive Programming Example ===");
        
        // 1. Basic reactive streams
        demonstrateBasicReactiveStreams();
        
        // 2. Operators
        demonstrateOperators();
        
        // 3. Error handling
        demonstrateErrorHandling();
        
        // 4. Backpressure
        demonstrateBackpressure();
        
        // 5. Real-world example
        demonstrateRealWorldExample();
    }
    
    public static void demonstrateBasicReactiveStreams() {
        System.out.println("\n=== Basic Reactive Streams ===");
        
        // Create a simple stream
        Flux<String> flux = Flux.just("Hello", "World", "Reactive", "Programming");
        
        // Subscribe to the stream
        flux.subscribe(
            value -> System.out.println("Received: " + value),
            error -> System.err.println("Error: " + error),
            () -> System.out.println("Completed")
        );
    }
    
    public static void demonstrateOperators() {
        System.out.println("\n=== Operators ===");
        
        Flux<Integer> numbers = Flux.range(1, 10);
        
        numbers
            .filter(n -> n % 2 == 0)
            .map(n -> n * 2)
            .take(3)
            .subscribe(System.out::println);
    }
    
    public static void demonstrateErrorHandling() {
        System.out.println("\n=== Error Handling ===");
        
        Flux<String> flux = Flux.just("Hello", "World", "Error", "Reactive");
        
        flux
            .map(s -> {
                if ("Error".equals(s)) {
                    throw new RuntimeException("Error occurred");
                }
                return s.toUpperCase();
            })
            .onErrorResume(throwable -> {
                System.out.println("Error handled: " + throwable.getMessage());
                return Flux.just("DEFAULT");
            })
            .subscribe(System.out::println);
    }
    
    public static void demonstrateBackpressure() {
        System.out.println("\n=== Backpressure ===");
        
        Flux<Integer> fastProducer = Flux.range(1, 1000)
            .delayElements(Duration.ofMillis(10));
        
        fastProducer
            .onBackpressureBuffer(10)
            .subscribe(
                value -> {
                    System.out.println("Processed: " + value);
                    try {
                        Thread.sleep(100); // Slow consumer
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                },
                error -> System.err.println("Error: " + error)
            );
    }
    
    public static void demonstrateRealWorldExample() throws InterruptedException {
        System.out.println("\n=== Real-World Example ===");
        
        // Simulate user service
        Flux<User> userFlux = Flux.range(1, 5)
            .map(id -> new User("User" + id, "user" + id + "@example.com"))
            .delayElements(Duration.ofMillis(100));
        
        // Simulate order service
        Flux<Order> orderFlux = Flux.range(1, 5)
            .map(id -> new Order((long) id, 100.0 * id))
            .delayElements(Duration.ofMillis(150));
        
        // Combine streams
        Flux.zip(userFlux, orderFlux)
            .map(tuple -> {
                User user = tuple.getT1();
                Order order = tuple.getT2();
                return "User: " + user.getName() + ", Order: " + order.getAmount();
            })
            .subscribe(System.out::println);
        
        // Wait for completion
        Thread.sleep(2000);
    }
}

// Supporting classes
class User {
    private String name;
    private String email;
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    public String getName() { return name; }
    public String getEmail() { return email; }
}

class Order {
    private Long id;
    private Double amount;
    
    public Order(Long id, Double amount) {
        this.id = id;
        this.amount = amount;
    }
    
    public Long getId() { return id; }
    public Double getAmount() { return amount; }
}
```

### آنالوژی دنیای واقعی:
Reactive Programming مانند داشتن یک سیستم آبیاری هوشمند است که:
- **Streams:** مانند جریان آب که به صورت مداوم جاری است
- **Operators:** مانند فیلترها و تبدیل‌کننده‌های مختلف
- **Backpressure:** مانند سیستم کنترل فشار آب

## 15.7 Virtual Threads (Project Loom)

Virtual Threads (Project Loom) یکی از جدیدترین ویژگی‌های Java است که امکان ایجاد میلیون‌ها thread با overhead کم را فراهم می‌کند.

### مفاهیم کلیدی:

**1. Virtual Threads:**
- Lightweight threads
- Managed by JVM
- Millions of threads
- Low overhead

**2. Structured Concurrency:**
- Scoped execution
- Better error handling
- Resource management
- Lifecycle control

**3. Use Cases:**
- I/O intensive applications
- Web servers
- Microservices
- Event processing

### مثال عملی:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class VirtualThreadsExample {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Virtual Threads Example ===");
        
        // 1. Basic virtual threads
        demonstrateBasicVirtualThreads();
        
        // 2. Virtual thread executor
        demonstrateVirtualThreadExecutor();
        
        // 3. Structured concurrency
        demonstrateStructuredConcurrency();
        
        // 4. Performance comparison
        demonstratePerformanceComparison();
    }
    
    public static void demonstrateBasicVirtualThreads() throws InterruptedException {
        System.out.println("\n=== Basic Virtual Threads ===");
        
        // Create virtual thread
        Thread virtualThread = Thread.ofVirtual().start(() -> {
            System.out.println("Virtual thread: " + Thread.currentThread());
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Virtual thread completed");
        });
        
        // Wait for completion
        virtualThread.join();
    }
    
    public static void demonstrateVirtualThreadExecutor() throws InterruptedException {
        System.out.println("\n=== Virtual Thread Executor ===");
        
        ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " running on: " + Thread.currentThread());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("Task " + taskId + " completed");
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    public static void demonstrateStructuredConcurrency() throws InterruptedException {
        System.out.println("\n=== Structured Concurrency ===");
        
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            // Submit multiple tasks
            Future<String> task1 = scope.fork(() -> {
                Thread.sleep(1000);
                return "Task 1 completed";
            });
            
            Future<String> task2 = scope.fork(() -> {
                Thread.sleep(1500);
                return "Task 2 completed";
            });
            
            Future<String> task3 = scope.fork(() -> {
                Thread.sleep(800);
                return "Task 3 completed";
            });
            
            // Wait for all tasks to complete
            scope.join();
            scope.throwIfFailed();
            
            // Get results
            System.out.println("Result 1: " + task1.resultNow());
            System.out.println("Result 2: " + task2.resultNow());
            System.out.println("Result 3: " + task3.resultNow());
        }
    }
    
    public static void demonstratePerformanceComparison() throws InterruptedException {
        System.out.println("\n=== Performance Comparison ===");
        
        int taskCount = 10000;
        
        // Platform threads
        long startTime = System.currentTimeMillis();
        ExecutorService platformExecutor = Executors.newFixedThreadPool(100);
        
        for (int i = 0; i < taskCount; i++) {
            final int taskId = i;
            platformExecutor.submit(() -> {
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        platformExecutor.shutdown();
        platformExecutor.awaitTermination(30, TimeUnit.SECONDS);
        
        long platformTime = System.currentTimeMillis() - startTime;
        System.out.println("Platform threads time: " + platformTime + " ms");
        
        // Virtual threads
        startTime = System.currentTimeMillis();
        ExecutorService virtualExecutor = Executors.newVirtualThreadPerTaskExecutor();
        
        for (int i = 0; i < taskCount; i++) {
            final int taskId = i;
            virtualExecutor.submit(() -> {
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        virtualExecutor.shutdown();
        virtualExecutor.awaitTermination(30, TimeUnit.SECONDS);
        
        long virtualTime = System.currentTimeMillis() - startTime;
        System.out.println("Virtual threads time: " + virtualTime + " ms");
    }
}
```

### آنالوژی دنیای واقعی:
Virtual Threads مانند داشتن یک سیستم مدیریت هوشمند است که:
- **Lightweight:** مانند کارگران مجازی که نیازی به فضای فیزیکی ندارند
- **Millions:** مانند امکان داشتن میلیون‌ها کارگر مجازی
- **Structured Concurrency:** مانند سیستم مدیریت پروژه که همه کارها را هماهنگ می‌کند