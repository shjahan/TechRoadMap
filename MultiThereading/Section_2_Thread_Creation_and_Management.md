# Section 2 - Thread Creation and Management

## 2.1 Thread Creation Methods

Creating threads is the fundamental step in multithreading. Java provides multiple ways to create and manage threads, each with its own advantages and use cases.

### Thread Creation Approaches:

#### 1. **Extending Thread Class**
- Inherit from Thread class
- Override run() method
- Simple but limits inheritance
- Not recommended for most cases

#### 2. **Implementing Runnable Interface**
- Implement Runnable interface
- Pass to Thread constructor
- Better design (composition over inheritance)
- Recommended approach

#### 3. **Using Lambda Expressions**
- Modern Java approach
- Concise syntax
- Functional programming style
- Most popular method

#### 4. **Using ExecutorService**
- High-level thread management
- Thread pool management
- Better resource control
- Enterprise applications

### Java Examples:

#### Extending Thread Class:
```java
public class ThreadExtensionExample extends Thread {
    private String threadName;
    
    public ThreadExtensionExample(String name) {
        this.threadName = name;
    }
    
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(threadName + " executing: " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                System.out.println(threadName + " interrupted");
                Thread.currentThread().interrupt();
                return;
            }
        }
    }
    
    public static void main(String[] args) {
        ThreadExtensionExample thread1 = new ThreadExtensionExample("Thread-1");
        ThreadExtensionExample thread2 = new ThreadExtensionExample("Thread-2");
        
        thread1.start();
        thread2.start();
    }
}
```

#### Implementing Runnable Interface:
```java
public class RunnableImplementationExample implements Runnable {
    private String threadName;
    
    public RunnableImplementationExample(String name) {
        this.threadName = name;
    }
    
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(threadName + " executing: " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                System.out.println(threadName + " interrupted");
                Thread.currentThread().interrupt();
                return;
            }
        }
    }
    
    public static void main(String[] args) {
        RunnableImplementationExample task1 = new RunnableImplementationExample("Task-1");
        RunnableImplementationExample task2 = new RunnableImplementationExample("Task-2");
        
        Thread thread1 = new Thread(task1);
        Thread thread2 = new Thread(task2);
        
        thread1.start();
        thread2.start();
    }
}
```

#### Using Lambda Expressions:
```java
public class LambdaThreadExample {
    public static void main(String[] args) {
        // Simple lambda thread
        Thread thread1 = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Lambda Thread executing: " + i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        });
        
        // Lambda with parameters
        String message = "Hello from lambda thread";
        Thread thread2 = new Thread(() -> {
            System.out.println(message);
            System.out.println("Thread ID: " + Thread.currentThread().getId());
        });
        
        thread1.start();
        thread2.start();
    }
}
```

#### Using ExecutorService:
```java
public class ExecutorServiceExample {
    public static void main(String[] args) {
        // Create thread pool
        ExecutorService executor = Executors.newFixedThreadPool(3);
        
        // Submit tasks
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
        
        // Shutdown executor
        executor.shutdown();
        try {
            if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}
```

### Real-World Analogy:
Think of thread creation methods like different ways to hire workers:
- **Extending Thread**: Like hiring someone who is already a "Worker" by birth
- **Implementing Runnable**: Like hiring someone who can "do work" (more flexible)
- **Lambda**: Like hiring someone on the spot for a specific task
- **ExecutorService**: Like having a staffing agency manage all your workers

## 2.2 Thread Lifecycle

Understanding the thread lifecycle is crucial for effective thread management. Threads go through various states during their execution.

### Thread States in Java:

#### 1. **NEW**
- Thread created but not started
- start() method not called yet
- No execution has begun

#### 2. **RUNNABLE**
- Thread is executing or ready to execute
- May be waiting for CPU time
- Active state of execution

#### 3. **BLOCKED**
- Thread waiting for a monitor lock
- Synchronized block or method
- Waiting for another thread to release lock

#### 4. **WAITING**
- Thread waiting indefinitely
- wait(), join(), or LockSupport.park()
- No timeout specified

#### 5. **TIMED_WAITING**
- Thread waiting with timeout
- sleep(), wait(timeout), join(timeout)
- Will wake up after specified time

#### 6. **TERMINATED**
- Thread has completed execution
- run() method finished
- Cannot be restarted

