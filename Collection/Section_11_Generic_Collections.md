# Section 11 – Generic Collections

## 11.1 Generic Collection Concepts

Generic collections provide type safety at compile time, allowing you to specify the type of elements a collection will contain. Understanding generics is crucial for writing robust, maintainable Java code.

### What are Generic Collections?

Generic collections are collections that use Java's generics feature to provide:
- **Type Safety**: Compile-time type checking
- **Elimination of Casting**: No need for explicit type casting
- **Better Code Readability**: Clear indication of collection element types
- **Reduced Runtime Errors**: Prevents ClassCastException at runtime

### Key Characteristics of Generic Collections

#### 1. Type Parameters
- Use angle brackets `<T>` to specify element types
- Can use multiple type parameters `<K, V>`
- Support bounded type parameters `<T extends Comparable<T>>`

#### 2. Type Erasure
- Generic type information is removed at runtime
- Compiler inserts necessary casts
- No performance overhead at runtime

#### 3. Wildcards
- `?` represents unknown types
- `? extends T` represents upper bounded wildcards
- `? super T` represents lower bounded wildcards

### Common Generic Collection Patterns

| Pattern | Syntax | Purpose |
|---------|--------|---------|
| Basic Generic | `List<String>` | Type-safe list |
| Bounded Generic | `List<? extends Number>` | Upper bounded |
| Lower Bounded | `List<? super String>` | Lower bounded |
| Multiple Types | `Map<String, Integer>` | Key-value pairs |

### Real-World Analogy: Labeled Containers

Think of generic collections as labeled containers:

- **Non-generic collections**: Like unlabeled boxes where you have to guess what's inside
- **Generic collections**: Like clearly labeled boxes that tell you exactly what type of items are inside
- **Type parameters**: Like the labels on the boxes that specify the contents
- **Wildcards**: Like "any type" labels that can hold different types of items

## 11.2 Type Safety

Type safety in generic collections ensures that only compatible types can be stored and retrieved, preventing runtime errors.

### Understanding Type Safety

#### 1. Compile-Time Type Checking
```java
// Generic collection with type safety
List<String> names = new ArrayList<>();
names.add("Alice");
names.add("Bob");
names.add("Charlie");

// This will cause a compile error
// names.add(123); // Compile error: incompatible types

// No casting needed when retrieving
String first = names.get(0); // Type-safe retrieval
System.out.println("First name: " + first);
```

#### 2. Runtime Type Safety
```java
// Non-generic collection (unsafe)
List rawList = new ArrayList();
rawList.add("Alice");
rawList.add(123); // No compile error, but dangerous

// This will throw ClassCastException at runtime
String name = (String) rawList.get(1); // Runtime error

// Generic collection (safe)
List<String> safeList = new ArrayList<>();
safeList.add("Alice");
// safeList.add(123); // Compile error prevents this
String safeName = safeList.get(0); // Always safe
```

#### 3. Type Safety with Custom Objects
```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Getters and setters
    public String getName() { return name; }
    public int getAge() { return age; }
}

// Type-safe collection of Person objects
List<Person> people = new ArrayList<>();
people.add(new Person("Alice", 25));
people.add(new Person("Bob", 30));

// Type-safe retrieval
Person firstPerson = people.get(0);
System.out.println("First person: " + firstPerson.getName());
```

### Real-World Example: Type-Safe Data Manager
```java
public class TypeSafeDataManager<T> {
    private List<T> data = new ArrayList<>();
    private Class<T> type;
    
    public TypeSafeDataManager(Class<T> type) {
        this.type = type;
    }
    
    public void addData(T item) {
        if (item == null) {
            throw new IllegalArgumentException("Item cannot be null");
        }
        data.add(item);
    }
    
    public T getData(int index) {
        if (index < 0 || index >= data.size()) {
            throw new IndexOutOfBoundsException("Invalid index: " + index);
        }
        return data.get(index);
    }
    
    public List<T> getAllData() {
        return new ArrayList<>(data);
    }
    
    public boolean containsData(T item) {
        return data.contains(item);
    }
    
    public int getDataCount() {
        return data.size();
    }
    
    public Class<T> getType() {
        return type;
    }
    
    public void clearData() {
        data.clear();
    }
}

// Usage examples
TypeSafeDataManager<String> stringManager = new TypeSafeDataManager<>(String.class);
stringManager.addData("Hello");
stringManager.addData("World");

TypeSafeDataManager<Integer> intManager = new TypeSafeDataManager<>(Integer.class);
intManager.addData(42);
intManager.addData(100);
```

