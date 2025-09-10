# Section 5 – Queue Implementations

## 5.1 Queue Implementation Concepts

Queue implementations are concrete classes that provide specific ways to store and manage elements in a FIFO (First-In-First-Out) or LIFO (Last-In-First-Out) order. Understanding the different Queue implementations and their characteristics is essential for choosing the right one for your use case.

### What are Queue Implementations?

Queue implementations are classes that implement the Queue interface, providing different underlying data structures and performance characteristics. Each implementation is optimized for specific operations and use cases while maintaining the fundamental property of ordered element processing.

### Key Characteristics of Queue Implementations

#### 1. Ordered Collection
- Elements are processed in a specific order
- FIFO (First-In-First-Out) for most implementations
- LIFO (Last-In-First-Out) for stack-like implementations

#### 2. Limited Access
- Elements can only be accessed at specific positions
- Typically at the head (front) and tail (back)
- No random access to middle elements

#### 3. Processing Order
- Designed for sequential processing
- Elements are added at one end and removed from the other
- Maintains processing order

#### 4. Thread Safety
- Some implementations are thread-safe
- Blocking operations available in some implementations
- Concurrent access support

### Common Queue Implementations

| Implementation | Data Structure | Order | Thread Safe | Blocking | Performance |
|----------------|----------------|-------|-------------|----------|-------------|
| PriorityQueue | Binary Heap | Priority | No | No | O(log n) |
| ArrayDeque | Circular Array | FIFO/LIFO | No | No | O(1) |
| LinkedList | Doubly Linked List | FIFO | No | No | O(1) |
| BlockingQueue | Various | FIFO | Yes | Yes | Varies |

### Real-World Analogy: Different Types of Queues

Think of Queue implementations as different types of waiting lines:

- **PriorityQueue**: Like a hospital emergency room where patients are treated based on severity, not arrival time
- **ArrayDeque**: Like a double-ended line where people can join or leave from either end
- **LinkedList**: Like a simple line where people join at the back and leave from the front
- **BlockingQueue**: Like a line with a maximum capacity where people must wait if it's full

## 5.2 PriorityQueue

PriorityQueue implements a priority queue using a binary heap, where elements are ordered according to their natural ordering or a provided comparator.

### Core Characteristics

#### 1. Binary Heap Implementation
- Uses a complete binary tree stored in an array
- Maintains heap property (parent is smaller/larger than children)
- Automatically reorders elements based on priority

#### 2. Performance Characteristics
- **Add**: O(log n)
- **Remove**: O(log n)
- **Peek**: O(1)
- **Contains**: O(n)
- **Iteration**: O(n) - not in priority order

#### 3. Ordering Characteristics
- Elements are ordered by priority, not insertion order
- Highest priority element is always at the head
- Natural ordering or custom comparator

### Understanding PriorityQueue Operations

#### 1. Basic Operations
```java
// Create PriorityQueue
Queue<String> queue = new PriorityQueue<>();
Queue<String> queueWithCapacity = new PriorityQueue<>(10);
Queue<String> queueWithComparator = new PriorityQueue<>(String.CASE_INSENSITIVE_ORDER);

// Add elements
queue.offer("Charlie");
queue.offer("Alice");
queue.offer("Bob");
queue.offer("David");

System.out.println("Queue: " + queue); // [Alice, Bob, Charlie, David] (sorted order)
System.out.println("Size: " + queue.size()); // 4
```

#### 2. Priority Ordering
```java
// Natural ordering (alphabetical)
Queue<String> names = new PriorityQueue<>();
names.offer("Zoe");
names.offer("Alice");
names.offer("Bob");
names.offer("Charlie");

// Peek at highest priority element
String highest = names.peek();
System.out.println("Highest priority: " + highest); // Alice

// Remove highest priority element
String removed = names.poll();
System.out.println("Removed: " + removed); // Alice
System.out.println("After poll: " + names); // [Bob, Charlie, Zoe]
```

