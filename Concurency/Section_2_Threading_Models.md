# Section 2 – Threading Models

## 2.1 User-Level Threads

User-level threads are threads that are managed entirely by the application or user-level library, without direct kernel involvement. The operating system is unaware of these threads and only sees the process as a single unit of execution.

### Key Concepts
- **User Space Management**: Threads are created, scheduled, and managed in user space
- **Fast Operations**: Thread operations are very fast since they don't require kernel calls
- **Blocking Problem**: If one thread blocks, the entire process blocks
- **No True Parallelism**: Cannot take advantage of multiple CPU cores

### Real-World Analogy
Think of a single worker who can rapidly switch between different tasks without needing permission from a supervisor. The worker is very efficient at task switching, but if they get stuck on one task, all other tasks must wait.

### Java Example
```java
public class UserLevelThreadsExample {
    // Simulating user-level threads with Java's green threads concept
    public static class UserLevelThread {
        private final String name;
        private final Runnable task;
        private volatile boolean running = false;
        private volatile boolean finished = false;
        
        public UserLevelThread(String name, Runnable task) {
            this.name = name;
            this.task = task;
        }
        
        public void start() {
            running = true;
            new Thread(() -> {
                System.out.println("User-level thread " + name + " started");
                try {
                    task.run();
                } catch (Exception e) {
                    System.err.println("Error in thread " + name + ": " + e.getMessage());
                } finally {
                    finished = true;
                    running = false;
                    System.out.println("User-level thread " + name + " finished");
                }
            }).start();
        }
        
        public boolean isRunning() { return running; }
        public boolean isFinished() { return finished; }
    }
    
    // User-level thread scheduler
    public static class UserLevelScheduler {
        private final List<UserLevelThread> threads = new ArrayList<>();
        private volatile boolean running = false;
        
        public void addThread(UserLevelThread thread) {
            threads.add(thread);
        }
        
        public void start() {
            running = true;
            System.out.println("User-level scheduler started");
            
            // Start all threads
            for (UserLevelThread thread : threads) {
                thread.start();
            }
            
            // Monitor threads
            while (running) {
                boolean allFinished = true;
                for (UserLevelThread thread : threads) {
                    if (thread.isRunning()) {
                        allFinished = false;
                        break;
                    }
                }
                
                if (allFinished) {
                    running = false;
                }
                
                try {
                    Thread.sleep(10);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            
            System.out.println("User-level scheduler finished");
        }
    }
    
    public static void demonstrateUserLevelThreads() {
        System.out.println("=== User-Level Threads Example ===");
        
        UserLevelScheduler scheduler = new UserLevelScheduler();
        
        // Create user-level threads
        scheduler.addThread(new UserLevelThread("Thread1", () -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("User-level Thread1: Task " + i);
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }));
        
        scheduler.addThread(new UserLevelThread("Thread2", () -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("User-level Thread2: Task " + i);
                try {
                    Thread.sleep(150);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }));
        
        scheduler.start();
    }
    
    public static void main(String[] args) {
        demonstrateUserLevelThreads();
    }
}
```

## 2.2 Kernel-Level Threads

Kernel-level threads are threads that are managed directly by the operating system kernel. The kernel is aware of each thread and can schedule them independently on different CPU cores.

### Key Concepts
- **Kernel Management**: Threads are created, scheduled, and managed by the OS kernel
- **True Parallelism**: Can run on multiple CPU cores simultaneously
- **Blocking Independence**: If one thread blocks, other threads can continue
- **Higher Overhead**: Thread operations require kernel calls

### Real-World Analogy
Think of multiple workers in a factory, each managed by a supervisor (kernel). Each worker can work independently on different machines, and if one worker gets stuck, the others can continue working.

