# Section 9 – Collections Utility Class

## 9.1 Collections Utility Concepts

The Collections utility class provides static methods for operating on collections, offering a wide range of operations including sorting, searching, synchronization, and transformation. Understanding these utility methods is essential for efficient collection manipulation.

### What is the Collections Utility Class?

The Collections class is a utility class that contains static methods for:
- **Sorting**: Ordering elements in collections
- **Searching**: Finding elements in sorted collections
- **Synchronization**: Making collections thread-safe
- **Transformation**: Creating unmodifiable views
- **Statistics**: Finding min/max values
- **Shuffling**: Randomizing element order

### Key Characteristics of Collections Utility

#### 1. Static Methods
- All methods are static
- No need to create instances
- Easy to use and access

#### 2. Generic Support
- Type-safe operations
- Works with any collection type
- Compile-time type checking

#### 3. Performance Optimized
- Efficient implementations
- Optimized for different collection types
- Minimal overhead

### Common Collections Utility Categories

| Category | Methods | Purpose |
|----------|---------|---------|
| Sorting | sort(), reverse() | Order elements |
| Searching | binarySearch() | Find elements |
| Synchronization | synchronizedList(), synchronizedSet() | Thread safety |
| Transformation | unmodifiableList(), emptyList() | Immutable views |
| Statistics | min(), max(), frequency() | Data analysis |
| Shuffling | shuffle() | Randomize order |

### Real-World Analogy: Swiss Army Knife

Think of the Collections utility class as a Swiss Army knife for collections:

- **Sorting methods**: Like a ruler that helps you organize items in order
- **Searching methods**: Like a magnifying glass that helps you find specific items
- **Synchronization methods**: Like a lock that makes shared items safe for multiple people
- **Transformation methods**: Like a mold that creates unchangeable copies
- **Statistics methods**: Like a calculator that finds the biggest, smallest, or most common items
- **Shuffling methods**: Like a dice that randomizes the order of items

## 9.2 Sorting Methods

Sorting methods provide various ways to order elements in collections, from simple natural ordering to complex custom comparators.

### Core Sorting Methods

```java
public class Collections {
    // Basic sorting
    public static <T extends Comparable<? super T>> void sort(List<T> list)
    public static <T> void sort(List<T> list, Comparator<? super T> c)
    
    // Reverse operations
    public static void reverse(List<?> list)
    public static <T> Comparator<T> reverseOrder()
    public static <T> Comparator<T> reverseOrder(Comparator<T> cmp)
    
    // Rotate and swap
    public static void rotate(List<?> list, int distance)
    public static void swap(List<?> list, int i, int j)
}
```

### Understanding Sorting Operations

#### 1. Natural Ordering
```java
List<String> names = new ArrayList<>();
names.add("Charlie");
names.add("Alice");
names.add("Bob");
names.add("David");

// Sort using natural ordering
Collections.sort(names);
System.out.println("Sorted: " + names); // [Alice, Bob, Charlie, David]
```

#### 2. Custom Comparator
```java
List<Person> people = new ArrayList<>();
people.add(new Person("Alice", 25));
people.add(new Person("Bob", 30));
people.add(new Person("Charlie", 35));

// Sort by age
Collections.sort(people, (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));
System.out.println("Sorted by age: " + people);

// Sort by name
Collections.sort(people, (p1, p2) -> p1.getName().compareTo(p2.getName()));
System.out.println("Sorted by name: " + people);
```

#### 3. Reverse Operations
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

// Reverse the list
Collections.reverse(names);
System.out.println("Reversed: " + names); // [Charlie, Bob, Alice]

// Sort in reverse order
Collections.sort(names, Collections.reverseOrder());
System.out.println("Reverse sorted: " + names); // [Charlie, Bob, Alice]
```

#### 4. Rotate and Swap
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");
names.add("David");

// Rotate by 2 positions
Collections.rotate(names, 2);
System.out.println("Rotated: " + names); // [Charlie, David, Alice, Bob]

// Swap elements
Collections.swap(names, 0, 2);
System.out.println("After swap: " + names); // [Alice, David, Charlie, Bob]
```

