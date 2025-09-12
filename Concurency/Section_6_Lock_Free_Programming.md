# Section 6 – Lock-Free Programming

## 6.1 Lock-Free Algorithms

Lock-free algorithms are algorithms that guarantee that at least one thread will make progress, even if other threads are delayed or fail, without using traditional locking mechanisms.

### Key Characteristics
- **Progress Guarantee**: At least one thread makes progress
- **No Blocking**: Threads never block waiting for locks
- **Atomic Operations**: Use hardware-level atomic instructions
- **Complexity**: More complex to implement and reason about

### Real-World Analogy
Think of a busy intersection where cars can proceed without traffic lights, but each car must yield to others and find a safe way through. The system keeps moving even if some cars are slow or stopped.

### Java Example
```java
public class LockFreeAlgorithmsExample {
    // Lock-free stack implementation
    public static class LockFreeStack<T> {
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        
        private static class Node<T> {
            final T data;
            final AtomicReference<Node<T>> next;
            
            Node(T data) {
                this.data = data;
                this.next = new AtomicReference<>();
            }
        }
        
        public void push(T item) {
            Node<T> newNode = new Node<>(item);
            Node<T> currentHead;
            
            do {
                currentHead = head.get();
                newNode.next.set(currentHead);
            } while (!head.compareAndSet(currentHead, newNode));
        }
        
        public T pop() {
            Node<T> currentHead;
            Node<T> newHead;
            
            do {
                currentHead = head.get();
                if (currentHead == null) {
                    return null;
                }
                newHead = currentHead.next.get();
            } while (!head.compareAndSet(currentHead, newHead));
            
            return currentHead.data;
        }
        
        public boolean isEmpty() {
            return head.get() == null;
        }
    }
    
    // Lock-free counter
    public static class LockFreeCounter {
        private final AtomicInteger count = new AtomicInteger(0);
        
        public void increment() {
            int current;
            do {
                current = count.get();
            } while (!count.compareAndSet(current, current + 1));
        }
        
        public void decrement() {
            int current;
            do {
                current = count.get();
            } while (!count.compareAndSet(current, current - 1));
        }
        
        public int get() {
            return count.get();
        }
    }
    
    public static void demonstrateLockFreeAlgorithms() {
        LockFreeStack<String> stack = new LockFreeStack<>();
        LockFreeCounter counter = new LockFreeCounter();
        
        // Multiple threads pushing to stack
        Thread[] pushers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int pusherId = i;
            pushers[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    stack.push("Thread-" + pusherId + "-Item-" + j);
                    counter.increment();
                }
            });
            pushers[i].start();
        }
        
        // Multiple threads popping from stack
        Thread[] poppers = new Thread[2];
        
        for (int i = 0; i < 2; i++) {
            final int popperId = i;
            poppers[i] = new Thread(() -> {
                for (int j = 0; j < 15; j++) {
                    String item = stack.pop();
                    if (item != null) {
                        System.out.println("Popper " + popperId + " got: " + item);
                    }
                }
            });
            poppers[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : pushers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        for (Thread thread : poppers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Final counter: " + counter.get());
    }
}
```

## 6.2 Compare-and-Swap (CAS)

Compare-and-Swap (CAS) is an atomic operation that compares a value with an expected value and, if they match, updates the value to a new value.

### Key Characteristics
- **Atomic**: Operation completes as a single unit
- **Optimistic**: Assumes no conflict, retries if conflict occurs
- **Lock-Free**: No blocking or waiting
- **Hardware Support**: Implemented using CPU instructions

### Real-World Analogy
Think of a vending machine where you insert coins and press a button. If the machine has the item you want, it gives it to you and takes your money. If not, it returns your money and you can try again.

