# Section 7 - Thread Pools and Executors

## 7.1 Thread Pool Fundamentals

Thread pools are a collection of pre-created threads that can be reused to execute tasks, eliminating the overhead of creating and destroying threads for each task. They provide better performance and resource management in multithreaded applications.

### Key Concepts:

**1. Thread Reuse:**
- Threads are created once and reused for multiple tasks
- Eliminates thread creation/destruction overhead
- Better resource utilization

**2. Task Queue:**
- Tasks are queued when all threads are busy
- Different queue types for different needs
- Bounded vs unbounded queues

**3. Thread Lifecycle Management:**
- Automatic thread creation and destruction
- Configurable pool size
- Graceful shutdown handling

### Java Example - Basic Thread Pool:

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ThreadPoolFundamentals {
    public static void main(String[] args) throws InterruptedException {
        // Create a thread pool with 4 threads
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Submit tasks to the thread pool
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " executed by " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000); // Simulate work
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Shutdown the executor
        executor.shutdown();
        
        // Wait for all tasks to complete
        if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
            executor.shutdownNow();
        }
        
        System.out.println("All tasks completed");
    }
}
```

### Real-World Analogy:
Think of thread pools like a team of workers in a factory:
- **Threads**: Like individual workers
- **Tasks**: Like work orders that need to be completed
- **Queue**: Like a work order board where new orders are posted
- **Pool Manager**: Like a supervisor who assigns work to available workers

## 7.2 Executor Framework

The Executor framework provides a high-level interface for executing tasks asynchronously. It separates task submission from task execution, making multithreaded programming easier and more flexible.

### Key Components:

**1. Executor Interface:**
- Simple interface for executing tasks
- `execute(Runnable)` method
- Foundation of the framework

**2. ExecutorService Interface:**
- Extends Executor with lifecycle management
- Methods for shutdown, task submission, and result handling
- More control over execution

**3. ScheduledExecutorService Interface:**
- Extends ExecutorService with scheduling capabilities
- Delayed and periodic task execution
- Timer-like functionality

### Java Example - Executor Framework:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ExecutorFrameworkExample {
    private final AtomicInteger taskCounter = new AtomicInteger(0);
    
    public void demonstrateExecutorFramework() throws InterruptedException {
        // Create different types of executors
        demonstrateFixedThreadPool();
        demonstrateCachedThreadPool();
        demonstrateSingleThreadExecutor();
        demonstrateScheduledExecutor();
    }
    
    private void demonstrateFixedThreadPool() throws InterruptedException {
        System.out.println("=== Fixed Thread Pool ===");
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        for (int i = 0; i < 6; i++) {
            executor.submit(createTask("FixedPool"));
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateCachedThreadPool() throws InterruptedException {
        System.out.println("=== Cached Thread Pool ===");
        ExecutorService executor = Executors.newCachedThreadPool();
        
        for (int i = 0; i < 6; i++) {
            executor.submit(createTask("CachedPool"));
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateSingleThreadExecutor() throws InterruptedException {
        System.out.println("=== Single Thread Executor ===");
        ExecutorService executor = Executors.newSingleThreadExecutor();
        
        for (int i = 0; i < 3; i++) {
            executor.submit(createTask("SingleThread"));
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateScheduledExecutor() throws InterruptedException {
        System.out.println("=== Scheduled Executor ===");
        ScheduledExecutorService executor = Executors.newScheduledThreadPool(2);
        
        // Schedule a task to run after 2 seconds
        executor.schedule(createTask("Scheduled"), 2, TimeUnit.SECONDS);
        
        // Schedule a task to run every 1 second
        executor.scheduleAtFixedRate(createTask("Periodic"), 0, 1, TimeUnit.SECONDS);
        
        // Let it run for 5 seconds
        Thread.sleep(5000);
        
        executor.shutdown();
        executor.awaitTermination(2, TimeUnit.SECONDS);
    }
    
    private Runnable createTask(String poolType) {
        return () -> {
            int taskId = taskCounter.incrementAndGet();
            System.out.println(poolType + " - Task " + taskId + " executed by " + 
                             Thread.currentThread().getName());
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        };
    }
    
    public static void main(String[] args) throws InterruptedException {
        ExecutorFrameworkExample example = new ExecutorFrameworkExample();
        example.demonstrateExecutorFramework();
    }
}
```