### Real-World Example: Student Grade Management
```java
public class StudentGradeManager {
    private List<Student> students = new ArrayList<>();
    
    public void addStudent(Student student) {
        students.add(student);
    }
    
    public void sortByGrade() {
        Collections.sort(students, (s1, s2) -> 
            Double.compare(s2.getGrade(), s1.getGrade())); // Descending order
    }
    
    public void sortByName() {
        Collections.sort(students, (s1, s2) -> 
            s1.getName().compareTo(s2.getName()));
    }
    
    public void sortByGradeThenName() {
        Collections.sort(students, (s1, s2) -> {
            int gradeCompare = Double.compare(s2.getGrade(), s1.getGrade());
            if (gradeCompare != 0) {
                return gradeCompare;
            }
            return s1.getName().compareTo(s2.getName());
        });
    }
    
    public void reverseOrder() {
        Collections.reverse(students);
    }
    
    public List<Student> getTopStudents(int count) {
        List<Student> sortedStudents = new ArrayList<>(students);
        Collections.sort(sortedStudents, (s1, s2) -> 
            Double.compare(s2.getGrade(), s1.getGrade()));
        return sortedStudents.subList(0, Math.min(count, sortedStudents.size()));
    }
    
    public void printStudents() {
        for (Student student : students) {
            System.out.println(student.getName() + ": " + student.getGrade());
        }
    }
    
    public static class Student {
        private String name;
        private double grade;
        
        public Student(String name, double grade) {
            this.name = name;
            this.grade = grade;
        }
        
        public String getName() { return name; }
        public double getGrade() { return grade; }
        
        @Override
        public String toString() {
            return "Student{name='" + name + "', grade=" + grade + "}";
        }
    }
}
```

## 9.3 Searching Methods

Searching methods provide efficient ways to find elements in collections, particularly in sorted collections.

### Core Searching Methods

```java
public class Collections {
    // Binary search
    public static <T> int binarySearch(List<? extends Comparable<? super T>> list, T key)
    public static <T> int binarySearch(List<? extends T> list, T key, Comparator<? super T> c)
    
    // Frequency and statistics
    public static int frequency(Collection<?> c, Object o)
    public static <T> T max(Collection<? extends T> coll, Comparator<? super T> comp)
    public static <T extends Object & Comparable<? super T>> T max(Collection<? extends T> coll)
    public static <T> T min(Collection<? extends T> coll, Comparator<? super T> comp)
    public static <T extends Object & Comparable<? super T>> T min(Collection<? extends T> coll)
}
```

### Understanding Searching Operations

#### 1. Binary Search
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");
names.add("David");

// Sort the list first (binary search requires sorted list)
Collections.sort(names);

// Binary search
int index = Collections.binarySearch(names, "Charlie");
System.out.println("Charlie found at index: " + index); // 2

// Search for non-existent element
int notFound = Collections.binarySearch(names, "Eve");
System.out.println("Eve not found, insertion point: " + (-notFound - 1)); // 4
```

#### 2. Custom Comparator Search
```java
List<Person> people = new ArrayList<>();
people.add(new Person("Alice", 25));
people.add(new Person("Bob", 30));
people.add(new Person("Charlie", 35));

// Sort by age
Collections.sort(people, (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));

// Search by age
Person searchKey = new Person("", 30);
int index = Collections.binarySearch(people, searchKey, 
    (p1, p2) -> Integer.compare(p1.getAge(), p2.getAge()));
System.out.println("Person with age 30 found at index: " + index);
```

#### 3. Frequency and Statistics
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Alice");
names.add("Charlie");
names.add("Alice");

// Count frequency
int aliceCount = Collections.frequency(names, "Alice");
System.out.println("Alice appears " + aliceCount + " times"); // 3

// Find maximum
String maxName = Collections.max(names);
System.out.println("Maximum name: " + maxName); // Charlie

// Find minimum
String minName = Collections.min(names);
System.out.println("Minimum name: " + minName); // Alice
```