### Java Example
```java
public class CompareAndSwapExample {
    // Simple CAS implementation
    public static class CASInteger {
        private volatile int value;
        
        public CASInteger(int initialValue) {
            this.value = initialValue;
        }
        
        public int get() {
            return value;
        }
        
        public boolean compareAndSet(int expected, int newValue) {
            return value == expected && (value = newValue) == newValue;
        }
        
        public int incrementAndGet() {
            int current;
            do {
                current = value;
            } while (!compareAndSet(current, current + 1));
            return current + 1;
        }
    }
    
    // Using AtomicInteger for CAS operations
    private static final AtomicInteger atomicCounter = new AtomicInteger(0);
    
    public static void demonstrateCAS() {
        // Basic CAS operations
        System.out.println("Initial value: " + atomicCounter.get());
        
        // Compare and set
        boolean success = atomicCounter.compareAndSet(0, 10);
        System.out.println("CAS(0, 10) successful: " + success + ", value: " + atomicCounter.get());
        
        // Compare and set (should fail)
        success = atomicCounter.compareAndSet(0, 20);
        System.out.println("CAS(0, 20) successful: " + success + ", value: " + atomicCounter.get());
        
        // Compare and set (should succeed)
        success = atomicCounter.compareAndSet(10, 20);
        System.out.println("CAS(10, 20) successful: " + success + ", value: " + atomicCounter.get());
    }
    
    // CAS-based counter
    public static void demonstrateCASCounter() {
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    atomicCounter.incrementAndGet();
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
        
        System.out.println("Final counter value: " + atomicCounter.get());
    }
    
    // CAS-based lock-free queue
    public static class LockFreeQueue<T> {
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        private final AtomicReference<Node<T>> tail = new AtomicReference<>();
        
        private static class Node<T> {
            final T data;
            final AtomicReference<Node<T>> next;
            
            Node(T data) {
                this.data = data;
                this.next = new AtomicReference<>();
            }
        }
        
        public void enqueue(T item) {
            Node<T> newNode = new Node<>(item);
            Node<T> currentTail;
            Node<T> currentNext;
            
            do {
                currentTail = tail.get();
                currentNext = currentTail.next.get();
                
                if (currentTail == tail.get()) {
                    if (currentNext == null) {
                        if (currentTail.next.compareAndSet(null, newNode)) {
                            break;
                        }
                    } else {
                        tail.compareAndSet(currentTail, currentNext);
                    }
                }
            } while (true);
            
            tail.compareAndSet(currentTail, newNode);
        }
        
        public T dequeue() {
            Node<T> currentHead;
            Node<T> currentTail;
            Node<T> currentNext;
            T data;
            
            do {
                currentHead = head.get();
                currentTail = tail.get();
                currentNext = currentHead.next.get();
                
                if (currentHead == head.get()) {
                    if (currentHead == currentTail) {
                        if (currentNext == null) {
                            return null;
                        }
                        tail.compareAndSet(currentTail, currentNext);
                    } else {
                        data = currentNext.data;
                        if (head.compareAndSet(currentHead, currentNext)) {
                            break;
                        }
                    }
                }
            } while (true);
            
            return data;
        }
    }
}
```

## 6.3 Load-Link/Store-Conditional

Load-Link/Store-Conditional (LL/SC) is a pair of atomic operations that provide a more powerful alternative to CAS for implementing lock-free data structures.

### Key Characteristics
- **Load-Link**: Loads a value and creates a link to that memory location
- **Store-Conditional**: Stores a value only if the link is still valid
- **ABA Prevention**: Prevents ABA problem by detecting modifications
- **Hardware Support**: Supported by some architectures (ARM, MIPS)

### Real-World Analogy
Think of a reservation system where you first check if a seat is available (load-link) and then try to book it (store-conditional). If someone else books the seat between your check and booking attempt, your booking fails.

