# Section 8 – Iterator and Iteration

## 8.1 Iterator Concepts

Iterators are objects that provide a way to traverse through collections in a standardized manner, regardless of the underlying collection implementation. Understanding iterator concepts is fundamental to effective collection manipulation.

### What are Iterators?

An iterator is an object that enables you to traverse through a collection, providing methods to:
- Check if there are more elements
- Get the next element
- Remove the current element (in some cases)
- Navigate through the collection in a controlled manner

### Key Characteristics of Iterators

#### 1. Standardized Interface
- Common interface across all collections
- Consistent behavior regardless of implementation
- Easy to use and understand

#### 2. One-Way Traversal
- Most iterators move in one direction
- Cannot go backwards (except ListIterator)
- Efficient for sequential processing

#### 3. Safe Modification
- Some iterators allow safe removal during iteration
- Prevents concurrent modification exceptions
- Controlled modification of collections

### Iterator Design Patterns

#### 1. Iterator Pattern
- Provides a way to access elements of a collection
- Hides the underlying implementation
- Supports multiple traversal algorithms

#### 2. Fail-Fast vs Fail-Safe
- **Fail-Fast**: Throws exception on concurrent modification
- **Fail-Safe**: Continues iteration even with modifications

### Real-World Analogy: Reading a Book

Think of iterators as different ways to read a book:

- **Basic Iterator**: Like reading page by page from beginning to end
- **ListIterator**: Like being able to go back and forth, bookmark pages, and make notes
- **Enhanced for Loop**: Like having someone read the book to you automatically
- **Stream API**: Like having a smart assistant that can filter, transform, and process the content as you read

## 8.2 Iterator Interface

The Iterator interface is the foundation of iteration in the Collection Framework, providing basic methods for traversing collections.

### Core Methods

```java
public interface Iterator<E> {
    boolean hasNext();
    E next();
    void remove();
}
```

### Understanding Iterator Operations

#### 1. Basic Iteration
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    System.out.println(name);
}
// Output:
// Alice
// Bob
// Charlie
```

#### 2. Safe Removal During Iteration
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");
names.add("David");

Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.startsWith("B")) {
        iterator.remove(); // Safe removal during iteration
    }
}

System.out.println("After removal: " + names); // [Alice, Charlie, David]
```

#### 3. Error Handling
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");

Iterator<String> iterator = names.iterator();
try {
    while (iterator.hasNext()) {
        String name = iterator.next();
        System.out.println(name);
    }
} catch (NoSuchElementException e) {
    System.out.println("No more elements");
}
```

### Real-World Example: Data Processing
```java
public class DataProcessor {
    private List<String> data = new ArrayList<>();
    
    public void addData(String item) {
        data.add(item);
    }
    
    public void processData() {
        Iterator<String> iterator = data.iterator();
        while (iterator.hasNext()) {
            String item = iterator.next();
            
            // Process the item
            if (isValid(item)) {
                processItem(item);
            } else {
                // Remove invalid items
                iterator.remove();
                System.out.println("Removed invalid item: " + item);
            }
        }
    }
    
    private boolean isValid(String item) {
        return item != null && !item.trim().isEmpty();
    }
    
    private void processItem(String item) {
        System.out.println("Processing: " + item);
        // Actual processing logic here
    }
    
    public List<String> getData() {
        return new ArrayList<>(data);
    }
}
```

## 8.3 ListIterator

ListIterator extends Iterator and provides bidirectional traversal and additional operations for List implementations.

### Core Methods

```java
public interface ListIterator<E> extends Iterator<E> {
    // Forward operations
    boolean hasNext();
    E next();
    int nextIndex();
    
    // Backward operations
    boolean hasPrevious();
    E previous();
    int previousIndex();
    
    // Modification operations
    void remove();
    void set(E e);
    void add(E e);
}
```

### Understanding ListIterator Operations

#### 1. Forward Iteration
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

ListIterator<String> iterator = names.listIterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    int index = iterator.nextIndex() - 1;
    System.out.println("Index " + index + ": " + name);
}
// Output:
// Index 0: Alice
// Index 1: Bob
// Index 2: Charlie
```