### Real-World Example: Library Management
```java
public class LibraryManager {
    private List<Book> books = new ArrayList<>();
    
    public void addBook(Book book) {
        books.add(book);
    }
    
    public Book findBookByTitle(String title) {
        // Sort by title first
        Collections.sort(books, (b1, b2) -> b1.getTitle().compareTo(b2.getTitle()));
        
        // Create search key
        Book searchKey = new Book(title, "", 0);
        
        // Binary search
        int index = Collections.binarySearch(books, searchKey, 
            (b1, b2) -> b1.getTitle().compareTo(b2.getTitle()));
        
        return index >= 0 ? books.get(index) : null;
    }
    
    public List<Book> findBooksByAuthor(String author) {
        return books.stream()
            .filter(book -> book.getAuthor().equals(author))
            .collect(Collectors.toList());
    }
    
    public Book findMostExpensiveBook() {
        return Collections.max(books, (b1, b2) -> 
            Double.compare(b1.getPrice(), b2.getPrice()));
    }
    
    public Book findCheapestBook() {
        return Collections.min(books, (b1, b2) -> 
            Double.compare(b1.getPrice(), b2.getPrice()));
    }
    
    public int countBooksByAuthor(String author) {
        return Collections.frequency(books, new Book("", author, 0));
    }
    
    public void sortBooksByTitle() {
        Collections.sort(books, (b1, b2) -> b1.getTitle().compareTo(b2.getTitle()));
    }
    
    public void sortBooksByPrice() {
        Collections.sort(books, (b1, b2) -> Double.compare(b1.getPrice(), b2.getPrice()));
    }
    
    public static class Book {
        private String title;
        private String author;
        private double price;
        
        public Book(String title, String author, double price) {
            this.title = title;
            this.author = author;
            this.price = price;
        }
        
        public String getTitle() { return title; }
        public String getAuthor() { return author; }
        public double getPrice() { return price; }
        
        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            Book book = (Book) obj;
            return Objects.equals(author, book.author);
        }
        
        @Override
        public int hashCode() {
            return Objects.hash(author);
        }
        
        @Override
        public String toString() {
            return "Book{title='" + title + "', author='" + author + "', price=" + price + "}";
        }
    }
}
```

## 9.4 Synchronization Methods

Synchronization methods provide thread-safe wrappers for collections, ensuring safe access in multi-threaded environments.

### Core Synchronization Methods

```java
public class Collections {
    // List synchronization
    public static <T> List<T> synchronizedList(List<T> list)
    
    // Set synchronization
    public static <T> Set<T> synchronizedSet(Set<T> s)
    public static <T> SortedSet<T> synchronizedSortedSet(SortedSet<T> s)
    
    // Map synchronization
    public static <K,V> Map<K,V> synchronizedMap(Map<K,V> m)
    public static <K,V> SortedMap<K,V> synchronizedSortedMap(SortedMap<K,V> m)
    
    // Collection synchronization
    public static <T> Collection<T> synchronizedCollection(Collection<T> c)
}
```

### Understanding Synchronization Operations

#### 1. List Synchronization
```java
List<String> originalList = new ArrayList<>();
List<String> synchronizedList = Collections.synchronizedList(originalList);

// Multiple threads can safely access
Thread thread1 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        synchronizedList.add("Thread1-" + i);
    }
});

Thread thread2 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        synchronizedList.add("Thread2-" + i);
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

System.out.println("Final size: " + synchronizedList.size()); // 2000
```

#### 2. Set Synchronization
```java
Set<String> originalSet = new HashSet<>();
Set<String> synchronizedSet = Collections.synchronizedSet(originalSet);

// Multiple threads can safely access
Thread thread1 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        synchronizedSet.add("Item-" + i);
    }
});

Thread thread2 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        synchronizedSet.add("Item-" + i);
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

System.out.println("Final size: " + synchronizedSet.size()); // 1000 (duplicates removed)
```

#### 3. Map Synchronization
```java
Map<String, Integer> originalMap = new HashMap<>();
Map<String, Integer> synchronizedMap = Collections.synchronizedMap(originalMap);

// Multiple threads can safely access
Thread thread1 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        synchronizedMap.put("Key-" + i, i);
    }
});

Thread thread2 = new Thread(() -> {
    for (int i = 0; i < 1000; i++) {
        synchronizedMap.put("Key-" + (i + 1000), i + 1000);
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

System.out.println("Final size: " + synchronizedMap.size()); // 2000
```

