# Section 4 – Set Implementations

## 4.1 Set Implementation Concepts

Set implementations are concrete classes that provide specific ways to store and manage collections of unique elements. Understanding the different Set implementations and their characteristics is essential for choosing the right one for your use case.

### What are Set Implementations?

Set implementations are classes that implement the Set interface, providing different underlying data structures and performance characteristics. Each implementation is optimized for specific operations and use cases while maintaining the fundamental property of uniqueness.

### Key Characteristics of Set Implementations

#### 1. Uniqueness Guarantee
- No duplicate elements allowed
- Each element appears at most once
- Equality is determined by equals() method

#### 2. No Order Guarantee (in most implementations)
- Elements may not be in insertion order
- Order depends on the specific implementation
- Some implementations maintain order

#### 3. Null Element Handling
- Most implementations allow at most one null element
- Some implementations don't allow null elements
- Behavior varies by implementation

#### 4. Mathematical Set Operations
- Union, intersection, difference operations
- Follows mathematical set theory principles
- Efficient set operations

### Common Set Implementations

| Implementation | Data Structure | Order | Null Allowed | Performance |
|----------------|----------------|-------|--------------|-------------|
| HashSet | Hash Table | No | Yes | O(1) average |
| LinkedHashSet | Hash Table + Linked List | Yes | Yes | O(1) average |
| TreeSet | Red-Black Tree | Yes (sorted) | No | O(log n) |
| EnumSet | Bit Vector | Yes (enum order) | No | O(1) |

### Real-World Analogy: Different Types of Collections

Think of Set implementations as different types of collections:

- **HashSet**: Like a bag where you can quickly find items by their "fingerprint" (hash), but items are in random order
- **LinkedHashSet**: Like a bag with a chain connecting items in the order they were added, allowing quick access and maintaining order
- **TreeSet**: Like a filing cabinet with items organized alphabetically, allowing quick access and maintaining sorted order
- **EnumSet**: Like a specialized container for a specific type of items (enums), extremely efficient for that type

## 4.2 HashSet

HashSet is the most commonly used Set implementation, providing fast lookup, insertion, and deletion operations using a hash table.

### Core Characteristics

#### 1. Hash Table Implementation
- Uses hash table with chaining for collision resolution
- Elements are stored in buckets based on hash code
- Load factor determines when to resize the table

#### 2. Performance Characteristics
- **Add**: O(1) average, O(n) worst case
- **Remove**: O(1) average, O(n) worst case
- **Contains**: O(1) average, O(n) worst case
- **Iteration**: O(n) - depends on number of elements

#### 3. Memory Characteristics
- Memory usage depends on load factor
- Good cache locality for small sets
- Overhead for hash table structure

### Understanding HashSet Operations

#### 1. Basic Operations
```java
// Create HashSet
Set<String> names = new HashSet<>();
Set<String> namesWithCapacity = new HashSet<>(16); // Initial capacity
Set<String> namesWithLoadFactor = new HashSet<>(16, 0.75f); // Capacity, load factor

// Add elements
names.add("Alice");
names.add("Bob");
names.add("Alice"); // Duplicate - will not be added
names.add("Charlie");

System.out.println("Names: " + names); // [Alice, Bob, Charlie] (order may vary)
System.out.println("Size: " + names.size()); // 3
```

#### 2. Duplicate Handling
```java
Set<String> names = new HashSet<>();
names.add("Alice");
names.add("Bob");
names.add("Alice"); // Duplicate
names.add("Bob");   // Duplicate

System.out.println("Size: " + names.size()); // 2 (duplicates ignored)
System.out.println("Contains Alice: " + names.contains("Alice")); // true
System.out.println("Contains David: " + names.contains("David")); // false
```

#### 3. Null Element Handling
```java
Set<String> names = new HashSet<>();
names.add("Alice");
names.add(null);
names.add("Bob");
names.add(null); // Second null - will not be added

System.out.println("Size: " + names.size()); // 3
System.out.println("Contains null: " + names.contains(null)); // true
System.out.println("Names: " + names); // [null, Alice, Bob] (order may vary)
```