### Java Example - Thread Lifecycle:
```java
public class ThreadLifecycleExample {
    public static void main(String[] args) throws InterruptedException {
        Object lock = new Object();
        
        Thread thread = new Thread(() -> {
            System.out.println("Thread started - State: " + 
                             Thread.currentThread().getState());
            
            try {
                // Simulate work
                Thread.sleep(2000);
                
                // Wait for lock
                synchronized (lock) {
                    System.out.println("Thread acquired lock - State: " + 
                                     Thread.currentThread().getState());
                    Thread.sleep(1000);
                }
                
                System.out.println("Thread finished - State: " + 
                                 Thread.currentThread().getState());
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // NEW state
        System.out.println("Before start - State: " + thread.getState());
        
        thread.start();
        
        // RUNNABLE state
        System.out.println("After start - State: " + thread.getState());
        
        // Wait for thread to complete
        thread.join();
        
        // TERMINATED state
        System.out.println("After join - State: " + thread.getState());
    }
}
```

### Thread State Monitoring:
```java
public class ThreadStateMonitoring {
    public static void main(String[] args) throws InterruptedException {
        Object lock = new Object();
        
        Thread thread = new Thread(() -> {
            try {
                // Simulate different states
                Thread.sleep(1000); // TIMED_WAITING
                
                synchronized (lock) {
                    Thread.sleep(1000); // RUNNABLE
                }
                
                // Wait indefinitely
                synchronized (lock) {
                    lock.wait(); // WAITING
                }
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // Monitor thread states
        thread.start();
        
        for (int i = 0; i < 10; i++) {
            Thread.sleep(500);
            System.out.println("Thread state: " + thread.getState());
        }
        
        // Interrupt to wake up waiting thread
        thread.interrupt();
        thread.join();
    }
}
```

## 2.3 Thread States

Thread states represent the current condition of a thread in the JVM. Understanding these states helps in debugging and optimizing multithreaded applications.

### Detailed State Analysis:

#### NEW State:
```java
public class NewStateExample {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            System.out.println("Thread running");
        });
        
        System.out.println("Thread state: " + thread.getState()); // NEW
        System.out.println("Thread alive: " + thread.isAlive()); // false
    }
}
```

#### RUNNABLE State:
```java
public class RunnableStateExample {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Running: " + i + " - State: " + 
                                 Thread.currentThread().getState());
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        });
        
        thread.start();
        Thread.sleep(200);
        System.out.println("Thread state: " + thread.getState()); // RUNNABLE
        thread.join();
    }
}
```

#### BLOCKED State:
```java
public class BlockedStateExample {
    private static final Object lock = new Object();
    
    public static void main(String[] args) throws InterruptedException {
        // Thread that holds the lock
        Thread lockHolder = new Thread(() -> {
            synchronized (lock) {
                try {
                    Thread.sleep(3000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        // Thread that waits for the lock
        Thread lockWaiter = new Thread(() -> {
            synchronized (lock) {
                System.out.println("Got the lock!");
            }
        });
        
        lockHolder.start();
        Thread.sleep(100); // Ensure lockHolder gets the lock first
        lockWaiter.start();
        
        Thread.sleep(100);
        System.out.println("Lock waiter state: " + lockWaiter.getState()); // BLOCKED
        
        lockHolder.join();
        lockWaiter.join();
    }
}
```

#### WAITING State:
```java
public class WaitingStateExample {
    private static final Object lock = new Object();
    
    public static void main(String[] args) throws InterruptedException {
        Thread waitingThread = new Thread(() -> {
            synchronized (lock) {
                try {
                    lock.wait(); // WAITING state
                    System.out.println("Woken up!");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        });
        
        waitingThread.start();
        Thread.sleep(100);
        System.out.println("Waiting thread state: " + waitingThread.getState()); // WAITING
        
        // Wake up the waiting thread
        synchronized (lock) {
            lock.notify();
        }
        
        waitingThread.join();
    }
}
```

#### TIMED_WAITING State:
```java
public class TimedWaitingStateExample {
    public static void main(String[] args) throws InterruptedException {
        Thread sleepingThread = new Thread(() -> {
            try {
                Thread.sleep(2000); // TIMED_WAITING state
                System.out.println("Sleep completed");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        sleepingThread.start();
        Thread.sleep(100);
        System.out.println("Sleeping thread state: " + sleepingThread.getState()); // TIMED_WAITING
        
        sleepingThread.join();
        System.out.println("After completion state: " + sleepingThread.getState()); // TERMINATED
    }
}
```

## 2.4 Thread Priorities

Thread priorities help the scheduler decide which threads should run when multiple threads are competing for CPU time. However, priorities are hints, not guarantees.

### Priority Levels:
- **MIN_PRIORITY**: 1 (lowest priority)
- **NORM_PRIORITY**: 5 (default priority)
- **MAX_PRIORITY**: 10 (highest priority)