### Real-World Example: Thread-Safe Data Manager
```java
public class ThreadSafeDataManager {
    private List<String> data = new ArrayList<>();
    private Set<String> uniqueData = new HashSet<>();
    private Map<String, Integer> dataCount = new HashMap<>();
    
    public ThreadSafeDataManager() {
        // Wrap collections with synchronized versions
        this.data = Collections.synchronizedList(new ArrayList<>());
        this.uniqueData = Collections.synchronizedSet(new HashSet<>());
        this.dataCount = Collections.synchronizedMap(new HashMap<>());
    }
    
    public void addData(String item) {
        data.add(item);
        uniqueData.add(item);
        dataCount.merge(item, 1, Integer::sum);
    }
    
    public boolean containsData(String item) {
        return data.contains(item);
    }
    
    public int getDataCount() {
        return data.size();
    }
    
    public int getUniqueDataCount() {
        return uniqueData.size();
    }
    
    public int getItemCount(String item) {
        return dataCount.getOrDefault(item, 0);
    }
    
    public List<String> getAllData() {
        return new ArrayList<>(data);
    }
    
    public Set<String> getUniqueData() {
        return new HashSet<>(uniqueData);
    }
    
    public Map<String, Integer> getDataCounts() {
        return new HashMap<>(dataCount);
    }
    
    public void clearData() {
        data.clear();
        uniqueData.clear();
        dataCount.clear();
    }
}
```

## 9.5 Unmodifiable Collections

Unmodifiable collections provide read-only views of collections, preventing modifications while allowing access to the underlying data.

### Core Unmodifiable Methods

```java
public class Collections {
    // List unmodifiable views
    public static <T> List<T> unmodifiableList(List<? extends T> list)
    public static <T> List<T> emptyList()
    public static <T> List<T> singletonList(T o)
    public static <T> List<T> nCopies(int n, T o)
    
    // Set unmodifiable views
    public static <T> Set<T> unmodifiableSet(Set<? extends T> s)
    public static <T> Set<T> emptySet()
    public static <T> Set<T> singleton(T o)
    
    // Map unmodifiable views
    public static <K,V> Map<K,V> unmodifiableMap(Map<? extends K, ? extends V> m)
    public static <K,V> Map<K,V> emptyMap()
    public static <K,V> Map<K,V> singletonMap(K key, V value)
    
    // Collection unmodifiable views
    public static <T> Collection<T> unmodifiableCollection(Collection<? extends T> c)
}
```

### Understanding Unmodifiable Operations

#### 1. Unmodifiable Views
```java
List<String> originalList = new ArrayList<>();
originalList.add("Alice");
originalList.add("Bob");
originalList.add("Charlie");

// Create unmodifiable view
List<String> unmodifiableList = Collections.unmodifiableList(originalList);

// Can read from unmodifiable list
System.out.println("First element: " + unmodifiableList.get(0)); // Alice

// Cannot modify unmodifiable list
try {
    unmodifiableList.add("David"); // UnsupportedOperationException
} catch (UnsupportedOperationException e) {
    System.out.println("Cannot modify unmodifiable list");
}

// Can still modify original list
originalList.add("David");
System.out.println("Original list: " + originalList); // [Alice, Bob, Charlie, David]
System.out.println("Unmodifiable list: " + unmodifiableList); // [Alice, Bob, Charlie, David]
```

#### 2. Empty Collections
```java
// Empty collections
List<String> emptyList = Collections.emptyList();
Set<String> emptySet = Collections.emptySet();
Map<String, String> emptyMap = Collections.emptyMap();

System.out.println("Empty list size: " + emptyList.size()); // 0
System.out.println("Empty set size: " + emptySet.size()); // 0
System.out.println("Empty map size: " + emptyMap.size()); // 0

// Cannot modify empty collections
try {
    emptyList.add("Alice"); // UnsupportedOperationException
} catch (UnsupportedOperationException e) {
    System.out.println("Cannot modify empty list");
}
```

#### 3. Singleton Collections
```java
// Singleton collections
List<String> singletonList = Collections.singletonList("Alice");
Set<String> singletonSet = Collections.singleton("Bob");
Map<String, String> singletonMap = Collections.singletonMap("key", "value");

System.out.println("Singleton list: " + singletonList); // [Alice]
System.out.println("Singleton set: " + singletonSet); // [Bob]
System.out.println("Singleton map: " + singletonMap); // {key=value}

// Cannot modify singleton collections
try {
    singletonList.add("Bob"); // UnsupportedOperationException
} catch (UnsupportedOperationException e) {
    System.out.println("Cannot modify singleton list");
}
```

