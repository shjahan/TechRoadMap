# Section 6 – Map Implementations

## 6.1 Map Implementation Concepts

Map implementations are concrete classes that provide specific ways to store and manage key-value pairs. Understanding the different Map implementations and their characteristics is essential for choosing the right one for your use case.

### What are Map Implementations?

Map implementations are classes that implement the Map interface, providing different underlying data structures and performance characteristics. Each implementation is optimized for specific operations and use cases while maintaining the fundamental property of key-value mapping.

### Key Characteristics of Map Implementations

#### 1. Key-Value Pairs
- Each entry consists of a key and a value
- Keys must be unique within the map
- Values can be duplicated

#### 2. No Order Guarantee (in most implementations)
- Key-value pairs may not be in insertion order
- Order depends on the specific implementation
- Some implementations maintain order

#### 3. Null Handling
- Depends on implementation
- Some allow null keys and values
- Others don't allow null keys or values

#### 4. Performance Characteristics
- Lookup, insertion, and deletion performance varies
- Memory usage differs between implementations
- Thread safety varies by implementation

### Common Map Implementations

| Implementation | Data Structure | Order | Null Keys | Null Values | Performance |
|----------------|----------------|-------|-----------|-------------|-------------|
| HashMap | Hash Table | No | Yes | Yes | O(1) avg |
| LinkedHashMap | Hash Table + Linked List | Yes | Yes | Yes | O(1) avg |
| TreeMap | Red-Black Tree | Yes (sorted) | No | Yes | O(log n) |
| Hashtable | Synchronized Hash Table | No | No | No | O(1) avg |

### Real-World Analogy: Different Types of Dictionaries

Think of Map implementations as different types of dictionaries:

- **HashMap**: Like a regular dictionary where you can quickly find words by their "fingerprint" (hash), but words are in random order
- **LinkedHashMap**: Like a dictionary with a chain connecting words in the order they were added, allowing quick access and maintaining order
- **TreeMap**: Like a dictionary with words organized alphabetically, allowing quick access and maintaining sorted order
- **Hashtable**: Like a locked dictionary that only one person can access at a time, but it's safe for multiple people

## 6.2 HashMap

HashMap is the most commonly used Map implementation, providing fast lookup, insertion, and deletion operations using a hash table.

### Core Characteristics

#### 1. Hash Table Implementation
- Uses hash table with chaining for collision resolution
- Key-value pairs are stored in buckets based on hash code
- Load factor determines when to resize the table

#### 2. Performance Characteristics
- **Get**: O(1) average, O(n) worst case
- **Put**: O(1) average, O(n) worst case
- **Remove**: O(1) average, O(n) worst case
- **Contains Key**: O(1) average, O(n) worst case

#### 3. Memory Characteristics
- Memory usage depends on load factor
- Good cache locality for small maps
- Overhead for hash table structure

### Understanding HashMap Operations

#### 1. Basic Operations
```java
// Create HashMap
Map<String, Integer> ages = new HashMap<>();
Map<String, Integer> agesWithCapacity = new HashMap<>(16); // Initial capacity
Map<String, Integer> agesWithLoadFactor = new HashMap<>(16, 0.75f); // Capacity, load factor

// Add key-value pairs
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

System.out.println("Ages: " + ages); // {Alice=25, Bob=30, Charlie=35}
System.out.println("Size: " + ages.size()); // 3
```

#### 2. Key-Value Operations
```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);

// Get value by key
Integer aliceAge = ages.get("Alice");
System.out.println("Alice's age: " + aliceAge); // 25

// Check if key exists
boolean hasAlice = ages.containsKey("Alice"); // true
boolean hasDavid = ages.containsKey("David"); // false

// Check if value exists
boolean hasAge25 = ages.containsValue(25); // true
boolean hasAge40 = ages.containsValue(40); // false

// Update existing key
ages.put("Alice", 26); // Updates Alice's age to 26
System.out.println("Alice's new age: " + ages.get("Alice")); // 26
```