### Java Example
```java
public class LoadLinkStoreConditionalExample {
    // Simulating LL/SC with Java's atomic operations
    public static class LLSCSimulation {
        private final AtomicInteger value = new AtomicInteger(0);
        private final AtomicInteger version = new AtomicInteger(0);
        
        public int loadLink() {
            return value.get();
        }
        
        public boolean storeConditional(int expectedValue, int newValue) {
            return value.compareAndSet(expectedValue, newValue);
        }
        
        public boolean compareAndSwap(int expectedValue, int newValue) {
            return value.compareAndSet(expectedValue, newValue);
        }
    }
    
    // Lock-free counter using LL/SC simulation
    public static class LLSCCounter {
        private final LLSCSimulation llsc = new LLSCSimulation();
        
        public void increment() {
            int current;
            do {
                current = llsc.loadLink();
            } while (!llsc.storeConditional(current, current + 1));
        }
        
        public int get() {
            return llsc.loadLink();
        }
    }
    
    public static void demonstrateLLSC() {
        LLSCSimulation llsc = new LLSCSimulation();
        
        // Test basic LL/SC operations
        int initialValue = llsc.loadLink();
        System.out.println("Initial value: " + initialValue);
        
        boolean success = llsc.storeConditional(initialValue, 10);
        System.out.println("Store conditional successful: " + success);
        
        int newValue = llsc.loadLink();
        System.out.println("New value: " + newValue);
        
        // Test with multiple threads
        LLSCCounter counter = new LLSCCounter();
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    counter.increment();
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
        
        System.out.println("Final counter value: " + counter.get());
    }
}
```

## 6.4 ABA Problem

The ABA problem occurs when a value is changed from A to B and back to A, making it appear as if no change occurred when using CAS operations.

### Key Concepts
- **Value Change**: A → B → A
- **CAS Confusion**: CAS sees A and thinks nothing changed
- **Memory Reuse**: Same memory location reused for different values
- **Solutions**: Version numbers, hazard pointers, or LL/SC

### Real-World Analogy
Think of a parking spot where you see a red car, then a blue car, then a red car again. If you only check the color, you might think the same red car is still there, but it's actually a different red car.

