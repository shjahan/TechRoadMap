# Section 14 - Thread Scheduling

## 14.1 Thread Scheduling Concepts

Thread scheduling is the process by which the operating system decides which thread should run at any given time. Understanding scheduling is crucial for optimizing multithreaded applications.

### Key Concepts:

**1. Scheduler:**
- Operating system component
- Decides thread execution order
- Manages CPU time allocation

**2. Scheduling Policies:**
- Preemptive vs cooperative
- Priority-based scheduling
- Fair scheduling

**3. Context Switching:**
- Switching between threads
- Overhead cost
- Performance impact

### Java Example - Thread Scheduling:

```java
public class ThreadSchedulingConcepts {
    public void demonstrateThreadScheduling() throws InterruptedException {
        // Create threads with different priorities
        Thread highPriorityThread = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println("High priority: " + i);
            }
        });
        highPriorityThread.setPriority(Thread.MAX_PRIORITY);
        
        Thread lowPriorityThread = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println("Low priority: " + i);
            }
        });
        lowPriorityThread.setPriority(Thread.MIN_PRIORITY);
        
        // Start threads
        highPriorityThread.start();
        lowPriorityThread.start();
        
        // Wait for completion
        highPriorityThread.join();
        lowPriorityThread.join();
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadSchedulingConcepts example = new ThreadSchedulingConcepts();
        example.demonstrateThreadScheduling();
    }
}
```

### Real-World Analogy:
Think of thread scheduling like managing a busy restaurant:
- **Scheduler**: Like the restaurant manager who decides which orders to prioritize
- **Priority**: Like VIP customers who get served first
- **Context Switching**: Like switching between different cooking stations

## 14.2 Preemptive Scheduling

Preemptive scheduling allows the operating system to interrupt a running thread and switch to another thread. This ensures fair CPU time distribution and responsiveness.

### Key Features:

**1. Interruption:**
- Threads can be interrupted
- No cooperation required
- Better responsiveness

**2. Time Slicing:**
- Fixed time quantum
- Fair CPU distribution
- Prevents starvation

**3. Priority Handling:**
- Higher priority threads preempt lower ones
- Dynamic priority adjustment
- Better system responsiveness

### Java Example - Preemptive Scheduling:

```java
public class PreemptiveSchedulingExample {
    public void demonstratePreemptiveScheduling() throws InterruptedException {
        // Create CPU-intensive threads
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                long startTime = System.currentTimeMillis();
                long sum = 0;
                for (int j = 0; j < 1000000000; j++) {
                    sum += j;
                }
                long endTime = System.currentTimeMillis();
                System.out.println("Thread " + threadId + " completed in " + 
                                 (endTime - startTime) + "ms");
            });
            threads[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        PreemptiveSchedulingExample example = new PreemptiveSchedulingExample();
        example.demonstratePreemptiveScheduling();
    }
}
```

## 14.3 Cooperative Scheduling

Cooperative scheduling requires threads to voluntarily yield control to other threads. This approach relies on threads being well-behaved and yielding appropriately.

### Key Features:

**1. Voluntary Yielding:**
- Threads must yield control
- No forced interruption
- Requires cooperation

**2. Performance:**
- Lower overhead
- No context switching cost
- Better for some workloads

**3. Risks:**
- Poorly behaved threads can block others
- Potential for starvation
- Less responsive

### Java Example - Cooperative Scheduling:

```java
public class CooperativeSchedulingExample {
    public void demonstrateCooperativeScheduling() throws InterruptedException {
        // Create threads that yield control
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    System.out.println("Thread " + threadId + ": " + j);
                    
                    // Cooperative yielding
                    if (j % 100 == 0) {
                        Thread.yield();
                    }
                }
            });
            threads[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        CooperativeSchedulingExample example = new CooperativeSchedulingExample();
        example.demonstrateCooperativeScheduling();
    }
}
```

## 14.4 Priority Scheduling

Priority scheduling assigns priorities to threads and schedules higher priority threads before lower priority ones. This ensures important tasks get CPU time first.

### Key Features:

**1. Priority Levels:**
- Thread priorities (1-10 in Java)
- Higher priority gets CPU first
- Dynamic priority adjustment

**2. Preemption:**
- Higher priority threads preempt lower ones
- Immediate scheduling
- Better responsiveness

**3. Starvation Prevention:**
- Priority aging
- Fair scheduling
- Prevents low priority starvation

### Java Example - Priority Scheduling:

```java
public class PrioritySchedulingExample {
    public void demonstratePriorityScheduling() throws InterruptedException {
        // Create threads with different priorities
        Thread highPriorityThread = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println("High priority: " + i);
            }
        });
        highPriorityThread.setPriority(Thread.MAX_PRIORITY);
        
        Thread normalPriorityThread = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println("Normal priority: " + i);
            }
        });
        normalPriorityThread.setPriority(Thread.NORM_PRIORITY);
        
        Thread lowPriorityThread = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println("Low priority: " + i);
            }
        });
        lowPriorityThread.setPriority(Thread.MIN_PRIORITY);
        
        // Start threads
        highPriorityThread.start();
        normalPriorityThread.start();
        lowPriorityThread.start();
        
        // Wait for completion
        highPriorityThread.join();
        normalPriorityThread.join();
        lowPriorityThread.join();
    }
    
    public static void main(String[] args) throws InterruptedException {
        PrioritySchedulingExample example = new PrioritySchedulingExample();
        example.demonstratePriorityScheduling();
    }
}
```

## 14.5 Round-Robin Scheduling

Round-robin scheduling gives each thread a fixed time slice and cycles through all threads in a circular manner. This ensures fair CPU time distribution.

### Key Features:

**1. Time Slicing:**
- Fixed time quantum
- Equal CPU time for all threads
- Fair scheduling

**2. Circular Queue:**
- Threads in a circular queue
- Cycle through all threads
- No thread left behind

**3. Performance:**
- Good for interactive systems
- Fair resource distribution
- Predictable behavior

### Java Example - Round-Robin Scheduling:

```java
public class RoundRobinSchedulingExample {
    public void demonstrateRoundRobinScheduling() throws InterruptedException {
        // Create multiple threads
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    System.out.println("Thread " + threadId + ": " + j);
                    
                    // Simulate work
                    try {
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }
                }
            });
            threads[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        RoundRobinSchedulingExample example = new RoundRobinSchedulingExample();
        example.demonstrateRoundRobinScheduling();
    }
}
```

## 14.6 Fair Scheduling

Fair scheduling ensures that all threads get equal CPU time and prevents starvation. It's particularly important in systems with many threads.

### Key Features:

**1. Equal Time:**
- All threads get equal CPU time
- No thread gets more than others
- Fair resource distribution

**2. Starvation Prevention:**
- No thread waits indefinitely
- Guaranteed execution time
- Better system stability

**3. Load Balancing:**
- Distributes load evenly
- Prevents bottlenecks
- Better performance

### Java Example - Fair Scheduling:

```java
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;

public class FairSchedulingExample {
    public void demonstrateFairScheduling() throws InterruptedException {
        // Use fair thread pool
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        // Submit tasks
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " started");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                System.out.println("Task " + taskId + " completed");
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(10, java.util.concurrent.TimeUnit.SECONDS);
    }
    
    public static void main(String[] args) throws InterruptedException {
        FairSchedulingExample example = new FairSchedulingExample();
        example.demonstrateFairScheduling();
    }
}
```

## 14.7 Real-Time Scheduling

Real-time scheduling is designed for systems with strict timing requirements. It ensures that critical tasks meet their deadlines.

### Key Features:

**1. Deadline Guarantees:**
- Tasks must complete by deadline
- Predictable timing
- Critical for real-time systems

**2. Priority Inversion:**
- Higher priority tasks can be blocked
- Priority inheritance
- Deadline monotonic scheduling

**3. Deterministic Behavior:**
- Predictable execution
- Bounded response times
- Real-time guarantees

### Java Example - Real-Time Scheduling:

```java
public class RealTimeSchedulingExample {
    public void demonstrateRealTimeScheduling() throws InterruptedException {
        // Create real-time tasks
        Thread realTimeTask = new Thread(() -> {
            long startTime = System.currentTimeMillis();
            System.out.println("Real-time task started at " + startTime);
            
            // Simulate real-time work
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            long endTime = System.currentTimeMillis();
            System.out.println("Real-time task completed at " + endTime + 
                             " (duration: " + (endTime - startTime) + "ms)");
        });
        
        realTimeTask.setPriority(Thread.MAX_PRIORITY);
        realTimeTask.start();
        realTimeTask.join();
    }
    
    public static void main(String[] args) throws InterruptedException {
        RealTimeSchedulingExample example = new RealTimeSchedulingExample();
        example.demonstrateRealTimeScheduling();
    }
}
```

## 14.8 NUMA-Aware Scheduling

NUMA-aware scheduling considers the Non-Uniform Memory Access architecture and schedules threads on the same NUMA node as their data.

### Key Features:

**1. NUMA Awareness:**
- Consider memory locality
- Schedule threads on same node
- Better performance

**2. Memory Affinity:**
- Keep data and threads together
- Reduce memory access latency
- Better cache utilization

**3. Load Balancing:**
- Balance load across NUMA nodes
- Prevent node overload
- Better scalability

### Java Example - NUMA-Aware Scheduling:

```java
public class NUMAwareSchedulingExample {
    public void demonstrateNUMAwareScheduling() throws InterruptedException {
        // Get number of processors
        int processors = Runtime.getRuntime().availableProcessors();
        System.out.println("Number of processors: " + processors);
        
        // Create threads for each processor
        Thread[] threads = new Thread[processors];
        for (int i = 0; i < processors; i++) {
            final int processorId = i;
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + processorId + " running on processor " + 
                                 Thread.currentThread().getName());
                
                // Simulate work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                
                System.out.println("Thread " + processorId + " completed with sum: " + sum);
            });
            threads[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    public static void main(String[] args) throws InterruptedException {
        NUMAwareSchedulingExample example = new NUMAwareSchedulingExample();
        example.demonstrateNUMAwareScheduling();
    }
}
```