### Java Example
```java
public class KernelLevelThreadsExample {
    // Java threads are kernel-level threads (on most modern JVMs)
    public static class KernelLevelThread extends Thread {
        private final String name;
        private final int workCount;
        
        public KernelLevelThread(String name, int workCount) {
            this.name = name;
            this.workCount = workCount;
        }
        
        @Override
        public void run() {
            System.out.println("Kernel-level thread " + name + " started on core: " + 
                             Thread.currentThread().getId());
            
            for (int i = 0; i < workCount; i++) {
                System.out.println("Kernel-level " + name + ": Task " + i + 
                                 " on thread " + Thread.currentThread().getId());
                
                // Simulate CPU-intensive work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            
            System.out.println("Kernel-level thread " + name + " finished");
        }
    }
    
    public static void demonstrateKernelLevelThreads() {
        System.out.println("=== Kernel-Level Threads Example ===");
        System.out.println("Available processors: " + Runtime.getRuntime().availableProcessors());
        
        // Create multiple kernel-level threads
        KernelLevelThread[] threads = new KernelLevelThread[4];
        
        for (int i = 0; i < threads.length; i++) {
            threads[i] = new KernelLevelThread("Thread" + (i + 1), 3);
        }
        
        // Start all threads - they can run in parallel on different cores
        for (KernelLevelThread thread : threads) {
            thread.start();
        }
        
        // Wait for all threads to complete
        for (KernelLevelThread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("All kernel-level threads completed");
    }
    
    // Demonstrate blocking independence
    public static void demonstrateBlockingIndependence() {
        System.out.println("\n=== Blocking Independence Example ===");
        
        Thread blockingThread = new Thread(() -> {
            System.out.println("Blocking thread started");
            try {
                Thread.sleep(3000); // Block for 3 seconds
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            System.out.println("Blocking thread finished");
        });
        
        Thread nonBlockingThread = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                System.out.println("Non-blocking thread: Task " + i);
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        blockingThread.start();
        nonBlockingThread.start();
        
        try {
            blockingThread.join();
            nonBlockingThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) {
        demonstrateKernelLevelThreads();
        demonstrateBlockingIndependence();
    }
}
```

## 2.3 Hybrid Threading Models

Hybrid threading models combine the benefits of user-level and kernel-level threads. They use a many-to-many mapping where multiple user-level threads are mapped to multiple kernel-level threads.

### Key Concepts
- **Many-to-Many Mapping**: Multiple user threads mapped to multiple kernel threads
- **Flexibility**: Can adjust the number of kernel threads based on workload
- **Performance**: Combines fast user-level operations with true parallelism
- **Complexity**: More complex to implement and manage

### Real-World Analogy
Think of a company with multiple departments (user-level threads) and multiple managers (kernel-level threads). The managers can assign work to different departments, and if one department gets busy, work can be redistributed to other departments.

### Java Example
```java
public class HybridThreadingModelExample {
    // Simulating hybrid model with Java's thread pool
    public static class HybridThreadManager {
        private final ExecutorService kernelThreadPool;
        private final int maxKernelThreads;
        private final AtomicInteger activeUserThreads = new AtomicInteger(0);
        
        public HybridThreadManager(int maxKernelThreads) {
            this.maxKernelThreads = maxKernelThreads;
            this.kernelThreadPool = Executors.newFixedThreadPool(maxKernelThreads);
        }
        
        public void submitUserThread(Runnable userTask) {
            activeUserThreads.incrementAndGet();
            kernelThreadPool.submit(() -> {
                try {
                    System.out.println("User thread executing on kernel thread: " + 
                                     Thread.currentThread().getId());
                    userTask.run();
                } finally {
                    activeUserThreads.decrementAndGet();
                }
            });
        }
        
        public int getActiveUserThreads() {
            return activeUserThreads.get();
        }
        
        public void shutdown() {
            kernelThreadPool.shutdown();
        }
    }
    
    // User-level thread simulation
    public static class UserLevelThread {
        private final String name;
        private final Runnable task;
        private volatile boolean running = false;
        
        public UserLevelThread(String name, Runnable task) {
            this.name = name;
            this.task = task;
        }
        
        public void start(HybridThreadManager manager) {
            running = true;
            manager.submitUserThread(() -> {
                System.out.println("User-level thread " + name + " started");
                try {
                    task.run();
                } catch (Exception e) {
                    System.err.println("Error in user thread " + name + ": " + e.getMessage());
                } finally {
                    running = false;
                    System.out.println("User-level thread " + name + " finished");
                }
            });
        }
        
        public boolean isRunning() { return running; }
    }
    
    public static void demonstrateHybridModel() {
        System.out.println("=== Hybrid Threading Model Example ===");
        
        HybridThreadManager manager = new HybridThreadManager(2); // 2 kernel threads
        
        // Create multiple user-level threads
        List<UserLevelThread> userThreads = new ArrayList<>();
        
        for (int i = 0; i < 6; i++) {
            final int threadId = i;
            UserLevelThread userThread = new UserLevelThread("UserThread" + threadId, () -> {
                for (int j = 0; j < 3; j++) {
                    System.out.println("UserThread" + threadId + ": Task " + j);
                    try {
                        Thread.sleep(200);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            userThreads.add(userThread);
        }
        
        // Start all user threads
        for (UserLevelThread userThread : userThreads) {
            userThread.start(manager);
        }
        
        // Monitor active threads
        for (int i = 0; i < 10; i++) {
            System.out.println("Active user threads: " + manager.getActiveUserThreads());
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
        
        manager.shutdown();
    }
    
    public static void main(String[] args) {
        demonstrateHybridModel();
    }
}
```

