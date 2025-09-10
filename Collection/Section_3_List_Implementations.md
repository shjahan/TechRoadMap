# Section 3 – List Implementations

## 3.1 List Implementation Concepts

List implementations are concrete classes that provide specific ways to store and manage ordered collections of elements. Understanding the different implementations and their characteristics is crucial for choosing the right one for your use case.

### What are List Implementations?

List implementations are classes that implement the List interface, providing different underlying data structures and performance characteristics. Each implementation is optimized for specific operations and use cases.

### Key Characteristics of List Implementations

#### 1. Ordered Collection
- Elements maintain insertion order
- Each element has a specific position (index)
- Can access elements by their position

#### 2. Duplicate Elements
- Lists can contain duplicate elements
- Each element is independent of others

#### 3. Null Elements
- Most implementations allow null elements
- Null elements are treated as regular elements

#### 4. Indexed Access
- Elements can be accessed by index (0-based)
- Index operations are implementation-dependent

### Common List Implementations

| Implementation | Data Structure | Random Access | Insertion/Deletion | Memory Usage |
|----------------|----------------|---------------|-------------------|---------------|
| ArrayList | Dynamic Array | O(1) | O(n) | Lower |
| LinkedList | Doubly Linked List | O(n) | O(1) | Higher |
| Vector | Synchronized Array | O(1) | O(n) | Lower |
| Stack | LIFO Stack | O(1) | O(1) | Lower |

### Real-World Analogy: Different Types of Shelves

Think of list implementations as different types of shelves in a library:

- **ArrayList**: Like a bookshelf with numbered slots - you can quickly find any book by its number, but adding a book in the middle requires shifting all books after it
- **LinkedList**: Like a chain of connected boxes - you can easily add or remove boxes anywhere in the chain, but to find a specific box, you need to follow the chain from the beginning
- **Vector**: Like a bookshelf with a lock - only one person can access it at a time, but it's safe for multiple people
- **Stack**: Like a stack of plates - you can only add or remove from the top

## 3.2 ArrayList

ArrayList is the most commonly used List implementation, providing dynamic array functionality with efficient random access.

### Core Characteristics

#### 1. Dynamic Array Implementation
- Internally uses a resizable array
- Automatically grows when capacity is exceeded
- Shrinks when elements are removed (in some cases)

#### 2. Performance Characteristics
- **Random Access**: O(1) - constant time
- **Add at End**: O(1) amortized - usually constant time
- **Add at Middle**: O(n) - linear time
- **Remove**: O(n) - linear time
- **Search**: O(n) - linear time

#### 3. Memory Characteristics
- Contiguous memory allocation
- Lower memory overhead per element
- Good cache locality

### Understanding ArrayList Operations

#### 1. Basic Operations
```java
// Create ArrayList
List<String> names = new ArrayList<>();
List<String> namesWithCapacity = new ArrayList<>(10); // Initial capacity

// Add elements
names.add("Alice");        // Add to end
names.add("Bob");          // Add to end
names.add(0, "Charlie");   // Add at specific index

System.out.println("Names: " + names); // [Charlie, Alice, Bob]
System.out.println("Size: " + names.size()); // 3
```

#### 2. Access Operations
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

// Get element by index
String first = names.get(0);        // "Alice"
String last = names.get(names.size() - 1); // "Charlie"

// Set element at index
names.set(1, "Bobby");              // Replace "Bob" with "Bobby"
System.out.println("After set: " + names); // [Alice, Bobby, Charlie]

// Check if contains element
boolean hasAlice = names.contains("Alice"); // true
boolean hasDavid = names.contains("David"); // false
```

#### 3. Search Operations
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Alice");
names.add("Charlie");

// Find first occurrence
int firstIndex = names.indexOf("Alice");    // 0
int lastIndex = names.lastIndexOf("Alice"); // 2
int notFound = names.indexOf("David");      // -1

System.out.println("First Alice at: " + firstIndex);
System.out.println("Last Alice at: " + lastIndex);
```

#### 4. Remove Operations
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");
names.add("David");

// Remove by index
String removed = names.remove(1);           // Remove "Bob"
System.out.println("Removed: " + removed); // "Bob"
System.out.println("After remove by index: " + names); // [Alice, Charlie, David]

