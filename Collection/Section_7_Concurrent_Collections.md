# Section 7 – Concurrent Collections

## 7.1 Concurrent Collection Concepts

Concurrent collections are thread-safe implementations of the Collection Framework that allow multiple threads to safely access and modify collections without external synchronization. Understanding these concepts is crucial for building robust multi-threaded applications.

### What are Concurrent Collections?

Concurrent collections are specialized implementations that provide thread safety through various mechanisms:
- **Lock-free algorithms**: Use compare-and-swap operations
- **Fine-grained locking**: Multiple locks for different parts of the collection
- **Copy-on-write**: Create new copies when modifications occur
- **Atomic operations**: Use hardware-level atomic operations

### Key Characteristics of Concurrent Collections

#### 1. Thread Safety
- Multiple threads can safely access and modify collections
- No external synchronization required
- Operations are atomic and consistent

#### 2. Performance Considerations
- Better performance than synchronized collections
- Reduced contention between threads
- Optimized for concurrent access patterns

#### 3. Consistency Guarantees
- Operations are atomic
- Iterators may not reflect all modifications
- Some operations may have relaxed consistency

### Common Concurrent Collection Types

| Collection Type | Concurrent Implementation | Thread Safety | Performance |
|----------------|---------------------------|---------------|-------------|
| Map | ConcurrentHashMap | Yes | High |
| List | CopyOnWriteArrayList | Yes | Medium |
| Set | CopyOnWriteArraySet | Yes | Medium |
| Queue | BlockingQueue implementations | Yes | High |

### Real-World Analogy: Shared Workspace

Think of concurrent collections as different types of shared workspaces:

- **ConcurrentHashMap**: Like a shared filing cabinet where multiple people can access different drawers simultaneously without blocking each other
- **CopyOnWriteArrayList**: Like a shared whiteboard where everyone gets a copy when someone wants to write, ensuring no one's reading is interrupted
- **BlockingQueue**: Like a shared mailbox where people can put messages in and take messages out, with automatic waiting when the mailbox is full or empty

## 7.2 ConcurrentHashMap

ConcurrentHashMap is a thread-safe implementation of Map that provides high performance for concurrent access through fine-grained locking and lock-free operations.

### Core Characteristics

#### 1. Fine-Grained Locking
- Uses multiple locks (segments) instead of a single lock
- Reduces contention between threads
- Allows concurrent read operations

#### 2. Performance Characteristics
- **Get**: O(1) average, O(n) worst case
- **Put**: O(1) average, O(n) worst case
- **Remove**: O(1) average, O(n) worst case
- **Concurrent Operations**: High performance

#### 3. Thread Safety
- All operations are thread-safe
- No external synchronization required
- Iterators are weakly consistent

### Understanding ConcurrentHashMap Operations

#### 1. Basic Operations
```java
// Create ConcurrentHashMap
ConcurrentHashMap<String, Integer> ages = new ConcurrentHashMap<>();
ConcurrentHashMap<String, Integer> agesWithCapacity = new ConcurrentHashMap<>(16);
ConcurrentHashMap<String, Integer> agesWithLoadFactor = new ConcurrentHashMap<>(16, 0.75f);

// Add key-value pairs
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

System.out.println("Ages: " + ages); // {Alice=25, Bob=30, Charlie=35}
System.out.println("Size: " + ages.size()); // 3
```

#### 2. Thread-Safe Operations
```java
ConcurrentHashMap<String, Integer> ages = new ConcurrentHashMap<>();

// Multiple threads can safely access
Thread thread1 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        ages.put("Thread1-" + i, i);
    }
});

Thread thread2 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        ages.put("Thread2-" + i, i);
    }
});

thread1.start();
thread2.start();

// Wait for threads to complete
try {
    thread1.join();
    thread2.join();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

System.out.println("Final size: " + ages.size()); // 2000
```