#### 4. Set Operations
```java
Set<String> set1 = new HashSet<>();
set1.add("Alice");
set1.add("Bob");
set1.add("Charlie");

Set<String> set2 = new HashSet<>();
set2.add("Bob");
set2.add("Charlie");
set2.add("David");

// Union (all elements from both sets)
Set<String> union = new HashSet<>(set1);
union.addAll(set2);
System.out.println("Union: " + union); // [Alice, Bob, Charlie, David]

// Intersection (elements common to both sets)
Set<String> intersection = new HashSet<>(set1);
intersection.retainAll(set2);
System.out.println("Intersection: " + intersection); // [Bob, Charlie]

// Difference (elements in set1 but not in set2)
Set<String> difference = new HashSet<>(set1);
difference.removeAll(set2);
System.out.println("Difference: " + difference); // [Alice]
```

### HashSet Internal Working

#### 1. Hash Function
```java
// Simplified hash function concept
public int hash(String key) {
    return key.hashCode() % tableSize;
}
```

#### 2. Collision Resolution
```java
// Chaining for collision resolution
// Each bucket contains a linked list of elements with same hash
class HashBucket {
    List<String> elements = new ArrayList<>();
    
    void add(String element) {
        elements.add(element);
    }
    
    boolean contains(String element) {
        return elements.contains(element);
    }
}
```

#### 3. Load Factor and Resizing
```java
Set<String> names = new HashSet<>(4, 0.75f); // Initial capacity 4, load factor 0.75
names.add("Alice"); // Load factor: 1/4 = 0.25
names.add("Bob");   // Load factor: 2/4 = 0.5
names.add("Charlie"); // Load factor: 3/4 = 0.75
names.add("David"); // Load factor: 4/4 = 1.0, triggers resize to 8
```

### Real-World Example: User Management System
```java
public class UserManager {
    private Set<String> usernames = new HashSet<>();
    private Set<String> emailAddresses = new HashSet<>();
    
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
}
```

## 4.3 LinkedHashSet

LinkedHashSet extends HashSet and maintains insertion order while providing the performance benefits of hash table operations.

### Core Characteristics

#### 1. Hash Table + Linked List Implementation
- Uses hash table for fast lookup
- Maintains doubly linked list for insertion order
- Combines benefits of HashSet and LinkedList

#### 2. Performance Characteristics
- **Add**: O(1) average, O(n) worst case
- **Remove**: O(1) average, O(n) worst case
- **Contains**: O(1) average, O(n) worst case
- **Iteration**: O(n) - maintains insertion order

#### 3. Memory Characteristics
- Higher memory overhead than HashSet
- Additional memory for linked list structure
- Good cache locality for sequential access

### Understanding LinkedHashSet Operations

#### 1. Basic Operations
```java
// Create LinkedHashSet
Set<String> names = new LinkedHashSet<>();
Set<String> namesWithCapacity = new LinkedHashSet<>(16);
Set<String> namesWithLoadFactor = new LinkedHashSet<>(16, 0.75f);

// Add elements
names.add("Alice");
names.add("Bob");
names.add("Charlie");
names.add("David");

System.out.println("Names: " + names); // [Alice, Bob, Charlie, David] (insertion order)
System.out.println("Size: " + names.size()); // 4
```

#### 2. Order Preservation
```java
Set<String> names = new LinkedHashSet<>();
names.add("Alice");
names.add("Bob");
names.add("Alice"); // Duplicate - will not be added
names.add("Charlie");
names.add("Bob");   // Duplicate - will not be added

System.out.println("Names: " + names); // [Alice, Bob, Charlie] (insertion order preserved)
```