#### 2. Backward Iteration
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

ListIterator<String> iterator = names.listIterator(names.size());
while (iterator.hasPrevious()) {
    String name = iterator.previous();
    int index = iterator.previousIndex() + 1;
    System.out.println("Index " + index + ": " + name);
}
// Output:
// Index 2: Charlie
// Index 1: Bob
// Index 0: Alice
```

#### 3. Bidirectional Iteration
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

ListIterator<String> iterator = names.listIterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.equals("Bob")) {
        // Go back to previous element
        iterator.previous();
        String previousName = iterator.previous();
        System.out.println("Previous: " + previousName);
        iterator.next(); // Go forward again
        iterator.next(); // Skip Bob
    }
}
```

#### 4. Modification Operations
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

ListIterator<String> iterator = names.listIterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.equals("Bob")) {
        iterator.set("Bobby"); // Replace current element
        iterator.add("New Item"); // Add after current element
    }
}

System.out.println("After modification: " + names); // [Alice, Bobby, New Item, Charlie]
```

### Real-World Example: Text Editor
```java
public class TextEditor {
    private List<String> lines = new ArrayList<>();
    private int cursorPosition = 0;
    
    public void addLine(String line) {
        lines.add(line);
    }
    
    public void insertLineAt(int position, String line) {
        if (position >= 0 && position <= lines.size()) {
            lines.add(position, line);
        }
    }
    
    public void replaceLine(int position, String newLine) {
        if (position >= 0 && position < lines.size()) {
            lines.set(position, newLine);
        }
    }
    
    public void removeLine(int position) {
        if (position >= 0 && position < lines.size()) {
            lines.remove(position);
        }
    }
    
    public void navigateForward() {
        if (cursorPosition < lines.size() - 1) {
            cursorPosition++;
        }
    }
    
    public void navigateBackward() {
        if (cursorPosition > 0) {
            cursorPosition--;
        }
    }
    
    public String getCurrentLine() {
        if (cursorPosition >= 0 && cursorPosition < lines.size()) {
            return lines.get(cursorPosition);
        }
        return null;
    }
    
    public void printAllLines() {
        ListIterator<String> iterator = lines.listIterator();
        int lineNumber = 0;
        while (iterator.hasNext()) {
            String line = iterator.next();
            String marker = (lineNumber == cursorPosition) ? " -> " : "    ";
            System.out.println(marker + (lineNumber + 1) + ": " + line);
            lineNumber++;
        }
    }
    
    public int getLineCount() {
        return lines.size();
    }
    
    public int getCursorPosition() {
        return cursorPosition;
    }
}
```

## 8.4 Enhanced for Loop

The enhanced for loop (for-each loop) provides a simplified way to iterate through collections and arrays.

### Syntax and Usage

```java
// Basic syntax
for (ElementType element : collection) {
    // Process element
}
```

### Understanding Enhanced for Loop

#### 1. Basic Usage
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

// Enhanced for loop
for (String name : names) {
    System.out.println(name);
}
// Output:
// Alice
// Bob
// Charlie
```

#### 2. Array Iteration
```java
String[] names = {"Alice", "Bob", "Charlie"};

// Enhanced for loop with arrays
for (String name : names) {
    System.out.println(name);
}
// Output:
// Alice
// Bob
// Charlie
```

#### 3. Map Iteration
```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Alice", 25);
ages.put("Bob", 30);
ages.put("Charlie", 35);

// Iterate through keys
for (String name : ages.keySet()) {
    System.out.println(name + ": " + ages.get(name));
}

// Iterate through values
for (Integer age : ages.values()) {
    System.out.println("Age: " + age);
}

// Iterate through entries
for (Map.Entry<String, Integer> entry : ages.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

#### 4. Limitations
```java
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

// Cannot modify collection during iteration
for (String name : names) {
    if (name.startsWith("B")) {
        // names.remove(name); // ConcurrentModificationException
    }
}

// Cannot access index
for (String name : names) {
    // int index = names.indexOf(name); // Inefficient
    System.out.println(name);
}
```

### Real-World Example: Data Analysis
```java
public class DataAnalyzer {
    private List<Double> numbers = new ArrayList<>();
    
