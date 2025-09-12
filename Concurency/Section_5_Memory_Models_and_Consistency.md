# Section 5 – Memory Models and Consistency

## 5.1 Sequential Consistency

Sequential consistency is a memory model where the result of any execution is the same as if the operations of all processors were executed in some sequential order, and the operations of each individual processor appear in this sequence in the order specified by its program.

### Key Characteristics
- **Program Order**: Operations within a thread appear to execute in program order
- **Global Order**: All threads see the same global order of operations
- **Simple Model**: Easy to reason about but may limit performance
- **Hardware Support**: Not always efficiently supported by modern processors

### Real-World Analogy
Think of a single-file line where everyone must wait for the person in front of them to complete their transaction before proceeding. The order is always the same for everyone.

### Java Example
```java
public class SequentialConsistencyExample {
    private static int x = 0;
    private static int y = 0;
    private static volatile boolean flag = false;
    
    // Thread 1
    public static void thread1() {
        x = 1;           // 1
        flag = true;     // 2
    }
    
    // Thread 2
    public static void thread2() {
        if (flag) {      // 3
            y = x;       // 4
        }
    }
    
    // With sequential consistency, if thread2 sees flag=true,
    // then y will always be 1 (not 0)
    public static void demonstrateSequentialConsistency() {
        Thread t1 = new Thread(() -> thread1());
        Thread t2 = new Thread(() -> thread2());
        
        t1.start();
        t2.start();
        
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("x=" + x + ", y=" + y + ", flag=" + flag);
    }
}
```

## 5.2 Relaxed Memory Models

Relaxed memory models allow for more aggressive optimizations by relaxing some ordering constraints, potentially improving performance but making reasoning more complex.

### Key Characteristics
- **Reordering**: Operations may be reordered for performance
- **Visibility**: Changes may not be immediately visible to other threads
- **Performance**: Better performance due to optimizations
- **Complexity**: More complex to reason about

### Real-World Analogy
Think of a busy restaurant where orders might be prepared out of sequence to optimize kitchen efficiency, but the final result still satisfies all customers.

### Java Example
```java
public class RelaxedMemoryModelExample {
    private static int x = 0;
    private static int y = 0;
    private static int a = 0;
    private static int b = 0;
    
    // Without proper synchronization, reordering can occur
    public static void demonstrateReordering() {
        Thread t1 = new Thread(() -> {
            x = 1;  // 1
            a = y;  // 2 - might be reordered with 1
        });
        
        Thread t2 = new Thread(() -> {
            y = 1;  // 3
            b = x;  // 4 - might be reordered with 3
        });
        
        t1.start();
        t2.start();
        
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // With reordering, both a and b could be 0
        System.out.println("a=" + a + ", b=" + b);
    }
    
    // Using volatile to prevent reordering
    private static volatile int volatileX = 0;
    private static volatile int volatileY = 0;
    private static volatile int volatileA = 0;
    private static volatile int volatileB = 0;
    
    public static void demonstrateVolatilePrevention() {
        Thread t1 = new Thread(() -> {
            volatileX = 1;  // 1
            volatileA = volatileY;  // 2 - cannot be reordered with 1
        });
        
        Thread t2 = new Thread(() -> {
            volatileY = 1;  // 3
            volatileB = volatileX;  // 4 - cannot be reordered with 3
        });
        
        t1.start();
        t2.start();
        
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("volatileA=" + volatileA + ", volatileB=" + volatileB);
    }
}
```

## 5.3 Happens-Before Relationships

Happens-before is a partial ordering on all actions within a program that determines when one action is guaranteed to be visible to another action.

### Key Concepts
- **Program Order**: Actions in the same thread happen in program order
- **Synchronization**: Synchronization actions create happens-before relationships
- **Transitivity**: If A happens-before B and B happens-before C, then A happens-before C
- **Visibility**: If A happens-before B, then A is visible to B

### Real-World Analogy
Think of a chain of events where each event must complete before the next one can begin, and everyone can see the results of previous events.