#### 3. Iteration Order
```java
Set<String> names = new LinkedHashSet<>();
names.add("Charlie");
names.add("Alice");
names.add("Bob");
names.add("David");

// Iteration follows insertion order
for (String name : names) {
    System.out.println("Name: " + name); // Charlie, Alice, Bob, David
}
```

### Real-World Example: Recently Viewed Items
```java
public class RecentlyViewedItems {
    private Set<String> viewedItems = new LinkedHashSet<>();
    private int maxSize = 10;
    
    public void viewItem(String itemId) {
        // Remove if already exists (to move to end)
        viewedItems.remove(itemId);
        
        // Add to end
        viewedItems.add(itemId);
        
        // Maintain size limit
        if (viewedItems.size() > maxSize) {
            String oldest = viewedItems.iterator().next();
            viewedItems.remove(oldest);
        }
    }
    
    public List<String> getRecentlyViewed() {
        return new ArrayList<>(viewedItems);
    }
    
    public List<String> getRecentlyViewed(int count) {
        return viewedItems.stream()
            .limit(count)
            .collect(Collectors.toList());
    }
    
    public void clearHistory() {
        viewedItems.clear();
    }
    
    public boolean hasViewed(String itemId) {
        return viewedItems.contains(itemId);
    }
}
```

## 4.4 TreeSet

TreeSet implements a Set using a Red-Black tree, providing sorted order and efficient range operations.

### Core Characteristics

#### 1. Red-Black Tree Implementation
- Self-balancing binary search tree
- Maintains sorted order automatically
- Guarantees O(log n) performance for all operations

#### 2. Performance Characteristics
- **Add**: O(log n)
- **Remove**: O(log n)
- **Contains**: O(log n)
- **Iteration**: O(n) - in sorted order

#### 3. Memory Characteristics
- Higher memory overhead than HashSet
- Additional memory for tree structure
- Good cache locality for sequential access

### Understanding TreeSet Operations

#### 1. Basic Operations
```java
// Create TreeSet
Set<String> names = new TreeSet<>();
Set<String> namesWithComparator = new TreeSet<>(String.CASE_INSENSITIVE_ORDER);

// Add elements
names.add("Charlie");
names.add("Alice");
names.add("Bob");
names.add("David");

System.out.println("Names: " + names); // [Alice, Bob, Charlie, David] (sorted order)
System.out.println("Size: " + names.size()); // 4
```

#### 2. Sorted Order
```java
Set<String> names = new TreeSet<>();
names.add("Zoe");
names.add("Alice");
names.add("Bob");
names.add("Alice"); // Duplicate - will not be added

System.out.println("Names: " + names); // [Alice, Bob, Zoe] (sorted order)
```

#### 3. Range Operations
```java
Set<String> names = new TreeSet<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");
names.add("David");
names.add("Eve");

// Get subset
Set<String> subset = names.subSet("Bob", "Eve");
System.out.println("Subset: " + subset); // [Bob, Charlie, David]

// Get head set (elements less than specified)
Set<String> headSet = names.headSet("David");
System.out.println("Head set: " + headSet); // [Alice, Bob, Charlie]

// Get tail set (elements greater than or equal to specified)
Set<String> tailSet = names.tailSet("Charlie");
System.out.println("Tail set: " + tailSet); // [Charlie, David, Eve]
```

#### 4. First and Last Elements
```java
Set<String> names = new TreeSet<>();
names.add("Charlie");
names.add("Alice");
names.add("Bob");
names.add("David");

// Get first element
String first = names.first();
System.out.println("First: " + first); // Alice

// Get last element
String last = names.last();
System.out.println("Last: " + last); // David

// Remove first element
String removedFirst = names.pollFirst();
System.out.println("Removed first: " + removedFirst); // Alice
System.out.println("After pollFirst: " + names); // [Bob, Charlie, David]

// Remove last element
String removedLast = names.pollLast();
System.out.println("Removed last: " + removedLast); // David
System.out.println("After pollLast: " + names); // [Bob, Charlie]
```

