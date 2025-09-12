# Section 22 – Debugging Concurrent Code

## 22.1 Debugging Tools

Debugging concurrent code requires specialized tools that can handle multiple threads, race conditions, and timing-dependent issues.

### Key Concepts
- **Thread Debuggers**: Tools that can debug multiple threads simultaneously
- **Race Condition Detectors**: Tools that identify potential race conditions
- **Deadlock Detectors**: Tools that detect deadlock situations
- **Performance Profilers**: Tools that analyze thread performance

### Real-World Analogy
Think of debugging a complex machine with multiple moving parts. You need specialized tools like multimeters, oscilloscopes, and thermal cameras to see what's happening in different parts simultaneously, rather than just looking at one component at a time.

### Java Example
```java
// Debugging tools demonstration
public class ConcurrentDebuggingTools {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    private int counter = 0;
    
    // Method that can cause deadlock
    public void method1() {
        synchronized (lock1) {
            System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock1");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            synchronized (lock2) {
                System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock2");
                counter++;
            }
        }
    }
    
    public void method2() {
        synchronized (lock2) {
            System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock2");
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            synchronized (lock1) {
                System.out.println("Thread " + Thread.currentThread().getName() + " acquired lock1");
                counter++;
            }
        }
    }
    
    // Debugging helper methods
    public void printThreadInfo() {
        Thread currentThread = Thread.currentThread();
        System.out.println("Thread: " + currentThread.getName());
        System.out.println("State: " + currentThread.getState());
        System.out.println("Priority: " + currentThread.getPriority());
        System.out.println("Is Daemon: " + currentThread.isDaemon());
    }
    
    public void printLockInfo() {
        System.out.println("Lock1: " + lock1);
        System.out.println("Lock2: " + lock2);
        System.out.println("Counter: " + counter);
    }
}
```

## 22.2 Race Condition Debugging

Race conditions are among the most difficult bugs to debug because they depend on timing and may not occur consistently.

### Key Concepts
- **Heisenbugs**: Bugs that disappear when you try to debug them
- **Timing Dependencies**: Bugs that only occur under specific timing conditions
- **Reproducibility**: Making race conditions reproducible for debugging
- **Logging**: Using detailed logging to track execution order

### Real-World Analogy
Think of debugging a traffic intersection where accidents only happen when specific cars arrive at the same time. The accident might not happen every time you test it, but when it does, it's because of the specific timing of when cars arrive.

### Java Example
```java
// Race condition debugging
public class RaceConditionDebugging {
    private int counter = 0;
    private final Object lock = new Object();
    private final List<String> executionLog = Collections.synchronizedList(new ArrayList<>());
    
    // Vulnerable method with race condition
    public void incrementVulnerable() {
        int temp = counter;
        logExecution("Read counter: " + temp);
        
        // Simulate some processing
        try {
            Thread.sleep(1);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        counter = temp + 1;
        logExecution("Wrote counter: " + counter);
    }
    
    // Fixed method with synchronization
    public void incrementFixed() {
        synchronized (lock) {
            int temp = counter;
            logExecution("Read counter: " + temp);
            
            try {
                Thread.sleep(1);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            counter = temp + 1;
            logExecution("Wrote counter: " + counter);
        }
    }
    
    private void logExecution(String message) {
        String logEntry = Thread.currentThread().getName() + ": " + message + " at " + System.currentTimeMillis();
        executionLog.add(logEntry);
        System.out.println(logEntry);
    }
    
    public void printExecutionLog() {
        System.out.println("\nExecution Log:");
        for (String entry : executionLog) {
            System.out.println(entry);
        }
    }
    
    public int getCounter() {
        return counter;
    }
    
    public void reset() {
        counter = 0;
        executionLog.clear();
    }
}
```

## 22.3 Deadlock Debugging

Deadlocks occur when threads are waiting for each other indefinitely, creating a circular dependency.

### Key Concepts
- **Circular Wait**: Threads waiting for each other in a circle
- **Resource Ordering**: Preventing deadlocks by ordering resource acquisition
- **Timeout Mechanisms**: Using timeouts to break deadlocks
- **Deadlock Detection**: Identifying deadlock situations

### Real-World Analogy
Think of two people trying to pass through a narrow doorway. If both try to go through at the same time, they get stuck and neither can proceed. This is like a deadlock where both threads are waiting for each other.