### Java Example - Thread Priorities:
```java
public class ThreadPriorityExample {
    public static void main(String[] args) throws InterruptedException {
        // Create threads with different priorities
        Thread lowPriorityThread = new Thread(new CounterTask("Low Priority"));
        Thread normalPriorityThread = new Thread(new CounterTask("Normal Priority"));
        Thread highPriorityThread = new Thread(new CounterTask("High Priority"));
        
        // Set priorities
        lowPriorityThread.setPriority(Thread.MIN_PRIORITY);
        normalPriorityThread.setPriority(Thread.NORM_PRIORITY);
        highPriorityThread.setPriority(Thread.MAX_PRIORITY);
        
        // Start threads
        lowPriorityThread.start();
        normalPriorityThread.start();
        highPriorityThread.start();
        
        // Let them run for a while
        Thread.sleep(5000);
        
        // Interrupt all threads
        lowPriorityThread.interrupt();
        normalPriorityThread.interrupt();
        highPriorityThread.interrupt();
        
        // Wait for completion
        lowPriorityThread.join();
        normalPriorityThread.join();
        highPriorityThread.join();
    }
    
    static class CounterTask implements Runnable {
        private String name;
        private int count = 0;
        
        public CounterTask(String name) {
            this.name = name;
        }
        
        @Override
        public void run() {
            while (!Thread.currentThread().isInterrupted()) {
                count++;
                if (count % 1000000 == 0) {
                    System.out.println(name + " (Priority: " + 
                                     Thread.currentThread().getPriority() + 
                                     "): " + count);
                }
            }
            System.out.println(name + " final count: " + count);
        }
    }
}
```

### Priority Inheritance:
```java
public class PriorityInheritanceExample {
    public static void main(String[] args) throws InterruptedException {
        Thread parentThread = new Thread(() -> {
            System.out.println("Parent thread priority: " + 
                             Thread.currentThread().getPriority());
            
            Thread childThread = new Thread(() -> {
                System.out.println("Child thread priority: " + 
                                 Thread.currentThread().getPriority());
            });
            
            childThread.start();
            try {
                childThread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        parentThread.setPriority(Thread.MAX_PRIORITY);
        parentThread.start();
        parentThread.join();
    }
}
```

## 2.5 Thread Naming

Giving meaningful names to threads helps in debugging and monitoring. Thread names should be descriptive and unique when possible.

### Thread Naming Methods:

#### 1. **Constructor Naming**
```java
public class ThreadNamingExample {
    public static void main(String[] args) {
        // Name in constructor
        Thread thread1 = new Thread(() -> {
            System.out.println("Thread name: " + Thread.currentThread().getName());
        }, "Worker-Thread-1");
        
        // Default naming
        Thread thread2 = new Thread(() -> {
            System.out.println("Thread name: " + Thread.currentThread().getName());
        });
        
        thread1.start();
        thread2.start();
    }
}
```

#### 2. **setName() Method**
```java
public class SetNameExample {
    public static void main(String[] args) {
        Thread thread = new Thread(() -> {
            System.out.println("Thread name: " + Thread.currentThread().getName());
        });
        
        thread.setName("Custom-Thread-Name");
        thread.start();
    }
}
```

#### 3. **Thread Factory**
```java
public class ThreadFactoryExample {
    public static void main(String[] args) {
        ThreadFactory customFactory = new ThreadFactory() {
            private int counter = 0;
            
            @Override
            public Thread newThread(Runnable r) {
                Thread thread = new Thread(r);
                thread.setName("Custom-Thread-" + (++counter));
                thread.setDaemon(true);
                return thread;
            }
        };
        
        ExecutorService executor = Executors.newFixedThreadPool(3, customFactory);
        
        for (int i = 0; i < 5; i++) {
            executor.submit(() -> {
                System.out.println("Thread name: " + Thread.currentThread().getName());
            });
        }
        
        executor.shutdown();
    }
}
```

### Real-World Analogy:
Think of thread naming like naming employees in a company:
- **Default names**: Like "Employee #12345" - not very helpful
- **Custom names**: Like "John Smith - Marketing Manager" - much more useful
- **Descriptive names**: Like "Database-Connection-Thread" - tells you exactly what it does

## 2.6 Thread Groups

Thread groups provide a way to organize threads hierarchically and manage them as a unit. However, they are largely deprecated in favor of ExecutorService.