#### 3. Remove Operations
```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

// Remove by key
Integer removedAge = ages.remove("Bob");
System.out.println("Removed age: " + removedAge); // 30
System.out.println("After remove: " + ages); // {Alice=25, Charlie=35}

// Remove by key-value pair
boolean removed = ages.remove("Alice", 25);
System.out.println("Removed Alice: " + removed); // true
System.out.println("After remove: " + ages); // {Charlie=35}
```

#### 4. Null Handling
```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put(null, 30); // Null key allowed
ages.put("Bob", null); // Null value allowed

System.out.println("Ages: " + ages); // {null=30, Alice=25, Bob=null}
System.out.println("Null key value: " + ages.get(null)); // 30
System.out.println("Bob's age: " + ages.get("Bob")); // null
```

### HashMap Internal Working

#### 1. Hash Function
```java
// Simplified hash function concept
public int hash(Object key) {
    return key.hashCode() % tableSize;
}
```

#### 2. Collision Resolution
```java
// Chaining for collision resolution
// Each bucket contains a linked list of entries with same hash
class HashBucket {
    List<Map.Entry<String, Integer>> entries = new ArrayList<>();
    
    void add(String key, Integer value) {
        entries.add(new AbstractMap.SimpleEntry<>(key, value));
    }
    
    Integer get(String key) {
        for (Map.Entry<String, Integer> entry : entries) {
            if (entry.getKey().equals(key)) {
                return entry.getValue();
            }
        }
        return null;
    }
}
```

#### 3. Load Factor and Resizing
```java
Map<String, Integer> ages = new HashMap<>(4, 0.75f); // Initial capacity 4, load factor 0.75
ages.put("Alice", 25); // Load factor: 1/4 = 0.25
ages.put("Bob", 30);   // Load factor: 2/4 = 0.5
ages.put("Charlie", 35); // Load factor: 3/4 = 0.75
ages.put("David", 40); // Load factor: 4/4 = 1.0, triggers resize to 8
```

### Real-World Example: User Management System
```java
public class UserManager {
    private Map<String, User> users = new HashMap<>();
    private Map<String, String> emailToUsername = new HashMap<>();
    
    public void addUser(String username, String email, int age) {
        if (users.containsKey(username)) {
            throw new IllegalArgumentException("Username already exists: " + username);
        }
        
        if (emailToUsername.containsKey(email)) {
            throw new IllegalArgumentException("Email already registered: " + email);
        }
        
        User user = new User(username, email, age);
        users.put(username, user);
        emailToUsername.put(email, username);
        
        System.out.println("User added: " + username);
    }
    
    public User getUser(String username) {
        return users.get(username);
    }
    
    public User getUserByEmail(String email) {
        String username = emailToUsername.get(email);
        return username != null ? users.get(username) : null;
    }
    
    public boolean updateUser(String username, String newEmail, int newAge) {
        User user = users.get(username);
        if (user == null) {
            return false;
        }
        
        // Update email mapping
        emailToUsername.remove(user.getEmail());
        emailToUsername.put(newEmail, username);
        
        // Update user
        user.setEmail(newEmail);
        user.setAge(newAge);
        
        return true;
    }
    
    public boolean removeUser(String username) {
        User user = users.remove(username);
        if (user != null) {
            emailToUsername.remove(user.getEmail());
            return true;
        }
        return false;
    }
    
    public Set<String> getAllUsernames() {
        return new HashSet<>(users.keySet());
    }
    
    public Collection<User> getAllUsers() {
        return new ArrayList<>(users.values());
    }
    
    public static class User {
        private String username;
        private String email;
        private int age;
        
        public User(String username, String email, int age) {
            this.username = username;
            this.email = email;
            this.age = age;
        }
        
        // Getters and setters
        public String getUsername() { return username; }
        public String getEmail() { return email; }
        public int getAge() { return age; }
        public void setEmail(String email) { this.email = email; }
        public void setAge(int age) { this.age = age; }
        
        @Override
        public String toString() {
            return "User{username='" + username + "', email='" + email + "', age=" + age + "}";
        }
    }
}
```