### Java Example
```java
// Deadlock debugging
public class DeadlockDebugging {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    private final Map<String, String> threadLocks = new ConcurrentHashMap<>();
    
    // Method that can cause deadlock
    public void method1() {
        String threadName = Thread.currentThread().getName();
        System.out.println(threadName + " trying to acquire lock1");
        
        synchronized (lock1) {
            threadLocks.put(threadName, "lock1");
            System.out.println(threadName + " acquired lock1");
            
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            System.out.println(threadName + " trying to acquire lock2");
            synchronized (lock2) {
                threadLocks.put(threadName, "lock1,lock2");
                System.out.println(threadName + " acquired lock2");
                
                // Do work
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
        
        threadLocks.remove(threadName);
        System.out.println(threadName + " released all locks");
    }
    
    public void method2() {
        String threadName = Thread.currentThread().getName();
        System.out.println(threadName + " trying to acquire lock2");
        
        synchronized (lock2) {
            threadLocks.put(threadName, "lock2");
            System.out.println(threadName + " acquired lock2");
            
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            System.out.println(threadName + " trying to acquire lock1");
            synchronized (lock1) {
                threadLocks.put(threadName, "lock2,lock1");
                System.out.println(threadName + " acquired lock1");
                
                // Do work
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
        
        threadLocks.remove(threadName);
        System.out.println(threadName + " released all locks");
    }
    
    // Deadlock detection
    public void detectDeadlock() {
        System.out.println("\nCurrent thread locks:");
        for (Map.Entry<String, String> entry : threadLocks.entrySet()) {
            System.out.println(entry.getKey() + " holds: " + entry.getValue());
        }
        
        // Check for circular wait
        if (threadLocks.size() > 1) {
            System.out.println("Potential deadlock detected!");
        }
    }
    
    // Fixed method with ordered locking
    public void method1Fixed() {
        String threadName = Thread.currentThread().getName();
        System.out.println(threadName + " trying to acquire lock1");
        
        synchronized (lock1) {
            System.out.println(threadName + " acquired lock1");
            
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            System.out.println(threadName + " trying to acquire lock2");
            synchronized (lock2) {
                System.out.println(threadName + " acquired lock2");
                
                // Do work
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }
        
        System.out.println(threadName + " released all locks");
    }
}
```

## 22.4 Performance Profiling

Performance profiling helps identify bottlenecks and inefficiencies in concurrent code.

### Key Concepts
- **CPU Profiling**: Analyzing CPU usage patterns
- **Memory Profiling**: Analyzing memory allocation and usage
- **Thread Profiling**: Analyzing thread behavior and contention
- **Hotspot Analysis**: Identifying frequently executed code paths

### Real-World Analogy
Think of analyzing a factory's production line. You need to measure how long each station takes, how much energy is used, and where bottlenecks occur. Performance profiling works similarly by measuring how much time and resources each part of your code uses.

### Java Example
```java
// Performance profiling
public class PerformanceProfiling {
    private final Map<String, Long> methodTimes = new ConcurrentHashMap<>();
    private final Map<String, Integer> methodCalls = new ConcurrentHashMap<>();
    private final Map<String, Long> threadTimes = new ConcurrentHashMap<>();
    
    // Profiled method
    public void profiledMethod() {
        String methodName = "profiledMethod";
        long startTime = System.nanoTime();
        
        try {
            // Simulate work
            Thread.sleep(100);
            
            // Simulate CPU-intensive work
            for (int i = 0; i < 1000000; i++) {
                Math.sqrt(i);
            }
            
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        } finally {
            long endTime = System.nanoTime();
            long duration = endTime - startTime;
            
            // Record timing
            methodTimes.merge(methodName, duration, Long::sum);
            methodCalls.merge(methodName, 1, Integer::sum);
            
            // Record thread timing
            String threadName = Thread.currentThread().getName();
            threadTimes.merge(threadName, duration, Long::sum);
        }
    }
    
    // Memory profiling
    public void memoryProfiling() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        
        System.out.println("Total Memory: " + totalMemory / 1024 / 1024 + " MB");
        System.out.println("Free Memory: " + freeMemory / 1024 / 1024 + " MB");
        System.out.println("Used Memory: " + usedMemory / 1024 / 1024 + " MB");
        
        // Force garbage collection
        System.gc();
        
        long afterGcMemory = totalMemory - runtime.freeMemory();
        System.out.println("Used Memory after GC: " + afterGcMemory / 1024 / 1024 + " MB");
    }
    
    // Thread profiling
    public void threadProfiling() {
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        long[] threadIds = threadBean.getAllThreadIds();
        
        System.out.println("Thread Profiling:");
        System.out.println("=================");
        
        for (long threadId : threadIds) {
            ThreadInfo threadInfo = threadBean.getThreadInfo(threadId);
            if (threadInfo != null) {
                System.out.println("Thread: " + threadInfo.getThreadName());
                System.out.println("State: " + threadInfo.getThreadState());
                System.out.println("CPU Time: " + threadBean.getThreadCpuTime(threadId) / 1000000 + " ms");
                System.out.println("User Time: " + threadBean.getThreadUserTime(threadId) / 1000000 + " ms");
                System.out.println("---");
            }
        }
    }
    
    // Print profiling results
    public void printProfilingResults() {
        System.out.println("Method Profiling Results:");
        System.out.println("========================");
        
        for (Map.Entry<String, Long> entry : methodTimes.entrySet()) {
            String methodName = entry.getKey();
            Long totalTime = entry.getValue();
            Integer calls = methodCalls.get(methodName);
            
            if (calls != null && calls > 0) {
                double avgTime = (double) totalTime / calls / 1000000; // Convert to milliseconds
                System.out.println(methodName + ": " + calls + " calls, " + 
                                 totalTime / 1000000 + " ms total, " + 
                                 avgTime + " ms average");
            }
        }
        
        System.out.println("\nThread Profiling Results:");
        System.out.println("========================");
        
        for (Map.Entry<String, Long> entry : threadTimes.entrySet()) {
            System.out.println(entry.getKey() + ": " + entry.getValue() / 1000000 + " ms");
        }
    }
}
```