// Remove by object
boolean removedBob = names.remove("Bob");   // false (already removed)
boolean removedCharlie = names.remove("Charlie"); // true
System.out.println("After remove by object: " + names); // [Alice, David]
```

### ArrayList Internal Working

#### 1. Capacity Management
```java
// ArrayList grows automatically
List<String> names = new ArrayList<>(2); // Initial capacity 2
names.add("Alice"); // Capacity: 2
names.add("Bob");   // Capacity: 2
names.add("Charlie"); // Capacity: 4 (doubled)

// Check capacity (not directly accessible, but affects performance)
for (int i = 0; i < 1000; i++) {
    names.add("Item " + i);
    // ArrayList will grow: 4 -> 8 -> 16 -> 32 -> 64 -> 128 -> 256 -> 512 -> 1024
}
```

#### 2. Array Copying
```java
// When capacity is exceeded, ArrayList creates new array
List<String> names = new ArrayList<>(2);
names.add("Alice");
names.add("Bob");

// Adding third element triggers array growth
names.add("Charlie");
// Internally: new array created, old elements copied, old array discarded
```

### Real-World Example: Student Grade Management
```java
public class GradeManager {
    private List<Double> grades = new ArrayList<>();
    
    public void addGrade(double grade) {
        if (grade >= 0 && grade <= 100) {
            grades.add(grade);
        } else {
            throw new IllegalArgumentException("Grade must be between 0 and 100");
        }
    }
    
    public double getGrade(int index) {
        if (index < 0 || index >= grades.size()) {
            throw new IndexOutOfBoundsException("Invalid grade index");
        }
        return grades.get(index);
    }
    
    public double calculateAverage() {
        if (grades.isEmpty()) {
            return 0.0;
        }
        
        double sum = 0.0;
        for (double grade : grades) {
            sum += grade;
        }
        return sum / grades.size();
    }
    
    public List<Double> getGradesAbove(double threshold) {
        List<Double> aboveThreshold = new ArrayList<>();
        for (double grade : grades) {
            if (grade > threshold) {
                aboveThreshold.add(grade);
            }
        }
        return aboveThreshold;
    }
    
    public void removeLowestGrade() {
        if (grades.isEmpty()) {
            return;
        }
        
        double minGrade = Double.MAX_VALUE;
        int minIndex = -1;
        
        for (int i = 0; i < grades.size(); i++) {
            if (grades.get(i) < minGrade) {
                minGrade = grades.get(i);
                minIndex = i;
            }
        }
        
        if (minIndex != -1) {
            grades.remove(minIndex);
        }
    }
}
```

## 3.3 LinkedList

LinkedList implements the List interface using a doubly linked list data structure, providing efficient insertion and deletion operations.

### Core Characteristics

#### 1. Doubly Linked List Implementation
- Each element (node) contains data and references to next and previous nodes
- No contiguous memory allocation
- Dynamic size without capacity concerns

#### 2. Performance Characteristics
- **Random Access**: O(n) - linear time
- **Add at End**: O(1) - constant time
- **Add at Middle**: O(n) - linear time (finding position)
- **Remove**: O(1) - constant time (if you have the node reference)
- **Search**: O(n) - linear time

#### 3. Memory Characteristics
- Higher memory overhead per element (node structure)
- Non-contiguous memory allocation
- Poor cache locality

### Understanding LinkedList Operations

#### 1. Basic Operations
```java
// Create LinkedList
List<String> names = new LinkedList<>();
List<String> namesFromCollection = new LinkedList<>(Arrays.asList("Alice", "Bob"));

// Add elements
names.add("Alice");        // Add to end
names.add("Bob");          // Add to end
names.add(0, "Charlie");   // Add at beginning

System.out.println("Names: " + names); // [Charlie, Alice, Bob]
System.out.println("Size: " + names.size()); // 3
```

#### 2. Efficient End Operations
```java
LinkedList<String> names = new LinkedList<>();
names.add("Alice");        // Add to end
names.add("Bob");          // Add to end
names.addLast("Charlie");  // Add to end (same as add)

// Remove from end
String last = names.removeLast(); // Remove and return last element
System.out.println("Removed last: " + last); // "Charlie"
System.out.println("After removeLast: " + names); // [Alice, Bob]

// Add to beginning
names.addFirst("David");   // Add to beginning
System.out.println("After addFirst: " + names); // [David, Alice, Bob]