### Java Example
```java
public class ABAProblemExample {
    // Node that can be reused (causing ABA problem)
    public static class ReusableNode {
        private final int value;
        private final AtomicReference<ReusableNode> next = new AtomicReference<>();
        
        public ReusableNode(int value) {
            this.value = value;
        }
        
        public int getValue() { return value; }
        public AtomicReference<ReusableNode> getNext() { return next; }
    }
    
    // Stack that can suffer from ABA problem
    public static class ABAStack {
        private final AtomicReference<ReusableNode> head = new AtomicReference<>();
        
        public void push(ReusableNode node) {
            ReusableNode currentHead;
            do {
                currentHead = head.get();
                node.getNext().set(currentHead);
            } while (!head.compareAndSet(currentHead, node));
        }
        
        public ReusableNode pop() {
            ReusableNode currentHead;
            ReusableNode newHead;
            
            do {
                currentHead = head.get();
                if (currentHead == null) {
                    return null;
                }
                newHead = currentHead.getNext().get();
            } while (!head.compareAndSet(currentHead, newHead));
            
            return currentHead;
        }
    }
    
    // Solution: Using version numbers
    public static class VersionedNode {
        private final int value;
        private final int version;
        private final AtomicReference<VersionedNode> next = new AtomicReference<>();
        
        public VersionedNode(int value, int version) {
            this.value = value;
            this.version = version;
        }
        
        public int getValue() { return value; }
        public int getVersion() { return version; }
        public AtomicReference<VersionedNode> getNext() { return next; }
    }
    
    public static class VersionedStack {
        private final AtomicReference<VersionedNode> head = new AtomicReference<>();
        private final AtomicInteger versionCounter = new AtomicInteger(0);
        
        public void push(int value) {
            VersionedNode newNode = new VersionedNode(value, versionCounter.incrementAndGet());
            VersionedNode currentHead;
            
            do {
                currentHead = head.get();
                newNode.getNext().set(currentHead);
            } while (!head.compareAndSet(currentHead, newNode));
        }
        
        public Integer pop() {
            VersionedNode currentHead;
            VersionedNode newHead;
            
            do {
                currentHead = head.get();
                if (currentHead == null) {
                    return null;
                }
                newHead = currentHead.getNext().get();
            } while (!head.compareAndSet(currentHead, newHead));
            
            return currentHead.getValue();
        }
    }
    
    public static void demonstrateABAProblem() {
        // Demonstrate ABA problem
        ABAStack abaStack = new ABAStack();
        
        ReusableNode node1 = new ReusableNode(1);
        ReusableNode node2 = new ReusableNode(2);
        
        abaStack.push(node1);
        abaStack.push(node2);
        
        // Thread 1: Pop node2, then push it back
        Thread thread1 = new Thread(() -> {
            ReusableNode popped = abaStack.pop();
            if (popped != null) {
                System.out.println("Thread 1 popped: " + popped.getValue());
                // Simulate some work
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                abaStack.push(popped);
                System.out.println("Thread 1 pushed back: " + popped.getValue());
            }
        });
        
        // Thread 2: Pop node2, modify it, and push it back
        Thread thread2 = new Thread(() -> {
            ReusableNode popped = abaStack.pop();
            if (popped != null) {
                System.out.println("Thread 2 popped: " + popped.getValue());
                // Modify the node (this is the problem)
                // In real scenario, this would be memory reuse
                abaStack.push(popped);
                System.out.println("Thread 2 pushed back: " + popped.getValue());
            }
        });
        
        thread1.start();
        thread2.start();
        
        try {
            thread1.join();
            thread2.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Demonstrate solution with versioned stack
        System.out.println("\n--- Using Versioned Stack ---");
        VersionedStack versionedStack = new VersionedStack();
        
        versionedStack.push(1);
        versionedStack.push(2);
        
        Thread thread3 = new Thread(() -> {
            Integer popped = versionedStack.pop();
            if (popped != null) {
                System.out.println("Thread 3 popped: " + popped);
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                versionedStack.push(popped);
                System.out.println("Thread 3 pushed back: " + popped);
            }
        });
        
        Thread thread4 = new Thread(() -> {
            Integer popped = versionedStack.pop();
            if (popped != null) {
                System.out.println("Thread 4 popped: " + popped);
                versionedStack.push(popped);
                System.out.println("Thread 4 pushed back: " + popped);
            }
        });
        
        thread3.start();
        thread4.start();
        
        try {
            thread3.join();
            thread4.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

## 6.5 Hazard Pointers

Hazard pointers are a memory management technique used in lock-free programming to safely reclaim memory that might be accessed by other threads.

### Key Concepts
- **Memory Reclamation**: Safely reclaiming memory in lock-free structures
- **Hazard Pointers**: Thread-local pointers to memory being accessed
- **Retirement**: Marking memory for later reclamation
- **Scanning**: Checking if memory is safe to reclaim

### Real-World Analogy
Think of a library where books are being used by multiple people. Before a book can be removed from the shelf, the librarian must check if anyone is currently reading it (hazard pointer).

### Java Example
```java
public class HazardPointersExample {
    // Simplified hazard pointer implementation
    public static class HazardPointer<T> {
        private final AtomicReference<T> pointer = new AtomicReference<>();
        
        public void set(T value) {
            pointer.set(value);
        }
        
        public T get() {
            return pointer.get();
        }
        
        public void clear() {
            pointer.set(null);
        }
    }
    
    // Thread-local hazard pointers
    public static class ThreadLocalHazardPointers<T> {
        private final ThreadLocal<HazardPointer<T>> hazardPointers = 
            ThreadLocal.withInitial(() -> new HazardPointer<>());
        
        public HazardPointer<T> get() {
            return hazardPointers.get();
        }
    }
    
    // Lock-free stack with hazard pointers
    public static class HazardPointerStack<T> {
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        private final ThreadLocalHazardPointers<Node<T>> hazardPointers = 
            new ThreadLocalHazardPointers<>();
        private final AtomicReference<Set<Node<T>>> retiredNodes = 
            new AtomicReference<>(new HashSet<>());
        
        private static class Node<T> {
            final T data;
            final AtomicReference<Node<T>> next;
            
            Node(T data) {
                this.data = data;
                this.next = new AtomicReference<>();
            }
        }
        