### Real-World Example: Leaderboard System
```java
public class Leaderboard {
    private TreeSet<PlayerScore> scores = new TreeSet<>((a, b) -> {
        // Sort by score descending, then by name ascending
        int scoreCompare = Integer.compare(b.getScore(), a.getScore());
        return scoreCompare != 0 ? scoreCompare : a.getName().compareTo(b.getName());
    });
    
    public void addScore(String playerName, int score) {
        scores.add(new PlayerScore(playerName, score));
    }
    
    public List<PlayerScore> getTopPlayers(int count) {
        return scores.stream()
            .limit(count)
            .collect(Collectors.toList());
    }
    
    public List<PlayerScore> getPlayersInRange(int minScore, int maxScore) {
        return scores.stream()
            .filter(score -> score.getScore() >= minScore && score.getScore() <= maxScore)
            .collect(Collectors.toList());
    }
    
    public PlayerScore getHighestScore() {
        return scores.first();
    }
    
    public PlayerScore getLowestScore() {
        return scores.last();
    }
    
    public int getPlayerRank(String playerName) {
        int rank = 1;
        for (PlayerScore score : scores) {
            if (score.getName().equals(playerName)) {
                return rank;
            }
            rank++;
        }
        return -1; // Player not found
    }
    
    public static class PlayerScore {
        private String name;
        private int score;
        
        public PlayerScore(String name, int score) {
            this.name = name;
            this.score = score;
        }
        
        public String getName() { return name; }
        public int getScore() { return score; }
        
        @Override
        public String toString() {
            return name + ": " + score;
        }
    }
}
```

## 4.5 EnumSet

EnumSet is a specialized Set implementation for enum types, providing extremely efficient operations and memory usage.

### Core Characteristics

#### 1. Bit Vector Implementation
- Uses bit vector for storage
- Extremely memory efficient
- Fast operations using bitwise operations

#### 2. Performance Characteristics
- **Add**: O(1)
- **Remove**: O(1)
- **Contains**: O(1)
- **Iteration**: O(n) - in enum declaration order

#### 3. Memory Characteristics
- Minimal memory usage
- Uses bit vector representation
- Excellent cache locality

### Understanding EnumSet Operations

#### 1. Basic Operations
```java
// Define enum
enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

// Create EnumSet
EnumSet<Day> workingDays = EnumSet.of(Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY);
EnumSet<Day> weekend = EnumSet.of(Day.SATURDAY, Day.SUNDAY);
EnumSet<Day> allDays = EnumSet.allOf(Day.class);
EnumSet<Day> none = EnumSet.noneOf(Day.class);

System.out.println("Working days: " + workingDays);
System.out.println("Weekend: " + weekend);
System.out.println("All days: " + allDays);
```

#### 2. Range Operations
```java
// Create range
EnumSet<Day> midWeek = EnumSet.range(Day.TUESDAY, Day.THURSDAY);
System.out.println("Mid week: " + midWeek); // [TUESDAY, WEDNESDAY, THURSDAY]

// Complement
EnumSet<Day> notWorkingDays = EnumSet.complementOf(workingDays);
System.out.println("Not working days: " + notWorkingDays); // [SATURDAY, SUNDAY]
```

#### 3. Set Operations
```java
EnumSet<Day> set1 = EnumSet.of(Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY);
EnumSet<Day> set2 = EnumSet.of(Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY);

// Union
EnumSet<Day> union = EnumSet.copyOf(set1);
union.addAll(set2);
System.out.println("Union: " + union); // [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY]

// Intersection
EnumSet<Day> intersection = EnumSet.copyOf(set1);
intersection.retainAll(set2);
System.out.println("Intersection: " + intersection); // [WEDNESDAY]

// Difference
EnumSet<Day> difference = EnumSet.copyOf(set1);
difference.removeAll(set2);
System.out.println("Difference: " + difference); // [MONDAY, TUESDAY]
```