#### 3. Atomic Operations
```java
ConcurrentHashMap<String, Integer> ages = new ConcurrentHashMap<>();
ages.put("Alice", 25);

// Atomic update
ages.compute("Alice", (key, value) -> value + 1);
System.out.println("Alice's age: " + ages.get("Alice")); // 26

// Atomic put if absent
Integer previous = ages.putIfAbsent("Bob", 30);
System.out.println("Previous value: " + previous); // null
System.out.println("Bob's age: " + ages.get("Bob")); // 30

// Atomic replace
boolean replaced = ages.replace("Alice", 26, 27);
System.out.println("Replaced: " + replaced); // true
System.out.println("Alice's age: " + ages.get("Alice")); // 27
```

#### 4. Bulk Operations
```java
ConcurrentHashMap<String, Integer> ages = new ConcurrentHashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

// For each operation
ages.forEach((name, age) -> System.out.println(name + ": " + age));

// Search operation
String result = ages.search(1, (name, age) -> age > 30 ? name : null);
System.out.println("Person over 30: " + result); // Charlie

// Reduce operation
int totalAge = ages.reduce(1, (name, age) -> age, Integer::sum);
System.out.println("Total age: " + totalAge); // 90
```

### Real-World Example: Thread-Safe Cache
```java
public class ThreadSafeCache<K, V> {
    private final ConcurrentHashMap<K, V> cache = new ConcurrentHashMap<>();
    private final int maxSize;
    
    public ThreadSafeCache(int maxSize) {
        this.maxSize = maxSize;
    }
    
    public V get(K key) {
        return cache.get(key);
    }
    
    public V put(K key, V value) {
        if (cache.size() >= maxSize) {
            // Remove oldest entry (simplified)
            cache.entrySet().iterator().next().getKey();
        }
        return cache.put(key, value);
    }
    
    public V computeIfAbsent(K key, Function<K, V> mappingFunction) {
        return cache.computeIfAbsent(key, mappingFunction);
    }
    
    public V computeIfPresent(K key, BiFunction<K, V, V> remappingFunction) {
        return cache.computeIfPresent(key, remappingFunction);
    }
    
    public boolean remove(K key, V value) {
        return cache.remove(key, value);
    }
    
    public void clear() {
        cache.clear();
    }
    
    public int size() {
        return cache.size();
    }
    
    public boolean isEmpty() {
        return cache.isEmpty();
    }
    
    public Set<K> keySet() {
        return cache.keySet();
    }
    
    public Collection<V> values() {
        return cache.values();
    }
    
    public Set<Map.Entry<K, V>> entrySet() {
        return cache.entrySet();
    }
}
```

## 7.3 CopyOnWriteArrayList

CopyOnWriteArrayList is a thread-safe implementation of List that creates a new copy of the underlying array whenever it is modified.

### Core Characteristics

#### 1. Copy-on-Write Implementation
- Creates new array copy on each modification
- Readers never block writers
- Writers never block readers

#### 2. Performance Characteristics
- **Get**: O(1)
- **Add**: O(n) - due to array copying
- **Remove**: O(n) - due to array copying
- **Iteration**: O(n) - no locking required

#### 3. Memory Characteristics
- Higher memory usage due to copying
- Good for read-heavy workloads
- Poor for write-heavy workloads

### Understanding CopyOnWriteArrayList Operations

#### 1. Basic Operations
```java
// Create CopyOnWriteArrayList
List<String> names = new CopyOnWriteArrayList<>();
List<String> namesFromCollection = new CopyOnWriteArrayList<>(Arrays.asList("Alice", "Bob"));

// Add elements
names.add("Alice");
names.add("Bob");
names.add("Charlie");

System.out.println("Names: " + names); // [Alice, Bob, Charlie]
System.out.println("Size: " + names.size()); // 3
```