## 6.3 LinkedHashMap

LinkedHashMap extends HashMap and maintains insertion order while providing the performance benefits of hash table operations.

### Core Characteristics

#### 1. Hash Table + Linked List Implementation
- Uses hash table for fast lookup
- Maintains doubly linked list for insertion order
- Combines benefits of HashMap and LinkedList

#### 2. Performance Characteristics
- **Get**: O(1) average, O(n) worst case
- **Put**: O(1) average, O(n) worst case
- **Remove**: O(1) average, O(n) worst case
- **Iteration**: O(n) - maintains insertion order

#### 3. Memory Characteristics
- Higher memory overhead than HashMap
- Additional memory for linked list structure
- Good cache locality for sequential access

### Understanding LinkedHashMap Operations

#### 1. Basic Operations
```java
// Create LinkedHashMap
Map<String, Integer> ages = new LinkedHashMap<>();
Map<String, Integer> agesWithCapacity = new LinkedHashMap<>(16);
Map<String, Integer> agesWithLoadFactor = new LinkedHashMap<>(16, 0.75f);

// Add key-value pairs
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);
ages.put("David", 40);

System.out.println("Ages: " + ages); // {Alice=25, Bob=30, Charlie=35, David=40} (insertion order)
System.out.println("Size: " + ages.size()); // 4
```

#### 2. Order Preservation
```java
Map<String, Integer> ages = new LinkedHashMap<>();
ages.put("Charlie", 35);
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Alice", 26); // Updates existing key, maintains position

System.out.println("Ages: " + ages); // {Charlie=35, Alice=26, Bob=30} (insertion order preserved)
```

#### 3. Access Order Mode
```java
// Create LinkedHashMap with access order
Map<String, Integer> ages = new LinkedHashMap<>(16, 0.75f, true);

ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

// Access elements to change order
ages.get("Alice"); // Moves Alice to end
ages.get("Bob");   // Moves Bob to end

System.out.println("Ages: " + ages); // {Charlie=35, Alice=25, Bob=30} (access order)
```

#### 4. Iteration Order
```java
Map<String, Integer> ages = new LinkedHashMap<>();
ages.put("Charlie", 35);
ages.put("Alice", 25);
ages.put("Bob", 30);

// Iteration follows insertion order
for (Map.Entry<String, Integer> entry : ages.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
// Output:
// Charlie: 35
// Alice: 25
// Bob: 30
```

### Real-World Example: LRU Cache
```java
public class LRUCache<K, V> {
    private final int maxSize;
    private Map<K, V> cache;
    
    public LRUCache(int maxSize) {
        this.maxSize = maxSize;
        this.cache = new LinkedHashMap<K, V>(16, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
                return size() > maxSize;
            }
        };
    }
    
    public V get(K key) {
        return cache.get(key);
    }
    
    public void put(K key, V value) {
        cache.put(key, value);
    }
    
    public V remove(K key) {
        return cache.remove(key);
    }
    
    public boolean containsKey(K key) {
        return cache.containsKey(key);
    }
    
    public int size() {
        return cache.size();
    }
    
    public void clear() {
        cache.clear();
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

## 6.4 TreeMap

TreeMap implements a Map using a Red-Black tree, providing sorted order and efficient range operations.

### Core Characteristics

#### 1. Red-Black Tree Implementation
- Self-balancing binary search tree
- Maintains sorted order automatically
- Guarantees O(log n) performance for all operations

#### 2. Performance Characteristics
- **Get**: O(log n)
- **Put**: O(log n)
- **Remove**: O(log n)
- **Contains Key**: O(log n)

#### 3. Memory Characteristics
- Higher memory overhead than HashMap
- Additional memory for tree structure
- Good cache locality for sequential access

### Understanding TreeMap Operations

#### 1. Basic Operations
```java
// Create TreeMap
Map<String, Integer> ages = new TreeMap<>();
Map<String, Integer> agesWithComparator = new TreeMap<>(String.CASE_INSENSITIVE_ORDER);