## 11.3 Generic Wildcards

Generic wildcards provide flexibility when working with generic types, allowing you to work with unknown or partially known types.

### Understanding Wildcards

#### 1. Unbounded Wildcards
```java
// Unbounded wildcard - can hold any type
List<?> unknownList = new ArrayList<String>();
unknownList = new ArrayList<Integer>();
unknownList = new ArrayList<Object>();

// Can only read as Object
Object item = unknownList.get(0);

// Cannot add elements (except null)
// unknownList.add("Hello"); // Compile error
unknownList.add(null); // OK
```

#### 2. Upper Bounded Wildcards
```java
// Upper bounded wildcard - can hold Number or its subtypes
List<? extends Number> numbers = new ArrayList<Integer>();
numbers = new ArrayList<Double>();
numbers = new ArrayList<Long>();

// Can read as Number
Number num = numbers.get(0);

// Cannot add elements (except null)
// numbers.add(42); // Compile error
numbers.add(null); // OK
```

#### 3. Lower Bounded Wildcards
```java
// Lower bounded wildcard - can hold String or its supertypes
List<? super String> strings = new ArrayList<String>();
strings = new ArrayList<Object>();
strings = new ArrayList<CharSequence>();

// Can add String or its subtypes
strings.add("Hello");
strings.add("World");

// Can read as Object
Object obj = strings.get(0);
```

### Real-World Example: Generic Data Processor
```java
public class GenericDataProcessor {
    
    // Process any type of data
    public static void processData(List<?> data) {
        System.out.println("Processing " + data.size() + " items");
        for (Object item : data) {
            System.out.println("Item: " + item);
        }
    }
    
    // Process numbers only
    public static double sumNumbers(List<? extends Number> numbers) {
        double sum = 0.0;
        for (Number num : numbers) {
            sum += num.doubleValue();
        }
        return sum;
    }
    
    // Add strings to any collection that can hold strings
    public static void addStrings(List<? super String> strings, String... items) {
        for (String item : items) {
            strings.add(item);
        }
    }
    
    // Copy data from source to destination
    public static <T> void copyData(List<? extends T> source, List<? super T> destination) {
        for (T item : source) {
            destination.add(item);
        }
    }
    
    // Find maximum element
    public static <T extends Comparable<T>> T findMax(List<T> list) {
        if (list.isEmpty()) {
            throw new IllegalArgumentException("List is empty");
        }
        
        T max = list.get(0);
        for (T item : list) {
            if (item.compareTo(max) > 0) {
                max = item;
            }
        }
        return max;
    }
}

// Usage examples
List<Integer> integers = Arrays.asList(1, 2, 3, 4, 5);
List<Double> doubles = Arrays.asList(1.1, 2.2, 3.3, 4.4, 5.5);
List<String> strings = Arrays.asList("Alice", "Bob", "Charlie");

// Process any type
GenericDataProcessor.processData(integers);
GenericDataProcessor.processData(strings);

// Sum numbers
double intSum = GenericDataProcessor.sumNumbers(integers);
double doubleSum = GenericDataProcessor.sumNumbers(doubles);

// Add strings
List<Object> objectList = new ArrayList<>();
GenericDataProcessor.addStrings(objectList, "Hello", "World");

// Copy data
List<Number> numberList = new ArrayList<>();
GenericDataProcessor.copyData(integers, numberList);

// Find maximum
Integer maxInt = GenericDataProcessor.findMax(integers);
String maxString = GenericDataProcessor.findMax(strings);
```

## 11.4 Bounded Generics

Bounded generics restrict the types that can be used as type parameters, providing more specific constraints and enabling more operations.

### Understanding Bounded Generics