## 7.3 Thread Pool Types

Different types of thread pools are designed for different use cases. Each type has its own characteristics and trade-offs.

### Thread Pool Types:

**1. Fixed Thread Pool:**
- Fixed number of threads
- Good for CPU-intensive tasks
- Predictable resource usage

**2. Cached Thread Pool:**
- Creates threads as needed
- Good for I/O-intensive tasks
- Threads are terminated after 60 seconds of inactivity

**3. Single Thread Pool:**
- Only one thread
- Tasks execute sequentially
- Good for maintaining order

**4. Scheduled Thread Pool:**
- For delayed and periodic tasks
- Timer-like functionality
- Configurable thread count

### Java Example - Thread Pool Types Comparison:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

public class ThreadPoolTypesExample {
    private final AtomicLong taskCounter = new AtomicLong(0);
    
    public void compareThreadPoolTypes() throws InterruptedException {
        System.out.println("=== Thread Pool Types Comparison ===");
        
        // Test with CPU-intensive tasks
        testFixedThreadPool(1000, "CPU-Intensive");
        testCachedThreadPool(1000, "CPU-Intensive");
        
        // Test with I/O-intensive tasks
        testFixedThreadPool(100, "I/O-Intensive");
        testCachedThreadPool(100, "I/O-Intensive");
    }
    
    private void testFixedThreadPool(int taskCount, String taskType) throws InterruptedException {
        System.out.println("\n--- Fixed Thread Pool (" + taskType + ") ---");
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < taskCount; i++) {
            executor.submit(createTask(taskType));
        }
        
        executor.shutdown();
        executor.awaitTermination(30, TimeUnit.SECONDS);
        