    public void addNumber(double number) {
        numbers.add(number);
    }
    
    public double calculateSum() {
        double sum = 0.0;
        for (double number : numbers) {
            sum += number;
        }
        return sum;
    }
    
    public double calculateAverage() {
        if (numbers.isEmpty()) {
            return 0.0;
        }
        return calculateSum() / numbers.size();
    }
    
    public double findMaximum() {
        double max = Double.NEGATIVE_INFINITY;
        for (double number : numbers) {
            if (number > max) {
                max = number;
            }
        }
        return max;
    }
    
    public double findMinimum() {
        double min = Double.POSITIVE_INFINITY;
        for (double number : numbers) {
            if (number < min) {
                min = number;
            }
        }
        return min;
    }
    
    public List<Double> getNumbersAbove(double threshold) {
        List<Double> aboveThreshold = new ArrayList<>();
        for (double number : numbers) {
            if (number > threshold) {
                aboveThreshold.add(number);
            }
        }
        return aboveThreshold;
    }
    
    public void printStatistics() {
        System.out.println("Count: " + numbers.size());
        System.out.println("Sum: " + calculateSum());
        System.out.println("Average: " + calculateAverage());
        System.out.println("Maximum: " + findMaximum());
        System.out.println("Minimum: " + findMinimum());
    }
}
```

## 8.5 Stream API

The Stream API provides a functional approach to processing collections, offering powerful operations for filtering, mapping, and reducing data.

### Core Concepts

#### 1. Stream Creation
```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

// Create stream from collection
Stream<String> stream = names.stream();

// Create stream from array
Stream<String> arrayStream = Arrays.stream(new String[]{"Alice", "Bob"});

// Create stream from values
Stream<String> valueStream = Stream.of("Alice", "Bob", "Charlie");
```

#### 2. Intermediate Operations
```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

// Filter
Stream<String> filtered = names.stream()
    .filter(name -> name.length() > 3);

// Map
Stream<String> mapped = names.stream()
    .map(String::toUpperCase);

// Sorted
Stream<String> sorted = names.stream()
    .sorted();

// Distinct
Stream<String> distinct = names.stream()
    .distinct();
```

#### 3. Terminal Operations
```java
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

// Collect
List<String> result = names.stream()
    .filter(name -> name.length() > 3)
    .collect(Collectors.toList());

// ForEach
names.stream()
    .filter(name -> name.length() > 3)
    .forEach(System.out::println);

// Count
long count = names.stream()
    .filter(name -> name.length() > 3)
    .count();

// AnyMatch
boolean anyMatch = names.stream()
    .anyMatch(name -> name.startsWith("A"));

// AllMatch
boolean allMatch = names.stream()
    .allMatch(name -> name.length() > 2);

// NoneMatch
boolean noneMatch = names.stream()
    .noneMatch(name -> name.length() < 2);
```

### Understanding Stream Operations

#### 1. Filtering and Mapping
```java
List<Person> people = Arrays.asList(
    new Person("Alice", 25),
    new Person("Bob", 30),
    new Person("Charlie", 35),
    new Person("David", 28)
);

// Filter and map
List<String> adultNames = people.stream()
    .filter(person -> person.getAge() >= 30)
    .map(Person::getName)
    .collect(Collectors.toList());

System.out.println("Adult names: " + adultNames); // [Bob, Charlie]
```

#### 2. Reduction Operations
```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// Sum
int sum = numbers.stream()
    .reduce(0, Integer::sum);

// Product
int product = numbers.stream()
    .reduce(1, (a, b) -> a * b);

// Maximum
Optional<Integer> max = numbers.stream()
    .reduce(Integer::max);

// Minimum
Optional<Integer> min = numbers.stream()
    .reduce(Integer::min);
```

#### 3. Grouping and Partitioning
```java
List<Person> people = Arrays.asList(
    new Person("Alice", 25),
    new Person("Bob", 30),
    new Person("Charlie", 35),
    new Person("David", 28)
);