### Java Example
```java
public class HappensBeforeExample {
    private int x = 0;
    private int y = 0;
    private volatile boolean ready = false;
    
    // Writer thread
    public void writer() {
        x = 1;           // 1
        y = 2;           // 2
        ready = true;    // 3 - volatile write
    }
    
    // Reader thread
    public void reader() {
        if (ready) {     // 4 - volatile read
            int a = x;   // 5
            int b = y;   // 6
            System.out.println("x=" + a + ", y=" + b);
        }
    }
    
    // The volatile write in writer() happens-before the volatile read in reader()
    // This ensures that if reader() sees ready=true, it will also see x=1 and y=2
    
    public static void demonstrateHappensBefore() {
        HappensBeforeExample example = new HappensBeforeExample();
        
        Thread writer = new Thread(() -> example.writer());
        Thread reader = new Thread(() -> example.reader());
        
        reader.start();
        writer.start();
        
        try {
            reader.join();
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Synchronized blocks create happens-before relationships
    private final Object lock = new Object();
    private int synchronizedX = 0;
    private int synchronizedY = 0;
    
    public void synchronizedWriter() {
        synchronized (lock) {
            synchronizedX = 1;  // 1
            synchronizedY = 2;  // 2
        }  // 3 - end of synchronized block
    }
    
    public void synchronizedReader() {
        synchronized (lock) {  // 4 - synchronized block
            int a = synchronizedX;  // 5
            int b = synchronizedY;  // 6
            System.out.println("synchronizedX=" + a + ", synchronizedY=" + b);
        }
    }
}
```

## 5.4 Memory Ordering

Memory ordering defines the order in which memory operations become visible to other threads, affecting the consistency and performance of concurrent programs.

### Types of Memory Ordering
- **Sequential Consistency**: Strongest ordering, operations appear in program order
- **Acquire-Release**: Weaker ordering, provides synchronization
- **Relaxed**: Weakest ordering, allows reordering for performance
- **Consume**: Special ordering for dependent loads

### Real-World Analogy
Think of a news broadcast where the order of news items might be rearranged for better flow, but certain critical information must be presented in a specific sequence.

### Java Example
```java
public class MemoryOrderingExample {
    // Using volatile for acquire-release semantics
    private static volatile int volatileData = 0;
    private static volatile boolean volatileFlag = false;
    
    public static void demonstrateAcquireRelease() {
        Thread writer = new Thread(() -> {
            volatileData = 42;      // 1 - release
            volatileFlag = true;    // 2 - release
        });
        
        Thread reader = new Thread(() -> {
            if (volatileFlag) {     // 3 - acquire
                int data = volatileData;  // 4 - acquire
                System.out.println("Data: " + data);
            }
        });
        
        reader.start();
        writer.start();
        
        try {
            reader.join();
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Using synchronized for sequential consistency
    private static final Object lock = new Object();
    private static int synchronizedData = 0;
    private static boolean synchronizedFlag = false;
    
    public static void demonstrateSequentialConsistency() {
        Thread writer = new Thread(() -> {
            synchronized (lock) {
                synchronizedData = 42;      // 1
                synchronizedFlag = true;    // 2
            }
        });
        
        Thread reader = new Thread(() -> {
            synchronized (lock) {
                if (synchronizedFlag) {     // 3
                    int data = synchronizedData;  // 4
                    System.out.println("Synchronized Data: " + data);
                }
            }
        });
        
        reader.start();
        writer.start();
        
        try {
            reader.join();
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 5.5 Cache Coherence

Cache coherence ensures that all processors in a multiprocessor system see the same value for a shared memory location.

### Key Concepts
- **MESI Protocol**: Modified, Exclusive, Shared, Invalid states
- **Write-Through**: Writes go to both cache and memory
- **Write-Back**: Writes go to cache first, memory later
- **Snooping**: Caches monitor each other's transactions

### Real-World Analogy
Think of multiple people working on the same document, each with their own copy. When someone makes changes, all copies must be updated to maintain consistency.

### Java Example
```java
public class CacheCoherenceExample {
    // Shared data that will be accessed by multiple threads
    private static volatile int sharedData = 0;
    private static final int ITERATIONS = 1000000;
    
    // Thread that writes to shared data
    public static void writerThread() {
        for (int i = 0; i < ITERATIONS; i++) {
            sharedData = i;
        }
    }
    
    // Thread that reads from shared data
    public static void readerThread() {
        int localSum = 0;
        for (int i = 0; i < ITERATIONS; i++) {
            localSum += sharedData;
        }
        System.out.println("Reader sum: " + localSum);
    }
    