// Remove from beginning
String first = names.removeFirst(); // Remove and return first element
System.out.println("Removed first: " + first); // "David"
System.out.println("After removeFirst: " + names); // [Alice, Bob]
```

#### 3. Iterator Operations
```java
LinkedList<String> names = new LinkedList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

// Forward iteration
ListIterator<String> forward = names.listIterator();
while (forward.hasNext()) {
    System.out.println("Next: " + forward.next());
}

// Backward iteration
ListIterator<String> backward = names.listIterator(names.size());
while (backward.hasPrevious()) {
    System.out.println("Previous: " + backward.previous());
}

// Bidirectional iteration with modification
ListIterator<String> iterator = names.listIterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.equals("Bob")) {
        iterator.set("Bobby");        // Replace current element
        iterator.add("New Item");     // Add after current element
    }
}
```

### LinkedList Internal Working

#### 1. Node Structure
```java
// Simplified node structure (conceptual)
class Node<E> {
    E data;
    Node<E> next;
    Node<E> previous;
    
    Node(E data) {
        this.data = data;
    }
}
```

#### 2. Insertion Process
```java
LinkedList<String> names = new LinkedList<>();
names.add("Alice");
names.add("Bob");

// When adding "Charlie":
// 1. Create new node with "Charlie"
// 2. Set new node's next to null (it's the last)
// 3. Set new node's previous to "Bob" node
// 4. Set "Bob" node's next to new node
// 5. Update tail reference to new node
```

### Real-World Example: Music Playlist
```java
public class MusicPlaylist {
    private LinkedList<String> songs = new LinkedList<>();
    private int currentIndex = 0;
    
    public void addSong(String song) {
        songs.add(song);
    }
    
    public void addSongAt(int position, String song) {
        songs.add(position, song);
    }
    
    public String playNext() {
        if (currentIndex < songs.size()) {
            String song = songs.get(currentIndex);
            currentIndex++;
            return song;
        }
        return null; // End of playlist
    }
    
    public String playPrevious() {
        if (currentIndex > 0) {
            currentIndex--;
            return songs.get(currentIndex);
        }
        return null; // Beginning of playlist
    }
    
    public String getCurrentSong() {
        if (currentIndex < songs.size()) {
            return songs.get(currentIndex);
        }
        return null;
    }
    
    public void removeCurrentSong() {
        if (currentIndex < songs.size()) {
            songs.remove(currentIndex);
            if (currentIndex >= songs.size()) {
                currentIndex = Math.max(0, songs.size() - 1);
            }
        }
    }
    
    public void shuffle() {
        Collections.shuffle(songs);
        currentIndex = 0;
    }
    
    public List<String> getPlaylist() {
        return new ArrayList<>(songs); // Return copy
    }
}
```

## 3.4 Vector

Vector is a legacy synchronized implementation of List that provides thread-safe operations but with performance overhead.

### Core Characteristics

#### 1. Synchronized Implementation
- All methods are synchronized
- Thread-safe for multiple readers and writers
- Performance overhead due to synchronization

#### 2. Performance Characteristics
- **Random Access**: O(1) - constant time
- **Add at End**: O(1) amortized - usually constant time
- **Add at Middle**: O(n) - linear time
- **Remove**: O(n) - linear time
- **Search**: O(n) - linear time
- **Synchronization Overhead**: Additional cost for thread safety

#### 3. Legacy Features
- Capacity increment parameter
- Legacy methods (addElement, removeElement, etc.)
- Enumeration support

### Understanding Vector Operations

#### 1. Basic Operations
```java
// Create Vector
Vector<String> names = new Vector<>();
Vector<String> namesWithCapacity = new Vector<>(10); // Initial capacity
Vector<String> namesWithIncrement = new Vector<>(10, 5); // Initial capacity, increment

// Add elements
names.add("Alice");        // Add to end
names.add("Bob");          // Add to end
names.add(0, "Charlie");   // Add at specific index

System.out.println("Names: " + names); // [Charlie, Alice, Bob]
System.out.println("Size: " + names.size()); // 3
System.out.println("Capacity: " + names.capacity()); // Current capacity
```

#### 2. Legacy Methods
```java
Vector<String> names = new Vector<>();
names.addElement("Alice");     // Legacy method (same as add)
names.addElement("Bob");
names.addElement("Charlie");

// Legacy iteration
Enumeration<String> enumeration = names.elements();
while (enumeration.hasMoreElements()) {
    System.out.println("Element: " + enumeration.nextElement());
}