### Thread Group Basics:
```java
public class ThreadGroupExample {
    public static void main(String[] args) throws InterruptedException {
        // Create thread group
        ThreadGroup workerGroup = new ThreadGroup("Worker Threads");
        
        // Create threads in the group
        Thread worker1 = new Thread(workerGroup, () -> {
            System.out.println("Worker 1 in group: " + 
                             Thread.currentThread().getThreadGroup().getName());
        }, "Worker-1");
        
        Thread worker2 = new Thread(workerGroup, () -> {
            System.out.println("Worker 2 in group: " + 
                             Thread.currentThread().getThreadGroup().getName());
        }, "Worker-2");
        
        worker1.start();
        worker2.start();
        
        // Wait for completion
        worker1.join();
        worker2.join();
        
        // Group information
        System.out.println("Group name: " + workerGroup.getName());
        System.out.println("Active threads: " + workerGroup.activeCount());
        System.out.println("Active groups: " + workerGroup.activeGroupCount());
    }
}
```

### Thread Group Management:
```java
public class ThreadGroupManagement {
    public static void main(String[] args) throws InterruptedException {
        ThreadGroup parentGroup = new ThreadGroup("Parent Group");
        ThreadGroup childGroup = new ThreadGroup(parentGroup, "Child Group");
        
        // Create threads in different groups
        Thread parentThread = new Thread(parentGroup, () -> {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, "Parent-Thread");
        
        Thread childThread = new Thread(childGroup, () -> {
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }, "Child-Thread");
        
        parentThread.start();
        childThread.start();
        
        // Monitor groups
        while (parentGroup.activeCount() > 0) {
            System.out.println("Parent group active threads: " + parentGroup.activeCount());
            System.out.println("Child group active threads: " + childGroup.activeCount());
            Thread.sleep(500);
        }
    }
}
```

## 2.7 Daemon Threads

Daemon threads are background threads that don't prevent the JVM from exiting. They are typically used for background tasks like garbage collection.

### Daemon Thread Characteristics:
- Automatically terminated when all non-daemon threads finish
- Cannot prevent JVM shutdown
- Used for background services
- Cannot be converted to non-daemon after start

### Java Example - Daemon Threads:
```java
public class DaemonThreadExample {
    public static void main(String[] args) throws InterruptedException {
        // Create daemon thread
        Thread daemonThread = new Thread(() -> {
            while (true) {
                System.out.println("Daemon thread running...");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        
        daemonThread.setDaemon(true);
        daemonThread.start();
        
        // Create non-daemon thread
        Thread userThread = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("User thread: " + i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        });
        
        userThread.start();
        userThread.join();
        
        // JVM will exit here, daemon thread will be terminated
        System.out.println("Main thread finished, JVM will exit");
    }
}
```

### Daemon Thread Use Cases:
```java
public class DaemonThreadUseCases {
    public static void main(String[] args) throws InterruptedException {
        // Background logging thread
        Thread loggingThread = new Thread(() -> {
            while (true) {
                // Simulate background logging
                System.out.println("Log: " + System.currentTimeMillis());
                try {
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        loggingThread.setDaemon(true);
        loggingThread.start();
        
        // Background cleanup thread
        Thread cleanupThread = new Thread(() -> {
            while (true) {
                // Simulate cleanup tasks
                System.out.println("Performing cleanup...");
                try {
                    Thread.sleep(10000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        });
        cleanupThread.setDaemon(true);
        cleanupThread.start();
        
        // Main application work
        Thread mainWork = new Thread(() -> {
            for (int i = 0; i < 3; i++) {
                System.out.println("Main work: " + i);
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        });
        
        mainWork.start();
        mainWork.join();
        
        System.out.println("Application finished, daemon threads will be terminated");
    }
}
```

## 2.8 Thread Termination

Proper thread termination is crucial for clean application shutdown. There are several ways to terminate threads safely.

### Thread Termination Methods:

#### 1. **Natural Termination**
```java
public class NaturalTerminationExample {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            for (int i = 0; i < 5; i++) {
                System.out.println("Working: " + i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
            System.out.println("Thread completed naturally");
        });
        
        thread.start();
        thread.join();
        System.out.println("Thread terminated: " + thread.getState());
    }
}
```

#### 2. **Interruption**
```java
public class InterruptionExample {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            while (!Thread.currentThread().isInterrupted()) {
                System.out.println("Working...");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    System.out.println("Interrupted, cleaning up...");
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        });
        
        thread.start();
        Thread.sleep(3000);
        thread.interrupt();
        thread.join();
        System.out.println("Thread terminated via interruption");
    }
}
```

#### 3. **Volatile Flag**
```java
public class VolatileFlagExample {
    private static volatile boolean shouldStop = false;
    
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            while (!shouldStop) {
                System.out.println("Working...");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
            System.out.println("Stopped via flag");
        });
        
        thread.start();
        Thread.sleep(3000);
        shouldStop = true;
        thread.join();
        System.out.println("Thread terminated via flag");
    }
}
```