## 2.4 Green Threads

Green threads are user-level threads that are scheduled by a virtual machine or runtime environment rather than the operating system. They are called "green" because they are environmentally friendly in terms of resource usage.

### Key Concepts
- **VM Scheduling**: Threads are scheduled by the virtual machine
- **Lightweight**: Very low overhead for thread creation and switching
- **Cooperative**: Threads must yield control voluntarily
- **No True Parallelism**: Cannot utilize multiple CPU cores

### Real-World Analogy
Think of a single worker who can very quickly switch between different tasks without any overhead. The worker is extremely efficient but can only work on one task at a time, and they must remember to take breaks to let other tasks have a chance.

### Java Example
```java
public class GreenThreadsExample {
    // Simulating green threads with cooperative scheduling
    public static class GreenThread {
        private final String name;
        private final Runnable task;
        private volatile boolean running = false;
        private volatile boolean finished = false;
        private volatile boolean yielded = false;
        
        public GreenThread(String name, Runnable task) {
            this.name = name;
            this.task = task;
        }
        
        public void start() {
            running = true;
            System.out.println("Green thread " + name + " started");
        }
        
        public void yield() {
            yielded = true;
            System.out.println("Green thread " + name + " yielded");
        }
        
        public boolean isRunning() { return running && !finished; }
        public boolean isYielded() { return yielded; }
        public boolean isFinished() { return finished; }
        
        public void resetYield() { yielded = false; }
        
        public void execute() {
            if (running && !finished) {
                try {
                    task.run();
                    finished = true;
                    running = false;
                    System.out.println("Green thread " + name + " finished");
                } catch (Exception e) {
                    System.err.println("Error in green thread " + name + ": " + e.getMessage());
                    finished = true;
                    running = false;
                }
            }
        }
    }
    
    // Green thread scheduler
    public static class GreenThreadScheduler {
        private final List<GreenThread> threads = new ArrayList<>();
        private volatile boolean running = false;
        
        public void addThread(GreenThread thread) {
            threads.add(thread);
        }
        
        public void start() {
            running = true;
            System.out.println("Green thread scheduler started");
            
            // Start all threads
            for (GreenThread thread : threads) {
                thread.start();
            }
            
            // Cooperative scheduling loop
            while (running) {
                boolean allFinished = true;
                
                for (GreenThread thread : threads) {
                    if (thread.isRunning()) {
                        allFinished = false;
                        
                        if (!thread.isYielded()) {
                            // Execute a small portion of the thread
                            thread.execute();
                            
                            // Thread yields after some work
                            if (Math.random() < 0.3) { // 30% chance to yield
                                thread.yield();
                            }
                        } else {
                            // Reset yield after some time
                            if (Math.random() < 0.5) { // 50% chance to reset yield
                                thread.resetYield();
                            }
                        }
                    }
                }
                
                if (allFinished) {
                    running = false;
                }
                
                try {
                    Thread.sleep(10); // Small delay for cooperative scheduling
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            
            System.out.println("Green thread scheduler finished");
        }
    }
    
    public static void demonstrateGreenThreads() {
        System.out.println("=== Green Threads Example ===");
        
        GreenThreadScheduler scheduler = new GreenThreadScheduler();
        
        // Create green threads
        scheduler.addThread(new GreenThread("GreenThread1", () -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("GreenThread1: Task " + i);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }));
        
        scheduler.addThread(new GreenThread("GreenThread2", () -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("GreenThread2: Task " + i);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }));
        
        scheduler.start();
    }
    
    public static void main(String[] args) {
        demonstrateGreenThreads();
    }
}
```