### Real-World Example: Permission System
```java
public class PermissionManager {
    public enum Permission {
        READ, WRITE, DELETE, EXECUTE, ADMIN
    }
    
    private Map<String, EnumSet<Permission>> userPermissions = new HashMap<>();
    
    public void grantPermission(String username, Permission permission) {
        userPermissions.computeIfAbsent(username, k -> EnumSet.noneOf(Permission.class))
                      .add(permission);
    }
    
    public void grantPermissions(String username, Permission... permissions) {
        userPermissions.computeIfAbsent(username, k -> EnumSet.noneOf(Permission.class))
                      .addAll(EnumSet.of(permissions[0], permissions));
    }
    
    public boolean hasPermission(String username, Permission permission) {
        return userPermissions.getOrDefault(username, EnumSet.noneOf(Permission.class))
                             .contains(permission);
    }
    
    public boolean hasAllPermissions(String username, Permission... permissions) {
        EnumSet<Permission> userPerms = userPermissions.getOrDefault(username, EnumSet.noneOf(Permission.class));
        return userPerms.containsAll(EnumSet.of(permissions[0], permissions));
    }
    
    public boolean hasAnyPermission(String username, Permission... permissions) {
        EnumSet<Permission> userPerms = userPermissions.getOrDefault(username, EnumSet.noneOf(Permission.class));
        EnumSet<Permission> requiredPerms = EnumSet.of(permissions[0], permissions);
        
        for (Permission perm : requiredPerms) {
            if (userPerms.contains(perm)) {
                return true;
            }
        }
        return false;
    }
    
    public void revokePermission(String username, Permission permission) {
        EnumSet<Permission> perms = userPermissions.get(username);
        if (perms != null) {
            perms.remove(permission);
            if (perms.isEmpty()) {
                userPermissions.remove(username);
            }
        }
    }
    
    public Set<Permission> getUserPermissions(String username) {
        return userPermissions.getOrDefault(username, EnumSet.noneOf(Permission.class));
    }
}
```

## 4.6 Set Implementation Best Practices

Following best practices ensures optimal performance and maintainable code when working with Set implementations.

### 1. Choose the Right Implementation

#### Use HashSet When:
- Fast lookup is required
- Order doesn't matter
- Memory efficiency is important
- General-purpose set operations

```java
// Good for fast lookup
Set<String> usernames = new HashSet<>();
boolean exists = usernames.contains("alice"); // O(1) average
```

#### Use LinkedHashSet When:
- Fast lookup is required
- Insertion order must be maintained
- Memory usage is not critical
- LRU cache implementation

```java
// Good for maintaining order
Set<String> recentlyViewed = new LinkedHashSet<>();
recentlyViewed.add("item1");
recentlyViewed.add("item2");
// Order is preserved: [item1, item2]
```

#### Use TreeSet When:
- Sorted order is required
- Range operations are needed
- Memory usage is not critical
- Comparable elements

```java
// Good for sorted order
Set<String> sortedNames = new TreeSet<>();
sortedNames.add("Charlie");
sortedNames.add("Alice");
// Automatically sorted: [Alice, Charlie]
```

#### Use EnumSet When:
- Working with enum types
- Maximum performance required
- Memory efficiency is critical
- Bitwise operations are acceptable

```java
// Good for enum types
EnumSet<Day> workingDays = EnumSet.of(Day.MONDAY, Day.TUESDAY);
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

// Use in Set
Set<Person> people = new HashSet<>();
people.add(new Person("Alice", 25));
people.add(new Person("Bob", 30));
people.add(new Person("Alice", 25)); // Duplicate - will not be added
```

### 3. Use Immutable Sets When Possible

```java
// Good: Immutable set
Set<String> immutableSet = Set.of("Alice", "Bob", "Charlie");

// Good: Unmodifiable view
Set<String> unmodifiableSet = Collections.unmodifiableSet(originalSet);

// Bad: Mutable set when immutability is desired
Set<String> mutableSet = new HashSet<>();
mutableSet.add("Alice");
mutableSet.add("Bob");
```