## 2.9 Thread Cleanup

Proper cleanup ensures that resources are released and threads terminate gracefully without leaving orphaned resources.

### Cleanup Strategies:
```java
public class ThreadCleanupExample {
    private static volatile boolean running = true;
    
    public static void main(String[] args) throws InterruptedException {
        Thread workerThread = new Thread(() -> {
            // Resource that needs cleanup
            File tempFile = null;
            try {
                tempFile = File.createTempFile("worker", ".tmp");
                System.out.println("Created temp file: " + tempFile.getName());
                
                while (running) {
                    System.out.println("Working with file...");
                    Thread.sleep(1000);
                }
                
            } catch (IOException | InterruptedException e) {
                System.out.println("Exception in worker: " + e.getMessage());
                Thread.currentThread().interrupt();
            } finally {
                // Cleanup resources
                if (tempFile != null && tempFile.exists()) {
                    tempFile.delete();
                    System.out.println("Cleaned up temp file");
                }
                System.out.println("Worker thread cleanup completed");
            }
        });
        
        workerThread.start();
        
        // Let it run for a while
        Thread.sleep(3000);
        
        // Signal termination
        running = false;
        workerThread.interrupt();
        
        // Wait for cleanup
        workerThread.join();
        System.out.println("Main thread finished");
    }
}
```

### Shutdown Hook Example:
```java
public class ShutdownHookExample {
    public static void main(String[] args) throws InterruptedException {
        // Register shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            System.out.println("Shutdown hook executing...");
            // Perform cleanup operations
            System.out.println("Cleanup completed");
        }));
        
        // Simulate application work
        Thread worker = new Thread(() -> {
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        worker.start();
        worker.join();
        
        System.out.println("Application finished");
    }
}
```

## 2.10 Thread Management Best Practices

Following best practices ensures robust, maintainable, and efficient multithreaded applications.

### Best Practices:

#### 1. **Use ExecutorService Instead of Raw Threads**
```java
public class BestPracticesExample {
    public static void main(String[] args) throws InterruptedException {
        // Good: Use ExecutorService
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        try {
            for (int i = 0; i < 10; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    System.out.println("Task " + taskId + " executed by " + 
                                     Thread.currentThread().getName());
                });
            }
        } finally {
            executor.shutdown();
            if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        }
    }
}
```

#### 2. **Handle InterruptedException Properly**
```java
public class InterruptedExceptionHandling {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            try {
                while (!Thread.currentThread().isInterrupted()) {
                    // Do work
                    Thread.sleep(1000);
                }
            } catch (InterruptedException e) {
                // Restore interrupted status
                Thread.currentThread().interrupt();
                System.out.println("Thread interrupted, cleaning up...");
            }
        });
        
        thread.start();
        Thread.sleep(3000);
        thread.interrupt();
        thread.join();
    }
}
```

#### 3. **Use Thread-Safe Collections**
```java
public class ThreadSafeCollectionsExample {
    public static void main(String[] args) throws InterruptedException {
        // Good: Thread-safe collection
        List<String> threadSafeList = Collections.synchronizedList(new ArrayList<>());
        
        // Bad: Non-thread-safe collection
        // List<String> unsafeList = new ArrayList<>();
        
        ExecutorService executor = Executors.newFixedThreadPool(4);
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                threadSafeList.add("Task " + taskId);
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
        
        System.out.println("List size: " + threadSafeList.size());
    }
}
```

#### 4. **Avoid Thread Leaks**
```java
public class ThreadLeakPrevention {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        try {
            // Submit tasks
            for (int i = 0; i < 5; i++) {
                executor.submit(() -> {
                    System.out.println("Task executed");
                });
            }
        } finally {
            // Always shutdown executor
            executor.shutdown();
            
            // Wait for completion
            if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        }
    }
}
```

### Real-World Analogy:
Think of thread management like managing a construction crew:
- **Thread Creation**: Like hiring workers with specific skills
- **Thread Naming**: Like giving workers name tags so you can identify them
- **Thread Priorities**: Like assigning different urgency levels to tasks
- **Thread Groups**: Like organizing workers into different departments
- **Daemon Threads**: Like background workers who clean up after everyone leaves
- **Thread Termination**: Like properly dismissing workers at the end of the day
- **Thread Cleanup**: Like ensuring all tools are put away and areas are clean

Following these practices ensures your multithreaded application runs smoothly, just like a well-managed construction site.