## 2.5 Virtual Threads (Project Loom)

Virtual threads are a new feature in Java (Project Loom) that provides lightweight, user-mode threads that are managed by the JVM. They offer the benefits of both user-level and kernel-level threads.

### Key Concepts
- **Lightweight**: Millions of virtual threads can be created
- **JVM Managed**: Managed by the Java Virtual Machine
- **True Parallelism**: Can run on multiple CPU cores
- **Automatic Scheduling**: JVM handles scheduling automatically

### Real-World Analogy
Think of a massive office building with thousands of workers, but instead of each worker needing their own office, they can work in shared spaces and the building manager (JVM) efficiently assigns them to available workstations as needed.

### Java Example
```java
public class VirtualThreadsExample {
    // Virtual threads (Java 19+)
    public static void demonstrateVirtualThreads() {
        System.out.println("=== Virtual Threads Example ===");
        
        try {
            // Create virtual threads using Executors.newVirtualThreadPerTaskExecutor()
            ExecutorService virtualThreadExecutor = Executors.newVirtualThreadPerTaskExecutor();
            
            // Submit multiple tasks
            List<Future<String>> futures = new ArrayList<>();
            
            for (int i = 0; i < 10; i++) {
                final int taskId = i;
                Future<String> future = virtualThreadExecutor.submit(() -> {
                    System.out.println("Virtual thread " + taskId + " started");
                    try {
                        Thread.sleep(1000); // Simulate work
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    return "Task " + taskId + " completed";
                });
                futures.add(future);
            }
            
            // Wait for all tasks to complete
            for (Future<String> future : futures) {
                try {
                    String result = future.get();
                    System.out.println("Result: " + result);
                } catch (InterruptedException | ExecutionException e) {
                    System.err.println("Error: " + e.getMessage());
                }
            }
            
            virtualThreadExecutor.shutdown();
            
        } catch (Exception e) {
            System.out.println("Virtual threads not available in this Java version");
            System.out.println("This example requires Java 19 or later");
        }
    }
    
    // Traditional platform threads for comparison
    public static void demonstratePlatformThreads() {
        System.out.println("\n=== Platform Threads Example ===");
        
        ExecutorService platformThreadExecutor = Executors.newFixedThreadPool(10);
        
        List<Future<String>> futures = new ArrayList<>();
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            Future<String> future = platformThreadExecutor.submit(() -> {
                System.out.println("Platform thread " + taskId + " started");
                try {
                    Thread.sleep(1000); // Simulate work
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                return "Task " + taskId + " completed";
            });
            futures.add(future);
        }
        
        // Wait for all tasks to complete
        for (Future<String> future : futures) {
            try {
                String result = future.get();
                System.out.println("Result: " + result);
            } catch (InterruptedException | ExecutionException e) {
                System.err.println("Error: " + e.getMessage());
            }
        }
        
        platformThreadExecutor.shutdown();
    }
    
    public static void main(String[] args) {
        demonstrateVirtualThreads();
        demonstratePlatformThreads();
    }
}
```

## 2.6 Thread Pools

Thread pools are a collection of pre-created threads that can be reused to execute tasks, avoiding the overhead of creating and destroying threads for each task.