        public void push(T item) {
            Node<T> newNode = new Node<>(item);
            Node<T> currentHead;
            
            do {
                currentHead = head.get();
                newNode.next.set(currentHead);
            } while (!head.compareAndSet(currentHead, newNode));
        }
        
        public T pop() {
            Node<T> currentHead;
            Node<T> newHead;
            
            do {
                currentHead = head.get();
                if (currentHead == null) {
                    return null;
                }
                
                // Set hazard pointer
                hazardPointers.get().set(currentHead);
                
                // Check if head changed
                if (head.get() != currentHead) {
                    continue;
                }
                
                newHead = currentHead.next.get();
            } while (!head.compareAndSet(currentHead, newHead));
            
            // Clear hazard pointer
            hazardPointers.get().clear();
            
            // Retire the node
            retireNode(currentHead);
            
            return currentHead.data;
        }
        
        private void retireNode(Node<T> node) {
            Set<Node<T>> currentRetired = retiredNodes.get();
            Set<Node<T>> newRetired = new HashSet<>(currentRetired);
            newRetired.add(node);
            retiredNodes.set(newRetired);
            
            // Periodically scan and reclaim
            if (newRetired.size() > 10) {
                scanAndReclaim();
            }
        }
        
        private void scanAndReclaim() {
            Set<Node<T>> currentRetired = retiredNodes.get();
            Set<Node<T>> newRetired = new HashSet<>();
            
            for (Node<T> node : currentRetired) {
                if (!isHazardous(node)) {
                    // Safe to reclaim
                    System.out.println("Reclaiming node: " + node.data);
                } else {
                    newRetired.add(node);
                }
            }
            
            retiredNodes.set(newRetired);
        }
        
        private boolean isHazardous(Node<T> node) {
            // Check if any thread has this node as a hazard pointer
            // This is a simplified check
            return false;
        }
    }
    
    public static void demonstrateHazardPointers() {
        HazardPointerStack<String> stack = new HazardPointerStack<>();
        
        // Push some items
        for (int i = 0; i < 10; i++) {
            stack.push("Item-" + i);
        }
        
        // Multiple threads popping
        Thread[] threads = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 5; j++) {
                    String item = stack.pop();
                    if (item != null) {
                        System.out.println("Thread " + threadId + " popped: " + item);
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
    }
}
```

## 6.6 Memory Reclamation

Memory reclamation is the process of safely returning memory to the system in lock-free data structures, which is more complex than in lock-based structures.

### Key Challenges
- **Dangling Pointers**: Memory might be accessed after being freed
- **ABA Problem**: Memory reuse can cause confusion
- **Race Conditions**: Multiple threads might try to reclaim the same memory
- **Solutions**: Hazard pointers, epoch-based reclamation, or garbage collection

### Real-World Analogy
Think of a shared workspace where multiple people are using tools. Before putting a tool away, you must ensure no one else is currently using it.

### Java Example
```java
public class MemoryReclamationExample {
    // Epoch-based memory reclamation
    public static class EpochBasedReclamation<T> {
        private final AtomicInteger globalEpoch = new AtomicInteger(0);
        private final ThreadLocal<Integer> threadEpoch = new ThreadLocal<>();
        private final ThreadLocal<Set<T>> retiredObjects = ThreadLocal.withInitial(HashSet::new);
        
        public void enterEpoch() {
            threadEpoch.set(globalEpoch.get());
        }
        
        public void exitEpoch() {
            threadEpoch.remove();
        }
        
        public void retire(T object) {
            retiredObjects.get().add(object);
            if (retiredObjects.get().size() > 100) {
                scanAndReclaim();
            }
        }
        
        private void scanAndReclaim() {
            int currentEpoch = globalEpoch.get();
            Set<T> toReclaim = new HashSet<>();
            
            for (T obj : retiredObjects.get()) {
                if (isSafeToReclaim(obj, currentEpoch)) {
                    toReclaim.add(obj);
                }
            }
            
            retiredObjects.get().removeAll(toReclaim);
            
            // Reclaim objects
            for (T obj : toReclaim) {
                System.out.println("Reclaiming object: " + obj);
            }
        }
        