#### 3. Custom Comparator
```java
// Custom comparator for reverse order
Queue<String> reverseQueue = new PriorityQueue<>(Collections.reverseOrder());
reverseQueue.offer("Alice");
reverseQueue.offer("Bob");
reverseQueue.offer("Charlie");

System.out.println("Reverse queue: " + reverseQueue); // [Charlie, Bob, Alice]

// Custom comparator for length
Queue<String> lengthQueue = new PriorityQueue<>((a, b) -> Integer.compare(a.length(), b.length()));
lengthQueue.offer("Alice");
lengthQueue.offer("Bob");
lengthQueue.offer("Charlie");

System.out.println("Length queue: " + lengthQueue); // [Bob, Alice, Charlie]
```

#### 4. Object Priority Queue
```java
// Custom object with priority
class Task implements Comparable<Task> {
    private String name;
    private int priority;
    
    public Task(String name, int priority) {
        this.name = name;
        this.priority = priority;
    }
    
    @Override
    public int compareTo(Task other) {
        return Integer.compare(this.priority, other.priority); // Lower number = higher priority
    }
    
    @Override
    public String toString() {
        return name + " (priority: " + priority + ")";
    }
}

Queue<Task> taskQueue = new PriorityQueue<>();
taskQueue.offer(new Task("Low priority task", 3));
taskQueue.offer(new Task("High priority task", 1));
taskQueue.offer(new Task("Medium priority task", 2));

// Process tasks in priority order
while (!taskQueue.isEmpty()) {
    Task task = taskQueue.poll();
    System.out.println("Processing: " + task);
}
```

### Real-World Example: Task Scheduler
```java
public class TaskScheduler {
    private Queue<Task> taskQueue = new PriorityQueue<>();
    private int maxTasks = 1000;
    
    public void addTask(Task task) {
        if (taskQueue.size() >= maxTasks) {
            throw new IllegalStateException("Task queue is full");
        }
        taskQueue.offer(task);
    }
    
    public Task getNextTask() {
        return taskQueue.poll();
    }
    
    public Task peekNextTask() {
        return taskQueue.peek();
    }
    
    public boolean hasTasks() {
        return !taskQueue.isEmpty();
    }
    
    public int getTaskCount() {
        return taskQueue.size();
    }
    
    public List<Task> getAllTasks() {
        return new ArrayList<>(taskQueue);
    }
    
    public void clearCompletedTasks() {
        taskQueue.clear();
    }
    
    public static class Task implements Comparable<Task> {
        private String name;
        private int priority;
        private long timestamp;
        
        public Task(String name, int priority) {
            this.name = name;
            this.priority = priority;
            this.timestamp = System.currentTimeMillis();
        }
        
        @Override
        public int compareTo(Task other) {
            // First by priority (lower number = higher priority)
            int priorityCompare = Integer.compare(this.priority, other.priority);
            if (priorityCompare != 0) {
                return priorityCompare;
            }
            // Then by timestamp (earlier = higher priority)
            return Long.compare(this.timestamp, other.timestamp);
        }
        
        public String getName() { return name; }
        public int getPriority() { return priority; }
        public long getTimestamp() { return timestamp; }
        
        @Override
        public String toString() {
            return name + " (priority: " + priority + ", time: " + timestamp + ")";
        }
    }
}
```

## 5.3 ArrayDeque

ArrayDeque implements a double-ended queue using a resizable array, providing efficient operations at both ends.

### Core Characteristics

#### 1. Circular Array Implementation
- Uses a resizable array with head and tail pointers
- Elements can be added/removed from both ends
- Automatically grows when capacity is exceeded

#### 2. Performance Characteristics
- **Add at End**: O(1) amortized
- **Add at Beginning**: O(1) amortized
- **Remove from End**: O(1)
- **Remove from Beginning**: O(1)
- **Random Access**: O(1) - but not recommended

#### 3. Memory Characteristics
- Contiguous memory allocation
- Good cache locality
- Lower memory overhead than LinkedList

### Understanding ArrayDeque Operations