### Key Concepts
- **Pre-created Threads**: Threads are created once and reused
- **Task Queue**: Tasks are queued and assigned to available threads
- **Resource Management**: Limits the number of concurrent threads
- **Performance**: Reduces thread creation/destruction overhead

### Real-World Analogy
Think of a taxi company with a fleet of cars. Instead of buying a new car for each customer, the company maintains a pool of cars that can be assigned to customers as needed. When a customer is done, the car returns to the pool for the next customer.

### Java Example
```java
public class ThreadPoolsExample {
    // Custom thread pool implementation
    public static class CustomThreadPool {
        private final int poolSize;
        private final List<Thread> threads;
        private final BlockingQueue<Runnable> taskQueue;
        private volatile boolean running = true;
        
        public CustomThreadPool(int poolSize) {
            this.poolSize = poolSize;
            this.threads = new ArrayList<>();
            this.taskQueue = new LinkedBlockingQueue<>();
            
            // Create worker threads
            for (int i = 0; i < poolSize; i++) {
                Thread worker = new Thread(() -> {
                    while (running) {
                        try {
                            Runnable task = taskQueue.take();
                            task.run();
                        } catch (InterruptedException e) {
                            Thread.currentThread().interrupt();
                            break;
                        }
                    }
                });
                worker.setName("Worker-" + i);
                threads.add(worker);
                worker.start();
            }
        }
        
        public void submit(Runnable task) {
            if (running) {
                taskQueue.offer(task);
            }
        }
        
        public void shutdown() {
            running = false;
            for (Thread thread : threads) {
                thread.interrupt();
            }
        }
    }
    
    // Using Java's built-in thread pools
    public static void demonstrateBuiltInThreadPools() {
        System.out.println("=== Built-in Thread Pools Example ===");
        
        // Fixed thread pool
        ExecutorService fixedPool = Executors.newFixedThreadPool(3);
        
        // Cached thread pool
        ExecutorService cachedPool = Executors.newCachedThreadPool();
        
        // Single thread executor
        ExecutorService singlePool = Executors.newSingleThreadExecutor();
        
        // Submit tasks to fixed pool
        System.out.println("Fixed Thread Pool (3 threads):");
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            fixedPool.submit(() -> {
                System.out.println("Fixed pool task " + taskId + " on thread: " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Submit tasks to cached pool
        System.out.println("\nCached Thread Pool:");
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            cachedPool.submit(() -> {
                System.out.println("Cached pool task " + taskId + " on thread: " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Submit tasks to single pool
        System.out.println("\nSingle Thread Pool:");
        for (int i = 0; i < 3; i++) {
            final int taskId = i;
            singlePool.submit(() -> {
                System.out.println("Single pool task " + taskId + " on thread: " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Shutdown pools
        fixedPool.shutdown();
        cachedPool.shutdown();
        singlePool.shutdown();
    }
    
    public static void demonstrateCustomThreadPool() {
        System.out.println("\n=== Custom Thread Pool Example ===");
        
        CustomThreadPool customPool = new CustomThreadPool(2);
        
        // Submit tasks
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            customPool.submit(() -> {
                System.out.println("Custom pool task " + taskId + " on thread: " + 
                                 Thread.currentThread().getName());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // Wait a bit then shutdown
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        customPool.shutdown();
    }
    
    public static void main(String[] args) {
        demonstrateBuiltInThreadPools();
        demonstrateCustomThreadPool();
    }
}
```

## 2.7 Thread Lifecycle Management

Thread lifecycle management involves understanding and controlling the different states a thread can be in during its lifetime.

### Key Concepts
- **Thread States**: NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED
- **State Transitions**: How threads move between different states
- **Lifecycle Control**: Starting, stopping, and monitoring threads
- **Resource Cleanup**: Properly cleaning up thread resources

### Real-World Analogy
Think of an employee's workday. They start in the morning (NEW), begin working (RUNNABLE), might wait for a meeting room (BLOCKED), wait for a colleague (WAITING), take a timed break (TIMED_WAITING), and finally go home (TERMINATED).