// Group by age range
Map<String, List<Person>> grouped = people.stream()
    .collect(Collectors.groupingBy(person -> 
        person.getAge() < 30 ? "Young" : "Old"));

// Partition by age
Map<Boolean, List<Person>> partitioned = people.stream()
    .collect(Collectors.partitioningBy(person -> person.getAge() >= 30));
```

### Real-World Example: Employee Management
```java
public class EmployeeManager {
    private List<Employee> employees = new ArrayList<>();
    
    public void addEmployee(Employee employee) {
        employees.add(employee);
    }
    
    public List<Employee> getEmployeesByDepartment(String department) {
        return employees.stream()
            .filter(emp -> emp.getDepartment().equals(department))
            .collect(Collectors.toList());
    }
    
    public List<Employee> getEmployeesAboveSalary(double salary) {
        return employees.stream()
            .filter(emp -> emp.getSalary() > salary)
            .collect(Collectors.toList());
    }
    
    public double getAverageSalary() {
        return employees.stream()
            .mapToDouble(Employee::getSalary)
            .average()
            .orElse(0.0);
    }
    
    public Map<String, List<Employee>> getEmployeesByDepartment() {
        return employees.stream()
            .collect(Collectors.groupingBy(Employee::getDepartment));
    }
    
    public Map<String, Double> getAverageSalaryByDepartment() {
        return employees.stream()
            .collect(Collectors.groupingBy(
                Employee::getDepartment,
                Collectors.averagingDouble(Employee::getSalary)
            ));
    }
    
    public List<String> getTopEarners(int count) {
        return employees.stream()
            .sorted((e1, e2) -> Double.compare(e2.getSalary(), e1.getSalary()))
            .limit(count)
            .map(Employee::getName)
            .collect(Collectors.toList());
    }
    
    public static class Employee {
        private String name;
        private String department;
        private double salary;
        
        public Employee(String name, String department, double salary) {
            this.name = name;
            this.department = department;
            this.salary = salary;
        }
        
        // Getters
        public String getName() { return name; }
        public String getDepartment() { return department; }
        public double getSalary() { return salary; }
        
        @Override
        public String toString() {
            return "Employee{name='" + name + "', department='" + department + "', salary=" + salary + "}";
        }
    }
}
```

## 8.6 Iterator Best Practices

Following best practices ensures efficient and maintainable code when working with iterators.

### 1. Choose the Right Iteration Method

#### Use Enhanced for Loop When:
- Simple iteration needed
- No modification during iteration
- Read-only operations

```java
// Good: Simple iteration
for (String name : names) {
    System.out.println(name);
}
```

#### Use Iterator When:
- Modification during iteration needed
- More control required
- Complex iteration logic

```java
// Good: Modification during iteration
Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.startsWith("A")) {
        iterator.remove();
    }
}
```

#### Use ListIterator When:
- Bidirectional traversal needed
- Index-based operations required
- List-specific operations needed

```java
// Good: Bidirectional traversal
ListIterator<String> iterator = names.listIterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.equals("Bob")) {
        iterator.set("Bobby");
    }
}
```

#### Use Stream API When:
- Functional operations needed
- Complex data processing required
- Parallel processing needed

```java
// Good: Functional operations
List<String> result = names.stream()
    .filter(name -> name.length() > 3)
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

### 2. Handle Exceptions Properly

```java
// Good: Handle exceptions
try {
    Iterator<String> iterator = names.iterator();
    while (iterator.hasNext()) {
        String name = iterator.next();
        System.out.println(name);
    }
} catch (NoSuchElementException e) {
    System.out.println("No more elements");
} catch (ConcurrentModificationException e) {
    System.out.println("Collection was modified during iteration");
}
```

### 3. Avoid Concurrent Modification

```java
// Bad: Concurrent modification
for (String name : names) {
    if (name.startsWith("A")) {
        names.remove(name); // ConcurrentModificationException
    }
}

// Good: Use iterator for safe removal
Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.startsWith("A")) {
        iterator.remove(); // Safe removal
    }
}
```

### 4. Use Appropriate Data Structures