// Add key-value pairs
ages.put("Charlie", 35);
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("David", 40);

System.out.println("Ages: " + ages); // {Alice=25, Bob=30, Charlie=35, David=40} (sorted order)
System.out.println("Size: " + ages.size()); // 4
```

#### 2. Sorted Order
```java
Map<String, Integer> ages = new TreeMap<>();
ages.put("Zoe", 35);
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Alice", 26); // Updates existing key

System.out.println("Ages: " + ages); // {Alice=26, Bob=30, Zoe=35} (sorted order)
```

#### 3. Range Operations
```java
Map<String, Integer> ages = new TreeMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);
ages.put("David", 40);
ages.put("Eve", 45);

// Get submap
Map<String, Integer> submap = ages.subMap("Bob", "Eve");
System.out.println("Submap: " + submap); // {Bob=30, Charlie=35, David=40}

// Get head map (keys less than specified)
Map<String, Integer> headMap = ages.headMap("David");
System.out.println("Head map: " + headMap); // {Alice=25, Bob=30, Charlie=35}

// Get tail map (keys greater than or equal to specified)
Map<String, Integer> tailMap = ages.tailMap("Charlie");
System.out.println("Tail map: " + tailMap); // {Charlie=35, David=40, Eve=45}
```

#### 4. First and Last Elements
```java
Map<String, Integer> ages = new TreeMap<>();
ages.put("Charlie", 35);
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("David", 40);

// Get first entry
Map.Entry<String, Integer> first = ages.firstEntry();
System.out.println("First: " + first); // Alice=25

// Get last entry
Map.Entry<String, Integer> last = ages.lastEntry();
System.out.println("Last: " + last); // David=40

// Remove first entry
Map.Entry<String, Integer> removedFirst = ages.pollFirstEntry();
System.out.println("Removed first: " + removedFirst); // Alice=25
System.out.println("After pollFirst: " + ages); // {Bob=30, Charlie=35, David=40}

// Remove last entry
Map.Entry<String, Integer> removedLast = ages.pollLastEntry();
System.out.println("Removed last: " + removedLast); // David=40
System.out.println("After pollLast: " + ages); // {Bob=30, Charlie=35}
```

### Real-World Example: Leaderboard System
```java
public class Leaderboard {
    private TreeMap<Integer, List<String>> scores = new TreeMap<>(Collections.reverseOrder());
    
    public void addScore(String playerName, int score) {
        scores.computeIfAbsent(score, k -> new ArrayList<>()).add(playerName);
    }
    
    public List<String> getTopPlayers(int count) {
        List<String> topPlayers = new ArrayList<>();
        for (Map.Entry<Integer, List<String>> entry : scores.entrySet()) {
            topPlayers.addAll(entry.getValue());
            if (topPlayers.size() >= count) {
                break;
            }
        }
        return topPlayers.stream().limit(count).collect(Collectors.toList());
    }
    
    public List<String> getPlayersInRange(int minScore, int maxScore) {
        List<String> players = new ArrayList<>();
        for (Map.Entry<Integer, List<String>> entry : scores.entrySet()) {
            int score = entry.getKey();
            if (score >= minScore && score <= maxScore) {
                players.addAll(entry.getValue());
            }
        }
        return players;
    }
    
    public int getHighestScore() {
        return scores.firstKey();
    }
    
    public int getLowestScore() {
        return scores.lastKey();
    }
    
    public int getPlayerRank(String playerName) {
        int rank = 1;
        for (Map.Entry<Integer, List<String>> entry : scores.entrySet()) {
            if (entry.getValue().contains(playerName)) {
                return rank;
            }
            rank += entry.getValue().size();
        }
        return -1; // Player not found
    }
    