#### 1. Upper Bounded Generics
```java
// Upper bounded generic - T must extend Number
public class NumberBox<T extends Number> {
    private T value;
    
    public NumberBox(T value) {
        this.value = value;
    }
    
    public T getValue() {
        return value;
    }
    
    public double getDoubleValue() {
        return value.doubleValue(); // Can call Number methods
    }
    
    public int getIntValue() {
        return value.intValue(); // Can call Number methods
    }
}

// Usage
NumberBox<Integer> intBox = new NumberBox<>(42);
NumberBox<Double> doubleBox = new NumberBox<>(3.14);
// NumberBox<String> stringBox = new NumberBox<>("Hello"); // Compile error
```

#### 2. Multiple Bounds
```java
// Multiple bounds - T must extend Number and implement Comparable
public class ComparableNumberBox<T extends Number & Comparable<T>> {
    private T value;
    
    public ComparableNumberBox(T value) {
        this.value = value;
    }
    
    public T getValue() {
        return value;
    }
    
    public int compareTo(ComparableNumberBox<T> other) {
        return this.value.compareTo(other.value);
    }
    
    public boolean isGreaterThan(ComparableNumberBox<T> other) {
        return this.value.compareTo(other.value) > 0;
    }
}

// Usage
ComparableNumberBox<Integer> intBox1 = new ComparableNumberBox<>(42);
ComparableNumberBox<Integer> intBox2 = new ComparableNumberBox<>(30);
System.out.println("Is greater: " + intBox1.isGreaterThan(intBox2)); // true
```

#### 3. Lower Bounded Generics
```java
// Lower bounded generic - T must be supertype of String
public class StringContainer<T super String> {
    private List<T> items = new ArrayList<>();
    
    public void addItem(T item) {
        items.add(item);
    }
    
    public T getItem(int index) {
        return items.get(index);
    }
    
    public void addString(String str) {
        items.add((T) str); // Safe cast
    }
}

// Usage
StringContainer<Object> container = new StringContainer<>();
container.addString("Hello");
container.addItem("World");
container.addItem(42); // Object can hold anything
```

### Real-World Example: Generic Repository
```java
public class GenericRepository<T, ID> {
    private Map<ID, T> data = new HashMap<>();
    private Class<T> entityType;
    
    public GenericRepository(Class<T> entityType) {
        this.entityType = entityType;
    }
    
    public void save(ID id, T entity) {
        if (entity == null) {
            throw new IllegalArgumentException("Entity cannot be null");
        }
        data.put(id, entity);
    }
    
    public T findById(ID id) {
        return data.get(id);
    }
    
    public List<T> findAll() {
        return new ArrayList<>(data.values());
    }
    
    public void deleteById(ID id) {
        data.remove(id);
    }
    
    public boolean existsById(ID id) {
        return data.containsKey(id);
    }
    
    public long count() {
        return data.size();
    }
    
    public Class<T> getEntityType() {
        return entityType;
    }
}

// Usage examples
GenericRepository<User, Long> userRepository = new GenericRepository<>(User.class);
userRepository.save(1L, new User("Alice", "alice@email.com"));
userRepository.save(2L, new User("Bob", "bob@email.com"));

User user = userRepository.findById(1L);
List<User> allUsers = userRepository.findAll();

GenericRepository<Product, String> productRepository = new GenericRepository<>(Product.class);
productRepository.save("P001", new Product("Laptop", 999.99));
productRepository.save("P002", new Product("Mouse", 29.99));
```

## 11.5 Generic Methods

Generic methods allow you to create methods that can work with different types while maintaining type safety.

### Understanding Generic Methods

#### 1. Basic Generic Methods
```java
public class GenericMethodExample {
    
    // Generic method with type parameter
    public static <T> void printArray(T[] array) {
        for (T item : array) {
            System.out.println(item);
        }
    }
    
    // Generic method with return type
    public static <T> T getFirstElement(List<T> list) {
        if (list.isEmpty()) {
            throw new IllegalArgumentException("List is empty");
        }
        return list.get(0);
    }
    
    // Generic method with multiple type parameters
    public static <T, U> void printPair(T first, U second) {
        System.out.println("First: " + first + ", Second: " + second);
    }
}

// Usage
String[] strings = {"Hello", "World", "Java"};
Integer[] numbers = {1, 2, 3, 4, 5};

GenericMethodExample.printArray(strings);
GenericMethodExample.printArray(numbers);

List<String> stringList = Arrays.asList("Alice", "Bob", "Charlie");
String first = GenericMethodExample.getFirstElement(stringList);

GenericMethodExample.printPair("Hello", 42);
GenericMethodExample.printPair(3.14, "Pi");
```