#### 1. Basic Operations
```java
// Create ArrayDeque
Deque<String> deque = new ArrayDeque<>();
Deque<String> dequeWithCapacity = new ArrayDeque<>(10);

// Add elements at the end
deque.addLast("Alice");
deque.addLast("Bob");
deque.addLast("Charlie");

System.out.println("Deque: " + deque); // [Alice, Bob, Charlie]
System.out.println("Size: " + deque.size()); // 3
```

#### 2. Double-Ended Operations
```java
Deque<String> deque = new ArrayDeque<>();

// Add at beginning
deque.addFirst("First");
deque.addFirst("Second");

// Add at end
deque.addLast("Third");
deque.addLast("Fourth");

System.out.println("Deque: " + deque); // [Second, First, Third, Fourth]

// Remove from beginning
String first = deque.removeFirst();
System.out.println("Removed first: " + first); // Second
System.out.println("After removeFirst: " + deque); // [First, Third, Fourth]

// Remove from end
String last = deque.removeLast();
System.out.println("Removed last: " + last); // Fourth
System.out.println("After removeLast: " + deque); // [First, Third]
```

#### 3. Peek Operations
```java
Deque<String> deque = new ArrayDeque<>();
deque.addLast("Alice");
deque.addLast("Bob");
deque.addLast("Charlie");

// Peek at first element
String first = deque.peekFirst();
System.out.println("First element: " + first); // Alice

// Peek at last element
String last = deque.peekLast();
System.out.println("Last element: " + last); // Charlie

// Peek at first element (same as peekFirst)
String head = deque.peek();
System.out.println("Head element: " + head); // Alice
```

#### 4. Stack Operations
```java
// Use ArrayDeque as a stack
Deque<String> stack = new ArrayDeque<>();

// Push elements
stack.push("Alice");
stack.push("Bob");
stack.push("Charlie");

System.out.println("Stack: " + stack); // [Charlie, Bob, Alice]

// Pop elements
String popped = stack.pop();
System.out.println("Popped: " + popped); // Charlie
System.out.println("After pop: " + stack); // [Bob, Alice]

// Peek at top
String top = stack.peek();
System.out.println("Top: " + top); // Bob
```

### Real-World Example: Undo/Redo System
```java
public class UndoRedoManager {
    private Deque<String> undoStack = new ArrayDeque<>();
    private Deque<String> redoStack = new ArrayDeque<>();
    private int maxHistory = 100;
    
    public void performAction(String action) {
        // Add to undo stack
        undoStack.push(action);
        
        // Clear redo stack when new action is performed
        redoStack.clear();
        
        // Maintain size limit
        if (undoStack.size() > maxHistory) {
            // Remove oldest action
            Deque<String> temp = new ArrayDeque<>();
            while (undoStack.size() > maxHistory - 1) {
                temp.push(undoStack.pop());
            }
            undoStack.clear();
            while (!temp.isEmpty()) {
                undoStack.push(temp.pop());
            }
        }
        
        System.out.println("Performed: " + action);
    }
    
    public String undo() {
        if (undoStack.isEmpty()) {
            System.out.println("Nothing to undo");
            return null;
        }
        
        String action = undoStack.pop();
        redoStack.push(action);
        System.out.println("Undone: " + action);
        return action;
    }
    
    public String redo() {
        if (redoStack.isEmpty()) {
            System.out.println("Nothing to redo");
            return null;
        }
        
        String action = redoStack.pop();
        undoStack.push(action);
        System.out.println("Redone: " + action);
        return action;
    }
    
    public boolean canUndo() {
        return !undoStack.isEmpty();
    }
    
    public boolean canRedo() {
        return !redoStack.isEmpty();
    }
    
    public void clear() {
        undoStack.clear();
        redoStack.clear();
    }
    
    public List<String> getUndoHistory() {
        return new ArrayList<>(undoStack);
    }
    
    public List<String> getRedoHistory() {
        return new ArrayList<>(redoStack);
    }
}
```

## 5.4 LinkedList as Queue

LinkedList can be used as a Queue implementation, providing efficient operations at both ends.

### Core Characteristics

