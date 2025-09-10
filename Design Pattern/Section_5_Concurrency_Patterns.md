# Section 5 - Concurrency Patterns

## 5.1 Active Object Pattern

The Active Object pattern decouples method execution from method invocation to enhance concurrency and simplify synchronized access to objects that reside in their own thread of control.

### When to Use:
- When you need to decouple method invocation from execution
- When you want to simplify synchronized access to objects
- When you need to handle requests asynchronously

### Real-World Analogy:
Think of a restaurant where orders are taken by waiters (invocation) but prepared by chefs (execution) in the kitchen, allowing the restaurant to serve multiple customers simultaneously.

### Implementation:
```java
// Active object interface
public interface ActiveObject {
    Future<String> processRequest(String request);
}

// Concrete active object
public class ActiveObjectImpl implements ActiveObject {
    private ExecutorService executor;
    private Queue<Request> requestQueue;
    
    public ActiveObjectImpl() {
        this.executor = Executors.newSingleThreadExecutor();
        this.requestQueue = new ConcurrentLinkedQueue<>();
    }
    
    public Future<String> processRequest(String request) {
        return executor.submit(() -> {
            // Simulate processing
            Thread.sleep(1000);
            return "Processed: " + request;
        });
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

## 5.2 Monitor Pattern

The Monitor pattern provides a mechanism for threads to safely access shared resources by using synchronized methods and wait/notify mechanisms.

### When to Use:
- When you need to protect shared resources from concurrent access
- When you want to coordinate thread execution
- When you need to implement producer-consumer scenarios

### Real-World Analogy:
Think of a bank teller window where only one customer can be served at a time, and customers wait in line for their turn.

### Implementation:
```java
public class BankAccount {
    private double balance;
    private final Object lock = new Object();
    
    public void deposit(double amount) {
        synchronized (lock) {
            balance += amount;
            System.out.println("Deposited: " + amount + ", Balance: " + balance);
            lock.notifyAll();
        }
    }
    
    public void withdraw(double amount) throws InterruptedException {
        synchronized (lock) {
            while (balance < amount) {
                System.out.println("Insufficient funds, waiting...");
                lock.wait();
            }
            balance -= amount;
            System.out.println("Withdrawn: " + amount + ", Balance: " + balance);
        }
    }
    
    public double getBalance() {
        synchronized (lock) {
            return balance;
        }
    }
}
```

## 5.3 Half-Sync/Half-Async Pattern

The Half-Sync/Half-Async pattern separates synchronous and asynchronous processing to simplify concurrent programming while maintaining good performance.

### When to Use:
- When you need to handle both synchronous and asynchronous operations
- When you want to simplify concurrent programming
- When you need to maintain good performance

### Real-World Analogy:
Think of a restaurant with both dine-in (synchronous) and takeout (asynchronous) services, each handled by different staff members.

### Implementation:
```java
public class HalfSyncHalfAsyncProcessor {
    private ExecutorService asyncExecutor;
    private ExecutorService syncExecutor;
    
    public HalfSyncHalfAsyncProcessor() {
        this.asyncExecutor = Executors.newCachedThreadPool();
        this.syncExecutor = Executors.newFixedThreadPool(2);
    }
    
    public void processAsync(String request) {
        asyncExecutor.submit(() -> {
            System.out.println("Async processing: " + request);
            // Simulate async work
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Async completed: " + request);
        });
    }
    
    public String processSync(String request) {
        return syncExecutor.submit(() -> {
            System.out.println("Sync processing: " + request);
            // Simulate sync work
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return "Sync result: " + request;
        }).get();
    }
}
```

## 5.4 Leader/Followers Pattern

The Leader/Followers pattern provides an efficient concurrency model where multiple threads take turns being the leader to process events.

### When to Use:
- When you need to process events efficiently
- When you want to minimize context switching
- When you need to handle high-throughput scenarios

### Real-World Analogy:
Think of a relay race where runners take turns being the leader, passing the baton to the next runner.

### Implementation:
```java
public class LeaderFollowersPattern {
    private final Object lock = new Object();
    private Thread leader;
    private Queue<Thread> followers;
    private Queue<Runnable> events;
    
    public LeaderFollowersPattern() {
        this.followers = new LinkedList<>();
        this.events = new LinkedList<>();
    }
    
    public void processEvent(Runnable event) {
        synchronized (lock) {
            events.offer(event);
            if (leader == null) {
                promoteFollower();
            }
        }
    }
    
    private void promoteFollower() {
        if (!followers.isEmpty()) {
            leader = followers.poll();
            leader.interrupt();
        }
    }
    
