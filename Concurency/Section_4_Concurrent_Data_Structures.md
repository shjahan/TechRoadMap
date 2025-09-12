# Section 4 – Concurrent Data Structures

## 4.1 Thread-Safe Collections

Thread-safe collections are data structures that can be safely accessed by multiple threads simultaneously without external synchronization.

### Key Characteristics
- **Atomic Operations**: All operations are atomic
- **Internal Synchronization**: Built-in thread safety mechanisms
- **Performance Trade-offs**: May be slower than non-thread-safe alternatives
- **Consistency**: Maintains data integrity under concurrent access

### Real-World Analogy
Think of a shared whiteboard that multiple people can write on simultaneously, but the whiteboard has built-in mechanisms to prevent conflicts and ensure everyone's writing is preserved.

### Java Example
```java
public class ThreadSafeCollectionsExample {
    // Thread-safe collections
    private static final List<String> synchronizedList = Collections.synchronizedList(new ArrayList<>());
    private static final Set<Integer> synchronizedSet = Collections.synchronizedSet(new HashSet<>());
    private static final Map<String, String> synchronizedMap = Collections.synchronizedMap(new HashMap<>());
    
    // Concurrent collections (better performance)
    private static final ConcurrentHashMap<String, String> concurrentMap = new ConcurrentHashMap<>();
    private static final CopyOnWriteArrayList<String> copyOnWriteList = new CopyOnWriteArrayList<>();
    private static final ConcurrentLinkedQueue<String> concurrentQueue = new ConcurrentLinkedQueue<>();
    
    public static void demonstrateThreadSafeCollections() {
        // Multiple threads adding to synchronized list
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    synchronizedList.add("Thread-" + threadId + "-Item-" + j);
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
        
        System.out.println("Synchronized list size: " + synchronizedList.size());
    }
    
    // Concurrent collections example
    public static void demonstrateConcurrentCollections() {
        // Multiple threads working with concurrent collections
        Thread[] threads = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    concurrentMap.put("key-" + threadId + "-" + j, "value-" + j);
                    concurrentQueue.offer("queue-item-" + threadId + "-" + j);
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
        
        System.out.println("Concurrent map size: " + concurrentMap.size());
        System.out.println("Concurrent queue size: " + concurrentQueue.size());
    }
}
```

## 4.2 Lock-Free Data Structures

Lock-free data structures use atomic operations and compare-and-swap (CAS) operations to achieve thread safety without traditional locking mechanisms.

### Key Characteristics
- **No Blocking**: Threads never block waiting for locks
- **Atomic Operations**: Use hardware-level atomic instructions
- **ABA Problem**: Potential issue with CAS operations
- **Performance**: Often faster than lock-based structures

### Real-World Analogy
Think of a vending machine where multiple people can try to buy items simultaneously. The machine uses atomic operations to ensure only one person gets each item, without anyone having to wait in line.

### Java Example
```java
public class LockFreeDataStructuresExample {
    // Lock-free stack using atomic operations
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
        
        public int get() {
            return count.get();
        }
    }
    
    public static void demonstrateLockFreeStructures() {
        LockFreeStack<String> stack = new LockFreeStack<>();
        LockFreeCounter counter = new LockFreeCounter();
        
        // Multiple threads pushing to stack
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 10; j++) {
                    stack.push("Thread-" + threadId + "-Item-" + j);
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
        
        System.out.println("Counter value: " + counter.get());
        
        // Pop items from stack
        String item;
        int count = 0;
        while ((item = stack.pop()) != null) {
            System.out.println("Popped: " + item);
            count++;
        }
        System.out.println("Total items popped: " + count);
    }
}
```

## 4.3 Concurrent Hash Maps

Concurrent hash maps are thread-safe implementations of hash table data structures that allow multiple threads to read and write simultaneously.