// Legacy access
String first = names.firstElement();    // First element
String last = names.lastElement();      // Last element
```

#### 3. Thread Safety
```java
Vector<String> names = new Vector<>();

// Multiple threads can safely access Vector
Thread thread1 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        names.add("Thread1-" + i);
    }
});

Thread thread2 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        names.add("Thread2-" + i);
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

System.out.println("Final size: " + names.size()); // 2000
```

### Real-World Example: Thread-Safe Logging
```java
public class ThreadSafeLogger {
    private Vector<String> logEntries = new Vector<>();
    private int maxEntries = 1000;
    
    public synchronized void log(String message) {
        if (logEntries.size() >= maxEntries) {
            logEntries.remove(0); // Remove oldest entry
        }
        logEntries.add(System.currentTimeMillis() + ": " + message);
    }
    
    public synchronized List<String> getLogEntries() {
        return new ArrayList<>(logEntries); // Return copy
    }
    
    public synchronized void clearLogs() {
        logEntries.clear();
    }
    
    public synchronized int getLogCount() {
        return logEntries.size();
    }
    
    public synchronized String getLastEntry() {
        if (logEntries.isEmpty()) {
            return null;
        }
        return logEntries.lastElement();
    }
}
```

## 3.5 Stack

Stack extends Vector and implements a LIFO (Last-In-First-Out) data structure, though it's considered legacy and not recommended for new code.

### Core Characteristics

#### 1. LIFO Implementation
- Last element added is first to be removed
- Extends Vector (inherits synchronization)
- Legacy implementation

#### 2. Performance Characteristics
- **Push**: O(1) - constant time
- **Pop**: O(1) - constant time
- **Peek**: O(1) - constant time
- **Search**: O(n) - linear time
- **Synchronization Overhead**: Inherited from Vector

#### 3. Legacy Status
- Not recommended for new code
- Use Deque implementations instead
- Still available for backward compatibility

### Understanding Stack Operations

#### 1. Basic Stack Operations
```java
// Create Stack
Stack<String> stack = new Stack<>();

// Push elements (add to top)
stack.push("Alice");
stack.push("Bob");
stack.push("Charlie");

System.out.println("Stack: " + stack); // [Alice, Bob, Charlie]
System.out.println("Size: " + stack.size()); // 3

// Peek at top element (without removing)
String top = stack.peek();
System.out.println("Top element: " + top); // "Charlie"

// Pop element (remove from top)
String popped = stack.pop();
System.out.println("Popped: " + popped); // "Charlie"
System.out.println("Stack after pop: " + stack); // [Alice, Bob]
```

#### 2. Stack Search
```java
Stack<String> stack = new Stack<>();
stack.push("Alice");
stack.push("Bob");
stack.push("Charlie");
stack.push("David");

// Search for element (returns distance from top, 1-based)
int alicePos = stack.search("Alice");    // 4 (4th from top)
int bobPos = stack.search("Bob");        // 3 (3rd from top)
int charliePos = stack.search("Charlie"); // 2 (2nd from top)
int davidPos = stack.search("David");    // 1 (1st from top)
int notFound = stack.search("Eve");      // -1 (not found)

System.out.println("Alice position: " + alicePos);
System.out.println("Bob position: " + bobPos);
```

#### 3. Stack Iteration
```java
Stack<String> stack = new Stack<>();
stack.push("Alice");
stack.push("Bob");
stack.push("Charlie");

// Iterate through stack (from bottom to top)
for (String item : stack) {
    System.out.println("Item: " + item);
}

// Pop all elements
while (!stack.isEmpty()) {
    String item = stack.pop();
    System.out.println("Popped: " + item);
}
```

### Real-World Example: Undo/Redo System
```java
public class UndoRedoManager {
    private Stack<String> undoStack = new Stack<>();
    private Stack<String> redoStack = new Stack<>();
    