### Java Example
```java
public class ThreadLifecycleExample {
    // Thread state monitor
    public static class ThreadStateMonitor {
        private final Thread thread;
        private volatile boolean monitoring = true;
        
        public ThreadStateMonitor(Thread thread) {
            this.thread = thread;
        }
        
        public void startMonitoring() {
            new Thread(() -> {
                while (monitoring && thread.isAlive()) {
                    System.out.println("Thread " + thread.getName() + " state: " + thread.getState());
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
                System.out.println("Thread " + thread.getName() + " final state: " + thread.getState());
            }).start();
        }
        
        public void stopMonitoring() {
            monitoring = false;
        }
    }
    
    // Thread with different lifecycle states
    public static class LifecycleThread extends Thread {
        private final String name;
        private volatile boolean running = true;
        
        public LifecycleThread(String name) {
            this.name = name;
        }
        
        @Override
        public void run() {
            System.out.println(name + " started - State: " + getState());
            
            // RUNNABLE state
            for (int i = 0; i < 3 && running; i++) {
                System.out.println(name + " working - State: " + getState());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            
            // BLOCKED state (waiting for synchronized block)
            synchronized (this) {
                System.out.println(name + " in synchronized block - State: " + getState());
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
            
            // WAITING state
            try {
                System.out.println(name + " waiting - State: " + getState());
                wait(2000); // Wait for 2 seconds
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            // TIMED_WAITING state
            try {
                System.out.println(name + " timed waiting - State: " + getState());
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            System.out.println(name + " finished - State: " + getState());
        }
        
        public void stopThread() {
            running = false;
        }
    }
    
    public static void demonstrateThreadLifecycle() {
        System.out.println("=== Thread Lifecycle Example ===");
        
        LifecycleThread thread = new LifecycleThread("LifecycleThread");
        ThreadStateMonitor monitor = new ThreadStateMonitor(thread);
        
        // Start monitoring
        monitor.startMonitoring();
        
        // Start thread
        thread.start();
        
        // Wait for thread to complete
        try {
            thread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Stop monitoring
        monitor.stopMonitoring();
        
        System.out.println("Thread lifecycle demonstration completed");
    }
    
    // Thread interruption example
    public static void demonstrateThreadInterruption() {
        System.out.println("\n=== Thread Interruption Example ===");
        
        Thread interruptibleThread = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                System.out.println("Thread running...");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    System.out.println("Thread interrupted!");
                    Thread.currentThread().interrupt(); // Restore interrupt status
                    break;
                }
            }
            System.out.println("Thread finished");
        });
        
        interruptibleThread.start();
        
        // Let it run for a bit, then interrupt
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        interruptibleThread.interrupt();
        
        try {
            interruptibleThread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) {
        demonstrateThreadLifecycle();
        demonstrateThreadInterruption();
    }
}
```

## 2.8 Thread Local Storage

Thread Local Storage (TLS) provides each thread with its own copy of a variable, ensuring that each thread can access and modify its own version without interference from other threads.

### Key Concepts
- **Thread-Specific**: Each thread has its own copy of the variable
- **No Synchronization**: No need for locks or synchronization
- **Memory Management**: Automatic cleanup when thread terminates
- **Performance**: Fast access to thread-local data

### Real-World Analogy
Think of a classroom where each student has their own desk drawer. Each student can store their own belongings in their drawer without worrying about other students accessing or modifying their items.