#### 4. N Copies
```java
// Create list with n copies
List<String> repeatedList = Collections.nCopies(3, "Hello");
System.out.println("Repeated list: " + repeatedList); // [Hello, Hello, Hello]

// Cannot modify n copies list
try {
    repeatedList.add("World"); // UnsupportedOperationException
} catch (UnsupportedOperationException e) {
    System.out.println("Cannot modify n copies list");
}
```

### Real-World Example: Configuration Manager
```java
public class ConfigurationManager {
    private Map<String, String> config = new HashMap<>();
    private Map<String, String> unmodifiableConfig;
    
    public ConfigurationManager() {
        this.unmodifiableConfig = Collections.unmodifiableMap(config);
    }
    
    public void setProperty(String key, String value) {
        config.put(key, value);
    }
    
    public String getProperty(String key) {
        return config.get(key);
    }
    
    public String getProperty(String key, String defaultValue) {
        return config.getOrDefault(key, defaultValue);
    }
    
    public Map<String, String> getUnmodifiableConfig() {
        return unmodifiableConfig; // Returns read-only view
    }
    
    public Map<String, String> getConfigCopy() {
        return new HashMap<>(config); // Returns modifiable copy
    }
    
    public void loadDefaultConfig() {
        config.put("database.url", "jdbc:mysql://localhost:3306/mydb");
        config.put("database.username", "admin");
        config.put("database.password", "password");
        config.put("server.port", "8080");
        config.put("server.host", "localhost");
    }
    
    public void printConfig() {
        System.out.println("Configuration:");
        for (Map.Entry<String, String> entry : unmodifiableConfig.entrySet()) {
            System.out.println("  " + entry.getKey() + " = " + entry.getValue());
        }
    }
}
```

## 9.6 Collections Utility Best Practices

Following best practices ensures efficient and maintainable code when working with Collections utility methods.

### 1. Choose the Right Method

#### Use sort() When:
- Need to order elements
- Performance is important
- Working with large collections

```java
// Good: Use sort() for ordering
List<String> names = new ArrayList<>();
names.add("Charlie");
names.add("Alice");
names.add("Bob");
Collections.sort(names);
```

#### Use binarySearch() When:
- Collection is already sorted
- Need efficient searching
- Working with large collections

```java
// Good: Use binarySearch() for sorted collections
Collections.sort(names);
int index = Collections.binarySearch(names, "Alice");
```

#### Use synchronizedX() When:
- Thread safety is required
- Legacy code compatibility
- Simple synchronization needed

```java
// Good: Use synchronizedX() for thread safety
List<String> synchronizedList = Collections.synchronizedList(new ArrayList<>());
```

#### Use unmodifiableX() When:
- Need read-only access
- Prevent accidental modifications
- Return data to clients

```java
// Good: Use unmodifiableX() for read-only access
List<String> unmodifiableList = Collections.unmodifiableList(originalList);
```

### 2. Handle Exceptions Properly

```java
// Good: Handle exceptions
try {
    List<String> unmodifiableList = Collections.unmodifiableList(originalList);
    unmodifiableList.add("New Item"); // UnsupportedOperationException
} catch (UnsupportedOperationException e) {
    System.out.println("Cannot modify unmodifiable list");
}
```

### 3. Use Appropriate Comparators

```java
// Good: Use appropriate comparators
List<Person> people = new ArrayList<>();
Collections.sort(people, (p1, p2) -> p1.getName().compareTo(p2.getName()));

// Good: Use method references
Collections.sort(people, Comparator.comparing(Person::getName));
```

### 4. Consider Performance Implications

```java
// Good: Sort once, search multiple times
Collections.sort(names);
int index1 = Collections.binarySearch(names, "Alice");
int index2 = Collections.binarySearch(names, "Bob");

// Bad: Sort every time before searching
Collections.sort(names);
int index1 = Collections.binarySearch(names, "Alice");
Collections.sort(names); // Unnecessary
int index2 = Collections.binarySearch(names, "Bob");
```

## 9.7 Collections Utility Testing