#### 2. Thread-Safe Operations
```java
CopyOnWriteArrayList<String> names = new CopyOnWriteArrayList<>();
names.add("Alice");
names.add("Bob");

// Multiple threads can safely access
Thread reader = new Thread(() -> {
    for (String name : names) {
        System.out.println("Reader: " + name);
    }
});

Thread writer = new Thread(() -> {
    names.add("Charlie");
    names.add("David");
});

reader.start();
writer.start();

// Wait for threads to complete
try {
    reader.join();
    writer.join();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

#### 3. Iterator Behavior
```java
CopyOnWriteArrayList<String> names = new CopyOnWriteArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

// Iterator is a snapshot of the list at creation time
Iterator<String> iterator = names.iterator();
names.add("David"); // This won't be seen by the iterator

while (iterator.hasNext()) {
    System.out.println("Iterator: " + iterator.next());
}
// Output: Alice, Bob, Charlie (David not included)

// New iterator will see all elements
Iterator<String> newIterator = names.iterator();
while (newIterator.hasNext()) {
    System.out.println("New Iterator: " + newIterator.next());
}
// Output: Alice, Bob, Charlie, David
```

### Real-World Example: Event Listener Management
```java
public class EventManager {
    private CopyOnWriteArrayList<EventListener> listeners = new CopyOnWriteArrayList<>();
    
    public void addListener(EventListener listener) {
        listeners.add(listener);
    }
    
    public void removeListener(EventListener listener) {
        listeners.remove(listener);
    }
    
    public void fireEvent(Event event) {
        // Safe to iterate without locking
        for (EventListener listener : listeners) {
            try {
                listener.onEvent(event);
            } catch (Exception e) {
                System.err.println("Error in event listener: " + e.getMessage());
            }
        }
    }
    
    public int getListenerCount() {
        return listeners.size();
    }
    
    public void clearListeners() {
        listeners.clear();
    }
    
    public interface EventListener {
        void onEvent(Event event);
    }
    
    public static class Event {
        private String type;
        private Object data;
        
        public Event(String type, Object data) {
            this.type = type;
            this.data = data;
        }
        
        public String getType() { return type; }
        public Object getData() { return data; }
    }
}
```

## 7.4 CopyOnWriteArraySet

CopyOnWriteArraySet is a thread-safe implementation of Set that uses CopyOnWriteArrayList internally.

### Core Characteristics

#### 1. Copy-on-Write Implementation
- Uses CopyOnWriteArrayList internally
- Creates new array copy on each modification
- Readers never block writers

#### 2. Performance Characteristics
- **Add**: O(n) - due to array copying and uniqueness check
- **Remove**: O(n) - due to array copying
- **Contains**: O(n) - linear search
- **Iteration**: O(n) - no locking required

#### 3. Memory Characteristics
- Higher memory usage due to copying
- Good for read-heavy workloads
- Poor for write-heavy workloads

### Understanding CopyOnWriteArraySet Operations

#### 1. Basic Operations
```java
// Create CopyOnWriteArraySet
Set<String> names = new CopyOnWriteArraySet<>();
Set<String> namesFromCollection = new CopyOnWriteArraySet<>(Arrays.asList("Alice", "Bob"));

// Add elements
names.add("Alice");
names.add("Bob");
names.add("Alice"); // Duplicate - will not be added
names.add("Charlie");

System.out.println("Names: " + names); // [Alice, Bob, Charlie]
System.out.println("Size: " + names.size()); // 3
```

#### 2. Thread-Safe Operations
```java
CopyOnWriteArraySet<String> names = new CopyOnWriteArraySet<>();
names.add("Alice");
names.add("Bob");

// Multiple threads can safely access
Thread reader = new Thread(() -> {
    for (String name : names) {
        System.out.println("Reader: " + name);
    }
});

Thread writer = new Thread(() -> {
    names.add("Charlie");
    names.add("David");
    names.add("Alice"); // Duplicate - will not be added
});

reader.start();
writer.start();