```java
// Good: Use appropriate collection for iteration pattern
List<String> names = new ArrayList<>(); // Good for random access
for (int i = 0; i < names.size(); i++) {
    System.out.println(names.get(i));
}

// Good: Use LinkedList for frequent insertions/deletions
List<String> names = new LinkedList<>();
ListIterator<String> iterator = names.listIterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.equals("Bob")) {
        iterator.add("New Item"); // Efficient insertion
    }
}
```

## 8.7 Iterator Testing

Comprehensive testing ensures iterators work correctly and meet performance requirements.

### 1. Unit Testing

```java
@Test
public void testIteratorOperations() {
    List<String> names = new ArrayList<>();
    names.add("Alice");
    names.add("Bob");
    names.add("Charlie");
    
    Iterator<String> iterator = names.iterator();
    
    // Test hasNext
    assertTrue(iterator.hasNext());
    
    // Test next
    assertEquals("Alice", iterator.next());
    assertEquals("Bob", iterator.next());
    assertEquals("Charlie", iterator.next());
    
    // Test end of iteration
    assertFalse(iterator.hasNext());
    
    // Test NoSuchElementException
    assertThrows(NoSuchElementException.class, () -> iterator.next());
}
```

### 2. Performance Testing

```java
@Test
public void testIteratorPerformance() {
    List<String> names = new ArrayList<>();
    for (int i = 0; i < 100000; i++) {
        names.add("Name" + i);
    }
    
    // Test iterator performance
    long startTime = System.currentTimeMillis();
    Iterator<String> iterator = names.iterator();
    while (iterator.hasNext()) {
        String name = iterator.next();
    }
    long iteratorTime = System.currentTimeMillis() - startTime;
    
    // Test enhanced for loop performance
    startTime = System.currentTimeMillis();
    for (String name : names) {
        // Process name
    }
    long forEachTime = System.currentTimeMillis() - startTime;
    
    System.out.println("Iterator time: " + iteratorTime + "ms");
    System.out.println("For-each time: " + forEachTime + "ms");
    
    assertTrue(iteratorTime < 1000); // Should complete within 1 second
    assertTrue(forEachTime < 1000);  // Should complete within 1 second
}
```

### 3. Concurrent Modification Testing

```java
@Test
public void testConcurrentModification() {
    List<String> names = new ArrayList<>();
    names.add("Alice");
    names.add("Bob");
    names.add("Charlie");
    
    // Test concurrent modification exception
    Iterator<String> iterator = names.iterator();
    names.add("David"); // Modify collection during iteration
    
    assertThrows(ConcurrentModificationException.class, () -> {
        while (iterator.hasNext()) {
            iterator.next();
        }
    });
}
```

## 8.8 Iterator Performance

Understanding performance characteristics helps in choosing the right iteration method and optimizing code.

### Performance Comparison

| Iteration Method | ArrayList | LinkedList | HashSet | TreeSet |
|------------------|-----------|------------|---------|---------|
| Iterator | O(n) | O(n) | O(n) | O(n) |
| Enhanced for Loop | O(n) | O(n) | O(n) | O(n) |
| Index-based | O(n) | O(n²) | N/A | N/A |
| Stream API | O(n) | O(n) | O(n) | O(n) |

### Memory Usage

```java
// Iterator memory usage
Iterator<String> iterator = names.iterator();
// Memory: iterator object + references

// Enhanced for loop memory usage
for (String name : names) {
    // Memory: loop variable + references
}

// Stream API memory usage
names.stream()
    .filter(name -> name.length() > 3)
    .collect(Collectors.toList());
// Memory: stream objects + intermediate collections
```

### Performance Optimization Tips

#### 1. Use Appropriate Iteration Method
```java
// Good: Use enhanced for loop for simple iteration
for (String name : names) {
    System.out.println(name);
}

// Good: Use iterator for modification
Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.startsWith("A")) {
        iterator.remove();
    }
}
```

#### 2. Avoid Unnecessary Operations
```java
// Bad: Unnecessary operations
for (String name : names) {
    if (name.length() > 3) {
        System.out.println(name.toUpperCase());
    }
}

// Good: Use stream API for complex operations
names.stream()
    .filter(name -> name.length() > 3)
    .map(String::toUpperCase)
    .forEach(System.out::println);
```