        long endTime = System.currentTimeMillis();
        System.out.println("Fixed Thread Pool completed in " + (endTime - startTime) + "ms");
    }
    
    private void testCachedThreadPool(int taskCount, String taskType) throws InterruptedException {
        System.out.println("\n--- Cached Thread Pool (" + taskType + ") ---");
        ExecutorService executor = Executors.newCachedThreadPool();
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < taskCount; i++) {
            executor.submit(createTask(taskType));
        }
        
        executor.shutdown();
        executor.awaitTermination(30, TimeUnit.SECONDS);
        
        long endTime = System.currentTimeMillis();
        System.out.println("Cached Thread Pool completed in " + (endTime - startTime) + "ms");
    }
    
    private Runnable createTask(String taskType) {
        return () -> {
            long taskId = taskCounter.incrementAndGet();
            
            if ("CPU-Intensive".equals(taskType)) {
                // CPU-intensive work
                long sum = 0;
                for (int i = 0; i < 1000000; i++) {
                    sum += i;
                }
            } else {
                // I/O-intensive work (simulated)
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            
            if (taskId % 100 == 0) {
                System.out.println(taskType + " Task " + taskId + " completed by " + 
                                 Thread.currentThread().getName());
            }
        };
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadPoolTypesExample example = new ThreadPoolTypesExample();
        example.compareThreadPoolTypes();
    }
}
```

## 7.4 Thread Pool Configuration

Proper thread pool configuration is crucial for optimal performance. Consider factors like core pool size, maximum pool size, queue type, and thread keep-alive time.

### Configuration Parameters:

**1. Core Pool Size:**
- Number of threads to keep in the pool
- Threads are created even if idle
- Should match expected workload

**2. Maximum Pool Size:**
- Maximum number of threads allowed
- New threads created when queue is full
- Prevents resource exhaustion

**3. Queue Type:**
- Bounded vs unbounded queues
- Different queue types for different needs
- Affects task scheduling behavior

### Java Example - Custom Thread Pool Configuration:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadPoolConfigurationExample {
    public void demonstrateCustomConfiguration() throws InterruptedException {
        // Custom thread pool with specific configuration
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2,                              // core pool size
            5,                              // maximum pool size
            60L,                            // keep alive time
            TimeUnit.SECONDS,               // time unit
            new LinkedBlockingQueue<>(10),  // work queue
            new CustomThreadFactory(),      // thread factory
            new CustomRejectedExecutionHandler() // rejection handler
        );
        
        // Allow core threads to timeout
        executor.allowCoreThreadTimeOut(true);
        
        System.out.println("Thread pool created with custom configuration");
        System.out.println("Core pool size: " + executor.getCorePoolSize());
        System.out.println("Maximum pool size: " + executor.getMaximumPoolSize());
        System.out.println("Queue capacity: " + executor.getQueue().remainingCapacity());
        
        // Submit tasks
        for (int i = 0; i < 20; i++) {
            final int taskId = i;
            try {
                executor.submit(() -> {
                    System.out.println("Task " + taskId + " executed by " + 
                                     Thread.currentThread().getName());
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                });
            } catch (RejectedExecutionException e) {
                System.out.println("Task " + taskId + " rejected: " + e.getMessage());
            }
        }
        
        // Monitor thread pool
        monitorThreadPool(executor);
        
        executor.shutdown();
        executor.awaitTermination(30, TimeUnit.SECONDS);
    }
    
    private void monitorThreadPool(ThreadPoolExecutor executor) {
        Thread monitor = new Thread(() -> {
            while (!executor.isShutdown()) {
                System.out.println("Pool size: " + executor.getPoolSize() + 
                                 ", Active: " + executor.getActiveCount() + 
                                 ", Queue size: " + executor.getQueue().size());
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        monitor.start();
    }
    
    // Custom thread factory
    private static class CustomThreadFactory implements ThreadFactory {
        private final AtomicInteger threadNumber = new AtomicInteger(1);
        
        @Override
        public Thread newThread(Runnable r) {
            Thread thread = new Thread(r, "CustomThread-" + threadNumber.getAndIncrement());
            thread.setDaemon(false);
            thread.setPriority(Thread.NORM_PRIORITY);
            return thread;
        }
    }
    
    // Custom rejection handler
    private static class CustomRejectedExecutionHandler implements RejectedExecutionHandler {
        @Override
        public void rejectedExecution(Runnable r, ThreadPoolExecutor executor) {
            System.out.println("Task rejected: " + r.toString());
            // Could implement custom logic like logging, retry, etc.
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadPoolConfigurationExample example = new ThreadPoolConfigurationExample();
        example.demonstrateCustomConfiguration();
    }
}
```

## 7.5 Task Submission

Task submission is the process of providing tasks to the thread pool for execution. Different submission methods offer different capabilities and return types.

### Submission Methods:

**1. execute(Runnable):**
- Fire-and-forget execution
- No return value
- No exception handling

**2. submit(Runnable):**
- Returns Future<?>
- Can check completion status
- Can cancel the task

**3. submit(Callable<T>):**
- Returns Future<T>
- Can get return value
- Exception handling

**4. invokeAll/Any:**
- Submit multiple tasks
- Wait for all/any to complete
- Batch processing

### Java Example - Task Submission Methods:

```java
import java.util.concurrent.*;
import java.util.List;
import java.util.ArrayList;
import java.util.Random;

public class TaskSubmissionExample {
    private final Random random = new Random();
    
    public void demonstrateTaskSubmission() throws InterruptedException, ExecutionException {
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        // Method 1: execute() - fire and forget
        demonstrateExecute(executor);
        
        // Method 2: submit() with Runnable
        demonstrateSubmitRunnable(executor);
        
        // Method 3: submit() with Callable
        demonstrateSubmitCallable(executor);
        
        // Method 4: invokeAll() - batch processing
        demonstrateInvokeAll(executor);
        
        // Method 5: invokeAny() - first result
        demonstrateInvokeAny(executor);
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    private void demonstrateExecute(ExecutorService executor) {
        System.out.println("=== execute() method ===");
        for (int i = 0; i < 3; i++) {
            final int taskId = i;
            executor.execute(() -> {
                System.out.println("Execute task " + taskId + " running on " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
    }
    
    private void demonstrateSubmitRunnable(ExecutorService executor) throws InterruptedException {
        System.out.println("\n=== submit() with Runnable ===");
        List<Future<?>> futures = new ArrayList<>();
        
        for (int i = 0; i < 3; i++) {
            final int taskId = i;
            Future<?> future = executor.submit(() -> {
                System.out.println("Submit Runnable task " + taskId + " running on " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
            futures.add(future);
        }
        
        // Wait for all tasks to complete
        for (Future<?> future : futures) {
            future.get();
        }
        System.out.println("All Runnable tasks completed");
    }
    
    private void demonstrateSubmitCallable(ExecutorService executor) throws InterruptedException, ExecutionException {
        System.out.println("\n=== submit() with Callable ===");
        List<Future<Integer>> futures = new ArrayList<>();
        
        for (int i = 0; i < 3; i++) {
            final int taskId = i;
            Future<Integer> future = executor.submit(() -> {
                System.out.println("Submit Callable task " + taskId + " running on " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                return taskId * 100;
            });
            futures.add(future);
        }
        
        // Get results
        for (Future<Integer> future : futures) {
            Integer result = future.get();
            System.out.println("Callable task result: " + result);
        }
    }
    
    private void demonstrateInvokeAll(ExecutorService executor) throws InterruptedException, ExecutionException {
        System.out.println("\n=== invokeAll() method ===");
        List<Callable<String>> tasks = new ArrayList<>();
        
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            tasks.add(() -> {
                int sleepTime = random.nextInt(2000) + 500;
                Thread.sleep(sleepTime);
                return "Task " + taskId + " completed in " + sleepTime + "ms";
            });
        }
        
        List<Future<String>> futures = executor.invokeAll(tasks);
        
        for (Future<String> future : futures) {
            System.out.println("invokeAll result: " + future.get());
        }
    }
    
    private void demonstrateInvokeAny(ExecutorService executor) throws InterruptedException, ExecutionException {
        System.out.println("\n=== invokeAny() method ===");
        List<Callable<String>> tasks = new ArrayList<>();
        
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            tasks.add(() -> {
                int sleepTime = random.nextInt(2000) + 500;
                Thread.sleep(sleepTime);
                return "Task " + taskId + " completed in " + sleepTime + "ms";
            });
        }
        
        String result = executor.invokeAny(tasks);
        System.out.println("invokeAny result: " + result);
    }
    
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        TaskSubmissionExample example = new TaskSubmissionExample();
        example.demonstrateTaskSubmission();
    }
}
```

## 7.6 Task Execution

Task execution involves the actual running of tasks by threads in the pool. Understanding execution behavior helps in optimizing performance and handling edge cases.

### Execution Characteristics:

**1. Thread Assignment:**
- Tasks are assigned to available threads
- Threads can execute multiple tasks sequentially
- Load balancing across threads

**2. Task Ordering:**
- Tasks may not execute in submission order
- Queue type affects execution order
- Priority can influence ordering

**3. Exception Handling:**
- Uncaught exceptions can terminate threads
- Proper exception handling is crucial
- Thread pool may need to create new threads