#### 1. Doubly Linked List Implementation
- Uses doubly linked list structure
- Elements can be added/removed from both ends
- No capacity restrictions

#### 2. Performance Characteristics
- **Add at End**: O(1)
- **Add at Beginning**: O(1)
- **Remove from End**: O(1)
- **Remove from Beginning**: O(1)
- **Random Access**: O(n)

#### 3. Memory Characteristics
- Higher memory overhead than ArrayDeque
- Non-contiguous memory allocation
- Poor cache locality

### Understanding LinkedList as Queue

#### 1. Basic Queue Operations
```java
// Create LinkedList as Queue
Queue<String> queue = new LinkedList<>();

// Add elements
queue.offer("Alice");
queue.offer("Bob");
queue.offer("Charlie");

System.out.println("Queue: " + queue); // [Alice, Bob, Charlie]
System.out.println("Size: " + queue.size()); // 3
```

#### 2. Queue-Specific Operations
```java
Queue<String> queue = new LinkedList<>();
queue.offer("Alice");
queue.offer("Bob");
queue.offer("Charlie");

// Peek at head element
String head = queue.peek();
System.out.println("Head: " + head); // Alice

// Remove head element
String removed = queue.poll();
System.out.println("Removed: " + removed); // Alice
System.out.println("After poll: " + queue); // [Bob, Charlie]

// Check if empty
System.out.println("Empty: " + queue.isEmpty()); // false
```

#### 3. Deque Operations
```java
// Use LinkedList as Deque
Deque<String> deque = new LinkedList<>();

// Add at beginning
deque.addFirst("First");
deque.addFirst("Second");

// Add at end
deque.addLast("Third");
deque.addLast("Fourth");

System.out.println("Deque: " + deque); // [Second, First, Third, Fourth]

// Remove from beginning
String first = deque.removeFirst();
System.out.println("Removed first: " + first); // Second

// Remove from end
String last = deque.removeLast();
System.out.println("Removed last: " + last); // Fourth
```

### Real-World Example: Message Queue
```java
public class MessageQueue {
    private Queue<Message> messageQueue = new LinkedList<>();
    private int maxSize = 1000;
    
    public void enqueue(Message message) {
        if (messageQueue.size() >= maxSize) {
            throw new IllegalStateException("Message queue is full");
        }
        messageQueue.offer(message);
    }
    
    public Message dequeue() {
        return messageQueue.poll();
    }
    
    public Message peek() {
        return messageQueue.peek();
    }
    
    public boolean isEmpty() {
        return messageQueue.isEmpty();
    }
    
    public int size() {
        return messageQueue.size();
    }
    
    public void clear() {
        messageQueue.clear();
    }
    
    public List<Message> getAllMessages() {
        return new ArrayList<>(messageQueue);
    }
    
    public static class Message {
        private String content;
        private long timestamp;
        private String sender;
        
        public Message(String content, String sender) {
            this.content = content;
            this.sender = sender;
            this.timestamp = System.currentTimeMillis();
        }
        
        public String getContent() { return content; }
        public String getSender() { return sender; }
        public long getTimestamp() { return timestamp; }
        
        @Override
        public String toString() {
            return "[" + sender + "]: " + content + " (" + timestamp + ")";
        }
    }
}
```

## 5.5 BlockingQueue

BlockingQueue is an interface that extends Queue and provides blocking operations for thread-safe queue operations.

### Core Characteristics

#### 1. Thread-Safe Operations
- All operations are thread-safe
- Multiple threads can safely access the queue
- Blocking operations for synchronization

#### 2. Blocking Operations
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

## 5.6 Queue Implementation Best Practices

Following best practices ensures optimal performance and maintainable code when working with Queue implementations.

### 1. Choose the Right Implementation

#### Use PriorityQueue When:
- Elements need to be processed by priority
- Order doesn't matter, only priority
- Custom ordering is required

```java
// Good for priority-based processing
Queue<Task> taskQueue = new PriorityQueue<>();
taskQueue.offer(new Task("High priority", 1));
taskQueue.offer(new Task("Low priority", 3));
// High priority task will be processed first
```