## 22.5 Memory Leak Detection

Memory leaks in concurrent code can be particularly problematic because they may not be immediately apparent.

### Key Concepts
- **Memory Leaks**: Memory that is allocated but never freed
- **Reference Cycles**: Circular references that prevent garbage collection
- **Thread Local Storage**: Memory leaks in thread-local variables
- **Event Listeners**: Memory leaks from unremoved event listeners

### Real-World Analogy
Think of a library where books are checked out but never returned. Over time, the library runs out of books even though they're not being used. Memory leaks work similarly where memory is allocated but never freed, eventually exhausting available memory.

### Java Example
```java
// Memory leak detection
public class MemoryLeakDetection {
    private final List<Object> memoryLeak = new ArrayList<>();
    private final Map<String, Object> cache = new ConcurrentHashMap<>();
    private final ThreadLocal<Object> threadLocal = new ThreadLocal<>();
    
    // Method that causes memory leak
    public void causeMemoryLeak() {
        // Add objects to list that never gets cleared
        for (int i = 0; i < 1000; i++) {
            memoryLeak.add(new Object());
        }
        
        // Add to cache without size limit
        String key = "key" + System.currentTimeMillis();
        cache.put(key, new byte[1024 * 1024]); // 1MB
        
        // Set thread local without clearing
        threadLocal.set(new byte[1024 * 1024]); // 1MB
    }
    
    // Method that fixes memory leak
    public void fixMemoryLeak() {
        // Clear the list
        memoryLeak.clear();
        
        // Limit cache size
        if (cache.size() > 100) {
            cache.clear();
        }
        
        // Clear thread local
        threadLocal.remove();
    }
    
    // Memory monitoring
    public void monitorMemory() {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory();
        long freeMemory = runtime.freeMemory();
        long usedMemory = totalMemory - freeMemory;
        long maxMemory = runtime.maxMemory();
        
        System.out.println("Memory Usage:");
        System.out.println("Total Memory: " + totalMemory / 1024 / 1024 + " MB");
        System.out.println("Free Memory: " + freeMemory / 1024 / 1024 + " MB");
        System.out.println("Used Memory: " + usedMemory / 1024 / 1024 + " MB");
        System.out.println("Max Memory: " + maxMemory / 1024 / 1024 + " MB");
        System.out.println("Memory Usage: " + (usedMemory * 100 / maxMemory) + "%");
        
        // Check for potential memory leak
        if (usedMemory > maxMemory * 0.8) {
            System.out.println("WARNING: High memory usage detected!");
        }
    }
    
    // Garbage collection monitoring
    public void monitorGarbageCollection() {
        List<GarbageCollectorMXBean> gcBeans = ManagementFactory.getGarbageCollectorMXBeans();
        
        System.out.println("Garbage Collection:");
        System.out.println("==================");
        
        for (GarbageCollectorMXBean gcBean : gcBeans) {
            System.out.println("GC Name: " + gcBean.getName());
            System.out.println("Collection Count: " + gcBean.getCollectionCount());
            System.out.println("Collection Time: " + gcBean.getCollectionTime() + " ms");
            System.out.println("---");
        }
    }
    
    // Memory leak detection
    public boolean detectMemoryLeak() {
        Runtime runtime = Runtime.getRuntime();
        long usedMemory = runtime.totalMemory() - runtime.freeMemory();
        long maxMemory = runtime.maxMemory();
        
        // Force garbage collection
        System.gc();
        System.runFinalization();
        System.gc();
        
        long usedMemoryAfterGc = runtime.totalMemory() - runtime.freeMemory();
        
        // If memory usage is still high after GC, there might be a leak
        if (usedMemoryAfterGc > maxMemory * 0.7) {
            System.out.println("Potential memory leak detected!");
            System.out.println("Memory usage after GC: " + usedMemoryAfterGc / 1024 / 1024 + " MB");
            return true;
        }
        
        return false;
    }
}
```