    public void performAction(String action) {
        undoStack.push(action);
        redoStack.clear(); // Clear redo stack when new action is performed
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
}
```

## 3.6 List Implementation Best Practices

Following best practices ensures optimal performance and maintainable code when working with List implementations.

### 1. Choose the Right Implementation

#### Use ArrayList When:
- Frequent random access by index
- More reads than writes
- Memory efficiency is important
- Simple sequential processing

```java
// Good for random access
List<String> names = new ArrayList<>();
for (int i = 0; i < names.size(); i++) {
    System.out.println(names.get(i)); // O(1) access
}
```

#### Use LinkedList When:
- Frequent insertions/deletions at beginning or middle
- Implementing queues or stacks
- Memory usage is not critical
- Sequential processing with modifications

```java
// Good for frequent insertions
List<String> names = new LinkedList<>();
names.add(0, "New Item"); // O(1) insertion at beginning
```

#### Use Vector When:
- Thread safety is required
- Legacy code compatibility
- Synchronization overhead is acceptable

```java
// Good for thread safety
Vector<String> names = new Vector<>();
// Multiple threads can safely access
```

### 2. Initialize with Appropriate Capacity

```java
// Good: Set initial capacity if known
List<String> names = new ArrayList<>(1000);

// Bad: Let ArrayList grow multiple times
List<String> names = new ArrayList<>(); // Will grow: 10 -> 20 -> 40 -> 80 -> 160...
```

### 3. Use Enhanced for Loop When Possible

```java
// Good: Enhanced for loop (read-only)
List<String> names = new ArrayList<>();
for (String name : names) {
    System.out.println(name);
}

// Bad: Index-based loop when not needed
for (int i = 0; i < names.size(); i++) {
    System.out.println(names.get(i));
}
```

### 4. Avoid Concurrent Modification

```java
// Bad: Concurrent modification
List<String> names = new ArrayList<>();
for (String name : names) {
    if (name.equals("Remove")) {
        names.remove(name); // ConcurrentModificationException
    }
}

// Good: Use iterator
Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.equals("Remove")) {
        iterator.remove(); // Safe removal
    }
}
```

### 5. Use Generic Types

```java
// Good: Type-safe
List<String> names = new ArrayList<>();
names.add("Alice");
String name = names.get(0); // No casting needed

// Bad: Raw types
List names = new ArrayList();
names.add("Alice");
String name = (String) names.get(0); // Requires casting
```

## 3.7 List Implementation Testing

Comprehensive testing ensures List implementations work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testArrayListOperations() {
    List<String> list = new ArrayList<>();
    
    // Test add
    assertTrue(list.add("Alice"));
    assertEquals(1, list.size());
    assertTrue(list.contains("Alice"));
    
    // Test get
    assertEquals("Alice", list.get(0));
    
    // Test set
    assertEquals("Alice", list.set(0, "Bob"));
    assertEquals("Bob", list.get(0));
    
    // Test remove
    assertTrue(list.remove("Bob"));
    assertEquals(0, list.size());
    assertFalse(list.contains("Bob"));
}
```

### 2. Performance Testing

```java
@Test
public void testArrayListPerformance() {
    List<String> list = new ArrayList<>();
    int size = 100000;
    
    // Test add performance
    long startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        list.add("Item " + i);
    }
    long addTime = System.currentTimeMillis() - startTime;
    
    // Test get performance
    startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        String item = list.get(i);
    }
    long getTime = System.currentTimeMillis() - startTime;
    
    System.out.println("Add time: " + addTime + "ms");
    System.out.println("Get time: " + getTime + "ms");
    
    assertTrue(addTime < 1000); // Should complete within 1 second
    assertTrue(getTime < 100);  // Should complete within 100ms
}
```

### 3. Edge Case Testing

```java
@Test
public void testEdgeCases() {
    List<String> list = new ArrayList<>();
    
    // Test empty list
    assertTrue(list.isEmpty());
    assertEquals(0, list.size());
    
    // Test null elements
    list.add(null);
    assertTrue(list.contains(null));
    assertEquals(1, list.size());
    
    // Test index bounds
    assertThrows(IndexOutOfBoundsException.class, () -> list.get(1));
    assertThrows(IndexOutOfBoundsException.class, () -> list.set(1, "test"));
}
```

## 3.8 List Implementation Performance

Understanding performance characteristics helps in choosing the right implementation and optimizing code.

### Performance Comparison

| Operation | ArrayList | LinkedList | Vector |
|-----------|-----------|------------|--------|
| get(index) | O(1) | O(n) | O(1) |
| add(element) | O(1) amortized | O(1) | O(1) amortized |
| add(index, element) | O(n) | O(n) | O(n) |
| remove(index) | O(n) | O(n) | O(n) |
| remove(element) | O(n) | O(n) | O(n) |
| contains(element) | O(n) | O(n) | O(n) |
| indexOf(element) | O(n) | O(n) | O(n) |