### Key Features
- **Segment-based Locking**: Different segments can be locked independently
- **Read Operations**: No locking required for reads
- **Write Operations**: Minimal locking for writes
- **Iterators**: Weakly consistent iterators

### Real-World Analogy
Think of a library with multiple sections, each with its own librarian. People can read books in any section simultaneously, but only one person can check out books from each section at a time.

### Java Example
```java
public class ConcurrentHashMapExample {
    private static final ConcurrentHashMap<String, Integer> concurrentMap = new ConcurrentHashMap<>();
    
    public static void demonstrateConcurrentHashMap() {
        // Multiple threads writing to different keys
        Thread[] writers = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            writers[i] = new Thread(() -> {
                for (int j = 0; j < 100; j++) {
                    String key = "thread-" + threadId + "-key-" + j;
                    concurrentMap.put(key, j);
                }
            });
            writers[i].start();
        }
        
        // Multiple threads reading
        Thread[] readers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int readerId = i;
            readers[i] = new Thread(() -> {
                for (int j = 0; j < 50; j++) {
                    String key = "thread-0-key-" + j;
                    Integer value = concurrentMap.get(key);
                    if (value != null) {
                        System.out.println("Reader " + readerId + " read: " + key + " = " + value);
                    }
                }
            });
            readers[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : writers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        for (Thread thread : readers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Final map size: " + concurrentMap.size());
    }
    
    // Atomic operations on ConcurrentHashMap
    public static void demonstrateAtomicOperations() {
        concurrentMap.put("counter", 0);
        
        // Atomic increment
        concurrentMap.compute("counter", (key, value) -> value + 1);
        
        // Atomic update
        concurrentMap.merge("counter", 1, Integer::sum);
        
        // Atomic put if absent
        concurrentMap.putIfAbsent("newKey", 42);
        
        // Atomic replace
        concurrentMap.replace("counter", 2, 100);
        
        System.out.println("Counter value: " + concurrentMap.get("counter"));
    }
}
```

## 4.4 Concurrent Queues

Concurrent queues are thread-safe implementations of queue data structures that support multiple producers and consumers.

### Key Features
- **Lock-free Operations**: Most operations are lock-free
- **Multiple Producers/Consumers**: Support for concurrent access
- **Bounded/Unbounded**: Can have size limits or be unlimited
- **Blocking/Non-blocking**: Different waiting strategies

### Real-World Analogy
Think of a conveyor belt in a factory where multiple workers can place items on the belt (producers) and multiple workers can take items off the belt (consumers) simultaneously.

### Java Example
```java
public class ConcurrentQueueExample {
    // Unbounded concurrent queue
    private static final ConcurrentLinkedQueue<String> unboundedQueue = new ConcurrentLinkedQueue<>();
    
    // Bounded blocking queue
    private static final ArrayBlockingQueue<String> boundedQueue = new ArrayBlockingQueue<>(10);
    
    // Priority blocking queue
    private static final PriorityBlockingQueue<Integer> priorityQueue = new PriorityBlockingQueue<>();
    
    public static void demonstrateConcurrentQueues() {
        // Producer threads
        Thread[] producers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int producerId = i;
            producers[i] = new Thread(() -> {
                for (int j = 0; j < 20; j++) {
                    String item = "Producer-" + producerId + "-Item-" + j;
                    unboundedQueue.offer(item);
                    priorityQueue.offer(j);
                    
                    try {
                        boundedQueue.put(item);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
            producers[i].start();
        }
        
        // Consumer threads
        Thread[] consumers = new Thread[2];
        
        for (int i = 0; i < 2; i++) {
            final int consumerId = i;
            consumers[i] = new Thread(() -> {
                for (int j = 0; j < 30; j++) {
                    // Poll from unbounded queue
                    String item = unboundedQueue.poll();
                    if (item != null) {
                        System.out.println("Consumer " + consumerId + " got: " + item);
                    }
                    
                    // Take from bounded queue
                    try {
                        String boundedItem = boundedQueue.take();
                        System.out.println("Consumer " + consumerId + " got bounded: " + boundedItem);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    
                    // Poll from priority queue
                    Integer priorityItem = priorityQueue.poll();
                    if (priorityItem != null) {
                        System.out.println("Consumer " + consumerId + " got priority: " + priorityItem);
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

## 4.5 Concurrent Stacks

Concurrent stacks are thread-safe implementations of stack data structures that support multiple threads pushing and popping elements.

### Key Features
- **LIFO Order**: Last In, First Out ordering
- **Atomic Operations**: Push and pop operations are atomic
- **Lock-free**: Often implemented using lock-free algorithms
- **ABA Problem**: Potential issue with CAS operations

### Real-World Analogy
Think of a stack of plates where multiple people can add plates to the top or take plates from the top simultaneously, but the stack maintains its LIFO order.

### Java Example
```java
public class ConcurrentStackExample {
    // Using ConcurrentLinkedDeque as a stack
    private static final ConcurrentLinkedDeque<String> concurrentStack = new ConcurrentLinkedDeque<>();
    