## 22.6 Thread Dump Analysis

Thread dumps provide snapshots of all threads in a JVM, helping identify deadlocks, performance issues, and other problems.

### Key Concepts
- **Thread States**: Different states threads can be in
- **Stack Traces**: Call stacks showing where threads are executing
- **Lock Information**: Information about locks held by threads
- **Deadlock Detection**: Identifying deadlock situations from thread dumps

### Real-World Analogy
Think of taking a photograph of a busy intersection during rush hour. The photo shows exactly where each car is, which direction it's going, and if any cars are stuck. A thread dump works similarly by showing exactly where each thread is and what it's doing.

### Java Example
```java
// Thread dump analysis
public class ThreadDumpAnalysis {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    public void generateThreadDump() {
        ThreadMXBean threadBean = ManagementFactory.getThreadMXBean();
        ThreadInfo[] threadInfos = threadBean.dumpAllThreads(true, true);
        
        System.out.println("Thread Dump Analysis:");
        System.out.println("====================");
        
        for (ThreadInfo threadInfo : threadInfos) {
            System.out.println("Thread: " + threadInfo.getThreadName());
            System.out.println("State: " + threadInfo.getThreadState());
            System.out.println("Priority: " + threadInfo.getPriority());
            System.out.println("Is Daemon: " + threadInfo.isDaemon());
            
            // Print stack trace
            StackTraceElement[] stackTrace = threadInfo.getStackTrace();
            System.out.println("Stack Trace:");
            for (StackTraceElement element : stackTrace) {
                System.out.println("  " + element);
            }
            
            // Print lock information
            if (threadInfo.getLockInfo() != null) {
                System.out.println("Lock: " + threadInfo.getLockInfo());
            }
            
            if (threadInfo.getLockOwnerName() != null) {
                System.out.println("Lock Owner: " + threadInfo.getLockOwnerName());
            }
            
            System.out.println("---");
        }
        
        // Check for deadlocks
        long[] deadlockedThreads = threadBean.findDeadlockedThreads();
        if (deadlockedThreads != null) {
            System.out.println("DEADLOCK DETECTED!");
            System.out.println("Deadlocked Threads: " + Arrays.toString(deadlockedThreads));
        }
    }
    
    // Method that can cause deadlock
    public void method1() {
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
    
    public void method2() {
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
```

## 22.7 Logging in Concurrent Systems

Effective logging is crucial for debugging concurrent systems, but it must be done carefully to avoid performance issues.

### Key Concepts
- **Thread-Safe Logging**: Ensuring logging doesn't cause race conditions
- **Performance Impact**: Minimizing the performance cost of logging
- **Log Levels**: Using appropriate log levels for different situations
- **Structured Logging**: Using structured formats for better analysis

### Real-World Analogy
Think of a security camera system in a building. You need cameras that can record multiple events simultaneously without interfering with each other, and you need to store the footage in a way that makes it easy to find specific events later.

### Java Example
```java
// Concurrent logging
public class ConcurrentLogging {
    private final Logger logger = LoggerFactory.getLogger(ConcurrentLogging.class);
    private final Map<String, String> context = new ConcurrentHashMap<>();
    private final ThreadLocal<String> threadId = new ThreadLocal<>();
    
    public void setThreadId(String id) {
        threadId.set(id);
    }
    
    public void logWithContext(String message) {
        String threadIdValue = threadId.get();
        if (threadIdValue != null) {
            logger.info("Thread {}: {}", threadIdValue, message);
        } else {
            logger.info(message);
        }
    }
    
    public void logWithStructuredData(String message, Map<String, Object> data) {
        StringBuilder sb = new StringBuilder();
        sb.append(message);
        
        if (data != null && !data.isEmpty()) {
            sb.append(" | ");
            data.forEach((key, value) -> sb.append(key).append("=").append(value).append(" "));
        }
        
        logger.info(sb.toString());
    }
    
    public void logPerformance(String operation, long duration) {
        Map<String, Object> data = new HashMap<>();
        data.put("operation", operation);
        data.put("duration", duration);
        data.put("thread", Thread.currentThread().getName());
        
        logWithStructuredData("Performance", data);
    }
    
    public void logError(String message, Throwable throwable) {
        Map<String, Object> data = new HashMap<>();
        data.put("thread", Thread.currentThread().getName());
        data.put("error", throwable.getMessage());
        
        logWithStructuredData(message, data);
        logger.error("Error details", throwable);
    }
    
    // Async logging to avoid blocking
    public void logAsync(String message) {
        CompletableFuture.runAsync(() -> {
            logger.info(message);
        });
    }
}
```