### Java Example
```java
public class ThreadLocalStorageExample {
    // ThreadLocal for user context
    private static final ThreadLocal<String> userContext = new ThreadLocal<>();
    
    // ThreadLocal for request ID
    private static final ThreadLocal<String> requestId = new ThreadLocal<>();
    
    // ThreadLocal for counter
    private static final ThreadLocal<Integer> threadCounter = new ThreadLocal<Integer>() {
        @Override
        protected Integer initialValue() {
            return 0;
        }
    };
    
    // ThreadLocal for complex object
    private static final ThreadLocal<Map<String, Object>> threadData = new ThreadLocal<Map<String, Object>>() {
        @Override
        protected Map<String, Object> initialValue() {
            return new HashMap<>();
        }
    };
    
    // Service that uses ThreadLocal
    public static class UserService {
        public void setUserContext(String user) {
            userContext.set(user);
        }
        
        public String getCurrentUser() {
            return userContext.get();
        }
        
        public void clearUserContext() {
            userContext.remove();
        }
        
        public void processRequest(String request) {
            String currentUser = getCurrentUser();
            if (currentUser != null) {
                System.out.println("Processing request '" + request + "' for user: " + currentUser);
            } else {
                System.out.println("Processing request '" + request + "' for anonymous user");
            }
        }
    }
    
    // Request processor
    public static class RequestProcessor {
        public void processRequest(String request) {
            // Set request ID for this thread
            requestId.set("REQ-" + System.currentTimeMillis());
            
            System.out.println("Processing request: " + request + " with ID: " + requestId.get());
            
            // Simulate processing
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            System.out.println("Completed request: " + request + " with ID: " + requestId.get());
            
            // Clean up
            requestId.remove();
        }
    }
    
    // Counter service
    public static class CounterService {
        public void increment() {
            threadCounter.set(threadCounter.get() + 1);
        }
        
        public int getCount() {
            return threadCounter.get();
        }
        
        public void reset() {
            threadCounter.set(0);
        }
    }
    
    // Data service
    public static class DataService {
        public void setData(String key, Object value) {
            threadData.get().put(key, value);
        }
        
        public Object getData(String key) {
            return threadData.get().get(key);
        }
        
        public void clearData() {
            threadData.remove();
        }
    }
    
    public static void demonstrateThreadLocalStorage() {
        System.out.println("=== Thread Local Storage Example ===");
        
        UserService userService = new UserService();
        RequestProcessor requestProcessor = new RequestProcessor();
        CounterService counterService = new CounterService();
        DataService dataService = new DataService();
        
        // Test user context
        System.out.println("=== User Context Test ===");
        userService.setUserContext("John Doe");
        userService.processRequest("Get profile");
        
        userService.setUserContext("Jane Smith");
        userService.processRequest("Update settings");
        
        userService.clearUserContext();
        userService.processRequest("Public data");
        
        // Test request processing
        System.out.println("\n=== Request Processing Test ===");
        Thread requestThread1 = new Thread(() -> requestProcessor.processRequest("Request 1"));
        Thread requestThread2 = new Thread(() -> requestProcessor.processRequest("Request 2"));
        
        requestThread1.start();
        requestThread2.start();
        
        try {
            requestThread1.join();
            requestThread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Test counter
        System.out.println("\n=== Counter Test ===");
        Thread counterThread1 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                counterService.increment();
                System.out.println("Thread 1 counter: " + counterService.getCount());
            }
        });
        
        Thread counterThread2 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                counterService.increment();
                System.out.println("Thread 2 counter: " + counterService.getCount());
            }
        });
        
        counterThread1.start();
        counterThread2.start();
        
        try {
            counterThread1.join();
            counterThread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Test data service
        System.out.println("\n=== Data Service Test ===");
        Thread dataThread1 = new Thread(() -> {
            dataService.setData("name", "Thread 1");
            dataService.setData("id", 1);
            System.out.println("Thread 1 data: " + dataService.getData("name") + " - " + dataService.getData("id"));
        });
        
        Thread dataThread2 = new Thread(() -> {
            dataService.setData("name", "Thread 2");
            dataService.setData("id", 2);
            System.out.println("Thread 2 data: " + dataService.getData("name") + " - " + dataService.getData("id"));
        });
        
        dataThread1.start();
        dataThread2.start();
        
        try {
            dataThread1.join();
            dataThread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    public static void main(String[] args) {
        demonstrateThreadLocalStorage();
    }
}
```

This comprehensive explanation covers all the threading models, providing both theoretical understanding and practical Java examples to illustrate each concept. Each subsection builds upon the previous ones, creating a solid foundation for understanding different threading approaches and their trade-offs.