    public Map<Integer, List<String>> getAllScores() {
        return new TreeMap<>(scores);
    }
}
```

## 6.5 Hashtable

Hashtable is a legacy synchronized implementation of Map that provides thread-safe operations but with performance overhead.

### Core Characteristics

#### 1. Synchronized Implementation
- All methods are synchronized
- Thread-safe for multiple readers and writers
- Performance overhead due to synchronization

#### 2. Performance Characteristics
- **Get**: O(1) average, O(n) worst case
- **Put**: O(1) average, O(n) worst case
- **Remove**: O(1) average, O(n) worst case
- **Synchronization Overhead**: Additional cost for thread safety

#### 3. Legacy Features
- No null keys or values allowed
- Legacy methods (putIfAbsent, etc.)
- Enumeration support

### Understanding Hashtable Operations

#### 1. Basic Operations
```java
// Create Hashtable
Hashtable<String, Integer> ages = new Hashtable<>();
Hashtable<String, Integer> agesWithCapacity = new Hashtable<>(16);
Hashtable<String, Integer> agesWithLoadFactor = new Hashtable<>(16, 0.75f);

// Add key-value pairs
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

System.out.println("Ages: " + ages); // {Alice=25, Bob=30, Charlie=35}
System.out.println("Size: " + ages.size()); // 3
```

#### 2. Null Handling
```java
Hashtable<String, Integer> ages = new Hashtable<>();
ages.put("Alice", 25);

// These will throw NullPointerException
try {
    ages.put(null, 30); // NullPointerException
} catch (NullPointerException e) {
    System.out.println("Null key not allowed");
}

try {
    ages.put("Bob", null); // NullPointerException
} catch (NullPointerException e) {
    System.out.println("Null value not allowed");
}
```

#### 3. Thread Safety
```java
Hashtable<String, Integer> ages = new Hashtable<>();

// Multiple threads can safely access Hashtable
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

### Real-World Example: Thread-Safe Configuration
```java
public class ThreadSafeConfig {
    private Hashtable<String, String> config = new Hashtable<>();
    
    public synchronized void setProperty(String key, String value) {
        if (key == null || value == null) {
            throw new IllegalArgumentException("Key and value cannot be null");
        }
        config.put(key, value);
    }
    
    public synchronized String getProperty(String key) {
        return config.get(key);
    }
    
    public synchronized String getProperty(String key, String defaultValue) {
        String value = config.get(key);
        return value != null ? value : defaultValue;
    }
    
    public synchronized boolean hasProperty(String key) {
        return config.containsKey(key);
    }
    
    public synchronized void removeProperty(String key) {
        config.remove(key);
    }
    
    public synchronized Set<String> getAllKeys() {
        return new HashSet<>(config.keySet());
    }
    
    public synchronized void loadFromProperties(Properties props) {
        for (String key : props.stringPropertyNames()) {
            config.put(key, props.getProperty(key));
        }
    }
    
    public synchronized void clear() {
        config.clear();
    }
}
```

## 6.6 WeakHashMap

WeakHashMap is a special Map implementation that uses weak references for keys, allowing garbage collection of keys when they are no longer referenced elsewhere.

### Core Characteristics

#### 1. Weak Reference Implementation
- Uses weak references for keys
- Keys can be garbage collected when no longer referenced
- Values are held by strong references

#### 2. Performance Characteristics
- **Get**: O(1) average, O(n) worst case
- **Put**: O(1) average, O(n) worst case
- **Remove**: O(1) average, O(n) worst case
- **Automatic Cleanup**: Keys are removed when garbage collected

#### 3. Memory Characteristics
- Helps prevent memory leaks
- Keys can be garbage collected
- Values remain until explicitly removed

### Understanding WeakHashMap Operations