## 22.8 Monitoring and Observability

Monitoring and observability provide continuous insight into the health and performance of concurrent systems.

### Key Concepts
- **Metrics**: Quantitative measurements of system behavior
- **Logs**: Detailed records of events and activities
- **Traces**: Records of requests as they flow through the system
- **Alerts**: Notifications when something goes wrong

### Real-World Analogy
Think of a hospital's monitoring system. It continuously tracks vital signs (metrics), records all medical procedures (logs), traces patient journeys through different departments (traces), and alerts staff when something needs attention.

### Java Example
```java
// Monitoring and observability
public class ConcurrentMonitoring {
    private final MeterRegistry meterRegistry;
    private final Counter requestCounter;
    private final Timer requestTimer;
    private final Gauge activeThreads;
    private final Map<String, String> tags = new ConcurrentHashMap<>();
    
    public ConcurrentMonitoring(MeterRegistry meterRegistry) {
        this.meterRegistry = meterRegistry;
        this.requestCounter = Counter.builder("requests_total")
            .description("Total number of requests")
            .register(meterRegistry);
        
        this.requestTimer = Timer.builder("request_duration")
            .description("Request duration")
            .register(meterRegistry);
        
        this.activeThreads = Gauge.builder("active_threads")
            .description("Number of active threads")
            .register(meterRegistry, this, ConcurrentMonitoring::getActiveThreadCount);
    }
    
    public void recordRequest(String endpoint) {
        requestCounter.increment(Tags.of("endpoint", endpoint));
    }
    
    public void recordRequestDuration(String endpoint, long duration) {
        requestTimer.record(duration, TimeUnit.MILLISECONDS, Tags.of("endpoint", endpoint));
    }
    
    public void recordError(String errorType) {
        Counter.builder("errors_total")
            .description("Total number of errors")
            .tag("type", errorType)
            .register(meterRegistry)
            .increment();
    }
    
    public void recordMemoryUsage() {
        Runtime runtime = Runtime.getRuntime();
        long usedMemory = runtime.totalMemory() - runtime.freeMemory();
        long maxMemory = runtime.maxMemory();
        
        Gauge.builder("memory_used")
            .description("Used memory in bytes")
            .register(meterRegistry, usedMemory, Number::doubleValue);
        
        Gauge.builder("memory_usage_percent")
            .description("Memory usage percentage")
            .register(meterRegistry, (usedMemory * 100.0) / maxMemory, Number::doubleValue);
    }
    
    public void recordThreadPoolMetrics(ExecutorService executorService) {
        if (executorService instanceof ThreadPoolExecutor) {
            ThreadPoolExecutor tpe = (ThreadPoolExecutor) executorService;
            
            Gauge.builder("thread_pool_active")
                .description("Active threads in pool")
                .register(meterRegistry, tpe.getActiveCount(), Number::doubleValue);
            
            Gauge.builder("thread_pool_size")
                .description("Pool size")
                .register(meterRegistry, tpe.getPoolSize(), Number::doubleValue);
            
            Gauge.builder("thread_pool_queue_size")
                .description("Queue size")
                .register(meterRegistry, tpe.getQueue().size(), Number::doubleValue);
        }
    }
    
    private double getActiveThreadCount() {
        return Thread.activeCount();
    }
    
    public void generateHealthCheck() {
        Map<String, Object> health = new HashMap<>();
        
        // Check memory
        Runtime runtime = Runtime.getRuntime();
        long usedMemory = runtime.totalMemory() - runtime.freeMemory();
        long maxMemory = runtime.maxMemory();
        health.put("memory_usage_percent", (usedMemory * 100.0) / maxMemory);
        
        // Check threads
        health.put("active_threads", Thread.activeCount());
        
        // Check if system is healthy
        boolean isHealthy = (usedMemory * 100.0) / maxMemory < 80 && Thread.activeCount() < 100;
        health.put("healthy", isHealthy);
        
        System.out.println("Health Check: " + health);
    }
}
```

This comprehensive explanation covers all aspects of debugging concurrent code, providing both theoretical understanding and practical examples to illustrate each concept.