Comprehensive testing ensures Collections utility methods work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testSortOperations() {
    List<String> names = new ArrayList<>();
    names.add("Charlie");
    names.add("Alice");
    names.add("Bob");
    
    // Test sort
    Collections.sort(names);
    assertEquals("Alice", names.get(0));
    assertEquals("Bob", names.get(1));
    assertEquals("Charlie", names.get(2));
    
    // Test reverse
    Collections.reverse(names);
    assertEquals("Charlie", names.get(0));
    assertEquals("Bob", names.get(1));
    assertEquals("Alice", names.get(2));
}
```

### 2. Performance Testing

```java
@Test
public void testSortPerformance() {
    List<String> names = new ArrayList<>();
    for (int i = 0; i < 100000; i++) {
        names.add("Name" + i);
    }
    
    // Test sort performance
    long startTime = System.currentTimeMillis();
    Collections.sort(names);
    long sortTime = System.currentTimeMillis() - startTime;
    
    // Test binary search performance
    startTime = System.currentTimeMillis();
    int index = Collections.binarySearch(names, "Name50000");
    long searchTime = System.currentTimeMillis() - startTime;
    
    System.out.println("Sort time: " + sortTime + "ms");
    System.out.println("Search time: " + searchTime + "ms");
    
    assertTrue(sortTime < 1000); // Should complete within 1 second
    assertTrue(searchTime < 10);  // Should complete within 10ms
}
```

### 3. Thread Safety Testing

```java
@Test
public void testSynchronization() throws InterruptedException {
    List<String> originalList = new ArrayList<>();
    List<String> synchronizedList = Collections.synchronizedList(originalList);
    
    int numThreads = 10;
    int itemsPerThread = 1000;
    
    // Create threads
    List<Thread> threads = new ArrayList<>();
    for (int i = 0; i < numThreads; i++) {
        final int threadId = i;
        Thread thread = new Thread(() -> {
            for (int j = 0; j < itemsPerThread; j++) {
                synchronizedList.add("Thread-" + threadId + "-Item-" + j);
            }
        });
        threads.add(thread);
        thread.start();
    }
    
    // Wait for all threads to complete
    for (Thread thread : threads) {
        thread.join();
    }
    
    // Verify all items were added
    assertEquals(numThreads * itemsPerThread, synchronizedList.size());
}
```

## 9.8 Collections Utility Performance

Understanding performance characteristics helps in choosing the right utility method and optimizing code.

### Performance Comparison

| Operation | ArrayList | LinkedList | HashSet | TreeSet |
|-----------|-----------|------------|---------|---------|
| sort() | O(n log n) | O(n log n) | N/A | N/A |
| binarySearch() | O(log n) | O(n) | N/A | N/A |
| frequency() | O(n) | O(n) | O(n) | O(n) |
| min/max() | O(n) | O(n) | O(n) | O(n) |

### Memory Usage

```java
// sort() memory usage
Collections.sort(list);
// Memory: O(1) additional space for in-place sorting

// binarySearch() memory usage
Collections.binarySearch(list, key);
// Memory: O(1) additional space

// synchronizedX() memory usage
Collections.synchronizedList(list);
// Memory: O(1) additional space for wrapper

// unmodifiableX() memory usage
Collections.unmodifiableList(list);
// Memory: O(1) additional space for wrapper
```

### Performance Optimization Tips

#### 1. Use Appropriate Sorting Algorithm
```java
// Good: Use sort() for general purpose
Collections.sort(list);

// Good: Use specialized sorting for specific cases
list.sort(Comparator.naturalOrder());
```

#### 2. Sort Once, Search Multiple Times
```java
// Good: Sort once, search multiple times
Collections.sort(list);
int index1 = Collections.binarySearch(list, "Alice");
int index2 = Collections.binarySearch(list, "Bob");

// Bad: Sort every time before searching
Collections.sort(list);
int index1 = Collections.binarySearch(list, "Alice");
Collections.sort(list); // Unnecessary
int index2 = Collections.binarySearch(list, "Bob");
```

#### 3. Use Appropriate Data Structures
```java
// Good: Use TreeSet for sorted data
TreeSet<String> sortedSet = new TreeSet<>();
sortedSet.add("Alice");
sortedSet.add("Bob");
// Already sorted, no need to sort