#### 1. Basic Operations
```java
// Create WeakHashMap
WeakHashMap<String, Integer> ages = new WeakHashMap<>();
WeakHashMap<String, Integer> agesWithCapacity = new WeakHashMap<>(16);
WeakHashMap<String, Integer> agesWithLoadFactor = new WeakHashMap<>(16, 0.75f);

// Add key-value pairs
String key1 = new String("Alice");
String key2 = new String("Bob");
ages.put(key1, 25);
ages.put(key2, 30);

System.out.println("Ages: " + ages); // {Alice=25, Bob=30}
System.out.println("Size: " + ages.size()); // 2
```

#### 2. Weak Reference Behavior
```java
WeakHashMap<String, Integer> ages = new WeakHashMap<>();

// Create keys
String key1 = new String("Alice");
String key2 = new String("Bob");
ages.put(key1, 25);
ages.put(key2, 30);

System.out.println("Before GC: " + ages.size()); // 2

// Remove strong reference to key1
key1 = null;

// Force garbage collection
System.gc();

// Wait a bit for GC to complete
try {
    Thread.sleep(100);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

System.out.println("After GC: " + ages.size()); // 1 (key1 was garbage collected)
System.out.println("Ages: " + ages); // {Bob=30}
```

#### 3. Automatic Cleanup
```java
WeakHashMap<String, Integer> ages = new WeakHashMap<>();

// Add elements
for (int i = 0; i < 1000; i++) {
    String key = new String("Key" + i);
    ages.put(key, i);
    // key goes out of scope, becomes eligible for GC
}

System.out.println("Before GC: " + ages.size()); // 1000

// Force garbage collection
System.gc();

// Wait for GC to complete
try {
    Thread.sleep(100);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

System.out.println("After GC: " + ages.size()); // 0 (all keys were garbage collected)
```

### Real-World Example: Cache with Automatic Cleanup
```java
public class WeakCache<K, V> {
    private WeakHashMap<K, V> cache = new WeakHashMap<>();
    private int maxSize = 1000;
    
    public void put(K key, V value) {
        if (cache.size() >= maxSize) {
            // Force cleanup of garbage collected keys
            System.gc();
        }
        cache.put(key, value);
    }
    
    public V get(K key) {
        return cache.get(key);
    }
    
    public boolean containsKey(K key) {
        return cache.containsKey(key);
    }
    
    public V remove(K key) {
        return cache.remove(key);
    }
    
    public int size() {
        return cache.size();
    }
    
    public void clear() {
        cache.clear();
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
    
    public void forceCleanup() {
        System.gc();
    }
}
```

## 6.7 Map Implementation Best Practices

Following best practices ensures optimal performance and maintainable code when working with Map implementations.

### 1. Choose the Right Implementation

#### Use HashMap When:
- Fast lookup is required
- Order doesn't matter
- Memory efficiency is important
- General-purpose map operations

```java
// Good for fast lookup
Map<String, Integer> ages = new HashMap<>();
Integer age = ages.get("Alice"); // O(1) average
```

#### Use LinkedHashMap When:
- Fast lookup is required
- Insertion order must be maintained
- Memory usage is not critical
- LRU cache implementation

```java
// Good for maintaining order
Map<String, Integer> ages = new LinkedHashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
// Order is preserved: {Alice=25, Bob=30}
```

#### Use TreeMap When:
- Sorted order is required
- Range operations are needed
- Memory usage is not critical
- Comparable keys

```java
// Good for sorted order
Map<String, Integer> ages = new TreeMap<>();
ages.put("Charlie", 35);
ages.put("Alice", 25);
// Automatically sorted: {Alice=25, Charlie=35}
```

#### Use Hashtable When:
- Thread safety is required
- Legacy code compatibility
- Synchronization overhead is acceptable

```java
// Good for thread safety
Hashtable<String, Integer> ages = new Hashtable<>();
// Multiple threads can safely access
```