#### Use ArrayDeque When:
- Efficient operations at both ends needed
- Memory efficiency is important
- Stack or double-ended queue functionality

```java
// Good for double-ended operations
Deque<String> deque = new ArrayDeque<>();
deque.addFirst("First");
deque.addLast("Last");
```

#### Use LinkedList When:
- Simple queue operations needed
- No capacity restrictions
- Memory usage is not critical

```java
// Good for simple queue operations
Queue<String> queue = new LinkedList<>();
queue.offer("Alice");
queue.poll();
```

#### Use BlockingQueue When:
- Thread safety is required
- Producer-consumer pattern
- Synchronization between threads

```java
// Good for thread-safe operations
BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
queue.put("Alice"); // Thread-safe
```

### 2. Handle Blocking Operations Properly

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

### 3. Use Appropriate Capacity

```java
// Good: Set appropriate capacity
BlockingQueue<String> queue = new ArrayBlockingQueue<>(expectedSize);

// Bad: Use default capacity
BlockingQueue<String> queue = new ArrayBlockingQueue<>(1); // Too small
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

## 5.7 Queue Implementation Testing

Comprehensive testing ensures Queue implementations work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testQueueOperations() {
    Queue<String> queue = new LinkedList<>();
    
    // Test offer
    assertTrue(queue.offer("Alice"));
    assertEquals(1, queue.size());
    
    // Test peek
    assertEquals("Alice", queue.peek());
    assertEquals(1, queue.size()); // Size unchanged
    
    // Test poll
    assertEquals("Alice", queue.poll());
    assertEquals(0, queue.size());
    
    // Test empty queue
    assertNull(queue.poll());
    assertTrue(queue.isEmpty());
}
```

### 2. Performance Testing

```java
@Test
public void testQueuePerformance() {
    Queue<String> queue = new LinkedList<>();
    int size = 100000;
    
    // Test offer performance
    long startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        queue.offer("Item " + i);
    }
    long offerTime = System.currentTimeMillis() - startTime;
    
    // Test poll performance
    startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        String item = queue.poll();
    }
    long pollTime = System.currentTimeMillis() - startTime;
    
    System.out.println("Offer time: " + offerTime + "ms");
    System.out.println("Poll time: " + pollTime + "ms");
    
    assertTrue(offerTime < 1000); // Should complete within 1 second
    assertTrue(pollTime < 1000);  // Should complete within 1 second
}
```

### 3. Thread Safety Testing

```java
@Test
public void testThreadSafety() throws InterruptedException {
    BlockingQueue<String> queue = new ArrayBlockingQueue<>(1000);
    int numThreads = 10;
    int itemsPerThread = 1000;
    
    // Create producer threads
    List<Thread> producers = new ArrayList<>();
    for (int i = 0; i < numThreads; i++) {
        final int threadId = i;
        Thread producer = new Thread(() -> {
            for (int j = 0; j < itemsPerThread; j++) {
                try {
                    queue.put("Thread-" + threadId + "-Item-" + j);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
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
    assertEquals(numThreads * itemsPerThread, queue.size());
}
```

## 5.8 Queue Implementation Performance

Understanding performance characteristics helps in choosing the right implementation and optimizing code.

### Performance Comparison

| Operation | PriorityQueue | ArrayDeque | LinkedList | BlockingQueue |
|-----------|---------------|------------|------------|---------------|
| offer() | O(log n) | O(1) avg | O(1) | O(1) avg |
| poll() | O(log n) | O(1) | O(1) | O(1) |
| peek() | O(1) | O(1) | O(1) | O(1) |
| size() | O(1) | O(1) | O(1) | O(1) |

### Memory Usage

```java
// PriorityQueue memory usage
Queue<String> priorityQueue = new PriorityQueue<>();
// Memory: array + heap structure

// ArrayDeque memory usage
Deque<String> arrayDeque = new ArrayDeque<>();
// Memory: array + head/tail pointers

// LinkedList memory usage
Queue<String> linkedList = new LinkedList<>();
// Memory: node objects + references

// BlockingQueue memory usage
BlockingQueue<String> blockingQueue = new ArrayBlockingQueue<>(10);
// Memory: array + synchronization overhead
```