### Memory Usage

```java
// ArrayList memory usage
List<String> arrayList = new ArrayList<>();
// Memory: array + object overhead
// Good cache locality

// LinkedList memory usage
List<String> linkedList = new LinkedList<>();
// Memory: node objects + references
// Poor cache locality
```

### Performance Optimization Tips

#### 1. Use Appropriate Initial Capacity
```java
// Good: Set capacity if known
List<String> list = new ArrayList<>(expectedSize);

// Bad: Let it grow multiple times
List<String> list = new ArrayList<>(); // Will grow: 10 -> 20 -> 40 -> 80...
```

#### 2. Avoid Unnecessary Operations
```java
// Bad: Multiple contains checks
if (list.contains(item)) {
    list.remove(item);
}

// Good: Single operation
if (list.remove(item)) {
    // Item was removed
}
```

#### 3. Use Bulk Operations
```java
// Good: Bulk operations
list.addAll(otherList);
list.removeAll(toRemove);

// Bad: Individual operations
for (String item : otherList) {
    list.add(item);
}
```

## 3.9 List Implementation Troubleshooting

Common issues and solutions when working with List implementations.

### 1. ConcurrentModificationException

```java
// Problem: Modifying list during iteration
List<String> list = new ArrayList<>();
list.add("Alice");
list.add("Bob");

for (String item : list) {
    if (item.equals("Alice")) {
        list.remove(item); // ConcurrentModificationException
    }
}

// Solution: Use iterator
Iterator<String> iterator = list.iterator();
while (iterator.hasNext()) {
    String item = iterator.next();
    if (item.equals("Alice")) {
        iterator.remove(); // Safe removal
    }
}
```

### 2. IndexOutOfBoundsException

```java
// Problem: Accessing invalid index
List<String> list = new ArrayList<>();
String item = list.get(0); // IndexOutOfBoundsException

// Solution: Check bounds
if (!list.isEmpty() && index < list.size()) {
    String item = list.get(index);
}
```

### 3. Performance Issues

```java
// Problem: Using wrong implementation
List<String> list = new LinkedList<>();
for (int i = 0; i < 1000000; i++) {
    String item = list.get(i); // O(n) operation
}

// Solution: Use ArrayList for random access
List<String> list = new ArrayList<>();
for (int i = 0; i < 1000000; i++) {
    String item = list.get(i); // O(1) operation
}
```

### 4. Memory Issues

```java
// Problem: Not clearing references
List<String> largeList = new ArrayList<>();
// ... populate with large data
largeList = null; // Still holds references

// Solution: Clear references
largeList.clear();
largeList = null;
```

## 3.10 List Implementation Security

Security considerations when working with List implementations.

### 1. Input Validation

```java
public class SecureListManager {
    private List<String> data = new ArrayList<>();
    private int maxSize = 1000;
    
    public boolean addData(String input) {
        // Validate input
        if (input == null || input.trim().isEmpty()) {
            throw new IllegalArgumentException("Input cannot be null or empty");
        }
        
        if (input.length() > 1000) {
            throw new IllegalArgumentException("Input too long");
        }
        
        if (data.size() >= maxSize) {
            throw new IllegalStateException("List is full");
        }
        
        // Sanitize input
        String sanitized = input.trim().replaceAll("[<>\"'&]", "");
        
        return data.add(sanitized);
    }
}
```

### 2. Access Control

```java
public class SecureListWrapper {
    private List<String> data = new ArrayList<>();
    private Set<String> allowedUsers = new HashSet<>();
    
    public boolean addData(String user, String data) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return this.data.add(data);
    }
    
    public List<String> getData(String user) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return new ArrayList<>(data); // Return copy
    }
}
```

### 3. Data Encryption

```java
public class EncryptedListManager {
    private List<String> encryptedData = new ArrayList<>();
    private String encryptionKey = "secret-key";
    
    public void addEncryptedData(String data) {
        String encrypted = encrypt(data, encryptionKey);
        encryptedData.add(encrypted);
    }
    
    public String getDecryptedData(int index) {
        String encrypted = encryptedData.get(index);
        return decrypt(encrypted, encryptionKey);
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

Understanding List implementations is crucial for effective Java programming. Each implementation has its strengths and weaknesses, and choosing the right one depends on your specific use case, performance requirements, and thread safety needs.