// Wait for threads to complete
try {
    reader.join();
    writer.join();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

#### 3. Set Operations
```java
CopyOnWriteArraySet<String> set1 = new CopyOnWriteArraySet<>();
set1.add("Alice");
set1.add("Bob");
set1.add("Charlie");

CopyOnWriteArraySet<String> set2 = new CopyOnWriteArraySet<>();
set2.add("Bob");
set2.add("Charlie");
set2.add("David");

// Union
CopyOnWriteArraySet<String> union = new CopyOnWriteArraySet<>(set1);
union.addAll(set2);
System.out.println("Union: " + union); // [Alice, Bob, Charlie, David]

// Intersection
CopyOnWriteArraySet<String> intersection = new CopyOnWriteArraySet<>(set1);
intersection.retainAll(set2);
System.out.println("Intersection: " + intersection); // [Bob, Charlie]

// Difference
CopyOnWriteArraySet<String> difference = new CopyOnWriteArraySet<>(set1);
difference.removeAll(set2);
System.out.println("Difference: " + difference); // [Alice]
```

### Real-World Example: Thread-Safe User Management
```java
public class ThreadSafeUserManager {
    private CopyOnWriteArraySet<String> usernames = new CopyOnWriteArraySet<>();
    private CopyOnWriteArraySet<String> emailAddresses = new CopyOnWriteArraySet<>();
    
    public boolean registerUser(String username, String email) {
        // Check for duplicate username
        if (usernames.contains(username)) {
            System.out.println("Username already exists: " + username);
            return false;
        }
        
        // Check for duplicate email
        if (emailAddresses.contains(email)) {
            System.out.println("Email already registered: " + email);
            return false;
        }
        
        // Add new user
        usernames.add(username);
        emailAddresses.add(email);
        System.out.println("User registered successfully: " + username);
        return true;
    }
    
    public boolean isUsernameAvailable(String username) {
        return !usernames.contains(username);
    }
    
    public boolean isEmailRegistered(String email) {
        return emailAddresses.contains(email);
    }
    
    public Set<String> getAllUsernames() {
        return new HashSet<>(usernames); // Return copy
    }
    
    public boolean removeUser(String username) {
        if (usernames.remove(username)) {
            // Also remove associated email (simplified)
            emailAddresses.remove(username + "@example.com");
            return true;
        }
        return false;
    }
    
    public int getUserCount() {
        return usernames.size();
    }
    
    public void clearUsers() {
        usernames.clear();
        emailAddresses.clear();
    }
}
```

## 7.5 BlockingQueue Implementations

BlockingQueue implementations provide thread-safe queue operations with blocking behavior for synchronization between producer and consumer threads.

### Core Characteristics

#### 1. Thread-Safe Operations
- All operations are thread-safe
- Multiple threads can safely access the queue
- Blocking operations for synchronization

#### 2. Blocking Behavior
- **put()**: Blocks if queue is full
- **take()**: Blocks if queue is empty
- **offer()**: Non-blocking add operation
- **poll()**: Non-blocking remove operation

#### 3. Capacity Management
- Some implementations have fixed capacity
- Others can grow dynamically
- Blocking behavior depends on capacity

### Understanding BlockingQueue Operations

#### 1. Basic Operations
```java
// Create BlockingQueue
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
BlockingQueue<String> linkedQueue = new LinkedBlockingQueue<>();
BlockingQueue<String> priorityQueue = new PriorityBlockingQueue<>();

// Add elements
queue.offer("Alice");
queue.offer("Bob");
queue.offer("Charlie");

System.out.println("Queue: " + queue); // [Alice, Bob, Charlie]
System.out.println("Size: " + queue.size()); // 3
```

#### 2. Blocking Operations
```java
BlockingQueue<String> queue = new ArrayBlockingQueue<>(2);

// Non-blocking operations
boolean added = queue.offer("Alice"); // true
boolean added2 = queue.offer("Bob");  // true
boolean added3 = queue.offer("Charlie"); // false (queue full)

// Blocking operations
try {
    queue.put("David"); // Will block until space is available
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

// Remove with blocking
try {
    String item = queue.take(); // Will block until item is available
    System.out.println("Took: " + item);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

#### 3. Timeout Operations
```java
BlockingQueue<String> queue = new ArrayBlockingQueue<>(2);

// Offer with timeout
try {
    boolean added = queue.offer("Alice", 1, TimeUnit.SECONDS);
    System.out.println("Added: " + added);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

// Poll with timeout
try {
    String item = queue.poll(1, TimeUnit.SECONDS);
    System.out.println("Polled: " + item);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

### Real-World Example: Producer-Consumer Pattern
```java
public class ProducerConsumerExample {
    private BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
    private volatile boolean running = true;
    
    public void start() {
        // Start producer thread
        Thread producer = new Thread(this::produce);
        producer.start();
        
        // Start consumer thread
        Thread consumer = new Thread(this::consume);
        consumer.start();
        
        // Let it run for 5 seconds
        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        // Stop
        running = false;
        producer.interrupt();
        consumer.interrupt();
    }
    
    private void produce() {
        int count = 0;
        while (running) {
            try {
                String item = "Item " + count++;
                queue.put(item); // Blocks if queue is full
                System.out.println("Produced: " + item);
                Thread.sleep(100); // Simulate work
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    private void consume() {
        while (running) {
            try {
                String item = queue.take(); // Blocks if queue is empty
                System.out.println("Consumed: " + item);
                Thread.sleep(150); // Simulate work
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
}
```

## 7.6 Concurrent Collection Best Practices

Following best practices ensures optimal performance and maintainable code when working with concurrent collections.

### 1. Choose the Right Implementation

#### Use ConcurrentHashMap When:
- Thread-safe map operations needed
- High performance required
- Fine-grained locking acceptable

```java
// Good for thread-safe map operations
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("Alice", 25);
Integer age = map.get("Alice"); // Thread-safe
```

#### Use CopyOnWriteArrayList When:
- Thread-safe list operations needed
- Read-heavy workload
- Infrequent modifications

```java
// Good for read-heavy workloads
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
list.add("Alice");
for (String item : list) { // Safe iteration
    System.out.println(item);
}
```

#### Use CopyOnWriteArraySet When:
- Thread-safe set operations needed
- Read-heavy workload
- Infrequent modifications

```java
// Good for read-heavy set operations
CopyOnWriteArraySet<String> set = new CopyOnWriteArraySet<>();
set.add("Alice");
for (String item : set) { // Safe iteration
    System.out.println(item);
}
```

#### Use BlockingQueue When:
- Producer-consumer pattern
- Thread synchronization needed
- Bounded queue operations

```java
// Good for producer-consumer pattern
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
queue.put("Alice"); // Thread-safe
String item = queue.take(); // Thread-safe
```

### 2. Handle InterruptedException Properly

```java
// Good: Handle InterruptedException
try {
    String item = queue.take();
    // Process item
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    // Handle interruption
}

// Bad: Ignore InterruptedException
String item = queue.take(); // Can throw InterruptedException
```

### 3. Use Atomic Operations

```java
// Good: Use atomic operations
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.compute("Alice", (key, value) -> value == null ? 1 : value + 1);

// Bad: Non-atomic operations
Integer value = map.get("Alice");
map.put("Alice", value + 1); // Not atomic
```

### 4. Avoid Blocking in Main Thread

```java
// Good: Use non-blocking operations in main thread
if (queue.offer(item)) {
    // Item added successfully
} else {
    // Handle queue full
}

// Bad: Use blocking operations in main thread
queue.put(item); // Can block main thread
```

### 5. Use Timeout Operations

```java
// Good: Use timeout operations
try {
    String item = queue.poll(1, TimeUnit.SECONDS);
    if (item != null) {
        // Process item
    } else {
        // Handle timeout
    }
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}
```

## 7.7 Concurrent Collection Testing

Comprehensive testing ensures concurrent collections work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testConcurrentHashMapOperations() {
    ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
    
    // Test put
    map.put("Alice", 25);
    assertEquals(1, map.size());
    assertTrue(map.containsKey("Alice"));
    assertTrue(map.containsValue(25));
    
    // Test get
    assertEquals(Integer.valueOf(25), map.get("Alice"));
    assertNull(map.get("Bob"));
    
    // Test remove
    assertEquals(Integer.valueOf(25), map.remove("Alice"));
    assertEquals(0, map.size());
    assertFalse(map.containsKey("Alice"));
}
```

### 2. Thread Safety Testing

```java
@Test
public void testThreadSafety() throws InterruptedException {
    ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
    int numThreads = 10;
    int itemsPerThread = 1000;
    
    // Create producer threads
    List<Thread> producers = new ArrayList<>();
    for (int i = 0; i < numThreads; i++) {
        final int threadId = i;
        Thread producer = new Thread(() -> {
            for (int j = 0; j < itemsPerThread; j++) {
                map.put("Thread-" + threadId + "-Item-" + j, j);
            }
        });
        producers.add(producer);
        producer.start();
    }
    
    // Wait for all producers to complete
    for (Thread producer : producers) {
        producer.join();
    }
    
    // Verify all items were added
    assertEquals(numThreads * itemsPerThread, map.size());
}
```

### 3. Performance Testing

```java
@Test
public void testConcurrentPerformance() throws InterruptedException {
    ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
    int numThreads = 10;
    int operationsPerThread = 10000;
    
    // Create threads
    List<Thread> threads = new ArrayList<>();
    for (int i = 0; i < numThreads; i++) {
        final int threadId = i;
        Thread thread = new Thread(() -> {
            for (int j = 0; j < operationsPerThread; j++) {
                String key = "Thread-" + threadId + "-Item-" + j;
                map.put(key, j);
                map.get(key);
                map.remove(key);
            }
        });
        threads.add(thread);
        thread.start();
    }
    
    // Wait for all threads to complete
    for (Thread thread : threads) {
        thread.join();
    }
    
    // Verify map is empty
    assertTrue(map.isEmpty());
}
```

## 7.8 Concurrent Collection Performance

Understanding performance characteristics helps in choosing the right implementation and optimizing code.

### Performance Comparison

| Operation | ConcurrentHashMap | CopyOnWriteArrayList | CopyOnWriteArraySet | BlockingQueue |
|-----------|-------------------|---------------------|-------------------|---------------|
| get() | O(1) avg | O(1) | O(n) | O(1) |
| put() | O(1) avg | O(n) | O(n) | O(1) |
| remove() | O(1) avg | O(n) | O(n) | O(1) |
| contains() | O(1) avg | O(n) | O(n) | O(n) |

### Memory Usage

```java
// ConcurrentHashMap memory usage
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
// Memory: hash table + buckets + entries + locks

// CopyOnWriteArrayList memory usage
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
// Memory: array + copying overhead

// CopyOnWriteArraySet memory usage
CopyOnWriteArraySet<String> set = new CopyOnWriteArraySet<>();
// Memory: array + copying overhead + uniqueness check

// BlockingQueue memory usage
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
// Memory: array + synchronization overhead
```

### Performance Optimization Tips

#### 1. Use Appropriate Implementation
```java
// Good: Use ConcurrentHashMap for thread-safe map operations
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// Bad: Use CopyOnWriteArrayList for frequent modifications
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
for (int i = 0; i < 1000000; i++) {
    list.add("Item " + i); // O(n) per operation
}
```

#### 2. Use Atomic Operations
```java
// Good: Use atomic operations
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.compute("Alice", (key, value) -> value == null ? 1 : value + 1);

// Bad: Non-atomic operations
Integer value = map.get("Alice");
map.put("Alice", value + 1); // Not atomic
```

#### 3. Avoid Unnecessary Copying
```java
// Good: Use appropriate collection for use case
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("Alice", 25);

// Bad: Use CopyOnWriteArrayList for frequent modifications
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
for (int i = 0; i < 1000000; i++) {
    list.add("Item " + i); // Creates new array each time
}
```

## 7.9 Concurrent Collection Troubleshooting

Common issues and solutions when working with concurrent collections.

### 1. InterruptedException Handling

```java
// Problem: Ignoring InterruptedException
try {
    String item = queue.take();
} catch (InterruptedException e) {
    // Ignoring interruption
}

// Solution: Properly handle interruption
try {
    String item = queue.take();
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    // Handle interruption appropriately
}
```

### 2. Performance Issues

```java
// Problem: Using wrong implementation
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
for (int i = 0; i < 1000000; i++) {
    list.add("Item " + i); // O(n) per operation
}

// Solution: Use appropriate implementation
ConcurrentHashMap<String, String> map = new ConcurrentHashMap<>();
for (int i = 0; i < 1000000; i++) {
    map.put("Key" + i, "Item " + i); // O(1) average per operation
}
```

### 3. Memory Issues

```java
// Problem: Not clearing references
ConcurrentHashMap<String, Integer> largeMap = new ConcurrentHashMap<>();
// ... populate with large data
largeMap = null; // Still holds references

// Solution: Clear references
largeMap.clear();
largeMap = null;
```

### 4. Thread Safety Issues

```java
// Problem: Using non-thread-safe collections in multi-threaded environment
Map<String, Integer> map = new HashMap<>();
// Multiple threads accessing map can cause issues

// Solution: Use thread-safe collections
Map<String, Integer> map = new ConcurrentHashMap<>();
// Multiple threads can safely access
```

## 7.10 Concurrent Collection Security

Security considerations when working with concurrent collections.

### 1. Input Validation

```java
public class SecureConcurrentManager {
    private ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();
    private int maxSize = 1000;
    
    public boolean addData(String key, String value) {
        // Validate input
        if (key == null || key.trim().isEmpty()) {
            throw new IllegalArgumentException("Key cannot be null or empty");
        }
        
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException("Value cannot be null or empty");
        }
        
        if (data.size() >= maxSize) {
            throw new IllegalStateException("Map is full");
        }
        
        // Sanitize input
        String sanitizedKey = key.trim().replaceAll("[<>\"'&]", "");
        String sanitizedValue = value.trim().replaceAll("[<>\"'&]", "");
        
        return data.put(sanitizedKey, sanitizedValue) == null;
    }
}
```

### 2. Access Control

```java
public class SecureConcurrentWrapper {
    private ConcurrentHashMap<String, String> data = new ConcurrentHashMap<>();
    private Set<String> allowedUsers = new ConcurrentHashMap<String, Boolean>().keySet();
    
    public boolean addData(String user, String key, String value) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return data.put(key, value) == null;
    }
    
    public String getData(String user, String key) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return data.get(key);
    }
}
```

### 3. Data Encryption

```java
public class EncryptedConcurrentManager {
    private ConcurrentHashMap<String, String> encryptedData = new ConcurrentHashMap<>();
    private String encryptionKey = "secret-key";
    
    public void addEncryptedData(String key, String value) {
        String encrypted = encrypt(value, encryptionKey);
        encryptedData.put(key, encrypted);
    }
    
    public String getDecryptedData(String key) {
        String encrypted = encryptedData.get(key);
        if (encrypted != null) {
            return decrypt(encrypted, encryptionKey);
        }
        return null;
    }
    
    private String encrypt(String data, String key) {
        // Implementation of encryption
        return data; // Placeholder
    }
    
    private String decrypt(String encrypted, String key) {
        // Implementation of decryption
        return encrypted; // Placeholder
    }
}
```

Understanding concurrent collections is crucial for building robust multi-threaded applications. Each implementation has its strengths and weaknesses, and choosing the right one depends on your specific use case, performance requirements, and concurrency patterns.