### Performance Optimization Tips

#### 1. Use Appropriate Implementation
```java
// Good: Use ArrayDeque for simple queue operations
Deque<String> deque = new ArrayDeque<>();

// Bad: Use PriorityQueue when order doesn't matter
Queue<String> queue = new PriorityQueue<>(); // Unnecessary overhead
```

#### 2. Set Appropriate Capacity
```java
// Good: Set capacity if known
BlockingQueue<String> queue = new ArrayBlockingQueue<>(expectedSize);

// Bad: Use default capacity
BlockingQueue<String> queue = new ArrayBlockingQueue<>(1); // Too small
```

#### 3. Avoid Unnecessary Operations
```java
// Good: Check before polling
if (!queue.isEmpty()) {
    String item = queue.poll();
}

// Bad: Always poll and check for null
String item = queue.poll();
if (item != null) {
    // Process item
}
```

## 5.9 Queue Implementation Troubleshooting

Common issues and solutions when working with Queue implementations.

### 1. Blocking Operations in Main Thread

```java
// Problem: Blocking operations in main thread
BlockingQueue<String> queue = new ArrayBlockingQueue<>(1);
queue.put("item1");
queue.put("item2"); // Blocks main thread

// Solution: Use non-blocking operations or separate thread
if (queue.offer("item2")) {
    // Item added successfully
} else {
    // Handle queue full
}
```

### 2. InterruptedException Handling

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

### 3. Performance Issues

```java
// Problem: Using wrong implementation
Queue<String> queue = new PriorityQueue<>();
for (int i = 0; i < 1000000; i++) {
    queue.offer("Item " + i); // O(log n) per operation
}

// Solution: Use appropriate implementation
Queue<String> queue = new LinkedList<>();
for (int i = 0; i < 1000000; i++) {
    queue.offer("Item " + i); // O(1) per operation
}
```

### 4. Memory Issues

```java
// Problem: Not clearing references
Queue<String> largeQueue = new LinkedList<>();
// ... populate with large data
largeQueue = null; // Still holds references

// Solution: Clear references
largeQueue.clear();
largeQueue = null;
```

## 5.10 Queue Implementation Security

Security considerations when working with Queue implementations.

### 1. Input Validation

```java
public class SecureQueueManager {
    private Queue<String> queue = new LinkedList<>();
    private int maxSize = 1000;
    
    public boolean enqueue(String input) {
        // Validate input
        if (input == null || input.trim().isEmpty()) {
            throw new IllegalArgumentException("Input cannot be null or empty");
        }
        
        if (input.length() > 1000) {
            throw new IllegalArgumentException("Input too long");
        }
        
        if (queue.size() >= maxSize) {
            throw new IllegalStateException("Queue is full");
        }
        
        // Sanitize input
        String sanitized = input.trim().replaceAll("[<>\"'&]", "");
        
        return queue.offer(sanitized);
    }
}
```

### 2. Access Control

```java
public class SecureQueueWrapper {
    private Queue<String> queue = new LinkedList<>();
    private Set<String> allowedUsers = new HashSet<>();
    
    public boolean enqueue(String user, String data) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return queue.offer(data);
    }
    
    public String dequeue(String user) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return queue.poll();
    }
}
```

### 3. Data Encryption

```java
public class EncryptedQueueManager {
    private Queue<String> encryptedQueue = new LinkedList<>();
    private String encryptionKey = "secret-key";
    
    public void enqueueEncrypted(String data) {
        String encrypted = encrypt(data, encryptionKey);
        encryptedQueue.offer(encrypted);
    }
    
    public String dequeueDecrypted() {
        String encrypted = encryptedQueue.poll();
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

Understanding Queue implementations is crucial for effective Java programming. Each implementation has its strengths and weaknesses, and choosing the right one depends on your specific use case, performance requirements, and whether you need thread safety or blocking operations.