### Java Example - Task Execution Monitoring:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class TaskExecutionExample {
    private final AtomicInteger taskCounter = new AtomicInteger(0);
    private final AtomicInteger completedTasks = new AtomicInteger(0);
    
    public void demonstrateTaskExecution() throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Submit tasks with different characteristics
        submitTasks(executor);
        
        // Monitor execution
        monitorExecution(executor);
        
        executor.shutdown();
        executor.awaitTermination(10, TimeUnit.SECONDS);
    }
    
    private void submitTasks(ExecutorService executor) {
        // Fast tasks
        for (int i = 0; i < 5; i++) {
            executor.submit(createTask("Fast", 100));
        }
        
        // Slow tasks
        for (int i = 0; i < 3; i++) {
            executor.submit(createTask("Slow", 2000));
        }
        
        // Tasks with exceptions
        for (int i = 0; i < 2; i++) {
            executor.submit(createTaskWithException("Exception", 500));
        }
        
        // CPU-intensive tasks
        for (int i = 0; i < 4; i++) {
            executor.submit(createCPUTask("CPU", 1000));
        }
    }
    
    private Runnable createTask(String type, int duration) {
        return () -> {
            int taskId = taskCounter.incrementAndGet();
            System.out.println(type + " task " + taskId + " started on " + 
                             Thread.currentThread().getName());
            
            try {
                Thread.sleep(duration);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println(type + " task " + taskId + " interrupted");
                return;
            }
            
            completedTasks.incrementAndGet();
            System.out.println(type + " task " + taskId + " completed on " + 
                             Thread.currentThread().getName());
        };
    }
    
    private Runnable createTaskWithException(String type, int duration) {
        return () -> {
            int taskId = taskCounter.incrementAndGet();
            System.out.println(type + " task " + taskId + " started on " + 
                             Thread.currentThread().getName());
            
            try {
                Thread.sleep(duration);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
            
            // Simulate exception
            if (taskId % 2 == 0) {
                throw new RuntimeException("Simulated exception in task " + taskId);
            }
            
            completedTasks.incrementAndGet();
            System.out.println(type + " task " + taskId + " completed on " + 
                             Thread.currentThread().getName());
        };
    }
    
    private Runnable createCPUTask(String type, int iterations) {
        return () -> {
            int taskId = taskCounter.incrementAndGet();
            System.out.println(type + " task " + taskId + " started on " + 
                             Thread.currentThread().getName());
            
            // CPU-intensive work
            long sum = 0;
            for (int i = 0; i < iterations * 1000000; i++) {
                sum += i;
            }
            
            completedTasks.incrementAndGet();
            System.out.println(type + " task " + taskId + " completed on " + 
                             Thread.currentThread().getName() + " (sum: " + sum + ")");
        };
    }
    
    private void monitorExecution(ExecutorService executor) {
        Thread monitor = new Thread(() -> {
            while (!executor.isShutdown()) {
                if (executor instanceof ThreadPoolExecutor) {
                    ThreadPoolExecutor tpe = (ThreadPoolExecutor) executor;
                    System.out.println("Pool size: " + tpe.getPoolSize() + 
                                     ", Active: " + tpe.getActiveCount() + 
                                     ", Completed: " + tpe.getCompletedTaskCount() + 
                                     ", Queue size: " + tpe.getQueue().size());
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        monitor.start();
    }
    
    public static void main(String[] args) throws InterruptedException {
        TaskExecutionExample example = new TaskExecutionExample();
        example.demonstrateTaskExecution();
    }
}
```

## 7.7 Thread Pool Lifecycle

Understanding the thread pool lifecycle is crucial for proper resource management. Thread pools go through different states from creation to shutdown.

### Lifecycle States:

**1. Running:**
- Accepting new tasks
- Executing submitted tasks
- Normal operation state

**2. Shutdown:**
- No longer accepting new tasks
- Executing remaining tasks
- Graceful shutdown initiated

**3. Stopped:**
- No longer accepting tasks
- Not executing tasks
- All resources released

### Java Example - Thread Pool Lifecycle:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadPoolLifecycleExample {
    private final AtomicInteger taskCounter = new AtomicInteger(0);
    
    public void demonstrateLifecycle() throws InterruptedException {
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2, 4, 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(10)
        );
        
        System.out.println("=== Thread Pool Lifecycle ===");
        
        // State 1: Running
        demonstrateRunningState(executor);
        
        // State 2: Shutdown
        demonstrateShutdownState(executor);
        
        // State 3: Stopped
        demonstrateStoppedState(executor);
    }
    
    private void demonstrateRunningState(ThreadPoolExecutor executor) throws InterruptedException {
        System.out.println("\n--- Running State ---");
        System.out.println("Is running: " + !executor.isShutdown());
        System.out.println("Is terminated: " + executor.isTerminated());
        
        // Submit tasks
        for (int i = 0; i < 5; i++) {
            executor.submit(createTask("Running"));
        }
        
        Thread.sleep(2000);
    }
    
    private void demonstrateShutdownState(ThreadPoolExecutor executor) throws InterruptedException {
        System.out.println("\n--- Shutdown State ---");
        
        // Initiate shutdown
        executor.shutdown();
        System.out.println("Shutdown initiated");
        System.out.println("Is running: " + !executor.isShutdown());
        System.out.println("Is terminated: " + executor.isTerminated());
        
        // Try to submit new task (will be rejected)
        try {
            executor.submit(createTask("AfterShutdown"));
        } catch (RejectedExecutionException e) {
            System.out.println("Task rejected after shutdown: " + e.getMessage());
        }
        
        // Wait for tasks to complete
        boolean terminated = executor.awaitTermination(5, TimeUnit.SECONDS);
        System.out.println("Graceful shutdown completed: " + terminated);
    }
    
    private void demonstrateStoppedState(ThreadPoolExecutor executor) {
        System.out.println("\n--- Stopped State ---");
        System.out.println("Is running: " + !executor.isShutdown());
        System.out.println("Is terminated: " + executor.isTerminated());
        
        // Try to submit task (will be rejected)
        try {
            executor.submit(createTask("AfterTermination"));
        } catch (RejectedExecutionException e) {
            System.out.println("Task rejected after termination: " + e.getMessage());
        }
    }
    
    private Runnable createTask(String phase) {
        return () -> {
            int taskId = taskCounter.incrementAndGet();
            System.out.println(phase + " task " + taskId + " executed by " + 
                             Thread.currentThread().getName());
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        };
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadPoolLifecycleExample example = new ThreadPoolLifecycleExample();
        example.demonstrateLifecycle();
    }
}
```

## 7.8 Thread Pool Monitoring

Monitoring thread pools helps identify performance bottlenecks, resource usage patterns, and potential issues. It's essential for production systems.

### Monitoring Metrics:

**1. Pool Size Metrics:**
- Current pool size
- Active thread count
- Core pool size
- Maximum pool size

**2. Task Metrics:**
- Total tasks submitted
- Completed tasks
- Rejected tasks
- Queue size

**3. Performance Metrics:**
- Average task execution time
- Throughput
- Resource utilization

### Java Example - Thread Pool Monitoring:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;
import java.util.Timer;
import java.util.TimerTask;

public class ThreadPoolMonitoringExample {
    private final AtomicLong totalExecutionTime = new AtomicLong(0);
    private final AtomicLong taskCount = new AtomicLong(0);
    
    public void demonstrateMonitoring() throws InterruptedException {
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2, 5, 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(10),
            new ThreadFactory() {
                private final AtomicInteger threadNumber = new AtomicInteger(1);
                @Override
                public Thread newThread(Runnable r) {
                    Thread thread = new Thread(r, "MonitoredThread-" + threadNumber.getAndIncrement());
                    thread.setDaemon(false);
                    return thread;
                }
            }
        );
        
        // Start monitoring
        startMonitoring(executor);
        
        // Submit various tasks
        submitTasks(executor);
        
        // Wait for completion
        executor.shutdown();
        executor.awaitTermination(30, TimeUnit.SECONDS);
        
        // Print final statistics
        printFinalStatistics(executor);
    }
    
    private void startMonitoring(ThreadPoolExecutor executor) {
        Timer timer = new Timer("ThreadPoolMonitor", true);
        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                System.out.println("=== Thread Pool Status ===");
                System.out.println("Pool size: " + executor.getPoolSize());
                System.out.println("Active threads: " + executor.getActiveCount());
                System.out.println("Core pool size: " + executor.getCorePoolSize());
                System.out.println("Maximum pool size: " + executor.getMaximumPoolSize());
                System.out.println("Completed tasks: " + executor.getCompletedTaskCount());
                System.out.println("Total tasks: " + executor.getTaskCount());
                System.out.println("Queue size: " + executor.getQueue().size());
                System.out.println("Is shutdown: " + executor.isShutdown());
                System.out.println("Is terminated: " + executor.isTerminated());
                System.out.println("=========================");
            }
        }, 0, 2000);
    }
    
    private void submitTasks(ThreadPoolExecutor executor) {
        // Submit tasks with different characteristics
        for (int i = 0; i < 20; i++) {
            final int taskId = i;
            executor.submit(() -> {
                long startTime = System.currentTimeMillis();
                
                try {
                    // Simulate work
                    Thread.sleep(1000 + (int)(Math.random() * 2000));
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                
                long executionTime = System.currentTimeMillis() - startTime;
                totalExecutionTime.addAndGet(executionTime);
                taskCount.incrementAndGet();
                
                System.out.println("Task " + taskId + " completed in " + executionTime + "ms");
            });
        }
    }
    
    private void printFinalStatistics(ThreadPoolExecutor executor) {
        System.out.println("\n=== Final Statistics ===");
        System.out.println("Total tasks executed: " + taskCount.get());
        System.out.println("Total execution time: " + totalExecutionTime.get() + "ms");
        System.out.println("Average execution time: " + 
                         (taskCount.get() > 0 ? totalExecutionTime.get() / taskCount.get() : 0) + "ms");
        System.out.println("Completed tasks: " + executor.getCompletedTaskCount());
        System.out.println("Rejected tasks: " + (executor.getTaskCount() - executor.getCompletedTaskCount()));
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadPoolMonitoringExample example = new ThreadPoolMonitoringExample();
        example.demonstrateMonitoring();
    }
}
```

## 7.9 Thread Pool Tuning

Thread pool tuning involves adjusting parameters to optimize performance for specific workloads. The optimal configuration depends on the nature of tasks and system resources.

### Tuning Parameters:

**1. Pool Size Tuning:**
- CPU-bound tasks: Number of CPU cores
- I/O-bound tasks: Higher than CPU cores
- Mixed workloads: Experiment with different values

**2. Queue Tuning:**
- Bounded queues: Prevent memory issues
- Unbounded queues: Better throughput
- Priority queues: Task prioritization

**3. Thread Lifecycle Tuning:**
- Keep-alive time: Thread reuse
- Core thread timeout: Resource management
- Thread factory: Custom thread creation

### Java Example - Thread Pool Tuning:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

public class ThreadPoolTuningExample {
    public void demonstrateTuning() throws InterruptedException {
        System.out.println("=== Thread Pool Tuning Comparison ===");
        
        // Test different configurations
        testConfiguration("Small Pool", 2, 4, 10);
        testConfiguration("Medium Pool", 4, 8, 20);
        testConfiguration("Large Pool", 8, 16, 50);
        testConfiguration("CPU Optimized", Runtime.getRuntime().availableProcessors(), 
                         Runtime.getRuntime().availableProcessors() * 2, 100);
    }
    
    private void testConfiguration(String name, int coreSize, int maxSize, int queueSize) 
            throws InterruptedException {
        System.out.println("\n--- " + name + " (Core: " + coreSize + ", Max: " + maxSize + 
                          ", Queue: " + queueSize + ") ---");
        
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            coreSize, maxSize, 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(queueSize)
        );
        
        long startTime = System.currentTimeMillis();
        AtomicLong completedTasks = new AtomicLong(0);
        
        // Submit tasks
        for (int i = 0; i < 50; i++) {
            final int taskId = i;
            try {
                executor.submit(() -> {
                    try {
                        // Simulate mixed workload
                        if (taskId % 3 == 0) {
                            // CPU-intensive
                            long sum = 0;
                            for (int j = 0; j < 1000000; j++) {
                                sum += j;
                            }
                        } else {
                            // I/O-intensive
                            Thread.sleep(100);
                        }
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    completedTasks.incrementAndGet();
                });
            } catch (RejectedExecutionException e) {
                System.out.println("Task " + taskId + " rejected");
            }
        }
        
        executor.shutdown();
        executor.awaitTermination(30, TimeUnit.SECONDS);
        
        long endTime = System.currentTimeMillis();
        System.out.println("Completed tasks: " + completedTasks.get());
        System.out.println("Execution time: " + (endTime - startTime) + "ms");
        System.out.println("Throughput: " + (completedTasks.get() * 1000.0 / (endTime - startTime)) + " tasks/sec");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadPoolTuningExample example = new ThreadPoolTuningExample();
        example.demonstrateTuning();
    }
}
```

## 7.10 Thread Pool Best Practices

Following best practices ensures efficient, maintainable, and robust thread pool usage in production applications.

### Best Practices:

**1. Proper Shutdown:**
- Always shutdown executors
- Use awaitTermination() for graceful shutdown
- Handle shutdownNow() for forced shutdown

**2. Exception Handling:**
- Handle exceptions in tasks
- Use UncaughtExceptionHandler
- Monitor for thread deaths

**3. Resource Management:**
- Don't create too many thread pools
- Reuse executors when possible
- Monitor resource usage

### Java Example - Best Practices:

```java
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;

public class ThreadPoolBestPracticesExample {
    private final AtomicInteger taskCounter = new AtomicInteger(0);
    
    public void demonstrateBestPractices() throws InterruptedException {
        // Best Practice 1: Proper shutdown
        demonstrateProperShutdown();
        
        // Best Practice 2: Exception handling
        demonstrateExceptionHandling();
        
        // Best Practice 3: Resource management
        demonstrateResourceManagement();
    }
    
    private void demonstrateProperShutdown() throws InterruptedException {
        System.out.println("=== Proper Shutdown ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Submit tasks
        for (int i = 0; i < 5; i++) {
            executor.submit(createTask("Shutdown"));
        }
        
        // Proper shutdown sequence
        executor.shutdown(); // No more tasks accepted
        
        try {
            // Wait for tasks to complete
            if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                System.out.println("Tasks did not complete, forcing shutdown");
                executor.shutdownNow(); // Force shutdown
                
                // Wait a bit more
                if (!executor.awaitTermination(1, TimeUnit.SECONDS)) {
                    System.out.println("Executor did not terminate");
                }
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
        
        System.out.println("Executor shutdown completed");
    }
    
    private void demonstrateExceptionHandling() throws InterruptedException {
        System.out.println("\n=== Exception Handling ===");
        
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2, 4, 60L, TimeUnit.SECONDS,
            new LinkedBlockingQueue<>(10),
            new ThreadFactory() {
                private final AtomicInteger threadNumber = new AtomicInteger(1);
                @Override
                public Thread newThread(Runnable r) {
                    Thread thread = new Thread(r, "ExceptionHandlingThread-" + threadNumber.getAndIncrement());
                    thread.setUncaughtExceptionHandler((t, e) -> {
                        System.out.println("Uncaught exception in thread " + t.getName() + ": " + e.getMessage());
                    });
                    return thread;
                }
            }
        );
        
        // Submit tasks that may throw exceptions
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                if (taskId % 2 == 0) {
                    throw new RuntimeException("Simulated exception in task " + taskId);
                }
                System.out.println("Task " + taskId + " completed successfully");
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstrateResourceManagement() throws InterruptedException {
        System.out.println("\n=== Resource Management ===");
        
        // Good: Reuse executor
        ExecutorService sharedExecutor = Executors.newFixedThreadPool(4);
        
        // Submit tasks to shared executor
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            sharedExecutor.submit(() -> {
                System.out.println("Task " + taskId + " executed by shared executor");
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        sharedExecutor.shutdown();
        sharedExecutor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("Resource management demonstration completed");
    }
    
    private Runnable createTask(String type) {
        return () -> {
            int taskId = taskCounter.incrementAndGet();
            System.out.println(type + " task " + taskId + " executed by " + 
                             Thread.currentThread().getName());
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        };
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadPoolBestPracticesExample example = new ThreadPoolBestPracticesExample();
        example.demonstrateBestPractices();
    }
}
```

### Real-World Analogy:
Think of thread pool best practices like managing a professional kitchen:
- **Proper Shutdown**: Like closing the kitchen properly - finish current orders, clean up, and turn off equipment
- **Exception Handling**: Like having proper safety procedures when something goes wrong
- **Resource Management**: Like not having too many chefs or too few, and reusing equipment efficiently

Following these practices ensures your "kitchen" (thread pool) runs smoothly and efficiently!