        private boolean isSafeToReclaim(T obj, int currentEpoch) {
            // Simplified check - in reality, this would check if any thread
            // is currently accessing this object
            return true;
        }
    }
    
    // Lock-free stack with memory reclamation
    public static class ReclaimingStack<T> {
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        private final EpochBasedReclamation<Node<T>> reclaimer = new EpochBasedReclamation<>();
        
        private static class Node<T> {
            final T data;
            final AtomicReference<Node<T>> next;
            
            Node(T data) {
                this.data = data;
                this.next = new AtomicReference<>();
            }
        }
        
        public void push(T item) {
            reclaimer.enterEpoch();
            
            try {
                Node<T> newNode = new Node<>(item);
                Node<T> currentHead;
                
                do {
                    currentHead = head.get();
                    newNode.next.set(currentHead);
                } while (!head.compareAndSet(currentHead, newNode));
            } finally {
                reclaimer.exitEpoch();
            }
        }
        
        public T pop() {
            reclaimer.enterEpoch();
            
            try {
                Node<T> currentHead;
                Node<T> newHead;
                
                do {
                    currentHead = head.get();
                    if (currentHead == null) {
                        return null;
                    }
                    newHead = currentHead.next.get();
                } while (!head.compareAndSet(currentHead, newHead));
                
                // Retire the node for later reclamation
                reclaimer.retire(currentHead);
                
                return currentHead.data;
            } finally {
                reclaimer.exitEpoch();
            }
        }
    }
    
    public static void demonstrateMemoryReclamation() {
        ReclaimingStack<String> stack = new ReclaimingStack<>();
        
        // Push some items
        for (int i = 0; i < 20; i++) {
            stack.push("Item-" + i);
        }
        
        // Multiple threads popping
        Thread[] threads = new Thread[4];
        
        for (int i = 0; i < 4; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    String item = stack.pop();
                    if (item != null) {
                        System.out.println("Thread " + threadId + " popped: " + item);
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
    }
}
```

## 6.7 Lock-Free Queues

Lock-free queues are queue implementations that allow multiple threads to enqueue and dequeue elements without using locks.

### Key Features
- **Multiple Producers/Consumers**: Support for concurrent access
- **Lock-Free Operations**: No blocking or waiting
- **Memory Ordering**: Proper ordering of memory operations
- **Complexity**: More complex than lock-based queues

### Real-World Analogy
Think of a conveyor belt where multiple workers can add items to the front and multiple workers can take items from the back simultaneously, without any coordination mechanisms.

### Java Example
```java
public class LockFreeQueueExample {
    // Lock-free queue using Michael & Scott algorithm
    public static class LockFreeQueue<T> {
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        private final AtomicReference<Node<T>> tail = new AtomicReference<>();
        
        private static class Node<T> {
            final T data;
            final AtomicReference<Node<T>> next;
            
            Node(T data) {
                this.data = data;
                this.next = new AtomicReference<>();
            }
        }
        
        public LockFreeQueue() {
            Node<T> dummy = new Node<>(null);
            head.set(dummy);
            tail.set(dummy);
        }
        
        public void enqueue(T item) {
            Node<T> newNode = new Node<>(item);
            Node<T> currentTail;
            Node<T> currentNext;
            
            while (true) {
                currentTail = tail.get();
                currentNext = currentTail.next.get();
                
                if (currentTail == tail.get()) {
                    if (currentNext == null) {
                        if (currentTail.next.compareAndSet(null, newNode)) {
                            break;
                        }
                    } else {
                        tail.compareAndSet(currentTail, currentNext);
                    }
                }
            }
            
            tail.compareAndSet(currentTail, newNode);
        }
        
        public T dequeue() {
            Node<T> currentHead;
            Node<T> currentTail;
            Node<T> currentNext;
            T data;
            
            while (true) {
                currentHead = head.get();
                currentTail = tail.get();
                currentNext = currentHead.next.get();
                
                if (currentHead == head.get()) {
                    if (currentHead == currentTail) {
                        if (currentNext == null) {
                            return null;
                        }
                        tail.compareAndSet(currentTail, currentNext);
                    } else {
                        data = currentNext.data;
                        if (head.compareAndSet(currentHead, currentNext)) {
                            break;
                        }
                    }
                }
            }
            
            return data;
        }
        
        public boolean isEmpty() {
            return head.get() == tail.get();
        }
    }
    
    public static void demonstrateLockFreeQueue() {
        LockFreeQueue<String> queue = new LockFreeQueue<>();
        
        // Multiple producers
        Thread[] producers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            producers[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    String item = "Producer-" + producerId + "-Item-" + j;
                    queue.enqueue(item);
                    System.out.println("Enqueued: " + item);
                }
            });
            producers[i].start();
        }
        