#### 3. Use Parallel Streams for Large Collections
```java
// Good: Use parallel streams for large collections
List<String> result = names.parallelStream()
    .filter(name -> name.length() > 3)
    .map(String::toUpperCase)
    .collect(Collectors.toList());
```

## 8.9 Iterator Troubleshooting

Common issues and solutions when working with iterators.

### 1. ConcurrentModificationException

```java
// Problem: Concurrent modification
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");

for (String name : names) {
    if (name.startsWith("A")) {
        names.remove(name); // ConcurrentModificationException
    }
}

// Solution: Use iterator for safe removal
Iterator<String> iterator = names.iterator();
while (iterator.hasNext()) {
    String name = iterator.next();
    if (name.startsWith("A")) {
        iterator.remove(); // Safe removal
    }
}
```

### 2. NoSuchElementException

```java
// Problem: Calling next() without checking hasNext()
Iterator<String> iterator = names.iterator();
String name = iterator.next(); // NoSuchElementException if empty

// Solution: Always check hasNext()
if (iterator.hasNext()) {
    String name = iterator.next();
}
```

### 3. Performance Issues

```java
// Problem: Using wrong iteration method
List<String> names = new LinkedList<>();
for (int i = 0; i < names.size(); i++) {
    String name = names.get(i); // O(n) per operation
}

// Solution: Use appropriate iteration method
for (String name : names) {
    System.out.println(name); // O(1) per operation
}
```

### 4. Memory Issues

```java
// Problem: Not closing streams
Stream<String> stream = names.stream();
// Process stream
// stream is not closed

// Solution: Use try-with-resources or collect immediately
List<String> result = names.stream()
    .filter(name -> name.length() > 3)
    .collect(Collectors.toList());
```

## 8.10 Iterator Security

Security considerations when working with iterators.

### 1. Input Validation

```java
public class SecureIteratorManager {
    private List<String> data = new ArrayList<>();
    
    public void addData(String item) {
        if (item == null || item.trim().isEmpty()) {
            throw new IllegalArgumentException("Item cannot be null or empty");
        }
        data.add(item.trim());
    }
    
    public void processData() {
        Iterator<String> iterator = data.iterator();
        while (iterator.hasNext()) {
            String item = iterator.next();
            
            // Validate item before processing
            if (isValidItem(item)) {
                processItem(item);
            } else {
                iterator.remove();
                System.out.println("Removed invalid item: " + item);
            }
        }
    }
    
    private boolean isValidItem(String item) {
        // Additional validation logic
        return item != null && !item.contains("<script>");
    }
    
    private void processItem(String item) {
        System.out.println("Processing: " + item);
        // Actual processing logic here
    }
}
```

### 2. Access Control

```java
public class SecureIteratorWrapper {
    private List<String> data = new ArrayList<>();
    private Set<String> allowedUsers = new HashSet<>();
    
    public Iterator<String> getIterator(String user) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        
        return data.iterator();
    }
    
    public void processData(String user) {
        Iterator<String> iterator = getIterator(user);
        while (iterator.hasNext()) {
            String item = iterator.next();
            System.out.println("Processing: " + item);
        }
    }
}
```

### 3. Data Encryption

```java
public class EncryptedIteratorManager {
    private List<String> encryptedData = new ArrayList<>();
    private String encryptionKey = "secret-key";
    
    public void addEncryptedData(String data) {
        String encrypted = encrypt(data, encryptionKey);
        encryptedData.add(encrypted);
    }
    
    public void processDecryptedData() {
        Iterator<String> iterator = encryptedData.iterator();
        while (iterator.hasNext()) {
            String encrypted = iterator.next();
            String decrypted = decrypt(encrypted, encryptionKey);
            System.out.println("Processing: " + decrypted);
        }
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

Understanding iterators and iteration is crucial for effective collection manipulation. Each iteration method has its strengths and weaknesses, and choosing the right one depends on your specific use case, performance requirements, and whether you need to modify the collection during iteration.