// Bad: Use ArrayList and sort every time
List<String> list = new ArrayList<>();
list.add("Alice");
list.add("Bob");
Collections.sort(list); // Unnecessary if using TreeSet
```

## 9.9 Collections Utility Troubleshooting

Common issues and solutions when working with Collections utility methods.

### 1. UnsupportedOperationException

```java
// Problem: Trying to modify unmodifiable collection
List<String> unmodifiableList = Collections.unmodifiableList(originalList);
unmodifiableList.add("New Item"); // UnsupportedOperationException

// Solution: Use original collection or create new list
originalList.add("New Item"); // OK
// Or
List<String> newList = new ArrayList<>(unmodifiableList);
newList.add("New Item"); // OK
```

### 2. ClassCastException

```java
// Problem: Incompatible types in sorting
List<Object> mixedList = new ArrayList<>();
mixedList.add("String");
mixedList.add(123);
Collections.sort(mixedList); // ClassCastException

// Solution: Use appropriate types or comparators
List<String> stringList = new ArrayList<>();
stringList.add("String1");
stringList.add("String2");
Collections.sort(stringList); // OK
```

### 3. Performance Issues

```java
// Problem: Sorting large collections frequently
List<String> largeList = new ArrayList<>();
// ... populate with large data
for (int i = 0; i < 1000; i++) {
    Collections.sort(largeList); // O(n log n) each time
    // ... do something
}

// Solution: Sort once or use appropriate data structure
Collections.sort(largeList); // Sort once
// Or use TreeSet for automatically sorted data
TreeSet<String> sortedSet = new TreeSet<>(largeList);
```

### 4. Thread Safety Issues

```java
// Problem: Using non-synchronized collections in multi-threaded environment
List<String> list = new ArrayList<>();
// Multiple threads accessing list can cause issues

// Solution: Use synchronized collections
List<String> synchronizedList = Collections.synchronizedList(new ArrayList<>());
// Multiple threads can safely access
```

## 9.10 Collections Utility Security

Security considerations when working with Collections utility methods.

### 1. Input Validation

```java
public class SecureCollectionsManager {
    private List<String> data = new ArrayList<>();
    
    public void addData(String item) {
        if (item == null || item.trim().isEmpty()) {
            throw new IllegalArgumentException("Item cannot be null or empty");
        }
        data.add(item.trim());
    }
    
    public List<String> getSortedData() {
        List<String> sortedData = new ArrayList<>(data);
        Collections.sort(sortedData);
        return Collections.unmodifiableList(sortedData);
    }
    
    public List<String> searchData(String searchTerm) {
        if (searchTerm == null || searchTerm.trim().isEmpty()) {
            throw new IllegalArgumentException("Search term cannot be null or empty");
        }
        
        List<String> sortedData = new ArrayList<>(data);
        Collections.sort(sortedData);
        
        List<String> results = new ArrayList<>();
        for (String item : sortedData) {
            if (item.contains(searchTerm)) {
                results.add(item);
            }
        }
        
        return Collections.unmodifiableList(results);
    }
}
```

### 2. Access Control

```java
public class SecureCollectionsWrapper {
    private List<String> data = new ArrayList<>();
    private Set<String> allowedUsers = new HashSet<>();
    
    public List<String> getSortedData(String user) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        List<String> sortedData = new ArrayList<>(data);
        Collections.sort(sortedData);
        return Collections.unmodifiableList(sortedData);
    }
    
    public void addData(String user, String item) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        data.add(item);
    }
}
```

### 3. Data Encryption

```java
public class EncryptedCollectionsManager {
    private List<String> encryptedData = new ArrayList<>();
    private String encryptionKey = "secret-key";
    
    public void addEncryptedData(String data) {
        String encrypted = encrypt(data, encryptionKey);
        encryptedData.add(encrypted);
    }
    
    public List<String> getSortedDecryptedData() {
        List<String> decryptedData = new ArrayList<>();
        for (String encrypted : encryptedData) {
            decryptedData.add(decrypt(encrypted, encryptionKey));
        }
        
        Collections.sort(decryptedData);
        return Collections.unmodifiableList(decryptedData);
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

Understanding the Collections utility class is crucial for efficient collection manipulation. These utility methods provide powerful tools for sorting, searching, synchronization, and transformation, making collection operations more efficient and maintainable.