## 14.9 Thread Scheduling Tuning

Thread scheduling tuning involves adjusting various parameters to optimize performance for specific workloads.

### Tuning Parameters:

**1. Thread Priorities:**
- Adjust thread priorities
- Balance between threads
- Optimize for workload

**2. Time Slices:**
- Adjust time quantum
- Balance responsiveness and overhead
- Optimize for workload

**3. Load Balancing:**
- Distribute load evenly
- Prevent bottlenecks
- Optimize resource usage

### Java Example - Thread Scheduling Tuning:

```java
public class ThreadSchedulingTuningExample {
    public void demonstrateSchedulingTuning() throws InterruptedException {
        // Tune thread priorities
        Thread highPriorityThread = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println("High priority: " + i);
            }
        });
        highPriorityThread.setPriority(Thread.MAX_PRIORITY);
        
        Thread lowPriorityThread = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println("Low priority: " + i);
            }
        });
        lowPriorityThread.setPriority(Thread.MIN_PRIORITY);
        
        // Start threads
        highPriorityThread.start();
        lowPriorityThread.start();
        
        // Wait for completion
        highPriorityThread.join();
        lowPriorityThread.join();
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadSchedulingTuningExample example = new ThreadSchedulingTuningExample();
        example.demonstrateSchedulingTuning();
    }
}
```

## 14.10 Thread Scheduling Best Practices

Following best practices ensures optimal thread scheduling and better performance.

### Best Practices:

**1. Appropriate Priorities:**
- Use appropriate thread priorities
- Don't overuse high priorities
- Balance between threads

**2. Avoid Starvation:**
- Ensure all threads get CPU time
- Use fair scheduling
- Monitor thread states

**3. Performance Monitoring:**
- Monitor thread performance
- Identify bottlenecks
- Optimize scheduling

### Java Example - Thread Scheduling Best Practices:

```java
import java.util.concurrent.Executors;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.TimeUnit;

public class ThreadSchedulingBestPracticesExample {
    public void demonstrateBestPractices() throws InterruptedException {
        // Best practice 1: Use appropriate thread priorities
        demonstrateAppropriatePriorities();
        
        // Best practice 2: Avoid starvation
        demonstrateStarvationPrevention();
        
        // Best practice 3: Performance monitoring
        demonstratePerformanceMonitoring();
    }
    
    private void demonstrateAppropriatePriorities() throws InterruptedException {
        System.out.println("=== Appropriate Priorities ===");
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + threadId + " with priority " + 
                                 Thread.currentThread().getPriority());
            });
            threads[i].setPriority(Thread.NORM_PRIORITY);
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
    }
    
    private void demonstrateStarvationPrevention() throws InterruptedException {
        System.out.println("\n=== Starvation Prevention ===");
        
        ExecutorService executor = Executors.newFixedThreadPool(5);
        
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Task " + taskId + " executed");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        executor.shutdown();
        executor.awaitTermination(5, TimeUnit.SECONDS);
    }
    
    private void demonstratePerformanceMonitoring() throws InterruptedException {
        System.out.println("\n=== Performance Monitoring ===");
        
        long startTime = System.currentTimeMillis();
        
        Thread[] threads = new Thread[5];
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                long threadStartTime = System.currentTimeMillis();
                
                // Simulate work
                long sum = 0;
                for (int j = 0; j < 1000000; j++) {
                    sum += j;
                }
                
                long threadEndTime = System.currentTimeMillis();
                System.out.println("Thread " + threadId + " completed in " + 
                                 (threadEndTime - threadStartTime) + "ms");
            });
            threads[i].start();
        }
        
        for (Thread thread : threads) {
            thread.join();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Total execution time: " + (endTime - startTime) + "ms");
    }
    
    public static void main(String[] args) throws InterruptedException {
        ThreadSchedulingBestPracticesExample example = new ThreadSchedulingBestPracticesExample();
        example.demonstrateBestPractices();
    }
}
```

### Real-World Analogy:
Think of thread scheduling like managing a busy restaurant:
- **Preemptive Scheduling**: Like the manager who can interrupt any chef to handle urgent orders
- **Cooperative Scheduling**: Like chefs who voluntarily help each other when they finish their tasks
- **Priority Scheduling**: Like VIP customers who get served first
- **Round-Robin Scheduling**: Like giving each chef equal time to work on orders
- **Fair Scheduling**: Like ensuring all customers get equal service
- **Real-Time Scheduling**: Like ensuring critical orders are completed on time
- **NUMA-Aware Scheduling**: Like keeping chefs close to their ingredients

The key is to choose the right scheduling strategy for your specific needs!