#### 2. Bounded Generic Methods
```java
public class BoundedGenericMethodExample {
    
    // Upper bounded generic method
    public static <T extends Comparable<T>> T findMax(T[] array) {
        if (array.length == 0) {
            throw new IllegalArgumentException("Array is empty");
        }
        
        T max = array[0];
        for (T item : array) {
            if (item.compareTo(max) > 0) {
                max = item;
            }
        }
        return max;
    }
    
    // Generic method with multiple bounds
    public static <T extends Number & Comparable<T>> T findMaxNumber(T[] array) {
        if (array.length == 0) {
            throw new IllegalArgumentException("Array is empty");
        }
        
        T max = array[0];
        for (T item : array) {
            if (item.compareTo(max) > 0) {
                max = item;
            }
        }
        return max;
    }
    
    // Generic method with wildcards
    public static double sumNumbers(List<? extends Number> numbers) {
        double sum = 0.0;
        for (Number num : numbers) {
            sum += num.doubleValue();
        }
        return sum;
    }
}

// Usage
Integer[] integers = {1, 5, 3, 9, 2};
String[] strings = {"Alice", "Bob", "Charlie"};

Integer maxInt = BoundedGenericMethodExample.findMax(integers);
String maxString = BoundedGenericMethodExample.findMax(strings);

List<Integer> intList = Arrays.asList(1, 2, 3, 4, 5);
List<Double> doubleList = Arrays.asList(1.1, 2.2, 3.3, 4.4, 5.5);

double intSum = BoundedGenericMethodExample.sumNumbers(intList);
double doubleSum = BoundedGenericMethodExample.sumNumbers(doubleList);
```

#### 3. Generic Methods with Constraints
```java
public class ConstrainedGenericMethodExample {
    
    // Generic method that requires specific interface
    public static <T extends Cloneable> T cloneObject(T obj) {
        try {
            return (T) obj.getClass().getMethod("clone").invoke(obj);
        } catch (Exception e) {
            throw new RuntimeException("Failed to clone object", e);
        }
    }
    
    // Generic method with custom constraint
    public static <T> void processItems(List<T> items, Processor<T> processor) {
        for (T item : items) {
            processor.process(item);
        }
    }
    
    // Generic method with type inference
    public static <T> List<T> createList(T... items) {
        List<T> list = new ArrayList<>();
        for (T item : items) {
            list.add(item);
        }
        return list;
    }
}

// Custom interface for processing
interface Processor<T> {
    void process(T item);
}

// Usage
List<String> items = Arrays.asList("Hello", "World", "Java");
ConstrainedGenericMethodExample.processItems(items, item -> 
    System.out.println("Processing: " + item));

List<String> newList = ConstrainedGenericMethodExample.createList("A", "B", "C");
List<Integer> intList = ConstrainedGenericMethodExample.createList(1, 2, 3, 4, 5);
```

### Real-World Example: Generic Data Processor
```java
public class GenericDataProcessor {
    
    // Process any type of data with custom processor
    public static <T> void processData(List<T> data, Processor<T> processor) {
        for (T item : data) {
            processor.process(item);
        }
    }
    
    // Filter data based on predicate
    public static <T> List<T> filterData(List<T> data, Predicate<T> predicate) {
        List<T> result = new ArrayList<>();
        for (T item : data) {
            if (predicate.test(item)) {
                result.add(item);
            }
        }
        return result;
    }
    
    // Transform data using mapper
    public static <T, R> List<R> transformData(List<T> data, Mapper<T, R> mapper) {
        List<R> result = new ArrayList<>();
        for (T item : data) {
            result.add(mapper.map(item));
        }
        return result;
    }
    
    // Reduce data using reducer
    public static <T> T reduceData(List<T> data, T identity, Reducer<T> reducer) {
        T result = identity;
        for (T item : data) {
            result = reducer.reduce(result, item);
        }
        return result;
    }
    
    // Find data based on predicate
    public static <T> Optional<T> findData(List<T> data, Predicate<T> predicate) {
        for (T item : data) {
            if (predicate.test(item)) {
                return Optional.of(item);
            }
        }
        return Optional.empty();
    }
}

// Functional interfaces
interface Processor<T> {
    void process(T item);
}

interface Predicate<T> {
    boolean test(T item);
}

interface Mapper<T, R> {
    R map(T item);
}

interface Reducer<T> {
    T reduce(T accumulator, T item);
}

// Usage examples
List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "David");

// Process data
GenericDataProcessor.processData(names, name -> 
    System.out.println("Hello, " + name));

// Filter data
List<String> longNames = GenericDataProcessor.filterData(names, 
    name -> name.length() > 4);

// Transform data
List<String> upperNames = GenericDataProcessor.transformData(names, 
    String::toUpperCase);

// Reduce data
String concatenated = GenericDataProcessor.reduceData(names, "", 
    (acc, name) -> acc + name + " ");

// Find data
Optional<String> found = GenericDataProcessor.findData(names, 
    name -> name.startsWith("C"));
```