### 4. Avoid Concurrent Modification

```java
// Bad: Concurrent modification
Set<String> names = new HashSet<>();
for (String name : names) {
    if (name.startsWith("A")) {
        names.remove(name); // ConcurrentModificationException
    }
}

// Good: Use iterator
Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.startsWith("A")) {
        iterator.remove(); // Safe removal
    }
}
```

### 5. Use Bulk Operations

```java
// Good: Bulk operations
Set<String> set1 = new HashSet<>();
Set<String> set2 = new HashSet<>();

// Union
Set<String> union = new HashSet<>(set1);
union.addAll(set2);

// Intersection
Set<String> intersection = new HashSet<>(set1);
intersection.retainAll(set2);

// Difference
Set<String> difference = new HashSet<>(set1);
difference.removeAll(set2);
```

## 4.7 Set Implementation Testing

Comprehensive testing ensures Set implementations work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testHashSetOperations() {
    Set<String> set = new HashSet<>();
    
    // Test add
    assertTrue(set.add("Alice"));
    assertFalse(set.add("Alice")); // Duplicate
    assertEquals(1, set.size());
    
    // Test contains
    assertTrue(set.contains("Alice"));
    assertFalse(set.contains("Bob"));
    
    // Test remove
    assertTrue(set.remove("Alice"));
    assertFalse(set.remove("Alice")); // Already removed
    assertEquals(0, set.size());
}
```

### 2. Performance Testing

```java
@Test
public void testSetPerformance() {
    Set<String> set = new HashSet<>();
    int size = 100000;
    
    // Test add performance
    long startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        set.add("Item " + i);
    }
    long addTime = System.currentTimeMillis() - startTime;
    
    // Test contains performance
    startTime = System.currentTimeMillis();
    for (int i = 0; i < size; i++) {
        boolean contains = set.contains("Item " + i);
    }
    long containsTime = System.currentTimeMillis() - startTime;
    
    System.out.println("Add time: " + addTime + "ms");
    System.out.println("Contains time: " + containsTime + "ms");
    
    assertTrue(addTime < 1000); // Should complete within 1 second
    assertTrue(containsTime < 100); // Should complete within 100ms
}
```

### 3. Edge Case Testing

```java
@Test
public void testEdgeCases() {
    Set<String> set = new HashSet<>();
    
    // Test empty set
    assertTrue(set.isEmpty());
    assertEquals(0, set.size());
    
    // Test null element
    set.add(null);
    assertTrue(set.contains(null));
    assertEquals(1, set.size());
    
    // Test duplicate null
    assertFalse(set.add(null)); // Duplicate null
    assertEquals(1, set.size());
}
```

## 4.8 Set Implementation Performance

Understanding performance characteristics helps in choosing the right implementation and optimizing code.

### Performance Comparison

| Operation | HashSet | LinkedHashSet | TreeSet | EnumSet |
|-----------|---------|---------------|---------|---------|
| add() | O(1) avg | O(1) avg | O(log n) | O(1) |
| remove() | O(1) avg | O(1) avg | O(log n) | O(1) |
| contains() | O(1) avg | O(1) avg | O(log n) | O(1) |
| iteration | O(n) | O(n) | O(n) | O(n) |
| memory | Medium | High | High | Low |

### Memory Usage

```java
// HashSet memory usage
Set<String> hashSet = new HashSet<>();
// Memory: hash table + buckets + elements

// LinkedHashSet memory usage
Set<String> linkedHashSet = new LinkedHashSet<>();
// Memory: hash table + buckets + elements + linked list

// TreeSet memory usage
Set<String> treeSet = new TreeSet<>();
// Memory: tree nodes + elements