    public void run() {
        while (true) {
            Runnable event = null;
            synchronized (lock) {
                if (!events.isEmpty()) {
                    event = events.poll();
                } else {
                    followers.offer(Thread.currentThread());
                    leader = null;
                    try {
                        lock.wait();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            }
            
            if (event != null) {
                event.run();
            }
        }
    }
}
```

## 5.5 Thread-Safe Singleton

The Thread-Safe Singleton pattern ensures that only one instance of a class exists in a multi-threaded environment.

### When to Use:
- When you need a singleton in a multi-threaded environment
- When you want to ensure thread safety
- When you need lazy initialization

### Implementation:
```java
public class ThreadSafeSingleton {
    private static volatile ThreadSafeSingleton instance;
    
    private ThreadSafeSingleton() {}
    
    public static ThreadSafeSingleton getInstance() {
        if (instance == null) {
            synchronized (ThreadSafeSingleton.class) {
                if (instance == null) {
                    instance = new ThreadSafeSingleton();
                }
            }
        }
        return instance;
    }
}

// Alternative using enum
public enum ThreadSafeSingletonEnum {
    INSTANCE;
    
    public void doSomething() {
        System.out.println("Doing something...");
    }
}
```

## 5.6 Double-Checked Locking

The Double-Checked Locking pattern is an optimization technique for the thread-safe singleton pattern that reduces the overhead of acquiring a lock.

### When to Use:
- When you want to optimize thread-safe singleton creation
- When you need to reduce lock overhead
- When you want to ensure lazy initialization

### Implementation:
```java
public class DoubleCheckedLocking {
    private static volatile DoubleCheckedLocking instance;
    
    private DoubleCheckedLocking() {}
    
    public static DoubleCheckedLocking getInstance() {
        if (instance == null) {
            synchronized (DoubleCheckedLocking.class) {
                if (instance == null) {
                    instance = new DoubleCheckedLocking();
                }
            }
        }
        return instance;
    }
}
```

## 5.7 Thread Pool Pattern

The Thread Pool pattern maintains a pool of worker threads that execute tasks, avoiding the overhead of creating and destroying threads.

### When to Use:
- When you need to execute many short-lived tasks
- When you want to control the number of concurrent threads
- When you want to improve performance by reusing threads

### Real-World Analogy:
Think of a taxi company that maintains a fleet of taxis ready to serve customers, rather than building a new taxi for each ride.

### Implementation:
```java
public class ThreadPoolPattern {
    private ExecutorService executor;
    private int poolSize;
    
    public ThreadPoolPattern(int poolSize) {
        this.poolSize = poolSize;
        this.executor = Executors.newFixedThreadPool(poolSize);
    }
    
    public void submitTask(Runnable task) {
        executor.submit(task);
    }
    
    public Future<String> submitCallable(Callable<String> task) {
        return executor.submit(task);
    }
    
    public void shutdown() {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

## 5.8 Producer-Consumer Pattern

The Producer-Consumer pattern coordinates the production and consumption of data between multiple threads using a shared buffer.

### When to Use:
- When you need to decouple data production from consumption
- When you want to handle varying production and consumption rates
- When you need to implement asynchronous processing

### Real-World Analogy:
Think of a factory assembly line where workers produce items and place them on a conveyor belt, while other workers consume these items for further processing.

### Implementation:
```java
public class ProducerConsumerPattern {
    private final BlockingQueue<Integer> buffer;
    private final int capacity;
    
    public ProducerConsumerPattern(int capacity) {
        this.capacity = capacity;
        this.buffer = new ArrayBlockingQueue<>(capacity);
    }
    
    public void produce() throws InterruptedException {
        int value = 0;
        while (true) {
            buffer.put(value);
            System.out.println("Produced: " + value);
            value++;
            Thread.sleep(1000);
        }
    }
    
    public void consume() throws InterruptedException {
        while (true) {
            int value = buffer.take();
            System.out.println("Consumed: " + value);
            Thread.sleep(1500);
        }
    }
}
```

## 5.9 Read-Write Lock Pattern

The Read-Write Lock pattern allows multiple readers or one writer to access a shared resource, improving performance for read-heavy workloads.

### When to Use:
- When you have more reads than writes
- When you want to improve performance for read operations
- When you need to protect shared resources

### Real-World Analogy:
Think of a library where multiple people can read books simultaneously, but only one person can check out or return a book at a time.

### Implementation:
```java
public class ReadWriteLockPattern {
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    private final Lock readLock = lock.readLock();
    private final Lock writeLock = lock.writeLock();
    private String data;
    
    public String read() {
        readLock.lock();
        try {
            System.out.println("Reading data: " + data);
            return data;
        } finally {
            readLock.unlock();
        }
    }
    
    public void write(String newData) {
        writeLock.lock();
        try {
            System.out.println("Writing data: " + newData);
            this.data = newData;
        } finally {
            writeLock.unlock();
        }
    }
}
```

## 5.10 Future Pattern

The Future pattern represents the result of an asynchronous computation, allowing you to check if the computation is complete and retrieve the result.

### When to Use:
- When you need to perform asynchronous computations
- When you want to retrieve results from background tasks
- When you need to handle long-running operations

### Real-World Analogy:
Think of ordering food online - you get a receipt (Future) that you can use to check if your order is ready and collect it when it's done.

### Implementation:
```java
public class FuturePattern {
    private ExecutorService executor;
    
    public FuturePattern() {
        this.executor = Executors.newCachedThreadPool();
    }
    
    public Future<String> processAsync(String input) {
        return executor.submit(() -> {
            // Simulate long-running task
            Thread.sleep(2000);
            return "Processed: " + input;
        });
    }
    
    public void processWithCallback(String input, Consumer<String> callback) {
        executor.submit(() -> {
            try {
                Thread.sleep(2000);
                String result = "Processed: " + input;
                callback.accept(result);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
    }
    
    public void shutdown() {
        executor.shutdown();
    }
}
```

This section covers the essential concurrency patterns that help manage multi-threaded applications safely and efficiently, ensuring proper synchronization and resource management.