## 11.6 Generic Collection Best Practices

Following best practices ensures efficient and maintainable code when working with generic collections.

### 1. Use Appropriate Type Parameters

#### Use Specific Types When Possible
```java
// Good: Use specific types
List<String> names = new ArrayList<>();
Map<String, Integer> ages = new HashMap<>();

// Bad: Use raw types
List names = new ArrayList();
Map ages = new HashMap();
```

#### Use Wildcards When Appropriate
```java
// Good: Use wildcards for flexibility
public void processNumbers(List<? extends Number> numbers) {
    for (Number num : numbers) {
        System.out.println(num.doubleValue());
    }
}

// Bad: Use specific types when wildcards would be better
public void processNumbers(List<Number> numbers) {
    // Less flexible - can't pass List<Integer>
}
```

### 2. Avoid Raw Types

```java
// Good: Use generic types
List<String> names = new ArrayList<>();
names.add("Alice");
String name = names.get(0); // No casting needed

// Bad: Use raw types
List names = new ArrayList();
names.add("Alice");
String name = (String) names.get(0); // Requires casting
```

### 3. Use Bounded Types When Appropriate

```java
// Good: Use bounded types for specific operations
public static <T extends Comparable<T>> T findMax(List<T> list) {
    // Can use compareTo method
}

// Bad: Use unbounded types when bounds would be better
public static <T> T findMax(List<T> list) {
    // Cannot use compareTo method
}
```

### 4. Use Generic Methods for Reusability

```java
// Good: Use generic methods
public static <T> void swap(List<T> list, int i, int j) {
    T temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}

// Bad: Use specific types when generics would be better
public static void swapStrings(List<String> list, int i, int j) {
    // Only works with String lists
}
```

## 11.7 Generic Collection Testing

Comprehensive testing ensures generic collections work correctly and meet type safety requirements.

### 1. Unit Testing

```java
@Test
public void testGenericListOperations() {
    List<String> names = new ArrayList<>();
    names.add("Alice");
    names.add("Bob");
    
    assertEquals(2, names.size());
    assertEquals("Alice", names.get(0));
    assertEquals("Bob", names.get(1));
    
    // Test type safety
    // names.add(123); // This should cause compile error
}

@Test
public void testGenericMapOperations() {
    Map<String, Integer> ages = new HashMap<>();
    ages.put("Alice", 25);
    ages.put("Bob", 30);
    
    assertEquals(2, ages.size());
    assertEquals(Integer.valueOf(25), ages.get("Alice"));
    assertEquals(Integer.valueOf(30), ages.get("Bob"));
}
```

### 2. Type Safety Testing

```java
@Test
public void testTypeSafety() {
    List<String> names = new ArrayList<>();
    names.add("Alice");
    
    // Test that only strings can be added
    try {
        // This should cause compile error
        // names.add(123);
        fail("Should not allow non-string elements");
    } catch (Exception e) {
        // Expected
    }
    
    // Test that retrieval is type-safe
    String name = names.get(0);
    assertNotNull(name);
    assertTrue(name instanceof String);
}
```

### 3. Generic Method Testing