        // Multiple consumers
        Thread[] consumers = new Thread[2];
        
        for (int i = 0; i < 2; i++) {
            final int consumerId = i;
            consumers[i] = new Thread(() -> {
                for (int j = 0; j < 15; j++) {
                    String item = queue.dequeue();
                    if (item != null) {
                        System.out.println("Consumer " + consumerId + " dequeued: " + item);
                    }
                }
            });
            consumers[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : producers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        for (Thread thread : consumers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
```

## 6.8 Lock-Free Stacks

Lock-free stacks are stack implementations that allow multiple threads to push and pop elements without using locks.

### Key Features
- **LIFO Order**: Last In, First Out ordering
- **Lock-Free Operations**: No blocking or waiting
- **Memory Ordering**: Proper ordering of memory operations
- **ABA Problem**: Potential issue with CAS operations

### Real-World Analogy
Think of a stack of plates where multiple people can add plates to the top or take plates from the top simultaneously, but the stack maintains its LIFO order.

### Java Example
```java
public class LockFreeStackExample {
    // Lock-free stack using Treiber's algorithm
    public static class LockFreeStack<T> {
        private final AtomicReference<Node<T>> head = new AtomicReference<>();
        
        private static class Node<T> {
            final T data;
            final AtomicReference<Node<T>> next;
            
            Node(T data) {
                this.data = data;
                this.next = new AtomicReference<>();
            }
        }
        
        public void push(T item) {
            Node<T> newNode = new Node<>(item);
            Node<T> currentHead;
            
            do {
                currentHead = head.get();
                newNode.next.set(currentHead);
            } while (!head.compareAndSet(currentHead, newNode));
        }
        
        public T pop() {
            Node<T> currentHead;
            Node<T> newHead;
            
            do {
                currentHead = head.get();
                if (currentHead == null) {
                    return null;
                }
                newHead = currentHead.next.get();
            } while (!head.compareAndSet(currentHead, newHead));
            
            return currentHead.data;
        }
        
        public boolean isEmpty() {
            return head.get() == null;
        }
    }
    
    public static void demonstrateLockFreeStack() {
        LockFreeStack<String> stack = new LockFreeStack<>();
        
        // Multiple pushers
        Thread[] pushers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int pusherId = i;
            pushers[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    String item = "Pusher-" + pusherId + "-Item-" + j;
                    stack.push(item);
                    System.out.println("Pushed: " + item);
                }
            });
            pushers[i].start();
        }
        
        // Multiple poppers
        Thread[] poppers = new Thread[2];
        
        for (int i = 0; i < 2; i++) {
            final int popperId = i;
            poppers[i] = new Thread(() -> {
                for (int j = 0; j < 15; j++) {
                    String item = stack.pop();
                    if (item != null) {
                        System.out.println("Popper " + popperId + " popped: " + item);
                    }
                }
            });
            poppers[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : pushers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        for (Thread thread : poppers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
```

This comprehensive explanation covers all aspects of lock-free programming, providing both theoretical understanding and practical Java examples to illustrate each concept.