// EnumSet memory usage
EnumSet<Day> enumSet = EnumSet.of(Day.MONDAY, Day.TUESDAY);
// Memory: bit vector (very efficient)
```

### Performance Optimization Tips

#### 1. Use Appropriate Initial Capacity
```java
// Good: Set capacity if known
Set<String> set = new HashSet<>(expectedSize);

// Bad: Let it grow multiple times
Set<String> set = new HashSet<>(); // Will grow: 16 -> 32 -> 64 -> 128...
```

#### 2. Use EnumSet for Enums
```java
// Good: Use EnumSet for enum types
EnumSet<Day> days = EnumSet.of(Day.MONDAY, Day.TUESDAY);

// Bad: Use HashSet for enum types
Set<Day> days = new HashSet<>();
days.add(Day.MONDAY);
days.add(Day.TUESDAY);
```

#### 3. Use Immutable Sets When Possible
```java
// Good: Immutable set
Set<String> set = Set.of("Alice", "Bob", "Charlie");

// Bad: Mutable set when immutability is sufficient
Set<String> set = new HashSet<>();
set.add("Alice");
set.add("Bob");
set.add("Charlie");
```

## 4.9 Set Implementation Troubleshooting

Common issues and solutions when working with Set implementations.

### 1. Duplicate Elements Not Removed

```java
// Problem: Custom objects without proper equals/hashCode
class Person {
    private String name;
    private int age;
    
    // Missing equals() and hashCode() methods
}

Set<Person> people = new HashSet<>();
people.add(new Person("Alice", 25));
people.add(new Person("Alice", 25)); // Duplicate not removed

// Solution: Implement equals() and hashCode()
class Person {
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
```

### 2. NullPointerException in TreeSet

```java
// Problem: TreeSet doesn't allow null elements
Set<String> set = new TreeSet<>();
set.add(null); // NullPointerException

// Solution: Use HashSet or LinkedHashSet
Set<String> set = new HashSet<>();
set.add(null); // OK
```

### 3. Performance Issues

```java
// Problem: Using wrong implementation
Set<String> set = new TreeSet<>();
for (int i = 0; i < 1000000; i++) {
    set.add("Item " + i); // O(log n) per operation
}

// Solution: Use HashSet for better performance
Set<String> set = new HashSet<>();
for (int i = 0; i < 1000000; i++) {
    set.add("Item " + i); // O(1) average per operation
}
```

### 4. Memory Issues

```java
// Problem: Not clearing references
Set<String> largeSet = new HashSet<>();
// ... populate with large data
largeSet = null; // Still holds references

// Solution: Clear references
largeSet.clear();
largeSet = null;
```

## 4.10 Set Implementation Security

Security considerations when working with Set implementations.

### 1. Input Validation

```java
public class SecureSetManager {
    private Set<String> data = new HashSet<>();
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
            throw new IllegalStateException("Set is full");
        }
        
        // Sanitize input
        String sanitized = input.trim().replaceAll("[<>\"'&]", "");
        
        return data.add(sanitized);
    }
}
```

### 2. Access Control

```java
public class SecureSetWrapper {
    private Set<String> data = new HashSet<>();
    private Set<String> allowedUsers = new HashSet<>();
    
    public boolean addData(String user, String data) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return this.data.add(data);
    }
    
    public Set<String> getData(String user) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return new HashSet<>(data); // Return copy
    }
}
```

### 3. Data Encryption

```java
public class EncryptedSetManager {
    private Set<String> encryptedData = new HashSet<>();
    private String encryptionKey = "secret-key";
    
    public void addEncryptedData(String data) {
        String encrypted = encrypt(data, encryptionKey);
        encryptedData.add(encrypted);
    }
    
    public Set<String> getDecryptedData() {
        return encryptedData.stream()
            .map(encrypted -> decrypt(encrypted, encryptionKey))
            .collect(Collectors.toSet());
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

Understanding Set implementations is crucial for effective Java programming. Each implementation has its strengths and weaknesses, and choosing the right one depends on your specific use case, performance requirements, and whether you need ordering or sorting capabilities.