```java
@Test
public void testGenericMethods() {
    List<String> names = Arrays.asList("Alice", "Bob", "Charlie");
    
    // Test generic method
    String first = GenericMethodExample.getFirstElement(names);
    assertEquals("Alice", first);
    
    // Test bounded generic method
    Integer[] numbers = {1, 5, 3, 9, 2};
    Integer max = BoundedGenericMethodExample.findMax(numbers);
    assertEquals(Integer.valueOf(9), max);
}
```

## 11.8 Generic Collection Performance

Understanding performance characteristics helps in choosing the right generic collection and optimizing code.

### Performance Comparison

| Operation | ArrayList<String> | ArrayList<Object> | ArrayList (raw) |
|-----------|-------------------|-------------------|-----------------|
| add() | O(1) | O(1) | O(1) |
| get() | O(1) | O(1) | O(1) |
| remove() | O(n) | O(n) | O(n) |
| Type Safety | Yes | Yes | No |

### Memory Usage

```java
// Generic collections memory usage
List<String> genericList = new ArrayList<>();
// Memory: Same as non-generic, no additional overhead

// Raw collections memory usage
List rawList = new ArrayList();
// Memory: Same as generic, but less type safety
```

### Performance Optimization Tips

#### 1. Use Appropriate Generic Types
```java
// Good: Use specific generic types
List<String> names = new ArrayList<>();
Map<String, Integer> ages = new HashMap<>();

// Bad: Use Object types when specific types would be better
List<Object> names = new ArrayList<>();
Map<Object, Object> ages = new HashMap<>();
```

#### 2. Use Generic Methods for Reusability
```java
// Good: Use generic methods
public static <T> void swap(List<T> list, int i, int j) {
    T temp = list.get(i);
    list.set(i, list.get(j));
    list.set(j, temp);
}

// Bad: Use specific methods when generics would be better
public static void swapStrings(List<String> list, int i, int j) {
    // Only works with String lists
}
```

## 11.9 Generic Collection Troubleshooting

Common issues and solutions when working with generic collections.

### 1. Type Erasure Issues

```java
// Problem: Type information lost at runtime
List<String> names = new ArrayList<>();
// if (names instanceof List<String>) { // Compile error
//     // This doesn't work
// }

// Solution: Use raw types for runtime checks
if (names instanceof List) {
    // This works
}
```

### 2. Wildcard Issues

```java
// Problem: Cannot add to wildcard collections
List<? extends Number> numbers = new ArrayList<Integer>();
// numbers.add(42); // Compile error

// Solution: Use appropriate wildcards or methods
public static void addNumber(List<? super Integer> numbers, Integer num) {
    numbers.add(num); // This works
}
```

### 3. Generic Method Issues

```java
// Problem: Type inference issues
// List<String> names = GenericMethodExample.createList(); // Compile error

// Solution: Provide type information
List<String> names = GenericMethodExample.<String>createList();
// Or
List<String> names = GenericMethodExample.createList("Hello", "World");
```

## 11.10 Generic Collection Security

Security considerations when working with generic collections.

### 1. Input Validation

```java
public class SecureGenericManager<T> {
    private List<T> data = new ArrayList<>();
    private Class<T> type;
    
    public SecureGenericManager(Class<T> type) {
        this.type = type;
    }
    
    public void addData(T item) {
        if (item == null) {
            throw new IllegalArgumentException("Item cannot be null");
        }
        
        if (!type.isInstance(item)) {
            throw new IllegalArgumentException("Item must be of type " + type.getName());
        }
        
        data.add(item);
    }
    
    public T getData(int index) {
        if (index < 0 || index >= data.size()) {
            throw new IndexOutOfBoundsException("Invalid index: " + index);
        }
        return data.get(index);
    }
}
```

### 2. Access Control

```java
public class SecureGenericWrapper<T> {
    private List<T> data = new ArrayList<>();
    private Set<String> allowedUsers = new HashSet<>();
    
    public List<T> getData(String user) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        return new ArrayList<>(data);
    }
    
    public void addData(String user, T item) {
        if (!allowedUsers.contains(user)) {
            throw new SecurityException("User not authorized");
        }
        data.add(item);
    }
}
```

Understanding generic collections is crucial for writing type-safe, maintainable Java code. Generics provide compile-time type checking, eliminate the need for casting, and make code more readable and robust.