#### Use WeakHashMap When:
- Automatic cleanup is needed
- Preventing memory leaks
- Keys can be garbage collected

```java
// Good for automatic cleanup
WeakHashMap<String, Integer> ages = new WeakHashMap<>();
// Keys are automatically removed when garbage collected
```

### 2. Proper equals() and hashCode() Implementation

```java
public class Person {
    private String name;
    private int age;
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person person = (Person) obj;
        return age == person.age && Objects.equals(name, person.name);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
}

// Use in Map
Map<Person, String> personMap = new HashMap<>();
personMap.put(new Person("Alice", 25), "Engineer");
personMap.put(new Person("Bob", 30), "Manager");
personMap.put(new Person("Alice", 25), "Senior Engineer"); // Updates existing entry
```

### 3. Use Immutable Maps When Possible

```java
// Good: Immutable map
Map<String, Integer> immutableMap = Map.of("Alice", 25, "Bob", 30);

// Good: Unmodifiable view
Map<String, Integer> unmodifiableMap = Collections.unmodifiableMap(originalMap);

// Bad: Mutable map when immutability is desired
Map<String, Integer> mutableMap = new HashMap<>();
mutableMap.put("Alice", 25);
mutableMap.put("Bob", 30);
```

### 4. Handle Null Values Appropriately

```java
// Check if map allows nulls
Map<String, Integer> map = new HashMap<>();
map.put(null, 25); // HashMap allows null keys
map.put("Alice", null); // HashMap allows null values

// Check before adding
if (key != null && value != null) {
    map.put(key, value);
}
```

### 5. Use Bulk Operations

```java
// Good: Bulk operations
Map<String, Integer> map1 = new HashMap<>();
Map<String, Integer> map2 = new HashMap<>();

// Put all from map2 to map1
map1.putAll(map2);

// Remove all keys from map1 that are in map2
map1.keySet().removeAll(map2.keySet());

// Retain only keys from map1 that are in map2
map1.keySet().retainAll(map2.keySet());
```

## 6.8 Map Implementation Testing