    public static void demonstrateCacheCoherence() {
        Thread writer = new Thread(() -> writerThread());
        Thread reader = new Thread(() -> readerThread());
        
        writer.start();
        reader.start();
        
        try {
            writer.join();
            reader.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Demonstrating false sharing
    public static class FalseSharingExample {
        // These variables are likely to be on the same cache line
        private static volatile int counter1 = 0;
        private static volatile int counter2 = 0;
        
        public static void thread1() {
            for (int i = 0; i < ITERATIONS; i++) {
                counter1++;
            }
        }
        
        public static void thread2() {
            for (int i = 0; i < ITERATIONS; i++) {
                counter2++;
            }
        }
        
        public static void demonstrateFalseSharing() {
            Thread t1 = new Thread(() -> thread1());
            Thread t2 = new Thread(() -> thread2());
            
            long startTime = System.currentTimeMillis();
            
            t1.start();
            t2.start();
            
            try {
                t1.join();
                t2.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            long endTime = System.currentTimeMillis();
            System.out.println("False sharing time: " + (endTime - startTime) + "ms");
        }
    }
}
```

## 5.6 False Sharing

False sharing occurs when multiple threads access different variables that happen to be on the same cache line, causing unnecessary cache invalidations.

### Key Concepts
- **Cache Line**: Unit of data transfer between cache and memory
- **Invalidation**: When one thread modifies a cache line, other threads must invalidate their copies
- **Performance Impact**: Can significantly degrade performance
- **Padding**: Adding padding to separate variables onto different cache lines

### Real-World Analogy
Think of two people working on different parts of the same page. When one person makes a change, the other person's work is also affected because they're working on the same physical page.

### Java Example
```java
public class FalseSharingExample {
    // Variables that might be on the same cache line
    private static volatile int counter1 = 0;
    private static volatile int counter2 = 0;
    
    // Padded variables to avoid false sharing
    private static volatile int paddedCounter1 = 0;
    private static volatile long padding1, padding2, padding3, padding4, padding5, padding6, padding7;
    private static volatile int paddedCounter2 = 0;
    
    public static void demonstrateFalseSharing() {
        // Test without padding
        long startTime = System.currentTimeMillis();
        
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                counter1++;
            }
        });
        
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                counter2++;
            }
        });
        
        t1.start();
        t2.start();
        
        try {
            t1.join();
            t2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        long endTime = System.currentTimeMillis();
        System.out.println("Without padding time: " + (endTime - startTime) + "ms");
        
        // Test with padding
        startTime = System.currentTimeMillis();
        
        Thread t3 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                paddedCounter1++;
            }
        });
        
        Thread t4 = new Thread(() -> {
            for (int i = 0; i < 1000000; i++) {
                paddedCounter2++;
            }
        });
        
        t3.start();
        t4.start();
        
        try {
            t3.join();
            t4.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        endTime = System.currentTimeMillis();
        System.out.println("With padding time: " + (endTime - startTime) + "ms");
    }
    
    // Using @Contended annotation (Java 8+)
    public static class ContendedExample {
        @sun.misc.Contended
        private static volatile int contendedCounter1 = 0;
        
        @sun.misc.Contended
        private static volatile int contendedCounter2 = 0;
        
        public static void demonstrateContended() {
            Thread t1 = new Thread(() -> {
                for (int i = 0; i < 1000000; i++) {
                    contendedCounter1++;
                }
            });
            
            Thread t2 = new Thread(() -> {
                for (int i = 0; i < 1000000; i++) {
                    contendedCounter2++;
                }
            });
            
            t1.start();
            t2.start();
            
            try {
                t1.join();
                t2.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
```

## 5.7 Memory Visibility

Memory visibility ensures that changes made by one thread are visible to other threads, which is crucial for correct concurrent programming.

### Key Concepts
- **Visibility**: Changes must be visible to other threads
- **Synchronization**: Proper synchronization ensures visibility
- **Volatile**: Volatile variables provide visibility guarantees
- **Happens-Before**: Visibility is guaranteed by happens-before relationships

### Real-World Analogy
Think of a notice board where important announcements are posted. Everyone needs to be able to see the latest announcements, but without proper mechanisms, some people might miss updates.

### Java Example
```java
public class MemoryVisibilityExample {
    // Without proper synchronization, changes might not be visible
    private static int data = 0;
    private static boolean ready = false;
    
    // With volatile, changes are guaranteed to be visible
    private static volatile int volatileData = 0;
    private static volatile boolean volatileReady = false;
    
    // Without synchronization - visibility issues
    public static void demonstrateVisibilityIssues() {
        Thread writer = new Thread(() -> {
            data = 42;        // 1
            ready = true;     // 2
        });
        
        Thread reader = new Thread(() -> {
            while (!ready) {  // 3 - might not see the change
                // Busy wait
            }
            System.out.println("Data: " + data);  // 4 - might not see the change
        });
        
        reader.start();
        writer.start();
        
        try {
            reader.join();
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // With volatile - visibility guaranteed
    public static void demonstrateVolatileVisibility() {
        Thread writer = new Thread(() -> {
            volatileData = 42;        // 1
            volatileReady = true;     // 2
        });
        
        Thread reader = new Thread(() -> {
            while (!volatileReady) {  // 3 - guaranteed to see the change
                // Busy wait
            }
            System.out.println("Volatile Data: " + volatileData);  // 4 - guaranteed to see the change
        });
        
        reader.start();
        writer.start();
        
        try {
            reader.join();
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Using synchronized for visibility
    private static final Object lock = new Object();
    private static int synchronizedData = 0;
    private static boolean synchronizedReady = false;
    
    public static void demonstrateSynchronizedVisibility() {
        Thread writer = new Thread(() -> {
            synchronized (lock) {
                synchronizedData = 42;        // 1
                synchronizedReady = true;     // 2
            }
        });
        
        Thread reader = new Thread(() -> {
            synchronized (lock) {
                while (!synchronizedReady) {  // 3 - guaranteed to see the change
                    // Busy wait
                }
                System.out.println("Synchronized Data: " + synchronizedData);  // 4 - guaranteed to see the change
            }
        });
        
        reader.start();
        writer.start();
        
        try {
            reader.join();
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 5.8 Volatile Variables

Volatile variables provide visibility guarantees and prevent certain reorderings, making them useful for simple synchronization scenarios.

### Key Characteristics
- **Visibility**: Changes are immediately visible to all threads
- **No Reordering**: Volatile operations cannot be reordered with each other
- **No Atomicity**: Volatile does not provide atomicity for compound operations
- **Performance**: Volatile reads/writes are generally faster than synchronized blocks

### Real-World Analogy
Think of a flag that's visible to everyone in a room. When someone changes the flag, everyone can immediately see the change, but the flag itself doesn't prevent multiple people from trying to change it simultaneously.

### Java Example
```java
public class VolatileVariablesExample {
    // Volatile variables
    private static volatile boolean flag = false;
    private static volatile int counter = 0;
    private static volatile String message = null;
    
    // Simple flag-based synchronization
    public static void demonstrateVolatileFlag() {
        Thread writer = new Thread(() -> {
            try {
                Thread.sleep(1000); // Simulate work
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            message = "Hello from writer!";
            flag = true; // Signal that message is ready
        });
        
        Thread reader = new Thread(() -> {
            while (!flag) { // Wait for flag
                // Busy wait
            }
            System.out.println("Message: " + message);
        });
        
        reader.start();
        writer.start();
        
        try {
            reader.join();
            writer.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    // Volatile counter (not thread-safe for increments)
    public static void demonstrateVolatileCounter() {
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter++; // Not atomic! Race condition possible
                }
            });
            threads[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Final counter value: " + counter); // Likely not 5000
    }
    
    // Volatile with proper synchronization
    private static final Object lock = new Object();
    private static volatile int volatileCounter = 0;
    
    public static void demonstrateVolatileWithSynchronization() {
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    synchronized (lock) {
                        volatileCounter++; // Atomic increment
                    }
                }
            });
            threads[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : threads) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Final volatile counter value: " + volatileCounter); // Will be 5000
    }
    
    // Double-checked locking with volatile
    public static class Singleton {
        private static volatile Singleton instance;
        
        private Singleton() {}
        
        public static Singleton getInstance() {
            if (instance == null) { // First check
                synchronized (Singleton.class) {
                    if (instance == null) { // Second check
                        instance = new Singleton();
                    }
                }
            }
            return instance;
        }
    }
}
```

This comprehensive explanation covers all aspects of memory models and consistency, providing both theoretical understanding and practical Java examples to illustrate each concept.