    // Custom lock-free stack implementation
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
    
    public static void demonstrateConcurrentStacks() {
        LockFreeStack<String> stack = new LockFreeStack<>();
        
        // Multiple threads pushing to stack
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
        
        // Multiple threads popping from stack
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

## 4.6 Concurrent Lists

Concurrent lists are thread-safe implementations of list data structures that support multiple threads accessing and modifying the list.

### Key Features
- **Indexed Access**: Support for random access by index
- **Iteration**: Safe iteration over the list
- **Modification**: Safe modification during iteration
- **Performance**: Trade-offs between safety and performance

### Real-World Analogy
Think of a shared notebook where multiple people can read, write, and modify entries simultaneously, but the notebook has built-in mechanisms to prevent conflicts and maintain consistency.

### Java Example
```java
public class ConcurrentListExample {
    // Copy-on-write list
    private static final CopyOnWriteArrayList<String> copyOnWriteList = new CopyOnWriteArrayList<>();
    
    // Synchronized list
    private static final List<String> synchronizedList = Collections.synchronizedList(new ArrayList<>());
    
    public static void demonstrateConcurrentLists() {
        // Initialize lists
        for (int i = 0; i < 10; i++) {
            copyOnWriteList.add("Item-" + i);
            synchronizedList.add("Item-" + i);
        }
        
        // Multiple threads modifying copy-on-write list
        Thread[] modifiers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int modifierId = i;
            modifiers[i] = new Thread(() -> {
                for (int j = 0; j < 5; j++) {
                    String item = "Modifier-" + modifierId + "-Item-" + j;
                    copyOnWriteList.add(item);
                    System.out.println("Added to COW list: " + item);
                }
            });
            modifiers[i].start();
        }
        
        // Multiple threads reading from copy-on-write list
        Thread[] readers = new Thread[2];
        
        for (int i = 0; i < 2; i++) {
            final int readerId = i;
            readers[i] = new Thread(() -> {
                for (String item : copyOnWriteList) {
                    System.out.println("Reader " + readerId + " read: " + item);
                }
            });
            readers[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : modifiers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        for (Thread thread : readers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Final COW list size: " + copyOnWriteList.size());
    }
}
```

## 4.7 Copy-on-Write (COW) Structures

Copy-on-write structures create a new copy of the data structure when modifications are made, allowing readers to continue using the old version.

### Key Characteristics
- **Immutability**: Readers see consistent snapshots
- **Copy Overhead**: Modifications create new copies
- **Memory Usage**: Higher memory usage due to copying
- **Read Performance**: Excellent read performance

### Real-World Analogy
Think of a library where when someone wants to modify a book, a new copy is made. Readers can continue using the old copy while the new copy is being prepared.

### Java Example
```java
public class CopyOnWriteExample {
    private static final CopyOnWriteArrayList<String> cowList = new CopyOnWriteArrayList<>();
    private static final CopyOnWriteArraySet<String> cowSet = new CopyOnWriteArraySet<>();
    
    public static void demonstrateCopyOnWrite() {
        // Initialize
        cowList.add("Initial-Item-1");
        cowList.add("Initial-Item-2");
        cowList.add("Initial-Item-3");
        
        // Multiple readers
        Thread[] readers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int readerId = i;
            readers[i] = new Thread(() -> {
                for (int j = 0; j < 5; j++) {
                    System.out.println("Reader " + readerId + " iteration " + j + ":");
                    for (String item : cowList) {
                        System.out.println("  " + item);
                    }
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
            readers[i].start();
        }
        
        // Multiple writers
        Thread[] writers = new Thread[2];
        
        for (int i = 0; i < 2; i++) {
            final int writerId = i;
            writers[i] = new Thread(() -> {
                for (int j = 0; j < 3; j++) {
                    String item = "Writer-" + writerId + "-Item-" + j;
                    cowList.add(item);
                    cowSet.add(item);
                    System.out.println("Writer " + writerId + " added: " + item);
                    
                    try {
                        Thread.sleep(200);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
            writers[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : readers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        for (Thread thread : writers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        
        System.out.println("Final COW list size: " + cowList.size());
        System.out.println("Final COW set size: " + cowSet.size());
    }
}
```

## 4.8 Immutable Data Structures

Immutable data structures cannot be modified after creation, providing natural thread safety and eliminating the need for synchronization.

### Key Characteristics
- **Thread Safety**: Naturally thread-safe
- **No Synchronization**: No need for locks or synchronization
- **Memory Efficiency**: Can share data between instances
- **Functional Programming**: Aligns with functional programming principles

### Real-World Analogy
Think of a stone tablet with text carved into it. Once carved, the text cannot be changed, but anyone can read it safely without worrying about modifications.

### Java Example
```java
public class ImmutableDataStructuresExample {
    // Immutable class
    public static final class ImmutablePerson {
        private final String name;
        private final int age;
        private final List<String> hobbies;
        
        public ImmutablePerson(String name, int age, List<String> hobbies) {
            this.name = name;
            this.age = age;
            this.hobbies = Collections.unmodifiableList(new ArrayList<>(hobbies));
        }
        
        public String getName() { return name; }
        public int getAge() { return age; }
        public List<String> getHobbies() { return hobbies; }
        
        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + ", hobbies=" + hobbies + "}";
        }
    }
    
    // Immutable list operations
    public static void demonstrateImmutableLists() {
        List<String> originalList = Arrays.asList("A", "B", "C");
        
        // Create immutable list
        List<String> immutableList = Collections.unmodifiableList(originalList);
        
        // Multiple threads can safely read
        Thread[] readers = new Thread[3];
        
        for (int i = 0; i < 3; i++) {
            final int readerId = i;
            readers[i] = new Thread(() -> {
                for (String item : immutableList) {
                    System.out.println("Reader " + readerId + " read: " + item);
                }
            });
            readers[i].start();
        }
        
        // Wait for all threads
        for (Thread thread : readers) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
    
    // Using immutable collections
    public static void demonstrateImmutableCollections() {
        // Create immutable collections
        Set<String> immutableSet = Set.of("Apple", "Banana", "Cherry");
        Map<String, Integer> immutableMap = Map.of("Apple", 1, "Banana", 2, "Cherry", 3);
        
        // Multiple threads can safely access
        Thread[] threads = new Thread[5];
        
        for (int i = 0; i < 5; i++) {
            final int threadId = i;
            threads[i] = new Thread(() -> {
                System.out.println("Thread " + threadId + " set: " + immutableSet);
                System.out.println("Thread " + threadId + " map: " + immutableMap);
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

This comprehensive explanation covers all concurrent data structures, providing both theoretical understanding and practical Java examples to illustrate each concept.