Comprehensive testing ensures Map implementations work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testMapOperations() {
    Map<String, Integer> map = new HashMap<>();
    
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

### 2. Performance Testing

```java
@Test
public void testMapPerformance() {
    Map<String, Integer> map = new HashMap<>();
    int size = 100000;
    
    // Test put performance
    long startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        map.put("Key" + i, i);
    }
    long putTime = System.currentTimeMillis() - startTime;
    
    // Test get performance
    startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        Integer value = map.get("Key" + i);
    }
    long getTime = System.currentTimeMillis() - startTime;
    
    System.out.println("Put time: " + putTime + "ms");
    System.out.println("Get time: " + getTime + "ms");
    
    assertTrue(putTime < 1000); // Should complete within 1 second
    assertTrue(getTime < 100);  // Should complete within 100ms
}
```

### 3. Edge Case Testing

```java
@Test
public void testEdgeCases() {
    Map<String, Integer> map = new HashMap<>();
    
    // Test empty map
    assertTrue(map.isEmpty());
    assertEquals(0, map.size());
    
    // Test null handling
    map.put(null, 25);
    assertTrue(map.containsKey(null));
    assertEquals(Integer.valueOf(25), map.get(null));
    
    // Test duplicate keys
    map.put("Alice", 25);
    map.put("Alice", 30);
    assertEquals(Integer.valueOf(30), map.get("Alice"));
    assertEquals(2, map.size()); // null + Alice
}
```

## 6.9 Map Implementation Performance

Understanding performance characteristics helps in choosing the right implementation and optimizing code.

### Performance Comparison

| Operation | HashMap | LinkedHashMap | TreeMap | Hashtable | WeakHashMap |
|-----------|---------|---------------|---------|-----------|-------------|
| get() | O(1) avg | O(1) avg | O(log n) | O(1) avg | O(1) avg |
| put() | O(1) avg | O(1) avg | O(log n) | O(1) avg | O(1) avg |
| remove() | O(1) avg | O(1) avg | O(log n) | O(1) avg | O(1) avg |
| containsKey() | O(1) avg | O(1) avg | O(log n) | O(1) avg | O(1) avg |
| memory | Medium | High | High | Medium | Medium |

### Memory Usage

```java
// HashMap memory usage
Map<String, Integer> hashMap = new HashMap<>();
// Memory: hash table + buckets + entries

// LinkedHashMap memory usage
Map<String, Integer> linkedHashMap = new LinkedHashMap<>();
// Memory: hash table + buckets + entries + linked list

// TreeMap memory usage
Map<String, Integer> treeMap = new TreeMap<>();
// Memory: tree nodes + entries

// Hashtable memory usage
Hashtable<String, Integer> hashtable = new Hashtable<>();
// Memory: hash table + buckets + entries + synchronization overhead

// WeakHashMap memory usage
WeakHashMap<String, Integer> weakHashMap = new WeakHashMap<>();
// Memory: hash table + buckets + entries + weak references
```

### Performance Optimization Tips

#### 1. Use Appropriate Initial Capacity
```java
// Good: Set capacity if known
Map<String, Integer> map = new HashMap<>(expectedSize);

// Bad: Let it grow multiple times
Map<String, Integer> map = new HashMap<>(); // Will grow: 16 -> 32 -> 64 -> 128...
```

#### 2. Use Appropriate Load Factor
```java
// Good: Set load factor if known
Map<String, Integer> map = new HashMap<>(16, 0.5f); // Lower load factor for better performance

// Bad: Use default load factor when not appropriate
Map<String, Integer> map = new HashMap<>(16, 0.75f); // Default load factor
```

#### 3. Use Immutable Maps When Possible
```java
// Good: Immutable map
Map<String, Integer> map = Map.of("Alice", 25, "Bob", 30);

// Bad: Mutable map when immutability is sufficient
Map<String, Integer> map = new HashMap<>();
map.put("Alice", 25);
map.put("Bob", 30);
```

## 6.10 Map Implementation Troubleshooting

Common issues and solutions when working with Map implementations.

### 1. NullPointerException

```java
// Problem: Null keys or values in TreeMap
Map<String, Integer> map = new TreeMap<>();
map.put(null, 25); // NullPointerException

// Solution: Use HashMap or check for null
Map<String, Integer> map = new HashMap<>();
map.put(null, 25); // OK

// Or check before adding
if (key != null) {
    map.put(key, value);
}
```

### 2. Performance Issues

```java
// Problem: Using wrong implementation
Map<String, Integer> map = new TreeMap<>();
for (int i = 0; i < 1000000; i++) {
    map.put("Key" + i, i); // O(log n) per operation
}

// Solution: Use HashMap for better performance
Map<String, Integer> map = new HashMap<>();
for (int i = 0; i < 1000000; i++) {
    map.put("Key" + i, i); // O(1) average per operation
}
```

### 3. Memory Issues

```java
// Problem: Not clearing references
Map<String, Integer> largeMap = new HashMap<>();
// ... populate with large data
largeMap = null; // Still holds references

// Solution: Clear references
largeMap.clear();
largeMap = null;
```

### 4. Thread Safety Issues

```java
// Problem: Using non-thread-safe map in multi-threaded environment
Map<String, Integer> map = new HashMap<>();
// Multiple threads accessing map can cause issues

// Solution: Use thread-safe map or synchronization
Map<String, Integer> map = new ConcurrentHashMap<>();
// Or use synchronized map
Map<String, Integer> map = Collections.synchronizedMap(new HashMap<>());
```

Understanding Map implementations is crucial for effective Java programming. Each implementation has its strengths and weaknesses, and choosing the right one depends on your specific use case, performance requirements, and whether you need ordering, sorting, or thread safety capabilities.